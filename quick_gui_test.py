#!/usr/bin/env python3
"""
Hızlı GUI Manager Test - PyGubu Entegrasyonu
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def quick_test():
    """Hızlı test"""
    print("🚀 Quick GUI Manager Test")
    print("=" * 30)
    
    try:
        # İlk önce bağımlılıkları test et
        print("� Testing dependencies...")
        
        import pygubu
        print(f"✅ PyGubu: {pygubu.__version__}")
        
        import tkinter as tk
        print("✅ Tkinter: Available")
        
        # UI dosyasını kontrol et
        ui_file = Path(__file__).parent / "gui_designs" / "d64_converter_main.ui"
        print(f"✅ UI file: {ui_file.exists()}")
        
        # GUI Manager'ı minimal test et
        print("\n🎨 Testing GUI Manager...")
        
        # Modülü adım adım import et
        try:
            from gui_manager import D64ConverterGUI
            print("✅ GUI Manager imported successfully")
        except ImportError as e:
            print(f"❌ GUI Manager import failed: {e}")
            return
        
        # Root pencere oluştur
        root = tk.Tk()
        root.withdraw()
        root.title("Quick Test")
        
        print("� Creating GUI instance...")
        
        # GUI'yi oluştur
        gui = D64ConverterGUI(root)
        
        # PyGubu durumunu kontrol et
        if hasattr(gui, 'pygubu_enabled') and gui.pygubu_enabled:
            print("✅ PyGubu mode active!")
            print(f"📊 PyGubu widgets: {len(gui.pygubu_widgets)}")
            
            # Widget listesi
            if gui.pygubu_widgets:
                print("🧩 Available widgets:")
                for widget_name in gui.pygubu_widgets:
                    print(f"  • {widget_name}")
            
            # Pencereyi kısa süre göster
            if hasattr(gui, 'pygubu_main_window'):
                gui.pygubu_main_window.deiconify()
                gui.pygubu_main_window.title("D64 Converter - PyGubu Quick Test")
                
                # 3 saniye sonra kapat
                root.after(3000, root.quit)
                print("\n� GUI penceresi 3 saniye açılacak...")
                root.mainloop()
                
        else:
            print("⚠️ Traditional mode active")
            
            # Geleneksel GUI penceresi
            if hasattr(gui, 'root'):
                gui.root.deiconify()
                gui.root.title("D64 Converter - Traditional Quick Test")
                root.after(3000, root.quit)
                print("\n💡 Traditional GUI penceresi 3 saniye açılacak...")
                root.mainloop()
        
        print("\n🎉 Quick test completed successfully!")
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()
