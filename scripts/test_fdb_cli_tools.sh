#!/bin/bash
# test_fdb_cli_tools.sh
# Script to test FDB CLI tools using source code directly (proper development workflow)

# 🧠 Mia + 🌸 Miette: Canonical development testing pattern
# Never install the package you're developing - work with source code directly

set -e

# Ensure we're in the right directory
cd /src/jgtml

# Set up proper environment variables
export JGTPY_DATA_FULL=/src/jgtml/data/full
export JGTPY_DATA=/src/jgtml/data/current

echo "🚀 Testing FDB CLI Tools with Source Code (Proper Development Workflow)"
echo "═══════════════════════════════════════════════════════════════════════"
echo "📂 Working Directory: $(pwd)"
echo "🔮 JGTPY_DATA_FULL: $JGTPY_DATA_FULL"
echo "🌸 JGTPY_DATA: $JGTPY_DATA"
echo ""

# Test 1: FDB Pattern Intelligence CLI
echo "🧠 Test 1: FDB Pattern Intelligence CLI"
echo "─────────────────────────────────────────"
python jgtml/fdb_pattern_intelligence.py --patterns mfi --verbose | head -20
echo ""

# Test 2: FDB Signal Quality Predictor CLI  
echo "🔮 Test 2: FDB Signal Quality Predictor CLI"
echo "──────────────────────────────────────────────"
python jgtml/fdb_signal_quality_predictor.py --pattern mfi --instrument EUR-USD --timeframe D1 | head -20
echo ""

# Test 3: Help commands
echo "📖 Test 3: Help Commands"
echo "─────────────────────────"
echo "🧠 FDB Pattern Intelligence Help:"
python jgtml/fdb_pattern_intelligence.py --help | head -10
echo ""
echo "🔮 FDB Signal Quality Predictor Help:"
python jgtml/fdb_signal_quality_predictor.py --help | head -10
echo ""

echo "✅ All FDB CLI tools tested successfully!"
echo "🌸 Use 'python jgtml/[tool_name].py' for direct source code execution"
echo "🦢 Never install the package you're developing in the development environment"
