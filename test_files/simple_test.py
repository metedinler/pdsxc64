#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))

from opcode_manager import OpcodeManager

print("=== OpCode Manager Test ===")

try:
    manager = OpcodeManager()
    print(f"Opcodes loaded: {len(manager.opcodes)}")
    print(f"Translations loaded: {len(manager.translations)}")
    
    # Test birkaç opcode
    test_codes = [0xA9, 0x8D, 0x60]  # LDA #, STA abs, RTS
    
    for code in test_codes:
        info = manager.get_opcode_info(code)
        print(f"0x{code:02X}: {info}")
        
    # Test translations
    if 'LDA' in manager.translations:
        print("\nLDA translations:")
        for key, val in manager.translations['LDA'].items():
            print(f"  {key}: {val}")
    
    print("\nTest completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
