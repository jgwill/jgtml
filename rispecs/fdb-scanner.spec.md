# FDB Scanner Specification

> Fractal Divergent Bar Signal Detection Engine

**Specification Version**: 1.0  
**Module**: `jgtml/fdb_scanner_2508.py` (current), `jgtml/fdb_scanner_2408.py` (legacy)  
**CLI Entry**: `fdbscan`, `fdbscan2`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: An automated scanner that detects valid FDB (Fractal Divergent Bar) trading signals across multiple instruments and timeframes, validates them against Alligator state, calculates risk, and generates executable entry order scripts.

**Achievement Indicator**: Running `fdbscan -i EUR/USD -t H4` produces:
- List of valid FDB buy/sell signals
- Entry rate and stop rate with tick adjustments
- Risk calculation in pips
- Executable shell script for order placement
- JSON and Markdown signal files

**Value Proposition**: Transform manual chart scanning into automated signal detection with validation, risk calculation, and ready-to-execute trade scripts.

---

## Structural Tension

**Current Reality**: Trader manually scans charts looking for FDB patterns, calculates entry/stop levels, and creates orders by hand.

**Desired State**: Automated scanner runs continuously or on-demand, detecting signals, validating against Alligator state, and outputting executable trade commands.

**Natural Progression**: Scanner loads CDS data → detects FDB signals → validates Alligator mouth state → calculates risk → generates entry order script.

---

## Core Algorithm

### FDB Detection Logic

```python
def detect_fdb_signal(signal_bar: pd.Series) -> Optional[str]:
    """
    Detect FDB signal from completed bar.
    
    FDB Buy (fdb == 1):
        - Price makes new fractal low
        - AO does NOT make new low (bullish divergence)
        - Creates buy entry opportunity
        
    FDB Sell (fdb == -1):
        - Price makes new fractal high
        - AO does NOT make new high (bearish divergence)
        - Creates sell entry opportunity
    
    Returns:
        "B" for buy, "S" for sell, None for no signal
    """
    fdb_value = signal_bar['fdb']
    if fdb_value == 1:
        return "B"  # Buy signal
    elif fdb_value == -1:
        return "S"  # Sell signal
    return None
```

### Signal Validation Flow

```
1. Load CDS Data
   └── Use cache if valid (timeframe-based expiration)
   └── Generate fresh if cache invalid

2. Get Last Two Bars
   └── signal_bar = last completed bar (index -2)
   └── current_bar = current incomplete bar (index -1)

3. Check FDB Signal
   └── signal_bar['fdb'] == 1 (buy) or -1 (sell)

4. Validate Signal Not Broken
   └── For Buy: current_bar.high <= entry_rate AND current_bar.low >= stop_rate
   └── For Sell: current_bar.low >= entry_rate AND current_bar.high <= stop_rate

5. Validate Alligator State
   └── is_mouth_open(bar, bs) - Lips/Teeth/Jaw properly ordered
   └── is_bar_out_of_mouth(bar, bs) - Price outside Alligator lines

6. Calculate Entry/Stop with Tick Adjustment
   └── Add/subtract tick_shift for spread buffer

7. Calculate Risk
   └── risk_in_pips = |entry_rate - stop_rate| / pip_size

8. Generate Output
   └── Shell script for jgtnewsession
   └── JSON signal file
   └── Markdown summary
```

---

## Type Definitions

### Input Types

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
import pandas as pd

# Instrument format: "EUR/USD", "SPX500", "XAU/USD"
Instrument = str

# Timeframe format: "m1", "m5", "m15", "m30", "H1", "H2", "H3", "H4", "H6", "H8", "D1", "W1", "M1"
Timeframe = str

# Buy/Sell direction
Direction = str  # "B" or "S"

# TLID timestamp string: "YYMMDDHHMMSS"
TLID = str
```

### Output Types

```python
@dataclass
class FDBSignalResult:
    """Result from FDB signal detection and validation"""
    instrument: Instrument
    timeframe: Timeframe
    direction: Direction           # "B" or "S"
    tlid_id: TLID                  # Unique signal identifier
    entry_rate: float              # Entry price with tick adjustment
    stop_rate: float               # Stop loss price with tick adjustment
    lots: float                    # Position size
    total_risk: float              # Total monetary risk
    unit_risk: float               # Risk per unit
    pips_risk: float               # Risk in pips
    sh: str                        # Executable shell script
    htfsig: Optional[str]          # Higher timeframe signals string

@dataclass
class HTFSignals:
    """Higher timeframe context signals"""
    zone1: str                     # HTF level 1 zone ("buy", "sell", "gray")
    zone2: str                     # HTF level 2 zone
    fade1: bool                    # HTF level 1 MFI fade
    fade2: bool                    # HTF level 2 MFI fade
    squat1: bool                   # HTF level 1 MFI squat
    squat2: bool                   # HTF level 2 MFI squat
    b4zlc1: int                    # Bars before ZLC at HTF level 1
    b4zlc2: int                    # Bars before ZLC at HTF level 2
```

---

## Function Specifications

### Main Entry Point

```python
def main() -> None:
    """
    FDB Scanner main entry point.
    
    CLI Arguments:
        -i, --instrument: Instrument(s) to scan (comma-separated or single)
        -t, --timeframe: Timeframe(s) to scan (comma-separated or single)
        -nc, --no-cache: Force fresh data, ignore cache
        --demo: Use demo broker connection
        -v, --verbose: Verbosity level (0-3)
        -q, --quiet: Suppress output
    
    Environment Variables:
        INSTRUMENTS: Override instrument list
        TIMEFRAMES: Override timeframe list
        LOTS: Position size (default: 1)
        JGT_CACHE: Cache directory path
    
    Output:
        - Console: Signal summaries
        - Files: 
          - rjgt/{instrument}_{timeframe}_{tlid}.sh - Individual signal scripts
          - rjgt/fdb_signals_out__{date}.sh - Combined script
          - data/jgt/signals/fdb_signals_out__{date}.json - All signals JSON
    """
```

### Cache Management

```python
def is_timeframe_cached_valid(
    df: pd.DataFrame, 
    timeframe: Timeframe,
    use_utc: bool = True,
    quiet: bool = True
) -> bool:
    """
    Check if cached data is still valid for the given timeframe.
    
    Validity is based on whether current time is within the timeframe period
    of the last bar in the cache.
    
    Args:
        df: Cached DataFrame with Date column or DatetimeIndex
        timeframe: Timeframe to validate ("m1" through "M1")
        use_utc: Use UTC time comparison
        quiet: Suppress debug output
    
    Returns:
        True if cache is still valid, False if refresh needed
    
    Timeframe Expiration Logic:
        m1: 1 minute after last bar
        m5: 5 minutes after last bar
        m15: 15 minutes after last bar
        m30: 30 minutes after last bar
        H1: 1 hour after last bar
        H2-H8: Next boundary (e.g., H4 at 00:00, 04:00, 08:00, 12:00, 16:00, 20:00)
        D1: 24 hours after last bar
        W1: 7 days after last bar
        M1: 30 days after last bar
    """

def generate_fresh_and_cache(
    instrument: Instrument,
    timeframe: Timeframe,
    quotescount: int = 300,
    cache_filepath: Optional[str] = None
) -> pd.DataFrame:
    """
    Generate fresh CDS data and cache it.
    
    Uses jgtpy.JGTCDSSvc.get() to fetch data, then saves to cache file.
    
    Args:
        instrument: Instrument symbol
        timeframe: Timeframe
        quotescount: Number of bars to fetch
        cache_filepath: Override cache file path
    
    Returns:
        Fresh CDS DataFrame
    """
```

### Signal Validation

```python
def is_mouth_open(bar: pd.Series, bs: Direction) -> bool:
    """
    Check if Alligator mouth is open in the given direction.
    
    For Buy (bs="B"):
        lips < teeth < jaw (Alligator pointing down, mouth open upward)
    
    For Sell (bs="S"):
        lips > teeth > jaw (Alligator pointing up, mouth open downward)
    
    Args:
        bar: Price bar with 'lips', 'teeth', 'jaw' columns
        bs: Direction to check ("B" or "S")
    
    Returns:
        True if mouth is open in the specified direction
    """

def is_bar_out_of_mouth(bar: pd.Series, bs: Direction) -> bool:
    """
    Check if price bar is outside the Alligator mouth.
    
    For Buy:
        bar.High < bar.Lips (price below all Alligator lines)
        AND mouth not open in opposite direction
    
    For Sell:
        bar.Low > bar.Lips (price above all Alligator lines)
        AND mouth not open in opposite direction
    
    Args:
        bar: Price bar with 'High', 'Low', 'lips' columns
        bs: Direction ("B" or "S")
    
    Returns:
        True if bar is out of the Alligator mouth
    """

def valid_gator(
    last_bar_completed: pd.Series,
    current_bar: pd.Series,
    bs: Direction
) -> bool:
    """
    Validate Alligator state for both signal bar and current bar.
    
    Both bars must pass:
        - is_mouth_open(bar, bs)
        - is_bar_out_of_mouth(bar, bs)
    
    Returns:
        True if both bars have valid Alligator state
    """
```

### Risk Calculation

```python
def calculate_entry_risk(
    instrument: Instrument,
    bs: Direction,
    entry_rate: float,
    stop_rate: float,
    position_size: float,
    tick_shift: int = 1,
    rounding_add: int = 2,
    timeframe: Optional[Timeframe] = None,
    quiet: bool = True,
    verbose_level: int = 0
) -> tuple[float, float, float]:
    """
    Calculate risk metrics for an entry order.
    
    Args:
        instrument: Trading instrument
        bs: Buy/Sell direction
        entry_rate: Entry price
        stop_rate: Stop loss price
        position_size: Lots/units
        tick_shift: Ticks to add/subtract for spread buffer
        rounding_add: Additional decimal places for rounding
        timeframe: Optional timeframe context
        quiet: Suppress output
        verbose_level: Debug verbosity
    
    Returns:
        Tuple of (total_risk, risk_per_unit, risk_in_pips)
    
    Calculation:
        pip_size = get_pips(instrument)  # e.g., 0.0001 for EUR/USD
        tick_size = pip_size / 10
        
        # Adjust for spread
        if bs == "B":
            entry_rate += tick_size * tick_shift
            stop_rate -= tick_size * tick_shift
        else:  # "S"
            entry_rate -= tick_size * tick_shift
            stop_rate += tick_size * tick_shift
        
        risk_per_unit = abs(entry_rate - stop_rate)
        total_risk = risk_per_unit * position_size
        risk_in_pips = risk_per_unit / pip_size
    """

def get_entry_stop_rate_ticked(
    instrument: Instrument,
    bs: Direction,
    entry_rate: float,
    stop_rate: float,
    tick_shift: int = 1,
    rounding_add: int = 2,
    timeframe: Optional[Timeframe] = None
) -> tuple[float, float]:
    """
    Adjust entry and stop rates with tick buffer.
    
    For Buy: entry += tick, stop -= tick
    For Sell: entry -= tick, stop += tick
    
    Returns:
        Tuple of (adjusted_entry_rate, adjusted_stop_rate)
    """
```

### Order Generation

```python
def create_fdb_entry_order(
    instrument: Instrument,
    signal_bar: pd.Series,
    current_bar: pd.Series,
    lots: float = 1,
    tick_shift: int = 2,
    quiet: bool = True,
    valid_gator_mouth_open_in_mouth: bool = False,
    validate_signal_out_of_mouth: bool = True,
    timeframe: Optional[Timeframe] = None,
    validation_timestamp: Optional[datetime] = None,
    verbose_level: int = 0,
    demo_flag: bool = True
) -> tuple[Optional[FDBSignalResult], str]:
    """
    Create entry order from FDB signal with full validation.
    
    Validation Steps:
        1. Check if signal_bar has FDB signal (fdb == 1 or -1)
        2. Check if signal not already broken by current_bar price action
        3. Optionally validate Alligator mouth state
        4. Calculate entry/stop with tick adjustment
        5. Calculate risk metrics
        6. Generate executable shell script
    
    Args:
        instrument: Trading instrument
        signal_bar: Last completed bar with FDB signal
        current_bar: Current incomplete bar
        lots: Position size
        tick_shift: Tick buffer for spread
        quiet: Suppress output
        valid_gator_mouth_open_in_mouth: Require Alligator mouth validation
        validate_signal_out_of_mouth: Require bar out of mouth validation
        timeframe: Timeframe for context
        validation_timestamp: Signal bar timestamp
        verbose_level: Debug verbosity
        demo_flag: Use demo broker
    
    Returns:
        Tuple of (FDBSignalResult or None, message string)
        Returns (None, msg) if signal invalid or validation fails
    """

def generate_entry_order_script(
    lots: float,
    entry_rate: float,
    stop_rate: float,
    instrument: Instrument,
    buysell: Direction,
    tlid_id: Optional[TLID] = None,
    timeframe: Optional[Timeframe] = None,
    validation_timestamp_str: str = "",
    demo_flag: bool = True,
    total_risk: Optional[float] = None,
    risk_per_unit: Optional[float] = None,
    risk_in_pips: Optional[float] = None,
    extra_scripting_output: Optional[str] = None
) -> str:
    """
    Generate executable shell script for entry order.
    
    Output Format:
        ```sh
        ### --- COPY FROM HERE ---
        demo_arg="--demo"
        # FDB Buy Entry EUR/USD H4 - bts/now:2026-01-31 14:00/2026-01-31 14:05
        risk_in_pips=25.5
        instrument="EUR/USD";timeframe="H4";bs="B"
        tlid_id=260131140500;lots=1
        entry_rate=1.0950;stop_rate=1.0900
        jgtnewsession $tlid_id $instrument $timeframe $entry_rate $stop_rate $bs $lots $demo_arg
        zone=B-B-S-N-N;fade1=False;squat1=False;b4zlc1=5
        ### ---- COPY TO HERE ---
        ```
    """
```

---

## HTF Context Gathering

```python
def _get_htf_signal(timeframe: Timeframe) -> Optional[str]:
    """
    Gather higher timeframe context signals.
    
    For each scanned timeframe, looks up 1 and 2 levels higher to get:
        - Zone signal (buy/sell/gray)
        - MFI fade status
        - MFI squat status
        - Bars before ZLC
    
    Example for H1:
        HTF level 1 = H4
        HTF level 2 = D1
    
    Returns:
        String like "zone1=buy;fade1=False;squat1=False;b4zlc1=5;zone2=sell;..."
    """

def expand_timeframe_list(timeframes_to_parse: List[Timeframe]) -> None:
    """
    Expand timeframe list to include necessary HTF levels.
    
    If scanning m5, also need m15 for context
    If scanning m1, need m5 and m15
    
    Modifies list in place to add required timeframes.
    """
```

---

## Output Serialization

```python
from JGTOutputHelper import (
    serialize_signal_to_json_file,
    serialize_signal_to_markdown_file_from_json_file
)

# Signal saved to: data/jgt/signals/{instrument}_{timeframe}_{tlid}.json
# Markdown saved to: data/jgt/signals/{instrument}_{timeframe}_{tlid}.md
# Combined signals: data/jgt/signals/fdb_signals_out__{date}.json
# Combined script: rjgt/fdb_signals_out__{date}.sh
```

---

## CLI Usage Examples

```bash
# Scan single instrument/timeframe
fdbscan -i EUR/USD -t H4

# Scan multiple instruments
fdbscan -i "EUR/USD,SPX500,XAU/USD" -t "H1,H4,D1"

# Force fresh data (ignore cache)
fdbscan -i EUR/USD -t H4 --no-cache

# Verbose output
fdbscan -i EUR/USD -t H4 -v -v -v

# Demo mode (default)
fdbscan -i EUR/USD -t H4 --demo

# Real trading mode
fdbscan -i EUR/USD -t H4 --real

# Using environment variables
INSTRUMENTS="EUR/USD,GBP/USD" TIMEFRAMES="H1,H4" LOTS=0.1 fdbscan
```

---

## Creative Advancement Scenario

### Scenario: Morning FDB Scan

**Desired Outcome**: Trader discovers valid FDB signals at start of trading day

**Current Reality**: Markets just opened, need to find opportunities

**Natural Progression**:
1. Trader runs: `fdbscan -i "EUR/USD,GBP/USD,SPX500" -t "H1,H4"`
2. Scanner loads CDS data for each instrument/timeframe
3. For EUR/USD H4:
   - Last bar has `fdb = 1` (buy signal)
   - Current bar: High < entry_rate (signal not broken)
   - Alligator: Mouth open downward, price below lips
   - HTF D1: Zone is buy, no fade/squat
4. Signal validated, output generated:
   ```
   a=Scanning;i=EUR/USD;t=H4;vtlid=2601311400
   # FDB Buy Entry EUR/USD H4
   risk_in_pips=25.5
   . rjgt/EUR-USD_H4_260131140500.sh
   ```
5. Trader reviews and executes: `. rjgt/EUR-USD_H4_260131140500.sh`

**Resolution**: Validated trading signal with risk calculated and order ready

---

## Dependencies

```python
# External
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import signal
import atexit

# JGT Packages
from jgtpy import JGTCDSSvc as svc  # CDS data service
from jgtutils.jgtconstants import LOW, HIGH, FDB, ZONE_SIGNAL, MFI_FADE, MFI_SQUAT
from jgtutils.coltypehelper import DTYPE_DEFINITIONS
from jgtutils import jgtcommon  # CLI argument parsing
from jgtutils.iprops import get_pips  # Pip size lookup

# JGTML Internal
import tlid  # Timestamp ID generation
from xhelper import count_bars_before_zero_line_cross
from SOHelper import get_bar_at_index, get_last_two_bars
from SignalOrderingHelper import create_fdb_entry_order
from JGTOutputHelper import serialize_signal_to_json_file
import JGTBalanceAnalyzer as ba
from mlconstants import *  # Alligator column names
```

---

## Quality Criteria

✅ **Signal Validation**: Multi-layer validation (FDB → broken → Alligator → HTF)  
✅ **Risk Calculation**: Tick-adjusted entry/stop with pips risk  
✅ **Cache Management**: Timeframe-aware cache expiration  
✅ **Output Formats**: Shell script, JSON, Markdown  
✅ **HTF Context**: Higher timeframe zone/fade/squat/b4zlc  
✅ **Graceful Cleanup**: Signal handlers for SIGINT/SIGTERM  
✅ **Tracing Support**: JGTTracer integration for observability
