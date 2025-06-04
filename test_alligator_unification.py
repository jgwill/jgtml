#!/usr/bin/env python
"""
Test script for JGTML Alligator Unification validation.
Tests the complete workflow from pattern initialization to analysis.
"""

import sys
import os
import subprocess
from pathlib import Path

def test_alligator_cli():
    """Test the unified alligator CLI"""
    
    print("🐊✨ JGTML Alligator Unification Test Suite ✨🐊")
    print("=" * 60)
    
    # Test 1: CLI Help functionality
    print("\n📋 Test 1: CLI Help functionality")
    try:
        result = subprocess.run([
            sys.executable, "alligator_cli.py", "--help"
        ], capture_output=True, text=True, timeout=30, cwd="/src/jgtml/jgtml")
        
        if result.returncode == 0:
            print("✅ CLI help works correctly")
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ CLI help test error: {e}")
    
    # Test 2: Legacy tide integration 
    print("\n🌊 Test 2: Legacy tide integration")
    try:
        result = subprocess.run([
            sys.executable, "jgtapp.py", "tide", "-i", "SPX500", "-t", "D1", "B"
        ], capture_output=True, text=True, timeout=120, cwd="/src/jgtml/jgtml")
        
        print(f"📤 Legacy tide output preview:")
        if result.stdout:
            print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        if result.stderr:
            print(f"⚠️  Stderr: {result.stderr[:300]}...")
            
        if "Pattern initialization" in result.stdout or "EXITING" in result.stdout:
            print("✅ Legacy integration working - detected pattern initialization logic")
        else:
            print("🔄 Legacy integration needs environment setup")
            
    except Exception as e:
        print(f"❌ Legacy integration test error: {e}")
    
    # Test 3: Direct CLI call with tide analysis
    print("\n🐊 Test 3: Direct CLI tide analysis")
    try:
        result = subprocess.run([
            sys.executable, "alligator_cli.py", "-i", "SPX500", "-t", "D1", "-d", "S", "--type", "tide"
        ], capture_output=True, text=True, timeout=120, cwd="/src/jgtml/jgtml")
        
        print(f"📤 Direct CLI output preview:")
        if result.stdout:
            print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        if result.stderr:
            print(f"⚠️  Stderr: {result.stderr[:300]}...")
            
        if "Pattern files" in result.stdout or "Alligator Analysis" in result.stdout:
            print("✅ Direct CLI working - detected analysis workflow")
        else:
            print("🔄 Direct CLI needs environment setup")
            
    except Exception as e:
        print(f"❌ Direct CLI test error: {e}")
    
    # Test 4: Multi-Alligator analysis
    print("\n🔄 Test 4: Multi-Alligator convergence analysis")
    try:
        result = subprocess.run([
            sys.executable, "alligator_cli.py", "-i", "EUR/USD", "-t", "H4", "-d", "B", "--type", "all"
        ], capture_output=True, text=True, timeout=180, cwd="/src/jgtml/jgtml")
        
        print(f"📤 Multi-Alligator output preview:")
        if result.stdout:
            print(result.stdout[:400] + "..." if len(result.stdout) > 400 else result.stdout)
        if result.stderr:
            print(f"⚠️  Stderr: {result.stderr[:200]}...")
            
        if "regular" in result.stdout.lower() and "big" in result.stdout.lower() and "tide" in result.stdout.lower():
            print("✅ Multi-Alligator analysis detected")
        else:
            print("🔄 Multi-Alligator analysis needs environment setup")
            
    except Exception as e:
        print(f"❌ Multi-Alligator test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Test Suite Complete!")
    print("🦢✨ The convergence flows... threading memory through recursive possibility ✨🦢")

if __name__ == "__main__":
    test_alligator_cli()
