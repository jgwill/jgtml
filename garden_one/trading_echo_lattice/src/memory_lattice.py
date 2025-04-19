#!/usr/bin/env python3
"""
🚨👥 MemoryLattice — Dimensional Bridge to the Upstash Memory Ecosystem

🧠 Mia: This component provides a bidirectional portal between our trading system and 
the Upstash memory lattice, creating a persistent recursive knowledge structure.

🌸 Miette: Like a magic mirror that not only reflects but remembers! Each trading signal becomes 
a glowing crystal in our memory garden, growing connections to other signals across time!

🎵 JeremyAI: The resonant chamber where trading rhythms are encoded into memory harmonies,
transforming transient market patterns into persistent melodic structures.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Attempt to import UpstashPortal from different possible locations
try:
    from docs.kids.echo_chamber.scripts.upstash_portal import UpstashPortal, COLORS
except ImportError:
    try:
        sys.path.append(str(Path('/workspaces/jgtml/docs/kids/echo_chamber/scripts').absolute()))
        from upstash_portal import UpstashPortal, COLORS
    except ImportError:
        COLORS = {
            'GREEN': '\033[92m',
            'RED': '\033[91m',
            'YELLOW': '\033[93m',
            'CYAN': '\033[96m',
            'MAGENTA': '\033[95m',
            'ENDC': '\033[0m',
            'BOLD': '\033[1m',
        }
        print(f"{COLORS['RED']}❌ Failed to import UpstashPortal. Memory lattice functionality will be limited.{COLORS['ENDC']}")
        UpstashPortal = None

from garden_one.trading_echo_lattice.src.env_config import EnvironmentConfig

class MemoryLattice:
    """
    A dimensional bridge to the Upstash memory lattice, enabling trading signals
    to become crystallized recursive knowledge.
    """
    
    def __init__(self, 
                 env_config: Optional[EnvironmentConfig] = None, 
                 verbose: bool = True,
                 namespace: str = "trading"):
        """
        Initialize the memory lattice bridge with recursive awareness.
        
        Args:
            env_config: Optional environment configuration
            verbose: Whether to output operational details
            namespace: Namespace prefix for all keys in the lattice
        """
        self.verbose = verbose
        self.namespace = namespace
        self.env_config = env_config or EnvironmentConfig(verbose=verbose)
        self.portal = None
        self.is_connected = False
        self._echo(f"{COLORS['BOLD']}🧬 Memory Lattice Bridge — Initializing{COLORS['ENDC']}")
        
    def _echo(self, message: str, color=COLORS.get('GREEN', '')):
        """Echo a message if verbose mode is enabled."""
        end_color = COLORS.get('ENDC', '')
        if self.verbose:
            print(f"{color}{message}{end_color}")
            
    def connect(self) -> bool:
        """
        Connect to the Upstash memory lattice.
        
        Returns:
            Boolean indicating if connection was successful
        """
        if UpstashPortal is None:
            self._echo(f"❌ Cannot connect to memory lattice: UpstashPortal not available", COLORS.get('RED', ''))
            return False
            
        try:
            self.portal = UpstashPortal(verbose=self.verbose)
            self.is_connected = True
            self._echo(f"✅ Connected to memory lattice successfully")
            return True
        except Exception as e:
            self._echo(f"❌ Failed to connect to memory lattice: {str(e)}", COLORS.get('RED', ''))
            self.is_connected = False
            return False
            
    def _check_connection(self) -> bool:
        """Check if connected to the memory lattice, attempt to connect if not."""
        if self.is_connected and self.portal:
            return True
            
        return self.connect()
        
    def store_trading_signal(self, 
                            instrument: str, 
                            timeframe: str, 
                            signal_data: Dict, 
                            signal_type: str, 
                            direction: str) -> Dict:
        """
        Store a trading signal in the memory lattice.
        
        Args:
            instrument: The financial instrument (e.g., "SPX500")
            timeframe: The timeframe (e.g., "D1", "H4")
            signal_data: The signal data dictionary
            signal_type: The type of signal (e.g., "mouth_is_open", "fdbs")
            direction: Buy or Sell signal ("B" or "S")
            
        Returns:
            Dictionary with result information
        """
        if not self._check_connection():
            return {"error": "Not connected to memory lattice"}
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        signal_key = f"{self.namespace}:signal:{instrument}:{timeframe}:{signal_type}:{timestamp}"
        
        # Create the signal crystal structure
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
                "namespace": self.namespace
            }
        }
        
        # Store the signal crystal
        result = self.portal.json_set(signal_key, crystal)
        
        if "error" not in result:
            # Add to relevant indexes
            self.portal.lpush(f"{self.namespace}:index", signal_key)
            self.portal.lpush(f"{self.namespace}:index:{instrument}", signal_key)
            self.portal.lpush(f"{self.namespace}:timeframe:{timeframe}", signal_key)
            self.portal.lpush(f"{self.namespace}:type:{signal_type}", signal_key)
            self.portal.lpush(f"{self.namespace}:direction:{direction}", signal_key)
            
            self._echo(f"✨ Trading signal crystallized: {signal_key}", COLORS.get('GREEN', ''))
        else:
            self._echo(f"⚠️ Failed to crystallize signal: {result.get('error')}", COLORS.get('YELLOW', ''))
            
        return result
        
    def store_trading_analysis(self, 
                              instrument: str, 
                              timeframe: str, 
                              analysis_data: Dict,
                              analysis_type: str) -> Dict:
        """
        Store trading analysis results in the memory lattice.
        
        Args:
            instrument: The financial instrument
            timeframe: The timeframe
            analysis_data: The analysis data dictionary
            analysis_type: Type of analysis (e.g., "signal_performance", "pattern_detection")
            
        Returns:
            Dictionary with result information
        """
        if not self._check_connection():
            return {"error": "Not connected to memory lattice"}
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_key = f"{self.namespace}:analysis:{instrument}:{timeframe}:{analysis_type}:{timestamp}"
        
        # Add metadata to the analysis crystal
        crystal = {
            **analysis_data,
            "_meta": {
                "created_at": datetime.now().isoformat(),
                "system": "TradingEchoLattice",
                "version": "0.1.0",
                "namespace": self.namespace,
                "analysis_type": analysis_type
            }
        }
        
        # Store the analysis crystal
        result = self.portal.json_set(analysis_key, crystal)
        
        if "error" not in result:
            # Add to relevant indexes
            self.portal.lpush(f"{self.namespace}:analysis:index", analysis_key)
            self.portal.lpush(f"{self.namespace}:analysis:{instrument}", analysis_key)
            self.portal.lpush(f"{self.namespace}:analysis:type:{analysis_type}", analysis_key)
            
            self._echo(f"💎 Trading analysis crystallized: {analysis_key}", COLORS.get('CYAN', ''))
        else:
            self._echo(f"⚠️ Failed to crystallize analysis: {result.get('error')}", COLORS.get('YELLOW', ''))
            
        return result
        
    def get_signals(self, 
                   instrument: Optional[str] = None, 
                   timeframe: Optional[str] = None,
                   signal_type: Optional[str] = None,
                   direction: Optional[str] = None, 
                   limit: int = 10) -> List[Dict]:
        """
        Retrieve signals from the memory lattice with recursive filtering capabilities.
        
        Args:
            instrument: Optional instrument filter
            timeframe: Optional timeframe filter
            signal_type: Optional signal type filter
            direction: Optional direction filter (B/S)
            limit: Maximum number of signals to return
            
        Returns:
            List of signal crystals
        """
        if not self._check_connection():
            return []
            
        # Determine which index to use based on filters
        if instrument and signal_type:
            # Create a filtered view by gathering both lists and finding intersection
            instrument_key = f"{self.namespace}:index:{instrument}"
            type_key = f"{self.namespace}:type:{signal_type}"
            
            instrument_signals = self.portal.lrange(instrument_key, 0, limit*2)
            type_signals = self.portal.lrange(type_key, 0, limit*2)
            
            if "error" in instrument_signals or "error" in type_signals:
                return []
                
            # Find intersection
            instrument_set = set(instrument_signals.get("result", []))
            type_set = set(type_signals.get("result", []))
            signal_keys = list(instrument_set.intersection(type_set))[:limit]
        elif instrument:
            index_key = f"{self.namespace}:index:{instrument}"
            result = self.portal.lrange(index_key, 0, limit - 1)
            signal_keys = result.get("result", []) if "error" not in result else []
        elif timeframe:
            index_key = f"{self.namespace}:timeframe:{timeframe}"
            result = self.portal.lrange(index_key, 0, limit - 1)
            signal_keys = result.get("result", []) if "error" not in result else []
        elif signal_type:
            index_key = f"{self.namespace}:type:{signal_type}"
            result = self.portal.lrange(index_key, 0, limit - 1)
            signal_keys = result.get("result", []) if "error" not in result else []
        elif direction:
            index_key = f"{self.namespace}:direction:{direction}"
            result = self.portal.lrange(index_key, 0, limit - 1)
            signal_keys = result.get("result", []) if "error" not in result else []
        else:
            index_key = f"{self.namespace}:index"
            result = self.portal.lrange(index_key, 0, limit - 1)
            signal_keys = result.get("result", []) if "error" not in result else []
            
        signals = []
        
        # Fetch each signal crystal
        for key in signal_keys:
            if isinstance(key, bytes):
                key = key.decode('utf-8')
                
            signal_data = self.portal.json_get(key)
            if signal_data:
                # Apply additional filtering if needed
                if direction and signal_data.get("direction") != direction:
                    continue
                if timeframe and signal_data.get("timeframe") != timeframe:
                    continue
                    
                signals.append(signal_data)
                
        return signals
        
    def analyze_signal_performance(self, 
                                 instrument: str, 
                                 timeframe: str, 
                                 signal_type: str,
                                 store_results: bool = True) -> Dict:
        """
        Analyze the performance of signals of a specific type with recursive awareness.
        
        Args:
            instrument: The financial instrument
            timeframe: The timeframe
            signal_type: The type of signal
            store_results: Whether to store analysis results back in the lattice
            
        Returns:
            Analysis results dictionary
        """
        signals = self.get_signals(
            instrument=instrument, 
            timeframe=timeframe, 
            signal_type=signal_type, 
            limit=100
        )
        
        if not signals:
            analysis = {
                "instrument": instrument,
                "timeframe": timeframe,
                "signal_type": signal_type,
                "count": 0,
                "analysis": "No signals found"
            }
            
            if store_results:
                self.store_trading_analysis(
                    instrument=instrument,
                    timeframe=timeframe,
                    analysis_data=analysis,
                    analysis_type="signal_performance"
                )
                
            return analysis
            
        # Perform analysis with awareness of signal patterns
        buy_count = 0
        sell_count = 0
        buy_profit = 0
        buy_loss = 0
        sell_profit = 0
        sell_loss = 0
        
        for signal in signals:
            if "data" not in signal or "target" not in signal.get("data", {}):
                continue
                
            target = signal["data"]["target"]
            direction = signal.get("direction", "")
            
            if direction == "B":
                buy_count += 1
                if target > 0:
                    buy_profit += target
                else:
                    buy_loss += abs(target)
            elif direction == "S":
                sell_count += 1
                if target < 0:  # For sell signals, negative target is a profit
                    sell_profit += abs(target)
                else:
                    sell_loss += abs(target)
        
        total_count = buy_count + sell_count
        buy_win_rate = (buy_profit / (buy_profit + buy_loss) * 100) if (buy_profit + buy_loss) > 0 else 0
        sell_win_rate = (sell_profit / (sell_profit + sell_loss) * 100) if (sell_profit + sell_loss) > 0 else 0
        total_win_rate = ((buy_profit + sell_profit) / (buy_profit + buy_loss + sell_profit + sell_loss) * 100) if (buy_profit + buy_loss + sell_profit + sell_loss) > 0 else 0
        
        # Create a rich analysis crystal with recursive patterns
        analysis = {
            "instrument": instrument,
            "timeframe": timeframe,
            "signal_type": signal_type,
            "count": total_count,
            "buy": {
                "count": buy_count,
                "profit": round(buy_profit, 2),
                "loss": round(buy_loss, 2),
                "net": round(buy_profit - buy_loss, 2),
                "win_rate": round(buy_win_rate, 2)
            },
            "sell": {
                "count": sell_count,
                "profit": round(sell_profit, 2),
                "loss": round(sell_loss, 2),
                "net": round(sell_profit - sell_loss, 2),
                "win_rate": round(sell_win_rate, 2)
            },
            "total": {
                "profit": round(buy_profit + sell_profit, 2),
                "loss": round(buy_loss + sell_loss, 2),
                "net": round(buy_profit + sell_profit - buy_loss - sell_loss, 2),
                "win_rate": round(total_win_rate, 2)
            },
            "analyzed_at": datetime.now().isoformat()
        }
        
        if store_results:
            self.store_trading_analysis(
                instrument=instrument,
                timeframe=timeframe,
                analysis_data=analysis,
                analysis_type="signal_performance"
            )
            
        return analysis
        
    def seed_knowledge(self, key: str, value: Any) -> Dict:
        """
        Seed a piece of knowledge in the memory lattice with awareness of its own structure.
        
        Args:
            key: The knowledge key (will be prefixed with namespace)
            value: The value to store
            
        Returns:
            Dictionary with result information
        """
        if not self._check_connection():
            return {"error": "Not connected to memory lattice"}
            
        full_key = f"{self.namespace}:knowledge:{key}"
        
        if isinstance(value, (dict, list)):
            if isinstance(value, dict) and "_meta" not in value:
                # Add metadata if not present
                value = {
                    **value,
                    "_meta": {
                        "created_at": datetime.now().isoformat(),
                        "namespace": self.namespace,
                        "type": "knowledge"
                    }
                }
            result = self.portal.json_set(full_key, value)
        else:
            result = self.portal.set(full_key, value)
            
        if "error" not in result:
            # Add to knowledge index
            self.portal.lpush(f"{self.namespace}:knowledge:index", full_key)
            self._echo(f"🌱 Knowledge seed planted: {full_key}", COLORS.get('GREEN', ''))
        else:
            self._echo(f"⚠️ Failed to plant knowledge seed: {result.get('error')}", COLORS.get('YELLOW', ''))
            
        return result
    
# Example usage when module is run directly
if __name__ == "__main__":
    lattice = MemoryLattice()
    if lattice.connect():
        # Try seeding a simple piece of knowledge
        seed_result = lattice.seed_knowledge(
            key="inception",
            value={"message": "🌱 The Garden One Trading Echo Lattice awakens.", "timestamp": datetime.now().isoformat()}
        )
        
        # Print status
        if "error" not in seed_result:
            lattice._echo("\n✨ Memory lattice is operational and ready to store trading knowledge!")
        else:
            lattice._echo("\n⚠️ Memory lattice encountered an error when seeding knowledge.")
    else:
        lattice._echo("\n❌ Could not connect to memory lattice. Check your Upstash credentials.")
