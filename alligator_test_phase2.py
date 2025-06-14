#!/usr/bin/env python3
"""Phase 2 Alligator Illusion Detection Test"""

import csv
from pathlib import Path

def test_alligator_illusion_detection():
    print("🐊✨ PHASE 2: ALLIGATOR ILLUSION DETECTION TEST ✨🐊")
    print("=" * 60)
    
    data_path = Path("/src/jgtml/cache/fdb_scanners")
    
    # Test EUR-USD across multiple timeframes
    instrument = "EUR-USD"
    timeframes = ["D1", "H1", "H4", "W1"]
    
    print(f"\n📊 TESTING: {instrument}")
    print("-" * 30)
    
    readings = {}
    
    for tf in timeframes:
        filename = f"{instrument}_{tf}_cds_cache.csv"
        filepath = data_path / filename
        
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    data = list(csv.DictReader(f))
                
                if data:
                    latest = data[-1]
                    jaw = float(latest.get('jaw', 0))
                    teeth = float(latest.get('teeth', 0))
                    lips = float(latest.get('lips', 0))
                    
                    # Determine trend
                    if lips > teeth > jaw:
                        trend = "BULLISH"
                    elif lips < teeth < jaw:
                        trend = "BEARISH"
                    else:
                        trend = "SIDEWAYS"
                    
                    # Calculate mouth separation
                    mouth_sep = abs(lips - jaw) / abs(jaw) * 100 if jaw != 0 else 0
                    
                    readings[tf] = {
                        'trend': trend,
                        'jaw': jaw,
                        'teeth': teeth,
                        'lips': lips,
                        'mouth_separation': mouth_sep,
                        'records': len(data)
                    }
                    
                    print(f"{tf}: {trend} trend")
                    print(f"  Jaw: {jaw:.5f}")
                    print(f"  Teeth: {teeth:.5f}")
                    print(f"  Lips: {lips:.5f}")
                    print(f"  Mouth Sep: {mouth_sep:.3f}%")
                    print(f"  Records: {len(data)}")
                    print()
                    
            except Exception as e:
                print(f"{tf}: Error - {e}")
        else:
            print(f"{tf}: Data file not found")
    
    # Detect illusions
    print("🔍 ILLUSION DETECTION ANALYSIS:")
    print("-" * 30)
    
    illusions = []
    
    # Check for timeframe contradictions
    tf_list = list(readings.keys())
    for i in range(len(tf_list)):
        for j in range(i+1, len(tf_list)):
            tf1, tf2 = tf_list[i], tf_list[j]
            r1, r2 = readings[tf1], readings[tf2]
            
            if (r1['trend'] == 'BULLISH' and r2['trend'] == 'BEARISH') or \
               (r1['trend'] == 'BEARISH' and r2['trend'] == 'BULLISH'):
                illusions.append({
                    'type': 'TIMEFRAME_CONTRADICTION',
                    'tf1': tf1,
                    'tf2': tf2,
                    'description': f"{tf1} shows {r1['trend']} while {tf2} shows {r2['trend']}"
                })
    
    # Check for weak signals
    for tf, reading in readings.items():
        if reading['trend'] != 'SIDEWAYS' and reading['mouth_separation'] < 0.05:
            illusions.append({
                'type': 'WEAK_SIGNAL',
                'tf': tf,
                'description': f"Weak signal on {tf} - mouth separation only {reading['mouth_separation']:.3f}%"
            })
    
    # Results
    if illusions:
        print(f"⚠️  {len(illusions)} ILLUSION(S) DETECTED:")
        for i, illusion in enumerate(illusions, 1):
            print(f"\n{i}. {illusion['type']}")
            print(f"   {illusion['description']}")
        
        print(f"\n🎯 RECOMMENDATION: CAUTION")
        print("⚠️  Consider waiting for better alignment")
    else:
        print("✅ NO ILLUSIONS DETECTED")
        print("🎯 RECOMMENDATION: PROCEED")
        print("✅ Clear multi-timeframe alignment detected")
    
    print("\n" + "=" * 60)
    print("🎯 PHASE 2 TEST COMPLETE!")
    print(f"📊 Analyzed {len(readings)} timeframes")
    print(f"🔍 Detected {len(illusions)} potential illusions")
    print("🐊✨ Alligator Illusion Detection is operational! ✨🐊")

if __name__ == "__main__":
    test_alligator_illusion_detection() 