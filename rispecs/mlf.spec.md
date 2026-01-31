# MLF (Meta Lag Features) Specification

> Lagged Features for Machine Learning

**Specification Version**: 1.0  
**Modules**: `jgtml/mlfcli.py`, `jgtml/mlfsvc.py`, `jgtml/realityhelper.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: ML-ready feature datasets with time-lagged versions of indicators, enabling models to learn from temporal patterns (how did indicators behave over the last N bars before a signal?).

**Achievement Indicator**: Running `mlfcli -i EUR/USD -t H1 -pn mz -lp 1 -tlp 5` produces:
- CSV file with original TTF features
- Lagged columns: `ao_lag_1`, `ao_lag_2`, ..., `ao_lag_5` for each feature
- Feature count multiplied by (1 + lag_periods)

**Value Proposition**: ML models need temporal context. MLF transforms static snapshots into sequences that reveal momentum, acceleration, and pattern evolution.

---

## Structural Tension

**Current Reality**: TTF data shows current state with HTF context but no temporal memory.

**Desired State**: Each row contains current values plus lagged history, enabling sequence-aware ML training.

**Natural Progression**: TTF → Add lag columns → Clean NaN → Save MLF CSV.

---

## Data Pipeline Position

```
PDS → IDS → CDS → TTF → [MLF] → MX
                          ↑
                    Current stage
```

**Dependencies**: Requires TTF data for the specified pattern name.

---

## Core Function: generate_mlf_feature_pattern

```python
def generate_mlf_feature_pattern(
    i: str,                              # Instrument symbol
    t: str,                              # Timeframe
    lag_period: int = 1,                 # Lag step size (usually 1)
    total_lagging_periods: int = 5,      # Number of lag periods
    dropna: bool = True,                 # Drop rows with NaN
    use_full: bool = True,               # Full vs current data
    columns_to_keep: List[str] = None,   # Columns to retain
    columns_to_drop: List[str] = None,   # Columns to remove
    drop_bid_ask: bool = False,          # Remove bid/ask columns
    force_refresh: bool = False,         # Force regenerate TTF
    quiet: bool = True,                  # Suppress output
    pn: str = "ttf",                     # Pattern name
    out_lag_midfix_str: str = '_lag_',   # Lag column naming
    just_keep_lagging_columns: bool = False,  # Only keep lag columns
    save_to_csv: bool = True,            # Write output file
    args: argparse.Namespace = None
) -> pd.DataFrame:
    """
    Generate MLF feature dataset with lagged columns.
    
    Algorithm:
        1. Read pattern column metadata from TTF
        2. Load TTF DataFrame for pattern
        3. Clean DataFrame (drop columns, remove bid/ask)
        4. For each column in columns_list_from_higher_tf:
           - Create lag_1, lag_2, ..., lag_N columns
           - Each lag_k = column shifted by k periods
        5. Write MLF pattern metadata
        6. Save to CSV
    
    Returns:
        DataFrame with original + lagged features
    
    Output Path:
        $JGTPY_DATA/mlf/{instrument}_{timeframe}_{patternname}.csv
    """
```

---

## Lagging Algorithm

### Column Creation

```python
def add_lagging_columns(
    df: pd.DataFrame,
    columns_list: List[str],
    lag_period: int = 1,
    total_lagging_periods: int = 5,
    out_lag_midfix_str: str = '_lag_'
) -> pd.DataFrame:
    """
    Add lagged versions of specified columns.
    
    For each column in columns_list:
        for k in range(1, total_lagging_periods + 1):
            lag_step = k * lag_period
            new_col = f"{column}{out_lag_midfix_str}{k}"
            df[new_col] = df[column].shift(lag_step)
    
    Example (lag_period=1, total_lagging_periods=3):
        ao -> ao_lag_1, ao_lag_2, ao_lag_3
        
    Example with lag_period=2, total_lagging_periods=3:
        ao -> ao_lag_1 (shift 2), ao_lag_2 (shift 4), ao_lag_3 (shift 6)
    """
```

### Lagging Example

Original data:
```
Date        ao      zone_sig
2026-01-30  0.0025  B
2026-01-31  0.0030  B
2026-02-01  0.0028  S
2026-02-02  0.0035  B
2026-02-03  0.0040  B
```

After MLF with lag_period=1, total_lagging_periods=2:
```
Date        ao      ao_lag_1  ao_lag_2  zone_sig  zone_sig_lag_1  zone_sig_lag_2
2026-01-30  0.0025  NaN       NaN       B         NaN             NaN
2026-01-31  0.0030  0.0025    NaN       B         B               NaN
2026-02-01  0.0028  0.0030    0.0025    S         B               B
2026-02-02  0.0035  0.0028    0.0030    B         S               B
2026-02-03  0.0040  0.0035    0.0028    B         B               S
```

---

## CLI Interface

```python
# jgtml/mlfcli.py

def main():
    """
    MLF CLI Entry Point.
    
    Arguments:
        -i, --instrument: Instrument symbol (required)
        -t, --timeframe: Timeframe (required)
        -pn, --patternname: Pattern name (default: "ttf")
        -lp, --lag_period: Lag step size (default: 1)
        -tlp, --total_lagging_periods: Number of lags (default: 5)
        --fresh: Force refresh TTF data
        --full: Use full historical data
        -ctk, --columns_to_keep: Columns to retain
        -ctd, --columns_to_drop: Columns to remove
        --rmbidask: Remove bid/ask columns
        --dropna-volume: Drop zero-volume rows
    
    Examples:
        # Default MLF with 5 lag periods
        mlfcli -i EUR/USD -t H1 -pn mz
        
        # Custom lag configuration
        mlfcli -i EUR/USD -t H1 -pn mz -lp 1 -tlp 10
        
        # Specific columns only
        mlfcli -i SPX500 -t D1 -pn mz -ctk ao zone_sig mfi_sig
        
        # Fresh data regeneration
        mlfcli -i GBPUSD -t H4 --fresh
    """
```

---

## Programmatic API

```python
def generate_mlf_for_pattern(
    instrument: str,
    timeframe: str,
    patternname: str = "ttf",
    lag_period: int = 1,
    total_lagging_periods: int = 5,
    use_full: bool = True,
    use_fresh: bool = False,
    columns_to_keep: List[str] = None,
    columns_to_drop: List[str] = None,
    drop_bid_ask: bool = False,
    args: argparse.Namespace = None
) -> pd.DataFrame:
    """
    Programmatic wrapper for MLF generation.
    
    Includes JGTTracer integration for observability.
    """
```

---

## Service Layer

```python
class MLFService:
    """
    MLF Service for programmatic access.
    """
    
    def generate_features(self, request: MLFRequest) -> pd.DataFrame:
        """
        Generate MLF features from request object.
        
        If TTF pattern not found, suggests running:
            ttfcli -i {instrument} -t {timeframe} -pn {pattern}
        """
    
    def create_request(
        self,
        instrument: str,
        timeframe: str,
        pn: str,
        lag_period: int = 1,
        total_lagging_periods: int = 5,
        use_full: bool = True,
        force_refresh: bool = False,
        dropna: bool = True,
        columns_to_keep: List[str] = None,
        columns_to_drop: List[str] = None,
        drop_bid_ask: bool = True
    ) -> MLFRequest:
        """Create MLFRequest object for service consumption."""
```

---

## Output Schema

### Feature Multiplication

```
Original columns: N
Lag periods: L
Total output columns: N * (1 + L)

Example:
- 10 base features
- 5 lag periods
- 10 * 6 = 60 total features
```

### Column Naming Pattern

```python
# Original column: {name}
# Lagged columns: {name}_lag_{k}

# Example for 'ao' with 5 lags:
ao           # Current value
ao_lag_1     # 1 bar ago
ao_lag_2     # 2 bars ago
ao_lag_3     # 3 bars ago
ao_lag_4     # 4 bars ago
ao_lag_5     # 5 bars ago
```

---

## File Locations

```python
def get_mlf_outfile_fullpath(
    i: str,
    t: str,
    use_full: bool,
    suffix: str = "",
    ns: str = "mlf"
) -> str:
    """
    Get output file path for MLF CSV.
    
    Path Construction:
        base_dir = $JGTPY_DATA/mlf (current) or $JGTPY_DATA_FULL/mlf (full)
        filename = {instrument}_{timeframe}_{suffix}.csv
        
    Examples:
        -> /src/jgtml/data/current/mlf/EUR-USD_H1_mz.csv
        -> /src/jgtml/data/current/mlf/EUR-USD_H1_mz_columns.json
    """
```

---

## Fallback Logic

```python
# If TTF not found, attempt auto-generation:
try:
    df = generate_mlf_feature_pattern(...)
except Exception:
    print("TTF not found, generating...")
    from jgtapp import ttf
    ttf(instrument, timeframe, pn=patternname, use_fresh=fresh)
    df = generate_mlf_feature_pattern(...)  # Retry
```

---

## DataFrame Cleaning

```python
def __clean_dataframe(
    df: pd.DataFrame,
    columns_to_keep: List[str] = None,
    columns_to_drop: List[str] = None,
    drop_bid_ask: bool = False,
    dropna: bool = True
) -> pd.DataFrame:
    """
    Clean DataFrame before adding lags.
    
    Operations:
        1. dropna() if requested
        2. Remove columns_to_drop
        3. If drop_bid_ask: remove BidOpen, BidHigh, BidLow, BidClose,
           AskOpen, AskHigh, AskLow, AskClose
    """
```

---

## Dependencies

```python
import pandas as pd
import argparse
from jgtutils import jgtcommon
from jgtml.ptottf import read_ttf_csv
from jgtml.mldatahelper import (
    pndata__read_new_pattern_columns_list_with_htf,
    write_mlf_pattern_lagging_columns_list,
    _get_lagging_columns_list
)
from jgtml.anhelper import add_lagging_columns
from jgtml.realityhelper import generate_mlf_feature_pattern
```

---

## Quality Criteria

✅ **Temporal Context**: Models can see N periods of history  
✅ **Configurable Lags**: Adjustable lag_period and total_lagging_periods  
✅ **Pattern Aware**: Uses TTF pattern column definitions  
✅ **Clean Data**: NaN rows dropped, bid/ask removal option  
✅ **Auto-fallback**: Generates TTF if missing  
✅ **Metadata**: Column definitions saved for MX consumption

---

## Downstream Usage

```python
# MLF is consumed by MX for final ML matrix:
from jgtml.mxcli import create_mx_dataset

mx_df = create_mx_dataset(
    "EUR/USD", "H1",
    patternname="mz",
    target_column="fdb"
)
```
