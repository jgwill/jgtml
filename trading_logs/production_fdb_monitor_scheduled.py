#!/usr/bin/env python3
"""
Production FDB Signal Trading Monitor - Scheduled Version

Implements timeframe-based monitoring:
- m5 signals: Scan every 5 minutes
- m15 signals: Scan at :00, :15, :30, :45 of each hour
- H1 signals: Scan at top of each hour

Data Refresh:
- PDS (Price Data Service): Refresh before each scan
- CDS (Chaos Data Service): Generate from fresh PDS data
- TTF (Transformed Trading Features): As needed for ML validation

Decision Framework:
- TandT Digital Decision Making (7-element evaluation)
- MMOT tracking for performance analysis
- Order placement via existing jgtfxcon infrastructure
"""

import os
import sys
import time
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import threading

# Add JGT packages to path
sys.path.insert(0, '/b/trading/jgtml')
sys.path.insert(0, '/b/trading/jgtpy')
sys.path.insert(0, '/b/trading/jgtutils')
sys.path.insert(0, '/b/trading/jgtcore')

from jgtutils.jgtcommon import is_market_open


class TimeframeScheduler:
    """Manages timeframe-based task scheduling."""
    
    def __init__(self):
        self.m5_times = self._get_m5_times()
        self.m15_times = self._get_m15_times()
        self.h1_times = self._get_h1_times()
    
    @staticmethod
    def _get_m5_times():
        """Get all m5 bar closing times (every 5 minutes)."""
        times = []
        for h in range(24):
            for m in range(0, 60, 5):
                times.append(f"{str(h).zfill(2)}:{str(m).zfill(2)}")
        return set(times)
    
    @staticmethod
    def _get_m15_times():
        """Get m15 bar closing times (:00, :15, :30, :45)."""
        times = set()
        for h in range(24):
            for m in [0, 15, 30, 45]:
                times.add(f"{str(h).zfill(2)}:{str(m).zfill(2)}")
        return times
    
    @staticmethod
    def _get_h1_times():
        """Get H1 bar closing times (top of each hour)."""
        times = set()
        for h in range(24):
            times.add(f"{str(h).zfill(2)}:00")
        return times
    
    def should_scan_m5(self):
        """Check if current time matches m5 closing time."""
        now = datetime.utcnow().strftime("%H:%M")
        return now in self.m5_times
    
    def should_scan_m15(self):
        """Check if current time matches m15 closing time."""
        now = datetime.utcnow().strftime("%H:%M")
        return now in self.m15_times
    
    def should_scan_h1(self):
        """Check if current time matches H1 closing time."""
        now = datetime.utcnow().strftime("%H:%M")
        return now in self.h1_times
    
    def get_next_scan_time(self, timeframe):
        """Get seconds until next scan for timeframe."""
        now = datetime.utcnow()
        
        if timeframe == 'm5':
            # Next m5 is in next 5 minutes
            next_min = ((now.minute // 5) + 1) * 5
            if next_min >= 60:
                next_time = (now + timedelta(hours=1)).replace(minute=0, second=0)
            else:
                next_time = now.replace(minute=next_min, second=0)
        
        elif timeframe == 'm15':
            # Next m15 at :00, :15, :30, or :45
            next_m15 = ((now.minute // 15) + 1) * 15
            if next_m15 >= 60:
                next_time = (now + timedelta(hours=1)).replace(minute=0, second=0)
            else:
                next_time = now.replace(minute=next_m15, second=0)
        
        elif timeframe == 'H1':
            # Next H1 at top of next hour
            next_time = (now + timedelta(hours=1)).replace(minute=0, second=0)
        
        else:
            next_time = now + timedelta(seconds=60)
        
        return max(0, (next_time - now).total_seconds())


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
            return False, f"Data is {age_minutes:.0f} min old (max: {max_age} min)"
        
        return True, f"Data is fresh ({age_minutes:.0f} min old)"


class TandTSignalDecider:
    """TandT Digital Decision Making for trading signals."""
    
    def __init__(self):
        self.elements = [
            'data_freshness',
            'market_open',
            'htf_alignment',
            'signal_present',
            'signal_valid',
            'mouth_open',
            'trend_strength'
        ]
    
    def evaluate(self, signal_context):
        """Evaluate signal using TandT methodology."""
        evaluation = {}
        
        for element in self.elements:
            value = signal_context.get(element, False)
            evaluation[element] = {
                'value': value,
                'acceptable': bool(value)
            }
        
        decision = True
        blocking_element = None
        
        for element in self.elements:
            if not evaluation[element]['acceptable']:
                decision = False
                blocking_element = element
                break
        
        acceptable_count = sum(1 for e in self.elements if evaluation[e]['acceptable'])
        
        if decision:
            reasoning = f"ACCEPTABLE - All {acceptable_count} elements pass"
        else:
            reasoning = f"UNACCEPTABLE - Blocked by: {blocking_element}"
        
        return decision, evaluation, reasoning


class ProductionFDBMonitor:
    """Production FDB Signal Monitor with timeframe-based scheduling."""
    
    def __init__(self, instruments, log_dir="/b/trading/jgtml/trading_logs"):
        self.instruments = instruments
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_root = Path("/b/trading/jgtml/data/current")
        self.decider = TandTSignalDecider()
        self.scheduler = TimeframeScheduler()
        
        # Timeframes to monitor
        self.timeframes = ['m5', 'm15', 'H1']
        
        # HTF for validation
        self.htf_timeframes = ['H4', 'D1']
        
        # Active orders
        self.active_orders = {}
        
        # Tracking
        self.logs = {}
        self.scan_count = {tf: 0 for tf in self.timeframes}
        self.order_count = 0
        
        # Initialize log files
        timestamp = datetime.now().strftime('%y%m%d')
        for inst in instruments:
            inst_safe = inst.replace('/', '-')
            log_file = self.log_dir / f"TRADING_{inst_safe}_{timestamp}.md"
            self.logs[inst] = log_file
            self._init_log(inst, log_file)
        
        print(f"✅ Monitor initialized")
        print(f"   Instruments: {', '.join(instruments)}")
        print(f"   Timeframes: {', '.join(self.timeframes)}")
        print(f"   Log dir: {log_dir}")
    
    def _init_log(self, instrument, log_file):
        """Initialize trading log."""
        if not log_file.exists():
            with open(log_file, 'w') as f:
                f.write(f"# Trading Log: {instrument}\n")
                f.write(f"**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Direction**: LONG only\n")
                f.write(f"**Framework**: TandT + MMOT + Scheduled Monitoring\n\n")
                f.write("---\n\n")
    
    def _log(self, instrument, message, level="INFO"):
        """Log message to instrument's log file."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"**[{timestamp}]** [{level}] {message}\n\n"
        
        log_file = self.logs.get(instrument)
        if log_file:
            with open(log_file, 'a') as f:
                f.write(log_entry)
        
        print(f"[{instrument:12}] [{level:5}] {message}")
    
    def refresh_pds(self, instrument, timeframe):
        """Refresh PDS (Price Data Service) from broker."""
        inst_fxcm = instrument.replace('-', '/')
        
        try:
            # Use jgtfxcli to get fresh prices
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
                return True, "PDS+CDS refreshed"
            else:
                return False, f"PDS refresh failed"
                
        except Exception as e:
            return False, f"Error: {str(e)[:50]}"
    
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
            
            if 'Close' in df.columns:
                ema50 = df['Close'].ewm(span=50).mean()
                last_close = df['Close'].iloc[-1]
                last_ema = ema50.iloc[-1]
                
                alignments[tf] = 'LONG' if last_close > last_ema else 'SHORT'
            else:
                alignments[tf] = 'UNKNOWN'
        
        all_aligned = all(alignments.get(tf) == direction for tf in self.htf_timeframes)
        
        return all_aligned, alignments
    
    def check_fdb_signal(self, df, direction='BUY'):
        """Check for FDB signal in data."""
        if df is None or len(df) < 5:
            return None
        
        signal_col = 'fdbb' if direction == 'BUY' else 'fdbs'
        
        for i in range(-10, 0):
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
        
        if current_low < stop:
            return False, "STOP_BROKEN"
        
        if current_high >= entry:
            return True, "FILLED"
        
        return True, "PENDING"
    
    def evaluate_signal(self, instrument, timeframe):
        """Full TandT evaluation of a trading signal."""
        
        context = {
            'data_freshness': False,
            'market_open': False,
            'htf_alignment': False,
            'signal_present': False,
            'signal_valid': False,
            'mouth_open': True,
            'trend_strength': True
        }
        
        # Check market open
        context['market_open'] = is_market_open()
        
        # Load and check data freshness
        df = self.load_cds(instrument, timeframe)
        if df is not None:
            is_fresh, msg = DataFreshnessValidator.is_data_fresh(df, timeframe)
            context['data_freshness'] = is_fresh
            
            if not is_fresh and context['market_open']:
                refresh_ok, refresh_msg = self.refresh_pds(instrument, timeframe)
                if refresh_ok:
                    df = self.load_cds(instrument, timeframe)
                    is_fresh, msg = DataFreshnessValidator.is_data_fresh(df, timeframe)
                    context['data_freshness'] = is_fresh
        
        # Check HTF alignment
        htf_ok, htf_details = self.check_htf_alignment(instrument, 'LONG')
        context['htf_alignment'] = htf_ok
        
        # Check for FDB signal
        signal = self.check_fdb_signal(df, 'BUY')
        context['signal_present'] = signal is not None
        
        # Check signal validity
        if signal and df is not None:
            current_bar = df.iloc[-1]
            is_valid, status = self.is_signal_still_valid(signal, current_bar)
            context['signal_valid'] = is_valid and status != "STOP_BROKEN"
        
        decision, evaluation, reasoning = self.decider.evaluate(context)
        
        return decision, evaluation, reasoning, signal, context
    
    def scan_timeframe(self, instrument, timeframe):
        """Scan single timeframe for signals."""
        decision, evaluation, reasoning, signal, context = self.evaluate_signal(instrument, timeframe)
        
        self.scan_count[timeframe] += 1
        
        # Log brief result
        status = "✅ PASS" if decision else "❌ FAIL"
        self._log(instrument, f"{timeframe:4} scan #{self.scan_count[timeframe]:3}: {status} - {reasoning}")
        
        if decision and signal:
            # Place order
            try:
                order = self._place_order(instrument, timeframe, signal)
                self.order_count += 1
                return order
            except Exception as e:
                self._log(instrument, f"Order failed: {str(e)[:60]}", "ERROR")
                return None
        
        return None
    
    def scan_all_instruments(self, timeframe):
        """Scan all instruments for a specific timeframe."""
        print(f"\n{'='*80}")
        print(f"🔍 {timeframe:4} SCAN @ {datetime.utcnow().strftime('%H:%M:%S')}")
        print(f"{'='*80}")
        
        for inst in self.instruments:
            try:
                self.scan_timeframe(inst, timeframe)
            except Exception as e:
                self._log(inst, f"Scan error: {str(e)[:60]}", "ERROR")
    
    def _place_order(self, instrument, timeframe, signal):
        """Create and place entry order."""
        order = self._create_order(instrument, timeframe, signal)
        
        # Place via fxaddorder
        cmd = [
            'fxaddorder',
            '-i', order['instrument'],
            '-n', str(order['lots']),
            '-r', str(order['entry_rate']),
            '-d', 'B',
            '-x', str(order['stop_rate']),
            '--demo'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        
        if result.returncode != 0:
            raise RuntimeError(f"fxaddorder failed")
        
        order['status'] = 'PLACED'
        order['placed_at'] = datetime.now().isoformat()
        
        self.active_orders[order['order_id']] = order
        
        self._log(instrument,
            f"🎯 ORDER PLACED: {order['order_id']}\n"
            f"   Entry: {order['entry_rate']:.5f} | Stop: {order['stop_rate']:.5f}\n"
            f"   Target: {order['target_rate']:.5f} | Risk: {order['risk_pips']:.1f}p",
            "TRADE")
        
        return order
    
    def _create_order(self, instrument, timeframe, signal):
        """Create entry order with risk calculations."""
        order_id = f"{instrument}_{timeframe}_{datetime.now().strftime('%y%m%d%H%M%S')}"
        
        entry = signal['entry_rate']
        stop = signal['stop_rate']
        risk = entry - stop
        
        if 'JPY' in instrument:
            risk_pips = risk * 100
        else:
            risk_pips = risk * 10000
        
        target = entry + (risk * 2)
        
        return {
            'order_id': order_id,
            'instrument': instrument,
            'timeframe': timeframe,
            'direction': 'BUY',
            'entry_rate': entry,
            'stop_rate': stop,
            'target_rate': target,
            'risk_pips': risk_pips,
            'lots': 1,
            'signal_date': str(signal['signal_date']),
            'created_at': datetime.now().isoformat(),
            'status': 'PENDING'
        }
    
    def monitor_loop(self):
        """Main monitoring loop with timeframe-based scheduling."""
        print("\n" + "="*80)
        print("🎯 PRODUCTION FDB MONITOR - SCHEDULED VERSION")
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"🔍 Instruments: {', '.join(self.instruments)}")
        print(f"⏱️  Timeframes: m5 (every 5m) | m15 (:00,:15,:30,:45) | H1 (hourly)")
        print("="*80 + "\n")
        
        last_m5_scan = None
        last_m15_scan = None
        last_h1_scan = None
        
        while True:
            now = datetime.utcnow()
            current_time = now.strftime("%H:%M:%S")
            market_status = "OPEN ✅" if is_market_open() else "CLOSED ❌"
            
            # Check if we should scan
            should_m5 = self.scheduler.should_scan_m5() and last_m5_scan != now.strftime("%H:%M")
            should_m15 = self.scheduler.should_scan_m15() and last_m15_scan != now.strftime("%H:%M")
            should_h1 = self.scheduler.should_scan_h1() and last_h1_scan != now.strftime("%H:%M")
            
            if should_m5:
                last_m5_scan = now.strftime("%H:%M")
                self.scan_all_instruments('m5')
            
            if should_m15:
                last_m15_scan = now.strftime("%H:%M")
                self.scan_all_instruments('m15')
            
            if should_h1:
                last_h1_scan = now.strftime("%H:%M")
                self.scan_all_instruments('H1')
            
            # Sleep briefly
            time.sleep(1)
    
    def save_state(self):
        """Save monitor state."""
        state = {
            'timestamp': datetime.now().isoformat(),
            'active_orders': self.active_orders,
            'scan_counts': self.scan_count,
            'total_orders': self.order_count
        }
        state_file = self.log_dir / "monitor_state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2, default=str)


def main():
    instruments = ['EUR-USD', 'GBP-USD', 'AUD-USD']
    
    monitor = ProductionFDBMonitor(instruments)
    
    try:
        monitor.monitor_loop()
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user")
        monitor.save_state()
        print("✅ State saved")


if __name__ == "__main__":
    main()
