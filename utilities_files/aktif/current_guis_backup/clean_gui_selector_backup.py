"""
D64 Converter - GUI Selector
Basit ve temiz tasarım
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class D64GUISelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D64 Converter - GUI Seçici")
        self.root.resizable(True, True)
        
        # Tema seçimi
        self.theme_var = tk.StringVar(value="light")
        self.gui_var = tk.StringVar(value="x1_gui")  # Default: X1 GUI
        
        # Tema ayarları
        self.themes = {
            "light": {
                "bg": "#F0F0F0",
                "fg": "#000000",
                "select_bg": "#E0E0E0",
                "button_bg": "#FFFFFF",
                "accent": "#4CAF50"
            },
            "dark": {
                "bg": "#2E2E2E",
                "fg": "#FFFFFF", 
                "select_bg": "#404040",
                "button_bg": "#505050",
                "accent": "#81C784"
            }
        }
        
        self.setup_gui()
        self.apply_theme()
        self.update_descriptions()
        
        # Pencere boyutunu düzgün ayarla
        self.root.update_idletasks()
        width = 600
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_gui(self):
        """GUI oluştur"""
        # Ana frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Başlık
        title_label = tk.Label(main_frame, text="D64 Converter", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Program açıklaması
        self.desc_label = tk.Label(main_frame, text="", 
                                  font=("Arial", 10), 
                                  wraplength=550, justify=tk.LEFT)
        self.desc_label.pack(pady=(0, 20))
        
        # Tema seçimi
        theme_frame = tk.LabelFrame(main_frame, text="Tema Seçimi", font=("Arial", 10, "bold"))
        theme_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Radiobutton(theme_frame, text="Açık Tema", variable=self.theme_var, 
                      value="light", command=self.apply_theme).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Radiobutton(theme_frame, text="Koyu Tema", variable=self.theme_var, 
                      value="dark", command=self.apply_theme).pack(side=tk.LEFT, padx=10, pady=5)
        
        # GUI seçimi
        gui_frame = tk.LabelFrame(main_frame, text="GUI Seçimi", font=("Arial", 10, "bold"))
        gui_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Ana GUI Seçenekleri - Sadece 3 Aktif GUI
        gui_row1 = tk.Frame(gui_frame)
        gui_row1.pack(fill=tk.X, pady=5)
        
        tk.Radiobutton(gui_row1, text="X1 GUI", variable=self.gui_var, 
                      value="x1_gui", command=self.update_descriptions,
                      font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10, pady=2)
        tk.Radiobutton(gui_row1, text="Klasik GUI", variable=self.gui_var, 
                      value="classic", command=self.update_descriptions,
                      font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10, pady=2)
        tk.Radiobutton(gui_row1, text="Eski GUI v3", variable=self.gui_var, 
                      value="original3", command=self.update_descriptions,
                      font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=10, pady=2)
        
        # Yedek Seçici Seçeneği
        gui_row2 = tk.Frame(gui_frame)
        gui_row2.pack(fill=tk.X, pady=3)
        
        tk.Radiobutton(gui_row2, text="Modern Selector (Yedek)", variable=self.gui_var, 
                      value="modern_selector", command=self.update_descriptions,
                      font=("Arial", 9), fg="gray").pack(side=tk.LEFT, padx=10, pady=2)
        
        # GUI açıklaması
        self.gui_desc_label = tk.Label(main_frame, text="", 
                                      font=("Arial", 9), 
                                      wraplength=550, justify=tk.LEFT)
        self.gui_desc_label.pack(pady=(0, 20))
        
        # Düğmeler
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.launch_btn = tk.Button(button_frame, text="GUI Başlat", 
                                   command=self.launch_selected_gui,
                                   font=("Arial", 12, "bold"),
                                   width=15, height=2)
        self.launch_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Çıkış", command=self.root.quit,
                 font=("Arial", 10), width=10, height=2).pack(side=tk.RIGHT, padx=5)
        
    def apply_theme(self):
        """Tema uygula"""
        theme = self.themes[self.theme_var.get()]
        
        def apply_to_widget(widget):
            try:
                widget.configure(bg=theme["bg"], fg=theme["fg"])
            except:
                pass
            for child in widget.winfo_children():
                apply_to_widget(child)
        
        apply_to_widget(self.root)
        
        # Düğme renklerini ayarla
        try:
            self.launch_btn.configure(bg=theme["accent"], fg="#FFFFFF")
        except:
            pass
    
    def update_descriptions(self):
        """Açıklamaları güncelle - Sadece 3 Aktif GUI"""
        main_desc = """Commodore 64 disk imajlarını (D64, D71, D81) ve program dosyalarını (PRG, T64, TAP) 
çeşitli formatlara çeviren profesyonel araç. 6502 assembly kodunu C, QBasic, Pseudo Code 
ve diğer formatlara dönüştürür."""
        
        self.desc_label.configure(text=main_desc)
        
        if self.gui_var.get() == "x1_gui":
            gui_desc = """X1 GUI: d64_converterX1.py - Gelişmiş X serisi 1. versiyon. 2630 satır kodlu kapsamlı GUI, 
enhanced disassembler, decompiler entegrasyonu, threading desteği. EN GELİŞMİŞ VERSİYON."""
        elif self.gui_var.get() == "classic":
            gui_desc = """Klasik GUI: gui_restored.py - Sekme tabanlı arayüz. Dosya analizi, başlangıç adresi görüntüleme, 
içerik önizleme, işlenen dosyalar geçmişi. PETCAT BASIC desteği ve arama sistemi. RESTORE EDİLMİŞ VERSİYON."""
        elif self.gui_var.get() == "original3":
            gui_desc = """Eski GUI v3: eski_gui_3.py - Kopya klasöründen alınan GUI versiyonu. 16.07.2025 10:05 tarihli, 
87KB boyutunda, gelişmiş özellikler ve stabil versiyon. STABİL ÇALIŞAN VERSİYON."""
        elif self.gui_var.get() == "modern_selector":
            gui_desc = """Modern Selector: modern_gui_selector.py - Modern tasarımda GUI seçici. Koyu tema, gradient butonlar, 
professional görünüm. YEDEK SEÇİCİ OLARAK KULLANILIYOR."""
        else:
            gui_desc = """Lütfen yukarıdaki seçeneklerden birini seçin."""
        
        self.gui_desc_label.configure(text=gui_desc)
    
    def launch_selected_gui(self):
        """Seçili GUI'yi başlat - Sadece 3 Aktif GUI"""
        try:
            self.root.withdraw()
            
            if self.gui_var.get() == "x1_gui":
                from d64_converterX1 import D64ConverterApp  # X1 GUI - Ana güçlü GUI
                new_root = tk.Toplevel()
                app = D64ConverterApp(new_root)
            elif self.gui_var.get() == "classic":
                from gui_restored import D64ConverterRestoredGUI  # Klasik GUI - Restore edilmiş
                new_root = tk.Toplevel()
                app = D64ConverterRestoredGUI(new_root)
            elif self.gui_var.get() == "original3":
                from eski_gui_3 import D64ConverterApp  # Eski GUI v3 - Stabil versiyon
                new_root = tk.Toplevel()
                app = D64ConverterApp(new_root)
            elif self.gui_var.get() == "modern_selector":
                from modern_gui_selector import ModernGUISelector  # Yedek Selector
                app = ModernGUISelector()
                app.run()
                self.root.deiconify()
                return
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir GUI seçin!")
                self.root.deiconify()
                return
            
            def on_close():
                new_root.destroy()
                self.root.deiconify()
            
            new_root.protocol("WM_DELETE_WINDOW", on_close)
            
        except Exception as e:
            messagebox.showerror("Hata", f"GUI başlatılamadı: {e}")
            self.root.deiconify()
    
    def run(self):
        """Çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    print("D64 Converter GUI Seçici başlatılıyor...")
    selector = D64GUISelector()
    selector.run()
