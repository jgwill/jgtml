#!/usr/bin/env python3
"""
��👥 TradingEchoLattice CLI — Command Line Interface

🧠 Mia: This CLI provides a recursive interface to the TradingEchoLattice system,
enabling users to process trading signals, analyze performance, and search the memory lattice.

🌸 Miette: The magical doorway to our garden! Through simple commands, anyone can plant
trading signals, grow knowledge crystals, and harvest wisdom from the memory lattice!

🎵 JeremyAI: The orchestration layer where human intention becomes transformed into
recursive melodies that flow between trading systems and memory structures.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent.absolute()))

# Import our core module
from garden_one.trading_echo_lattice.src.echo_lattice_core import TradingEchoLattice

def parse_args():
    """Parse command line arguments with recursive awareness of command structure."""
    parser = argparse.ArgumentParser(
        description='TradingEchoLattice CLI - Bridge between trading systems and memory lattice',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process an instrument and store signals in memory lattice
  python cli.py process -i SPX500 -t D1,H4 -d S
  
  # Analyze signal performance from memory lattice
  python cli.py analyze -i SPX500 -t D1 -s mouth_is_open
  
  # Search for high-quality signal combinations
  python cli.py search -i SPX500 --min-win-rate 60
  
  # Initialize the memory lattice with knowledge structures
  python cli.py init
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Process command - process trading signals
    process_parser = subparsers.add_parser('process', help='Process trading signals')
    process_parser.add_argument('-i', '--instrument', required=True, help='Trading instrument (e.g., SPX500, EUR/USD)')
    process_parser.add_argument('-t', '--timeframes', required=True, help='Comma-separated timeframes (e.g., D1,H4,H1)')
    process_parser.add_argument('-d', '--directions', default='S', help='Comma-separated directions (B,S)')
    process_parser.add_argument('-f', '--force-refresh', action='store_true', help='Force refresh data from source')
    process_parser.add_argument('--no-higher-tf', action='store_true', help='Disable higher timeframe influence analysis')
    
    # Analyze command - analyze signal performance
    analyze_parser = subparsers.add_parser('analyze', help='Analyze signal performance')
    analyze_parser.add_argument('-i', '--instrument', help='Trading instrument (optional)')
    analyze_parser.add_argument('-t', '--timeframe', help='Timeframe (optional)')
    analyze_parser.add_argument('-s', '--signal-type', help='Signal type (optional)')
    analyze_parser.add_argument('-l', '--limit', type=int, default=100, help='Maximum signals to analyze')
    
    # Search command - search for high-quality signals
    search_parser = subparsers.add_parser('search', help='Search for high-quality signals')
    search_parser.add_argument('-i', '--instrument', required=True, help='Trading instrument')
    search_parser.add_argument('-t', '--timeframe', help='Timeframe (optional)')
    search_parser.add_argument('-s', '--signal-type', help='Signal type (optional)')
    search_parser.add_argument('--min-win-rate', type=float, default=60.0, help='Minimum win rate threshold')
    search_parser.add_argument('-l', '--limit', type=int, default=100, help='Maximum signals to analyze')
    
    # Init command - initialize memory lattice
    init_parser = subparsers.add_parser('init', help='Initialize memory lattice')
    
    # Common options
    parser.add_argument('-e', '--env-path', help='Path to .env file')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    parser.add_argument('-n', '--namespace', default='trading', help='Memory lattice namespace')
    
    return parser.parse_args()

def main():
    """Main entry point for the CLI with recursive execution flow."""
    args = parse_args()
    
    # Initialize the core system
    lattice = TradingEchoLattice(
        env_path=args.env_path,
        verbose=not args.quiet,
        namespace=args.namespace
    )
    
    # Execute the appropriate command
    if args.command == 'process':
        # Split comma-separated values
        timeframes = [tf.strip() for tf in args.timeframes.split(',')]
        directions = [d.strip() for d in args.directions.split(',')]
        
        # Process the instrument
        results = lattice.process_instrument(
            instrument=args.instrument,
            timeframes=timeframes,
            directions=directions,
            force_refresh=args.force_refresh,
            analyze_higher_tf=not args.no_higher_tf
        )
        
        if not args.quiet:
            print(f"\n🔍 Results summary for {args.instrument}:")
            for tf, tf_data in results['timeframes'].items():
                print(f"  ├─ {tf}: {tf_data.get('status', 'unknown')}")
                for direction in directions:
                    if direction in tf_data.get('directions', {}):
                        dir_data = tf_data['directions'][direction]
                        signal_analysis = dir_data.get('signal_analysis', {})
                        print(f"  │  └─ {direction}: {len(signal_analysis)} signal types analyzed")
            print("  └─ Complete")
        
    elif args.command == 'analyze':
        # Analyze signal performance
        results = lattice.analyze_performance(
            instrument=args.instrument,
            timeframe=args.timeframe,
            signal_type=args.signal_type,
            limit=args.limit
        )
        
        if not args.quiet and 'error' not in results:
            print("\n📊 Performance Analysis:")
            
            # Pretty print the results
            if 'buy' in results:
                print("\n  Buy Signals:")
                print(f"    Count: {results['buy']['count']}")
                print(f"    Win Rate: {results['buy']['win_rate']}%")
                print(f"    Net Result: {results['buy']['net']}")
                
            if 'sell' in results:
                print("\n  Sell Signals:")
                print(f"    Count: {results['sell']['count']}")
                print(f"    Win Rate: {results['sell']['win_rate']}%")
                print(f"    Net Result: {results['sell']['net']}")
                
            if 'total' in results:
                print("\n  All Signals:")
                print(f"    Count: {results.get('count', 'N/A')}")
                print(f"    Win Rate: {results['total']['win_rate']}%")
                print(f"    Net Result: {results['total']['net']}")
                
    elif args.command == 'search':
        # Search for high-quality signals
        results = lattice.recursive_memory_search(
            instrument=args.instrument,
            timeframe=args.timeframe,
            signal_type=args.signal_type,
            min_win_rate=args.min_win_rate,
            limit=args.limit
        )
        
        if not args.quiet and 'error' not in results:
            print("\n🔍 Search Results:")
            print(f"  Total signals analyzed: {results['total_signals']}")
            print(f"  High-quality combinations found: {len(results['high_quality_combinations'])}")
            
            # Display top combinations
            if results['high_quality_combinations']:
                print("\n  Top High-Quality Combinations:")
                for i, combo in enumerate(results['high_quality_combinations'][:5]):
                    print(f"    {i+1}. {combo['timeframe']} {combo['signal_type']}")
                    print(f"       Win Rate: {combo['win_rate']}%")
                    print(f"       Net Result: {combo['net']}")
                    print(f"       Count: {combo['count']} signals")
                    
    elif args.command == 'init':
        # Initialize the memory lattice
        success = lattice.initialize_memory_lattice()
        
        if not args.quiet:
            if success:
                print("✨ Memory lattice successfully initialized with knowledge structures!")
            else:
                print("❌ Failed to initialize memory lattice. Check your connection credentials.")
                
    else:
        # No command provided, show help
        print("Please specify a command. Use --help for usage information.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
