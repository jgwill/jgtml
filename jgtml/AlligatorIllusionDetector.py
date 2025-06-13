#!/usr/bin/env python3
"""
AlligatorIllusionDetector.py - Multi-timeframe Alligator Pattern Illusion Detection

Detects false-positive trade entries when lower timeframes contradict broader market structure.
Implements multi-timeframe validation across m15→H1→H4→D1→W1→MN1 progression.

Author: JGT Platform
Created: 2025-01-15
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TimeFrame(Enum):
    """Supported timeframes for multi-timeframe analysis"""
    M15 = "M15"
    H1 = "H1" 
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    MN1 = "MN1"

class AlligatorState(Enum):
    """Alligator mouth states"""
    SLEEPING = "sleeping"
    AWAKENING = "awakening"
    EATING = "eating"
    SATISFIED = "satisfied"

class IllusionType(Enum):
    """Types of alligator illusions detected"""
    TIMEFRAME_CONTRADICTION = "timeframe_contradiction"
    FALSE_BREAKOUT = "false_breakout"
    PREMATURE_ENTRY = "premature_entry"
    TREND_EXHAUSTION = "trend_exhaustion"

@dataclass
class AlligatorReading:
    """Single timeframe alligator reading"""
    timeframe: TimeFrame
    jaw: float
    teeth: float
    lips: float
    state: AlligatorState
    mouth_open: bool
    trend_direction: str
    strength: float
    timestamp: str

@dataclass
class IllusionDetection:
    """Detected illusion pattern"""
    illusion_type: IllusionType
    confidence: float
    primary_timeframe: TimeFrame
    conflicting_timeframes: List[TimeFrame]
    description: str
    recommendation: str
    campaign_duration_guidance: str

class AlligatorIllusionDetector:
    """
    Multi-timeframe Alligator Illusion Detection System
    
    Analyzes alligator patterns across multiple timeframes to detect:
    - False-positive trade entries
    - Timeframe contradictions
    - Premature entry signals
    - Trend exhaustion patterns
    """
    
    def __init__(self, data_path: str = "/src/jgtml/cds"):
        self.data_path = Path(data_path)
        self.timeframe_hierarchy = [
            TimeFrame.MN1, TimeFrame.W1, TimeFrame.D1, 
            TimeFrame.H4, TimeFrame.H1, TimeFrame.M15
        ]
        
    def load_market_data(self, instrument: str, timeframe: TimeFrame) -> Optional[pd.DataFrame]:
        """Load CDS market data for specified instrument and timeframe"""
        try:
            # Map timeframe to file naming convention
            tf_map = {
                TimeFrame.D1: "D1",
                TimeFrame.H1: "H1", 
                TimeFrame.W1: "W1"
            }
            
            if timeframe not in tf_map:
                logger.warning(f"Timeframe {timeframe.value} not available in CDS data")
                return None
                
            filename = f"{instrument}_{tf_map[timeframe]}.csv"
            filepath = self.data_path / filename
            
            if not filepath.exists():
                logger.warning(f"Data file not found: {filepath}")
                return None
                
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} records for {instrument} {timeframe.value}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data for {instrument} {timeframe.value}: {e}")
            return None
    
    def extract_alligator_reading(self, df: pd.DataFrame, timeframe: TimeFrame, 
                                index: int = -1) -> Optional[AlligatorReading]:
        """Extract alligator reading from market data"""
        try:
            if df is None or len(df) == 0:
                return None
                
            row = df.iloc[index]
            
            # Extract alligator values (assuming regular alligator for now)
            jaw = row.get('alligator_jaw', 0)
            teeth = row.get('alligator_teeth', 0) 
            lips = row.get('alligator_lips', 0)
            
            # Determine alligator state
            state = self._determine_alligator_state(jaw, teeth, lips)
            mouth_open = abs(lips - jaw) > abs(teeth - jaw) * 0.1
            
            # Determine trend direction and strength
            trend_direction = "bullish" if lips > teeth > jaw else "bearish" if lips < teeth < jaw else "sideways"
            strength = self._calculate_trend_strength(jaw, teeth, lips)
            
            return AlligatorReading(
                timeframe=timeframe,
                jaw=jaw,
                teeth=teeth,
                lips=lips,
                state=state,
                mouth_open=mouth_open,
                trend_direction=trend_direction,
                strength=strength,
                timestamp=str(row.get('timestamp', ''))
            )
            
        except Exception as e:
            logger.error(f"Error extracting alligator reading: {e}")
            return None
    
    def _determine_alligator_state(self, jaw: float, teeth: float, lips: float) -> AlligatorState:
        """Determine alligator state based on line positions"""
        if abs(jaw - teeth) < 0.001 and abs(teeth - lips) < 0.001:
            return AlligatorState.SLEEPING
        elif lips > teeth > jaw or lips < teeth < jaw:
            return AlligatorState.EATING
        elif abs(lips - teeth) > abs(teeth - jaw):
            return AlligatorState.AWAKENING
        else:
            return AlligatorState.SATISFIED
    
    def _calculate_trend_strength(self, jaw: float, teeth: float, lips: float) -> float:
        """Calculate trend strength based on alligator line separation"""
        if jaw == 0:
            return 0.0
        
        separation = abs(lips - jaw) / jaw
        return min(separation * 100, 1.0)  # Normalize to 0-1 range
    
    def analyze_multi_timeframe(self, instrument: str, 
                              timeframes: List[TimeFrame] = None) -> Dict[TimeFrame, AlligatorReading]:
        """Analyze alligator patterns across multiple timeframes"""
        if timeframes is None:
            timeframes = [TimeFrame.D1, TimeFrame.H1]  # Available in CDS data
            
        readings = {}
        
        for tf in timeframes:
            df = self.load_market_data(instrument, tf)
            if df is not None:
                reading = self.extract_alligator_reading(df, tf)
                if reading:
                    readings[tf] = reading
                    
        return readings
    
    def detect_illusions(self, readings: Dict[TimeFrame, AlligatorReading]) -> List[IllusionDetection]:
        """Detect illusion patterns from multi-timeframe readings"""
        illusions = []
        
        # Check for timeframe contradictions
        contradiction_illusion = self._detect_timeframe_contradiction(readings)
        if contradiction_illusion:
            illusions.append(contradiction_illusion)
            
        # Check for false breakout patterns
        false_breakout_illusion = self._detect_false_breakout(readings)
        if false_breakout_illusion:
            illusions.append(false_breakout_illusion)
            
        # Check for premature entry signals
        premature_entry_illusion = self._detect_premature_entry(readings)
        if premature_entry_illusion:
            illusions.append(premature_entry_illusion)
            
        return illusions
    
    def _detect_timeframe_contradiction(self, readings: Dict[TimeFrame, AlligatorReading]) -> Optional[IllusionDetection]:
        """Detect when lower timeframes contradict higher timeframe trends"""
        if len(readings) < 2:
            return None
            
        # Get higher and lower timeframe readings
        sorted_tfs = sorted(readings.keys(), key=lambda x: self.timeframe_hierarchy.index(x))
        
        if len(sorted_tfs) < 2:
            return None
            
        higher_tf = sorted_tfs[0]  # Higher timeframe (more important)
        lower_tf = sorted_tfs[-1]  # Lower timeframe
        
        higher_reading = readings[higher_tf]
        lower_reading = readings[lower_tf]
        
        # Check for trend contradiction
        if (higher_reading.trend_direction == "bullish" and lower_reading.trend_direction == "bearish") or \
           (higher_reading.trend_direction == "bearish" and lower_reading.trend_direction == "bullish"):
            
            confidence = min(higher_reading.strength + lower_reading.strength, 1.0)
            
            return IllusionDetection(
                illusion_type=IllusionType.TIMEFRAME_CONTRADICTION,
                confidence=confidence,
                primary_timeframe=higher_tf,
                conflicting_timeframes=[lower_tf],
                description=f"Higher TF ({higher_tf.value}) shows {higher_reading.trend_direction} while lower TF ({lower_tf.value}) shows {lower_reading.trend_direction}",
                recommendation="Wait for timeframe alignment before entry",
                campaign_duration_guidance=f"Monitor {higher_tf.value} for trend continuation, expect {lower_tf.value} correction"
            )
            
        return None
    
    def _detect_false_breakout(self, readings: Dict[TimeFrame, AlligatorReading]) -> Optional[IllusionDetection]:
        """Detect false breakout patterns"""
        for tf, reading in readings.items():
            if reading.state == AlligatorState.AWAKENING and reading.strength < 0.3:
                return IllusionDetection(
                    illusion_type=IllusionType.FALSE_BREAKOUT,
                    confidence=0.7,
                    primary_timeframe=tf,
                    conflicting_timeframes=[],
                    description=f"Weak alligator awakening on {tf.value} suggests potential false breakout",
                    recommendation="Wait for stronger confirmation before entry",
                    campaign_duration_guidance="Short-term pattern, monitor for 1-3 periods"
                )
        return None
    
    def _detect_premature_entry(self, readings: Dict[TimeFrame, AlligatorReading]) -> Optional[IllusionDetection]:
        """Detect premature entry signals"""
        for tf, reading in readings.items():
            if reading.state == AlligatorState.AWAKENING and not reading.mouth_open:
                return IllusionDetection(
                    illusion_type=IllusionType.PREMATURE_ENTRY,
                    confidence=0.6,
                    primary_timeframe=tf,
                    conflicting_timeframes=[],
                    description=f"Alligator awakening but mouth not fully open on {tf.value}",
                    recommendation="Wait for mouth to open before entry",
                    campaign_duration_guidance="Monitor for 2-5 periods for full pattern development"
                )
        return None
    
    def generate_report(self, instrument: str, illusions: List[IllusionDetection]) -> str:
        """Generate comprehensive illusion detection report"""
        report = f"""
🐊 ALLIGATOR ILLUSION DETECTION REPORT
Instrument: {instrument}
Timestamp: {pd.Timestamp.now()}

{'='*50}
"""
        
        if not illusions:
            report += "\n✅ NO ILLUSIONS DETECTED - Clear signal environment\n"
        else:
            report += f"\n⚠️  {len(illusions)} ILLUSION(S) DETECTED:\n\n"
            
            for i, illusion in enumerate(illusions, 1):
                report += f"""
{i}. {illusion.illusion_type.value.upper()}
   Confidence: {illusion.confidence:.2f}
   Primary TF: {illusion.primary_timeframe.value}
   Description: {illusion.description}
   Recommendation: {illusion.recommendation}
   Campaign Guidance: {illusion.campaign_duration_guidance}
"""
        
        report += f"\n{'='*50}\n"
        return report
    
    def scan_instrument(self, instrument: str, timeframes: List[TimeFrame] = None) -> Dict[str, Any]:
        """Complete illusion detection scan for an instrument"""
        logger.info(f"🐊 Starting Alligator Illusion Detection scan for {instrument}")
        
        # Analyze multi-timeframe patterns
        readings = self.analyze_multi_timeframe(instrument, timeframes)
        
        if not readings:
            return {
                'instrument': instrument,
                'status': 'error',
                'message': 'No data available for analysis'
            }
        
        # Detect illusions
        illusions = self.detect_illusions(readings)
        
        # Generate report
        report = self.generate_report(instrument, illusions)
        
        return {
            'instrument': instrument,
            'status': 'success',
            'readings': readings,
            'illusions': illusions,
            'report': report,
            'recommendation': 'PROCEED' if not illusions else 'CAUTION'
        }

def main():
    """CLI interface for Alligator Illusion Detection"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Alligator Illusion Detection Scanner')
    parser.add_argument('-i', '--instrument', required=True, help='Instrument to analyze (e.g., SPX500, EUR-USD)')
    parser.add_argument('-t', '--timeframes', nargs='+', default=['D1', 'H1'], 
                       help='Timeframes to analyze (D1, H1, W1)')
    parser.add_argument('--data-path', default='/src/jgtml/cds', help='Path to CDS data files')
    
    args = parser.parse_args()
    
    # Convert timeframe strings to enums
    timeframes = []
    for tf_str in args.timeframes:
        try:
            timeframes.append(TimeFrame(tf_str))
        except ValueError:
            logger.warning(f"Invalid timeframe: {tf_str}")
    
    # Initialize detector
    detector = AlligatorIllusionDetector(args.data_path)
    
    # Perform scan
    result = detector.scan_instrument(args.instrument, timeframes)
    
    # Output results
    print(result['report'])
    
    if result['status'] == 'success':
        print(f"\n🎯 RECOMMENDATION: {result['recommendation']}")
        if result['illusions']:
            print(f"⚠️  {len(result['illusions'])} illusion(s) detected - proceed with caution")
        else:
            print("✅ Clear signal environment - safe to proceed")

if __name__ == "__main__":
    main()