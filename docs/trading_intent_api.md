# 📡 Trading Intent Capture API

This document proposes a structured HTTP interface for recording trader observations and generating `.jgtml-spec` packages.

## NOTICE

* This is really just a first Scaffolding to work with that Specification Language that this package would receive.  see jgwill/jgtagentic repository documentation for more.

## Overview

Traders narrate their market analysis across multiple instruments and timeframes. The API maintains session state so that an LLM can transform these observations into a specification. This design supports real-time voice or text input and allows a stateless LLM to recall the full context.

> **Note from William**: The flow below is still evolving. The sequential, multi-timeframe rhythm of an actual trading session may require further refinement. Treat this specification as a draft for future tightening.

## Endpoints

### `POST /intent/initiate`
Start a new intent session.
- **Payload**:
  ```json
  {
    "instrument": "EUR/USD",
    "timeframes": ["H4", "H1"]
  }
  ```
- **Returns**: `{ "session_id": "uuid", "timestamp": "ISO-8601" }`

### `POST /intent/observe`
Send a raw observation string.
- **Payload**:
  ```json
  {
    "session_id": "uuid",
    "observation": "Wave 3 complete, AO rising"
  }
  ```
- The LLM interprets and appends to the session state.

### `GET /intent/state`
Retrieve current session information.
- **Response**:
  ```json
  {
    "current_observations": ["..."],
    "inferred_components": {"bias": "bullish"},
    "pending_slots": ["wave_count"]
  }
  ```

### `POST /intent/label`
Annotate or correct an element.
- **Payload**:
  ```json
  {
    "session_id": "uuid",
    "label_type": "wave_count",
    "value": "Wave 3 complete"
  }
  ```

### `POST /intent/confirm`
Finalize the `.jgtml-spec` generation.
- **Payload**: `{ "session_id": "uuid" }`
- **Returns**:
  ```json
  {
    "jgtml_spec": "<YAML representation>",
    "signal_package_preview": "..."
  }
  ```

### `GET /intent/history`
Retrieve past specifications or narrative echoes.

## Requirements
- Support partial or streaming-style input.
- Stateless LLMs should fetch session context at any time.
- Clean JSON schemas.
- Extendable for voice input and echo crystallization.

This API is intended to integrate with the broader `jgtagentic` ecosystem and enable recursive narrative capture from trader to specification.
