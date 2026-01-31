# Signal Ordering Helper Specification

> Entry Order Generation and Risk Calculation

**Specification Version**: 1.0  
**Module**: `jgtml/SignalOrderingHelper.py`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Executable trading entry orders from FDB signals, with tick-adjusted entry/stop rates, risk calculations, and ready-to-run shell scripts for order placement.

**Achievement Indicator**: Given a signal bar and current bar, produces:
- Tick-adjusted entry and stop rates
- Risk calculation (total, per unit, in pips)
- Executable shell script calling `jgtnewsession`
- Structured order result object

**Value Proposition**: Bridge between raw signal detection and order execution with proper risk management.

---

## Structural Tension

**Current Reality**: FDB signal detected in CDS data with raw high/low prices.

**Desired State**: Complete order specification with spread-adjusted prices, calculated risk, and executable command.

**Natural Progression**: Signal bar → Validate not broken → Validate Alligator → Calculate rates → Calculate risk → Generate script.

---

## Core Functions

### Entry Order Creation

```python
def create_fdb_entry_order(
    i: str,                              # Instrument symbol
    signal_bar: pd.Series,               # Last completed bar with FDB signal
    current_bar: pd.Series,              # Current incomplete bar
    lots: float = 1,                     # Position size
    tick_shift: int = 2,                 # Ticks to add/subtract for spread
    quiet: bool = True,                  # Suppress output
    valid_gator_mouth_open_in_mouth: bool = False,  # Require mouth validation
    validate_signal_out_of_mouth: bool = True,      # Require out-of-mouth
    t: Optional[str] = None,             # Timeframe
    validation_timestamp: Optional[datetime] = None,
    verbose_level: int = 0,
    demo_flag: bool = True               # Use demo broker
) -> tuple[Optional[dict], str]:
    """
    Create entry order from FDB signal.
    
    Returns:
        (order_result, message) - order_result is None if invalid
    
    Order Result Structure:
        {
            "sh": str,           # Executable shell script
            "entry": float,      # Entry rate
            "stop": float,       # Stop rate
            "bs": str,           # "B" or "S"
            "lots": float,       # Position size
            "tlid_id": str,      # Unique ID
            "i": str,            # Instrument
            "t": str,            # Timeframe
            "total_risk": float, # Total monetary risk
            "unit_risk": float,  # Risk per unit
            "pips_risk": float,  # Risk in pips
            "htfsig": str        # HTF context (added later)
        }
    """
```

### Rate Calculation

```python
def get_entry_stop_rate_ticked(
    i: str,                    # Instrument
    bs: str,                   # "B" or "S"
    entry_rate: float,         # Raw entry price
    stop_rate: float,          # Raw stop price
    tick_shift: int = 1,       # Tick adjustment
    rounding_add: int = 2,     # Extra decimal places
    t: Optional[str] = None    # Timeframe
) -> tuple[float, float]:
    """
    Adjust entry and stop rates with tick buffer for spread.
    
    Logic:
        pip_size = get_pips(instrument)  # e.g., 0.0001
        tick_size = pip_size / 10
        
        For Buy:
            entry_rate += tick_size * tick_shift  # Enter higher
            stop_rate -= tick_size * tick_shift   # Stop lower
        
        For Sell:
            entry_rate -= tick_size * tick_shift  # Enter lower
            stop_rate += tick_size * tick_shift   # Stop higher
        
        Round to appropriate decimal places
    
    Returns:
        (adjusted_entry_rate, adjusted_stop_rate)
    """
```

### Risk Calculation

```python
def calculate_entry_risk(
    i: str,                    # Instrument
    bs: str,                   # "B" or "S"
    entry_rate: float,         # Entry price
    stop_rate: float,          # Stop price
    position_size: float,      # Lots/units
    tick_shift: int = 1,
    rounding_add: int = 2,
    t: Optional[str] = None,
    quiet: bool = True,
    verbose_level: int = 0
) -> tuple[float, float, float]:
    """
    Calculate risk metrics for entry order.
    
    Calculation:
        pip_size = get_pips(instrument)
        risk_per_unit = abs(entry_rate - stop_rate)
        total_risk = risk_per_unit * position_size
        risk_in_pips = risk_per_unit / pip_size
    
    Returns:
        (total_risk, risk_per_unit, risk_in_pips)
    """
```

---

## Alligator Validation Functions

### Mouth State Detection

```python
def is_mouth_open(bar: pd.Series, bs: str) -> bool:
    """
    Check if Alligator mouth is open for given direction.
    
    For Buy (bs="B"):
        lips < teeth < jaw
        Alligator lines fan down, mouth opens upward
    
    For Sell (bs="S"):
        lips > teeth > jaw
        Alligator lines fan up, mouth opens downward
    
    Uses columns: 'lips', 'teeth', 'jaw'
    """

def is_big_mouth_open(bar: pd.Series, bs: str) -> bool:
    """
    Check if Big Alligator (34-55-89) mouth is open.
    
    Uses columns: 'blips', 'bteeth', 'bjaw'
    """

def is_bar_out_of_mouth(bar: pd.Series, bs: str) -> bool:
    """
    Check if price bar is outside the Alligator mouth.
    
    For Buy:
        bar.High < bar.Lips (entirely below lips)
        AND mouth not open in opposite direction
    
    For Sell:
        bar.Low > bar.Lips (entirely above lips)
        AND mouth not open in opposite direction
    """

def is_mouth_open_and_bar_out_of_it(bar: pd.Series, bs: str) -> bool:
    """
    Combined check: mouth is open AND bar is out of it.
    
    Returns:
        is_bar_out_of_mouth(bar, bs) AND is_mouth_open(bar, bs)
    """

def valid_gator(
    last_bar_completed: pd.Series,
    current_bar: pd.Series,
    bs: str
) -> bool:
    """
    Validate Alligator state for both signal bar and current bar.
    
    Both bars must have:
        - Mouth open in signal direction
        - Price out of mouth
    
    This ensures the Alligator "agrees" with the trade direction.
    """
```

### Signal Crossing Detection

```python
def is_fdbsignal_crossed_t(bar: pd.Series, bs: str, tcol: str) -> bool:
    """
    Check if FDB signal bar crosses a specific Alligator line.
    
    For Buy: bar.High < bar[tcol] (price below the line)
    For Sell: bar.Low > bar[tcol] (price above the line)
    """

def is_fdbsignal_in_big_mouth(bar: pd.Series, bs: str) -> bool:
    """Check if signal is within Big Alligator lips."""
    
def is_fdbsignal_in_big_mouth_teeth(bar: pd.Series, bs: str) -> bool:
    """Check if signal is within Big Alligator teeth."""
```

---

## Script Generation

```python
def generate_entry_order_script(
    lots: float,
    entry_rate: float,
    stop_rate: float,
    instrument: str,
    buysell: str,
    tlid_id: Optional[str] = None,
    t: Optional[str] = None,
    validation_timestamp_str: str = "",
    demo_flag: bool = True,
    total_risk: Optional[float] = None,
    risk_per_unit: Optional[float] = None,
    risk_in_pips: Optional[float] = None,
    extra_scripting_output: Optional[str] = None
) -> str:
    """
    Generate executable shell script for jgtnewsession.
    
    Output Format:
    ```sh
    ### --- COPY FROM HERE ---
    demo_arg="--demo"  # or --real
    # FDB Buy Entry EUR/USD H4 - bts/now:2026-01-31 14:00/2026-01-31 14:05
    risk_in_pips=25.5
    instrument="EUR/USD";timeframe="H4";bs="B"
    tlid_id=260131140500;lots=1
    entry_rate=1.0950;stop_rate=1.0900
    jgtnewsession $tlid_id $instrument $timeframe $entry_rate $stop_rate $bs $lots $demo_arg
    zone=B-B-S-N-N  # extra_scripting_output
    ### ---- COPY TO HERE ---
    ```
    """
```

---

## Order Result Object

```python
def build_order_result_object(
    lots: float,
    entry_rate: float,
    stop_rate: float,
    buysell: str,
    tlid_id: str,
    output_script: str,
    i: str,
    t: str,
    total_risk: Optional[float] = None,
    risk_per_unit: Optional[float] = None,
    risk_in_pips: Optional[float] = None
) -> dict:
    """
    Build structured order result object.
    
    Returns:
        {
            "sh": output_script,
            "entry": entry_rate,
            "stop": stop_rate,
            "bs": buysell,
            "lots": lots,
            "tlid_id": tlid_id,
            "i": i,
            "t": t,
            "total_risk": total_risk,
            "unit_risk": risk_per_unit,
            "pips_risk": risk_in_pips
        }
    """
```

---

## Validation Flow

```
1. Check FDB Signal
   └── signal_bar['fdb'] == 1 (buy) or -1 (sell)
   └── Return None if no signal

2. Determine Entry/Stop Rates
   └── Buy: entry=AskHigh, stop=BidLow
   └── Sell: entry=BidLow, stop=AskHigh
   └── Apply tick_shift adjustment

3. Check Signal Not Broken
   └── Buy: current.high <= entry AND current.low >= stop
   └── Sell: current.low >= entry AND current.high <= stop
   └── Return None if broken

4. Validate Alligator (optional)
   └── valid_gator_mouth_open_in_mouth: full mouth validation
   └── validate_signal_out_of_mouth: bar outside lips
   └── Return None if validation fails

5. Calculate Risk
   └── total_risk, unit_risk, pips_risk

6. Generate Script
   └── jgtnewsession command with all parameters

7. Build Result Object
   └── Complete order specification
```

---

## Column Dependencies

```python
# From CDS data
HIGH = "High"
LOW = "Low"
FDB = "fdb"           # -1 (sell), 0 (none), 1 (buy)
ASKHIGH = "AskHigh"   # Ask price high
ASKLOW = "AskLow"     # Ask price low
BIDHIGH = "BidHigh"   # Bid price high
BIDLOW = "BidLow"     # Bid price low

# Regular Alligator
JAW = "jaw"           # 13-period SMMA, shifted 8
TEETH = "teeth"       # 8-period SMMA, shifted 5
LIPS = "lips"         # 5-period SMMA, shifted 3

# Big Alligator
BJAW = "bjaw"         # 89-period SMMA
BTEETH = "bteeth"     # 55-period SMMA
BLIPS = "blips"       # 34-period SMMA
```

---

## Dependencies

```python
import datetime
from typing import Optional
import pandas as pd
import tlid                    # Timestamp ID generation
from jgtutils import iprops    # Instrument properties
from jgtutils.jgtconstants import (
    HIGH, LOW, FDB, ASKHIGH, ASKLOW, BIDHIGH, BIDLOW,
    JAW, TEETH, LIPS, BJAW, BTEETH, BLIPS, DATE
)
```

---

## Quality Criteria

✅ **Tick Adjustment**: Entry/stop adjusted for spread  
✅ **Multi-layer Validation**: Signal → Broken → Alligator  
✅ **Risk Calculation**: Total, per-unit, and pips  
✅ **Executable Output**: Ready-to-run shell script  
✅ **Structured Result**: Complete order object  
✅ **Demo/Real Support**: Flag for broker mode
