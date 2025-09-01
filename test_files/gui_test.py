#!/usr/bin/env python3
"""
GUI Test - D64 Converter
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
sys.path.insert(0, os.getcwd())

def test_gui():
    """GUI test fonksiyonu"""
    try:
        # Test root window
        root = tk.Tk()
        root.title("D64 Converter Test")
        root.geometry("200x100")
        
        # Test D64ConverterApp import
        from d64_converter import D64ConverterApp
        print("✅ D64ConverterApp import başarılı")
        
        # Test app creation
        app = D64ConverterApp(root)
        print("✅ D64ConverterApp oluşturuldu")
        
        # Test methods
        if hasattr(app, 'analyze_illegal_opcodes'):
            print("✅ analyze_illegal_opcodes method var")
        else:
            print("❌ analyze_illegal_opcodes method yok")
        
        if hasattr(app, 'show_illegal_analysis_results'):
            print("✅ show_illegal_analysis_results method var")
        else:
            print("❌ show_illegal_analysis_results method yok")
        
        if hasattr(app, 'extract_prg_data'):
            print("✅ extract_prg_data method var")
        else:
            print("❌ extract_prg_data method yok")
        
        # Test simple analyzer import
        try:
            from simple_analyzer import SimpleIllegalAnalyzer
            print("✅ SimpleIllegalAnalyzer import başarılı")
        except Exception as e:
            print(f"❌ SimpleIllegalAnalyzer import hatası: {e}")
        
        # Test advanced disassembler import
        try:
            from advanced_disassembler import AdvancedDisassembler
            print("✅ AdvancedDisassembler import başarılı")
        except Exception as e:
            print(f"❌ AdvancedDisassembler import hatası: {e}")
        
        # Test button
        tk.Button(root, text="Test Tamamlandı", command=root.quit).pack(pady=20)
        
        print("\n🚀 GUI test tamamlandı! Pencereyi kapatın.")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ GUI test hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui()
