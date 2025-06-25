# Purpose of TTF Data

The **Transformed Trading Features (TTF)** files contain the core pattern columns extracted from CDS data. TTF datasets are created using the `ttf` pattern defined in `$HOME/.jgt/settings.json`, which currently includes the `mfi_sig` and `zone_sig` columns.

TTF builds directly on the CDS outputs described in [MFI_and_other_signals_indicators__250609.md](MFI_and_other_signals_indicators__250609.md).

These files provide the minimal feature set used for further lagging and signal generation. They live under `./data/full/ttf` (or `data/current/ttf` for the latest slice).

Each TTF file typically mirrors the instrument and timeframe of its source CDS file (e.g., `AUD-CAD_H4_ttf.csv`). These datasets act as the bridge between raw market data and the more expansive MLF and MX series.
