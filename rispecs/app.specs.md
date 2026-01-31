# JGTML Application Specification

> Master specification for the JGT Trading Signal Analysis Platform

**Specification Version**: 1.0  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: A comprehensive trading signal analysis platform that validates FDB signals within larger market structure, provides multi-Alligator confluence detection, and generates ML-ready features for predictive trading.

**Achievement Indicator**: Users can scan for FDB signals, validate them against HTF alignment, assess risk through multi-Alligator analysis, and generate datasets for machine learning.

**Value Proposition**: Transform raw CDS signals into validated, context-aware trading opportunities with clear entry/exit strategies and ML-ready feature sets.

---

## Application Overview

JGTML is a Python package that:
1. Scans for FDB (Fractal Divergent Bar) signals across instruments
2. Validates signals against Higher Timeframe (HTF) alignment
3. Provides Regular/Big/Tide Alligator confluence analysis
4. Generates cross-timeframe features (TTF) for ML
5. Creates meta lag features (MLF) for predictive models
6. Outputs matrix (MX) datasets for training

---

## Structural Tension

**Current Reality**: Raw FDB signals from CDS lack context about higher timeframe trends, Alligator states, and validation criteria.

**Desired State**: Each signal is enriched with HTF alignment, multi-Alligator confluence, risk assessment, and ML-ready features.

**Natural Progression**: JGTML builds upon jgtpy CDS data, adding validation layers and feature engineering for trading decisions.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    JGTML Signal Analysis                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CDS Data (jgtpy)                                               │
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │           FDB Scanner & Signal Validation                   ││
│  │  fdb_scanner_2508.py → SignalOrderingHelper.py              ││
│  └─────────────────────────────────────────────────────────────┘│
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │           Multi-Alligator Analysis                          ││
│  │  Regular (5-8-13) | Big (34-55-89) | Tide (144-233-377)     ││
│  │  TideAlligatorAnalysis.py → alligator_cli.py                ││
│  └─────────────────────────────────────────────────────────────┘│
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │           Feature Engineering                                ││
│  │  TTF (ttfcli) → MLF (mlfcli) → MX (mxcli)                   ││
│  └─────────────────────────────────────────────────────────────┘│
│       ↓                                                         │
│  ML-Ready Datasets / Trading Decisions                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## FDB Scanner

### Purpose
Scan for Fractal Divergent Bar signals with validation and quality scoring.

### Usage

```bash
# Scan for FDB signals
fdbscan -i EUR/USD -t H4

# Scan multiple instruments
fdbscan -i "EUR/USD,SPX500,XAU/USD" -t "H1,H4,D1"

# With HTF alignment check
fdbscan -i EUR/USD -t H4 --htf
```

### Signal Output

```python
@dataclass
class FDBSignal:
    instrument: str         # "EUR/USD"
    timeframe: str          # "H4"
    direction: str          # "B" (buy) or "S" (sell)
    date: datetime          # Signal bar datetime
    entry_price: float      # Recommended entry
    stop_loss: float        # Below/above fractal
    risk_pips: float        # Entry to stop distance
    quality_score: float    # 0.0 - 1.0 signal quality
    htf_aligned: bool       # HTF trend alignment
    alligator_state: str    # "mouth_open", "sleeping", etc.
```

---

## Multi-Alligator Analysis

### Three Alligator Periods

| Type | Periods | Use Case |
|------|---------|----------|
| Regular | 5-8-13 | Quick direction, day trading |
| Big | 34-55-89 | Swing trading, weekly cycles |
| Tide | 144-233-377 | Position trading, monthly trends |

### CLI Usage

```bash
# Single Alligator type
python -m jgtml.alligator_cli -i SPX500 -t D1 -d S --type tide

# All three types (convergence)
python -m jgtml.alligator_cli -i EUR/USD -t H4 -d B --type all

# Generate .jgtml-spec for agents
python -m jgtml.alligator_cli -i GBPUSD -t D1 -d S --generate-spec
```

### Convergence Analysis

```python
@dataclass
class AlligatorConvergence:
    instrument: str
    timeframe: str
    regular: AlligatorState  # 5-8-13 analysis
    big: AlligatorState      # 34-55-89 analysis
    tide: AlligatorState     # 144-233-377 analysis
    convergence_score: float # 0.0 - 1.0
    aligned_direction: Optional[str]  # "B", "S", or None
```

---

## Feature Engineering Pipeline

### TTF - Cross-Timeframe Features

**Purpose**: Add higher timeframe context to lower timeframe signals.

```bash
# Generate TTF features
ttfcli -i EUR/USD -t H4 --pattern mz

# All patterns
ttfcli --all
```

**Added Features**:
- HTF Alligator state (D1, W1)
- HTF trend direction
- Multi-timeframe confluence score

### MLF - Meta Lag Features

**Purpose**: Add lagged features for ML prediction.

```bash
# Generate MLF features
mlfcli -i EUR/USD -t H4
```

**Added Features**:
- Previous N bar values
- Rolling statistics
- Change rates

### MX - Matrix Generation

**Purpose**: Generate ML-ready datasets with targets.

```bash
# Generate MX data
mxcli -i EUR/USD -t H4 --fresh
```

**Output**: Dataset with features + target variable (signal outcome)

---

## CLI Tools

### jgtapp - Main Application

```bash
# Tide Alligator analysis (legacy wrapper)
jgtapp tide -i SPX500 -t D1 B

# Add entry order
jgtapp fxaddorder -i EUR/USD -n 0.1 -r 1.0950 -d B -x 1.0900

# Move stop to Alligator line
jgtapp fxmvstopgator -i EUR/USD -t H4 -tid TRADE_ID --lips
```

### jgtmlcli - Data Processing

```bash
# Process signals for instrument
jgtmlcli -i SPX500 -t D1 --full --fresh

# Generate all data layers
jgtmlcli -i EUR/USD -t H4 --ttf --mlf
```

---

## Type Definitions

```python
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum

class AlligatorType(Enum):
    REGULAR = "regular"   # 5-8-13
    BIG = "big"          # 34-55-89
    TIDE = "tide"        # 144-233-377

class AlligatorMouth(Enum):
    SLEEPING = "sleeping"
    AWAKENING = "awakening"
    FEEDING = "feeding"
    SATED = "sated"

@dataclass
class AlligatorState:
    type: AlligatorType
    mouth: AlligatorMouth
    direction: Optional[str]  # "B" or "S" or None
    jaw: float
    teeth: float
    lips: float
    spread: float  # Distance between lines
    
@dataclass
class SignalValidation:
    signal: FDBSignal
    htf_aligned: bool
    regular_mouth: AlligatorMouth
    big_aligned: bool
    tide_direction: Optional[str]
    risk_reward: float
    quality_score: float
    recommendation: str  # "TAKE", "SKIP", "WAIT"

def scan_fdb(
    instrument: str,
    timeframe: str,
    validate_htf: bool = True
) -> List[FDBSignal]: ...

def analyze_alligator(
    instrument: str,
    timeframe: str,
    direction: str,
    alligator_type: AlligatorType = AlligatorType.REGULAR
) -> AlligatorState: ...

def validate_signal(
    signal: FDBSignal,
    check_htf: bool = True,
    check_tide: bool = True
) -> SignalValidation: ...
```

---

## Creative Advancement Scenarios

### Scenario: FDB Signal Validation

**Desired Outcome**: Validate FDB buy signal against HTF trend

**Current Reality**: fdbscan detected buy signal on EUR/USD H4

**Natural Progression**:
1. FDB detected on H4 with bullish divergence
2. Check D1 Alligator: mouth open, lips > teeth > jaw
3. Check H4 Regular Alligator: mouth opening
4. Calculate risk: entry at 1.0950, stop at 1.0900 (50 pips)
5. Score signal: HTF aligned + Alligator confirming = 0.85

**Resolution**: Signal validated with "TAKE" recommendation

### Scenario: Multi-Alligator Confluence

**Desired Outcome**: Find instruments where all Alligators align

**Current Reality**: Need strongest trend opportunities

**Natural Progression**:
1. User runs: `python -m jgtml.alligator_cli -i SPX500 -t D1 -d B --type all`
2. Regular (5-8-13): Lips > Teeth > Jaw ✓
3. Big (34-55-89): Clear uptrend, mouth open ✓
4. Tide (144-233-377): Major uptrend ✓
5. Convergence score: 0.95

**Resolution**: Triple Alligator convergence signals strong trend

### Scenario: ML Feature Generation

**Desired Outcome**: Create dataset for FDB outcome prediction

**Current Reality**: Historical signals need feature engineering

**Natural Progression**:
1. Start with CDS: `cdscli --fresh`
2. Add TTF: `ttfcli --pattern mz`
3. Add MLF: `mlfcli`
4. Generate MX: `mxcli --fresh`
5. Output: CSV with features + target (signal profit/loss)

**Resolution**: ML-ready dataset for training signal predictor

---

## Module Structure

```
jgtml/
├── __init__.py                 # Package exports
├── jgtapp.py                   # Main application CLI
├── jgtmlcli.py                 # Data processing CLI
├── fdb_scanner_2508.py         # FDB scanning (current version)
├── fdb_scanner_2408.py         # FDB scanning (legacy)
├── SignalOrderingHelper.py     # Signal validation logic
├── TideAlligatorAnalysis.py    # Multi-period Alligator
├── AlligatorIllusionDetector.py # Alligator pattern detection
├── alligator_cli.py            # Unified Alligator CLI
├── ttfcli.py                   # TTF feature generation
├── ttfsvc.py                   # TTF service layer
├── mlfcli.py                   # MLF feature generation
├── mlfsvc.py                   # MLF service layer
├── mxcli.py                    # MX matrix generation
├── mxsvc.py                    # MX service layer
├── jtc.py                      # Target calculation
├── jplt.py                     # Plotting utilities
├── trading_orchestrator.py     # Trade lifecycle
└── experiments/                # Experimental features
```

---

## Integration with JGT Ecosystem

```
jgtpy (CDS signals)
    ↓ provides signal data
jgtml (this package) ← Analysis layer
    ↓ provides validated signals
jgt-data-server
    ↓ serves analysis via API
jgt-code
    ↓ displays in terminal
Trading Execution
```

---

## Quality Criteria

✅ **FDB Validation**: Multi-layer signal quality assessment  
✅ **HTF Alignment**: Higher timeframe trend confirmation  
✅ **Triple Alligator**: Regular/Big/Tide convergence analysis  
✅ **Feature Engineering**: TTF→MLF→MX pipeline complete  
✅ **CLI Complete**: All analysis available via command line  
✅ **ML Ready**: Output datasets for model training
