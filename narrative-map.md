# Narrative Map

## Recent Commits

- **4bd1fce** `chmod` – permission adjustments for scripts.
- **225c2a4** `Add new documentation for Starting New Phases of Work` – added docs about workflow phases.
- **5446cc9** `Add Enhanced Trading CLI for Integrated FDB and Illusion Detection` – extended CLI capabilities.
- **393164c** `Add Enhanced FDB Scanner with Alligator Illusion Detection` – improved scanning features.
- **f86105b** `Add Phase 2 Alligator Illusion Detection Test Script` – provided additional tests.

## Current Update

Implemented graceful dependency check in `jgtml/ttfcli.py` and updated `README.md` to mention installing `python-dateutil` if missing.

Enhanced packaging by adding `python-dateutil` directly to `requirements.txt` and `pyproject.toml` so installs include this pandas dependency automatically.

- **caea33f** `fix: handle missing illusion count` – improved resilience of enhanced FDB scanner and added CLI entrypoint.
Updated CLI offerings with 'enhancedfdbscan' command and improved error handling.
- Fixed idscli call to avoid conflicting -new/-old flags.

### branch: codex/fix-conflict-between--new-and--old-arguments-2025-06-18-16-30-36
- Updated cdscli invocation to pass -uf/-nf flags and validated wrappers, documenting fixes in CHANGELOG. Merged main at version 0.0.333 to integrate trading orchestrator.


### Latest Consolidation
- **67f0f1b** `Update version to 0.0.331` – preparing for new orchestrator features.
- **9bc2122** `Add new markdown for Unified Trading System` – document integration design.
- **9ba1311** `Add observation processor` – supports natural language market analysis.
- **19064dd** `Add unified trading loop` – centralizes trading system operations.
- **6b76b79** `Remove unused paths` – cleanup workspace settings.
- **e147f10** `Add JGT Unified FDB Scanner` – advanced market scanning script.
- **9b4877b** `Add test mode flag` – enables dry-run capability.
- **8e5cf36** `Add Trading Orchestrator` – orchestrates trading flows with scheduling.
- **d912369** `Update version to 0.0.332` – finalize stable release after integration.

- **de8d4fc** `Consolidation record` – confirmed branch merge and updated logs.

### Branch: codex/fix-conflict-between--new-and--old-arguments-2025-06-18-16-30-36
- Logged merge resolution in `ledger-merge-main-resolution-2506182049.json`
- **5a3b4b9** `fix: ensure enhancedtradingcli import path` – updated path handling for CLI.

- **9d5da56** `feat: expose pattern generation helpers` – added generate_ttf_for_pattern and generate_mlf_for_pattern for internal use.
- **c862081** `chore: log ledger for ttf/mlf helper addition` – recorded changes supporting automated dataset generation.
