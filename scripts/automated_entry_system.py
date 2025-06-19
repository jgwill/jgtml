#!/usr/bin/env python3
"""
Automated Trading Entry System
Integrates jgtml enhanced FDB scanning with intelligent market entry decisions
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Add jgtml to path for integration
sys.path.insert(0, '/src/jgtml')
sys.path.insert(0, '/src/jgtagentic')

class AutomatedTradingSystem:
    """Complete automated trading system with data refresh, scanning, and entry"""
    
    def __init__(self, config_file=None):
        self.config = self.load_config(config_file)
        self.min_quality_score = self.config.get('min_quality_score', 7.0)
        self.max_illusions = self.config.get('max_illusions', 1)
        self.monitored_instruments = self.config.get('instruments', 
            ["EUR-USD", "GBP-USD", "USD-JPY", "SPX500"])
        self.timeframes = self.config.get('timeframes', ["D1", "H1", "H4"])
        self.live_trading = self.config.get('live_trading', False)
        
    def load_config(self, config_file):
        """Load trading system configuration"""
        default_config = {
            'min_quality_score': 7.0,
            'max_illusions': 1,
            'instruments': ["EUR-USD", "GBP-USD", "USD-JPY", "SPX500"],
            'timeframes': ["D1", "H1", "H4"],
            'live_trading': False,
            'position_sizes': {
                'high_quality': 0.02,
                'medium_quality': 0.015,
                'low_quality': 0.01
            },
            'risk_management': {
                'stop_loss_pips': 50,
                'take_profit_pips': 100,
                'max_daily_trades': 5
            }
        }
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
                
        return default_config
    
    def refresh_market_data(self, instrument, timeframes=None):
        """Refresh market data using REAL jgtapp.cds() function"""
        if timeframes is None:
            timeframes = self.timeframes
            
        print(f"🔄 Refreshing data for {instrument}...")
        
        try:
            # Import the REAL jgtapp module
            sys.path.insert(0, '/src/jgtml')
            from jgtml.jgtapp import cds
            
            success_count = 0
            for tf in timeframes:
                try:
                    print(f"  🔄 Generating {instrument} {tf} via jgtapp.cds()...")
                    # Use the REAL CDS generation function
                    cds(instrument, tf, use_fresh=True, use_full=True)
                    print(f"  ✅ {tf}: Data generated successfully")
                    success_count += 1
                except Exception as e:
                    print(f"  ❌ {tf}: CDS generation failed: {e}")
                    
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Failed to import jgtapp.cds(): {e}")
            return False
    
    def run_enhanced_scan(self, instrument, timeframes):
        """Run enhanced FDB scan with illusion detection"""
        try:
            # Import the enhanced scanner
            from jgtml.enhanced_fdb_scanner_with_illusion_detection import EnhancedFDBScanner
            
            scanner = EnhancedFDBScanner()
            result = scanner.enhanced_scan(instrument, timeframes, include_illusion_detection=True)
            
            return result
            
        except Exception as e:
            print(f"❌ Error running enhanced scan for {instrument}: {e}")
            return None
    
    def analyze_signal_quality(self, scan_result):
        """Analyze scan result and extract quality metrics"""
        if not scan_result:
            return None
            
        quality_score = scan_result.get('signal_quality_score', 0)
        illusion_count = scan_result.get('illusion_results', {}).get('illusion_count', 0)
        fdb_signals = sum(r['total_signals'] for r in scan_result.get('fdb_results', {}).values())
        recommendation = scan_result.get('final_recommendation', '')
        
        return {
            'quality_score': quality_score,
            'illusion_count': illusion_count,
            'fdb_signals': fdb_signals,
            'recommendation': recommendation,
            'should_enter': self.should_enter(quality_score, illusion_count, recommendation)
        }
    
    def should_enter(self, quality_score, illusion_count, recommendation):
        """Determine if we should enter based on quality metrics"""
        quality_ok = quality_score >= self.min_quality_score
        illusions_ok = illusion_count <= self.max_illusions
        
        # Valid recommendations must be clearly directional
        valid_recommendations = [
            'STRONG BUY', 'STRONG SELL', 
            'MODERATE BUY', 'MODERATE SELL',
            'WEAK BUY', 'WEAK SELL'
        ]
        recommendation_ok = recommendation in valid_recommendations
        
        return quality_ok and illusions_ok and recommendation_ok
    
    def calculate_position_size(self, quality_score, illusion_count):
        """Calculate position size based on signal quality"""
        sizes = self.config['position_sizes']
        
        if quality_score >= 9.0 and illusion_count == 0:
            return sizes['high_quality']  # 2% - Full position
        elif quality_score >= 8.0:
            return sizes['medium_quality']  # 1.5% - 75% position
        else:
            return sizes['low_quality']  # 1% - 50% position
    
    def execute_entry(self, instrument, analysis, position_size):
        """Execute market entry (simulation or live)"""
        recommendation = analysis['recommendation']
        quality_score = analysis['quality_score']
        
        # Extract clear direction from recommendation
        if 'BUY' in recommendation:
            direction = "BUY"
        elif 'SELL' in recommendation:
            direction = "SELL"
        else:
            print(f"❌ Invalid recommendation: {recommendation}")
            return None
        
        entry_data = {
            'timestamp': datetime.now().isoformat(),
            'instrument': instrument,
            'direction': direction,
            'position_size': position_size,
            'quality_score': quality_score,
            'illusion_count': analysis['illusion_count'],
            'fdb_signals': analysis['fdb_signals'],
            'stop_loss': self.config['risk_management']['stop_loss_pips'],
            'take_profit': self.config['risk_management']['take_profit_pips']
        }
        
        print(f"🚀 ENTRY DECISION: {instrument}")
        print(f"   Direction: {direction}")
        print(f"   Position Size: {position_size}%")
        print(f"   Quality: {quality_score:.1f}/10")
        print(f"   Stop Loss: {entry_data['stop_loss']} pips")
        print(f"   Take Profit: {entry_data['take_profit']} pips")
        
        if self.live_trading:
            # Execute via jgtfxcon
            order_command = self.build_order_command(entry_data)
            print(f"📋 Executing: {order_command}")
            # os.system(order_command)  # Uncomment for live execution
        else:
            print("📊 SIMULATION MODE - No actual trade executed")
            
        # Log the entry decision
        self.log_entry_decision(entry_data)
        
        return entry_data
    
    def build_order_command(self, entry_data):
        """Build jgtfxcon order command"""
        return f"""jgtfxcon place-order \\
            --instrument {entry_data['instrument']} \\
            --direction {entry_data['direction']} \\
            --size {entry_data['position_size']} \\
            --stop-loss {entry_data['stop_loss']} \\
            --take-profit {entry_data['take_profit']}"""
    
    def log_entry_decision(self, entry_data):
        """Log entry decision for analysis"""
        log_file = Path("logs/entry_decisions.json")
        log_file.parent.mkdir(exist_ok=True)
        
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
                
            logs.append(entry_data)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            print(f"Warning: Could not log entry decision: {e}")
    
    def scan_and_enter_all(self):
        """Complete workflow: scan all instruments and make entry decisions"""
        print("🌸 AUTOMATED TRADING SYSTEM - FULL SCAN")
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Instruments: {', '.join(self.monitored_instruments)}")
        print(f"Timeframes: {', '.join(self.timeframes)}")
        print(f"Min Quality: {self.min_quality_score}")
        print(f"Max Illusions: {self.max_illusions}")
        print(f"Live Trading: {self.live_trading}")
        print("=" * 50)
        
        entries_made = 0
        
        for instrument in self.monitored_instruments:
            print(f"\n🔍 ANALYZING {instrument}")
            print("-" * 30)
            
            # Step 1: Refresh data if needed
            if not self.refresh_market_data(instrument):
                print(f"⚠️  Data refresh failed for {instrument}")
                continue
            
            # Step 2: Run enhanced scan
            scan_result = self.run_enhanced_scan(instrument, self.timeframes)
            if not scan_result:
                print(f"❌ Scan failed for {instrument}")
                continue
            
            # Step 3: Analyze quality
            analysis = self.analyze_signal_quality(scan_result)
            if not analysis:
                print(f"❌ Analysis failed for {instrument}")
                continue
            
            # Step 4: Display analysis
            print(f"📊 Quality Score: {analysis['quality_score']:.1f}/10")
            print(f"🐊 Illusions: {analysis['illusion_count']}")
            print(f"📈 FDB Signals: {analysis['fdb_signals']}")
            print(f"🎯 Recommendation: {analysis['recommendation']}")
            
            # Step 5: Entry decision
            if analysis['should_enter']:
                position_size = self.calculate_position_size(
                    analysis['quality_score'], 
                    analysis['illusion_count']
                )
                
                self.execute_entry(instrument, analysis, position_size)
                entries_made += 1
                
                # Check daily limit
                if entries_made >= self.config['risk_management']['max_daily_trades']:
                    print("⚠️  Daily trade limit reached")
                    break
            else:
                print("⏳ Waiting for better setup")
        
        print(f"\n🎯 SCAN COMPLETE: {entries_made} entries made")
        return entries_made

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated Trading Entry System')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--live', action='store_true', help='Enable live trading')
    parser.add_argument('--instrument', help='Single instrument to analyze')
    parser.add_argument('--min-quality', type=float, default=7.0, help='Minimum quality score')
    
    args = parser.parse_args()
    
    # Load system
    system = AutomatedTradingSystem(args.config)
    
    # Override config with command line args
    if args.live:
        system.live_trading = True
    if args.min_quality:
        system.min_quality_score = args.min_quality
    if args.instrument:
        system.monitored_instruments = [args.instrument]
    
    # Run the system
    try:
        system.scan_and_enter_all()
    except KeyboardInterrupt:
        print("\n🛑 System interrupted by user")
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 