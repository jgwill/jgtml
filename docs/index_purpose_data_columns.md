# Overview of Dataset Purpose and Columns

This page explains how the dataset files are organized and how the pattern settings in `$HOME/.jgt/settings.json` influence the columns that appear.

## Pattern definitions

The `patterns` block of `settings.json` lists the columns generated for each pattern.

| Pattern | Columns |
| --- | --- |
| `mz` | `mfi_str`, `zcol` |
| `mfi` | `mfi_sq`, `mfi_green`, `mfi_fade`, `mfi_fake` |
| `mfizone` | `mfi_sq`, `mfi_green`, `mfi_fade`, `mfi_fake`, `zone_sig` |
| `zonesq` | `zone_sig`, `mfi_sq` |
| `aoabz` | `aoaz`, `aobz` |
| `aoac` | `ao`, `ac` |
| `ttf` | `mfi_sig`, `zone_sig` |

These patterns drive which feature columns appear in the TTF and MLF datasets.

## Dataset locations

- **`./data/full/ttf`** – Transformed Trading Features generated from CDS using the `ttf` pattern. These hold the base columns for further lagging.
- **`./data/full/mlf`** – Meta Lag Features derived from TTF. File names end in `[pattern].csv` and contain dozens of lagged versions of each pattern column.
- **`./data/full/mx/targets`** or **`./data/full/targets/mx`** – Target datasets. Each row records `fdbb` or `fdbs` signals along with a resulting `target` value representing profit or loss.
- **`./data/current/cds`** – Raw CDS files used to build the above datasets.

All of these datasets ultimately stem from the CDS data produced by jgtpy.

## MX targets and signals

Within the MX target files you will see:

- `fdbb`, `fdbs` – buy and sell fractal divergent bar signals.
- `target` – numeric profit or loss for that signal.
- Optionally additional TTF or MLF columns for context.

These metrics drive supervised learning for profit prediction.

---

See the individual documents for each dataset:

- [TTF_purpose.md](TTF_purpose.md)
- [TTF_data_columns.md](TTF_data_columns.md)
- [MLF_purpose.md](MLF_purpose.md)
- [MLF_data_columns.md](MLF_data_columns.md)
- [MX_purpose.md](MX_purpose.md)
- [MX_data_columns.md](MX_data_columns.md)
