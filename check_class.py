#!/usr/bin/env python3

print("Direct class check...")

try:
    from pdsxv12xNEW import pdsXInterpreter
    
    print("Class loaded, checking methods:")
    methods = [m for m in dir(pdsXInterpreter) if m.startswith('_execute')]
    print("Found methods:", len(methods))
    
    has_c64 = '_execute_c64_gui_operations' in methods
    print("Has C64 method:", has_c64)
    
    if not has_c64:
        print("Missing C64 method!")
        print("Available execute methods:")
        for m in methods:
            print(f"  - {m}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
