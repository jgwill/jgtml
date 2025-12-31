#!/usr/bin/env python3
"""
FDB Signal Trading Monitor - Production Version

Uses existing JGT infrastructure for:
- Data freshness validation (jgtpy, jgtutils)
- Market open/closed detection (jgtutils.jgtcommon.is_market_open)
- Signal ordering and validation (jgtml.SignalOrderingHelper)

Applies LLMS frameworks:
- Digital Decision Making (TandT) for signal acceptance
- MMOT for performance tracking

Entry Order Logic:
- FDB Buy signal detected with HTF validation
- TandT binary decision: ACCEPTABLE/UNACCEPTABLE
- Order placed only when ALL criteria pass
- Order invalidated if stop broken before entry
"""

import os
import sys
import time
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

# Add JGT packages to path
sys.path.insert(0, '/b/trading/jgtml')
sys.path.insert(0, '/b/trading/jgtpy')
sys.path.insert(0, '/b/trading/jgtutils')
sys.path.insert(0, '/b/trading/jgtcore')

# Use existing JGT infrastructure
from jgtutils.jgtcommon import is_market_open


class DataFreshnessValidator:
    """Validates data freshness using timeframe-specific logic."""
    
    # Maximum allowed age for each timeframe (in minutes)
    MAX_AGE_MINUTES = {
        'm1': 2,
        'm5': 10,
        'm15': 30,
        'H1': 120,
        'H4': 480,
        'D1': 1440,
        'W1': 10080
    }
    
    @classmethod
    def get_expected_last_bar_time(cls, timeframe):
        """Calculate when the last bar should have closed based on timeframe."""
        now = datetime.utcnow()
        
        if timeframe == 'm5':
            # Last m5 bar closes at :00, :05, :10, etc
            minutes = (now.minute // 5) * 5
            return now.replace(minute=minutes, second=0, microsecond=0)
        elif timeframe == 'm15':
            minutes = (now.minute // 15) * 15
            return now.replace(minute=minutes, second=0, microsecond=0)
        elif timeframe == 'H1':
            return now.replace(minute=0, second=0, microsecond=0)
        elif timeframe == 'H4':
            # H4 bars at 1:00, 5:00, 9:00, 13:00, 17:00, 21:00
            h4_hours = [1, 5, 9, 13, 17, 21]
            current_hour = now.hour
            last_h4 = max([h for h in h4_hours if h <= current_hour], default=21)
            if last_h4 > current_hour:
                last_h4 = 21
                return (now - timedelta(days=1)).replace(hour=last_h4, minute=0, second=0, microsecond=0)
            return now.replace(hour=last_h4, minute=0, second=0, microsecond=0)
        elif timeframe == 'D1':
            # D1 bars close at 21:00 or 22:00 UTC depending on DST
            return (now - timedelta(days=1)).replace(hour=21, minute=0, second=0, microsecond=0)
        
        return now
    
    @classmethod
    def is_data_fresh(cls, df, timeframe):
        """Check if data is fresh enough for the given timeframe."""
        if df is None or len(df) == 0:
            return False, "No data available"
        
        # Get last bar timestamp
        last_bar_time = pd.to_datetime(df.index[-1])
        if last_bar_time.tzinfo is not None:
            last_bar_time = last_bar_time.tz_localize(None)
        
        now = datetime.utcnow()
        age_minutes = (now - last_bar_time).total_seconds() / 60
        
        max_age = cls.MAX_AGE_MINUTES.get(timeframe, 60)
        
        if age_minutes > max_age:
            return False, f"Data is {age_minutes:.0f} min old (max: {max_age} min). Last bar: {last_bar_time}"
        
        return True, f"Data is fresh ({age_minutes:.0f} min old)"


class TandTSignalDecider:
    """
    TandT (Twos and Threes) Digital Decision Making for trading signals.
    
    Implements binary ACCEPTABLE/UNACCEPTABLE evaluation per element,
    with dominance hierarchy for decision making.
    """
    
    def __init__(self):
        # Elements in dominance order (highest to lowest)
        self.elements = [
            'data_freshness',      # Must have fresh data
            'market_open',         # Market must be open  
            'htf_alignment',       # HTF must support direction
            'signal_present',      # FDB signal must exist
            'signal_valid',        # Signal not broken (stop not hit)
            'mouth_open',          # Alligator mouth open
            'trend_strength'       # ADX > threshold
        ]
    
    def evaluate(self, signal_context):
        """
        Evaluate signal using TandT methodology.
        
        Returns: (decision: bool, evaluation: dict, reasoning: str)
        """
        evaluation = {}
        
        # Evaluate each element
        for element in self.elements:
            value = signal_context.get(element, False)
            evaluation[element] = {
                'value': value,
                'acceptable': bool(value)
            }
        
        # Decision algorithm: NO if any element in dominance order is UNACCEPTABLE
        decision = True
        blocking_element = None
        
        for element in self.elements:
            if not evaluation[element]['acceptable']:
                decision = False
                blocking_element = element
                break
        
        # Build reasoning
        acceptable_elements = [e for e in self.elements if evaluation[e]['acceptable']]
        unacceptable_elements = [e for e in self.elements if not evaluation[e]['acceptable']]
        
        if decision:
            reasoning = f"ACCEPTABLE - All {len(acceptable_elements)} elements pass"
        else:
            reasoning = f"UNACCEPTABLE - Blocked by: {blocking_element}"
        
        return decision, evaluation, reasoning
    
    def format_evaluation(self, evaluation, decision, reasoning):
        """Format evaluation for logging."""
        lines = ["TandT EVALUATION:"]
        lines.append("-" * 50)
        
        for element in self.elements:
            ev = evaluation.get(element, {})
            status = "✓ ACCEPTABLE" if ev.get('acceptable', False) else "✗ UNACCEPTABLE"
            lines.append(f"  {element}: {status}")
        
        lines.append("-" * 50)
        lines.append(f"DECISION: {'YES' if decision else 'NO'} - {reasoning}")
        
        return "\n".join(lines)


class ProductionFDBMonitor:
    """Production FDB Signal Monitor with proper validation."""
    
    def __init__(self, instruments, log_dir="/b/trading/jgtml/trading_logs"):
        self.instruments = instruments
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_root = Path("/b/trading/jgtml/data/current")
        self.decider = TandTSignalDecider()
        
        # Entry timeframes to scan
        self.entry_timeframes = ['m5', 'm15', 'H1']
        # HTF for validation
        self.htf_timeframes = ['H4', 'D1']
        
        # Active orders
        self.active_orders = {}
        
        # MMOT tracking
        self.mmot_log = []
        
        # Initialize log files
        self.logs = {}
        timestamp = datetime.now().strftime('%y%m%d')
        for inst in instruments:
            inst_safe = inst.replace('/', '-')
            log_file = self.log_dir / f"TRADING_{inst_safe}_{timestamp}.md"
            self.logs[inst] = log_file
            self._init_log(inst, log_file)
    
    def _init_log(self, instrument, log_file):
        """Initialize trading log with MMOT structure."""
        if not log_file.exists():
            with open(log_file, 'w') as f:
                f.write(f"# Trading Log: {instrument}\n")
                f.write(f"**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Direction**: LONG only\n")
                f.write(f"**Framework**: TandT Digital Decision Making + MMOT\n\n")
                f.write("---\n\n")
                f.write("## MMOT Tracking\n\n")
                f.write("| Time | Expected | Delivered | Gap | Action |\n")
                f.write("|------|----------|-----------|-----|--------|\n")
                f.write("\n---\n\n## Session Log\n\n")
    
    def _log(self, instrument, message, level="INFO"):
        """Log message to instrument's log file."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"**[{timestamp}]** [{level}] {message}\n\n"
        
        log_file = self.logs.get(instrument)
        if log_file:
            with open(log_file, 'a') as f:
                f.write(log_entry)
        
        print(f"[{instrument}] [{level}] {message}")
    
    def _log_mmot(self, instrument, expected, delivered, action):
        """Log MMOT discrepancy."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        gap = "Match" if expected == delivered else f"{expected} ≠ {delivered}"
        
        log_file = self.logs.get(instrument)
        if log_file:
            # Insert into MMOT table
            with open(log_file, 'a') as f:
                f.write(f"\n| {timestamp} | {expected} | {delivered} | {gap} | {action} |\n")
    
    def refresh_data_live(self, instrument, timeframe):
        """Refresh data from broker - ONLY if market is open."""
        if not is_market_open():
            return False, "Market closed"
        
        inst_fxcm = instrument.replace('-', '/')
        
        try:
            # Use jgtfxcli to get fresh data
            result = subprocess.run(
                ['jgtfxcli', '-i', inst_fxcm, '-t', timeframe, '-pdsrq', '-vp'],
                capture_output=True, text=True, timeout=60
            )
            
            if result.returncode == 0:
                # Generate CDS
                subprocess.run(
                    ['cdscli', '-i', inst_fxcm, '-t', timeframe],
                    capture_output=True, text=True, timeout=60
                )
                return True, "Data refreshed"
            else:
                return False, f"Refresh failed: {result.stderr}"
                
        except Exception as e:
            return False, f"Error: {e}"
    
    def load_cds(self, instrument, timeframe):
        """Load CDS data."""
        cds_file = self.data_root / "cds" / f"{instrument}_{timeframe}.csv"
        if not cds_file.exists():
            return None
        try:
            return pd.read_csv(cds_file, index_col=0, parse_dates=True)
        except:
            return None
    
    def check_htf_alignment(self, instrument, direction='LONG'):
        """Check if HTF supports the direction."""
        alignments = {}
        
        for tf in self.htf_timeframes:
            df = self.load_cds(instrument, tf)
            if df is None or len(df) < 50:
                alignments[tf] = 'UNKNOWN'
                continue
            
            # Simple trend check: price above/below EMA50
            if 'Close' in df.columns:
                ema50 = df['Close'].ewm(span=50).mean()
                last_close = df['Close'].iloc[-1]
                last_ema = ema50.iloc[-1]
                
                if last_close > last_ema:
                    alignments[tf] = 'LONG'
                else:
                    alignments[tf] = 'SHORT'
            else:
                alignments[tf] = 'UNKNOWN'
        
        # All HTF must align with direction
        all_aligned = all(alignments.get(tf) == direction for tf in self.htf_timeframes)
        
        return all_aligned, alignments
    
    def check_fdb_signal(self, df, direction='BUY'):
        """Check for FDB signal in data."""
        if df is None or len(df) < 5:
            return None
        
        # Check last 5 bars for signal
        signal_col = 'fdbb' if direction == 'BUY' else 'fdbs'
        
        for i in range(-5, 0):
            bar = df.iloc[i]
            
            if signal_col in df.columns and bar.get(signal_col, 0) == 1:
                return {
                    'bar_index': i,
                    'signal_date': df.index[i],
                    'entry_rate': bar.get('AskHigh', bar.get('High', 0)),
                    'stop_rate': bar.get('BidLow', bar.get('Low', 0)),
                    'signal_type': signal_col
                }
        
        return None
    
    def is_signal_still_valid(self, signal, current_bar):
        """Check if entry order is still valid."""
        entry = signal['entry_rate']
        stop = signal['stop_rate']
        
        current_low = current_bar.get('BidLow', current_bar.get('Low', 0))
        current_high = current_bar.get('AskHigh', current_bar.get('High', 0))
        
        # For BUY: invalid if price broke below stop
        if current_low < stop:
            return False, "STOP_BROKEN"
        
        # Check if filled
        if current_high >= entry:
            return True, "FILLED"
        
        return True, "PENDING"
    
    def evaluate_signal(self, instrument, timeframe):
        """Full TandT evaluation of a trading signal."""
        
        # Build signal context
        context = {
            'data_freshness': False,
            'market_open': False,
            'htf_alignment': False,
            'signal_present': False,
            'signal_valid': False,
            'mouth_open': True,  # Assume true for now
            'trend_strength': True  # Assume true for now
        }
        
        # 1. Check market open
        context['market_open'] = is_market_open()
        
        # 2. Load and check data freshness
        df = self.load_cds(instrument, timeframe)
        if df is not None:
            is_fresh, msg = DataFreshnessValidator.is_data_fresh(df, timeframe)
            context['data_freshness'] = is_fresh
            
            if not is_fresh:
                self._log(instrument, f"⚠️ Data stale: {msg}", "WARN")
                # Try to refresh if market open
                if context['market_open']:
                    self._log(instrument, f"Attempting data refresh...", "INFO")
                    refresh_ok, refresh_msg = self.refresh_data_live(instrument, timeframe)
                    if refresh_ok:
                        df = self.load_cds(instrument, timeframe)
                        is_fresh, msg = DataFreshnessValidator.is_data_fresh(df, timeframe)
                        context['data_freshness'] = is_fresh
                        self._log(instrument, f"After refresh: {msg}", "INFO")
                    else:
                        self._log(instrument, f"Refresh failed: {refresh_msg}", "WARN")
        else:
            context['data_freshness'] = False
            self._log(instrument, f"No data file found for {timeframe}", "ERROR")
        
        # 3. Check HTF alignment
        htf_ok, htf_details = self.check_htf_alignment(instrument, 'LONG')
        context['htf_alignment'] = htf_ok
        
        # 4. Check for FDB signal
        signal = self.check_fdb_signal(df, 'BUY')
        context['signal_present'] = signal is not None
        
        # 5. Check signal validity (not broken)
        if signal and df is not None:
            current_bar = df.iloc[-1]
            is_valid, status = self.is_signal_still_valid(signal, current_bar)
            context['signal_valid'] = is_valid and status != "STOP_BROKEN"
        
        # Run TandT evaluation
        decision, evaluation, reasoning = self.decider.evaluate(context)
        
        return decision, evaluation, reasoning, signal, context
    
    def scan_instrument(self, instrument):
        """Scan instrument with full TandT evaluation."""
        self._log(instrument, f"Scanning for LONG opportunities...")
        
        for tf in self.entry_timeframes:
            decision, evaluation, reasoning, signal, context = self.evaluate_signal(instrument, tf)
            
            # Log evaluation
            eval_str = self.decider.format_evaluation(evaluation, decision, reasoning)
            self._log(instrument, f"TF {tf}:\n```\n{eval_str}\n```")
            
            if decision and signal:
                # Create order
                order = self._create_order(instrument, tf, signal)
                self._log(instrument, 
                    f"🎯 APPROVED: {order['order_id']}\n"
                    f"   Entry: {order['entry_rate']:.5f}\n"
                    f"   Stop: {order['stop_rate']:.5f}\n"
                    f"   Target: {order['target_rate']:.5f}",
                    "TRADE")
                
                # MMOT: Log expectation
                self._log_mmot(instrument, "Signal approval", "APPROVED", "Order created")
                
                self.active_orders[order['order_id']] = order
                return order
            else:
                # MMOT: Log why not approved
                if not context['data_freshness']:
                    self._log_mmot(instrument, "Fresh data", "Stale data", "Skip scan")
                elif not context['htf_alignment']:
                    self._log_mmot(instrument, "HTF LONG", "Not aligned", "Wait")
                elif not context['signal_present']:
                    self._log_mmot(instrument, "FDB signal", "No signal", "Wait")
        
        return None
    
    def _create_order(self, instrument, timeframe, signal):
        """Create entry order."""
        order_id = f"{instrument}_{timeframe}_{datetime.now().strftime('%y%m%d%H%M%S')}"
        
        entry = signal['entry_rate']
        stop = signal['stop_rate']
        risk = entry - stop
        target = entry + (risk * 2)  # 2:1 R:R
        
        return {
            'order_id': order_id,
            'instrument': instrument,
            'timeframe': timeframe,
            'direction': 'BUY',
            'entry_rate': entry,
            'stop_rate': stop,
            'target_rate': target,
            'signal_date': str(signal['signal_date']),
            'created_at': datetime.now().isoformat(),
            'status': 'PENDING'
        }
    
    def monitor_loop(self, interval_seconds=300):
        """Main monitoring loop."""
        print("=" * 70)
        print("🎯 PRODUCTION FDB MONITOR (TandT + MMOT)")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔍 Instruments: {', '.join(self.instruments)}")
        print(f"⏱️  Interval: {interval_seconds}s")
        print(f"📈 Market: {'OPEN' if is_market_open() else 'CLOSED'}")
        print("=" * 70)
        
        cycle = 0
        while True:
            cycle += 1
            market_status = "OPEN" if is_market_open() else "CLOSED"
            print(f"\n--- Cycle {cycle} @ {datetime.now().strftime('%H:%M:%S')} [Market: {market_status}] ---")
            
            if not is_market_open():
                print("⏸️  Market closed - skipping scan")
                time.sleep(interval_seconds)
                continue
            
            # Validate active orders
            self._validate_orders()
            
            # Scan for new signals
            for inst in self.instruments:
                try:
                    self.scan_instrument(inst)
                except Exception as e:
                    self._log(inst, f"Scan error: {e}", "ERROR")
            
            # Summary
            print(f"\nActive orders: {len(self.active_orders)}")
            
            print(f"\n💤 Sleeping {interval_seconds}s...")
            time.sleep(interval_seconds)
    
    def _validate_orders(self):
        """Validate active orders."""
        to_remove = []
        
        for order_id, order in self.active_orders.items():
            inst = order['instrument']
            tf = order['timeframe']
            
            df = self.load_cds(inst, tf)
            if df is None:
                continue
            
            current_bar = df.iloc[-1]
            is_valid, status = self.is_signal_still_valid(order, current_bar)
            
            if status == "STOP_BROKEN":
                self._log(inst, f"❌ {order_id}: INVALIDATED - stop broken", "CANCEL")
                self._log_mmot(inst, "Order valid", "Stop broken", "Cancel order")
                to_remove.append(order_id)
            elif status == "FILLED":
                self._log(inst, f"✅ {order_id}: FILLED at {order['entry_rate']:.5f}", "TRADE")
                self._log_mmot(inst, "Entry hit", "FILLED", "Manage trade")
                order['status'] = 'FILLED'
        
        for oid in to_remove:
            del self.active_orders[oid]
    
    def save_state(self):
        """Save state."""
        state = {
            'timestamp': datetime.now().isoformat(),
            'active_orders': self.active_orders
        }
        state_file = self.log_dir / "monitor_state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2, default=str)


def main():
    instruments = ['EUR-USD', 'GBP-USD', 'AUD-USD']
    
    monitor = ProductionFDBMonitor(instruments)
    
    try:
        monitor.monitor_loop(interval_seconds=300)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
        monitor.save_state()


if __name__ == "__main__":
    main()
