# Overview

**jgtml** is a toolkit for transforming trading data into machine-learning ready structures and executing automated trading workflows. It builds upon the `jgtpy` data layer and focuses on higher-level analysis, pattern discovery, and trade management.

## Architecture
1. **Data Acquisition** – Price and indicator data is pulled via `jgtpy` and stored under `data/full`.
2. **Signal Processing** – The `jgtmlcli` and `mxcli` tools analyze signals, create matrix datasets, and validate patterns.
3. **Pattern Generation** – `ttfcli` and `mlfcli` create TTF/MLF pattern files for model training and backtesting.
4. **Trading Operations** – `jgtapp` wraps order management and integrates with Alligator-based strategies.

## Core Concepts
- **Multi-Timeframe Alligator Analysis** – Aligns regular, big, and tide alligator configurations for precise trend detection.
- **FDB Signal Validation** – Confirms fractal breakouts with additional indicators to reduce false entries.
- **Matrix Generation** – Consolidates target variables and historical signals for ML experiments.
- **Automation Hooks** – Scripts and CLIs work together for unattended dataset refresh cycles.

## Data Layout
- `data/full/cds` – Enhanced candle data with Alligator, AO, MFI, etc.
- `data/full/ttf` – Generated TTF pattern CSV files.
- `data/full/mlf` – Generated MLF pattern CSV files.
- `data/mx` – Matrix datasets built from TTF + signal labels.

## Typical Workflow
1. Refresh CDS data: `jgtapp cds -i EUR/USD -t D1`
2. Generate TTF patterns: `ttfcli -i EUR/USD -t D1 -pn mfi --full`
3. Build MX files: `mxcli -i EUR/USD -t D1 --fresh`
4. Train or evaluate your models with the matrix files.

## Integration with jgtpy
`jgtml` relies on `jgtpy` for raw data retrieval and basic indicator calculations. Most CLIs accept the same instruments and timeframe syntax. Data directories follow the same structure so results remain compatible across packages.

## Versioning
The current release is **0.0.342**. New automation scripts may bump this version as more workflows become stable.

For detailed command references see [CLI Tools](cli_tools.md). Use `guidecli_jgtml --section overview` for this page.
