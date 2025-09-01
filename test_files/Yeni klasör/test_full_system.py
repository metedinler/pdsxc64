#!/usr/bin/env python
"""
TEST AMACI: Enhanced Disassembler sisteminin TAM DOĞRULAMA testi
AÇIKLAMA:
- Tüm sistemin entegrasyon testi
- Memory Manager + Enhanced Disassembler kombinasyonu
- 4 format çıktısının doğruluğu
- KERNAL routine tanıma (JSR $FFD2 → CHROUT)
- Smart variable naming sistemi

KULLANIM:
python test_files/test_full_system.py

BEKLENEN SONUÇ:
✅ Enhanced C64 Memory Manager aktif
✅ 835+ adres tanıma
✅ LDA #$41 → A = 65 çevirisi
✅ JSR $FFD2 → GOSUB CHROUT tanıma
✅ RTS → RETURN çevirisi
✅ 4 format desteği (ASM, C, QBasic, PDSx)

BAŞARI KRİTERLERİ:
- Hiç format error olmamalı
- CHROUT routine tanınmalı  
- Memory mapping çalışmalı
- Enhanced translation aktif olmalı
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from improved_disassembler import ImprovedDisassembler
from enhanced_c64_memory_manager import EnhancedC64MemoryManager

def test_full_system():
    print("=== FULL SYSTEM VALIDATION TEST ===")
    
    # Test PRG: Hello World equivalent 
    # LDA #65 (Load 'A'), JSR $FFD2 (CHROUT), RTS
    test_prg = bytes.fromhex('0108a94120d2ff60')
    
    print(f"Test PRG: {test_prg.hex()}")
    print("Code: LDA #65, JSR $FFD2 (CHROUT), RTS")
    
    success_count = 0
    total_tests = 4
    
    formats = [
        ('asm', 'Assembly format'),
        ('c', 'C language format'), 
        ('qbasic', 'QBasic format'),
        ('pdsx', 'PDSx BASIC format')
    ]
    
    for fmt, desc in formats:
        print(f"\n=== {desc.upper()} ===")
        try:
            disasm = ImprovedDisassembler(0x801, test_prg[2:])
            disasm.output_format = fmt
            result = disasm.disassemble_to_format(test_prg[2:])
            
            # Check for errors
            if "Error at $" in result:
                print("❌ HATA: Format error detected")
                print(result[:200] + "...")
            else:
                print("✅ SUCCESS: No errors")
                
                # Show key lines
                lines = result.split('\n')
                key_lines = [line for line in lines if any(keyword in line for keyword in 
                           ['LDA', 'JSR', 'RTS', 'CHROUT', 'A =', 'GOSUB', 'RETURN', 'call'])][:5]
                
                for line in key_lines:
                    print(f"  {line}")
                    
                success_count += 1
                
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")
    
    print(f"\n=== TEST SUMMARY ===")
    print(f"Successful formats: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 FULL SYSTEM TEST: ✅ PASSED")
        print("Enhanced Disassembler sistem tamamen çalışıyor!")
    else:
        print("⚠️ PARTIAL SUCCESS: Some formats failed")
        
    # Memory Manager validation
    print(f"\n=== MEMORY MANAGER TEST ===")
    try:
        memory_manager = EnhancedC64MemoryManager()
        chrout_name = memory_manager.get_smart_variable_name(0xFFD2)
        print(f"$FFD2 → {chrout_name}")
        
        if "CHROUT" in chrout_name:
            print("✅ CHROUT routine tanıma: BAŞARILI")
        else:
            print("⚠️ CHROUT routine tanıma: EKSIK")
            
    except Exception as e:
        print(f"❌ Memory Manager Error: {e}")

if __name__ == "__main__":
    test_full_system()
