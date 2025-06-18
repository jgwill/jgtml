#!/bin/bash
# Auto-generated trader script

TIMEFRAME="$1"
LOG_FILE=".jgt/logs/trader_${TIMEFRAME}.log"
PID_FILE=".jgt/pids/trader_${TIMEFRAME}.pid"

echo $$ > "$PID_FILE"

log_msg() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$TIMEFRAME] $1" | tee -a "$LOG_FILE"
}

log_msg "🚀 Starting $TIMEFRAME trader (PID: $$)"

while true; do
    log_msg "🔍 Running analysis for $TIMEFRAME..."
    
    python jgtml/simple_trading_orchestrator.py \
        --timeframe "$TIMEFRAME" \
        --instruments "EUR-USD,GBP-USD,XAU-USD" \
        --demo \
        --quality-threshold 8.0
    
    log_msg "✅ $TIMEFRAME analysis cycle completed"
    
    # Wait based on timeframe
    case "$TIMEFRAME" in
        "m5") sleep 300 ;;   # 5 minutes
        "m15") sleep 900 ;;  # 15 minutes  
        "H1") sleep 3600 ;;  # 1 hour
        *) sleep 600 ;;      # 10 minutes default
    esac
done
