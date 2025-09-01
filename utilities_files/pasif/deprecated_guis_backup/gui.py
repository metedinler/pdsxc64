#!/usr/bin/env python3
"""
D64 Converter - GUI Manager
Modern Tkinter tabanlı grafik arayüz - X1 GUI Integration

ADIM 5: GUI Integration + X1 Features
- Modern dark theme arayüz
- X1 GUI'nin tüm fonksiyonları
- 4 panel layout: Directory, Disassembly, Decompiler, Console
- Disk imajı okuma ve dosya seçimi
- Disassembler formatları: Assembly, C, QBasic, PDSX, Pseudo
- Decompiler sistemleri: C, C++, QBasic, Assembly
- BASIC detokenizers: Parser, Petcat, C64List
- Analiz araçları: Illegal opcode, Sprite, SID, Charset

Author: D64 Converter Team
Version: 5.0 (X1 Integration)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font
import threading
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Core system imports
from unified_decompiler import UnifiedDecompiler
from enhanced_c64_memory_manager import C64MemoryMapManager
from code_analyzer import CodeAnalyzer, PatternType

# X1 GUI imports - safer imports with defaults
try:
    from d64_reader import D64Reader
except ImportError:
    D64Reader = None

try:
    from enhanced_d64_reader import EnhancedD64Reader, EnhancedD64ReaderWrapper
except ImportError:
    EnhancedD64Reader = None
    EnhancedD64ReaderWrapper = None

try:
    from c1541_python_emulator import C1541PythonEmulator
except ImportError:
    C1541PythonEmulator = None

try:
    from advanced_disassembler import AdvancedDisassembler
except ImportError:
    AdvancedDisassembler = None

try:
    from improved_disassembler import ImprovedDisassembler
except ImportError:
    ImprovedDisassembler = None

try:
    from parser import Parser
except ImportError:
    Parser = None

try:
    from c64_basic_parser import C64BasicParser
except ImportError:
    C64BasicParser = None

try:
    from sprite_converter import SpriteConverter
except ImportError:
    SpriteConverter = None

try:
    from sid_converter import SIDConverter
except ImportError:
    SIDConverter = None

try:
    from petcat_detokenizer import PetcatDetokenizer
except ImportError:
    PetcatDetokenizer = None

# Decompiler imports
try:
    from decompiler_qbasic import DecompilerQBasic
    DECOMPILER_QBASIC_AVAILABLE = True
except ImportError:
    DECOMPILER_QBASIC_AVAILABLE = False

try:
    from decompiler_cpp import DecompilerCPP
    DECOMPILER_CPP_AVAILABLE = True
except ImportError:
    DECOMPILER_CPP_AVAILABLE = False

try:
    from decompiler_c2 import DecompilerC2
    DECOMPILER_C2_AVAILABLE = True
except ImportError:
    DECOMPILER_C2_AVAILABLE = False

try:
    from decompiler_c import DecompilerC
    DECOMPILER_C_AVAILABLE = True
except ImportError:
    DECOMPILER_C_AVAILABLE = False

try:
    from decompiler import Decompiler
    DECOMPILER_AVAILABLE = True
except ImportError:
    DECOMPILER_AVAILABLE = False

# Logging
import logging
logging.basicConfig(level=logging.INFO)

class ModernStyle:
    """Modern light theme color scheme - Default Light"""
    
    # Light theme colors (default)
    BG_DARK = "#ffffff"          # Ana arkaplan - beyaz
    BG_SECONDARY = "#f8f9fa"     # İkincil arkaplan - açık gri
    BG_TERTIARY = "#e9ecef"      # Üçüncül arkaplan - daha koyu gri
    FG_PRIMARY = "#212529"       # Ana metin - koyu siyah
    FG_SECONDARY = "#495057"     # İkincil metin - orta gri
    FG_ACCENT = "#0d6efd"        # Vurgu rengi - mavi
    FG_SUCCESS = "#198754"       # Başarı - yeşil
    FG_WARNING = "#fd7e14"       # Uyarı - turuncu
    FG_ERROR = "#dc3545"         # Hata - kırmızı
    
    # Syntax highlighting - light theme
    SYNTAX_KEYWORD = "#0000ff"   # Mavi - anahtar kelimeler
    SYNTAX_STRING = "#008000"    # Yeşil - string'ler
    SYNTAX_COMMENT = "#808080"   # Gri - yorumlar
    SYNTAX_NUMBER = "#ff0000"    # Kırmızı - sayılar
    SYNTAX_OPERATOR = "#000000"  # Siyah - operatörler
    
    @staticmethod
    def get_light_theme():
        """Aydınlık tema"""
        return {
            'BG_DARK': "#ffffff",
            'BG_SECONDARY': "#f8f9fa", 
            'BG_TERTIARY': "#e9ecef",
            'FG_PRIMARY': "#212529",
            'FG_SECONDARY': "#495057",
            'FG_ACCENT': "#0d6efd",
            'FG_SUCCESS': "#198754",
            'FG_WARNING': "#fd7e14",
            'FG_ERROR': "#dc3545",
            'SYNTAX_KEYWORD': "#0000ff",
            'SYNTAX_STRING': "#008000",
            'SYNTAX_COMMENT': "#808080",
            'SYNTAX_NUMBER': "#ff0000",
            'SYNTAX_OPERATOR': "#000000"
        }
    
    @staticmethod
    def get_dark_theme():
        """Karanlık tema"""
        return {
            'BG_DARK': "#1e1e1e",
            'BG_SECONDARY': "#2d2d30",
            'BG_TERTIARY': "#3e3e42",
            'FG_PRIMARY': "#ffffff",
            'FG_SECONDARY': "#cccccc",
            'FG_ACCENT': "#0078d4",
            'FG_SUCCESS': "#4ec9b0",
            'FG_WARNING': "#ffc107",
            'FG_ERROR': "#f44336",
            'SYNTAX_KEYWORD': "#569cd6",
            'SYNTAX_STRING': "#ce9178",
            'SYNTAX_COMMENT': "#6a9955",
            'SYNTAX_NUMBER': "#b5cea8",
            'SYNTAX_OPERATOR': "#d4d4d4"
        }
    
    def __init__(self, dark_mode=False):
        theme = self.get_dark_theme() if dark_mode else self.get_light_theme()
        for key, value in theme.items():
            setattr(self, key, value)

class DiskDirectoryPanel(tk.Frame):
    """Disk imajı directory listesi - X1 GUI tarzı"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.entries = []
        self.selected_entry = None
        self.parent_gui = None
        self.setup_ui()
    
    def setup_ui(self):
        """Directory panel UI setup"""
        # Header
        header_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(header_frame, text="📁 Disk Directory", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_PRIMARY, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # File controls
        controls_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        controls_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(controls_frame, text="📂 Seç", command=self.select_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="🔍 Dosya Bul", command=self.find_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="📋 İşlenenler", command=self.show_processed_files).pack(side=tk.LEFT, padx=2)
        
        # Directory tree
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview columns
        columns = ("filename", "filetype", "size", "start_addr", "end_addr")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Column headers
        self.tree.heading("filename", text="Dosya Adı")
        self.tree.heading("filetype", text="Tip")
        self.tree.heading("size", text="Boyut")
        self.tree.heading("start_addr", text="Start")
        self.tree.heading("end_addr", text="End")
        
        # Column widths
        self.tree.column("filename", width=150)
        self.tree.column("filetype", width=80)
        self.tree.column("size", width=80)
        self.tree.column("start_addr", width=80)
        self.tree.column("end_addr", width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Selection binding
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)
        self.tree.bind("<Double-1>", self.on_file_double_click)
        
        # Analysis buttons
        analysis_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        analysis_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(analysis_frame, text="🚫 Illegal Analiz", command=self.analyze_illegal_opcodes).pack(side=tk.LEFT, padx=2)
        ttk.Button(analysis_frame, text="🎮 Sprite Analiz", command=self.analyze_sprites).pack(side=tk.LEFT, padx=2)
        ttk.Button(analysis_frame, text="🎵 SID Analiz", command=self.analyze_sid).pack(side=tk.LEFT, padx=2)
        ttk.Button(analysis_frame, text="🔤 Charset Analiz", command=self.analyze_charset).pack(side=tk.LEFT, padx=2)
    
    def select_file(self):
        """Dosya seçim dialogu - X1 tarzı"""
        try:
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
                ('All Files', '*.*')
            ]
            
            file_path = filedialog.askopenfilename(
                title="Commodore 64 File Selector",
                filetypes=file_types,
                initialdir=os.path.expanduser("~\\Downloads")
            )
            
            if file_path:
                self.load_image(file_path)
                
        except Exception as e:
            messagebox.showerror("Dosya Seçim Hatası", f"Hata: {e}")
    
    def load_image(self, file_path):
        """Disk imajını yükle - X1 tarzı"""
        try:
            if self.parent_gui:
                self.parent_gui.update_status("Disk dosyası yükleniyor...")
            
            # Dosya uzantısını kontrol et
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext in ['.d64', '.d71', '.d81', '.d84']:
                # Disk imajı okuma - safe reader selection
                if EnhancedD64ReaderWrapper and os.path.exists("enhanced_d64_reader.py"):
                    reader = EnhancedD64ReaderWrapper(file_path)
                    self.log_message("Enhanced D64 Reader kullanıldı", "INFO")
                elif D64Reader:
                    reader = D64Reader(file_path)
                    self.log_message("Standard D64 Reader kullanıldı", "INFO")
                else:
                    raise ImportError("D64 Reader modülü bulunamadı")
                
                self.entries = reader.list_files()
                
            elif ext in ['.t64']:
                # T64 tape okuma
                self.entries = self.load_t64_file(file_path)
                
            elif ext in ['.prg', '.p00']:
                # PRG dosyası direkt
                self.entries = self.load_prg_file(file_path)
                
            else:
                # Diğer formatlar
                self.entries = self.load_generic_file(file_path)
            
            # Directory'yi güncelle
            self.update_directory_display()
            
            if self.parent_gui:
                self.parent_gui.update_status(f"Dosya yüklendi: {len(self.entries)} dosya bulundu")
                
        except Exception as e:
            if self.parent_gui:
                self.parent_gui.log_message(f"Dosya yükleme hatası: {e}", "ERROR")
            messagebox.showerror("Dosya Yükleme Hatası", f"Hata: {e}")
    
    def update_directory_display(self):
        """Directory görünümünü güncelle"""
        # Eski entryleri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yeni entryleri ekle
        for entry in self.entries:
            filename = entry.get('filename', 'Unknown')
            filetype = entry.get('filetype', 'PRG')
            size = entry.get('size', 0)
            start_addr = entry.get('start_address', 0)
            end_addr = entry.get('end_address', 0)
            
            # Format değerleri
            start_str = f"${start_addr:04X}" if start_addr else ""
            end_str = f"${end_addr:04X}" if end_addr else ""
            size_str = f"{size}" if size else ""
            
            self.tree.insert("", tk.END, values=(filename, filetype, size_str, start_str, end_str))
    
    def on_file_select(self, event):
        """Dosya seçildiğinde"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            filename = item['values'][0]
            
            # Seçili dosyayı bul
            for entry in self.entries:
                if entry.get('filename') == filename:
                    self.selected_entry = entry
                    break
            
            if self.parent_gui and self.selected_entry:
                self.parent_gui.on_file_selected(self.selected_entry)
    
    def on_file_double_click(self, event):
        """Dosya çift tıklanınca otomatik analiz"""
        if self.selected_entry and self.parent_gui:
            self.parent_gui.auto_analyze_file(self.selected_entry)
    
    def find_files(self):
        """X1 tarzı dosya bulma"""
        # Threading ile dosya arama
        threading.Thread(target=self._find_files_thread, daemon=True).start()
    
    def _find_files_thread(self):
        """Dosya arama thread'i"""
        try:
            if self.parent_gui:
                self.parent_gui.update_status("C64 dosyaları aranıyor...")
            
            supported_extensions = ['.d64', '.d71', '.d81', '.d84', '.t64', '.tap', '.prg', '.p00']
            found_files = []
            
            search_dirs = [
                os.path.expanduser("~\\Downloads"),
                os.path.expanduser("~\\Documents"),
                os.path.expanduser("~\\Desktop")
            ]
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for root_dir, dirs, files in os.walk(search_dir):
                        for file in files:
                            if os.path.splitext(file)[1].lower() in supported_extensions:
                                found_files.append(os.path.join(root_dir, file))
                                if len(found_files) >= 20:
                                    break
                        if len(found_files) >= 20:
                            break
                if len(found_files) >= 20:
                    break
            
            # Sonuçları göster
            if found_files:
                self.parent_gui.root.after(0, lambda: self.show_found_files(found_files))
            else:
                if self.parent_gui:
                    self.parent_gui.update_status("C64 dosyası bulunamadı")
                    
        except Exception as e:
            if self.parent_gui:
                self.parent_gui.log_message(f"Dosya arama hatası: {e}", "ERROR")
    
    def show_found_files(self, files):
        """Bulunan dosyaları göster"""
        # Dosya seçim penceresi
        file_window = tk.Toplevel(self.parent_gui.root if self.parent_gui else None)
        file_window.title("Bulunan C64 Dosyaları")
        file_window.geometry("600x400")
        file_window.grab_set()
        
        tk.Label(file_window, text=f"Bulunan C64 dosyaları ({len(files)} adet):").pack(pady=10)
        
        # Listbox
        listbox_frame = tk.Frame(file_window)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Dosyaları listele
        for file_path in files:
            filename = os.path.basename(file_path)
            ext = os.path.splitext(filename)[1].upper()
            try:
                size = os.path.getsize(file_path)
                listbox.insert(tk.END, f"{filename} ({ext}, {size} bytes) - {file_path}")
            except:
                listbox.insert(tk.END, f"{filename} ({ext}) - {file_path}")
        
        # Butonlar
        button_frame = tk.Frame(file_window)
        button_frame.pack(pady=10)
        
        def select_from_list():
            selection = listbox.curselection()
            if selection:
                selected_file = files[selection[0]]
                file_window.destroy()
                self.load_image(selected_file)
            else:
                messagebox.showwarning("Seçim Yok", "Lütfen bir dosya seçin")
        
        tk.Button(button_frame, text="Seç", command=select_from_list).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="İptal", command=file_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_processed_files(self):
        """İşlenmiş dosyaları göster"""
        # Çıktı klasörlerini kontrol et
        output_dirs = ["asm_files", "c_files", "qbasic_files", "pdsx_files", "pseudo_files"]
        found_files = []
        
        for output_dir in output_dirs:
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    found_files.append(os.path.join(output_dir, file))
        
        if found_files:
            # Dosya listesi penceresi
            proc_window = tk.Toplevel(self.parent_gui.root if self.parent_gui else None)
            proc_window.title("İşlenmiş Dosyalar")
            proc_window.geometry("500x400")
            
            tk.Label(proc_window, text=f"İşlenmiş dosyalar ({len(found_files)} adet):").pack(pady=10)
            
            listbox = tk.Listbox(proc_window)
            listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            for file_path in found_files:
                listbox.insert(tk.END, file_path)
                
            tk.Button(proc_window, text="Kapat", command=proc_window.destroy).pack(pady=10)
        else:
            messagebox.showinfo("İşlenmiş Dosyalar", "Henüz işlenmiş dosya bulunmuyor.")
    
    def analyze_illegal_opcodes(self):
        """Illegal opcode analizi"""
        if not self.selected_entry:
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_illegal_opcodes(self.selected_entry)
    
    def analyze_sprites(self):
        """Sprite analizi"""
        if not self.selected_entry:
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_sprites(self.selected_entry)
    
    def analyze_sid(self):
        """SID müzik analizi"""
        if not self.selected_entry:
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_sid(self.selected_entry)
    
    def analyze_charset(self):
        """Karakter seti analizi"""
        if not self.selected_entry:
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_charset(self.selected_entry)
    
    def load_t64_file(self, file_path):
        """T64 dosyası yükle"""
        # T64 okuma implementasyonu
        entries = []
        try:
            with open(file_path, 'rb') as f:
                # T64 header okuma
                signature = f.read(32)
                if b'C64-TAPE-RAW' not in signature:
                    raise ValueError("Geçersiz T64 dosyası")
                
                # Basit T64 parsing
                f.seek(32)
                version = int.from_bytes(f.read(2), 'little')
                max_entries = int.from_bytes(f.read(2), 'little')
                used_entries = int.from_bytes(f.read(2), 'little')
                
                # Directory entries
                f.seek(64)
                for i in range(used_entries):
                    entry_type = f.read(1)[0]
                    file_type = f.read(1)[0]
                    start_addr = int.from_bytes(f.read(2), 'little')
                    end_addr = int.from_bytes(f.read(2), 'little')
                    f.read(2)  # Reserved
                    offset = int.from_bytes(f.read(4), 'little')
                    f.read(4)  # Reserved
                    filename_raw = f.read(16)
                    filename = filename_raw.decode('ascii', errors='ignore').strip('\x00')
                    
                    if entry_type == 1:  # File entry
                        entries.append({
                            'filename': filename,
                            'filetype': 'PRG',
                            'start_address': start_addr,
                            'end_address': end_addr,
                            'size': end_addr - start_addr + 1,
                            'file_offset': offset,
                            'source_file': file_path
                        })
                        
        except Exception as e:
            print(f"T64 okuma hatası: {e}")
            # Fallback olarak dosyanın kendisini ekle
            entries = [{
                'filename': os.path.basename(file_path),
                'filetype': 'T64',
                'start_address': 0x0801,
                'end_address': 0x0801,
                'size': os.path.getsize(file_path),
                'source_file': file_path
            }]
        
        return entries
    
    def load_prg_file(self, file_path):
        """PRG dosyası yükle"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                
            if len(data) >= 2:
                start_addr = data[0] + (data[1] << 8)
                end_addr = start_addr + len(data) - 3
            else:
                start_addr = 0x0801
                end_addr = 0x0801
            
            return [{
                'filename': os.path.basename(file_path),
                'filetype': 'PRG',
                'start_address': start_addr,
                'end_address': end_addr,
                'size': len(data),
                'source_file': file_path,
                'prg_data': data
            }]
            
        except Exception as e:
            print(f"PRG okuma hatası: {e}")
            return []
    
    def load_generic_file(self, file_path):
        """Genel dosya yükleme"""
        try:
            size = os.path.getsize(file_path)
            return [{
                'filename': os.path.basename(file_path),
                'filetype': os.path.splitext(file_path)[1].upper()[1:],
                'start_address': 0x0801,
                'end_address': 0x0801 + size,
                'size': size,
                'source_file': file_path
            }]
        except Exception as e:
            print(f"Dosya okuma hatası: {e}")
            return []

class DisassemblyPanel(tk.Frame):
    """Disassembly sonuçları paneli - Sağ üst"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_code = ""
        self.current_format = "ASM"
        self.parent_gui = None
        self.setup_ui()
    
    def setup_ui(self):
        """Disassembly panel UI"""
        # Header
        header_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(header_frame, text="⚙️ Disassembly", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_PRIMARY, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Disassembler formatları
        format_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        format_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Disassembly grubu
        group1 = ttk.LabelFrame(format_frame, text="Disassembly")
        group1.pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(group1, text="Assembly", command=lambda: self.convert_format('assembly')).grid(row=0, column=0, padx=2)
        ttk.Button(group1, text="C", command=lambda: self.convert_format('c')).grid(row=0, column=1, padx=2)
        ttk.Button(group1, text="QBasic", command=lambda: self.convert_format('qbasic')).grid(row=0, column=2, padx=2)
        
        # BASIC Detokenizers grubu
        group2 = ttk.LabelFrame(format_frame, text="BASIC Detokenizers")
        group2.pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(group2, text="BASIC Parser", command=lambda: self.convert_format('basic')).grid(row=0, column=0, padx=2)
        ttk.Button(group2, text="Petcat", command=lambda: self.convert_format('petcat')).grid(row=0, column=1, padx=2)
        ttk.Button(group2, text="C64List", command=lambda: self.convert_format('c64list')).grid(row=0, column=2, padx=2)
        
        # Gelişmiş grubu
        group3 = ttk.LabelFrame(format_frame, text="Gelişmiş")
        group3.pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(group3, text="PDSX", command=lambda: self.convert_format('pdsx')).grid(row=0, column=0, padx=2)
        ttk.Button(group3, text="Pseudo", command=lambda: self.convert_format('pseudo')).grid(row=0, column=1, padx=2)
        ttk.Button(group3, text="Py65", command=lambda: self.convert_format('py65')).grid(row=0, column=2, padx=2)
        
        # Options
        options_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        options_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.use_advanced_disassembler = tk.BooleanVar(value=True)
        self.use_illegal_opcodes = tk.BooleanVar(value=False)
        self.use_py65_disassembler = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="Gelişmiş Disassembler", 
                       variable=self.use_advanced_disassembler).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="Illegal Opcode'lar", 
                       variable=self.use_illegal_opcodes).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="py65 Profesyonel", 
                       variable=self.use_py65_disassembler).pack(side=tk.LEFT, padx=5)
        
        # Code display
        self.code_display = scrolledtext.ScrolledText(self,
                                                     height=20,
                                                     bg=ModernStyle.BG_DARK,
                                                     fg=ModernStyle.FG_PRIMARY,
                                                     font=("Consolas", 10),
                                                     insertbackground=ModernStyle.FG_ACCENT)
        self.code_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status
        self.status_label = tk.Label(self, text="Hazır", bg=ModernStyle.BG_TERTIARY,
                                    fg=ModernStyle.FG_SECONDARY, font=("Arial", 9))
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def convert_format(self, format_type):
        """Format dönüştürme"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            self.parent_gui.convert_to_format(format_type, 'disassembly')
        else:
            self.update_code("Lütfen önce bir dosya seçin", format_type)
    
    def update_code(self, code, format_type=None):
        """Code display güncelle"""
        if format_type:
            self.current_format = format_type
        
        self.current_code = code
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(1.0, code)
        
        # Status güncelle
        lines = len(code.split('\n'))
        self.status_label.config(text=f"{self.current_format} - {lines} satır")

class DecompilerPanel(tk.Frame):
    """Decompiler sonuçları paneli - Sol alt"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_code = ""
        self.current_format = "C"
        self.parent_gui = None
        self.setup_ui()
    
    def setup_ui(self):
        """Decompiler panel UI"""
        # Header
        header_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(header_frame, text="🔄 Decompiler", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_PRIMARY, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Decompiler butonları
        decompiler_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        decompiler_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Decompiler grubu
        group4 = ttk.LabelFrame(decompiler_frame, text="Decompiler")
        group4.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Decompiler butonları - availability check ile
        if DECOMPILER_C_AVAILABLE:
            ttk.Button(group4, text="C Decompiler", command=lambda: self.convert_format('dec_c')).grid(row=0, column=0, padx=2)
        if DECOMPILER_C2_AVAILABLE:
            ttk.Button(group4, text="C2 Decompiler", command=lambda: self.convert_format('dec_c2')).grid(row=0, column=1, padx=2)
        if DECOMPILER_CPP_AVAILABLE:
            ttk.Button(group4, text="C++ Decompiler", command=lambda: self.convert_format('dec_cpp')).grid(row=0, column=2, padx=2)
        if DECOMPILER_QBASIC_AVAILABLE:
            ttk.Button(group4, text="QBasic Decompiler", command=lambda: self.convert_format('dec_qbasic')).grid(row=1, column=0, padx=2)
        
        ttk.Button(group4, text="ASM Decompiler", command=lambda: self.convert_format('dec_asm')).grid(row=1, column=1, padx=2)
        
        if DECOMPILER_AVAILABLE:
            ttk.Button(group4, text="Universal Decompiler", command=lambda: self.convert_format('decompiler')).grid(row=1, column=2, padx=2)
        
        # Code display
        self.code_display = scrolledtext.ScrolledText(self,
                                                     height=20,
                                                     bg=ModernStyle.BG_DARK,
                                                     fg=ModernStyle.FG_PRIMARY,
                                                     font=("Consolas", 10),
                                                     insertbackground=ModernStyle.FG_ACCENT)
        self.code_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status
        self.status_label = tk.Label(self, text="Hazır", bg=ModernStyle.BG_TERTIARY,
                                    fg=ModernStyle.FG_SECONDARY, font=("Arial", 9))
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def convert_format(self, format_type):
        """Decompiler format dönüştürme"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            self.parent_gui.convert_to_format(format_type, 'decompiler')
        else:
            self.update_code("Lütfen önce bir dosya seçin", format_type)
    
    def update_code(self, code, format_type=None):
        """Code display güncelle"""
        if format_type:
            self.current_format = format_type
        
        self.current_code = code
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(1.0, code)
        
        # Status güncelle
        lines = len(code.split('\n'))
        self.status_label.config(text=f"{self.current_format} - {lines} satır")

class HexEditor(tk.Frame):
    """Interactive hex editor widget"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.data = bytearray()
        self.start_address = 0x0801
        self.bytes_per_row = 16
        self.setup_ui()
    
    def setup_ui(self):
        """Setup hex editor interface"""
        # Header frame
        header_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(header_frame, text="Address", bg=ModernStyle.BG_SECONDARY, 
                fg=ModernStyle.FG_SECONDARY, font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Hex columns
        for i in range(self.bytes_per_row):
            tk.Label(header_frame, text=f"{i:02X}", bg=ModernStyle.BG_SECONDARY,
                    fg=ModernStyle.FG_SECONDARY, font=("Consolas", 9)).pack(side=tk.LEFT, padx=2)
        
        tk.Label(header_frame, text="ASCII", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_SECONDARY, font=("Consolas", 10, "bold")).pack(side=tk.LEFT, padx=10)
        
        # Scrollable hex area
        self.hex_frame = scrolledtext.ScrolledText(self, 
                                                  height=20, 
                                                  bg=ModernStyle.BG_DARK,
                                                  fg=ModernStyle.FG_PRIMARY,
                                                  font=("Consolas", 10),
                                                  insertbackground=ModernStyle.FG_ACCENT)
        self.hex_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def load_data(self, data: bytes, start_addr: int = 0x0801):
        """Load binary data into hex editor"""
        self.data = bytearray(data)
        self.start_address = start_addr
        self.refresh_display()
    
    def refresh_display(self):
        """Refresh hex editor display"""
        self.hex_frame.delete(1.0, tk.END)
        
        for row in range(0, len(self.data), self.bytes_per_row):
            # Address column
            addr = self.start_address + row
            line = f"{addr:04X}: "
            
            # Hex bytes
            hex_part = ""
            ascii_part = ""
            
            for col in range(self.bytes_per_row):
                if row + col < len(self.data):
                    byte = self.data[row + col]
                    hex_part += f"{byte:02X} "
                    ascii_part += chr(byte) if 32 <= byte <= 126 else "."
                else:
                    hex_part += "   "
                    ascii_part += " "
            
            line += hex_part + " | " + ascii_part + "\n"
            self.hex_frame.insert(tk.END, line)
            self.code_display.tag_configure("syntax_comment", foreground=ModernStyle.SYNTAX_COMMENT)
            self.code_display.tag_configure("syntax_number", foreground=ModernStyle.SYNTAX_NUMBER)

class AnalysisPanel(tk.Frame):
    """Code analysis results panel"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup analysis panel interface"""
        # Title
        title_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        title_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(title_frame, text="🔍 Code Analysis", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_PRIMARY, font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Analysis toggle
        self.analysis_var = tk.BooleanVar(value=True)
        analysis_check = tk.Checkbutton(title_frame, text="Enable Analysis",
                                      variable=self.analysis_var,
                                      bg=ModernStyle.BG_SECONDARY,
                                      fg=ModernStyle.FG_SECONDARY,
                                      selectcolor=ModernStyle.BG_TERTIARY,
                                      command=self.on_analysis_toggle)
        analysis_check.pack(side=tk.RIGHT, padx=5)
        
        # Analysis results
        self.results_display = scrolledtext.ScrolledText(self,
                                                        height=12,
                                                        bg=ModernStyle.BG_DARK,
                                                        fg=ModernStyle.FG_PRIMARY,
                                                        font=("Consolas", 9))
        self.results_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def on_analysis_toggle(self):
        """Handle analysis toggle"""
        if hasattr(self, 'parent_gui'):
            self.parent_gui.analysis_enabled = self.analysis_var.get()
            self.parent_gui.trigger_real_time_update()
    
    def update_analysis(self, analysis_text: str):
        """Update analysis results"""
        self.results_display.delete(1.0, tk.END)
        self.results_display.insert(1.0, analysis_text)

class ConsolePanel(tk.Frame):
    """Console output panel for logs and errors"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        """Console panel UI setup"""
        # Control panel
        control_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY, height=40)
        control_frame.pack(fill=tk.X, padx=5, pady=2)
        control_frame.pack_propagate(False)
        
        # Clear button
        clear_btn = tk.Button(control_frame, text="🗑️ Clear", 
                             command=self.clear_console,
                             bg=ModernStyle.BG_TERTIARY, fg=ModernStyle.FG_PRIMARY,
                             font=("Arial", 9), relief=tk.FLAT, padx=10)
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Auto-scroll toggle
        self.autoscroll_var = tk.BooleanVar(value=True)
        autoscroll_cb = tk.Checkbutton(control_frame, text="Auto-scroll",
                                      variable=self.autoscroll_var,
                                      bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_SECONDARY,
                                      selectcolor=ModernStyle.BG_TERTIARY,
                                      font=("Arial", 9))
        autoscroll_cb.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Console output
        self.console_display = scrolledtext.ScrolledText(self,
                                                        bg=ModernStyle.BG_DARK,
                                                        fg=ModernStyle.FG_PRIMARY,
                                                        font=("Consolas", 9),
                                                        wrap=tk.WORD,
                                                        state=tk.DISABLED)
        self.console_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure text tags for different log levels
        self.console_display.tag_configure("INFO", foreground=ModernStyle.FG_SUCCESS)
        self.console_display.tag_configure("WARNING", foreground=ModernStyle.FG_WARNING)
        self.console_display.tag_configure("ERROR", foreground=ModernStyle.FG_ERROR)
        self.console_display.tag_configure("DEBUG", foreground=ModernStyle.FG_SECONDARY)
    
    def clear_console(self):
        """Clear console output"""
        self.console_display.config(state=tk.NORMAL)
        self.console_display.delete(1.0, tk.END)
        self.console_display.config(state=tk.DISABLED)
    
    def add_log(self, message: str, level: str = "INFO"):
        """Add log message to console"""
        self.console_display.config(state=tk.NORMAL)
        
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Format message
        formatted_msg = f"[{timestamp}] {level}: {message}\n"
        
        # Insert with appropriate tag
        self.console_display.insert(tk.END, formatted_msg, level)
        
        # Auto-scroll if enabled
        if self.autoscroll_var.get():
            self.console_display.see(tk.END)
        
        self.console_display.config(state=tk.DISABLED)
        
        # Limit console history (keep last 1000 lines)
        lines = self.console_display.get(1.0, tk.END).count('\n')
        if lines > 1000:
            self.console_display.config(state=tk.NORMAL)
            self.console_display.delete(1.0, "100.0")
            self.console_display.config(state=tk.DISABLED)

class D64ConverterGUI:
    """Ana GUI Manager sınıfı - X1 Integration"""
    
    def __init__(self):
        # GUI state
        self.current_data = None
        self.current_start_addr = 0x0801
        self.analysis_enabled = True
        self.real_time_updates = True
        self.selected_entry = None
        self.entries = []
        
        # Core components - X1 imports
        self.unified_decompiler = None
        self.memory_manager = None
        self.d64_reader = None
        self.basic_parser = None
        self.sprite_converter = None
        self.sid_converter = None
        self.petcat_detokenizer = None
        
        # Logger
        self.logger = logging.getLogger(__name__)
        
        self.setup_main_window()
        self.setup_components()
        self.setup_layout()
        self.setup_menu()
        self.initialize_components()
        
        # Status
        self.update_status("D64 Converter v5.0 hazır - Dosya seçin")
    
    def setup_main_window(self):
        """Ana pencereyi kur"""
        self.root = tk.Tk()
        self.root.title("D64 Converter - Advanced Decompiler Suite v5.0 (X1 Integration)")
        self.root.geometry("1600x1000")
        self.root.configure(bg=ModernStyle.BG_DARK)
        
        # Window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def setup_components(self):
        """GUI bileşenlerini kur - 4 Panel Layout"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=ModernStyle.BG_DARK)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure main frame grid - 2x2 layout
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Sol üst panel - Directory/Dosya Listesi
        directory_frame = tk.LabelFrame(self.main_frame, text="📁 Disk Directory", 
                                       bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                                       font=("Arial", 10, "bold"))
        directory_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        directory_frame.grid_rowconfigure(0, weight=1)
        directory_frame.grid_columnconfigure(0, weight=1)
        
        self.directory_panel = DiskDirectoryPanel(directory_frame, bg=ModernStyle.BG_SECONDARY)
        self.directory_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.directory_panel.parent_gui = self
        
        # Sağ üst panel - Disassembly Sonuçları
        disassembly_frame = tk.LabelFrame(self.main_frame, text="⚙️ Disassembly Results",
                                         bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                                         font=("Arial", 10, "bold"))
        disassembly_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        disassembly_frame.grid_rowconfigure(0, weight=1)
        disassembly_frame.grid_columnconfigure(0, weight=1)
        
        self.disassembly_panel = DisassemblyPanel(disassembly_frame, bg=ModernStyle.BG_SECONDARY)
        self.disassembly_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.disassembly_panel.parent_gui = self
        
        # Sol alt panel - Console Output  
        console_frame = tk.LabelFrame(self.main_frame, text="�️ Console Output",
                                     bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                                     font=("Arial", 10, "bold"))
        console_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        console_frame.grid_rowconfigure(0, weight=1)
        console_frame.grid_columnconfigure(0, weight=1)
        
        self.console_panel = ConsolePanel(console_frame, bg=ModernStyle.BG_SECONDARY)
        self.console_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Sağ alt panel - Decompiler Sonuçları
        decompiler_frame = tk.LabelFrame(self.main_frame, text="� Decompiler Results",
                                        bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                                        font=("Arial", 10, "bold"))
        decompiler_frame.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
        decompiler_frame.grid_rowconfigure(0, weight=1)
        decompiler_frame.grid_columnconfigure(0, weight=1)
        
        self.decompiler_panel = DecompilerPanel(decompiler_frame, bg=ModernStyle.BG_SECONDARY)
        self.decompiler_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.decompiler_panel.parent_gui = self
    
    def initialize_components(self):
        """X1 core componentlerini başlat - Safe initialization"""
        try:
            # C64 Basic Parser - safe initialization
            if C64BasicParser:
                self.basic_parser = C64BasicParser()
                self.log_message("C64BasicParser yüklendi", "INFO")
            else:
                self.basic_parser = None
                self.log_message("C64BasicParser modülü bulunamadı", "WARNING")
            
            # Sprite Converter
            if SpriteConverter:
                self.sprite_converter = SpriteConverter()
                self.log_message("SpriteConverter yüklendi", "INFO")
            else:
                self.sprite_converter = None
                self.log_message("SpriteConverter modülü bulunamadı", "WARNING")
            
            # SID Converter
            if SIDConverter:
                self.sid_converter = SIDConverter()
                self.log_message("SIDConverter yüklendi", "INFO")
            else:
                self.sid_converter = None
                self.log_message("SIDConverter modülü bulunamadı", "WARNING")
            
            # Petcat Detokenizer
            if PetcatDetokenizer:
                self.petcat_detokenizer = PetcatDetokenizer()
                self.log_message("PetcatDetokenizer yüklendi", "INFO")
            else:
                self.petcat_detokenizer = None
                self.log_message("PetcatDetokenizer modülü bulunamadı", "WARNING")
            
            self.log_message("Component initialization tamamlandı", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Component initialization error: {e}", "ERROR")
    
    def setup_layout(self):
        """Layout ayarlarını tamamla"""
        # Status bar
        self.status_frame = tk.Frame(self.root, bg=ModernStyle.BG_TERTIARY, height=25)
        self.status_frame.grid(row=1, column=0, sticky="ew", padx=5)
        self.status_frame.grid_propagate(False)
        
        self.status_label = tk.Label(self.status_frame, text="🚀 D64 Converter Ready",
                                    bg=ModernStyle.BG_TERTIARY, fg=ModernStyle.FG_SECONDARY,
                                    font=("Arial", 9))
        self.status_label.pack(side=tk.LEFT, padx=10, pady=3)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var,
                                          maximum=100, length=200, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=3)
    
    def setup_menu(self):
        """Menu sistemi kur"""
        menubar = tk.Menu(self.root, bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PRG File...", command=self.open_prg_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Open D64 File...", command=self.open_d64_file)
        file_menu.add_command(label="Find C64 Files...", command=self.find_files)
        file_menu.add_separator()
        file_menu.add_command(label="Export Code...", command=self.export_code, accelerator="Ctrl+E")
        file_menu.add_command(label="Batch Export...", command=self.batch_export)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0, bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Illegal Opcode Analysis", command=self.analyze_illegal_opcodes_current)
        tools_menu.add_command(label="Sprite Analysis", command=self.analyze_sprites_current)
        tools_menu.add_command(label="SID Music Analysis", command=self.analyze_sid_current)
        tools_menu.add_command(label="Charset Analysis", command=self.analyze_charset_current)
        tools_menu.add_separator()
        tools_menu.add_command(label="Memory Map Viewer", command=self.show_memory_map)
        tools_menu.add_command(label="Pattern Analysis", command=self.show_pattern_analysis)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Real-time Updates", command=self.toggle_realtime)
        view_menu.add_checkbutton(label="Code Analysis", command=self.toggle_analysis)
        view_menu.add_separator()
        view_menu.add_command(label="Dark Theme", command=self.apply_dark_theme)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_help)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_prg_file())
        self.root.bind('<Control-e>', lambda e: self.export_code())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    # === X1 GUI Integration Methods ===
    
    def on_file_selected(self, entry):
        """Dosya seçildiğinde - X1 tarzı"""
        self.selected_entry = entry
        self.log_message(f"Dosya seçildi: {entry.get('filename')}", "INFO")
        
        # PRG datasını çıkar ve göster
        prg_data = self.extract_prg_data(entry)
        if prg_data:
            start_addr = entry.get('start_address', 0x0801)
            self.current_data = prg_data
            self.current_start_addr = start_addr
            
            # Hex editor'e yükle
            # self.hex_editor.load_data(prg_data, start_addr)
            
            self.log_message(f"PRG verisi yüklendi: {len(prg_data)} byte, start: ${start_addr:04X}", "INFO")
            self.update_status(f"Dosya hazır: {entry.get('filename')} - Dönüştürme için format seçin")
    
    def auto_analyze_file(self, entry):
        """Dosya çift tıklanınca otomatik analiz"""
        self.on_file_selected(entry)
        
        # Otomatik format algılama
        prg_data = self.extract_prg_data(entry)
        if prg_data and len(prg_data) >= 2:
            start_addr = prg_data[0] + (prg_data[1] << 8)
            
            if start_addr == 0x0801:
                # BASIC program
                self.log_message("BASIC program algılandı, detokenizing...", "INFO")
                self.convert_to_format('basic', 'disassembly')
            else:
                # Assembly program
                self.log_message("Assembly program algılandı, disassembling...", "INFO")
                self.convert_to_format('assembly', 'disassembly')
    
    def convert_to_format(self, format_type, target_panel):
        """Format dönüştürme - X1 tarzı"""
        if not self.selected_entry:
            self.log_message("Dosya seçilmemiş", "ERROR")
            return
        
        self.update_status(f"{format_type} formatına dönüştürülüyor...")
        
        # Threading ile dönüştür
        threading.Thread(target=self._convert_format_thread, 
                        args=(format_type, target_panel), daemon=True).start()
    
    def _convert_format_thread(self, format_type, target_panel):
        """Format dönüştürme thread'i"""
        try:
            # PRG verisi çıkar
            prg_data = self.extract_prg_data(self.selected_entry)
            if not prg_data:
                self.root.after(0, lambda: self.log_message("PRG verisi çıkarılamadı", "ERROR"))
                return
            
            if len(prg_data) < 2:
                self.root.after(0, lambda: self.log_message("Geçersiz PRG verisi", "ERROR"))
                return
            
            start_address = prg_data[0] + (prg_data[1] << 8)
            code_data = prg_data[2:]
            
            result_code = ""
            
            # Format'a göre işle
            if start_address == 0x0801 and format_type in ['basic', 'petcat', 'c64list']:
                # BASIC program
                if format_type == 'basic':
                    if self.basic_parser:
                        basic_lines = self.basic_parser.detokenize(prg_data)
                        result_code = "\n".join(basic_lines) if basic_lines else "BASIC detokenization failed"
                    else:
                        result_code = "; C64BasicParser modülü bulunamadı\n; Raw BASIC data görüntülenemedi"
                    
                elif format_type == 'petcat':
                    if self.petcat_detokenizer:
                        result_code = self.petcat_detokenizer.detokenize_prg(prg_data)
                    else:
                        result_code = "; PetcatDetokenizer modülü bulunamadı"
                    
                elif format_type == 'c64list':
                    if self.basic_parser:
                        basic_lines = self.basic_parser.detokenize(prg_data)
                        if basic_lines:
                            result_code = f"; C64List formatted output\n"
                            result_code += f"; Program start: ${start_address:04X}\n\n"
                            for line in basic_lines:
                                result_code += f"{line}\n"
                        else:
                            result_code = "; C64List: BASIC detokenization failed"
                    else:
                        result_code = "; C64List: C64BasicParser modülü bulunamadı"
                        
                # Assembly/Machine code program
                if format_type == 'assembly':
                    if AdvancedDisassembler:
                        disassembler = AdvancedDisassembler(
                            start_address=start_address,
                            code=code_data,
                            use_py65=self.disassembly_panel.use_py65_disassembler.get(),
                            use_illegal_opcodes=self.disassembly_panel.use_illegal_opcodes.get()
                        )
                        result_code = disassembler.disassemble()
                    else:
                        result_code = f"; AdvancedDisassembler modülü bulunamadı\n"
                        result_code += f"; Start Address: ${start_address:04X}\n"
                        result_code += f"; Raw bytes: {' '.join(f'${b:02X}' for b in code_data[:20])}"
                    
                elif format_type == 'c':
                    # C transpilation
                    if AdvancedDisassembler:
                        disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                        asm_code = disassembler.disassemble()
                        # Basic C conversion (can be enhanced)
                        result_code = f"// C Code generated from 6502 Assembly\n"
                        result_code += f"// Start Address: ${start_address:04X}\n\n"
                        result_code += f"void main() {{\n"
                        result_code += f"    // Assembly code:\n"
                        for line in asm_code.split('\n'):
                            if line.strip():
                                result_code += f"    // {line}\n"
                        result_code += f"}}\n"
                    else:
                        result_code = f"// AdvancedDisassembler modülü bulunamadı\n"
                        result_code += f"// Start Address: ${start_address:04X}\n"
                    
                elif format_type == 'qbasic':
                    # QBasic transpilation
                    result_code = f"' QBasic Code generated from 6502 Assembly\n"
                    result_code += f"' Start Address: ${start_address:04X}\n\n"
                    result_code += f"PRINT \"C64 Program Simulation\"\n"
                    result_code += f"' Original assembly code follows as comments\n"
                    
                elif format_type == 'pdsx':
                    # PDSX format
                    result_code = f"; PDSX Assembly Format\n"
                    result_code += f"; Generated from C64 PRG\n"
                    result_code += f".org ${start_address:04X}\n\n"
                    disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                    asm_lines = disassembler.disassemble().split('\n')
                    for line in asm_lines:
                        if line.strip() and not line.startswith(';'):
                            result_code += f"{line}\n"
                            
                elif format_type == 'pseudo':
                    # Pseudo code
                    result_code = f"// Pseudo Code\n"
                    result_code += f"// Original Address: ${start_address:04X}\n\n"
                    result_code += f"BEGIN PROGRAM\n"
                    result_code += f"  INITIALIZE_SYSTEM()\n"
                    result_code += f"  EXECUTE_CODE()\n"
                    result_code += f"END PROGRAM\n"
                    
                elif format_type == 'py65':
                    # py65 format
                    result_code = f"; py65 Professional Disassembler Output\n"
                    result_code += f"; Address: ${start_address:04X}\n\n"
                    # py65 integration would go here
                    result_code += f"; py65 disassembly not implemented yet\n"
                    
                # Decompiler formats
                elif format_type.startswith('dec_'):
                    if format_type == 'dec_c' and DECOMPILER_C_AVAILABLE:
                        decompiler = DecompilerC()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif format_type == 'dec_c2' and DECOMPILER_C2_AVAILABLE:
                        decompiler = DecompilerC2()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif format_type == 'dec_cpp' and DECOMPILER_CPP_AVAILABLE:
                        decompiler = DecompilerCPP()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif format_type == 'dec_qbasic' and DECOMPILER_QBASIC_AVAILABLE:
                        decompiler = DecompilerQBasic()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif format_type == 'dec_asm':
                        result_code = f"; ASM Decompiler (Enhanced)\n"
                        disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                        result_code += disassembler.disassemble()
                    else:
                        result_code = f"; Decompiler {format_type} not available\n"
                        result_code += f"; Available decompilers: C({DECOMPILER_C_AVAILABLE}), C++({DECOMPILER_CPP_AVAILABLE}), QBasic({DECOMPILER_QBASIC_AVAILABLE})\n"
            
            # Sonucu ilgili panele gönder
            if target_panel == 'disassembly':
                self.root.after(0, lambda: self.disassembly_panel.update_code(result_code, format_type))
            elif target_panel == 'decompiler':
                self.root.after(0, lambda: self.decompiler_panel.update_code(result_code, format_type))
            
            self.root.after(0, lambda: self.update_status(f"{format_type} dönüştürme tamamlandı"))
            self.root.after(0, lambda: self.log_message(f"{format_type} dönüştürme başarılı: {len(result_code)} karakter", "SUCCESS"))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.log_message(f"{format_type} dönüştürme hatası: {error_msg}", "ERROR"))
            self.root.after(0, lambda: self.update_status(f"{format_type} dönüştürme başarısız"))
    
    def extract_prg_data(self, entry):
        """PRG verisi çıkar - X1 tarzı"""
        try:
            # Eğer entry'de zaten prg_data varsa direkt kullan
            if 'prg_data' in entry:
                return entry['prg_data']
            
            # Kaynak dosyadan oku
            source_file = entry.get('source_file')
            if not source_file or not os.path.exists(source_file):
                self.log_message(f"Kaynak dosya bulunamadı: {source_file}", "ERROR")
                return None
            
            # Dosya tipine göre işle
            ext = os.path.splitext(source_file)[1].lower()
            
            if ext in ['.prg', '.p00']:
                # PRG dosyası direkt oku
                with open(source_file, 'rb') as f:
                    return f.read()
                    
            elif ext in ['.d64', '.d71', '.d81', '.d84']:
                # Disk imajından çıkar
                reader = D64Reader(source_file)
                return reader.extract_file(entry['filename'])
                
            elif ext == '.t64':
                # T64'ten çıkar
                file_offset = entry.get('file_offset')
                if file_offset:
                    with open(source_file, 'rb') as f:
                        f.seek(file_offset)
                        size = entry.get('size', 0)
                        return f.read(size)
                        
            return None
            
        except Exception as e:
            self.log_message(f"PRG çıkarma hatası: {e}", "ERROR")
            return None
    
    # === Analysis Methods ===
    
    def analyze_illegal_opcodes(self, entry):
        """Illegal opcode analizi"""
        threading.Thread(target=self._analyze_illegal_thread, args=(entry,), daemon=True).start()
    
    def _analyze_illegal_thread(self, entry):
        """Illegal opcode analiz thread'i"""
        try:
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.log_message("PRG verisi çıkarılamadı", "ERROR"))
                return
            
            # Basit illegal opcode analizi
            illegal_opcodes = []
            for i, byte in enumerate(prg_data[2:], start=2):  # Skip load address
                if byte in [0x02, 0x12, 0x22, 0x32, 0x42, 0x52, 0x62, 0x72, 0x92, 0xB2, 0xD2, 0xF2]:  # JAM/KIL opcodes
                    addr = (prg_data[0] + (prg_data[1] << 8)) + i - 2
                    illegal_opcodes.append({
                        'address': addr,
                        'opcode': byte,
                        'description': 'JAM/KIL instruction (freezes CPU)',
                        'is_dangerous': True
                    })
            
            results = {
                'total_instructions': len(prg_data) - 2,
                'illegal_count': len(illegal_opcodes),
                'illegal_opcodes': illegal_opcodes
            }
            
            # Sonuçları göster
            self.root.after(0, lambda: self.show_illegal_analysis_results(results))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Illegal analiz hatası: {e}", "ERROR"))
    
    def show_illegal_analysis_results(self, results):
        """Illegal analiz sonuçlarını göster"""
        result_text = f"🚫 Illegal Opcode Analysis\n"
        result_text += f"Total instructions: {results['total_instructions']}\n"
        result_text += f"Illegal opcodes found: {results['illegal_count']}\n\n"
        
        if results['illegal_count'] > 0:
            result_text += "⚠️ Illegal opcodes found:\n"
            for illegal in results['illegal_opcodes']:
                result_text += f"  ${illegal['address']:04X}: ${illegal['opcode']:02X} - {illegal['description']}\n"
        else:
            result_text += "✅ No illegal opcodes found\n"
        
        # Console'a yazdır
        self.log_message(result_text, "INFO")
        
        # Decompiler paneline göster
        self.decompiler_panel.update_code(result_text, "illegal_analysis")
    
    def analyze_sprites(self, entry):
        """Sprite analizi"""
        threading.Thread(target=self._analyze_sprites_thread, args=(entry,), daemon=True).start()
    
    def _analyze_sprites_thread(self, entry):
        """Sprite analiz thread'i"""
        try:
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.log_message("PRG verisi çıkarılamadı", "ERROR"))
                return
            
            # Sprite analizi
            sprite_results = self.sprite_converter.analyze_sprites(prg_data)
            
            result_text = f"🎮 Sprite Analysis\n"
            result_text += f"File: {entry.get('filename')}\n"
            result_text += f"Size: {len(prg_data)} bytes\n\n"
            
            if sprite_results.get('sprites_found', 0) > 0:
                result_text += f"✅ {sprite_results['sprites_found']} sprites found!\n"
                result_text += f"Addresses: {sprite_results.get('sprite_addresses', [])}\n"
            else:
                result_text += "❌ No sprite data found\n"
            
            self.root.after(0, lambda: self.log_message(result_text, "INFO"))
            self.root.after(0, lambda: self.decompiler_panel.update_code(result_text, "sprite_analysis"))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Sprite analiz hatası: {e}", "ERROR"))
    
    def analyze_sid(self, entry):
        """SID müzik analizi"""
        threading.Thread(target=self._analyze_sid_thread, args=(entry,), daemon=True).start()
    
    def _analyze_sid_thread(self, entry):
        """SID analiz thread'i"""
        try:
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.log_message("PRG verisi çıkarılamadı", "ERROR"))
                return
            
            # SID analizi
            sid_results = self.sid_converter.analyze_sid(prg_data)
            
            result_text = f"🎵 SID Music Analysis\n"
            result_text += f"File: {entry.get('filename')}\n\n"
            
            if sid_results.get('sid_found'):
                result_text += f"✅ SID music detected!\n"
                result_text += f"Play address: ${sid_results.get('play_address', 0):04X}\n"
                result_text += f"Init address: ${sid_results.get('init_address', 0):04X}\n"
            else:
                result_text += "❌ No SID music found\n"
            
            self.root.after(0, lambda: self.log_message(result_text, "INFO"))
            self.root.after(0, lambda: self.decompiler_panel.update_code(result_text, "sid_analysis"))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"SID analiz hatası: {e}", "ERROR"))
    
    def analyze_charset(self, entry):
        """Karakter seti analizi"""
        threading.Thread(target=self._analyze_charset_thread, args=(entry,), daemon=True).start()
    
    def _analyze_charset_thread(self, entry):
        """Charset analiz thread'i"""
        try:
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.log_message("PRG verisi çıkarılamadı", "ERROR"))
                return
            
            result_text = f"🔤 Charset Analysis\n"
            result_text += f"File: {entry.get('filename')}\n\n"
            
            # Basit charset analizi
            charset_data = []
            for i in range(0, len(prg_data) - 8, 8):
                chunk = prg_data[i:i+8]
                if all(b < 0x100 for b in chunk):  # Valid charset data
                    charset_data.append(i)
            
            if charset_data:
                result_text += f"✅ Potential charset data found at {len(charset_data)} locations\n"
                result_text += f"Addresses: {[f'${addr:04X}' for addr in charset_data[:10]]}\n"
            else:
                result_text += "❌ No charset data found\n"
            
            self.root.after(0, lambda: self.log_message(result_text, "INFO"))
            self.root.after(0, lambda: self.decompiler_panel.update_code(result_text, "charset_analysis"))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Charset analiz hatası: {e}", "ERROR"))
    
    # === Wrapper methods for current file ===
    
    def analyze_illegal_opcodes_current(self):
        """Mevcut dosya için illegal analiz"""
        if self.selected_entry:
            self.analyze_illegal_opcodes(self.selected_entry)
        else:
            self.log_message("Lütfen önce bir dosya seçin", "WARNING")
    
    def analyze_sprites_current(self):
        """Mevcut dosya için sprite analiz"""
        if self.selected_entry:
            self.analyze_sprites(self.selected_entry)
        else:
            self.log_message("Lütfen önce bir dosya seçin", "WARNING")
    
    def analyze_sid_current(self):
        """Mevcut dosya için SID analiz"""
        if self.selected_entry:
            self.analyze_sid(self.selected_entry)
        else:
            self.log_message("Lütfen önce bir dosya seçin", "WARNING")
    
    def analyze_charset_current(self):
        """Mevcut dosya için charset analiz"""
        if self.selected_entry:
            self.analyze_charset(self.selected_entry)
        else:
            self.log_message("Lütfen önce bir dosya seçin", "WARNING")
    
    # === File Operations ===
    
    def open_prg_file(self):
        """PRG dosyası aç"""
        self.directory_panel.select_file()
    
    def open_d64_file(self):
        """D64 dosyası aç"""
        self.directory_panel.select_file()
    
    def find_files(self):
        """Dosya bul"""
        self.directory_panel.find_files()
        
    # === Utility Methods ===
    
    def update_status(self, message):
        """Status güncelle"""
        self.status_label.config(text=message)
        
    def log_message(self, message, level="INFO"):
        """Console'a log mesajı ekle"""
        if hasattr(self, 'console_panel'):
            self.console_panel.add_log(message, level)
        else:
            print(f"[{level}] {message}")

    def load_sample_data(self):
        """Sample data yükle"""
        self.log_message("Loading sample data (Hello World example)...", "INFO")
        
        # Hello World example
        sample_data = bytes([
            0x01, 0x08,        # Load address $0801
            0x20, 0xD2, 0xFF,  # JSR $FFD2 (CHROUT)
            0x60               # RTS
        ])
        
        # Sample entry oluştur
        sample_entry = {
            'filename': 'HELLO_WORLD.PRG',
            'filetype': 'PRG',
            'start_address': 0x0801,
            'end_address': 0x0806,
            'size': len(sample_data),
            'prg_data': sample_data,
            'source_file': 'sample'
        }
        
        # Directory paneline ekle
        self.directory_panel.entries = [sample_entry]
        self.directory_panel.update_directory_display()
        
        self.log_message(f"Sample data loaded: {len(sample_data)} bytes", "INFO")
        self.update_status("Sample data loaded - Dosya seçin veya dönüştürme yapın")
    
    def init_decompiler(self):
        """Decompiler'ı başlat"""
        try:
            self.console_panel.add_log("Initializing unified decompiler...", "INFO")
            
            self.unified_decompiler = UnifiedDecompiler(
                start_addr=self.current_start_addr,
                enable_code_analysis=self.analysis_enabled
            )
            self.update_status("✅ Unified Decompiler initialized")
            self.console_panel.add_log("Unified decompiler successfully initialized", "INFO")
        except Exception as e:
            error_msg = f"Decompiler init error: {str(e)}"
            self.update_status(f"❌ {error_msg}")
            self.console_panel.add_log(error_msg, "ERROR")
    
    def trigger_real_time_update(self):
        """Real-time güncelleme tetikle"""
        if not self.real_time_updates or not self.current_data:
            return
        
        def update_thread():
            try:
                # Log start
                self.console_panel.add_log(f"Starting decompilation process...", "INFO")
                
                # Update progress
                self.progress_var.set(20)
                
                # Get selected format
                target_format = self.code_preview.current_format
                self.console_panel.add_log(f"Target format: {target_format}", "INFO")
                
                # Decompile
                if self.unified_decompiler:
                    self.progress_var.set(50)
                    self.console_panel.add_log(f"Running unified decompiler...", "INFO")
                    
                    result = self.unified_decompiler.decompile(
                        self.current_data,
                        target_format=target_format,
                        enable_code_analysis=self.analysis_enabled
                    )
                    
                    self.progress_var.set(80)
                    self.console_panel.add_log(f"Decompilation completed successfully", "INFO")
                    
                    # Update code preview
                    self.code_preview.update_code(result, target_format)
                    
                    # Update analysis if enabled
                    if self.analysis_enabled and hasattr(self.unified_decompiler, 'get_analysis_report'):
                        self.console_panel.add_log(f"Running code analysis...", "INFO")
                        analysis_report = self.unified_decompiler.get_analysis_report()
                        self.analysis_panel.update_analysis(analysis_report)
                        self.console_panel.add_log(f"Code analysis completed", "INFO")
                    
                    self.progress_var.set(100)
                    
                    # Show stats
                    if hasattr(self.unified_decompiler, 'get_enhanced_statistics'):
                        stats = self.unified_decompiler.get_enhanced_statistics()
                        patterns = stats.get('patterns_detected', 0)
                        complexity = stats.get('complexity_score', 0)
                        self.update_status(f"✅ {target_format} - {patterns} patterns, complexity: {complexity:.1f}")
                        self.console_panel.add_log(f"Statistics: {patterns} patterns detected, complexity: {complexity:.1f}", "INFO")
                
                # Reset progress
                self.root.after(1000, lambda: self.progress_var.set(0))
                
            except Exception as e:
                self.console_panel.add_log(f"Decompilation error: {str(e)}", "ERROR")
                self.update_status(f"❌ Error: {str(e)}")
                self.progress_var.set(0)
                
            except Exception as e:
                self.update_status(f"❌ Update error: {str(e)}")
                self.progress_var.set(0)
        
        # Run in background thread
        threading.Thread(target=update_thread, daemon=True).start()
    
    def update_status(self, message: str):
        """Status mesajını güncelle"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def open_prg_file(self):
        """PRG dosyası aç"""
        filename = filedialog.askopenfilename(
            title="Open PRG File",
            filetypes=[("PRG files", "*.prg"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        
        if filename:
            try:
                self.console_panel.add_log(f"Opening file: {filename}", "INFO")
                
                with open(filename, 'rb') as f:
                    data = f.read()
                
                # PRG files start with load address
                if len(data) >= 2:
                    load_addr = data[0] + (data[1] << 8)
                    actual_data = data[2:]
                    
                    self.console_panel.add_log(f"File loaded: {len(actual_data)} bytes, load address: ${load_addr:04X}", "INFO")
                    
                    self.current_data = actual_data
                    self.current_start_addr = load_addr
                    
                    # Update displays
                    self.hex_editor.load_data(actual_data, load_addr)
                    self.init_decompiler()
                    self.trigger_real_time_update()
                    
                    self.update_status(f"✅ Loaded: {os.path.basename(filename)} (${load_addr:04X})")
                    self.console_panel.add_log(f"File successfully loaded and processed", "INFO")
                
            except Exception as e:
                error_msg = f"Could not load file: {str(e)}"
                self.console_panel.add_log(error_msg, "ERROR")
                messagebox.showerror("Error", error_msg)
    
    def open_d64_file(self):
        """D64 dosyası aç (placeholder)"""
        messagebox.showinfo("Coming Soon", "D64 file support will be added in next version!")
    
    def export_code(self):
        """Kodu dışa aktar"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        format_type = self.code_preview.current_format
        ext_map = {"ASM": ".asm", "C": ".c", "QBasic": ".bas", "PDSx": ".pdsx"}
        
        filename = filedialog.asksaveasfilename(
            title=f"Export {format_type} Code",
            defaultextension=ext_map.get(format_type, ".txt"),
            filetypes=[(f"{format_type} files", f"*{ext_map.get(format_type, '.txt')}"), 
                      ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.code_preview.current_code)
                
                self.update_status(f"✅ Exported: {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not export file:\n{str(e)}")
    
    def batch_export(self):
        """Batch export (placeholder)"""
        messagebox.showinfo("Coming Soon", "Batch export will be implemented!")
    
    def toggle_realtime(self):
        """Real-time güncellemeleri aç/kapat"""
        self.real_time_updates = not self.real_time_updates
        status = "enabled" if self.real_time_updates else "disabled"
        self.update_status(f"Real-time updates {status}")
    
    def toggle_analysis(self):
        """Code analysis aç/kapat"""
        self.analysis_enabled = not self.analysis_enabled
        self.analysis_panel.analysis_var.set(self.analysis_enabled)
        self.init_decompiler()
        self.trigger_real_time_update()
    
    def apply_dark_theme(self):
        """Dark theme uygula"""
        self.update_status("Dark theme already active!")
    
    def show_memory_map(self):
        """Memory map viewer göster"""
        messagebox.showinfo("Memory Map", "Memory map viewer coming soon!")
    
    def show_pattern_analysis(self):
        """Pattern analysis göster"""
        messagebox.showinfo("Pattern Analysis", "Advanced pattern analysis coming soon!")
    
    def show_optimization_report(self):
        """Optimization report göster"""
        messagebox.showinfo("Optimization", "Optimization report coming soon!")
    
    def show_about(self):
        """About dialog"""
        about_text = """D64 Converter v5.0
Advanced Commodore 64 Decompiler Suite

🚀 Features:
• Multi-format decompilation (ASM, C, QBasic, PDSx)
• Advanced pattern recognition
• Real-time code preview
• Interactive hex editor
• Memory mapping integration
• Code optimization analysis

👨‍💻 Developed by D64 Converter Team
📅 2024"""
        
        messagebox.showinfo("About D64 Converter", about_text)
    
    def show_help(self):
        """Yardım göster"""
        messagebox.showinfo("Help", "User guide will be available online soon!")
    
    def run(self):
        """GUI'yi başlat"""
        self.update_status("🚀 D64 Converter GUI Ready - Load a PRG file to begin!")
    # === Missing Methods - UI Requirements ===
    
    def export_code(self):
        """Kod dışa aktar"""
        if not self.selected_entry:
            messagebox.showwarning("Uyarı", "Önce bir dosya seçin")
            return
        
        # Mevcut disassembly sonucunu al
        current_code = self.disassembly_panel.current_code
        if not current_code:
            messagebox.showwarning("Uyarı", "Dışa aktarılacak kod yok")
            return
        
        # Kaydetme dialogu
        file_path = filedialog.asksaveasfilename(
            title="Kod Dışa Aktar",
            defaultextension=".asm",
            filetypes=[
                ("Assembly files", "*.asm"),
                ("C files", "*.c"),
                ("QBasic files", "*.bas"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(current_code)
                self.log_message(f"Kod dışa aktarıldı: {file_path}", "SUCCESS")
                messagebox.showinfo("Başarılı", f"Kod dışa aktarıldı:\n{file_path}")
            except Exception as e:
                self.log_message(f"Dışa aktarma hatası: {e}", "ERROR")
                messagebox.showerror("Hata", f"Dışa aktarma hatası: {e}")
    
    def batch_export(self):
        """Toplu dışa aktarma"""
        if not self.directory_panel.entries:
            messagebox.showwarning("Uyarı", "Hiç dosya yüklenmemiş")
            return
        
        # Çıktı klasörü seç
        output_dir = filedialog.askdirectory(title="Çıktı Klasörü Seç")
        if not output_dir:
            return
        
        self.log_message(f"Toplu dışa aktarma başlatıldı: {len(self.directory_panel.entries)} dosya", "INFO")
        
        # Threading ile toplu işlem
        threading.Thread(target=self._batch_export_thread, args=(output_dir,), daemon=True).start()
    
    def _batch_export_thread(self, output_dir):
        """Toplu dışa aktarma thread'i"""
        try:
            total_files = len(self.directory_panel.entries)
            for i, entry in enumerate(self.directory_panel.entries):
                filename = entry.get('filename', f'unknown_{i}')
                
                # PRG verisi çıkar
                prg_data = self.extract_prg_data(entry)
                if prg_data:
                    # Assembly formatında dışa aktar
                    start_addr = entry.get('start_address', 0x0801)
                    if len(prg_data) >= 2:
                        start_addr = prg_data[0] + (prg_data[1] << 8)
                        code_data = prg_data[2:]
                        
                        disassembler = AdvancedDisassembler(start_address=start_addr, code=code_data)
                        asm_code = disassembler.disassemble()
                        
                        # Dosya kaydet
                        output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.asm")
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(asm_code)
                        
                        self.root.after(0, lambda f=filename: self.log_message(f"Dışa aktarıldı: {f}", "INFO"))
                
                # Progress güncelle
                progress = ((i + 1) / total_files) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
            
            self.root.after(0, lambda: self.log_message("Toplu dışa aktarma tamamlandı", "SUCCESS"))
            self.root.after(0, lambda: messagebox.showinfo("Başarılı", "Toplu dışa aktarma tamamlandı"))
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Toplu dışa aktarma hatası: {e}", "ERROR"))
    
    def show_memory_map(self):
        """Memory map göster"""
        if not self.selected_entry:
            messagebox.showwarning("Uyarı", "Önce bir dosya seçin")
            return
        
        prg_data = self.extract_prg_data(self.selected_entry)
        if not prg_data or len(prg_data) < 2:
            messagebox.showerror("Hata", "Geçersiz PRG verisi")
            return
        
        start_addr = prg_data[0] + (prg_data[1] << 8)
        end_addr = start_addr + len(prg_data) - 2
        
        memory_info = f"📊 Memory Map\n\n"
        memory_info += f"Start Address: ${start_addr:04X}\n"
        memory_info += f"End Address: ${end_addr:04X}\n"
        memory_info += f"Size: {len(prg_data)} bytes\n\n"
        
        # C64 memory regions
        if start_addr == 0x0801:
            memory_info += "🔹 BASIC Program Area\n"
        elif start_addr >= 0xA000:
            memory_info += "🔹 BASIC ROM Area\n"
        elif start_addr >= 0xE000:
            memory_info += "🔹 KERNAL ROM Area\n"
        else:
            memory_info += "🔹 User RAM Area\n"
        
        self.decompiler_panel.update_code(memory_info, "memory_map")
        self.log_message("Memory map görüntülendi", "INFO")
    
    def show_pattern_analysis(self):
        """Pattern analizi göster"""
        if not self.selected_entry:
            messagebox.showwarning("Uyarı", "Önce bir dosya seçin")
            return
        
        prg_data = self.extract_prg_data(self.selected_entry)
        if not prg_data:
            messagebox.showerror("Hata", "PRG verisi yok")
            return
        
        pattern_info = f"🔍 Pattern Analysis\n\n"
        
        # Basit pattern analizi
        patterns = {}
        for i in range(len(prg_data) - 1):
            pattern = f"{prg_data[i]:02X}{prg_data[i+1]:02X}"
            patterns[pattern] = patterns.get(pattern, 0) + 1
        
        # En yaygın pattern'ları bul
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        
        pattern_info += "Top 10 Byte Patterns:\n"
        for i, (pattern, count) in enumerate(sorted_patterns[:10]):
            pattern_info += f"{i+1:2d}. ${pattern} - {count} times\n"
        
        self.decompiler_panel.update_code(pattern_info, "pattern_analysis")
        self.log_message("Pattern analizi tamamlandı", "INFO")
    
    def toggle_realtime(self):
        """Real-time update toggle"""
        self.real_time_updates = not self.real_time_updates
        status = "açık" if self.real_time_updates else "kapalı"
        self.log_message(f"Real-time updates {status}", "INFO")
    
    def toggle_analysis(self):
        """Analysis toggle"""
        self.analysis_enabled = not self.analysis_enabled
        status = "açık" if self.analysis_enabled else "kapalı"
        self.log_message(f"Code analysis {status}", "INFO")
    
    def apply_dark_theme(self):
        """Dark theme uygula"""
        self.log_message("Dark theme zaten aktif", "INFO")
    
    def show_about(self):
        """Hakkında penceresi"""
        about_text = """D64 Converter v5.0
Advanced Commodore 64 Decompiler Suite

X1 GUI Integration
- Disk imajı okuma (D64, D71, D81, D84, T64, PRG)
- Disassembly formatları (Assembly, C, QBasic, PDSX, Pseudo)
- Decompiler sistemleri (C, C++, QBasic, Assembly)
- BASIC detokenizers (Parser, Petcat, C64List)
- Analiz araçları (Illegal opcode, Sprite, SID, Charset)

Geliştirici: D64 Converter Team
"""
        messagebox.showinfo("Hakkında", about_text)
    
    def show_help(self):
        """Yardım göster"""
        help_text = """D64 Converter Kullanım Kılavuzu:

1. Dosya Yükleme:
   - File > Open D64/PRG File ile dosya seç
   - File > Find C64 Files ile otomatik arama

2. Disassembly:
   - Dosya seç ve sağ üst paneldeki formatları kullan
   - Assembly, C, QBasic, PDSX seçenekleri

3. Decompiler:
   - Sol alt panelde decompiler formatlarını seç
   - C, C++, QBasic decompiler'ları mevcut

4. Analiz:
   - Illegal opcode, Sprite, SID, Charset analizi
   - Tools menüsünden erişilebilir

5. Export:
   - File > Export Code ile tek dosya
   - File > Batch Export ile toplu dışa aktarma
"""
        messagebox.showinfo("Yardım", help_text)
    
    def run(self):
        """GUI'yi çalıştır"""
        try:
            self.log_message("D64 Converter GUI v5.0 başlatıldı", "SUCCESS")
            self.root.mainloop()
        except Exception as e:
            self.log_message(f"GUI çalıştırma hatası: {e}", "ERROR")
            raise

def main():
    """GUI uygulamasını başlat"""
    print("🚀 D64 Converter GUI v5.0 Starting...")
    print("X1 Integration: ✅ Enabled")
    print("4-Panel Layout: ✅ Active")
    
    try:
        app = D64ConverterGUI()
        app.run()
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
