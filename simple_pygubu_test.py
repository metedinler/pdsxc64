#!/usr/bin/env python3
"""
Basit PyGubu Import Test
"""

try:
    print("Testing PyGubu import...")
    import pygubu
    print(f"✅ PyGubu version: {pygubu.__version__}")
    
    print("Testing UI file...")
    from pathlib import Path
    ui_file = Path(__file__).parent / "gui_designs" / "d64_converter_main.ui"
    
    if ui_file.exists():
        print(f"✅ UI file found: {ui_file}")
        
        # UI dosyasını yüklemeyi dene
        builder = pygubu.Builder()
        builder.add_from_file(str(ui_file))
        print("✅ UI file loaded successfully")
        
        # Widget'ları kontrol et
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        
        main_window = builder.get_object('main_window', root)
        print("✅ Main window created")
        
        root.destroy()
        print("✅ Basic PyGubu test completed successfully!")
        
    else:
        print(f"❌ UI file not found: {ui_file}")
        
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
