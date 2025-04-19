# 📘 Usage Guide

This guide provides detailed instructions on how to use the Trading Echo Lattice system to bridge trading signals and memory structures.

## 🧬 Basic Concepts

Before diving into specific commands, let's understand the key concepts:

- **Signal Crystallization**: The process of transforming trading signals into persistent memory structures
- **Memory Lattice**: A recursive knowledge network in Upstash Redis where signals are stored with their relationships
- **Recursive Analysis**: Analysis methods that recognize patterns across different dimensions (time, instrument, signal type)
- **Trading Adapter**: The bridge that connects to JGTML trading systems and extracts signal data

## 🚀 Command Line Interface

The Trading Echo Lattice provides a command-line interface (CLI) for all operations.

### Getting Help

```bash
# Show all available commands
python -m garden_one.trading_echo_lattice.cli --help

# Get help for a specific command
python -m garden_one.trading_echo_lattice.cli process --help
```

### Initializing the Memory Lattice

Before processing signals, you should initialize the memory lattice with essential knowledge structures:

```bash
python -m garden_one.trading_echo_lattice.cli init
```

This creates reference data and indexes in the memory lattice that help organize signals and analysis results.

### Processing Trading Signals

The core functionality is processing trading signals and storing them in the memory lattice:

```bash
python -m garden_one.trading_echo_lattice.cli process -i SPX500 -t D1,H4,H1 -d S,B
```

This command:
- Processes the SPX500 instrument
- Analyzes the D1, H4, and H1 timeframes
- Processes both Sell (S) and Buy (B) signals
- Stores the results in the memory lattice

#### Options:

- `-i, --instrument`: Trading instrument (e.g., SPX500, EUR/USD)
- `-t, --timeframes`: Comma-separated timeframes (e.g., D1,H4,H1)
- `-d, --directions`: Comma-separated directions (B,S)
- `-f, --force-refresh`: Force refresh data from source
- `--no-higher-tf`: Disable higher timeframe influence analysis

### Analyzing Signal Performance

To analyze the performance of signals stored in the memory lattice:

```bash
python -m garden_one.trading_echo_lattice.cli analyze -i SPX500 -t D1 -s mouth_is_open
```

This analyzes all "mouth_is_open" signals for SPX500 on the D1 timeframe.

#### Options:

- `-i, --instrument`: Trading instrument (optional, analyzes all if omitted)
- `-t, --timeframe`: Timeframe (optional, analyzes all if omitted)
- `-s, --signal-type`: Signal type (optional, analyzes all if omitted)
- `-l, --limit`: Maximum signals to analyze (default 100)

### Searching for High-Quality Signals

To find high-quality signal combinations in the memory lattice:

```bash
python -m garden_one.trading_echo_lattice.cli search -i SPX500 --min-win-rate 60
```

This searches for signal combinations for SPX500 with at least 60% win rate.

#### Options:

- `-i, --instrument`: Trading instrument
- `-t, --timeframe`: Timeframe (optional)
- `-s, --signal-type`: Signal type (optional)
- `--min-win-rate`: Minimum win rate threshold (default 60.0)
- `-l, --limit`: Maximum signals to analyze (default 100)

## 🔄 Advanced Usage

### Working with Different Namespaces

You can segment your memory lattice data using different namespaces:

```bash
# Initialize a separate namespace for experimental signals
python -m garden_one.trading_echo_lattice.cli -n experimental init

# Process signals in the experimental namespace
python -m garden_one.trading_echo_lattice.cli -n experimental process -i SPX500 -t D1
```

### Batch Processing Multiple Instruments

For processing multiple instruments, you can create a shell script:

```bash
#!/bin/bash
# batch_process.sh

INSTRUMENTS=("SPX500" "EUR/USD" "GBP/USD" "AUD/USD")
TIMEFRAMES="D1,H4"
DIRECTIONS="B,S"

for instrument in "${INSTRUMENTS[@]}"; do
  echo "Processing $instrument..."
  python -m garden_one.trading_echo_lattice.cli process -i "$instrument" -t "$TIMEFRAMES" -d "$DIRECTIONS"
  sleep 2
done
```

Make it executable and run it:

```bash
chmod +x batch_process.sh
./batch_process.sh
```

### Quiet Mode for Scripts

For scripting purposes, use the quiet mode to suppress output:

```bash
python -m garden_one.trading_echo_lattice.cli -q process -i SPX500 -t D1
```

## 🧪 Example Workflows

### 1. Daily Trading Signal Analysis

```bash
# Refresh and process today's signals
python -m garden_one.trading_echo_lattice.cli process -i SPX500 -t D1,H4 -d S -f

# Search for high-quality combinations
python -m garden_one.trading_echo_lattice.cli search -i SPX500 --min-win-rate 70
```

### 2. Multi-Instrument Performance Analysis

```bash
# Process multiple instruments
python -m garden_one.trading_echo_lattice.cli process -i EUR/USD -t D1,H4,H1 -d B,S
python -m garden_one.trading_echo_lattice.cli process -i GBP/USD -t D1,H4,H1 -d B,S

# Analyze specific signal types across instruments
python -m garden_one.trading_echo_lattice.cli analyze -s mouth_is_open -t D1
```

### 3. Long-term Pattern Discovery

```bash
# Process long-term timeframes
python -m garden_one.trading_echo_lattice.cli process -i SPX500 -t W1,D1 -d S

# Analyze how weekly patterns influence daily signals
python -m garden_one.trading_echo_lattice.cli search -i SPX500 -t D1 --min-win-rate 60
```

## 🔍 Understanding Output

The system provides detailed output on the console. Here's how to interpret it:

- **Processing output**: Shows the number of signals processed for each timeframe and direction
- **Analysis output**: Displays win rates, profit/loss metrics, and signal counts
- **Search output**: Lists high-quality signal combinations with their performance metrics

For more detailed output, you can explore the data directly in Upstash Redis using their console interface.

---

> 🧠 **Mia:** The usage patterns recursively build knowledge in the memory lattice.  
> 🌸 **Miette:** Each command is like tending a different part of your trading garden, watching patterns bloom across time!  
> 🎵 **JeremyAI:** The rhythmic invocation of processing and analysis creates a harmonic progression that gradually reveals market wisdom.