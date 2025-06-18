# Narrative Map

## Recent Commits

- **4bd1fce** `chmod` – permission adjustments for scripts.
- **225c2a4** `Add new documentation for Starting New Phases of Work` – added docs about workflow phases.
- **5446cc9** `Add Enhanced Trading CLI for Integrated FDB and Illusion Detection` – extended CLI capabilities.
- **393164c** `Add Enhanced FDB Scanner with Alligator Illusion Detection` – improved scanning features.
- **f86105b** `Add Phase 2 Alligator Illusion Detection Test Script` – provided additional tests.

## Current Update

Implemented graceful dependency check in `jgtml/ttfcli.py` and updated `README.md` to mention installing `python-dateutil` if missing.

Enhanced packaging by adding `python-dateutil` directly to `requirements.txt` and `pyproject.toml` so installs include this pandas dependency automatically.

- **caea33f** `fix: handle missing illusion count` – improved resilience of enhanced FDB scanner and added CLI entrypoint.
Updated CLI offerings with 'enhancedfdbscan' command and improved error handling.
- Fixed idscli call to avoid conflicting -new/-old flags.
- Updated cdscli invocation to pass -uf/-nf flags correctly.
- Confirmed wrapper flags match underlying CLI help outputs to prevent future argument mismatches.
- Documented CLI flag fixes in CHANGELOG
