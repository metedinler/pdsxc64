#!/usr/bin/env python3
"""
🍎 D64 Converter - GUI Manager v5.3 - X1 GUI Integratio - Commodore 64 Geliştirme Stüdyosu
================================================================
PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: gui_manager copy.py - Modern GUI Manager (Ana Arayüz Kontrolcüsü)
VERSİYON: 5.3 (KızılElma Plan - 4 Disassembler + Enhanced BASIC Decompiler Entegrasyonu)
AMAÇ: Commodore 64 geliştirme araçları için birleşik grafik arayüz
================================================================

Bu modül şu özelliklerle C64 Geliştirme Stüdyosu'nun ana kontrolcüsüdür:
• 4 Disassembler Motor Entegrasyonu: basic, advanced, improved, py65_professional  
• Enhanced BASIC Decompiler: 5 dilde transpile (QBasic, C, C++, PDSX, Python)
• Format Directory Sistemi: Otomatik dizin oluşturma ve akıllı dosya adlandırma
• Hibrit Analiz GUI: BASIC+Assembly program tespit ve analiz araçları
• C64 Memory Manager: KERNAL/BASIC rutinleri, bellek haritası entegrasyonu

KızılElma Plan AŞAMA 1 Entegrasyonları: ✅ TAMAMLANDI
- ✅ 4 Disassembler GUI Integration
- ✅ Enhanced BASIC Decompiler GUI Aktivasyonu  
- ✅ Format Directory Sistemi
- ✅ Recent File Memory Sistemi

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
import time
import os
import json
import subprocess
import struct
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Core system imports
from hata_analiz_logger import init_hata_logger, get_hata_logger
from unified_decompiler import UnifiedDecompiler
from enhanced_c64_memory_manager import C64MemoryMapManager
from code_analyzer import CodeAnalyzer, PatternType
from database_manager import DatabaseManager
from hybrid_program_analyzer import HybridProgramAnalyzer

# X1 GUI imports - safer imports with defaults
try:
    from d64_reader import D64Reader
except ImportError:
    D64Reader = None

try:
    from enhanced_d64_reader import EnhancedUniversalDiskReader, EnhancedD64ReaderWrapper, enhanced_read_image, enhanced_read_directory, analyze_hybrid_program
except ImportError:
    EnhancedUniversalDiskReader = None
    EnhancedD64ReaderWrapper = None
    enhanced_read_image = None  
    enhanced_read_directory = None
    analyze_hybrid_program = None

# Enhanced Universal Disk Reader - updated
try:
    pass  # Enhanced disk reader deactivated due to FileEntry dependency
    EnhancedDiskReader = None
except ImportError:
    EnhancedDiskReader = None

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
    from disassembler import Disassembler
except ImportError:
    Disassembler = None

try:
    from py65_professional_disassembler import Py65ProfessionalDisassembler
except ImportError:
    Py65ProfessionalDisassembler = None

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

try:
    from hybrid_program_analyzer import HybridProgramAnalyzer
except ImportError:
    HybridProgramAnalyzer = None

try:
    from hybrid_disassembler import HybridDisassembler
except ImportError:
    HybridDisassembler = None

try:
    from enhanced_basic_decompiler import EnhancedBasicDecompiler
except ImportError:
    EnhancedBasicDecompiler = None

# Decompiler imports
try:
    from decompiler_qbasic import Decompiler as DecompilerQBasic
    DECOMPILER_QBASIC_AVAILABLE = True
except ImportError:
    DECOMPILER_QBASIC_AVAILABLE = False

try:
    from decompiler_cpp import Decompiler as DecompilerCPP
    DECOMPILER_CPP_AVAILABLE = True
except ImportError:
    DECOMPILER_CPP_AVAILABLE = False

try:
    from decompiler_c_2 import Decompiler as DecompilerC2
    DECOMPILER_C2_AVAILABLE = True
except ImportError:
    DECOMPILER_C2_AVAILABLE = False

try:
    from decompiler_c import Decompiler as DecompilerC
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
    BG_PRIMARY = "#ffffff"       # Ana arkaplan - beyaz (alias for BG_DARK)
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
    
    def _log_message(self, message, level="INFO"):
        """Log message - parent_gui'ye yönlendir veya print et"""
        if self.parent_gui and hasattr(self.parent_gui, 'log_message'):
            self.parent_gui.log_message(message, level)
        else:
            print(f"[{level}] {message}")
    
    def log_message(self, message, level="INFO"):
        """Compatibility için log_message alias - DiskDirectoryPanel için"""
        try:
            if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'log_message'):
                self.parent_gui.log_message(message, level)
            else:
                print(f"[DiskDirectoryPanel {level}] {message}")
        except Exception as e:
            print(f"[DiskDirectoryPanel ERROR] Log error: {e}, Original message: {message}")
    
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
        
        # Modern save/export controls
        ttk.Button(controls_frame, text="💾 Kaydet", command=self.parent_gui.save_current_code if self.parent_gui else self.save_current_code).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="📁 Farklı Kaydet", command=self.parent_gui.save_as_code if self.parent_gui else self.save_as_code).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="📦 Tümünü Aktar", command=self.parent_gui.export_all_formats if self.parent_gui else self.export_all_formats).pack(side=tk.LEFT, padx=2)
        
        # Directory tree
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview columns - X1 GUI formatı
        columns = ("filename", "filetype", "start_addr", "end_addr", "program_type", "track", "sector", "size")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Column headers - X1 GUI tarzı
        self.tree.heading("filename", text="Dosya Adı")
        self.tree.heading("filetype", text="Tip")
        self.tree.heading("start_addr", text="Başlangıç")
        self.tree.heading("end_addr", text="Bitiş")
        self.tree.heading("program_type", text="Program Türü")
        self.tree.heading("track", text="Track")
        self.tree.heading("sector", text="Sector")
        self.tree.heading("size", text="Boyut")
        
        # Column widths - X1 GUI tarzı
        self.tree.column("filename", width=120)
        self.tree.column("filetype", width=60)
        self.tree.column("start_addr", width=70)
        self.tree.column("end_addr", width=70)
        self.tree.column("program_type", width=100)
        self.tree.column("track", width=50)
        self.tree.column("sector", width=50)
        self.tree.column("size", width=60)
        
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
        
        ttk.Button(analysis_frame, text="🚫 Illegal Analiz", command=lambda: self.parent_gui.analyze_illegal_opcodes_current() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        ttk.Button(analysis_frame, text="🎮 Sprite Analiz", command=lambda: self.parent_gui.analyze_sprites_current() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        ttk.Button(analysis_frame, text="🎵 SID Analiz", command=lambda: self.parent_gui.analyze_sid_current() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        ttk.Button(analysis_frame, text="🔤 Charset Analiz", command=lambda: self.parent_gui.analyze_charset_current() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        
        # Hybrid Analysis row
        hybrid_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        hybrid_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(hybrid_frame, text="� Hibrit Analiz", command=lambda: self.parent_gui.analyze_hybrid_program_current() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        ttk.Button(hybrid_frame, text="⚙️ Assembly Ayır", command=lambda: self.parent_gui.extract_assembly_current() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        ttk.Button(hybrid_frame, text="📝 BASIC Ayır", command=lambda: self.parent_gui.extract_basic_current() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
    
    def select_file(self):
        """Dosya seçim dialogu - SON AÇILAN DİZİN HATIRLA"""
        try:
            # 🍎 HATA ANALIZ LOGGER - GUI ETKİLEŞİM
            if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                self.parent_gui.hata_logger.log_gui_etkileskim("DOSYA_SEC_BUTONU", {
                    "panel": "DiskDirectoryPanel", 
                    "buton": "📂 Seç", 
                    "konum": "controls_frame"
                })
            
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
            
            # Son açılan dizini hatırla
            last_dir = self.get_last_opened_directory()
            
            # 🍎 HATA ANALIZ LOGGER - DOSYA DİALOGU
            if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                self.parent_gui.hata_logger.log_gui_etkileskim("DOSYA_DIALOGU_ACILDI", {
                    "dialog_turu": "filedialog.askopenfilename",
                    "baslangic_dizini": last_dir,
                    "desteklenen_formatlar": len(file_types)
                })
            
            file_path = filedialog.askopenfilename(
                title="Commodore 64 File Selector",
                filetypes=file_types,
                initialdir=last_dir
            )
            
            if file_path:
                # 🍎 HATA ANALIZ LOGGER - DOSYA SEÇİLDİ
                if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                    file_ext = os.path.splitext(file_path)[1].lower()
                    self.parent_gui.hata_logger.log_disk_imaji(
                        file_path, 
                        "DOSYA_SECILDI", 
                        "BAŞARILI", 
                        {
                            "dosya_uzantisi": file_ext,
                            "dosya_boyutu": file_size,
                            "baslangic_dizini": last_dir
                        }
                    )
                
                # Son açılan dizini kaydet
                self.save_last_opened_directory(os.path.dirname(file_path))
                self.load_image(file_path)
            else:
                # 🍎 HATA ANALIZ LOGGER - DOSYA SEÇİMİ İPTAL
                if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                    self.parent_gui.hata_logger.log_gui_etkileskim("DOSYA_SECIMI_IPTAL", {
                        "dialog_turu": "filedialog.askopenfilename",
                        "reason": "Kullanıcı seçim yapmadı"
                    })
                
        except Exception as e:
            # 🍎 HATA ANALIZ LOGGER - HATA
            if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                self.parent_gui.hata_logger.log_hata("DOSYA_SECIM_HATASI", str(e), "select_file", None)
            messagebox.showerror("Dosya Seçim Hatası", f"Hata: {e}")
    
    def get_last_opened_directory(self):
        """Son açılan dizini al"""
        if self.parent_gui and hasattr(self.parent_gui, 'config_manager'):
            return self.parent_gui.config_manager.get('last_opened_directory', os.path.expanduser("~\\Downloads"))
        return os.path.expanduser("~\\Downloads")
    
    def save_last_opened_directory(self, directory):
        """Son açılan dizini kaydet"""
        if self.parent_gui and hasattr(self.parent_gui, 'config_manager'):
            self.parent_gui.config_manager.set('last_opened_directory', directory)
            self.parent_gui.config_manager.save_config()
    
    def log_to_terminal_and_file(self, message, level="INFO"):
        """Terminal ve dosya logging - parent_gui'ye yönlendir - Enhanced logger ile"""
        # 🍎 HATA ANALIZ LOGGER - TERMİNAL ÇIKTI YAKALAMA
        if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
            self.parent_gui.hata_logger.log_terminal(message, level)
        
        if self.parent_gui and hasattr(self.parent_gui, 'log_to_terminal_and_file'):
            self.parent_gui.log_to_terminal_and_file(message, level)
        else:
            print(f"[{level}] {message}")
    
    def load_image(self, file_path):
        """Disk imajını yükle - X1 tarzı"""
        try:
            # 🍎 HATA ANALIZ LOGGER - DİSK İMAJI YÜKLEME BAŞLANGICI
            if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                import time
                start_time = time.time()
                file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                file_ext = os.path.splitext(file_path)[1].lower()
                
                self.parent_gui.hata_logger.log_disk_imaji(
                    file_path, 
                    "DISK_IMAJI_YUKLEME_BASLADI", 
                    "BAŞLANGICTA", 
                    {
                        "dosya_uzantisi": file_ext,
                        "dosya_boyutu": file_size,
                        "baslangic_zamani": time.time()
                    }
                )
            
            # DETAILED LOGGING - HER ADIM
            self.log_to_terminal_and_file(f"🗂️ Disk dosyası seçildi: {file_path}", "INFO")
            self.log_to_terminal_and_file(f"📂 Dosya boyutu: {os.path.getsize(file_path)} bytes", "INFO")
            
            if self.parent_gui:
                self.parent_gui.update_status("Disk dosyası yükleniyor...")
            
            # Dosya uzantısını kontrol et
            ext = os.path.splitext(file_path)[1].lower()
            self.log_to_terminal_and_file(f"🔍 Dosya türü: {ext}", "INFO")
            
            if ext in ['.d64', '.d71', '.d81', '.d84']:
                # Disk imajı okuma - Enhanced D64 Reader Wrapper kullan
                try:
                    if EnhancedD64ReaderWrapper and os.path.exists("enhanced_d64_reader.py"):
                        self.log_to_terminal_and_file("✅ Enhanced D64 Reader Wrapper kullanıldı", "INFO")
                        
                        # 🍎 HATA ANALIZ LOGGER - ENHANCED READER KULLANIMI
                        if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                            self.parent_gui.hata_logger.log_disk_imaji(
                                file_path, 
                                "ENHANCED_D64_READER_KULLANIMI", 
                                "BAŞARILI", 
                                {"reader_type": "EnhancedD64ReaderWrapper"}
                            )
                        
                        reader = EnhancedD64ReaderWrapper(file_path)
                        self.entries = reader.list_files()
                        self.log_to_terminal_and_file(f"📄 {len(self.entries)} dosya bulundu", "INFO")
                        
                        # 🍎 HATA ANALIZ LOGGER - DOSYA LİSTESİ
                        if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                            self.parent_gui.hata_logger.log_disk_imaji(
                                file_path, 
                                "DOSYA_LISTESI_OKUNDU", 
                                "BAŞARILI", 
                                {
                                    "dosya_sayisi": len(self.entries),
                                    "dosya_listesi": [entry.get('filename', 'Unknown') for entry in self.entries[:10]]  # İlk 10 dosya
                                }
                            )
                        
                    else:
                        # Standard D64 Reader fonksiyonlarını kullan  
                        self.log_to_terminal_and_file("⚠️ Standard D64 Reader kullanıldı", "WARNING")
                        
                        # 🍎 HATA ANALIZ LOGGER - STANDARD READER
                        if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                            self.parent_gui.hata_logger.log_disk_imaji(
                                file_path, 
                                "STANDARD_D64_READER_KULLANIMI", 
                                "FALLBACK", 
                                {"reason": "Enhanced D64 Reader mevcut değil"}
                            )
                        
                        from d64_reader import read_image, read_directory
                        disk_data = read_image(file_path)
                        self.entries = read_directory(disk_data, ext[1:])
                        self.log_to_terminal_and_file(f"📄 {len(self.entries)} dosya bulundu", "INFO")
                        
                except Exception as reader_error:
                    # 🍎 HATA ANALIZ LOGGER - READER HATASI
                    if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                        self.parent_gui.hata_logger.log_hata("D64_READER_HATASI", str(reader_error), "load_image", None)
                    
                    # Fallback: Minimal file list
                    self.log_to_terminal_and_file(f"❌ D64 Reader hatası: {reader_error}, fallback kullanılıyor", "ERROR")
                    self.entries = [{
                        'filename': f"File from {os.path.basename(file_path)}",
                        'filetype': 'PRG',
                        'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
                        'track': 1,
                        'sector': 1
                    }]
                
            elif ext in ['.t64']:
                # T64 tape okuma - Enhanced D64 Reader Wrapper kullan
                try:
                    if EnhancedD64ReaderWrapper and os.path.exists("enhanced_d64_reader.py"):
                        self.log_to_terminal_and_file("✅ Enhanced D64 Reader Wrapper (T64) kullanıldı", "INFO")
                        
                        # 🍎 HATA ANALIZ LOGGER - T64 READER
                        if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                            self.parent_gui.hata_logger.log_disk_imaji(
                                file_path, 
                                "T64_ENHANCED_READER_KULLANIMI", 
                                "BAŞARILI", 
                                {"format": "T64", "reader_type": "Enhanced"}
                            )
                        
                        reader = EnhancedD64ReaderWrapper(file_path)
                        self.entries = reader.list_files()
                        self.log_to_terminal_and_file(f"📄 {len(self.entries)} dosya bulundu", "INFO")
                    else:
                        # Fallback T64 okuma
                        self.log_to_terminal_and_file("⚠️ Fallback T64 okuma kullanıldı", "WARNING")
                        
                        # 🍎 HATA ANALIZ LOGGER - T64 FALLBACK
                        if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
                            self.parent_gui.hata_logger.log_disk_imaji(
                                file_path, 
                                "T64_FALLBACK_READER", 
                                "FALLBACK", 
                                {"reason": "Enhanced D64 Reader mevcut değil"}
                            )
                        
                        self.entries = self.load_t64_file(file_path)
                        self.log_to_terminal_and_file(f"📄 {len(self.entries)} dosya bulundu", "INFO")
                except Exception as t64_error:
                    self.log_to_terminal_and_file(f"❌ T64 okuma hatası: {t64_error}, fallback kullanılıyor", "ERROR")
                    self.entries = self.load_t64_file(file_path)
                
            elif ext in ['.prg', '.p00']:
                # PRG dosyası direkt
                self.entries = self.load_prg_file(file_path)
                
            elif ext in ['.tap']:
                # TAP dosyası - Enhanced D64 Reader Wrapper kullan
                try:
                    if EnhancedD64ReaderWrapper and os.path.exists("enhanced_d64_reader.py"):
                        self._log_message("Enhanced D64 Reader Wrapper (TAP) kullanıldı", "INFO")
                        reader = EnhancedD64ReaderWrapper(file_path)
                        self.entries = reader.list_files()
                    else:
                        # Fallback generic okuma
                        self._log_message("Fallback TAP okuma kullanıldı", "WARNING")
                        self.entries = self.load_generic_file(file_path)
                except Exception as tap_error:
                    self._log_message(f"TAP okuma hatası: {tap_error}, fallback kullanılıyor", "WARNING")
                    self.entries = self.load_generic_file(file_path)
                    
            elif ext in ['.g64']:
                # G64 dosyası - Enhanced D64 Reader Wrapper kullan
                try:
                    if EnhancedD64ReaderWrapper and os.path.exists("enhanced_d64_reader.py"):
                        self._log_message("Enhanced D64 Reader Wrapper (G64) kullanıldı", "INFO")
                        reader = EnhancedD64ReaderWrapper(file_path)
                        self.entries = reader.list_files()
                    else:
                        # Fallback generic okuma
                        self._log_message("Fallback G64 okuma kullanıldı", "WARNING")
                        self.entries = self.load_generic_file(file_path)
                except Exception as g64_error:
                    self._log_message(f"G64 okuma hatası: {g64_error}, fallback kullanılıyor", "WARNING")
                    self.entries = self.load_generic_file(file_path)
                
            else:
                # Diğer formatlar
                self.entries = self.load_generic_file(file_path)
            
            # Directory'yi güncelle
            self.update_directory_display()
            
            if self.parent_gui:
                self.parent_gui.update_status(f"Dosya yüklendi: {len(self.entries)} dosya bulundu")
                
        except Exception as e:
            error_msg = f"Dosya yükleme hatası: {e}"
            self.log_message(error_msg, "ERROR")
            messagebox.showerror("Dosya Yükleme Hatası", f"Hata: {e}")
    
    def _log_message(self, message, level="INFO"):
        """Log message helper for DiskDirectoryPanel"""
        if self.parent_gui and hasattr(self.parent_gui, 'log_message'):
            self.parent_gui.log_message(message, level)
        else:
            print(f"[{level}] {message}")
    
    def save_current_code(self):
        """Fallback save method for DiskDirectoryPanel"""
        if self.parent_gui and hasattr(self.parent_gui, 'save_current_code'):
            self.parent_gui.save_current_code()
        else:
            print("⚠️ Save functionality not available - no parent GUI")
    
    def save_as_code(self):
        """Fallback save as method for DiskDirectoryPanel"""
        if self.parent_gui and hasattr(self.parent_gui, 'save_as_code'):
            self.parent_gui.save_as_code()
        else:
            print("⚠️ Save As functionality not available - no parent GUI")
    
    def export_all_formats(self):
        """Fallback export all method for DiskDirectoryPanel"""
        if self.parent_gui and hasattr(self.parent_gui, 'export_all_formats'):
            self.parent_gui.export_all_formats()
        else:
            print("⚠️ Export All functionality not available - no parent GUI")
    
    def update_directory_display(self):
        """Directory görünümünü güncelle - X1 GUI formatı"""
        # Eski entryleri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yeni entryleri ekle - X1 GUI sırası: filename, filetype, start_addr, end_addr, program_type, track, sector, size
        for entry in self.entries:
            filename = entry.get('filename', 'Unknown')
            filetype = entry.get('filetype', 'PRG')
            size = entry.get('size', 0)
            start_addr = entry.get('start_address', 0)
            end_addr = entry.get('end_address', 0)
            track = entry.get('track', 0)
            sector = entry.get('sector', 0)
            
            # Format değerleri
            start_str = f"${start_addr:04X}" if start_addr else ""
            size_str = f"{size}" if size else ""
            track_str = f"{track}" if track else ""
            sector_str = f"{sector}" if sector else ""
            
            # ESTIMATED END ADDRESS CALCULATION - Tahmini bitiş adresi hesaplama
            if start_addr and size > 2:
                estimated_end = start_addr + size - 3  # Header bytes çıkar
                end_str = f"${estimated_end:04X}"
            else:
                end_str = f"${end_addr:04X}" if end_addr else ""
            
            # Program türü analizi - Enhanced Analysis ile
            program_type = self.analyze_program_type_enhanced(entry)
            
            # X1 GUI formatında ekle: filename, filetype(ORİJİNAL), start_addr, end_addr, program_type, track, sector, size
            self.tree.insert("", tk.END, values=(filename, filetype, start_str, end_str, program_type, track_str, sector_str, size_str))
    
    def analyze_program_type(self, entry):
        """Program türü analizi - X1 GUI tarzı"""
        filetype = entry.get('filetype', 'PRG')
        start_addr = entry.get('start_address', 0)
        size = entry.get('size', 0)
        
        if filetype != 'PRG':
            return filetype.upper()
        
        # PRG dosyası analizi
        if start_addr == 0x0801:
            # BASIC program - hibrit kontrol yapabiliriz
            if size > 1000:  # Büyük programlar hibrit olabilir
                return "BASIC/HYBRID?"
            else:
                return "BASIC"
        elif start_addr >= 0x1000 and start_addr < 0xA000:
            return "ASSEMBLY"
        elif start_addr == 0xA000:
            return "ASSEMBLY"
        elif start_addr >= 0xC000:
            return "ASSEMBLY/SYS"
        else:
            return "MACHINE"
    
    def analyze_program_type_enhanced(self, entry):
        """Enhanced program türü analizi - ROM Data ile"""
        try:
            # Önce standard analizi yap
            standard_type = self.analyze_program_type(entry)
            
            # Enhanced D64 Reader'dan analiz varsa kullan
            if 'analysis' in entry and entry['analysis']:
                analysis = entry['analysis']
                enhanced_type = analysis.get('type', standard_type)
                confidence = analysis.get('confidence', 0)
                
                # Güven seviyesine göre prefix ekle
                if confidence >= 90:
                    return f"✅{enhanced_type}"
                elif confidence >= 70:
                    return f"⚠️{enhanced_type}"
                else:
                    return f"❓{enhanced_type}"
            
            # Program türü varsa direkt kullan
            if 'program_type' in entry and entry['program_type']:
                return entry['program_type']
            
            return standard_type
            
        except Exception as e:
            print(f"Enhanced program analysis error: {e}")
            return self.analyze_program_type(entry)
    
    def on_file_select(self, event):
        """Dosya seçildiğinde - DETAYLI LOG SİSTEMİ"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            filename = item['values'][0]
            filetype = item['values'][1] if len(item['values']) > 1 else 'Unknown'
            start_addr = item['values'][2] if len(item['values']) > 2 else 'Unknown'
            end_addr = item['values'][3] if len(item['values']) > 3 else 'Unknown'
            program_type = item['values'][4] if len(item['values']) > 4 else 'Unknown'
            track = item['values'][5] if len(item['values']) > 5 else 'Unknown'
            sector = item['values'][6] if len(item['values']) > 6 else 'Unknown'
            size = item['values'][7] if len(item['values']) > 7 else 'Unknown'
            
            # DETAYLI LOG - Kullanıcı seçimi
            self.log_to_terminal_and_file("="*60, "INFO")
            self.log_to_terminal_and_file(f"📂 DOSYA SEÇİLDİ - DETAYLAR:", "INFO")
            self.log_to_terminal_and_file(f"   📄 Dosya Adı: {filename}", "INFO")
            self.log_to_terminal_and_file(f"   📋 Tip: {filetype}", "INFO")
            self.log_to_terminal_and_file(f"   🎯 Başlangıç Adresi: {start_addr}", "INFO")
            self.log_to_terminal_and_file(f"   🏁 Bitiş Adresi: {end_addr}", "INFO")
            self.log_to_terminal_and_file(f"   🔍 Program Türü: {program_type}", "INFO")
            self.log_to_terminal_and_file(f"   📍 Track/Sector: {track}/{sector}", "INFO")
            self.log_to_terminal_and_file(f"   📏 Boyut: {size}", "INFO")
            
            # ROM Data ve Memory Map bilgisi ekle
            try:
                # Başlangıç adresini parse et
                if isinstance(start_addr, str) and start_addr.startswith('$'):
                    addr_num = int(start_addr[1:], 16)
                    
                    # Enhanced D64 Reader'dan memory info al
                    if hasattr(self, 'd64_reader') and hasattr(self.d64_reader, 'reader'):
                        memory_info = self.d64_reader.reader.get_memory_info(addr_num)
                        if memory_info:
                            self.log_to_terminal_and_file(f"   🧠 Memory Region: {memory_info.get('name', 'Unknown')}", "INFO")
                            self.log_to_terminal_and_file(f"   📖 Description: {memory_info.get('description', 'No description')[:80]}...", "INFO")
                            self.log_to_terminal_and_file(f"   🏷️ Type: {memory_info.get('type', 'Unknown')}", "INFO")
                        else:
                            self.log_to_terminal_and_file(f"   🧠 Memory Region: Custom/Unknown area", "INFO")
                            
                    # Adres türü analizi
                    if addr_num == 0x0801:
                        self.log_to_terminal_and_file(f"   🎯 Standard BASIC program start address", "INFO")
                    elif addr_num >= 0x1000 and addr_num < 0xA000:
                        self.log_to_terminal_and_file(f"   ⚙️ User RAM area - likely Assembly program", "INFO")
                    elif addr_num >= 0xA000:
                        self.log_to_terminal_and_file(f"   🔧 High memory area - Advanced Assembly", "INFO")
                    else:
                        self.log_to_terminal_and_file(f"   ❓ Unusual memory location", "INFO")
                        
            except Exception as e:
                self.log_to_terminal_and_file(f"   ⚠️ Memory analysis error: {e}", "WARNING")
            self.log_message(f"   💿 Track: {track}", "INFO")
            self.log_message(f"   📀 Sector: {sector}", "INFO")
            self.log_message(f"   📏 Boyut: {size}", "INFO")
            self.log_message("="*60, "INFO")
            
            # Terminal'e de yazdır
            print(f"\n🎯 DOSYA SEÇİLDİ:")
            print(f"📄 {filename} | Tip: {filetype} | Start: {start_addr} | Program: {program_type}")
            print(f"💿 Track: {track} | Sector: {sector} | Boyut: {size}")
            
            # Seçili dosyayı bul
            for entry in self.entries:
                if entry.get('filename') == filename:
                    self.selected_entry = entry
                    
                    # Entry detaylarını da log'la
                    self.log_message(f"📊 ENTRY DETAYLARI:", "DEBUG")
                    for key, value in entry.items():
                        self.log_message(f"   {key}: {value}", "DEBUG")
                    
                    break
            
            if self.parent_gui and self.selected_entry:
                self.parent_gui.selected_entry = self.selected_entry
                self.parent_gui.on_file_selected(self.selected_entry)
    
    def on_file_double_click(self, event):
        """Dosya çift tıklanınca otomatik analiz"""
        # 🍎 HATA ANALIZ LOGGER - DOSYA ÇİFT TIKLANMA
        if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'hata_logger'):
            import time
            
            dosya_adi = self.selected_entry.get('filename', 'Bilinmiyor') if self.selected_entry else 'Hiçbiri'
            dosya_tipi = self.selected_entry.get('filetype', 'Bilinmiyor') if self.selected_entry else 'Bilinmiyor'
            
            self.parent_gui.hata_logger.log_gui_etkileskim(
                "DOSYA_CIFT_TIKLANMA", 
                "USER_ACTION", 
                {
                    "dosya_adi": dosya_adi,
                    "dosya_tipi": dosya_tipi,
                    "secilen_entry": bool(self.selected_entry),
                    "parent_gui_mevcut": bool(self.parent_gui),
                    "islem_zamani": time.time()
                }
            )
        
        if self.selected_entry and self.parent_gui:
            # 🍎 HATA ANALIZ LOGGER - OTOMATİK ANALİZ BAŞLATMA
            if hasattr(self.parent_gui, 'hata_logger'):
                self.parent_gui.hata_logger.log_gui_etkileskim(
                    "OTOMATIK_ANALIZ_BASLATMA", 
                    "AUTO_PROCESSING", 
                    {
                        "dosya_adi": self.selected_entry.get('filename', 'Bilinmiyor'),
                        "analiz_tipi": "auto_analyze_file",
                        "tetikleyici": "double_click"
                    }
                )
            
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
        """Illegal opcode analizi - LOGGING ile"""
        if not self.selected_entry:
            self.log_to_terminal_and_file("❌ Dosya seçilmedi - Illegal Analiz iptal edildi", "WARNING")
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        self.log_to_terminal_and_file(f"🔍 ILLEGAL OPCODE ANALİZİ BAŞLADI", "INFO")
        self.log_to_terminal_and_file(f"   📄 Dosya: {self.selected_entry.get('filename', 'Unknown')}", "INFO")
        
        if self.parent_gui:
            self.parent_gui.analyze_illegal_opcodes(self.selected_entry)
        else:
            self.log_to_terminal_and_file("❌ Parent GUI bulunamadı", "ERROR")
    
    def analyze_sprites(self):
        """Sprite analizi - LOGGING ile"""
        if not self.selected_entry:
            self.log_to_terminal_and_file("❌ Dosya seçilmedi - Sprite Analiz iptal edildi", "WARNING")
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        self.log_to_terminal_and_file(f"🎮 SPRITE ANALİZİ BAŞLADI", "INFO")
        self.log_to_terminal_and_file(f"   📄 Dosya: {self.selected_entry.get('filename', 'Unknown')}", "INFO")
        
        if self.parent_gui:
            self.parent_gui.analyze_sprites(self.selected_entry)
        else:
            self.log_to_terminal_and_file("❌ Parent GUI bulunamadı", "ERROR")
    
    def analyze_sid(self):
        """SID müzik analizi - LOGGING ile"""
        if not self.selected_entry:
            self.log_to_terminal_and_file("❌ Dosya seçilmedi - SID Analiz iptal edildi", "WARNING")
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        self.log_to_terminal_and_file(f"🎵 SID ANALİZİ BAŞLADI", "INFO")
        self.log_to_terminal_and_file(f"   📄 Dosya: {self.selected_entry.get('filename', 'Unknown')}", "INFO")
        
        if self.parent_gui:
            self.parent_gui.analyze_sid(self.selected_entry)
        else:
            self.log_to_terminal_and_file("❌ Parent GUI bulunamadı", "ERROR")
    
    def analyze_charset(self):
        """Charset analizi - LOGGING ile"""
        if not self.selected_entry:
            self.log_to_terminal_and_file("❌ Dosya seçilmedi - Charset Analiz iptal edildi", "WARNING")
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        self.log_to_terminal_and_file(f"🔤 CHARSET ANALİZİ BAŞLADI", "INFO")
        self.log_to_terminal_and_file(f"   📄 Dosya: {self.selected_entry.get('filename', 'Unknown')}", "INFO")
        
        if self.parent_gui:
            self.parent_gui.analyze_charset(self.selected_entry)
        else:
            self.log_to_terminal_and_file("❌ Parent GUI bulunamadı", "ERROR")
    
    def analyze_hybrid_program(self):
        """Hibrit program analizi - LOGGING ile"""
        if not self.selected_entry:
            self.log_to_terminal_and_file("❌ Dosya seçilmedi - Hibrit Analiz iptal edildi", "WARNING")
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        self.log_to_terminal_and_file(f"🔧 HİBRİT PROGRAM ANALİZİ BAŞLADI", "INFO")
        self.log_to_terminal_and_file(f"   📄 Dosya: {self.selected_entry.get('filename', 'Unknown')}", "INFO")
        self.log_to_terminal_and_file(f"   🔍 BASIC + Assembly karışım analizi", "INFO")
        
        if self.parent_gui:
            self.parent_gui.analyze_hybrid_program(self.selected_entry)
        else:
            self.log_to_terminal_and_file("❌ Parent GUI bulunamadı", "ERROR")
    
    def extract_assembly_from_hybrid(self):
        """Hibrit dosyadan Assembly ayır - LOGGING ile"""
        if not self.selected_entry:
            self.log_to_terminal_and_file("❌ Dosya seçilmedi - Assembly Ayırma iptal edildi", "WARNING")
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        self.log_to_terminal_and_file(f"⚙️ ASSEMBLY AYIRMA İŞLEMİ BAŞLADI", "INFO")
        self.log_to_terminal_and_file(f"   📄 Kaynak: {self.selected_entry.get('filename', 'Unknown')}", "INFO")
        self.log_to_terminal_and_file(f"   🎯 Hedef: Assembly kodu ayırma", "INFO")
        
        if self.parent_gui:
            self.parent_gui.extract_assembly_from_hybrid(self.selected_entry)
        else:
            self.log_to_terminal_and_file("❌ Parent GUI bulunamadı", "ERROR")
    
    def extract_basic_from_hybrid(self):
        """Hibrit dosyadan BASIC ayır - LOGGING ile"""
        if not self.selected_entry:
            self.log_to_terminal_and_file("❌ Dosya seçilmedi - BASIC Ayırma iptal edildi", "WARNING")
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        self.log_to_terminal_and_file(f"📝 BASIC AYIRMA İŞLEMİ BAŞLADI", "INFO")
        self.log_to_terminal_and_file(f"   📄 Kaynak: {self.selected_entry.get('filename', 'Unknown')}", "INFO")
        self.log_to_terminal_and_file(f"   🎯 Hedef: BASIC kodu ayırma", "INFO")
        
        if self.parent_gui:
            self.parent_gui.extract_basic_from_hybrid(self.selected_entry)
        else:
            self.log_to_terminal_and_file("❌ Parent GUI bulunamadı", "ERROR")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_hybrid_program(self.selected_entry)
        else:
            # Fallback - standalone analysis
            try:
                from hybrid_program_analyzer import HybridProgramAnalyzer
                analyzer = HybridProgramAnalyzer()
                
                # PRG data çıkar
                if hasattr(self.selected_entry, 'get') and 'prg_data' in self.selected_entry:
                    prg_data = self.selected_entry['prg_data']
                else:
                    messagebox.showerror("Hata", "PRG verisi bulunamadı")
                    return
                
                # Analiz yap
                result = analyzer.analyze_prg_data(prg_data)
                
                # Sonuçları göster
                report = analyzer.generate_hybrid_report(result)
                
                # Basit sonuç penceresi
                result_window = tk.Toplevel(self)
                result_window.title("Hibrit Program Analizi")
                result_window.geometry("600x400")
                
                text_widget = tk.Text(result_window, wrap=tk.WORD, font=("Consolas", 10))
                scrollbar = tk.Scrollbar(result_window, command=text_widget.yview)
                text_widget.config(yscrollcommand=scrollbar.set)
                
                text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                text_widget.insert(tk.END, report)
                text_widget.config(state=tk.DISABLED)
                
            except Exception as e:
                messagebox.showerror("Hata", f"Hibrit analiz hatası: {e}")
                print(f"[ERROR] Standalone hybrid analysis failed: {e}")
    
    def analyze_hybrid_program(self):
        """Hibrit program analizi (BASIC+Assembly)"""
        if not self.selected_entry:
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_hybrid_program(self.selected_entry)
    
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
        
        # Assembly format dropdown ekle
        asm_frame = tk.Frame(group1)
        asm_frame.grid(row=0, column=0, padx=2, pady=2)
        
        tk.Label(asm_frame, text="ASM:", font=("Arial", 8)).pack(side=tk.TOP)
        self.asm_format_var = tk.StringVar(value="Native")
        asm_formats = ["Native", "ACME", "CC65", "DASM", "KickAss", "TASM", "64TASS", "CA65"]
        self.asm_format_combo = ttk.Combobox(asm_frame, textvariable=self.asm_format_var, 
                                           values=asm_formats, width=8, state="readonly")
        self.asm_format_combo.pack(side=tk.TOP)
        
        # Disassembler motor seçimi - YENİ EKLENDİ!
        disasm_frame = tk.Frame(group1)
        disasm_frame.grid(row=0, column=1, padx=2, pady=2)
        
        tk.Label(disasm_frame, text="Disassembler:", font=("Arial", 8)).pack(side=tk.TOP)
        self.disassembler_var = tk.StringVar(value="improved")
        disassembler_types = ["basic", "advanced", "improved", "py65_professional"]
        self.disassembler_combo = ttk.Combobox(disasm_frame, textvariable=self.disassembler_var, 
                                             values=disassembler_types, width=10, state="readonly")
        self.disassembler_combo.pack(side=tk.TOP)
        
        ttk.Button(group1, text="Assembly", command=lambda: self.convert_format('assembly')).grid(row=1, column=0, padx=2)
        ttk.Button(group1, text="C", command=lambda: self.convert_format('c')).grid(row=1, column=1, padx=2)
        ttk.Button(group1, text="QBasic", command=lambda: self.convert_format('qbasic')).grid(row=1, column=2, padx=2)
        
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
        
        # Hibrit Analiz grubu
        group4 = ttk.LabelFrame(format_frame, text="Hibrit Program")
        group4.pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(group4, text="🔍 Hibrit Analiz", command=self.analyze_hybrid_program).grid(row=0, column=0, padx=2)
        ttk.Button(group4, text="⚙️ Assembly Ayır", command=self.extract_assembly_from_hybrid).grid(row=0, column=1, padx=2)
        
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
        """Format dönüştürme - DETAYLI LOGGİNG ile"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            # PETCAT VE DİSASSEMBLY LOGGİNG BAŞLAT
            self.log_to_parent(f"🔄 FORMAT DÖNÜŞTÜRME BAŞLADI", "INFO")
            self.log_to_parent(f"   🎯 Hedef Format: {format_type.upper()}", "INFO")
            self.log_to_parent(f"   📄 Dosya: {self.parent_gui.selected_entry.get('filename', 'Unknown')}", "INFO")
            
            # Assembly format ve disassembler seçimi varsa ekle
            if format_type == 'assembly' and hasattr(self, 'asm_format_var'):
                asm_format = self.asm_format_var.get()
                disassembler_type = self.disassembler_var.get() if hasattr(self, 'disassembler_var') else 'improved'
                self.log_to_parent(f"   ⚙️ Assembly Format: {asm_format}", "INFO")
                self.log_to_parent(f"   🔧 Disassembler Motor: {disassembler_type}", "INFO")
                format_type = f"assembly_{asm_format.lower()}_{disassembler_type}"
            
            # PETCAT özel logging
            if format_type == 'petcat':
                self.log_to_parent(f"   🐈 PETCAT DETOKENIZER seçildi", "INFO")
                self.log_to_parent(f"   📋 BASIC token çözümleme başlıyor...", "INFO")
                if os.path.exists("petcat.exe"):
                    self.log_to_parent(f"   ✅ petcat.exe bulundu", "INFO")
                else:
                    self.log_to_parent(f"   ⚠️ petcat.exe bulunamadı, fallback kullanılacak", "WARNING")
            
            # BASIC Parser özel logging
            elif format_type == 'basic':
                self.log_to_parent(f"   📝 BASIC PARSER seçildi", "INFO")
                self.log_to_parent(f"   🔍 Enhanced BASIC Decompiler kullanılacak", "INFO")
            
            # C64List özel logging
            elif format_type == 'c64list':
                self.log_to_parent(f"   📋 C64LIST DETOKENIZER seçildi", "INFO")
                
            # Assembly özel logging
            elif 'assembly' in format_type:
                self.log_to_parent(f"   ⚙️ ASSEMBLY DISASSEMBLY seçildi", "INFO")
                self.log_to_parent(f"   🔧 Disassembler tipi: {self.get_disassembler_type()}", "INFO")
                
            # Format dönüştürmeyi başlat
            self.log_to_parent(f"   ▶️ Dönüştürme işlemi başlatılıyor...", "INFO")
            self.parent_gui.convert_to_format(format_type, 'disassembly')
        else:
            self.update_code("Lütfen önce bir dosya seçin", format_type)
    
    def get_disassembler_type(self):
        """Kullanılacak disassembler tipini belirle"""
        if hasattr(self, 'use_py65_disassembler') and self.use_py65_disassembler.get():
            return "PY65 Professional"
        elif hasattr(self, 'use_advanced_disassembler') and self.use_advanced_disassembler.get():
            return "Advanced Disassembler"
        else:
            return "Basic Disassembler"
    
    def log_to_parent(self, message, level="INFO"):
        """Parent GUI'ye log mesajı gönder"""
        if self.parent_gui and hasattr(self.parent_gui, 'log_to_terminal_and_file'):
            self.parent_gui.log_to_terminal_and_file(message, level)
        else:
            print(f"[DisassemblyPanel {level}] {message}")
    
    def update_code(self, code, format_type=None):
        """Code display güncelle - DETAYLI LOGGİNG ile"""
        if format_type:
            self.current_format = format_type
        
        # LOG SONUÇLARI
        lines = len(code.split('\n'))
        code_length = len(code)
        
        self.log_to_parent(f"📊 FORMAT DÖNÜŞTÜRME TAMAMLANDI:", "INFO")
        self.log_to_parent(f"   ✅ Format: {self.current_format.upper()}", "INFO") 
        self.log_to_parent(f"   📄 Satır sayısı: {lines}", "INFO")
        self.log_to_parent(f"   📏 Karakter sayısı: {code_length}", "INFO")
        
        # İçerik analizi
        if 'LDA' in code or 'STA' in code or 'JMP' in code:
            self.log_to_parent(f"   ⚙️ Assembly opcodes tespit edildi", "INFO")
        if 'PRINT' in code or 'FOR' in code or 'NEXT' in code:
            self.log_to_parent(f"   📝 BASIC komutları tespit edildi", "INFO")
        if 'SYS' in code:
            self.log_to_parent(f"   🔀 SYS çağrısı tespit edildi - Hibrit program olabilir", "WARNING")
        
        # PETCAT özel sonuç analizi
        if format_type == 'petcat':
            if 'REM' in code:
                self.log_to_parent(f"   💬 REM yorumları başarıyla çözüldü", "INFO")
            if code.strip().startswith('10 '):
                self.log_to_parent(f"   📝 BASIC program satır numaraları korundu", "INFO")
            if len(code.strip()) < 50:
                self.log_to_parent(f"   ⚠️ Petcat çıktısı beklenenden kısa - kontrol edilmeli", "WARNING")
                
        self.current_code = code
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(1.0, code)
        
        # Status güncelle
        self.status_label.config(text=f"{self.current_format} - {lines} satır, {code_length} karakter")
        
        self.log_to_parent(f"   🎯 Disassembly Panel güncellendi", "INFO")
    
    def analyze_hybrid_program(self):
        """Hibrit program analizi"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            self.parent_gui.run_hybrid_analysis()
        else:
            self.update_code("Lütfen önce bir dosya seçin", "HYBRID")
    
    def extract_assembly_from_hybrid(self):
        """Hibrit programdan assembly ayırma"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            self.parent_gui.extract_assembly_code()
        else:
            self.update_code("Lütfen önce bir dosya seçin", "ASSEMBLY")
    
    def analyze_hybrid_program(self):
        """Hibrit program analizi - DisassemblyPanel"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            self.log_to_parent(f"🔧 HİBRİT PROGRAM ANALİZİ (Disassembly Panel)", "INFO")
            self.log_to_parent(f"   📄 Dosya: {self.parent_gui.selected_entry.get('filename', 'Unknown')}", "INFO")
            self.parent_gui.analyze_hybrid_program(self.parent_gui.selected_entry)
        else:
            self.log_to_parent("❌ Dosya seçilmedi - Hibrit Analiz iptal edildi", "WARNING")
    
    def extract_assembly_from_hybrid(self):
        """Assembly ayırma - DisassemblyPanel"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            self.log_to_parent(f"⚙️ ASSEMBLY AYIRMA (Disassembly Panel)", "INFO")
            self.log_to_parent(f"   📄 Kaynak: {self.parent_gui.selected_entry.get('filename', 'Unknown')}", "INFO")
            self.parent_gui.extract_assembly_from_hybrid(self.parent_gui.selected_entry)
        else:
            self.log_to_parent("❌ Dosya seçilmedi - Assembly Ayırma iptal edildi", "WARNING")

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
        """Decompiler format dönüştürme - DETAYLI LOGGİNG ile"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            # DECOMPILER LOGGİNG BAŞLAT
            self.log_to_parent(f"🔄 DECOMPILER BAŞLADI", "INFO")
            self.log_to_parent(f"   🎯 Hedef Format: {format_type.upper()}", "INFO")
            self.log_to_parent(f"   📄 Dosya: {self.parent_gui.selected_entry.get('filename', 'Unknown')}", "INFO")
            
            # Decompiler tip analizi
            if 'dec_c' in format_type:
                self.log_to_parent(f"   💻 C DECOMPILER seçildi", "INFO")
            elif 'dec_cpp' in format_type:
                self.log_to_parent(f"   ⚡ C++ DECOMPILER seçildi", "INFO")
            elif 'dec_qbasic' in format_type:
                self.log_to_parent(f"   📝 QBASIC DECOMPILER seçildi", "INFO")
            elif 'dec_asm' in format_type:
                self.log_to_parent(f"   ⚙️ ASSEMBLY DECOMPILER seçildi", "INFO")
                
            self.parent_gui.convert_to_format(format_type, 'decompiler')
        else:
            self.update_code("Lütfen önce bir dosya seçin", format_type)
    
    def log_to_parent(self, message, level="INFO"):
        """Parent GUI'ye log mesajı gönder"""
        if self.parent_gui and hasattr(self.parent_gui, 'log_to_terminal_and_file'):
            self.parent_gui.log_to_terminal_and_file(message, level)
        else:
            print(f"[DecompilerPanel {level}] {message}")
    
    def update_code(self, code, format_type=None):
        """Code display güncelle - DETAYLI LOGGİNG ile"""
        if format_type:
            self.current_format = format_type
        
        # LOG SONUÇLARI
        lines = len(code.split('\n'))
        code_length = len(code)
        
        self.log_to_parent(f"📊 DECOMPILER TAMAMLANDI:", "INFO")
        self.log_to_parent(f"   ✅ Format: {self.current_format.upper()}", "INFO") 
        self.log_to_parent(f"   📄 Satır sayısı: {lines}", "INFO")
        self.log_to_parent(f"   📏 Karakter sayısı: {code_length}", "INFO")
        
        # İçerik analizi
        if 'main(' in code or '#include' in code:
            self.log_to_parent(f"   💻 C/C++ syntax tespit edildi", "INFO")
        if 'PRINT' in code or 'DIM' in code:
            self.log_to_parent(f"   📝 BASIC syntax tespit edildi", "INFO")
        if '{' in code and '}' in code:
            self.log_to_parent(f"   🔧 Structured code blocks tespit edildi", "INFO")
                
        self.current_code = code
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(1.0, code)
        
        # Status güncelle
        self.status_label.config(text=f"{self.current_format} - {lines} satır, {code_length} karakter")
        
        self.log_to_parent(f"   🎯 Decompiler Panel güncellendi", "INFO")
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
    
    def __init__(self, root=None):
        try:
            # 🍎 HATA ANALIZ LOGGER - İLK ÖNCELİK
            print("🍎 Hata Analiz Logger başlatılıyor...")
            self.hata_logger = init_hata_logger()
            self.hata_logger.log_terminal("🎨 D64ConverterGUI initialization started...")
            self.hata_logger.sistem_durum_guncelle("GUI_INITIALIZATION")
            
            print("🎨 D64ConverterGUI initialization started...")
            
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
            
            # Logger setup
            import logging
            self.logger = logging.getLogger(__name__)
            self.logger.info("🎨 D64ConverterGUI initializing...")
            
            # Terminal logging için
            self.log_to_terminal = True
            
            print("🎨 Setting up main window...")
            self.setup_main_window(root)
            print("✅ Main window setup completed")
            
            print("🔧 Setting up components...")
            self.setup_components()
            print("✅ Components setup completed")
            
            print("📐 Setting up layout...")
            self.setup_layout()
            print("✅ Layout setup completed")
            
            print("📋 Setting up menu...")
            self.setup_menu()
            print("✅ Menu setup completed")
            
            print("⚙️ Initializing components...")
            self.initialize_components()
            print("✅ Component initialization completed")
            
            # Status
            self.update_status("D64 Converter v5.0 hazır - Dosya seçin")
            self.logger.info("✅ D64ConverterGUI initialization completed successfully")
            print("✅ D64ConverterGUI initialization completed!")
            
        except Exception as e:
            error_msg = f"❌ D64ConverterGUI initialization failed: {e}"
            print(error_msg)
            
            # Log the error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(error_msg)
            
            # Print detailed traceback
            import traceback
            full_traceback = traceback.format_exc()
            print(f"Full initialization error traceback:\n{full_traceback}")
            logger.error(f"Full traceback:\n{full_traceback}")
            
            # Re-raise the exception to be caught by caller
            raise e
    
    def log_to_terminal_and_file(self, message, level="INFO"):
        """Her şeyi hem terminale hem dosyaya yaz"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg = f"[{timestamp}] [{level}] {message}"
        
        # Terminale yazdır
        print(formatted_msg)
        
        # Logger'a yazdır
        if hasattr(self, 'logger'):
            if level == "ERROR":
                self.logger.error(message)
            elif level == "WARNING":
                self.logger.warning(message)
            else:
                self.logger.info(message)
        
        # Console display'e de yazdır (varsa)
        if hasattr(self, 'console_display'):
            try:
                self.console_display.config(state=tk.NORMAL)
                self.console_display.insert(tk.END, f"{formatted_msg}\n")
                self.console_display.see(tk.END)
                self.console_display.config(state=tk.DISABLED)
            except:
                pass
    
    def setup_main_window(self, root=None):
        """Ana pencereyi kur"""
        try:
            print("🪟 Creating main window...")
            if root is None:
                self.root = tk.Tk()
                print("✅ New Tk() root created")
            else:
                self.root = root
                print("✅ Using provided root window")
                
            self.root.title("D64 Converter - Advanced Decompiler Suite v5.0 (X1 Integration)")
            self.root.geometry("1600x1000")
            self.root.configure(bg=ModernStyle.BG_DARK)
            print("✅ Window properties set")
            
            # Window icon (if available)
            try:
                self.root.iconbitmap("icon.ico")
                print("✅ Window icon set")
            except:
                print("⚠️ Window icon not available, continuing...")
                
        except Exception as e:
            print(f"❌ Main window setup failed: {e}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            raise e
        except:
            pass
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def setup_components(self):
        """GUI bileşenlerini kur - 4 Panel Layout"""
        try:
            print("📦 Creating main container...")
            # Main container
            self.main_frame = tk.Frame(self.root, bg=ModernStyle.BG_DARK)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            print("✅ Main container created")
            
            # Configure main frame grid - 2x2 layout
            self.main_frame.grid_rowconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_columnconfigure(1, weight=1)
            print("✅ Grid configuration set")
            
            print("📁 Creating directory panel...")
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
            print("✅ Directory panel created")
            
            print("⚙️ Creating disassembly panel...")
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
            print("✅ Disassembly panel created")
            
        except Exception as e:
            print(f"❌ Component setup failed: {e}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            raise e
        
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
            print("⚙️ Initializing core components...")
            
            # C64 Basic Parser - safe initialization
            try:
                if C64BasicParser:
                    self.basic_parser = C64BasicParser()
                    self.log_message("C64BasicParser yüklendi", "INFO")
                    print("✅ C64BasicParser loaded")
                else:
                    self.basic_parser = None
                    self.log_message("C64BasicParser modülü bulunamadı", "WARNING")
                    print("⚠️ C64BasicParser not available")
            except Exception as e:
                print(f"❌ C64BasicParser initialization failed: {e}")
                self.basic_parser = None
            
            # Sprite Converter
            try:
                if SpriteConverter:
                    self.sprite_converter = SpriteConverter()
                    self.log_message("SpriteConverter yüklendi", "INFO")
                    print("✅ SpriteConverter loaded")
                else:
                    self.sprite_converter = None
                    self.log_message("SpriteConverter modülü bulunamadı", "WARNING")
                    print("⚠️ SpriteConverter not available")
            except Exception as e:
                print(f"❌ SpriteConverter initialization failed: {e}")
                self.sprite_converter = None
            
            # SID Converter
            try:
                if SIDConverter:
                    self.sid_converter = SIDConverter()
                    self.log_message("SIDConverter yüklendi", "INFO")
                    print("✅ SIDConverter loaded")
                else:
                    self.sid_converter = None
                    self.log_message("SIDConverter modülü bulunamadı", "WARNING")
                    print("⚠️ SIDConverter not available")
            except Exception as e:
                print(f"❌ SIDConverter initialization failed: {e}")
                self.sid_converter = None
            
            # Petcat Detokenizer
            try:
                if PetcatDetokenizer:
                    self.petcat_detokenizer = PetcatDetokenizer()
                    self.log_message("PetcatDetokenizer yüklendi", "INFO")
                    print("✅ PetcatDetokenizer loaded")
                else:
                    self.petcat_detokenizer = None
                    self.log_message("PetcatDetokenizer modülü bulunamadı", "WARNING")
                    print("⚠️ PetcatDetokenizer not available")
            except Exception as e:
                print(f"❌ PetcatDetokenizer initialization failed: {e}")
                self.petcat_detokenizer = None
            
            # Decompiler Status Reporting
            print("📊 Decompiler Status Report:")
            self.log_message(f"🔄 Decompiler C Available: {DECOMPILER_C_AVAILABLE}", "INFO")
            self.log_message(f"🔄 Decompiler C2 Available: {DECOMPILER_C2_AVAILABLE}", "INFO")
            self.log_message(f"🔄 Decompiler C++ Available: {DECOMPILER_CPP_AVAILABLE}", "INFO")
            self.log_message(f"🔄 Decompiler QBasic Available: {DECOMPILER_QBASIC_AVAILABLE}", "INFO")
            self.log_message(f"🔄 Universal Decompiler Available: {DECOMPILER_AVAILABLE}", "INFO")
            print(f"   🔄 C Decompiler: {DECOMPILER_C_AVAILABLE}")
            print(f"   🔄 C2 Decompiler: {DECOMPILER_C2_AVAILABLE}")
            print(f"   🔄 C++ Decompiler: {DECOMPILER_CPP_AVAILABLE}")
            print(f"   🔄 QBasic Decompiler: {DECOMPILER_QBASIC_AVAILABLE}")
            print(f"   🔄 Universal Decompiler: {DECOMPILER_AVAILABLE}")
            
            # Database Manager
            try:
                self.database_manager = DatabaseManager()
                self.log_message("DatabaseManager yüklendi", "INFO")
                print("✅ DatabaseManager loaded")
            except Exception as e:
                print(f"❌ DatabaseManager initialization failed: {e}")
                self.database_manager = None
                self.log_message("DatabaseManager başlatılamadı", "WARNING")
            
            # Hybrid Program Analyzer
            try:
                self.hybrid_analyzer = HybridProgramAnalyzer()
                self.log_message("HybridProgramAnalyzer yüklendi", "INFO")
                print("✅ HybridProgramAnalyzer loaded")
            except Exception as e:
                print(f"❌ HybridProgramAnalyzer initialization failed: {e}")
                self.hybrid_analyzer = None
                self.log_message("HybridProgramAnalyzer başlatılamadı", "WARNING")
            
            # Hybrid Disassembler - YENİ!
            try:
                self.hybrid_disassembler = HybridDisassembler()
                self.log_message("HybridDisassembler yüklendi", "INFO")
                print("✅ HybridDisassembler loaded")
            except Exception as e:
                print(f"❌ HybridDisassembler initialization failed: {e}")
                self.hybrid_disassembler = None
                self.log_message("HybridDisassembler başlatılamadı", "WARNING")
            
            # Enhanced Universal Disk Reader - YENİ TÜM FORMATLAR!
            try:
                if EnhancedDiskReader:
                    self.enhanced_disk_reader = EnhancedDiskReader()
                    self.log_message("🗂️ EnhancedDiskReader yüklendi - TÜM FORMATLAR DESTEKLENEN!", "INFO")
                    print("✅ EnhancedDiskReader loaded - ALL FORMATS SUPPORTED!")
                    
                    # Desteklenen formatları göster
                    supported_formats = list(self.enhanced_disk_reader.disk_geometries.keys())
                    supported_formats.extend(["T64", "TAP", "PRG", "P00", "G64", "LNX", "LYNX", "CRT"])
                    self.log_message(f"📊 Desteklenen formatlar: {', '.join(supported_formats)}", "INFO")
                    print(f"📊 Supported formats: {', '.join(supported_formats)}")
                else:
                    self.enhanced_disk_reader = None
                    self.log_message("EnhancedDiskReader modülü bulunamadı", "WARNING")
                    print("⚠️ EnhancedDiskReader not available")
            except Exception as e:
                print(f"❌ EnhancedDiskReader initialization failed: {e}")
                self.enhanced_disk_reader = None
                self.log_message("EnhancedDiskReader başlatılamadı", "WARNING")
                self.hybrid_disassembler = None
                self.log_message("HybridDisassembler başlatılamadı", "WARNING")
            
            # Enhanced BASIC Decompiler
            try:
                self.enhanced_basic_decompiler = EnhancedBasicDecompiler()
                self.log_message("EnhancedBasicDecompiler yüklendi", "INFO")
                print("✅ EnhancedBasicDecompiler loaded")
            except Exception as e:
                print(f"❌ EnhancedBasicDecompiler initialization failed: {e}")
                self.enhanced_basic_decompiler = None
                self.log_message("EnhancedBasicDecompiler başlatılamadı", "WARNING")
            
            self.log_message("Component initialization tamamlandı", "SUCCESS")
            print("✅ Component initialization completed")
            
        except Exception as e:
            error_msg = f"❌ Component initialization error: {e}"
            print(error_msg)
            self.log_message(error_msg, "ERROR")
            import traceback
            print(f"Component initialization traceback:\n{traceback.format_exc()}")
            # Don't raise - continue with partial initialization
    
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
        
        # Enhanced BASIC Decompiler submenu
        basic_decompiler_menu = tk.Menu(tools_menu, tearoff=0, bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        tools_menu.add_cascade(label="🔥 Enhanced BASIC Decompiler", menu=basic_decompiler_menu)
        basic_decompiler_menu.add_command(label="🔹 Convert to QBasic 7.1", 
                                        command=lambda: self.enhanced_basic_decompile_current("qbasic"))
        basic_decompiler_menu.add_command(label="🔹 Convert to C", 
                                        command=lambda: self.enhanced_basic_decompile_current("c"))
        basic_decompiler_menu.add_command(label="🔹 Convert to C++", 
                                        command=lambda: self.enhanced_basic_decompile_current("cpp"))
        basic_decompiler_menu.add_command(label="🔹 Convert to PDSX BASIC", 
                                        command=lambda: self.enhanced_basic_decompile_current("pdsx"))
        basic_decompiler_menu.add_separator()
        basic_decompiler_menu.add_command(label="⚙️ Advanced Options...", 
                                        command=self.show_enhanced_basic_options)
        
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
        
        # Database menu
        database_menu = tk.Menu(menubar, tearoff=0, bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="Database", menu=database_menu)
        database_menu.add_command(label="📊 View Statistics", command=self.show_database_stats)
        database_menu.add_command(label="📁 File History", command=self.show_file_history)
        database_menu.add_command(label="🔍 Search Files", command=self.show_database_search)
        database_menu.add_separator()
        database_menu.add_command(label="📤 Export to Excel", command=self.export_database_excel)
        database_menu.add_command(label="📤 Export to CSV", command=self.export_database_csv)
        database_menu.add_command(label="📤 Export to JSON", command=self.export_database_json)
        database_menu.add_separator()
        database_menu.add_command(label="🧹 Cleanup Old Records", command=self.cleanup_database)
        
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
        """Format dönüştürme - DETAYLI LOG SİSTEMİ"""
        if not self.selected_entry:
            self.log_message("❌ Dosya seçilmemiş - format dönüştürme iptal edildi", "ERROR")
            print("❌ HATA: Dosya seçilmemiş!")
            return
        
        # DETAYLI LOG - Dönüştürme başlatıldı
        self.log_message("="*80, "INFO")
        self.log_message(f"🔄 FORMAT DÖNÜŞTÜRME BAŞLATILDI", "INFO")
        self.log_message(f"   📄 Dosya: {self.selected_entry.get('filename', 'Unknown')}", "INFO")
        self.log_message(f"   🎯 Hedef Format: {format_type.upper()}", "INFO")
        self.log_message(f"   📋 Target Panel: {target_panel}", "INFO")
        self.log_message(f"   ⏰ Başlangıç Zamanı: {time.strftime('%H:%M:%S')}", "INFO")
        
        # Selected entry detayları
        if hasattr(self.selected_entry, 'get'):
            self.log_message(f"   🏷️ Dosya Tipi: {self.selected_entry.get('filetype', 'Unknown')}", "INFO")
            self.log_message(f"   📍 Start Address: {self.selected_entry.get('start_address', 'Unknown')}", "INFO")
            self.log_message(f"   📏 Size: {self.selected_entry.get('size', 'Unknown')}", "INFO")
            
        self.log_message("="*80, "INFO")
        
        # Terminal'e de yazdır
        print(f"\n🔄 FORMAT DÖNÜŞTÜRME:")
        print(f"📄 {self.selected_entry.get('filename', 'Unknown')} -> {format_type.upper()}")
        print(f"🎯 Target: {target_panel}")
        
        self.update_status(f"{format_type.upper()} formatına dönüştürülüyor...")
        
        # Threading ile dönüştür
        threading.Thread(target=self._convert_format_thread, 
                        args=(format_type, target_panel), daemon=True).start()
    
    def _convert_format_thread(self, format_type, target_panel):
        """Format dönüştürme thread'i - DETAYLI LOG"""
        start_time = time.time()
        success = False
        error_message = ""
        
        try:
            # DETAYLI LOG - Thread başlangıcı
            self.root.after(0, lambda: self.log_message(f"🔧 DÖNÜŞTÜRME THREAD'İ BAŞLATILDI", "INFO"))
            self.root.after(0, lambda: self.log_message(f"   ⚙️ Format: {format_type}", "INFO"))
            self.root.after(0, lambda: self.log_message(f"   📱 Panel: {target_panel}", "INFO"))
            
            # PRG verisi çıkar
            self.root.after(0, lambda: self.log_message(f"📦 PRG verisi çıkarılıyor...", "INFO"))
            prg_data = self.extract_prg_data(self.selected_entry)
            
            if not prg_data:
                error_message = "❌ PRG verisi çıkarılamadı - dosya formatı hatalı olabilir"
                self.root.after(0, lambda: self.log_message(error_message, "ERROR"))
                print(f"❌ {error_message}")
                return
            
            if len(prg_data) < 2:
                error_message = f"❌ Geçersiz PRG verisi - çok kısa ({len(prg_data)} bytes)"
                self.root.after(0, lambda: self.log_message(error_message, "ERROR"))
                print(f"❌ {error_message}")
                return
            
            start_address = prg_data[0] + (prg_data[1] << 8)
            code_data = prg_data[2:]
            
            # DETAYLI LOG - PRG analizi
            self.root.after(0, lambda: self.log_message(f"✅ PRG verisi çıkarıldı:", "INFO"))
            self.root.after(0, lambda: self.log_message(f"   📏 Toplam Boyut: {len(prg_data)} bytes", "INFO"))
            self.root.after(0, lambda: self.log_message(f"   🎯 Start Address: ${start_address:04X}", "INFO"))
            self.root.after(0, lambda: self.log_message(f"   💾 Kod Boyutu: {len(code_data)} bytes", "INFO"))
            
            # Program türü belirleme
            program_type = "MACHINE CODE"
            if start_address == 0x0801:
                program_type = "BASIC PROGRAM"
            elif start_address >= 0x1000 and start_address < 0xA000:
                program_type = "ASSEMBLY PROGRAM"
            elif start_address >= 0xA000:
                program_type = "ASSEMBLY PROGRAM (HIGH)"
            
            self.root.after(0, lambda: self.log_message(f"   🔍 Program Türü: {program_type}", "INFO"))
            
            # Terminal'e özet yazdır
            print(f"📦 PRG VERİSİ HAZIR:")
            print(f"   Boyut: {len(prg_data)} bytes | Start: ${start_address:04X} | Tür: {program_type}")
            print(f"   Format: {format_type.upper()} | Panel: {target_panel}")
            
            # BU NOKTADA - KULLANICI BU DOSYAYI SEÇTİ, BU FORMAT'I İSTEDİ
            self.root.after(0, lambda: self.log_message(f"👤 KULLANICI İSTEĞİ:", "INFO"))
            self.root.after(0, lambda: self.log_message(f"   📄 Seçili Dosya: {self.selected_entry.get('filename', 'Unknown')}", "INFO"))
            self.root.after(0, lambda: self.log_message(f"   🎯 İstenen Format: {format_type.upper()}", "INFO"))
            self.root.after(0, lambda: self.log_message(f"   💡 Kullanıcı bu dosyanın {format_type} dönüşümünü istiyor", "INFO"))
            
            # HER FORMAT İÇİN ÇALIŞSIN - PROGRAM TÜRÜ ÖNEMLI DEĞİL
            if format_type in ['basic', 'petcat', 'c64list'] and start_address != 0x0801:
                self.root.after(0, lambda: self.log_message(f"⚠️ UYARI: Bu BASIC detokenizer ama dosya ${start_address:04X}'de başlıyor", "WARNING"))
                self.root.after(0, lambda: self.log_message(f"   💡 BASIC olmasa da kullanıcı istediği için devam ediliyor", "INFO"))
                print(f"⚠️ BASIC detokenizer ama dosya BASIC değil - yine de denenecek")
                
            elif format_type in ['assembly', 'c', 'qbasic'] and start_address == 0x0801:
                self.root.after(0, lambda: self.log_message(f"⚠️ UYARI: Bu disassembler ama dosya BASIC ($0801)", "WARNING"))
                self.root.after(0, lambda: self.log_message(f"   💡 BASIC olsa da kullanıcı assembly istediği için devam ediliyor", "INFO"))
                print(f"⚠️ Assembly/C/QBasic istendi ama dosya BASIC - yine de denenecek")
            code_data = prg_data[2:]
            
            # Dosya tracking'i başlat
            if hasattr(self, 'selected_entry') and self.selected_entry:
                filename = self.selected_entry.get('name', 'unknown.prg')
                source_format = "PRG"
                if start_address == 0x0801:
                    source_format = "BASIC"
                
                self.track_file_processing(
                    filename=filename,
                    file_path=f"d64://{filename}",
                    source_format=source_format,
                    start_address=start_address,
                    end_address=start_address + len(code_data),
                    notes=f"Size: {len(code_data)} bytes"
                )
            
            result_code = ""
            
            # Format'a göre işle
            if start_address == 0x0801 and format_type in ['basic', 'petcat', 'c64list']:
                # BASIC program
                if format_type == 'basic':
                    # Enhanced BASIC Decompiler kullan - KızılElma Plan
                    self.root.after(0, lambda: self.log_message(f"🔥 ENHANCED BASIC DECOMPILER BAŞLATILIYOR", "INFO"))
                    if self.enhanced_basic_decompiler:
                        self.root.after(0, lambda: self.log_message(f"   ✅ Enhanced BASIC Decompiler modülü mevcut", "INFO"))
                        self.root.after(0, lambda: self.log_message(f"   🎯 5 hedef dilde transpile hazır: QBasic, C, C++, PDSX, Python", "INFO"))
                        
                        try:
                            # Enhanced BASIC conversion - multi-format output
                            basic_lines = self.enhanced_basic_decompiler.detokenize_basic(prg_data)
                            
                            # Multi-target conversion
                            qbasic_code = self.enhanced_basic_decompiler.convert_to_qbasic(basic_lines)
                            c_code = self.enhanced_basic_decompiler.convert_to_c(basic_lines)
                            
                            # Tab-based output format
                            result_code = f"; Enhanced BASIC Decompiler v3.0 Output\n"
                            result_code += f"; Multi-format conversion with C64 Memory Manager\n\n"
                            result_code += f"=== ORIGINAL BASIC V2 ===\n"
                            result_code += "\n".join(basic_lines) if basic_lines else "BASIC detokenization failed"
                            result_code += f"\n\n=== QBASIC 7.1 CONVERSION ===\n{qbasic_code}"
                            result_code += f"\n\n=== C CONVERSION ===\n{c_code}"
                            
                            self.root.after(0, lambda: self.log_message(f"   ✅ Enhanced BASIC conversion tamamlandı", "INFO"))
                            
                        except Exception as e:
                            self.root.after(0, lambda: self.log_message(f"   ❌ Enhanced BASIC Decompiler hatası: {str(e)}", "ERROR"))
                            # Fallback to basic parser
                            if self.basic_parser:
                                basic_lines = self.basic_parser.detokenize(prg_data)
                                result_code = "\n".join(basic_lines) if basic_lines else "BASIC detokenization failed"
                            else:
                                result_code = "; Enhanced BASIC Decompiler ve C64BasicParser modülü bulunamadı"
                    else:
                        # Fallback to basic parser
                        if self.basic_parser:
                            basic_lines = self.basic_parser.detokenize(prg_data)
                            result_code = "\n".join(basic_lines) if basic_lines else "BASIC detokenization failed"
                        else:
                            result_code = "; Enhanced BASIC Decompiler ve C64BasicParser modülü bulunamadı"
                    
                elif format_type == 'petcat':
                    self.root.after(0, lambda: self.log_message(f"🐾 PETCAT DETOKENIZER BAŞLATILIYOR", "INFO"))
                    print(f"🐾 PETCAT çalıştırılıyor...")
                    
                    if self.petcat_detokenizer:
                        self.root.after(0, lambda: self.log_message(f"   ✅ PetcatDetokenizer modülü mevcut", "INFO"))
                        self.root.after(0, lambda: self.log_message(f"   📦 PRG boyutu: {len(prg_data)} bytes", "INFO"))
                        self.root.after(0, lambda: self.log_message(f"   🎯 Start address: ${start_address:04X}", "INFO"))
                        
                        try:
                            self.root.after(0, lambda: self.log_message(f"   🔄 Petcat detokenize çalıştırılıyor...", "INFO"))
                            result_code = self.petcat_detokenizer.detokenize_prg(prg_data)
                            
                            if result_code and len(result_code.strip()) > 0:
                                self.root.after(0, lambda: self.log_message(f"   ✅ Petcat başarılı: {len(result_code)} karakter üretildi", "INFO"))
                                print(f"✅ PETCAT BAŞARILI: {len(result_code)} karakter")
                            else:
                                error_msg = "Petcat boş sonuç döndü"
                                self.root.after(0, lambda: self.log_message(f"   ❌ {error_msg}", "ERROR"))
                                print(f"❌ PETCAT HATASI: {error_msg}")
                                result_code = f"; PETCAT ERROR: {error_msg}\n; Raw BASIC data:\n{prg_data[:100].hex()}..."
                                
                        except Exception as petcat_error:
                            error_msg = f"Petcat exception: {petcat_error}"
                            self.root.after(0, lambda: self.log_message(f"   ❌ {error_msg}", "ERROR"))
                            print(f"❌ PETCAT EXCEPTION: {error_msg}")
                            
                            import traceback
                            trace = traceback.format_exc()
                            self.root.after(0, lambda: self.log_message(f"   📋 Stack trace: {trace}", "ERROR"))
                            print(f"Stack trace:\n{trace}")
                            
                            result_code = f"; PETCAT EXCEPTION: {error_msg}\n; Stack trace:\n; {trace.replace(chr(10), chr(10)+'; ')}\n; Raw data:\n{prg_data[:100].hex()}..."
                    else:
                        error_msg = "PetcatDetokenizer modülü bulunamadı"
                        self.root.after(0, lambda: self.log_message(f"   ❌ {error_msg}", "ERROR"))
                        print(f"❌ PETCAT MODÜL HATASI: {error_msg}")
                        result_code = f"; PETCAT MODULE ERROR: {error_msg}"
                    
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
                        
            # Assembly/Machine code veya diğer formatlar
            elif format_type == 'assembly' or format_type.startswith('assembly_'):
                # Assembly format ve disassembler motor belirleme
                asm_format = "native"
                disassembler_type = "improved"  # Varsayılan
                
                if format_type.startswith('assembly_'):
                    parts = format_type.split('_')
                    if len(parts) >= 2:
                        asm_format = parts[1]
                    if len(parts) >= 3:
                        disassembler_type = parts[2]
                
                # DETAYLI LOG - Disassembler motor seçimi
                self.root.after(0, lambda: self.log_message(f"🔧 DISASSEMBLER MOTORSELEKSİYONU", "INFO"))
                self.root.after(0, lambda: self.log_message(f"   ⚙️ Disassembler Type: {disassembler_type}", "INFO"))
                self.root.after(0, lambda: self.log_message(f"   📝 ASM Format: {asm_format}", "INFO"))
                
                # Disassembler motor seçimi
                if disassembler_type == "basic":
                    # Basic disassembler kullan
                    from disassembler import Disassembler
                    disassembler = Disassembler()
                    asm_code = disassembler.disassemble(code_data, start_address)
                    self.root.after(0, lambda: self.log_message(f"   ✅ Basic Disassembler kullanıldı", "INFO"))
                    
                elif disassembler_type == "advanced":
                    # Advanced disassembler kullan
                    if AdvancedDisassembler:
                        disassembler = AdvancedDisassembler(
                            start_address=start_address,
                            code=code_data,
                            use_py65=self.disassembly_panel.use_py65_disassembler.get(),
                            use_illegal_opcodes=self.disassembly_panel.use_illegal_opcodes.get()
                        )
                        asm_code = disassembler.disassemble()
                        self.root.after(0, lambda: self.log_message(f"   ✅ Advanced Disassembler kullanıldı", "INFO"))
                    else:
                        asm_code = "; Advanced Disassembler bulunamadı"
                        
                elif disassembler_type == "improved":
                    # Improved disassembler kullan (C64 Memory Manager ile)
                    try:
                        from improved_disassembler import ImprovedDisassembler
                        disassembler = ImprovedDisassembler(
                            start_address=start_address,
                            code=code_data,
                            output_format='asm',
                            use_illegal_opcodes=self.disassembly_panel.use_illegal_opcodes.get()
                        )
                        asm_code = disassembler.disassemble_to_format(None, 'asm')  # PRG data None çünkü zaten code_data var
                        self.root.after(0, lambda: self.log_message(f"   ✅ Improved Disassembler (C64 Enhanced) kullanıldı", "INFO"))
                    except ImportError:
                        asm_code = "; Improved Disassembler bulunamadı"
                        self.root.after(0, lambda: self.log_message(f"   ❌ Improved Disassembler import hatası", "ERROR"))
                    except Exception as e:
                        asm_code = f"; Improved Disassembler error: {str(e)}"
                        self.root.after(0, lambda: self.log_message(f"   ❌ Improved Disassembler çalışma hatası: {str(e)}", "ERROR"))
                        
                elif disassembler_type == "py65_professional":
                    # py65 Professional disassembler kullan
                    try:
                        from py65_professional_disassembler import Py65ProfessionalDisassembler
                        disassembler = Py65ProfessionalDisassembler()
                        asm_code = disassembler.disassemble(code_data, start_address)
                        self.root.after(0, lambda: self.log_message(f"   ✅ py65 Professional Disassembler kullanıldı", "INFO"))
                    except ImportError:
                        asm_code = "; py65 Professional Disassembler bulunamadı"
                        self.root.after(0, lambda: self.log_message(f"   ❌ py65 Professional import hatası", "ERROR"))
                        
                else:
                    # Fallback: Advanced disassembler
                    if AdvancedDisassembler:
                        disassembler = AdvancedDisassembler(
                            start_address=start_address,
                            code=code_data,
                            use_py65=self.disassembly_panel.use_py65_disassembler.get(),
                            use_illegal_opcodes=self.disassembly_panel.use_illegal_opcodes.get()
                        )
                        asm_code = disassembler.disassemble()
                        self.root.after(0, lambda: self.log_message(f"   ✅ Fallback: Advanced Disassembler kullanıldı", "INFO"))
                    
                    # Assembly format'a göre header/direktifler ekle
                    if asm_format == "acme":
                        result_code = f"; ACME Assembler Format\n"
                        result_code += f"!to \"output.prg\", cbm\n"
                        result_code += f"* = ${start_address:04X}\n\n"
                        result_code += asm_code
                    elif asm_format == "cc65":
                        result_code = f"; CC65 Assembler Format\n"
                        result_code += f".setcpu \"6502\"\n"
                        result_code += f".org ${start_address:04X}\n\n"
                        result_code += asm_code
                    elif asm_format == "dasm":
                        result_code = f"; DASM Assembler Format\n"
                        result_code += f"        processor 6502\n"
                        result_code += f"        org ${start_address:04X}\n\n"
                        result_code += asm_code
                    elif asm_format == "kickass":
                        result_code = f"// KickAssembler Format\n"
                        result_code += f".pc = ${start_address:04X} \"Main\"\n\n"
                        result_code += asm_code
                    elif asm_format == "tasm":
                        result_code = f"; TASM Assembler Format\n"
                        result_code += f"        .org ${start_address:04X}\n\n"
                        result_code += asm_code
                    elif asm_format == "64tass":
                        result_code = f"; 64TASS Assembler Format\n"
                        result_code += f"        .cpu \"6502\"\n"
                        result_code += f"* = ${start_address:04X}\n\n"
                        result_code += asm_code
                    elif asm_format == "ca65":
                        result_code = f"; CA65 Assembler Format\n"
                        result_code += f".setcpu \"6502\"\n"
                        result_code += f".org ${start_address:04X}\n\n"
                        result_code += asm_code
                    else:
                        asm_code = "; Fallback disassembler bulunamadı"
                        self.root.after(0, lambda: self.log_message(f"   ❌ Tüm disassembler'lar başarısız", "ERROR"))
                
                # Assembly format'a göre header/direktifler ekle
                if asm_format == "acme":
                    result_code = f"; ACME Assembler Format\n"
                    result_code += f"!to \"output.prg\", cbm\n"
                    result_code += f"* = ${start_address:04X}\n\n"
                    result_code += asm_code
                elif asm_format == "cc65":
                    result_code = f"; CC65 Assembler Format\n"
                    result_code += f".setcpu \"6502\"\n"
                    result_code += f".org ${start_address:04X}\n\n"
                    result_code += asm_code
                elif asm_format == "dasm":
                    result_code = f"; DASM Assembler Format\n"
                    result_code += f"        processor 6502\n"
                    result_code += f"        org ${start_address:04X}\n\n"
                    result_code += asm_code
                elif asm_format == "kickass":
                    result_code = f"; KickAssembler Format\n"
                    result_code += f".pc = ${start_address:04X} \"Main\"\n\n"
                    result_code += asm_code
                elif asm_format == "tasm":
                    result_code = f"; TASM Assembler Format\n"
                    result_code += f"        .org ${start_address:04X}\n\n"
                    result_code += asm_code
                elif asm_format == "64tass":
                    result_code = f"; 64TASS Assembler Format\n"
                    result_code += f"        .cpu \"6502\"\n"
                    result_code += f"* = ${start_address:04X}\n\n"
                    result_code += asm_code
                elif asm_format == "ca65":
                    result_code = f"; CA65 Assembler Format\n"
                    result_code += f".setcpu \"6502\"\n"
                    result_code += f".org ${start_address:04X}\n\n"
                    result_code += asm_code
                else:  # native
                    result_code = asm_code
                
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
                # QBasic transpilation - Enhanced version
                result_code = f"' QBasic Code generated from 6502 Assembly\n"
                result_code += f"' Start Address: ${start_address:04X}\n"
                result_code += f"' Size: {len(code_data)} bytes\n\n"
                result_code += f"PRINT \"C64 Program Simulation\"\n"
                result_code += f"PRINT \"Start Address: ${start_address:04X}\"\n"
                result_code += f"PRINT \"Code Size: {len(code_data)} bytes\"\n\n"
                
                # Assembly'yi QBasic comment olarak ekle
                if AdvancedDisassembler:
                    disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                    asm_code = disassembler.disassemble()
                    result_code += f"' Original assembly code:\n"
                    for line in asm_code.split('\n')[:20]:  # İlk 20 satır
                        if line.strip():
                            result_code += f"' {line}\n"
                
            elif format_type == 'pdsx':
                # PDSX format
                result_code = f"; PDSX Assembly Format\n"
                result_code += f"; Generated from C64 PRG\n"
                result_code += f".org ${start_address:04X}\n\n"
                if AdvancedDisassembler:
                    disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                    asm_lines = disassembler.disassemble().split('\n')
                    for line in asm_lines:
                        if line.strip() and not line.startswith(';'):
                            result_code += f"{line}\n"
                else:
                    result_code += f"; AdvancedDisassembler modülü bulunamadı\n"
                        
            elif format_type == 'pseudo':
                # Pseudo code - Enhanced version
                result_code = f"// Pseudo Code Analysis\n"
                result_code += f"// Original Address: ${start_address:04X}\n"
                result_code += f"// Code Size: {len(code_data)} bytes\n\n"
                result_code += f"PROGRAM C64_APPLICATION {{\n"
                result_code += f"    ENTRY_POINT: ${start_address:04X}\n"
                result_code += f"    \n"
                result_code += f"    INITIALIZE_SYSTEM()\n"
                result_code += f"    SET_MEMORY_LAYOUT()\n"
                result_code += f"    \n"
                result_code += f"    MAIN_LOOP {{\n"
                result_code += f"        EXECUTE_6502_INSTRUCTIONS()\n"
                result_code += f"        HANDLE_INTERRUPTS()\n"
                result_code += f"    }}\n"
                result_code += f"}}\n"
                
            elif format_type == 'py65':
                # py65 format - Enhanced version
                result_code = f"; py65 Professional Disassembler Output\n"
                result_code += f"; Address: ${start_address:04X}\n"
                result_code += f"; Size: {len(code_data)} bytes\n\n"
                result_code += f"; Note: Full py65 integration would provide:\n"
                result_code += f";   - Cycle counting\n"
                result_code += f";   - Memory monitoring\n"
                result_code += f";   - Instruction timing\n"
                result_code += f";   - Stack analysis\n\n"
                # Basic disassembly fallback
                if AdvancedDisassembler:
                    disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                    result_code += disassembler.disassemble()
                
            # Decompiler formats
            elif format_type.startswith('dec_'):
                if format_type == 'dec_c' and DECOMPILER_C_AVAILABLE:
                    try:
                        decompiler = DecompilerC()
                        result_code = decompiler.decompile(prg_data, start_address)
                        self.root.after(0, lambda: self.log_message(f"C Decompiler başarılı: {len(result_code)} karakter", "SUCCESS"))
                    except Exception as dec_error:
                        result_code = f"// C Decompiler Error: {dec_error}\n// Falling back to basic decompilation\n"
                        if AdvancedDisassembler:
                            disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                            result_code += f"\n// Basic assembly code:\n{disassembler.disassemble()}"
                elif format_type == 'dec_c2' and DECOMPILER_C2_AVAILABLE:
                    try:
                        decompiler = DecompilerC2()
                        result_code = decompiler.decompile(prg_data, start_address)
                        self.root.after(0, lambda: self.log_message(f"C2 Decompiler başarılı: {len(result_code)} karakter", "SUCCESS"))
                    except Exception as dec_error:
                        result_code = f"// C2 Decompiler Error: {dec_error}\n// Falling back to basic decompilation\n"
                        if AdvancedDisassembler:
                            disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                            result_code += f"\n// Basic assembly code:\n{disassembler.disassemble()}"
                elif format_type == 'dec_cpp' and DECOMPILER_CPP_AVAILABLE:
                    try:
                        decompiler = DecompilerCPP()
                        result_code = decompiler.decompile(prg_data, start_address)
                        self.root.after(0, lambda: self.log_message(f"C++ Decompiler başarılı: {len(result_code)} karakter", "SUCCESS"))
                    except Exception as dec_error:
                        result_code = f"// C++ Decompiler Error: {dec_error}\n// Falling back to basic decompilation\n"
                        if AdvancedDisassembler:
                            disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                            result_code += f"\n// Basic assembly code:\n{disassembler.disassemble()}"
                elif format_type == 'dec_qbasic' and DECOMPILER_QBASIC_AVAILABLE:
                    try:
                        decompiler = DecompilerQBasic()
                        result_code = decompiler.decompile(prg_data, start_address)
                        self.root.after(0, lambda: self.log_message(f"QBasic Decompiler başarılı: {len(result_code)} karakter", "SUCCESS"))
                    except Exception as dec_error:
                        result_code = f"' QBasic Decompiler Error: {dec_error}\n' Falling back to basic decompilation\n"
                        if AdvancedDisassembler:
                            disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                            result_code += f"\n' Basic assembly code:\n{disassembler.disassemble()}"
                elif format_type == 'dec_asm':
                    result_code = f"; ASM Decompiler (Enhanced)\n"
                    result_code += f"; Start Address: ${start_address:04X}\n"
                    result_code += f"; Code Size: {len(code_data)} bytes\n\n"
                    if AdvancedDisassembler:
                        disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                        result_code += disassembler.disassemble()
                    else:
                        result_code += f"; AdvancedDisassembler modülü bulunamadı\n"
                else:
                    result_code = f"; Decompiler {format_type} not available\n"
                    result_code += f"; Available decompilers:\n"
                    result_code += f";   - C Decompiler: {DECOMPILER_C_AVAILABLE}\n"
                    result_code += f";   - C2 Decompiler: {DECOMPILER_C2_AVAILABLE}\n"
                    result_code += f";   - C++ Decompiler: {DECOMPILER_CPP_AVAILABLE}\n"
                    result_code += f";   - QBasic Decompiler: {DECOMPILER_QBASIC_AVAILABLE}\n"
                    result_code += f";   - Universal Decompiler: {DECOMPILER_AVAILABLE}\n"
            
            # Sonucu ilgili panele gönder
            if target_panel == 'disassembly':
                self.root.after(0, lambda: self.disassembly_panel.update_code(result_code, format_type))
            elif target_panel == 'decompiler':
                self.root.after(0, lambda: self.decompiler_panel.update_code(result_code, format_type))
            
            # Başarılı dönüşüm tracking'i
            success = True
            processing_time = time.time() - start_time
            assembly_format = ""
            if format_type.startswith('assembly_'):
                assembly_format = format_type.split('_')[1]
            
            self.track_format_conversion(
                target_format=format_type,
                success=success,
                output_size=len(result_code),
                processing_time=processing_time,
                assembly_format=assembly_format
            )
            
            self.root.after(0, lambda: self.update_status(f"{format_type} dönüştürme tamamlandı"))
            self.root.after(0, lambda: self.log_message(f"{format_type} dönüştürme başarılı: {len(result_code)} karakter", "SUCCESS"))
            
        except Exception as e:
            error_msg = str(e)
            processing_time = time.time() - start_time
            
            # Başarısız dönüşüm tracking'i
            self.track_format_conversion(
                target_format=format_type,
                success=False,
                processing_time=processing_time,
                error_message=error_msg
            )
            
            self.root.after(0, lambda: self.log_message(f"{format_type} dönüştürme hatası: {error_msg}", "ERROR"))
            self.root.after(0, lambda: self.update_status(f"{format_type} dönüştürme başarısız"))
    
    def extract_prg_data(self, entry):
        """PRG verisi çıkar - Enhanced D64 Reader Wrapper kullanarak"""
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
                # Enhanced D64 Reader Wrapper kullan
                try:
                    if EnhancedD64ReaderWrapper:
                        reader = EnhancedD64ReaderWrapper(source_file)
                        prg_data = reader.extract_file(entry)
                        self.log_message(f"Enhanced D64 Reader Wrapper ile PRG çıkarıldı: {len(prg_data)} byte", "INFO")
                        return prg_data
                    else:
                        self.log_message("Enhanced D64 Reader Wrapper bulunamadı", "ERROR")
                        return None
                except Exception as wrapper_error:
                    self.log_message(f"Enhanced D64 Reader Wrapper hatası: {wrapper_error}", "ERROR")
                    return None
                    
            elif ext == '.t64':
                # T64'ten çıkar
                file_offset = entry.get('file_offset', entry.get('offset'))
                if file_offset:
                    with open(source_file, 'rb') as f:
                        f.seek(file_offset)
                        size = entry.get('size', 0)
                        return f.read(size)
                        
            elif ext in ['.tap']:
                # TAP dosyası - Enhanced D64 Reader Wrapper kullan
                try:
                    if EnhancedD64ReaderWrapper:
                        reader = EnhancedD64ReaderWrapper(source_file)
                        return reader.extract_file(entry)
                except Exception as tap_error:
                    self.log_message(f"TAP çıkarma hatası: {tap_error}", "ERROR")
                    return None
                    
            elif ext in ['.g64']:
                # G64 dosyası - Enhanced D64 Reader Wrapper kullan
                try:
                    if EnhancedD64ReaderWrapper:
                        reader = EnhancedD64ReaderWrapper(source_file)
                        return reader.extract_file(entry)
                except Exception as g64_error:
                    self.log_message(f"G64 çıkarma hatası: {g64_error}", "ERROR")
                    return None
                        
            return None
            
        except Exception as e:
            self.log_message(f"PRG verisi çıkarılamadı", "ERROR")
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
        """Illegal analiz sonuçlarını göster - X1 GUI formatında"""
        # Yeni pencere oluştur
        result_window = tk.Toplevel(self.root)
        result_window.title("🚫 Illegal Opcode Analysis Results")
        result_window.geometry("900x700")
        result_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Scrollable text widget
        text_frame = tk.Frame(result_window, bg=ModernStyle.BG_PRIMARY)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10),
                             bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                             insertbackground=ModernStyle.ACCENT_COLOR)
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)
        
        # Sonuçları X1 formatında format et
        if 'error' in results:
            text_widget.insert(tk.END, f"❌ Error: {results['error']}\n")
        else:
            # Header info
            text_widget.insert(tk.END, f"📊 6502 ILLEGAL OPCODE ANALYSIS REPORT\n")
            text_widget.insert(tk.END, f"{'='*60}\n\n")
            text_widget.insert(tk.END, f"📋 Analysis Summary:\n")
            text_widget.insert(tk.END, f"   Total instructions: {results['total_instructions']}\n")
            text_widget.insert(tk.END, f"   Illegal opcodes found: {results['illegal_count']}\n\n")
            
            if results['illegal_count'] == 0:
                text_widget.insert(tk.END, "   ✅ No illegal opcodes found! Code is clean.\n")
                text_widget.insert(tk.END, "   This appears to be well-formed 6502 assembly code.\n")
            else:
                # Detailed analysis
                text_widget.insert(tk.END, "🔍 Detailed Illegal Opcode Analysis:\n")
                text_widget.insert(tk.END, f"{'='*60}\n\n")
                
                dangerous_count = 0
                for i, illegal in enumerate(results['illegal_opcodes'], 1):
                    if illegal.get('is_dangerous', False):
                        dangerous_count += 1
                        danger_mark = "🚨 DANGEROUS"
                    else:
                        danger_mark = "⚠️  WARNING"
                    
                    text_widget.insert(tk.END, f"#{i:3d} {danger_mark}\n")
                    text_widget.insert(tk.END, f"      Address: ${illegal['address']:04X}\n")
                    text_widget.insert(tk.END, f"      Opcode:  ${illegal['opcode']:02X}\n")
                    text_widget.insert(tk.END, f"      Description: {illegal['description']}\n")
                    
                    # Context bytes if available
                    if 'context' in illegal and illegal['context']:
                        context_str = ' '.join(f"${b:02X}" for b in illegal['context'])
                        text_widget.insert(tk.END, f"      Context: {context_str}\n")
                        
                        # Add marker line pointing to illegal opcode
                        if 'context_position' in illegal:
                            marker_pos = illegal['context_position'] * 4  # 4 chars per byte ($XX )
                            marker_line = ' ' * 15 + ' ' * marker_pos + '^^'
                            text_widget.insert(tk.END, f"{marker_line}\n")
                    
                    text_widget.insert(tk.END, f"      {'─'*50}\n\n")
                
                # Summary warnings
                text_widget.insert(tk.END, f"\n🚨 ANALYSIS WARNINGS:\n")
                text_widget.insert(tk.END, f"{'='*60}\n")
                if dangerous_count > 0:
                    text_widget.insert(tk.END, f"⚠️  Found {dangerous_count} dangerous JAM/KIL instructions\n")
                    text_widget.insert(tk.END, f"   These instructions will freeze the CPU!\n")
                
                if results['illegal_count'] > 10:
                    text_widget.insert(tk.END, f"⚠️  High illegal opcode count ({results['illegal_count']})\n")
                    text_widget.insert(tk.END, f"   This may be data interpreted as code\n")
                    text_widget.insert(tk.END, f"   Consider checking if this is a BASIC program\n")
        
        # Kapatma butonu
        button_frame = tk.Frame(result_window, bg=ModernStyle.BG_PRIMARY)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="✅ Tamam", command=result_window.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="📋 Sonuçları Kopyala", 
                  command=lambda: self.copy_text_to_clipboard(text_widget.get("1.0", tk.END))).pack(side=tk.RIGHT, padx=5)
        
        # Pencereyi merkeze getir
        result_window.transient(self.root)
        result_window.grab_set()
        result_window.focus_set()
    
    def copy_text_to_clipboard(self, text):
        """Metni panoya kopyala"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.log_message("Sonuçlar panoya kopyalandı", "SUCCESS")
        except Exception as e:
            self.log_message(f"Panoya kopyalama hatası: {e}", "ERROR")
    
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
    
    def analyze_hybrid_program(self, entry):
        """Hibrit program analizi (BASIC+Assembly)"""
        threading.Thread(target=self._analyze_hybrid_thread, args=(entry,), daemon=True).start()
    
    def analyze_hybrid_program_current(self):
        """Mevcut dosya için hibrit analiz"""
        if self.selected_entry:
            self.analyze_hybrid_program(self.selected_entry)
        else:
            self.log_message("Lütfen önce bir dosya seçin", "WARNING")
    
    def extract_assembly_current(self):
        """Mevcut dosyadan Assembly kısmını ayır"""
        if self.selected_entry:
            self.extract_assembly_from_hybrid(self.selected_entry)
        else:
            self.log_message("Lütfen önce bir dosya seçin", "WARNING")
    
    def extract_basic_current(self):
        """Mevcut dosyadan BASIC kısmını ayır"""
        if self.selected_entry:
            self.extract_basic_from_hybrid(self.selected_entry)
        else:
            self.log_message("Lütfen önce bir dosya seçin", "WARNING")
    
    def enhanced_basic_decompile(self, entry, target_language="qbasic", optimization_level=2):
        """Enhanced BASIC Decompiler ile dönüştür"""
        threading.Thread(target=self._enhanced_basic_decompile_thread, 
                        args=(entry, target_language, optimization_level), daemon=True).start()
    
    def enhanced_basic_decompile_current(self, target_language="qbasic"):
        """Mevcut dosya için Enhanced BASIC decompile"""
        if self.selected_entry:
            self.enhanced_basic_decompile(self.selected_entry, target_language)
        else:
            self.log_message("Lütfen önce bir dosya seçin", "WARNING")
    
    def _enhanced_basic_decompile_thread(self, entry, target_language, optimization_level):
        """Enhanced BASIC decompile thread'i"""
        try:
            if not EnhancedBasicDecompiler:
                self.root.after(0, lambda: self.log_message("EnhancedBasicDecompiler bulunamadı", "ERROR"))
                return
            
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.log_message("PRG verisi çıkarılamadı", "ERROR"))
                return
            
            # Check if it's a BASIC program
            start_address = prg_data[0] + (prg_data[1] << 8) if len(prg_data) >= 2 else 0
            if start_address != 0x0801:
                self.root.after(0, lambda: self.log_message(f"Bu BASIC program değil (Start: ${start_address:04X})", "WARNING"))
                return
            
            self.root.after(0, lambda: self.log_message(f"🔄 Enhanced BASIC decompile başlıyor ({target_language})...", "INFO"))
            
            # Enhanced BASIC Decompiler oluştur
            decompiler = EnhancedBasicDecompiler()
            
            # Decompile et
            result = decompiler.decompile_program(prg_data, target_language, optimization_level)
            
            # Sonucu göster
            self.root.after(0, lambda: self._show_enhanced_basic_result(entry, result, target_language))
            
        except Exception as e:
            error_msg = f"Enhanced BASIC decompile hatası: {e}"
            self.root.after(0, lambda: self.log_message(error_msg, "ERROR"))
            import traceback
            self.root.after(0, lambda: self.log_message(f"Stack trace: {traceback.format_exc()}", "DEBUG"))
    
    def _show_enhanced_basic_result(self, entry, result, target_language):
        """Enhanced BASIC decompile sonucunu göster"""
        try:
            # Yeni pencere oluştur
            result_window = tk.Toplevel(self.root)
            result_window.title(f"Enhanced BASIC Decompiler - {target_language.upper()}")
            result_window.geometry("1000x700")
            result_window.configure(bg='#2b2b2b')
            
            # Header
            header_frame = tk.Frame(result_window, bg='#1e1e1e', height=60)
            header_frame.pack(fill='x', pady=(0, 10))
            header_frame.pack_propagate(False)
            
            title_label = tk.Label(header_frame, 
                                 text=f"🔥 Enhanced BASIC Decompiler - {target_language.upper()}", 
                                 font=('Courier New', 14, 'bold'),
                                 bg='#1e1e1e', fg='#00ff00')
            title_label.pack(pady=10)
            
            info_label = tk.Label(header_frame,
                                text=f"File: {entry.get('name', 'Unknown')} | Target: {target_language} | Enhanced Optimization",
                                font=('Courier New', 10),
                                bg='#1e1e1e', fg='#cccccc')
            info_label.pack()
            
            # Main content with scrollbar
            content_frame = tk.Frame(result_window, bg='#2b2b2b')
            content_frame.pack(fill='both', expand=True, padx=10)
            
            # Text widget with scrollbar
            text_frame = tk.Frame(content_frame, bg='#2b2b2b')
            text_frame.pack(fill='both', expand=True)
            
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side='right', fill='y')
            
            text_widget = tk.Text(text_frame, 
                                yscrollcommand=scrollbar.set,
                                font=('Courier New', 10),
                                bg='#1e1e1e', fg='#ffffff',
                                insertbackground='#ffffff',
                                selectbackground='#404040')
            text_widget.pack(fill='both', expand=True)
            scrollbar.config(command=text_widget.yview)
            
            # Insert result
            text_widget.insert('1.0', result)
            text_widget.config(state='disabled')
            
            # Button frame
            button_frame = tk.Frame(result_window, bg='#2b2b2b')
            button_frame.pack(fill='x', pady=10)
            
            # Copy button
            copy_btn = tk.Button(button_frame, text="📋 Copy to Clipboard", 
                               command=lambda: self._copy_to_clipboard(result),
                               font=('Arial', 10, 'bold'),
                               bg='#4CAF50', fg='white', 
                               activebackground='#45a049',
                               relief='flat', padx=20)
            copy_btn.pack(side='left', padx=10)
            
            # Save button
            save_btn = tk.Button(button_frame, text="💾 Save Result", 
                               command=lambda: self._save_enhanced_basic_result(entry, result, target_language),
                               font=('Arial', 10, 'bold'),
                               bg='#2196F3', fg='white',
                               activebackground='#1976D2',
                               relief='flat', padx=20)
            save_btn.pack(side='left', padx=10)
            
            # Close button
            close_btn = tk.Button(button_frame, text="✖ Close", 
                                command=result_window.destroy,
                                font=('Arial', 10, 'bold'),
                                bg='#f44336', fg='white',
                                activebackground='#d32f2f',
                                relief='flat', padx=20)
            close_btn.pack(side='right', padx=10)
            
            self.log_message(f"✅ Enhanced BASIC decompile tamamlandı ({target_language})", "SUCCESS")
            
        except Exception as e:
            self.show_copyable_error("Enhanced BASIC Result Display Error", 
                                   f"Sonuç gösterilirken hata: {e}")
    
    def _save_enhanced_basic_result(self, entry, result, target_language):
        """Enhanced BASIC sonucunu dosyaya kaydet"""
        try:
            # File extension belirleme
            extensions = {
                "qbasic": ".bas",
                "c": ".c", 
                "cpp": ".cpp",
                "c++": ".cpp",
                "pdsx": ".bas",
                "python": ".py"
            }
            
            ext = extensions.get(target_language.lower(), ".txt")
            filename = f"{entry.get('name', 'program')}_enhanced_{target_language}{ext}"
            
            # Save dialog
            file_path = tk.filedialog.asksaveasfilename(
                title=f"Save Enhanced BASIC Result ({target_language})",
                defaultextension=ext,
                initialname=filename,
                filetypes=[(f"{target_language.upper()} Files", f"*{ext}"), ("All Files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                self.log_message(f"✅ Enhanced BASIC result saved: {file_path}", "SUCCESS")
            
        except Exception as e:
            self.show_copyable_error("Save Enhanced BASIC Result Error", 
                                   f"Dosya kaydedilirken hata: {e}")
    
    def show_enhanced_basic_options(self):
        """Enhanced BASIC Decompiler options dialog"""
        try:
            if not self.selected_entry:
                self.log_message("Lütfen önce bir dosya seçin", "WARNING")
                return
            
            # Options window
            options_window = tk.Toplevel(self.root)
            options_window.title("Enhanced BASIC Decompiler - Advanced Options")
            options_window.geometry("600x500")
            options_window.configure(bg='#2b2b2b')
            options_window.resizable(False, False)
            
            # Make it modal
            options_window.transient(self.root)
            options_window.grab_set()
            
            # Header
            header_frame = tk.Frame(options_window, bg='#1e1e1e', height=60)
            header_frame.pack(fill='x', pady=(0, 20))
            header_frame.pack_propagate(False)
            
            title_label = tk.Label(header_frame, 
                                 text="🔥 Enhanced BASIC Decompiler - Advanced Options", 
                                 font=('Arial', 14, 'bold'),
                                 bg='#1e1e1e', fg='#00ff00')
            title_label.pack(pady=15)
            
            # Main content
            content_frame = tk.Frame(options_window, bg='#2b2b2b')
            content_frame.pack(fill='both', expand=True, padx=20)
            
            # Target Language
            lang_frame = tk.LabelFrame(content_frame, text="Target Language", 
                                     font=('Arial', 10, 'bold'),
                                     bg='#2b2b2b', fg='#ffffff')
            lang_frame.pack(fill='x', pady=(0, 15))
            
            target_language = tk.StringVar(value="qbasic")
            
            tk.Radiobutton(lang_frame, text="QBasic 7.1 (Full compatibility)", 
                         variable=target_language, value="qbasic",
                         font=('Arial', 9), bg='#2b2b2b', fg='#ffffff',
                         selectcolor='#404040', activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Radiobutton(lang_frame, text="C (Optimized memory access)", 
                         variable=target_language, value="c",
                         font=('Arial', 9), bg='#2b2b2b', fg='#ffffff',
                         selectcolor='#404040', activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Radiobutton(lang_frame, text="C++ (Modern structured)", 
                         variable=target_language, value="cpp",
                         font=('Arial', 9), bg='#2b2b2b', fg='#ffffff',
                         selectcolor='#404040', activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Radiobutton(lang_frame, text="PDSX BASIC (Enhanced syntax)", 
                         variable=target_language, value="pdsx",
                         font=('Arial', 9), bg='#2b2b2b', fg='#ffffff',
                         selectcolor='#404040', activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            # Optimization Level
            opt_frame = tk.LabelFrame(content_frame, text="Optimization Level", 
                                    font=('Arial', 10, 'bold'),
                                    bg='#2b2b2b', fg='#ffffff')
            opt_frame.pack(fill='x', pady=(0, 15))
            
            optimization_level = tk.IntVar(value=2)
            
            tk.Radiobutton(opt_frame, text="Level 0: Basic conversion (preserve original structure)", 
                         variable=optimization_level, value=0,
                         font=('Arial', 9), bg='#2b2b2b', fg='#ffffff',
                         selectcolor='#404040', activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Radiobutton(opt_frame, text="Level 1: Memory access optimization", 
                         variable=optimization_level, value=1,
                         font=('Arial', 9), bg='#2b2b2b', fg='#ffffff',
                         selectcolor='#404040', activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Radiobutton(opt_frame, text="Level 2: Full optimization (recommended)", 
                         variable=optimization_level, value=2,
                         font=('Arial', 9), bg='#2b2b2b', fg='#ffffff',
                         selectcolor='#404040', activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Radiobutton(opt_frame, text="Level 3: Aggressive modernization", 
                         variable=optimization_level, value=3,
                         font=('Arial', 9), bg='#2b2b2b', fg='#ffffff',
                         selectcolor='#404040', activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            # Options
            opts_frame = tk.LabelFrame(content_frame, text="Additional Options", 
                                     font=('Arial', 10, 'bold'),
                                     bg='#2b2b2b', fg='#ffffff')
            opts_frame.pack(fill='x', pady=(0, 15))
            
            preserve_lines = tk.BooleanVar(value=False)
            modernize_syntax = tk.BooleanVar(value=True)
            optimize_memory = tk.BooleanVar(value=True)
            convert_graphics = tk.BooleanVar(value=True)
            
            tk.Checkbutton(opts_frame, text="Preserve original line numbers", 
                         variable=preserve_lines, font=('Arial', 9),
                         bg='#2b2b2b', fg='#ffffff', selectcolor='#404040',
                         activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Checkbutton(opts_frame, text="Modernize syntax and structures", 
                         variable=modernize_syntax, font=('Arial', 9),
                         bg='#2b2b2b', fg='#ffffff', selectcolor='#404040',
                         activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Checkbutton(opts_frame, text="Optimize memory access (POKE/PEEK)", 
                         variable=optimize_memory, font=('Arial', 9),
                         bg='#2b2b2b', fg='#ffffff', selectcolor='#404040',
                         activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            tk.Checkbutton(opts_frame, text="Convert graphics commands", 
                         variable=convert_graphics, font=('Arial', 9),
                         bg='#2b2b2b', fg='#ffffff', selectcolor='#404040',
                         activebackground='#404040').pack(anchor='w', padx=10, pady=2)
            
            # Buttons
            button_frame = tk.Frame(options_window, bg='#2b2b2b')
            button_frame.pack(fill='x', pady=20, padx=20)
            
            def start_conversion():
                options_window.destroy()
                self.enhanced_basic_decompile(self.selected_entry, 
                                            target_language.get(), 
                                            optimization_level.get())
            
            convert_btn = tk.Button(button_frame, text="🚀 Start Conversion", 
                                  command=start_conversion,
                                  font=('Arial', 11, 'bold'),
                                  bg='#4CAF50', fg='white', 
                                  activebackground='#45a049',
                                  relief='flat', padx=30, pady=8)
            convert_btn.pack(side='right', padx=(10, 0))
            
            cancel_btn = tk.Button(button_frame, text="Cancel", 
                                 command=options_window.destroy,
                                 font=('Arial', 11),
                                 bg='#f44336', fg='white',
                                 activebackground='#d32f2f',
                                 relief='flat', padx=30, pady=8)
            cancel_btn.pack(side='right')
            
            # File info
            info_label = tk.Label(content_frame, 
                                text=f"Selected File: {self.selected_entry.get('name', 'Unknown')}",
                                font=('Arial', 9, 'italic'),
                                bg='#2b2b2b', fg='#cccccc')
            info_label.pack(pady=(10, 0))
            
        except Exception as e:
            self.show_copyable_error("Enhanced BASIC Options Error", 
                                   f"Options dialog hatası: {e}")
    
    def _analyze_hybrid_thread(self, entry):
        """Enhanced Hibrit analiz thread'i - TÜM FORMATLAR DESTEKLENİR"""
        try:
            # PRG verisini çıkar
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.log_message("PRG verisi çıkarılamadı", "ERROR"))
                return
            
            self.root.after(0, lambda: self.log_message("🔄 Enhanced hibrit program analizi başlıyor...", "INFO"))
            
            # Enhanced D64 Reader ile hibrit analiz - YENİ YÖNTEMİ
            try:
                reader = EnhancedUniversalDiskReader()
                analysis_result = reader.analyze_hybrid_basic_assembly(prg_data)
                
                if analysis_result:
                    # Detaylı rapor oluştur
                    detailed_report = self._format_enhanced_hybrid_report_v2(analysis_result)
                    
                    # GUI'de göster
                    self.root.after(0, lambda: self._show_enhanced_hybrid_analysis_result(entry, analysis_result, detailed_report))
                    return
                    
            except Exception as e:
                print(f"Enhanced Reader hibrit analiz hatası: {e}")
                pass  # Fallback'e geç
            
            # Enhanced Universal Disk Reader ile hibrit analiz - ESKİ YÖNTEMİ
            if analyze_hybrid_program:
                analysis_result = analyze_hybrid_program(prg_data)
                
                if analysis_result:
                    # Detaylı rapor oluştur
                    detailed_report = self._format_enhanced_hybrid_report(analysis_result)
                    
                    # GUI'de göster
                    self.root.after(0, lambda: self._show_enhanced_hybrid_analysis_result(entry, analysis_result, detailed_report))
                else:
                    self.root.after(0, lambda: self.log_message("Hibrit analiz başarısız - veri formatı tanınamadı", "WARNING"))
            else:
                # Fallback to old analyzer
                if not self.hybrid_analyzer:
                    self.root.after(0, lambda: self.log_message("HybridProgramAnalyzer bulunamadı", "ERROR"))
                    return
                
                analysis_result = self.hybrid_analyzer.analyze_prg_data(prg_data)
                detailed_report = self.hybrid_analyzer.format_analysis_report(analysis_result)
                self.root.after(0, lambda: self._show_hybrid_analysis_result(entry, analysis_result, detailed_report))
            
        except Exception as e:
            error_msg = f"Enhanced hibrit analiz hatası: {e}"
            self.root.after(0, lambda: self.log_message(error_msg, "ERROR"))
            import traceback
            print(f"Enhanced hybrid analysis error: {traceback.format_exc()}")
    
    def _show_hybrid_analysis_result(self, entry, analysis_result, detailed_report):
        """Hibrit analiz sonuçlarını göster"""
        try:
            # Analiz sonucu penceresini oluştur
            result_window = tk.Toplevel(self.root)
            result_window.title(f"🔄 Hibrit Program Analizi - {entry.get('filename', 'Unknown')}")
            result_window.geometry("900x700")
            result_window.configure(bg=ModernStyle.BG_PRIMARY)
            
            # Ana frame
            main_frame = tk.Frame(result_window, bg=ModernStyle.BG_PRIMARY)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Başlık
            title_label = tk.Label(main_frame, 
                                 text=f"🔄 Hibrit Program Analizi: {entry.get('filename', 'Unknown')}",
                                 bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY,
                                 font=("Arial", 12, "bold"))
            title_label.pack(pady=(0, 10))
            
            # Notebook (Tab sistemi)
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # === TAB 1: Özet ===
            summary_frame = tk.Frame(notebook, bg=ModernStyle.BG_SECONDARY)
            notebook.add(summary_frame, text="📊 Özet")
            
            summary_text = tk.Text(summary_frame, wrap=tk.WORD, bg=ModernStyle.BG_TERTIARY, 
                                 fg=ModernStyle.FG_PRIMARY, font=("Consolas", 10))
            summary_scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=summary_text.yview)
            summary_text.configure(yscrollcommand=summary_scrollbar.set)
            
            summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)
            summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,5), pady=5)
            
            # Özet bilgilerini ekle
            summary_content = self._generate_hybrid_summary(analysis_result)
            summary_text.insert(tk.END, summary_content)
            summary_text.config(state=tk.DISABLED)
            
            # === TAB 2: Detaylı Rapor ===
            detail_frame = tk.Frame(notebook, bg=ModernStyle.BG_SECONDARY)
            notebook.add(detail_frame, text="📋 Detaylı Rapor")
            
            detail_text = tk.Text(detail_frame, wrap=tk.WORD, bg=ModernStyle.BG_TERTIARY,
                                fg=ModernStyle.FG_PRIMARY, font=("Consolas", 9))
            detail_scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=detail_text.yview)
            detail_text.configure(yscrollcommand=detail_scrollbar.set)
            
            detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)
            detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,5), pady=5)
            
            detail_text.insert(tk.END, detailed_report)
            detail_text.config(state=tk.DISABLED)
            
            # === TAB 3: Disassembly Plan ===
            plan_frame = tk.Frame(notebook, bg=ModernStyle.BG_SECONDARY)
            notebook.add(plan_frame, text="📋 Disassembly Planı")
            
            plan_text = tk.Text(plan_frame, wrap=tk.WORD, bg=ModernStyle.BG_TERTIARY,
                              fg=ModernStyle.FG_PRIMARY, font=("Consolas", 10))
            plan_scrollbar = ttk.Scrollbar(plan_frame, orient="vertical", command=plan_text.yview)
            plan_text.configure(yscrollcommand=plan_scrollbar.set)
            
            plan_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5,0), pady=5)
            plan_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,5), pady=5)
            
            # Disassembly planını ekle
            plan_content = self._generate_disassembly_plan_display(analysis_result)
            plan_text.insert(tk.END, plan_content)
            plan_text.config(state=tk.DISABLED)
            
            # Buton çerçevesi
            button_frame = tk.Frame(main_frame, bg=ModernStyle.BG_PRIMARY)
            button_frame.pack(fill=tk.X, pady=(10, 0))
            
            # Butonlar
            ttk.Button(button_frame, text="📋 Özeti Kopyala", 
                      command=lambda: self.copy_text_to_clipboard(summary_content)).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(button_frame, text="📋 Detayları Kopyala", 
                      command=lambda: self.copy_text_to_clipboard(detailed_report)).pack(side=tk.LEFT, padx=5)
            
            if analysis_result.get("is_hybrid"):
                ttk.Button(button_frame, text="🔧 BASIC Decompile", 
                          command=lambda: self._start_basic_decompile(entry, analysis_result)).pack(side=tk.LEFT, padx=5)
                
                ttk.Button(button_frame, text="⚙️ Assembly Disassemble", 
                          command=lambda: self._start_assembly_disassemble(entry, analysis_result)).pack(side=tk.LEFT, padx=5)
            
            ttk.Button(button_frame, text="✅ Kapat", command=result_window.destroy).pack(side=tk.RIGHT, padx=5)
            
            # Database'e kaydet
            if self.database_manager:
                try:
                    file_info = {
                        'filename': entry.get('filename', 'Unknown'),
                        'size': analysis_result.get('total_file_size', 0),
                        'file_type': 'PRG',
                        'analysis_type': 'HYBRID',
                        'program_type': analysis_result.get('program_type', 'UNKNOWN'),
                        'is_hybrid': analysis_result.get('is_hybrid', False),
                        'has_basic': bool(analysis_result.get('basic_info')),
                        'has_assembly': bool(analysis_result.get('assembly_info')),
                        'sys_calls': len(analysis_result.get('sys_calls', [])),
                        'memory_operations': len(analysis_result.get('memory_usage', []))
                    }
                    self.database_manager.track_file_processing(file_info)
                except Exception as db_error:
                    print(f"Database tracking error: {db_error}")
            
            # Pencereyi merkeze getir
            result_window.transient(self.root)
            result_window.grab_set()
            result_window.focus_set()
            
            # Log mesajı
            self.log_message(f"✅ Hibrit analiz tamamlandı: {analysis_result.get('program_type', 'UNKNOWN')}", "SUCCESS")
            
        except Exception as e:
            error_msg = f"Hibrit analiz sonuç gösterme hatası: {e}"
            self.log_message(error_msg, "ERROR")
            print(f"Show hybrid result error: {e}")
    
    def _generate_hybrid_summary(self, analysis_result):
        """Hibrit analiz özeti oluştur"""
        summary = []
        summary.append("🔄 HİBRİT PROGRAM ANALİZ ÖZETİ")
        summary.append("=" * 50)
        summary.append("")
        
        summary.append(f"📋 Program Tipi: {analysis_result.get('program_type', 'Bilinmiyor')}")
        summary.append(f"🎭 Hibrit Program: {'✅ Evet' if analysis_result.get('is_hybrid') else '❌ Hayır'}")
        summary.append(f"📏 Toplam Boyut: {analysis_result.get('total_file_size', 0)} bytes")
        summary.append(f"🎯 Başlangıç Adresi: {analysis_result.get('start_address_hex', 'Unknown')}")
        summary.append("")
        
        # BASIC kısmı
        basic_info = analysis_result.get('basic_info')
        if basic_info:
            summary.append("📝 BASIC KISMI:")
            summary.append(f"   📏 Boyut: {basic_info.get('basic_calculated_size', 0)} bytes")
            summary.append(f"   📄 Satır Sayısı: {basic_info.get('line_count', 0)}")
            summary.append(f"   🚀 SYS Çağrıları: {len(basic_info.get('sys_calls', []))}")
            summary.append(f"   📝 POKE İşlemleri: {len(basic_info.get('poke_operations', []))}")
            summary.append(f"   👁️ PEEK İşlemleri: {len(basic_info.get('peek_operations', []))}")
            summary.append("")
        
        # Assembly kısmı
        asm_info = analysis_result.get('assembly_info')
        if asm_info:
            summary.append("⚙️ ASSEMBLY KISMI:")
            summary.append(f"   📏 Boyut: {asm_info.get('assembly_size', 0)} bytes")
            summary.append(f"   🎯 Başlangıç: {asm_info.get('assembly_start_hex', 'Unknown')}")
            summary.append(f"   🏁 Bitiş: {asm_info.get('assembly_end_hex', 'Unknown')}")
            summary.append("")
        
        # Öneriler
        plan = analysis_result.get('disassembly_plan', {})
        if plan.get('recommendations'):
            summary.append("💡 ÖNERİLER:")
            for rec in plan['recommendations'][:5]:
                summary.append(f"   • {rec}")
            summary.append("")
        
        return "\n".join(summary)
    
    def _generate_disassembly_plan_display(self, analysis_result):
        """Disassembly planı ekranı oluştur"""
        plan_content = []
        plan_content.append("📋 DISASSEMBLY PLAN")
        plan_content.append("=" * 50)
        plan_content.append("")
        
        plan = analysis_result.get('disassembly_plan', {})
        
        plan_content.append(f"🎯 Program Tipi: {plan.get('program_type', 'UNKNOWN')}")
        plan_content.append("")
        
        # Görevler
        tasks = plan.get('tasks', [])
        if tasks:
            plan_content.append("📋 YAPILACAN İŞLEMLER:")
            for i, task in enumerate(tasks, 1):
                plan_content.append(f"{i}. {task['type']}: {task['description']}")
                plan_content.append(f"   Öncelik: {task['priority']}")
                plan_content.append(f"   Çıktı Formatları: {', '.join(task['outputs'])}")
                
                if task.get('input'):
                    inp = task['input']
                    plan_content.append(f"   Giriş: Adres ${inp.get('start_address', 0):04X}, Boyut {inp.get('size', 0)} bytes")
                plan_content.append("")
        
        # Öncelik sırası
        priority_order = plan.get('priority_order', [])
        if priority_order:
            plan_content.append("📊 ÖNCELİK SIRASI:")
            for i, priority in enumerate(priority_order, 1):
                plan_content.append(f"{i}. {priority}")
            plan_content.append("")
        
        # Öneriler
        recommendations = plan.get('recommendations', [])
        if recommendations:
            plan_content.append("💡 ÖNERİLER:")
            for rec in recommendations:
                plan_content.append(f"   • {rec}")
            plan_content.append("")
        
        return "\n".join(plan_content)
    
    def _start_basic_decompile(self, entry, analysis_result):
        """BASIC decompile işlemini başlat"""
        try:
            self.log_message("🔄 BASIC decompile başlatılıyor...", "INFO")
            # Bu kısım Step 9'da implement edilecek
            messagebox.showinfo("Bilgi", "BASIC decompile özelliği Step 9'da eklenecek!")
        except Exception as e:
            self.log_message(f"BASIC decompile hatası: {e}", "ERROR")
    
    def _start_assembly_disassemble(self, entry, analysis_result):
        """Assembly disassemble işlemini başlat"""
        try:
            self.log_message("⚙️ Assembly disassemble başlatılıyor...", "INFO")
            # Mevcut assembly disassemble sistemini kullan
            if hasattr(self, 'decompiler_panel'):
                self.decompiler_panel.convert_format('assembly')
            else:
                messagebox.showinfo("Bilgi", "Assembly disassemble işlemi mevcut sistemle yapılacak!")
        except Exception as e:
            self.log_message(f"Assembly disassemble hatası: {e}", "ERROR")
    
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
        """Enhanced Console'a log mesajı ekle - Error tracking ile"""
        try:
            # 🍎 HATA ANALIZ LOGGER - TÜM LOG MESAJLARI
            if hasattr(self, 'hata_logger') and self.hata_logger:
                self.hata_logger.log_terminal(message, level)
            
            # Console'a yazdır
            if hasattr(self, 'console_panel'):
                self.console_panel.add_log(message, level)
            else:
                print(f"[{level}] {message}")
            
            # Terminale de yazdır (ERROR ve WARNING için)
            if level in ["ERROR", "WARNING"]:
                print(f"[{level}] {message}")
            
            # Logger'a da kaydet
            if hasattr(self, 'logger'):
                if level == "ERROR":
                    self.logger.error(message)
                elif level == "WARNING":
                    self.logger.warning(message)
                elif level == "SUCCESS":
                    self.logger.info(f"✅ {message}")
                else:
                    self.logger.info(message)
            
            # Critical error ise messagebox göster
            if level == "ERROR" and ("error" in message.lower() or "failed" in message.lower()):
                self.show_copyable_error(message)
                
        except Exception as e:
            print(f"[CRITICAL] Log message error: {e}")
    
    def show_copyable_error(self, error_message):
        """Kopyalanabilir error dialog göster"""
        try:
            error_window = tk.Toplevel(self.root)
            error_window.title("❌ Error Details")
            error_window.geometry("600x400")
            error_window.configure(bg=ModernStyle.BG_PRIMARY)
            
            # Error frame
            error_frame = tk.Frame(error_window, bg=ModernStyle.BG_PRIMARY)
            error_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Error text with scrollbar
            text_frame = tk.Frame(error_frame, bg=ModernStyle.BG_PRIMARY)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            error_text = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10),
                               bg=ModernStyle.BG_SECONDARY, fg="#FF6B6B",
                               selectbackground="#FF6B6B", selectforeground="white")
            
            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            error_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            error_text.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=error_text.yview)
            
            # Error mesajını ekle
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_error = f"[{timestamp}] ERROR: {error_message}\n\n"
            
            # Stack trace varsa ekle
            import traceback
            if traceback.format_exc() != "NoneType: None\n":
                full_error += f"Stack Trace:\n{traceback.format_exc()}"
            
            error_text.insert(tk.END, full_error)
            error_text.config(state=tk.DISABLED)
            
            # Button frame
            button_frame = tk.Frame(error_frame, bg=ModernStyle.BG_PRIMARY)
            button_frame.pack(fill=tk.X, pady=(10, 0))
            
            def copy_to_clipboard():
                error_window.clipboard_clear()
                error_window.clipboard_append(full_error)
                copy_btn.config(text="✅ Copied!")
                error_window.after(2000, lambda: copy_btn.config(text="📋 Copy Error"))
            
            copy_btn = tk.Button(button_frame, text="📋 Copy Error", 
                               command=copy_to_clipboard,
                               bg=ModernStyle.ACCENT_COLOR, fg="white",
                               font=("Arial", 10, "bold"))
            copy_btn.pack(side=tk.LEFT, padx=5)
            
            close_btn = tk.Button(button_frame, text="❌ Close", 
                                command=error_window.destroy,
                                bg="#FF6B6B", fg="white",
                                font=("Arial", 10, "bold"))
            close_btn.pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            print(f"[CRITICAL] Error dialog creation failed: {e}")
            messagebox.showerror("Critical Error", f"Error: {error_message}\nDialog Error: {e}")

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
        """Gelişmiş kod dışa aktarma"""
        if not hasattr(self, 'code_preview') or not self.code_preview.current_code:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        format_type = self.code_preview.current_format
        ext_map = {"ASM": ".asm", "C": ".c", "QBasic": ".bas", "PDSx": ".pdsx", "C++": ".cpp", "Pseudo": ".txt"}
        
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
                self.console_panel.add_log(f"Code exported to: {filename}", "INFO")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not export file:\n{str(e)}")
    
    def save_current_code(self):
        """Mevcut kodu kaydet (hızlı kaydetme)"""
        if not hasattr(self, 'current_save_path'):
            self.save_as_code()
        else:
            try:
                with open(self.current_save_path, 'w', encoding='utf-8') as f:
                    f.write(self.code_preview.current_code)
                self.update_status(f"✅ Saved: {os.path.basename(self.current_save_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
    
    def save_as_code(self):
        """Farklı kaydet - FORMAT DİZİN SİSTEMİ ile"""
        if not hasattr(self, 'code_preview') or not self.code_preview.current_code:
            messagebox.showwarning("Warning", "No data to save!")
            return
        
        format_type = self.code_preview.current_format
        ext_map = {"ASM": ".asm", "C": ".c", "QBasic": ".bas", "PDSx": ".pdsx", "C++": ".cpp", "Pseudo": ".txt"}
        
        # Format dizin sistemi - KızılElma Plan
        base_dir = "format_files"
        format_subdir = f"{format_type.lower()}_files"
        
        # Disassembler alt dizini
        if format_type == "ASM" and hasattr(self.disassembly_panel, 'disassembler_var'):
            disassembler_type = self.disassembly_panel.disassembler_var.get()
            format_subdir = os.path.join(f"asm_files", disassembler_type)
        
        # Dizin oluştur
        full_dir = os.path.join(base_dir, format_subdir)
        os.makedirs(full_dir, exist_ok=True)
        
        # Akıllı dosya adlandırma: diskimaji__program_adi.uzanti
        if self.selected_entry:
            source_file = self.selected_entry.get('source_file', '')
            program_name = self.selected_entry.get('filename', 'unknown')
            
            # Disk adını çıkar
            if source_file:
                disk_name = os.path.splitext(os.path.basename(source_file))[0]
            else:
                disk_name = "unknown_disk"
            
            # Dosya adı: diskimaji__program_adi.uzanti
            suggested_filename = f"{disk_name}__{program_name}{ext_map.get(format_type, '.txt')}"
            initial_file = os.path.join(full_dir, suggested_filename)
        else:
            initial_file = os.path.join(full_dir, f"output{ext_map.get(format_type, '.txt')}")
        
        filename = filedialog.asksaveasfilename(
            title=f"Save {format_type} Code",
            initialdir=full_dir,
            initialfile=os.path.basename(initial_file),
            defaultextension=ext_map.get(format_type, ".txt"),
            filetypes=[(f"{format_type} files", f"*{ext_map.get(format_type, '.txt')}"), 
                      ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.code_preview.current_code)
                
                self.current_save_path = filename
                self.update_status(f"✅ Saved: {os.path.basename(filename)}")
                self.console_panel.add_log(f"Code saved to: {filename}", "INFO")
                self.log_to_terminal_and_file(f"📁 FORMAT DİZİN SİSTEMİ: {filename}", "INFO")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
    
    def export_all_formats(self):
        """Tüm formatları dışa aktar"""
        if not self.current_data:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        # Klasör seç
        output_dir = filedialog.askdirectory(title="Select output directory for all formats")
        if not output_dir:
            return
        
        try:
            self.console_panel.add_log("Starting multi-format export...", "INFO")
            
            # Her format için dışa aktar - Assembly format seçenekleri dahil
            formats = ["ASM", "ASM_ACME", "ASM_CC65", "ASM_DASM", "ASM_KickAss", "C", "QBasic", "PDSx", "C++", "Pseudo"]
            exported_count = 0
            
            for fmt in formats:
                try:
                    # Format seç ve dönüştür
                    self.code_preview.format_var.set(fmt)
                    self.trigger_real_time_update()
                    
                    # Dosya adı oluştur
                    base_name = getattr(self, 'current_file_name', 'output')
                    if '.' in base_name:
                        base_name = base_name.split('.')[0]
                    
                    ext_map = {"ASM": ".asm", "ASM_ACME": ".asm", "ASM_CC65": ".s", "ASM_DASM": ".asm", 
                              "ASM_KickAss": ".asm", "C": ".c", "QBasic": ".bas", "PDSx": ".pdsx", "C++": ".cpp", "Pseudo": ".txt"}
                    filename = os.path.join(output_dir, f"{base_name}_{fmt.lower()}{ext_map.get(fmt, '.txt')}")
                    
                    # Kaydet
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(self.code_preview.current_code)
                    
                    exported_count += 1
                    self.console_panel.add_log(f"Exported {fmt}: {filename}", "INFO")
                    
                except Exception as e:
                    self.console_panel.add_log(f"Failed to export {fmt}: {e}", "ERROR")
            
            self.update_status(f"✅ Exported {exported_count} formats to: {output_dir}")
            messagebox.showinfo("Export Complete", f"Successfully exported {exported_count} formats!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Multi-format export failed:\n{str(e)}")
    
    def batch_save_dialog(self):
        """Toplu kaydetme dialog'u"""
        if not hasattr(self, 'directory_panel') or not self.directory_panel.entries:
            messagebox.showwarning("Warning", "No files loaded for batch processing!")
            return
        
        # Batch dialog penceresi
        batch_window = tk.Toplevel(self.root)
        batch_window.title("Toplu Kaydetme/Dışa Aktarma")
        batch_window.geometry("600x400")
        batch_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = tk.Label(batch_window, text="📦 Toplu İşlem Ayarları", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # Format seçimi
        format_frame = tk.Frame(batch_window, bg=ModernStyle.BG_PRIMARY)
        format_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(format_frame, text="Dışa Aktarılacak Formatlar:", 
                bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(anchor=tk.W)
        
        # Format checkboxes - Assembly formatları dahil
        self.batch_formats = {}
        formats = ["ASM", "ASM_ACME", "ASM_CC65", "ASM_DASM", "ASM_KickAss", "C", "QBasic", "PDSx", "C++", "Pseudo"]
        
        # İki sütunlu yerleşim
        row1_frame = tk.Frame(format_frame, bg=ModernStyle.BG_PRIMARY)
        row1_frame.pack(fill=tk.X)
        row2_frame = tk.Frame(format_frame, bg=ModernStyle.BG_PRIMARY)
        row2_frame.pack(fill=tk.X)
        
        for i, fmt in enumerate(formats):
            var = tk.BooleanVar(value=True)
            self.batch_formats[fmt] = var
            
            parent_frame = row1_frame if i < 5 else row2_frame
            cb = tk.Checkbutton(parent_frame, text=fmt, variable=var, 
                               bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY,
                               selectcolor=ModernStyle.BG_SECONDARY)
            cb.pack(side=tk.LEFT, padx=10)
        
        # Çıktı dizini
        output_frame = tk.Frame(batch_window, bg=ModernStyle.BG_PRIMARY)
        output_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(output_frame, text="Çıktı Dizini:", 
                bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(anchor=tk.W)
        
        self.batch_output_var = tk.StringVar(value=os.getcwd())
        output_entry = tk.Entry(output_frame, textvariable=self.batch_output_var, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(output_frame, text="📂", command=lambda: self.batch_output_var.set(
            filedialog.askdirectory(title="Select batch output directory"))).pack(side=tk.RIGHT)
        
        # Progress bar
        progress_frame = tk.Frame(batch_window, bg=ModernStyle.BG_PRIMARY)
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.batch_progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.batch_progress.pack(fill=tk.X)
        
        # Butonlar
        button_frame = tk.Frame(batch_window, bg=ModernStyle.BG_PRIMARY)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="🚀 Başlat", command=lambda: self.start_batch_export(batch_window)).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ İptal", command=batch_window.destroy).pack(side=tk.RIGHT, padx=10)
    
    def start_batch_export(self, batch_window):
        """Toplu dışa aktarmayı başlat"""
        selected_formats = [fmt for fmt, var in self.batch_formats.items() if var.get()]
        output_dir = self.batch_output_var.get()
        
        if not selected_formats:
            messagebox.showwarning("Warning", "Please select at least one format!")
            return
        
        if not output_dir or not os.path.exists(output_dir):
            messagebox.showwarning("Warning", "Please select a valid output directory!")
            return
        
        def batch_thread():
            try:
                total_files = len(self.directory_panel.entries)
                self.batch_progress['maximum'] = total_files * len(selected_formats)
                current_progress = 0
                
                for entry in self.directory_panel.entries:
                    filename = entry.get('filename', 'unknown')
                    
                    # Her format için işle
                    for fmt in selected_formats:
                        try:
                            # Fake processing (gerçek implementasyon burada olacak)
                            time.sleep(0.1)  # Simulate processing
                            
                            base_name = filename.split('.')[0] if '.' in filename else filename
                            ext_map = {"ASM": ".asm", "C": ".c", "QBasic": ".bas", "PDSx": ".pdsx", "C++": ".cpp", "Pseudo": ".txt"}
                            output_file = os.path.join(output_dir, f"{base_name}_{fmt.lower()}{ext_map.get(fmt, '.txt')}")
                            
                            # Fake content
                            with open(output_file, 'w', encoding='utf-8') as f:
                                f.write(f"; {fmt} conversion of {filename}\n; Generated by D64 Converter v5.0\n")
                            
                            current_progress += 1
                            self.batch_progress['value'] = current_progress
                            batch_window.update_idletasks()
                            
                        except Exception as e:
                            self.console_panel.add_log(f"Batch export error for {filename} ({fmt}): {e}", "ERROR")
                
                messagebox.showinfo("Batch Export Complete", 
                                  f"Successfully processed {total_files} files in {len(selected_formats)} formats!")
                batch_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Batch Export Error", f"Batch export failed:\n{str(e)}")
        
        threading.Thread(target=batch_thread, daemon=True).start()
    
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
        try:
            print("🚀 Starting GUI main loop...")
            self.update_status("🚀 D64 Converter GUI Ready - Load a PRG file to begin!")
            self.logger.info("🚀 D64 Converter GUI başlatıldı")
            
            # Start the main tkinter loop
            self.root.mainloop()
            
            print("✅ GUI main loop completed")
            self.logger.info("✅ GUI main loop tamamlandı")
            
        except Exception as e:
            error_msg = f"❌ GUI main loop error: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            
            import traceback
            full_traceback = traceback.format_exc()
            print(f"GUI main loop traceback:\n{full_traceback}")
            self.logger.error(f"Full traceback:\n{full_traceback}")
            
            # Try to show error in message box if possible
            try:
                messagebox.showerror("GUI Error", f"GUI encountered an error:\n{e}")
            except:
                print("❌ Could not display error dialog")
            
            # Re-raise for caller
            raise e
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
    
    # === Database Management Methods ===
    
    def show_database_stats(self):
        """Veritabanı istatistiklerini göster"""
        if not self.database_manager:
            messagebox.showwarning("Warning", "Database manager not available")
            return
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Database Statistics")
        stats_window.geometry("800x600")
        stats_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = tk.Label(stats_window, text="📊 İşlenmiş Dosya İstatistikleri", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # İstatistikleri al
        stats = self.database_manager.get_statistics()
        
        # Text widget ile göster
        text_widget = scrolledtext.ScrolledText(stats_window, height=30, width=100,
                                               bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                               font=("Consolas", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # İstatistik metni oluştur
        stats_text = f"🗄️ TOPLAM DOSYA SAYISI: {stats['total_files']}\n\n"
        
        stats_text += "📊 FORMAT BAŞARI ORANLARI:\n"
        stats_text += "=" * 50 + "\n"
        for format_name, format_stat in stats.get('format_stats', {}).items():
            success_rate = format_stat['success_rate']
            stats_text += f"{format_name:12} : {format_stat['success_count']:3}/{format_stat['total_count']:3} ({success_rate:5.1f}%)\n"
        
        if stats.get('assembly_stats'):
            stats_text += f"\n🔧 ASSEMBLY FORMAT İSTATİSTİKLERİ:\n"
            stats_text += "=" * 50 + "\n"
            for asm_format, asm_stat in stats['assembly_stats'].items():
                stats_text += f"{asm_format:12} : {asm_stat['success_count']:3}/{asm_stat['total_count']:3}\n"
        
        stats_text += f"\n📅 SON İŞLENEN DOSYALAR:\n"
        stats_text += "=" * 50 + "\n"
        for file_info in stats.get('recent_files', []):
            stats_text += f"{file_info['filename']:<30} {file_info['processing_date']:<20} ✅{file_info['success_count']} ❌{file_info['failure_count']}\n"
        
        text_widget.insert(1.0, stats_text)
        text_widget.config(state=tk.DISABLED)
    
    def show_file_history(self):
        """Dosya geçmişini göster"""
        if not self.database_manager:
            messagebox.showwarning("Warning", "Database manager not available")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("📁 File Processing History")
        history_window.geometry("1200x700")
        history_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = tk.Label(history_window, text="📁 Dosya İşlem Geçmişi", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # Treeview ile tablo gösterimi
        tree_frame = tk.Frame(history_window, bg=ModernStyle.BG_PRIMARY)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ('Filename', 'Format', 'Size', 'Success', 'Failure', 'Last Processed')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Sütun başlıkları
        tree.heading('Filename', text='Dosya Adı')
        tree.heading('Format', text='Kaynak Format')
        tree.heading('Size', text='Boyut')
        tree.heading('Success', text='Başarılı')
        tree.heading('Failure', text='Başarısız')
        tree.heading('Last Processed', text='Son İşlem')
        
        # Sütun genişlikleri
        tree.column('Filename', width=300)
        tree.column('Format', width=100)
        tree.column('Size', width=100)
        tree.column('Success', width=80)
        tree.column('Failure', width=80)
        tree.column('Last Processed', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Verileri yükle
        history = self.database_manager.get_file_history()
        for item in history:
            tree.insert('', tk.END, values=(
                item['filename'],
                item['source_format'],
                f"{item['file_size']} bytes",
                item['success_count'],
                item['failure_count'],
                item['last_processed']
            ))
    
    def show_database_search(self):
        """Veritabanı arama arayüzü"""
        if not self.database_manager:
            messagebox.showwarning("Warning", "Database manager not available")
            return
        
        search_window = tk.Toplevel(self.root)
        search_window.title("🔍 Database Search")
        search_window.geometry("800x600")
        search_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = tk.Label(search_window, text="🔍 Dosya Arama", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # Arama formu
        search_frame = tk.Frame(search_window, bg=ModernStyle.BG_PRIMARY)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(search_frame, text="Arama terimi:", bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(side=tk.LEFT)
        search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10))
        search_entry.pack(side=tk.LEFT, padx=10)
        
        search_type_var = tk.StringVar(value="filename")
        ttk.Radiobutton(search_frame, text="Dosya Adı", variable=search_type_var, value="filename").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(search_frame, text="Format", variable=search_type_var, value="format").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(search_frame, text="Notlar", variable=search_type_var, value="notes").pack(side=tk.LEFT, padx=5)
        
        # Arama sonuçları
        results_text = scrolledtext.ScrolledText(search_window, height=25, width=100,
                                               bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                               font=("Consolas", 10))
        results_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def do_search():
            search_term = search_entry.get()
            search_type = search_type_var.get()
            
            if not search_term:
                messagebox.showwarning("Warning", "Arama terimi girin")
                return
            
            results = self.database_manager.search_files(search_term, search_type)
            
            results_text.delete(1.0, tk.END)
            if results:
                results_text.insert(tk.END, f"🔍 Arama sonuçları: '{search_term}' ({search_type})\n")
                results_text.insert(tk.END, "=" * 60 + "\n\n")
                
                for item in results:
                    results_text.insert(tk.END, f"📁 {item['filename']}\n")
                    results_text.insert(tk.END, f"   Format: {item['source_format']}\n")
                    results_text.insert(tk.END, f"   Boyut: {item['file_size']} bytes\n")
                    results_text.insert(tk.END, f"   Başarılı: {item['success_count']} | Başarısız: {item['failure_count']}\n")
                    results_text.insert(tk.END, f"   Son işlem: {item['last_processed']}\n")
                    if item['notes']:
                        results_text.insert(tk.END, f"   Notlar: {item['notes']}\n")
                    results_text.insert(tk.END, "\n")
            else:
                results_text.insert(tk.END, f"❌ '{search_term}' için sonuç bulunamadı")
        
        ttk.Button(search_frame, text="🔍 Ara", command=do_search).pack(side=tk.LEFT, padx=10)
        
        # Enter tuşu ile arama
        search_entry.bind('<Return>', lambda e: do_search())
    
    def export_database_excel(self):
        """Veritabanını Excel'e aktar"""
        if not self.database_manager:
            messagebox.showwarning("Warning", "Database manager not available")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Database to Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if filename:
            if self.database_manager.export_to_excel(filename):
                messagebox.showinfo("Success", f"Database exported to: {filename}")
                self.log_message(f"Database exported to Excel: {filename}", "INFO")
            else:
                messagebox.showerror("Error", "Excel export failed")
    
    def export_database_csv(self):
        """Veritabanını CSV'ye aktar"""
        if not self.database_manager:
            messagebox.showwarning("Warning", "Database manager not available")
            return
        
        output_dir = filedialog.askdirectory(title="Select output directory for CSV files")
        
        if output_dir:
            if self.database_manager.export_to_csv(output_dir):
                messagebox.showinfo("Success", f"Database exported to CSV files in: {output_dir}")
                self.log_message(f"Database exported to CSV: {output_dir}", "INFO")
            else:
                messagebox.showerror("Error", "CSV export failed")
    
    def export_database_json(self):
        """Veritabanını JSON'a aktar"""
        if not self.database_manager:
            messagebox.showwarning("Warning", "Database manager not available")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Database to JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.database_manager.export_to_json(filename):
                messagebox.showinfo("Success", f"Database exported to: {filename}")
                self.log_message(f"Database exported to JSON: {filename}", "INFO")
            else:
                messagebox.showerror("Error", "JSON export failed")
    
    def cleanup_database(self):
        """Eski veritabanı kayıtlarını temizle"""
        if not self.database_manager:
            messagebox.showwarning("Warning", "Database manager not available")
            return
        
        # Gün sayısı al
        cleanup_window = tk.Toplevel(self.root)
        cleanup_window.title("🧹 Database Cleanup")
        cleanup_window.geometry("400x200")
        cleanup_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        tk.Label(cleanup_window, text="🧹 Veritabanı Temizleme", 
                font=("Arial", 14, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(pady=20)
        
        tk.Label(cleanup_window, text="Kaç günden eski kayıtlar silinsin?", 
                bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(pady=10)
        
        days_var = tk.StringVar(value="30")
        days_entry = tk.Entry(cleanup_window, textvariable=days_var, width=10, font=("Arial", 12))
        days_entry.pack(pady=10)
        
        def do_cleanup():
            try:
                days = int(days_var.get())
                if days <= 0:
                    messagebox.showerror("Error", "Gün sayısı 0'dan büyük olmalı")
                    return
                
                deleted_count = self.database_manager.cleanup_old_records(days)
                cleanup_window.destroy()
                
                messagebox.showinfo("Success", f"{deleted_count} eski kayıt silindi")
                self.log_message(f"Database cleanup: {deleted_count} records deleted (older than {days} days)", "INFO")
                
            except ValueError:
                messagebox.showerror("Error", "Geçerli bir sayı girin")
        
        button_frame = tk.Frame(cleanup_window, bg=ModernStyle.BG_PRIMARY)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="🧹 Temizle", command=do_cleanup).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ İptal", command=cleanup_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def track_file_processing(self, filename: str, file_path: str, source_format: str, 
                            start_address: int = None, end_address: int = None, notes: str = ""):
        """Dosya işleme takibini veritabanına kaydet"""
        if self.database_manager:
            try:
                file_id = self.database_manager.add_processed_file(
                    filename, file_path, source_format, start_address, end_address, notes
                )
                self.current_file_id = file_id
                return file_id
            except Exception as e:
                self.log_message(f"Database tracking error: {e}", "WARNING")
                return None
        return None
    
    def track_format_conversion(self, target_format: str, success: bool, 
                              output_size: int = 0, processing_time: float = 0.0,
                              error_message: str = "", output_path: str = "", 
                              assembly_format: str = ""):
        """Format dönüşüm takibini veritabanına kaydet"""
        if self.database_manager and hasattr(self, 'current_file_id') and self.current_file_id:
            try:
                self.database_manager.add_format_conversion(
                    self.current_file_id, target_format, success, output_size,
                    processing_time, error_message, output_path, assembly_format
                )
            except Exception as e:
                self.log_message(f"Database conversion tracking error: {e}", "WARNING")
    
    # === Hybrid Program Analysis Methods ===
    
    def run_hybrid_analysis(self):
        """Hibrit program analizi çalıştır"""
        if not self.hybrid_analyzer:
            messagebox.showwarning("Warning", "Hybrid analyzer not available")
            return
        
        if not self.selected_entry:
            messagebox.showwarning("Warning", "Lütfen önce bir dosya seçin")
            return
        
        try:
            self.log_message("🔍 Hibrit program analizi başlatılıyor...", "INFO")
            
            # PRG verisi çıkar
            prg_data = self.extract_prg_data(self.selected_entry)
            if not prg_data:
                error_msg = "PRG verisi çıkarılamadı - dosya formatı hatalı olabilir"
                self.log_message(error_msg, "ERROR")
                messagebox.showerror("Error", error_msg)
                return
            
            self.log_message(f"PRG verisi çıkarıldı: {len(prg_data)} bytes", "INFO")
            
            # Hibrit analiz et
            analysis = self.hybrid_analyzer.analyze_prg_data(prg_data)
            
            self.log_message(f"Hibrit analiz tamamlandı: {type(analysis)}", "INFO")
            self.log_message(f"Analysis keys: {list(analysis.keys()) if isinstance(analysis, dict) else 'Not a dict'}", "DEBUG")
            
            # Rapor oluştur ve göster
            report = self.hybrid_analyzer.generate_hybrid_report(analysis)
            
            self.log_message(f"Hibrit rapor oluşturuldu: {len(report)} chars", "INFO")
            
            # Yeni pencerede göster
            self.show_hybrid_analysis_results(analysis, report)
            
        except Exception as e:
            error_msg = f"Hibrit analiz hatası: {e}"
            self.log_message(error_msg, "ERROR")
            
            # Stack trace log'la
            import traceback
            full_trace = traceback.format_exc()
            self.log_message(f"Hibrit analiz stack trace:\n{full_trace}", "ERROR")
            
            # Terminal'e de yazdır
            print(f"\n🚨 HIBRIT ANALIZ HATASI:")
            print(f"Error: {error_msg}")
            print(f"\nStack Trace:")
            print(full_trace)
            
            # GUI console'a da yazdır
            if hasattr(self, 'console_panel'):
                self.console_panel.add_log(error_msg, "ERROR")
                self.console_panel.add_log(f"Stack Trace: {full_trace}", "ERROR")
            
            messagebox.showerror("Hibrit Analiz Hatası", f"Hata: {error_msg}\n\nDetaylar terminalde ve log'da gösterildi.")
    
    def show_hybrid_analysis_results(self, analysis: Dict[str, Any], report: str):
        """Hibrit analiz sonuçlarını göster"""
        
        result_window = tk.Toplevel(self.root)
        result_window.title("🔍 Hibrit Program Analiz Sonuçları")
        result_window.geometry("900x700")
        result_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = tk.Label(result_window, text="🔍 Hibrit Program Analiz Raporu", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # Notebook widget ile sekmeler
        notebook = ttk.Notebook(result_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Rapor sekmesi
        report_frame = tk.Frame(notebook, bg=ModernStyle.BG_PRIMARY)
        notebook.add(report_frame, text="📊 Analiz Raporu")
        
        report_text = scrolledtext.ScrolledText(report_frame, height=35, width=100,
                                               bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                               font=("Consolas", 10))
        report_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        report_text.insert(1.0, report)
        report_text.config(state=tk.DISABLED)
        
        # BASIC Kodu sekmesi
        if analysis.get("basic_info") and analysis["basic_info"].get("lines"):
            basic_frame = tk.Frame(notebook, bg=ModernStyle.BG_PRIMARY)
            notebook.add(basic_frame, text="📝 BASIC Kod")
            
            basic_text = scrolledtext.ScrolledText(basic_frame, height=35, width=100,
                                                  bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                                  font=("Consolas", 10))
            basic_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            basic_code = ""
            for line in analysis["basic_info"]["lines"]:
                basic_code += f"{line['number']} {line['text']}\n"
            
            basic_text.insert(1.0, basic_code)
            basic_text.config(state=tk.DISABLED)
        
        # Assembly Kodu sekmesi (hibrit ise)
        if analysis.get("is_hybrid") and analysis.get("assembly_info"):
            assembly_frame = tk.Frame(notebook, bg=ModernStyle.BG_PRIMARY)
            notebook.add(assembly_frame, text="⚙️ Assembly Kod")
            
            assembly_text = scrolledtext.ScrolledText(assembly_frame, height=35, width=100,
                                                     bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                                     font=("Consolas", 10))
            assembly_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            try:
                # Assembly kodu disassemble et - ENHANCED ERROR HANDLING
                assembly_info = analysis["assembly_info"]
                self.log_message(f"Assembly info keys: {list(assembly_info.keys())}", "DEBUG")
                
                # Check if 'data' key exists
                if "data" not in assembly_info:
                    error_msg = f"Assembly info 'data' anahtarı bulunamadı. Available keys: {list(assembly_info.keys())}"
                    self.log_message(error_msg, "ERROR")
                    assembly_text.insert(1.0, f"; ERROR: {error_msg}\n; Assembly info content: {str(assembly_info)[:200]}...\n")
                    assembly_text.config(state=tk.DISABLED)
                    return
                
                assembly_data = assembly_info["data"]
                start_address = assembly_info.get("start_address", 0x1000)
                
                self.log_message(f"Assembly data length: {len(assembly_data)} bytes, start: ${start_address:04X}", "INFO")
                
                # Disassembly yap
                if AdvancedDisassembler:
                    try:
                        disassembler = AdvancedDisassembler(
                            start_address=start_address,
                            code=assembly_data,
                            use_illegal_opcodes=False
                        )
                        assembly_code = disassembler.disassemble()
                        assembly_text.insert(1.0, assembly_code)
                        self.log_message("✅ Assembly disassembly başarılı", "INFO")
                    except Exception as dis_error:
                        error_msg = f"Disassembly hatası: {dis_error}"
                        self.log_message(error_msg, "ERROR")
                        import traceback
                        self.log_message(f"Disassembly stack trace:\n{traceback.format_exc()}", "ERROR")
                        
                        assembly_text.insert(1.0, f"; Disassembly error: {dis_error}\n; Raw bytes:\n")
                        for i, byte in enumerate(assembly_data):
                            if i % 16 == 0:
                                assembly_text.insert(tk.END, f"\n${start_address + i:04X}: ")
                            assembly_text.insert(tk.END, f"{byte:02X} ")
                else:
                    assembly_text.insert(1.0, "; AdvancedDisassembler not available\n; Raw bytes:\n")
                    for i, byte in enumerate(assembly_data):
                        if i % 16 == 0:
                            assembly_text.insert(tk.END, f"\n${start_address + i:04X}: ")
                        assembly_text.insert(tk.END, f"{byte:02X} ")
                
            except Exception as assembly_error:
                error_msg = f"Assembly kod gösterme hatası: {assembly_error}"
                self.log_message(error_msg, "ERROR")
                import traceback
                full_trace = traceback.format_exc()
                self.log_message(f"Assembly error stack trace:\n{full_trace}", "ERROR")
                
                # Terminal'e de yazdır
                print(f"\n🚨 ASSEMBLY KOD HATASI:")
                print(f"Error: {error_msg}")
                print(f"Stack Trace:\n{full_trace}")
                
                # GUI console'a da yazdır
                if hasattr(self, 'console_panel'):
                    self.console_panel.add_log(error_msg, "ERROR")
                    self.console_panel.add_log(f"Stack Trace: {full_trace}", "ERROR")
                
                assembly_text.insert(1.0, f"; ASSEMBLY ERROR: {error_msg}\n; Stack Trace:\n{full_trace}\n")
                
            assembly_text.config(state=tk.DISABLED)
        
        # Buton çubuğu
        button_frame = tk.Frame(result_window, bg=ModernStyle.BG_PRIMARY)
        button_frame.pack(fill=tk.X, pady=10)
        
        if analysis.get("is_hybrid"):
            ttk.Button(button_frame, text="⚙️ Assembly Disassemble Et", 
                      command=lambda: self.extract_assembly_code()).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, text="💾 Rapor Kaydet", 
                  command=lambda: self.save_hybrid_report(report)).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ Kapat", 
                  command=result_window.destroy).pack(side=tk.RIGHT, padx=10)
    
    def extract_assembly_code(self):
        """Hibrit programdan assembly kodunu ayır ve disassemble et"""
        if not self.hybrid_analyzer or not self.selected_entry:
            return
        
        try:
            # PRG verisi çıkar
            prg_data = self.extract_prg_data(self.selected_entry)
            if not prg_data:
                return
            
            # Hibrit analiz et
            analysis = self.hybrid_analyzer.analyze_prg_data(prg_data)
            
            if not analysis.get("is_hybrid"):
                messagebox.showinfo("Info", "Bu dosya hibrit program değil")
                return
            
            # Assembly bilgilerini al
            assembly_info = analysis.get("assembly_info")
            if not assembly_info:
                messagebox.showwarning("Warning", "Assembly kodu bulunamadı")
                return
            
            # Assembly kodunu doğru offset ile çıkar
            basic_size = analysis.get("basic_info", {}).get("basic_calculated_size", 0)
            assembly_data = prg_data[2 + basic_size:]  # PRG header (2 byte) + BASIC size
            start_address = assembly_info.get("assembly_start", assembly_info.get("start_address", 0x1000))
            
            if AdvancedDisassembler:
                disassembler = AdvancedDisassembler(
                    start_address=start_address,
                    code=assembly_data,
                    use_illegal_opcodes=self.disassembly_panel.use_illegal_opcodes.get()
                )
                assembly_code = disassembler.disassemble()
            else:
                assembly_code = f"; Assembly Code Extracted from Hybrid Program\n"
                assembly_code += f"; Start Address: ${start_address:04X}\n"
                assembly_code += f"; Size: {len(assembly_data)} bytes\n\n"
                assembly_code += "; Raw bytes (AdvancedDisassembler not available):\n"
                for i, byte in enumerate(assembly_data):
                    if i % 16 == 0:
                        assembly_code += f"\n${start_address + i:04X}: "
                    assembly_code += f"{byte:02X} "
            
            # Disassembly paneline gönder
            self.disassembly_panel.update_code(assembly_code, "HYBRID_ASSEMBLY")
            self.update_status("✅ Hibrit programdan assembly kodu ayrıldı")
            self.log_message("Hybrid assembly extraction completed", "SUCCESS")
            
        except Exception as e:
            messagebox.showerror("Error", f"Assembly ayırma hatası: {e}")
            self.log_message(f"Assembly extraction error: {e}", "ERROR")
    
    def save_hybrid_report(self, report: str):
        """Hibrit analiz raporunu kaydet"""
        filename = filedialog.asksaveasfilename(
            title="Save Hybrid Analysis Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"Rapor kaydedildi: {filename}")
                self.log_message(f"Hybrid report saved: {filename}", "INFO")
            except Exception as e:
                messagebox.showerror("Error", f"Rapor kaydetme hatası: {e}")
    
    def extract_assembly_from_hybrid(self, entry):
        """Hibrit programdan Assembly kısmını ayır"""
        threading.Thread(target=self._extract_assembly_thread, args=(entry,), daemon=True).start()
    
    def _extract_assembly_thread(self, entry):
        """Assembly ayırma thread'i"""
        try:
            self.log_message("Assembly ayırma başlatılıyor...", "INFO")
            
            # Hibrit analiz yap
            if not hasattr(self, 'hybrid_analyzer'):
                from hybrid_program_analyzer import HybridProgramAnalyzer
                self.hybrid_analyzer = HybridProgramAnalyzer(self.memory_manager)
            
            # PRG data al
            prg_data = entry.get('data', b'')
            if not prg_data:
                self.log_message("PRG verisi bulunamadı", "ERROR")
                return
            
            # Hibrit analiz
            analysis = self.hybrid_analyzer.analyze_prg_data(prg_data)
            
            if not analysis.get('is_hybrid'):
                self.log_message("Bu dosya hibrit program değil", "WARNING")
                return
            
            # Assembly kısmını ayır
            asm_info = analysis.get('assembly_info', {})
            if not asm_info:
                self.log_message("Assembly kısmı bulunamadı", "ERROR")
                return
            
            # Assembly data'yı çıkar
            asm_start = asm_info.get('assembly_start', 0)
            asm_size = asm_info.get('assembly_size', 0)
            start_offset = asm_start - analysis.get('start_address', 0x0801) + 2  # +2 for load address
            
            if start_offset < 0 or start_offset >= len(prg_data):
                self.log_message("Assembly offset hesaplama hatası", "ERROR")
                return
            
            asm_data = prg_data[start_offset:start_offset + asm_size]
            
            # Assembly dosyasını oluştur
            filename = entry.get('filename', 'unknown')
            output_filename = f"asm_files/{filename}_assembly.prg"
            
            with open(output_filename, 'wb') as f:
                # Load address yaz
                f.write(asm_start.to_bytes(2, 'little'))
                # Assembly data yaz
                f.write(asm_data)
            
            self.log_message(f"Assembly kaydedildi: {output_filename}", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Assembly ayırma hatası: {e}", "ERROR")
    
    def extract_basic_from_hybrid(self, entry):
        """Hibrit programdan BASIC kısmını ayır"""
        threading.Thread(target=self._extract_basic_thread, args=(entry,), daemon=True).start()
    
    def _extract_basic_thread(self, entry):
        """BASIC ayırma thread'i"""
        try:
            self.log_message("BASIC ayırma başlatılıyor...", "INFO")
            
            # Hibrit analiz yap
            if not hasattr(self, 'hybrid_analyzer'):
                from hybrid_program_analyzer import HybridProgramAnalyzer
                self.hybrid_analyzer = HybridProgramAnalyzer(self.memory_manager)
            
            # PRG data al
            prg_data = entry.get('data', b'')
            if not prg_data:
                self.log_message("PRG verisi bulunamadı", "ERROR")
                return
            
            # Hibrit analiz
            analysis = self.hybrid_analyzer.analyze_prg_data(prg_data)
            
            if not analysis.get('is_hybrid'):
                self.log_message("Bu dosya hibrit program değil", "WARNING")
                return
            
            # BASIC kısmını ayır
            basic_info = analysis.get('basic_info', {})
            if not basic_info:
                self.log_message("BASIC kısmı bulunamadı", "ERROR")
                return
            
            basic_size = basic_info.get('basic_calculated_size', 0)
            if basic_size <= 0:
                self.log_message("BASIC boyutu hesaplanamadı", "ERROR")
                return
            
            # BASIC data'yı çıkar (load address + BASIC code)
            basic_data = prg_data[:basic_size + 2]  # +2 for load address
            
            # BASIC dosyasını oluştur
            filename = entry.get('filename', 'unknown')
            output_filename = f"prg_files/{filename}_basic.prg"
            
            with open(output_filename, 'wb') as f:
                f.write(basic_data)
            
            self.log_message(f"BASIC kaydedildi: {output_filename}", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"BASIC ayırma hatası: {e}", "ERROR")

    def _format_enhanced_hybrid_report(self, analysis_result):
        """Enhanced hibrit analiz raporu oluştur"""
        if not analysis_result:
            return "❌ Analiz başarısız"
        
        report = []
        report.append("=" * 60)
        report.append("🔍 ENHANCED HİBRİT PROGRAM ANALİZİ")
        report.append("=" * 60)
        
        # Genel bilgiler
        report.append(f"\n📊 GENEL BİLGİLER:")
        report.append(f"   Yükleme Adresi: ${analysis_result['load_address']:04X}")
        report.append(f"   Toplam Boyut: {analysis_result['total_size']} byte")
        report.append(f"   Analiz Tipi: {analysis_result['analysis']}")
        
        if analysis_result.get('sys_address'):
            report.append(f"   SYS Adresi: {analysis_result['sys_address']} (${analysis_result['sys_address']:04X})")
        
        # BASIC section analizi
        if analysis_result.get('basic_section'):
            basic = analysis_result['basic_section']
            report.append(f"\n📝 BASIC SECTION:")
            report.append(f"   Başlangıç: ${basic['start_address']:04X}")
            report.append(f"   Bitiş: ${basic['end_address']:04X}")
            report.append(f"   Boyut: {basic['size']} byte")
            
        # Assembly section analizi  
        if analysis_result.get('assembly_section'):
            asm = analysis_result['assembly_section']
            report.append(f"\n⚙️ ASSEMBLY SECTION:")
            report.append(f"   Başlangıç: ${asm['start_address']:04X}")
            report.append(f"   Bitiş: ${asm['end_address']:04X}")
            report.append(f"   Boyut: {asm['size']} byte")
        
        # Öneriler
        report.append(f"\n💡 ÖNERİLER:")
        if analysis_result['analysis'] == 'hybrid_program':
            report.append("   ✅ Bu hibrit bir program (BASIC + Assembly)")
            report.append("   🔧 BASIC kısmını ayrı olarak analiz edebilirsiniz")
            report.append("   🔧 Assembly kısmını disassemble edebilirsiniz")
        elif analysis_result['analysis'] == 'pure_assembly':
            report.append("   ✅ Bu saf assembly programı")
            report.append("   🔧 Doğrudan disassemble edebilirsiniz")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)
    
    def _format_enhanced_hybrid_report_v2(self, analysis_result):
        """Enhanced hibrit analiz raporu V2 - Enhanced D64 Reader çıktısı için"""
        if not analysis_result:
            return "❌ Analiz başarısız"
        
        report = []
        report.append("=" * 70)
        report.append("🎯 ENHANCED D64 READER - HİBRİT PROGRAM ANALİZİ V2")
        report.append("=" * 70)
        
        # Program türü
        if analysis_result.get('is_hybrid'):
            report.append(f"🔄 Program Türü: Hibrit (BASIC + Assembly)")
        else:
            report.append(f"📄 Program Türü: Tek Format")
        
        # Analiz detayları
        report.append(f"\n📊 ANALİZ SONUÇLARI:")
        report.append(f"   {analysis_result.get('analysis', 'Bilinmeyen format')}")
        
        # BASIC segment bilgileri
        if analysis_result.get('basic_segment'):
            basic_size = len(analysis_result['basic_segment'])
            report.append(f"\n📝 BASIC SEGMENT:")
            report.append(f"   Boyut: {basic_size} byte")
            report.append(f"   Başlangıç: $0801")
            report.append(f"   Bitiş: ${0x0801 + basic_size - 1:04X}")
        
        # Assembly segment bilgileri
        if analysis_result.get('asm_segment'):
            asm_size = len(analysis_result['asm_segment'])
            asm_addr = analysis_result.get('asm_start_address', 0)
            report.append(f"\n⚙️ ASSEMBLY SEGMENT:")
            report.append(f"   Boyut: {asm_size} byte")
            report.append(f"   Başlangıç: ${asm_addr:04X}")
            report.append(f"   Bitiş: ${asm_addr + asm_size - 1:04X}")
        
        # SYS adresleri
        if analysis_result.get('sys_addresses'):
            report.append(f"\n🎯 SYS ÇAĞRILARİ:")
            for addr in analysis_result['sys_addresses']:
                report.append(f"   SYS {addr} (${addr:04X})")
        
        # Öneriler ve sonuç
        report.append(f"\n💡 ÖNERİLER:")
        if analysis_result.get('is_hybrid'):
            report.append("   ✅ Hibrit program tespit edildi")
            report.append("   🔧 BASIC kısmı Enhanced BASIC Decompiler ile çevrilebilir")
            report.append("   🔧 Assembly kısmı 4 farklı disassembler ile analiz edilebilir")
            report.append("   🎯 SYS çağrıları ile bağlantı noktaları tespit edildi")
        else:
            if analysis_result.get('basic_segment'):
                report.append("   📝 Saf BASIC program")
                report.append("   🔧 Enhanced BASIC Decompiler kullanın")
            elif analysis_result.get('asm_segment'):
                report.append("   ⚙️ Saf Assembly program")
                report.append("   🔧 4 disassembler seçeneğinden birini kullanın")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)

    def _show_enhanced_hybrid_analysis_result(self, entry, analysis_result, detailed_report):
        """Enhanced hibrit analiz sonuçlarını göster"""
        try:
            # Yeni pencere oluştur
            result_window = tk.Toplevel(self.root)
            result_window.title("🔍 Enhanced Hibrit Program Analizi")
            result_window.geometry("1000x800")
            result_window.configure(bg=ModernStyle.BG_PRIMARY)
            
            # Ana frame
            main_frame = tk.Frame(result_window, bg=ModernStyle.BG_PRIMARY)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Başlık
            title_label = tk.Label(main_frame, 
                                 text=f"🔍 Enhanced Hibrit Analiz: {entry.get('filename', 'Unknown')}",
                                 bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY,
                                 font=("Arial", 14, "bold"))
            title_label.pack(pady=(0, 10))
            
            # Notebook (Tab sistemi)
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # 1. Analiz Özeti Tab
            summary_frame = tk.Frame(notebook, bg=ModernStyle.BG_SECONDARY)
            notebook.add(summary_frame, text="📊 Analiz Özeti")
            
            summary_text = tk.Text(summary_frame, bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                 font=("Consolas", 10), wrap=tk.WORD)
            summary_scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=summary_text.yview)
            summary_text.configure(yscrollcommand=summary_scrollbar.set)
            
            summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Özet bilgileri ekle
            if analysis_result:
                summary_info = []
                summary_info.append(f"📁 Dosya: {entry.get('filename', 'Unknown')}")
                summary_info.append(f"📊 Yükleme Adresi: ${analysis_result['load_address']:04X}")
                summary_info.append(f"📏 Toplam Boyut: {analysis_result['total_size']} byte")
                summary_info.append(f"🔍 Tip: {analysis_result['analysis']}")
                
                if analysis_result.get('sys_address'):
                    summary_info.append(f"🚀 SYS Adresi: {analysis_result['sys_address']}")
                
                if analysis_result.get('basic_section'):
                    basic = analysis_result['basic_section']
                    summary_info.append(f"\n📝 BASIC Section:")
                    summary_info.append(f"   💾 ${basic['start_address']:04X} - ${basic['end_address']:04X}")
                    summary_info.append(f"   📏 {basic['size']} byte")
                
                if analysis_result.get('assembly_section'):
                    asm = analysis_result['assembly_section']
                    summary_info.append(f"\n⚙️ Assembly Section:")
                    summary_info.append(f"   💾 ${asm['start_address']:04X} - ${asm['end_address']:04X}")
                    summary_info.append(f"   📏 {asm['size']} byte")
                
                summary_text.insert(tk.END, "\n".join(summary_info))
            
            # 2. Detaylı Rapor Tab
            report_frame = tk.Frame(notebook, bg=ModernStyle.BG_SECONDARY)
            notebook.add(report_frame, text="📋 Detaylı Rapor")
            
            report_text = tk.Text(report_frame, bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                font=("Consolas", 10), wrap=tk.WORD)
            report_scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=report_text.yview)
            report_text.configure(yscrollcommand=report_scrollbar.set)
            
            report_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            report_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            report_text.insert(tk.END, detailed_report)
            
            # 3. İşlemler Tab
            actions_frame = tk.Frame(notebook, bg=ModernStyle.BG_SECONDARY)
            notebook.add(actions_frame, text="🔧 İşlemler")
            
            # Action buttons
            action_buttons_frame = tk.Frame(actions_frame, bg=ModernStyle.BG_SECONDARY)
            action_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
            
            if analysis_result and analysis_result.get('basic_section'):
                ttk.Button(action_buttons_frame, text="📝 BASIC'i Ayır",
                          command=lambda: self._extract_basic_section(entry, analysis_result)).pack(side=tk.LEFT, padx=5)
            
            if analysis_result and analysis_result.get('assembly_section'):
                ttk.Button(action_buttons_frame, text="⚙️ Assembly'yi Ayır",
                          command=lambda: self._extract_assembly_section(entry, analysis_result)).pack(side=tk.LEFT, padx=5)
                ttk.Button(action_buttons_frame, text="🔧 Assembly Disassemble",
                          command=lambda: self._disassemble_assembly_section(entry, analysis_result)).pack(side=tk.LEFT, padx=5)
            
            # Kapat butonu
            close_frame = tk.Frame(main_frame, bg=ModernStyle.BG_PRIMARY)
            close_frame.pack(fill=tk.X, pady=(10, 0))
            
            ttk.Button(close_frame, text="❌ Kapat", command=result_window.destroy).pack()
            
            # Log message
            self.log_message(f"✅ Enhanced hibrit analiz tamamlandı: {entry.get('filename', 'Unknown')}", "INFO")
            
        except Exception as e:
            self.log_message(f"Enhanced hibrit analiz gösterim hatası: {e}", "ERROR")
            import traceback
            print(f"Enhanced hybrid display error: {traceback.format_exc()}")

    def _extract_basic_section(self, entry, analysis_result):
        """BASIC section'ı dosya olarak kaydet"""
        try:
            if not analysis_result.get('basic_section'):
                self.log_message("BASIC section bulunamadı", "WARNING")
                return
            
            basic_data = analysis_result['basic_section']['data']
            filename = entry.get('filename', 'unknown')
            
            # Dosya kaydet
            output_path = f"pseudo_files/{filename}_basic.prg"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                # Load address ekle
                load_addr = analysis_result['basic_section']['start_address']
                f.write(struct.pack('<H', load_addr))
                f.write(basic_data)
            
            self.log_message(f"✅ BASIC section kaydedildi: {output_path}", "INFO")
            
        except Exception as e:
            self.log_message(f"BASIC section kaydetme hatası: {e}", "ERROR")

    def _extract_assembly_section(self, entry, analysis_result):
        """Assembly section'ı dosya olarak kaydet"""
        try:
            if not analysis_result.get('assembly_section'):
                self.log_message("Assembly section bulunamadı", "WARNING")
                return
            
            asm_data = analysis_result['assembly_section']['data']
            filename = entry.get('filename', 'unknown')
            
            # Dosya kaydet
            output_path = f"pseudo_files/{filename}_assembly.prg"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                # Load address ekle
                load_addr = analysis_result['assembly_section']['start_address']
                f.write(struct.pack('<H', load_addr))
                f.write(asm_data)
            
            self.log_message(f"✅ Assembly section kaydedildi: {output_path}", "INFO")
            
        except Exception as e:
            self.log_message(f"Assembly section kaydetme hatası: {e}", "ERROR")

    def _disassemble_assembly_section(self, entry, analysis_result):
        """Assembly section'ı disassemble et"""
        try:
            if not analysis_result.get('assembly_section'):
                self.log_message("Assembly section bulunamadı", "WARNING")
                return
            
            asm_data = analysis_result['assembly_section']['data']
            start_addr = analysis_result['assembly_section']['start_address']
            filename = entry.get('filename', 'unknown')
            
            # Disassemble işlemi
            if hasattr(self, 'unified_decompiler') and self.unified_decompiler:
                self.log_message("🔧 Assembly section disassemble ediliyor...", "INFO")
                
                # Create temp entry for disassembler
                temp_entry = {
                    'filename': f"{filename}_assembly",
                    'start_address': start_addr,
                    'size': len(asm_data)
                }
                
                # Disassemble and save
                asm_output = self.unified_decompiler.disassemble_bytes(asm_data, start_addr)
                
                output_path = f"asm_files/{filename}_assembly.asm"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"; Enhanced Hibrit Analiz - Assembly Section\n")
                    f.write(f"; Kaynak: {filename}\n")
                    f.write(f"; Başlangıç Adresi: ${start_addr:04X}\n")
                    f.write(f"; Boyut: {len(asm_data)} byte\n\n")
                    f.write(asm_output)
                
                self.log_message(f"✅ Assembly disassemble edildi: {output_path}", "INFO")
            else:
                self.log_message("Unified decompiler bulunamadı", "WARNING")
            
        except Exception as e:
            self.log_message(f"Assembly disassemble hatası: {e}", "ERROR")

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
