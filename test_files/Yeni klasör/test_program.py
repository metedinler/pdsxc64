#!/usr/bin/env python3
"""
D64 Converter Test Programı
"""

import sys
import os
import traceback

def test_imports():
    """Import testleri"""
    try:
        print("1. Temel modülleri import ediliyor...")
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        import threading
        import json
        print("✓ Temel modüller başarılı")
        
        print("2. Proje modülleri import ediliyor...")
        import d64_reader
        print("✓ d64_reader başarılı")
        
        import advanced_disassembler
        print("✓ advanced_disassembler başarılı")
        
        import opcode_manager
        print("✓ opcode_manager başarılı")
        
        print("3. Ana program import ediliyor...")
        import d64_converter
        print("✓ d64_converter başarılı")
        
        return True
    except Exception as e:
        print(f"❌ Import hatası: {e}")
        traceback.print_exc()
        return False

def test_advanced_disassembler():
    """AdvancedDisassembler test"""
    try:
        print("\n4. AdvancedDisassembler test ediliyor...")
        from advanced_disassembler import AdvancedDisassembler
        
        # Test verileri
        test_data = bytes([0x00, 0x08, 0xa9, 0x01, 0x8d, 0x20, 0xd0, 0x60])  # LDA #$01, STA $D020, RTS
        
        print("   4a. Basit mod test...")
        disasm = AdvancedDisassembler(0x0800, test_data[2:], use_py65=False)
        result = disasm.disassemble()
        print(f"   ✓ Basit mod: {len(result)} satır")
        
        print("   4b. PRG data test...")
        result2 = disasm.disassemble_simple(test_data)
        print(f"   ✓ PRG data: {len(result2)} karakter")
        
        return True
    except Exception as e:
        print(f"❌ AdvancedDisassembler hatası: {e}")
        traceback.print_exc()
        return False

def test_gui():
    """GUI test"""
    try:
        print("\n5. GUI test ediliyor...")
        import tkinter as tk
        from d64_converter import D64Converter
        
        root = tk.Tk()
        root.withdraw()  # Pencereyi gösterme
        
        app = D64Converter(root)
        print("✓ GUI başarılı oluşturuldu")
        
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ GUI hatası: {e}")
        traceback.print_exc()
        return False

def main():
    """Ana test fonksiyonu"""
    print("D64 Converter Test Başlıyor...")
    print("=" * 50)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_advanced_disassembler():
        success = False
    
    if not test_gui():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Tüm testler başarılı!")
        print("Program çalıştırılabilir durumda.")
    else:
        print("❌ Bazı testler başarısız!")
        print("Hataları düzeltmek gerekiyor.")
    
    return success

if __name__ == "__main__":
    main()
