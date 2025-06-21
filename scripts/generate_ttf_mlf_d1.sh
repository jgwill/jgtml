#!/usr/bin/env bash
# generate_ttf_mlf_d1.sh - create TTF and MLF files from CDS for D1 timeframe
set -euo pipefail

TIMEFRAMES="D1"
INSTRUMENTS="EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD"
PATTERNS="mfi mz zonesq"
MAX_PARALLEL=${MAX_PARALLEL:-4}

source .env 2>/dev/null || true
export JGTPY_DATA_FULL=${JGTPY_DATA_FULL:-$(pwd)/data/full}
DATA_CHECK_GLOB="$JGTPY_DATA_FULL/cds/*.csv"

if ! ls $DATA_CHECK_GLOB 1> /dev/null 2>&1; then
    echo "No CDS data found in $JGTPY_DATA_FULL. Place CSV files under cds/ and rerun." >&2
    exit 1
fi

queue(){
    while (( $(jobs -r | wc -l) >= MAX_PARALLEL )); do
        sleep 0.5
    done
    "$@" &
}

for inst in $INSTRUMENTS; do
    for pat in $PATTERNS; do
        queue ttfcli -i "$inst" -t D1 -pn "$pat" --full -old
        queue mlfcli -i "$inst" -t D1 -pn "$pat" --full -old
    done
done

wait
printf '\nGeneration complete.\n'
