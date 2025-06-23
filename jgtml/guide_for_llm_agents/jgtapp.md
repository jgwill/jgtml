# jgtapp

`jgtapp` acts as a wrapper around various trading utilities. It mirrors
legacy bash functions and allows you to manage orders and refresh datasets from
one entry point.

## Subcommand Overview

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `fxaddorder` | Add a new order | `-i` instrument, `-n` lots, `-r` rate, `-d` buy/sell |
| `fxrmorder` | Cancel a pending order | `-id` order ID |
| `entryvalidate` | Remove order if stop becomes invalid | `-id` order ID |
| `fxrmtrade` | Close an existing trade | `-tid` trade ID |
| `fxtr` | Display trade details | `-tid` trade ID |
| `fxmvstop` | Move trade stop level | `-tid` trade ID, `-x` stop |
| `ids` | Refresh IDS calculations | `-i` instrument, `-t` timeframe |
| `fxmvstopgator` | Move stop using Alligator | `-tid` trade ID, `--lips/--teeth/--jaw` |
| `fxmvstopfdb` | Move stop using FDB breakout logic | `-tid` trade ID |
| `tide` | Unified Alligator analysis | `-i` instrument, `-t` timeframe |
| `pds` `cds` `ads` | Refresh data services | `-i` instrument, `-t` timeframe, `--fresh`|
| `ocds` | Build CDS from old PDS archives | `-i` instrument, `-t` timeframe |
| `w` | Wait for timeframe events | none |
| `ttf` | Create TTF patterns | `-i` instrument, `-t` timeframe, `-pn` pattern |
| `mlf` | Create MLF patterns | `-i` instrument, `-t` timeframe, `-pn` pattern |
| `ttfmxwf` | Generate TTF, MX and CDS together | `-i` instrument, `-t` timeframe |
| `mx` | Build matrix datasets | `-i` instrument, `-t` timeframe |
| `ttfwf` | Prepare data for TTF generation | `-i` instrument, `-t` timeframe |


Each subcommand accepts its own options. For example:
```bash
jgtapp fxaddorder -i EUR/USD -n 0.1 -r 1.0950 -d B -x 1.0900
jgtapp cds -i EUR/USD -t D1 --fresh
```
Use `jgtapp <subcommand> --help` for a detailed list of arguments.
