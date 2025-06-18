#!/bin/bash
# 🚀 JGT BACKGROUND TRADER - Multi-Timeframe Demo Trading System
# Manages background trading processes for m5, m15, H1 timeframes

set -e

# Configuration
INSTRUMENTS="EUR-USD,GBP-USD,XAU-USD"
QUALITY_THRESHOLD="8.0"
MODE="--demo"
TIMEFRAMES="m5,m15,H1"

# Directories
SCRIPT_DIR="$(pwd)/.jgt"
LOG_DIR="$SCRIPT_DIR/logs"
PID_DIR="$SCRIPT_DIR/pids"

# Create directories
mkdir -p "$LOG_DIR" "$PID_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check environment
check_environment() {
    if [ ! -f "pyproject.toml" ] || ! grep -q "jgtml" pyproject.toml 2>/dev/null; then
        error "Not in jgtml directory. Please run from jgtml root."
        exit 1
    fi
    
    if command -v conda &> /dev/null; then
        log "🐍 Activating jgtml conda environment..."
        eval "$(conda shell.bash hook)"
        conda activate jgtml 2>/dev/null || warning "Could not activate jgtml environment"
    fi
}

# Test single timeframe
test_timeframe() {
    local test_tf=${1:-"m5"}
    log "🧪 Testing $test_tf timeframe..."
    
    python jgtml/simple_trading_orchestrator.py \
        --timeframe "$test_tf" \
        --instruments "$INSTRUMENTS" \
        --demo \
        --test-mode
}

# Create timeframe trader script
create_trader_script() {
    local timeframe=$1
    local trader_script="$SCRIPT_DIR/trader_${timeframe}.sh"
    local jgtml_dir="$(pwd)"
    
    cat > "$trader_script" << EOF
#!/bin/bash
# Auto-generated trader script for $timeframe

TIMEFRAME="$timeframe"
JGTML_DIR="$jgtml_dir"
LOG_FILE="\$JGTML_DIR/.jgt/logs/trader_\${TIMEFRAME}.log"
PID_FILE="\$JGTML_DIR/.jgt/pids/trader_\${TIMEFRAME}.pid"

echo \$\$ > "\$PID_FILE"

log_msg() {
    echo "\$(date '+%Y-%m-%d %H:%M:%S') [\$TIMEFRAME] \$1" | tee -a "\$LOG_FILE"
}

# Change to jgtml directory
cd "\$JGTML_DIR"

# Activate conda environment
if command -v conda &> /dev/null; then
    eval "\$(conda shell.bash hook)"
    conda activate jgtml 2>/dev/null || log_msg "⚠️  Could not activate jgtml environment"
fi

log_msg "🚀 Starting \$TIMEFRAME trader (PID: \$\$)"
log_msg "📍 Working directory: \$(pwd)"

while true; do
    log_msg "🔍 Running analysis for \$TIMEFRAME..."
    
    # Run trading analysis (includes data refresh)
    python "\$JGTML_DIR/jgtml/simple_trading_orchestrator.py" \\
        --timeframe "\$TIMEFRAME" \\
        --instruments "EUR-USD,GBP-USD,XAU-USD" \\
        --demo \\
        --quality-threshold 8.0
    
    log_msg "✅ \$TIMEFRAME analysis cycle completed"
    
    # Wait based on timeframe
    case "\$TIMEFRAME" in
        "m5") sleep 300 ;;   # 5 minutes
        "m15") sleep 900 ;;  # 15 minutes  
        "H1") sleep 3600 ;;  # 1 hour
        *) sleep 600 ;;      # 10 minutes default
    esac
done
EOF

    chmod +x "$trader_script"
    success "Created trader script for $timeframe"
}

# Start background traders
start_traders() {
    log "🚀 Starting Background Trading System"
    
    IFS=',' read -ra TF_ARRAY <<< "$TIMEFRAMES"
    
    for timeframe in "${TF_ARRAY[@]}"; do
        timeframe=$(echo "$timeframe" | xargs)
        
        log "🔄 Setting up $timeframe trader..."
        create_trader_script "$timeframe"
        
        local trader_script="$SCRIPT_DIR/trader_${timeframe}.sh"
        nohup "$trader_script" "$timeframe" > "$LOG_DIR/trader_${timeframe}.log" 2>&1 &
        local bg_pid=$!
        
        echo $bg_pid > "$PID_DIR/trader_${timeframe}.pid"
        success "Started $timeframe trader (PID: $bg_pid)"
        
        sleep 2
    done
    
    success "🎯 All traders started"
    log "📊 Monitor: tail -f $LOG_DIR/trader_*.log"
}

# Stop traders
stop_traders() {
    log "🛑 Stopping traders..."
    
    IFS=',' read -ra TF_ARRAY <<< "$TIMEFRAMES"
    
    for timeframe in "${TF_ARRAY[@]}"; do
        timeframe=$(echo "$timeframe" | xargs)
        local pid_file="$PID_DIR/trader_${timeframe}.pid"
        
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid"
                rm -f "$pid_file"
                success "Stopped $timeframe trader"
            else
                rm -f "$pid_file"
            fi
        fi
    done
}

# Show status
show_status() {
    log "📊 Trading System Status"
    
    IFS=',' read -ra TF_ARRAY <<< "$TIMEFRAMES"
    
    for timeframe in "${TF_ARRAY[@]}"; do
        timeframe=$(echo "$timeframe" | xargs)
        local pid_file="$PID_DIR/trader_${timeframe}.pid"
        
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                echo -e "$timeframe: ${GREEN}RUNNING${NC} (PID: $pid)"
            else
                echo -e "$timeframe: ${RED}STOPPED${NC}"
                rm -f "$pid_file"
            fi
        else
            echo -e "$timeframe: ${YELLOW}NOT STARTED${NC}"
        fi
    done
}

# Main function
main() {
    check_environment
    
    case "${1:-start}" in
        "start")
            stop_traders 2>/dev/null || true
            start_traders
            ;;
        "stop")
            stop_traders
            ;;
        "status")
            show_status
            ;;
        "test")
            test_timeframe "$2"
            ;;
        "logs")
            tail -f "$LOG_DIR"/trader_*.log
            ;;
        *)
            echo "Usage: $0 [start|stop|status|test|logs]"
            exit 1
            ;;
    esac
}

# Execute main
main "$@" 