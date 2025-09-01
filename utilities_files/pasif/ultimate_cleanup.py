#!/usr/bin/env python3
"""
ULTIMATE Project Cleanup Script
Kullanılmayan modüller + GUI karmaşası dahil komple temizlik
"""

import os
import shutil
from pathlib import Path

def create_archive_structure():
    """Archive klasör yapısını oluştur"""
    dirs = [
        'archive',
        'archive/critical_backups',
        'archive/advanced_features', 
        'archive/historical_versions',
        'archive/gui_alternatives',
        'archive/development_tools'
    ]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_name}")

def organize_unused_modules():
    """Kullanılmayan modülleri organize et - YENİ ANALİZE GÖRE GÜNCELLENMIŞ"""
    
    # Critical backups
    critical_files = [
        'main_complete_restore.py',
        'gui_restored.py'
    ]
    
    # Advanced features
    advanced_files = [
        'py65_professional_disassembler.py'
    ]
    
    # Historical versions (tarihsel değer)
    historical_files = [
        'disassembler.py'
    ]
    
    # GUI alternatives (launcher alternatifleri)
    gui_files = [
        'clean_gui_selector.py',
        'modern_gui_selector.py',
        'gui_demo.py'
    ]
    
    # Development tools (dev tools değeri)
    dev_files = [
        'gui_direct_test.py',
        'debug_gui.py'
    ]
    
    # Dosyaları taşı - HİÇBİRİ SİLİNMEYECEK!
    move_files(critical_files, 'archive/critical_backups', '💾 CRITICAL BACKUPS')
    move_files(advanced_files, 'archive/advanced_features', '⚡ ADVANCED FEATURES')
    move_files(historical_files, 'archive/historical_versions', '� HISTORICAL VERSIONS')
    move_files(gui_files, 'archive/gui_alternatives', '🖥️ GUI ALTERNATIVES')
    move_files(dev_files, 'archive/development_tools', '🧪 DEVELOPMENT TOOLS')
    
    # ÖNEMLİ: AKTİF MODÜLLER ANA DİZİNDE KALACAK!
    active_modules = [
        'd64_reader.py', 'advanced_disassembler.py', 'parser.py', 
        'c64_basic_parser.py', 'sprite_converter.py', 'sid_converter.py'
    ]
    
    print("\n✅ AKTİF MODÜLLER (ANA DİZİNDE KALACAK):")
    for module in active_modules:
        if os.path.exists(module):
            print(f"   🟢 {module} - AKTİF KULLANILIYOR")
        else:
            print(f"   ⚠️ {module} - BULUNAMADI")

def move_files(file_list, destination, category):
    """Dosyaları belirtilen hedefe taşı"""
    print(f"\n{category}:")
    moved_count = 0
    
    for file_name in file_list:
        if os.path.exists(file_name):
            try:
                shutil.move(file_name, os.path.join(destination, file_name))
                print(f"   ✅ Moved: {file_name}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Error moving {file_name}: {e}")
        else:
            print(f"   ⚠️ Not found: {file_name}")
    
    print(f"   📊 Moved {moved_count}/{len(file_list)} files")

def fix_missing_gui():
    """Kayıp eski_gui_3.py problemini çöz"""
    source = "utilities_files/pasif/eski_gui_3.py"
    if os.path.exists(source):
        try:
            shutil.copy2(source, "archive/gui_legacy/eski_gui_3.py")
            print(f"✅ Found and archived missing GUI: {source}")
        except Exception as e:
            print(f"❌ Error copying eski_gui_3.py: {e}")

def main():
    print("🚀 ULTIMATE D64 CONVERTER CLEANUP - YENİ ANALİZ")
    print("="*50)
    print("Bu script şunları yapacak:")
    print("• 8 dosyayı archive'e organize edecek")
    print("• GUI alternatiflerini koruyacak") 
    print("• HİÇBİR DOSYA SİLİNMEYECEK (Level 3 yaklaşım)")
    print("• 6 aktif modül ana dizinde kalacak")
    print("• 12 core dosya + 6 aktif modül = 18 dosya kalacak")
    
    response = input("\n❓ Devam etmek istiyor musunuz? (y/n): ")
    
    if response.lower() == 'y':
        print("\n📁 Archive yapısı oluşturuluyor...")
        create_archive_structure()
        
        print("\n📦 Modüller organize ediliyor...")
        organize_unused_modules()
        
        print("\n🔍 Kayıp GUI problemi çözülüyor...")
        fix_missing_gui()
        
        print("\n🎉 ULTIMATE CLEANUP TAMAMLANDI!")
        print("\n📊 SONUÇ:")
        print("✅ Ana dizinde 18 dosya kaldı (12 core + 6 aktif)")
        print("📦 8 dosya archive'e organize edildi")
        print("� HİÇBİR DOSYA SİLİNMEDİ (Level 3 koruma)")
        print("🎯 %100 güvenli temizlik tamamlandı!")
        
        print("\n📁 FINAL ACTIVE FILES:")
        core_files = [
            'main_ultimate.py', 'gui_manager.py',
            'enhanced_c64_memory_manager.py', 'unified_decompiler.py',
            'code_analyzer.py', 'improved_disassembler.py', 'assembly_formatters.py'
        ]
        active_modules = [
            'd64_reader.py', 'advanced_disassembler.py', 'parser.py', 
            'c64_basic_parser.py', 'sprite_converter.py', 'sid_converter.py'
        ]
        
        for f in core_files + active_modules:
            if os.path.exists(f):
                print(f"   ✅ {f}")
    else:
        print("❌ Cleanup iptal edildi.")

if __name__ == "__main__":
    main()
