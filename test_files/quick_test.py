#!/usr/bin/env python3
"""
Test - quick illegal analyzer test
"""

import os
import sys
sys.path.insert(0, os.getcwd())

# Test PRG dosyası oluştur
os.makedirs("prg_files", exist_ok=True)

# Mixed illegal opcode program
mixed_program = [
    0x00, 0x10,  # Load address $1000
    0xA9, 0xFF,  # LDA #$FF
    0x03, 0x20,  # SLO $20 (illegal - undocumented)
    0x8D, 0x00, 0x02,  # STA $0200
    0xCB, 0x05,  # AXS #$05 (illegal - undocumented)
    0x60   # RTS
]

with open("prg_files/test_mixed.prg", "wb") as f:
    f.write(bytes(mixed_program))

print("test_mixed.prg oluşturuldu")

# Test et
from simple_analyzer import SimpleIllegalAnalyzer

analyzer = SimpleIllegalAnalyzer()
results = analyzer.analyze_prg_file("prg_files/test_mixed.prg")
analyzer.print_results(results)
