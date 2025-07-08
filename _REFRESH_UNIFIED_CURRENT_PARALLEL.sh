#!/bin/bash
# Unified current data refresh script with parallel processing
# Optimized for current/recent data with controlled parallelism

set -e  # Exit on error
set +m  # Disable job control messages

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

# Dynamic parallel job calculation
CPU_CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "4")
MAX_PARALLEL=${JGT_MAX_PARALLEL:-$((CPU_CORES * 2))}  # Default: 2x CPU cores, override with env var

# Job control functions
get_job_count() {
    jobs -r | wc -l
}

wait_for_slots() {
    while (( $(get_job_count) >= MAX_PARALLEL )); do
        sleep 0.3
    done
}

# Parallel CDS processing with upload
process_cds_parallel() {
    local instrument="$1"
    local timeframe="$2"
    
    wait_for_slots
    {
        if jgtcli -i "$instrument" -t "$timeframe" --fresh &>/dev/null; then
            fp=$(jgtcli -i "$instrument" -t "$timeframe" --fresh -vp 2>/dev/null)
            if [ -n "$fp" ] && [ -f "$fp" ]; then
                if droxul upload "$fp" "/dist/data/current/cds/" &>/dev/null; then
                    echo "✓ CDS $instrument $timeframe"
                else
                    echo "✗ CDS $instrument $timeframe - upload failed"
                fi
            else
                echo "✗ CDS $instrument $timeframe - no file generated"
            fi
        else
            echo "✗ CDS $instrument $timeframe - processing failed"
        fi
    } &
}

# Parallel TTF processing
process_ttf_parallel() {
    local instrument="$1"
    local timeframe="$2"
    local pattern="$3"
    
    wait_for_slots
    {
        if ttfcli -i "$instrument" -t "$timeframe" -pn "$pattern" &>/dev/null; then
            echo "✓ TTF $instrument $timeframe $pattern"
        else
            echo "✗ TTF $instrument $timeframe $pattern - failed"
        fi
    } &
}

echo "Starting parallel unified current data refresh..."
echo "CPU cores detected: $CPU_CORES"
echo "Max parallel jobs: $MAX_PARALLEL (${JGT_MAX_PARALLEL:+override set, }default: ${CPU_CORES}x2)"
echo "CDS timeframes: $TIMEFRAMES_CDS"
echo "TTF timeframes: $TIMEFRAMES_TTF"

# Create remote directories in parallel
echo "Creating remote directories..."
{
    droxul mkdir /dist/data/current/cds &>/dev/null
    droxul mkdir /dist/data/current/ttf &>/dev/null
} &

# Process CDS current data in parallel
echo ""
echo "Processing CDS current data in parallel..."
for t in $TIMEFRAMES_CDS; do
    echo "Timeframe: $t"
    for i in $INSTRUMENTS_CDS; do
        process_cds_parallel "$i" "$t"
    done
done

# Wait for CDS processing to complete
wait
echo "✓ All CDS processing completed"

# Process TTF current data in parallel
echo ""
echo "Processing TTF current data in parallel..."
for i in $INSTRUMENTS_TTF; do
    for t in $TIMEFRAMES_TTF; do
        for p in $PATTERNS_TTF; do
            process_ttf_parallel "$i" "$t" "$p"
        done
    done
done

# Wait for TTF processing to complete
wait
echo "✓ All TTF processing completed"

# Batch upload TTF files
echo ""
echo "Uploading TTF files..."
if [ -d "$JGTPY_DATA/ttf" ]; then
    cd "$JGTPY_DATA/ttf"
    file_count=0
    for f in *.csv; do
        if [ -f "$f" ]; then
            wait_for_slots
            {
                if droxul upload "$f" "/dist/data/current/ttf/$f" &>/dev/null; then
                    echo "✓ TTF upload: $f"
                else
                    echo "✗ TTF upload failed: $f"
                fi
            } &
            ((file_count++))
        fi
    done
    wait
    echo "✓ TTF upload completed ($file_count files)"
else
    echo "✗ TTF directory not found: $JGTPY_DATA/ttf"
fi

# Final synchronization
echo ""
echo "Waiting for all background processes to complete..."
wait

echo ""
echo "Parallel job statistics:"
echo "- Max parallel jobs: $MAX_PARALLEL"
echo "- CDS instruments processed: $(echo $INSTRUMENTS_CDS | wc -w)"
echo "- TTF patterns processed: $(echo $PATTERNS_TTF | wc -w)"
echo "- Total timeframes: $(echo $TIMEFRAMES_CDS $TIMEFRAMES_TTF | tr ' ' '\n' | sort -u | wc -l)"

echo ""
echo "Unified parallel current data refresh completed successfully!"
echo "Check results with:"
echo "  ls -la \$JGTPY_DATA/{cds,ttf}/"