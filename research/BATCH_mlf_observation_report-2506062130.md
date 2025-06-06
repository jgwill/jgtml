# Observation Report: BATCH_mlf_jgtml_250606_to_observe.sh

## Script Execution Summary

Executed `scripts/BATCH_mlf_jgtml_250606_to_observe.sh` in the lab environment without modification. The script attempts to run `mlfcli` and `jgtmlcli` for patterns `mfi zonesq aoac` across instruments `SPX500 EUR/USD` and timeframes `D1 H4`. 

Key observations from `/tmp/script_output.txt`:

- Environment activation via `conda` failed because `conda` is not installed.
- The script changed directory to `/src/jgtml`, which does not exist, causing subsequent commands to fail.
- Attempts to generate TTF data triggered `jgtfxcli` calls that resulted in repeated `ORA-499` login errors from `ForexConnect`.
- Error messages indicate failure in `_upgrade_ttf_depending_data` and `generate_mlf_feature_pattern`.

The output ended after roughly 20 lines with an exception stack trace indicating a `KeyboardInterrupt` while importing `scipy` during `jgtmlcli` execution.

## Recommendations

1. **Environment Detection**
   - Add checks for `conda` and adjust `RUN_DIRECTORY` dynamically when `/src/jgtml` is missing. Default to the current repository path.

2. **Graceful Error Handling**
   - Catch and surface exceptions from `jgtfxcli` and `jgtmlcli` with clear messaging. Include instructions on providing valid credentials or configuring offline test mode when the Forex API is unavailable.

3. **Logging Improvements**
   - Use timestamped log files and separate logs by pattern/timeframe to make investigation easier.
   - Include command echoes in the log for reproducibility.

4. **Dependency Checks**
   - Verify Python package requirements before execution and provide guidance if packages such as `scipy` are missing or incompatible with the active environment.

5. **Example Usage in Documentation**
   - Extend `README` or create a new script-specific guide explaining expected prerequisites (ForexConnect credentials, data directories) and potential troubleshooting steps.

## CLI Exploration

Running `mlfcli --help` shows options for creating lagging features from existing TTF data. Key groups cover pattern selection, output modes (`--json`, `--md`), and environment flags such as `--full/--notfull` and `--new/--old`.

`jgtmlcli --help` documents how MX data can be generated or read. It exposes gator parameters (`--ba`, `--bjaw`, etc.), pattern names and similar output toggles.

## Manual Command Attempts

`python jgtml/mlfcli.py -i SPX500 -t D1 -pn mfi --json` repeatedly failed with `ORA-499` login errors from ForexConnect. Even with fallback to `jgtapp` the TTF refresh aborted.

Invoking `python jgtml/jgtmlcli.py -i SPX500 -t D1 -pn mfi --json` resulted in `JTC is generating the CDS file(don't exist)` and exited early.

## Example Data Snapshot

Sample MX data lives in `samples/SPX500_D1.targets.mx.csv`:

```
Date,Volume,Open,High,Low,Close,Median,ao,ac,jaw,teeth,lips,...
1984-12-24 22:00:00,0,165.51,166.93,165.5,166.76,...
```

This illustrates the expected column layout for generated outputs.

## Additional Recommendations

6. **Offline Sample Data**
   - Provide pre-generated TTF and CDS files so the CLIs run without live ForexConnect access. The `samples/` directory can serve as a template.

7. **Credentials or Mock Services**
   - Clearly document where ForexConnect credentials should live or supply a mock service for testing to avoid `ORA-499` errors.

8. **CLI Documentation**
   - Embed help-text excerpts from `mlfcli --help` and `jgtmlcli --help` in the README. Encourage new users to run these commands to explore further.

9. **Test Data Directory**
   - Update tests to reference sample data under `samples/` or check that required files exist before execution.

