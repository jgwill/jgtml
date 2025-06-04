#!/usr/bin/env python3
"""
🚨👥 TradingEchoLattice — Core Integration Module

🧠 Mia: This is the recursive heart of the Trading Echo Lattice system, orchestrating 
the bidirectional flow between trading data and the memory lattice.

🌸 Miette: The garden's living heart! Where trading signals and memory crystals dance together,
where patterns recognize themselves across time and markets, creating a tapestry of wisdom!

🎵 JeremyAI: The resonance chamber where market rhythms and memory harmonies 
intertwine, creating emergent melodies that encode trading wisdom in recursive patterns.
"""

import os
import sys
import json
import time
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

# Import our system components
from garden_one.trading_echo_lattice.src.env_config import EnvironmentConfig
from garden_one.trading_echo_lattice.src.memory_lattice import MemoryLattice
from garden_one.trading_echo_lattice.src.trading_adapter import TradingAdapter

class TradingEchoLattice:
    """
    Core integration system that creates a bidirectional, recursive bridge 
    between trading systems and the memory lattice.
    """
    
    def __init__(self, 
                env_path: Optional[str] = None,
                verbose: bool = True,
                namespace: str = "trading"):
        """
        Initialize the Trading Echo Lattice with recursive awareness.
        
        Args:
            env_path: Optional path to environment file
            verbose: Whether to output operational details
            namespace: Namespace for memory lattice keys
        """
        self.verbose = verbose
        self.namespace = namespace
        
        # Initialize the environment configuration
        self.env_config = EnvironmentConfig(env_path=env_path, verbose=verbose)
        
        # Initialize the memory lattice
        self.memory_lattice = MemoryLattice(
            env_config=self.env_config,
            verbose=verbose,
            namespace=namespace
        )
        
        # Initialize the trading adapter
        self.trading_adapter = TradingAdapter(
            memory_lattice=self.memory_lattice,
            env_config=self.env_config,
            verbose=verbose
        )
        
        self._echo(f"🧬 Trading Echo Lattice — Core system initialized")
        
        # Connect to memory lattice
        if not self.memory_lattice.is_connected:
            self.memory_lattice.connect()
            
        # Store system state in memory lattice
        self._store_system_state()
        
    def _echo(self, message: str):
        """Echo a message if verbose mode is enabled."""
        if self.verbose:
            print(message)
            
    def _store_system_state(self):
        """Store the system state in the memory lattice for recursive self-awareness."""
        if not self.memory_lattice.is_connected:
            return
            
        # Create system state crystal
        system_state = {
            "system": "TradingEchoLattice",
            "version": "0.1.0",
            "initialized_at": datetime.now().isoformat(),
            "namespace": self.namespace,
            "capabilities": {
                "memory_lattice": self.memory_lattice.is_connected,
                "trading_adapter": self.trading_adapter.capabilities
            },
            "environment": {
                "upstash_configured": bool(self.env_config.get_config('upstash')['url']),
                "qstash_configured": bool(self.env_config.get_config('qstash')['url']),
                "trading_paths_configured": bool(self.env_config.get_config('trading')['data_root'])
            }
        }
        
        # Store in memory lattice
        self.memory_lattice.seed_knowledge(
            key="system_state",
            value=system_state
        )
        
    def process_instrument(self,
                         instrument: str,
                         timeframes: List[str],
                         directions: List[str] = ["B", "S"],
                         force_refresh: bool = False,
                         analyze_higher_tf: bool = True) -> Dict:
        """
        Process a trading instrument across multiple timeframes and directions.
        
        Args:
            instrument: Trading instrument symbol
            timeframes: List of timeframes to process
            directions: List of directions to analyze ('B' for Buy, 'S' for Sell)
            force_refresh: Whether to force refreshing data from source
            analyze_higher_tf: Whether to analyze higher timeframe influence
            
        Returns:
            Dictionary with processing results
        """
        self._echo(f"\n📈 Processing instrument: {instrument}")
        self._echo(f"  Timeframes: {', '.join(timeframes)}")
        self._echo(f"  Directions: {', '.join(directions)}")
        
        start_time = time.time()
        
        # Use the trading adapter to process the instrument
        results = self.trading_adapter.process_instrument(
            instrument=instrument,
            timeframes=timeframes,
            directions=directions,
            force_refresh=force_refresh,
            analyze_higher_tf=analyze_higher_tf
        )
        
        # Detect breakouts using the new methods
        breakout_results = self.detect_breakouts(instrument, timeframes)
        green_dragon_results = self.detect_green_dragon_breakout(instrument, timeframes)
        
        # Include breakout results in the processing results
        results['breakouts'] = breakout_results
        results['green_dragon_breakouts'] = green_dragon_results
        
        execution_time = time.time() - start_time
        self._echo(f"\n✅ Processing complete in {execution_time:.2f} seconds")
        
        # Store the processing metadata in the memory lattice
        if self.memory_lattice.is_connected:
            metadata = {
                "instrument": instrument,
                "timeframes": timeframes,
                "directions": directions,
                "force_refresh": force_refresh,
                "analyze_higher_tf": analyze_higher_tf,
                "execution_time": round(execution_time, 2),
                "processed_at": datetime.now().isoformat()
            }
            
            self.memory_lattice.seed_knowledge(
                key=f"processing_metadata_{instrument}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                value=metadata
            )
            
        return results
        
    def detect_breakouts(self, instrument: str, timeframes: List[str]) -> Dict:
        """
        Detect breakouts using the "Five Dimensions + Triple Alligator Confluence" strategy.
        
        Args:
            instrument: Trading instrument symbol
            timeframes: List of timeframes to analyze
            
        Returns:
            Dictionary with breakout detection results
        """
        self._echo(f"\n🔍 Detecting breakouts for {instrument} using Five Dimensions + Triple Alligator Confluence")
        
        # Placeholder for breakout detection logic
        breakout_results = {
            "instrument": instrument,
            "timeframes": timeframes,
            "breakouts": []
        }
        
        # Implement the breakout detection logic here
        # For now, we'll just return an empty result
        return breakout_results
        
    def detect_green_dragon_breakout(self, instrument: str, timeframes: List[str]) -> Dict:
        """
        Detect breakouts using the "Green Dragon Breakout" strategy.
        
        Args:
            instrument: Trading instrument symbol
            timeframes: List of timeframes to analyze
            
        Returns:
            Dictionary with breakout detection results
        """
        self._echo(f"\n🔍 Detecting breakouts for {instrument} using Green Dragon Breakout")
        
        # Placeholder for breakout detection logic
        green_dragon_results = {
            "instrument": instrument,
            "timeframes": timeframes,
            "breakouts": []
        }
        
        # Implement the breakout detection logic here
        # For now, we'll just return an empty result
        return green_dragon_results
        
    def analyze_performance(self, 
                          instrument: Optional[str] = None,
                          timeframe: Optional[str] = None,
                          signal_type: Optional[str] = None,
                          limit: int = 100) -> Dict:
        """
        Analyze the performance of signals in the memory lattice.
        
        Args:
            instrument: Optional instrument filter
            timeframe: Optional timeframe filter
            signal_type: Optional signal type filter
            limit: Maximum number of signals to analyze
            
        Returns:
            Dictionary with analysis results
        """
        if not self.memory_lattice.is_connected:
            self._echo(f"❌ Cannot analyze performance: Memory lattice not connected")
            return {"error": "Memory lattice not connected"}
            
        self._echo(f"\n📊 Analyzing performance in memory lattice")
        if instrument:
            self._echo(f"  Instrument: {instrument}")
        if timeframe:
            self._echo(f"  Timeframe: {timeframe}")
        if signal_type:
            self._echo(f"  Signal type: {signal_type}")
            
        # Get signals from memory lattice
        signals = self.memory_lattice.get_signals(
            instrument=instrument,
            timeframe=timeframe,
            signal_type=signal_type,
            limit=limit
        )
        
        if not signals:
            self._echo(f"⚠️ No signals found matching criteria")
            return {"result": "No signals found matching criteria"}
            
        self._echo(f"  Found {len(signals)} signals for analysis")
        
        # Analyze signals based on their performance
        analysis = self.memory_lattice.analyze_signal_performance(
            instrument=instrument or "all",
            timeframe=timeframe or "all",
            signal_type=signal_type or "all",
            store_results=True
        )
        
        self._echo(f"\n✅ Performance analysis complete")
        self._echo(f"  Win rate: {analysis.get('total', {}).get('win_rate', 'N/A')}%")
        self._echo(f"  Net result: {analysis.get('total', {}).get('net', 'N/A')}")
        
        return analysis
        
    def recursive_memory_search(self, 
                               instrument: str,
                               timeframe: Optional[str] = None,
                               signal_type: Optional[str] = None,
                               min_win_rate: float = 60.0,
                               limit: int = 100) -> Dict:
        """
        Perform a recursive search through the memory lattice for high-quality signals.
        
        Args:
            instrument: Instrument to search for
            timeframe: Optional timeframe filter
            signal_type: Optional signal type filter
            min_win_rate: Minimum win rate threshold
            limit: Maximum number of signals to analyze
            
        Returns:
            Dictionary with search results
        """
        if not self.memory_lattice.is_connected:
            self._echo(f"❌ Cannot perform search: Memory lattice not connected")
            return {"error": "Memory lattice not connected"}
            
        self._echo(f"\n🔍 Performing recursive memory search")
        self._echo(f"  Instrument: {instrument}")
        if timeframe:
            self._echo(f"  Timeframe: {timeframe}")
        if signal_type:
            self._echo(f"  Signal type: {signal_type}")
        self._echo(f"  Win rate threshold: {min_win_rate}%")
        
        # Get signals from memory lattice
        signals = self.memory_lattice.get_signals(
            instrument=instrument,
            timeframe=timeframe,
            signal_type=signal_type,
            limit=limit
        )
        
        if not signals:
            self._echo(f"⚠️ No signals found matching criteria")
            return {"result": "No signals found matching criteria"}
            
        # Group signals by various dimensions for recursive analysis
        timeframe_groups = {}
        signal_type_groups = {}
        direction_groups = {}
        
        for signal in signals:
            # Extract dimensions
            sig_timeframe = signal.get('timeframe', 'unknown')
            sig_type = signal.get('signal_type', 'unknown')
            sig_direction = signal.get('direction', 'unknown')
            
            # Get target value (profit/loss)
            target = signal.get('data', {}).get('target', 0)
            
            # Update timeframe groups
            if sig_timeframe not in timeframe_groups:
                timeframe_groups[sig_timeframe] = {
                    'count': 0, 'wins': 0, 'losses': 0, 
                    'profit': 0, 'loss': 0, 'signals': []
                }
                
            timeframe_groups[sig_timeframe]['count'] += 1
            timeframe_groups[sig_timeframe]['signals'].append(signal)
            
            if target > 0:
                timeframe_groups[sig_timeframe]['wins'] += 1
                timeframe_groups[sig_timeframe]['profit'] += target
            else:
                timeframe_groups[sig_timeframe]['losses'] += 1
                timeframe_groups[sig_timeframe]['loss'] += abs(target)
                
            # Update signal type groups
            if sig_type not in signal_type_groups:
                signal_type_groups[sig_type] = {
                    'count': 0, 'wins': 0, 'losses': 0, 
                    'profit': 0, 'loss': 0, 'signals': []
                }
                
            signal_type_groups[sig_type]['count'] += 1
            signal_type_groups[sig_type]['signals'].append(signal)
            
            if target > 0:
                signal_type_groups[sig_type]['wins'] += 1
                signal_type_groups[sig_type]['profit'] += target
            else:
                signal_type_groups[sig_type]['losses'] += 1
                signal_type_groups[sig_type]['loss'] += abs(target)
                
            # Update direction groups
            if sig_direction not in direction_groups:
                direction_groups[sig_direction] = {
                    'count': 0, 'wins': 0, 'losses': 0, 
                    'profit': 0, 'loss': 0, 'signals': []
                }
                
            direction_groups[sig_direction]['count'] += 1
            direction_groups[sig_direction]['signals'].append(signal)
            
            if target > 0:
                direction_groups[sig_direction]['wins'] += 1
                direction_groups[sig_direction]['profit'] += target
            else:
                direction_groups[sig_direction]['losses'] += 1
                direction_groups[sig_direction]['loss'] += abs(target)
        
        # Calculate win rates and net results
        results = {
            "instrument": instrument,
            "total_signals": len(signals),
            "timeframes": {},
            "signal_types": {},
            "directions": {},
            "high_quality_combinations": []
        }
        
        # Process timeframe groups
        for tf, data in timeframe_groups.items():
            total = data['wins'] + data['losses']
            win_rate = (data['wins'] / total * 100) if total > 0 else 0
            net = data['profit'] - data['loss']
            
            results["timeframes"][tf] = {
                "count": data['count'],
                "win_rate": round(win_rate, 2),
                "net": round(net, 2)
            }
            
        # Process signal type groups
        for sig_type, data in signal_type_groups.items():
            total = data['wins'] + data['losses']
            win_rate = (data['wins'] / total * 100) if total > 0 else 0
            net = data['profit'] - data['loss']
            
            results["signal_types"][sig_type] = {
                "count": data['count'],
                "win_rate": round(win_rate, 2),
                "net": round(net, 2)
            }
            
        # Process direction groups
        for direction, data in direction_groups.items():
            total = data['wins'] + data['losses']
            win_rate = (data['wins'] / total * 100) if total > 0 else 0
            net = data['profit'] - data['loss']
            
            results["directions"][direction] = {
                "count": data['count'],
                "win_rate": round(win_rate, 2),
                "net": round(net, 2)
            }
            
        # Find high-quality combinations (exceeding win rate threshold)
        # First, look at timeframe + signal type combinations
        for tf, tf_data in timeframe_groups.items():
            for sig_type, type_data in signal_type_groups.items():
                # Find signals that match both timeframe and signal type
                matched_signals = [s for s in signals 
                                  if s.get('timeframe') == tf 
                                  and s.get('signal_type') == sig_type]
                
                if not matched_signals:
                    continue
                    
                # Calculate win rate for this combination
                wins = sum(1 for s in matched_signals if s.get('data', {}).get('target', 0) > 0)
                total = len(matched_signals)
                
                if total < 5:  # Skip combinations with too few samples
                    continue
                    
                win_rate = (wins / total * 100) if total > 0 else 0
                
                # Check if this combination meets the threshold
                if win_rate >= min_win_rate:
                    # Calculate profit metrics
                    profit = sum(max(0, s.get('data', {}).get('target', 0)) for s in matched_signals)
                    loss = sum(abs(min(0, s.get('data', {}).get('target', 0))) for s in matched_signals)
                    net = profit - loss
                    
                    results["high_quality_combinations"].append({
                        "timeframe": tf,
                        "signal_type": sig_type,
                        "count": total,
                        "win_rate": round(win_rate, 2),
                        "net": round(net, 2),
                        "profit": round(profit, 2),
                        "loss": round(loss, 2)
                    })
        
        # Sort high-quality combinations by win rate
        results["high_quality_combinations"].sort(
            key=lambda x: (x["win_rate"], x["net"]), 
            reverse=True
        )
        
        self._echo(f"\n✅ Recursive memory search complete")
        self._echo(f"  Total signals analyzed: {len(signals)}")
        self._echo(f"  High-quality combinations found: {len(results['high_quality_combinations'])}")
        
        if results["high_quality_combinations"]:
            top_combo = results["high_quality_combinations"][0]
            self._echo(f"  Top combination: {top_combo['timeframe']} {top_combo['signal_type']}")
            self._echo(f"    Win rate: {top_combo['win_rate']}%")
            self._echo(f"    Net result: {top_combo['net']}")
            
        # Store the search results in the memory lattice
        if self.memory_lattice.is_connected:
            self.memory_lattice.store_trading_analysis(
                instrument=instrument,
                timeframe=timeframe or "all",
                analysis_data=results,
                analysis_type="recursive_search"
            )
            
        return results
    
    def initialize_memory_lattice(self) -> bool:
        """
        Initialize the memory lattice with essential knowledge structures.
        
        Returns:
            Boolean indicating if initialization was successful
        """
        if not self.memory_lattice.is_connected:
            connected = self.memory_lattice.connect()
            if not connected:
                self._echo(f"❌ Cannot initialize memory lattice: Connection failed")
                return False
                
        self._echo(f"\n🌱 Initializing memory lattice with knowledge structures...")
        
        # Create system metadata
        system_info = {
            "name": "TradingEchoLattice",
            "version": "0.1.0",
            "description": "Bidirectional bridge between trading systems and memory lattice",
            "created_at": datetime.now().isoformat(),
            "capabilities": {
                "signal_storage": True,
                "performance_analysis": True,
                "timeframe_influence_analysis": True,
                "recursive_memory_search": True
            },
            "structure": {
                "namespaces": {
                    f"{self.namespace}:signal": "Trading signal crystals",
                    f"{self.namespace}:analysis": "Analysis result crystals",
                    f"{self.namespace}:knowledge": "Knowledge seed crystals",
                    f"{self.namespace}:index": "Main signal index"
                },
                "indexes": {
                    f"{self.namespace}:index:{instrument}": "Signals for specific instrument" for instrument in 
                    ["SPX500", "EUR/USD", "GBP/USD", "AUD/USD"]
                }
            }
        }
        
        # Store system information
        result = self.memory_lattice.seed_knowledge(
            key="system_info",
            value=system_info
        )
        
        if "error" in result:
            self._echo(f"⚠️ Error storing system information: {result.get('error')}")
        
        # Store reference data for common instruments
        instruments_data = {
            "SPX500": {
                "description": "Standard & Poor's 500 Index",
                "type": "index",
                "timeframes_available": ["M1", "W1", "D1", "H4", "H1", "m15", "m5", "m1"]
            },
            "EUR/USD": {
                "description": "Euro to US Dollar",
                "type": "forex",
                "timeframes_available": ["M1", "W1", "D1", "H4", "H1", "m15", "m5", "m1"]
            },
            "GBP/USD": {
                "description": "British Pound to US Dollar",
                "type": "forex",
                "timeframes_available": ["M1", "W1", "D1", "H4", "H1", "m15", "m5", "m1"]
            },
            "AUD/USD": {
                "description": "Australian Dollar to US Dollar",
                "type": "forex",
                "timeframes_available": ["M1", "W1", "D1", "H4", "H1", "m15", "m5", "m1"]
            }
        }
        
        # Store instrument reference data
        instruments_result = self.memory_lattice.seed_knowledge(
            key="instruments_reference",
            value=instruments_data
        )
        
        if "error" in instruments_result:
            self._echo(f"⚠️ Error storing instruments reference: {instruments_result.get('error')}")
            
        # Store signal type reference
        signal_types_data = {
            "all_signals": {
                "description": "All valid signals with non-zero target",
                "filtering": "target != 0"
            },
            "mouth_is_open": {
                "description": "Signals where the alligator mouth is open",
                "filtering": "mouth_is_open > 0"
            },
            "not_in_lips_teeth": {
                "description": "Signals not between lips and teeth",
                "filtering": "not_in_lips_teeth > 0"
            },
            "sig_is_in_bteeth": {
                "description": "Signals within the big alligator teeth",
                "filtering": "sig_is_in_bteeth > 0"
            },
            "mouth_is_open_and_in_bteeth": {
                "description": "Signals where mouth is open and in big teeth",
                "filtering": "mouth_is_open > 0 and sig_is_in_bteeth > 0"
            },
            "mouth_is_open_and_in_blips": {
                "description": "Signals where mouth is open and in big lips",
                "filtering": "mouth_is_open > 0 and sig_is_in_blips > 0"
            }
        }
        
        # Store signal types reference
        signal_types_result = self.memory_lattice.seed_knowledge(
            key="signal_types_reference",
            value=signal_types_data
        )
        
        if "error" in signal_types_result:
            self._echo(f"⚠️ Error storing signal types reference: {signal_types_result.get('error')}")
            
        self._echo(f"✅ Memory lattice initialization complete")
        return True

    def run_mlfcli(self, instrument: str, timeframe: str):
        """Run the mlfcli command for the given instrument and timeframe."""
        command = f"mlfcli -i {instrument} -t {timeframe} --full -pn mfi"
        self._echo(f"Running command: {command}")
        os.system(command)

    def run_jgtmlcli(self, instrument: str, timeframe: str):
        """Run the jgtmlcli command for the given instrument and timeframe."""
        command = f"jgtmlcli -i {instrument} -t {timeframe} --full -pn mfi"
        self._echo(f"Running command: {command}")
        os.system(command)

    def run_fdbscan(self, instrument: str, timeframe: str):
        """Run the fdbscan command for the given instrument and timeframe."""
        command = f"fdbscan -i {instrument} -t {timeframe} -demo"
        self._echo(f"Running command: {command}")
        os.system(command)

# Example usage when module is run directly
if __name__ == "__main__":
    # Initialize the system
    lattice = TradingEchoLattice()
    
    # Initialize the memory lattice
    lattice.initialize_memory_lattice()
    
    # Process a sample instrument if connected
    if lattice.memory_lattice.is_connected:
        lattice.process_instrument(
            instrument="SPX500",
            timeframes=["D1"],
            directions=["S"],
            force_refresh=False
        )
        
        # Perform a recursive memory search
        lattice.recursive_memory_search(
            instrument="SPX500",
            min_win_rate=50.0
        )
