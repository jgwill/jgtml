#!/bin/bash
# 🧠 JGT Discovery Workflow - ML Pattern Research & Training Data Generation
# TTF+MLF+MX full historical pipeline for machine learning discovery
# Generates complete feature sets and training targets

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_refresh_functions.sh"

# ============================================================================
# CONFIGURATION
# ============================================================================

detect_environment
load_jgt_config

# Discovery-optimized defaults
INSTRUMENTS="${INSTRUMENTS:-EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD SPX500}"
TIMEFRAMES="${TIMEFRAMES:-D1 H4}"
PATTERNS="${PATTERNS:-mfi mz zonesq aoac}"
MAX_PARALLEL_JOBS="${MAX_PARALLEL_JOBS:-4}"

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

show_help() {
    cat <<EOF
🧠 JGT Discovery Workflow - ML Research & Training Data

USAGE:
    $0 [OPTIONS]

DESCRIPTION:
    Generates complete historical data pipelines for ML model development.
    Creates TTF (features) → MLF (lagged features) → MX (training targets).

OPTIONS:
    --instruments LIST     Instruments to process
                          (default: EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD SPX500)

    --timeframes LIST      Timeframes for full history
                          (default: D1 H4)

    --patterns LIST        Feature patterns
                          (default: mfi mz zonesq aoac)

    --max-jobs N          Parallel jobs (default: $MAX_PARALLEL_JOBS)

    --cleanup DAYS        Remove data older than N days

    --verbose             Enable debug output

    -h, --help           Show this help message

EXAMPLES:
    # Full discovery workflow (all instruments)
    $0

    # Specific pair with extended patterns
    $0 --instruments "EUR/USD" --patterns "mfi mz zonesq aoac"

    # Multiple pairs, fewer parallel jobs
    $0 --instruments "EUR/USD,XAU/USD,SPX500" --max-jobs 2

    # Generate then cleanup
    $0 --cleanup 14

WORKFLOW STAGES:
    Stage 1: CDS Generation
             └─ Market data + technical indicators (foundation)

    Stage 2: TTF Generation (Cross-timeframe Features)
             └─ Base columns: instrument/timeframe
             └─ Enhanced: higher timeframe versions

    Stage 3: MLF Generation (Meta Lag Features)
             └─ Depends on: TTF success
             └─ Creates: Temporal lag features

    Stage 4: MX Generation (ML Training Targets)
             └─ Depends on: MLF success
             └─ Outputs: Training labels & targets

PATTERN DETAILS:
    mfi (Money Flow Index):
       • mfi_sq, mfi_green, mfi_fade, mfi_fake
       • Identifies accumulation/distribution zones

    mz (Mouth Zone):
       • mfi_str, zcol
       • Alligator mouth position analysis

    zonesq (Zone Squeeze):
       • zone_sig, mfi_sq
       • High volatility contraction patterns

    aoac (Awesome Oscillator + Accelerator):
       • ao, ac
       • Momentum and acceleration indicators

DATA OUTPUT:
    TTF:  $JGTPY_DATA_FULL/ttf/
    MLF:  $JGTPY_DATA_FULL/mlf/
    MX:   $JGTPY_DATA_FULL/targets/mx/

PROCESSING TIME:
    • Single instrument: ~5-10 minutes
    • Multiple instruments: 20-60 minutes (parallelized)
    • Full dataset: Can take several hours

EOF
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    parse_args "$@"

    init_logging "jgtml_discovery"

    log_msg "info" "╔═══════════════════════════════════════════════════════╗"
    log_msg "info" "║  JGT DISCOVERY WORKFLOW - ML RESEARCH & TRAINING     ║"
    log_msg "info" "╚═══════════════════════════════════════════════════════╝"
    echo ""

    log_msg "info" "Mode: DISCOVERY (Full history + ML targets)"
    log_msg "info" "Environment: $ENVIRONMENT"
    log_msg "info" "Data paths: $JGTPY_DATA_FULL (full history)"
    log_msg "info" "Instruments: $(echo $INSTRUMENTS | wc -w) instruments"
    log_msg "info" "Timeframes: $(echo $TIMEFRAMES | wc -w) timeframes"
    log_msg "info" "Patterns: $(echo $PATTERNS | wc -w) patterns"
    log_msg "info" "Parallel jobs: $MAX_PARALLEL_JOBS"
    echo ""

    if is_market_closed; then
        log_msg "warn" "Markets closed - using offline mode"
    else
        log_msg "info" "Markets open - fetching fresh data"
    fi
    echo ""

    log_msg "info" "⏳ Processing pipeline stages..."
    echo ""

    # Execute discovery workflow with MX targets
    local start_time=$(date +%s)

    discovery_workflow "$INSTRUMENTS" "$TIMEFRAMES" "$PATTERNS"

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    echo ""
    log_msg "success" "╔═══════════════════════════════════════════════════════╗"
    log_msg "success" "║     DISCOVERY WORKFLOW COMPLETED                      ║"
    log_msg "success" "╚═══════════════════════════════════════════════════════╝"
    log_msg "info" "Total duration: ${duration}s"
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
    log_msg "success" "✓ ML training data ready"
    log_msg "success" "✓ TTF features generated"
    log_msg "success" "✓ MLF lag features created"
    log_msg "success" "✓ MX training targets available"
    log_msg "info" "Log: $LOG_FILE"
    echo ""

    log_msg "info" "Next steps:"
    log_msg "info" "  1. Review features: ls -la \$JGTPY_DATA_FULL/{ttf,mlf}/"
    log_msg "info" "  2. Validate targets: ls -la \$JGTPY_DATA_FULL/targets/mx/"
    log_msg "info" "  3. Train ML models with discovered patterns"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
