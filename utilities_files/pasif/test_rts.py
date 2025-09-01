#!/usr/bin/env python
# Test RTS instruction specifically

import sys
sys.path.append('.')
from improved_disassembler import ImprovedDisassembler

# Test PRG: LDA #$41 (A9 41), JSR $FFD2 (20 D2 FF), RTS (60)
test_prg = bytes.fromhex('a94120d2ff60')

print("=== TEST: RTS instruction ===")

disasm = ImprovedDisassembler(0x801, test_prg)
disasm.output_format = 'pdsx'

try:
    result = disasm.disassemble_to_format(test_prg)
    print("SUCCESS:")
    print(result)
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    print(f"TRACEBACK:\n{traceback.format_exc()}")
