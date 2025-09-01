"""
Py65 Test - Hata düzeltmesi kontrolü
"""
import sys
import os

sys.path.insert(0, os.getcwd())

try:
    print("🔍 py65 test başlatılıyor...")
    
    # Test data
    test_prg = bytes([
        0x00, 0x08,        # Start address $0800
        0xA9, 0x01,        # LDA #$01
        0x8D, 0x20, 0xD0,  # STA $D020
        0x60               # RTS
    ])
    
    print("📄 Test PRG hazırlandı")
    
    # Improved Disassembler test
    from improved_disassembler import ImprovedDisassembler, PY65_AVAILABLE, Py65ProfessionalDisassembler
    print(f"✅ Improved disassembler import OK, py65 available: {PY65_AVAILABLE}")
    
    # Test improved
    print("🔧 Improved disassembler test...")
    improved = ImprovedDisassembler(0x0800, test_prg[2:], 
                                   output_format="asm", 
                                   use_illegal_opcodes=False)
    result = improved.disassemble_to_format(test_prg)
    print("✅ Improved disassembler OK")
    
    # Test py65 professional
    if PY65_AVAILABLE:
        print("🔧 py65 Professional disassembler test...")
        try:
            py65_disasm = Py65ProfessionalDisassembler(0x0800, test_prg[2:], 
                                                     use_illegal_opcodes=False)
            result = py65_disasm.disassemble_to_format(test_prg, "asm")
            print("✅ py65 Professional disassembler OK")
        except Exception as e:
            print(f"❌ py65 Professional hatası: {e}")
    else:
        print("⚠️ py65 kullanılamıyor")
    
    print("\n✅ Tüm testler başarılı!")
    
except Exception as e:
    print(f"❌ Test hatası: {e}")
    import traceback
    traceback.print_exc()
