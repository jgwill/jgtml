# Purpose of MLF Data

**Meta Lag Features (MLF)** datasets extend TTF by generating multiple lagged versions of each pattern column. They allow the models to consider historical context across several bars and timeframes.

They rely on the same core indicators defined in the IDS/CDS stages documented in [MFI_and_other_signals_indicators__250609.md](MFI_and_other_signals_indicators__250609.md).

MLF files are produced for each pattern defined in `settings.json` and are stored in `./data/full/mlf`.

Their lag columns enable models to learn how earlier bars influence later outcomes. The names include the pattern (e.g., `_mfi.csv`) so you can quickly relate them back to the settings file.
