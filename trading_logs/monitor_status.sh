#!/bin/bash
# Monitor Status Dashboard

clear
echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║              PRODUCTION FDB MONITOR STATUS DASHBOARD                          ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

MONITOR_PID=$(pgrep -f "production_fdb_monitor_scheduled.py" | head -1)

if [ -z "$MONITOR_PID" ]; then
    echo "❌ Monitor NOT RUNNING"
    exit 1
fi

echo "✅ Monitor ACTIVE (PID: $MONITOR_PID)"
echo "📅 Time: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 LATEST SCANS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for inst in EUR-USD GBP-USD AUD-USD; do
    LOG="/b/trading/jgtml/trading_logs/TRADING_${inst}_251231.md"
    if [ -f "$LOG" ]; then
        echo ""
        echo "📈 $inst"
        echo "─────────────────────────────────────────"
        
        # Get latest scans
        m5_scans=$(grep -c "m5.*scan" "$LOG" 2>/dev/null || echo 0)
        m15_scans=$(grep -c "m15.*scan" "$LOG" 2>/dev/null || echo 0)
        h1_scans=$(grep -c "H1.*scan" "$LOG" 2>/dev/null || echo 0)
        
        echo "  m5 scans:  $m5_scans"
        echo "  m15 scans: $m15_scans"
        echo "  H1 scans:  $h1_scans"
        
        # Get latest order
        latest_order=$(grep "\[ORDER\].*PLACED" "$LOG" | tail -1)
        if [ ! -z "$latest_order" ]; then
            echo ""
            echo "  Latest order: $(echo $latest_order | sed 's/.*PLACED: //' | cut -d' ' -f1)"
        fi
        
        # Get latest timestamp
        latest=$(tail -5 "$LOG" | grep "^\*\*\[" | tail -1)
        if [ ! -z "$latest" ]; then
            timestamp=$(echo "$latest" | grep -oP '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
            echo "  Last activity: $timestamp"
        fi
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 MONITORING SCHEDULE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔵 m5  signals: Every 5 minutes    (:00, :05, :10, :15, :20, :25, :30...)"
echo "🟢 m15 signals: At :00, :15, :30, :45 of each hour"
echo "🟡 H1  signals: Every hour at :00"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
