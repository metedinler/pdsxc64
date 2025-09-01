#!/usr/bin/env python3
"""
GUI Temizlik Scripti
Çoklu GUI karmaşasını çözer
"""

import os
import shutil

def cleanup_gui_chaos():
    print("🚀 GUI CHAOS CLEANUP BAŞLATILIYOR...")
    
    # Ana GUI (korunacak)
    keep_guis = ['gui_manager.py']
    
    # Archive edilecek GUI'ler
    archive_guis = [
        'gui_restored.py',
        'clean_gui_selector.py', 
        'modern_gui_selector.py',
        'gui_demo.py',
        'gui_direct_test.py',
        'debug_gui.py'
    ]
    
    # Archive klasörü oluştur
    archive_dir = 'archive/gui_legacy'
    os.makedirs(archive_dir, exist_ok=True)
    
    # GUI'leri archive'e taşı
    for gui_file in archive_guis:
        if os.path.exists(gui_file):
            try:
                shutil.move(gui_file, os.path.join(archive_dir, gui_file))
                print(f"✅ Archived: {gui_file}")
            except Exception as e:
                print(f"❌ Error archiving {gui_file}: {e}")
    
    print("\n🎉 GUI CLEANUP TAMAMLANDI!")
    print("📁 Ana dizinde sadece gui_manager.py kaldı")
    print("📦 Diğer GUI'ler archive/gui_legacy/ klasöründe")

if __name__ == "__main__":
    cleanup_gui_chaos()
