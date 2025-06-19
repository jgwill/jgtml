#!/bin/bash
# Simple JGT Background Trader

# Configuration
JGTML_DIR="/src/jgtml"
TIMEFRAME="${1:-m5}"

# Function to log messages
log_msg() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$TIMEFRAME] $1"
}

# Change to jgtml directory
cd "$JGTML_DIR"

# Activate conda environment
if command -v conda &> /dev/null; then
    eval "$(conda shell.bash hook)"
    conda activate jgtml 2>/dev/null || log_msg "⚠️  Could not activate jgtml environment"
fi

log_msg "🚀 Starting $TIMEFRAME background trader"
log_msg "📍 Working directory: $(pwd)"

# Use unified trading service which handles refresh and analysis
log_msg "🔍 Running unified trading service for $TIMEFRAME..."
"$JGTML_DIR/.jgt/unified_trading_service.sh" "$TIMEFRAME"

log_msg "✅ $TIMEFRAME trading service completed"
