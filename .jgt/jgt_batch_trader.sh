#!/bin/bash
# 🚀 JGT BATCH TRADER - Multi-Timeframe Background Trading System
# This script manages multiple timeframe trading processes in background
# Integrates: Enhanced Trading CLI, Trading Orchestrator, Timeframe Scheduler, FDB Scanner

#set -e

# Configuration
DEFAULT_INSTRUMENTS="EUR-USD,GBP-USD,XAU-USD"
DEFAULT_QUALITY_THRESHOLD="8.0"
DEFAULT_MODE="--demo"
DEFAULT_TIMEFRAMES="m5,m15,H1"

# Parse command line arguments
INSTRUMENTS=${1:-$DEFAULT_INSTRUMENTS}
TIMEFRAMES=${2:-$DEFAULT_TIMEFRAMES}
MODE=${3:-$DEFAULT_MODE}
QUALITY_THRESHOLD=${4:-$DEFAULT_QUALITY_THRESHOLD}
ACTION=${5:-"start"}  # start, stop, status, restart

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Directories
BATCH_DIR="$(pwd)/.jgt/batch"
LOG_DIR="$(pwd)/.jgt/logs"
PID_DIR="$(pwd)/.jgt/pids"

# Create directories
mkdir -p "$BATCH_DIR" "$LOG_DIR" "$PID_DIR"

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

info() {
    echo -e "${PURPLE}📊 $1${NC}"
}

# Check if we're in the right directory
check_environment() {
    if [ ! -f "pyproject.toml" ] || ! grep -q "jgtml" pyproject.toml 2>/dev/null; then
        error "Not in jgtml directory. Please run from jgtml root."
        exit 1
    fi
    
    # Activate conda environment
    if command -v conda &> /dev/null; then
        log "🐍 Activating jgtml conda environment..."
        eval "$(conda shell.bash hook)"
        conda activate jgtml 2>/dev/null || warning "Could not activate jgtml environment"
    fi
}

# Create individual timeframe runner script
create_timeframe_runner() {
    local timeframe=$1
    local instruments=$2
    local mode=$3
    local quality_threshold=$4
    
    local runner_script="$BATCH_DIR/trader_${timeframe}.sh"
    
    cat > "$runner_script" << EOF
#!/bin/bash
# Auto-generated timeframe trader for $timeframe
# Generated: $(date)

TIMEFRAME="$timeframe"
INSTRUMENTS="$instruments"
MODE="$mode"
QUALITY_THRESHOLD="$quality_threshold"

LOG_FILE="$LOG_DIR/trader_\${TIMEFRAME}.log"
PID_FILE="$PID_DIR/trader_\${TIMEFRAME}.pid"

# Store PID
echo \$\$ > "\$PID_FILE"

log_with_timestamp() {
    echo "\$(date '+%Y-%m-%d %H:%M:%S') [\$TIMEFRAME] \$1" >> "\$LOG_FILE"
}

log_with_timestamp "🚀 Starting \$TIMEFRAME trader (PID: \$\$)"
log_with_timestamp "📊 Instruments: \$INSTRUMENTS | Mode: \$MODE | Quality: \$QUALITY_THRESHOLD"

# Change to jgtml directory
cd "$(pwd)"

# Activate conda environment
if command -v conda &> /dev/null; then
    eval "\$(conda shell.bash hook)"
    conda activate jgtml 2>/dev/null
fi

# Main trading loop using timeframe scheduler
while true; do
    log_with_timestamp "⏰ Waiting for \$TIMEFRAME timeframe..."
    
    # Use timeframe scheduler to wait for the specific timeframe
    if wtf -t "\$TIMEFRAME" -N -S "$(pwd)/.jgt/jgt_fdb_unified_scan.sh" "\$TIMEFRAME" "\$(date '+%H:%M')" "\$MODE" "\$INSTRUMENTS" "\$QUALITY_THRESHOLD"; then
        log_with_timestamp "✅ \$TIMEFRAME cycle completed successfully"
    else
        log_with_timestamp "❌ \$TIMEFRAME cycle failed"
    fi
    
    # Small delay to prevent rapid cycling
    sleep 5
done
EOF

    chmod +x "$runner_script"
    success "Created runner for $timeframe: $runner_script"
}

# Start background trading processes
start_trading() {
    log "🚀 Starting JGT Batch Trading System"
    info "Instruments: $INSTRUMENTS"
    info "Timeframes: $TIMEFRAMES"
    info "Mode: $MODE"
    info "Quality Threshold: $QUALITY_THRESHOLD"
    
    # Parse timeframes
    IFS=',' read -ra TF_ARRAY <<< "$TIMEFRAMES"
    
    for timeframe in "${TF_ARRAY[@]}"; do
        timeframe=$(echo "$timeframe" | xargs) # Trim whitespace
        
        log "🔄 Setting up $timeframe trader..."
        
        # Create runner script
        create_timeframe_runner "$timeframe" "$INSTRUMENTS" "$MODE" "$QUALITY_THRESHOLD"
        
        # Start the trader in background
        local runner_script="$BATCH_DIR/trader_${timeframe}.sh"
        local log_file="$LOG_DIR/trader_${timeframe}.log"
        local pid_file="$PID_DIR/trader_${timeframe}.pid"
        
        # Start in background
        nohup "$runner_script" > "$log_file" 2>&1 &
        local bg_pid=$!
        
        # Update PID file with background process PID
        echo $bg_pid > "$pid_file"
        
        success "Started $timeframe trader (PID: $bg_pid)"
        info "Log: $log_file"
        info "PID: $pid_file"
        
        sleep 2  # Small delay between starts
    done
    
    log "🎯 All trading processes started"
    echo
    info "Monitor logs: tail -f $LOG_DIR/trader_*.log"
    info "Check status: $0 \"$INSTRUMENTS\" \"$TIMEFRAMES\" \"$MODE\" \"$QUALITY_THRESHOLD\" status"
    info "Stop trading: $0 \"$INSTRUMENTS\" \"$TIMEFRAMES\" \"$MODE\" \"$QUALITY_THRESHOLD\" stop"
}

# Stop all trading processes
stop_trading() {
    log "🛑 Stopping JGT Batch Trading System"
    
    # Parse timeframes
    IFS=',' read -ra TF_ARRAY <<< "$TIMEFRAMES"
    
    for timeframe in "${TF_ARRAY[@]}"; do
        timeframe=$(echo "$timeframe" | xargs)
        local pid_file="$PID_DIR/trader_${timeframe}.pid"
        
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                log "🛑 Stopping $timeframe trader (PID: $pid)"
                kill "$pid"
                rm -f "$pid_file"
                success "Stopped $timeframe trader"
            else
                warning "$timeframe trader (PID: $pid) was not running"
                rm -f "$pid_file"
            fi
        else
            warning "No PID file found for $timeframe trader"
        fi
    done
    
    success "All trading processes stopped"
}

# Show status of trading processes
show_status() {
    log "📊 JGT Batch Trading System Status"
    
    # Parse timeframes
    IFS=',' read -ra TF_ARRAY <<< "$TIMEFRAMES"
    
    echo
    printf "%-10s %-10s %-15s %-50s\n" "Timeframe" "Status" "PID" "Log File"
    printf "%-10s %-10s %-15s %-50s\n" "----------" "----------" "---------------" "--------------------------------------------------"
    
    for timeframe in "${TF_ARRAY[@]}"; do
        timeframe=$(echo "$timeframe" | xargs)
        local pid_file="$PID_DIR/trader_${timeframe}.pid"
        local log_file="$LOG_DIR/trader_${timeframe}.log"
        
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                printf "%-10s ${GREEN}%-10s${NC} %-15s %-50s\n" "$timeframe" "RUNNING" "$pid" "$log_file"
            else
                printf "%-10s ${RED}%-10s${NC} %-15s %-50s\n" "$timeframe" "STOPPED" "$pid (dead)" "$log_file"
                rm -f "$pid_file"
            fi
        else
            printf "%-10s ${YELLOW}%-10s${NC} %-15s %-50s\n" "$timeframe" "NOT STARTED" "N/A" "$log_file"
        fi
    done
    
    echo
    info "Real-time monitoring: tail -f $LOG_DIR/trader_*.log"
}

# Test single timeframe (for debugging)
test_single_timeframe() {
    local test_timeframe=${1:-"m5"}
    log "🧪 Testing single timeframe: $test_timeframe"
    
    python jgtml/simple_trading_orchestrator.py \
        --timeframe "$test_timeframe" \
        --instruments "$INSTRUMENTS" \
        --demo \
        --test-mode \
        --max-cycles 1
}

# Main function
main() {
    check_environment
    
    case "$ACTION" in
        "start")
            stop_trading 2>/dev/null || true  # Stop any existing processes
            start_trading
            ;;
        "stop")
            stop_trading
            ;;
        "restart")
            stop_trading 2>/dev/null || true
            sleep 3
            start_trading
            ;;
        "status")
            show_status
            ;;
        "test")
            test_single_timeframe "$6"
            ;;
        *)
            echo "Usage: $0 [instruments] [timeframes] [mode] [quality_threshold] [action]"
            echo
            echo "Arguments:"
            echo "  instruments       Comma-separated instruments (default: $DEFAULT_INSTRUMENTS)"
            echo "  timeframes        Comma-separated timeframes (default: $DEFAULT_TIMEFRAMES)"
            echo "  mode             Trading mode (default: $DEFAULT_MODE)"
            echo "  quality_threshold Quality threshold (default: $DEFAULT_QUALITY_THRESHOLD)"
            echo "  action           Action to perform: start|stop|restart|status|test"
            echo
            echo "Examples:"
            echo "  $0                                          # Start with defaults"
            echo "  $0 EUR-USD m5,m15 --demo 8.0 start        # Start specific config"
            echo "  $0 \"\" \"\" \"\" \"\" status                      # Check status"
            echo "  $0 \"\" \"\" \"\" \"\" stop                        # Stop all"
            echo "  $0 \"\" \"\" \"\" \"\" test m5                      # Test m5 timeframe"
            exit 1
            ;;
    esac
}

# Error handling
trap 'error "Script interrupted"; exit 1' INT TERM

# Execute main function
main "$@" 