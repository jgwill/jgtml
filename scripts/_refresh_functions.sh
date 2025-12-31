#!/bin/bash
# 🧠 JGT Unified Data Refresh Function Library
# Enhanced infrastructure for CDS → TTF → MLF → MX pipeline
# Provides environment detection, error handling, monitoring, and parallel processing

set -o pipefail

# ============================================================================
# CONFIGURATION & ENVIRONMENT DETECTION
# ============================================================================

# Auto-detect environment (lab/prod)
detect_environment() {
    if [ -d "/workspace/data" ]; then
        export ENVIRONMENT="prod"
        export JGTPY_DATA="/workspace/data/current"
        export JGTPY_DATA_FULL="/workspace/data/full"
        export CONDA_ENV="i"
        echo "🔧 Environment: PRODUCTION (/workspace)"
    else
        export ENVIRONMENT="lab"
        export JGTPY_DATA="${JGTPY_DATA:-/src/jgtml/data/current}"
        export JGTPY_DATA_FULL="${JGTPY_DATA_FULL:-/src/jgtml/data/full}"
        export CONDA_ENV="jgtml"
        echo "🔧 Environment: LAB (/src/jgtml)"
    fi
}

# Load JGT settings and patterns
load_jgt_config() {
    local config_file="${1:-$HOME/.jgt/settings.json}"

    if [ -f "$config_file" ]; then
        export PATTERNS=$(jq -r '.patterns | keys[]' "$config_file" 2>/dev/null || echo "mfi mz zonesq aoac")
        echo "📋 Patterns loaded: $PATTERNS"
    else
        export PATTERNS="${PATTERNS:-mfi mz zonesq aoac}"
        echo "⚠️ No config found, using default patterns: $PATTERNS"
    fi
}

# Detect if markets are currently closed
is_market_closed() {
    local hour=$(date +%H)
    local day=$(date +%u)

    # Markets closed: 22:00 Friday - 17:00 Sunday (rough estimate, adjust as needed)
    if [ "$day" -eq 5 ] && [ "$hour" -ge 22 ]; then
        return 0
    elif [ "$day" -eq 6 ]; then
        return 0
    elif [ "$day" -eq 7 ] && [ "$hour" -lt 17 ]; then
        return 0
    fi
    return 1
}

# ============================================================================
# LOGGING & MONITORING
# ============================================================================

# Initialize logging
init_logging() {
    local script_name="${1:-jgtml_refresh}"
    export LOG_DIR="${LOG_DIR:-/tmp/jgtml_logs}"
    export LOG_FILE="$LOG_DIR/${script_name}_$(date +%Y%m%d_%H%M%S).log"
    mkdir -p "$LOG_DIR"

    # Log header
    {
        echo "🧠 JGT Data Refresh Log"
        echo "========================"
        echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Environment: $ENVIRONMENT"
        echo "Data paths: $JGTPY_DATA / $JGTPY_DATA_FULL"
        echo ""
    } | tee "$LOG_FILE"
}

# Log messages with timestamp and level
log_msg() {
    local level="$1"
    shift
    local msg="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local emoji=""

    case "$level" in
        info)   emoji="ℹ️" ;;
        success) emoji="✓" ;;
        warn)   emoji="⚠️" ;;
        error)  emoji="✗" ;;
        *)      emoji="•" ;;
    esac

    echo "[$timestamp] $emoji $msg" | tee -a "$LOG_FILE"
}

# Progress tracker for operations
track_progress() {
    local current="$1"
    local total="$2"
    local operation="$3"
    local percent=$((current * 100 / total))
    log_msg "info" "[$operation] Progress: $current/$total ($percent%)"
}

# ============================================================================
# DATA PIPELINE FUNCTIONS
# ============================================================================

# Validate instrument/timeframe pair
validate_instrument_timeframe() {
    local instrument="$1"
    local timeframe="$2"

    if [ -z "$instrument" ] || [ -z "$timeframe" ]; then
        log_msg "error" "Invalid instrument or timeframe"
        return 1
    fi
    return 0
}

# Generate CDS data (foundation of pipeline)
generate_cds() {
    local instrument="$1"
    local timeframe="$2"
    local mode="${3:-current}"  # current or full

    validate_instrument_timeframe "$instrument" "$timeframe" || return 1

    local flags="--fresh"
    [ "$mode" = "full" ] && flags="$flags --full"

    if is_market_closed; then
        flags="$flags -old"
    fi

    if jgtcli -i "$instrument" -t "$timeframe" $flags &>/dev/null; then
        log_msg "success" "CDS: $instrument/$timeframe"
        return 0
    else
        log_msg "error" "CDS failed: $instrument/$timeframe"
        return 1
    fi
}

# Generate TTF (cross-timeframe features)
generate_ttf() {
    local instrument="$1"
    local timeframe="$2"
    local pattern="$3"
    local mode="${4:-current}"

    validate_instrument_timeframe "$instrument" "$timeframe" || return 1

    local flags=""
    [ "$mode" = "full" ] && flags="--full"

    if is_market_closed; then
        flags="$flags -old"
    fi

    if ttfcli -i "$instrument" -t "$timeframe" -pn "$pattern" $flags &>/dev/null; then
        log_msg "success" "TTF: $instrument/$timeframe/$pattern"
        return 0
    else
        log_msg "error" "TTF failed: $instrument/$timeframe/$pattern"
        return 1
    fi
}

# Generate MLF (meta lag features - depends on TTF)
generate_mlf() {
    local instrument="$1"
    local timeframe="$2"
    local pattern="$3"
    local mode="${4:-current}"

    validate_instrument_timeframe "$instrument" "$timeframe" || return 1

    local flags=""
    [ "$mode" = "full" ] && flags="--full"

    if is_market_closed; then
        flags="$flags -old"
    fi

    if mlfcli -i "$instrument" -t "$timeframe" -pn "$pattern" $flags &>/dev/null; then
        log_msg "success" "MLF: $instrument/$timeframe/$pattern"
        return 0
    else
        log_msg "warn" "MLF failed: $instrument/$timeframe/$pattern (non-critical)"
        return 1
    fi
}

# Generate MX (ML targets - depends on MLF)
generate_mx() {
    local instrument="$1"
    local timeframe="$2"
    local pattern="$3"
    local mode="${4:-current}"

    validate_instrument_timeframe "$instrument" "$timeframe" || return 1

    local flags=""
    [ "$mode" = "full" ] && flags="--full"

    if is_market_closed; then
        flags="$flags -old"
    fi

    if jgtmlcli -i "$instrument" -t "$timeframe" -pn "$pattern" $flags &>/dev/null; then
        log_msg "success" "MX: $instrument/$timeframe/$pattern"
        return 0
    else
        log_msg "warn" "MX skipped: $instrument/$timeframe/$pattern"
        return 1
    fi
}

# ============================================================================
# PIPELINE ORCHESTRATION
# ============================================================================

# Sequential pipeline for single instrument/timeframe (RESPECTS DEPENDENCIES)
execute_pipeline_sequence() {
    local instrument="$1"
    local timeframe="$2"
    local patterns="$3"
    local mode="${4:-current}"
    local include_mx="${5:-false}"

    log_msg "info" "Pipeline: $instrument/$timeframe ($mode mode)"

    # Step 1: CDS (foundation)
    if ! generate_cds "$instrument" "$timeframe" "$mode"; then
        log_msg "error" "Pipeline aborted: CDS generation failed"
        return 1
    fi

    # Step 2-4: TTF → MLF → MX (sequential per pattern)
    for pattern in $patterns; do
        # TTF (must succeed)
        if ! generate_ttf "$instrument" "$timeframe" "$pattern" "$mode"; then
            continue
        fi

        # MLF (depends on TTF, non-blocking)
        generate_mlf "$instrument" "$timeframe" "$pattern" "$mode"

        # MX (optional, depends on MLF)
        if [ "$include_mx" = "true" ]; then
            generate_mx "$instrument" "$timeframe" "$pattern" "$mode"
        fi
    done

    return 0
}

# Parallel processing wrapper (parallelizes across instruments, not within)
execute_parallel_instruments() {
    local timeframe="$1"
    local instruments="$2"
    local patterns="$3"
    local mode="${4:-current}"
    local include_mx="${5:-false}"
    local max_jobs="${6:-4}"

    log_msg "info" "Starting parallel processing for timeframe: $timeframe (max $max_jobs jobs)"

    local job_count=0
    for instrument in $instruments; do
        # Respect max concurrent jobs
        while [ $(jobs -r -p | wc -l) -ge $max_jobs ]; do
            sleep 1
        done

        # Launch pipeline in background
        {
            execute_pipeline_sequence "$instrument" "$timeframe" "$patterns" "$mode" "$include_mx"
        } &

        ((job_count++))
    done

    # Wait for all background jobs
    wait
    log_msg "success" "Parallel processing completed for timeframe: $timeframe ($job_count instruments)"
}

# Production workflow (TTF+MLF only for real-time trading)
production_workflow() {
    local instruments="${1:-EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD SPX500}"
    local timeframes="${2:-D1 H4 H1}"
    local patterns="${3:-mfi mz zonesq aoac}"

    log_msg "info" "=== PRODUCTION WORKFLOW (TTF+MLF) ==="
    log_msg "info" "Instruments: $instruments"
    log_msg "info" "Timeframes: $timeframes"
    log_msg "info" "Patterns: $patterns"

    local total=0
    for tf in $timeframes; do
        for i in $instruments; do
            for p in $patterns; do
                ((total++))
            done
        done
    done

    local current=0
    for timeframe in $timeframes; do
        execute_parallel_instruments "$timeframe" "$instruments" "$patterns" "current" false 4
    done

    log_msg "success" "Production workflow completed"
}

# Discovery workflow (TTF+MLF+MX for ML training)
discovery_workflow() {
    local instruments="${1:-EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD SPX500}"
    local timeframes="${2:-D1 H4}"
    local patterns="${3:-mfi mz zonesq aoac}"

    log_msg "info" "=== DISCOVERY WORKFLOW (TTF+MLF+MX) ==="
    log_msg "info" "Instruments: $instruments"
    log_msg "info" "Timeframes: $timeframes"
    log_msg "info" "Patterns: $patterns"

    for timeframe in $timeframes; do
        execute_parallel_instruments "$timeframe" "$instruments" "$patterns" "full" true 4
    done

    log_msg "success" "Discovery workflow completed"
}

# ============================================================================
# DATA MANAGEMENT
# ============================================================================

# Show data statistics
show_data_stats() {
    log_msg "info" "Data Statistics:"

    echo ""
    echo "📊 CDS Data:"
    if [ -d "$JGTPY_DATA/cds" ]; then
        du -sh "$JGTPY_DATA/cds"
        find "$JGTPY_DATA/cds" -name "*.csv" | wc -l | xargs echo "  Files:"
    fi

    echo "📊 TTF Data:"
    if [ -d "$JGTPY_DATA/ttf" ]; then
        du -sh "$JGTPY_DATA/ttf"
        find "$JGTPY_DATA/ttf" -name "*.csv" | wc -l | xargs echo "  Files:"
    fi

    echo "📊 MLF Data:"
    if [ -d "$JGTPY_DATA/mlf" ]; then
        du -sh "$JGTPY_DATA/mlf"
        find "$JGTPY_DATA/mlf" -name "*.csv" | wc -l | xargs echo "  Files:"
    fi
}

# Cleanup old/stale data
cleanup_stale_data() {
    local days_old="${1:-7}"
    log_msg "info" "Cleaning up data older than $days_old days"

    for dir in "$JGTPY_DATA/cds" "$JGTPY_DATA/ttf" "$JGTPY_DATA/mlf"; do
        if [ -d "$dir" ]; then
            find "$dir" -name "*.csv" -mtime +$days_old -delete
        fi
    done

    log_msg "success" "Cleanup completed"
}

# Export for sourcing
export -f detect_environment load_jgt_config is_market_closed
export -f init_logging log_msg track_progress
export -f validate_instrument_timeframe generate_cds generate_ttf generate_mlf generate_mx
export -f execute_pipeline_sequence execute_parallel_instruments
export -f production_workflow discovery_workflow
export -f show_data_stats cleanup_stale_data
