# JGTML RISE Specifications

> Reverse-engineer → Intent-extract → Specify → Export

This directory contains RISE-compliant specifications for JGTML - the trading signal analysis platform for fractal patterns, Alligator analysis, and multi-timeframe confluence detection.

## Quick Start

1. **Start Here**: [`app.specs.md`](./app.specs.md) - Master orchestration specification
2. **FDB Scanner**: [`fdb-scanner.spec.md`](./fdb-scanner.spec.md) - Signal detection
3. **Signal Ordering**: [`signal-ordering.spec.md`](./signal-ordering.spec.md) - Entry order generation

## Specification Map

| Spec File | Status | Source Module | Purpose |
|-----------|--------|---------------|---------|
| **Signal Detection** ||||
| [fdb-scanner.spec.md](./fdb-scanner.spec.md) | ✅ Complete | fdb_scanner_2508.py | FDB signal scanning & validation |
| [signal-ordering.spec.md](./signal-ordering.spec.md) | ✅ Complete | SignalOrderingHelper.py | Entry order generation & risk |
| **Alligator Analysis** ||||
| [alligator-analysis.spec.md](./alligator-analysis.spec.md) | ✅ Complete | TideAlligatorAnalysis.py | Three-scale Alligator convergence |
| **Feature Engineering** ||||
| [ttf.spec.md](./ttf.spec.md) | ✅ Complete | ttfcli.py, ptottf.py | Cross-timeframe features |
| [mlf.spec.md](./mlf.spec.md) | ✅ Complete | mlfcli.py, realityhelper.py | Meta lag features for ML |
| [mx.spec.md](./mx.spec.md) | ✅ Complete | mxcli.py, jtc.py | ML matrix with targets |

## RISE Framework Compliance

✅ **Desired Outcome Definition** - What users CREATE, not problems to solve  
✅ **Structural Tension** - Current reality vs desired state drives progression  
✅ **Natural Advancement** - Clear flow from current to desired  
✅ **Autonomous Specification** - Another LLM could implement from spec alone  
✅ **Complete Type Definitions** - Full function signatures and data structures

## Key Concepts

### Three Alligator Periods
1. **Regular** (5-8-13) - Quick direction, day trading
2. **Big** (34-55-89) - Swing trading, weekly cycles
3. **Tide** (144-233-377) - Position trading, monthly trends

### Feature Engineering Pipeline
```
CDS (signals) → TTF (cross-timeframe) → MLF (meta lag) → MX (ML-ready)
```

### Core Tools
- `fdbscan` - FDB signal scanning
- `jgtapp` - Main CLI with trading commands
- `alligator_cli` - Multi-Alligator analysis
- `ttfcli` / `mlfcli` / `mxcli` - Feature generation

## Specification Version

- **Version**: 1.1
- **Framework**: RISE
- **Created**: 2026-01-31
- **Updated**: 2026-01-31 (detailed module specs)
