# TTF (Cross-Timeframe Features) Specification

> Higher Timeframe Context for Signal Validation

**Specification Version**: 1.0  
**Modules**: `jgtml/ttfcli.py`, `jgtml/ptottf.py`, `jgtml/ttfsvc.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Cross-timeframe feature datasets that enrich current timeframe signals with context from all higher timeframes (H1 signal knows D1/W1/MN conditions).

**Achievement Indicator**: Running `ttfcli -i EUR/USD -t H1 -pn mz` produces:
- CSV file with base H1 CDS data
- Additional columns for each HTF: `zone_sig_H4`, `zone_sig_D1`, etc.
- Pattern name metadata stored for downstream MLF consumption

**Value Proposition**: Never trade H1 signals against D1 trend - TTF makes HTF context instantly available in every row.

---

## Structural Tension

**Current Reality**: CDS data exists for each timeframe independently.

**Desired State**: Single dataset with current TF features plus all HTF features aligned by timestamp.

**Natural Progression**: CDS → Get HTF datasets → Merge by timestamp → Save TTF CSV.

---

## Data Pipeline Position

```
PDS → IDS → CDS → [TTF] → MLF → MX
                    ↑
              Current stage
```

**Dependencies**: Requires CDS data for instrument across all timeframes.

---

## Core Function: create_ttf_csv

```python
def create_ttf_csv(
    i: str,                                  # Instrument symbol
    t: str,                                  # Target timeframe
    use_full: bool = False,                  # Full vs current data
    use_fresh: bool = True,                  # Force refresh CDS first
    quotescount: int = -1,                   # Bars to fetch (-1 = default)
    force_read: bool = False,                # Force read existing CDS
    dropna: bool = True,                     # Drop NaN rows
    quiet: bool = True,                      # Suppress output
    columns_list_from_higher_tf: List[str] = None,  # Columns to get from HTF
    not_needed_columns: List[str] = None,    # Columns to remove
    dropna_volume: bool = True,              # Drop zero-volume rows
    pn: str = "ttf",                         # Pattern name
    also_output_sel_csv: bool = False,       # Also save selected columns
    args: argparse.Namespace = None          # CLI args for settings
) -> pd.DataFrame:
    """
    Create TTF dataset with cross-timeframe features.
    
    Algorithm:
        1. Load settings for pattern (pn) to get columns_list_from_higher_tf
        2. Get higher timeframe array: H1 -> [H4, D1, W1, MN]
        3. If use_fresh: refresh all dependent CDS data
        4. Load CDS workset (dict of timeframe -> DataFrame)
        5. Get base DataFrame for target timeframe
        6. For each HTF in workset:
           - For each column in columns_list_from_higher_tf:
             - Create new column: {col}_{htf} (e.g., zone_sig_D1)
             - For each row in base DF:
               - Find latest HTF row <= current timestamp
               - Copy HTF column value to base DF
        7. Write pattern column metadata
        8. Drop not_needed_columns
        9. Save to CSV
    
    Returns:
        DataFrame with merged TTF features
    
    Output Path:
        $JGTPY_DATA/ttf/{instrument}_{timeframe}_{patternname}.csv
    """
```

---

## Timeframe Hierarchy

```python
def get_higher_tf_array(t: str) -> List[str]:
    """
    Get array of all timeframes higher than target.
    
    Examples:
        "m1" -> ["m5", "m15", "m30", "H1", "H4", "D1", "W1", "MN"]
        "H1" -> ["H4", "D1", "W1", "MN"]
        "D1" -> ["W1", "MN"]
        "W1" -> ["MN"]
        "MN" -> []
    """
```

Timeframe Order (low to high):
```
m1 < m5 < m15 < m30 < H1 < H2 < H3 < H4 < H6 < H8 < D1 < W1 < MN
```

---

## Pattern Configuration

### Pattern Columns Definition

Patterns are defined by which columns to copy from higher timeframes.

```python
# Pattern: mz (MFI + Zone)
COLUMNS_MZ = ["mfi_sig", "zone_sig", "ao"]

# Pattern: full (all Williams indicators)  
COLUMNS_FULL = ["mfi_sig", "zone_sig", "ao", "ac", "fdb", "fh", "fl"]
```

### Pattern Metadata Storage

```python
def write_patternname_columns_list(
    i: str,
    t: str,
    use_full: bool,
    columns_list: List[str],
    pn: str = "ttf"
) -> None:
    """
    Save pattern column metadata for MLF consumption.
    
    Output Path:
        $JGTPY_DATA/ttf/{instrument}_{timeframe}_{pn}_columns.json
    
    Format:
        ["zone_sig", "mfi_sig", "ao", "zone_sig_H4", "zone_sig_D1", ...]
    """
```

---

## CLI Interface

```python
# jgtml/ttfcli.py

def main():
    """
    TTF CLI Entry Point.
    
    Arguments:
        -i, --instrument: Instrument symbol (required)
        -t, --timeframe: Target timeframe (required)
        -pn, --patternname: Pattern name (default: "ttf")
        --fresh: Force refresh dependent CDS data
        --full: Use full historical data
        -n, --quotescount: Number of bars to include
        -clh, --columns_list_from_higher_tf: Custom column list
    
    Examples:
        # Default TTF with standard columns
        ttfcli -i EUR/USD -t H1
        
        # MZ pattern (MFI + Zone)
        ttfcli -i EUR/USD -t H1 -pn mz
        
        # Custom column selection
        ttfcli -i SPX500 -t D1 -clh ao ac zone_sig
        
        # Force refresh CDS before TTF
        ttfcli -i GBPUSD -t H4 --fresh
    """
```

---

## Programmatic API

```python
def generate_ttf_for_pattern(
    instrument: str,
    timeframe: str,
    patternname: str = "ttf",
    use_full: bool = True,
    use_fresh: bool = False,
    quotescount: int = -1,
    columns_list_from_higher_tf: List[str] = None,
    args: argparse.Namespace = None
) -> pd.DataFrame:
    """
    Programmatic helper mirroring CLI behavior for JTC integrations.
    
    Includes JGTTracer integration for observability.
    """
```

---

## Output Schema

### Column Naming Convention

```
{original_column}_{higher_timeframe}

Examples:
- zone_sig_H4    # Zone signal from H4
- zone_sig_D1    # Zone signal from D1
- mfi_sig_W1     # MFI signal from W1
- ao_H4          # AO from H4
```

### Output DataFrame Structure

```python
# For H1 with mz pattern, output columns:
{
    # Base CDS columns
    "Date": datetime,      # Index
    "Open": float,
    "High": float,
    "Low": float,
    "Close": float,
    "Volume": int,
    # Williams indicators
    "ao": float,
    "zone_sig": str,       # "B", "S", "N"
    "mfi_sig": str,
    "fdb": int,
    # Regular Alligator
    "jaw": float,
    "teeth": float,
    "lips": float,
    # HTF Context (added by TTF)
    "zone_sig_H4": str,
    "zone_sig_D1": str,
    "zone_sig_W1": str,
    "zone_sig_MN": str,
    "mfi_sig_H4": str,
    "mfi_sig_D1": str,
    "mfi_sig_W1": str,
    "mfi_sig_MN": str,
    "ao_H4": float,
    "ao_D1": float,
    "ao_W1": float,
    "ao_MN": float,
}
```

---

## Merge Algorithm

### Timestamp Alignment

```python
# For each row in base DataFrame:
for ii in df.index:
    date = ii  # Timestamp of current row
    
    # For each higher timeframe dataset:
    for key_tf, v in workset.items():
        if key_tf != t:  # Skip current timeframe
            v_sorted = v.sort_index()
            
            # Find latest HTF data <= current timestamp
            data = v_sorted[v_sorted.index <= date]
            
            if not data.empty:
                latest_data = data.iloc[-1]  # Most recent HTF bar
                
                for col in columns_list_from_higher_tf:
                    new_col_name = f"{col}_{key_tf}"
                    df.at[ii, new_col_name] = latest_data[col]
```

### Why This Works

- H1 bar at 14:00 gets D1 context from the last completed D1 bar (yesterday's close)
- W1 context comes from the most recent completed weekly bar
- This ensures we never have look-ahead bias (only using data that was available at the time)

---

## File Locations

```python
def get_ttf_outfile_fullpath(
    i: str,
    t: str,
    use_full: bool,
    suffix: str = "",
    pn: str = "ttf"
) -> str:
    """
    Get output file path for TTF CSV.
    
    Path Construction:
        base_dir = $JGTPY_DATA/ttf (current) or $JGTPY_DATA_FULL/ttf (full)
        filename = {instrument}_{timeframe}_{patternname}{suffix}.csv
        
    Examples:
        JGTPY_DATA=/src/jgtml/data/current
        -> /src/jgtml/data/current/ttf/EUR-USD_H1_mz.csv
        -> /src/jgtml/data/current/ttf/EUR-USD_H1_mz_columns.json
    """
```

---

## Configuration via Settings

```python
def get_settings() -> dict:
    """
    Load TTF settings from ~/.jgt/config.json or pattern-specific config.
    
    Settings Keys:
        ttf_columns_to_remove: List[str]  # Columns to drop from output
        columns_to_remove: List[str]      # Additional columns to remove
    """
```

---

## Dependencies

```python
import pandas as pd
from jgtpy import JGTCDSSvc as svc         # CDS service for data loading
from jgtutils import jgtpov as jpov        # Timeframe ordering
from mlutils import drop_columns_if_exists, dropna_volume_in_dataframe
from mlconstants import TTF_NOT_NEEDED_COLUMNS_LIST
from mldatahelper import (
    get_settings,
    get_ttf_outfile_fullpath,
    write_patternname_columns_list,
    pndata__read_new_pattern_columns_list
)
```

---

## Quality Criteria

✅ **HTF Context**: Every row includes data from all higher timeframes  
✅ **No Look-Ahead**: Only uses data available at each timestamp  
✅ **Pattern Support**: Custom column selection via pattern names  
✅ **Metadata Storage**: Column definitions saved for MLF consumption  
✅ **Fresh Data Option**: Can force-refresh dependent CDS data  
✅ **Tracing**: JGTTracer integration for observability

---

## Downstream Usage

```python
# TTF is consumed by MLF to add lagging features:
from jgtml.mlfcli import generate_mlf_for_pattern

df = generate_mlf_for_pattern(
    "EUR/USD", "H1",
    patternname="mz",           # Uses TTF output
    lag_period=1,               # 1-bar lag
    total_lagging_periods=5     # 5 lagged versions
)
```
