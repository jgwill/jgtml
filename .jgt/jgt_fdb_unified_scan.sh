#!/bin/bash
# JGT Unified FDB Scanner - Enhanced version of fdbscan.sh
# This script integrates with the trading orchestrator and jgtcore timeframe library
# Usage: Called by timeframe scheduler (wtf/tfw) or trading orchestrator

# Load environment (compatible with user's pattern)
if [ -f "/opt/binscripts/load.sh" ]; then
    . /opt/binscripts/load.sh
fi

# Load local environment if exists
if [ -f "$(pwd)/.jgt/load.sh" ]; then
    . "$(pwd)/.jgt/load.sh"
fi

# Logging setup (compatible with user's pattern)
LOG_FILE=${LOG_FILE:-"/var/log/jgt/jgt_unified_fdb_scan.log"}
LOG_ENABLED=${LOG_ENABLED:-"y"}

# Parameters
TIMEFRAME=${1:-"H4"}
CURRENT_TIME=${2:-$(date '+%H:%M')}
MODE=${3:-"--demo"}
INSTRUMENTS=${4:-"EUR-USD,GBP-USD,XAU-USD"}
QUALITY_THRESHOLD=${5:-"8.0"}

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    if [ "$LOG_ENABLED" = "y" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1" | tee -a "$LOG_FILE"
    else
        echo -e "${GREEN}[INFO]${NC} $1"
    fi
}

log_error() {
    if [ "$LOG_ENABLED" = "y" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1" | tee -a "$LOG_FILE"
    else
        echo -e "${RED}[ERROR]${NC} $1"
    fi
}

log_warn() {
    if [ "$LOG_ENABLED" = "y" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') [WARN] $1" | tee -a "$LOG_FILE"
    else
        echo -e "${YELLOW}[WARN]${NC} $1"
    fi
}

main() {
    log_info "🚀 JGT Unified FDB Scan started for $TIMEFRAME at $CURRENT_TIME"
    log_info "📊 Instruments: $INSTRUMENTS | Quality: $QUALITY_THRESHOLD | Mode: $MODE"
    
    # Check if we're in jgtml directory
    if [ ! -f "pyproject.toml" ] || ! grep -q "jgtml" pyproject.toml 2>/dev/null; then
        log_error "❌ Not in jgtml directory. Please run from jgtml root."
        exit 1
    fi
    
    # Activate conda environment if available
    if command -v conda &> /dev/null; then
        log_info "🐍 Activating jgtml conda environment..."
        eval "$(conda shell.bash hook)"
        conda activate jgtml 2>/dev/null || log_warn "⚠️  Could not activate jgtml environment"
    fi
    
    # Method 1: Try enhanced trading CLI (preferred - new unified approach)
    log_info "🔍 Running Enhanced Trading CLI Analysis..."
    if enhancedtradingcli auto -i "$INSTRUMENTS" $MODE --quality-threshold "$QUALITY_THRESHOLD"; then
        log_info "✅ Enhanced Trading CLI completed successfully"
        
        # Generate analysis charts
        log_info "📊 Generating analysis charts..."
        IFS=',' read -ra INSTRUMENT_ARRAY <<< "$INSTRUMENTS"
        for instrument in "${INSTRUMENT_ARRAY[@]}"; do
            instrument=$(echo "$instrument" | xargs) # Trim whitespace
            log_info "📈 Generating chart for $instrument $TIMEFRAME"
            
            if jgtads -i "$instrument" -t "$TIMEFRAME" --save_figure "charts/" --save_figure_as_timeframe; then
                log_info "✅ Chart generated for $instrument"
            else
                log_warn "⚠️  Chart generation failed for $instrument"
            fi
        done
        
        # Update trade management if lower timeframes
        if [[ "$TIMEFRAME" == "m15" || "$TIMEFRAME" == "m5" ]]; then
            log_info "🎯 Updating trade management for $TIMEFRAME"
            
            # Update trailing stops
            log_info "🐊 Updating Alligator trailing stops..."
            if jgtapp fxtr $MODE > /dev/null 2>&1; then
                log_info "✅ Trade data refreshed"
                
                if jgtapp fxmvstopfdb -t "$TIMEFRAME" --lips $MODE; then
                    log_info "✅ FDB trailing stops updated"
                else
                    log_warn "⚠️  FDB trailing stops update failed"
                fi
            else
                log_warn "⚠️  No active trades found"
            fi
        fi
        
        exit 0
    else
        log_error "❌ Enhanced Trading CLI failed, falling back to legacy FDB scan"
    fi
    
    # Method 2: Fallback to legacy FDB scan (compatible with user's existing pattern)
    log_info "🔄 Falling back to legacy FDB scan..."
    if command -v fdbscan &> /dev/null; then
        if fdbscan -t "$TIMEFRAME" -v 2; then
            log_info "✅ Legacy FDB Scan completed for $TIMEFRAME"
            exit 0
        else
            log_error "❌ Legacy FDB Scan failed for $TIMEFRAME"
            exit 1
        fi
    else
        log_error "❌ No FDB scan method available"
        exit 1
    fi
}

# Error handling
trap 'log_error "Script interrupted"; exit 1' INT TERM

# Execute main function
main "$@" 