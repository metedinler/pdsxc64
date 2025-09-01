#!/usr/bin/env python3
"""
D64 Converter Manual Test Script
"""

import os
import sys

def test_program():
    """Programı test et"""
    print("D64 Converter Manual Test")
    print("=" * 50)
    
    # Mevcut dizini kontrol et
    current_dir = os.getcwd()
    print(f"Mevcut dizin: {current_dir}")
    
    # Python sürümü
    print(f"Python version: {sys.version}")
    
    # Dosya seçim testi
    print("\n1. Dosya seçim test başlatılıyor...")
    
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        
        # Test dosya türleri
        file_types = [
            ('D64 Disk Files', '*.d64'),
            ('D71 Disk Files', '*.d71'),
            ('D81 Disk Files', '*.d81'),
            ('D84 Disk Files', '*.d84'),
            ('T64 Tape Files', '*.t64'),
            ('TAP Tape Files', '*.tap'),
            ('PRG Program Files', '*.prg'),
            ('P00 Program Files', '*.p00'),
            ('G64 GCR Files', '*.g64'),
            ('LNX Archive Files', '*.lnx'),
            ('LYNX Archive Files', '*.lynx'),
            ('CRT Cartridge Files', '*.crt'),
            ('BIN Binary Files', '*.bin'),
            ('All C64 Files', '*.d64;*.d71;*.d81;*.d84;*.t64;*.tap;*.prg;*.p00;*.g64;*.lnx;*.lynx;*.crt;*.bin'),
            ('All Files', '*.*')
        ]
        
        print("Dosya seçim dialogu açılıyor...")
        print("Desteklenen formatlar:")
        for desc, pattern in file_types:
            print(f"  {desc}: {pattern}")
        
        file_path = filedialog.askopenfilename(
            title="TEST: C64 Dosyası Seç",
            filetypes=file_types,
            initialdir=os.path.expanduser("~\\Downloads")
        )
        
        if file_path:
            print(f"\n✅ Seçilen dosya: {file_path}")
            print(f"📁 Dosya adı: {os.path.basename(file_path)}")
            print(f"📂 Dizin: {os.path.dirname(file_path)}")
            print(f"🔗 Uzantı: {os.path.splitext(file_path)[1]}")
            
            if os.path.exists(file_path):
                print(f"💾 Dosya boyutu: {os.path.getsize(file_path)} bytes")
                print("✔️ Dosya mevcut")
                
                # Ana programı çalıştır
                print("\n2. Ana program başlatılıyor...")
                os.system("python d64_converter.py")
                
            else:
                print("❌ Dosya bulunamadı")
        else:
            print("❌ Dosya seçimi iptal edildi")
            
        root.destroy()
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_program()
