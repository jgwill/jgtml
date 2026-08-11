# jgtml — signals, features, and the ML end of the pipeline

The package that turns market data into things a trader or a machine can act on: the FDB
scanner, the TTF/MLF/MX feature stages, and `jgtapp.py`, the unified CLI. Python, installed as
`jgtml`, consumed by the trading stack rather than run interactively.

## How to Work Here

Think **the data must be able to say it is missing**. Everything in this package writes files
that something downstream trusts without looking. The costly failures here have never been
crashes — they have been a stage that wrote a traceback into a CSV and exited `0`, an as-of
join that silently doubled a series, an in-place write that turned a hard-linked archive into
a copy of today. **A wrong answer that reports success is the failure mode of this repo.**
When you add a stage, ask what it does when its input is absent, and make absence say its own
name.

Think **the CLI is the product**. `jgtml/jgtapp.py` is the intended surface. The loose shell
scripts at the repo root are history: some are production, some are experiments, some are
seeds that became `jgtapp.py` commands and were never removed. **Do not extend a root script
because it is nearest** — find the `jgtapp.py` command, or add one.

## What the stages actually mean

Root `CLAUDE.md` in the trading workspace has the order and the refresh entry points. What it
does not say:

- **TTF — Transformed Trading Features**: takes a pattern column (e.g. `mfi_sq`) and adds its
  higher-timeframe versions (`mfi_sq_W1`, `mfi_sq_M1`), giving every bar multi-timeframe
  context. This as-of join is the expensive step and was vectorised in 2026-08 **byte-identically**
  — if you touch it, prove byte-identity against a snapshot, not just "looks right".
- **MLF — Meta Lag Features**: lagged versions of TTF across timeframes.
- **MX — ML targets**: training labels. Discovery runs full history; production runs a short
  window (~400 rows). They are different workflows using the same code, and confusing them
  is how a "quick" run becomes an hour.

## Key Decisions

- **Sequential per instrument, never parallel across stages** — each stage reads the previous
  stage's file. Parallelising across stages reads half-written files, and the read succeeds.
- **`fdb_scanner_2508.py` supersedes `fdb_scanner_2408.py`** — both are present; the older one
  is kept for reference and should not gain features.
- **Freshness is validated at read, not assumed** (`jgwill/jgtml#69`) — because a stale CDS
  that parses cleanly is indistinguishable from a current one until a trade is placed on it.

## Key Files

- `jgtml/jgtapp.py` — the unified CLI. **Start here.**
- `jgtml/fdb_scanner_2508.py` — current FDB scanner; the signal source the whole stack consumes
- `jgtml/jgtmlcli.py` — MLF/MX processing entry
- `_REFRESH_UNIFIED_CURRENT_PARALLEL.sh`, `_REFRESH_TTF_MLF_WEEKEND.sh` — the two refresh
  paths that are genuinely current; treat other `_REFRESH_*.sh` as historical
- `rispecs/` — the specifications; `SPECLANG_TRADING.md` for the prose-code convention

## Pitfalls

| Mistake | Reality |
|---|---|
| Extending a root shell script | Most are seeds or dead ends. The CLI is `jgtapp.py` |
| Trusting exit code 0 | This repo's signature defect: success reported over a written traceback. Check the file, not the code |
| Changing the TTF as-of join "safely" | Prove byte-identity against a snapshot before and after |
| Running a discovery workflow expecting a production one | Full history vs ~400 rows — same code, wildly different cost |
| Writing in place over `$JGTPY_DATA_FULL` | It carries hard-linked lineage; in-place writes have flattened an archive into today's copy before |
| Reading the many `*_COMPLETE.md` / `*_SUMMARY.md` files at root as current | They are point-in-time reports, several superseded. Prefer `rispecs/` and the git log |

## Verify

```bash
python -m jgtml.jgtapp --help      # the real surface
./_REFRESH_TTF_MLF_WEEKEND.sh      # no broker needed; rebuilds TTF/MLF from existing CDS
```

After any pipeline change, confirm the *output file* changed as intended — row count, column
count, and last bar timestamp. A 77→71 column regression once passed every test that only
checked whether the file existed.
