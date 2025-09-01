#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))

from advanced_disassembler import AdvancedDisassembler

print("=== Advanced Disassembler Test ===")

# Test verisi: LDA #$01, STA $D020, RTS
test_data = bytes([0xA9, 0x01,  # LDA #$01
                   0x8D, 0x20, 0xD0,  # STA $D020
                   0x60])  # RTS

formats = ['asm', 'c', 'qbasic', 'pdsx', 'commodorebasicv2', 'pseudo']

for fmt in formats:
    print(f"\n=== {fmt.upper()} FORMAT ===")
    try:
        disasm = AdvancedDisassembler(0x0800, test_data, output_format=fmt)
        result = disasm.disassemble()
        for line in result:
            print(line)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
