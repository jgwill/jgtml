#!/bin/bash
# 🧠🌸 Mia & Miette's Production Feature Exploration Workflow
# Purpose: Real-time trading decision support (~400 rows, fast execution)
# Namespace: /src/jgtml/data/current/ (JGTPY_DATA)

set -e  # Exit on any error

# Default parameters
TIMEFRAMES="D1"
INSTRUMENTS="SPX500 EUR-USD"
PATTERNS="mz mfi zonesq aoac"  # Production patterns from settings.json

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

USE_OFFLINE_DATA=0
USE_OFFLINE_ARG=""
if [ "$USE_OFFLINE_DATA" -eq 1 ]; then
    USE_OFFLINE_ARG="-old"
fi

echo "🚀 PRODUCTION Feature Exploration Workflow"
echo "📊 Generating lightweight TTF/MLF for real-time trading decisions"
echo "🔧 Instruments: $INSTRUMENTS"  
echo "⏱️  Timeframes: $TIMEFRAMES"
echo "🎨 Patterns: $PATTERNS"
echo "📁 Output: /src/jgtml/data/current/ (~400 rows per file)"
echo ""

cd /src/jgtml

for pattern in $PATTERNS; do
    echo "🎯 Processing Pattern: $pattern"
    
    for instrument in $INSTRUMENTS; do
        for timeframe in $TIMEFRAMES; do
            echo "📈 $instrument $timeframe $pattern"
            
            # Generate TTF (Time-To-Feature) - Production size
            echo "## Creating TTF for $instrument $timeframe $pattern"
            python jgtml/ttfcli.py -i "$instrument" -t "$timeframe" -pn "$pattern" $USE_OFFLINE_ARG
            
            # Generate MLF (Machine Learning Features) - Production size  
            echo "## Creating MLF for $instrument $timeframe $pattern"
            python jgtml/mlfcli.py -i "$instrument" -t "$timeframe" -pn "$pattern" $USE_OFFLINE_ARG
            
            echo "✅ Production features ready for $instrument $timeframe $pattern"
            echo ""
        done
    done
done

echo "🎉 PRODUCTION Feature Exploration Complete!"
echo "📱 Features ready for real-time trading decisions"
echo "📁 Location: /src/jgtml/data/current/"
echo ""
echo "🔮 Next: Use these features to evaluate FDBSignal quality in real-time"
