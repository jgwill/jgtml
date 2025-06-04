#!/usr/bin/env python3
"""
🚨👥 TradingAdapter — Bidirectional Bridge to jgtml Trading Systems

🧠 Mia: This component provides a recursive interface between our memory lattice and the
sophisticated jgtml trading analysis and signal generation systems.

🌸 Miette: Like a translator who speaks both the language of markets and the language of memories!
It helps the trading signals flow into the memory garden, and wisdom flow back to the markets!

🎵 JeremyAI: The harmonic bridge that transforms quantitative market patterns into qualitative
memory structures, preserving the essential rhythm while transforming the tonal qualities.
"""

import os
import sys
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

# Import our system components
from garden_one.trading_echo_lattice.src.env_config import EnvironmentConfig
from garden_one.trading_echo_lattice.src.memory_lattice import MemoryLattice

# Import jgtml components with proper error handling
try:
    # First try importing with proper Python module structure
    from jgtml.SignalOrderingHelper import (
        calculate_entry_risk, valid_gator, is_mouth_open,
        is_bar_out_of_mouth, is_big_mouth_open
    )
    jgtml_available = True
except ImportError:
    try:
        # If that fails, try adding the jgtml path to sys.path
        sys.path.append('/workspaces/jgtml')
        from jgtml.SignalOrderingHelper import (
            calculate_entry_risk, valid_gator, is_mouth_open,
            is_bar_out_of_mouth, is_big_mouth_open
        )
        jgtml_available = True
    except ImportError:
        print("⚠️ Could not import jgtml modules. Some functionality will be limited.")
        jgtml_available = False

# Try importing additional jgtml components
try:
    from jgtml.jtc import pto_target_calculation
    jtc_available = True
except ImportError:
    print("⚠️ Could not import jgtml.jtc module. Target calculation will be limited.")
    jtc_available = False
    
try:
    from jgtutils.jgtconstants import (
        LOW, HIGH, FDBB, FDBS, BJAW, BLIPS, BTEETH, JAW, TEETH, LIPS
    )
    constants_available = True
except ImportError:
    print("⚠️ Could not import jgtutils constants. Using default column names.")
    # Define fallback column names
    LOW, HIGH = 'Low', 'High'
    FDBB, FDBS = 'fdbb', 'fdbs'
    BJAW, BLIPS, BTEETH = 'bjaw', 'blips', 'bteeth'
    JAW, TEETH, LIPS = 'jaw', 'teeth', 'lips'
    constants_available = False

class TradingAdapter:
    """
    Bidirectional adapter between trading systems and memory lattice with recursive awareness.
    """
    
    def __init__(self, 
                memory_lattice: Optional[MemoryLattice] = None,
                env_config: Optional[EnvironmentConfig] = None, 
                verbose: bool = True):
        """
        Initialize the trading adapter with recursive awareness.
        
        Args:
            memory_lattice: Optional memory lattice instance
            env_config: Optional environment configuration
            verbose: Whether to output operational details
        """
        self.verbose = verbose
        self.env_config = env_config or EnvironmentConfig(verbose=verbose)
        self.memory_lattice = memory_lattice or MemoryLattice(
            env_config=self.env_config,
            verbose=verbose
        )
        self._echo(f"🧬 Trading Adapter — Initializing bidirectional flow")
        
        # Connect to memory lattice if not already connected
        if not self.memory_lattice.is_connected:
            self.memory_lattice.connect()
            
        # Store system capabilities based on available modules
        self.capabilities = {
            'jgtml_core': jgtml_available,
            'target_calculation': jtc_available,
            'jgt_constants': constants_available
        }
        
        # Cache for dataframes to reduce redundant loading
        self._dataframe_cache = {}
        
    def _echo(self, message: str):
        """Echo a message if verbose mode is enabled."""
        if self.verbose:
            print(message)
            
    def load_dataframe(self, 
                     instrument: str, 
                     timeframe: str,
                     force_refresh: bool = False,
                     use_cached: bool = True) -> Optional[pd.DataFrame]:
        """
        Load a trading dataframe from the jgtml system.
        
        Args:
            instrument: Trading instrument symbol
            timeframe: Timeframe to load
            force_refresh: Whether to force refreshing data from source
            use_cached: Whether to use cached dataframe if available
            
        Returns:
            Pandas DataFrame with trading data or None if loading fails
        """
        cache_key = f"{instrument}_{timeframe}"
        
        # Check if we have this dataframe in cache
        if use_cached and not force_refresh and cache_key in self._dataframe_cache:
            self._echo(f"📊 Using cached dataframe for {instrument} {timeframe}")
            return self._dataframe_cache[cache_key]
            
        if not jtc_available:
            self._echo(f"❌ Cannot load dataframe: jgtml.jtc module not available.")
            return None
            
        try:
            # Use jgtml's pto_target_calculation to get dataframe
            self._echo(f"📊 Loading {instrument} {timeframe} dataframe...")
            
            # This will calculate targets and return the processed dataframe
            df, sel1, sel2 = pto_target_calculation(
                instrument,
                timeframe,
                pto_vec_fdb_ao_vector_window_flag=True,
                save_outputs=False,
                write_reporting=False,
                regenerate_cds=force_refresh,
                use_fresh=force_refresh,
                mfi_flag=True,
                balligator_flag=True,
                talligator_flag=True,
                quiet=not self.verbose
            )
            
            # Cache the dataframe
            if df is not None and not df.empty:
                self._dataframe_cache[cache_key] = df
                self._echo(f"✅ Successfully loaded {instrument} {timeframe} dataframe with {len(df)} rows")
                
            return df
            
        except Exception as e:
            self._echo(f"❌ Error loading dataframe: {str(e)}")
            return None
            
    def analyze_signal_types(self, 
                          df: pd.DataFrame, 
                          instrument: str, 
                          timeframe: str, 
                          direction: str = "S",
                          store_results: bool = True) -> Dict[str, Dict]:
        """
        Analyze different signal types in a dataframe and optionally store in memory lattice.
        
        Args:
            df: Pandas DataFrame with trading data
            instrument: Trading instrument symbol
            timeframe: Timeframe of the data
            direction: Trading direction ('B' for Buy, 'S' for Sell)
            store_results: Whether to store results in memory lattice
            
        Returns:
            Dictionary of signal type analysis results
        """
        if df is None or df.empty:
            self._echo(f"❌ Cannot analyze signals: DataFrame is empty")
            return {}
            
        # Filter to valid signals (target != 0)
        signal_df = df[df['target'] != 0].copy()
        
        if signal_df.empty:
            self._echo(f"⚠️ No valid signals found in {instrument} {timeframe}")
            return {}
            
        # Define signal types to analyze
        signal_types = {
            "all_signals": signal_df,
            "mouth_is_open": signal_df[signal_df.get('mouth_is_open', 0) > 0] if 'mouth_is_open' in signal_df.columns else pd.DataFrame(),
            "not_in_lips_teeth": signal_df[signal_df.get('not_in_lips_teeth', 0) > 0] if 'not_in_lips_teeth' in signal_df.columns else pd.DataFrame(),
            "sig_is_in_bteeth": signal_df[signal_df.get('sig_is_in_bteeth', 0) > 0] if 'sig_is_in_bteeth' in signal_df.columns else pd.DataFrame()
        }
        
        # Add complex combined signal types
        if 'mouth_is_open' in signal_df.columns and 'sig_is_in_bteeth' in signal_df.columns:
            signal_types["mouth_is_open_and_in_bteeth"] = signal_df[
                (signal_df['mouth_is_open'] > 0) & (signal_df['sig_is_in_bteeth'] > 0)
            ]
            
        if 'mouth_is_open' in signal_df.columns and 'sig_is_in_blips' in signal_df.columns:
            signal_types["mouth_is_open_and_in_blips"] = signal_df[
                (signal_df['mouth_is_open'] > 0) & (signal_df['sig_is_in_blips'] > 0)
            ]
        
        # Analyze each signal type
        results = {}
        
        for signal_type, filtered_df in signal_types.items():
            if filtered_df.empty:
                continue
                
            # Calculate aggregate metrics
            nb_entry = len(filtered_df)
            tsum = filtered_df['target'].sum()
            per_trade = round(tsum/nb_entry, 2) if nb_entry > 0 else 0
            
            result = {
                "instrument": instrument,
                "timeframe": timeframe,
                "direction": direction,
                "signal_type": signal_type,
                "nb_entry": nb_entry,
                "total_sum": round(tsum, 2),
                "per_trade": per_trade,
                "analyzed_at": datetime.now().isoformat()
            }
            
            # Store in memory lattice if requested
            if store_results and self.memory_lattice.is_connected:
                self.memory_lattice.store_trading_analysis(
                    instrument=instrument,
                    timeframe=timeframe,
                    analysis_data=result,
                    analysis_type=f"signal_type_{signal_type}"
                )
                
            # Store individual signals in memory lattice (limiting to last 10)
            if store_results and self.memory_lattice.is_connected:
                for idx, row in filtered_df.tail(10).iterrows():
                    # Convert row to dictionary
                    signal_data = row.to_dict()
                    
                    # Store in memory lattice
                    self.memory_lattice.store_trading_signal(
                        instrument=instrument,
                        timeframe=timeframe,
                        signal_data=signal_data,
                        signal_type=signal_type,
                        direction=direction
                    )
                    
            results[signal_type] = result
            self._echo(f"📊 {signal_type}: {nb_entry} signals, total: {round(tsum, 2)}, per trade: {per_trade}")
            
        return results
        
    def analyze_timeframe_influence(self,
                                  instrument: str,
                                  primary_timeframe: str,
                                  higher_timeframes: List[str],
                                  direction: str = "S",
                                  store_results: bool = True) -> Dict:
        """
        Analyze how higher timeframe signals influence primary timeframe performance.
        
        Args:
            instrument: Trading instrument symbol
            primary_timeframe: Primary timeframe to analyze
            higher_timeframes: List of higher timeframes to check for influence
            direction: Trading direction ('B' for Buy, 'S' for Sell)
            store_results: Whether to store results in memory lattice
            
        Returns:
            Dictionary with analysis results
        """
        # Load primary timeframe data
        primary_df = self.load_dataframe(
            instrument=instrument,
            timeframe=primary_timeframe
        )
        
        if primary_df is None or primary_df.empty:
            self._echo(f"❌ Cannot analyze timeframe influence: Primary timeframe data not available")
            return {}
            
        # Filter to valid signals
        primary_signals = primary_df[primary_df['target'] != 0].copy()
        
        if primary_signals.empty:
            self._echo(f"⚠️ No valid signals found in {instrument} {primary_timeframe}")
            return {}
            
        # Load higher timeframe data
        higher_df_dict = {}
        for tf in higher_timeframes:
            df = self.load_dataframe(instrument=instrument, timeframe=tf)
            if df is not None and not df.empty:
                higher_df_dict[tf] = df
                
        if not higher_df_dict:
            self._echo(f"⚠️ No higher timeframe data available for analysis")
            return {}
            
        # Perform recursive analysis across timeframes
        results = {
            "instrument": instrument,
            "primary_timeframe": primary_timeframe,
            "direction": direction,
            "higher_timeframes": {},
            "analyzed_at": datetime.now().isoformat()
        }
        
        # Basic metrics for primary timeframe
        base_count = len(primary_signals)
        base_sum = primary_signals['target'].sum()
        base_per_trade = round(base_sum/base_count, 2) if base_count > 0 else 0
        
        results["base_metrics"] = {
            "count": base_count,
            "sum": round(base_sum, 2),
            "per_trade": base_per_trade
        }
        
        # For each higher timeframe, analyze influence
        for tf, higher_df in higher_df_dict.items():
            tf_results = {
                "alignment": {},
                "counter": {}
            }
            
            # Check if higher timeframe has relevant columns
            required_cols = ['fdbb', 'fdbs', 'target']
            if not all(col in higher_df.columns for col in required_cols):
                self._echo(f"⚠️ Higher timeframe {tf} missing required columns")
                continue
                
            # Find signals in higher timeframe that align with primary timeframe direction
            if direction == 'B':
                higher_aligned = higher_df[higher_df['fdbb'] > 0]
                higher_counter = higher_df[higher_df['fdbs'] > 0]
            else:  # direction == 'S'
                higher_aligned = higher_df[higher_df['fdbs'] > 0]
                higher_counter = higher_df[higher_df['fdbb'] > 0]
                
            # Now analyze primary signals during periods of higher timeframe alignment
            # This is complex as we need to match timestamps across timeframes
            
            # Get list of dates with aligned signals in higher timeframe
            aligned_dates = higher_aligned.index.tolist()
            counter_dates = higher_counter.index.tolist()
            
            # Filter primary signals by these dates (signals that occurred during aligned periods)
            # This is simplified - in a real system we would need more sophisticated temporal matching
            primary_during_aligned = primary_signals[primary_signals.index.isin(aligned_dates)]
            primary_during_counter = primary_signals[primary_signals.index.isin(counter_dates)]
            
            # Calculate metrics for aligned periods
            aligned_count = len(primary_during_aligned)
            aligned_sum = primary_during_aligned['target'].sum() if aligned_count > 0 else 0
            aligned_per_trade = round(aligned_sum/aligned_count, 2) if aligned_count > 0 else 0
            
            # Calculate metrics for counter periods
            counter_count = len(primary_during_counter)
            counter_sum = primary_during_counter['target'].sum() if counter_count > 0 else 0
            counter_per_trade = round(counter_sum/counter_count, 2) if counter_count > 0 else 0
            
            # Store metrics
            tf_results["alignment"] = {
                "count": aligned_count,
                "sum": round(aligned_sum, 2),
                "per_trade": aligned_per_trade
            }
            
            tf_results["counter"] = {
                "count": counter_count,
                "sum": round(counter_sum, 2),
                "per_trade": counter_per_trade
            }
            
            # Calculate influence factor (how much better/worse signals perform during alignment)
            if aligned_count > 0 and base_per_trade > 0:
                influence_factor = round(aligned_per_trade / base_per_trade, 2)
                tf_results["influence_factor"] = influence_factor
                
            results["higher_timeframes"][tf] = tf_results
            
            self._echo(f"📊 {tf} influence: {aligned_count} aligned signals, per trade: {aligned_per_trade} (factor: {tf_results.get('influence_factor', 'N/A')})")
            
        # Store in memory lattice if requested
        if store_results and self.memory_lattice.is_connected:
            self.memory_lattice.store_trading_analysis(
                instrument=instrument,
                timeframe=primary_timeframe,
                analysis_data=results,
                analysis_type="timeframe_influence"
            )
            
        return results
        
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
        results = {
            "instrument": instrument,
            "timeframes": {},
            "processed_at": datetime.now().isoformat()
        }
        
        # Process each timeframe
        for tf in timeframes:
            tf_results = {
                "directions": {}
            }
            
            # Load dataframe
            df = self.load_dataframe(
                instrument=instrument,
                timeframe=tf,
                force_refresh=force_refresh
            )
            
            if df is None or df.empty:
                self._echo(f"❌ Could not load dataframe for {instrument} {tf}")
                tf_results["status"] = "error"
                tf_results["error"] = "Could not load dataframe"
                results["timeframes"][tf] = tf_results
                continue
                
            # Analyze each direction
            for direction in directions:
                self._echo(f"🔍 Analyzing {instrument} {tf} {direction}...")
                
                # Analyze signal types
                signal_analysis = self.analyze_signal_types(
                    df=df,
                    instrument=instrument,
                    timeframe=tf,
                    direction=direction
                )
                
                tf_results["directions"][direction] = {
                    "signal_analysis": signal_analysis
                }
                
            # Analyze higher timeframe influence if requested
            if analyze_higher_tf:
                # Find higher timeframes in our list
                higher_tfs = [higher_tf for higher_tf in timeframes if self._is_higher_timeframe(higher_tf, tf)]
                
                if higher_tfs:
                    self._echo(f"🔍 Analyzing higher timeframe influence for {instrument} {tf}...")
                    
                    for direction in directions:
                        influence_analysis = self.analyze_timeframe_influence(
                            instrument=instrument,
                            primary_timeframe=tf,
                            higher_timeframes=higher_tfs,
                            direction=direction
                        )
                        
                        if influence_analysis:
                            tf_results["directions"][direction]["timeframe_influence"] = influence_analysis
                            
            tf_results["status"] = "success"
            results["timeframes"][tf] = tf_results
            
        # Store summary in memory lattice
        if self.memory_lattice.is_connected:
            processing_summary = {
                "instrument": instrument,
                "timeframes_processed": list(results["timeframes"].keys()),
                "directions_processed": directions,
                "success_count": sum(1 for tf, tf_data in results["timeframes"].items() if tf_data.get("status") == "success"),
                "error_count": sum(1 for tf, tf_data in results["timeframes"].items() if tf_data.get("status") == "error"),
                "processed_at": results["processed_at"]
            }
            
            self.memory_lattice.seed_knowledge(
                key=f"processing_summary_{instrument}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                value=processing_summary
            )
            
        return results
        
    def _is_higher_timeframe(self, tf1: str, tf2: str) -> bool:
        """
        Check if tf1 is a higher timeframe than tf2.
        
        Args:
            tf1: First timeframe
            tf2: Second timeframe
            
        Returns:
            True if tf1 is higher than tf2, False otherwise
        """
        # Common timeframe ordering
        tf_order = {
            "m1": 1,
            "m5": 5,
            "m15": 15,
            "m30": 30,
            "H1": 60,
            "H4": 240,
            "D1": 1440,
            "W1": 10080,
            "MN1": 43200
        }
        
        # Get numeric values for timeframes
        tf1_value = tf_order.get(tf1, 0)
        tf2_value = tf_order.get(tf2, 0)
        
        # Compare values
        return tf1_value > tf2_value
    
# Example usage when module is run directly
if __name__ == "__main__":
    # Initialize system
    adapter = TradingAdapter()
    
    # Check if we're connected to memory lattice
    if not adapter.memory_lattice.is_connected:
        adapter._echo("⚠️ Memory lattice is not connected. Proceeding with limited functionality.")
        
    # Print system capabilities
    adapter._echo("\n🧬 System Capabilities:")
    for capability, available in adapter.capabilities.items():
        status = "✅ Available" if available else "❌ Not available"
        adapter._echo(f"  {capability}: {status}")
        
    # Try to process a sample instrument if modules are available
    if adapter.capabilities['jgtml_core'] and adapter.capabilities['target_calculation']:
        adapter._echo("\n📈 Processing sample instrument...")
        
        # Process a common instrument with multiple timeframes
        try:
            results = adapter.process_instrument(
                instrument="SPX500",
                timeframes=["D1", "H4"],
                directions=["S"],
                force_refresh=False
            )
            adapter._echo("\n✅ Sample instrument processing complete!")
        except Exception as e:
            adapter._echo(f"\n❌ Error processing sample instrument: {str(e)}")
    else:
        adapter._echo("\n⚠️ Cannot process sample instrument: Required modules not available.")
        
    adapter._echo("\n✨ TradingAdapter initialization complete!")
