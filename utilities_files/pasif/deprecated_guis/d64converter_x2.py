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
from petcat_detokenizer import PetcatDetokenizer

# Decompiler modüllerini import et
try:
    from decompiler_qbasic import DecompilerQBasic
    DECOMPILER_QBASIC_AVAILABLE = True
except ImportError:
    logging.warning("decompiler_qbasic.py bulunamadı")
    DECOMPILER_QBASIC_AVAILABLE = False

try:
    from decompiler_c import DecompilerC
    DECOMPILER_C_AVAILABLE = True
except ImportError:
    logging.warning("decompiler_c.py bulunamadı")
    DECOMPILER_C_AVAILABLE = False

try:
    from decompiler_cpp import DecompilerCPP
    DECOMPILER_CPP_AVAILABLE = True
except ImportError:
    logging.warning("decompiler_cpp.py bulunamadı")
    DECOMPILER_CPP_AVAILABLE = False

try:
    from decompiler_c_2 import DecompilerC2
    DECOMPILER_C2_AVAILABLE = True
except ImportError:
    logging.warning("decompiler_c_2.py bulunamadı")
    DECOMPILER_C2_AVAILABLE = False

try:
    from decompiler import Decompiler
    DECOMPILER_AVAILABLE = True
except ImportError:
    logging.warning("decompiler.py bulunamadı")
    DECOMPILER_AVAILABLE = False

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
        self.entries = []
        self.basic_parser = C64BasicParser()
        self.sprite_converter = SpriteConverter()
        self.sid_converter = SIDConverter()
        self.petcat_detokenizer = PetcatDetokenizer()
        self.selected_files = []
        
        # Processed files history
        self.processed_files = []
        self.last_file_location = ""
        
        # Illegal opcode analyzer
        if ILLEGAL_ANALYZER_AVAILABLE:
            self.illegal_analyzer = IllegalOpcodeAnalyzer()
            self.illegal_analysis_results = None
        else:
            self.illegal_analyzer = None
            self.illegal_analysis_results = None
        
        # Çıktı klasörlerini oluştur
        self.setup_output_directories()
        
        self.setup_gui()
        
        self.logger.info("D64ConverterApp başarıyla başlatıldı")
        self.setup_logging()
        
        # Disassembler seçeneklerini açıkla
        self.show_startup_info()
        
        # Sürükle-bırak desteği - opsiyonel
        if TkinterDnD and DND_FILES:
            try:
                self.setup_drag_drop()
            except Exception as e:
                print(f"Sürükle-bırak desteği başlatılamadı: {e}")
        else:
            print("Sürükle-bırak desteği yok - sadece dosya seçim butonu kullanılacak")

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
        ttk.Entry(file_frame, textvariable=self.d64_path, width=50).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(file_frame, text="Seç", command=self.select_file).grid(row=0, column=2, padx=(10, 0))
        ttk.Button(file_frame, text="Dosya Bul", command=self.find_files).grid(row=0, column=3, padx=(5, 0))
        ttk.Button(file_frame, text="İşlenenler", command=self.show_processed_files).grid(row=0, column=4, padx=(5, 0))
        
        # Dosya türü bilgisi
        info_label = ttk.Label(file_frame, text="💡 İpucu: Dosya seçim dialogunda 'All C64 Files' seçeneğini kullanın veya Windows'da Dosya Gezgini > Görünüm > Dosya adı uzantıları'nı etkinleştirin", 
                              font=('Arial', 8), foreground='blue')
        info_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        # Dosya listesi
        list_frame = ttk.LabelFrame(main_frame, text="Dosya Listesi", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Treeview ile dosya listesi
        columns = ('Name', 'Type', 'Address', 'Program_Type', 'Track', 'Sector', 'Size')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Sütun başlıkları
        self.tree.heading('Name', text='Dosya Adı')
        self.tree.heading('Type', text='Tip')
        self.tree.heading('Address', text='Adres')
        self.tree.heading('Program_Type', text='Program Türü')
        self.tree.heading('Track', text='Track')
        self.tree.heading('Sector', text='Sector')
        self.tree.heading('Size', text='Boyut')
        
        # Sütun genişlikleri
        self.tree.column('Name', width=150, minwidth=120)
        self.tree.column('Type', width=50, minwidth=40)
        self.tree.column('Address', width=90, minwidth=80)
        self.tree.column('Program_Type', width=100, minwidth=90)
        self.tree.column('Track', width=60, minwidth=50)
        self.tree.column('Sector', width=60, minwidth=50)
        self.tree.column('Size', width=80, minwidth=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Çift tıklama event handler ekle
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # Seçenekler
        options_frame = ttk.LabelFrame(main_frame, text="Seçenekler", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # İlk satır - Temel seçenekler
        row1_frame = ttk.Frame(options_frame)
        row1_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Checkbutton(row1_frame, text="Gelişmiş Disassembler Kullan", 
                       variable=self.use_advanced_disassembler).grid(row=0, column=0, sticky=tk.W)
        
        # İkinci satır - Illegal opcode seçenekleri
        row2_frame = ttk.Frame(options_frame)
        row2_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Illegal opcode checkbox'u duruma göre
        if ILLEGAL_ANALYZER_AVAILABLE:
            ttk.Checkbutton(row2_frame, text="Illegal Opcode'ları Kullan", 
                           variable=self.use_illegal_opcodes).grid(row=0, column=0, sticky=tk.W)
            ttk.Label(row2_frame, text="(🔬 Advanced Analysis)", foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        else:
            ttk.Checkbutton(row2_frame, text="Illegal Opcode'ları Kullan", 
                           variable=self.use_illegal_opcodes,
                           state="disabled").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(row2_frame, text="(⚠ Analyzer yüklenmedi)", foreground="orange").grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Üçüncü satır - py65 seçenekleri
        row3_frame = ttk.Frame(options_frame)
        row3_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 0))
        
        # py65 Checkbox'u durum kontrolü ile
        if PY65_AVAILABLE and 'PROF_PY65_AVAILABLE' in globals() and PROF_PY65_AVAILABLE:
            ttk.Checkbutton(row3_frame, text="py65 Profesyonel Disassembler Kullan", 
                           variable=self.use_py65_disassembler).grid(row=0, column=0, sticky=tk.W)
            ttk.Label(row3_frame, text="(🚀 Professional Mode)", foreground="green").grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        else:
            ttk.Checkbutton(row3_frame, text="py65 Profesyonel Disassembler Kullan", 
                           variable=self.use_py65_disassembler, 
                           state="disabled").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(row3_frame, text="(✗ py65 kütüphanesi yüklü değil)", foreground="red").grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Format seçimi kaldırıldı - her format kendi butonuna sahip
        
        # Butonlar - tek satır
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # İlk grup - Disassembly
        group1 = ttk.LabelFrame(button_frame, text="Disassembly", padding="5")
        group1.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(group1, text="Assembly'e Çevir", command=self.convert_to_assembly).grid(row=0, column=0, padx=2)
        ttk.Button(group1, text="C'ye Çevir", command=self.convert_to_c).grid(row=0, column=1, padx=2)
        ttk.Button(group1, text="QBasic'e Çevir", command=self.convert_to_qbasic).grid(row=0, column=2, padx=2)
        
        # İkinci grup - BASIC Detokenizers
        group2 = ttk.LabelFrame(button_frame, text="BASIC Detokenizers", padding="5")
        group2.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(group2, text="BASIC Parser", command=self.convert_to_basic).grid(row=0, column=0, padx=2)
        ttk.Button(group2, text="Petcat", command=self.convert_to_petcat).grid(row=0, column=1, padx=2)
        ttk.Button(group2, text="C64List", command=self.convert_to_c64list).grid(row=0, column=2, padx=2)
        
        # Üçüncü grup - Gelişmiş
        group3 = ttk.LabelFrame(button_frame, text="Gelişmiş", padding="5")
        group3.grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        ttk.Button(group3, text="PDSX'e Çevir", command=self.convert_to_pdsx).grid(row=0, column=0, padx=2)
        ttk.Button(group3, text="Pseudo'ya Çevir", command=self.convert_to_pseudo).grid(row=0, column=1, padx=2)
        ttk.Button(group3, text="Py65 Disasm", command=self.convert_to_py65).grid(row=0, column=2, padx=2)
        
        # Dördüncü grup - Decompiler
        group4 = ttk.LabelFrame(button_frame, text="Decompiler", padding="5")
        group4.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        ttk.Button(group4, text="Decompiler", command=self.convert_to_decompiler).grid(row=0, column=0, padx=2)
        ttk.Button(group4, text="QBasic Dec", command=self.convert_to_dec_qbasic).grid(row=0, column=1, padx=2)
        ttk.Button(group4, text="C Dec", command=self.convert_to_dec_c).grid(row=0, column=2, padx=2)
        
        # Beşinci grup - Decompiler 2
        group5 = ttk.LabelFrame(button_frame, text="Decompiler 2", padding="5")
        group5.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        ttk.Button(group5, text="C++ Dec", command=self.convert_to_dec_cpp).grid(row=0, column=0, padx=2)
        ttk.Button(group5, text="C_2 Dec", command=self.convert_to_dec_c2).grid(row=0, column=1, padx=2)
        ttk.Button(group5, text="ASM Dec", command=self.convert_to_dec_asm).grid(row=0, column=2, padx=2)
        
        # Altıncı grup - Özellikler
        group6 = ttk.LabelFrame(button_frame, text="Özellikler", padding="5")
        group6.grid(row=1, column=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(group6, text="Illegal Opcode", command=self.analyze_illegal_opcodes).grid(row=0, column=0, padx=2)
        ttk.Button(group6, text="Sprite Analiz", command=self.analyze_sprites).grid(row=0, column=1, padx=2)
        ttk.Button(group6, text="SID Analiz", command=self.analyze_sid).grid(row=0, column=2, padx=2)
        
        # Yedinci grup - Kaydetme
        group7 = ttk.LabelFrame(button_frame, text="Kaydetme", padding="5")
        group7.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(group7, text="Tek Dosya Çevir", command=self.convert_single_file).grid(row=0, column=0, padx=2)
        ttk.Button(group7, text="Aktif Sekmeyi Kaydet", command=self.save_active_tab).grid(row=0, column=1, padx=2)
        ttk.Button(group7, text="Tüm Sekmeleri Kaydet", command=self.save_all_tabs).grid(row=0, column=2, padx=2)
        ttk.Button(group7, text="Çıktı Klasörünü Aç", command=self.open_output_folder).grid(row=0, column=3, padx=2)
        
        # Notebook için farklı çıktılar
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Çıktı sekmeleri
        self.output_tabs = {}
        tab_names = ['Assembly', 'C', 'QBasic', 'PDSX', 'Pseudo', 'BASIC', 'Petcat', 'C64List', 'Py65Disasm', 'Decompiler', 'DecQBasic', 'DecC++', 'DecC_2', 'DecC', 'DecASM']
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
        self.status_var = tk.StringVar(value="Hazır - Lütfen 'Seç' düğmesi ile D64 dosyası seçin")
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
            
            # Adres ve program türü bilgisini al
            address_info, program_type = self.get_program_info(entry)
            
            self.tree.insert('', 'end', values=(filename, file_type, address_info, program_type, track, sector, size))
        
        print(f"Dosya listesi güncellendi: {len(self.entries)} dosya")  # Debug

    def get_program_info(self, entry):
        """Program bilgilerini al (adres ve tür)"""
        try:
            # PRG verisini çıkar
            prg_data = self.extract_prg_data(entry)
            if not prg_data or len(prg_data) < 2:
                return "Unknown", "Unknown"
            
            # Start address
            start_address = prg_data[0] + (prg_data[1] << 8)
            address_hex = f"${start_address:04X}"
            address_dec = f"({start_address})"
            address_info = f"{address_hex} {address_dec}"
            
            # Program türü
            file_type = entry.get('type', entry.get('file_type', 'UNKNOWN'))
            
            if start_address == 0x0801:
                program_type = "BASIC"
            elif file_type == 'SEQ':
                program_type = "Sequential"
            elif file_type == 'USR':
                program_type = "User Defined"
            elif file_type == 'DEL':
                program_type = "Deleted"
            else:
                program_type = "Machine Code"
            
            return address_info, program_type
            
        except Exception as e:
            print(f"Program info hatası: {e}")
            return "Unknown", "Unknown"
        
        # İlk dosyayı göster
        if self.entries:
            print(f"İlk dosya yapısı: {self.entries[0]}")  # Debug
            self.status_var.set(f"✅ {len(self.entries)} dosya yüklendi - Dönüştürme düğmelerini kullanabilirsiniz")
        else:
            self.status_var.set("Hazır - Lütfen 'Seç' düğmesi ile D64 dosyası seçin")

    def convert_to_specific_format(self, format_code, tab_name):
        """Belirli bir formata dönüştür ve sadece o sekmesini güncelle"""
        # Önce entries kontrolü
        if not self.entries:
            messagebox.showwarning("Uyarı", "Lütfen önce 'Seç' düğmesi ile bir D64 dosyası seçin!")
            return
            
        selection = self.tree.selection()
        if not selection:
            # Seçim yoksa ilk dosyayı al
            selected_entry = self.entries[0]
            print(f"Seçim yok, ilk dosya kullanılıyor: {selected_entry.get('filename')}")
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
            
            # Format'a göre işle
            if start_address == 0x0801:
                # BASIC program
                print("BASIC program tespit edildi")
                basic_parser = C64BasicParser()
                basic_lines = basic_parser.detokenize(prg_data)
                
                if basic_lines:
                    if format_code == 'commodorebasicv2':
                        result_code = "\n".join(basic_lines)
                    elif format_code == 'petcat':
                        result_code = self.petcat_detokenizer.detokenize_prg(prg_data)
                    elif format_code == 'c64list':
                        result_code = f"; C64List henüz implement edilmedi\n; BASIC parser kullanılıyor\n\n"
                        result_code += "\n".join(basic_lines)
                    elif format_code == 'qbasic':
                        result_code = basic_parser.transpile(basic_lines, "qbasic")
                    elif format_code == 'pdsx':
                        result_code = basic_parser.transpile(basic_lines, "pdsx")
                    elif format_code == 'c':
                        result_code = basic_parser.transpile(basic_lines, "c")
                    elif format_code == 'py65':
                        result_code = f"; BASIC Program (${start_address:04X})\n; Py65 disassembler için BASIC listing\n\n"
                        result_code += "\n".join([f"; {line}" for line in basic_lines])
                    else:
                        result_code = f"; BASIC Program (${start_address:04X})\n; {format_code} formatı için BASIC listing\n\n"
                        result_code += "\n".join([f"; {line}" for line in basic_lines])
                else:
                    result_code = f"; BASIC Program detokenization failed\n"
            else:
                # Assembly program
                print("Assembly program tespit edildi")
                if format_code.startswith('dec_'):
                    # Decompiler formatları
                    if format_code == 'dec_qbasic' and DECOMPILER_QBASIC_AVAILABLE:
                        decompiler = DecompilerQBasic()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif format_code == 'dec_cpp' and DECOMPILER_CPP_AVAILABLE:
                        decompiler = DecompilerCPP()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif format_code == 'dec_c2' and DECOMPILER_C2_AVAILABLE:
                        decompiler = DecompilerC2()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif format_code == 'dec_c' and DECOMPILER_C_AVAILABLE:
                        decompiler = DecompilerC()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif format_code == 'decompiler' and DECOMPILER_AVAILABLE:
                        decompiler = Decompiler()
                        result_code = decompiler.decompile()
                    elif format_code == 'dec_asm':
                        result_code = f"; ASM Decompiler henüz implement edilmedi\n; Assembly disassembler kullanılıyor\n\n"
                        disassembler = AdvancedDisassembler(
                            start_address=start_address,
                            code=code_data,
                            use_py65=self.use_py65_disassembler.get(),
                            use_illegal_opcodes=self.use_illegal_opcodes.get(),
                            output_format='asm'
                        )
                        result_code += disassembler.disassemble_simple(prg_data)
                    else:
                        result_code = f"; {format_code} decompiler bulunamadı\n; Assembly disassembler kullanılıyor\n\n"
                        disassembler = AdvancedDisassembler(
                            start_address=start_address,
                            code=code_data,
                            use_py65=self.use_py65_disassembler.get(),
                            use_illegal_opcodes=self.use_illegal_opcodes.get(),
                            output_format='asm'
                        )
                        result_code += disassembler.disassemble_simple(prg_data)
                else:
                    # Normal disassembler
                    disassembler = AdvancedDisassembler(
                        start_address=start_address,
                        code=code_data,
                        use_py65=self.use_py65_disassembler.get(),
                        use_illegal_opcodes=self.use_illegal_opcodes.get(),
                        output_format=format_code
                    )
                    
                    if format_code == 'py65' or self.use_py65_disassembler.get():
                        result_code = disassembler.disassemble_py65(prg_data)
                    else:
                        result_code = disassembler.disassemble_simple(prg_data)
            
            # GUI'de göster
            self.root.after(0, self._update_specific_tab, result_code, tab_name, entry)
            
        except Exception as e:
            error_msg = str(e)
            print(f"_convert_specific_format_thread hatası: {error_msg}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda msg=error_msg: self.status_var.set(f"Dönüştürme hatası: {msg}"))
    
    def _update_specific_tab(self, result_code, tab_name, entry):
        """Belirli bir sekmesini güncelle"""
        try:
            if tab_name in self.output_tabs:
                self.output_tabs[tab_name].delete(1.0, tk.END)
                self.output_tabs[tab_name].insert(tk.END, result_code)
                
                # Sekmeyi aktif et
                for i, (tab_text, tab_widget) in enumerate([(self.notebook.tab(i, "text"), self.notebook.nametowidget(self.notebook.tabs()[i])) for i in range(self.notebook.index("end"))]):
                    if tab_text == tab_name:
                        self.notebook.select(i)
                        break
                        
                filename = entry.get('filename', 'unknown')
                self.status_var.set(f"✅ {tab_name} formatı hazır: {filename}")
                
                # Dosyayı kaydet
                self.save_output_file(result_code, tab_name.lower(), filename)
                
            else:
                print(f"Uyarı: {tab_name} sekmesi bulunamadı")
                
        except Exception as e:
            print(f"_update_specific_tab hatası: {e}")
            self.status_var.set(f"Sekme güncellenirken hata: {e}")

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
        print(f"Dönüştürülecek dosya: {selected_entry.get('filename')}")
        
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
            
            # Çıktı formatını al - varsayılan olarak assembly kullan
            output_format = 'asm'
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
                    elif output_format == 'petcat':
                        # Petcat detokenizer kullan
                        result_code = self.petcat_detokenizer.detokenize_prg(prg_data)
                    elif output_format == 'c64list':
                        # C64List detokenizer için placeholder
                        result_code = f"; C64List detokenizer henüz implement edilmedi\n; Şimdilik BASIC parser kullanılıyor\n\n"
                        result_code += "\n".join(basic_lines)
                    else:
                        # ASM, pseudo formatları için de BASIC listesini ver
                        result_code = f"; BASIC Program (Start: ${start_address:04X})\n; Use commodorebasicv2 format for proper BASIC code\n\n"
                        result_code += "\n".join([f"; {line}" for line in basic_lines])
                else:
                    result_code = f"; BASIC Program detokenization failed\n; Raw data at ${start_address:04X}\n"
                    
            else:
                print(f"Assembly program tespit edildi - Assembly disassembler kullanılacak")
                
                # Decompiler formatları için decompiler kullan
                if output_format.startswith('dec_'):
                    if output_format == 'dec_qbasic' and DECOMPILER_QBASIC_AVAILABLE:
                        decompiler = DecompilerQBasic()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif output_format == 'dec_cpp' and DECOMPILER_CPP_AVAILABLE:
                        decompiler = DecompilerCPP()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif output_format == 'dec_c2' and DECOMPILER_C2_AVAILABLE:
                        decompiler = DecompilerC2()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif output_format == 'dec_c' and DECOMPILER_C_AVAILABLE:
                        decompiler = DecompilerC()
                        result_code = decompiler.decompile(prg_data, start_address)
                    elif output_format == 'decompiler' and DECOMPILER_AVAILABLE:
                        decompiler = Decompiler()
                        result_code = decompiler.decompile(prg_data, start_address)
                    else:
                        result_code = f"; {output_format} decompiler'ı bulunamadı\n; Assembly kodu kullanılıyor:\n\n"
                        # Assembly disassembler ile işle
                        disassembler = AdvancedDisassembler(
                            start_address=start_address,
                            code=code_data,
                            use_py65=self.use_py65_disassembler.get(),
                            use_illegal_opcodes=self.use_illegal_opcodes.get(),
                            output_format='asm'
                        )
                        
                        if self.use_py65_disassembler.get():
                            asm_code = disassembler.disassemble_py65(prg_data)
                        else:
                            asm_code = disassembler.disassemble_simple(prg_data)
                        
                        result_code += asm_code
                else:
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
            tab_mapping = {
                'asm': 'Assembly',
                'c': 'C',
                'qbasic': 'QBasic',
                'pdsx': 'PDSX',
                'pseudo': 'Pseudo',
                'commodorebasicv2': 'BASIC',
                'petcat': 'Petcat',
                'c64list': 'C64List',
                'py65': 'Py65Disasm',
                'decompiler': 'Decompiler',
                'dec_qbasic': 'DecQBasic',
                'dec_cpp': 'DecC++',
                'dec_c2': 'DecC_2',
                'dec_c': 'DecC',
                'dec_asm': 'DecASM'
            }
            
            tab_name = tab_mapping.get(output_format)
            if tab_name and tab_name in self.output_tabs:
                self.output_tabs[tab_name].delete(1.0, tk.END)
                self.output_tabs[tab_name].insert(tk.END, result_code)
            else:
                print(f"Uyarı: {output_format} formatı için GUI sekmesi bulunamadı")
            
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

    def convert_to_petcat(self):
        """Petcat ile dönüştür"""
        self.convert_to_specific_format('petcat', 'Petcat')

    def convert_to_c64list(self):
        """C64List ile dönüştür"""
        self.convert_to_specific_format('c64list', 'C64List')

    def convert_to_py65(self):
        """Py65 disassembler ile dönüştür"""
        self.convert_to_specific_format('py65', 'Py65Disasm')

    def convert_to_decompiler(self):
        """Decompiler ile dönüştür"""
        self.convert_to_specific_format('decompiler', 'Decompiler')

    def convert_to_dec_qbasic(self):
        """QBasic decompiler ile dönüştür"""
        self.convert_to_specific_format('dec_qbasic', 'DecQBasic')

    def convert_to_dec_c(self):
        """C decompiler ile dönüştür"""
        self.convert_to_specific_format('dec_c', 'DecC')

    def convert_to_dec_cpp(self):
        """C++ decompiler ile dönüştür"""
        self.convert_to_specific_format('dec_cpp', 'DecC++')

    def convert_to_dec_c2(self):
        """C_2 decompiler ile dönüştür"""
        self.convert_to_specific_format('dec_c2', 'DecC_2')

    def convert_to_dec_asm(self):
        """ASM decompiler ile dönüştür"""
        self.convert_to_specific_format('dec_asm', 'DecASM')

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

    def analyze_sprites(self):
        """Sprite analizi yap"""
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
            self.status_var.set(f"Sprite analizi başlatılıyor: {selected_entry.get('filename')}")
            
            # PRG dosyasını çıkart
            prg_data = self.extract_prg_data(selected_entry)
            if not prg_data:
                messagebox.showerror("Hata", "PRG verisi çıkarılamadı")
                return
            
            # Sprite analizi için sprite_converter kullan
            try:
                from sprite_converter import SpriteConverter
                sprite_converter = SpriteConverter()
                
                # Sprite verilerini analiz et
                sprite_results = sprite_converter.analyze_sprites(prg_data)
                
                # Sonuçları göster
                result_message = f"🎨 Sprite Analizi Sonuçları\n\n"
                result_message += f"Dosya: {selected_entry.get('filename')}\n"
                result_message += f"Dosya boyutu: {len(prg_data)} byte\n\n"
                
                if sprite_results.get('sprites_found', 0) > 0:
                    result_message += f"✅ {sprite_results['sprites_found']} sprite bulundu!\n"
                    result_message += f"Sprite adresleri: {sprite_results.get('sprite_addresses', [])}\n"
                    result_message += f"Sprite formatı: {sprite_results.get('sprite_format', 'Standart')}\n"
                else:
                    result_message += "❌ Sprite verisi bulunamadı\n"
                    result_message += "Bu dosya sprite içermiyor olabilir.\n"
                
                messagebox.showinfo("Sprite Analizi", result_message)
                self.status_var.set("Sprite analizi tamamlandı")
                
            except ImportError:
                messagebox.showerror("Hata", "Sprite analizi için sprite_converter modülü gerekli")
                self.status_var.set("Sprite analizi başarısız - modül eksik")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Sprite analizi sırasında hata: {str(e)}")
            print(f"Sprite analizi hatası: {e}")
            import traceback
            traceback.print_exc()

    def analyze_sid(self):
        """SID analizi yap"""
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
            self.status_var.set(f"SID analizi başlatılıyor: {selected_entry.get('filename')}")
            
            # PRG dosyasını çıkart
            prg_data = self.extract_prg_data(selected_entry)
            if not prg_data:
                messagebox.showerror("Hata", "PRG verisi çıkarılamadı")
                return
            
            # SID analizi için sid_converter kullan
            try:
                from sid_converter import SidConverter
                sid_converter = SidConverter()
                
                # SID verilerini analiz et
                sid_results = sid_converter.analyze_sid(prg_data)
                
                # Sonuçları göster
                result_message = f"🎵 SID Analizi Sonuçları\n\n"
                result_message += f"Dosya: {selected_entry.get('filename')}\n"
                result_message += f"Dosya boyutu: {len(prg_data)} byte\n\n"
                
                if sid_results.get('sid_found', False):
                    result_message += f"✅ SID müzik verisi bulundu!\n"
                    result_message += f"SID adresleri: {sid_results.get('sid_addresses', [])}\n"
                    result_message += f"Müzik formatı: {sid_results.get('music_format', 'Standart')}\n"
                    result_message += f"Kanal sayısı: {sid_results.get('channels', 'Bilinmiyor')}\n"
                else:
                    result_message += "❌ SID müzik verisi bulunamadı\n"
                    result_message += "Bu dosya müzik içermiyor olabilir.\n"
                
                messagebox.showinfo("SID Analizi", result_message)
                self.status_var.set("SID analizi tamamlandı")
                
            except ImportError:
                messagebox.showerror("Hata", "SID analizi için sid_converter modülü gerekli")
                self.status_var.set("SID analizi başarısız - modül eksik")
                
        except Exception as e:
            messagebox.showerror("Hata", f"SID analizi sırasında hata: {str(e)}")
            print(f"SID analizi hatası: {e}")
            import traceback
            traceback.print_exc()

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

    def setup_drag_drop(self):
        """Sürükle-bırak desteği"""
        try:
            if TKINTER_DND_AVAILABLE and TkinterDnD and DND_FILES:
                # TkinterDnD root'u kontrol et
                if hasattr(self.root, 'drop_target_register'):
                    self.root.drop_target_register(DND_FILES)
                    self.root.dnd_bind('<<Drop>>', self.on_drop)
                    print("Sürükle-bırak desteği başarıyla aktif edildi")
                    self.logger.info("Sürükle-bırak desteği aktif")
                else:
                    # Sessiz uyarı - sadece loglama
                    self.logger.warning("TkinterDnD drop_target_register desteklenmiyor - sürükle-bırak sınırlı")
            else:
                print("TkinterDnD veya DND_FILES bulunamadı")
                self.logger.warning("TkinterDnD bulunamadı")
        except Exception as e:
            error_msg = f"Sürükle-bırak setup hatası: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            traceback.print_exc()

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

    # Yeni method'lar
    def on_double_click(self, event):
        """Çift tıklama event handler"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            filename = item['values'][0]
            program_type = item['values'][3]  # Program türü sütunu
            
            # BASIC programları için otomatik parse
            if program_type == "BASIC":
                self.parse_basic_program(filename)
            else:
                # Diğer programlar için normal convert
                self.convert_single_file()

    def parse_basic_program(self, filename):
        """BASIC programını parse et ve BASIC tabında göster"""
        try:
            # Dosyayı entries'den bul
            selected_entry = None
            for entry in self.entries:
                if entry.get('filename') == filename:
                    selected_entry = entry
                    break
            
            if not selected_entry:
                messagebox.showerror("Hata", "Seçili dosya bulunamadı")
                return
            
            # PRG verisini çıkar
            prg_data = self.extract_prg_data(selected_entry)
            if not prg_data:
                messagebox.showerror("Hata", "PRG verisi çıkarılamadı")
                return
            
            # Start address kontrolü
            start_address = prg_data[0] + (prg_data[1] << 8)
            if start_address != 0x0801:
                messagebox.showwarning("Uyarı", f"Bu program BASIC değil (${start_address:04X})")
                return
            
            # BASIC parse et
            basic_lines = self.basic_parser.detokenize(prg_data)
            if basic_lines:
                basic_text = "\n".join(basic_lines)
                
                # BASIC tabında göster
                self.output_tabs['BASIC'].delete(1.0, tk.END)
                self.output_tabs['BASIC'].insert(tk.END, basic_text)
                
                # BASIC tabını seç
                for i, tab_id in enumerate(self.notebook.tabs()):
                    if self.notebook.tab(tab_id, "text") == "BASIC":
                        self.notebook.select(tab_id)
                        break
                
                self.status_var.set(f"BASIC program parse edildi: {filename}")
                
                # İşlem geçmişine ekle
                self.add_to_processed_files(filename, "BASIC Parse")
                
            else:
                messagebox.showerror("Hata", "BASIC program parse edilemedi")
                
        except Exception as e:
            messagebox.showerror("Hata", f"BASIC parse hatası: {str(e)}")

    def find_files(self):
        """Gelişmiş dosya bulma penceresi"""
        find_window = tk.Toplevel(self.root)
        find_window.title("Dosya Bul")
        find_window.geometry("600x400")
        find_window.transient(self.root)
        find_window.grab_set()
        
        # Arama çubuğu
        search_frame = ttk.Frame(find_window)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Dosya Adı:").pack(side=tk.LEFT)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        def search_files():
            search_pattern = search_var.get().lower()
            if not search_pattern:
                return
            
            # Dosya listesini filtrele
            filtered_files = []
            for item in file_listbox.get(0, tk.END):
                if search_pattern in item.lower():
                    filtered_files.append(item)
            
            # Listeyi güncelle
            file_listbox.delete(0, tk.END)
            for file in filtered_files:
                file_listbox.insert(tk.END, file)
        
        ttk.Button(search_frame, text="Ara", command=search_files).pack(side=tk.LEFT, padx=(5, 0))
        
        # Dosya listesi
        list_frame = ttk.Frame(find_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        file_listbox = tk.Listbox(list_frame)
        file_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Başlangıç dizini
        start_dir = self.last_file_location or os.getcwd()
        
        # Dosyaları listele
        def load_files():
            try:
                for root, dirs, files in os.walk(start_dir):
                    for file in files:
                        if file.lower().endswith(('.d64', '.d71', '.d81', '.d84', '.t64', '.tap', '.prg', '.p00')):
                            file_listbox.insert(tk.END, os.path.join(root, file))
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya listesi yüklenemedi: {str(e)}")
        
        load_files()
        
        # Çift tıklama ile dosya seç
        def on_file_select(event):
            selection = file_listbox.curselection()
            if selection:
                selected_file = file_listbox.get(selection[0])
                self.d64_path.set(selected_file)
                self.load_image(selected_file)
                find_window.destroy()
        
        file_listbox.bind('<Double-1>', on_file_select)
        
        # Butonlar
        button_frame = ttk.Frame(find_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Seç", command=lambda: on_file_select(None)).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="İptal", command=find_window.destroy).pack(side=tk.LEFT, padx=(5, 0))

    def show_processed_files(self):
        """İşlem geçmişini göster"""
        processed_window = tk.Toplevel(self.root)
        processed_window.title("İşlenen Dosyalar")
        processed_window.geometry("800x600")
        processed_window.transient(self.root)
        processed_window.grab_set()
        
        # Treeview
        columns = ('Disk', 'Program', 'İşlem', 'Tarih')
        tree = ttk.Treeview(processed_window, columns=columns, show='headings')
        
        tree.heading('Disk', text='Disk İmajı')
        tree.heading('Program', text='Program')
        tree.heading('İşlem', text='İşlem')
        tree.heading('Tarih', text='Tarih')
        
        tree.column('Disk', width=200)
        tree.column('Program', width=150)
        tree.column('İşlem', width=150)
        tree.column('Tarih', width=150)
        
        # Verileri ekle
        for item in self.processed_files:
            tree.insert('', 'end', values=(item['disk'], item['program'], item['operation'], item['date']))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Temizle butonu
        ttk.Button(processed_window, text="Geçmişi Temizle", 
                  command=lambda: self.clear_processed_files()).pack(pady=5)
        ttk.Button(processed_window, text="Kapat", 
                  command=processed_window.destroy).pack(pady=5)

    def add_to_processed_files(self, program_name, operation):
        """İşlem geçmişine ekle"""
        from datetime import datetime
        
        disk_name = os.path.basename(self.d64_path.get()) if self.d64_path.get() else "Unknown"
        
        self.processed_files.append({
            'disk': disk_name,
            'program': program_name,
            'operation': operation,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Maksimum 1000 kayıt tut
        if len(self.processed_files) > 1000:
            self.processed_files = self.processed_files[-1000:]

    def clear_processed_files(self):
        """İşlem geçmişini temizle"""
        self.processed_files = []
        messagebox.showinfo("Bilgi", "İşlem geçmişi temizlendi")

    # Yeni dönüştürme method'ları
    def convert_to_py65(self):
        """Py65 disassembler ile çevir"""
        self.output_format.set('py65')
        self.convert_single_file()

    def convert_to_decompiler(self):
        """Decompiler ile çevir"""
        self.output_format.set('decompiler')
        self.convert_single_file()

    def convert_to_dec_qbasic(self):
        """QBasic decompiler ile çevir"""
        self.output_format.set('dec_qbasic')
        self.convert_single_file()

    def convert_to_dec_cpp(self):
        """C++ decompiler ile çevir"""
        self.output_format.set('dec_cpp')
        self.convert_single_file()

    def convert_to_dec_c2(self):
        """C_2 decompiler ile çevir"""
        self.output_format.set('dec_c2')
        self.convert_single_file()

    def convert_to_dec_c(self):
        """C decompiler ile çevir"""
        self.output_format.set('dec_c')
        self.convert_single_file()

    def convert_to_dec_asm(self):
        """ASM decompiler ile çevir"""
        self.output_format.set('dec_asm')
        self.convert_single_file()

    def convert_to_petcat(self):
        """Petcat detokenizer ile çevir"""
        self.output_format.set('petcat')
        self.convert_single_file()

    def convert_to_c64list(self):
        """C64List detokenizer ile çevir"""
        self.output_format.set('c64list')
        self.convert_single_file()

    # Eski update_output_format metodları kaldırıldı - artık her format kendi metoduna sahip

def main():
    """
    Ana fonksiyon - TkinterDnD desteğiyle
    """
    # TkinterDnD desteği varsa onu kullan
    try:
        if TKINTER_DND_AVAILABLE and TkinterDnD:
            print("TkinterDnD ile GUI başlatılıyor...")
            root = TkinterDnD.Tk()
        else:
            print("Normal Tkinter ile GUI başlatılıyor...")
            root = tk.Tk()
    except Exception as e:
        print(f"TkinterDnD hatası: {e}, normal Tkinter kullanılıyor...")
        root = tk.Tk()
    
    # Hata yakalama
    try:
        print("D64ConverterApp başlatılıyor...")
        app = D64ConverterApp(root)
        print("GUI hazır, mainloop başlatılıyor...")
        root.mainloop()
    except Exception as e:
        print(f"Kritik hata: {e}")
        traceback.print_exc()
        input("Devam etmek için Enter tuşuna basın...")

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

if __name__ == "__main__":
    main()
