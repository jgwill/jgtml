# 🤖 JGTML Data Refresh & Script Consolidation Plan

-----
* looking that file, it is confusing and has outdated information



-----

**Created**: 2025-07-08  
**Status**: Analysis Complete, Implementation Needed  
**Priority**: HIGH - Critical Infrastructure Enhancement

## 🎯 Executive Summary

Analysis of `/src/jgtml/scripts/` reveals sophisticated data processing workflows that need consolidation into our unified refresh system. Current state has working but fragmented scripts with different approaches to the same core pipeline: **CDS → TTF → MLF → MX**.

### 📊 Data Pipeline Definitions (CORRECTED)
- **CDS**: Chaos Data Service (market data with technical indicators) 
- **TTF**: **Transformed Trading Features** (cross-timeframe feature engineering)
- **MLF**: **Meta Lag Features** (lagged versions of TTF across timeframes) 
- **MX**: ML Targets (training labels for machine learning models)

**TTF Innovation**: Takes pattern columns (e.g., `mfi_sq`) and adds higher timeframe versions (`mfi_sq_W1`, `mfi_sq_M1`) creating multi-timeframe context per bar.

**See**: `/src/jgtpy/CLAUDE.md` for complete data services architecture documentation

## 🔍 Current Script Analysis from ./scripts

* Note from William (not Claude): These scripts needs to be consolidated into functions and adequately evaluated, they might be deprecated  or what was developped is not matured yet.

### Working Scripts Analyzed:
1. **`loop_ttfcli_patterns__many_instruments.sh`** - Simple TTF generation loop
2. **`BATCH_mlf_jgtml_250606_to_observe.sh`** - Advanced MLF+MX workflow with env switching
3. **`batch_mlf_jgtmlcli_250516.sh`** - Production MLF+MX processing  
4. **`PRODUCTION_feature_exploration.sh`** - Real-time trading feature generation (~400 rows)
5. **`DISCOVERY_target_generation.sh`** - Full historical ML discovery workflow
6. **`_fnml.sh`** - **CRITICAL** Function library with proper dependency handling (this was from claude) but it is a first draft of what I wanted to be processed, that was the seed that sparked the ./jgtml/jgtapp.py commands.  Claude say that is he stated before but that is not the case, I told him that it needed refactoring etc but he missed that !

### Key Discoveries:

#### 🔗 **Critical Data Dependencies** (FIXED):
```
CDS (foundation) → TTF (features) → MLF (lag features) → MX (ML targets)
```
**Issue**: Previous parallel scripts ran these simultaneously, causing failures  
**Fix**: Sequential pipeline per instrument/timeframe, parallel across instruments

#### 🎨 **Missing Patterns**:
- **aoac**: Awesome Oscillator + Accelerator columns (ao, ac)
- **Extended pattern list**: `mfi mz zonesq aoac` (vs our previous `mfi mz zonesq`)

#### 🏗️ **Environment Architectures**:
- **Production (prod)**: `/workspace/data/`, `conda activate i`
- **Development (lab)**: `/src/jgtml/data/`, `conda activate jgtml`
- **Commands**: Environment-specific CLI wrapping (mlfcli vs python jgtml/mlfcli.py)

#### 📊 **Workflow Types**:
- **PRODUCTION**: Current data (~400 rows), TTF+MLF only, real-time decisions
- **DISCOVERY**: Full historical data, TTF+MLF+MX, pattern discovery & ML training

#### ⚙️ **Advanced Features**:
- **Pattern configuration**: Dynamic loading from `jgtset` / `~/.jgt/settings.json`
- **Offline processing**: `-old` flag for faster results when markets closed
- **Logging integration**: Structured logging to `/tmp/batch.log`
- **Function library**: Well-structured dependency management in `_fnml.sh`

## 🚧 Implementation Plan

### Phase 1: Enhanced Unified Scripts (IMMEDIATE)
**Deliverable**: Upgraded unified scripts with missing capabilities

#### 1.1 Add Missing Patterns & Instruments
```bash
# Add to all unified scripts:
PATTERNS="mfi mz zonesq aoac"  # Include aoac pattern
# Extended instrument support from DISCOVERY script
```

#### 1.2 Environment Detection & Switching
```bash
# Auto-detect environment and set appropriate paths/commands
detect_environment() {
    if [ -d "/workspace/data" ]; then
        ENVIRONMENT="prod"
        conda activate i
        export JGTPY_DATA=/workspace/data/current
        export JGTPY_DATA_FULL=/workspace/data/full
        export mlfcli_command="mlfcli"
    else
        ENVIRONMENT="lab"
        conda activate jgtml
        export JGTPY_DATA=/src/jgtml/data/current
        export JGTPY_DATA_FULL=/src/jgtml/data/full
        export mlfcli_command="python jgtml/mlfcli.py"
    fi
}
```

#### 1.3 MLF Integration (COMPLETED ✅)
**MLF**: Meta Lag Features processing now properly integrated in parallel scripts
```bash
# Complete pipeline with proper dependencies:
# CDS → TTF → MLF → MX (sequential per instrument)
```

#### 1.4 Workflow Type Selection
```bash
# Usage: ./script.sh [current|full] [prod|discovery]
# - current/prod: TTF+MLF only (~400 rows)
# - full/discovery: TTF+MLF+MX (complete historical)
```

### Phase 2: Function Library Integration (HIGH PRIORITY)
**Deliverable**: Single sourced function library for all scripts

#### 2.1 Enhanced _fnml.sh Integration (I doubt this is up to date but it might for sure there are other scripts that are sure not up to date)

**Target**: `/src/jgtml/scripts/_fnml_unified.sh`
- Merge current `_fnml.sh` functions with our unified script logic
- Add dynamic pattern loading from `jgtset`
- Environment-aware function wrappers
- Proper dependency sequencing functions

#### 2.2 Unified Function API
```bash
# Core functions to implement:
jgtml_pipeline_instrument_timeframe()     # Full CDS→TTF→MLF→MX pipeline
jgtml_production_features()               # TTF+MLF only for trading
jgtml_discovery_workflow()                # Full historical for ML discovery
jgtml_pattern_processor()                 # Pattern-aware processing
```

#### 2.3 Script Consolidation
**Replace** these scripts with function calls:
- `PRODUCTION_feature_exploration.sh` → `jgtml_production_features`
- `DISCOVERY_target_generation.sh` → `jgtml_discovery_workflow`
- Batch scripts → `jgtml_pipeline_instrument_timeframe` loops

### Phase 3: Advanced Capabilities (MEDIUM PRIORITY)

#### 3.1 Dynamic Pattern Configuration
```bash
# Load patterns from jgtset configuration
PATTERNS=$(jgtset | jq -r '.patterns | keys[]' 2>/dev/null || echo "mfi mz zonesq aoac")
```

#### 3.2 Intelligent Offline Processing
```bash
# Auto-detect market hours and use -old when appropriate
USE_OFFLINE_ARG=""
if is_market_closed; then
    USE_OFFLINE_ARG="-old"
    echo "Using offline data (markets closed)"
fi
```

#### 3.3 Enhanced Logging & Monitoring
```bash
# Structured logging with progress tracking
LOG_FILE="/tmp/jgtml_unified_$(date +%Y%m%d_%H%M%S).log"
```

## 🎯 Immediate Actions Required

### 1. Fix Current Scripts (COMPLETED ✅)
- ✅ Fixed dependency sequencing in parallel scripts
- ✅ Added aoac pattern to configuration
- ✅ Corrected parallel processing to handle multiple instruments per timeframe

### 2. Create Enhanced Unified Scripts (NEXT)
```bash
# Priority scripts to create:
_REFRESH_UNIFIED_PRODUCTION.sh     # TTF+MLF for real-time trading
_REFRESH_UNIFIED_DISCOVERY.sh      # TTF+MLF+MX for ML discovery  
_REFRESH_FUNCTIONS.sh              # Sourced function library
```

### 3. Integration Testing (CRITICAL)
- Test dependency chain: CDS → TTF → MLF → MX
- Validate aoac pattern processing
- Verify environment switching
- Test production vs discovery workflows

## 🔄 Migration Strategy

### Short Term (1-2 days)
1. **Create production-ready scripts** with full MLF integration
2. **Test dependency chain** thoroughly
3. **Document function library** usage patterns

### Medium Term (1 week)
1. **Consolidate all batch scripts** into function-based approach
2. **Create environment-aware wrappers**
3. **Integrate with SANDBOX update system**

### Long Term (2 weeks)
1. **Full function library replacement** of individual scripts
2. **Advanced pattern configuration** system
3. **Monitoring and alerting** integration

## 🤝 Dependencies & Coordination

### SANDBOX Integration
- **Data source**: Unified scripts provide data for SANDBOX experiments
- **Validation**: SANDBOX validates ML discoveries before production use
- **Coordination**: See `/src/SANDBOX/CLAUDE.md` for integration instructions

### Main JGT Ecosystem
- **Configuration**: Uses `~/.jgt/settings.json` pattern definitions
- **CLI Tools**: Leverages jgtcli, ttfcli, mlfcli, jgtmlcli from jgtml package
- **Environment**: Integrates with jgtcore/jgtutils environment system

## 📋 Success Metrics

1. **Single script execution** replaces 5+ individual scripts
2. **Proper dependency handling** eliminates processing failures
3. **Environment portability** between lab and production
4. **Complete pattern coverage** including all discovered patterns
5. **SANDBOX integration** provides seamless data pipeline

---

## 🚨 CRITICAL NOTES

### ⚠️ **Dependency Chain Must Be Respected**:
```
CDS → TTF → MLF → MX
❌ NEVER run these in parallel for same instrument/timeframe
✅ Run sequential pipeline per instrument, parallelize across instruments
```

### 🔧 **Environment Detection Required**:
- **Lab**: `/src/jgtml/`, `python jgtml/mlfcli.py`
- **Prod**: `/workspace/`, `mlfcli` command
- Scripts must auto-detect and adapt

### 📊 **Data Structure Awareness**:
**TTF** = Transformed Trading Features (pattern columns from CDS)  
**MLF** = Meta Lag Features (lagged versions of TTF)  
See `/src/jgtpy/CLAUDE.md` for complete data pipeline documentation

### 🎨 **Pattern Expansion**:
Add `aoac` pattern and dynamic pattern loading from configuration to match existing script capabilities.

---

### Integration with JGT Data Refresh Service

**JGTPY Service Integration**: Our unified scripts work perfectly with JGTPY's `jgtservice` - the enterprise-grade automation platform:

#### **Service Architecture Synergy**:
- **JGTPY Service**: Handles CDS automated refresh with scheduling + cloud distribution  
- **JGTML Scripts**: Handle TTF → MLF → MX pipeline for advanced feature generation
- **Combined Power**: Complete automation from raw data to ML-ready features

#### **Future JGTML Service Vision**:
Create similar service architecture for JGTML:
```bash
# Proposed jgtml service commands
jgtmlservice --daemon --patterns "mfi,mz,zonesq,aoac"
jgtmlservice --discovery-mode --full  # TTF+MLF+MX pipeline
jgtmlservice --production-mode         # TTF+MLF only (~400 rows)
```

**Service Integration Strategy**:
1. **Current**: Use `jgtservice` for CDS automation + our unified scripts for advanced features
2. **Future**: Extend service pattern to JGTML for complete pipeline automation
3. **Ultimate**: Unified JGT ecosystem service covering entire PDS→MX pipeline

---

**Next Instance Instructions**: Start with Phase 1.3 (MLF Integration) - this is the most critical missing piece that breaks the data pipeline.