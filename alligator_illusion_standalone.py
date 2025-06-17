#!/usr/bin/env python3
"""Alligator Illusion standalone detector.

This script implements a lightweight version of the Alligator Illusion
detection logic so it can be executed on its own without the rest of the
`jgtml` package.  It loads cached CDS data, analyzes the Alligator indicator
for multiple timeframes, and surfaces contradictory or weak signals.  The
standalone form is useful for quick experiments or debugging when the full
environment with `jgtpy` and heavier dependencies is unavailable.
"""

import csv
from pathlib import Path

class StandaloneAlligatorDetector:
    """Standalone version for testing without NumPy compatibility issues"""
    
    def __init__(self, data_path="/src/jgtml/cache/fdb_scanners"):
        self.data_path = Path(data_path)
    
    def load_csv_data(self, instrument, timeframe):
        """Load CDS cache data using basic CSV reader"""
        filename = f"{instrument}_{timeframe}_cds_cache.csv"
        filepath = self.data_path / filename
        
        if not filepath.exists():
            print(f"⚠️  Data file not found: {filepath}")
            return None
        
        try:
            data = []
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            
            print(f"✅ Loaded {len(data)} records for {instrument} {timeframe}")
            return data
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def analyze_latest_alligator(self, data, timeframe):
        """Analyze latest alligator reading from data"""
        if not data or len(data) == 0:
            return None
        
        # Get latest record
        latest = data[-1]
        
        # Extract alligator values (try different column name patterns)
        jaw = self.safe_float(latest.get('alligator_jaw', 
                                       latest.get('Alligator_Jaw', 
                                                latest.get('jaw', 0))))
        teeth = self.safe_float(latest.get('alligator_teeth', 
                                         latest.get('Alligator_Teeth', 
                                                  latest.get('teeth', 0))))
        lips = self.safe_float(latest.get('alligator_lips', 
                                        latest.get('Alligator_Lips', 
                                                 latest.get('lips', 0))))
        
        # Determine trend direction
        if lips > teeth > jaw:
            trend = "bullish"
        elif lips < teeth < jaw:
            trend = "bearish"
        else:
            trend = "sideways"
        
        # Calculate mouth openness
        if jaw != 0:
            mouth_separation = abs(lips - jaw) / abs(jaw) * 100
            mouth_open = mouth_separation > 0.1
        else:
            mouth_separation = 0
            mouth_open = False
        
        return {
            'timeframe': timeframe,
            'jaw': jaw,
            'teeth': teeth,
            'lips': lips,
            'trend': trend,
            'mouth_open': mouth_open,
            'mouth_separation': mouth_separation,
            'timestamp': latest.get('timestamp', latest.get('Timestamp', ''))
        }
    
    def safe_float(self, value):
        """Safely convert value to float"""
        try:
            return float(value) if value else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def detect_timeframe_illusions(self, readings):
        """Detect illusions across timeframes"""
        illusions = []
        
        if len(readings) < 2:
            return illusions
        
        timeframes = list(readings.keys())
        
        # Check for trend contradictions
        for i in range(len(timeframes)):
            for j in range(i+1, len(timeframes)):
                tf1, tf2 = timeframes[i], timeframes[j]
                r1, r2 = readings[tf1], readings[tf2]
                
                # Timeframe contradiction detection
                if (r1['trend'] == 'bullish' and r2['trend'] == 'bearish') or \
                   (r1['trend'] == 'bearish' and r2['trend'] == 'bullish'):
                    
                    illusions.append({
                        'type': 'TIMEFRAME_CONTRADICTION',
                        'primary_tf': tf1,
                        'conflicting_tf': tf2,
                        'description': f"{tf1} shows {r1['trend']} trend while {tf2} shows {r2['trend']} trend",
                        'recommendation': 'Wait for timeframe alignment before entry',
                        'confidence': 0.8,
                        'campaign_guidance': f"Monitor {tf1} for trend continuation"
                    })
        
        # Check for weak signals
        for tf, reading in readings.items():
            if reading['trend'] != 'sideways' and reading['mouth_separation'] < 0.05:
                illusions.append({
                    'type': 'WEAK_SIGNAL',
                    'primary_tf': tf,
                    'conflicting_tf': None,
                    'description': f"Weak alligator signal on {tf} - mouth barely open ({reading['mouth_separation']:.3f}%)",
                    'recommendation': 'Wait for stronger confirmation',
                    'confidence': 0.6,
                    'campaign_guidance': 'Short-term pattern, monitor for 2-3 periods'
                })
        
        return illusions
    
    def scan_instrument(self, instrument, timeframes=None):
        """Complete scan with illusion detection"""
        if timeframes is None:
            timeframes = ['D1', 'H1']
        
        print(f"\n🐊 ALLIGATOR ILLUSION DETECTION SCAN")
        print(f"Instrument: {instrument}")
        print(f"Timeframes: {timeframes}")
        print("=" * 50)
        
        # Load and analyze each timeframe
        readings = {}
        for tf in timeframes:
            data = self.load_csv_data(instrument, tf)
            if data:
                analysis = self.analyze_latest_alligator(data, tf)
                if analysis:
                    readings[tf] = analysis
        
        if not readings:
            return {
                'status': 'error',
                'message': 'No data available for analysis'
            }
        
        # Display timeframe analysis
        print(f"\n📊 TIMEFRAME ANALYSIS:")
        for tf, reading in readings.items():
            print(f"\n{tf}: {reading['trend'].upper()} trend")
            print(f"  Jaw: {reading['jaw']:.5f}")
            print(f"  Teeth: {reading['teeth']:.5f}")
            print(f"  Lips: {reading['lips']:.5f}")
            print(f"  Mouth Open: {'Yes' if reading['mouth_open'] else 'No'} ({reading['mouth_separation']:.3f}%)")
        
        # Detect illusions
        illusions = self.detect_timeframe_illusions(readings)
        
        # Display results
        if illusions:
            print(f"\n⚠️  {len(illusions)} ILLUSION(S) DETECTED:")
            for i, illusion in enumerate(illusions, 1):
                print(f"\n{i}. {illusion['type']}")
                print(f"   Description: {illusion['description']}")
                print(f"   Recommendation: {illusion['recommendation']}")
                print(f"   Confidence: {illusion['confidence']:.2f}")
                print(f"   Campaign Guidance: {illusion['campaign_guidance']}")
        else:
            print(f"\n✅ NO ILLUSIONS DETECTED - Clear signal environment")
        
        # Final recommendation
        recommendation = "PROCEED" if not illusions else "CAUTION"
        print(f"\n🎯 RECOMMENDATION: {recommendation}")
        
        if illusions:
            print(f"⚠️  {len(illusions)} pattern(s) suggest caution before entry")
        else:
            print("✅ Clear multi-timeframe alignment - safe to proceed")
        
        print("=" * 50)
        
        return {
            'status': 'success',
            'instrument': instrument,
            'readings': readings,
            'illusions': illusions,
            'recommendation': recommendation
        }

def main():
    """Test the standalone detector"""
    import sys
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python alligator_illusion_standalone.py <instrument> [timeframes...]")
        print("Example: python alligator_illusion_standalone.py EUR-USD D1 H1")
        return
    
    instrument = sys.argv[1]
    timeframes = sys.argv[2:] if len(sys.argv) > 2 else ['D1', 'H1']
    
    # Initialize detector
    detector = StandaloneAlligatorDetector()
    
    # Perform scan
    result = detector.scan_instrument(instrument, timeframes)
    
    # Summary
    if result['status'] == 'success':
        print(f"\n🎯 SCAN COMPLETE - {result['recommendation']}")
    else:
        print(f"\n❌ SCAN FAILED: {result['message']}")

if __name__ == "__main__":
    main() 
