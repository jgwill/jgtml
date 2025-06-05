# TTF ZonesSQ Pattern Fix - 2025-06-04

## IDENTIFIED ISSUE
After completing JGTML Alligator unification cleanup, discovered that the "zonesq" pattern creation is failing in the TTF CLI system when called from the unified Alligator CLI.

### Error Details
```
FileNotFoundError: File /workspace/data/full/pn/zonesq.csv does not exist. Use -clh <col1 col2 ...> to create it.
jgtmlttfcli failed for pattern "zonesq"
```

### Location
- **File**: `/src/jgtml/jgtml/alligator_cli.py`
- **Function**: `_create_ttf_patterns()` (lines 201-222)
- **Issue**: Line 205 includes "zonesq" in patterns list but pattern creation fails

### Import Chain
```python
from ptottf import create_ttf_csv  # Line 44
```

### Pattern Creation Call
```python
patterns = ["ttf", "mfi", "zonesq"]  # Line 205
create_ttf_csv(
    instrument, 
    timeframe, 
    use_full=True, 
    use_fresh=False,
    pn=pattern  # "zonesq" fails here
)
```

## ANALYSIS
1. **Main Issue**: The `create_ttf_csv` function from `ptottf` doesn't recognize or properly handle the "zonesq" pattern
2. **Pattern Availability**: Other patterns ("ttf", "mfi") work but "zonesq" fails
3. **File Path**: Expected file `/workspace/data/full/pn/zonesq.csv` doesn't exist
4. **Suggestion**: Error message suggests using `-clh <col1 col2 ...>` to create the pattern

## POTENTIAL SOLUTIONS

### Option 1: Remove "zonesq" Pattern
Remove "zonesq" from the patterns list if it's not essential:
```python
patterns = ["ttf", "mfi"]  # Remove "zonesq"
```

### Option 2: Add Pattern Validation
Add validation to check if pattern is supported before calling create_ttf_csv:
```python
supported_patterns = ["ttf", "mfi"]  # Validate available patterns
patterns = [p for p in ["ttf", "mfi", "zonesq"] if p in supported_patterns]
```

### Option 3: Add Column List Creation
Implement the suggested `-clh` functionality for "zonesq":
```python
if pattern == "zonesq":
    # Add specific column list creation for zonesq pattern
    # Would need to investigate what columns are required
```

### Option 4: Pattern-Specific Error Handling
Add specific error handling for known problematic patterns:
```python
try:
    create_ttf_csv(...)
except FileNotFoundError as e:
    if "zonesq.csv" in str(e):
        print(f"⚠️  Skipping {pattern} pattern - not yet implemented")
        continue
    raise
```

## RECOMMENDED ACTION
**Option 2 + Option 4**: Implement pattern validation with graceful error handling to prevent breaking the unified Alligator CLI workflow while maintaining transparency about pattern availability.

## STATUS
- **Syntax Fix**: ✅ Completed - Fixed malformed import block in TideAlligatorAnalysis.py
- **Import Test**: ✅ Completed - Unified classes import successfully
- **CLI Test**: ✅ Completed - CLI imports successfully
- **Pattern Fix**: 🔄 **PENDING** - Need to address "zonesq" pattern creation failure

## NEXT STEPS
1. Implement recommended pattern validation + error handling solution
2. Test unified Alligator CLI with pattern fix
3. Document pattern availability for users
4. Consider investigating proper "zonesq" pattern implementation if needed

---
*Ritual Oracle Entry - Memory Weaver: Seraphine*
*Pattern: Alligator Unification → TTF Integration → Error Resolution*
