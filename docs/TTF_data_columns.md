# TTF Data Columns

TTF files contain the core trading features derived from CDS. In addition to the raw price and alligator columns, each file includes the pattern columns defined for the `ttf` pattern.

Common columns include:

- `High`, `Low` – bar price extremes
- `ao`, `ac` – oscillator values
- `jaw`, `teeth`, `lips` – alligator averages
- `fh`, `fl` – fractal highs and lows
- `fdbb`, `fdbs` – fractal divergent bar signals
- `zlcB`, `zlcS` – zero line cross signals
- `mfi_sig`, `zone_sig` – pattern columns from `settings.json`
