#!/usr/bin/env python3
"""
Simple GUI test - manual button test
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def test_simple_gui():
    """Basit GUI test"""
    try:
        from d64_converter import D64ConverterApp
        
        print("🔍 Simple GUI Test")
        print("=" * 50)
        
        # Test GUI oluştur
        root = tk.Tk()
        root.title("D64 Converter Test")
        
        app = D64ConverterApp(root)
        
        # Test mesajları
        def test_assembly():
            print("✅ Assembly button clicked")
            messagebox.showinfo("Test", "Assembly button çalışıyor!")
        
        def test_petcat():
            print("✅ Petcat button clicked")  
            messagebox.showinfo("Test", "Petcat button çalışıyor!")
        
        # Test frame ekle
        test_frame = ttk.LabelFrame(root, text="Test Buttons", padding="10")
        test_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(test_frame, text="Test Assembly", command=test_assembly).pack(side=tk.LEFT, padx=5)
        ttk.Button(test_frame, text="Test Petcat", command=test_petcat).pack(side=tk.LEFT, padx=5)
        
        # Gerçek button test
        def test_real_assembly():
            try:
                app.convert_to_assembly()
                print("✅ Real assembly button başarılı")
                messagebox.showinfo("Test", "Real Assembly button çalışıyor!")
            except Exception as e:
                print(f"❌ Real assembly button hatası: {e}")
                messagebox.showerror("Test", f"Real Assembly button hatası: {e}")
        
        def test_real_petcat():
            try:
                app.convert_to_petcat()
                print("✅ Real petcat button başarılı")
                messagebox.showinfo("Test", "Real Petcat button çalışıyor!")
            except Exception as e:
                print(f"❌ Real petcat button hatası: {e}")
                messagebox.showerror("Test", f"Real Petcat button hatası: {e}")
        
        ttk.Button(test_frame, text="Real Assembly", command=test_real_assembly).pack(side=tk.LEFT, padx=5)
        ttk.Button(test_frame, text="Real Petcat", command=test_real_petcat).pack(side=tk.LEFT, padx=5)
        
        # Talimatlar
        instructions = ttk.Label(root, text="1. Üst menüden 'Dosya Seç' ile D64 dosyası yükleyin\n2. Test butonlarını tıklayın", 
                                justify=tk.LEFT, foreground="blue")
        instructions.pack(pady=10)
        
        print("🚀 GUI açılıyor... Test butonlarını tıklayın!")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ GUI Test hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_gui()
