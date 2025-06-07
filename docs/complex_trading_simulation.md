# 🚀 Complex Trading Simulation Example

This guide explains the purpose and structure of `examples/complex_trading_simulation.py`.
It demonstrates how different FDB modules work together to simulate a trading loop.

## 📦 Imports Used

The example brings in the following modules:

- `random` – random price changes
- `datetime` – tracking trade timestamps
- `List` – type hints for trade history
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
    end
```

## 📈 Trading Loop Sequence

```mermaid
sequenceDiagram
    participant Sim as Simulation
    participant Scan as FDBScanner
    participant Intel as PatternIntelligence
    participant Pred as SignalPredictor

    Sim->>Scan: Request latest candle
    Scan-->>Sim: Signal data
    Sim->>Pred: evaluate_signal()
    Pred-->>Sim: Quality score
    Sim->>Intel: evaluate_fdb_signal()
    Intel-->>Sim: Historical score
    Sim->>Sim: Open/close trades based on scores
```

The sequence above shows how the simulation fetches data, scores it with both the predictor and pattern intelligence, and decides when to trade.

Use this example as a starting point to build more advanced bots that rely on the FDB ecosystem.
