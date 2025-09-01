#!/usr/bin/env python3
"""
D64 Converter - PyGubu Entegrasyon Test
GUI Manager'ın PyGubu entegrasyonunu test eder
"""

import sys
import os
from pathlib import Path

# Mevcut dizini Python path'ine ekle
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_pygubu_integration():
    """PyGubu entegrasyonunu test et"""
    print("🚀 D64 Converter PyGubu Integration Test")
    print("=" * 50)
    
    try:
        # GUI Manager'ı import et
        print("📦 Importing GUI Manager...")
        from gui_manager import D64ConverterGUI
        
        print("🎨 Creating GUI with PyGubu integration...")
        import tkinter as tk
        
        # Root pencere oluştur
        root = tk.Tk()
        root.withdraw()  # Ana root'u gizle
        
        # GUI'yi oluştur
        gui = D64ConverterGUI(root)
        
        if gui.pygubu_enabled:
            print("✅ PyGubu integration successful!")
            print(f"📊 PyGubu widgets loaded: {len(gui.pygubu_widgets)}")
            
            for widget_name in gui.pygubu_widgets:
                print(f"  • {widget_name}")
            
            # GUI'yi göster
            if hasattr(gui, 'pygubu_main_window'):
                gui.pygubu_main_window.deiconify()
                
                # Pencere başlığını güncelle
                gui.pygubu_main_window.title("D64 Converter - PyGubu Integration Test")
                
                print("\n💡 PyGubu GUI açıldı! Test etmek için:")
                print("   1. Dosya açma butonunu deneyin")
                print("   2. Disassemble butonunu test edin") 
                print("   3. Transpile butonunu deneyin")
                print("   4. Pencereyi kapatarak çıkın")
                
                # Event loop'u başlat
                root.mainloop()
                
            else:
                print("❌ PyGubu main window not found")
                
        else:
            print("⚠️ PyGubu integration disabled, using traditional GUI")
            
            # Geleneksel GUI'yi göster
            if hasattr(gui, 'root'):
                gui.root.deiconify()
                print("💡 Traditional GUI açıldı!")
                root.mainloop()
        
        print("\n🎉 Test tamamlandı!")
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()

def test_ui_file():
    """UI dosyasını kontrol et"""
    print("\n🔍 UI File Check:")
    print("-" * 30)
    
    ui_file = current_dir / "gui_designs" / "d64_converter_main.ui"
    
    if ui_file.exists():
        print(f"✅ UI file found: {ui_file}")
        
        with open(ui_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"📄 File size: {len(content)} characters")
            
            # Widget sayısını kontrol et
            widget_count = content.count('<object class=')
            print(f"🧩 Widget count: {widget_count}")
            
    else:
        print(f"❌ UI file not found: {ui_file}")

if __name__ == "__main__":
    test_ui_file()
    test_pygubu_integration()
