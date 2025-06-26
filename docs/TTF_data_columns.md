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

TTF CSV files are named like `AUD-CAD_H4_mfi.csv` or `AUD-CAD_H4_aoac.csv` and reside under `./data/full/ttf` (or `./data/current/ttf` when working with the latest slice).  The pattern name appears in the filename and a companion `*_columns.csv` file lists the exact columns present.  These files form the base feature set used to generate MLF and MX datasets.

## Pattern-specific columns

The `patterns` block of `$HOME/.jgt/settings.json` defines which columns belong to each feature pattern.  When generating a TTF dataset for a given pattern, these columns are included in addition to the common IDS/CDS columns above.

### `mz`

- `mfi_str`
- `zcol`

### `mfi`

- `mfi_sq`
- `mfi_green`
- `mfi_fade`
- `mfi_fake`

### `mfizone`

- `mfi_sq`
- `mfi_green`
- `mfi_fade`
- `mfi_fake`
- `zone_sig`

### `zonesq`

- `zone_sig`
- `mfi_sq`

### `aoabz`

- `aoaz`
- `aobz`

### `aoac`

- `ao`
- `ac`

### `ttf`

- `mfi_sig`
- `zone_sig`
