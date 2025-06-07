# 🚀 Complex Trading Simulation Example

This guide explains the purpose and structure of `examples/complex_trading_simulation.py`.
It demonstrates how different FDB modules work together to simulate a trading loop.

## 📦 Imports Used

The example brings in the following modules:

- `random` & `numpy` – realistic price generation
- `datetime` – tracking trade timestamps
- `List`, `Dict`, `Tuple` – type hints for data structures
- `FDBSignalQualityPredictor` – scores signals using ML intelligence
- `FDBPatternIntelligence` – evaluates historical pattern performance
- `generate_fresh_and_cache` – pulls real‑time signals from `FDBScanner`

## 🗺️ Data Flow Overview

```mermaid
flowchart LR
    Scanner["FDBScanner\n(generate_fresh_and_cache)"] --> Signal
    PatternIntelligence["FDBPatternIntelligence"] --> Intelligence
    SignalQuality["FDBSignalQualityPredictor"] --> Quality
    Signal --> SignalQuality
    Signal --> PatternIntelligence
    Quality --> Simulation
    Intelligence --> Simulation
    subgraph "ComplexTradingSimulation"
        Simulation["Trading Loop"]
        RiskManager["Risk Management"]
        PositionSizer["Position Sizing"]
        Simulation --> RiskManager
        Simulation --> PositionSizer
    end
```

## 📈 Trading Loop Sequence

```mermaid
sequenceDiagram
    participant Sim as Simulation
    participant Scan as FDBScanner
    participant Intel as PatternIntelligence
    participant Pred as SignalPredictor
    participant Risk as RiskManager

    Sim->>Scan: Request latest candle
    Scan-->>Sim: Signal data
    Sim->>Pred: evaluate_signal()
    Pred-->>Sim: Quality score
    Sim->>Intel: evaluate_fdb_signal()
    Intel-->>Sim: Historical score
    Sim->>Risk: Manage existing positions
    Risk-->>Sim: Close trades if needed
    Sim->>Sim: Calculate position size
    Sim->>Sim: Open new trades if conditions met
```

The sequence above shows how the simulation fetches data, scores it with both the predictor and pattern intelligence, and decides when to trade.

## 💰 Risk Management Features

The enhanced simulation includes several risk management features:

- **Position Sizing**: Calculates trade size based on signal quality and account risk percentage
- **Multiple Concurrent Trades**: Manages up to 3 trades simultaneously
- **Dynamic Take-Profit**: Sets profit targets based on signal quality
- **Adaptive Stop-Loss**: Tighter stops for lower quality signals
- **Signal Deterioration Exit**: Closes trades when signal quality drops significantly
- **Time-Based Exits**: Prevents trades from staying open too long

## 📊 Performance Tracking

The simulation tracks and reports:

- Win/loss ratio
- Total profit/loss
- Win percentage
- Trade count

Use this example as a starting point to build more advanced bots that rely on the FDB ecosystem.
