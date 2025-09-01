#!/usr/bin/env python
"""
TEST AMACI: Enhanced Disassembler'ın tüm formatlarda çalışmasını test eder
AÇIKLAMA: 
- LDA #$41 (immediate load) testi
- JSR $FFD2 (KERNAL CHROUT call) testi  
- RTS (return from subroutine) testi
- 4 format desteği: ASM, C, QBasic, PDSx

KULLANIM:
python test_files/test_enhanced_disassembler.py

BEKLENEN SONUÇ:
- ASM: $0801: LDA #$41, $0803: JSR $FFD2, $0806: RTS
- C: a = 65; putchar(a); return;
- QBasic: A = 65, GOSUB CHROUT, RETURN
- PDSx: 100 A = 65, 110 GOSUB CHROUT, 120 RETURN
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from improved_disassembler import ImprovedDisassembler

def test_enhanced_disassembler():
    # Test PRG: LDA #$41 (A9 41), JSR $FFD2 (20 D2 FF), RTS (60)
    # Hex string: 0108a94120d2ff60 (with BASIC start header 0108)
    test_prg = bytes.fromhex('0108a94120d2ff60')
    
    print("=== TEST: Enhanced Disassembler ===")
    print(f"Test PRG: {test_prg.hex()}")
    
    formats = ['asm', 'c', 'qbasic', 'pdsx']
    
    for fmt in formats:
        print(f"\n=== {fmt.upper()} FORMAT ===")
        try:
            disasm = ImprovedDisassembler(0x801, test_prg[2:])  # Skip BASIC header
            disasm.output_format = fmt
            result = disasm.disassemble_to_format(test_prg[2:])
            
            # Show limited output to avoid clutter
            lines = result.split('\n')
            for line in lines[:20]:  # First 20 lines only
                print(line)
            if len(lines) > 20:
                print("...")
                
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            print(f"TRACEBACK:\n{traceback.format_exc()}")

if __name__ == "__main__":
    test_enhanced_disassembler()
