#!/bin/bash
# Unified current data refresh script for CDS + TTF
# Optimized for current/recent data processing

set -e  # Exit on error

# Environment setup
unset JGTPY_DATA_FULL JGTPY_DATA
source .env 2>/dev/null || true
export JGTPY_DATA JGTPY_DATA_FULL

# Configuration
TIMEFRAMES_CDS="W1 M1 D1 H4 H1 m15 m5"
TIMEFRAMES_TTF="D1 H4"
INSTRUMENTS_CDS="XAU/USD EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD"
INSTRUMENTS_TTF="EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD"
PATTERNS_TTF="mz"

echo "Starting unified current data refresh..."

# Create remote directories
echo "Creating remote directories..."
droxul mkdir /dist/data/current/cds &>/dev/null || true
droxul mkdir /dist/data/current/ttf &>/dev/null || true

# Process CDS current data
echo "Processing CDS current data..."
for t in $TIMEFRAMES_CDS; do
    echo "  Timeframe: $t"
    for i in $INSTRUMENTS_CDS; do
        echo "    Processing CDS for $i..."
        if jgtcli -i "$i" -t "$t" --fresh &>/dev/null; then
            fp=$(jgtcli -i "$i" -t "$t" --fresh -vp 2>/dev/null)
            if [ -n "$fp" ] && [ -f "$fp" ]; then
                droxul upload "$fp" "/dist/data/current/cds/" &>/dev/null
                echo "    CDS uploaded: $(basename "$fp")"
            fi
        else
            echo "    CDS failed for $i $t"
        fi
    done
done

# Process TTF current data
echo "Processing TTF current data..."
for i in $INSTRUMENTS_TTF; do
    for t in $TIMEFRAMES_TTF; do
        for p in $PATTERNS_TTF; do
            echo "  Processing TTF: $i $t $p"
            if ttfcli -i "$i" -t "$t" -pn "$p" &>/dev/null; then
                echo "    TTF completed"
            else
                echo "    TTF failed"
            fi
        done
    done
done

# Upload TTF files
echo "Uploading TTF files..."
if [ -d "$JGTPY_DATA/ttf" ]; then
    cd "$JGTPY_DATA/ttf"
    for f in *.csv; do
        if [ -f "$f" ]; then
            droxul upload "$f" "/dist/data/current/ttf/$f" &>/dev/null
        fi
    done
    echo "TTF upload completed"
fi

echo "Unified current data refresh completed successfully!"