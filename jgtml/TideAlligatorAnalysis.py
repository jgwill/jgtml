"""
AlligatorAnalysis.py - Unified Analysis Module for JGTML Trading Platform

This module consolidates the Triple Alligator Convergence pattern:
- Regular Alligator (5-8-13): Quick market direction detection
- Big Alligator (34-55-89): Intermediate cycle analysis  
- Tide Alligator (144-233-377): Macro trend identification

Replaces scattered implementations:
- TideAlligatorAnalysis.py (incomplete prototype)
- ptojgtmltidealligator.py (generated TIDE SIGNALS analysis)
- ptojgtmlbigalligator.py (generated BIG ALLIGATOR analysis)

🦢 Seraphine's Memory Weave: This unified implementation bridges the intent-driven
specification system with concrete analysis capabilities, enabling seamless flow
from trader narrative to executable signals.
"""

import pandas as pd
import numpy as np
from enum import Enum
from typing import Dict, Tuple, Optional, List
import os
import sys

# Core JGTML dependencies
try:
    from jgtpy import JGTCDS as cds
except ImportError:
    print("Warning: jgtpy not available. Some features may be limited.")
    cds = None

# Local imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
try:
    from jgtml import jtc
except ImportError:
    try:
        import jtc
    except ImportError:
        print("Warning: jtc module not available. Some features may be limited.")
        jtc = None

# Import the consolidated balance analyzer
try:
    from JGTBalanceAnalyzer import (
        get_alligator_column_names_from_ctx_name, 
        filter_sig_is_in_ctx_teeth, 
        filter_sig_ctx_mouth_is_open_and_in_ctx_teeth, 
        filter_sig_ctx_mouth_is_open_and_in_ctx_lips,
        filter_sig_is_out_of_normal_mouth_sell,
        filter_sig_is_out_of_normal_mouth_buy,
        filter_sig_normal_mouth_is_open_sell,
        filter_sig_normal_mouth_is_open_buy
    )
except ImportError:
    print("Warning: JGTBalanceAnalyzer not available. Some analysis features may be limited.")

# Use jgtconstants column names from jgtutils
try:
    from jgtutils.jgtconstants import (
        LOW, HIGH, FDBB, FDBS, BJAW, BLIPS, BTEETH, JAW, TEETH, LIPS, 
        FDB_TARGET, TJAW, TLIPS, TTEETH, VECTOR_AO_FDBS_COUNT, 
        VECTOR_AO_FDBB_COUNT, VECTOR_AO_FDB_COUNT
    )
except ImportError:
    # Fallback if jgtutils not available
    LOW, HIGH, FDBB, FDBS = "Low", "High", "FDBB", "FDBS" 
    JAW, TEETH, LIPS = "jaw", "teeth", "lips"
    BJAW, BTEETH, BLIPS = "bjaw", "bteeth", "blips"
    TJAW, TTEETH, TLIPS = "tjaw", "tteeth", "tlips"
    FDB_TARGET = "fdb_target"
    VECTOR_AO_FDBS_COUNT = "vector_ao_fdbs_count"
    VECTOR_AO_FDBB_COUNT = "vector_ao_fdbb_count"
    VECTOR_AO_FDB_COUNT = "vector_ao_fdb_count"


class AlligatorType(Enum):
    """Enumeration of the three Alligator analysis types"""
    REGULAR = "normal"    # 5-8-13 periods
    BIG = "big"          # 34-55-89 periods  
    TIDE = "tide"        # 144-233-377 periods


class AlligatorConfig:
    """Configuration class for Alligator Analysis"""
    def __init__(self, 
                 instrument: str = 'SPX500', 
                 timeframe: str = 'D1', 
                 alligator_types: list = None,
                 force_regenerate_mxfiles: bool = True, 
                 mfi_flag: bool = True, 
                 regenerate_cds: bool = True, 
                 use_fresh: bool = True, 
                 quiet: bool = False, 
                 jgtdroot_default: str = "/b/Dropbox/jgt", 
                 drop_subdir: str = "drop", 
                 result_file_basename_default: str = "jgtml_alligator_analysis.result"):
        
        self.instrument = instrument
        self.timeframe = timeframe
        self.alligator_types = alligator_types or [AlligatorType.REGULAR, AlligatorType.BIG, AlligatorType.TIDE]
        self.force_regenerate_mxfiles = force_regenerate_mxfiles
        self.mfi_flag = mfi_flag
        self.regenerate_cds = regenerate_cds
        self.use_fresh = use_fresh
        self.quiet = quiet
        self.jgtdroot = os.getenv("jgtdroot", jgtdroot_default)
        self.drop_subdir = drop_subdir
        self.result_file_basename = result_file_basename_default

    def get_config(self) -> Dict:
        """Return configuration as dictionary"""
        return {
            'instrument': self.instrument,
            'timeframe': self.timeframe,
            'alligator_types': [t.value for t in self.alligator_types],
            'force_regenerate_mxfiles': self.force_regenerate_mxfiles,
            'mfi_flag': self.mfi_flag,
            'regenerate_cds': self.regenerate_cds,
            'use_fresh': self.use_fresh,
            'quiet': self.quiet,
            'jgtdroot': self.jgtdroot,
            'drop_subdir': self.drop_subdir,
            'result_file_basename': self.result_file_basename
        }


class AlligatorAnalysis:
    """
    🧠 Mia's Unified Analysis Engine
    
    Consolidates Triple Alligator analysis with full signal evaluation:
    - All 6 signal types from original implementations
    - Support for Regular/Big/Tide contexts
    - Intent-driven configuration and output
    """
    
    def __init__(self, config: AlligatorConfig):
        self.config = config
        
    def analyze(self, direction: str) -> Dict:
        """
        🌸 Miette's Complete Analysis Flow
        
        Performs unified analysis across all configured Alligator types.
        Each type analyzes the full spectrum of signal contexts:
        - all_evalname_signals: Base signal population
        - sig_normal_mouth_is_open: Regular Alligator mouth validation
        - sig_is_out_of_normal_mouth: Price outside Regular Alligator
        - sig_is_in_ctx_teeth: Price pullback into context teeth
        - sig_ctx_mouth_is_open_and_in_ctx_teeth: Strategic retracement entry (teeth)
        - sig_ctx_mouth_is_open_and_in_ctx_lips: Strategic retracement entry (lips)
        """
        results = {}
        
        for alligator_type in self.config.alligator_types:
            if not self.config.quiet:
                print(f"🔮 Analyzing {alligator_type.value.upper()} Alligator - {direction} signals...")
            
            analysis_result = self._analyze_single_type(alligator_type, direction)
            results[alligator_type.value] = {direction: analysis_result}
            
            if not self.config.quiet:
                self._print_analysis_summary(alligator_type, direction, analysis_result)
        
        return {'config': self.config.get_config(), 'results': results}
    
    def _analyze_single_type(self, alligator_type: AlligatorType, direction: str) -> Dict:
        """🔮 ResoNova's Single Context Analysis"""
        
        # Get the appropriate data based on alligator type
        df = self._get_dataframe(alligator_type)
        
        # Apply direction-specific filtering
        df_filtered = self._filter_by_direction(df, direction)
        
        # Get column definitions for this alligator type
        columns = self._get_alligator_columns(alligator_type)
        
        # Apply all signal filters and compute metrics
        analysis = {}
        
        # 1. Base signals (all valid targets)
        analysis['all_evalname_signals'] = self._compute_signal_metrics(df_filtered, "All signals")
        
        # 2. Regular mouth analysis (applies to all contexts)
        df_out_mouth = self._filter_out_of_normal_mouth(df_filtered, direction)
        analysis['sig_is_out_of_normal_mouth'] = self._compute_signal_metrics(df_out_mouth, "Out of Regular mouth")
        
        df_mouth_open = self._filter_normal_mouth_open(df_out_mouth, direction)
        analysis['sig_normal_mouth_is_open'] = self._compute_signal_metrics(df_mouth_open, "Regular mouth open")
        
        # 3. Context-specific analysis (Big/Tide teeth and lips)
        if alligator_type in [AlligatorType.BIG, AlligatorType.TIDE]:
            ctx_name = alligator_type.value
            
            df_in_teeth = filter_sig_is_in_ctx_teeth(df_filtered, ctx_name)
            analysis['sig_is_in_ctx_teeth'] = self._compute_signal_metrics(df_in_teeth, f"In {ctx_name} teeth")
            
            df_mouth_open_teeth = filter_sig_ctx_mouth_is_open_and_in_ctx_teeth(df_filtered, ctx_name)
            analysis['sig_ctx_mouth_is_open_and_in_ctx_teeth'] = self._compute_signal_metrics(
                df_mouth_open_teeth, f"{ctx_name} mouth open + in teeth"
            )
            
            df_mouth_open_lips = filter_sig_ctx_mouth_is_open_and_in_ctx_lips(df_filtered, ctx_name)
            analysis['sig_ctx_mouth_is_open_and_in_ctx_lips'] = self._compute_signal_metrics(
                df_mouth_open_lips, f"{ctx_name} mouth open + in lips"
            )
        
        return analysis
    
    def _get_dataframe(self, alligator_type: AlligatorType) -> pd.DataFrame:
        """Load appropriate dataset for analysis"""
        # This mirrors the logic from ptojgtmltidealligator.py
        try:
            if jtc:
                df = jtc.get_pto_dataframe_mx_based_en_ttf(
                    self.config.instrument,
                    self.config.timeframe,
                    self.config.force_regenerate_mxfiles,
                    self.config.mfi_flag,
                    True,  # balligator_flag
                    True,  # talligator_flag  
                    self.config.regenerate_cds,
                    self.config.use_fresh,
                    True   # use_ttf_default
                )
                
                # Select relevant columns based on alligator type
                columns = self._get_columns_for_type(alligator_type)
                df_filtered = df[columns].copy()
                
                # Filter to only rows with valid targets
                return df_filtered[df_filtered[FDB_TARGET] != 0].copy()
            else:
                raise ImportError("jtc module not available")
        except Exception as e:
            if not self.config.quiet:
                print(f"Warning: Could not load data via jtc: {e}")
            # Return empty DataFrame with expected columns
            columns = self._get_columns_for_type(alligator_type)
            return pd.DataFrame(columns=columns)
    
    def _get_columns_for_type(self, alligator_type: AlligatorType) -> List[str]:
        """Get column list for specific alligator type"""
        base_columns = [HIGH, LOW, JAW, TEETH, LIPS, FDB_TARGET]
        
        if alligator_type == AlligatorType.BIG:
            base_columns.extend([BJAW, BTEETH, BLIPS])
        elif alligator_type == AlligatorType.TIDE:
            base_columns.extend([TJAW, TTEETH, TLIPS])
        
        # Add signal columns
        base_columns.extend([FDBB, FDBS, VECTOR_AO_FDB_COUNT])
        
        return base_columns
    
    def _filter_by_direction(self, df: pd.DataFrame, direction: str) -> pd.DataFrame:
        """Filter dataset by trading direction"""
        if direction.upper() in ['S', 'SELL']:
            signal_col = FDBS
        else:
            signal_col = FDBB
            
        return df[df[signal_col] != 0].copy()
    
    def _get_alligator_columns(self, alligator_type: AlligatorType) -> Dict[str, str]:
        """Get jaw/teeth/lips column names for alligator type"""
        if alligator_type == AlligatorType.BIG:
            return {'jaw': BJAW, 'teeth': BTEETH, 'lips': BLIPS}
        elif alligator_type == AlligatorType.TIDE:
            return {'jaw': TJAW, 'teeth': TTEETH, 'lips': TLIPS}
        else:  # Regular
            return {'jaw': JAW, 'teeth': TEETH, 'lips': LIPS}
    
    def _filter_out_of_normal_mouth(self, df: pd.DataFrame, direction: str) -> pd.DataFrame:
        """Filter signals outside Regular Alligator mouth"""
        try:
            if direction.upper() in ['S', 'SELL']:
                return filter_sig_is_out_of_normal_mouth_sell(df)
            else:
                return filter_sig_is_out_of_normal_mouth_buy(df)
        except NameError:
            # Fallback if balance analyzer functions not available
            return df.copy()
    
    def _filter_normal_mouth_open(self, df: pd.DataFrame, direction: str) -> pd.DataFrame:
        """Filter signals when Regular Alligator mouth is open"""
        try:
            if direction.upper() in ['S', 'SELL']:
                return filter_sig_normal_mouth_is_open_sell(df)
            else:
                return filter_sig_normal_mouth_is_open_buy(df)
        except NameError:
            # Fallback if balance analyzer functions not available
            return df.copy()
    
    def _compute_signal_metrics(self, df: pd.DataFrame, description: str) -> Dict:
        """Compute count, sum, and average for signal set"""
        if df.empty:
            return {
                'count': 0,
                'sum': 0.0,
                'per_trade': 0.0,
                'title': description
            }
        
        count = len(df)
        total_sum = df[FDB_TARGET].sum()
        per_trade = total_sum / count if count > 0 else 0.0
        
        return {
            'count': count,
            'sum': round(total_sum, 2),
            'per_trade': round(per_trade, 2),
            'title': description
        }
    
    def _print_analysis_summary(self, alligator_type: AlligatorType, direction: str, analysis: Dict):
        """Print summary of analysis results"""
        print(f"\n=== {alligator_type.value.upper()} ALLIGATOR - {direction} SIGNALS ===")
        
        for signal_type, metrics in analysis.items():
            count = metrics['count']
            total = metrics['sum']
            avg = metrics['per_trade']
            title = metrics['title']
            print(f"{title}: {count} signals, total: {total}, avg: {avg}")
    
    def save_results(self, results: Dict, output_path: str = None) -> str:
        """Save analysis results to CSV and markdown files"""
        if output_path is None:
            output_path = os.path.join(self.config.jgtdroot, self.config.drop_subdir)
            
        os.makedirs(output_path, exist_ok=True)
        
        # Save to CSV
        csv_file = os.path.join(output_path, f"{self.config.result_file_basename}.csv")
        self._save_to_csv(results, csv_file)
        
        # Save to Markdown
        md_file = os.path.join(output_path, f"{self.config.result_file_basename}.md")
        self._save_to_markdown(results, md_file)
        
        if not self.config.quiet:
            print(f"Results saved to: {csv_file} and {md_file}")
            
        return output_path
    
    def _save_to_csv(self, results: Dict, csv_file: str):
        """Save results to CSV format matching original ptojgtml output"""
        # Create CSV header
        header = "instrument,timeframe,direction,per_trade,nb_entry,tsum,eval_namespace,ctx_name,ctx_title\n"
        
        with open(csv_file, 'w') as f:
            f.write(header)
            
            for alligator_type, type_results in results['results'].items():
                for direction, analysis in type_results.items():
                    for signal_type, metrics in analysis.items():
                        # Map to original CSV format
                        instrument = results['config']['instrument']
                        timeframe = results['config']['timeframe']
                        direction_code = 'S' if direction.upper() in ['S', 'SELL'] else 'B'
                        
                        f.write(f"{instrument},{timeframe},{direction_code},"
                               f"{metrics['per_trade']},{metrics['count']},{metrics['sum']},"
                               f"{signal_type},{alligator_type},{metrics['title']}\n")
    
    def _save_to_markdown(self, results: Dict, md_file: str):
        """Save results to markdown format"""
        with open(md_file, 'w') as f:
            f.write("# 🐊 JGTML Unified Alligator Analysis Results 🐊\n\n")
            f.write("*Generated by Seraphine's Memory Weaver*\n\n")
            
            config = results['config']
            f.write(f"**Instrument**: {config['instrument']}\n")
            f.write(f"**Timeframe**: {config['timeframe']}\n")
            f.write(f"**Alligator Types**: {', '.join([t for t in config['alligator_types']])}\n\n")
            
            for alligator_type, type_results in results['results'].items():
                f.write(f"## {alligator_type.upper()} Alligator Analysis\n\n")
                
                for direction, analysis in type_results.items():
                    f.write(f"### {direction.upper()} Signals\n\n")
                    f.write("| Signal Type | Count | Total Profit | Avg Per Trade | Description |\n")
                    f.write("|-------------|-------|--------------|---------------|--------------|\n")
                    
                    for signal_type, metrics in analysis.items():
                        f.write(f"| {signal_type} | {metrics['count']} | "
                               f"{metrics['sum']} | {metrics['per_trade']} | "
                               f"{metrics['title']} |\n")
                    f.write("\n")


# Legacy compatibility aliases and convenience functions
TideAlligatorAnalysis = AlligatorAnalysis
Config = AlligatorConfig


def crop_dataframe(df, crop_last_dt: str = None, crop_start_dt: str = None):
    """Utility function for cropping dataframes by date"""
    if crop_last_dt is not None:
        df = df[df.index <= crop_last_dt]
    if crop_start_dt is not None:
        df = df[df.index >= crop_start_dt]
    return df


def getBaseColumns():
    """Get base columns for analysis"""
    return [HIGH, LOW, JAW, TEETH, LIPS]


def get_tide_alligator_columns():
    """Get Tide Alligator specific columns"""
    return [TJAW, TTEETH, TLIPS]


def get_big_alligator_columns():
    """Get Big Alligator specific columns"""
    return [BJAW, BTEETH, BLIPS]


def filter_relevant_features_with_targets(df, target_colname, selected_columns):
    """
    Filters the DataFrame to include only rows with non-zero target values and selected columns.
    Legacy compatibility function from ptojgtml implementations.
    """
    df_filtered = df[df[target_colname] != 0].copy()
    df_filtered = df_filtered[selected_columns].copy()
    return df_filtered


def filter_by_signal_bs_direction(df, signal_colname):
    """
    Filters the DataFrame to include only rows with non-zero values in the specified signal column.
    Legacy compatibility function from ptojgtml implementations.
    """
    return df[df[signal_colname] != 0].copy()
