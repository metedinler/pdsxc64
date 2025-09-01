"""
test_prg_creator.py
Test PRG dosyaları oluşturucu
"""

import os

def create_test_prg_files():
    """Test PRG dosyaları oluştur"""
    
    # PRG files klasörünü oluştur
    os.makedirs("prg_files", exist_ok=True)
    
    # Test 1: Sadece legal opcodes
    legal_program = [
        0x00, 0x10,  # Load address $1000
        0xA9, 0x01,  # LDA #$01
        0x8D, 0x00, 0x02,  # STA $0200
        0xA2, 0x00,  # LDX #$00
        0xE8,  # INX
        0x60   # RTS
    ]
    
    with open("prg_files/test_legal.prg", "wb") as f:
        f.write(bytes(legal_program))
    
    # Test 2: Birkaç illegal opcode içeren
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
    
    # Test 3: Dangerous illegal opcodes
    dangerous_program = [
        0x00, 0x10,  # Load address $1000
        0xA9, 0x01,  # LDA #$01
        0x02,  # KIL (illegal - dangerous!)
        0x8D, 0x00, 0x02,  # STA $0200 (never reached)
        0x60   # RTS
    ]
    
    with open("prg_files/test_dangerous.prg", "wb") as f:
        f.write(bytes(dangerous_program))
    
    # Test 4: Çok fazla illegal opcode
    heavy_illegal_program = [
        0x00, 0x10,  # Load address $1000
        0xA9, 0x01,  # LDA #$01
        0x03, 0x20,  # SLO $20 (illegal)
        0x23, 0x20,  # RLA ($20,X) (illegal)
        0x43, 0x20,  # SRE ($20,X) (illegal)
        0x63, 0x20,  # RRA ($20,X) (illegal)
        0x83, 0x20,  # SAX ($20,X) (illegal)
        0xA3, 0x20,  # LAX ($20,X) (illegal)
        0xC3, 0x20,  # DCP ($20,X) (illegal)
        0xE3, 0x20,  # ISC ($20,X) (illegal)
        0x04, 0x20,  # NOP $20 (illegal)
        0x1A,  # NOP (illegal)
        0x8B, 0x05,  # XAA #$05 (illegal - highly unstable!)
        0x60   # RTS
    ]
    
    with open("prg_files/test_heavy_illegal.prg", "wb") as f:
        f.write(bytes(heavy_illegal_program))
    
    # Test 5: Çok büyük program (cycle count testi için)
    large_program = [0x00, 0x10]  # Load address
    
    # Çok sayıda instruction ekle
    for i in range(100):
        large_program.extend([0xA9, i & 0xFF])  # LDA #$xx
        large_program.extend([0x8D, 0x00, 0x02])  # STA $0200
        if i % 10 == 0:
            large_program.extend([0x03, 0x20])  # SLO $20 (illegal)
        if i % 20 == 0:
            large_program.extend([0x04, 0x20])  # NOP $20 (illegal)
    
    large_program.append(0x60)  # RTS
    
    with open("prg_files/test_large.prg", "wb") as f:
        f.write(bytes(large_program))
    
    print("Test PRG dosyaları oluşturuldu:")
    print("  prg_files/test_legal.prg - Sadece legal opcodes")
    print("  prg_files/test_mixed.prg - Birkaç illegal opcode")
    print("  prg_files/test_dangerous.prg - Dangerous illegal opcodes")
    print("  prg_files/test_heavy_illegal.prg - Çok fazla illegal opcode")
    print("  prg_files/test_large.prg - Büyük program (cycle count testi)")

if __name__ == "__main__":
    create_test_prg_files()
