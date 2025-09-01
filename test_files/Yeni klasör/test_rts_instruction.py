#!/usr/bin/env python
"""
TEST AMACI: RTS (Return from Subroutine) instruction'ının düzgün çalışmasını test eder
AÇIKLAMA:
- RTS instruction format error'ını debug eder
- Sadece RTS instruction'ı test eder
- Tüm formatlarda RTS çevirisini kontrol eder
- None operand handling'ini test eder

KULLANIM:
python test_files/test_rts_instruction.py

BEKLENEN SONUÇ:
- ASM: $0801: RTS
- C: return; // Return from subroutine  
- QBasic: RETURN
- PDSx: 100 RETURN

HATA DURUMU:
- Eğer "unsupported format string passed to NoneType.__format__" hatası alırsanız
- RTS instruction'da operand None handling problemi var demektir
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from improved_disassembler import ImprovedDisassembler

def test_rts_instruction():
    # Test PRG: BASIC header + RTS instruction
    # 0108 = BASIC load address, 60 = RTS
    test_prg = bytes.fromhex('010860')
    
    print("=== TEST: RTS Instruction Debug ===")
    print(f"Test PRG: {test_prg.hex()} (BASIC header + RTS)")
    
    formats = ['asm', 'c', 'qbasic', 'pdsx']
    
    for fmt in formats:
        print(f"\n=== {fmt.upper()} FORMAT TEST ===")
        try:
            disasm = ImprovedDisassembler(0x801, test_prg[2:])  # Skip BASIC header
            disasm.output_format = fmt
            result = disasm.disassemble_to_format(test_prg[2:])
            
            print("SUCCESS:")
            lines = result.split('\n')
            for line in lines[:10]:  # First 10 lines only
                print(line)
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            print(f"TRACEBACK:\n{traceback.format_exc()}")

if __name__ == "__main__":
    test_rts_instruction()
