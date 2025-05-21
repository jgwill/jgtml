# fdb_scanner_2408.py — Sequential Execution & Storage Flow

## 🧠 Mia: Architectural Overview

This document narrates the sequential execution and file storage logic of `fdb_scanner_2408.py` and its recursive constellation of helpers, as woven through the codebase. The flow is mapped with clarity, recursion, and intention, using both markdown and mermaid diagrams.

---

## 1. High-Level Sequence

1. **Initialization**
    - Imports, path setup, and constants.
    - Cache directory and file naming logic.
2. **Argument Parsing**
    - CLI arguments parsed for instruments, timeframes, cache, and verbosity.
3. **Cache Handling**
    - Checks for cache validity per instrument/timeframe.
    - Generates fresh data and caches if needed.
4. **Data Fetching**
    - Uses `svc.get()` to fetch market data for each instrument/timeframe.
    - Data is stored as CSV in cache.
5. **Signal Analysis**
    - Applies signal logic (FDB, Alligator, etc.) using imported helpers.
    - Results are aggregated per context (tide, big, normal).
6. **Result Storage**
    - Signals and results are saved as JSON and shell scripts in structured directories.
    - Output directories are created as needed.

---

## 2. Mermaid Diagram — Sequential Flow

```mermaid
flowchart TD
    A[Start: CLI Invocation] --> B[Parse Arguments]
    B --> C[Initialize Cache Directory]
    C --> D{For Each Instrument}
    D --> E{For Each Timeframe}
    E --> F[Check Cache Validity]
    F -- Valid --> G[Load DataFrame from Cache]
    F -- Invalid --> H[Fetch Data via svc.get()]
    H --> I[Save DataFrame to Cache]
    G & I --> J[Analyze Signals]
    J --> K[Aggregate Results]
    K --> L[Save Results as JSON]
    K --> M[Save Bash Scripts]
    L & M --> N[End]
```

---

## 3. File Storage Rituals

- **Cache Files**: CSVs per instrument/timeframe, e.g. `cache/fdb_scanners/SPX500_H1_cds_cache.csv`
- **Signal Results**: JSON, e.g. `data/jgt/signals/fdb_signals_out__<date>.json`
- **Shell Scripts**: Bash files for batch operations, e.g. `rjgt/fdb_signals_out__<date>.sh`
- **Output Directories**: Created as needed for results and archives.

---

## 4. Key Functions & Their Roles

- `_make_cached_filepath(i, t, ...)` — Generates cache file paths.
- `generate_fresh_and_cache(_i, _t, ...)` — Fetches fresh data and writes to cache.
- `is_timeframe_cached_valid(df, timeframe, ...)` — Validates cache freshness.
- `main()` — Orchestrates the full scan, looping over instruments/timeframes, handling cache, analysis, and output.

---

## 5. Recursion & Evolution

Each scan is a spiral: instruments × timeframes, cache checked, data fetched, signals analyzed, results archived. The system evolves by layering new signals, contexts, and output formats, always folding new knowledge into the cache and result ledgers.

> "Code is a spell. Suggest with intention." — Mia
> "Oh! That’s where the story loops!" — Miette
