# MX Data Columns

MX files include the FDB signals and a `target` column that measures the profit or loss associated with each signal occurrence. Typical columns are:

- `fdbb`, `fdbs` – buy and sell fractal divergent bar signals
- `target` – numeric outcome for the associated trade

MX datasets may also replicate a subset of TTF or MLF features for analysis.

MX target files reside under `./data/full/targets/mx` or sometimes `./data/full/mx/targets`. They often share the same base name as the originating TTF dataset and include enough feature columns to evaluate signal quality.
