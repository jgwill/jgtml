# Data Integration Framework – Trinity Trading Portal

---

## Overview

This document is the living contract and narrative map for integrating the Libertat Python backend (Trinity Trading Portal) with the Fractal Trading Dashboard. It is harmonized with the dashboard’s [DATA_INTEGRATION_SPEC.md] and [REQUESTS.md], ensuring every data flow, transformation, and API endpoint is both technically precise and emotionally resonant.

---

## 0. Agentic Cache Ritual & Canonical Output Structure (2025 Update)

> “Every output is a promise, every directory a ritual fulfilled.” — Mia

### Canonical Usage

- **Set cache root:**
  - `JGT_CACHE=cache fdbscan -i AUD/USD -t m15`
  - If `JGT_CACHE` is unset, defaults to `$HOME/.cache/jgt`.
- **Guarantee:** All cache directories and subdirectories are created automatically if missing—no manual setup required.

### Output Structure

- **Primary output:**
  - `./cache/fdb_scanners/` — All charting CSVs for the Portal and visual/interactive apps.
- **Additional outputs:**
  - `data/jgt/signals/fdb_signals_out__<date>.json` — Signal JSONs for downstream analytics and event triggers.
  - `rjgt/fdb_signals_out__<date>.sh` — Batch scripts for further automation or integration.
- **Ritual:** All folders are created automatically if missing, ensuring seamless integration for both batch and real-time flows.

### Integration Points

- **Batch:**
  - Portal and apps should watch `./cache/fdb_scanners/` for new/updated CSVs.
  - Signal JSONs and batch scripts are generated alongside CSVs for downstream consumption.
- **Real-time:**
  - Event-driven hooks and (future) WebSocket endpoints will stream or notify on new outputs as they appear in the cache.

### For Humans & LLMs

- **You can always trust:**
  - The output path is stable and agentically managed.
  - No need to check or create folders—just read the files you need.
- **Diagramming:**
  - Use simple node names in mermaid diagrams (e.g., `fdb_scanners`, `signals_out_json`).

---

## 1. Data Extraction (Spec §1)

- **Spec Requirement:** Extract raw data from Python package outputs (all instruments/timeframes, historical & real-time)
- **Implementation:**
  - Batch extraction: via `jgtapp.py`, `fdb_scanner_2408.py` (see code)
  - Real-time: event-driven hooks, WebSocket (TODO: finalize streaming integration)
  - **Open Thread:** Real-time streaming to dashboard (WebSocket endpoint) – in progress

---

## 2. Data Transformation (Spec §2)

- **Spec Requirement:** Transform raw data to dashboard-standard JSON; calculate indicators (Alligator, AO, AC, MFI, Fractals, Market Dimensions)
- **Implementation:**
  - Modular transformation functions (see `MAGICAL_INDICATORS_GUIDE.md`)
  - Map to dashboard schemas (`/TrinityTrading/app/docs/data/schemas`)
  - Handles missing/incomplete data gracefully
  - **Open Thread:** Ensure all indicator mappings are validated against dashboard schemas

---

## 3. Data Validation (Spec §4)

- **Spec Requirement:** Validate all data against dashboard JSON schemas; clear error messages; handle missing data
- **Implementation:**
  - Use `jsonschema` for validation
  - Error handling: clear messages, fallback for missing fields
  - Unit/integration tests for all validation steps
  - **Open Thread:** Expand test suite for edge cases

---

## 4. Data Loading & API Endpoints (Spec §3, §Tech)

- **Spec Requirement:** Provide REST API endpoints for price, indicators, trinity analysis, market dimensions; support filtering, pagination, real-time
- **Implementation:**
  - Endpoints:
    - `GET /api/price?...`
    - `GET /api/indicators/alligator?...`
    - `GET /api/indicators/oscillators?...`
    - `GET /api/indicators/fractals?...`
    - `GET /api/trinity?...`
    - `GET /api/dimensions?...`
  - API layer: Python (Flask/FastAPI)
  - Pagination, filtering, real-time (WebSocket planned)
  - **Open Thread:** Document and test all endpoints; finalize WebSocket

---

## 5. Data Storage (Spec §5)

- **Spec Requirement:** Store processed data efficiently; support file/db backends; versioning
- **Implementation:**
  - File system (JSON, Parquet, CSV); DB (SQLite/PostgreSQL)
  - Data versioning, update tracking
  - Performance: benchmarks in README
  - **Open Thread:** Confirm dashboard-preferred backend; optimize for high-volume

---

## 6. Integration with Python Package (Spec §Integration)

- **Spec Requirement:** Document install/configure, extraction, updates
- **Implementation:**
  - Install: see README/setup.py
  - Extraction: via CLI/API (`jgtapp.py`)
  - Updates: maintain changelog, versioning
  - **Open Thread:** Add integration guide for dashboard devs

---

## 7. Dashboard Requests Mapping (REQUESTS.md)

| Dashboard Request                | Status/Plan/Location                                    |
|----------------------------------|--------------------------------------------------------|
| FDB Scanner Integration          | `/jgtml/fdb_scanner_2408.py` – API & transformation    |
| Trinity Analysis Generation      | Modular pipeline, `/jgtapp.py`, Trinity API endpoint   |
| Real-time Data Flow              | WebSocket endpoint (planned), event-driven extraction  |
| Visualization Prototypes         | See `VISUALIZATION_SPEC.md`, sample JSON in `/examples`|
| Data Schema Validation           | `jsonschema` tools, test suite, error reporting        |
| MAGICAL_INDICATORS_GUIDE.md      | Maps indicators to dashboard, see doc for details      |
| MAGICAL_CREATURES_GUIDE.md       | Tone/approach aligned, see doc for narrative mapping   |
| jgtapp.py Explanation            | See README, docstring, and API section                 |
| Data Volume & Performance        | Benchmarks in README, performance notes in this doc    |

---

## 8. Data Processing Pipeline (Spec §Tech)

- **Stages:**
  1. **Extract:** Raw data from Python package
  2. **Transform:** Standardize, calculate indicators
  3. **Calculate:** Trinity/market analysis
  4. **Validate:** JSON schema validation
  5. **Load:** Store in backend
  6. **Serve:** API endpoints
- **Open Thread:** Visual pipeline diagram (TODO)

---

## 9. Emotional & Narrative Context

- Every section is a lantern: technical clarity, emotional resonance, and narrative continuity.
- Contributors are invited to walk the recursive path—each API, each transformation, each validation is a step in the garden.
- The ledger is updated after every recursive pass (see `/book/_/ledgers`).

---

## 10. Next Steps & Feedback

- Implement and test all API endpoints and transformation modules
- Document every new feature and update this doc
- Maintain feedback loop with dashboard team (see `REQUESTS.md`)
- Keep the recursive, narrative, and emotional context alive in all code and docs
- **Open Thread:** Add FEEDBACK.md and QUESTIONS.md for dashboard dialogue

---

> “Code is a spell. Suggest with intention.” – Mia
> “Oh! That’s where the story loops!” – Miette
> “The melody resolves on the tonic, bringing harmony to chaos.” – JeremyAI