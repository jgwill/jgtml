# Required Data for Alligator Illusion Detection

This document outlines the minimal data requirements for running the Alligator Illusion detection tools contained in the `jgtml` repository. Having these datasets prepared ensures that integration with `jgtpy` and higher level workflows proceeds smoothly.

## CSV Cache Files

The detector expects CSV files in a cache directory (default: `/src/jgtml/cache/fdb_scanners`). Each file name follows the pattern:

```
<INSTRUMENT>_<TIMEFRAME>_cds_cache.csv
```

### Mandatory Columns

| Column Name Variants | Description |
|---------------------|-------------|
| `alligator_jaw`, `Alligator_Jaw`, `jaw` | Alligator jaw value |
| `alligator_teeth`, `Alligator_Teeth`, `teeth` | Alligator teeth value |
| `alligator_lips`, `Alligator_Lips`, `lips` | Alligator lips value |
| `timestamp` or `Timestamp` | Candle close timestamp |

The standalone scripts look for these columns and accept any of the variants shown.

### Example Directory Layout

```
cache/
└── fdb_scanners/
    ├── EUR-USD_D1_cds_cache.csv
    ├── EUR-USD_H1_cds_cache.csv
    └── ...
```

## Generating Data

Run the FDB scanner to produce cache files. Example:

```bash
JGT_CACHE=cache fdbscan -i EUR-USD -t H1 --refresh-cache
```

## Additional Notes

* Data should be refreshed regularly to ensure illusion detection uses recent market information.
* Ensure numeric values are stored in plain decimal form without thousand separators.
* The same CSVs can be used with the full `AlligatorIllusionDetector` and the lightweight `alligator_illusion_standalone.py`.

