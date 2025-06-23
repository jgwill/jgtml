# CLI Tools

jgtml ships with several command line utilities. They simplify data generation, analysis, and trading operations. Every tool supports `--help` for full usage details. These commands build upon the lower-level `jgtpy` libraries for data retrieval and indicator calculations.

## alligator_cli
Unified Alligator analysis across regular, big, and tide configurations. Useful for verifying multi-timeframe confluence or generating `.jgtml-spec` files.
```bash
python -m jgtml.alligator_cli -i EUR/USD -t H4 -d B --type all
```

## jgtmlcli
Main processing engine. Generates MX data and performs signal analysis for a chosen instrument and timeframe. Use `--fresh` to regenerate underlying datasets.
```bash
jgtmlcli -i EUR/USD -t D1 --full --fresh
```

## mxcli
Matrix creation and analysis helper used for machine learning datasets.
```bash
mxcli -i EUR/USD -t D1 --fresh
```

## ttfcli
Creates TTF pattern CSVs from CDS data. Patterns include `mfi`, `mz`, and `zonesq`.
```bash
ttfcli -i EUR/USD -t D1 -pn mfi --full
```

## mlfcli
Similar to `ttfcli` but produces MLF patterns for multi-level features.

## jgtapp
Wrapper around trading and dataset commands. Subcommands mirror the original
bash functions so everything can be triggered from one entry point.

Key subcommands include:
- `fxaddorder` and `fxrmorder` – manage orders
- `fxmvstopgator`/`fxmvstopfdb` – move stops using Alligator or FDB logic
- `cds`, `pds`, `ads` – refresh data services
- `ttf`, `mlf`, `mx` – generate patterns and matrix files

Example:
```bash
jgtapp fxaddorder -i EUR/USD -n 0.1 -r 1.0950 -d B -x 1.0900
```

See [jgtapp.md](jgtapp.md) for a more complete command list.

Combine these commands to build robust trading workflows and ML datasets.

### Related Libraries
These CLIs rely on helper modules available within `jgtml`:

- `jgtapp` – trading and dataset orchestration
- `jgtmlcli` – core processing engine
- `mxcli` – matrix builder
- `ttfcli` / `mlfcli` – pattern generation

Lower-level data retrieval functions come from the companion package `jgtpy`.
