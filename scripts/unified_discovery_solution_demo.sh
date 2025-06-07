#!/bin/bash
# unified_discovery_solution_demo.sh
# Demonstrates the Unified Discovery Dataset Generator for ML pattern analysis

# Set environment variables
export JGTPY_DATA_FULL=${JGTPY_DATA_FULL:-"/var/lib/jgt/full/data"}

# Display header
echo "🌸🔮🧠 JGTML Unified Discovery Dataset Generator Demo"
echo "======================================================"
echo "This script demonstrates how to create unified datasets that preserve"
echo "TTF pattern features while including MX profitability targets."
echo ""

# Check if Python and required modules are available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3."
    exit 1
fi

# Create a simple demo dataset
echo "🚀 Creating a demo unified discovery dataset..."
echo ""

# Run the unified discovery dataset generator with a single instrument/timeframe/pattern
python3 -m jgtml.unified_discovery_dataset_generator \
    --instruments SPX500 \
    --timeframes D1 \
    --patterns mfi \
    --output-namespace discovery_demo

echo ""
echo "📊 Dataset Analysis"
echo "=================="

# Check if the dataset was created
DEMO_DATASET="${JGTPY_DATA_FULL}/discovery_demo/SPX500_D1_mfi_unified_discovery.csv"
if [ -f "$DEMO_DATASET" ]; then
    echo "✅ Demo dataset created successfully!"
    echo "📁 Location: $DEMO_DATASET"
    
    # Count rows and columns
    ROWS=$(wc -l < "$DEMO_DATASET")
    ROWS=$((ROWS - 1))  # Subtract header row
    COLS=$(head -n 1 "$DEMO_DATASET" | tr ',' '\n' | wc -l)
    
    echo "📈 Dataset contains $ROWS rows and $COLS columns"
    
    # Show sample of columns (first 10)
    echo ""
    echo "🔍 Sample columns (first 10):"
    head -n 1 "$DEMO_DATASET" | tr ',' '\n' | head -10 | sed 's/^/  - /'
    
    echo ""
    echo "🎯 Next steps:"
    echo "  1. Use this unified dataset for ML pattern discovery"
    echo "  2. Train models that leverage both TTF features and MX targets"
    echo "  3. Discover profitable patterns that were previously hidden"
    echo ""
    echo "✨ For more options, run: python3 -m jgtml.unified_discovery_dataset_generator --help"
else
    echo "❌ Demo dataset creation failed. Please check error messages above."
fi

echo ""
echo "🌟 Demo complete!"