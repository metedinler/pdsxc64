#!/usr/bin/env python3
"""
Dosya Seçim Dialog Test - Detaylı
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os

def test_file_dialog_detailed():
    """Detaylı dosya seçim dialogu testi"""
    root = tk.Tk()
    root.title("Dosya Seçim Test")
    root.geometry("400x300")
    
    # Test sonuçları için text widget
    text_widget = tk.Text(root, wrap=tk.WORD, width=50, height=15)
    text_widget.pack(padx=10, pady=10)
    
    def show_file_dialog():
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Dosya seçim dialogu açılıyor...\n\n")
        
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
        
        text_widget.insert(tk.END, "Desteklenen formatlar:\n")
        for desc, pattern in file_types:
            text_widget.insert(tk.END, f"  {desc}: {pattern}\n")
        text_widget.insert(tk.END, "\n")
        
        file_path = filedialog.askopenfilename(
            title="Commodore 64 Dosyası Seç - D64, D71, D81, D84, T64, TAP, PRG, P00, G64, LNX, LYNX, CRT, BIN",
            filetypes=file_types,
            initialdir=os.path.expanduser("~"),
            defaultextension=".d64"
        )
        
        if file_path:
            text_widget.insert(tk.END, f"✅ Seçilen dosya: {file_path}\n")
            text_widget.insert(tk.END, f"📁 Dosya adı: {os.path.basename(file_path)}\n")
            text_widget.insert(tk.END, f"📂 Dizin: {os.path.dirname(file_path)}\n")
            text_widget.insert(tk.END, f"🔗 Uzantı: {os.path.splitext(file_path)[1]}\n")
            text_widget.insert(tk.END, f"💾 Dosya boyutu: {os.path.getsize(file_path)} bytes\n")
            text_widget.insert(tk.END, f"✔️ Dosya var: {os.path.exists(file_path)}\n")
        else:
            text_widget.insert(tk.END, "❌ Dosya seçimi iptal edildi\n")
    
    def check_current_dir():
        text_widget.delete(1.0, tk.END)
        current_dir = os.getcwd()
        text_widget.insert(tk.END, f"📂 Mevcut dizin: {current_dir}\n\n")
        
        # C64 dosyalarını ara
        supported_extensions = ['.d64', '.d71', '.d81', '.d84', '.t64', '.tap', '.prg', '.p00', '.g64', '.lnx', '.lynx', '.crt', '.bin']
        
        found_files = []
        for root_dir, dirs, files in os.walk(current_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    found_files.append(os.path.join(root_dir, file))
        
        if found_files:
            text_widget.insert(tk.END, f"🔍 Bulunan C64 dosyaları ({len(found_files)} adet):\n")
            for file_path in found_files[:10]:  # İlk 10 dosya
                text_widget.insert(tk.END, f"  {file_path}\n")
            if len(found_files) > 10:
                text_widget.insert(tk.END, f"  ... ve {len(found_files) - 10} dosya daha\n")
        else:
            text_widget.insert(tk.END, "❌ Mevcut dizinde C64 dosyası bulunamadı\n")
        
        # Downloads klasörünü kontrol et
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.exists(downloads_dir):
            text_widget.insert(tk.END, f"\n📥 Downloads klasörü: {downloads_dir}\n")
            downloads_files = []
            for file in os.listdir(downloads_dir):
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    downloads_files.append(file)
            
            if downloads_files:
                text_widget.insert(tk.END, f"🔍 Downloads'ta bulunan C64 dosyaları ({len(downloads_files)} adet):\n")
                for file in downloads_files[:5]:  # İlk 5 dosya
                    text_widget.insert(tk.END, f"  {file}\n")
            else:
                text_widget.insert(tk.END, "❌ Downloads klasöründe C64 dosyası bulunamadı\n")
    
    # Butonlar
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Dosya Seç", command=show_file_dialog, width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Dosya Ara", command=check_current_dir, width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Çıkış", command=root.quit, width=15).pack(side=tk.LEFT, padx=5)
    
    # Başlangıç mesajı
    text_widget.insert(tk.END, "Dosya Seçim Test Programı\n")
    text_widget.insert(tk.END, "=" * 30 + "\n\n")
    text_widget.insert(tk.END, "1. 'Dosya Seç' butonu ile dosya seçim dialogunu test edin\n")
    text_widget.insert(tk.END, "2. 'Dosya Ara' butonu ile mevcut C64 dosyalarını bulun\n")
    text_widget.insert(tk.END, "3. Dialog'da dosya türü filtresini kullanın\n\n")
    text_widget.insert(tk.END, "NOT: Windows'da dosya uzantıları gizli olabilir.\n")
    text_widget.insert(tk.END, "Çözüm: Dosya Gezgini > Görünüm > Dosya adı uzantıları ✓\n\n")
    
    root.mainloop()

if __name__ == "__main__":
    test_file_dialog_detailed()
