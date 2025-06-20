#!/bin/bash
# Unset environment variables
unset JGTPY_DATA_FULL
unset JGTPY_DATA

# Source environment file
source .env 2>/dev/null || true

# Export variables
export JGTPY_DATA
export JGTPY_DATA_FULL

# Ensure folders exist
{
    droxul mkdir /dist/data &>/dev/null
    for d in cds ttf mlf targets; do
        droxul mkdir "/dist/data/full/$d" &>/dev/null
    done
    droxul mkdir "/dist/data/full/targets/mx" &>/dev/null
} &

patterns="mfi mz zonesq"

# Process timeframes and instruments
for t in W1 M1 D1 H4; do 
    for i in EUR/USD USD/CAD SPX500 AUD/USD AUD/CAD GBP/USD; do 
        # Process CDS data and upload
        if jgtcli -i "$i" -t "$t" --fresh --full; then
            fp=$(jgtcli -i "$i" -t "$t" --fresh --full -vp)
            if [ -n "$fp" ]; then
                droxul upload "$fp" "/dist/data/full/cds/" &
            fi
        fi

        # Process patterns (skip M1)
        if [ "$t" != "M1" ]; then 
            for p in $patterns; do 
                ttfcli -i "$i" -t "$t" -pn "$p" --full -old
                mlfcli -i "$i" -t "$t" -pn "$p" --full -old
                jgtmlcli -i "$i" -t "$t" -pn "$p" --full -old
            done
        fi
    done

    # Upload pattern files for timeframe
    for p in $patterns; do 
        (
            cd "$JGTPY_DATA_FULL" || exit 1
            for d in ttf mlf targets/mx; do 
                (
                    cd "$d" 2>/dev/null || continue
                    droxul upload ./*"$t"*"$p"*.csv "/dist/data/full/$d/"
                )
            done
        ) >/dev/null 2>&1 && \
        echo "---- $t UPLOADED OK ----"
    done &
done

# Wait for background processes
wait
