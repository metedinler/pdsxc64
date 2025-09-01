#!/usr/bin/env python3
import sys
import os
sys.path.append('utilities_files/aktif')

from c64bas_transpiler_c_temel import C64BasicToCTranspiler

def test_transpiler():
    transpiler = C64BasicToCTranspiler()
    
    # Test basic program
    with open('simple_array_test.bas', 'r') as f:
        basic_code = f.read()
    
    print("BASIC Code:")
    print(basic_code)
    print("\n" + "="*50 + "\n")
    
    # Transpile to C
    c_code = transpiler.transpile_source(basic_code)
    
    print("Generated C Code:")
    print(c_code)
    
    # Save to file
    with open('test_output.c', 'w') as f:
        f.write(c_code)
    
    print(f"\nC code saved to test_output.c")

if __name__ == "__main__":
    test_transpiler()
