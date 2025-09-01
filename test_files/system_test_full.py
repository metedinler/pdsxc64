#!/usr/bin/env python3
"""
D64 Converter - Test Script
Tüm sistem fonksiyonlarını test et
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_imports():
    """Import testleri"""
    print("🔍 Import testleri başlatılıyor...")
    
    try:
        from d64_reader import read_image, read_directory
        print("✅ d64_reader - OK")
    except Exception as e:
        print(f"❌ d64_reader - HATA: {e}")
    
    try:
        from advanced_disassembler import AdvancedDisassembler
        print("✅ advanced_disassembler - OK")
    except Exception as e:
        print(f"❌ advanced_disassembler - HATA: {e}")
    
    try:
        from simple_analyzer import SimpleIllegalAnalyzer
        print("✅ simple_analyzer - OK")
    except Exception as e:
        print(f"❌ simple_analyzer - HATA: {e}")
    
    try:
        from opcode_manager import OpcodeManager
        print("✅ opcode_manager - OK")
    except Exception as e:
        print(f"❌ opcode_manager - HATA: {e}")
    
    try:
        import py65
        print("✅ py65 - OK")
    except Exception as e:
        print(f"❌ py65 - HATA: {e}")

def test_disassembler():
    """Disassembler testleri"""
    print("\n🔍 Disassembler testleri başlatılıyor...")
    
    # Test data
    test_data = bytes([
        0x01, 0x08,  # Load address
        0xA9, 0x01,  # LDA #$01
        0x8D, 0x00, 0x02,  # STA $0200
        0xA2, 0x00,  # LDX #$00
        0xE8,  # INX
        0x60   # RTS
    ])
    
    try:
        from advanced_disassembler import AdvancedDisassembler
        
        # Test 1: Normal disassembly
        disasm = AdvancedDisassembler(0x0801, test_data[2:], use_py65=False, output_format='asm')
        result = disasm.disassemble_simple(test_data)
        print(f"✅ Normal disassembly - {len(result)} karakter")
        print(f"   İlk 100 karakter: {result[:100]}")
        
        # Test 2: C format
        disasm_c = AdvancedDisassembler(0x0801, test_data[2:], use_py65=False, output_format='c')
        result_c = disasm_c.disassemble_simple(test_data)
        print(f"✅ C format - {len(result_c)} karakter")
        print(f"   İlk 100 karakter: {result_c[:100]}")
        
        # Test 3: QBasic format
        disasm_qb = AdvancedDisassembler(0x0801, test_data[2:], use_py65=False, output_format='qbasic')
        result_qb = disasm_qb.disassemble_simple(test_data)
        print(f"✅ QBasic format - {len(result_qb)} karakter")
        print(f"   İlk 100 karakter: {result_qb[:100]}")
        
    except Exception as e:
        print(f"❌ Disassembler testleri - HATA: {e}")
        import traceback
        traceback.print_exc()

def test_illegal_analyzer():
    """Illegal opcode analyzer testleri"""
    print("\n🔍 Illegal opcode analyzer testleri başlatılıyor...")
    
    try:
        from simple_analyzer import SimpleIllegalAnalyzer
        
        # Test PRG dosyası oluştur
        test_prg = "test_illegal.prg"
        with open(test_prg, 'wb') as f:
            f.write(bytes([
                0x00, 0x10,  # Load address
                0xA9, 0x01,  # LDA #$01
                0x03, 0x20,  # SLO $20 (illegal)
                0x60   # RTS
            ]))
        
        # Analiz et
        analyzer = SimpleIllegalAnalyzer()
        results = analyzer.analyze_prg_file(test_prg)
        
        print(f"✅ Illegal analyzer - {results['illegal_count']} illegal opcode bulundu")
        
        # Temizle
        os.remove(test_prg)
        
    except Exception as e:
        print(f"❌ Illegal analyzer testleri - HATA: {e}")
        import traceback
        traceback.print_exc()

def test_gui_components():
    """GUI component testleri"""
    print("\n🔍 GUI component testleri başlatılıyor...")
    
    try:
        import tkinter as tk
        from d64_converter import D64ConverterApp
        
        # Test root window
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test app creation
        app = D64ConverterApp(root)
        print("✅ GUI App - OK")
        
        # Test illegal analyzer method
        if hasattr(app, 'analyze_illegal_opcodes'):
            print("✅ analyze_illegal_opcodes method - OK")
        else:
            print("❌ analyze_illegal_opcodes method - MISSING")
        
        # Test show_illegal_analysis_results method
        if hasattr(app, 'show_illegal_analysis_results'):
            print("✅ show_illegal_analysis_results method - OK")
        else:
            print("❌ show_illegal_analysis_results method - MISSING")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ GUI component testleri - HATA: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Ana test fonksiyonu"""
    print("🚀 D64 Converter - Sistem Testleri")
    print("=" * 50)
    
    test_imports()
    test_disassembler()
    test_illegal_analyzer()
    test_gui_components()
    
    print("\n" + "=" * 50)
    print("✅ Testler tamamlandı!")

if __name__ == "__main__":
    main()
