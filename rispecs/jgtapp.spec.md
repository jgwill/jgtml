# jgtapp (Trading Application CLI) Specification

> Unified CLI for Trading Operations and Data Workflows

**Specification Version**: 1.0  
**Module**: `jgtml/jgtapp.py`  
**CLI Command**: `jgtapp`  
**RISE Framework Compliance**: Full  
**Last Updated**: 2026-01-31

---

## Desired Outcome Definition

**What Users Create**: Executed trading operations (orders, stop management) and data pipeline commands through a unified interface.

**Achievement Indicator**: Running `jgtapp fxaddorder -i EUR/USD -n 1 -r 1.0950 -d B -x 1.0900 --demo` produces:
- Entry order placed on broker
- Order confirmation with ID

**Value Proposition**: Single command interface for entire trading workflow - from data refresh to order execution to trade management.

---

## Structural Tension

**Current Reality**: Multiple CLI tools across packages require remembering different commands.

**Desired State**: Unified `jgtapp` command with subcommands for all trading operations.

**Natural Progression**: Parse subcommand → Execute corresponding function → Output JSONL status.

---

## CLI Architecture

```
jgtapp
├── Trading Operations
│   ├── fxaddorder (add)     - Create entry orders
│   ├── fxrmorder (rm)       - Remove pending orders
│   ├── fxrmtrade (close)    - Close open trades
│   ├── fxtr                 - Get trade/order details
│   ├── fxmvstop (mv)        - Move stop loss
│   ├── fxmvstopgator        - Move stop to Alligator line
│   └── fxmvstopfdb (fdb)    - Move stop to FDB signal
│
├── Data Operations
│   ├── pds                  - Refresh price data
│   ├── ids                  - Refresh indicators
│   ├── cds                  - Refresh signals
│   ├── ads                  - Generate charts
│   ├── ttf                  - Cross-timeframe features
│   ├── mlf                  - Meta lag features
│   └── mx                   - ML matrix
│
├── Workflows
│   ├── ttfmxwf              - Full TTF→MX pipeline
│   ├── ttfwf                - TTF preparation workflow
│   ├── ocds                 - Old CDS refresh
│   └── w                    - Wait for timeframe
│
├── Analysis
│   ├── tide                 - Alligator analysis
│   └── entryvalidate        - Validate pending entry
```

---

## Trading Operations

### fxaddorder - Create Entry Order

```python
def fxaddorder(
    instrument: str,
    lots: str,
    rate: str,
    buysell: str,
    stop: str,
    demo: bool = False,
    flag_pips: bool = False
) -> None:
    """
    Create entry stop order on broker.
    
    Wraps: fxaddorder CLI from jgtfxcon
    
    Args:
        instrument: Trading pair (EUR/USD)
        lots: Position size in lots
        rate: Entry price
        buysell: Direction (B/S)
        stop: Stop loss price (or pips if flag_pips)
        demo: Use demo account
        flag_pips: Interpret stop as pips distance
    """
```

### fxrmorder - Remove Order

```python
def fxrmorder(orderid: str, demo: bool = False) -> None:
    """
    Remove pending entry order.
    
    Used when:
        - Signal invalidated
        - Stop level hit before entry
        - Trading plan changed
    """
```

### fxmvstopgator - Stop to Alligator Line

```python
def fxmvstopgator(
    i: str,                    # Instrument
    t: str,                    # Timeframe
    tradeid: str,              # Trade ID
    lips: bool = True,         # Use lips (default)
    teeth: bool = False,       # Use teeth
    jaw: bool = False,         # Use jaw
    demo: bool = False,
    skip_trade_data_update: bool = False,
    loop_action: bool = False  # Recursive on timeframe
) -> None:
    """
    Move stop to Alligator balance line.
    
    Algorithm:
        1. Get trade data (direction, current stop)
        2. Update IDS for instrument/timeframe
        3. Get current bar's Alligator values
        4. Select line (lips/teeth/jaw)
        5. Move stop to selected line value
        6. If loop_action: wait for next TF, recurse
    
    Use case:
        - Trailing stop on Alligator lines
        - Automated stop management during trade
    """
```

### fxmvstopfdb - Stop to FDB Signal

```python
def fxmvstopfdb(
    i: str,
    t: str,
    tradeid: str,
    demo: bool = False,
    close: bool = False,
    lips: bool = False,
    teeth: bool = False,
    jaw: bool = False,
    not_if_stop_closer: bool = True
) -> None:
    """
    Move stop to FDB signal level.
    
    Algorithm:
        1. Get trade data
        2. Update IDS, calculate FDB column
        3. Get last completed bar
        4. If opposite FDB signal:
           - Calculate stop from bar high/low
           - If stop already hit: close trade
           - Else: move stop to FDB level
           - Set moved_to_fdb flag
        5. If no FDB signal and lips/teeth/jaw:
           - Check if previously moved to FDB
           - If not: fallback to Alligator line
    
    Flags stored: .jgt/fdb_moved_flag_{tradeid}.json
    """
```

---

## Data Operations

### Wrappers for Pipeline CLIs

```python
def pds(instrument: str, timeframe: str, use_full: bool = True) -> None:
    """Refresh PDS (price data) via pdscli."""

def ids(instrument: str, timeframe: str, use_full: bool = False, use_fresh: bool = True) -> None:
    """Refresh IDS (indicators) via idscli."""

def cds(instrument: str, timeframe: str, use_fresh: bool = False, use_full: bool = True) -> None:
    """Refresh CDS (signals) via cdscli."""

def ads(instrument: str, timeframe: str, use_fresh: bool = False, tc: bool = True, pov: bool = False) -> None:
    """Generate ADS charts via adscli."""

def ttf(instrument: str, timeframe: str, pn: str = "ttf", use_fresh: bool = False, use_full: bool = True) -> None:
    """Generate TTF (cross-timeframe features) via ttfcli."""

def mlf(instrument: str, timeframe: str, pn: str = "ttf", total_lagging_periods: int = 5, ...) -> None:
    """Generate MLF (meta lag features) via mlfcli."""

def mx(instrument: str, timeframe: str, use_fresh: bool = False) -> None:
    """Generate MX (ML matrix) via mxcli."""
```

---

## Workflow Operations

### ttfmxwf - Full ML Preparation

```python
def ttfmxwf(instrument: str, use_fresh: bool = False) -> None:
    """
    Complete ML data preparation workflow.
    
    For each timeframe [MN, W1, D1, H4]:
        1. Refresh CDS
        2. Generate TTF (except MN)
        3. Generate MX (except MN, W1)
    """
```

### w - Timeframe Wait

```python
def w(
    timeframe: str,
    script_to_run: str = None,
    exit_on_timeframe: bool = False
) -> None:
    """
    Wait for timeframe, then execute or exit.
    
    Wraps: tfw CLI from jgtutils
    
    Used by:
        - fxmvstopgator loop_action
        - Trading campaign automation
    """
```

---

## Analysis Operations

### tide - Alligator Analysis

```python
def tide(
    instrument: str,
    timeframe: str,
    buysell: str,
    type: str = 'tide',
    quiet: bool = False
) -> None:
    """
    Unified Alligator analysis.
    
    Types:
        - tide: 144-233-377 periods (macro)
        - big: 34-55-89 periods (intermediate)
        - regular: 5-8-13 periods (quick)
        - all: All three analyses
    
    Wraps: alligator_cli unified CLI
    """
```

### entryvalidate - Validate Pending Entry

```python
def entryvalidate(orderid: str, timeframe: str, demo: bool = False) -> None:
    """
    Validate pending entry order against current price.
    
    Algorithm:
        1. Get order data (instrument, direction, stop)
        2. Check if order became a trade
        3. If still pending:
           - Get current bar close
           - If stop hit: remove order
    
    Used in campaign automation to clean invalid entries.
    """
```

---

## Helper Functions

### Trade Data Access

```python
def _get_trade_data(tradeid: str, demo: bool, fresh: bool = True) -> dict:
    """Load trade details from cached or fresh data."""

def _get_order_data(orderid: str, demo: bool) -> dict:
    """Load order details from cached or fresh data."""

def _get_instrument_from_orderid(orderid: str, demo: bool) -> str:
    """Extract instrument from order data."""

def order_became_a_trade(orderid: str, demo: bool) -> bool:
    """Check if pending order has been filled."""
```

### IDS Update

```python
def _get_ids_updated(i: str, t: str, skip_generating: bool = False) -> pd.DataFrame:
    """
    Get fresh IDS with FDB column.
    
    1. Run ids() to refresh
    2. Read IDS CSV
    3. Add FDB column via _ids_add_fdb_column_logics_v2
    """
```

---

## JSONL Output

```python
def print_jsonl_message(
    msg: str,
    extra_dict: dict = None,
    scope: str = None
) -> None:
    """
    Print structured JSONL message.
    
    Format:
        {"message": "...", "trade_id": "123", "scope": "jgtapp::fxtr"}
    """
```

---

## CLI Constants Used

```python
from jgtutils.jgtcliconstants import (
    CLI_FXADDORDER_PROG_NAME,    # fxaddorder
    CLI_FXMVSTOP_PROG_NAME,      # fxmvstop
    CLI_FXRMORDER_PROG_NAME,     # fxrmorder
    CLI_FXRMTRADE_PROG_NAME,     # fxrmtrade
    CLI_FXTR_PROG_NAME,          # fxtr
    PDSCLI_PROG_NAME             # jgtfxcli
)

from jgtpy.jgtpyconstants import (
    IDSCLI_PROG_NAME,   # idscli
    CDSCLI_PROG_NAME,   # cdscli
    ADSCLI_PROG_NAME,   # adscli
    JGTCLI_PROG_NAME    # jgtcli
)

from mlcliconstants import (
    MLFCLI_PROG_NAME,   # mlfcli
    TTFCLI_PROG_NAME,   # ttfcli
    MXCLI_PROG_NAME     # mxcli
)
```

---

## Integration Points

### jgtfxcon (Broker Layer)
- fxaddorder, fxrmorder, fxtr, fxmvstop → Direct CLI calls
- Transaction data stored in `data/jgt/fxtransact*.json`

### jgtpy (Data Layer)
- ids, cds, ads → Refresh data pipeline
- Read IDS for Alligator values

### jgtutils (Utilities)
- tfw for timeframe waiting
- FXTransact for trade data structures

### jgt-data-server
- Could expose jgtapp functions via API

### jgt-code
- Uses jgtapp for trade execution
- Medicine Wheel North direction

---

## Dependencies

```python
import subprocess
import json
from jgtutils import jgtcommon
from jgtutils.FXTransact import FXTransactWrapper, FXTrade, FXTrades
from jgtpy.JGTIDS import _ids_add_fdb_column_logics_v2
from jgtpy import jgtapyhelper as th
from SOHelper import get_bar_at_index
from alligator_cli import main as alligator_main
```

---

## Quality Criteria

✅ **Unified Interface**: All trading operations in one CLI  
✅ **Wrapper Pattern**: Delegates to specialized CLIs  
✅ **JSONL Output**: Structured logging for automation  
✅ **Demo/Real**: Account type switching  
✅ **FDB Integration**: Advanced stop management with signals  
✅ **Loop Actions**: Recursive execution on timeframes  
✅ **Campaign State**: Flag files for FDB moved tracking
