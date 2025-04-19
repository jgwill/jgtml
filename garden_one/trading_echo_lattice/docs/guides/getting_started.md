# 🚀 Getting Started with Trading Echo Lattice

This guide will help you take your first steps with the Trading Echo Lattice system, establishing your own recursive bridge between trading signals and memory persistence.

## 🌱 Prerequisites

Before starting, make sure you have:

1. **Python 3.8+** installed on your system
2. **Upstash Redis** account and credentials
3. **JGTML** trading system (optional but recommended for full functionality)

## 🔍 Quick Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/jgtml.git
cd jgtml

# Set up your environment
cp .env.example .env
# Edit .env with your Upstash credentials

# Install the package
cd garden_one/trading_echo_lattice
pip install -e .
```

## 🌟 First Steps

### 1. Initialize the Memory Lattice

Your first step is to initialize the memory lattice with essential knowledge structures:

```bash
python -m garden_one.trading_echo_lattice.cli init
```

This creates reference data and indexes in your Upstash Redis database, preparing it to store trading signals and analysis results.

### 2. Process Your First Instrument

Now let's process a common instrument to generate and store signals:

```bash
python -m garden_one.trading_echo_lattice.cli process -i SPX500 -t D1 -d S
```

This processes sell signals for SPX500 on the daily timeframe. You should see output showing how many signals were processed and stored in the memory lattice.

### 3. Analyze Signal Performance

With signals stored in your memory lattice, you can analyze their performance:

```bash
python -m garden_one.trading_echo_lattice.cli analyze -i SPX500 -t D1
```

This will show you performance metrics for different signal types, including win rates, profit/loss figures, and counts.

### 4. Search for High-Quality Signals

Now let's search for high-quality signal combinations:

```bash
python -m garden_one.trading_echo_lattice.cli search -i SPX500 --min-win-rate 60
```

This will identify signal combinations for SPX500 that have at least a 60% win rate based on historical data in your memory lattice.

## 🧪 Exploring Further

### Multiple Timeframes

Process signals across multiple timeframes to see how patterns differ:

```bash
python -m garden_one.trading_echo_lattice.cli process -i SPX500 -t D1,H4,H1 -d S
```

### Multiple Instruments

Compare different instruments to find which respond best to certain signal types:

```bash
python -m garden_one.trading_echo_lattice.cli process -i EUR/USD -t D1 -d B,S
python -m garden_one.trading_echo_lattice.cli process -i GBP/USD -t D1 -d B,S
python -m garden_one.trading_echo_lattice.cli analyze -s mouth_is_open
```

## 🔄 Understanding Your Memory Lattice

Each time you process signals or perform analysis, you're building a richer knowledge structure in your memory lattice. Over time, this structure becomes more capable of recognizing complex patterns across different dimensions:

1. **Temporal Patterns**: How signals perform across different timeframes
2. **Instrument Patterns**: How different instruments respond to the same signal types
3. **Signal Combinations**: How different signal types interact and influence each other

## 🚨 Common Issues

### Connection Problems

If you see "Cannot connect to memory lattice" errors:

```bash
# Check your .env file contains the correct credentials
cat .env

# Verify Upstash connection
curl -X GET https://your-upstash-url -H "Authorization: Bearer your-token"
```

### Missing Data

If you see "No data available" or similar messages:

```bash
# Make sure JGTML is properly installed and the files are accessible
python -c "from jgtml.SignalOrderingHelper import calculate_entry_risk; print('JGTML is available')"

# Check if data directories exist
ls -la /var/lib/jgt/full
```

## 🎯 Next Steps

Once you're comfortable with the basics, explore these advanced features:

1. **Custom Namespaces**: Create separate memory spaces for different strategies
2. **Batch Processing**: Create scripts to process multiple instruments and timeframes
3. **Long-term Analysis**: Study how signal performance changes over extended periods

For more detailed information, refer to the [full documentation](../usage.md).

---

> 🧠 **Mia:** Each step builds your knowledge lattice recursively.  
> 🌸 **Miette:** With every signal you plant, your memory garden grows wiser!  
> 🎵 **JeremyAI:** Listen for the emerging patterns as trading rhythms and memory harmonies dance together.