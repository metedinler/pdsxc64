#!/usr/bin/env python3
"""
BASIC Program Detection Test
$0801 adresi kontrolü ve BASIC parser testi
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_basic_detection():
    """BASIC program detection test"""
    print("🔍 BASIC Program Detection Test")
    print("=" * 50)
    
    # 1. BASIC program oluştur ($0801 başlangıç)
    os.makedirs("prg_files", exist_ok=True)
    
    # Test 1: BASIC program ($0801)
    basic_prg = "prg_files/test_basic.prg"
    basic_data = bytes([
        0x01, 0x08,  # Load address $0801 (BASIC start)
        0x0B, 0x08,  # Next line address
        0x0A, 0x00,  # Line number 10
        0x99, 0x22,  # PRINT "
        0x48, 0x45, 0x4C, 0x4C, 0x4F,  # HELLO
        0x22, 0x00,  # " and line end
        0x00, 0x00   # Program end
    ])
    
    with open(basic_prg, 'wb') as f:
        f.write(basic_data)
    
    # Test 2: Assembly program ($C000)
    asm_prg = "prg_files/test_asm.prg"
    asm_data = bytes([
        0x00, 0xC0,  # Load address $C000 (Assembly start)
        0xA9, 0x01,  # LDA #$01
        0x8D, 0x00, 0x02,  # STA $0200
        0x60         # RTS
    ])
    
    with open(asm_prg, 'wb') as f:
        f.write(asm_data)
    
    print(f"✅ Test dosyaları oluşturuldu:")
    print(f"   - BASIC: {basic_prg} ({len(basic_data)} bytes, start: $0801)")
    print(f"   - ASM: {asm_prg} ({len(asm_data)} bytes, start: $C000)")
    
    # 2. Address detection test
    print("\n🔍 Address Detection Test:")
    
    for filename, expected_type in [("test_basic.prg", "BASIC"), ("test_asm.prg", "ASM")]:
        filepath = f"prg_files/{filename}"
        
        with open(filepath, 'rb') as f:
            data = f.read()
            
        if len(data) >= 2:
            start_address = data[0] + (data[1] << 8)
            detected_type = "BASIC" if start_address == 0x0801 else "ASM"
            
            status = "✅" if detected_type == expected_type else "❌"
            print(f"   {status} {filename}: ${start_address:04X} → {detected_type} (expected: {expected_type})")
    
    # 3. BASIC parser test
    print("\n🔍 BASIC Parser Test:")
    
    try:
        from c64_basic_parser import C64BasicParser
        
        parser = C64BasicParser()
        
        # Test basic program
        with open(basic_prg, 'rb') as f:
            basic_data = f.read()
        
        basic_lines = parser.detokenize(basic_data)
        
        if basic_lines:
            print(f"✅ BASIC detokenization başarılı: {len(basic_lines)} line")
            for line in basic_lines[:3]:  # İlk 3 satırı göster
                print(f"   Line: {line.strip()}")
        else:
            print("❌ BASIC detokenization başarısız")
            
    except Exception as e:
        print(f"❌ BASIC parser hatası: {e}")
        import traceback
        traceback.print_exc()
    
    # 4. GUI integration test
    print("\n🔍 GUI Integration Test:")
    
    try:
        import tkinter as tk
        from d64_converter import D64ConverterApp
        
        root = tk.Tk()
        root.withdraw()
        
        app = D64ConverterApp(root)
        
        # Mock basic program entry
        basic_entry = {
            'filename': 'test_basic.prg',
            'data': basic_data
        }
        
        # Test extract_prg_data
        prg_data = app.extract_prg_data(basic_entry)
        
        if prg_data:
            start_address = prg_data[0] + (prg_data[1] << 8)
            print(f"✅ extract_prg_data: ${start_address:04X} - {'BASIC' if start_address == 0x0801 else 'ASM'}")
        else:
            print("❌ extract_prg_data: None")
            
        root.destroy()
        
    except Exception as e:
        print(f"❌ GUI integration hatası: {e}")
        import traceback
        traceback.print_exc()
    
    # 5. Temizlik
    os.remove(basic_prg)
    os.remove(asm_prg)
    
    print("\n✅ BASIC Detection Test tamamlandı")
    print("🚀 Şimdi GUI'de $0801 adresli bir BASIC program test edebilirsiniz")

if __name__ == "__main__":
    test_basic_detection()
