#!/usr/bin/env python3
"""
JGTML ML Integration Example

This script demonstrates how to integrate the new ML baseline classifier
with existing JGTML tools for enhanced trading decisions.

Usage:
    python examples/ml_integration_demo.py
"""

import sys
from pathlib import Path

# Add jgtml to path for import
sys.path.insert(0, str(Path(__file__).parent.parent))

from jgtml.experiments.baseline_classifier import JGTMLBaseline

def demo_ml_enhanced_trading():
    """
    Demonstrate ML-enhanced trading decision making.
    
    This shows how the ML classifier can replace hardcoded quality scores
    in existing JGTML tools.
    """
    print("🚀 JGTML ML Integration Demo")
    print("=" * 50)
    
    # Initialize ML classifier
    classifier = JGTMLBaseline()
    
    # Test instruments that might be in production
    test_cases = [
        ("EUR/USD", "H4"),
        ("AUD/CAD", "H4"), 
        ("XAU/USD", "D1"),
        ("GBP/USD", "H1")
    ]
    
    for instrument, timeframe in test_cases:
        print(f"\n📊 Testing {instrument} {timeframe}")
        
        try:
            # Train model (using demo data for this example)
            print("   🔄 Training ML model...")
            metrics = classifier.train(instrument, timeframe, use_demo=True)
            
            # Make prediction
            print("   🎯 Making prediction...")
            prediction = classifier.predict(instrument, timeframe, use_demo=True)
            
            # Enhanced decision logic (replaces hardcoded quality scores)
            signal = prediction['prediction']
            confidence = prediction['confidence']
            
            # Traditional JGTML might use hardcoded thresholds
            # New ML-driven approach uses learned patterns
            if confidence > 0.8:
                decision_quality = "HIGH"
                action = "EXECUTE TRADE" if signal == 1 else "AVOID TRADE"
            elif confidence > 0.6:
                decision_quality = "MEDIUM" 
                action = "CONSIDER TRADE" if signal == 1 else "WAIT"
            else:
                decision_quality = "LOW"
                action = "NO ACTION"
            
            print(f"   ✅ Accuracy: {metrics['accuracy']:.3f}")
            print(f"   📈 Signal: {signal} ({'BUY' if signal == 1 else 'HOLD/SELL'})")
            print(f"   🎲 Confidence: {confidence:.3f}")
            print(f"   ⭐ Quality: {decision_quality}")
            print(f"   🎯 Action: {action}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo complete!")
    print("\n💡 Integration Points:")
    print("   • Replace hardcoded quality scores in fdb_signal_quality_predictor.py")
    print("   • Enhance enhanced_fdb_scanner_with_illusion_detection.py")
    print("   • Integrate with enhanced_trading_cli.py decisions")
    print("   • Use in automated_fdb_trading_system.py")


def show_integration_benefits():
    """Show the benefits of ML integration vs rule-based approaches."""
    print("\n🔍 ML vs Rule-Based Comparison:")
    print("-" * 40)
    
    comparison = {
        "Data Adaptation": {
            "Rule-based": "Fixed thresholds, manual updates",
            "ML-driven": "Learns from historical patterns automatically"
        },
        "Market Changes": {
            "Rule-based": "Requires manual recalibration", 
            "ML-driven": "Adapts through retraining on new data"
        },
        "Multi-timeframe": {
            "Rule-based": "Simple signal aggregation",
            "ML-driven": "Complex pattern recognition across timeframes"
        },
        "Confidence Estimation": {
            "Rule-based": "Binary or simple scoring",
            "ML-driven": "Probabilistic confidence measures"
        },
        "Feature Interactions": {
            "Rule-based": "Limited to predefined combinations",
            "ML-driven": "Discovers complex feature relationships"
        }
    }
    
    for aspect, approaches in comparison.items():
        print(f"\n📋 {aspect}:")
        print(f"   🔧 Rule-based: {approaches['Rule-based']}")
        print(f"   🤖 ML-driven: {approaches['ML-driven']}")


if __name__ == "__main__":
    demo_ml_enhanced_trading()
    show_integration_benefits()
    
    print("\n🚀 Next Steps:")
    print("   1. Integrate ML predictions into existing JGTML CLI tools")
    print("   2. Replace hardcoded quality scores with ML confidence")
    print("   3. Create A/B testing framework (ML vs rules)")
    print("   4. Add continuous model retraining")
    print("   5. Implement ensemble methods for better accuracy")