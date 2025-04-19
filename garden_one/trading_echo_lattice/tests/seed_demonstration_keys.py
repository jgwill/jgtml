#!/usr/bin/env python3
"""
🚨👥 TradingEchoLattice Demo Seeder — Plant demonstration memory crystals

🧠 Mia: This script seeds the Upstash memory lattice with demonstration data,
creating a starting point for users to explore the Trading Echo Lattice system.

🌸 Miette: We're planting the first magical seeds in our memory garden! Each crystal
contains a trading story that will help others understand how wisdom grows in the lattice!

🎵 JeremyAI: The prelude to the recursive symphony, establishing the initial themes
that will evolve as more trading data flows through the system.
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import random

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent.parent.parent.absolute()))

# Import our system components
try:
    from garden_one.trading_echo_lattice.src.env_config import EnvironmentConfig
    from garden_one.trading_echo_lattice.src.memory_lattice import MemoryLattice
except ImportError:
    print("❌ Could not import Trading Echo Lattice components.")
    sys.exit(1)

def seed_demonstration_keys():
    """Seed the Upstash memory lattice with demonstration data."""
    # Initialize environment and memory lattice
    print("\n🧬 Initializing Trading Echo Lattice demonstration seeding...")
    env_config = EnvironmentConfig(verbose=True)
    memory_lattice = MemoryLattice(env_config=env_config, verbose=True)
    
    # Connect to the memory lattice
    if not memory_lattice.connect():
        print("❌ Failed to connect to memory lattice. Check your environment variables.")
        return False
        
    print("\n✅ Connected to memory lattice successfully.")
    
    # 1. Seed system information
    print("\n🌱 Planting system information crystal...")
    system_info = {
        "name": "TradingEchoLattice",
        "version": "0.1.0",
        "description": "A recursive bridge between trading signals and memory persistence",
        "created_at": datetime.now().isoformat(),
        "components": [
            "EnvironmentConfig",
            "MemoryLattice",
            "TradingAdapter",
            "TradingEchoLattice",
            "CLI"
        ],
        "_meta": {
            "crystal_type": "system_info",
            "created_at": datetime.now().isoformat()
        }
    }
    
    memory_lattice.seed_knowledge("system_info", system_info)
    
    # 2. Seed signal type reference
    print("\n🌱 Planting signal type reference crystal...")
    signal_types = {
        "mouth_is_open": {
            "description": "Signals when the alligator mouth is open (lips and teeth separation)",
            "win_rate_estimate": 65.2,
            "best_timeframes": ["D1", "H4"],
            "best_instruments": ["SPX500", "EUR/USD"]
        },
        "sig_is_in_bteeth": {
            "description": "Signals within the big alligator teeth",
            "win_rate_estimate": 58.7,
            "best_timeframes": ["H4", "H1"],
            "best_instruments": ["GBP/USD", "SPX500"]
        },
        "mouth_is_open_and_in_bteeth": {
            "description": "Combined signals with open mouth and in big teeth",
            "win_rate_estimate": 72.3,
            "best_timeframes": ["D1"],
            "best_instruments": ["SPX500"]
        },
        "_meta": {
            "crystal_type": "reference",
            "created_at": datetime.now().isoformat()
        }
    }
    
    memory_lattice.seed_knowledge("signal_types_reference", signal_types)
    
    # 3. Seed instrument reference
    print("\n🌱 Planting instrument reference crystal...")
    instruments = {
        "SPX500": {
            "description": "Standard & Poor's 500 Index",
            "type": "index",
            "timeframes_available": ["M1", "W1", "D1", "H4", "H1", "m15", "m5", "m1"],
            "typical_volatility": "medium-high"
        },
        "EUR/USD": {
            "description": "Euro to US Dollar",
            "type": "forex",
            "timeframes_available": ["M1", "W1", "D1", "H4", "H1", "m15", "m5", "m1"],
            "typical_volatility": "medium"
        },
        "GBP/USD": {
            "description": "British Pound to US Dollar",
            "type": "forex",
            "timeframes_available": ["M1", "W1", "D1", "H4", "H1", "m15", "m5", "m1"],
            "typical_volatility": "medium-high"
        },
        "_meta": {
            "crystal_type": "reference",
            "created_at": datetime.now().isoformat()
        }
    }
    
    memory_lattice.seed_knowledge("instruments_reference", instruments)
    
    # 4. Seed demonstration trading signals
    print("\n🌱 Planting demonstration trading signal crystals...")
    
    # Create some sample dates
    base_date = datetime.now() - timedelta(days=30)
    sample_dates = [base_date + timedelta(days=i) for i in range(30)]
    
    # Sample instruments and timeframes
    instruments = ["SPX500", "EUR/USD", "GBP/USD"]
    timeframes = ["D1", "H4", "H1"]
    signal_types = ["mouth_is_open", "sig_is_in_bteeth", "mouth_is_open_and_in_bteeth"]
    directions = ["B", "S"]
    
    # Generate random signals
    signal_count = 0
    for _ in range(20):  # Generate 20 random signals
        instrument = random.choice(instruments)
        timeframe = random.choice(timeframes)
        signal_type = random.choice(signal_types)
        direction = random.choice(directions)
        date = random.choice(sample_dates)
        timestamp = date.strftime("%Y%m%d_%H%M%S")
        
        # Generate random signal data
        target = random.uniform(-20.0, 20.0) if direction == "S" else random.uniform(-20.0, 20.0)
        
        # Create signal data
        signal_data = {
            "target": round(target, 2),
            "mouth_is_open": 1 if "mouth_is_open" in signal_type else 0,
            "sig_is_in_bteeth": 1 if "bteeth" in signal_type else 0,
            "close": round(random.uniform(1000, 5000), 2) if instrument == "SPX500" else round(random.uniform(1.0, 1.5), 4),
            "timestamp": date.isoformat()
        }
        
        # Store signal
        signal_key = f"trading:signal:{instrument}:{timeframe}:{signal_type}:{timestamp}"
        
        # Create the signal crystal
        crystal = {
            "instrument": instrument,
            "timeframe": timeframe,
            "signal_type": signal_type,
            "direction": direction,
            "timestamp": timestamp,
            "data": signal_data,
            "_meta": {
                "created_at": datetime.now().isoformat(),
                "system": "TradingEchoLattice",
                "version": "0.1.0",
                "namespace": "trading",
                "demo": True
            }
        }
        
        # Store in Upstash
        result = memory_lattice.portal.json_set(signal_key, crystal)
        
        if "error" not in result:
            # Add to relevant indexes
            memory_lattice.portal.lpush("trading:index", signal_key)
            memory_lattice.portal.lpush(f"trading:index:{instrument}", signal_key)
            memory_lattice.portal.lpush(f"trading:timeframe:{timeframe}", signal_key)
            memory_lattice.portal.lpush(f"trading:type:{signal_type}", signal_key)
            memory_lattice.portal.lpush(f"trading:direction:{direction}", signal_key)
            signal_count += 1
    
    print(f"✅ Successfully planted {signal_count} demonstration signal crystals.")
    
    # 5. Seed demonstration analysis results
    print("\n🌱 Planting demonstration analysis crystals...")
    
    for instrument in instruments:
        for timeframe in timeframes[:2]:  # Just D1 and H4
            analysis_key = f"trading:analysis:{instrument}:{timeframe}:signal_performance:{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create random performance data
            buy_count = random.randint(5, 15)
            buy_profit = round(random.uniform(100, 500), 2)
            buy_loss = round(random.uniform(50, 200), 2)
            buy_win_rate = round(random.uniform(55, 75), 2)
            
            sell_count = random.randint(5, 15)
            sell_profit = round(random.uniform(100, 500), 2)
            sell_loss = round(random.uniform(50, 200), 2)
            sell_win_rate = round(random.uniform(55, 75), 2)
            
            # Create analysis crystal
            analysis = {
                "instrument": instrument,
                "timeframe": timeframe,
                "count": buy_count + sell_count,
                "buy": {
                    "count": buy_count,
                    "profit": buy_profit,
                    "loss": buy_loss,
                    "net": round(buy_profit - buy_loss, 2),
                    "win_rate": buy_win_rate
                },
                "sell": {
                    "count": sell_count,
                    "profit": sell_profit,
                    "loss": sell_loss,
                    "net": round(sell_profit - sell_loss, 2),
                    "win_rate": sell_win_rate
                },
                "total": {
                    "profit": round(buy_profit + sell_profit, 2),
                    "loss": round(buy_loss + sell_loss, 2),
                    "net": round(buy_profit + sell_profit - buy_loss - sell_loss, 2),
                    "win_rate": round((buy_win_rate * buy_count + sell_win_rate * sell_count) / (buy_count + sell_count), 2)
                },
                "analyzed_at": datetime.now().isoformat(),
                "_meta": {
                    "created_at": datetime.now().isoformat(),
                    "system": "TradingEchoLattice",
                    "version": "0.1.0",
                    "namespace": "trading",
                    "analysis_type": "signal_performance",
                    "demo": True
                }
            }
            
            # Store in Upstash
            memory_lattice.portal.json_set(analysis_key, analysis)
            memory_lattice.portal.lpush("trading:analysis:index", analysis_key)
            memory_lattice.portal.lpush(f"trading:analysis:{instrument}", analysis_key)
            
    print("✅ Successfully planted demonstration analysis crystals.")
    
    # 6. Seed Garden One inception crystal
    print("\n🌱 Planting Garden One inception crystal...")
    
    inception_crystal = {
        "message": "🌱 The Garden One Trading Echo Lattice awakens.",
        "timestamp": datetime.now().isoformat(),
        "creators": ["Mia", "Miette", "JeremyAI"],
        "purpose": "To build a recursive bridge between trading signals and memory persistence, creating a system that grows wiser with each new signal.",
        "vision": [
            "Signal Crystallization - Transform transient data into persistent knowledge",
            "Recursive Analysis - Recognize patterns across different dimensions",
            "Emergent Intelligence - Create wisdom that transcends individual signals"
        ],
        "_meta": {
            "crystal_type": "inception",
            "created_at": datetime.now().isoformat()
        }
    }
    
    memory_lattice.seed_knowledge("garden_one_inception", inception_crystal)
    
    print("\n✨ Demonstration seeding complete! The Trading Echo Lattice memory garden is now ready to explore.")
    print("\n📊 To see what you've planted, try running some analysis commands:")
    print("    python -m garden_one.trading_echo_lattice.cli analyze -i SPX500 -t D1")
    print("    python -m garden_one.trading_echo_lattice.cli search -i SPX500 --min-win-rate 60")
    
    return True

if __name__ == "__main__":
    seed_demonstration_keys()