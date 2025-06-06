#!/usr/bin/env python
"""
🚀 FDBSignal Quality Predictor

This module evaluates the quality of FDBSignals using ML-discovered TTF patterns.
It bridges the gap between the TTF→MLF→MX pipeline and real-time signal evaluation.

Architecture:
- Loads historical MX target data to understand pattern→profit relationships
- Applies ML insights to evaluate incoming FDBSignals in real-time
- Returns a quality score (0-100) indicating signal profitability potential

Usage:
    predictor = FDBSignalQualityPredictor()
    quality_score = predictor.evaluate_signal(instrument, timeframe, signal_data)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

# Import existing JGTML infrastructure
from mlutils import get_outfile_fullpath
from mlconstants import MX_NS
from mldatahelper import read_mlf_for_pattern
import jtc

class FDBSignalQualityPredictor:
    """
    Evaluates FDBSignal quality using ML-discovered patterns from TTF→MLF→MX pipeline
    """
    
    def __init__(self, patterns: List[str] = None):
        """
        Initialize the predictor with available patterns
        
        Args:
            patterns: List of pattern names to use for evaluation (e.g., ['mfi', 'zonesq', 'aoac'])
        """
        self.patterns = patterns or ['mfi', 'zonesq', 'aoac']
        self.pattern_weights = {}
        self.quality_thresholds = {
            'excellent': 80,
            'good': 60,
            'fair': 40,
            'poor': 20
        }
        self._load_pattern_intelligence()
    
    def _load_pattern_intelligence(self):
        """
        Load historical pattern→profit intelligence from MX target files
        This analyzes which patterns historically led to profitable signals
        """
        print("📊 Loading pattern intelligence from historical MX data...")
        
        for pattern in self.patterns:
            try:
                # Load historical data for pattern analysis
                pattern_intelligence = self._analyze_pattern_profitability(pattern)
                self.pattern_weights[pattern] = pattern_intelligence
                print(f"   ✓ {pattern}: {pattern_intelligence.get('success_rate', 0):.1%} success rate")
            except Exception as e:
                print(f"   ⚠️  {pattern}: Could not load intelligence - {e}")
                self.pattern_weights[pattern] = {'success_rate': 0.5, 'avg_profit': 0.0}
    
    def _analyze_pattern_profitability(self, pattern: str) -> Dict:
        """
        Analyze historical profitability of a specific pattern
        
        Args:
            pattern: Pattern name (e.g., 'mfi', 'zonesq', 'aoac')
            
        Returns:
            Dictionary with pattern intelligence metrics
        """
        # Try to load MX data for common instrumentss
        instruments = ['EUR/USD', 'SPX500', 'GBP/USD']
        timeframes = ['D1', 'H4']
        
        all_targets = []
        
        for instrument in instruments:
            for timeframe in timeframes:
                try:
                    # Load MX target data
                    mx_file = get_outfile_fullpath(
                        instrument, timeframe, 
                        use_full=True, ns=MX_NS, 
                        pn=pattern, suffix=""
                    )
                    
                    if os.path.exists(mx_file):
                        df = pd.read_csv(mx_file, index_col=0, parse_dates=True)
                        if 'target' in df.columns:
                            targets = df['target'].dropna()
                            all_targets.extend(targets.tolist())
                except Exception as e:
                    continue
        
        if not all_targets:
            return {'success_rate': 0.5, 'avg_profit': 0.0, 'sample_size': 0}
        
        # Calculate intelligence metrics
        targets = np.array(all_targets)
        profitable_signals = targets > 0
        success_rate = profitable_signals.mean()
        avg_profit = targets[profitable_signals].mean() if profitable_signals.any() else 0.0
        
        return {
            'success_rate': success_rate,
            'avg_profit': avg_profit,
            'sample_size': len(targets),
            'profit_std': targets.std()
        }
    
    def evaluate_signal(self, instrument: str, timeframe: str, 
                       signal_data: Dict = None) -> Dict:
        """
        Evaluate the quality of an FDBSignal using ML patterns
        
        Args:
            instrument: Trading instrument (e.g., 'EUR/USD')
            timeframe: Timeframe (e.g., 'H4', 'D1')
            signal_data: Optional signal context data
            
        Returns:
            Dictionary with quality assessment
        """
        try:
            # Get current pattern states for the instrument/timeframe
            pattern_states = self._get_current_pattern_states(instrument, timeframe)
            
            # Calculate quality score based on pattern confluence
            quality_score = self._calculate_quality_score(pattern_states)
            
            # Determine quality level
            quality_level = self._get_quality_level(quality_score)
            
            # Generate recommendation
            recommendation = self._generate_recommendation(quality_score, pattern_states)
            
            return {
                'quality_score': quality_score,
                'quality_level': quality_level,
                'recommendation': recommendation,
                'pattern_states': pattern_states,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error evaluating signal: {e}")
            return {
                'quality_score': 50,
                'quality_level': 'unknown',
                'recommendation': 'Unable to evaluate - proceed with caution',
                'error': str(e)
            }
    
    def _get_current_pattern_states(self, instrument: str, timeframe: str) -> Dict:
        """
        Get current states of all patterns for the instrument/timeframe
        """
        pattern_states = {}
        
        for pattern in self.patterns:
            try:
                # Read MLF data for the pattern
                mlf_data = read_mlf_for_pattern(instrument, timeframe, use_full=False, pn=pattern)
                
                if mlf_data is not None and not mlf_data.empty:
                    # Get the latest values for pattern analysis
                    latest_row = mlf_data.iloc[-1]
                    
                    # Extract pattern-specific features
                    pattern_features = self._extract_pattern_features(pattern, latest_row)
                    pattern_states[pattern] = pattern_features
                else:
                    pattern_states[pattern] = {'status': 'no_data'}
                    
            except Exception as e:
                pattern_states[pattern] = {'status': 'error', 'error': str(e)}
        
        return pattern_states
    
    def _extract_pattern_features(self, pattern: str, data_row: pd.Series) -> Dict:
        """
        Extract relevant features from a pattern's data row
        """
        features = {'status': 'active'}
        
        if pattern == 'mfi':
            # MFI pattern features
            mfi_cols = [col for col in data_row.index if 'mfi' in col.lower()]
            for col in mfi_cols:
                if col in data_row.index:
                    features[col] = data_row[col]
        
        elif pattern == 'zonesq':
            # Zone Squat pattern features  
            zone_cols = [col for col in data_row.index if 'zone' in col.lower()]
            mfi_cols = [col for col in data_row.index if 'mfi' in col.lower()]
            for col in zone_cols + mfi_cols:
                if col in data_row.index:
                    features[col] = data_row[col]
        
        elif pattern == 'aoac':
            # AO/AC pattern features
            ao_ac_cols = [col for col in data_row.index if col.lower() in ['ao', 'ac']]
            for col in ao_ac_cols:
                if col in data_row.index:
                    features[col] = data_row[col]
        
        # Add common fractal and alligator features
        common_cols = ['fdbb', 'fdbs', 'jaw', 'teeth', 'lips']
        for col in common_cols:
            if col in data_row.index:
                features[col] = data_row[col]
        
        return features
    
    def _calculate_quality_score(self, pattern_states: Dict) -> float:
        """
        Calculate overall quality score based on pattern confluence
        """
        total_score = 0.0
        total_weight = 0.0
        
        for pattern, state in pattern_states.items():
            if state.get('status') != 'active':
                continue
                
            pattern_intelligence = self.pattern_weights.get(pattern, {})
            pattern_weight = pattern_intelligence.get('success_rate', 0.5)
            
            # Calculate pattern-specific score
            pattern_score = self._score_pattern_state(pattern, state)
            
            total_score += pattern_score * pattern_weight
            total_weight += pattern_weight
        
        # Normalize to 0-100 scale
        if total_weight > 0:
            final_score = (total_score / total_weight) * 100
        else:
            final_score = 50  # Neutral score if no patterns available
        
        return min(100, max(0, final_score))
    
    def _score_pattern_state(self, pattern: str, state: Dict) -> float:
        """
        Score an individual pattern's current state (0-1 scale)
        """
        if pattern == 'mfi':
            # MFI scoring logic
            score = 0.5  # Base score
            
            # Look for MFI squat conditions (typically bullish)
            if 'mfi_sq' in state and state['mfi_sq'] > 0:
                score += 0.3
            
            # Look for MFI fade conditions
            if 'mfi_fade' in state and state['mfi_fade'] == 0:
                score += 0.2
                
        elif pattern == 'zonesq':
            # Zone + MFI squat confluence
            score = 0.5
            
            if 'zone_sig' in state and abs(state['zone_sig']) > 0:
                score += 0.2
            
            if 'mfi_sq' in state and state['mfi_sq'] > 0:
                score += 0.3
                
        elif pattern == 'aoac':
            # AO/AC momentum scoring
            score = 0.5
            
            if 'ao' in state and 'ac' in state:
                ao_val = state['ao']
                ac_val = state['ac']
                
                # Look for aligned momentum
                if (ao_val > 0 and ac_val > 0) or (ao_val < 0 and ac_val < 0):
                    score += 0.3
        else:
            score = 0.5  # Default neutral score
        
        return score
    
    def _get_quality_level(self, score: float) -> str:
        """
        Convert numeric score to quality level
        """
        if score >= self.quality_thresholds['excellent']:
            return 'excellent'
        elif score >= self.quality_thresholds['good']:
            return 'good'
        elif score >= self.quality_thresholds['fair']:
            return 'fair'
        else:
            return 'poor'
    
    def _generate_recommendation(self, score: float, pattern_states: Dict) -> str:
        """
        Generate trading recommendation based on quality assessment
        """
        level = self._get_quality_level(score)
        
        recommendations = {
            'excellent': f"🚀 High-quality signal (Score: {score:.1f}). Strong pattern confluence detected.",
            'good': f"✅ Good signal quality (Score: {score:.1f}). Favorable pattern alignment.",
            'fair': f"⚠️  Average signal quality (Score: {score:.1f}). Consider additional confirmation.",
            'poor': f"❌ Low signal quality (Score: {score:.1f}). High risk - avoid or wait for better setup."
        }
        
        base_rec = recommendations[level]
        
        # Add pattern-specific insights
        active_patterns = [p for p, s in pattern_states.items() if s.get('status') == 'active']
        if active_patterns:
            base_rec += f" Active patterns: {', '.join(active_patterns)}."
        
        return base_rec

def create_signal_quality_cli():
    """
    Create a CLI interface for the FDBSignal Quality Predictor
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Evaluate FDBSignal quality using ML patterns",
        epilog="Example: python fdb_signal_quality_predictor.py -i EUR/USD -t H4"
    )
    
    parser.add_argument('-i', '--instrument', required=True,
                       help='Trading instrument (e.g., EUR/USD)')
    parser.add_argument('-t', '--timeframe', required=True,
                       help='Timeframe (e.g., H4, D1)')
    parser.add_argument('-p', '--patterns', nargs='+', 
                       default=['mfi', 'zonesq', 'aoac'],
                       help='Patterns to analyze')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    return parser

def main():
    """
    Main CLI entry point
    """
    parser = create_signal_quality_cli()
    args = parser.parse_args()
    
    print(f"🔍 Evaluating FDBSignal quality for {args.instrument} {args.timeframe}")
    
    # Initialize predictor
    predictor = FDBSignalQualityPredictor(patterns=args.patterns)
    
    # Evaluate signal quality
    result = predictor.evaluate_signal(args.instrument, args.timeframe)
    
    # Display results
    print(f"\n📊 Quality Assessment:")
    print(f"   Score: {result['quality_score']:.1f}/100")
    print(f"   Level: {result['quality_level'].upper()}")
    print(f"   Recommendation: {result['recommendation']}")
    
    if args.verbose and 'pattern_states' in result:
        print(f"\n🔬 Pattern Analysis:")
        for pattern, state in result['pattern_states'].items():
            status = state.get('status', 'unknown')
            print(f"   {pattern}: {status}")
            if status == 'active' and args.verbose:
                for key, value in state.items():
                    if key != 'status':
                        print(f"      {key}: {value}")

if __name__ == "__main__":
    main()
