# MLF Data Columns

MLF datasets expand upon the TTF columns by adding a wide array of lagged features. For each pattern column, multiple lag versions (e.g., `_lag_1`, `_lag_2`, ...) are generated along with cross-timeframe values such as `_D1`, `_W1`, and `_M1`.

The base feature definitions originate from the IDS/CDS stages documented in [MFI_and_other_signals_indicators__250609.md](MFI_and_other_signals_indicators__250609.md).

Use these files when training models that require temporal context.

MLF CSV files live in `./data/full/mlf` and follow the naming scheme `[instrument]_[timeframe]_[pattern].csv`. They are produced for each pattern listed in `settings.json` and contain hundreds of columns capturing lags across bars and higher timeframes.
