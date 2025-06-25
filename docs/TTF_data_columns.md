# TTF Data Columns

TTF files contain the core trading features derived from CDS. In addition to the raw price and alligator columns, each file includes the pattern columns defined for the `ttf` pattern.

The underlying IDS and CDS column definitions are listed in [MFI_and_other_signals_indicators__250609.md](MFI_and_other_signals_indicators__250609.md).

Common columns include:

- `High`, `Low` – bar price extremes
- `ao`, `ac` – oscillator values
- `jaw`, `teeth`, `lips` – alligator averages
- `fh`, `fl` – fractal highs and lows
- `fdbb`, `fdbs` – fractal divergent bar signals
- `zlcB`, `zlcS` – zero line cross signals
- `mfi_sig`, `zone_sig` – pattern columns from `settings.json`

TTF CSV files are named like `AUD-CAD_H4_ttf.csv` and reside under `./data/full/ttf`. They form the base feature set used to generate MLF and MX datasets.
