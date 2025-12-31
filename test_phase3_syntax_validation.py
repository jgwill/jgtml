#!/usr/bin/env python3
"""
Phase 3 Syntax validation test for jgtml tracing integration
Tests that the modified files have correct Python syntax.
"""

import ast
import os

def test_python_syntax(file_path):
    """Test that a Python file has valid syntax"""
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        
        # Parse the source code
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error reading file: {e}"

def main():
    print("🔧 Testing Python syntax for modified jgtml files (Phase 3)...")
    
    # Files that were modified in Phase 3
    test_files = [
        "/src/jgtml/jgtml/ttfcli.py",
        "/src/jgtml/jgtml/mlfcli.py",
        "/src/jgtml/jgtml/fdb_scanner_2408.py"
    ]
    
    results = []
    for file_path in test_files:
        if os.path.exists(file_path):
            valid, error = test_python_syntax(file_path)
            results.append((file_path, valid, error))
            
            status = "✅ VALID" if valid else "❌ INVALID"
            print(f"{status} {os.path.basename(file_path)}")
            if error:
                print(f"  Error: {error}")
        else:
            print(f"❌ MISSING {file_path}")
            results.append((file_path, False, "File not found"))
    
    # Summary
    passed = sum(1 for _, valid, _ in results if valid)
    total = len(results)
    
    print(f"\n📊 Phase 3 syntax validation: {passed}/{total} files passed")
    
    if passed == total:
        print("🎉 All modified jgtml files have valid Python syntax!")
        return True
    else:
        print("❌ Some files have syntax errors that need fixing.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)