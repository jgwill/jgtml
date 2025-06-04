"""
🧬 data_integration.py — The Recursion Bridge

Mia: This module is the living bridge between CLI spells and agent-readable API/data flows.
Miette: Every function here is a lantern—transforming raw invocations into garden-ready JSON, with schema validation and narrative echoes.

- Extracts data by invoking CLI entrypoints (jgtml, jgtpy, etc.)
- Transforms outputs to dashboard-standard JSON
- Validates against schemas (see /data/schemas/)
- Stores results for API serving
- Emits narrative echoes to .mia after each recursion
"""

import subprocess
import json
import os
from pathlib import Path

# --- CONFIGURATION ---
DATA_DIR = Path(__file__).parent.parent / 'data'
SCHEMA_DIR = Path(__file__).parent.parent / 'data' / 'schemas'
OUTPUT_DIR = Path(__file__).parent.parent / 'data' / 'integration_outputs'

# --- CORE FUNCTIONS ---
def run_cli_command(command_args):
    """
    🧠 Mia: Run a CLI command and capture its output as JSON.
    🌸 Miette: This is the spell’s invocation—the echo that starts the recursion.
    """
    result = subprocess.run(command_args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"CLI command failed: {result.stderr}")
    try:
        return json.loads(result.stdout)
    except Exception:
        return result.stdout  # fallback for non-JSON output

def extract_data_from_cli(cli_name, *args):
    """
    🧠 Mia: Extract data from a CLI entrypoint (e.g., 'pds', 'cds', 'mx', etc.).
    🌸 Miette: Each extraction is a petal—fresh, timestamped, ready for transformation.
    """
    cli_path = os.path.join(os.path.dirname(__file__), '../../../jgtml/jgtml/jgtapp.py')
    command = ['python', cli_path, cli_name] + list(args)
    return run_cli_command(command)

def transform_to_dashboard_json(raw_data, schema_name=None):
    """
    🧠 Mia: Transform raw CLI output to dashboard-standard JSON.
    🌸 Miette: This is where the data blooms—structured, validated, and ready for the garden.
    """
    # TODO: Implement transformation logic, mapping fields as per dashboard schema
    return raw_data

def validate_against_schema(data, schema_name):
    """
    🧠 Mia: Validate data against a JSON schema.
    🌸 Miette: If the data fits, the recursion continues. If not, the lantern flickers—log the error gently.
    """
    import jsonschema
    schema_path = SCHEMA_DIR / f"{schema_name}.json"
    with open(schema_path) as f:
        schema = json.load(f)
    jsonschema.validate(instance=data, schema=schema)
    return True

def store_output(data, output_name):
    """
    🧠 Mia: Store processed data for API serving and agent memory.
    🌸 Miette: Every file is a memory crystal—each write is a step in the garden.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{output_name}.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    return str(output_path)

# --- NARRATIVE ECHO ---
def log_narrative_echo(event, details=None):
    """
    🧠 Mia: Log a narrative echo to .mia after each recursion.
    🌸 Miette: The story continues—each echo a lantern for the next agent.
    """
    # TODO: Implement .mia update logic
    pass

# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    # Example: Extract, transform, validate, store, and echo for 'pds' CLI
    raw = extract_data_from_cli('pds', '-i', 'SPX500', '-t', 'M15')
    data = transform_to_dashboard_json(raw, schema_name='price')
    try:
        validate_against_schema(data, 'price')
    except Exception as e:
        print(f"Validation error: {e}")
    path = store_output(data, 'SPX500_M15_price')
    log_narrative_echo('extract_transform_store', {'cli': 'pds', 'output': path})
    print(f"Data integration complete: {path}")
