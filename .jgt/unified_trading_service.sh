#!/bin/bash

# 🚀 Unified JGT Trading Service - Proper Implementation
# Uses REAL FDB scanner, proper cache system, and integrated components

set -e

# Configuration
JGTML_DIR="/src/jgtml"
JGTAGENTIC_DIR="/src/jgtagentic"
JGT_CACHE_DIR="${JGT_CACHE:-$HOME/.cache/jgt}"
TIMEFRAME="${1:-m5}"
LOG_DIR="$JGTML_DIR/logs"
LOG_FILE="$LOG_DIR/unified_trading_$(date +%Y%m%d_%H%M%S).log"

# Ensure directories exist
mkdir -p "$LOG_DIR"
mkdir -p "$JGT_CACHE_DIR"

# Export cache directory
export JGT_CACHE="$JGT_CACHE_DIR"

log_msg() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$TIMEFRAME] $1" | tee -a "$LOG_FILE"
}

check_environment() {
    log_msg "🔍 Environment Check"
    
    # Check if we're in jgtml environment
    if ! conda list | grep -q jgtml 2>/dev/null; then
        log_msg "⚠️ Not in jgtml conda environment - activating..."
        eval "$(conda shell.bash hook)"
        conda activate jgtml
    fi
    
    # Check cache directory
    if [ ! -w "$JGT_CACHE_DIR" ]; then
        log_msg "❌ Cache directory not writable: $JGT_CACHE_DIR"
        exit 1
    fi
    
    log_msg "✅ Environment ready - Cache: $JGT_CACHE_DIR"
}

run_unified_system() {
    log_msg "🚀 Starting Unified Trading System"
    
    cd "$JGTML_DIR"
    
    # Use the proper unified trading system
    python -m jgtml.unified_trading_system \
        --instruments "EUR/USD" "GBP/USD" "XAU/USD" \
        --timeframes "$TIMEFRAME" \
        --cache-dir "$JGT_CACHE_DIR" \
        --demo \
        --quality-threshold 7.0
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_msg "✅ Unified trading system completed successfully"
    else
        log_msg "❌ Unified trading system failed with code: $exit_code"
    fi
    
    return $exit_code
}

run_real_fdb_scanner() {
    log_msg "🔍 Running REAL FDB Scanner"
    
    cd "$JGTML_DIR"
    
    # Set instruments and timeframes for FDB scanner
    export INSTRUMENTS="EUR/USD,GBP/USD,XAU/USD"
    export TIMEFRAMES="$TIMEFRAME"
    
    # Run the REAL fdb_scanner_2408.py
    python -m jgtml.fdb_scanner_2408 \
        --verbose 2 \
        --demo
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_msg "✅ FDB Scanner completed successfully"
        
        # Check what was generated
        log_msg "📁 Generated cache files:"
        find "$JGT_CACHE_DIR" -name "*_cds_cache.csv" -mmin -10 -exec ls -la {} \;
        
        log_msg "📊 Generated signal files:"
        find "$JGTML_DIR" -name "fdb_signals_out__*.json" -mmin -10 -exec ls -la {} \;
        
    else
        log_msg "❌ FDB Scanner failed with code: $exit_code"
    fi
    
    return $exit_code
}

integrate_with_jgtagentic() {
    log_msg "🔮 Checking JGTagentic Integration"
    
    if [ -d "$JGTAGENTIC_DIR" ]; then
        log_msg "✅ JGTagentic available - running enhanced analysis"
        
        cd "$JGTAGENTIC_DIR"
        
        # Run enhanced FDB scanner if available
        if [ -f "jgtagentic/fdbscan_agent.py" ]; then
            python -m jgtagentic.fdbscan_agent scan \
                --timeframe "$TIMEFRAME" \
                --real \
                --with-intent
                
            log_msg "✅ Enhanced FDB analysis completed"
        fi
        
        # Run observation-based analysis
        python -m jgtagentic.jgtagenticcli observe \
            "Market analysis for $TIMEFRAME timeframe showing potential trading opportunities" \
            --scan
            
        log_msg "✅ Observation-based analysis completed"
        
    else
        log_msg "⚠️ JGTagentic not available - using basic FDB scanner only"
    fi
}

show_results() {
    log_msg "📊 Trading Session Results"
    echo "=" >> "$LOG_FILE"
    
    # Show cache status
    log_msg "📁 Cache Status:"
    for instrument in "EUR-USD" "GBP-USD" "XAU-USD"; do
        for tf in "H4" "H1" "m15"; do
            cache_file="$JGT_CACHE_DIR/fdb_scanners/${instrument}_${tf}_cds_cache.csv"
            if [ -f "$cache_file" ]; then
                size=$(stat -c%s "$cache_file")
                log_msg "  ✅ $instrument $tf: $size bytes"
            else
                log_msg "  ❌ $instrument $tf: missing"
            fi
        done
    done
    
    # Show signal files
    log_msg "📈 Signal Files:"
    find "$JGTML_DIR" -name "fdb_signals_out__*.json" -mmin -30 -exec echo "  📄 {}" \;
    
    # Show script files
    log_msg "📜 Generated Scripts:"
    find "$JGTML_DIR/rjgt" -name "*.sh" -mmin -30 -exec echo "  🔧 {}" \;
    
    log_msg "📋 Session log: $LOG_FILE"
}

cleanup_background_processes() {
    # Stop any running background traders
    pkill -f "jgt_background_trader" 2>/dev/null || true
    pkill -f "unified_trading" 2>/dev/null || true
    log_msg "🧹 Background processes cleaned up"
}

main() {
    log_msg "🚀 Unified JGT Trading Service Starting"
    log_msg "   Timeframe: $TIMEFRAME"
    log_msg "   Cache Dir: $JGT_CACHE_DIR"
    log_msg "   Log File: $LOG_FILE"
    
    # Cleanup any previous processes
    cleanup_background_processes
    
    # Check environment
    check_environment
    
    # Run unified system (primary method)
    if run_unified_system; then
        log_msg "✅ Unified system successful"
    else
        log_msg "⚠️ Unified system failed - falling back to real FDB scanner"
        run_real_fdb_scanner
    fi
    
    # Integrate with jgtagentic if available
    integrate_with_jgtagentic
    
    # Show results
    show_results
    
    log_msg "🎯 Unified JGT Trading Service Completed"
}

# Handle script termination
trap cleanup_background_processes EXIT

# Run main function
main "$@" 
