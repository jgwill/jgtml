# jgtml Project Roadmap

> Updated: $(date +%Y-%m-%d %H:%M UTC)

This roadmap outlines the progressive consolidation of *jgtml* with the upgraded **jgtpy** *jgtservice* and the downstream automation in **jgtagentic**.  It is divided into incremental phases so that work can be tackled in small, verifiable units.

## Phase 1 — Service-Centric Data Refresh
- Migrate all legacy refresh/bash workflows to the unified `jgtservice` CLI.
- Provide wrapper functions so that existing helpers (`jgtmlcli`, `ttfcli`, `mlfcli`) transparently call the new service when `--fresh/--full` flags are provided.
- Validate parity against historical outputs (`_REFRESH_*` scripts) for ≥ 3 instruments × 3 timeframes.

## Phase 2 — Feature & Target Generation
- Standardise MX (target) generation using `jgtmlcli`.
- Harmonise feature extraction through `ttfcli` (TTF) and `mlfcli` (MLF) so the same instrument/timeframe invocation yields comparable CSV structures.
- Adopt a canonical column spec (incl. `fdbb`, `fdbs`, *zone*, *mfi* signals).

## Phase 3 — Model Baseline
- Create an experiment module under `jgtml/experiments/` that trains a first ML model (🎯 classification on `target`).
- Provide notebook + scripted variant powered by scikit-learn & joblib serialization.
- Ship a reference `predict_cli` that loads the model and predicts on new MX files.

## Phase 4 — Continuous Evaluation
- Add nightly GitHub Action (or cron) that:
  1. Downloads most recent data via `jgtservice refresh`.
  2. Regenerates MX/TTF/MLF.
  3. Evaluates model accuracy drift.
- Store metrics in `data/reports/metrics/*.json`.

## Phase 5 — Agentic Integration
- Expose inference endpoint through *jgtservice* (`POST /api/v1/predict`).
- Teach `fdb_scanner_2408.py` to call this endpoint for real-time decision support.
- Update *jgtagentic* to respect ML recommendations when building orders.

## Phase 6 — Documentation & Examples
- Extend `guidecli_jgtpy` docs with *ML pipeline* section.
- Publish an end-to-end tutorial under `docs/ML_Pipeline_Guide.md`.

---

Please keep this file updated as tasks move from planning to completion.
