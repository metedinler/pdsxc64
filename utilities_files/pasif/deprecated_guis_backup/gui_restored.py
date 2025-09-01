"""
D64 Converter - Restored GUI with Enhanced Features
Eski güzel GUI'yi restore ediyoruz:
- Tabs için disassembler'lar
- File list'te tip ve hex address bilgisi
- İşlenen dosyalar sistemi
- Dosya arama özelliği
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from pathlib import Path
import json
import datetime

# Ana modüller
from d64_reader import (read_image, read_directory, read_t64_directory, read_tap_directory,
                       extract_prg_file, extract_t64_prg, extract_tap_prg, extract_p00_prg)
from improved_disassembler import ImprovedDisassembler, PY65_AVAILABLE, Py65ProfessionalDisassembler
from advanced_disassembler import AdvancedDisassembler, Disassembler
from parser import CodeEmitter, parse_line, load_instruction_map
from c64_basic_parser import C64BasicParser
from sprite_converter import SpriteConverter
from sid_converter import SIDConverter
import logging

class D64ConverterRestoredGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("D64 Converter - Professional Edition (Restored)")
        self.root.geometry("1400x900")
        
        # Ana değişkenler
        self.d64_path = tk.StringVar()
        self.disassembler_var = tk.StringVar(value="improved")
        self.use_illegal_opcodes = tk.BooleanVar(value=False)
        self.entries = []
        self.selected_files = []
        
        # PETCAT ve Token sistemi
        self.basic_parser = C64BasicParser()
        self.sprite_converter = SpriteConverter()
        self.sid_converter = SIDConverter()
        
        # İşlenen dosyalar sistemi
        self.processed_files = []
        self.recent_files = []
        
        # GUI kurulumu
        self.setup_gui()
        self.setup_logging()
        
        # İşlem geçmişini yükle
        self.load_processed_files()
        
    def setup_gui(self):
        """Ana GUI bileşenlerini oluştur"""
        # Ana container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Üst panel - Dosya seçimi ve ayarlar
        self.setup_top_panel(main_frame)
        
        # Orta panel - File list ve tip bilgileri
        self.setup_file_panel(main_frame)
        
        # Alt panel - Disassembler tabs
        self.setup_tabs_panel(main_frame)
        
        # Alt status bar
        self.setup_status_bar(main_frame)
        
    def setup_top_panel(self, parent):
        """Üst panel - dosya seçimi ve ayarlar"""
        top_frame = tk.Frame(parent)
        top_frame.pack(fill=tk.X, pady=5)
        
        # Dosya seçimi
        file_frame = tk.Frame(top_frame)
        file_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(file_frame, text="D64/D71/D81/TAP/T64 Dosyası:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        tk.Entry(file_frame, textvariable=self.d64_path, width=60, font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="📁 Dosya Seç", command=self.select_file, 
                 bg="#4CAF50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # Disassembler seçimi
        disasm_frame = tk.LabelFrame(top_frame, text="Disassembler Selection", font=("Arial", 9, "bold"))
        disasm_frame.pack(fill=tk.X, pady=5)
        
        disasm_options = [
            ("Basic (99 lines)", "basic", "Basit disassembler - sadece ASM"),
            ("Advanced (500 lines)", "advanced", "Gelişmiş disassembler + py65"), 
            ("Improved (1200+ lines)", "improved", "En gelişmiş - 6 format"),
            ("Professional py65", "py65_professional", "Profesyonel py65 wrapper")
        ]
        
        for i, (text, value, desc) in enumerate(disasm_options):
            frame = tk.Frame(disasm_frame)
            frame.pack(side=tk.LEFT, padx=10)
            
            rb = tk.Radiobutton(frame, text=text, variable=self.disassembler_var, 
                               value=value, font=("Arial", 9))
            rb.pack(anchor=tk.W)
            
            tk.Label(frame, text=desc, font=("Arial", 8), fg="gray").pack(anchor=tk.W)
        
        # Diğer ayarlar
        options_frame = tk.Frame(top_frame)
        options_frame.pack(fill=tk.X, pady=2)
        
        tk.Checkbutton(options_frame, text="🔬 Illegal Opcodes", 
                      variable=self.use_illegal_opcodes, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        
        tk.Button(options_frame, text="🔍 Dosya Arama", command=self.show_file_search,
                 bg="#2196F3", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(options_frame, text="📊 İşlenenler", command=self.show_processed_files,
                 bg="#FF9800", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
    def setup_file_panel(self, parent):
        """Dosya listesi paneli - gelişmiş bilgilerle"""
        file_frame = tk.LabelFrame(parent, text="Disk Content", font=("Arial", 10, "bold"))
        file_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Treeview - gelişmiş sütunlar için container oluştur
        content_frame = tk.Frame(file_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sol taraf - Disk content (ana alan)
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        columns = ("filename", "type", "start_addr", "info", "track_sector", "size")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        
        # Sütun başlıkları
        self.tree.heading("filename", text="Dosya Adı")
        self.tree.heading("type", text="Tip")
        self.tree.heading("start_addr", text="Başlangıç Adresi")
        self.tree.heading("info", text="İçerik Bilgisi")
        self.tree.heading("track_sector", text="Track/Sector")
        self.tree.heading("size", text="Boyut")
        
        # Sütun genişlikleri
        self.tree.column("filename", width=180)
        self.tree.column("type", width=80)
        self.tree.column("start_addr", width=120)
        self.tree.column("info", width=250)
        self.tree.column("track_sector", width=100)
        self.tree.column("size", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sağ taraf - Düğmeler (vertical layout)
        button_frame = tk.Frame(content_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Düğmeler alt alta - daha büyük ve görünür
        tk.Button(button_frame, text="🔄 Disk Yenile", command=self.refresh_disk_content,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                 width=16, height=2).pack(pady=5)
                 
        tk.Button(button_frame, text="🎯 Seçili Çevir", command=self.convert_selected_files,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                 width=16, height=2).pack(pady=5)
                 
        tk.Button(button_frame, text="🚀 Tümünü Çevir", command=self.convert_all_files,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                 width=16, height=2).pack(pady=5)
        
        # Event bindings
        self.tree.bind("<Double-1>", self.on_file_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)  # Tek tıklama event'i
        
    def setup_tabs_panel(self, parent):
        """Disassembler çıktıları için tab paneli"""
        tabs_frame = tk.LabelFrame(parent, text="Disassembler Output", font=("Arial", 10, "bold"))
        tabs_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Notebook widget
        self.notebook = ttk.Notebook(tabs_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Text widget'ları ve tab'ları
        self.output_texts = {}
        self.tab_frames = {}  # tab_frames sözlüğünü başlat
        formats = [
            ("Assembly", "asm", "Assembly output"),
            ("C Code", "c", "C language conversion"),
            ("QBasic", "qbasic", "QBasic conversion"),
            ("PDSX", "pdsx", "PDSX format"),
            ("Commodore BASIC V2", "commodorebasicv2", "CBM BASIC V2"),
            ("Pseudo Code", "pseudo", "Pseudo-code representation")
        ]
        
        for tab_name, format_key, description in formats:
            frame = tk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            
            # Header
            header = tk.Label(frame, text=f"{tab_name} - {description}", 
                             font=("Arial", 9, "bold"), bg="lightgray")
            header.pack(fill=tk.X)
            
            # Text widget
            text_widget = tk.Text(frame, wrap=tk.WORD, font=("Courier", 9))
            text_widget.pack(fill=tk.BOTH, expand=True)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.output_texts[format_key] = text_widget
            self.tab_frames[format_key] = frame  # frame'i de kaydedelim
    
    def setup_status_bar(self, parent):
        """Status bar"""
        status_frame = tk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=2)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır - Disk dosyası seçin")
        
        status_bar = tk.Label(status_frame, textvariable=self.status_var,
                             relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 9))
        status_bar.pack(fill=tk.X)
        
    def setup_logging(self):
        """Logging setup"""
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def select_file(self):
        """Dosya seçim dialogu"""
        file_path = filedialog.askopenfilename(
            title="C64 Disk/File Seç",
            filetypes=[
                ("All C64 Files", "*.d64 *.d71 *.d81 *.d84 *.tap *.t64 *.p00 *.prg"),
                ("Disk Images", "*.d64 *.d71 *.d81 *.d84"),
                ("Tape Images", "*.tap *.t64"),
                ("Program Files", "*.p00 *.prg"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.d64_path.set(file_path)
            self.load_image(file_path)
            
    def load_image(self, file_path):
        """Disk/file image'ını yükle ve analiz et"""
        try:
            self.status_var.set("📁 Dosya yükleniyor...")
            disk_data, ext = read_image(file_path)
            
            if ext in (".d64", ".d71", ".d81", ".d84"):
                self.entries = read_directory(disk_data, ext)
            elif ext == ".t64":
                self.entries = read_t64_directory(disk_data)
            elif ext == ".tap":
                self.entries = read_tap_directory(disk_data)
            else:
                # Single PRG file
                self.entries = [{
                    "filename": Path(file_path).name,
                    "track": 0,
                    "sector": 0,
                    "size": len(disk_data),
                    "address": 0,
                    "offset": 0
                }]
            
            self.analyze_and_update_file_list()
            self.status_var.set(f"✅ Yüklendi: {len(self.entries)} dosya bulundu")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya yüklenirken hata: {e}")
            self.status_var.set("❌ Hata!")
            
    def analyze_and_update_file_list(self):
        """Dosya listesini analiz et ve gelişmiş bilgilerle güncelle"""
        # Eski verileri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Her dosyayı analiz et
        for entry in self.entries:
            try:
                # Temel bilgiler
                filename = entry["filename"]
                size = entry.get("size", "N/A")
                track_sector = f"{entry.get('track', 'N/A')}/{entry.get('sector', 'N/A')}"
                
                # Dosya tipini ve start address'i tespit et
                file_type, start_addr_info, content_info = self.analyze_file_content(entry)
                
                # Treeview'e ekle
                self.tree.insert("", "end", values=(
                    filename,
                    file_type,
                    start_addr_info,
                    content_info,
                    track_sector,
                    size
                ))
                
            except Exception as e:
                self.tree.insert("", "end", values=(
                    entry["filename"],
                    "ERROR",
                    "N/A",
                    "N/A",
                    "N/A",
                    f"Error: {e}"
                ))
    
    def analyze_file_content(self, entry):
        """Dosya içeriğini analiz et - tip, start address, content bilgisi"""
        try:
            # PRG verisini çıkar
            disk_data, ext = read_image(self.d64_path.get())
            
            if ext in (".d64", ".d71", ".d81", ".d84"):
                prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
            elif ext == ".t64":
                prg_data = extract_t64_prg(disk_data, entry["offset"], entry.get("size", 1000))
            elif ext == ".tap":
                prg_data = extract_tap_prg(disk_data, entry["offset"], entry.get("size", 1000))
            else:
                prg_data = disk_data
            
            if not prg_data or len(prg_data) < 2:
                return "EMPTY", "N/A", "Boş dosya"
            
            # Start address
            start_addr = prg_data[0] + (prg_data[1] << 8)
            start_addr_info = f"${start_addr:04X} ({start_addr})"
            
            # Dosya tipini belirle
            if start_addr == 0x0801:  # BASIC start
                file_type = "BASIC"
                content_info = self.analyze_basic_content(prg_data)
            elif start_addr >= 0x0800 and start_addr <= 0x9FFF:
                file_type = "PRG"
                content_info = self.analyze_machine_code(prg_data)
            elif start_addr >= 0xA000:
                file_type = "HI-MEM"
                content_info = "Yüksek bellek programı"
            else:
                file_type = "DATA"
                content_info = "Veri dosyası"
            
            return file_type, start_addr_info, content_info
            
        except Exception as e:
            return "ERROR", "N/A", f"Analiz hatası: {e}"
    
    def analyze_basic_content(self, prg_data):
        """BASIC program içeriğini analiz et"""
        try:
            # BASIC token analizi (basit)
            code_data = prg_data[2:]  # Skip load address
            
            # İlk satır numarasını bul
            if len(code_data) >= 4:
                line_num = code_data[2] + (code_data[3] << 8)
                return f"BASIC program, ilk satır: {line_num}"
            else:
                return "BASIC program (kısa)"
                
        except:
            return "BASIC program (analiz hatası)"
    
    def analyze_machine_code(self, prg_data):
        """Makine kodu analiz et"""
        try:
            code_data = prg_data[2:]
            
            if len(code_data) == 0:
                return "Boş kod"
            
            # İlk birkaç byte'ı kontrol et
            first_bytes = " ".join(f"${b:02X}" for b in code_data[:min(6, len(code_data))])
            
            # Yaygın pattern'leri kontrol et
            if len(code_data) >= 3:
                if code_data[0] == 0x4C:  # JMP
                    jump_addr = code_data[1] + (code_data[2] << 8)
                    return f"Makine kodu, JMP ${jump_addr:04X}, bytes: {first_bytes}"
                elif code_data[0] == 0xA9:  # LDA #
                    return f"Makine kodu, LDA #{code_data[1]:02X}, bytes: {first_bytes}"
            
            return f"Makine kodu, bytes: {first_bytes}"
            
        except:
            return "Makine kodu (analiz hatası)"
    
    def on_file_select(self, event):
        """Dosya seçildiğinde içeriği göster"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            filename = item["values"][0]
            
            # Dosyayı bul ve analiz et
            entry = next((e for e in self.entries if e["filename"] == filename), None)
            if entry:
                self.show_file_content_preview(entry)
    
    def show_file_content_preview(self, entry):
        """Seçili dosyanın içeriği önizlemesini göster"""
        try:
            # PRG verisini çıkar
            disk_data, ext = read_image(self.d64_path.get())
            
            if ext in (".d64", ".d71", ".d81", ".d84"):
                prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
            elif ext == ".t64":
                prg_data = extract_t64_prg(disk_data, entry["offset"], entry.get("size", 1000))
            elif ext == ".tap":
                prg_data = extract_tap_prg(disk_data, entry["offset"], entry.get("size", 1000))
            else:
                prg_data = disk_data
            
            if not prg_data or len(prg_data) < 2:
                # Boş dosya için mesaj göster
                for text_widget in self.output_texts.values():
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(1.0, f"Dosya '{entry['filename']}' boş veya okunamıyor.")
                return
            
            # Start address bilgisi
            start_addr = prg_data[0] + (prg_data[1] << 8)
            
            # Kısa disassembly önizlemesi (ilk 20 satır)
            try:
                from improved_disassembler import ImprovedDisassembler
                disasm = ImprovedDisassembler(start_addr, prg_data[2:], output_format='asm')
                preview = disasm.disassemble_to_format(prg_data)
                
                # İlk 20 satır al
                lines = preview.split('\n')[:20]
                preview_text = '\n'.join(lines)
                if len(preview.split('\n')) > 20:
                    preview_text += f"\n\n... ({len(preview.split('\n')) - 20} satır daha)"
                
                # Assembly tab'ına önizleme ekle
                if 'asm' in self.output_texts:
                    self.output_texts['asm'].delete(1.0, tk.END)
                    self.output_texts['asm'].insert(1.0, preview_text)
                    
                # Diğer tab'lara da kısa bilgi ekle
                info_text = f"""Dosya: {entry['filename']}
Start Address: ${start_addr:04X} ({start_addr})
Boyut: {len(prg_data)} byte
Kod Boyutu: {len(prg_data[2:])} byte

Tam disassembly için dosyaya çift tıklayın."""

                for tab_name, text_widget in self.output_texts.items():
                    if tab_name != 'asm':
                        text_widget.delete(1.0, tk.END)
                        text_widget.insert(1.0, info_text)
                        
            except Exception as e:
                # Hata durumunda basit bilgi göster
                error_text = f"""Dosya: {entry['filename']}
Start Address: ${start_addr:04X} ({start_addr})
Boyut: {len(prg_data)} byte

Önizleme hatası: {e}
Tam disassembly için dosyaya çift tıklayın."""
                
                for text_widget in self.output_texts.values():
                    text_widget.delete(1.0, tk.END)
                    text_widget.insert(1.0, error_text)
                    
        except Exception as e:
            print(f"Önizleme hatası: {e}")
    
    def on_file_double_click(self, event):
        """Dosyaya çift tıklandığında"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            filename = item["values"][0]
            
            # Dosyayı bul ve çevir
            entry = next((e for e in self.entries if e["filename"] == filename), None)
            if entry:
                self.convert_single_file(entry)
    
    def convert_single_file(self, entry):
        """Tek dosyayı çevir - gelişmiş disassembler sistemi"""
        try:
            filename = entry["filename"]
            self.status_var.set(f"🔄 Çeviriliyor: {filename}")
            
            # PRG verisini çıkar
            disk_data, ext = read_image(self.d64_path.get())
            
            if ext in (".d64", ".d71", ".d81", ".d84"):
                prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
            elif ext == ".t64":
                prg_data = extract_t64_prg(disk_data, entry["offset"], entry.get("size", 1000))
            elif ext == ".tap":
                prg_data = extract_tap_prg(disk_data, entry["offset"], entry.get("size", 1000))
            else:
                prg_data = disk_data
            
            if not prg_data or len(prg_data) < 2:
                messagebox.showerror("Hata", "PRG verisi okunamadı")
                return
            
            # Start address
            start_addr = prg_data[0] + (prg_data[1] << 8)
            code_data = prg_data[2:]
            
            # BASIC program kontrolü
            if start_addr == 0x0801:
                self.convert_basic_program(prg_data, filename)
            else:
                self.convert_assembly_program(prg_data, filename, start_addr, code_data)
            
            # İşlenen dosya listesine ekle
            self.add_to_processed_files(filename, entry)
            
            self.status_var.set(f"✅ Tamamlandı: {filename}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Çeviri hatası: {e}")
            self.status_var.set("❌ Hata!")
    
    def convert_basic_program(self, prg_data, filename):
        """BASIC program çevirisi"""
        try:
            # PETCAT ile detokenize et
            basic_lines = self.basic_parser.detokenize_basic(prg_data)
            
            # Assembly tab'ına BASIC koy
            self.output_texts["asm"].delete(1.0, tk.END)
            self.output_texts["asm"].insert(tk.END, f"; BASIC Program: {filename}\\n")
            self.output_texts["asm"].insert(tk.END, "\\n".join([f"; {line}" for line in basic_lines]))
            
            # Diğer formatlara da BASIC'i koy
            for format_key, text_widget in self.output_texts.items():
                if format_key != "asm":
                    text_widget.delete(1.0, tk.END)
                    if format_key == "c":
                        text_widget.insert(tk.END, f"/* BASIC Program: {filename} */\\n")
                        text_widget.insert(tk.END, "\\n".join([f"/* {line} */" for line in basic_lines]))
                    elif format_key in ["qbasic", "commodorebasicv2"]:
                        text_widget.insert(tk.END, f"REM BASIC Program: {filename}\\n")
                        text_widget.insert(tk.END, "\\n".join(basic_lines))
                    else:
                        text_widget.insert(tk.END, f"// BASIC Program: {filename}\\n")
                        text_widget.insert(tk.END, "\\n".join([f"// {line}" for line in basic_lines]))
            
        except Exception as e:
            # BASIC hatalıysa asm olarak işle
            self.convert_assembly_program(prg_data, filename, 0x0801, prg_data[2:])
    
    def convert_assembly_program(self, prg_data, filename, start_addr, code_data):
        """Assembly program çevirisi - gelişmiş disassembler sistemi"""
        try:
            selected_disassembler = self.disassembler_var.get()
            
            # Her format için çeviri yap
            for format_key in self.output_texts.keys():
                try:
                    result_code = self.perform_disassembly(selected_disassembler, prg_data, 
                                                         start_addr, code_data, format_key)
                    
                    # Sonucu göster
                    self.output_texts[format_key].delete(1.0, tk.END)
                    self.output_texts[format_key].insert(tk.END, result_code)
                    
                except Exception as e:
                    self.output_texts[format_key].delete(1.0, tk.END)
                    self.output_texts[format_key].insert(tk.END, f"// Error in {format_key} format: {e}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Assembly çeviri hatası: {e}")
    
    def perform_disassembly(self, disassembler_type, prg_data, start_addr, code_data, output_format):
        """Disassembly işlemini gerçekleştir"""
        if disassembler_type == "improved":
            disasm = ImprovedDisassembler(start_addr, code_data, 
                                        output_format=output_format,
                                        use_illegal_opcodes=self.use_illegal_opcodes.get())
            return disasm.disassemble_to_format(prg_data)
            
        elif disassembler_type == "py65_professional":
            if PY65_AVAILABLE:
                disasm = Py65ProfessionalDisassembler(start_addr, code_data,
                                                    use_illegal_opcodes=self.use_illegal_opcodes.get())
                return disasm.disassemble_to_format(prg_data, output_format)
            else:
                return f"// py65 not available, falling back to improved\\n" + \
                       self.perform_disassembly("improved", prg_data, start_addr, code_data, output_format)
        
        elif disassembler_type == "advanced":
            disasm = AdvancedDisassembler(start_addr, code_data, 
                                        output_format=output_format,
                                        use_illegal_opcodes=self.use_illegal_opcodes.get())
            return disasm.disassemble_simple(prg_data)
            
        elif disassembler_type == "basic":
            disasm = Disassembler(start_addr, code_data)
            asm_lines = disasm.disassemble()
            if output_format == "asm":
                return "\\n".join(asm_lines)
            else:
                return f"// Basic disassembler only produces assembly\\n// Format {output_format} not supported\\n" + \
                       "\\n".join([f"// {line}" for line in asm_lines])
        
        else:
            return f"// Unknown disassembler: {disassembler_type}"
    
    def add_to_processed_files(self, filename, entry):
        """İşlenen dosya listesine ekle"""
        processed_info = {
            "filename": filename,
            "timestamp": datetime.datetime.now().isoformat(),
            "disassembler": self.disassembler_var.get(),
            "illegal_opcodes": self.use_illegal_opcodes.get(),
            "start_addr": entry.get("address", 0),
            "size": entry.get("size", 0)
        }
        
        # Listenin başına ekle (en son işlenen üstte)
        self.processed_files.insert(0, processed_info)
        
        # Maksimum 100 dosya tut
        if len(self.processed_files) > 100:
            self.processed_files = self.processed_files[:100]
        
        # Kaydet
        self.save_processed_files()
    
    def load_processed_files(self):
        """İşlenen dosya listesini yükle"""
        try:
            if os.path.exists("logs/processed_files.json"):
                with open("logs/processed_files.json", "r", encoding="utf-8") as f:
                    self.processed_files = json.load(f)
        except:
            self.processed_files = []
    
    def save_processed_files(self):
        """İşlenen dosya listesini kaydet"""
        try:
            os.makedirs("logs", exist_ok=True)
            with open("logs/processed_files.json", "w", encoding="utf-8") as f:
                json.dump(self.processed_files, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Processed files kaydetme hatası: {e}")
    
    def show_processed_files(self):
        """İşlenen dosyalar penceresini göster - Excel benzeri"""
        processed_window = tk.Toplevel(self.root)
        processed_window.title("İşlenen Dosyalar - Excel Benzeri")
        processed_window.geometry("800x600")
        
        # Treeview
        columns = ("filename", "timestamp", "disassembler", "start_addr", "size")
        tree = ttk.Treeview(processed_window, columns=columns, show="headings")
        
        tree.heading("filename", text="Dosya Adı")
        tree.heading("timestamp", text="İşlem Zamanı")
        tree.heading("disassembler", text="Disassembler")
        tree.heading("start_addr", text="Start Address")
        tree.heading("size", text="Boyut")
        
        # En son işlenenler üstte
        for processed in self.processed_files:
            tree.insert("", "end", values=(
                processed["filename"],
                processed["timestamp"][:19],  # Remove microseconds
                processed["disassembler"],
                f"${processed.get('start_addr', 0):04X}",
                processed.get("size", 0)
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        tk.Button(processed_window, text="Kapat", 
                 command=processed_window.destroy).pack(pady=5)
    
    def show_file_search(self):
        """Dosya arama penceresi"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Dosya Arama Sistemi")
        search_window.geometry("600x400")
        
        tk.Label(search_window, text="Dosya Arama - Sistem Genelinde C64 Dosyaları", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        search_frame = tk.Frame(search_window)
        search_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(search_frame, text="Arama dizini:").pack(side=tk.LEFT)
        search_dir = tk.StringVar(value=os.getcwd())
        tk.Entry(search_frame, textvariable=search_dir, width=50).pack(side=tk.LEFT, padx=5)
        
        tk.Button(search_frame, text="🔍 Ara", 
                 command=lambda: self.perform_file_search(search_dir.get(), search_window)).pack(side=tk.LEFT)
    
    def perform_file_search(self, search_dir, window):
        """Dosya arama işlemi"""
        try:
            c64_files = []
            extensions = [".d64", ".d71", ".d81", ".d84", ".tap", ".t64", ".p00", ".prg"]
            
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        c64_files.append(os.path.join(root, file))
            
            # Sonuçları göster
            result_frame = tk.Frame(window)
            result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            tk.Label(result_frame, text=f"{len(c64_files)} C64 dosyası bulundu:", 
                    font=("Arial", 10, "bold")).pack()
            
            listbox = tk.Listbox(result_frame)
            listbox.pack(fill=tk.BOTH, expand=True)
            
            for file_path in c64_files:
                listbox.insert(tk.END, file_path)
            
            def load_selected():
                selection = listbox.curselection()
                if selection:
                    selected_file = c64_files[selection[0]]
                    self.d64_path.set(selected_file)
                    self.load_image(selected_file)
                    window.destroy()
            
            tk.Button(result_frame, text="Seçili Dosyayı Yükle", 
                     command=load_selected).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Arama hatası: {e}")
    
    def refresh_disk_content(self):
        """Disk içeriğini yenile"""
        if self.d64_path.get():
            self.load_image(self.d64_path.get())
        else:
            messagebox.showwarning("Uyarı", "Önce bir disk dosyası seçin!")
    
    def convert_selected_files(self):
        """Seçili dosyaları çevir"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Dosya seçin!")
            return
        
        # İlk seçili dosyayı çevir
        item = self.tree.item(selection[0])
        filename = item["values"][0]
        entry = next((e for e in self.entries if e["filename"] == filename), None)
        if entry:
            self.convert_single_file(entry)
    
    def convert_all_files(self):
        """Tüm dosyaları çevir"""
        if not self.entries:
            messagebox.showwarning("Uyarı", "Dosya bulunamadı!")
            return
        
        # İlk dosyayı çevir (örnek)
        self.convert_single_file(self.entries[0])

def start_restored_gui():
    """Restored GUI'yi başlat"""
    root = tk.Tk()
    app = D64ConverterRestoredGUI(root)
    root.mainloop()

if __name__ == "__main__":
    start_restored_gui()
