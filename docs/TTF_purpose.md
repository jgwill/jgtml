# Purpose of TTF Data

The **Transformed Trading Features (TTF)** files perform sophisticated **cross-timeframe feature engineering** by taking pattern-specific columns from CDS data and enriching them with higher timeframe versions of the same signals.

## Cross-Timeframe Transformation Process

TTF is not just about extracting columns - it's about **multi-timeframe context creation**:

1. **Base Pattern Extraction**: Takes pattern-specific columns from the current timeframe's CDS data
2. **Higher Timeframe Integration**: Uses `get_higher_tf_array()` to determine relevant higher timeframes
3. **Cross-Timeframe Enrichment**: For each higher timeframe, adds columns with `_TF` suffix

## Example: D1 MFI Pattern Transformation

For a D1 (Daily) timeframe with "mfi" pattern:
- **Base columns** (from D1 CDS): `mfi_sq`, `mfi_green`, `mfi_fade`, `mfi_fake`
- **Weekly enrichment**: `mfi_sq_W1`, `mfi_green_W1`, `mfi_fade_W1`, `mfi_fake_W1` 
- **Monthly enrichment**: `mfi_sq_M1`, `mfi_green_M1`, `mfi_fade_M1`, `mfi_fake_M1`

**Result**: Each D1 bar now contains not just its own MFI signals, but also the Weekly and Monthly MFI context at that point in time.

## Multi-Timeframe Context

This approach allows models to understand:
- **Current timeframe signals**: What's happening now
- **Higher timeframe trend**: What's the broader market context
- **Signal alignment**: When multiple timeframes agree or diverge

TTF builds directly on the CDS outputs described in [MFI_and_other_signals_indicators__250609.md](MFI_and_other_signals_indicators__250609.md).

These files provide the **multi-dimensional feature set** used for MLF lagging and MX target generation. They live under `./data/full/ttf` (or `data/current/ttf` for the latest slice).

Each TTF file contains transformed cross-timeframe data (e.g., `AUD-CAD_H4_mfi.csv` contains H4 data with D1, W1, M1 context). These datasets act as the bridge between single-timeframe CDS data and the temporally-aware MLF and MX series.
