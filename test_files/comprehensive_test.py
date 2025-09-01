#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from advanced_disassembler import AdvancedDisassembler

# Test PRG verisi
prg_data = bytes([
    0x00, 0x08,        # Start address: $0800
    0xA9, 0x01,        # LDA #$01
    0x8D, 0x20, 0xD0,  # STA $D020
    0xA9, 0x0E,        # LDA #$0E  
    0x8D, 0x21, 0xD0,  # STA $D021
    0x60               # RTS
])

formats = ['asm', 'c', 'qbasic', 'pdsx', 'commodorebasicv2', 'pseudo']

for fmt in formats:
    print(f"\n=== {fmt.upper()} FORMAT ===")
    disasm = AdvancedDisassembler(0x0800, prg_data[2:], output_format=fmt)
    result = disasm.disassemble()
    for line in result:
        print(line)
