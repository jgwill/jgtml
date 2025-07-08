#!/bin/bash
# Unified full data refresh script with parallel processing
# Incorporates parallel techniques from the .mia script with better error handling

set -e  # Exit on error
set +m  # Disable job control messages

# Environment setup
unset JGTPY_DATA_FULL JGTPY_DATA
source .env 2>/dev/null || true
export JGTPY_DATA JGTPY_DATA_FULL

# Configuration  
TIMEFRAMES="M1 W1 D1 H4"
INSTRUMENTS="EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD XAU/USD"
PATTERNS="mfi mz zonesq aoac"  # Added aoac pattern from scripts analysis

# Dynamic parallel job calculation
CPU_CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "4")
MAX_PARALLEL=${JGT_MAX_PARALLEL:-$((CPU_CORES + 2))}  # Default: CPU cores + 2, override with env var

# Job control functions
get_job_count() {
    jobs -r | wc -l
}

wait_for_slots() {
    while (( $(get_job_count) >= MAX_PARALLEL )); do
        sleep 0.5
    done
}

# Silent background processing with job control
run_background() {
    local cmd="$1"
    local description="$2"
    
    wait_for_slots
    {
        if eval "$cmd" &>/dev/null; then
            echo "✓ $description"
        else
            echo "✗ $description FAILED"
        fi
    } &
}

# Silent upload with retry
silent_upload() {
    local file="$1"
    local target="$2"
    
    if [ -f "$file" ]; then
        for attempt in 1 2 3; do
            if droxul upload "$file" "$target" &>/dev/null; then
                return 0
            fi
            sleep 1
        done
        echo "Upload failed after 3 attempts: $file"
        return 1
    fi
}

echo "Starting parallel unified full data refresh..."
echo "CPU cores detected: $CPU_CORES"
echo "Max parallel jobs: $MAX_PARALLEL (${JGT_MAX_PARALLEL:+override set, }default: ${CPU_CORES}+2)"
echo "Timeframes: $TIMEFRAMES"
echo "Instruments: $INSTRUMENTS"
echo "Patterns: $PATTERNS"

# Create remote directories in parallel
echo "Creating remote directories..."
{
    droxul mkdir /dist/data/full/cds &>/dev/null
    droxul mkdir /dist/data/full/ttf &>/dev/null
    droxul mkdir /dist/data/full/mlf &>/dev/null
    droxul mkdir /dist/data/full/targets/mx &>/dev/null
} &

# Process each timeframe and instrument with controlled parallelism
for t in $TIMEFRAMES; do
    echo "Processing timeframe: $t"
    
    # Process all instruments in parallel for this timeframe
    for i in $INSTRUMENTS; do
        wait_for_slots
        {
            echo "🔄 Processing pipeline for $i $t"
            
            # SEQUENTIAL PIPELINE: CDS → TTF → MLF → MX (DEPENDENCIES!)
            # Step 1: CDS (foundation data)
            if jgtcli -i "$i" -t "$t" --fresh --full &>/dev/null; then
                fp=$(jgtcli -i "$i" -t "$t" --fresh --full -vp 2>/dev/null)
                if [ -n "$fp" ]; then
                    silent_upload "$fp" "/dist/data/full/cds/" &
                    echo "✓ CDS $i $t processed and uploading"
                else
                    echo "✗ CDS $i $t - no file path returned"
                    exit 1  # Exit this background job
                fi
            else
                echo "✗ CDS $i $t - processing failed"
                exit 1  # Exit this background job
            fi
            
            # Pattern processing (skip M1 for performance)
            if [ "$t" != "M1" ]; then
                for p in $PATTERNS; do
                    # Step 2: TTF (Transformed Trading Features - depends on CDS)
                    if ttfcli -i "$i" -t "$t" -pn "$p" --full -old &>/dev/null; then
                        echo "✓ TTF $i $t $p"
                        
                        # Step 3: MLF (Meta Lag Features - depends on TTF)
                        if mlfcli -i "$i" -t "$t" -pn "$p" --full -old &>/dev/null; then
                            echo "✓ MLF $i $t $p"
                            
                            # Step 4: MX (ML targets - depends on MLF/TTF)
                            if jgtmlcli -i "$i" -t "$t" -pn "$p" --full -old &>/dev/null; then
                                echo "✓ MX $i $t $p"
                            else
                                echo "✗ MX $i $t $p - failed"
                            fi
                        else
                            echo "✗ MLF $i $t $p - failed (skipping MX)"
                        fi
                    else
                        echo "✗ TTF $i $t $p - failed (skipping MLF/MX)"
                    fi
                done
            fi
        } &
    done
    
    # Wait for current timeframe to complete before starting uploads
    wait
    echo "✓ All processing completed for $t"
    
    # Batch upload pattern files for this timeframe (parallel by pattern)
    if [ "$t" != "M1" ]; then
        echo "Uploading pattern files for $t..."
        
        for p in $PATTERNS; do
            wait_for_slots
            {
                if [ -d "$JGTPY_DATA_FULL" ]; then
                    cd "$JGTPY_DATA_FULL" || exit 1
                    
                    # Upload each data type in parallel
                    for d in ttf mlf targets/mx; do
                        if [ -d "$d" ]; then
                            (
                                cd "$d" 2>/dev/null || exit 0
                                for f in *"$t"*"$p"*.csv; do
                                    if [ -f "$f" ]; then
                                        silent_upload "$f" "/dist/data/full/$d/" &
                                    fi
                                done
                                wait  # Wait for all uploads in this directory
                            ) &
                        fi
                    done
                    wait  # Wait for all directories
                    echo "✓ $t $p upload batch completed"
                else
                    echo "✗ $t $p - JGTPY_DATA_FULL not found"
                fi
            } &
        done
    fi
done

# Final synchronization
echo "Waiting for all background processes to complete..."
wait

echo ""
echo "Parallel job statistics:"
echo "- Max parallel jobs: $MAX_PARALLEL"
echo "- Processing completed for all timeframes"
echo "- All uploads synchronized"

echo ""
echo "Unified parallel full data refresh completed successfully!"
echo "Check results with:"
echo "  ls -la \$JGTPY_DATA_FULL/{cds,ttf,mlf,targets/mx}/"
