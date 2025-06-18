#!/usr/bin/env python3
"""Real Data Refresh using JGTApp CDS Function
Uses the actual jgtapp.cds() function that generates proper CDS cache"""

import sys
import os
sys.path.append('/src/jgtml')


def refresh_with_jgtapp():
    """Use the real jgtapp.cds() function to refresh data properly"""
    try:
        from jgtml.jgtapp import cds

        instruments = ['EUR/USD', 'GBP/USD', 'XAU/USD']  # Note: using / format for jgtapp
        timeframes = ['H4', 'H1', 'm15']

        print("🚀 REAL DATA REFRESH - Using JGTApp CDS")
        print("=" * 60)

        for instrument in instruments:
            print(f"🔄 Refreshing {instrument}...")

            for tf in timeframes:
                try:
                    print(f"  📊 Generating {instrument} {tf} CDS data...")
                    cds(instrument, tf, use_fresh=True, use_full=True)
                    print(f"  ✅ {instrument} {tf} CDS data generated")
                except Exception as e:
                    print(f"  ❌ {instrument} {tf} failed: {e}")

        print("=" * 60)
        print("✅ Real data refresh completed using jgtapp.cds()")
        return True

    except Exception as e:
        print(f"❌ Real data refresh failed: {e}")
        return False


if __name__ == "__main__":
    refresh_with_jgtapp()
