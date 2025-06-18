#!/usr/bin/env python3
"""
🧠 JGT Natural Language Observation Processor
Integrates natural language market observations with automated trading system

This module processes natural language observations about market conditions
and converts them into actionable trading specifications and automated analysis.

Usage:
    python observation_processor.py --observation "Monthly pullback due, Daily Alligator closing"
    echo "EUR-USD showing H4 resistance, expect pullback" | python observation_processor.py --stdin
"""

import sys
import json
import argparse
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

# Add path for jgtagentic imports
sys.path.insert(0, '../jgtagentic/jgtagentic')

try:
    from jgtagentic.intent_spec import IntentSpecParser
except ImportError:
    print("⚠️  Warning: Intent specification parser not available")
    IntentSpecParser = None

def log_observation(observation: str, spec: Dict, results: Dict = None):
    """Log observation and results to structured format"""
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "observation": observation,
        "intent_specification": spec,
        "analysis_results": results,
        "processed_by": "JGT Observation Processor v1.0"
    }
    
    # Create logs directory if it doesn't exist
    subprocess.run(["mkdir", "-p", "logs"], check=False)
    
    # Save to JSONL format for easy processing
    log_file = f"logs/market_observations_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    print(f"📝 Observation logged to: {log_file}")

def execute_automated_analysis(instruments: List[str], quality_threshold: float = 8.0) -> Dict:
    """Execute automated FDB trading analysis for given instruments"""
    
    print(f"🚀 Executing automated analysis for: {', '.join(instruments)}")
    
    try:
        # Run enhanced trading CLI
        cmd = [
            "enhancedtradingcli", "auto",
            "-i", ",".join(instruments),
            "--demo",
            "--quality-threshold", str(quality_threshold)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        return {
            "success": True,
            "output": result.stdout,
            "instruments_analyzed": instruments,
            "quality_threshold": quality_threshold
        }
        
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": str(e),
            "output": e.stdout if e.stdout else "",
            "stderr": e.stderr if e.stderr else ""
        }

def generate_analysis_charts(instruments: List[str], timeframes: List[str]) -> Dict:
    """Generate comprehensive chart analysis for given instruments and timeframes"""
    
    print(f"📊 Generating charts for {len(instruments)} instruments across {len(timeframes)} timeframes")
    
    results = {}
    
    for instrument in instruments:
        instrument_results = {}
        
        for tf in timeframes:
            try:
                # Generate chart
                cmd = [
                    "jgtads", "-i", instrument, "-t", tf,
                    "--save_figure", "charts/",
                    "--save_figure_as_timeframe"
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                instrument_results[tf] = {
                    "success": True,
                    "chart_path": f"charts/{tf}.png"
                }
                
                print(f"  ✅ {instrument} {tf} chart generated")
                
            except subprocess.CalledProcessError as e:
                instrument_results[tf] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"  ❌ {instrument} {tf} chart failed: {e}")
        
        results[instrument] = instrument_results
    
    return results

def process_market_observation(observation: str) -> Dict:
    """Main function to process natural language market observation"""
    
    print(f"🧠 Processing market observation...")
    print(f"📖 Observation: {observation}")
    
    if not IntentSpecParser:
        print("⚠️  Intent specification parser not available, using fallback processing")
        
        # Fallback: Extract common instruments and timeframes
        spec = {
            "strategy_intent": f"Analysis based on: {observation}",
            "instruments": ["EUR-USD", "GBP-USD", "XAU-USD"],  # Default instruments
            "timeframes": ["H4", "H1", "m15"],  # Default timeframes
            "observation_source": observation,
            "processing_mode": "fallback"
        }
    else:
        # Use full intent specification parser
        parser = IntentSpecParser()
        spec = parser.create_from_observation(observation)
        spec["processing_mode"] = "full_intent_spec"
    
    print(f"⚙️  Generated specification:")
    print(f"    Strategy: {spec.get('strategy_intent', 'N/A')}")
    print(f"    Instruments: {spec.get('instruments', [])}")
    print(f"    Timeframes: {spec.get('timeframes', [])}")
    
    # Execute automated analysis
    analysis_results = execute_automated_analysis(
        spec.get("instruments", ["EUR-USD"]),
        quality_threshold=8.0
    )
    
    # Generate charts for visual analysis
    chart_results = generate_analysis_charts(
        spec.get("instruments", ["EUR-USD"]),
        spec.get("timeframes", ["H4", "H1"])
    )
    
    # Compile complete results
    complete_results = {
        "observation": observation,
        "intent_specification": spec,
        "automated_analysis": analysis_results,
        "chart_generation": chart_results,
        "processing_timestamp": datetime.now().isoformat()
    }
    
    # Log the complete observation and results
    log_observation(observation, spec, complete_results)
    
    return complete_results

def main():
    parser = argparse.ArgumentParser(description="Process natural language market observations")
    parser.add_argument("--observation", "-o", help="Market observation text")
    parser.add_argument("--stdin", action="store_true", help="Read observation from stdin")
    parser.add_argument("--instruments", "-i", help="Comma-separated instruments (overrides spec)")
    parser.add_argument("--quality-threshold", "-q", type=float, default=8.0, help="Quality threshold for automated analysis")
    
    args = parser.parse_args()
    
    # Get observation text
    if args.stdin:
        observation = sys.stdin.read().strip()
    elif args.observation:
        observation = args.observation
    else:
        print("❌ No observation provided. Use --observation or --stdin")
        return 1
    
    if not observation:
        print("❌ Empty observation provided")
        return 1
    
    try:
        # Process the observation
        results = process_market_observation(observation)
        
        # Print summary
        print(f"\n🎯 OBSERVATION PROCESSING COMPLETE")
        print(f"📊 Analysis Status: {'✅ Success' if results['automated_analysis']['success'] else '❌ Failed'}")
        print(f"📈 Charts Generated: {sum(1 for inst in results['chart_generation'].values() for tf in inst.values() if tf.get('success', False))} charts")
        print(f"🕒 Processing Time: {results['processing_timestamp']}")
        
        # If automated analysis was successful, show key info
        if results['automated_analysis']['success']:
            print(f"\n📋 AUTOMATED ANALYSIS OUTPUT:")
            print(results['automated_analysis']['output'])
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing observation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 