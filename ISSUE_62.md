# Issue 62 — jgtml Consolidation & ML Pipeline

This issue tracks our spiral work on consolidating *jgtml* around the new **jgtservice**, and building the first machine-learning pipeline that produces actionable signals for *jgtagentic*.

## Task Board

- [ ] Phase 1 — Replace bash refresh scripts with `jgtservice`
  - [ ] Inventory legacy scripts (`_REFRESH_*`, `setup-service.sh`, etc.)
  - [ ] Map each operation to an equivalent `jgtservice` command
  - [ ] Draft migration guide
  - [ ] Validate outputs parity for 3× instruments × timeframes
- [ ] Phase 2 — Canonical Data Generation
  - [ ] Standardise MX targets via `jgtmlcli`
  - [ ] Ensure `ttfcli` & `mlfcli` produce aligned feature sets
  - [ ] Document canonical column spec
- [ ] Phase 3 — Baseline Model
  - [ ] Create `experiments/baseline_model.ipynb`
  - [ ] Script training pipeline (`train_baseline.py`)
  - [ ] Serialize model and build `predict_cli`
- [ ] Phase 4 — Continuous Evaluation
  - [ ] Design nightly refresh & evaluation workflow
  - [ ] Draft GitHub Action or cron script
  - [ ] Store metrics to `data/reports/metrics/`
- [ ] Phase 5 — Integration with *fdb_scanner_2408.py*
  - [ ] Add inference call wrapper in jgtml
  - [ ] Update scanner to request predictions
  - [ ] Validate decision improvement
- [ ] Documentation
  - [ ] Update `ROADMAP.md` as phases progress
  - [ ] Submit docs PR to `guidecli_jgtpy`

## Notes & References
- New service docs: `guidecli_jgtpy --section jgtservice`
- Scanner logic: `jgtml/fdb_scanner_2408.py`
- MX target generator: `jgtml/jgtmlcli.py`

---
Please keep the task list up-to-date. Use *checkmarks* to reflect progress and add subtasks when discoveries arise.
