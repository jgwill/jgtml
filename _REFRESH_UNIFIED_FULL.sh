#!/bin/bash
# Unified full data refresh script for CDS + MLF + TTF
# Combines functionality from multiple working scripts with proper error handling

set -e  # Exit on error

# Environment setup
unset JGTPY_DATA_FULL JGTPY_DATA
source .env 2>/dev/null || true
export JGTPY_DATA JGTPY_DATA_FULL

# Configuration
TIMEFRAMES="M1 W1 D1 H4"
INSTRUMENTS="EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD XAU/USD"
PATTERNS="mfi mz zonesq aoac"

echo "Starting unified full data refresh..."
echo "Timeframes: $TIMEFRAMES"
echo "Instruments: $INSTRUMENTS"
echo "Patterns: $PATTERNS"

# Create remote directories
echo "Creating remote directories..."
droxul mkdir /dist/data/full/cds &>/dev/null || true
droxul mkdir /dist/data/full/ttf &>/dev/null || true
droxul mkdir /dist/data/full/mlf &>/dev/null || true
droxul mkdir /dist/data/full/targets/mx &>/dev/null || true

# Process each timeframe and instrument
for t in $TIMEFRAMES; do
    echo "Processing timeframe: $t"
    
    for i in $INSTRUMENTS; do
        echo "  Processing $i..."
        
        # Generate and upload CDS data
        echo "    CDS processing..."
        if jgtcli -i "$i" -t "$t" --fresh --full &>/dev/null; then
            fp=$(jgtcli -i "$i" -t "$t" --fresh --full -vp 2>/dev/null)
            if [ -n "$fp" ] && [ -f "$fp" ]; then
                droxul upload "$fp" "/dist/data/full/cds/" &>/dev/null
                echo "    CDS uploaded: $(basename "$fp")"
            fi
        else
            echo "    CDS failed for $i $t"
        fi
        
        # Process patterns (skip M1 for performance)
        if [ "$t" != "M1" ]; then
            for p in $PATTERNS; do
                echo "    Pattern $p processing..."
                
                # TTF processing
                if ttfcli -i "$i" -t "$t" -pn "$p" --full -old &>/dev/null; then
                    echo "      TTF $p completed"
                else
                    echo "      TTF $p failed"
                fi
                
                # MLF processing  
                if mlfcli -i "$i" -t "$t" -pn "$p" --full -old &>/dev/null; then
                    echo "      MLF $p completed"
                else
                    echo "      MLF $p failed"
                fi
                
                # ML targets processing
                if jgtmlcli -i "$i" -t "$t" -pn "$p" --full -old &>/dev/null; then
                    echo "      MX $p completed"
                else
                    echo "      MX $p failed"
                fi
            done
        fi
    done
    
    # Upload pattern-generated files for this timeframe
    if [ "$t" != "M1" ]; then
        echo "  Uploading pattern files for $t..."
        
        for p in $PATTERNS; do
            if [ -d "$JGTPY_DATA_FULL" ]; then
                cd "$JGTPY_DATA_FULL" || continue
                
                # Upload TTF files
                if [ -d "ttf" ]; then
                    (cd ttf && droxul upload ./*"$t"*"$p"*.csv "/dist/data/full/ttf/" 2>/dev/null || true)
                fi
                
                # Upload MLF files
                if [ -d "mlf" ]; then
                    (cd mlf && droxul upload ./*"$t"*"$p"*.csv "/dist/data/full/mlf/" 2>/dev/null || true)
                fi
                
                # Upload ML target files
                if [ -d "targets/mx" ]; then
                    (cd targets/mx && droxul upload ./*"$t"*"$p"*.csv "/dist/data/full/targets/mx/" 2>/dev/null || true)
                fi
            fi
        done
        
        echo "  Upload completed for $t"
    fi
done

echo "Unified full data refresh completed successfully!"
