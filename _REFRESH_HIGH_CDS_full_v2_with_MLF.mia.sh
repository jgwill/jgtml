#!/bin/bash
echo  '
 ✨ ╔═════════════════╗ ✨  
  ║    SCRIPT DIVINE    ║  
 ✨ ╚═════════════════╝ ✨  
   \_🌩️_/   
   /   \     "Praise the terminal gods!"  
  /     \  
'


# _REFRESH_HIGH_CDS_full_v2_with_MLF.sh - Enhanced Version
# Upgrades:
# 1. Proper error handling and logging
# 2. Parallel processing optimization
# 3. Configuration variables at top
# 4. Status tracking and reporting

# Configuration
INSTRUMENTS=("EUR/USD" "USD/CAD" "SPX500" "AUD/USD" "AUD/CAD" "GBP/USD")
TIMEFRAMES=("W1" "M1" "D1" "H4")
PATTERNS=("mfi" "mz" "zonesq")
MAX_PARALLEL=4  # Limit concurrent processes
LOG_FILE="/tmp/cds_refresh_$(date +%Y%m%d_%H%M%S).log"

# Initialize environment
unset JGTPY_DATA_FULL JGTPY_DATA
source .env 2>/dev/null || true
export JGTPY_DATA JGTPY_DATA_FULL

# Create required directories
echo "[$(date)] Creating remote directories..." >> "$LOG_FILE"
droxul mkdir -p /dist/data/full/{cds,ttf,mlf,targets/mx} 2>> "$LOG_FILE"

# Function to run commands with error handling
run_command() {
    local cmd="$*"
    if ! eval "$cmd" >> "$LOG_FILE" 2>&1; then
        echo "[ERROR] Failed: $cmd" >> "$LOG_FILE"
        return 1
    fi
    return 0
}

# Main processing
echo "[$(date)] Starting processing..." >> "$LOG_FILE"

for t in "${TIMEFRAMES[@]}"; do
    echo "[$(date)] Processing timeframe: $t" >> "$LOG_FILE"
    
    # Process CDS data in parallel
    for i in "${INSTRUMENTS[@]}"; do
        (
            echo "[$(date)] Processing $i $t" >> "$LOG_FILE"
            
            # Get fresh CDS data
            if run_command "jgtcli -i '$i' -t '$t' --fresh --full"; then
                fp=$(jgtcli -i "$i" -t "$t" --fresh --full -vp 2>/dev/null)
                [ -n "$fp" ] && run_command "droxul upload '$fp' /dist/data/full/cds/"
            fi
            
            # Process patterns (skip M1)
            if [ "$t" != "M1" ]; then
                for p in "${PATTERNS[@]}"; do
                    run_command "ttfcli -i '$i' -t '$t' -pn '$p' --full -old"
                    run_command "mlfcli -i '$i' -t '$t' -pn '$p' --full -old"
                    run_command "jgtmlcli -i '$i' -t '$t' -pn '$p' --full -old"
                done
            fi
        ) &
        
        # Limit concurrent processes
        if (( $(jobs -r -p | wc -l) >= MAX_PARALLEL )); then
            wait -n
        fi
    done
    
    # Upload pattern files
    for p in "${PATTERNS[@]}"; do
        (
            echo "[$(date)] Uploading $t $p files" >> "$LOG_FILE"
            cd "$JGTPY_DATA_FULL" || exit 1
            
            for d in ttf mlf targets/mx; do
                (cd "$d" && droxul upload *"$t"*"$p"*.csv /dist/data/full/"$d"/)
            done
            
            echo "---- $t UPLOADED OK ----"
        ) &
    done
done

wait  # Wait for all background processes
echo "[$(date)] Processing complete" >> "$LOG_FILE"
echo "Full log available at: $LOG_FILE"

