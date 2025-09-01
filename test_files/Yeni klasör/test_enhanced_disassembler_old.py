#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test için basit PRG data oluştur
test_prg = bytes([
    0x01, 0x08,    # Start address $0801
    0xA9, 0x41,    # LDA #$41 (Load 'A')
    0x20, 0xD2, 0xFF,  # JSR $FFD2 (CHROUT)
    0x60           # RTS
])

print("=== TEST: Enhanced Disassembler ===")
print(f"Test PRG: {test_prg.hex()}")
print()

try:
    from improved_disassembler import ImprovedDisassembler
    
    # Test different formats
    formats = ['asm', 'c', 'qbasic', 'pdsx']
    
    for fmt in formats:
        print(f"=== {fmt.upper()} FORMAT ===")
        disasm = ImprovedDisassembler(0x0801, test_prg[2:], fmt)
        result = disasm.disassemble_to_format(test_prg)
        print(result[:500] + "..." if len(result) > 500 else result)
        print()

except Exception as e:
    print(f"HATA: {e}")
    import traceback
    traceback.print_exc()
