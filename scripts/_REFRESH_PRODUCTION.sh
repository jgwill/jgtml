#!/bin/bash
# 🧠 JGT Production Workflow - Real-time Trading Data Refresh
# TTF+MLF pipeline for immediate trading decisions (~400 most recent bars)
# Uses unified function library for environment detection, error handling, monitoring

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_refresh_functions.sh"

# ============================================================================
# CONFIGURATION
# ============================================================================

# Auto-configure based on environment
detect_environment
load_jgt_config

# Default configuration
INSTRUMENTS="${INSTRUMENTS:-EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD SPX500}"
TIMEFRAMES="${TIMEFRAMES:-D1 H4 H1}"
PATTERNS="${PATTERNS:-mfi mz zonesq aoac}"
MAX_PARALLEL_JOBS="${MAX_PARALLEL_JOBS:-4}"
WORKFLOW_MODE="${WORKFLOW_MODE:-production}"

# Parse command-line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --instruments)
                INSTRUMENTS="$2"
                shift 2
                ;;
            --timeframes)
                TIMEFRAMES="$2"
                shift 2
                ;;
            --patterns)
                PATTERNS="$2"
                shift 2
                ;;
            --max-jobs)
                MAX_PARALLEL_JOBS="$2"
                shift 2
                ;;
            --cleanup)
                CLEANUP_DAYS="$2"
                shift 2
                ;;
            --verbose)
                set -x
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_msg "warn" "Unknown option: $1"
                shift
                ;;
        esac
    done
}

# Help documentation
show_help() {
    cat <<EOF
🧠 JGT Production Workflow - Real-time Trading Data Refresh

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --instruments LIST      Comma/space-separated instruments
                           (default: $INSTRUMENTS)

    --timeframes LIST      Comma/space-separated timeframes
                          (default: $TIMEFRAMES)

    --patterns LIST        Comma/space-separated patterns
                          (default: $PATTERNS)

    --max-jobs N           Max parallel jobs (default: $MAX_PARALLEL_JOBS)

    --cleanup DAYS         Cleanup data older than N days

    --verbose              Enable verbose output

    -h, --help            Show this help message

EXAMPLES:
    # Default production refresh
    $0

    # Specific instruments and timeframes
    $0 --instruments "EUR/USD,XAU/USD" --timeframes "D1,H4"

    # With extended TTF/MLF patterns
    $0 --patterns "mfi mz zonesq aoac"

    # Cleanup and refresh
    $0 --cleanup 7

WORKFLOW:
    1. Detects lab/prod environment
    2. Loads configuration from ~/.jgt/settings.json
    3. Refreshes CDS data (market data + indicators)
    4. Generates TTF (cross-timeframe features)
    5. Generates MLF (lagged features)
    6. Reports data statistics
    7. Ready for real-time trading decisions

MODES:
    • Production: TTF+MLF only (~400 bars, fast)
    • Discovery: TTF+MLF+MX (full history, includes ML targets)

DATA LOCATIONS:
    Lab:  /src/jgtml/data/
    Prod: /workspace/data/

PATTERNS:
    • mfi:    Money Flow Index signals
    • mz:     Alligator mouth zones
    • zonesq: Zone squeezes
    • aoac:   Awesome Oscillator + Accelerator

EOF
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    parse_args "$@"

    # Initialize logging
    init_logging "jgtml_production"

    # Report configuration
    log_msg "info" "╔════════════════════════════════════════════════╗"
    log_msg "info" "║  JGT PRODUCTION WORKFLOW - REAL-TIME TRADING  ║"
    log_msg "info" "╚════════════════════════════════════════════════╝"
    echo ""

    log_msg "info" "Environment: $ENVIRONMENT"
    log_msg "info" "Data paths: $JGTPY_DATA (current) / $JGTPY_DATA_FULL (full)"
    log_msg "info" "Instruments: $(echo $INSTRUMENTS | wc -w) instruments"
    log_msg "info" "Timeframes: $(echo $TIMEFRAMES | wc -w) timeframes"
    log_msg "info" "Patterns: $(echo $PATTERNS | wc -w) patterns"
    log_msg "info" "Parallel jobs: $MAX_PARALLEL_JOBS"
    echo ""

    # Check market status
    if is_market_closed; then
        log_msg "warn" "Markets currently CLOSED - using offline mode (-old flag)"
    else
        log_msg "info" "Markets OPEN - fetching fresh data"
    fi
    echo ""

    # Execute production workflow
    local start_time=$(date +%s)

    production_workflow "$INSTRUMENTS" "$TIMEFRAMES" "$PATTERNS"

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    echo ""
    log_msg "success" "╔════════════════════════════════════════════════╗"
    log_msg "success" "║     PRODUCTION WORKFLOW COMPLETED              ║"
    log_msg "success" "╚════════════════════════════════════════════════╝"
    log_msg "info" "Duration: ${duration}s"
    echo ""

    # Show data statistics
    show_data_stats

    # Optional cleanup
    if [ -n "$CLEANUP_DAYS" ]; then
        echo ""
        cleanup_stale_data "$CLEANUP_DAYS"
    fi

    # Final report
    echo ""
    log_msg "success" "✓ Data ready for real-time trading"
    log_msg "info" "Log file: $LOG_FILE"
}

# Execute if sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
