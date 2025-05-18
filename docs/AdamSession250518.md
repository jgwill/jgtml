# Adam Session 250518

## Questions and Answers

### What does the `jgtml` Python package produce for the data?

The `jgtml` Python package processes trading signals and stores them in a memory lattice. It integrates with various data sources and processes data to generate trading signals, handling different timeframes, directions, and indicators. The package aims to improve trading strategies by providing insights into the effectiveness of various signals and indicators.

### Explain the different components and CLIs:

#### Data components:
* 🧠 **Trading signals**: Processes trading signals and stores them in a memory lattice. Relevant files include `garden_one/trading_echo_lattice/src/echo_lattice_core.py` and `jgtml/SignalOrderingHelper.py`.
* 🐍 **Memory lattice**: Stores trading signals and their performance data, enabling recursive analysis and signal validation. Implemented in `garden_one/trading_echo_lattice/src/memory_lattice.py`.
* 🔧 **Data integration**: Integrates with various data sources and processes data to generate trading signals. Relevant files include `jgtml/jgtapp.py` and `jgtml/jgtmlcli.py`.

#### Command-line interfaces (CLIs):
* 🌀 **TradingEchoLattice CLI**: Processes trading instruments, detects breakouts, and analyzes signal performance. Implemented in `garden_one/trading_echo_lattice/cli.py`.
* 📈 **SignalOrderingHelper CLI**: Validates and processes trading signals, including FDB signals. Implemented in `jgtml/SignalOrderingHelper.py`.
* 🔁 **MemoryLattice CLI**: Interacts with the memory lattice, storing and retrieving trading signals and analysis results. Implemented in `garden_one/trading_echo_lattice/src/memory_lattice.py`.
* 📡 **Data integration CLIs**: Handle data processing and integration tasks, such as refreshing data, generating features, and updating trading signals. Relevant files include `jgtml/jgtapp.py`, `jgtml/mlfcli.py`, and `jgtml/ttfcli.py`.

### What are the `jgtml/jgtapp.py` supplying?

The `jgtml/jgtapp.py` script provides various functions to interact with trading data, including adding orders, removing orders, validating entries, and moving stops. It also includes functions for refreshing data and generating features. Some of the key functions are:
* `fxaddorder`: Adds an entry order to the market.
* `fxrmorder`: Removes an existing entry order.
* `entryvalidate`: Validates that an entry order is still valid and removes it if not.
* `fxrmtrade`: Removes/closes an existing trade.
* `fxtr`: Gets trade details and updates local trade data.
* `fxmvstop`: Moves the stop for a trade.
* `ids`: Refreshes the Indicator Data Service (IDS) data.
* `fxmvstopgator`: Moves the stop using the Gator indicator.
* `fxmvstopfdb`: Moves the stop to the Fractal Divergent Bar (FDB) signal.
* `tide`: Runs the tide alligator analysis.
* `pds`: Refreshes the PDS data.
* `cds`: Refreshes the CDS data.
* `ads`: Refreshes the ADS charts.
* `ocds`: Refreshes the CDS from old PDS.
* `ttf`: Refreshes the TTF data.
* `mlf`: Refreshes the MLF data.
* `mx`: Refreshes the MX data.
* `ttfmxwf`: Refreshes the TTF, MX, and CDS data for an instrument.
* `ttfwf`: Refreshes TTF preparation for an instrument.
