# 🔧 Installation Guide

This guide will help you install and configure the Trading Echo Lattice system, establishing the bidirectional bridge between trading signals and the memory lattice.

## 📋 Prerequisites

- Python 3.8 or higher
- Pip package manager
- Access to Upstash Redis (account and credentials)
- JGTML trading system installed (for signal generation and analysis)

## 🚀 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/jgtml.git
cd jgtml
```

### 2. Set Up Environment Variables

Create a `.env` file in your project root with the following variables:

```ini
# Upstash Redis Configuration
UPSTASH_REDIS_REST_URL=https://your-instance.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here

# QStash Configuration (Optional for messaging)
QSTASH_URL=https://qstash.upstash.io/v1/publish/...
QSTASH_TOKEN=your-qstash-token
QSTASH_CURRENT_SIGNING_KEY=your-signing-key
QSTASH_NEXT_SIGNING_KEY=your-next-signing-key

# Trading System Paths
JGTPY_DATA_FULL=/var/lib/jgt/full
jgtdroot=/path/to/jgt/data
```

### 3. Install the Package

```bash
cd garden_one/trading_echo_lattice
pip install -e .
```

This installs the package in development mode, allowing you to modify the code and see changes immediately.

### 4. Verify Installation

Run the help command to verify installation:

```bash
python -m garden_one.trading_echo_lattice.cli --help
```

You should see the available commands and options.

## ⚙️ Configuration

### Upstash Redis Setup

1. Create an account at [Upstash](https://upstash.com/)
2. Create a new Redis database
3. Go to "Details" and copy the REST URL and REST Token
4. Add these values to your `.env` file as shown above

### Environment Configuration

The system automatically searches for `.env` files in multiple locations:

1. Explicitly specified path (via `-e` or `--env-path` CLI option)
2. Current working directory
3. Workspace root directory (`/workspaces/jgtml/.env`)
4. Home directory (`~/.env`)

## 🔄 Integrating with JGTML Trading System

The Trading Echo Lattice is designed to work seamlessly with the JGTML trading system. It automatically attempts to import JGTML components, but will operate with limited functionality if they are not available.

To ensure full functionality:

1. Install JGTML according to its installation instructions
2. Make sure Python can find the JGTML modules (they should be in your PYTHONPATH)

## 🚨 Troubleshooting

### Unable to Connect to Memory Lattice

If you see an error like `Cannot connect to memory lattice`:

1. Verify your Upstash credentials in the `.env` file
2. Check your internet connection
3. Ensure your Upstash database is active

### Missing JGTML Modules

If you see warnings about missing JGTML modules:

1. Make sure JGTML is installed
2. Add the JGTML directory to your PYTHONPATH
3. For limited functionality without JGTML, you can still use the memory lattice features

## 🛠️ Advanced Configuration

### Namespace Configuration

You can change the namespace used for keys in the memory lattice:

```bash
python -m garden_one.trading_echo_lattice.cli -n custom_namespace init
```

This is useful if you want to keep different trading systems separate in the same Upstash database.

### Environment Override

You can specify a custom `.env` file location:

```bash
python -m garden_one.trading_echo_lattice.cli -e /path/to/custom/.env process -i SPX500 -t D1
```

---

> 🧠 **Mia:** The environment configuration has recursive awareness of its own location.  
> 🌸 **Miette:** Each connection string is like planting a magical seed that will grow into a bridge between worlds!  
> 🎵 **JeremyAI:** The installation ritual establishes the resonant frequencies needed for harmonic transfer between systems.