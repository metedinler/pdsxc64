#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test PRG dosyası oluşturucu
Basit C64 programları oluşturur
"""

def create_basic_test_prg():
    """Basit test PRG dosyası oluştur"""
    
    # Basit bir C64 programı:
    # LDA #$01    ; A = 1
    # STA $D020   ; Border color = A  
    # LDA #$0E    ; A = 14 (light blue)
    # STA $D021   ; Background color = A
    # RTS         ; Return
    
    prg_data = bytes([
        0x00, 0x08,        # Start address: $0800
        0xA9, 0x01,        # LDA #$01
        0x8D, 0x20, 0xD0,  # STA $D020 
        0xA9, 0x0E,        # LDA #$0E
        0x8D, 0x21, 0xD0,  # STA $D021
        0x60               # RTS
    ])
    
    # Ana dizine test.prg olarak kaydet
    with open('test.prg', 'wb') as f:
        f.write(prg_data)
    
    print("✅ test.prg dosyası oluşturuldu")
    print(f"📄 Dosya boyutu: {len(prg_data)} bytes")
    print(f"🎯 Start address: $0800")
    return True

def create_illegal_opcode_test_prg():
    """Illegal opcode'lu test PRG dosyası oluştur"""
    
    # Illegal opcode içeren program
    prg_data = bytes([
        0x00, 0x10,        # Start address: $1000  
        0xA9, 0x01,        # LDA #$01
        0x0B, 0x01,        # Illegal: ANC #$01 (undocumented)
        0x8D, 0x20, 0xD0,  # STA $D020
        0x60               # RTS
    ])
    
    with open('test_illegal.prg', 'wb') as f:
        f.write(prg_data)
    
    print("✅ test_illegal.prg dosyası oluşturuldu")
    print(f"📄 Dosya boyutu: {len(prg_data)} bytes") 
    print(f"🔬 Illegal opcode: $0B (ANC)")
    return True

if __name__ == "__main__":
    print("🚀 Test PRG dosyaları oluşturuluyor...")
    create_basic_test_prg()
    create_illegal_opcode_test_prg()
    print("✅ Tüm test dosyaları hazır!")
