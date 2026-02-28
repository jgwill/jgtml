#!/bin/bash
# Weekend refresh: Regenerate TTF/MLF from existing CDS data
# No market data required, no cloud uploads

set -e
source .env 2>/dev/null || true

INSTRUMENTS="EUR/USD AUD/CAD AUD/USD USD/CAD GBP/USD XAU/USD"
TIMEFRAMES="D1 H4"
PATTERNS="mfi mz zonesq aoac"
MAX_JOBS=12

get_job_count() {
    jobs -r | wc -l
}

wait_for_slot() {
    while (( $(get_job_count) >= MAX_JOBS )); do
        sleep 0.2
    done
}

echo "🔄 Regenerating TTF/MLF from existing CDS data"
echo "Instruments: $INSTRUMENTS"
echo "Timeframes: $TIMEFRAMES"
echo "Patterns: $PATTERNS"
echo "Max parallel jobs: $MAX_JOBS"
echo ""

total=0
for i in $INSTRUMENTS; do
    for t in $TIMEFRAMES; do
        for p in $PATTERNS; do
            total=$((total + 1))
        done
    done
done

echo "Total operations: $total TTF + $total MLF = $((total * 2))"
echo ""

count=0
for i in $INSTRUMENTS; do
    for t in $TIMEFRAMES; do
        for p in $PATTERNS; do
            wait_for_slot
            {
                if ttfcli -i "$i" -t "$t" -pn "$p" &>/dev/null; then
                    echo "✓ TTF $i $t $p"
                    if mlfcli -i "$i" -t "$t" -pn "$p" &>/dev/null; then
                        echo "✓ MLF $i $t $p"
                    else
                        echo "✗ MLF $i $t $p"
                    fi
                else
                    echo "✗ TTF $i $t $p (skipping MLF)"
                fi
            } &
            count=$((count + 1))
        done
    done
done

wait
echo ""
echo "✅ Regeneration complete: $count operations processed"
