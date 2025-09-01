#!/usr/bin/env python3
"""
D64 Converter - PAGE Projesi
Düzgün PAGE ile oluşturulmuş GUI

PAGE kullanımı:
1. cd venv_asmto/page  
2. python page.py
3. File > New > d64_converter_gui.tcl dosyasını oluştur
4. Generate > Python Support Module
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os

# Proje dizinini ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class D64ConverterGUI:
    """PAGE ile uyumlu ana GUI sınıfı"""
    
    def __init__(self, master=None):
        self.master = master if master else tk.Tk()
        self.setup_gui()
        self.setup_variables()
        
    def setup_variables(self):
        """GUI değişkenlerini ayarla"""
        self.current_file = None
        self.file_content = None
        
    def setup_gui(self):
        """Ana GUI yapısını oluştur"""
        self.master.title("D64 Converter v5.0 - PAGE Edition")
        self.master.geometry("1200x800")
        self.master.configure(bg='#2b2b2b')
        
        # Menü çubuğu
        self.create_menubar()
        
        # Ana çerçeve
        self.main_frame = tk.Frame(self.master, bg='#2b2b2b')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Üst panel - Dosya seçimi
        self.create_file_panel()
        
        # Orta panel - 4 bölümlü alan
        self.create_main_panels()
        
        # Alt panel - Durum çubuğu
        self.create_status_bar()
        
    def create_menubar(self):
        """Menü çubuğunu oluştur"""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        # Dosya menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Aç...", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.master.quit)
        
        # Araçlar menüsü
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Araçlar", menu=tools_menu)
        tools_menu.add_command(label="PAGE Designer Aç", command=self.open_page_designer)
        
    def create_file_panel(self):
        """Dosya seçim panelini oluştur"""
        file_frame = tk.LabelFrame(self.main_frame, text="📁 Dosya Seçimi", 
                                  bg='#3c3c3c', fg='white', font=('Arial', 12, 'bold'))
        file_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Dosya seçim butonu
        self.open_button = tk.Button(file_frame, text="📂 PRG/D64 Dosyası Seç",
                                   command=self.open_file, bg='#4c4c4c', fg='white',
                                   font=('Arial', 11), padx=20, pady=5)
        self.open_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Dosya yolu etiketi
        self.file_label = tk.Label(file_frame, text="Dosya seçilmedi", 
                                 bg='#3c3c3c', fg='#cccccc', font=('Consolas', 10))
        self.file_label.pack(side=tk.LEFT, padx=10)
        
    def create_main_panels(self):
        """Ana 4 panelli alanı oluştur"""
        # Ana container
        panels_frame = tk.Frame(self.main_frame, bg='#2b2b2b')
        panels_frame.pack(fill=tk.BOTH, expand=True)
        
        # Üst paneller
        top_frame = tk.Frame(panels_frame, bg='#2b2b2b')
        top_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 2))
        
        # Sol üst - Dizin listesi
        self.create_directory_panel(top_frame)
        
        # Sağ üst - Disassembly
        self.create_disassembly_panel(top_frame)
        
        # Alt paneller
        bottom_frame = tk.Frame(panels_frame, bg='#2b2b2b')
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
        
        # Sol alt - Console
        self.create_console_panel(bottom_frame)
        
        # Sağ alt - Decompiler
        self.create_decompiler_panel(bottom_frame)
        
    def create_directory_panel(self, parent):
        """Dizin listesi panelini oluştur"""
        dir_frame = tk.LabelFrame(parent, text="📂 Dizin İçeriği", 
                                bg='#3c3c3c', fg='white', font=('Arial', 10, 'bold'))
        dir_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))
        
        # Listbox ile scrollbar
        scroll_frame = tk.Frame(dir_frame, bg='#3c3c3c')
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.dir_listbox = tk.Listbox(scroll_frame, bg='#2b2b2b', fg='white',
                                    font=('Consolas', 9), selectbackground='#4c4c4c')
        dir_scroll = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=self.dir_listbox.yview)
        self.dir_listbox.configure(yscrollcommand=dir_scroll.set)
        
        self.dir_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        dir_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_disassembly_panel(self, parent):
        """Disassembly panelini oluştur"""
        disasm_frame = tk.LabelFrame(parent, text="⚙️ Disassembly", 
                                   bg='#3c3c3c', fg='white', font=('Arial', 10, 'bold'))
        disasm_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2, 0))
        
        # Format butonları
        button_frame = tk.Frame(disasm_frame, bg='#3c3c3c')
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        formats = ["Assembly", "C", "QBasic", "BASIC", "Petcat"]
        for i, fmt in enumerate(formats):
            btn = tk.Button(button_frame, text=fmt, command=lambda f=fmt: self.convert_format(f),
                          bg='#4c4c4c', fg='white', font=('Arial', 9), padx=10)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Text alanı
        text_frame = tk.Frame(disasm_frame, bg='#3c3c3c')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.disasm_text = tk.Text(text_frame, bg='#2b2b2b', fg='white',
                                 font=('Consolas', 9), wrap=tk.WORD)
        disasm_scroll = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.disasm_text.yview)
        self.disasm_text.configure(yscrollcommand=disasm_scroll.set)
        
        self.disasm_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        disasm_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_console_panel(self, parent):
        """Console panelini oluştur"""
        console_frame = tk.LabelFrame(parent, text="📟 Console", 
                                    bg='#3c3c3c', fg='white', font=('Arial', 10, 'bold'))
        console_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))
        
        text_frame = tk.Frame(console_frame, bg='#3c3c3c')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.console_text = tk.Text(text_frame, bg='#1a1a1a', fg='#00ff00',
                                  font=('Consolas', 9), wrap=tk.WORD, state=tk.DISABLED)
        console_scroll = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=console_scroll.set)
        
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        console_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # İlk mesaj
        self.log_message("🚀 D64 Converter v5.0 PAGE Edition hazır")
        self.log_message("💡 Önce bir PRG/D64 dosyası seçin")
        
    def create_decompiler_panel(self, parent):
        """Decompiler panelini oluştur"""
        decompiler_frame = tk.LabelFrame(parent, text="🔄 Decompiler", 
                                       bg='#3c3c3c', fg='white', font=('Arial', 10, 'bold'))
        decompiler_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2, 0))
        
        # Analiz butonları
        analysis_frame = tk.Frame(decompiler_frame, bg='#3c3c3c')
        analysis_frame.pack(fill=tk.X, padx=5, pady=5)
        
        analyses = ["Sprites", "SID", "Charset", "Illegal Opcodes"]
        for analysis in analyses:
            btn = tk.Button(analysis_frame, text=analysis, 
                          command=lambda a=analysis: self.run_analysis(a),
                          bg='#4c4c4c', fg='white', font=('Arial', 9), padx=8)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Results alanı
        text_frame = tk.Frame(decompiler_frame, bg='#3c3c3c')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.decompiler_text = tk.Text(text_frame, bg='#2b2b2b', fg='white',
                                     font=('Consolas', 9), wrap=tk.WORD)
        decompiler_scroll = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.decompiler_text.yview)
        self.decompiler_text.configure(yscrollcommand=decompiler_scroll.set)
        
        self.decompiler_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        decompiler_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_status_bar(self):
        """Durum çubuğunu oluştur"""
        self.status_bar = tk.Label(self.master, text="Hazır", relief=tk.SUNKEN,
                                 anchor=tk.W, bg='#4c4c4c', fg='white', font=('Arial', 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def open_file(self):
        """Dosya seçme fonksiyonu"""
        filename = filedialog.askopenfilename(
            title="C64 Dosyası Seç",
            filetypes=[
                ("PRG files", "*.prg"),
                ("D64 files", "*.d64"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.current_file = filename
            self.file_label.config(text=os.path.basename(filename))
            self.status_bar.config(text=f"Dosya yüklendi: {os.path.basename(filename)}")
            self.log_message(f"📂 Dosya seçildi: {os.path.basename(filename)}")
            
            # Dosya içeriğini yükle
            self.load_file_content()
            
    def load_file_content(self):
        """Dosya içeriğini yükle"""
        if not self.current_file:
            return
            
        try:
            with open(self.current_file, 'rb') as f:
                self.file_content = f.read()
            
            # Dizin içeriğini güncelle
            self.update_directory_listing()
            self.log_message(f"✅ Dosya içeriği yüklendi ({len(self.file_content)} byte)")
            
        except Exception as e:
            self.log_message(f"❌ Dosya yükleme hatası: {e}")
            messagebox.showerror("Hata", f"Dosya yüklenemedi:\n{e}")
            
    def update_directory_listing(self):
        """Dizin listesini güncelle"""
        self.dir_listbox.delete(0, tk.END)
        
        if self.current_file:
            if self.current_file.lower().endswith('.d64'):
                self.dir_listbox.insert(tk.END, "D64 Disk Image")
                self.dir_listbox.insert(tk.END, "- Track/Sector analizi gerekli")
            else:
                self.dir_listbox.insert(tk.END, f"PRG Dosyası: {os.path.basename(self.current_file)}")
                if self.file_content and len(self.file_content) >= 2:
                    load_addr = self.file_content[0] + (self.file_content[1] << 8)
                    self.dir_listbox.insert(tk.END, f"- Load Address: ${load_addr:04X}")
                    self.dir_listbox.insert(tk.END, f"- Size: {len(self.file_content)-2} bytes")
                    
    def convert_format(self, format_type):
        """Format dönüştürme"""
        if not self.file_content:
            self.log_message("❌ Önce bir dosya seçin!")
            return
            
        self.log_message(f"🔄 {format_type} formatına dönüştürülüyor...")
        self.disasm_text.delete(1.0, tk.END)
        self.disasm_text.insert(tk.END, f"{format_type} Format Çıktısı\n{'='*40}\n\n")
        
        if format_type == "Assembly":
            self.disasm_text.insert(tk.END, "; Assembly output would go here\n")
        elif format_type == "C":
            self.disasm_text.insert(tk.END, "// C code output would go here\n")
        else:
            self.disasm_text.insert(tk.END, f"// {format_type} output placeholder\n")
            
        self.log_message(f"✅ {format_type} dönüştürme tamamlandı")
        
    def run_analysis(self, analysis_type):
        """Analiz çalıştırma"""
        if not self.file_content:
            self.log_message("❌ Önce bir dosya seçin!")
            return
            
        self.log_message(f"🔍 {analysis_type} analizi başlatılıyor...")
        self.decompiler_text.delete(1.0, tk.END)
        self.decompiler_text.insert(tk.END, f"{analysis_type} Analiz Sonuçları\n{'='*40}\n\n")
        self.decompiler_text.insert(tk.END, f"Analiz placeholder for {analysis_type}\n")
        
        self.log_message(f"✅ {analysis_type} analizi tamamlandı")
        
    def open_page_designer(self):
        """PAGE Designer'ı açma"""
        try:
            page_path = "venv_asmto/page/page.py"
            if os.path.exists(page_path):
                os.system(f"python {page_path}")
                self.log_message("🎨 PAGE Designer açılıyor...")
            else:
                self.log_message("❌ PAGE Designer bulunamadı!")
        except Exception as e:
            self.log_message(f"❌ PAGE açma hatası: {e}")
            
    def log_message(self, message):
        """Console'a mesaj yazdır"""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, f"{message}\n")
        self.console_text.config(state=tk.DISABLED)
        self.console_text.see(tk.END)
        
def main():
    """Ana fonksiyon"""
    print("🎨 D64 Converter v5.0 - PAGE Edition")
    print("📋 PAGE ile uyumlu GUI başlatılıyor...")
    
    app = D64ConverterGUI()
    app.master.mainloop()

if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
