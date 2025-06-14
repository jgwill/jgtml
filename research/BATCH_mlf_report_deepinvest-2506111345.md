# Batch Script Deep Investigation 250611

## Overview
This session attempted to run `scripts/BATCH_mlf_jgtml_250606_to_observe.sh` with default instruments and patterns. The script now detects the repository path and logs to `logs/`.

## Observed Output
Errors surfaced immediately when `mlfcli` invoked `jgtfxcli` to load price data. Each call returned `ORA-499` login failures from ForexConnect. Subsequent attempts to generate TTF data crashed with `TypeError: object of type 'NoneType' has no len()`. The log `logs/20250611134322_batch.log` captures these failures in detail.

Attempts to generate missing test caches using `JGT_CACHE=tests/fdb_data python jgtml/fdb_scanner_2408.py -i AUD/CAD -t H1` also failed with the same login error, preventing test data generation.

`pytest` continues to fail because `tests/fdb_data/AUD-CAD_H1_cds_cache_24082107.csv` does not exist. Without valid login credentials or offline data, the batch script and test suite cannot complete successfully.

## Recommendations
1. **Provide Offline Sample Data**: Include minimal CSVs under `tests/fdb_data` or `samples/` so the script and tests do not rely on ForexConnect.
2. **Mock ForexConnect**: Implement a stub or environment variable to bypass login during local testing.
3. **Graceful Error Handling**: Detect login failures early and abort the script with a helpful message, avoiding large stacks in the logs.
4. **Document Credentials**: Clarify where to supply ForexConnect credentials if live data is required.

