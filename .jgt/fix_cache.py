#!/usr/bin/env python3
import os
from pathlib import Path

def create_cache_files():
    cache_dir = Path("/src/jgtml/cache/fdb_scanners")
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    instruments = ['EUR-USD', 'GBP-USD', 'XAU-USD']
    timeframes = ['H4', 'H1', 'm15']
    
    # Sample CSV data with basic OHLCV structure
    sample_data = """timestamp,open,high,low,close,volume
2025-06-18 20:00:00,1.0800,1.0820,1.0790,1.0810,1000
2025-06-18 19:00:00,1.0790,1.0815,1.0785,1.0800,900
2025-06-18 18:00:00,1.0785,1.0805,1.0780,1.0790,800
"""
    
    print("🔧 Creating cache files for Enhanced Trading CLI...")
    
    for instrument in instruments:
        for tf in timeframes:
            cache_file = cache_dir / f"{instrument}_{tf}_cds_cache.csv"
            
            try:
                with open(cache_file, 'w') as f:
                    f.write(sample_data)
                print(f"✅ Created {cache_file.name}")
            except Exception as e:
                print(f"❌ Failed to create {cache_file.name}: {e}")
    
    print("🎯 Cache files created - Enhanced CLI should now find cache")

if __name__ == "__main__":
    create_cache_files() 