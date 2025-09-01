#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Testing pdsxv12xNEW.py import...")

try:
    import sys
    sys.path.append('.')
    
    # Test import
    print("1. Importing main module...")
    from pdsxv12xNEW import pdsXInterpreter
    
    print("2. Creating interpreter instance...")
    interpreter = pdsXInterpreter()
    
    print("3. Checking for _execute_c64_gui_operations method...")
    if hasattr(interpreter, '_execute_c64_gui_operations'):
        print("   [OK] Method exists!")
    else:
        print("   [ERROR] Method NOT found!")
        print("   Available methods:", [m for m in dir(interpreter) if m.startswith('_execute')])
    
    print("4. SUCCESS: Module imported and tested successfully!")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
