# 🧠 JGT Data Refresh - Quick Reference

## Most Common Commands

### Real-time Trading (3-5 minutes)
```bash
cd /src/jgtml
./jgtml_refresh production
```

### ML Research (30-60 minutes)
```bash
./jgtml_refresh discovery
```

### Check Data Status
```bash
./jgtml_refresh status
```

### View Help
```bash
./jgtml_refresh help
```

---

## Custom Configurations

### Specific Instruments
```bash
./jgtml_refresh production --instruments "EUR/USD,XAU/USD,SPX500"
```

### Specific Timeframes
```bash
./jgtml_refresh production --timeframes "D1,H4"
```

### Reduce Parallel Jobs (for slow systems)
```bash
./jgtml_refresh production --max-jobs 2
```

### Extended Pattern Analysis
```bash
./jgtml_refresh production --patterns "mfi mz zonesq aoac"
```

### Cleanup Old Data Then Refresh
```bash
./jgtml_refresh production --cleanup 7
```

---

## Pipeline Stages

| Stage | Command | Output | Time |
|-------|---------|--------|------|
| CDS | `jgtcli` | Market data + indicators | ~20s per pair |
| TTF | `ttfcli` | Cross-timeframe features | ~10s per pair/pattern |
| MLF | `mlfcli` | Lagged features | ~10s per pair/pattern |
| MX | `jgtmlcli` | ML training targets | ~10s per pair/pattern |

---

## Data Locations

**Lab Mode**: `/src/jgtml/data/`
```
current/
  ├─ cds/      (Market data)
  ├─ ttf/      (Features)
  └─ mlf/      (Lags)
full/
  ├─ cds/
  ├─ ttf/
  ├─ mlf/
  └─ targets/mx/  (ML targets)
```

**Production Mode**: `/workspace/data/` (same structure)

---

## Instruments Available

- `EUR/USD` - Euro/Dollar
- `AUD/CAD` - Aussie/Loonie
- `AUD/USD` - Aussie/Dollar
- `USD/CAD` - Dollar/Loonie
- `GBP/USD` - Pound/Dollar
- `XAU/USD` - Gold/Dollar
- `SPX500` - S&P 500 Index

---

## Timeframes

- `m5` - 5-minute
- `m15` - 15-minute
- `H1` - 1-hour
- `H4` - 4-hour
- `D1` - Daily
- `W1` - Weekly
- `M1` - Monthly

---

## Patterns

| Pattern | Columns | Use Case |
|---------|---------|----------|
| `mfi` | mfi_sq, mfi_green, mfi_fade, mfi_fake | Accumulation/distribution |
| `mz` | mfi_str, zcol | Alligator position |
| `zonesq` | zone_sig, mfi_sq | Volatility compression |
| `aoac` | ao, ac | Momentum analysis |

---

## Monitoring

### View Logs in Real-time
```bash
tail -f /tmp/jgtml_logs/jgtml_production_*.log
```

### See Latest Processed Files
```bash
ls -lt /src/jgtml/data/current/ttf/ | head -10
```

### Check Data Size
```bash
du -sh /src/jgtml/data/current/*
```

---

## Common Issues

**Problem**: Slow performance
**Solution**: Reduce parallel jobs with `--max-jobs 2`

**Problem**: MLF fails on H4/mz pattern
**Solution**: Non-blocking failure, ignore safely (data pipeline continues)

**Problem**: Need offline mode
**Solution**: System auto-detects closed markets, uses `-old` flag

---

## File Structure

```
/src/jgtml/
├── scripts/
│   ├── _refresh_functions.sh        (Core library)
│   ├── _REFRESH_PRODUCTION.sh       (Production workflow)
│   ├── _REFRESH_DISCOVERY.sh        (Discovery workflow)
│   └── jgtml_refresh                (Master command)
├── jgtml_refresh                    (Convenience symlink)
├── ENHANCEMENT_PLAN_COMPLETE.md     (Full documentation)
└── QUICK_REFERENCE.md               (This file)
```

---

## Typical Usage Patterns

### Daily Trading Refresh
```bash
# Each day before market open:
./jgtml_refresh production --cleanup 7
```

### Weekly Analysis
```bash
# For pattern research:
./jgtml_refresh discovery --instruments "EUR/USD" --max-jobs 1
```

### Full System Check
```bash
# Verify everything works:
./jgtml_refresh status
./jgtml_refresh production --verbose
```

---

## Environment Variables (Optional)

```bash
# Set default instruments
export INSTRUMENTS="EUR/USD,XAU/USD"

# Set default timeframes
export TIMEFRAMES="D1,H4"

# Set default patterns
export PATTERNS="mfi mz zonesq aoac"

# Set parallel job limit
export MAX_PARALLEL_JOBS="2"

# Then run:
./jgtml_refresh production
```

---

## Performance Estimates

**Production Mode** (TTF+MLF only):
- 1 instrument: 30-60 seconds
- 7 instruments: 3-5 minutes (parallel)
- Data freshness: ~400 bars

**Discovery Mode** (TTF+MLF+MX):
- 1 instrument: 5-10 minutes
- 7 instruments: 30-60 minutes (parallel)
- Data: Complete history

---

## Next Steps

1. ✓ Check current status: `./jgtml_refresh status`
2. ✓ Run production refresh: `./jgtml_refresh production`
3. ✓ Monitor progress: `tail -f /tmp/jgtml_logs/jgtml_production_*.log`
4. ✓ Start trading: Use generated TTF/MLF features

---

**See Also**: `ENHANCEMENT_PLAN_COMPLETE.md` for detailed documentation
