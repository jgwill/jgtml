#!/bin/bash
# 🔮🧠 ResoNova & Mia's Discovery Target Generation Workflow  
# Purpose: Historical analysis and ML pattern discovery (full datasets)
# Namespace: ./data/full/ (JGTPY_DATA_FULL)

set -e  # Exit on any error

# Load environment variables if present
if [ -f "$HOME/.env" ]; then
    set -o allexport
    source "$HOME/.env"
    set +o allexport
fi

# Verify JGT configuration exists
if [ ! -f "$HOME/.jgt/config.json" ] || [ ! -f "$HOME/.jgt/settings.json" ]; then
    echo "Missing JGT configuration files in $HOME/.jgt" >&2
fi

# Find the project root directory (where this script is run from)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Default parameters
TIMEFRAMES="D1"
INSTRUMENTS="SPX500 EUR-USD"
PATTERNS="mfi mz zonesq aoac"  # All patterns for discovery

# Override with command line arguments
if [ "$1" != "" ]; then
    TIMEFRAMES="$1"
fi
if [ "$2" != "" ]; then
    INSTRUMENTS="$2"
fi
if [ "$3" != "" ]; then
    PATTERNS="$3"
fi

USE_OFFLINE_DATA=1
USE_OFFLINE_ARG=""
if [ "$USE_OFFLINE_DATA" -eq 1 ]; then
    USE_OFFLINE_ARG="-old"
fi

echo "🔮 DISCOVERY Target Generation Workflow"
echo "🧠 Generating full historical datasets for ML pattern discovery"
echo "🔧 Instruments: $INSTRUMENTS"
echo "⏱️  Timeframes: $TIMEFRAMES" 
echo "🎨 Patterns: $PATTERNS"
echo "📁 Output: ${PROJECT_ROOT}/data/full/ (complete historical data)"
echo ""

cd "${PROJECT_ROOT}"

for pattern in $PATTERNS; do
    echo "🔮 Processing Pattern: $pattern"
    
    for instrument in $INSTRUMENTS; do
        for timeframe in $TIMEFRAMES; do
            echo "📊 $instrument $timeframe $pattern"
            
            # Generate TTF (Time-To-Feature) - Full historical dataset
            echo "## Creating FULL TTF for $instrument $timeframe $pattern"
            python - <<EOF
from jgtml.ttfcli import generate_ttf_for_pattern
generate_ttf_for_pattern("$instrument", "$timeframe", pn="$pattern", use_full=True)
EOF
            
            # Generate MLF (Machine Learning Features) - Full historical dataset
            echo "## Creating FULL MLF for $instrument $timeframe $pattern" 
            python - <<EOF
from jgtml.mlfcli import generate_mlf_for_pattern
generate_mlf_for_pattern("$instrument", "$timeframe", pn="$pattern", use_full=True)
EOF
            
            # Generate MX Targets - This is AUTONOMOUS and will create TTF if missing!
            echo "## Creating MX Targets for $instrument $timeframe $pattern"
            echo "🤖 jgtmlcli.py is autonomous - will generate prerequisites if missing"
            python jgtml/jgtmlcli.py -i "$instrument" -t "$timeframe" -pn "$pattern" $USE_OFFLINE_ARG
            
            echo "✅ Discovery targets ready for $instrument $timeframe $pattern"
            echo ""
        done
    done
done

echo "🎉 DISCOVERY Target Generation Complete!"
echo "🔮 Full historical datasets ready for ML analysis"
echo "📁 TTF/MLF: ./data/full/ttf/, ./data/full/mlf/"
echo "📁 MX Targets: ./data/full/targets/mx/"
echo ""
echo "🧠 Next: Train ML models to discover which patterns predict profitable FDBSignals"
echo "💎 Goal: Create FDBSignal Quality Predictor using discovered patterns"
