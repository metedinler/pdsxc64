#!/usr/bin/env python3

from disassembler import Disassembler

# Basit test kodu
test_code = [0xA9, 0x00, 0x85, 0x02, 0x60]  # LDA #$00, STA $02, RTS

try:
    disasm = Disassembler(0xC000, test_code)
    print("Test disassembly:")
    for line in disasm.disassemble():
        print(line)
except Exception as e:
    print(f"Hata: {e}")
    import traceback
    traceback.print_exc()
