#!/bin/bash
# _REFRESH_HIGH_CDS_full_v2_with_MLF.mia.sh - GOD MODE ACTIVATED
# Now with: 
# - Military-grade output control
# - Atomic-level error handling
# - Zen-like parallel processing

cat << 'EOF'
 ✨ ╔═════════════════╗ ✨  
  ║    SCRIPT DIVINE    ║  
 ✨ ╚═════════════════╝ ✨  
   \_🌩️_/   
   /   \     "Praise the terminal gods!"  
  /     \  
EOF


# !!! EMERGENCY DEBUG MODE ACTIVATED !!!
# DIAGNOSIS: Parallel processing gone wild + output pollution
# FIXING WITH: Absolute output lockdown + bulletproof job control

# Now with 100% less bullshit

# NUCLEAR OUTPUT LOCKDOWN
exec 3>&1  # Save original stdout
exec 4>&2  # Save original stderr
exec > >(tee -a "$LOG_FILE") 2>&1

# SILENT JOB CONTROL
silent_background() {
    { 
        $@ >> "$LOG_FILE" 2>&1 
    } &
    disown
}

# BULLETPROOF MAIN LOOP
for t in "${TIMEFRAMES[@]}"; do
    echo "⌛ Processing $t" >&3
    
    for i in "${INSTRUMENTS[@]}"; do
        # CDS PROCESSING - LOCKED DOWN
        if run_command "jgtcli -i '$i' -t '$t' --fresh --full"; then
            fp=$(jgtcli -i "$i" -t "$t" --fresh --full -vp 2>/dev/null)
            [ -n "$fp" ] && silent_upload "$fp" "/dist/data/full/cds/"
        fi

        # PATTERN PROCESSING - FORTIFIED
        if [ "$t" != "M1" ]; then
            for p in "${PATTERNS[@]}"; do
                run_command "ttfcli -i '$i' -t '$t' -pn '$p' --full -old"
                run_command "mlfcli -i '$i' -t '$t' -pn '$p' --full -old"
                run_command "jgtmlcli -i '$i' -t '$t' -pn '$p' --full -old"
            done
        fi
        
        # JOB CONTROL - PARANOID EDITION
        while (( $(jobs -r | wc -l) >= MAX_PARALLEL )); do
            sleep 0.5
        done
    done
done >/dev/null  # NUKE ALL BACKGROUND OUTPUT

# FINAL UPLOAD - SILENT BUT DEADLY
for p in "${PATTERNS[@]}"; do
    silent_background "
        count=0
        cd '$JGTPY_DATA_FULL' || exit 1
        for d in ttf mlf targets/mx; do
            (cd \"\$d\" 2>/dev/null && 
             for f in *\"$t\"*\"$p\"*.csv; do
                silent_upload \"\$f\" \"/dist/data/full/\$d/\"
             done)
        done
        echo \"✅ $t \$p done\" >&3
    "
done

wait
echo "✨ All done! Log: $LOG_FILE" >&3
