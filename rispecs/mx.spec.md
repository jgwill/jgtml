# MX (ML Matrix) Specification

> Final ML-Ready Feature Matrix with Target Calculation

**Specification Version**: 1.0  
**Modules**: `jgtml/mxcli.py`, `jgtml/mxsvc.py`, `jgtml/jtc.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Complete ML-ready dataset with features and calculated target variable showing actual profit/loss outcomes for each FDB signal.

**Achievement Indicator**: Running `mxcli -i EUR/USD -t H1` produces:
- MX CSV with all features plus calculated `target` column
- Target shows actual pips gained/lost if signal was taken
- Ready for ML model training/evaluation

**Value Proposition**: Training data that teaches models the true outcome of each signal - not just whether it was a valid signal, but how much money it made or lost.

---

## Structural Tension

**Current Reality**: MLF data with features but no labels - we don't know which signals were profitable.

**Desired State**: Dataset with calculated target variable showing actual P&L for each signal over a forward window.

**Natural Progression**: MLF → Apply target calculation → Forward-looking P&L → Save MX CSV.

---

## Data Pipeline Position

```
PDS → IDS → CDS → TTF → MLF → [MX]
                                ↑
                          Current stage
```

**Dependencies**: Can use MLF data or direct CDS data with TTF enrichment.

---

## Core Function: pto_target_calculation

```python
def pto_target_calculation(
    i: str,                              # Instrument symbol
    t: str,                              # Timeframe
    crop_start_dt: str = None,           # Start date for data crop
    crop_end_dt: str = None,             # End date for data crop
    tlid_tag: str = None,                # Timestamp ID tag
    WINDOW_MIN: int = 1,                 # Minimum forward window
    WINDOW_MAX: int = 150,               # Maximum forward window (bars)
    output_report_dir: str = None,       # Report output directory
    pto_vec_fdb_ao_vector_window_flag: bool = True,  # Calculate AO vectors
    drop_calc_col: bool = True,          # Drop intermediate columns
    write_reporting: bool = True,        # Write reports
    selected_columns_to_keep: List[str] = None,  # Feature selection
    save_outputs: bool = True,           # Save to CSV
    keep_bid_ask: bool = True,           # Keep bid/ask columns
    use_fresh: bool = True,              # Force fresh data
    regenerate_cds: bool = False,        # Regenerate CDS first
    gator_oscillator_flag: bool = False, # Include Gator Oscillator
    mfi_flag: bool = True,               # Include MFI
    balligator_flag: bool = False,       # Include Big Alligator
    balligator_period_jaws: int = 89,    # Big Alligator jaw period
    talligator_flag: bool = False,       # Include Tide Alligator
    talligator_period_jaws: int = 377,   # Tide Alligator jaw period
    use_ttf: bool = True,                # Use TTF enrichment
    pn: str = "ttf",                     # Pattern name
    quiet: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Calculate target variable for FDB signals.
    
    Returns:
        (df_result_tmx, sel1, sel2):
        - df_result_tmx: Full MX matrix with all features and target
        - sel1: Selected columns subset (_sel)
        - sel2: Minimal target-only subset (_tnd)
    
    Output Paths:
        $JGTPY_DATA_FULL/targets/mx/{instrument}_{timeframe}.csv
        $JGTPY_DATA_FULL/targets/mx/{instrument}_{timeframe}_sel.csv
        $JGTPY_DATA_FULL/targets/mx/{instrument}_{timeframe}_tnd.csv
    """
```

---

## Target Calculation Algorithm

### Calculate Target for Each FDB Signal

```python
def calculate_target_variable_min_max(
    dfsrc: pd.DataFrame,
    crop_last_dt: str = None,
    crop_start_dt: str = None,
    WINDOW_MIN: int = 1,
    WINDOW_MAX: int = 150,
    set_index: bool = True,
    rounder: int = 4,
    pipsize: float = -1,
    target_colname: str = ""
) -> pd.DataFrame:
    """
    Calculate P&L target for each FDB signal.
    
    Algorithm:
        For each row i with FDB Sell signal (fdbs=1):
            tmax = min(Close[i:i+WINDOW_MAX])  # Best exit price
            tmin = max(Close[i:i+WINDOW_MAX])  # Worst case
            
            if High[i] < tmin:  # Stop hit before profit
                target = -1 * (High - Low)     # Negative (loss)
            else:
                target = Low - tmax            # Positive (profit)
        
        For each row i with FDB Buy signal (fdbb=1):
            tmax = max(Close[i:i+WINDOW_MAX])  # Best exit price
            tmin = min(Close[i:i+WINDOW_MAX])  # Worst case
            
            if Low[i] > tmin:  # Stop hit before profit
                target = -1 * (High - Low)     # Negative (loss)
            else:
                target = tmax - High           # Positive (profit)
    
    Intermediate Columns:
        tmax: Best possible exit in window
        tmin: Worst possible price in window
        p: Profit amount if successful
        l: Loss amount if stopped
        target: Final P&L (can be normalized to pips)
    """
```

### Target Interpretation

| Target Value | Meaning |
|--------------|---------|
| Positive | Signal was profitable - price moved in signal direction |
| Negative | Signal was a loss - stop would have been hit |
| Zero | No FDB signal on this bar |

---

## AO Vector Window Calculation

```python
# Additional feature: Count of AO values from signal to ZLC

pto_vec_fdb_ao_out_s_name = "vaos"      # Sell signal AO vector
pto_vec_fdb_ao_out_b_name = "vaob"      # Buy signal AO vector
pto_vec_fdb_ao_out_s_count = "vaosc"    # Sell signal AO count
pto_vec_fdb_ao_out_b_count = "vaobc"    # Buy signal AO count
pto_vec_fdb_ao_count = "vaoc"           # Combined count

# Calculates: How many bars of AO momentum exist from FDB signal
# until ZLC (zero-line cross) occurs
```

---

## CLI Interface

```python
# jgtml/mxcli.py

def main():
    """
    MX CLI Entry Point.
    
    Arguments:
        -i, --instrument: Instrument symbol (required)
        -t, --timeframe: Timeframe (required)
        --fresh: Force fresh data
        --full/--notfull: Full vs current data
        -rcds: Regenerate CDS before calculation
        -pn, --patternname: Pattern name for TTF
        -sc, --selected-columns: Columns to keep in output
        -ddcc: Don't drop calculated columns
        --mfi: Include MFI indicator
        --gator: Include Gator Oscillator
        --balligator: Include Big Alligator
        --talligator: Include Tide Alligator
        --keepbidask/--rmbidask: Keep/remove bid-ask columns
        -tlidrange: TLID range for data subset (future)
    
    Examples:
        # Default MX calculation
        mxcli -i EUR/USD -t H1
        
        # With pattern name
        mxcli -i EUR/USD -t H1 -pn mz
        
        # Include all Alligators
        mxcli -i SPX500 -t D1 --balligator --talligator
        
        # Force CDS regeneration
        mxcli -i GBPUSD -t H4 -rcds
    """
```

---

## Output Schema

### Full MX DataFrame

```python
{
    # Price data
    "Date": datetime,        # Index
    "Open": float,
    "High": float,
    "Low": float,
    "Close": float,
    "Volume": int,
    
    # Williams indicators
    "ao": float,
    "ac": float,
    "fh": int,               # Fractal High
    "fl": int,               # Fractal Low
    "fdbb": int,             # FDB Buy
    "fdbs": int,             # FDB Sell
    "zlcb": int,             # Zero-line cross up
    "zlcs": int,             # Zero-line cross down
    
    # Alligator
    "jaw": float,
    "teeth": float,
    "lips": float,
    
    # AO Vectors
    "vaos": array,           # Sell AO vector (optional)
    "vaob": array,           # Buy AO vector (optional)
    "vaosc": int,            # Sell AO count
    "vaobc": int,            # Buy AO count
    "vaoc": int,             # Combined count
    
    # TARGET (the key output)
    "target": float,         # P&L in pips or price units
    
    # TTF columns if use_ttf=True
    "zone_sig_H4": str,
    "zone_sig_D1": str,
    ...
}
```

### Selection 1 (_sel)

```python
sel_1_keeping_columns = [
    "High", "Low",
    "fdbs", "fdbb",
    "tmax", "tmin",  # Best/worst prices
    "p", "l",        # Profit/loss amounts
    "target"         # Final P&L
]
```

### Selection 2 (_tnd)

```python
sel_2_keeping_columns = [
    "fdb",           # Signal column
    "target"         # P&L
]
```

---

## File Locations

```python
# MX outputs go to:
$JGTPY_DATA_FULL/targets/mx/

# Example files:
EUR-USD_H1.csv           # Full MX matrix
EUR-USD_H1_sel.csv       # Selected columns
EUR-USD_H1_tnd.csv       # Minimal target-only
```

---

## Configuration

### Default Columns to Keep

```python
ML_DEFAULT_COLUMNS_TO_KEEP = [
    'High', 'Low', 'ao', 'ac',
    'jaw', 'teeth', 'lips',
    'fh', 'fl', 'fdbb', 'fdbs',
    'zlcb', 'zlcs', 'target',
    'vaosc', 'vaobc'
]
```

### Window Configuration

```python
WINDOW_MIN = 1      # Start looking 1 bar after signal
WINDOW_MAX = 150    # Look up to 150 bars forward

# The window determines how far forward we look
# to calculate if the trade would have been profitable
```

---

## Dependencies

```python
import pandas as pd
import numpy as np
import tlid
from jgtpy import JGTPDSP as pds
from jgtutils.jgtos import get_data_path
from mlutils import get_outfile_fullpath
from mlconstants import MX_NS
from jgtutils.jgtconstants import (
    FDBB, FDBS, AO, ZLCB, ZLCS,
    OPEN, LOW, CLOSE, HIGH, DATE,
    FDB_TARGET, VECTOR_AO_FDBS, VECTOR_AO_FDBB,
    ML_DEFAULT_COLUMNS_TO_KEEP
)
```

---

## Service Layer

```python
class MXService:
    """
    MX Service for programmatic access.
    
    Capabilities:
    - Create MX (calculates targets)
    - Read MX (returns cached if exists)
    - Update MX (regenerates with fresh data)
    - Chain from TTF/MLF if needed
    
    Dependencies:
    - MXRequest
    - MLF Service
    """
```

---

## Quality Criteria

✅ **Forward-Looking Target**: Calculates actual P&L over configurable window  
✅ **Signal-Aware**: Only calculates targets for bars with FDB signals  
✅ **Loss Detection**: Identifies when stop would have been hit  
✅ **AO Vector Features**: Counts momentum bars until ZLC  
✅ **TTF Integration**: Includes HTF context when enabled  
✅ **Multiple Outputs**: Full matrix, selection, and minimal versions

---

## Usage in ML Pipeline

```python
# Training a model to predict signal profitability:
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load MX data
mx = pd.read_csv('EUR-USD_H1.csv')

# Create binary target: profitable or not
mx['profitable'] = (mx['target'] > 0).astype(int)

# Feature columns (exclude target and price)
features = ['ao', 'ac', 'jaw', 'teeth', 'lips', 
            'zone_sig_H4', 'zone_sig_D1', 'vaosc', 'vaobc']

X = mx[features]
y = mx['profitable']

# Train classifier
model = RandomForestClassifier()
model.fit(X, y)
```
