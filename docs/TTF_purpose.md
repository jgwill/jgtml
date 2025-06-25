# Purpose of TTF Data

The **Transformed Trading Features (TTF)** files contain the core pattern columns extracted from CDS data. TTF datasets are created using the `ttf` pattern defined in `$HOME/.jgt/settings.json`, which currently includes the `mfi_sig` and `zone_sig` columns.

These files provide the minimal feature set used for further lagging and signal generation. They live under `./data/full/ttf` (or `data/current/ttf` for the latest slice).
