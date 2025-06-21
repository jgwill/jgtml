# jgtapp

`jgtapp` acts as a wrapper around various trading utilities. It mirrors the original bash functions and allows you to manage orders and refresh datasets from one entry point.

## Common Subcommands
- `fxaddorder` — Add an order to the market
- `fxrmorder` — Remove a pending order
- `entryvalidate` — Cancel an order if its stop level becomes invalid
- `fxrmtrade` — Close an existing trade
- `fxtr` — Display trade details
- `fxmvstop` — Move the stop on a trade
- `fxmvstopgator` — Adjust stop based on Alligator signals
- `fxmvstopfdb` — Adjust stop using FDB breakout logic
- `tide` — Run unified Alligator analysis
- `pds`/`cds`/`ads` — Refresh data services
- `ocds` — Build CDS files from older PDS archives
- `ttf`/`mlf` — Generate pattern files
- `ttfmxwf` — Generate TTF, MX and CDS in one pass
- `mx` — Build matrix datasets from TTF patterns
- `ttfwf` — Prepare data for TTF generation
- `w` — Wait for timeframe events
- `ids` — Refresh IDS calculations

Each subcommand accepts its own options. For example:
```bash
jgtapp fxaddorder -i EUR/USD -n 0.1 -r 1.0950 -d B -x 1.0900
jgtapp cds -i EUR/USD -t D1 --fresh
```
Use `jgtapp <subcommand> --help` for a detailed list of arguments.
