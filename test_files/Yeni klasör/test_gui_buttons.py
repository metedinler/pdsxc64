#!/usr/bin/env python3
"""
GUI button test script
"""
import tkinter as tk
from tkinter import ttk

def test_button_functionality():
    """Test buton fonksiyonlarını kontrol et"""
    try:
        from d64_converter import D64ConverterApp
        
        # Test GUI oluştur
        root = tk.Tk()
        root.withdraw()  # Pencereyi gizle
        
        app = D64ConverterApp(root)
        
        # Test edilen fonksiyonlar
        test_functions = [
            'convert_to_assembly',
            'convert_to_c', 
            'convert_to_qbasic',
            'convert_to_pdsx',
            'convert_to_pseudo',
            'convert_to_basic',
            'convert_to_petcat',
            'convert_to_c64list',
            'convert_to_py65',
            'convert_to_decompiler',
            'convert_to_dec_qbasic',
            'convert_to_dec_c',
            'convert_to_dec_cpp',
            'convert_to_dec_c2',
            'convert_to_dec_asm'
        ]
        
        print("🔍 GUI Button Test")
        print("=" * 50)
        
        missing_functions = []
        working_functions = []
        
        for func_name in test_functions:
            if hasattr(app, func_name):
                func = getattr(app, func_name)
                if callable(func):
                    working_functions.append(func_name)
                    print(f"✅ {func_name} - ÇALIŞIR")
                else:
                    missing_functions.append(func_name)
                    print(f"❌ {func_name} - ÇAĞRILAMAZ")
            else:
                missing_functions.append(func_name)
                print(f"❌ {func_name} - BULUNAMADI")
        
        print("\n📊 Özet:")
        print(f"  ✅ Çalışan: {len(working_functions)}")
        print(f"  ❌ Eksik: {len(missing_functions)}")
        
        if missing_functions:
            print("\n🚨 Eksik fonksiyonlar:")
            for func in missing_functions:
                print(f"  - {func}")
        
        # Test: convert_to_specific_format var mı?
        if hasattr(app, 'convert_to_specific_format'):
            print("\n✅ convert_to_specific_format fonksiyonu mevcut")
        else:
            print("\n❌ convert_to_specific_format fonksiyonu eksik")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_button_functionality()
