# TTF Data Columns

TTF files contain **cross-timeframe trading features** derived from CDS data across multiple timeframes. Each file includes both the base CDS columns for the current timeframe AND higher timeframe versions of pattern-specific columns.

The underlying IDS and CDS column definitions are listed in [MFI_and_other_signals_indicators__250609.md](MFI_and_other_signals_indicators__250609.md).

## Core CDS Columns (Base Timeframe)

All TTF files include the standard CDS columns for the current timeframe:

- `High`, `Low` – bar price extremes
- `ao`, `ac` – oscillator values
- `jaw`, `teeth`, `lips` – alligator averages
- `fh`, `fl` – fractal highs and lows
- `fdbb`, `fdbs` – fractal divergent bar signals
- `zlcB`, `zlcS` – zero line cross signals

## Cross-Timeframe Pattern Columns

TTF's **key innovation** is adding higher timeframe versions of pattern-specific columns:

### Example: D1 MFI Pattern (`AUD-CAD_D1_mfi.csv`)
**Base D1 columns**: `mfi_sq`, `mfi_green`, `mfi_fade`, `mfi_fake`  
**Cross-timeframe additions**:
- `mfi_sq_W1`, `mfi_green_W1`, `mfi_fade_W1`, `mfi_fake_W1` (Weekly context)
- `mfi_sq_M1`, `mfi_green_M1`, `mfi_fade_M1`, `mfi_fake_M1` (Monthly context)

### Example: H4 AOAC Pattern (`EUR-USD_H4_aoac.csv`)
**Base H4 columns**: `ao`, `ac`  
**Cross-timeframe additions**:
- `ao_D1`, `ac_D1` (Daily context)
- `ao_W1`, `ac_W1` (Weekly context)  
- `ao_M1`, `ac_M1` (Monthly context)

## Multi-Timeframe Column Structure

TTF creates a **multi-dimensional view** where each bar contains:
1. **Current timeframe data**: Standard CDS columns
2. **Pattern base columns**: From current timeframe
3. **Higher timeframe pattern columns**: Same indicators from broader context

**Naming Convention**: `{indicator}_{higher_timeframe}`  
**Timeframe Hierarchy**: Determined by `get_higher_tf_array()` function

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
