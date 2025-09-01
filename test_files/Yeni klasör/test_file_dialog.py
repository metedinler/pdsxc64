#!/usr/bin/env python3
"""
Dosya Seçim Dialog Test
"""

import tkinter as tk
from tkinter import filedialog
import os

def test_file_dialog():
    """Dosya seçim dialogunu test et"""
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    
    file_types = [
        ('Commodore 64 Disk Files (*.d64, *.d71, *.d81, *.d84)', '*.d64 *.d71 *.d81 *.d84'),
        ('Commodore 64 Tape Files (*.t64, *.tap)', '*.t64 *.tap'),
        ('Commodore 64 Program Files (*.prg, *.p00)', '*.prg *.p00'),
        ('Commodore 64 GCR Files (*.g64)', '*.g64'),
        ('Commodore 64 Archive Files (*.lnx, *.lynx)', '*.lnx *.lynx'),
        ('Commodore 64 Cartridge Files (*.crt, *.bin)', '*.crt *.bin'),
        ('Tüm Commodore 64 Dosyaları', '*.d64 *.d71 *.d81 *.d84 *.t64 *.tap *.prg *.p00 *.g64 *.lnx *.lynx *.crt *.bin'),
        ('Tüm Dosyalar', '*.*')
    ]
    
    print("Dosya seçim dialogu açılıyor...")
    print("Desteklenen formatlar: D64, D71, D81, D84, T64, TAP, PRG, P00, G64, LNX, LYNX, CRT, BIN")
    
    file_path = filedialog.askopenfilename(
        title="Commodore 64 Dosyası Seç - Desteklenen formatlar: D64, D71, D81, D84, T64, TAP, PRG, P00, G64, LNX, LYNX, CRT, BIN",
        filetypes=file_types,
        initialdir=os.path.expanduser("~"),
        defaultextension=".d64"
    )
    
    if file_path:
        print(f"Seçilen dosya: {file_path}")
        print(f"Dosya uzantısı: {os.path.splitext(file_path)[1]}")
        print(f"Dosya var mı: {os.path.exists(file_path)}")
    else:
        print("Dosya seçimi iptal edildi")
    
    root.destroy()

if __name__ == "__main__":
    test_file_dialog()
