#!/bin/bash
echo '
 ✨ ╔═════════════════╗ ✨  
  ║    SCRIPT DIVINE    ║  
 ✨ ╚═════════════════╝ ✨  
   \_🌩️_/   
   /   \     "Praise the terminal gods!"  
  /     \  
'

# Configuration
INSTRUMENTS=("EUR/USD" "USD/CAD" "SPX500" "AUD/USD" "AUD/CAD" "GBP/USD")
TIMEFRAMES=("W1" "M1" "D1" "H4")
PATTERNS=("mfi" "mz" "zonesq")
MAX_PARALLEL=4
LOG_FILE="/tmp/cds_refresh_$(date +%Y%m%d_%H%M%S).log"

# Initialize environment
unset JGTPY_DATA_FULL JGTPY_DATA
source .env 2>/dev/null || true
export JGTPY_DATA JGTPY_DATA_FULL

# Create required directories
echo "[$(date)] Initializing..." | tee -a "$LOG_FILE"
(droxul mkdir -p /dist/data/full/{cds,ttf,mlf,targets/mx} 2>> "$LOG_FILE") &>/dev/null

# Enhanced run_command with output control
run_command() {
    local cmd="$*"
    echo "[RUN] $cmd" >> "$LOG_FILE"
    if ! eval "$cmd" >> "$LOG_FILE" 2>&1; then
        echo "[ERROR] Failed: $cmd" | tee -a "$LOG_FILE"
        return 1
    fi
    return 0
}

# Silent droxul wrapper
silent_upload() {
    droxul upload "$1" "$2" >/dev/null 2>&1
    local status=$?
    [ $status -eq 0 ] && echo "[UPLOAD] Success: $1" >> "$LOG_FILE"
    return $status
}

# Main processing
for t in "${TIMEFRAMES[@]}"; do
    echo "== Processing $t ==" | tee -a "$LOG_FILE"
    
    for i in "${INSTRUMENTS[@]}"; do
        (
            # CDS Processing
            if run_command "jgtcli -i '$i' -t '$t' --fresh --full"; then
                fp=$(jgtcli -i "$i" -t "$t" --fresh --full -vp 2>/dev/null)
                [ -n "$fp" ] && silent_upload "$fp" "/dist/data/full/cds/"
            fi

            # Pattern Processing (skip M1)
            if [ "$t" != "M1" ]; then
                for p in "${PATTERNS[@]}"; do
                    run_command "ttfcli -i '$i' -t '$t' -pn '$p' --full -old"
                    run_command "mlfcli -i '$i' -t '$t' -pn '$p' --full -old"
                    run_command "jgtmlcli -i '$i' -t '$t' -pn '$p' --full -old"
                done
            fi
        ) &
        
        # Job control
        while (( $(jobs -r -p | wc -l) >= MAX_PARALLEL )); do
            sleep 0.1
        done
    done
done

# Final uploads with progress
echo "== Finalizing Uploads ==" | tee -a "$LOG_FILE"
for p in "${PATTERNS[@]}"; do
    (
        count=0
        cd "$JGTPY_DATA_FULL" || exit 1
        for d in ttf mlf targets/mx; do
            (cd "$d" && for f in *"$t"*"$p"*.csv; do
                silent_upload "$f" "/dist/data/full/$d/" && ((count++))
            done)
        done
        echo "Uploaded $count $t $p files" >> "$LOG_FILE"
    ) &
done

wait
echo "✨ All done! Full log: $LOG_FILE" | tee -a "$LOG_FILE"

