# Purpose of MLF Data

**Meta Lag Features (MLF)** datasets extend TTF by generating multiple lagged versions of each pattern column. They allow the models to consider historical context across several bars and timeframes.

MLF files are produced for each pattern defined in `settings.json` and are stored in `./data/full/mlf`.

Their lag columns enable models to learn how earlier bars influence later outcomes. The names include the pattern (e.g., `_mfi.csv`) so you can quickly relate them back to the settings file.
