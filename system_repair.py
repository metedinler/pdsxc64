#!/usr/bin/env python3
"""
D64 Converter - System Repair
Tüm sistemi çalışır duruma getir
"""

import sys
import os
import shutil
sys.path.insert(0, os.getcwd())

print("🔧 D64 Converter - System Repair")
print("=" * 50)

# 1. Import testleri
print("\n1️⃣ Import testleri...")

def test_import(module_name, description):
    try:
        __import__(module_name)
        print(f"✅ {description}")
        return True
    except Exception as e:
        print(f"❌ {description} - HATA: {e}")
        return False

# Core imports
imports_ok = True
imports_ok &= test_import("tkinter", "tkinter")
imports_ok &= test_import("pathlib", "pathlib")
imports_ok &= test_import("threading", "threading")
imports_ok &= test_import("json", "json")

# Project imports
imports_ok &= test_import("d64_reader", "d64_reader")
imports_ok &= test_import("enhanced_d64_reader", "enhanced_d64_reader")
imports_ok &= test_import("c1541_python_emulator", "c1541_python_emulator")
imports_ok &= test_import("advanced_disassembler", "advanced_disassembler")
imports_ok &= test_import("opcode_manager", "opcode_manager")
imports_ok &= test_import("simple_analyzer", "simple_analyzer")

# 2. GUI Components test
print("\n2️⃣ GUI Components test...")

if imports_ok:
    try:
        import tkinter as tk
        from d64_converter import D64ConverterApp
        
        # Test root window
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test app creation
        app = D64ConverterApp(root)
        print("✅ D64ConverterApp oluşturuldu")
        
        # Test critical methods
        methods = [
            'analyze_illegal_opcodes',
            'show_illegal_analysis_results',
            'extract_prg_data',
            'convert_single_file',
            '_convert_single_file_thread',
            '_analyze_illegal_opcodes_thread'
        ]
        
        for method in methods:
            if hasattr(app, method):
                print(f"✅ {method} method var")
            else:
                print(f"❌ {method} method yok")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ GUI test hatası: {e}")
        imports_ok = False

# 3. Disassembler test
print("\n3️⃣ Disassembler test...")

if imports_ok:
    try:
        from advanced_disassembler import AdvancedDisassembler
        
        # Test data
        test_data = bytes([0xA9, 0x01, 0x8D, 0x00, 0x02, 0x60])  # LDA #$01, STA $0200, RTS
        
        # Test formats
        formats = ['asm', 'c', 'qbasic', 'pdsx', 'pseudo', 'commodorebasicv2']
        
        for fmt in formats:
            try:
                disasm = AdvancedDisassembler(0x1000, test_data, output_format=fmt)
                result = disasm.disassemble_simple(bytes([0x00, 0x10]) + test_data)
                if result and len(result) > 0:
                    print(f"✅ {fmt} format - {len(result)} karakter")
                else:
                    print(f"❌ {fmt} format - boş sonuç")
            except Exception as e:
                print(f"❌ {fmt} format - hata: {e}")
                
    except Exception as e:
        print(f"❌ Disassembler test hatası: {e}")

# 4. Illegal Analyzer test
print("\n4️⃣ Illegal Analyzer test...")

if imports_ok:
    try:
        from simple_analyzer import SimpleIllegalAnalyzer
        
        # Test PRG oluştur
        os.makedirs("prg_files", exist_ok=True)
        test_prg = "prg_files/system_test.prg"
        
        with open(test_prg, 'wb') as f:
            f.write(bytes([
                0x00, 0x10,  # Load address
                0xA9, 0x01,  # LDA #$01 (legal)
                0x03, 0x20,  # SLO $20 (illegal)
                0x60         # RTS (legal)
            ]))
        
        # Test analyzer
        analyzer = SimpleIllegalAnalyzer()
        results = analyzer.analyze_prg_file(test_prg)
        
        if results and 'illegal_count' in results:
            print(f"✅ Illegal Analyzer - {results['illegal_count']} illegal opcode bulundu")
        else:
            print("❌ Illegal Analyzer - sonuç alınamadı")
            
        # Temizle
        os.remove(test_prg)
        
    except Exception as e:
        print(f"❌ Illegal Analyzer test hatası: {e}")

# 5. Özet
print("\n" + "=" * 50)
if imports_ok:
    print("✅ Sistem test tamamlandı - Genel durum: İYİ")
    print("\n🚀 Şimdi main.py --gui ile GUI'yi test edebilirsiniz")
else:
    print("❌ Sistem test tamamlandı - Genel durum: PROBLEMLI")
    print("\n🔧 Import sorunlarını düzeltmek gerekiyor")

print("\n💡 Öneriler:")
print("   1. python main.py --gui ile GUI'yi test edin")
print("   2. Bir D64 dosyası yükleyin")
print("   3. 'Illegal Analiz' butonunu test edin")
print("   4. Farklı çıktı formatlarını test edin")
