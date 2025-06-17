# Production Trading Guide - Enhanced FDB System

## 🤖 AUTOMATED FDB TRADING SYSTEM - PRODUCTION READY

### 🔴 CRITICAL: Completed Bar Analysis

**NEVER analyze FDB signals on incomplete bars!**

- **Last CSV row** = INCOMPLETE bar (current forming period)  
- **Second-to-last CSV row** = COMPLETED bar (FDB signal analysis target)
- **Our system** = Correctly analyzes COMPLETED bars only via `get_last_two_bars()`

## 🚀 Enhanced Trading CLI Commands

### 1. Generate Fresh FDB Data
```bash
# Single instrument, multiple timeframes
enhancedtradingcli production -i EUR-USD -t D1 H4 H1

# Multiple instruments
enhancedtradingcli production -i EUR-USD,GBP-USD,XAU-USD -t D1 H4
```

### 2. Enhanced FDB Analysis with Illusion Detection
```bash
# Single instrument analysis
enhancedtradingcli enhanced -i EUR-USD -t D1 H4 --summary-only

# Multiple instruments with full details
enhancedtradingcli enhanced -i EUR-USD,GBP-USD -t D1 H4
```

### 3. **NEW: Automated Trading with Higher Timeframe Bias**
```bash
# Automated trading analysis with campaign creation
enhancedtradingcli auto-trade -i EUR-USD --demo --quality-threshold 7.0

# Multiple instruments, real trading mode
enhancedtradingcli auto-trade -i EUR-USD,GBP-USD,XAU-USD --real --quality-threshold 8.0

# Conservative approach (higher threshold)
enhancedtradingcli auto-trade -i USD-CAD --demo --quality-threshold 9.0
```

## 🎯 Automated Trading Workflow

### Step 1: Higher Timeframe Bias Analysis
- **Monthly (M1)**: Weight = 3x
- **Weekly (W1)**: Weight = 2x  
- **Daily (D1)**: Weight = 1x
- **Overall Bias**: Calculated with confidence scoring

### Step 2: Trading Timeframe Scanning
- **H4**: Primary trading timeframe (bonus +1.0)
- **H1**: Secondary timeframe (bonus +0.5)
- **m15**: Short-term entries (bonus +0.0)

### Step 3: Quality Scoring Algorithm
- **Base Score**: 5.0
- **HTF Alignment**: +3.0 × confidence (if signal aligns with bias)
- **Zone Confirmation**: +1.5 (if zone signal confirms FDB)
- **MFI Fade**: +0.5 (if MFI fade present)
- **Timeframe Bonus**: H4 > H1 > m15

### Step 4: Campaign Creation
**Automatic campaign creation when Quality Score ≥ threshold**

## 📁 Campaign System

### Campaign Structure
```
campaigns/
└── EUR-USD_H4_20250117_154500/
    ├── campaign.json          # Complete campaign metadata
    ├── entry.sh              # Execute trade order
    ├── status.sh             # Check order status  
    ├── watch.sh              # Monitor order
    ├── cancel.sh             # Cancel order
    └── README.md             # Complete instructions
```

### Campaign Execution
```bash
# 1. Navigate to campaign directory
cd campaigns/EUR-USD_H4_20250117_154500/

# 2. Review campaign details
cat README.md

# 3. Execute trade
./entry.sh

# 4. Update ORDER_ID in monitoring scripts (from fxaddorder output)
# Edit status.sh, watch.sh, cancel.sh with actual order ID

# 5. Monitor position
./status.sh    # Check current status
./watch.sh     # Continuous monitoring
./cancel.sh    # Cancel if needed
```

## 📊 Real Trading Examples

### High-Quality Signals (Automated Campaign Creation)
```bash
# EUR-USD: STRONG SELL (Quality: 9.0/10, 0 illusions)
# USD-CAD: STRONG BUY (Quality: 9.0/10, 0 illusions)  
# AUD-CAD: STRONG BUY (Quality: 9.0/10, 0 illusions)
# XAU-USD: STRONG SELL (Quality: 9.0/10, 0 illusions)
```

### Medium-Quality Signals (Manual Review)
```bash
# GBP-USD: MONITOR (Quality: 9.0/10, conflicting timeframes)
# EUR-CAD: MONITOR (Quality: 9.0/10, conflicting D1 SELL/H4 BUY)
```

### Low-Quality Signals (Monitor Only)
```bash
# SPX500: MONITOR (Quality: 6.0/10, 2 illusions detected)
# AUS200: MONITOR (Quality: 6.0/10, 2 illusions detected)
```

## ⚠️ Risk Management

### Demo vs Real Trading
- **Demo Mode**: `--demo` flag (default)
- **Real Mode**: `--real` flag (overrides demo)
- **Always test** in demo mode first

### Quality Thresholds
- **Conservative**: 9.0+ (very high quality only)
- **Balanced**: 8.0+ (high quality signals)
- **Aggressive**: 7.0+ (good quality signals)
- **Manual Review**: 6.0-6.9 (moderate quality)

### Position Sizing
- **Standard**: 1 lot (current system default)
- **Custom**: Modify in campaign scripts before execution
- **Risk**: 2% per trade maximum recommended

## 🔍 System Status Commands

### Check All Components
```bash
# Enhanced scanner status
enhancedtradingcli status

# Production scanner status  
enhancedtradingcli production --help

# Automated trading status
enhancedtradingcli auto-trade --help
```

### Data Validation
```bash
# Verify fresh data generation
enhancedtradingcli production -i EUR-USD -t H1

# Verify signal detection
enhancedtradingcli enhanced -i EUR-USD -t H1 --summary-only
```

## 🚀 Production Deployment Checklist

### Pre-Trading Setup ✅
- [x] Enhanced FDB Scanner operational
- [x] Production data generation working
- [x] Automated trading system implemented
- [x] Campaign creation system functional
- [x] Higher timeframe bias analysis operational
- [x] Completed bar analysis documented and implemented

### Risk Management Setup ✅
- [x] Demo mode thoroughly tested
- [x] Quality thresholds configured
- [x] Position sizing defined
- [x] Stop-loss automation via fxaddorder

### Monitoring Setup ✅
- [x] Campaign monitoring scripts created
- [x] Order status tracking implemented
- [x] Manual override capabilities available
- [x] Risk management procedures documented

## 📋 Troubleshooting

### Common Issues
1. **No campaigns created**: Lower quality threshold or check data availability
2. **Import errors**: Ensure package installed with `pip install -e .`
3. **Data issues**: Run production scanner to generate fresh data
4. **Signal validation**: Check SignalOrderingHelper for validation errors

### Support Commands
```bash
# Reinstall package
conda activate jgtml && pip install -e .

# Check package version
python -c "import jgtml; print(jgtml.__version__)"

# Test core functionality
python -c "from jgtml.enhanced_fdb_scanner_with_illusion_detection import EnhancedFDBScanner; print('✅ OK')"
```

## ✅ System Status: PRODUCTION READY

The automated FDB trading system is complete and operational with:
- ✅ Proper completed bar analysis (critical issue resolved)
- ✅ Higher timeframe bias integration  
- ✅ Automated campaign creation
- ✅ Complete trading workflow automation
- ✅ Risk management and monitoring tools
- ✅ Production-ready deployment capabilities

**Ready for live trading with full automation support.** 