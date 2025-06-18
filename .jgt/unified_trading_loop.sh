#!/bin/bash
# 🚀 JGT UNIFIED TRADING SYSTEM - Master Integration Loop
# This script orchestrates the complete JGT trading stack
# Author: JGT Trading System Integration
# Version: 1.0 - Complete Stack Integration

set -e  # Exit on any error

TIMEFRAME=${1:-"H4"}
INSTRUMENTS=${2:-"EUR-USD,GBP-USD,XAU-USD"}
QUALITY_THRESHOLD=${3:-"8.0"}
MODE=${4:-"--demo"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Main trading loop logic
main() {
    log "🚀 JGT Unified Trading System Starting..."
    log "📊 Timeframe: $TIMEFRAME | Instruments: $INSTRUMENTS | Quality: $QUALITY_THRESHOLD"
    
    case $TIMEFRAME in
        "H4"|"H1"|"D1")
            log "📈 PRIMARY MARKET ANALYSIS MODE"
            
            # Step 1: Run comprehensive FDB analysis
            log "🔍 Running Enhanced Trading CLI Analysis..."
            if enhancedtradingcli auto -i "$INSTRUMENTS" $MODE --quality-threshold "$QUALITY_THRESHOLD"; then
                success "Enhanced trading analysis completed"
            else
                error "Enhanced trading analysis failed"
                exit 1
            fi
            
            # Step 2: Generate analysis charts for visual confirmation
            log "📊 Generating Analysis Charts..."
            IFS=',' read -ra INSTRUMENT_ARRAY <<< "$INSTRUMENTS"
            for instrument in "${INSTRUMENT_ARRAY[@]}"; do
                instrument=$(echo "$instrument" | xargs) # Trim whitespace
                log "📈 Generating chart for $instrument $TIMEFRAME"
                
                if jgtads -i "$instrument" -t "$TIMEFRAME" --save_figure "charts/" --save_figure_as_timeframe; then
                    success "Chart generated for $instrument $TIMEFRAME"
                else
                    warning "Chart generation failed for $instrument $TIMEFRAME"
                fi
            done
            ;;
            
        "m15"|"m5")
            log "🎯 TRADE MANAGEMENT MODE"
            
            # Step 1: Update Alligator trailing stops for all active trades
            log "🐊 Updating Alligator Trailing Stops..."
            
            # Get list of active trades (demo mode)
            if jgtapp fxtr $MODE > /dev/null 2>&1; then
                success "Trade data refreshed"
                
                # Update trailing stops with FDB signals + Alligator fallback
                log "🔄 Updating FDB-based trailing stops with Alligator fallback..."
                if jgtapp fxmvstopfdb -t "$TIMEFRAME" --lips $MODE; then
                    success "FDB trailing stops updated"
                else
                    warning "FDB trailing stops update failed, continuing..."
                fi
            else
                warning "No active trades found or trade data unavailable"
            fi
            
            # Step 2: Quick chart updates for monitoring
            if [[ "$TIMEFRAME" == "m5" ]]; then
                log "📈 Quick monitoring chart update..."
                if jgtads -i "EUR-USD" -t "m5" --save_figure "charts/" -tf; then
                    success "Monitoring chart updated"
                else
                    warning "Monitoring chart update failed"
                fi
            fi
            ;;
            
        "m1")
            log "⚡ RAPID MONITORING MODE"
            
            # Ultra-quick status check
            log "⚡ Rapid trade status check..."
            if jgtapp fxtr $MODE --nosave; then
                success "Trade status checked"
            else
                warning "Trade status check failed"
            fi
            ;;
            
        *)
            error "Unsupported timeframe: $TIMEFRAME"
            echo "Supported timeframes: H4, H1, D1, m15, m5, m1"
            exit 1
            ;;
    esac
    
    success "🎯 JGT Trading Loop: $TIMEFRAME analysis complete"
    log "📊 System ready for next timeframe cycle"
}

# Error handling
trap 'error "Script interrupted"; exit 1' INT TERM

# Execute main function
main "$@" 