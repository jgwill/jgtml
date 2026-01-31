# Alligator Analysis Specification

> Multi-Period Alligator Convergence Analysis

**Specification Version**: 1.0  
**Module**: `jgtml/TideAlligatorAnalysis.py`  
**CLI**: `jgtml/alligator_cli.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Comprehensive Alligator analysis across three period scales (Regular, Big, Tide), revealing market structure from quick direction changes to macro trends, with convergence scoring for high-probability setups.

**Achievement Indicator**: Running `python -m jgtml.alligator_cli -i SPX500 -t D1 --type all` produces:
- Regular Alligator (5-8-13) state analysis
- Big Alligator (34-55-89) intermediate cycle analysis
- Tide Alligator (144-233-377) macro trend analysis
- Convergence score showing alignment across all three

**Value Proposition**: See the complete market structure at once - from micro direction to macro trend - enabling trades aligned with multiple timeframes of momentum.

---

## Structural Tension

**Current Reality**: Trader sees only regular Alligator on chart, missing larger cycle context.

**Desired State**: Complete three-scale Alligator view showing where current price sits within the fractal structure of the market.

**Natural Progression**: Load CDS → Calculate all Alligator periods → Analyze mouth states → Score convergence → Report alignment.

---

## Three Alligator Scales

### Regular Alligator (5-8-13)

**Periods**: Lips=5, Teeth=8, Jaw=13  
**Shifts**: Lips=3, Teeth=5, Jaw=8  
**Columns**: `lips`, `teeth`, `jaw`

**Use Case**: Quick market direction detection, day trading entries

**Mouth States**:
- **Sleeping**: Lines intertwined, no trend
- **Awakening**: Lines separating, trend starting
- **Feeding**: Lines spread apart, strong trend
- **Sated**: Lines converging, trend ending

### Big Alligator (34-55-89)

**Periods**: Lips=34, Teeth=55, Jaw=89  
**Columns**: `blips`, `bteeth`, `bjaw`

**Use Case**: Intermediate cycle analysis, swing trading

**Analysis Focus**:
- Weekly/monthly cycle position
- Larger wave structure
- Support/resistance from Big Alligator lines

### Tide Alligator (144-233-377)

**Periods**: Lips=144, Teeth=233, Jaw=377  
**Columns**: `tlips`, `tteeth`, `tjaw`

**Use Case**: Macro trend identification, position trading

**Analysis Focus**:
- Monthly/quarterly trend direction
- Major support/resistance levels
- Macro wave position

---

## Type Definitions

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict

class AlligatorType(Enum):
    """Three Alligator analysis types"""
    REGULAR = "normal"    # 5-8-13 periods
    BIG = "big"           # 34-55-89 periods
    TIDE = "tide"         # 144-233-377 periods

class MouthState(Enum):
    """Alligator mouth states"""
    SLEEPING = "sleeping"      # Lines intertwined
    AWAKENING = "awakening"    # Lines separating
    FEEDING = "feeding"        # Lines spread apart
    SATED = "sated"           # Lines converging

class Direction(Enum):
    """Market direction"""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"

@dataclass
class AlligatorState:
    """State of a single Alligator"""
    type: AlligatorType
    jaw: float
    teeth: float
    lips: float
    mouth_state: MouthState
    direction: Direction
    spread: float              # Distance between lines
    
@dataclass
class ConvergenceAnalysis:
    """Analysis of all three Alligators"""
    instrument: str
    timeframe: str
    regular: AlligatorState
    big: AlligatorState
    tide: AlligatorState
    convergence_score: float   # 0.0 to 1.0
    aligned_direction: Optional[Direction]
    recommendation: str
```

---

## Configuration

```python
@dataclass
class AlligatorConfig:
    """Configuration for Alligator Analysis"""
    instrument: str = 'SPX500'
    timeframe: str = 'D1'
    alligator_types: List[AlligatorType] = None  # Default: all three
    force_regenerate_mxfiles: bool = True
    mfi_flag: bool = True
    regenerate_cds: bool = True
    use_fresh: bool = True
    quiet: bool = False
    jgtdroot: str = "/b/Dropbox/jgt"
    drop_subdir: str = "drop"
    result_file_basename: str = "jgtml_alligator_analysis.result"
```

---

## Core Analysis Class

```python
class AlligatorAnalysis:
    """
    Unified Alligator Analysis supporting all three types.
    """
    
    def __init__(self, config: AlligatorConfig):
        self.config = config
        self.data_cache = {}
        self.results_cache = {}
    
    def analyze(self, direction: str = "B") -> ConvergenceAnalysis:
        """
        Run full analysis for specified direction.
        
        Args:
            direction: "B" for buy analysis, "S" for sell analysis
        
        Returns:
            ConvergenceAnalysis with all three Alligator states
        """
    
    def get_alligator_state(
        self, 
        alligator_type: AlligatorType,
        bar: pd.Series
    ) -> AlligatorState:
        """
        Get state of specific Alligator from bar data.
        
        Determines mouth state by analyzing:
        - Line order (lips/teeth/jaw)
        - Line spread (distance between lines)
        - Direction (bullish/bearish/neutral)
        """
    
    def calculate_convergence_score(
        self,
        regular: AlligatorState,
        big: AlligatorState,
        tide: AlligatorState
    ) -> float:
        """
        Calculate convergence score (0.0 to 1.0).
        
        Higher score = more alignment between all three Alligators
        
        Scoring:
        - Same direction for all three: +0.5
        - All mouths open: +0.3
        - Regular inside Big inside Tide: +0.2
        """
```

---

## Helper Functions

### Column Name Resolution

```python
def get_alligator_column_names_from_ctx_name(
    ctx_name: str
) -> tuple[str, str, str]:
    """
    Get jaw, teeth, lips column names for Alligator type.
    
    Args:
        ctx_name: "normal", "big", or "tide"
    
    Returns:
        (jaw_col, teeth_col, lips_col)
        
    Examples:
        "normal" -> ("jaw", "teeth", "lips")
        "big" -> ("bjaw", "bteeth", "blips")
        "tide" -> ("tjaw", "tteeth", "tlips")
    """
```

### Filtering Functions

```python
def filter_sig_is_in_ctx_teeth(
    df: pd.DataFrame,
    bs: str,
    ctx_name: str
) -> pd.DataFrame:
    """Filter bars where signal is in context Alligator teeth."""

def filter_sig_ctx_mouth_is_open_and_in_ctx_teeth(
    df: pd.DataFrame,
    bs: str,
    ctx_name: str
) -> pd.DataFrame:
    """Filter bars where mouth is open and signal in teeth."""

def filter_sig_ctx_mouth_is_open_and_in_ctx_lips(
    df: pd.DataFrame,
    bs: str,
    ctx_name: str
) -> pd.DataFrame:
    """Filter bars where mouth is open and signal in lips."""

def filter_sig_is_out_of_normal_mouth_sell(df: pd.DataFrame) -> pd.DataFrame:
    """Filter sell signals outside normal Alligator mouth."""

def filter_sig_is_out_of_normal_mouth_buy(df: pd.DataFrame) -> pd.DataFrame:
    """Filter buy signals outside normal Alligator mouth."""

def filter_sig_normal_mouth_is_open_sell(df: pd.DataFrame) -> pd.DataFrame:
    """Filter bars where normal mouth is open for sell."""

def filter_sig_normal_mouth_is_open_buy(df: pd.DataFrame) -> pd.DataFrame:
    """Filter bars where normal mouth is open for buy."""
```

---

## CLI Interface

```python
# jgtml/alligator_cli.py

def main():
    """
    Unified Alligator CLI.
    
    Arguments:
        -i, --instrument: Instrument symbol
        -t, --timeframe: Timeframe
        -d: Direction ("B" or "S")
        --type: Alligator type(s) - "regular", "big", "tide", "all"
        --generate-spec: Generate .jgtml-spec file
        --fresh: Force fresh data
        -q, --quiet: Suppress output
    
    Examples:
        # Single Alligator type
        python -m jgtml.alligator_cli -i SPX500 -t D1 -d S --type tide
        
        # All three types (convergence analysis)
        python -m jgtml.alligator_cli -i EUR/USD -t H4 -d B --type all
        
        # Generate spec file for agents
        python -m jgtml.alligator_cli -i GBPUSD -t D1 -d S --generate-spec
    """
```

---

## Output Format

### Console Output

```
╔═══════════════════════════════════════════════════════════════╗
║          ALLIGATOR CONVERGENCE ANALYSIS: EUR/USD H4           ║
╠═══════════════════════════════════════════════════════════════╣
║ Direction: BUY                                                ║
╠═══════════════════════════════════════════════════════════════╣
║ REGULAR (5-8-13)                                              ║
║   Jaw: 1.0850  Teeth: 1.0870  Lips: 1.0890                   ║
║   Mouth: FEEDING  Direction: BULLISH  Spread: 0.0040         ║
╠═══════════════════════════════════════════════════════════════╣
║ BIG (34-55-89)                                                ║
║   BJaw: 1.0750  BTeeth: 1.0800  BLips: 1.0850                ║
║   Mouth: FEEDING  Direction: BULLISH  Spread: 0.0100         ║
╠═══════════════════════════════════════════════════════════════╣
║ TIDE (144-233-377)                                            ║
║   TJaw: 1.0600  TTeeth: 1.0700  TLips: 1.0800                ║
║   Mouth: FEEDING  Direction: BULLISH  Spread: 0.0200         ║
╠═══════════════════════════════════════════════════════════════╣
║ CONVERGENCE SCORE: 0.95                                       ║
║ ALIGNED DIRECTION: BULLISH                                    ║
║ RECOMMENDATION: Strong buy alignment across all timeframes    ║
╚═══════════════════════════════════════════════════════════════╝
```

### .jgtml-spec Output

```json
{
  "instrument": "EUR/USD",
  "timeframe": "H4",
  "direction": "B",
  "analysis_timestamp": "2026-01-31T14:00:00Z",
  "regular": {
    "type": "normal",
    "jaw": 1.0850,
    "teeth": 1.0870,
    "lips": 1.0890,
    "mouth_state": "feeding",
    "direction": "bullish",
    "spread": 0.0040
  },
  "big": {
    "type": "big",
    "jaw": 1.0750,
    "teeth": 1.0800,
    "lips": 1.0850,
    "mouth_state": "feeding",
    "direction": "bullish",
    "spread": 0.0100
  },
  "tide": {
    "type": "tide",
    "jaw": 1.0600,
    "teeth": 1.0700,
    "lips": 1.0800,
    "mouth_state": "feeding",
    "direction": "bullish",
    "spread": 0.0200
  },
  "convergence_score": 0.95,
  "aligned_direction": "bullish",
  "recommendation": "Strong buy alignment across all timeframes"
}
```

---

## Dependencies

```python
import pandas as pd
import numpy as np
from enum import Enum
from typing import Dict, Tuple, Optional, List

from jgtpy import JGTCDS as cds
from jgtml import jtc
from JGTBalanceAnalyzer import (
    get_alligator_column_names_from_ctx_name,
    filter_sig_is_in_ctx_teeth,
    filter_sig_ctx_mouth_is_open_and_in_ctx_teeth,
    filter_sig_ctx_mouth_is_open_and_in_ctx_lips
)
from jgtutils.jgtconstants import (
    LOW, HIGH, FDBB, FDBS,
    JAW, TEETH, LIPS,
    BJAW, BTEETH, BLIPS,
    TJAW, TTEETH, TLIPS
)
```

---

## Quality Criteria

✅ **Three Scales**: Regular (5-8-13), Big (34-55-89), Tide (144-233-377)  
✅ **Mouth Detection**: Sleeping, Awakening, Feeding, Sated states  
✅ **Convergence Scoring**: 0.0-1.0 alignment metric  
✅ **Direction Analysis**: Bullish/Bearish/Neutral for each scale  
✅ **CLI Complete**: Single command for full analysis  
✅ **Spec Generation**: .jgtml-spec for agentic workflows
