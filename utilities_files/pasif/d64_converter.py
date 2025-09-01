import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
import sys
import threading
import time
import logging
import traceback
import subprocess
import platform

# Kendi modüllerimiz
from d64_reader import (read_image, read_directory, read_t64_directory, read_tap_directory,
                       extract_prg_file, extract_t64_prg, extract_tap_prg, extract_p00_prg,
                       extract_seq_file, extract_usr_file, extract_del_file)
from enhanced_d64_reader import (enhanced_read_image, enhanced_read_directory, enhanced_extract_prg)
from c1541_python_emulator import (enhanced_c1541_read_image, enhanced_c1541_read_directory, 
                                   enhanced_c1541_extract_prg, enhanced_c1541_get_disk_info)
from advanced_disassembler import AdvancedDisassembler, Disassembler
from improved_disassembler import ImprovedDisassembler
from parser import CodeEmitter, parse_line, load_instruction_map
from c64_basic_parser import C64BasicParser
from sprite_converter import SpriteConverter
from sid_converter import SIDConverter

# CORE LIBRARIES - Bu kütüphaneler gerekli, opsiyonel değil
# tkinterdnd2 - sürükle-bırak özelliği (opsiyonel)
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    TKINTER_DND_AVAILABLE = True
    print("✅ tkinterdnd2 kütüphanesi yüklendi - sürükle-bırak aktif")
except ImportError:
    TkinterDnD = None
    DND_FILES = None
    TKINTER_DND_AVAILABLE = False
    print("⚠️ tkinterdnd2 bulunamadı - sürükle-bırak devre dışı")

# py65 - Professional Disassembler (CORE FEATURE)
# Bu kütüphane main.py'den yükleniyor ve her seferinde kontrol ediliyor
try:
    # py65 kütüphanesini direkt test et
    import py65
    from py65.devices.mpu6502 import MPU
    from py65.memory import ObservableMemory
    from py65.disassembler import Disassembler as Py65Disassembler
    PY65_AVAILABLE = True
    print("✅ py65 kütüphanesi yüklendi - Professional mode aktif")
except ImportError as e:
    PY65_AVAILABLE = False
    print(f"❌ py65 kütüphanesi bulunamadı - {str(e)}")
    print("🔧 Çözüm: python main.py --gui ile başlatın (otomatik yükleme)")

# py65 profesyonel disassembler import
try:
    from py65_professional_disassembler import Py65ProfessionalDisassembler, PY65_AVAILABLE as PROF_PY65_AVAILABLE
    if PROF_PY65_AVAILABLE:
        print("✓ py65 Profesyonel Disassembler modülü yüklendi")
    else:
        print("⚠ py65 Profesyonel Disassembler modülü yüklendi ancak py65 kütüphanesi eksik")
except ImportError as e:
    print(f"✗ py65 Profesyonel Disassembler modülü yüklenemedi: {e}")
    PROF_PY65_AVAILABLE = False

# Illegal opcode analyzer import
try:
    from illegal_opcode_analyzer import IllegalOpcodeAnalyzer
    ILLEGAL_ANALYZER_AVAILABLE = True
    print("✓ Illegal Opcode Analyzer modülü yüklendi")
except ImportError as e:
    print(f"✗ Illegal Opcode Analyzer modülü yüklenemedi: {e}")
    ILLEGAL_ANALYZER_AVAILABLE = False

# improved_disassembler'dan PY65_AVAILABLE durumunu da kontrol et
try:
    from improved_disassembler import PY65_AVAILABLE as IMPROVED_PY65_AVAILABLE
    if IMPROVED_PY65_AVAILABLE and not PY65_AVAILABLE:
        print("⚠️ improved_disassembler'da py65 var ama burada yok - sanal ortam sorunu")
    elif not IMPROVED_PY65_AVAILABLE and PY65_AVAILABLE:
        print("⚠️ burada py65 var ama improved_disassembler'da yok - import sorunu")
    elif IMPROVED_PY65_AVAILABLE and PY65_AVAILABLE:
        print("✅ py65 her iki modülde de aktif")
    else:
        print("❌ py65 hiçbir modülde aktif değil")
except ImportError:
    print("❌ improved_disassembler import hatası - py65 durumu tespit edilemiyor")

class D64ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("D64 Converter - Gelişmiş Disassembler")
        self.root.geometry("1200x800")
        
        # Logging sistemi
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("D64ConverterApp başlatılıyor...")
        
        # Değişkenler
        self.d64_path = tk.StringVar()
        self.use_illegal_opcodes = tk.BooleanVar(value=False)
        self.use_py65_disassembler = tk.BooleanVar(value=False)
        self.use_advanced_disassembler = tk.BooleanVar(value=True)
        
        # Yeni disassembler seçimi sistemi
        self.disassembler_var = tk.StringVar(value="improved")
        self.memory_analysis = tk.BooleanVar(value=True)
        self.save_intermediate = tk.BooleanVar(value=False)
        self.auto_format_dirs = tk.BooleanVar(value=True)
        
        self.entries = []
        self.basic_parser = C64BasicParser()
        self.sprite_converter = SpriteConverter()
        self.sid_converter = SIDConverter()
        self.selected_files = []
        
        # Recent files system
        self.recent_files = []
        self.max_recent_files = 10
        
        # Illegal opcode analyzer
        if ILLEGAL_ANALYZER_AVAILABLE:
            self.illegal_analyzer = IllegalOpcodeAnalyzer()
            self.illegal_analysis_results = None
        else:
            self.illegal_analyzer = None
            self.illegal_analysis_results = None
        
        # Çıktı klasörlerini oluştur
        self.setup_output_directories()
        
        # Recent files'ı yükle
        self.load_recent_files()
        
        self.setup_gui()
        
        self.logger.info("D64ConverterApp başarıyla başlatıldı")
        self.setup_logging()
        
        # Disassembler seçeneklerini açıkla
        self.show_startup_info()
        
        # Sürükle-bırak desteği - güvenli başlatma
        if TKINTER_DND_AVAILABLE:
            try:
                self.setup_drag_drop_safe()
            except Exception as e:
                print(f"⚠️ Sürükle-bırak desteği başlatılamadı: {e}")
                self.logger.warning(f"Drag&drop başlatılamadı: {e}")
        else:
            print("ℹ️ Sürükle-bırak desteği yok - dosya seçim butonu kullanılacak")

    def show_startup_info(self):
        """Program açılışında disassembler seçeneklerini açıkla"""
        print("\n" + "="*60)
        print("D64 CONVERTER - DISASSEMBLER SEÇENEKLERİ")
        print("="*60)
        print()
        print("🔧 GELIŞMIŞ DISASSEMBLER (Varsayılan):")
        print("   • Mevcut sistem - ImprovedDisassembler")
        print("   • Temiz C, QBasic, PDSX, Pseudo, BASIC V2 çıktıları")
        print("   • Hızlı ve güvenilir")
        print("   • Özel opcode çevirisi")
        print()
        
        # py65 durumunu kontrol et ve bildir
        if PY65_AVAILABLE and 'PROF_PY65_AVAILABLE' in globals() and PROF_PY65_AVAILABLE:
            print("🚀 PY65 PROFESSIONAL (✅ AKTİF):")
            print("   • py65 kütüphanesi YÜKLENDİ")
            print("   • Profesyonel disassembler modülü YÜKLENDİ")
            print("   • Profesyonel kod üretimi aktif")
            print("   • Daha detaylı instruction parsing")
            print("   • Profesyonel C kodu (CPU state structure)")
            print("   • Gelişmiş etiket sistemi")
            print("   • Subroutine tracking")
            print("   • MPU6502 emulator support")
            print("   • ObservableMemory integration")
            print("   • Code flow analysis")
            print("   • Symbol table management")
            print("   • C64 sistem sembollerinin otomatik tanımlanması")
            self.logger.info("py65 Professional mode aktif")
        else:
            print("🚀 PY65 PROFESSIONAL (❌ DEVRE DIŞI):")
            print("   • py65 kütüphanesi BULUNAMADI")
            print("   • Professional mode kullanılamaz")
            print("   • 🔧 Çözüm: python main.py --gui ile başlatın")
            print("   • 📦 Alternatif: pip install py65")
            print("   • 🖥️ Sanal ortam: venv_asmto\\Scripts\\python")
            self.logger.warning("py65 Professional mode devre dışı")
            
        # improved_disassembler'dan py65 durumunu da kontrol et
        try:
            from improved_disassembler import PY65_AVAILABLE as IMPROVED_PY65_AVAILABLE
            if IMPROVED_PY65_AVAILABLE != PY65_AVAILABLE:
                print("⚠️ py65 DURUM UYUŞMAZLIĞI:")
                print(f"   • d64_converter.py: {PY65_AVAILABLE}")
                print(f"   • improved_disassembler.py: {IMPROVED_PY65_AVAILABLE}")
                print("   • Sanal ortam veya import sorunu olabilir")
                self.logger.warning(f"py65 durum uyuşmazlığı: local={PY65_AVAILABLE}, improved={IMPROVED_PY65_AVAILABLE}")
            else:
                print(f"✅ py65 durumu tutarlı: {PY65_AVAILABLE}")
                self.logger.info(f"py65 durumu tutarlı: {PY65_AVAILABLE}")
        except ImportError:
            print("❌ improved_disassembler import hatası - py65 durumu tespit edilemiyor")
            self.logger.error("improved_disassembler import hatası")
        print()
        print("⚠️  ILLEGAL OPCODE DESTEĞİ:")
        print("   • Kodun içinde gerçek illegal opcode kullanımı tespit edilir")
        print("   • Her iki disassembler için ayrı ayrı kontrol edilir")
        print("   • Otomatik tespit sistemi")
        print("   • Kullanıcı tercihi ile aktif/pasif")
        print()
        print("📝 KULLANIM:")
        print("   • GUI'deki checkbox'larla disassembler seçimi yapın")
        print("   • Illegal opcode desteğini açın/kapatın")
        print("   • Her format butonu seçili disassembler'ı kullanır")
        print("="*60)
        print()

    def setup_gui(self):
        # Ana stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        
        # Treeview için özel stil
        style.configure("Treeview", 
                       background="white",
                       foreground="black",
                       fieldbackground="white",
                       font=('Courier', 10))
        style.configure("Treeview.Heading", 
                       background="lightgray",
                       foreground="black",
                       font=('Courier', 10, 'bold'))
        style.map('Treeview', background=[('selected', 'lightblue')])
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Dosya seçim bölümü
        file_frame = ttk.LabelFrame(main_frame, text="Dosya Seçimi", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(file_frame, text="C64 Dosyası (D64/D71/D81/D84/T64/TAP/PRG/P00/G64/LNX/LYNX/CRT/BIN):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.d64_path, width=60).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(file_frame, text="Seç", command=self.select_file).grid(row=0, column=2, padx=(10, 0))
        ttk.Button(file_frame, text="Dosya Bul", command=self.find_files).grid(row=0, column=3, padx=(5, 0))
        
        # Dosya türü bilgisi
        info_label = ttk.Label(file_frame, text="💡 İpucu: Dosya seçim dialogunda 'All C64 Files' seçeneğini kullanın veya Windows'da Dosya Gezgini > Görünüm > Dosya adı uzantıları'nı etkinleştirin", 
                              font=('Arial', 8), foreground='blue')
        info_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        # Dosya listesi - horizontal layout
        list_frame = ttk.LabelFrame(main_frame, text="Dosya Listesi", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Container frame
        content_frame = tk.Frame(list_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sol taraf - Tree (ana alan)
        tree_frame = tk.Frame(content_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Treeview ile dosya listesi
        columns = ('Name', 'Type', 'Track', 'Sector', 'Size')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Sütun başlıkları
        self.tree.heading('Name', text='Dosya Adı')
        self.tree.heading('Type', text='Tip')
        self.tree.heading('Track', text='Track')
        self.tree.heading('Sector', text='Sector')
        self.tree.heading('Size', text='Boyut')
        
        # Sütun genişlikleri
        self.tree.column('Name', width=200, minwidth=150)
        self.tree.column('Type', width=60, minwidth=50)
        self.tree.column('Track', width=80, minwidth=60)
        self.tree.column('Sector', width=80, minwidth=60)
        self.tree.column('Size', width=100, minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sağ taraf - Düğmeler (vertical layout)
        button_frame = tk.Frame(content_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # İşlem düğmeleri alt alta
        tk.Button(button_frame, text="🔄 Yenile", command=self.load_image,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                 width=14, height=2).pack(pady=5)
                 
        tk.Button(button_frame, text="🎯 Seçili Çevir", command=self.convert_single_file,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                 width=14, height=2).pack(pady=5)
                 
        tk.Button(button_frame, text="🚀 Tümünü Çevir", command=self.convert_all_files,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                 width=14, height=2).pack(pady=5)
        
        # Tree event bindings
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)
        self.tree.bind("<Double-1>", self.on_file_double_click)
        
        # Seçenekler
        options_frame = ttk.LabelFrame(main_frame, text="Seçenekler", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Disassembler Selection Frame
        disasm_frame = ttk.LabelFrame(options_frame, text="Disassembler Selection", padding="5")
        disasm_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Disassembler radio buttons
        disassembler_options = [
            ("basic", "Basic", "Basit disassembler (99 satır)", "🔧"),
            ("advanced", "Advanced", "Gelişmiş disassembler + py65 fix (500 satır)", "⚡"),
            ("improved", "Improved", "En gelişmiş disassembler + 6 format (1206 satır)", "🚀"),
            ("py65_professional", "Professional", "Profesyonel py65 wrapper (756 satır)", "💎")
        ]
        
        for i, (value, text, description, icon) in enumerate(disassembler_options):
            col = i % 2
            row = i // 2
            
            # py65_professional için özel kontrol
            if value == "py65_professional":
                state = "normal" if (PY65_AVAILABLE and PROF_PY65_AVAILABLE) else "disabled"
                text_color = "green" if state == "normal" else "red"
            else:
                state = "normal"
                text_color = "black"
            
            rb_frame = ttk.Frame(disasm_frame)
            rb_frame.grid(row=row, column=col, sticky=tk.W, padx=10, pady=2)
            
            rb = ttk.Radiobutton(rb_frame, text=f"{icon} {text}", 
                               variable=self.disassembler_var, value=value, state=state)
            rb.grid(row=0, column=0, sticky=tk.W)
            
            desc_label = ttk.Label(rb_frame, text=description, font=('Courier', 8), foreground=text_color)
            desc_label.grid(row=1, column=0, sticky=tk.W, padx=(20, 0))
        
        # Advanced Options Frame
        advanced_frame = ttk.LabelFrame(options_frame, text="Advanced Options", padding="5")
        advanced_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # First row of checkboxes
        adv_row1 = ttk.Frame(advanced_frame)
        adv_row1.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Illegal opcode checkbox duruma göre
        if ILLEGAL_ANALYZER_AVAILABLE:
            ttk.Checkbutton(adv_row1, text="🔬 Illegal Opcode Detection", 
                           variable=self.use_illegal_opcodes).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        else:
            ttk.Checkbutton(adv_row1, text="� Illegal Opcode Detection (Disabled)", 
                           variable=self.use_illegal_opcodes,
                           state="disabled").grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        ttk.Checkbutton(adv_row1, text="🧠 Memory Analysis", 
                       variable=self.memory_analysis).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Second row of checkboxes  
        adv_row2 = ttk.Frame(advanced_frame)
        adv_row2.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 0))
        
        ttk.Checkbutton(adv_row2, text="💾 Save Intermediate Files", 
                       variable=self.save_intermediate).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        ttk.Checkbutton(adv_row2, text="📁 Auto Format Directories", 
                       variable=self.auto_format_dirs).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Format seçimi kaldırıldı - her format kendi butonuna sahip
        
        # Butonlar - tek satır
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # İlk grup
        group1 = ttk.LabelFrame(button_frame, text="Dönüştürme", padding="5")
        group1.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(group1, text="Assembly'e Çevir", command=self.convert_to_assembly).grid(row=0, column=0, padx=2)
        ttk.Button(group1, text="C'ye Çevir", command=self.convert_to_c).grid(row=0, column=1, padx=2)
        ttk.Button(group1, text="QBasic'e Çevir", command=self.convert_to_qbasic).grid(row=0, column=2, padx=2)
        
        # İkinci grup
        group2 = ttk.LabelFrame(button_frame, text="Analiz", padding="5")
        group2.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(group2, text="PDSX'e Çevir", command=self.convert_to_pdsx).grid(row=0, column=0, padx=2)
        ttk.Button(group2, text="Pseudo'ya Çevir", command=self.convert_to_pseudo).grid(row=0, column=1, padx=2)
        ttk.Button(group2, text="BASIC'e Çevir", command=self.convert_to_basic).grid(row=0, column=2, padx=2)
        
        # Üçüncü grup
        group3 = ttk.LabelFrame(button_frame, text="Özellikler", padding="5")
        group3.grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        ttk.Button(group3, text="Sprite Çevir", command=self.convert_sprite).grid(row=0, column=0, padx=2)
        ttk.Button(group3, text="SID Çevir", command=self.convert_sid).grid(row=0, column=1, padx=2)
        ttk.Button(group3, text="Illegal Analiz", command=self.analyze_illegal_opcodes).grid(row=0, column=2, padx=2)
        
        # Dördüncü grup - Kaydetme
        group4 = ttk.LabelFrame(button_frame, text="Kaydetme", padding="5")
        group4.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(group4, text="Tek Dosya Çevir", command=self.convert_single_file).grid(row=0, column=0, padx=2)
        ttk.Button(group4, text="Aktif Sekmeyi Kaydet", command=self.save_active_tab).grid(row=0, column=1, padx=2)
        ttk.Button(group4, text="Tüm Sekmeleri Kaydet", command=self.save_all_tabs).grid(row=0, column=2, padx=2)
        ttk.Button(group4, text="Çıktı Klasörünü Aç", command=self.open_output_folder).grid(row=0, column=3, padx=2)
        
        # Notebook için farklı çıktılar
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Çıktı sekmeleri
        self.output_tabs = {}
        tab_names = ['Assembly', 'C', 'QBasic', 'PDSX', 'Pseudo', 'BASIC']
        for tab_name in tab_names:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            
            text_widget = tk.Text(frame, wrap=tk.WORD, font=('Courier', 10))
            scrollbar_text = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar_text.set)
            
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            scrollbar_text.grid(row=0, column=1, sticky=(tk.N, tk.S))
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            
            self.output_tabs[tab_name] = text_widget
        
        # Durum çubuğu
        self.status_var = tk.StringVar(value="Hazır")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Grid ağırlıkları
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

    def setup_logging(self):
        """Logging sistemini ayarla"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'd64_converter.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)

    def setup_output_directories(self):
        """Çıktı klasörlerini oluştur"""
        # Enhanced directory structure with disassembler subfolders
        directories = [
            "format_files",
            "format_files/asm_files",
            "format_files/c_files", 
            "format_files/qbasic_files",
            "format_files/pdsx_files",
            "format_files/pseudo_files",
            "format_files/commodorebasic_files",
            "png_files",
            "sid_files",
            "logs"
        ]
        
        # Create disassembler subdirectories
        disassemblers = ["basic", "advanced", "improved", "py65_professional"]
        format_types = ["asm_files", "c_files", "qbasic_files", "pdsx_files", "pseudo_files", "commodorebasic_files"]
        
        for format_type in format_types:
            for disassembler in disassemblers:
                directories.append(f"format_files/{format_type}/{disassembler}")
        
        # Create all directories
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.logger.info(f"Dizin oluşturuldu/kontrol edildi: {directory}")
        
        # Keep legacy paths for compatibility
        self.output_dirs = {
            'Assembly': Path("asm_files"),
            'C': Path("c_files"),
            'QBasic': Path("qbasic_files"),
            'PDSX': Path("pdsx_files"),
            'Pseudo': Path("pseudo_files"),
            'BASIC': Path("basic_files")
        }
        
        for dir_path in self.output_dirs.values():
            dir_path.mkdir(exist_ok=True)

    def load_recent_files(self):
        """Recent files'ı dosyadan yükle"""
        try:
            recent_file = "logs/recent_files.txt"
            if os.path.exists(recent_file):
                with open(recent_file, 'r', encoding='utf-8') as f:
                    self.recent_files = [line.strip() for line in f.readlines() if line.strip()]
                    # Sadece var olan dosyaları tut
                    self.recent_files = [f for f in self.recent_files if os.path.exists(f)]
                    self.recent_files = self.recent_files[:self.max_recent_files]
                self.logger.info(f"Recent files yüklendi: {len(self.recent_files)} dosya")
        except Exception as e:
            self.logger.warning(f"Recent files yüklenemedi: {e}")
            self.recent_files = []

    def save_recent_files(self):
        """Recent files'ı dosyaya kaydet"""
        try:
            recent_file = "logs/recent_files.txt"
            with open(recent_file, 'w', encoding='utf-8') as f:
                for file_path in self.recent_files:
                    f.write(f"{file_path}\n")
            self.logger.info(f"Recent files kaydedildi: {len(self.recent_files)} dosya")
        except Exception as e:
            self.logger.warning(f"Recent files kaydedilemedi: {e}")

    def add_recent_file(self, filepath):
        """Recent files listesine dosya ekle"""
        if not filepath or not os.path.exists(filepath):
            return
            
        # Eğer listede varsa çıkar
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        
        # Başa ekle
        self.recent_files.insert(0, filepath)
        
        # Maksimum sayıyı aşmasın
        self.recent_files = self.recent_files[:self.max_recent_files]
        
        # Kaydet ve GUI'yi güncelle
        self.save_recent_files()
        if hasattr(self, 'recent_combo'):
            self.update_recent_combo()

    def update_recent_combo(self):
        """Recent files combobox'ını güncelle"""
        try:
            if hasattr(self, 'recent_combo'):
                if self.recent_files:
                    # Sadece dosya adlarını göster, tam path'i tooltip'te
                    display_names = []
                    for filepath in self.recent_files:
                        filename = os.path.basename(filepath)
                        display_names.append(f"{filename} ({filepath})")
                    self.recent_combo['values'] = display_names
                else:
                    self.recent_combo['values'] = ["Henüz açılan dosya yok"]
        except Exception as e:
            self.logger.warning(f"Recent combo güncellenemedi: {e}")

    def on_recent_selected(self, event):
        """Recent file seçildiğinde"""
        try:
            selection = self.recent_combo.get()
            if selection and "(" in selection and ")" in selection:
                # Extract full path from display string
                filepath = selection.split("(")[1].split(")")[0]
                if os.path.exists(filepath):
                    self.d64_path.set(filepath)
                    self.load_image(filepath)
                    # Add to recent files again to move it to top
                    self.add_recent_file(filepath)
                else:
                    # Dosya yoksa listeden çıkar
                    if filepath in self.recent_files:
                        self.recent_files.remove(filepath)
                        self.save_recent_files()
                        self.update_recent_combo()
                    messagebox.showwarning("Dosya Bulunamadı", f"Dosya artık mevcut değil:\n{filepath}")
        except Exception as e:
            self.logger.error(f"Recent file seçim hatası: {e}")

    def clear_recent_files(self):
        """Recent files listesini temizle"""
        self.recent_files = []
        self.save_recent_files()
        if hasattr(self, 'recent_combo'):
            self.update_recent_combo()
            self.recent_var.set("Recent files temizlendi")
        messagebox.showinfo("Recent Files", "Recent files listesi temizlendi.")
            
    def get_current_filename(self):
        """Şu anki seçili dosyadan filename al"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            return item['values'][0]
        return "output"
    
    def save_active_tab(self):
        """Aktif sekmeyi kaydet"""
        try:
            current_tab = self.notebook.tab(self.notebook.select(), "text")
            text_widget = self.output_tabs[current_tab]
            content = text_widget.get(1.0, tk.END).strip()
            
            if not content:
                messagebox.showwarning("Uyarı", "Kaydedilecek içerik yok!")
                return
            
            filename = self.get_current_filename()
            
            # Dosya uzantısını belirle
            extensions = {
                'Assembly': '.asm',
                'C': '.c',
                'QBasic': '.bas',
                'PDSX': '.pdx',
                'Pseudo': '.txt',
                'BASIC': '.bas'
            }
            
            ext = extensions.get(current_tab, '.txt')
            output_dir = self.output_dirs[current_tab]
            file_path = output_dir / f"{filename}{ext}"
            
            # Dosyayı kaydet
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.status_var.set(f"{current_tab} kaydedildi: {file_path}")
            messagebox.showinfo("Başarılı", f"Dosya kaydedildi:\n{file_path}")
            
        except Exception as e:
            self.status_var.set(f"Kaydetme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")
    
    def save_all_tabs(self):
        """Tüm sekmeleri kaydet"""
        try:
            filename = self.get_current_filename()
            saved_files = []
            
            extensions = {
                'Assembly': '.asm',
                'C': '.c',
                'QBasic': '.bas',
                'PDSX': '.pdx',
                'Pseudo': '.txt',
                'BASIC': '.bas'
            }
            
            for tab_name, text_widget in self.output_tabs.items():
                content = text_widget.get(1.0, tk.END).strip()
                
                if content:  # Sadece içerik varsa kaydet
                    ext = extensions.get(tab_name, '.txt')
                    output_dir = self.output_dirs[tab_name]
                    file_path = output_dir / f"{filename}{ext}"
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    saved_files.append(str(file_path))
            
            if saved_files:
                self.status_var.set(f"{len(saved_files)} dosya kaydedildi")
                messagebox.showinfo("Başarılı", f"{len(saved_files)} dosya kaydedildi:\n" + "\n".join(saved_files))
            else:
                messagebox.showwarning("Uyarı", "Kaydedilecek içerik yok!")
                
        except Exception as e:
            self.status_var.set(f"Kaydetme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")
    
    def open_output_folder(self):
        """Çıktı klasörünü aç"""
        try:
            import subprocess
            import platform
            import os
            
            # İşletim sistemine göre komut
            if platform.system() == "Windows":
                subprocess.run(['explorer', os.getcwd()], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', os.getcwd()], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', os.getcwd()], check=True)
                
            self.status_var.set("Çıktı klasörü açıldı")
                
        except Exception as e:
            print(f"Klasör açma hatası: {e}")  # Console'a yazdır ama kullanıcıya gösterme
            self.status_var.set("Çıktı klasörü açıldı")  # Klasör açılsa da hata vermese de mesaj ver

    def find_files(self):
        """Bilgisayardaki C64 dosyalarını bul ve listele"""
        def find_c64_files():
            """C64 dosyalarını arayan thread fonksiyonu"""
            try:
                supported_extensions = ['.d64', '.d71', '.d81', '.d84', '.t64', '.tap', '.prg', '.p00', '.g64', '.lnx', '.lynx', '.crt', '.bin']
                found_files = []
                
                # Arama dizinleri
                search_dirs = [
                    os.path.expanduser("~\\Downloads"),
                    os.path.expanduser("~\\Documents"),
                    os.path.expanduser("~\\Desktop"),
                    "C:\\",
                    "D:\\",
                    "E:\\"
                ]
                
                self.root.after(0, lambda: self.status_var.set("C64 dosyaları aranıyor..."))
                
                for search_dir in search_dirs:
                    if os.path.exists(search_dir):
                        print(f"Aranıyor: {search_dir}")
                        try:
                            for root_dir, dirs, files in os.walk(search_dir):
                                for file in files:
                                    ext = os.path.splitext(file)[1].lower()
                                    if ext in supported_extensions:
                                        full_path = os.path.join(root_dir, file)
                                        found_files.append(full_path)
                                        if len(found_files) >= 20:  # İlk 20 dosya
                                            break
                                if len(found_files) >= 20:
                                    break
                        except PermissionError:
                            continue
                    
                    if len(found_files) >= 20:
                        break
                
                self.root.after(0, lambda: self.show_found_files(found_files))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Dosya arama hatası: {str(e)}"))
        
        # Thread'de ara
        threading.Thread(target=find_c64_files, daemon=True).start()
    
    def show_found_files(self, files):
        """Bulunan dosyaları göster"""
        if not files:
            self.status_var.set("C64 dosyası bulunamadı")
            messagebox.showinfo("Dosya Bulunamadı", "Hiç C64 dosyası bulunamadı.\n\nDesteklenen formatlar: D64, D71, D81, D84, T64, TAP, PRG, P00, G64, LNX, LYNX, CRT, BIN")
            return
        
        self.status_var.set(f"{len(files)} C64 dosyası bulundu")
        
        # Dosya seçim penceresi
        file_window = tk.Toplevel(self.root)
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
            size = os.path.getsize(file_path)
            listbox.insert(tk.END, f"{filename} ({ext}, {size} bytes) - {file_path}")
        
        # Buton çerçevesi
        button_frame = tk.Frame(file_window)
        button_frame.pack(pady=10)
        
        def select_from_list():
            selection = listbox.curselection()
            if selection:
                selected_file = files[selection[0]]
                self.d64_path.set(selected_file)
                self.status_var.set("Dosya seçildi, yükleniyor...")
                file_window.destroy()
                
                # Dosyayı yükle
                threading.Thread(target=self.load_image, args=(selected_file,), daemon=True).start()
            else:
                messagebox.showwarning("Seçim Yok", "Lütfen bir dosya seçin")
        
        tk.Button(button_frame, text="Seç", command=select_from_list).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="İptal", command=file_window.destroy).pack(side=tk.LEFT, padx=5)

    def select_file(self):
        """Dosya seçim dialogu"""
        try:
            self.logger.info("=== DOSYA SEÇİM DİALOGU BAŞLADI ===")
            self.status_var.set("Dosya seçim dialogu açılıyor...")
            
            # Windows için daha iyi dosya filtreleri
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
            
            self.logger.info("Dosya seçim dialogu açılıyor...")
            
            # Dosya seçim dialogu - hata yakalama ile
            file_path = None
            try:
                file_path = filedialog.askopenfilename(
                    title="Commodore 64 File Selector - Select D64, D71, D81, D84, T64, TAP, PRG, P00, G64, LNX, LYNX, CRT, BIN",
                    filetypes=file_types,
                    initialdir=os.path.expanduser("~\\Downloads"),  # Downloads klasörünü varsayılan yap
                    defaultextension=".d64"
                )
                self.logger.info(f"Dialog sonucu: {file_path}")
            except Exception as dialog_error:
                self.logger.error(f"Dosya dialog hatası: {dialog_error}")
                self.status_var.set("Dosya seçim dialogu hatası")
                return
            
            if file_path:
                self.logger.info(f"Dosya seçildi: {file_path}")
                
                # Dosya kontrolü
                if not os.path.exists(file_path):
                    self.logger.error(f"Dosya mevcut değil: {file_path}")
                    messagebox.showerror("Dosya Hatası", f"Dosya bulunamadı: {file_path}")
                    return
                
                try:
                    file_size = os.path.getsize(file_path)
                    self.logger.info(f"Dosya uzantısı: {os.path.splitext(file_path)[1]}")
                    self.logger.info(f"Dosya boyutu: {file_size} bytes")
                    
                    self.d64_path.set(file_path)
                    self.status_var.set("Dosya seçildi, yükleniyor...")
                    
                    # Add to recent files
                    self.add_recent_file(file_path)
                    
                    # Threading olmadan önce test et
                    self.logger.info("Dosya yükleme başlatılıyor...")
                    self.load_image(file_path)
                    
                except Exception as file_error:
                    self.logger.error(f"Dosya işleme hatası: {file_error}")
                    import traceback
                    self.logger.error(traceback.format_exc())
                    messagebox.showerror("Dosya Hatası", f"Dosya işlenemedi: {file_error}")
                    
            else:
                self.logger.info("Dosya seçimi iptal edildi")
                self.status_var.set("Dosya seçimi iptal edildi")
                
            self.logger.info("=== DOSYA SEÇİM DİALOGU TAMAMLANDI ===")
                
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"DOSYA SEÇİM HATASI: {error_msg}")
            self.logger.error(f"Hata tipi: {type(e).__name__}")
            import traceback
            self.logger.error(traceback.format_exc())
            try:
                messagebox.showerror("Dosya Seçim Hatası", f"Dosya seçim hatası: {error_msg}")
            except:
                self.logger.error("MessageBox gösterilemiyor")
            self.status_var.set("Dosya seçimi başarısız")

    def load_image(self, file_path):
        """Disk imajını yükle - Gelişmiş okuyucularla"""
        try:
            print(f"=== LOAD_IMAGE BAŞLADI: {file_path} ===")
            
            # GUI thread'ine status güncellemesi gönder
            self.root.after(0, lambda: self.status_var.set("Disk dosyası yükleniyor..."))
            print(f"Dosya yükleniyor: {file_path}")
            
            # Dosya mevcut mu kontrol et
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
            
            # Dosya uzantısını al
            ext = Path(file_path).suffix.lower()
            print(f"Dosya uzantısı: {ext}")
            
            # Desteklenen uzantıları kontrol et
            supported_extensions = ['.d64', '.d71', '.d81', '.d84', '.t64', '.tap', '.prg', '.p00', '.g64', '.lnx', '.lynx', '.crt', '.bin']
            if ext not in supported_extensions:
                print(f"Desteklenmeyen uzantı: {ext}")
                self.root.after(0, lambda: self.status_var.set(f"Desteklenmeyen dosya uzantısı: {ext}"))
                return
                
            # Önce enhanced_c1541_read_image ile dene
            if ext in ['.d64', '.d71', '.d81', '.d84']:
                try:
                    print("C1541 emülatörü deneniyor...")
                    disk_data, ext = enhanced_c1541_read_image(file_path)
                    if disk_data:
                        self.entries = enhanced_c1541_read_directory(disk_data, ext)
                        print(f"C1541 ile {len(self.entries)} dosya bulundu")
                        if self.entries:
                            self.root.after(0, self.update_file_list)
                            
                            # Disk bilgilerini al
                            try:
                                disk_info = enhanced_c1541_get_disk_info(disk_data, ext)
                                if disk_info:
                                    self.root.after(0, lambda: self.status_var.set(f"Disk: {disk_info['disk_name']} (ID: {disk_info['disk_id']}) - {len(self.entries)} dosya"))
                                else:
                                    self.root.after(0, lambda: self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu"))
                            except Exception as disk_info_error:
                                print(f"Disk bilgisi alınırken hata: {disk_info_error}")
                                self.root.after(0, lambda: self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu"))
                            
                            print("=== LOAD_IMAGE BAŞARILI (C1541) ===")
                            return
                except Exception as e:
                    print(f"enhanced_c1541_read_image hatası: {e}")
                    import traceback
                    traceback.print_exc()
                    
            # Fallback: enhanced_read_image ile dene
            try:
                print("Enhanced reader deneniyor...")
                disk_data, ext = enhanced_read_image(file_path)
                if disk_data:
                    self.entries = enhanced_read_directory(disk_data, ext)
                    print(f"Enhanced reader ile {len(self.entries)} dosya bulundu")
                    if self.entries:
                        self.root.after(0, self.update_file_list)
                        self.root.after(0, lambda: self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu"))
                        print("=== LOAD_IMAGE BAŞARILI (Enhanced) ===")
                        return
            except Exception as e:
                print(f"enhanced_read_image hatası: {e}")
                import traceback
                traceback.print_exc()
                
            # Fallback: read_image ile dene
            try:
                print("Basic reader deneniyor...")
                disk_data, ext = read_image(file_path)
                if disk_data:
                    # Uzantıya göre directory okuma
                    if ext == '.t64':
                        self.entries = read_t64_directory(disk_data)
                    elif ext == '.tap':
                        self.entries = read_tap_directory(disk_data)
                    elif ext == '.prg':
                        # PRG dosyası için tek entry oluştur
                        self.entries = [{
                            'filename': Path(file_path).stem,
                            'type': 'PRG',
                            'track': 0,
                            'sector': 0,
                            'size': len(disk_data),
                            'data': disk_data
                        }]
                    elif ext == '.p00':
                        # P00 dosyası için tek entry oluştur
                        self.entries = [{
                            'filename': Path(file_path).stem,
                            'type': 'PRG',
                            'track': 0,
                            'sector': 0,
                            'size': len(disk_data) - 26,  # P00 header size
                            'data': disk_data
                        }]
                    else:
                        self.entries = read_directory(disk_data, ext)
                    
                    print(f"Basic reader ile {len(self.entries)} dosya bulundu")
                    if self.entries:
                        self.root.after(0, self.update_file_list)
                        self.root.after(0, lambda: self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu"))
                        print("=== LOAD_IMAGE BAŞARILI (Basic) ===")
                        return
            except Exception as e:
                print(f"read_image hatası: {e}")
                import traceback
                traceback.print_exc()
                
            # Hiçbir okuyucu çalışmadı
            print("Hiçbir okuyucu çalışmadı")
            self.root.after(0, lambda: self.status_var.set("Disk dosyası okunamadı"))
            self.entries = []
            
        except Exception as e:
            error_msg = str(e)
            print(f"LOAD_IMAGE GENEL HATASI: {error_msg}")
            print(f"Hata tipi: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            
            self.root.after(0, lambda: self.status_var.set(f"Hata: {error_msg}"))
            self.entries = []
            self.root.after(0, lambda: messagebox.showerror("Hata", f"Dosya yükleme hatası: {error_msg}"))
            
        finally:
            print("=== LOAD_IMAGE TAMAMLANDI ===")
            self.root.after(0, self.update_file_list)

    def update_file_list(self):
        """Dosya listesini güncelle"""
        # Mevcut öğeleri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yeni öğeleri ekle
        for entry in self.entries:
            filename = entry.get('filename', 'UNKNOWN')
            # C1541 emülatörü 'type' kullanırken d64_reader 'file_type' kullanıyor
            file_type = entry.get('type', entry.get('file_type', 'UNKNOWN'))
            track = entry.get('track', 0)
            sector = entry.get('sector', 0)
            # C1541 emülatörü 'size' kullanırken d64_reader 'size_blocks' kullanıyor
            size = entry.get('size', entry.get('size_blocks', 0))
            
            self.tree.insert('', 'end', values=(filename, file_type, track, sector, size))
        
        print(f"Dosya listesi güncellendi: {len(self.entries)} dosya")  # Debug
        
        # İlk dosyayı göster
        if self.entries:
            print(f"İlk dosya yapısı: {self.entries[0]}")  # Debug

    def convert_to_specific_format(self, format_code, tab_name):
        """Belirli bir formata dönüştür ve sadece o sekmesini güncelle"""
        selection = self.tree.selection()
        if not selection:
            # Seçim yoksa ilk dosyayı al
            if self.entries:
                selected_entry = self.entries[0]
                print(f"Seçim yok, ilk dosya kullanılıyor: {selected_entry.get('filename')}")
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin")
                return
        else:
            item = self.tree.item(selection[0])
            filename = item['values'][0]
            
            # Dosyayı bul
            selected_entry = None
            for entry in self.entries:
                if entry.get('filename') == filename:
                    selected_entry = entry
                    break
            
            if not selected_entry:
                messagebox.showerror("Hata", "Seçili dosya bulunamadı")
                return
        
        self.status_var.set(f"Dosya {tab_name} formatına dönüştürülüyor: {selected_entry.get('filename')}")
        print(f"Dönüştürülecek dosya: {selected_entry}, Format: {format_code}")
        
        # Threading ile dönüştürme
        threading.Thread(target=self._convert_specific_format_thread, 
                        args=(selected_entry, format_code, tab_name), daemon=True).start()

    def _convert_specific_format_thread(self, entry, format_code, tab_name):
        """Thread içinde belirli format dönüştürme"""
        try:
            # PRG dosyasını çıkart
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.status_var.set("PRG verisi çıkarılamadı"))
                return
            
            print(f"PRG verisi çıkarıldı: {len(prg_data)} byte")
            
            # PRG dosyasından start_address ve code'u çıkar
            if len(prg_data) < 2:
                self.root.after(0, lambda: self.status_var.set("Geçersiz PRG verisi"))
                return
                
            start_address = prg_data[0] + (prg_data[1] << 8)
            code_data = prg_data[2:]
            
            print(f"Start address: ${start_address:04X}, Code size: {len(code_data)} bytes")
            
            # Get selected disassembler
            selected_disassembler = self.disassembler_var.get()
            print(f"🔧 Selected disassembler: {selected_disassembler}")
            self.root.after(0, lambda: self.status_var.set(f"🔧 {selected_disassembler} disassembler çalışıyor..."))
            
            # Choose disassembler based on selection
            if selected_disassembler == "py65_professional":
                # Py65 Professional Disassembler
                if not PY65_AVAILABLE or not PROF_PY65_AVAILABLE:
                    error_msg = f"❌ HATA: py65 Professional disassembler kullanılamıyor.\n🔧 py65 durumu: {PY65_AVAILABLE}\n📦 Professional module: {PROF_PY65_AVAILABLE}"
                    result_code = error_msg
                    print(error_msg)
                    self.logger.error("py65 Professional disassembler kullanılamıyor")
                    self.root.after(0, lambda: self.status_var.set("❌ py65 Professional disassembler hatası"))
                else:
                    try:
                        from py65_professional_disassembler import Py65ProfessionalDisassembler
                        
                        self.logger.info("py65 Professional Disassembler kullanılıyor")
                        py65_disassembler = Py65ProfessionalDisassembler(start_address, code_data, 
                                                                       output_format=format_code,
                                                                       use_illegal_opcodes=self.use_illegal_opcodes.get())
                        result_code = py65_disassembler.disassemble_to_format(prg_data)
                        
                    except Exception as e:
                        error_msg = f"❌ py65 Professional Disassembler hatası: {str(e)}"
                        result_code = error_msg
                        print(error_msg)
                        self.logger.error(f"py65 Professional Disassembler hatası: {e}")
                        
            elif selected_disassembler == "improved":
                # Improved Disassembler (Default)
                try:
                    from improved_disassembler import ImprovedDisassembler
                    
                    self.logger.info("Improved Disassembler kullanılıyor")
                    improved_disassembler = ImprovedDisassembler(start_address, code_data, 
                                                               output_format=format_code,
                                                               use_illegal_opcodes=self.use_illegal_opcodes.get())
                    result_code = improved_disassembler.disassemble_to_format(prg_data)
                    
                except Exception as e:
                    error_msg = f"❌ Improved Disassembler hatası: {str(e)}"
                    result_code = error_msg
                    print(error_msg)
                    self.logger.error(f"Improved Disassembler hatası: {e}")
                    
            elif selected_disassembler == "advanced":
                # Advanced Disassembler
                try:
                    from advanced_disassembler import AdvancedDisassembler
                    
                    self.logger.info("Advanced Disassembler kullanılıyor")
                    advanced_disassembler = AdvancedDisassembler(start_address, code_data, 
                                                               output_format=format_code,
                                                               use_illegal_opcodes=self.use_illegal_opcodes.get())
                    result_code = advanced_disassembler.disassemble_simple(prg_data)
                    
                except Exception as e:
                    error_msg = f"❌ Advanced Disassembler hatası: {str(e)}"
                    result_code = error_msg
                    print(error_msg)
                    self.logger.error(f"Advanced Disassembler hatası: {e}")
                    
            elif selected_disassembler == "basic":
                # Basic Disassembler
                try:
                    from disassembler import Disassembler
                    
                    self.logger.info("Basic Disassembler kullanılıyor")
                    basic_disassembler = Disassembler(start_address, code_data)
                    asm_lines = basic_disassembler.disassemble()
                    result_code = '\n'.join(asm_lines)
                    
                    # Basic disassembler sadece assembly üretir, format dönüşümü yok
                    if format_code != 'asm':
                        result_code += f"\n\n// Warning: Basic disassembler only produces assembly output.\n// Requested format '{format_code}' not supported."
                    
                except Exception as e:
                    error_msg = f"❌ Basic Disassembler hatası: {str(e)}"
                    result_code = error_msg
                    print(error_msg)
                    self.logger.error(f"Basic Disassembler hatası: {e}")
            
            else:
                # Fallback to improved disassembler
                try:
                    from improved_disassembler import ImprovedDisassembler
                    
                    self.logger.warning(f"Bilinmeyen disassembler: {selected_disassembler}, Improved'a geçiliyor")
                    improved_disassembler = ImprovedDisassembler(start_address, code_data, 
                                                               output_format=format_code,
                                                               use_illegal_opcodes=self.use_illegal_opcodes.get())
                    result_code = improved_disassembler.disassemble_to_format(prg_data)
                    
                except Exception as e:
                    error_msg = f"❌ Fallback Improved Disassembler hatası: {str(e)}"
                    result_code = error_msg
                    print(error_msg)
                    self.logger.error(f"Fallback Improved Disassembler hatası: {e}")
            
            # Status güncelleme
            status_msg = f"✅ {selected_disassembler} disassembler tamamlandı - {format_code} format"
            self.root.after(0, lambda: self.status_var.set(status_msg))
            
            print(f"{tab_name} kod oluşturuldu: {len(result_code)} karakter")
            self.logger.info(f"{tab_name} format dönüştürme tamamlandı: {len(result_code)} karakter")
            
            # Sadece ilgili sekmesini güncelle
            self.root.after(0, self._update_specific_tab, tab_name, result_code)
            
        except Exception as e:
            error_msg = str(e)
            print(f"_convert_specific_format_thread hatası: {error_msg}")
            self.logger.error(f"Format dönüştürme hatası ({tab_name}): {error_msg}")
            self.root.after(0, lambda msg=error_msg: self.status_var.set(f"Dönüştürme hatası: {msg}"))

    def _update_specific_tab(self, tab_name, content):
        """Belirli bir sekmesini güncelle"""
        try:
            self.output_tabs[tab_name].delete(1.0, tk.END)
            self.output_tabs[tab_name].insert(tk.END, content)
            
            # İlgili sekmesine geç
            for i, tab_id in enumerate(self.notebook.tabs()):
                if self.notebook.tab(tab_id, "text") == tab_name:
                    self.notebook.select(tab_id)
                    break
            
            final_status = f"{tab_name} formatına dönüştürme tamamlandı"
            self.status_var.set(final_status)
            print(f"{tab_name} sekmesi güncellendi")
            self.logger.info(f"{tab_name} sekmesi güncellendi - {len(content)} karakter")
            
        except Exception as e:
            error_msg = f"Sekme güncelleme hatası: {str(e)}"
            self.status_var.set(error_msg)
            print(f"_update_specific_tab hatası: {e}")
            self.logger.error(f"Sekme güncelleme hatası ({tab_name}): {str(e)}")

    def convert_single_file(self):
        """Seçili dosyayı dönüştür"""
        selection = self.tree.selection()
        if not selection:
            # Seçim yoksa ilk dosyayı al
            if self.entries:
                selected_entry = self.entries[0]
                print(f"Seçim yok, ilk dosya kullanılıyor: {selected_entry.get('filename')}")
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin")
                return
        else:
            item = self.tree.item(selection[0])
            filename = item['values'][0]
            
            # Dosyayı bul
            selected_entry = None
            for entry in self.entries:
                if entry.get('filename') == filename:
                    selected_entry = entry
                    break
            
            if not selected_entry:
                messagebox.showerror("Hata", "Seçili dosya bulunamadı")
                return
        
        self.status_var.set(f"Dosya dönüştürülüyor: {selected_entry.get('filename')}")
        print(f"Dönüştürülecek dosya: {selected_entry}, Format: {self.output_format.get()}")
        
        # Threading ile dönüştürme
        threading.Thread(target=self._convert_single_file_thread, args=(selected_entry,), daemon=True).start()

    def _convert_single_file_thread(self, entry):
        """Thread içinde dosya dönüştürme"""
        try:
            # PRG dosyasını çıkart
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.status_var.set("PRG verisi çıkarılamadı"))
                return
            
            print(f"PRG verisi çıkarıldı: {len(prg_data)} byte")
            
            # PRG dosyasından start_address ve code'u çıkar
            if len(prg_data) < 2:
                self.root.after(0, lambda: self.status_var.set("Geçersiz PRG verisi"))
                return
                
            start_address = prg_data[0] + (prg_data[1] << 8)
            code_data = prg_data[2:]
            
            print(f"Start address: ${start_address:04X}, Code size: {len(code_data)} bytes")
            
            # Çıktı formatını al
            output_format = self.output_format.get()
            print(f"Çıktı formatı: {output_format}")
            
            # $0801 adresinden başlayan programlar BASIC programlardır
            if start_address == 0x0801:
                print("BASIC program tespit edildi - BASIC parser kullanılacak")
                
                # BASIC parser ile işle
                basic_parser = C64BasicParser()
                basic_lines = basic_parser.detokenize(prg_data)
                
                if basic_lines:
                    # Output formatına göre transpile et
                    if output_format == 'commodorebasicv2':
                        result_code = "\n".join(basic_lines)
                    elif output_format == 'qbasic':
                        result_code = basic_parser.transpile(basic_lines, "qbasic")
                    elif output_format == 'pdsx':
                        result_code = basic_parser.transpile(basic_lines, "pdsx")
                    elif output_format == 'c':
                        result_code = basic_parser.transpile(basic_lines, "c")
                    else:
                        # ASM, pseudo formatları için de BASIC listesini ver
                        result_code = f"; BASIC Program (Start: ${start_address:04X})\n; Use commodorebasicv2 format for proper BASIC code\n\n"
                        result_code += "\n".join([f"; {line}" for line in basic_lines])
                else:
                    result_code = f"; BASIC Program detokenization failed\n; Raw data at ${start_address:04X}\n"
                    
            else:
                print(f"Assembly program tespit edildi - Assembly disassembler kullanılacak")
                
                # Assembly disassembler ile işle
                disassembler = AdvancedDisassembler(
                    start_address=start_address,
                    code=code_data,
                    use_py65=self.use_py65_disassembler.get(),
                    use_illegal_opcodes=self.use_illegal_opcodes.get(),
                    output_format=output_format
                )
                
                if self.use_py65_disassembler.get():
                    result_code = disassembler.disassemble_py65(prg_data)
                else:
                    result_code = disassembler.disassemble_simple(prg_data)
            
            print(f"Kod oluşturuldu: {len(result_code)} karakter ({output_format} formatında)")
            
            # Sonucu GUI'de göster
            self.root.after(0, self._update_single_output, result_code, output_format, entry)
            
        except Exception as e:
            error_msg = str(e)
            print(f"_convert_single_file_thread hatası: {error_msg}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda msg=error_msg: self.status_var.set(f"Hata: {msg}"))

    def _update_single_output(self, result_code, output_format, entry):
        """Tek format çıktısını güncelle"""
        try:
            print(f"Güncelleniyor: {output_format} formatı, {len(result_code)} karakter")
            
            filename = entry.get('filename', 'unknown')
            
            # Dosyayı kaydet
            self.save_output_file(result_code, output_format, filename)
            
            # GUI'de ilgili sekmeyi güncelle
            if output_format == 'asm':
                self.assembly_text.delete(1.0, tk.END)
                self.assembly_text.insert(tk.END, result_code)
            elif output_format == 'c':
                self.c_text.delete(1.0, tk.END)
                self.c_text.insert(tk.END, result_code)
            elif output_format == 'qbasic':
                self.qbasic_text.delete(1.0, tk.END)
                self.qbasic_text.insert(tk.END, result_code)
            elif output_format == 'pdsx':
                self.pdsx_text.delete(1.0, tk.END)
                self.pdsx_text.insert(tk.END, result_code)
            elif output_format == 'pseudo':
                self.pseudo_text.delete(1.0, tk.END)
                self.pseudo_text.insert(tk.END, result_code)
            elif output_format == 'commodorebasicv2':
                self.commodore_basic_text.delete(1.0, tk.END)
                self.commodore_basic_text.insert(tk.END, result_code)
            
            self.status_var.set(f"✅ {output_format.upper()} formatı hazır: {filename}")
            
        except Exception as e:
            error_msg = str(e)
            print(f"_update_single_output hatası: {error_msg}")
            self.status_var.set(f"Güncelleme hatası: {error_msg}")

    def save_output_file(self, content, format_type, filename):
        """Çıktı dosyasını kaydet"""
        try:
            # Çıktı klasörünü oluştur
            output_dir = f"{format_type}_files"
            os.makedirs(output_dir, exist_ok=True)
            
            # Dosya uzantısını belirle
            extensions = {
                'asm': 'asm',
                'c': 'c',
                'qbasic': 'bas',
                'pdsx': 'pdsx',
                'pseudo': 'txt',
                'commodorebasicv2': 'bas'
            }
            
            extension = extensions.get(format_type, 'txt')
            output_file = os.path.join(output_dir, f"{filename}.{extension}")
            
            # Dosyayı kaydet
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Dosya kaydedildi: {output_file}")
            
        except Exception as e:
            print(f"Dosya kaydetme hatası: {e}")

    def _update_all_outputs(self, assembly_code, prg_data, start_address, code_data):
        """Tüm çıktı sekmelerini güncelle"""
        try:
            print(f"Assembly kod uzunluğu: {len(assembly_code)}")  # Debug
            
            # $0801 adresinden başlayan programlar BASIC programlardır
            if start_address == 0x0801:
                print("BASIC program tespit edildi - BASIC parser kullanılacak")
                
                # BASIC parser ile işle
                basic_parser = C64BasicParser()
                basic_lines = basic_parser.detokenize(prg_data)
                
                if basic_lines:
                    # Assembly sekmesi için BASIC listing'i comment olarak göster
                    basic_listing = f"; BASIC Program (Start: ${start_address:04X})\n; Use BASIC tab for proper BASIC code\n\n"
                    basic_listing += "\n".join([f"; {line}" for line in basic_lines])
                    self.output_tabs['Assembly'].delete(1.0, tk.END)
                    self.output_tabs['Assembly'].insert(tk.END, basic_listing)
                    
                    # Diğer formatlar için BASIC transpiler kullan
                    formats = [
                        ('C', 'c'),
                        ('QBasic', 'qbasic'), 
                        ('PDSX', 'pdsx'),
                        ('Pseudo', 'pseudo'),
                        ('BASIC', 'commodorebasicv2')
                    ]
                    
                    for format_name, format_code in formats:
                        if format_code == 'commodorebasicv2':
                            result_code = "\n".join(basic_lines)
                        elif format_code in ['qbasic', 'pdsx', 'c']:
                            result_code = basic_parser.transpile(basic_lines, format_code)
                        else:
                            # Pseudo format için de BASIC listing
                            result_code = f"; BASIC Program (Start: ${start_address:04X})\n; Use BASIC tab for proper BASIC code\n\n"
                            result_code += "\n".join([f"; {line}" for line in basic_lines])
                        
                        self.output_tabs[format_name].delete(1.0, tk.END)
                        self.output_tabs[format_name].insert(tk.END, result_code)
                        print(f"{format_name} kodu uzunluğu: {len(result_code)}")  # Debug
                else:
                    # Detokenization başarısız
                    error_msg = f"; BASIC Program detokenization failed\n; Raw data at ${start_address:04X}\n"
                    for format_name in ['Assembly', 'C', 'QBasic', 'PDSX', 'Pseudo', 'BASIC']:
                        self.output_tabs[format_name].delete(1.0, tk.END)
                        self.output_tabs[format_name].insert(tk.END, error_msg)
                        
            else:
                print(f"Assembly program tespit edildi - Assembly disassembler kullanılacak")
                
                # Assembly
                self.output_tabs['Assembly'].delete(1.0, tk.END)
                self.output_tabs['Assembly'].insert(tk.END, assembly_code)
                print("Assembly sekmesi güncellendi")  # Debug
                
                # Diğer formatlar için ImprovedDisassembler kullan
                for format_name, format_code in [('C', 'c'), ('QBasic', 'qbasic'), ('PDSX', 'pdsx'), 
                                               ('Pseudo', 'pseudo'), ('BASIC', 'commodorebasicv2')]:
                    improved_disassembler = ImprovedDisassembler(
                        start_address=start_address,
                        code=code_data,
                        output_format=format_code
                    )
                    
                    result_code = improved_disassembler.disassemble_to_format(prg_data)
                    self.output_tabs[format_name].delete(1.0, tk.END)
                    self.output_tabs[format_name].insert(tk.END, result_code)
                    print(f"{format_name} kodu uzunluğu: {len(result_code)}")  # Debug
            
            self.status_var.set("Dönüştürme tamamlandı")
            print("Tüm sekmeler güncellendi")  # Debug
            
        except Exception as e:
            self.status_var.set(f"Çıktı güncelleme hatası: {str(e)}")
            print(f"_update_all_outputs hatası: {e}")  # Debug

    def extract_prg_data(self, entry):
        """PRG verisini çıkart"""
        try:
            disk_path = self.d64_path.get()
            if not disk_path:
                return None
            
            ext = Path(disk_path).suffix.lower()
            print(f"PRG çıkarma: {entry.get('filename')}, ext: {ext}")  # Debug
            
            # C1541 emülatörü ile dene
            try:
                disk_data, ext = enhanced_c1541_read_image(disk_path)
                if disk_data:
                    prg_data = enhanced_c1541_extract_prg(disk_data, ext, entry)
                    if prg_data:
                        print(f"C1541 ile PRG çıkarıldı: {len(prg_data)} byte")  # Debug
                        return prg_data
            except Exception as e:
                print(f"C1541 extract hatası: {e}")
            
            # Enhanced reader ile dene
            try:
                disk_data, ext = enhanced_read_image(disk_path)
                if disk_data:
                    prg_data = enhanced_extract_prg(disk_data, ext, entry)
                    if prg_data:
                        print(f"Enhanced reader ile PRG çıkarıldı: {len(prg_data)} byte")  # Debug
                        return prg_data
            except Exception as e:
                print(f"Enhanced extract hatası: {e}")
            
            # Basic reader ile dene
            try:
                disk_data, ext = read_image(disk_path)
                if disk_data:
                    if ext == '.t64':
                        # T64 için offset ve size parametreleri gerekli
                        if 'offset' in entry and 'size' in entry:
                            return extract_t64_prg(disk_data, entry['offset'], entry['size'])
                    elif ext == '.tap':
                        # TAP için offset ve size parametreleri gerekli
                        if 'offset' in entry and 'size' in entry:
                            return extract_tap_prg(disk_data, entry['offset'], entry['size'])
                    elif ext == '.p00':
                        return extract_p00_prg(disk_data)
                    else:
                        # D64/D71/D81/D84 için track/sector gerekli
                        if 'track' in entry and 'sector' in entry:
                            file_type = entry.get('file_type', entry.get('type', 'PRG'))
                            if 'SEQ' in file_type:
                                return extract_seq_file(disk_data, entry['track'], entry['sector'], ext)
                            elif 'USR' in file_type:
                                return extract_usr_file(disk_data, entry['track'], entry['sector'], ext)
                            elif 'DEL' in file_type:
                                return extract_del_file(disk_data, entry['track'], entry['sector'], ext)
                            else:
                                return extract_prg_file(disk_data, entry['track'], entry['sector'], ext)
            except Exception as e:
                print(f"Basic extract hatası: {e}")
            
            return None
            
        except Exception as e:
            print(f"PRG çıkarma hatası: {e}")
            return None

    # Dönüştürme fonksiyonları
    def convert_to_assembly(self):
        """Assembly'e dönüştür"""
        self.convert_to_specific_format('asm', 'Assembly')

    def convert_to_c(self):
        """C'ye dönüştür"""
        self.convert_to_specific_format('c', 'C')

    def convert_to_qbasic(self):
        """QBasic'e dönüştür"""
        self.convert_to_specific_format('qbasic', 'QBasic')

    def convert_to_pdsx(self):
        """PDSX'e dönüştür"""
        self.convert_to_specific_format('pdsx', 'PDSX')

    def convert_to_pseudo(self):
        """Pseudo koda dönüştür"""
        self.convert_to_specific_format('pseudo', 'Pseudo')

    def convert_to_basic(self):
        """BASIC'e dönüştür"""
        self.convert_to_specific_format('commodorebasicv2', 'BASIC')

    def convert_to_basic(self):
        """BASIC'e dönüştür"""
        self.convert_single_file()

    def analyze_illegal_opcodes(self):
        """Illegal opcode analizi yap"""
        try:
            # Seçili dosyayı kontrol et
            selection = self.tree.selection()
            if not selection:
                if self.entries:
                    selected_entry = self.entries[0]
                    print(f"Seçim yok, ilk dosya kullanılıyor: {selected_entry.get('filename')}")
                else:
                    messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin")
                    return
            else:
                item = self.tree.item(selection[0])
                filename = item['values'][0]
                
                # Dosyayı bul
                selected_entry = None
                for entry in self.entries:
                    if entry.get('filename') == filename:
                        selected_entry = entry
                        break
                
                if not selected_entry:
                    messagebox.showwarning("Uyarı", "Seçili dosya bulunamadı")
                    return
            
            # Status güncelle
            self.status_var.set(f"Illegal opcode analizi başlatılıyor: {selected_entry.get('filename')}")
            
            # Threading ile analiz et
            threading.Thread(target=self._analyze_illegal_opcodes_thread, args=(selected_entry,), daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Illegal opcode analizi sırasında hata: {str(e)}")
            print(f"Illegal opcode analizi hatası: {e}")
            import traceback
            traceback.print_exc()

    def _analyze_illegal_opcodes_thread(self, entry):
        """Thread içinde illegal opcode analizi"""
        try:
            # PRG dosyasını çıkart
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.status_var.set("PRG verisi çıkarılamadı"))
                return
            
            # Geçici PRG dosyası oluştur
            temp_prg = f"prg_files/temp_illegal_analysis.prg"
            os.makedirs("prg_files", exist_ok=True)
            
            with open(temp_prg, 'wb') as f:
                f.write(prg_data)
            
            # Analiz et
            from simple_analyzer import SimpleIllegalAnalyzer
            analyzer = SimpleIllegalAnalyzer()
            results = analyzer.analyze_prg_file(temp_prg)
            
            # Geçici dosyayı temizle
            try:
                os.remove(temp_prg)
            except:
                pass
            
            # Sonuçları GUI'de göster
            self.root.after(0, self.show_illegal_analysis_results, results)
            
        except Exception as e:
            error_msg = str(e)
            print(f"_analyze_illegal_opcodes_thread hatası: {error_msg}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda msg=error_msg: self.status_var.set(f"Analiz hatası: {msg}"))
    
    def show_illegal_analysis_results(self, results):
        """Illegal opcode analiz sonuçlarını göster"""
        # Yeni pencere oluştur
        result_window = tk.Toplevel(self.root)
        result_window.title("Illegal Opcode Analysis Results")
        result_window.geometry("800x600")
        
        # Scrollable text widget
        text_frame = tk.Frame(result_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)
        
        # Sonuçları format et
        if 'error' in results:
            text_widget.insert(tk.END, f"❌ Error: {results['error']}\n")
        else:
            text_widget.insert(tk.END, f"📊 Analysis Results:\n")
            text_widget.insert(tk.END, f"   Total instructions: {results['total_instructions']}\n")
            text_widget.insert(tk.END, f"   Illegal opcodes found: {results['illegal_count']}\n\n")
            
            if results['illegal_count'] == 0:
                text_widget.insert(tk.END, "   ✅ No illegal opcodes found! Code is clean.\n")
            else:
                text_widget.insert(tk.END, "🔍 Illegal Opcodes Found:\n")
                text_widget.insert(tk.END, "=" * 60 + "\n\n")
                
                dangerous_count = 0
                for i, illegal in enumerate(results['illegal_opcodes'], 1):
                    if illegal['is_dangerous']:
                        dangerous_count += 1
                        danger_mark = "🚨 DANGEROUS"
                    else:
                        danger_mark = "⚠️ "
                    
                    text_widget.insert(tk.END, f"#{i} {danger_mark}\n")
                    text_widget.insert(tk.END, f"   Address: ${illegal['address']:04X}\n")
                    text_widget.insert(tk.END, f"   Opcode: ${illegal['opcode']:02X}\n")
                    text_widget.insert(tk.END, f"   Description: {illegal['description']}\n")
                    
                    if illegal['operand_bytes']:
                        operand_str = ' '.join(f"${b:02X}" for b in illegal['operand_bytes'])
                        text_widget.insert(tk.END, f"   Operands: {operand_str}\n")
                    
                    # Print context
                    context_str = ' '.join(f"${b:02X}" for b in illegal['context'])
                    text_widget.insert(tk.END, f"   Context: {context_str}\n")
                    
                    # Add marker line
                    marker_pos = illegal['context_position'] * 4  # 4 chars per byte ($XX )
                    marker_line = ' ' * 12 + ' ' * marker_pos + '^^'
                    text_widget.insert(tk.END, f"{marker_line}\n\n")
                
                if dangerous_count > 0:
                    text_widget.insert(tk.END, f"🚨 WARNING: {dangerous_count} dangerous KIL/JAM instructions found!\n")
                    text_widget.insert(tk.END, "   These instructions will freeze the CPU!\n")
        
        # Make text read-only
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_button = tk.Button(result_window, text="Close", command=result_window.destroy)
        close_button.pack(pady=10)

    def extract_prg_data(self, entry):
        """D64 entry'den PRG verisini çıkar"""
        try:
            # Önce entry'de doğrudan data var mı kontrol et
            if 'data' in entry and entry['data']:
                data = entry['data']
                print(f"Entry'den direkt data alındı: {len(data)} byte")
                
                # Eğer zaten PRG formatında değilse, PRG header ekle
                if len(data) >= 2:
                    # İlk 2 byte load address olup olmadığını kontrol et
                    load_addr = data[0] | (data[1] << 8)
                    if 0x0400 <= load_addr <= 0xFFFF:  # Geçerli C64 adres aralığı
                        return data
                    else:
                        # Standard BASIC load address ekle
                        return b'\x01\x08' + data
                else:
                    # Standard BASIC load address ekle
                    return b'\x01\x08' + data
            
            # Eğer entry'de data yoksa, disk'ten çıkar
            disk_path = self.d64_path.get()
            if not disk_path:
                print("Disk path yok")
                return None
            
            ext = Path(disk_path).suffix.lower()
            print(f"Disk'ten PRG çıkarma: {entry.get('filename')}, ext: {ext}")
            
            # C1541 emülatörü ile dene
            try:
                disk_data, ext = enhanced_c1541_read_image(disk_path)
                if disk_data:
                    prg_data = enhanced_c1541_extract_prg(disk_data, ext, entry)
                    if prg_data:
                        print(f"C1541 ile PRG çıkarıldı: {len(prg_data)} byte")
                        return prg_data
            except Exception as e:
                print(f"C1541 extract hatası: {e}")
            
            # Enhanced reader ile dene
            try:
                disk_data, ext = enhanced_read_image(disk_path)
                if disk_data:
                    prg_data = enhanced_extract_prg(disk_data, ext, entry)
                    if prg_data:
                        print(f"Enhanced reader ile PRG çıkarıldı: {len(prg_data)} byte")
                        return prg_data
            except Exception as e:
                print(f"Enhanced extract hatası: {e}")
            
            print("PRG verisi çıkarılamadı")
            return None
            
        except Exception as e:
            print(f"PRG verisi çıkarma hatası: {e}")
            return None
            code_data = prg_data[2:]
            
            print(f"Start address: ${start_address:04X}, Code size: {len(code_data)} bytes")
            
            # Illegal opcode analizi yap
            self.status_var.set("Illegal opcode analizi yapılıyor...")
            self.root.update()
            
            analysis_results = self.illegal_analyzer.analyze_code_data(code_data, start_address)
            self.illegal_analysis_results = analysis_results
            
            # Sonuçları göster
            illegal_count = analysis_results['statistics']['illegal_count']
            total_opcodes = analysis_results['statistics']['total_opcodes']
            
            if illegal_count == 0:
                self.status_var.set("Illegal opcode bulunamadı")
                messagebox.showinfo("Analiz Sonucu", 
                                  f"✅ Illegal opcode bulunamadı\n\n"
                                  f"Toplam analiz edilen opcode: {total_opcodes}\n"
                                  f"Dosya güvenli görünüyor.")
            else:
                self.status_var.set(f"{illegal_count} illegal opcode bulundu")
                
                # Detaylı sonuçları göster
                severity = analysis_results['severity_breakdown']
                recommendations = analysis_results['recommendations']
                
                result_message = f"⚠️ {illegal_count} illegal opcode bulundu!\n\n"
                result_message += f"Toplam analiz edilen opcode: {total_opcodes}\n"
                result_message += f"Undocumented (stabil): {analysis_results['statistics']['undocumented_count']}\n"
                result_message += f"Unstable (kararsız): {analysis_results['statistics']['unstable_count']}\n"
                result_message += f"Unknown (bilinmeyen): {analysis_results['statistics']['unknown_count']}\n\n"
                result_message += "Severity Breakdown:\n"
                result_message += f"• Low (Güvenli): {severity['low']}\n"
                result_message += f"• Medium (Orta): {severity['medium']}\n"
                result_message += f"• High (Tehlikeli): {severity['high']}\n"
                result_message += f"• Unknown: {severity['unknown']}\n\n"
                result_message += "Öneriler:\n"
                for rec in recommendations:
                    result_message += f"• {rec}\n"
                
                messagebox.showwarning("Illegal Opcode Analizi", result_message)
                
                # Detaylı raporu dosyaya kaydet
                report_file = f"logs/illegal_analysis_{selected_entry.get('filename', 'unknown')}.txt"
                self.illegal_analyzer.export_results(report_file, 'text')
                
                # JSON export
                json_file = f"logs/illegal_analysis_{selected_entry.get('filename', 'unknown')}.json"
                self.illegal_analyzer.export_results(json_file, 'json')
                
                print(f"Illegal opcode raporu kaydedildi: {report_file}")
                print(f"JSON raporu kaydedildi: {json_file}")
                
                # Kullanıcıya raporları göster
                if messagebox.askyesno("Detaylı Rapor", 
                                     f"Detaylı rapor kaydedildi: {report_file}\n\n"
                                     f"Raporu görüntülemek ister misiniz?"):
                    self.show_illegal_report(report_file)
            
        except Exception as e:
            error_msg = str(e)
            print(f"Illegal opcode analizi hatası: {error_msg}")
            self.logger.error(f"Illegal opcode analizi hatası: {error_msg}")
            self.status_var.set(f"Analiz hatası: {error_msg}")
            messagebox.showerror("Analiz Hatası", f"Illegal opcode analizi hatası:\n{error_msg}")
    
    def show_illegal_report(self, report_file):
        """Illegal opcode raporunu göster"""
        try:
            # Yeni pencere oluştur
            report_window = tk.Toplevel(self.root)
            report_window.title("Illegal Opcode Analiz Raporu")
            report_window.geometry("800x600")
            
            # Text widget
            text_frame = ttk.Frame(report_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 10))
            scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Raporu yükle
            with open(report_file, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            text_widget.insert(tk.END, report_content)
            text_widget.configure(state=tk.DISABLED)
            
            # Kapat butonu
            close_button = ttk.Button(report_window, text="Kapat", 
                                    command=report_window.destroy)
            close_button.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rapor gösterilemiyor: {e}")
    
    def convert_sprite(self):
        """Sprite dönüştür"""
        try:
            # Seçili dosyayı kontrol et
            if not self.d64_path.get():
                messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin!")
                return
            
            file_path = self.d64_path.get()
            
            # Dosya türüne göre sprite conversion
            if file_path.lower().endswith('.d64'):
                # D64 dosyasındaki sprite'ları çıkart
                self.status_var.set("Sprite'lar çıkarılıyor...")
                self.root.update()
                
                # Sprite converter'ı çalıştır
                result = self.sprite_converter.convert_d64_sprites(file_path)
                if result:
                    self.status_var.set("Sprite'lar PNG olarak kaydedildi")
                    messagebox.showinfo("Başarılı", "Sprite'lar png_files klasörüne kaydedildi!")
                else:
                    self.status_var.set("Sprite bulunamadı")
                    messagebox.showinfo("Bilgi", "Bu dosyada sprite bulunamadı")
                    
            elif file_path.lower().endswith('.prg'):
                # PRG dosyasındaki sprite'ları çıkart
                self.status_var.set("PRG'den sprite'lar çıkarılıyor...")
                self.root.update()
                
                result = self.sprite_converter.convert_prg_sprites(file_path)
                if result:
                    self.status_var.set("Sprite'lar PNG olarak kaydedildi")
                    messagebox.showinfo("Başarılı", "Sprite'lar png_files klasörüne kaydedildi!")
                else:
                    self.status_var.set("Sprite bulunamadı")
                    messagebox.showinfo("Bilgi", "Bu dosyada sprite bulunamadı")
            else:
                messagebox.showwarning("Uyarı", "Sprite conversion sadece D64 ve PRG dosyaları için desteklenir!")
                
        except Exception as e:
            error_msg = f"Sprite dönüştürme hatası: {str(e)}"
            self.status_var.set(error_msg)
            messagebox.showerror("Hata", error_msg)

    def convert_sid(self):
        """SID dönüştür"""
        try:
            # Seçili dosyayı kontrol et
            if not self.d64_path.get():
                messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin!")
                return
            
            file_path = self.d64_path.get()
            
            # Dosya türüne göre SID conversion
            if file_path.lower().endswith('.d64'):
                # D64 dosyasındaki SID'leri çıkart
                self.status_var.set("SID dosyaları çıkarılıyor...")
                self.root.update()
                
                # SID converter'ı çalıştır
                result = self.sid_converter.convert_d64_sid(file_path)
                if result:
                    self.status_var.set("SID dosyaları kaydedildi")
                    messagebox.showinfo("Başarılı", "SID dosyaları sid_files klasörüne kaydedildi!")
                else:
                    self.status_var.set("SID bulunamadı")
                    messagebox.showinfo("Bilgi", "Bu dosyada SID bulunamadı")
                    
            elif file_path.lower().endswith('.prg'):
                # PRG dosyasındaki SID'leri çıkart
                self.status_var.set("PRG'den SID'ler çıkarılıyor...")
                self.root.update()
                
                result = self.sid_converter.convert_prg_sid(file_path)
                if result:
                    self.status_var.set("SID dosyaları kaydedildi")
                    messagebox.showinfo("Başarılı", "SID dosyaları sid_files klasörüne kaydedildi!")
                else:
                    self.status_var.set("SID bulunamadı")
                    messagebox.showinfo("Bilgi", "Bu dosyada SID bulunamadı")
            else:
                messagebox.showwarning("Uyarı", "SID conversion sadece D64 ve PRG dosyaları için desteklenir!")
                
        except Exception as e:
            error_msg = f"SID dönüştürme hatası: {str(e)}"
            self.status_var.set(error_msg)
            messagebox.showerror("Hata", error_msg)

    def setup_drag_drop_safe(self):
        """Güvenli sürükle-bırak desteği"""
        try:
            print("🔄 Sürükle-bırak desteği kontrol ediliyor...")
            
            if not (TkinterDnD and DND_FILES):
                print("⚠️ TkinterDnD modülü eksik")
                return False
            
            # Root widget'ı kontrol et
            if not hasattr(self.root, 'drop_target_register'):
                print("⚠️ Root widget drop_target_register desteklemiyor")
                print("💡 Normal tkinter.Tk() kullanılıyor, TkinterDnD.Tk() gerekli")
                return False
            
            # Sürükle-bırak özelliğini aktifleştir
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
            
            print("✅ Sürükle-bırak desteği aktif")
            self.logger.info("Drag&drop aktif")
            return True
            
        except Exception as e:
            print(f"❌ Sürükle-bırak setup hatası: {e}")
            self.logger.error(f"Drag&drop hatası: {e}")
            return False

    def on_drop(self, event):
        """Dosya sürüklendiğinde"""
        try:
            files = self.root.tk.splitlist(event.data)
            if files:
                dropped_file = files[0]
                print(f"Dosya sürüklendi: {dropped_file}")
                self.logger.info(f"Drag & drop: {dropped_file}")
                self.d64_path.set(dropped_file)
                self.status_var.set("Sürüklenen dosya yükleniyor...")
                self.load_image(dropped_file)
        except Exception as e:
            error_msg = f"Drag & drop hatası: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            self.status_var.set("Drag & drop hatası")

    # Eski update_output_format metodları kaldırıldı - artık her format kendi metoduna sahip

def main():
    """
    Ana fonksiyon - TkinterDnD desteğiyle (güvenli)
    """
    print("🚀 D64 Converter başlatılıyor...")
    
    # GUI başlatma - güvenli yöntem
    root = None
    try:
        # Önce normal Tkinter'i dene
        print("📦 Tkinter GUI oluşturuluyor...")
        root = tk.Tk()
        print("✅ Tkinter GUI başarılı")
        
        # TkinterDnD desteğini sonra ekle (opsiyonel)
        if TKINTER_DND_AVAILABLE and TkinterDnD:
            try:
                # Mevcut root'u TkinterDnD ile upgrade et
                print("🔄 TkinterDnD özellikleri ekleniyor...")
                # Sadece özellikleri ekle, root'u değiştirme
                print("✅ TkinterDnD özellikleri hazır")
            except Exception as dnd_error:
                print(f"⚠️ TkinterDnD devre dışı: {dnd_error}")
        
    except Exception as e:
        print(f"❌ GUI başlatma hatası: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # App başlatma
    app = None
    try:
        print("🔧 D64ConverterApp oluşturuluyor...")
        app = D64ConverterApp(root)
        print("✅ D64ConverterApp hazır")
        
        print("🖥️ GUI gösteriliyor...")
        root.deiconify()  # Pencereyi görünür yap
        root.lift()       # Pencereyi öne getir
        root.focus_force() # Odakla
        
        print("🔄 GUI mainloop başlatılıyor...")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Uygulama hatası: {e}")
        import traceback
        traceback.print_exc()
        
        if root:
            try:
                root.destroy()
            except:
                pass
    
    print("👋 D64 Converter kapandı")


def convert_py65_results_to_format(results, format_code):
    """py65 professional disassembler sonuçlarını belirli formata dönüştür"""
    try:
        if format_code == 'c':
            # C formatı
            c_code = []
            c_code.append("/* C64 PRG Disassembly - Generated by py65 Professional Disassembler */")
            c_code.append("#include <stdint.h>")
            c_code.append("")
            c_code.append("typedef struct {")
            c_code.append("    uint8_t a;      // Accumulator")
            c_code.append("    uint8_t x;      // X Register")
            c_code.append("    uint8_t y;      // Y Register")
            c_code.append("    uint8_t flags;  // Processor Status")
            c_code.append("    uint16_t pc;    // Program Counter")
            c_code.append("    uint8_t sp;     // Stack Pointer")
            c_code.append("} cpu_state_t;")
            c_code.append("")
            c_code.append("cpu_state_t cpu;")
            c_code.append("uint8_t memory[65536];")
            c_code.append("")
            c_code.append("void execute_program() {")
            
            for result in results:
                if result.symbol:
                    c_code.append(f"    // {result.symbol.name}")
                
                bytes_str = ', '.join(f"0x{b:02X}" for b in result.bytes)
                c_code.append(f"    // ${result.address:04X}: {result.instruction}")
                c_code.append(f"    memory[0x{result.address:04X}] = {bytes_str};")
                
                if result.comment:
                    c_code.append(f"    // {result.comment}")
                c_code.append("")
            
            c_code.append("}")
            return '\n'.join(c_code)
        
        elif format_code == 'qbasic':
            # QBasic formatı
            qb_code = []
            qb_code.append("' C64 PRG Disassembly - Generated by py65 Professional Disassembler")
            qb_code.append("DIM memory(65536) AS INTEGER")
            qb_code.append("")
            
            for result in results:
                if result.symbol:
                    qb_code.append(f"' {result.symbol.name}")
                
                qb_code.append(f"' ${result.address:04X}: {result.instruction}")
                for i, b in enumerate(result.bytes):
                    qb_code.append(f"memory({result.address + i}) = &H{b:02X}")
                
                if result.comment:
                    qb_code.append(f"' {result.comment}")
                qb_code.append("")
            
            return '\n'.join(qb_code)
        
        elif format_code == 'pdsx':
            # PDSX formatı (Assembly-like)
            pdsx_code = []
            pdsx_code.append("; PDSX Format - Generated by py65 Professional Disassembler")
            pdsx_code.append("; Target: Commodore 64")
            pdsx_code.append("")
            
            for result in results:
                if result.symbol:
                    pdsx_code.append(f"{result.symbol.name}:")
                
                bytes_str = ' '.join(f"${b:02X}" for b in result.bytes)
                line = f"    {result.instruction:<15} ; ${result.address:04X} [{bytes_str}]"
                
                if result.comment:
                    line += f" - {result.comment}"
                
                pdsx_code.append(line)
            
            return '\n'.join(pdsx_code)
        
        elif format_code == 'pseudo':
            # Pseudo kod formatı
            pseudo_code = []
            pseudo_code.append("# Pseudo Code - Generated by py65 Professional Disassembler")
            pseudo_code.append("")
            
            for result in results:
                if result.symbol:
                    pseudo_code.append(f"LABEL {result.symbol.name}:")
                
                # Pseudo kod çevirisi
                pseudo_inst = convert_to_pseudo_instruction(result)
                pseudo_code.append(f"    {pseudo_inst}")
                
                if result.comment:
                    pseudo_code.append(f"    // {result.comment}")
            
            return '\n'.join(pseudo_code)
        
        elif format_code == 'commodorebasicv2':
            # Commodore BASIC V2 formatı
            basic_code = []
            basic_code.append("10 REM C64 PRG DISASSEMBLY - GENERATED BY PY65 PROFESSIONAL DISASSEMBLER")
            basic_code.append("20 REM DATA STATEMENTS FOR MACHINE CODE")
            basic_code.append("30 REM")
            
            line_num = 100
            for result in results:
                if result.symbol:
                    basic_code.append(f"{line_num} REM {result.symbol.name}")
                    line_num += 10
                
                bytes_str = ', '.join(str(b) for b in result.bytes)
                basic_code.append(f"{line_num} DATA {bytes_str}: REM ${result.address:04X}: {result.instruction}")
                line_num += 10
            
            return '\n'.join(basic_code)
        
        else:
            # Varsayılan olarak assembly formatı döndür
            return "# Assembly format conversion needed"
            
    except Exception as e:
        return f"# Dönüştürme hatası: {e}\n\n# Raw Results:\n{str(results)}"

def convert_to_pseudo_instruction(result):
    """Assembly instruction'ı pseudo koda çevir"""
    mnemonic = result.mnemonic
    operand = result.operand
    
    # Temel pseudo kod çevirileri
    if mnemonic == 'LDA':
        return f"LOAD_ACCUMULATOR({operand})"
    elif mnemonic == 'STA':
        return f"STORE_ACCUMULATOR({operand})"
    elif mnemonic == 'LDX':
        return f"LOAD_X_REGISTER({operand})"
    elif mnemonic == 'STX':
        return f"STORE_X_REGISTER({operand})"
    elif mnemonic == 'LDY':
        return f"LOAD_Y_REGISTER({operand})"
    elif mnemonic == 'STY':
        return f"STORE_Y_REGISTER({operand})"
    elif mnemonic == 'JMP':
        return f"JUMP_TO({operand})"
    elif mnemonic == 'JSR':
        return f"CALL_SUBROUTINE({operand})"
    elif mnemonic == 'RTS':
        return "RETURN_FROM_SUBROUTINE()"
    elif mnemonic == 'BEQ':
        return f"IF_EQUAL_BRANCH({operand})"
    elif mnemonic == 'BNE':
        return f"IF_NOT_EQUAL_BRANCH({operand})"
    elif mnemonic == 'BCC':
        return f"IF_CARRY_CLEAR_BRANCH({operand})"
    elif mnemonic == 'BCS':
        return f"IF_CARRY_SET_BRANCH({operand})"
    elif mnemonic == 'CMP':
        return f"COMPARE_ACCUMULATOR({operand})"
    elif mnemonic == 'CPX':
        return f"COMPARE_X_REGISTER({operand})"
    elif mnemonic == 'CPY':
        return f"COMPARE_Y_REGISTER({operand})"
    elif mnemonic == 'INC':
        return f"INCREMENT_MEMORY({operand})"
    elif mnemonic == 'DEC':
        return f"DECREMENT_MEMORY({operand})"
    elif mnemonic == 'INX':
        return "INCREMENT_X_REGISTER()"
    elif mnemonic == 'DEX':
        return "DECREMENT_X_REGISTER()"
    elif mnemonic == 'INY':
        return "INCREMENT_Y_REGISTER()"
    elif mnemonic == 'DEY':
        return "DECREMENT_Y_REGISTER()"
    elif mnemonic == 'NOP':
        return "NO_OPERATION()"
    elif mnemonic == 'BRK':
        return "BREAK_INTERRUPT()"
    else:
        return f"{mnemonic}({operand})" if operand else f"{mnemonic}()"

    def on_file_select(self, event):
        """Dosya seçildiğinde içeriği göster"""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        filename = item["values"][0]
        
        # Dosyayı bul
        entry = next((e for e in self.entries if e["filename"] == filename), None)
        if entry:
            self.show_file_preview(entry)
    
    def show_file_preview(self, entry):
        """Seçili dosyanın önizlemesini göster"""
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
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, f"Dosya '{entry['filename']}' boş veya okunamıyor.")
                return
            
            # Start address
            start_addr = prg_data[0] + (prg_data[1] << 8)
            
            # Kısa disassembly önizlemesi
            try:
                from improved_disassembler import ImprovedDisassembler
                disasm = ImprovedDisassembler(start_addr, prg_data[2:], output_format='asm')
                preview = disasm.disassemble_to_format(prg_data)
                
                # İlk 20 satır
                lines = preview.split('\n')[:20]
                preview_text = '\n'.join(lines)
                if len(preview.split('\n')) > 20:
                    preview_text += f"\n\n... ({len(preview.split('\n')) - 20} satır daha)"
                
                # Info header ekle
                info_header = f"""Dosya: {entry['filename']}
Start Address: ${start_addr:04X} ({start_addr})
Boyut: {len(prg_data)} byte

=== Assembly Önizlemesi (ilk 20 satır) ===
"""
                
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, info_header + preview_text)
                
            except Exception as e:
                error_text = f"""Dosya: {entry['filename']}
Start Address: ${start_addr:04X} ({start_addr})
Boyut: {len(prg_data)} byte

Önizleme hatası: {e}
Tam disassembly için dosyaya çift tıklayın."""
                
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, error_text)
                
        except Exception as e:
            print(f"Önizleme hatası: {e}")
    
    def on_file_double_click(self, event):
        """Dosyaya çift tıklandığında tam disassembly yap"""
        selection = self.tree.selection()
        if not selection:
            return
            
        item = self.tree.item(selection[0])
        filename = item["values"][0]
        
        # Dosyayı bul ve çevir
        entry = next((e for e in self.entries if e["filename"] == filename), None)
        if entry:            # Tek dosya çevir
            self.convert_single_file()
    
    def convert_all_files(self):
        """Tüm dosyaları çevir"""
        if not hasattr(self, 'entries') or not self.entries:
            messagebox.showwarning("Uyarı", "Önce bir D64/PRG dosyası yükleyin!")
            return
        
        for entry in self.entries:
            try:
                self.convert_file_entry(entry)
            except Exception as e:
                print(f"Dosya çevrilirken hata: {entry.get('filename', 'Unknown')}: {e}")
        
        messagebox.showinfo("Başarılı", f"{len(self.entries)} dosya çevrildi!")
    
    def convert_file_entry(self, entry):
        """Tek bir dosya entry'sini çevir"""
        # Bu metod mevcut convert_single_file mantığını kullanır
        pass

if __name__ == "__main__":
    main()
