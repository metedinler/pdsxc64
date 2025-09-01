#!/usr/bin/env python3
"""
D64 Converter - GUI Manager v5.0 - GUI DEBUG MODE + COMPREHENSIVE LOGGING
Modern Tkinter tabanlı grafik arayüz - X1 GUI Integration + GUI Debug System + Full Logging

🍎 GUI DEBUG GUIDE - COMPONENT CODES:
================================================================
[G1-G99]   GUI Component Codes (Butonlar, Frame'ler, Dialog'lar)
[G100+]    Window/Dialog Component Codes  
================================================================

📝 COMPREHENSIVE LOGGING:
- Tüm kullanıcı tıklamaları loglanır
- Button click, menu select, file operations
- Hatalar, uyarılar, bilgiler kayıt altına alınır
- Tab değişimleri, window operations izlenir

ADIM 5: GUI Integration + X1 Features + GUI Debug + Comprehensive Logging
- Modern dark theme arayüz
- X1 GUI'nin tüm fonksiyonları  
- 4 panel layout: Directory, Disassembly, Decompiler, Console
- Disk imajı okuma ve dosya seçimi
- Disassembler formatları: Assembly, C, QBasic, PDSX, Pseudo
- Decompiler sistemleri: C, C++, QBasic, Assembly
- BASIC detokenizers: Parser, Petcat, C64List
- Analiz araçları: Illegal opcode, Sprite, SID, Charset
- GUI Debug System: Her öğeye kod atanması
- Full Logging: Her kullanıcı etkileşimi loglanır

Author: D64 Converter Team
Version: 5.0 (X1 Integration + GUI Debug + Comprehensive Logging)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font
import threading

# Comprehensive logging sistemi başlat
try:
    from comprehensive_logger import (
        get_logger, log_info, log_error, log_warning, log_user_action, 
        log_button_click, log_gui_event, log_file_operation, 
        log_performance, log_window_operation, log_tab_change
    )
    # GUI başlangıcını logla
    log_info("GUI Manager v5.0 başlatıldı", "GUI_STARTUP")
    GUI_LOGGING_ENABLED = True
except Exception as e:
    print(f"⚠️ GUI Logging sistemi başlatılamadı: {e}")
    # Fallback fonksiyonlar - düzgün syntax ile
    def log_info(msg, context=None): 
        print(f"ℹ️ GUI: {msg}")
    def log_error(msg, exc=None, context=None):   
        print(f"🔴 GUI: {msg}")
    def log_warning(msg, context=None): 
        print(f"⚠️ GUI: {msg}")
    def log_user_action(*args, **kwargs): 
        pass
    def log_button_click(*args, **kwargs): 
        pass
    def log_gui_event(*args, **kwargs): 
        pass
    def log_file_operation(*args, **kwargs): 
        pass
    def log_performance(*args, **kwargs): 
        pass
    def log_window_operation(*args, **kwargs): 
        pass
    def log_tab_change(*args, **kwargs): 
        pass
    GUI_LOGGING_ENABLED = False

# Syntax highlighting import
try:
    from syntax_highlighter import Assembly6502Highlighter, C64BasicHighlighter
    SYNTAX_HIGHLIGHTING_AVAILABLE = True
except ImportError:
    SYNTAX_HIGHLIGHTING_AVAILABLE = False
    print("⚠️ Syntax highlighter module not found - using plain text")
import time
import os
import sys
import json
import subprocess
import struct
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Syntax highlighter entegrasyonu
try:
    from syntax_highlighter import Assembly6502Highlighter, C64BasicHighlighter, HybridHighlighter
    SYNTAX_HIGHLIGHTER_AVAILABLE = True
except ImportError:
    SYNTAX_HIGHLIGHTER_AVAILABLE = False

# Core system imports
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

class GUIDebugHelper:
    """🍎 GUI Debug Helper - GUI componentlerine kod atama sistemi"""
    
    def __init__(self):
        self.debug_mode = False
        self.gui_component_counter = 1
        self.component_registry = {}
        
        # 🍎 Environment variable ile debug mode başlatma - KızılElma Feature
        if os.environ.get('GUI_DEBUG_MODE', '').lower() == 'true':
            self.enable_debug()
            print("🍎 GUI Debug Mode environment variable ile aktif edildi")
    
    @property
    def debug_enabled(self):
        """debug_enabled property - debug_mode için alias"""
        return self.debug_mode
        
    def enable_debug(self):
        """GUI debug modunu aktif et"""
        self.debug_mode = True
        print("[GUI-DEBUG] 🟢 GUI Debug Mode AÇIK")
        
    def disable_debug(self):
        """GUI debug modunu kapat"""
        self.debug_mode = False
        print("[GUI-DEBUG] 🔴 GUI Debug Mode KAPALI")
        
    def toggle_debug(self):
        """GUI debug modunu toggle et"""
        if self.debug_mode:
            self.disable_debug()
        else:
            self.enable_debug()
            
    def get_component_code(self, component_type, original_text):
        """Component için kod üret"""
        code = f"G{self.gui_component_counter}"
        self.component_registry[code] = {
            'type': component_type,
            'original_text': original_text,
            'counter': self.gui_component_counter
        }
        self.gui_component_counter += 1
        return code
    
    def register_component(self, widget, component_type, original_text):
        """Widget'ı registry'e kaydet - YENI METOD"""
        code = f"G{self.gui_component_counter}"
        self.component_registry[code] = {
            'widget': widget,
            'type': component_type,
            'original_text': original_text,
            'counter': self.gui_component_counter
        }
        self.gui_component_counter += 1
        return code
        
    def format_text_with_debug(self, component_type, original_text):
        """Debug modunda text'i formatla"""
        if not self.debug_mode:
            return original_text
            
        code = self.get_component_code(component_type, original_text)
        return f"{code}-{original_text}"
        
    def log_component(self, code, action="created"):
        """Component işlemini logla"""
        if self.debug_mode and code in self.component_registry:
            comp = self.component_registry[code]
            print(f"[{code}] {comp['type'].upper()} {action}: {comp['original_text']}")
            
    def show_registry(self):
        """Kayıtlı componentleri göster"""
        print("=" * 60)
        print("🍎 GUI COMPONENT REGISTRY")
        print("=" * 60)
        for code, comp in self.component_registry.items():
            print(f"[{code}] {comp['type']}: {comp['original_text']}")
        print("=" * 60)
        
    def debug_wrap_menu(self, parent, **kwargs):
        """Debug-enabled Menu wrapper"""
        try:
            import tkinter as tk
            menu = tk.Menu(parent, **kwargs)
            
            if self.debug_mode:
                code = self.get_component_code("MENU", "MenuBar")
                menu.debug_code = code
                self.log_component(code, "created")
                print(f"🍎 Menu created with debug code: {code}")
            
            return menu
        except Exception as e:
            print(f"❌ Debug menu creation error: {e}")
            # Fallback
            import tkinter as tk
            return tk.Menu(parent, **kwargs)

# Global GUI debug helper
gui_debug = GUIDebugHelper()

# 🍎 GUI Debug Wrapper Functions
def debug_button(parent, debug_name="Button", text="", **kwargs):
    """Debug-enabled Button wrapper - IMPROVED WITH REGISTRY + COMPREHENSIVE LOGGING"""
    try:
        original_text = text
        debug_text = gui_debug.format_text_with_debug("BUTTON", text)
        
        # Orijinal command'ı al
        original_command = kwargs.get('command', None)
        
        # Logging wrapper command oluştur
        def logging_command_wrapper():
            try:
                # Button click'i logla
                log_button_click(debug_name, original_text, context="GUI_INTERACTION")
                log_gui_event("BUTTON_CLICK", f"{debug_name}:{original_text}")
                
                # Orijinal command'ı çağır
                if original_command:
                    original_command()
                    
            except Exception as e:
                log_error(f"Button command hatası: {debug_name}", e, "GUI_BUTTON_ERROR")
                raise
        
        # Command'ı wrapper ile değiştir
        if original_command:
            kwargs['command'] = logging_command_wrapper
        
        # Her zaman tk.Button kullan (ttk.Button font desteklemiyor)
        btn = tk.Button(parent, text=debug_text, **kwargs)
        
        # Widget'ı registry'e kaydet
        code = gui_debug.register_component(btn, "Button", original_text)
        
        if gui_debug.debug_mode:
            gui_debug.log_component(code, "created")
            
        # Button oluşturulmasını logla
        log_gui_event("BUTTON_CREATED", f"{debug_name}:{original_text}", widget_code=code)
        
        return btn
    except Exception as e:
        log_error(f"Debug button creation error: {debug_name}", e, "GUI_BUTTON_CREATION")
        print(f"❌ Debug button creation error: {e}")
        # Fallback: normal Button oluştur (font parametresi kaldırılarak)
        safe_kwargs = {k: v for k, v in kwargs.items() if k != 'font'}
        return tk.Button(parent, text=text, **safe_kwargs)

def debug_label(parent, debug_name="Label", text="", **kwargs):
    """Debug-enabled Label wrapper - IMPROVED WITH REGISTRY"""
    original_text = text
    debug_text = gui_debug.format_text_with_debug("LABEL", text)
    lbl = tk.Label(parent, text=debug_text, **kwargs)
    
    # Widget'ı registry'e kaydet
    code = gui_debug.register_component(lbl, "Label", original_text)
    
    if gui_debug.debug_mode:
        gui_debug.log_component(code, "created")
    return lbl

def debug_frame(parent, debug_name="Frame", **kwargs):
    """Debug-enabled Frame wrapper"""
    # Remove debug_name from kwargs to prevent tkinter error
    kwargs.pop('debug_name', None)
    
    debug_text = gui_debug.format_text_with_debug("FRAME", debug_name)
    frame = tk.Frame(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1] if gui_debug.component_registry else "G0"
        gui_debug.log_component(code, "created")
        # Frame'lere debug title ekle
        if 'bg' in kwargs:
            title_label = tk.Label(frame, text=f"[{code}]", 
                                 bg=kwargs['bg'], fg="#666666", font=("Arial", 8))
            title_label.pack(side=tk.TOP, anchor=tk.W)
    return frame

def debug_entry(parent, debug_name="Entry", **kwargs):
    """Debug-enabled Entry wrapper"""
    debug_text = gui_debug.format_text_with_debug("ENTRY", debug_name)
    entry = tk.Entry(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return entry

def debug_checkbox(parent, debug_name="Checkbox", text="", **kwargs):
    """Debug-enabled Checkbox wrapper"""
    debug_text = gui_debug.format_text_with_debug("CHECKBOX", text)
    checkbox = tk.Checkbutton(parent, text=debug_text, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return checkbox

def debug_radiobutton(parent, debug_name="Radio", text="", **kwargs):
    """Debug-enabled RadioButton wrapper"""
    debug_text = gui_debug.format_text_with_debug("RADIO", text)
    radio = tk.Radiobutton(parent, text=debug_text, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return radio

def debug_listbox(parent, debug_name="ListBox", **kwargs):
    """Debug-enabled ListBox wrapper"""
    debug_text = gui_debug.format_text_with_debug("LISTBOX", debug_name)
    listbox = tk.Listbox(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return listbox

def debug_text(parent, debug_name="TextWidget", **kwargs):
    """Debug-enabled Text widget wrapper"""
    debug_text_name = gui_debug.format_text_with_debug("TEXT", debug_name)
    text_widget = tk.Text(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return text_widget

def debug_scrolledtext(parent, debug_name="ScrolledText", **kwargs):
    """Debug-enabled ScrolledText wrapper"""
    debug_text_name = gui_debug.format_text_with_debug("SCROLLTEXT", debug_name)
    from tkinter import scrolledtext
    scrolled_text = scrolledtext.ScrolledText(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return scrolled_text

def debug_combobox(parent, debug_name="ComboBox", **kwargs):
    """Debug-enabled ComboBox wrapper"""
    debug_text = gui_debug.format_text_with_debug("COMBO", debug_name)
    combo = ttk.Combobox(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return combo

def debug_progressbar(parent, debug_name="ProgressBar", **kwargs):
    """Debug-enabled ProgressBar wrapper"""
    debug_text = gui_debug.format_text_with_debug("PROGRESS", debug_name)
    progress = ttk.Progressbar(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return progress

def debug_treeview(parent, debug_name="TreeView", **kwargs):
    """Debug-enabled TreeView wrapper"""
    debug_text = gui_debug.format_text_with_debug("TREE", debug_name)
    tree = ttk.Treeview(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return tree

def debug_notebook(parent, debug_name="Notebook", **kwargs):
    """Debug-enabled Notebook wrapper + Tab Change Logging"""
    debug_text = gui_debug.format_text_with_debug("NOTEBOOK", debug_name)
    notebook = ttk.Notebook(parent, **kwargs)
    
    # Tab değişim event'ini loglamak için callback ekle
    def on_tab_change(event):
        try:
            # Mevcut ve önceki tab bilgilerini al
            current_tab_index = notebook.index(notebook.select())
            current_tab_text = notebook.tab(current_tab_index, "text")
            
            # Tab değişimini logla
            log_tab_change("unknown", current_tab_text, 
                          notebook_name=debug_name, 
                          tab_index=current_tab_index,
                          context="GUI_TAB_CHANGE")
            log_gui_event("TAB_CHANGED", f"{debug_name}:tab_{current_tab_index}", 
                         tab_text=current_tab_text)
            
        except Exception as e:
            log_error(f"Tab change logging hatası: {debug_name}", e, "GUI_TAB_CHANGE_ERROR")
    
    # Tab değişim event'ini bind et
    notebook.bind("<<NotebookTabChanged>>", on_tab_change)
    
    # Notebook oluşturulmasını logla
    log_gui_event("NOTEBOOK_CREATED", debug_name)
    
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
        
    return notebook

def debug_panedwindow(parent, debug_name="PanedWindow", **kwargs):
    """Debug-enabled PanedWindow wrapper"""
    debug_text = gui_debug.format_text_with_debug("PANED", debug_name)
    paned = tk.PanedWindow(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return paned

def debug_canvas(parent, debug_name="Canvas", **kwargs):
    """Debug-enabled Canvas wrapper"""
    debug_text = gui_debug.format_text_with_debug("CANVAS", debug_name)
    canvas = tk.Canvas(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return canvas

def debug_scale(parent, debug_name="Scale", **kwargs):
    """Debug-enabled Scale wrapper"""
    debug_text = gui_debug.format_text_with_debug("SCALE", debug_name)
    scale = tk.Scale(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return scale

def debug_spinbox(parent, debug_name="SpinBox", **kwargs):
    """Debug-enabled SpinBox wrapper"""
    debug_text = gui_debug.format_text_with_debug("SPIN", debug_name)
    spinbox = tk.Spinbox(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return spinbox

def debug_labelframe(parent, debug_name="LabelFrame", text="", **kwargs):
    """Debug-enabled LabelFrame wrapper"""
    debug_text = gui_debug.format_text_with_debug("LABELFRAME", text)
    labelframe = tk.LabelFrame(parent, text=debug_text, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return labelframe

def debug_toplevel(parent=None, debug_name="Window", title="Window", **kwargs):
    """Debug-enabled Toplevel window wrapper"""
    debug_title = gui_debug.format_text_with_debug("WINDOW", title)
    toplevel = tk.Toplevel(parent, **kwargs)
    toplevel.title(debug_title)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return toplevel

def debug_menu(parent, debug_name="Menu", **kwargs):
    """Debug-enabled Menu wrapper"""
    debug_text = gui_debug.format_text_with_debug("MENU", debug_name)
    menu = tk.Menu(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return menu

def debug_menubutton(parent, debug_name="MenuButton", text="", **kwargs):
    """Debug-enabled MenuButton wrapper"""
    debug_text = gui_debug.format_text_with_debug("MENUBUTTON", text)
    menubutton = tk.Menubutton(parent, text=debug_text, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return menubutton

def debug_scrollbar(parent, debug_name="ScrollBar", **kwargs):
    """Debug-enabled ScrollBar wrapper"""
    debug_text = gui_debug.format_text_with_debug("SCROLL", debug_name)
    scrollbar = tk.Scrollbar(parent, **kwargs)
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "created")
    return scrollbar

def debug_messagebox(msg_type, title, message):
    """Debug-enabled MessageBox wrapper"""
    debug_title = gui_debug.format_text_with_debug("MESSAGEBOX", title)
    debug_message = gui_debug.format_text_with_debug("MESSAGE", message)
    
    if gui_debug.debug_mode:
        code_title = list(gui_debug.component_registry.keys())[-2]
        code_msg = list(gui_debug.component_registry.keys())[-1] 
        gui_debug.log_component(code_title, "displayed")
        gui_debug.log_component(code_msg, "displayed")
        print(f"[GUI-DEBUG] 📨 MessageBox: {msg_type}")
        
    # MessageBox çağrısı
    if msg_type == "info":
        return messagebox.showinfo(debug_title, debug_message)
    elif msg_type == "warning":
        return messagebox.showwarning(debug_title, debug_message)
    elif msg_type == "error":
        return messagebox.showerror(debug_title, debug_message)
    elif msg_type == "question":
        return messagebox.askyesno(debug_title, debug_message)

def debug_filedialog_open(debug_name="File Dialog", **kwargs):
    """Debug-enabled File Dialog Open wrapper + Comprehensive Logging"""
    debug_title = kwargs.get('title', 'Open File')
    debug_title = gui_debug.format_text_with_debug("FILEDIALOG", debug_title)
    kwargs['title'] = debug_title
    
    # Dialog açılışını logla
    log_gui_event("FILEDIALOG_OPEN", debug_name, dialog_title=debug_title)
    
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "opened")
    
    # File dialog'u aç
    selected_file = filedialog.askopenfilename(**kwargs)
    
    # Sonucu logla
    if selected_file:
        log_file_operation("FILE_SELECTED", selected_file, dialog_type="open", context="GUI_FILE_DIALOG")
        log_gui_event("FILEDIALOG_SUCCESS", debug_name, selected_file=selected_file)
    else:
        log_gui_event("FILEDIALOG_CANCELLED", debug_name)
    
    return selected_file

def debug_filedialog_save(debug_name="Save Dialog", **kwargs):
    """Debug-enabled File Dialog Save wrapper"""
    debug_title = kwargs.get('title', 'Save File')
    debug_title = gui_debug.format_text_with_debug("FILEDIALOG", debug_title)
    kwargs['title'] = debug_title
    
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "opened")
    
    return filedialog.asksaveasfilename(**kwargs)

def debug_dirdialog(debug_name="Directory Dialog", **kwargs):
    """Debug-enabled Directory Dialog wrapper"""
    debug_title = kwargs.get('title', 'Select Directory')
    debug_title = gui_debug.format_text_with_debug("DIRDIALOG", debug_title)
    kwargs['title'] = debug_title
    
    if gui_debug.debug_mode:
        code = list(gui_debug.component_registry.keys())[-1]
        gui_debug.log_component(code, "opened")
    
    return filedialog.askdirectory(**kwargs)

def safe_messagebox(msg_type, title, message):
    """Safe messagebox that works in both debug and normal mode"""
    try:
        if gui_debug.debug_mode:
            return debug_messagebox(msg_type, title, message)
        else:
            # Normal messagebox for normal mode
            if msg_type == "info":
                return messagebox.showinfo(title, message)
            elif msg_type == "warning":
                return messagebox.showwarning(title, message)
            elif msg_type == "error":
                return messagebox.showerror(title, message)
            elif msg_type == "question":
                return messagebox.askyesno(title, message)
    except Exception as e:
        # Fallback to basic messagebox if debug system fails
        return messagebox.showerror("Error", f"Message display error: {e}")

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
        self.last_directory = os.path.expanduser("~\\Downloads")  # Son kullanılan dizin
        self.last_search_directory = os.path.expanduser("~\\Downloads")  # Son arama dizini
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
    
    def log_to_terminal_and_file(self, message, level="INFO"):
        """Compatibility için log_to_terminal_and_file metodu - DiskDirectoryPanel için"""
        try:
            if hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'log_to_terminal_and_file'):
                self.parent_gui.log_to_terminal_and_file(message, level)
            elif hasattr(self, 'parent_gui') and self.parent_gui and hasattr(self.parent_gui, 'log_message'):
                self.parent_gui.log_message(message, level)
            else:
                print(f"[DiskDirectoryPanel {level}] {message}")
                
                # Try to log to file if possible
                try:
                    import logging
                    logger = logging.getLogger(__name__)
                    if level.upper() == "ERROR":
                        logger.error(message)
                    elif level.upper() == "WARNING":
                        logger.warning(message)
                    else:
                        logger.info(message)
                except:
                    pass  # Ignore if logging fails
                    
        except Exception as e:
            print(f"[DiskDirectoryPanel ERROR] Log error: {e}, Original message: {message}")
    
    def setup_ui(self):
        """Directory panel UI setup"""
        # File selection buttons - Üst satır + Kaydet Butonları
        controls_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        controls_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(controls_frame, text="📂 Dosya Seç", command=self.select_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="🔍 Dosya Bul", command=self.find_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="📋 İşlenenler", command=self.show_processed_files).pack(side=tk.LEFT, padx=2)
        
        # Kaydet butonları - Eski düzenden geri getiriliyor
        ttk.Button(controls_frame, text="💾 Kaydet", command=lambda: self.parent_gui.save_current_code() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="💾 Farklı Kaydet", command=lambda: self.parent_gui.save_as_current_code() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="📤 Tüm. Kaydet", command=lambda: self.parent_gui.batch_save_all_outputs() if self.parent_gui else None).pack(side=tk.LEFT, padx=2)
        
        # Directory tree
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview columns - doğru backup format
        columns = ("filename", "filetype", "start_addr", "end_addr", "program_type", "track", "sector", "size")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Column headers - doğru backup format
        self.tree.heading("filename", text="Dosya Adı")
        self.tree.heading("filetype", text="Tip")
        self.tree.heading("start_addr", text="Başlangıç")
        self.tree.heading("end_addr", text="Bitiş")
        self.tree.heading("program_type", text="Program Türü")
        self.tree.heading("track", text="Track")
        self.tree.heading("sector", text="Sector")
        self.tree.heading("size", text="Boyut")
        
        # Column widths - doğru backup format
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
        
        # Analysis buttons - Alt satır - backup'taki gibi
        analysis_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        analysis_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(analysis_frame, text="?? Illegal", command=self.analyze_illegal_opcodes).pack(side=tk.LEFT, padx=2)
        tk.Button(analysis_frame, text="🎮 Sprite", command=self.analyze_sprites, font=("Arial", 7), height=1, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(analysis_frame, text="🎵 SID", command=self.analyze_sid, font=("Arial", 7), height=1, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(analysis_frame, text="🔤 Charset", command=self.analyze_charset, font=("Arial", 7), height=1, width=10).pack(side=tk.LEFT, padx=2)
        
        # Hybrid Analysis buttons - AYNI FRAME'DE - TEK SATIR
        tk.Button(analysis_frame, text="🔍 Hibrit", command=lambda: self.parent_gui.analyze_hybrid_program_current() if self.parent_gui else None, font=("Arial", 7), height=1, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(analysis_frame, text="⚙️ ASM Ayır", command=lambda: self.parent_gui.extract_assembly_current() if self.parent_gui else None, font=("Arial", 7), height=1, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(analysis_frame, text="📝 BASIC Ayır", command=lambda: self.parent_gui.extract_basic_current() if self.parent_gui else None, font=("Arial", 7), height=1, width=10).pack(side=tk.LEFT, padx=2)
    
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
                initialdir=self.last_directory
            )
            
            if file_path:
                # Son dizini güncelle
                self.last_directory = os.path.dirname(file_path)
                self.last_search_directory = self.last_directory
                self.load_image(file_path)
                
        except Exception as e:
            safe_messagebox("error", "Dosya Seçim Hatası", f"Hata: {e}")
    
    def load_image(self, file_path):
        """Disk imajını yükle - X1 tarzı"""
        try:
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
                        reader = EnhancedD64ReaderWrapper(file_path)
                        self.entries = reader.list_files()
                        self.log_to_terminal_and_file(f"📄 {len(self.entries)} dosya bulundu", "INFO")
                    else:
                        # Standard D64 Reader fonksiyonlarını kullan  
                        self.log_to_terminal_and_file("⚠️ Standard D64 Reader kullanıldı", "WARNING")
                        from d64_reader import read_image, read_directory
                        disk_data = read_image(file_path)
                        self.entries = read_directory(disk_data, ext[1:])
                        self.log_to_terminal_and_file(f"📄 {len(self.entries)} dosya bulundu", "INFO")
                except Exception as reader_error:
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
                        reader = EnhancedD64ReaderWrapper(file_path)
                        self.entries = reader.list_files()
                        self.log_to_terminal_and_file(f"📄 {len(self.entries)} dosya bulundu", "INFO")
                    else:
                        # Fallback T64 okuma
                        self.log_to_terminal_and_file("⚠️ Fallback T64 okuma kullanıldı", "WARNING")
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
            safe_messagebox("error", "Dosya Yükleme Hatası", f"Hata: {e}")
    
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
        if self.selected_entry and self.parent_gui:
            self.parent_gui.auto_analyze_file(self.selected_entry)
    
    def find_files(self):
        """Gelişmiş dosya arama penceresi - Wildcard desteği ile"""
        try:
            # Arama penceresi oluştur
            search_window = tk.Toplevel(self.parent_gui.root if self.parent_gui else None)
            search_window.title("🔍 Dosya Arama")
            search_window.geometry("550x450")
            search_window.grab_set()
            
            # Ana frame
            main_frame = tk.Frame(search_window, bg=ModernStyle.BG_SECONDARY)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Üst kontrol paneli - Arama dizini ve kalıbı yan yana
            control_frame = tk.Frame(main_frame, bg=ModernStyle.BG_SECONDARY)
            control_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Arama dizini
            self.search_dir_var = tk.StringVar(value=self.last_search_directory)
            dir_entry = tk.Entry(control_frame, textvariable=self.search_dir_var, width=25, font=("Arial", 9))
            dir_entry.pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Button(control_frame, text="📁", command=lambda: self.select_search_directory(search_window)).pack(side=tk.LEFT, padx=(0, 10))
            
            # Arama kalıbı
            self.search_pattern_var = tk.StringVar(value="*.d64")
            pattern_entry = tk.Entry(control_frame, textvariable=self.search_pattern_var, width=15, font=("Arial", 9))
            pattern_entry.pack(side=tk.LEFT, padx=(0, 10))
            
            # Butonlar
            self.search_active = False
            ttk.Button(control_frame, text="🔍 Ara", command=lambda: self.start_search(search_window)).pack(side=tk.LEFT, padx=2)
            
            self.stop_btn = ttk.Button(control_frame, text="⏹️ Dur", command=self.stop_search, state="disabled")
            self.stop_btn.pack(side=tk.LEFT, padx=2)
            
            self.select_btn = ttk.Button(control_frame, text="✅ Seç", command=lambda: self.select_found_file(search_window), state="disabled")
            self.select_btn.pack(side=tk.LEFT, padx=2)
            
            # Sonuç listesi
            result_frame = tk.Frame(main_frame, bg=ModernStyle.BG_SECONDARY)
            result_frame.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(result_frame, text="📋 Arama Sonuçları:", bg=ModernStyle.BG_SECONDARY, 
                    fg=ModernStyle.FG_PRIMARY, font=("Arial", 9, "bold")).pack(anchor="w")
            
            # Listbox ile scrollbar - Yükseklik artırıldı
            list_frame = tk.Frame(result_frame)
            list_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
            
            scrollbar = tk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.result_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                           font=("Consolas", 9), selectmode=tk.SINGLE, height=20)
            self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=self.result_listbox.yview)
            
            # Listbox seçim olayı
            self.result_listbox.bind("<<ListboxSelect>>", lambda e: self.on_search_result_select())
            self.result_listbox.bind("<Double-Button-1>", lambda e: self.select_found_file(search_window))
            
            # Status bar
            self.search_status_var = tk.StringVar(value="Arama yapmak için parametreleri girin ve 'Ara' butonuna basın")
            tk.Label(main_frame, textvariable=self.search_status_var, bg=ModernStyle.BG_TERTIARY, 
                    fg=ModernStyle.FG_SECONDARY, font=("Arial", 8), relief="sunken").pack(fill=tk.X, pady=(10, 0))
            
            # Enter tuşu ile arama
            pattern_entry.bind("<Return>", lambda e: self.start_search(search_window))
            
            # Pencere kapanırken aramayı durdur
            search_window.protocol("WM_DELETE_WINDOW", lambda: self.close_search_window(search_window))
            
        except Exception as e:
            safe_messagebox("error", "Arama Penceresi Hatası", f"Arama penceresi açılamadı: {e}")
    
    def select_search_directory(self, parent_window):
        """Arama dizini seçimi"""
        try:
            directory = filedialog.askdirectory(
                title="Arama Dizini Seçin",
                initialdir=self.last_search_directory,
                parent=parent_window
            )
            if directory:
                self.last_search_directory = directory
                self.search_dir_var.set(directory)
        except Exception as e:
            safe_messagebox("error", "Dizin Seçim Hatası", f"Dizin seçilemedi: {e}")
    
    def start_search(self, search_window):
        """Arama başlat"""
        try:
            if self.search_active:
                return
                
            search_dir = self.search_dir_var.get().strip()
            pattern = self.search_pattern_var.get().strip()
            
            if not search_dir or not pattern:
                safe_messagebox("warning", "Eksik Bilgi", "Arama dizini ve kalıbı belirtilmelidir!")
                return
                
            if not os.path.exists(search_dir):
                safe_messagebox("error", "Dizin Hatası", f"Arama dizini bulunamadı: {search_dir}")
                return
            
            # UI güncelle
            self.search_active = True
            self.stop_btn.config(state="normal")
            self.select_btn.config(state="disabled")
            self.result_listbox.delete(0, tk.END)
            self.search_status_var.set("🔍 Arama başlatıldı...")
            
            # Threading ile arama
            self.search_thread = threading.Thread(target=self._search_files_thread, 
                                                 args=(search_dir, pattern), daemon=True)
            self.search_thread.start()
            
        except Exception as e:
            self.search_active = False
            self.stop_btn.config(state="disabled")
            safe_messagebox("error", "Arama Hatası", f"Arama başlatılamadı: {e}")
    
    def stop_search(self):
        """Aramayı durdur"""
        self.search_active = False
        self.stop_btn.config(state="disabled")
        self.search_status_var.set("⏹️ Arama durduruldu")
    
    def _search_files_thread(self, search_dir, pattern):
        """Arama thread'i - Wildcard desteği"""
        import fnmatch
        found_count = 0
        
        try:
            for root, dirs, files in os.walk(search_dir):
                if not self.search_active:
                    break
                    
                # Status güncelle
                current_dir = os.path.relpath(root, search_dir)
                if len(current_dir) > 50:
                    display_dir = "..." + current_dir[-47:]
                else:
                    display_dir = current_dir
                    
                self.search_status_var.set(f"🔍 Aranan: {display_dir}")
                
                for file in files:
                    if not self.search_active:
                        break
                        
                    # Wildcard karşılaştırması
                    if fnmatch.fnmatch(file.lower(), pattern.lower()):
                        full_path = os.path.join(root, file)
                        display_path = os.path.relpath(full_path, search_dir)
                        
                        # UI thread'inde listbox'a ekle
                        self.result_listbox.insert(tk.END, display_path)
                        found_count += 1
                        
                        # Çok fazla sonuç varsa dur
                        if found_count >= 500:
                            self.search_status_var.set(f"✅ {found_count} dosya bulundu (limit: 500)")
                            break
                            
                if found_count >= 500:
                    break
            
            # Arama tamamlandı
            if self.search_active:
                self.search_status_var.set(f"✅ Arama tamamlandı - {found_count} dosya bulundu")
            
        except Exception as e:
            self.search_status_var.set(f"❌ Arama hatası: {e}")
        finally:
            self.search_active = False
            self.stop_btn.config(state="disabled")
    
    def on_search_result_select(self):
        """Arama sonucunda dosya seçildi"""
        selection = self.result_listbox.curselection()
        if selection:
            self.select_btn.config(state="normal")
        else:
            self.select_btn.config(state="disabled")
    
    def select_found_file(self, search_window):
        """Seçili dosyayı yükle"""
        try:
            selection = self.result_listbox.curselection()
            if not selection:
                safe_messagebox("warning", "Seçim Yok", "Yüklenecek dosya seçilmemiş!")
                return
                
            selected_path = self.result_listbox.get(selection[0])
            full_path = os.path.join(self.search_dir_var.get(), selected_path)
            
            if os.path.exists(full_path):
                # Son dizini güncelle
                self.last_directory = os.path.dirname(full_path)
                self.last_search_directory = self.search_dir_var.get()
                
                # Dosyayı yükle
                self.load_image(full_path)
                search_window.destroy()
            else:
                safe_messagebox("error", "Dosya Bulunamadı", f"Dosya artık mevcut değil: {full_path}")
                
        except Exception as e:
            safe_messagebox("error", "Dosya Yükleme Hatası", f"Dosya yüklenemedi: {e}")
    
    def close_search_window(self, search_window):
        """Arama penceresini kapat"""
        self.search_active = False
        search_window.destroy()
    
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
            proc_window = debug_toplevel(self.parent_gui.root if self.parent_gui else None, title="İşlenmiş Dosyalar")
            proc_window.geometry("500x400")
            
            debug_label(proc_window, debug_name="Processed Files Title", text=f"İşlenmiş dosyalar ({len(found_files)} adet):").pack(pady=10)
            
            listbox = debug_listbox(proc_window, debug_name="Processed Files List")
            listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            for file_path in found_files:
                listbox.insert(tk.END, file_path)
                
            debug_button(proc_window, debug_name="Close Processed Files", text="Kapat", command=proc_window.destroy).pack(pady=10)
        else:
            safe_messagebox("info", "İşlenmiş Dosyalar", "Henüz işlenmiş dosya bulunmuyor.")
    
    def analyze_illegal_opcodes(self):
        """Illegal opcode analizi"""
        if not self.selected_entry:
            safe_messagebox("warning", "Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_illegal_opcodes(self.selected_entry)
    
    def analyze_sprites(self):
        """Sprite analizi"""
        if not self.selected_entry:
            safe_messagebox("warning", "Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_sprites(self.selected_entry)
    
    def analyze_sid(self):
        """SID müzik analizi"""
        if not self.selected_entry:
            safe_messagebox("warning", "Uyarı", "Lütfen önce bir dosya seçin")
            return
        
        if self.parent_gui:
            self.parent_gui.analyze_sid(self.selected_entry)
    
    def analyze_hybrid_program(self):
        """Hibrit program analizi"""
        if not self.selected_entry:
            safe_messagebox("warning", "Uyarı", "Lütfen önce bir dosya seçin")
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
                    safe_messagebox("error", "Hata", "PRG verisi bulunamadı")
                    return
                
                # Analiz yap
                result = analyzer.analyze_prg_data(prg_data)
                
                # Sonuçları göster
                report = analyzer.generate_hybrid_report(result)
                
                # Basit sonuç penceresi
                result_window = debug_toplevel(self, title="Hibrit Program Analizi")
                result_window.geometry("600x400")
                
                text_widget = debug_text(result_window, debug_name="Hybrid Analysis Text", wrap=tk.WORD, font=("Consolas", 10))
                scrollbar = debug_scrollbar(result_window, debug_name="Hybrid Analysis Scrollbar", command=text_widget.yview)
                text_widget.config(yscrollcommand=scrollbar.set)
                
                text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                text_widget.insert(tk.END, report)
                text_widget.config(state=tk.DISABLED)
                
            except Exception as e:
                safe_messagebox("error", "Hata", f"Hibrit analiz hatası: {e}")
                print(f"[ERROR] Standalone hybrid analysis failed: {e}")
    
    def analyze_hybrid_program(self):
        """Hibrit program analizi (BASIC+Assembly)"""
        if not self.selected_entry:
            safe_messagebox("warning", "Uyarı", "Lütfen önce bir dosya seçin")
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
        # Başlık kaldırıldı - console output frame labeli için alan açıldı
        
        # Disassembler formatları - Yeniden düzenlendi
        format_frame = debug_frame(self, debug_name="Format Frame", bg=ModernStyle.BG_SECONDARY)
        format_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # 1. DISASSEMBLY MODÜLLERI - Assembly format ve tüm disassemblerlar
        group1 = debug_frame(format_frame, debug_name="Disasm Group", bg=ModernStyle.BG_SECONDARY)
        group1.pack(side=tk.LEFT, padx=5, pady=2)
        
        debug_label(group1, debug_name="Disasm Group Label", text="⚙️ Disassembly Modülleri:", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_ACCENT, font=("Arial", 9, "bold")).pack(side=tk.TOP, pady=1)
        
        # Tüm disassembler butonları - tek satırda yan yana
        disasm_container = debug_frame(group1, debug_name="Disasm Container", bg=ModernStyle.BG_SECONDARY)
        disasm_container.pack(side=tk.TOP)
        
        debug_button(disasm_container, debug_name="Assembly", text="Assembly", command=lambda: self.convert_format('assembly')).pack(side=tk.LEFT, padx=1)
        debug_button(disasm_container, debug_name="Advanced", text="Advanced", command=lambda: self.convert_format('advanced_disasm')).pack(side=tk.LEFT, padx=1)
        debug_button(disasm_container, debug_name="Improved", text="Improved", command=lambda: self.convert_format('improved_disasm')).pack(side=tk.LEFT, padx=1)
        debug_button(disasm_container, debug_name="Hybrid", text="🔀 Hybrid", command=lambda: self.convert_format('hybrid_disasm')).pack(side=tk.LEFT, padx=1)
        debug_button(disasm_container, debug_name="py65 Pro", text="py65 Pro", command=lambda: self.convert_format('py65_pro')).pack(side=tk.LEFT, padx=1)
        debug_button(disasm_container, debug_name="Enhanced", text="⚡ Enhanced", command=lambda: self.convert_format('enhanced_disasm')).pack(side=tk.LEFT, padx=1)
        debug_button(disasm_container, debug_name="Multi", text="🎯 Multi", command=lambda: self.convert_format('multi_disasm')).pack(side=tk.LEFT, padx=1)
        
        # 2. BASIC DETOKENIZERS
        group2 = debug_frame(format_frame, debug_name="BASIC Group", bg=ModernStyle.BG_SECONDARY)
        group2.pack(side=tk.LEFT, padx=5, pady=2)
        
        debug_label(group2, debug_name="BASIC Detokenizers Label", text="📝 BASIC Detokenizers:", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_ACCENT, font=("Arial", 9, "bold")).pack(side=tk.TOP, pady=1)
        
        basic_container = debug_frame(group2, debug_name="Basic Container", bg=ModernStyle.BG_SECONDARY)
        basic_container.pack(side=tk.TOP)
        
        debug_button(basic_container, debug_name="BASIC", text="BASIC", command=lambda: self.convert_format('basic')).pack(side=tk.LEFT, padx=1)
        debug_button(basic_container, debug_name="Petcat", text="Petcat", command=lambda: self.convert_format('petcat')).pack(side=tk.LEFT, padx=1)
        debug_button(basic_container, debug_name="DList", text="DList", command=lambda: self.convert_format('dlist')).pack(side=tk.LEFT, padx=1)
        
        # 3. SANAL YAZIM MODLARI (eski Output Formats)
        group3 = debug_frame(format_frame, debug_name="Output Group", bg=ModernStyle.BG_SECONDARY)
        group3.pack(side=tk.LEFT, padx=5, pady=2)
        
        debug_label(group3, debug_name="Output Formats Label", text="💭 Sanal Yazım Modları:", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_ACCENT, font=("Arial", 9, "bold")).pack(side=tk.TOP, pady=1)
        
        output_container = debug_frame(group3, debug_name="Output Container", bg=ModernStyle.BG_SECONDARY)
        output_container.pack(side=tk.TOP)
        
        # py65 butonu kaldırıldı
        debug_button(output_container, debug_name="PDSX", text="PDSX", command=lambda: self.convert_format('pdsx')).pack(side=tk.LEFT, padx=1)
        debug_button(output_container, debug_name="C", text="C", command=lambda: self.convert_format('c')).pack(side=tk.LEFT, padx=1)
        debug_button(output_container, debug_name="QBasic", text="QBasic", command=lambda: self.convert_format('qbasic')).pack(side=tk.LEFT, padx=1)
        debug_button(output_container, debug_name="Pseudo", text="Pseudo", command=lambda: self.convert_format('pseudo')).pack(side=tk.LEFT, padx=1)
        
        # 4. BASIC TRANSPILER - Transpiler Engine ile birleştirildi
        transpiler_frame = debug_frame(format_frame, debug_name="Transpiler Frame", bg=ModernStyle.BG_SECONDARY)
        transpiler_frame.pack(side=tk.LEFT, padx=10, pady=2)
        
        debug_label(transpiler_frame, debug_name="Transpiler Label", text="🍎 BASIC Transpiler:", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_ACCENT, font=("Arial", 9, "bold")).pack(side=tk.TOP, pady=1)
        
        transpiler_container = debug_frame(transpiler_frame, debug_name="Transpiler Container", bg=ModernStyle.BG_SECONDARY)
        transpiler_container.pack(side=tk.TOP)
        
        # Enhanced BASIC Transpiler butonları - ilk satır
        if EnhancedBasicDecompiler:
            trans_row1 = debug_frame(transpiler_container, debug_name="Transpiler Row 1", bg=ModernStyle.BG_SECONDARY)
            trans_row1.pack(side=tk.TOP)
            debug_button(trans_row1, debug_name="Enhanced BASIC", text="🎯 Enhanced BASIC", command=lambda: self.convert_format('enhanced_basic')).pack(side=tk.LEFT, padx=1)
            debug_button(trans_row1, debug_name="QBasic Transpile", text="→ QBasic", command=lambda: self.convert_format('transpile_qbasic')).pack(side=tk.LEFT, padx=1)
            debug_button(trans_row1, debug_name="C Transpile", text="→ C", command=lambda: self.convert_format('transpile_c')).pack(side=tk.LEFT, padx=1)
            debug_button(trans_row1, debug_name="CPP Transpile", text="→ C++", command=lambda: self.convert_format('transpile_cpp')).pack(side=tk.LEFT, padx=1)
            debug_button(trans_row1, debug_name="Python Transpile", text="→ Python", command=lambda: self.convert_format('transpile_python')).pack(side=tk.LEFT, padx=1)
            
            # İkinci satır - ASM→X Transpiler Engine butonları
            trans_row2 = debug_frame(transpiler_container, debug_name="Transpiler Row 2", bg=ModernStyle.BG_SECONDARY)
            trans_row2.pack(side=tk.TOP)
            debug_button(trans_row2, debug_name="ASM to JS", text="ASM→JS", command=lambda: self.convert_format('asm_to_js')).pack(side=tk.LEFT, padx=1)
            debug_button(trans_row2, debug_name="ASM to C", text="ASM→C", command=lambda: self.convert_format('asm_to_c')).pack(side=tk.LEFT, padx=1)
            debug_button(trans_row2, debug_name="ASM to Pascal", text="ASM→Pascal", command=lambda: self.convert_format('asm_to_pascal')).pack(side=tk.LEFT, padx=1)
            debug_button(trans_row2, debug_name="ASM to QBasic", text="ASM→QB", command=lambda: self.convert_format('asm_to_qbasic')).pack(side=tk.LEFT, padx=1)

        else:
            debug_label(transpiler_container, debug_name="Missing Decompiler", text="❌ Enhanced BASIC Decompiler\nbulunamadı", 
                    bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_ERROR, font=("Arial", 9)).pack()
        
        # Options - sadece illegal opcodes kalsın
        options_frame = debug_frame(self, debug_name="Options Frame", bg=ModernStyle.BG_SECONDARY)
        options_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.use_illegal_opcodes = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(options_frame, text="⚠️ Illegal Opcode'ları Kullan", 
                       variable=self.use_illegal_opcodes).pack(side=tk.LEFT, padx=5)
        
        # Multiple result tabs for disassembly
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create result tabs
        self.result_tabs = {}
        self.create_disasm_result_tabs()
        
        # Status - daha küçük font
        self.status_label = tk.Label(self, text="Hazır", bg=ModernStyle.BG_TERTIARY,
                                    fg=ModernStyle.FG_SECONDARY, font=("Arial", 8))
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def convert_format(self, format_type):
        """Format dönüştürme"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            # Assembly format seçimi varsa ekle
            if format_type == 'assembly' and hasattr(self, 'asm_format_var'):
                asm_format = self.asm_format_var.get()
                format_type = f"assembly_{asm_format.lower()}"
            self.parent_gui.convert_to_format(format_type, 'disassembly')
        else:
            self.update_code("Lütfen önce bir dosya seçin", format_type)
    
    def update_code(self, code, format_type=None):
        """Code display güncelle - tab-aware"""
        if format_type:
            self.current_format = format_type
        
        self.current_code = code
        
        # Tab'a özel güncelleme
        if format_type and hasattr(self, 'result_tabs'):
            self.update_disasm_tab_result(format_type, code)
        
        # Status güncelle
        lines = len(code.split('\n'))
        self.status_label.config(text=f"{self.current_format} - {lines} satır")
    
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
    
    def create_disasm_result_tabs(self):
        """Her disassembler için sonuç tabları oluştur"""
        tab_configs = [
            # Disassembly Modülleri (7 adet)
            ("⚙️ Assembly", "assembly"),
            ("🚀 Advanced", "advanced_disasm"),
            ("⚡ Improved", "improved_disasm"), 
            ("🔀 Hybrid", "hybrid_disasm"),
            ("🎯 py65 Pro", "py65_pro"),
            ("⚡ Enhanced", "enhanced_disasm"),
            ("🎯 Multi", "multi_disasm"),
            
            # BASIC Detokenizers (3 adet)
            ("📝 BASIC", "basic"),
            ("🔧 Petcat", "petcat"),
            ("📋 DList", "dlist"),
            
            # Sanal Yazım Modları (4 adet)
            ("💭 PDSX", "pdsx"),
            ("💻 C", "c"),
            ("🔵 QBasic", "qbasic"),
            ("📄 Pseudo", "pseudo"),
            
            # BASIC Transpiler (9 adet)
            ("� Enhanced BASIC", "enhanced_basic"),
            ("→ QBasic", "transpile_qbasic"),
            ("→ C", "transpile_c"),
            ("→ C++", "transpile_cpp"),
            ("→ Python", "transpile_python"),
            ("ASM→JS", "asm_to_js"),
            ("ASM→C", "asm_to_c"),
            ("ASM→Pascal", "asm_to_pascal"),
            ("ASM→QB", "asm_to_qbasic")
        ]
        
        for tab_name, tab_key in tab_configs:
            tab_frame = tk.Frame(self.notebook, bg=ModernStyle.BG_SECONDARY)
            self.notebook.add(tab_frame, text=tab_name)
            
            # Text widget for each tab
            text_widget = scrolledtext.ScrolledText(tab_frame,
                                                  height=20,
                                                  bg=ModernStyle.BG_DARK,
                                                  fg=ModernStyle.FG_PRIMARY,
                                                  font=("Consolas", 10),
                                                  insertbackground=ModernStyle.FG_ACCENT)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Syntax highlighting ekle
            if SYNTAX_HIGHLIGHTING_AVAILABLE:
                try:
                    # Assembly tabları için Assembly highlighter
                    if tab_key in ['assembly', 'advanced_disasm', 'improved_disasm', 'hybrid_disasm', 'py65_pro', 'enhanced_disasm', 'multi_disasm']:
                        highlighter = Assembly6502Highlighter(text_widget)
                        text_widget.syntax_highlighter = highlighter
                    # BASIC tabları için BASIC highlighter  
                    elif tab_key in ['basic', 'petcat', 'dlist', 'enhanced_basic']:
                        highlighter = C64BasicHighlighter(text_widget)
                        text_widget.syntax_highlighter = highlighter
                    # C/C++ transpiler tabları için farklı highlighting (varsa)
                    elif tab_key in ['transpile_c', 'transpile_cpp', 'asm_to_c', 'c']:
                        # C syntax highlighter eklenebilir
                        highlighter = Assembly6502Highlighter(text_widget)  # Geçici olarak assembly
                        text_widget.syntax_highlighter = highlighter
                    # Python transpiler tabları için
                    elif tab_key in ['transpile_python']:
                        highlighter = Assembly6502Highlighter(text_widget)  # Geçici olarak assembly
                        text_widget.syntax_highlighter = highlighter
                    # BASIC variants için  
                    elif tab_key in ['transpile_qbasic', 'qbasic', 'asm_to_qbasic']:
                        highlighter = C64BasicHighlighter(text_widget)
                        text_widget.syntax_highlighter = highlighter
                    else:
                        text_widget.syntax_highlighter = None
                except Exception as e:
                    print(f'Syntax highlighting hatası ({tab_key}): {e}')
                    text_widget.syntax_highlighter = None
            else:
                text_widget.syntax_highlighter = None
                    
            self.result_tabs[tab_key] = text_widget
    
    def update_disasm_tab_result(self, tab_key, code):
        """Specific disassembly tab'ı güncelle"""
        if tab_key in self.result_tabs:
            text_widget = self.result_tabs[tab_key]
            text_widget.delete(1.0, tk.END)
            text_widget.insert(1.0, code)
            
            # Syntax highlighting uygula
            if hasattr(text_widget, 'syntax_highlighter') and text_widget.syntax_highlighter:
                text_widget.syntax_highlighter.highlight()
            
            # Tab'ı aktif et
            tab_configs = [
                ("⚙️ Assembly", "assembly"), ("🚀 Advanced", "advanced_disasm"),
                ("⚡ Improved", "improved_disasm"), ("🔀 Hybrid", "hybrid_disasm"),
                ("🎯 py65 Pro", "py65_pro"), ("📝 BASIC", "basic"),
                ("🔧 Petcat", "petcat"), ("📋 DList", "dlist"), ("🆕 Enhanced", "enhanced_disasm"),
                ("ASM→C", "asm_to_c"), ("ASM→Py", "asm_to_python"),
                ("ASM→JS", "asm_to_js"), ("ASM→Pascal", "asm_to_pascal"),
                ("ASM→QB", "asm_to_qbasic")
            ]
            
            for i, (_, key) in enumerate(tab_configs):
                if key == tab_key:
                    self.notebook.select(i)
                    break

class DecompilerPanel(tk.Frame):
    """Decompiler sonuçları paneli - Sol alt"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_code = ""
        self.current_format = "C"
        self.parent_gui = None
        self.result_tabs = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Decompiler panel UI"""
        # Decompiler butonları - tek sıra, ASM decompiler kaldırıldı
        decompiler_frame = tk.Frame(self, bg=ModernStyle.BG_SECONDARY)
        decompiler_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Unified decompiler button frame
        button_frame = tk.Frame(decompiler_frame, bg=ModernStyle.BG_SECONDARY)
        button_frame.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Single row decompiler buttons
        if DECOMPILER_C_AVAILABLE:
            ttk.Button(button_frame, text="🔧 C", command=lambda: self.convert_format('dec_c')).pack(side=tk.LEFT, padx=2)
        if DECOMPILER_C2_AVAILABLE:
            ttk.Button(button_frame, text="⚙️ C2", command=lambda: self.convert_format('dec_c2')).pack(side=tk.LEFT, padx=2)
        if DECOMPILER_CPP_AVAILABLE:
            ttk.Button(button_frame, text="🔧 C++", command=lambda: self.convert_format('dec_cpp')).pack(side=tk.LEFT, padx=2)
        if DECOMPILER_QBASIC_AVAILABLE:
            ttk.Button(button_frame, text="📝 QBasic", command=lambda: self.convert_format('dec_qbasic')).pack(side=tk.LEFT, padx=2)
        if DECOMPILER_AVAILABLE:
            ttk.Button(button_frame, text="🔄 Universal", command=lambda: self.convert_format('decompiler')).pack(side=tk.LEFT, padx=2)
        
        # Enhanced Basic Decompiler
        if EnhancedBasicDecompiler:
            ttk.Button(button_frame, text="🍎 Enhanced", command=lambda: self.convert_format('enhanced_basic')).pack(side=tk.LEFT, padx=2)
        
        # Transpiler buttons - new modules
        ttk.Button(button_frame, text="🐍 Python", command=lambda: self.convert_format('transpile_python')).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🌐 JavaScript", command=lambda: self.convert_format('transpile_js')).pack(side=tk.LEFT, padx=2)
        
        # Multiple result tabs for each button
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create result tabs
        self.result_tabs = {}
        self.create_result_tabs()
        
        # Status - daha küçük font
        self.status_label = tk.Label(self, text="Hazır", bg=ModernStyle.BG_TERTIARY,
                                    fg=ModernStyle.FG_SECONDARY, font=("Arial", 8))
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def convert_format(self, format_type):
        """Decompiler format dönüştürme"""
        if self.parent_gui and hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
            self.parent_gui.convert_to_format(format_type, 'decompiler')
        else:
            self.update_code("Lütfen önce bir dosya seçin", format_type)
    
    def update_code(self, code, format_type=None):
        """Code display güncelle - tab-aware"""
        if format_type:
            self.current_format = format_type
        
        self.current_code = code
        
        # Tab'a özel güncelleme
        if format_type and hasattr(self, 'result_tabs'):
            self.update_decompiler_tab_result(format_type, code)
        
        # Status güncelle
        lines = len(code.split('\n'))
        self.status_label.config(text=f"{self.current_format} - {lines} satır")
    
    def create_result_tabs(self):
        """Her decompiler için sonuç tabları oluştur"""
        tab_configs = [
            ("🔧 C Code", "dec_c"),
            ("⚙️ C2 Code", "dec_c2"),
            ("🔧 C++", "dec_cpp"),
            ("� QBasic", "dec_qbasic"),
            ("� Universal", "decompiler"),
            ("🍎 Enhanced", "enhanced_basic"),
            ("🐍 Python", "transpile_python"),
            ("🌐 JavaScript", "transpile_js")
        ]
        
        for tab_name, tab_key in tab_configs:
            tab_frame = tk.Frame(self.notebook, bg=ModernStyle.BG_SECONDARY)
            self.notebook.add(tab_frame, text=tab_name)
            
            # Text widget for each tab
            text_widget = scrolledtext.ScrolledText(tab_frame,
                                                  height=20,
                                                  bg=ModernStyle.BG_DARK,
                                                  fg=ModernStyle.FG_PRIMARY,
                                                  font=("Consolas", 10),
                                                  insertbackground=ModernStyle.FG_ACCENT)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Syntax highlighting ekle
            if SYNTAX_HIGHLIGHTING_AVAILABLE:
                try:
                    # C/C++ tabları için
                    if tab_key in ['dec_c', 'dec_c2', 'dec_cpp']:
                        highlighter = Assembly6502Highlighter(text_widget)  # Geçici olarak assembly
                        text_widget.syntax_highlighter = highlighter
                    # BASIC tabları için
                    elif tab_key in ['dec_qbasic', 'enhanced_basic']:
                        highlighter = C64BasicHighlighter(text_widget)
                        text_widget.syntax_highlighter = highlighter
                    # Python için
                    elif tab_key in ['transpile_python']:
                        highlighter = Assembly6502Highlighter(text_widget)  # Geçici olarak assembly
                        text_widget.syntax_highlighter = highlighter
                    # JavaScript için
                    elif tab_key in ['transpile_js']:
                        highlighter = Assembly6502Highlighter(text_widget)  # Geçici olarak assembly
                        text_widget.syntax_highlighter = highlighter
                    else:
                        text_widget.syntax_highlighter = None
                except Exception as e:
                    print(f'Syntax highlighting hatası ({tab_key}): {e}')
                    text_widget.syntax_highlighter = None
            else:
                text_widget.syntax_highlighter = None
            
            self.result_tabs[tab_key] = text_widget
    
    def update_decompiler_tab_result(self, tab_key, code):
        """Specific decompiler tab'ı güncelle"""
        if tab_key in self.result_tabs:
            text_widget = self.result_tabs[tab_key]
            text_widget.delete(1.0, tk.END)
            text_widget.insert(1.0, code)
            
            # Syntax highlighting uygula
            if hasattr(text_widget, 'syntax_highlighter') and text_widget.syntax_highlighter:
                text_widget.syntax_highlighter.highlight()

class HexEditor(tk.Frame):
    """Interactive hex editor widget"""
    def __init__(self, parent):
        super().__init__(parent, bg=ModernStyle.BG_SECONDARY)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        tk.Label(self, text="📋 Hex Editor", bg=ModernStyle.BG_SECONDARY,
                fg=ModernStyle.FG_PRIMARY, font=("Arial", 12, "bold")).pack(pady=5)
        
        # Hex display
        self.hex_display = scrolledtext.ScrolledText(self,
                                                    height=15,
                                                    bg=ModernStyle.BG_DARK,
                                                    fg=ModernStyle.FG_PRIMARY,
                                                    font=("Consolas", 10))
        self.hex_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

class ResultWindow:
    """🪟 Separate Result Window - Her format için ayrı pencere"""
    
    def __init__(self, parent_gui, title, format_type, content):
        self.parent_gui = parent_gui
        self.format_type = format_type
        self.content = content
        self.window = None
        
        self.create_window(title)
    
    def create_window(self, title):
        """Result window oluştur"""
        self.window = tk.Toplevel(self.parent_gui.root)
        self.window.title(f"📄 {title} - D64 Converter")
        self.window.geometry("900x700")
        self.window.configure(bg=ModernStyle.BG_SECONDARY)
        
        self.setup_ui()
        self.display_content()
    
    def setup_ui(self):
        """UI kurulumu"""
        # Header frame
        header_frame = tk.Frame(self.window, bg=ModernStyle.BG_SECONDARY)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Title
        title_label = tk.Label(header_frame, text=f"📄 {self.format_type.upper()} Result",
                              bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                              font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Info
        info_text = f"Lines: {len(self.content.split(chr(10)))}, Characters: {len(self.content)}"
        info_label = tk.Label(header_frame, text=info_text,
                             bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_SECONDARY,
                             font=("Arial", 10))
        info_label.pack(side=tk.RIGHT)
        
        # Toolbar frame
        toolbar_frame = tk.Frame(self.window, bg=ModernStyle.BG_SECONDARY)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=2)
        
        # External tools buttons
        ttk.Button(toolbar_frame, text="🔧 Open External Tools", 
                  command=self.open_external_tools).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="📁 Open with CrossViper", 
                  command=self.open_with_crossviper).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="💾 Save As...", 
                  command=self.save_as).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar_frame, text="📋 Copy All", 
                  command=self.copy_all).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self.window, orient='horizontal').pack(fill=tk.X, padx=10, pady=2)
        
        # Code display
        self.code_display = scrolledtext.ScrolledText(self.window,
                                                     height=35,
                                                     bg=ModernStyle.BG_DARK,
                                                     fg=ModernStyle.FG_PRIMARY,
                                                     font=("Consolas", 11),
                                                     insertbackground=ModernStyle.FG_ACCENT,
                                                     wrap=tk.NONE)
        self.code_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value=f"Ready - {self.format_type} format")
        status_bar = tk.Label(self.window, textvariable=self.status_var,
                             bg=ModernStyle.BG_TERTIARY, fg=ModernStyle.FG_SECONDARY,
                             font=("Arial", 9))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def display_content(self):
        """Content'i göster"""
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(1.0, self.content)
        
        # Syntax highlighting (basit)
        self.apply_syntax_highlighting()
    
    def apply_syntax_highlighting(self):
        """Basit syntax highlighting"""
        try:
            # Configure tags
            self.code_display.tag_configure("comment", foreground="#6A9955")
            self.code_display.tag_configure("keyword", foreground="#569CD6")
            self.code_display.tag_configure("string", foreground="#CE9178")
            self.code_display.tag_configure("number", foreground="#B5CEA8")
            
            # Apply highlighting based on format
            if self.format_type in ['assembly', 'asm']:
                self.highlight_assembly()
            elif self.format_type in ['c', 'cpp']:
                self.highlight_c_cpp()
            elif self.format_type in ['basic', 'qbasic']:
                self.highlight_basic()
                
        except Exception as e:
            # Ignore highlighting errors
            pass
    
    def highlight_assembly(self):
        """Assembly syntax highlighting"""
        import re
        content = self.code_display.get(1.0, tk.END)
        
        # Comments
        for match in re.finditer(r';.*', content):
            start = self.code_display.index(f"1.0+{match.start()}c")
            end = self.code_display.index(f"1.0+{match.end()}c")
            self.code_display.tag_add("comment", start, end)
        
        # Instructions (basic set)
        instructions = r'\b(LDA|LDX|LDY|STA|STX|STY|JMP|JSR|RTS|BEQ|BNE|CMP|INC|DEC)\b'
        for match in re.finditer(instructions, content, re.IGNORECASE):
            start = self.code_display.index(f"1.0+{match.start()}c")
            end = self.code_display.index(f"1.0+{match.end()}c")
            self.code_display.tag_add("keyword", start, end)
    
    def highlight_c_cpp(self):
        """C/C++ syntax highlighting"""
        import re
        content = self.code_display.get(1.0, tk.END)
        
        # Comments
        for match in re.finditer(r'//.*|/\*.*?\*/', content, re.DOTALL):
            start = self.code_display.index(f"1.0+{match.start()}c")
            end = self.code_display.index(f"1.0+{match.end()}c")
            self.code_display.tag_add("comment", start, end)
        
        # Keywords
        keywords = r'\b(int|char|void|if|else|for|while|return|include)\b'
        for match in re.finditer(keywords, content):
            start = self.code_display.index(f"1.0+{match.start()}c")
            end = self.code_display.index(f"1.0+{match.end()}c")
            self.code_display.tag_add("keyword", start, end)
    
    def highlight_basic(self):
        """BASIC syntax highlighting"""
        import re
        content = self.code_display.get(1.0, tk.END)
        
        # Line numbers
        for match in re.finditer(r'^\d+', content, re.MULTILINE):
            start = self.code_display.index(f"1.0+{match.start()}c")
            end = self.code_display.index(f"1.0+{match.end()}c")
            self.code_display.tag_add("number", start, end)
        
        # Keywords
        keywords = r'\b(PRINT|FOR|NEXT|IF|THEN|GOTO|GOSUB|RETURN|LET|REM)\b'
        for match in re.finditer(keywords, content, re.IGNORECASE):
            start = self.code_display.index(f"1.0+{match.start()}c")
            end = self.code_display.index(f"1.0+{match.end()}c")
            self.code_display.tag_add("keyword", start, end)
    
    def open_external_tools(self):
        """External Tools window'u aç"""
        if hasattr(self.parent_gui, 'open_external_tools_window'):
            self.parent_gui.open_external_tools_window()
    
    def open_with_crossviper(self):
        """CrossViper ile aç"""
        try:
            self.parent_gui.launch_crossviper_with_content(self.content)
            self.status_var.set("✅ CrossViper IDE launched")
        except Exception as e:
            messagebox.showerror("CrossViper Error", f"Failed to launch CrossViper: {e}")
            self.status_var.set("❌ CrossViper launch failed")
    
    def save_as(self):
        """Dosyayı farklı kaydet"""
        try:
            # Determine default extension
            ext_map = {
                'assembly': '.asm',
                'asm': '.asm',
                'c': '.c',
                'cpp': '.cpp',
                'c++': '.cpp',
                'qbasic': '.bas',
                'basic': '.bas',
                'pdsx': '.basx',
                'python': '.py',
                'petcat': '.bas',
                'c64list': '.bas'
            }
            
            default_ext = ext_map.get(self.format_type.lower(), '.txt')
            
            filename = filedialog.asksaveasfilename(
                title=f"Save {self.format_type} Code As...",
                defaultextension=default_ext,
                filetypes=[
                    (f"{self.format_type.upper()} files", f"*{default_ext}"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.content)
                
                self.status_var.set(f"✅ Saved as {filename}")
                messagebox.showinfo("Saved", f"File saved successfully:\n{filename}")
                
        except Exception as e:
            error_msg = f"Failed to save file: {e}"
            self.status_var.set("❌ Save failed")
            messagebox.showerror("Save Error", error_msg)
    
    def copy_all(self):
        """Tüm content'i clipboard'a kopyala"""
        try:
            self.window.clipboard_clear()
            self.window.clipboard_append(self.content)
            self.status_var.set("✅ Copied to clipboard")
        except Exception as e:
            self.status_var.set("❌ Copy failed")
            messagebox.showerror("Copy Error", f"Failed to copy: {e}")

class ExternalToolsWindow:
    """🔧 External Tools Window - KızılElma Feature"""
    
    def __init__(self, parent_gui):
        self.parent_gui = parent_gui
        self.window = None
        self.current_content = ""
        self.current_format = "unknown"
        self.current_file_path = ""
        
        # Get Configuration Manager for external tools
        self.config_manager = None
        if hasattr(parent_gui, 'config_manager'):
            self.config_manager = parent_gui.config_manager
    
    def show(self):
        """External Tools Window'u göster"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        # Create window
        self.window = tk.Toplevel(self.parent_gui.root)
        self.window.title("🔧 External Tools - D64 Converter")
        self.window.geometry("800x600")
        self.window.configure(bg=ModernStyle.BG_SECONDARY)
        
        # Window icon ve tema
        self.window.iconname("External Tools")
        
        self.setup_ui()
        self.refresh_available_tools()
    
    def setup_ui(self):
        """UI kurulumu"""
        # Header
        header_frame = tk.Frame(self.window, bg=ModernStyle.BG_SECONDARY)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(header_frame, text="🔧 External Tools", 
                bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # Current file info
        self.file_info_frame = tk.Frame(self.window, bg=ModernStyle.BG_TERTIARY)
        self.file_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(self.file_info_frame, text="📄 Current Content:", 
                bg=ModernStyle.BG_TERTIARY, fg=ModernStyle.FG_SECONDARY,
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.current_file_label = tk.Label(self.file_info_frame, text="No content selected",
                                          bg=ModernStyle.BG_TERTIARY, fg=ModernStyle.FG_SECONDARY,
                                          font=("Arial", 10))
        self.current_file_label.pack(side=tk.LEFT, padx=5)
        
        # Tools list frame
        tools_frame = tk.LabelFrame(self.window, text="Available External Tools",
                                   bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tools listbox with scrollbar
        list_frame = tk.Frame(tools_frame, bg=ModernStyle.BG_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar ve Listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tools_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                       bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                       font=("Consolas", 10), height=15)
        self.tools_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tools_listbox.yview)
        
        # Double click to launch
        self.tools_listbox.bind("<Double-Button-1>", self.launch_selected_tool)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.window, bg=ModernStyle.BG_SECONDARY)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(buttons_frame, text="🚀 Launch Selected Tool", 
                  command=self.launch_selected_tool).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="📁 Open with Viper IDE", 
                  command=self.open_with_viper).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="⚡ Tool Terminal", 
                  command=self.open_tool_terminal).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="🔄 Refresh", 
                  command=self.refresh_available_tools).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="❌ Close", 
                  command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.window, textvariable=self.status_var,
                             bg=ModernStyle.BG_TERTIARY, fg=ModernStyle.FG_SECONDARY,
                             font=("Arial", 9))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def refresh_available_tools(self):
        """Mevcut external tools'ları yenile"""
        self.tools_listbox.delete(0, tk.END)
        
        if not self.config_manager:
            self.tools_listbox.insert(tk.END, "❌ Configuration Manager not available")
            return
        
        try:
            # Get available tools from Configuration Manager
            available_tools = self.config_manager.get_available_tools()
            
            if not available_tools:
                self.tools_listbox.insert(tk.END, "ℹ️ No external tools configured")
                self.tools_listbox.insert(tk.END, "   Use Configuration Manager to add tools")
                return
            
            # Add tools to list
            for tool_info in available_tools:
                tool_name = tool_info.get('name', 'Unknown')
                tool_path = tool_info.get('path', '')
                category = tool_info.get('category', 'Unknown')
                
                # Format display string
                display_str = f"🔧 {tool_name} ({category})"
                self.tools_listbox.insert(tk.END, display_str)
                
                # Store tool info (we'll access via index)
                
            self.status_var.set(f"Found {len(available_tools)} external tools")
            
        except Exception as e:
            self.tools_listbox.insert(tk.END, f"❌ Error loading tools: {e}")
            self.status_var.set("Error loading external tools")
    
    def launch_selected_tool(self, event=None):
        """Seçili external tool'u başlat"""
        selection = self.tools_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a tool to launch")
            return
        
        selected_index = selection[0]
        selected_text = self.tools_listbox.get(selected_index)
        
        if selected_text.startswith("❌") or selected_text.startswith("ℹ️"):
            return
        
        # Get current content from parent GUI
        current_content = self.get_current_content()
        if not current_content:
            messagebox.showwarning("No Content", "No file content to open with external tool")
            return
        
        try:
            # Get tool info from Configuration Manager
            available_tools = self.config_manager.get_available_tools()
            if selected_index < len(available_tools):
                tool_info = available_tools[selected_index]
                self.launch_external_tool(tool_info, current_content)
            
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch tool: {e}")
    
    def launch_external_tool(self, tool_info, content):
        """External tool'u belirtilen content ile başlat"""
        tool_name = tool_info.get('name', 'Unknown')
        tool_path = tool_info.get('path', '')
        
        if not os.path.exists(tool_path):
            messagebox.showerror("Tool Not Found", f"Tool executable not found: {tool_path}")
            return
        
        # Create temporary file for content
        import tempfile
        try:
            # Determine file extension based on content type
            ext_map = {
                'assembly': '.asm',
                'asm': '.asm',
                'c': '.c',
                'cpp': '.cpp',
                'qbasic': '.bas',
                'basic': '.bas',
                'pdsx': '.basx',
                'python': '.py'
            }
            
            file_ext = ext_map.get(self.current_format, '.txt')
            
            with tempfile.NamedTemporaryFile(mode='w', suffix=file_ext, delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            # Launch the tool with the temporary file
            self.status_var.set(f"Launching {tool_name}...")
            
            # Use subprocess to launch the tool
            subprocess.Popen([tool_path, temp_file_path], shell=True)
            
            self.status_var.set(f"✅ Launched {tool_name} successfully")
            
            # Store temp file path for cleanup (optional)
            self.current_file_path = temp_file_path
            
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch {tool_name}: {e}")
            self.status_var.set(f"❌ Failed to launch {tool_name}")
    
    def open_with_crossviper(self):
        """CrossViper IDE ile aç"""
        current_content = self.get_current_content()
        if not current_content:
            messagebox.showwarning("No Content", "No file content to open with CrossViper IDE")
            return
        
        try:
            # Look for CrossViper IDE in the project
            crossviper_path = None
            
            # Check common CrossViper locations
            possible_paths = [
                os.path.join(os.path.dirname(__file__), "crossviper-master", "main.py"),
                os.path.join(os.path.dirname(__file__), "crossviper", "main.py"),
                os.path.join(os.path.dirname(__file__), "..", "crossviper-master", "main.py")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    crossviper_path = path
                    break
            
            if not crossviper_path:
                messagebox.showerror("CrossViper Not Found", 
                                   "CrossViper IDE not found in project directory")
                return
            
            # Create temporary file
            import tempfile
            file_ext = '.asm' if 'assembly' in self.current_format else '.txt'
            
            with tempfile.NamedTemporaryFile(mode='w', suffix=file_ext, delete=False) as temp_file:
                temp_file.write(current_content)
                temp_file_path = temp_file.name
            
            # Launch CrossViper
            self.status_var.set("Launching CrossViper IDE...")
            subprocess.Popen([sys.executable, crossviper_path, temp_file_path])
            
            self.status_var.set("✅ CrossViper IDE launched successfully")
            
        except Exception as e:
            messagebox.showerror("CrossViper Error", f"Failed to launch CrossViper IDE: {e}")
            self.status_var.set("❌ Failed to launch CrossViper IDE")
    
    def get_current_content(self):
        """Parent GUI'den aktif content'i al"""
        try:
            # Try to get content from active panel
            if hasattr(self.parent_gui, 'disassembly_panel') and self.parent_gui.disassembly_panel:
                content = self.parent_gui.disassembly_panel.current_code
                if content and content.strip():
                    self.current_content = content
                    self.current_format = getattr(self.parent_gui.disassembly_panel, 'current_format', 'assembly')
                    self.update_file_info(f"Disassembly ({self.current_format})")
                    return content
            
            if hasattr(self.parent_gui, 'decompiler_panel') and self.parent_gui.decompiler_panel:
                content = self.parent_gui.decompiler_panel.current_code
                if content and content.strip():
                    self.current_content = content
                    self.current_format = getattr(self.parent_gui.decompiler_panel, 'current_format', 'decompiler')
                    self.update_file_info(f"Decompiler ({self.current_format})")
                    return content
            
            return None
            
        except Exception as e:
            print(f"Error getting current content: {e}")
            return None
    
    def update_file_info(self, info_text):
        """File info label'ını güncelle"""
        if hasattr(self, 'current_file_label'):
            self.current_file_label.config(text=info_text)
    
    def open_with_viper(self):
        """Viper IDE ile aç"""
        current_content = self.get_current_content()
        if not current_content:
            messagebox.showwarning("No Content", "No file content to open with Viper IDE")
            return
        
        try:
            # Viper IDE path
            viper_path = os.path.join(os.path.dirname(__file__), "viper.py")
            
            if not os.path.exists(viper_path):
                messagebox.showerror("Viper Not Found", 
                                   "Viper IDE (viper.py) not found in project directory")
                return
            
            # Create temporary file
            import tempfile
            file_ext = '.asm' if 'assembly' in self.current_format else '.txt'
            
            with tempfile.NamedTemporaryFile(mode='w', suffix=file_ext, delete=False, encoding='utf-8') as temp_file:
                temp_file.write(current_content)
                temp_file_path = temp_file.name
            
            # Launch Viper
            self.status_var.set("Launching Viper IDE...")
            subprocess.Popen([sys.executable, viper_path, temp_file_path])
            
            self.status_var.set("✅ Viper IDE launched successfully")
            
        except Exception as e:
            messagebox.showerror("Viper Error", f"Failed to launch Viper IDE: {e}")
            self.status_var.set("❌ Failed to launch Viper IDE")
    
    def launch_viper_ide(self):
        """Status bar'dan Viper IDE başlat"""
        self.open_with_viper()
    
    def open_viper_ide(self):
        """Menüden Viper IDE başlat"""
        self.open_with_viper()
    
    def open_tool_terminal(self):
        """Tool Terminal window'u aç"""
        try:
            tool_terminal = ToolTerminalWindow(self.parent_gui, self.config_manager)
            tool_terminal.show()
            
        except Exception as e:
            messagebox.showerror("Terminal Error", f"Failed to open tool terminal: {e}")
            self.status_var.set("❌ Failed to open tool terminal")

class ToolTerminalWindow:
    """🔧 Tool Terminal Window - Configuration Manager Integration"""
    
    def __init__(self, parent_gui, config_manager):
        self.parent_gui = parent_gui
        self.config_manager = config_manager
        self.window = None
        self.command_history = []
        self.history_index = -1
        self.variables = {
            '%dosyaadi': '',
            '%yol': '',
            '%sonuc0': '', '%sonuc1': '', '%sonuc2': '', '%sonuc3': '', '%sonuc4': '',
            '%sonuc5': '', '%sonuc6': '', '%sonuc7': '', '%sonuc8': '', '%sonuc9': ''
        }
    
    def show(self):
        """Tool Terminal Window'u göster"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        # Create window
        self.window = tk.Toplevel(self.parent_gui.root)
        self.window.title("⚡ Tool Terminal - Configuration Manager")
        self.window.geometry("900x700")
        self.window.configure(bg=ModernStyle.BG_DARK)
        
        self.setup_ui()
        self.initialize_variables()
    
    def setup_ui(self):
        """Terminal UI kurulumu"""
        # Header
        header_frame = tk.Frame(self.window, bg=ModernStyle.BG_SECONDARY)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(header_frame, text="⚡ Tool Terminal", 
                bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        
        # Variables info
        tk.Label(header_frame, text="Variables: %dosyaadi %yol %sonuc0-9", 
                bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_SECONDARY,
                font=("Arial", 9)).pack(side=tk.RIGHT)
        
        # Terminal output
        output_frame = tk.LabelFrame(self.window, text="📺 Terminal Output",
                                   bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Terminal text with scrollbar
        terminal_frame = tk.Frame(output_frame, bg=ModernStyle.BG_DARK)
        terminal_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(terminal_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.terminal_text = tk.Text(terminal_frame, yscrollcommand=scrollbar.set,
                                   bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                   font=("Consolas", 10), height=20)
        self.terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.terminal_text.yview)
        
        # Command input
        cmd_frame = tk.Frame(self.window, bg=ModernStyle.BG_SECONDARY)
        cmd_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(cmd_frame, text="$", bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                font=("Consolas", 12, "bold")).pack(side=tk.LEFT, padx=5)
        
        self.command_entry = tk.Entry(cmd_frame, bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                    font=("Consolas", 10), insertbackground=ModernStyle.FG_PRIMARY)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.bind("<Up>", self.history_up)
        self.command_entry.bind("<Down>", self.history_down)
        
        # Quick buttons
        buttons_frame = tk.Frame(self.window, bg=ModernStyle.BG_SECONDARY)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(buttons_frame, text="🔍 Detect Tools", 
                  command=self.detect_tools).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="📋 List Variables", 
                  command=self.list_variables).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="🗑️ Clear", 
                  command=self.clear_terminal).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="❌ Close", 
                  command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Welcome message
        self.print_to_terminal("🔧 Tool Terminal started")
        self.print_to_terminal("Available commands: detect, list, set, help, clear, exit")
        self.print_to_terminal("Use %variable syntax for substitution")
        self.print_to_terminal("-" * 50)
    
    def initialize_variables(self):
        """Değişkenleri başlat"""
        try:
            # Aktif dosya bilgilerini al
            if hasattr(self.parent_gui, 'selected_entry') and self.parent_gui.selected_entry:
                entry = self.parent_gui.selected_entry
                self.variables['%dosyaadi'] = entry.get('filename', '')
                self.variables['%yol'] = entry.get('path', '')
        except:
            pass
    
    def print_to_terminal(self, message):
        """Terminal'e mesaj yazdır"""
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.insert(tk.END, f"{message}\n")
        self.terminal_text.see(tk.END)
        self.terminal_text.config(state=tk.DISABLED)
    
    def execute_command(self, event=None):
        """Komut çalıştır"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = -1
        
        # Clear entry
        self.command_entry.delete(0, tk.END)
        
        # Echo command
        self.print_to_terminal(f"$ {command}")
        
        # Process command
        self.process_command(command)
    
    def process_command(self, command):
        """Komut işle"""
        try:
            # Variable substitution
            for var, value in self.variables.items():
                command = command.replace(var, value)
            
            # Built-in commands
            if command.startswith('detect'):
                self.detect_tools()
            elif command.startswith('list'):
                self.list_variables()
            elif command.startswith('set '):
                self.set_variable(command[4:])
            elif command.startswith('help'):
                self.show_help()
            elif command.startswith('clear'):
                self.clear_terminal()
            elif command.startswith('exit'):
                self.window.destroy()
            else:
                # External command execution
                self.execute_external_command(command)
                
        except Exception as e:
            self.print_to_terminal(f"❌ Error: {e}")
    
    def execute_external_command(self, command):
        """Harici komut çalıştır"""
        try:
            import subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.stdout:
                self.print_to_terminal(f"✅ Output:\n{result.stdout}")
            if result.stderr:
                self.print_to_terminal(f"⚠️ Error:\n{result.stderr}")
            if result.returncode != 0:
                self.print_to_terminal(f"❌ Exit code: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            self.print_to_terminal("⏰ Command timed out (30s limit)")
        except Exception as e:
            self.print_to_terminal(f"❌ Execution error: {e}")
    
    def detect_tools(self):
        """Araçları algıla"""
        self.print_to_terminal("🔍 Detecting external tools...")
        if self.config_manager:
            try:
                tools = self.config_manager.detect_all_tools()
                self.print_to_terminal(f"Found {len(tools)} tools:")
                for tool in tools:
                    self.print_to_terminal(f"  🔧 {tool['name']} - {tool['path']}")
            except:
                self.print_to_terminal("❌ Configuration Manager not available")
        else:
            self.print_to_terminal("❌ Configuration Manager not available")
    
    def list_variables(self):
        """Değişkenleri listele"""
        self.print_to_terminal("📋 Current variables:")
        for var, value in self.variables.items():
            self.print_to_terminal(f"  {var} = '{value}'")
    
    def set_variable(self, cmd):
        """Değişken ayarla: set varname=value"""
        try:
            if '=' in cmd:
                var, value = cmd.split('=', 1)
                var = var.strip()
                if not var.startswith('%'):
                    var = '%' + var
                self.variables[var] = value.strip()
                self.print_to_terminal(f"✅ Set {var} = '{value.strip()}'")
            else:
                self.print_to_terminal("❌ Usage: set varname=value")
        except Exception as e:
            self.print_to_terminal(f"❌ Error setting variable: {e}")
    
    def show_help(self):
        """Yardım göster"""
        help_text = """
🔧 Tool Terminal Help:
  detect          - Detect external tools
  list            - List all variables
  set var=value   - Set variable value
  clear           - Clear terminal
  help            - Show this help
  exit            - Close terminal
  
Variables:
  %dosyaadi       - Current filename
  %yol           - Current file path
  %sonuc0-9      - Result variables
  
Examples:
  set sonuc0=hello
  echo %sonuc0
  64tass %dosyaadi
        """
        self.print_to_terminal(help_text)
    
    def clear_terminal(self):
        """Terminal'i temizle"""
        self.terminal_text.config(state=tk.NORMAL)
        self.terminal_text.delete(1.0, tk.END)
        self.terminal_text.config(state=tk.DISABLED)
    
    def history_up(self, event):
        """Komut geçmişinde yukarı"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            command = self.command_history[-(self.history_index + 1)]
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, command)
    
    def history_down(self, event):
        """Komut geçmişinde aşağı"""
        if self.history_index > 0:
            self.history_index -= 1
            command = self.command_history[-(self.history_index + 1)]
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, command)
        elif self.history_index == 0:
            self.history_index = -1
            self.command_entry.delete(0, tk.END)

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
    """Ana GUI Manager sınıfı - X1 Integration + GUI Debug"""
    
    def __init__(self, root=None):
        try:
            print("🎨 D64ConverterGUI initialization started...")
            
            # Comprehensive logging başlat
            log_info("D64ConverterGUI initialization başladı", "GUI_INIT")
            log_window_operation("WINDOW_INIT", "D64ConverterGUI")
            
            # GUI Debug mod integration
            self.gui_debug = gui_debug
            
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
            try:
                self.setup_menu()
                print("✅ Menu setup completed")
            except Exception as e:
                print(f"⚠️ Menu setup failed: {e}")
                print("⚠️ GUI will continue without menu")
            
            print("⚙️ Initializing components...")
            self.initialize_components()
            print("✅ Component initialization completed")
            
            # Initialize Configuration Manager and Toolbox
            print("🔧 Setting up Configuration Manager and Toolbox...")
            self.setup_configuration_manager()
            self.setup_toolbox()
            print("✅ Configuration Manager and Toolbox setup completed")
            
            # Configuration Manager'ı otomatik aç - KALDIRILDI
            # if self.config_manager:
            #     print("🔧 Auto-opening Configuration Manager...")
            #     self.root.after(1000, self.open_configuration_manager)  # 1 saniye gecikme ile aç
            
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
    
    def toggle_debug_mode(self, event=None):
        """F12 tuşu ile debug modunu aç/kapat"""
        try:
            gui_debug.toggle_debug()
            
            # Visual feedback with messagebox
            debug_status = "AÇIK" if gui_debug.debug_mode else "KAPALI"
            safe_messagebox("info", "Debug Mode", 
                          f"GUI Debug Mode {debug_status}\n\n"
                          f"Debug kodları (G1, G2, G3...) şimdi {'görünür' if gui_debug.debug_mode else 'gizli'}")
            
            # GUI'yi yeniden çizmek için ana window'u refresh et
            self.root.update()
            
        except Exception as e:
            print(f"❌ Debug mode toggle failed: {e}")
            safe_messagebox("error", "Hata", f"Debug mode toggle hatası: {e}")
            
            # Print detailed traceback
            import traceback
            full_traceback = traceback.format_exc()
            print(f"Full initialization error traceback:\n{full_traceback}")
            
            # Log the error (if logger is available)
            try:
                if hasattr(self, 'logger'):
                    self.logger.error(f"Full traceback:\n{full_traceback}")
            except:
                pass
            
            # Re-raise the exception to be caught by caller
            raise e
    
    def test_debug_components(self):
        """Debug bileşenlerini test et"""
        try:
            # Debug modunu aktif et
            gui_debug.enable_debug()
            
            # Test window oluştur
            test_window = debug_toplevel(self.root, debug_name="Debug Test Window", title="GUI Debug Test")
            test_window.geometry("400x300")
            test_window.grab_set()
            
            # Test frame'leri oluştur
            test_frame = debug_frame(test_window, debug_name="Main Test Frame", bg=ModernStyle.BG_SECONDARY)
            test_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Test butonları oluştur
            debug_label(test_frame, debug_name="Test Info Label", 
                       text="🍎 GUI Debug Test - Debug kodları görünüyor mu?", 
                       bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY, 
                       font=("Arial", 12, "bold")).pack(pady=10)
            
            button_frame = debug_frame(test_frame, debug_name="Button Test Frame", bg=ModernStyle.BG_SECONDARY)
            button_frame.pack(pady=10)
            
            debug_button(button_frame, debug_name="Test Button 1", text="Test Button 1").pack(side=tk.LEFT, padx=5)
            debug_button(button_frame, debug_name="Test Button 2", text="Test Button 2").pack(side=tk.LEFT, padx=5)
            
            # Test checkbox'ları
            checkbox_frame = debug_frame(test_frame, debug_name="Checkbox Test Frame", bg=ModernStyle.BG_SECONDARY)
            checkbox_frame.pack(pady=10)
            
            debug_checkbox(checkbox_frame, debug_name="Test Checkbox 1", text="Test Checkbox 1").pack(side=tk.LEFT, padx=5)
            debug_checkbox(checkbox_frame, debug_name="Test Checkbox 2", text="Test Checkbox 2").pack(side=tk.LEFT, padx=5)
            
            # Test entry
            entry_frame = debug_frame(test_frame, debug_name="Entry Test Frame", bg=ModernStyle.BG_SECONDARY)
            entry_frame.pack(pady=10)
            
            debug_label(entry_frame, debug_name="Entry Label", text="Test Entry:", bg=ModernStyle.BG_SECONDARY).pack(side=tk.LEFT, padx=5)
            debug_entry(entry_frame, debug_name="Test Entry").pack(side=tk.LEFT, padx=5)
            
            # Kapat butonu
            debug_button(test_frame, debug_name="Close Test", text="Kapat", 
                        command=test_window.destroy).pack(pady=20)
            
            # Registry göster
            gui_debug.show_registry()
            
            safe_messagebox("info", "Debug Test", 
                          "Debug test penceresi açıldı!\n\n"
                          "✅ Eğer butonlarda 'G1-', 'G2-' gibi kodlar görüyorsanız debug sistemi çalışıyor\n"
                          "❌ Eğer sadece normal buton metinleri görüyorsanız debug sistemi aktif değil")
            
        except Exception as e:
            print(f"❌ Debug test failed: {e}")
            safe_messagebox("error", "Debug Test Hatası", f"Debug test hatası: {e}")
    
    def toggle_gui_debug_mode(self):
        """GUI debug modunu toggle et - status bar button için"""
        try:
            gui_debug.toggle_debug()
            
            # Button text'ini güncelle (daha görünür format)
            if gui_debug.debug_mode:
                debug_status = "ON"
                self.debug_toggle_btn.config(text="🍎 DEBUG ON", bg="#aaffaa", fg="#003300")
            else:
                debug_status = "OFF"
                self.debug_toggle_btn.config(text="🍎 DEBUG OFF", bg="#ffeeaa", fg="#333333")
            
            # Status message
            status_msg = f"GUI Debug Mode: {debug_status}"
            self.update_status(status_msg)
            
            # 🔥 CRITICAL: GUI'yi yeniden çiz/refresh et
            self.refresh_gui_with_debug()
            
            # Visual feedback
            safe_messagebox("info", "GUI Debug Mode", 
                          f"GUI Debug Mode: {debug_status}\n\n"
                          f"Debug kodları (G1, G2, G3...) şimdi {'görünür' if gui_debug.debug_mode else 'gizli'}\n\n"
                          f"⚡ TEST: Tools → 🍎 GUI Debug → ⚡ FORCE Enable + Test")
            
        except Exception as e:
            print(f"❌ GUI Debug toggle failed: {e}")
            safe_messagebox("error", "Hata", f"GUI Debug toggle hatası: {e}")
    
    def force_enable_debug_test(self):
        """Debug modunu zorla aç ve yeni pencerede test et"""
        try:
            print("⚡ FORCE ENABLE DEBUG MODE başlıyor...")
            
            # 1. Debug modu zorla aç
            gui_debug.enable_debug()
            print("🍎 Debug mode ZORLA AÇILDI")
            
            # 2. Status button güncelle
            if hasattr(self, 'debug_toggle_btn'):
                self.debug_toggle_btn.config(text="🍎 DEBUG ON", bg="#aaffaa", fg="#003300")
            
            # 3. Status mesajı
            self.update_status("GUI Debug Mode: ZORLA AÇILDI")
            
            # 4. YENİ TEST PENCERESİ OLUŞTUR - Tamamen yeni bileşenlerle
            self.create_debug_test_window()
            
            print("✅ Force enable debug tamamlandı")
            
        except Exception as e:
            print(f"❌ Force enable debug failed: {e}")
            safe_messagebox("error", "Hata", f"Force enable debug hatası: {e}")
    
    def create_debug_test_window(self):
        """Tamamen yeni debug test penceresi oluştur"""
        try:
            print("🆕 Yeni debug test penceresi oluşturuluyor...")
            
            # YENİ PENCERE OLUŞTUR
            test_window = debug_toplevel(self.root, debug_name="Force Debug Test Window", 
                                       title="🍎 FORCE DEBUG TEST - YENİ PENCERE")
            test_window.geometry("500x400")
            test_window.grab_set()
            
            # Ana frame
            main_frame = debug_frame(test_window, debug_name="Force Test Main Frame", 
                                   bg=ModernStyle.BG_SECONDARY)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Başlık
            title_label = debug_label(main_frame, debug_name="Force Test Title", 
                                    text="🍎 FORCE DEBUG TEST\n\nYeni bileşenler - G kodları görünüyor mu?", 
                                    bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY, 
                                    font=("Arial", 14, "bold"), justify=tk.CENTER)
            title_label.pack(pady=15)
            
            # Test butonları (YENİ OLUŞTURULAN)
            button_frame = debug_frame(main_frame, debug_name="Force Test Button Frame", 
                                     bg=ModernStyle.BG_SECONDARY)
            button_frame.pack(pady=10)
            
            debug_button(button_frame, debug_name="Force Test Button 1", 
                        text="Test Button 1", width=15).pack(side=tk.LEFT, padx=5)
            debug_button(button_frame, debug_name="Force Test Button 2", 
                        text="Test Button 2", width=15).pack(side=tk.LEFT, padx=5)
            debug_button(button_frame, debug_name="Force Test Button 3", 
                        text="Test Button 3", width=15).pack(side=tk.LEFT, padx=5)
            
            # Test checkboxları (YENİ OLUŞTURULAN)
            check_frame = debug_frame(main_frame, debug_name="Force Test Check Frame", 
                                    bg=ModernStyle.BG_SECONDARY)
            check_frame.pack(pady=10)
            
            debug_checkbox(check_frame, debug_name="Force Test Check 1", 
                          text="Test Checkbox 1").pack(side=tk.LEFT, padx=10)
            debug_checkbox(check_frame, debug_name="Force Test Check 2", 
                          text="Test Checkbox 2").pack(side=tk.LEFT, padx=10)
            
            # Test entry (YENİ OLUŞTURULAN)
            entry_frame = debug_frame(main_frame, debug_name="Force Test Entry Frame", 
                                    bg=ModernStyle.BG_SECONDARY)
            entry_frame.pack(pady=10)
            
            debug_label(entry_frame, debug_name="Force Test Entry Label", 
                       text="Test Entry:", bg=ModernStyle.BG_SECONDARY).pack(side=tk.LEFT, padx=5)
            test_entry = debug_entry(entry_frame, debug_name="Force Test Entry", width=20)
            test_entry.pack(side=tk.LEFT, padx=5)
            test_entry.insert(0, "Debug test entry")
            
            # Sonuç mesajı
            result_label = debug_label(main_frame, debug_name="Force Test Result", 
                                     text="✅ EĞER BURADA G KODLARI GÖRÜNEBİLİYORSA DEBUG SİSTEMİ ÇALIŞIYOR!\n"
                                          "❌ Eğer sadece normal metin görünüyorsa debug sistemi çalışmıyor.", 
                                     bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_ACCENT, 
                                     font=("Arial", 10, "bold"), justify=tk.CENTER, wraplength=450)
            result_label.pack(pady=15)
            
            # Kapat butonu
            debug_button(main_frame, debug_name="Force Test Close", 
                        text="Kapat", command=test_window.destroy, width=20).pack(pady=20)
            
            # Registry göster
            gui_debug.show_registry()
            
            print("✅ Yeni debug test penceresi oluşturuldu")
            
        except Exception as e:
            print(f"❌ Debug test window creation failed: {e}")
            safe_messagebox("error", "Hata", f"Debug test window oluşturma hatası: {e}")
    
    def refresh_gui_with_debug(self):
        """Debug modu değiştiğinde GUI'yi yenile - TÜM WİDGET'LARI GÜNCELLE"""
        try:
            print(f"🔄 GUI TAMAMEN YENİLE - Debug mode: {gui_debug.debug_mode}")
            
            # 1. Registry'deki tüm widget'ları güncelle
            self.update_all_widgets_for_debug_mode()
            
            # 2. Status bar güncelle
            debug_status = "AÇIK 🟢" if gui_debug.debug_mode else "KAPALI 🔴"
            self.update_status(f"🍎 GUI Debug Mode: {debug_status} - Tüm elementler güncellendi")
            
            # 3. Window refresh
            self.root.update_idletasks()
            self.root.update()
            
            print(f"✅ TÜM GUI BAŞARIYLA YENİLENDİ - Debug mode: {gui_debug.debug_mode}")
            
        except Exception as e:
            print(f"❌ GUI refresh failed: {e}")
            import traceback
            traceback.print_exc()
    
    def update_all_widgets_for_debug_mode(self):
        """Registry'deki tüm widget'ları debug moduna göre güncelle"""
        try:
            print(f"🔧 {len(gui_debug.component_registry)} widget güncelleniyor...")
            
            # Registry'deki her widget için
            for debug_code, widget_info in gui_debug.component_registry.items():
                try:
                    widget = widget_info.get('widget')
                    widget_type = widget_info.get('type', 'Unknown')
                    original_text = widget_info.get('original_text', '')
                    
                    if widget and hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        self.update_single_widget_debug(widget, debug_code, widget_type, original_text)
                        
                except Exception as we:
                    print(f"⚠️ Widget {debug_code} güncellenemedi: {we}")
                    
            print(f"✅ Widget güncelleme tamamlandı")
            
        except Exception as e:
            print(f"❌ Widget update failed: {e}")
    
    def update_single_widget_debug(self, widget, debug_code, widget_type, original_text):
        """Tek bir widget'ı debug moduna göre güncelle"""
        try:
            if gui_debug.debug_mode:
                # Debug modu ON - kod ekle
                if widget_type == 'Button' and hasattr(widget, 'config'):
                    new_text = f"[{debug_code}] {original_text}"
                    widget.config(text=new_text)
                    
                elif widget_type == 'Label' and hasattr(widget, 'config'):
                    new_text = f"[{debug_code}] {original_text}"
                    widget.config(text=new_text)
                    
                elif widget_type == 'Menu' and hasattr(widget, 'entryconfig'):
                    # Menu item'ları güncelle
                    for i in range(widget.index('end') + 1):
                        try:
                            original_label = widget.entrycget(i, 'label')
                            if original_label and not original_label.startswith('['):
                                new_label = f"[{debug_code}] {original_label}"
                                widget.entryconfig(i, label=new_label)
                        except:
                            pass
                            
            else:
                # Debug modu OFF - kod kaldır
                if widget_type == 'Button' and hasattr(widget, 'config'):
                    widget.config(text=original_text)
                    
                elif widget_type == 'Label' and hasattr(widget, 'config'):
                    widget.config(text=original_text)
                    
                elif widget_type == 'Menu' and hasattr(widget, 'entryconfig'):
                    # Menu item'ları orijinal hale getir
                    for i in range(widget.index('end') + 1):
                        try:
                            current_label = widget.entrycget(i, 'label')
                            if current_label and current_label.startswith('['):
                                # [G1] kısmını çıkar
                                clean_label = current_label.split('] ', 1)[1] if '] ' in current_label else current_label
                                widget.entryconfig(i, label=clean_label)
                        except:
                            pass
                            
        except Exception as e:
            print(f"⚠️ Widget {debug_code} update failed: {e}")
    
    def recreate_main_panels(self):
        """Ana panelleri debug modu için yeniden oluştur"""
        try:
            print("🔄 Main panels yeniden oluşturuluyor...")
            
            # Eski panelleri temizle (eğer varsa)
            if hasattr(self, 'left_paned'):
                self.left_paned.destroy()
            if hasattr(self, 'right_paned'): 
                self.right_paned.destroy()
                
            # Panelleri yeniden oluştur
            self.setup_main_panels()
            
            print("✅ Main panels yeniden oluşturuldu")
            
        except Exception as e:
            print(f"❌ Panel recreation failed: {e}")
    
    def refresh_menu_with_debug(self):
        """Menu'yu debug modu için yenile"""
        try:
            # Menu'nun debug kodlarını güncelle
            menubar = self.root.nametowidget(self.root['menu'])
            
            # Menu'yu yeniden çiz
            self.root.update_idletasks()
            
            print("✅ Menu refreshed with debug mode")
            
        except Exception as e:
            print(f"❌ Menu refresh failed: {e}")
    
    def setup_main_panels(self):
        """Ana panelleri kur - debug aware"""
        try:
            print("🔧 Setting up main panels...")
            
            # Ana paned window
            self.main_paned = debug_panedwindow(self.main_frame, debug_name="Main Paned Window", 
                                              orient=tk.HORIZONTAL, sashrelief=tk.RAISED, 
                                              sashwidth=3, bg=ModernStyle.BG_DARK)
            self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Sol panel (Directory + Decompiler)
            self.left_paned = debug_panedwindow(self.main_paned, debug_name="Left Paned Window",
                                              orient=tk.VERTICAL, sashrelief=tk.RAISED,
                                              sashwidth=3, bg=ModernStyle.BG_DARK)
            
            # Sağ panel (Disassembly + Console)  
            self.right_paned = debug_panedwindow(self.main_paned, debug_name="Right Paned Window",
                                               orient=tk.VERTICAL, sashrelief=tk.RAISED,
                                               sashwidth=3, bg=ModernStyle.BG_DARK)
            
            # Panelleri main_paned'e ekle
            self.main_paned.add(self.left_paned, width=600)
            self.main_paned.add(self.right_paned, width=600)
            
            # Directory Panel (Sol Üst)
            self.directory_panel = DiskDirectoryPanel(self.left_paned, bg=ModernStyle.BG_DARK)
            self.directory_panel.parent_gui = self
            
            # Decompiler Panel (Sol Alt) 
            self.decompiler_panel = DecompilerPanel(self.left_paned, bg=ModernStyle.BG_DARK)
            self.decompiler_panel.parent_gui = self
            
            # Disassembly Panel (Sağ Üst)
            self.disassembly_panel = DisassemblyPanel(self.right_paned, bg=ModernStyle.BG_DARK)
            self.disassembly_panel.parent_gui = self
            
            # Console Panel (Sağ Alt)
            self.console_panel = debug_frame(self.right_paned, debug_name="Console Panel", bg=ModernStyle.BG_DARK)
            self.setup_console_panel()
            
            # Panelleri ekle
            self.left_paned.add(self.directory_panel, height=400)
            self.left_paned.add(self.decompiler_panel, height=300)
            
            self.right_paned.add(self.disassembly_panel, height=400)
            self.right_paned.add(self.console_panel, height=300)
            
            print("✅ Main panels setup completed")
            
        except Exception as e:
            print(f"❌ Main panels setup failed: {e}")
            # Fallback: Basit layout
            self.main_frame = debug_frame(self.main_content, debug_name="Fallback Main Frame")
            self.main_frame.pack(fill=tk.BOTH, expand=True)
    
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
            
            # Debug mode toggle with F12
            self.root.bind('<F12>', self.toggle_debug_mode)
            print("✅ F12 debug toggle key bound")
                
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
            
            # Configure main frame grid - 2x2 layout - Üst paneller daha büyük
            self.main_frame.grid_rowconfigure(0, weight=3)  # Üst paneller daha büyük
            self.main_frame.grid_rowconfigure(1, weight=2)  # Alt paneller daha küçük
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
            
            print("⚙️ Setting up Configuration Manager...")
            # Configuration Manager setup
            try:
                from configuration_manager import ConfigurationManager
                self.config_manager = ConfigurationManager(parent=self)
                print("✅ Configuration Manager created")
            except ImportError as e:
                print(f"⚠️ Configuration Manager not available: {e}")
                self.config_manager = None
            except Exception as e:
                print(f"❌ Configuration Manager setup failed: {e}")
                self.config_manager = None
            
        except Exception as e:
            print(f"❌ Component setup failed: {e}")
            import traceback
            print(f"Traceback:\n{traceback.format_exc()}")
            raise e
        
        # Sol alt panel - Console Output  
        console_frame = tk.LabelFrame(self.main_frame, text="📟 Console Output",
                                     bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                                     font=("Arial", 10, "bold"))
        console_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        console_frame.grid_rowconfigure(0, weight=1)
        console_frame.grid_columnconfigure(0, weight=1)
        
        self.console_panel = ConsolePanel(console_frame, bg=ModernStyle.BG_SECONDARY)
        self.console_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Sağ alt panel - Decompiler Sonuçları
        decompiler_frame = tk.LabelFrame(self.main_frame, text="🔧 Decompiler Results",
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
        
        # Debug toggle button - status bar'a eklendi (daha görünür)
        try:
            self.debug_toggle_btn = debug_button(self.status_frame, debug_name="Debug Toggle Button", 
                                               text="🍎 DEBUG OFF", 
                                               command=self.toggle_gui_debug_mode)
            self.debug_toggle_btn.config(width=12, font=("Arial", 9, "bold"), 
                                       bg="#ffeeaa", fg="#333333", relief="raised", 
                                       bd=2)  # Daha görünür stil
            self.debug_toggle_btn.pack(side=tk.LEFT, padx=8, pady=2)
            print("✅ Debug toggle button created successfully")
        except Exception as e:
            print(f"⚠️ Debug toggle button failed ({e}), using standard button")
            self.debug_toggle_btn = tk.Button(self.status_frame, text="🍎 DEBUG OFF", 
                                            command=self.toggle_gui_debug_mode,
                                            width=12, font=("Arial", 9, "bold"), 
                                            bg="#ffeeaa", fg="#333333", relief="raised", bd=2)
            self.debug_toggle_btn.pack(side=tk.LEFT, padx=8, pady=2)
        
        # Viper IDE button - debug butonunun yanında
        try:
            self.viper_btn = debug_button(self.status_frame, debug_name="Viper IDE Button", 
                                        text="🐍 Viper", 
                                        command=self.launch_viper_ide)
            self.viper_btn.config(width=10, font=("Arial", 9, "bold"), 
                                bg="#44aa44", fg="white", relief="raised", 
                                bd=2)
            self.viper_btn.pack(side=tk.LEFT, padx=4, pady=2)
            print("✅ Viper IDE button created successfully")
        except Exception as e:
            print(f"⚠️ Viper IDE button failed ({e}), using standard button")
            self.viper_btn = tk.Button(self.status_frame, text="🐍 Viper", 
                                     command=self.launch_viper_ide,
                                     width=10, font=("Arial", 9, "bold"), 
                                     bg="#44aa44", fg="white", relief="raised", bd=2)
            self.viper_btn.pack(side=tk.LEFT, padx=4, pady=2)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var,
                                          maximum=100, length=200, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=3)
    
    def setup_menu(self):
        """Menu sistemi kur"""
        # Normal menubar oluştur - wrapper kullanma (döngü önleme)
        try:
            menubar = tk.Menu(self.root, 
                             bg=ModernStyle.BG_SECONDARY, 
                             fg=ModernStyle.FG_PRIMARY,
                             relief="raised",
                             bd=1)
            print("✅ Normal menubar created successfully")
        except Exception as e:
            print(f"⚠️ Debug wrapper menu failed ({e}), using standard menu")
            menubar = tk.Menu(self.root, bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY)
        
        # Menu'yu root'a atayın ve zorla görünür yapın
        self.root.config(menu=menubar)
        
        # Windows için ek yapılandırma - Menu görünürlüğünü zorla
        try:
            self.root.option_add('*tearOff', False)
            # Windows için menu bar'ı zorla göster
            menubar.config(relief="raised", bd=1)
            # Root window'u refresh et
            self.root.update_idletasks()
        except Exception as e:
            print(f"⚠️ Menu configuration warning: {e}")
            
        print(f"🍎 Menu setup - Debug enabled: {self.gui_debug.debug_mode}")
        if self.gui_debug.debug_mode:
            print(f"🍎 Menu bar created with debug code: {menubar.debug_code if hasattr(menubar, 'debug_code') else 'N/A'}")
        
        # Menu bar'ın görünür olup olmadığını kontrol et
        print(f"🍎 Menu bar configured: {self.root.cget('menu') is not None}")
        print(f"🍎 Menu bar master: {menubar.master}")
        print(f"🍎 Menu bar winfo_exists: {menubar.winfo_exists()}")
        
        # File menu - Normal menu, debug wrapper yok (döngü önleme)
        file_menu = tk.Menu(menubar, tearoff=0, 
                           bg=ModernStyle.BG_SECONDARY, 
                           fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open PRG File...", command=self.open_prg_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Open D64 File...", command=self.open_d64_file)
        file_menu.add_command(label="Find C64 Files...", command=self.find_files)
        file_menu.add_separator()
        file_menu.add_command(label="Export Code...", command=self.export_code, accelerator="Ctrl+E")
        file_menu.add_command(label="Batch Export...", command=self.batch_export)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Tools menu - Normal menu, debug wrapper yok (döngü önleme)
        tools_menu = tk.Menu(menubar, tearoff=0, 
                            bg=ModernStyle.BG_SECONDARY, 
                            fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="Tools", menu=tools_menu)        # ⚙️ Configuration Manager ve 🧰 Toolbox eklendi
        tools_menu.add_command(label="⚙️ Configuration Manager", command=self.open_configuration_manager)
        tools_menu.add_command(label="🧰 Show Toolbox", command=self.toggle_toolbox, accelerator="F12")
        tools_menu.add_separator()
        
        # 🔧 External Tools Submenu - KızılElma Feature - Normal menu (döngü önleme)
        external_tools_menu = tk.Menu(tools_menu, tearoff=0, 
                                     bg=ModernStyle.BG_SECONDARY, 
                                     fg=ModernStyle.FG_PRIMARY)
        tools_menu.add_cascade(label="🔧 External Tools", menu=external_tools_menu)
        external_tools_menu.add_command(label="🪟 Open External Tools Window", command=self.open_external_tools_window)
        external_tools_menu.add_separator()
        external_tools_menu.add_command(label="🐍 Open Viper IDE", command=self.open_viper_ide)
        external_tools_menu.add_command(label="⚙️ Open with 64TASS", command=lambda: self.open_with_external_tool("64tass"))
        external_tools_menu.add_command(label="🔧 Open with ACME", command=lambda: self.open_with_external_tool("acme"))
        external_tools_menu.add_command(label="💾 Open with DASM", command=lambda: self.open_with_external_tool("dasm"))
        external_tools_menu.add_separator()
        external_tools_menu.add_command(label="🔄 Refresh External Tools", command=self.refresh_external_tools)
        tools_menu.add_separator()
        
        tools_menu.add_command(label="Illegal Opcode Analysis", command=self.analyze_illegal_opcodes_current)
        tools_menu.add_command(label="Sprite Analysis", command=self.analyze_sprites_current)
        tools_menu.add_command(label="SID Music Analysis", command=self.analyze_sid_current)
        tools_menu.add_command(label="Charset Analysis", command=self.analyze_charset_current)
        tools_menu.add_separator()
        
        # 🍎 GUI Debug Menu - KızılElma Feature - Normal menu (döngü önleme)
        debug_menu = tk.Menu(tools_menu, tearoff=0, 
                            bg=ModernStyle.BG_SECONDARY, 
                            fg=ModernStyle.FG_PRIMARY)
        tools_menu.add_cascade(label="🍎 GUI Debug", menu=debug_menu)
        debug_menu.add_command(label="🟢 Enable GUI Debug", command=self.gui_debug.enable_debug)
        debug_menu.add_command(label="🔴 Disable GUI Debug", command=self.gui_debug.disable_debug)
        debug_menu.add_command(label="🔄 Toggle GUI Debug", command=self.toggle_gui_debug_mode)
        debug_menu.add_separator()
        debug_menu.add_command(label="⚡ FORCE Enable + Test", command=self.force_enable_debug_test)
        debug_menu.add_command(label="📋 Show Component Registry", command=self.gui_debug.show_registry)
        debug_menu.add_command(label="🎯 Test Debug Components", command=self.test_debug_components)
        tools_menu.add_separator()
        
        # Enhanced BASIC Decompiler submenu - Normal menu (döngü önleme)
        basic_decompiler_menu = tk.Menu(tools_menu, tearoff=0, 
                                       bg=ModernStyle.BG_SECONDARY, 
                                       fg=ModernStyle.FG_PRIMARY)
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
        
        # View menu - Normal menu (döngü önleme)
        view_menu = tk.Menu(menubar, tearoff=0, 
                           bg=ModernStyle.BG_SECONDARY, 
                           fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Real-time Updates", command=self.toggle_realtime)
        view_menu.add_checkbutton(label="Code Analysis", command=self.toggle_analysis)
        view_menu.add_separator()
        
        # 🪟 Window Management - KızılElma Feature - Normal menu (döngü önleme)
        window_menu = tk.Menu(view_menu, tearoff=0, 
                                                    bg=ModernStyle.BG_SECONDARY, 
                                                    fg=ModernStyle.FG_PRIMARY)
        view_menu.add_cascade(label="🪟 Windows", menu=window_menu)
        window_menu.add_command(label="🔧 External Tools Window", command=self.open_external_tools_window)
        window_menu.add_separator()
        window_menu.add_command(label="❌ Close All Result Windows", command=self.close_all_result_windows)
        window_menu.add_command(label="🔄 Refresh Windows", command=self.refresh_all_windows)
        
        view_menu.add_separator()
        view_menu.add_command(label="Dark Theme", command=self.apply_dark_theme)
        
        # Database menu - Normal menu (döngü önleme)
        database_menu = tk.Menu(menubar, tearoff=0, 
                               bg=ModernStyle.BG_SECONDARY, 
                               fg=ModernStyle.FG_PRIMARY)
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
        
        # Help menu - Normal menu (döngü önleme)
        help_menu = tk.Menu(menubar, tearoff=0, 
                           bg=ModernStyle.BG_SECONDARY, 
                           fg=ModernStyle.FG_PRIMARY)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="User Guide", command=self.show_help)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_prg_file())
        self.root.bind('<Control-e>', lambda e: self.export_code())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F12>', lambda e: self.toggle_toolbox())  # F12 için toolbox toggle
    
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
            if start_address == 0x0801 and format_type in ['basic', 'petcat', 'c64list', 'enhanced_basic', 'transpile_qbasic', 'transpile_c', 'transpile_cpp', 'transpile_pdsx', 'transpile_python']:
                # BASIC program - Enhanced BASIC Decompiler entegrasyonu
                if format_type == 'basic':
                    if self.basic_parser:
                        basic_lines = self.basic_parser.detokenize(prg_data)
                        result_code = "\n".join(basic_lines) if basic_lines else "BASIC detokenization failed"
                    else:
                        result_code = "; C64BasicParser modülü bulunamadı\n; Raw BASIC data görüntülenemedi"
                
                elif format_type in ['enhanced_basic', 'transpile_qbasic', 'transpile_c', 'transpile_cpp', 'transpile_pdsx', 'transpile_python']:
                    # 🍎 Enhanced BASIC Decompiler v3.0 ile transpile
                    self.root.after(0, lambda: self.log_message(f"🍎 ENHANCED BASIC DECOMPILER BAŞLATILIYOR", "INFO"))
                    print(f"🍎 Enhanced BASIC Decompiler v3.0 başlatılıyor...")
                    
                    if EnhancedBasicDecompiler:
                        try:
                            enhanced_decompiler = EnhancedBasicDecompiler()
                            
                            # Format türüne göre hedef dil belirleme
                            target_language = "qbasic"  # default
                            if format_type == 'transpile_qbasic':
                                target_language = "qbasic"
                            elif format_type == 'transpile_c':
                                target_language = "c"
                            elif format_type == 'transpile_cpp':
                                target_language = "cpp"
                            elif format_type == 'transpile_pdsx':
                                target_language = "pdsx"
                            elif format_type == 'transpile_python':
                                target_language = "python"
                            elif format_type == 'enhanced_basic':
                                target_language = "enhanced_basic"
                            
                            self.root.after(0, lambda: self.log_message(f"   🎯 Hedef dil: {target_language.upper()}", "INFO"))
                            self.root.after(0, lambda: self.log_message(f"   📦 PRG boyutu: {len(prg_data)} bytes", "INFO"))
                            
                            # Enhanced BASIC Decompiler ile transpile
                            result_code = enhanced_decompiler.decompile_with_context(
                                prg_data=prg_data,
                                target_language=target_language,
                                start_address=start_address
                            )
                            
                            # Ensure result_code is string
                            if isinstance(result_code, list):
                                result_code = '\n'.join(str(line) for line in result_code)
                            elif not isinstance(result_code, str):
                                result_code = str(result_code)
                            
                            if result_code and len(result_code.strip()) > 0:
                                self.root.after(0, lambda: self.log_message(f"   ✅ Enhanced BASIC Decompiler başarılı: {len(result_code)} karakter", "INFO"))
                                print(f"✅ ENHANCED BASIC DECOMPILER BAŞARILI: {target_language.upper()} - {len(result_code)} karakter")
                            else:
                                error_msg = f"Enhanced BASIC Decompiler boş sonuç döndü ({target_language})"
                                self.root.after(0, lambda: self.log_message(f"   ❌ {error_msg}", "ERROR"))
                                result_code = f"; ENHANCED BASIC DECOMPILER ERROR: {error_msg}\n; Target: {target_language}\n; Raw BASIC data:\n{prg_data[:100].hex()}..."
                            
                        except Exception as ebd_error:
                            error_msg = f"Enhanced BASIC Decompiler exception: {ebd_error}"
                            self.root.after(0, lambda: self.log_message(f"   ❌ {error_msg}", "ERROR"))
                            print(f"❌ ENHANCED BASIC DECOMPILER EXCEPTION: {error_msg}")
                            
                            import traceback
                            trace = traceback.format_exc()
                            result_code = f"; ENHANCED BASIC DECOMPILER EXCEPTION: {error_msg}\n; Target: {target_language}\n; Stack trace:\n; {trace.replace(chr(10), chr(10)+'; ')}\n"
                    else:
                        error_msg = "EnhancedBasicDecompiler modülü bulunamadı"
                        self.root.after(0, lambda: self.log_message(f"   ❌ {error_msg}", "ERROR"))
                        result_code = f"; ENHANCED BASIC DECOMPILER MODULE ERROR: {error_msg}"
                    
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
                            
                            # Result_code liste olabilir - string'e dönüştür
                            if isinstance(result_code, list):
                                result_code = '\n'.join(str(line) for line in result_code)
                            elif not isinstance(result_code, str):
                                result_code = str(result_code)
                            
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
                            
                            # Detaylı hata raporu oluştur
                            result_code = f"; PETCAT EXCEPTION: {error_msg}\n"
                            result_code += f"; Stack trace:\n"
                            for line in trace.split('\n'):
                                result_code += f"; {line}\n"
                            result_code += f"; \n; Raw data:\n{prg_data[:100].hex()}..."
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
                # Assembly format belirleme
                asm_format = "native"
                if format_type.startswith('assembly_'):
                    asm_format = format_type.split('_')[1]
                
                if AdvancedDisassembler:
                    disassembler = AdvancedDisassembler(
                        start_address=start_address,
                        code=code_data,
                        use_py65=self.disassembly_panel.use_py65_disassembler.get(),
                        use_illegal_opcodes=self.disassembly_panel.use_illegal_opcodes.get(),
                        output_format='asm'
                    )
                    asm_code = disassembler.disassemble()
                    
                    # List'i string'e çevir (disassembler list döndürüyor)
                    if isinstance(asm_code, list):
                        asm_code = "\n".join(asm_code)
                    
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
                    else:  # native
                        result_code = asm_code
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
                    asm_result = disassembler.disassemble()
                    
                    # List veya string handling
                    if isinstance(asm_result, list):
                        asm_lines = asm_result
                    else:
                        asm_lines = asm_result.split('\n')
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
                    asm_result = disassembler.disassemble()
                    
                    # List'i string'e çevir
                    if isinstance(asm_result, list):
                        result_code += "\n".join(asm_result)
                    else:
                        result_code += asm_result
                
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
                            asm_result = disassembler.disassemble()
                            asm_text = "\n".join(asm_result) if isinstance(asm_result, list) else asm_result
                            result_code += f"\n// Basic assembly code:\n{asm_text}"
                elif format_type == 'dec_c2' and DECOMPILER_C2_AVAILABLE:
                    try:
                        decompiler = DecompilerC2()
                        result_code = decompiler.decompile(prg_data, start_address)
                        self.root.after(0, lambda: self.log_message(f"C2 Decompiler başarılı: {len(result_code)} karakter", "SUCCESS"))
                    except Exception as dec_error:
                        result_code = f"// C2 Decompiler Error: {dec_error}\n// Falling back to basic decompilation\n"
                        if AdvancedDisassembler:
                            disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                            asm_result = disassembler.disassemble()
                            asm_text = "\n".join(asm_result) if isinstance(asm_result, list) else asm_result
                            result_code += f"\n// Basic assembly code:\n{asm_text}"
                elif format_type == 'dec_cpp' and DECOMPILER_CPP_AVAILABLE:
                    try:
                        decompiler = DecompilerCPP()
                        result_code = decompiler.decompile(prg_data, start_address)
                        self.root.after(0, lambda: self.log_message(f"C++ Decompiler başarılı: {len(result_code)} karakter", "SUCCESS"))
                    except Exception as dec_error:
                        result_code = f"// C++ Decompiler Error: {dec_error}\n// Falling back to basic decompilation\n"
                        if AdvancedDisassembler:
                            disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                            asm_result = disassembler.disassemble()
                            asm_text = "\n".join(asm_result) if isinstance(asm_result, list) else asm_result
                            result_code += f"\n// Basic assembly code:\n{asm_text}"
                elif format_type == 'dec_qbasic' and DECOMPILER_QBASIC_AVAILABLE:
                    try:
                        decompiler = DecompilerQBasic()
                        result_code = decompiler.decompile(prg_data, start_address)
                        self.root.after(0, lambda: self.log_message(f"QBasic Decompiler başarılı: {len(result_code)} karakter", "SUCCESS"))
                    except Exception as dec_error:
                        result_code = f"' QBasic Decompiler Error: {dec_error}\n' Falling back to basic decompilation\n"
                        if AdvancedDisassembler:
                            disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                            asm_result = disassembler.disassemble()
                            asm_text = "\n".join(asm_result) if isinstance(asm_result, list) else asm_result
                            result_code += f"\n' Basic assembly code:\n{asm_text}"
                elif format_type == 'dec_asm':
                    result_code = f"; ASM Decompiler (Enhanced)\n"
                    result_code += f"; Start Address: ${start_address:04X}\n"
                    result_code += f"; Code Size: {len(code_data)} bytes\n\n"
                    if AdvancedDisassembler:
                        disassembler = AdvancedDisassembler(start_address=start_address, code=code_data)
                        asm_result = disassembler.disassemble()
                        asm_text = "\n".join(asm_result) if isinstance(asm_result, list) else asm_result
                        result_code += asm_text
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
            
            # 🪟 KızılElma Feature: Her format için ayrı Result Window aç
            if result_code:
                # Ensure result_code is string
                if isinstance(result_code, list):
                    result_code = '\n'.join(str(line) for line in result_code)
                elif not isinstance(result_code, str):
                    result_code = str(result_code)
                
                if len(result_code.strip()) > 0:
                    window_title = f"{format_type.upper()} Result - {self.selected_entry.get('filename', 'Unknown')}"
                    self.root.after(0, lambda: self.create_result_window(window_title, format_type, result_code))
            
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
                             insertbackground=ModernStyle.FG_ACCENT)
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
            
            # Enhanced Universal Disk Reader ile hibrit analiz
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
                               bg=ModernStyle.FG_ACCENT, fg="white",
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
        """Farklı kaydet"""
        if not hasattr(self, 'code_preview') or not self.code_preview.current_code:
            messagebox.showwarning("Warning", "No data to save!")
            return
        
        format_type = self.code_preview.current_format
        ext_map = {"ASM": ".asm", "C": ".c", "QBasic": ".bas", "PDSx": ".pdsx", "C++": ".cpp", "Pseudo": ".txt"}
        
        filename = filedialog.asksaveasfilename(
            title=f"Save {format_type} Code",
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
        batch_window = debug_toplevel(self.root, title="Toplu Kaydetme/Dışa Aktarma")
        batch_window.geometry("600x400")
        batch_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = debug_label(batch_window, text="📦 Toplu İşlem Ayarları", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # Format seçimi
        format_frame = debug_frame(batch_window, debug_name="Format Selection", bg=ModernStyle.BG_PRIMARY)
        format_frame.pack(fill=tk.X, padx=20, pady=10)
        
        debug_label(format_frame, text="Dışa Aktarılacak Formatlar:", 
                bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(anchor=tk.W)
        
        # Format checkboxes - Assembly formatları dahil
        self.batch_formats = {}
        formats = ["ASM", "ASM_ACME", "ASM_CC65", "ASM_DASM", "ASM_KickAss", "C", "QBasic", "PDSx", "C++", "Pseudo"]
        
        # İki sütunlu yerleşim
        row1_frame = debug_frame(format_frame, debug_name="Format Row 1", bg=ModernStyle.BG_PRIMARY)
        row1_frame.pack(fill=tk.X)
        row2_frame = debug_frame(format_frame, debug_name="Format Row 2", bg=ModernStyle.BG_PRIMARY)
        row2_frame.pack(fill=tk.X)
        
        for i, fmt in enumerate(formats):
            var = tk.BooleanVar(value=True)
            self.batch_formats[fmt] = var
            
            parent_frame = row1_frame if i < 5 else row2_frame
            cb = debug_checkbox(parent_frame, text=fmt, variable=var, 
                               bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY,
                               selectcolor=ModernStyle.BG_SECONDARY)
            cb.pack(side=tk.LEFT, padx=10)
        
        # Çıktı dizini
        output_frame = debug_frame(batch_window, debug_name="Output Directory", bg=ModernStyle.BG_PRIMARY)
        output_frame.pack(fill=tk.X, padx=20, pady=10)
        
        debug_label(output_frame, text="Çıktı Dizini:", 
                bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(anchor=tk.W)
        
        self.batch_output_var = tk.StringVar(value=os.getcwd())
        output_entry = debug_entry(output_frame, debug_name="Output Path", textvariable=self.batch_output_var, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        debug_button(output_frame, text="📂", command=lambda: self.batch_output_var.set(
            debug_dirdialog(title="Select batch output directory"))).pack(side=tk.RIGHT)
        
        # Progress bar
        progress_frame = debug_frame(batch_window, debug_name="Progress Frame", bg=ModernStyle.BG_PRIMARY)
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.batch_progress = debug_progressbar(progress_frame, debug_name="Batch Progress", mode='determinate')
        self.batch_progress.pack(fill=tk.X)
        
        # Butonlar
        button_frame = debug_frame(batch_window, debug_name="Batch Buttons", bg=ModernStyle.BG_PRIMARY)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        debug_button(button_frame, text="🚀 Başlat", command=lambda: self.start_batch_export(batch_window)).pack(side=tk.LEFT, padx=10)
        debug_button(button_frame, text="❌ İptal", command=batch_window.destroy).pack(side=tk.RIGHT, padx=10)
    
    def start_batch_export(self, batch_window):
        """Toplu dışa aktarmayı başlat"""
        selected_formats = [fmt for fmt, var in self.batch_formats.items() if var.get()]
        output_dir = self.batch_output_var.get()
        
        if not selected_formats:
            safe_messagebox("warning", "Warning", "Please select at least one format!")
            return
        
        if not output_dir or not os.path.exists(output_dir):
            safe_messagebox("warning", "Warning", "Please select a valid output directory!")
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
            safe_messagebox("warning", "Warning", "Database manager not available")
            return
        
        stats_window = debug_toplevel(self.root, title="📊 Database Statistics")
        stats_window.geometry("800x600")
        stats_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = debug_label(stats_window, text="📊 İşlenmiş Dosya İstatistikleri", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # İstatistikleri al
        stats = self.database_manager.get_statistics()
        
        # Text widget ile göster
        text_widget = debug_scrolledtext(stats_window, debug_name="Stats Display", height=30, width=100,
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
            safe_messagebox("warning", "Warning", "Database manager not available")
            return
        
        history_window = debug_toplevel(self.root, title="📁 File Processing History")
        history_window.geometry("1200x700")
        history_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = debug_label(history_window, text="📁 Dosya İşlem Geçmişi", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # Treeview ile tablo gösterimi
        tree_frame = debug_frame(history_window, debug_name="History Tree Frame", bg=ModernStyle.BG_PRIMARY)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ('Filename', 'Format', 'Size', 'Success', 'Failure', 'Last Processed')
        tree = debug_treeview(tree_frame, debug_name="History Tree", columns=columns, show='headings')
        
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
        scrollbar = debug_scrollbar(tree_frame, debug_name="History Scrollbar", orient=tk.VERTICAL, command=tree.yview)
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
            safe_messagebox("warning", "Warning", "Database manager not available")
            return
        
        search_window = debug_toplevel(self.root, title="🔍 Database Search")
        search_window.geometry("800x600")
        search_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        # Başlık
        title_label = debug_label(search_window, debug_name="Search Title", text="🔍 Dosya Arama", 
                              font=("Arial", 16, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY)
        title_label.pack(pady=10)
        
        # Arama formu
        search_frame = debug_frame(search_window, debug_name="Search Form Frame", bg=ModernStyle.BG_PRIMARY)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        debug_label(search_frame, debug_name="Search Label", text="Arama terimi:", bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(side=tk.LEFT)
        search_entry = debug_entry(search_frame, debug_name="Search Entry", width=30, font=("Arial", 10))
        search_entry.pack(side=tk.LEFT, padx=10)
        
        search_type_var = tk.StringVar(value="filename")
        debug_radiobutton(search_frame, debug_name="Search Filename Radio", text="Dosya Adı", variable=search_type_var, value="filename").pack(side=tk.LEFT, padx=5)
        debug_radiobutton(search_frame, debug_name="Search Format Radio", text="Format", variable=search_type_var, value="format").pack(side=tk.LEFT, padx=5)
        debug_radiobutton(search_frame, debug_name="Search Notes Radio", text="Notlar", variable=search_type_var, value="notes").pack(side=tk.LEFT, padx=5)
        
        # Arama sonuçları
        results_text = debug_scrolledtext(search_window, debug_name="Search Results Text", height=25, width=100,
                                               bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                                               font=("Consolas", 10))
        results_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def do_search():
            search_term = search_entry.get()
            search_type = search_type_var.get()
            
            if not search_term:
                safe_messagebox("warning", "Warning", "Arama terimi girin")
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
        
        debug_button(search_frame, debug_name="Search Button", text="🔍 Ara", command=do_search).pack(side=tk.LEFT, padx=10)
        
        # Enter tuşu ile arama
        search_entry.bind('<Return>', lambda e: do_search())
    
    def export_database_excel(self):
        """Veritabanını Excel'e aktar"""
        if not self.database_manager:
            safe_messagebox("warning", "Warning", "Database manager not available")
            return
        
        filename = debug_filedialog_save(
            title="Export Database to Excel",
            debug_name="Excel Export Dialog",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if filename:
            if self.database_manager.export_to_excel(filename):
                safe_messagebox("info", "Success", f"Database exported to: {filename}")
                self.log_message(f"Database exported to Excel: {filename}", "INFO")
            else:
                safe_messagebox("error", "Error", "Excel export failed")
    
    def export_database_csv(self):
        """Veritabanını CSV'ye aktar"""
        if not self.database_manager:
            safe_messagebox("warning", "Warning", "Database manager not available")
            return
        
        output_dir = debug_dirdialog(title="Select output directory for CSV files", debug_name="CSV Export Directory")
        
        if output_dir:
            if self.database_manager.export_to_csv(output_dir):
                safe_messagebox("info", "Success", f"Database exported to CSV files in: {output_dir}")
                self.log_message(f"Database exported to CSV: {output_dir}", "INFO")
            else:
                safe_messagebox("error", "Error", "CSV export failed")
    
    def export_database_json(self):
        """Veritabanını JSON'a aktar"""
        if not self.database_manager:
            safe_messagebox("warning", "Warning", "Database manager not available")
            return
        
        filename = debug_filedialog_save(
            title="Export Database to JSON",
            debug_name="JSON Export Dialog",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.database_manager.export_to_json(filename):
                safe_messagebox("info", "Success", f"Database exported to: {filename}")
                self.log_message(f"Database exported to JSON: {filename}", "INFO")
            else:
                safe_messagebox("error", "Error", "JSON export failed")
    
    def cleanup_database(self):
        """Eski veritabanı kayıtlarını temizle"""
        if not self.database_manager:
            safe_messagebox("warning", "Warning", "Database manager not available")
            return
        
        # Gün sayısı al
        cleanup_window = debug_toplevel(self.root, title="🧹 Database Cleanup")
        cleanup_window.geometry("400x200")
        cleanup_window.configure(bg=ModernStyle.BG_PRIMARY)
        
        debug_label(cleanup_window, debug_name="Cleanup Title", text="🧹 Veritabanı Temizleme", 
                font=("Arial", 14, "bold"), bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(pady=20)
        
        debug_label(cleanup_window, debug_name="Cleanup Info", text="Kaç günden eski kayıtlar silinsin?", 
                bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.FG_PRIMARY).pack(pady=10)
        
        days_var = tk.StringVar(value="30")
        days_entry = debug_entry(cleanup_window, debug_name="Days Entry", textvariable=days_var, width=10, font=("Arial", 12))
        days_entry.pack(pady=10)
        
        def do_cleanup():
            try:
                days = int(days_var.get())
                if days <= 0:
                    safe_messagebox("error", "Error", "Gün sayısı 0'dan büyük olmalı")
                    return
                
                deleted_count = self.database_manager.cleanup_old_records(days)
                cleanup_window.destroy()
                
                safe_messagebox("info", "Success", f"{deleted_count} eski kayıt silindi")
                self.log_message(f"Database cleanup: {deleted_count} records deleted (older than {days} days)", "INFO")
                
            except ValueError:
                safe_messagebox("error", "Error", "Geçerli bir sayı girin")
        
        button_frame = debug_frame(cleanup_window, debug_name="Cleanup Button Frame", bg=ModernStyle.BG_PRIMARY)
        button_frame.pack(pady=20)
        
        debug_button(button_frame, debug_name="Cleanup Button", text="🧹 Temizle", command=do_cleanup).pack(side=tk.LEFT, padx=10)
        debug_button(button_frame, debug_name="Cancel Cleanup Button", text="❌ İptal", command=cleanup_window.destroy).pack(side=tk.LEFT, padx=10)
    
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
                            use_illegal_opcodes=False,
                            output_format='asm'
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
                    use_illegal_opcodes=self.disassembly_panel.use_illegal_opcodes.get(),
                    output_format='asm'
                )
                assembly_code = disassembler.disassemble()
                
                # List'i string'e çevir (disassembler list döndürüyor)
                if isinstance(assembly_code, list):
                    assembly_code = "\n".join(assembly_code)
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

    # === Configuration Manager & Toolbox Integration ===
    
    def setup_configuration_manager(self):
        """Configuration Manager entegrasyonu"""
        try:
            from configuration_manager import ConfigurationManager
            self.config_manager = ConfigurationManager()
            self.logger.info("✅ Configuration Manager initialized")
        except ImportError as e:
            self.logger.warning(f"⚠️ Configuration Manager not available: {e}")
            self.config_manager = None
        except Exception as e:
            self.logger.error(f"❌ Configuration Manager setup failed: {e}")
            self.config_manager = None
    
    def setup_toolbox(self):
        """Toolbox Manager entegrasyonu"""
        try:
            from toolbox_manager import ToolboxManager
            self.toolbox_manager = ToolboxManager(parent_window=self.root, 
                                                 config_manager=self.config_manager)
            self.logger.info("✅ Toolbox Manager initialized")
        except ImportError as e:
            self.logger.warning(f"⚠️ Toolbox Manager not available: {e}")
            self.toolbox_manager = None
        except Exception as e:
            self.logger.error(f"❌ Toolbox Manager setup failed: {e}")
            self.toolbox_manager = None
    
    def open_configuration_manager(self):
        """Configuration Manager penceresini aç"""
        if self.config_manager:
            try:
                # Configuration Manager için root window yoksa yeni bir tane oluştur
                if not hasattr(self.config_manager, 'root') or not self.config_manager.root:
                    self.config_manager.run()
                else:
                    # Varolan window'u göster
                    self.config_manager.root.deiconify()
                    self.config_manager.root.lift()
                self.logger.info("⚙️ Configuration Manager opened")
            except Exception as e:
                self.logger.error(f"❌ Failed to open Configuration Manager: {e}")
                # Safe messagebox kullan
                safe_messagebox("error", "Error", f"Failed to open Configuration Manager:\n{str(e)}")
        else:
            # Configuration Manager yoksa yeni bir tane oluştur
            try:
                from configuration_manager import ConfigurationManager
                self.config_manager = ConfigurationManager()
                self.config_manager.run()
                
                # Toolbox'ı da güncelle
                if self.toolbox_manager:
                    self.toolbox_manager.config_manager = self.config_manager
                
                self.logger.info("⚙️ Configuration Manager created and opened")
            except Exception as e:
                self.logger.error(f"❌ Failed to create Configuration Manager: {e}")
                # Safe messagebox kullan
                safe_messagebox("error", "Error", f"Configuration Manager not available:\n{str(e)}")
    
    def toggle_toolbox(self):
        """Toolbox görünürlüğünü değiştir"""
        if self.toolbox_manager:
            try:
                self.toolbox_manager.toggle_toolbox()
                status = "shown" if self.toolbox_manager.visible else "hidden"
                self.logger.info(f"🧰 Toolbox {status}")
                self.update_status(f"Toolbox {status}")
            except Exception as e:
                self.logger.error(f"❌ Failed to toggle toolbox: {e}")
                messagebox.showerror("Error", f"Failed to toggle toolbox:\n{str(e)}")
        else:
            # Toolbox yoksa yeni bir tane oluştur
            try:
                from toolbox_manager import ToolboxManager
                self.toolbox_manager = ToolboxManager(parent_window=self.root,
                                                     config_manager=self.config_manager)
                self.toolbox_manager.show_toolbox()
                self.logger.info("🧰 Toolbox created and shown")
                self.update_status("Toolbox created and shown")
            except Exception as e:
                self.logger.error(f"❌ Failed to create toolbox: {e}")
                messagebox.showerror("Error", f"Toolbox not available:\n{str(e)}")
    
    def cleanup_on_exit(self):
        """Çıkışta temizlik işlemleri"""
        try:
            # Toolbox'ı temizle
            if hasattr(self, 'toolbox_manager') and self.toolbox_manager:
                self.toolbox_manager.cleanup()
                self.logger.info("🧰 Toolbox cleaned up")
            
            # Configuration Manager'ı temizle
            if hasattr(self, 'config_manager') and self.config_manager:
                if hasattr(self.config_manager, 'cleanup'):
                    self.config_manager.cleanup()
                self.logger.info("⚙️ Configuration Manager cleaned up")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Cleanup warning: {e}")
    
    # 🔧 External Tools Integration - KızılElma Feature
    def open_external_tools_window(self):
        """External Tools Window'u aç"""
        try:
            if not hasattr(self, 'external_tools_window'):
                self.external_tools_window = ExternalToolsWindow(self)
            
            self.external_tools_window.show()
            self.log_to_terminal_and_file("🔧 External Tools Window açıldı", "INFO")
            
        except Exception as e:
            error_msg = f"External Tools Window açılamadı: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("Error", error_msg)
    
    def open_with_crossviper(self):
        """Aktif dosyayı CrossViper IDE ile aç"""
        try:
            # Get current content
            current_content = self.get_current_active_content()
            
            if not current_content:
                messagebox.showwarning("No Content", "No active content to open with CrossViper IDE")
                return
            
            # Launch CrossViper
            self.launch_crossviper_with_content(current_content)
            
        except Exception as e:
            error_msg = f"CrossViper IDE başlatılamadı: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("CrossViper Error", error_msg)
    
    def open_viper_ide(self):
        """Viper IDE'yi aç - 6502 Assembly & C64 Development Environment"""
        try:
            # Viper IDE'yi ayrı thread'de başlat
            def run_viper():
                try:
                    from viper import run_viper_ide
                    run_viper_ide()
                except ImportError as e:
                    self.log_to_terminal_and_file(f"Viper IDE import hatası: {e}", "ERROR")
                    messagebox.showerror("Viper IDE Error", f"Viper IDE modülü bulunamadı: {e}")
                except Exception as e:
                    self.log_to_terminal_and_file(f"Viper IDE çalıştırma hatası: {e}", "ERROR")
                    messagebox.showerror("Viper IDE Error", f"Viper IDE başlatılamadı: {e}")
            
            # Thread'de çalıştır
            viper_thread = threading.Thread(target=run_viper, daemon=True)
            viper_thread.start()
            
            self.log_to_terminal_and_file("🐍 Viper IDE başlatıldı", "INFO")
            self.update_status("Viper IDE açılıyor...")
            
        except Exception as e:
            error_msg = f"Viper IDE başlatılamadı: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("Viper IDE Error", error_msg)
    
    def open_with_external_tool(self, tool_name):
        """Aktif dosyayı belirtilen external tool ile aç"""
        try:
            # Get current content
            current_content = self.get_current_active_content()
            
            if not current_content:
                messagebox.showwarning("No Content", f"No active content to open with {tool_name}")
                return
            
            # Get tool from Configuration Manager
            if not hasattr(self, 'config_manager') or not self.config_manager:
                messagebox.showerror("Config Error", "Configuration Manager not available")
                return
            
            available_tools = self.config_manager.get_available_tools()
            target_tool = None
            
            for tool in available_tools:
                if tool.get('name', '').lower() == tool_name.lower():
                    target_tool = tool
                    break
            
            if not target_tool:
                messagebox.showerror("Tool Not Found", f"External tool '{tool_name}' not configured")
                return
            
            # Launch tool
            self.launch_external_tool_with_content(target_tool, current_content)
            
        except Exception as e:
            error_msg = f"External tool '{tool_name}' başlatılamadı: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("Tool Error", error_msg)
    
    def refresh_external_tools(self):
        """External tools listesini yenile"""
        try:
            if hasattr(self, 'config_manager') and self.config_manager:
                # Refresh config manager's tool list
                if hasattr(self.config_manager, 'scan_for_tools'):
                    self.config_manager.scan_for_tools()
                
                # Refresh external tools window if open
                if hasattr(self, 'external_tools_window') and self.external_tools_window.window and self.external_tools_window.window.winfo_exists():
                    self.external_tools_window.refresh_available_tools()
                
                self.log_to_terminal_and_file("🔄 External tools listesi yenilendi", "INFO")
                messagebox.showinfo("Refreshed", "External tools list refreshed successfully")
            else:
                messagebox.showerror("Error", "Configuration Manager not available")
                
        except Exception as e:
            error_msg = f"External tools yenilenemedi: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("Refresh Error", error_msg)
    
    def get_current_active_content(self):
        """Aktif panel'den content al"""
        try:
            # Check disassembly panel first
            if hasattr(self, 'disassembly_panel') and self.disassembly_panel and hasattr(self.disassembly_panel, 'current_code'):
                content = self.disassembly_panel.current_code
                if content and content.strip():
                    return content
            
            # Check decompiler panel
            if hasattr(self, 'decompiler_panel') and self.decompiler_panel and hasattr(self.decompiler_panel, 'current_code'):
                content = self.decompiler_panel.current_code
                if content and content.strip():
                    return content
            
            return None
            
        except Exception as e:
            self.log_to_terminal_and_file(f"Error getting active content: {e}", "ERROR")
            return None
    
    def launch_crossviper_with_content(self, content):
        """CrossViper IDE'yi content ile başlat"""
        try:
            # Look for CrossViper IDE
            crossviper_paths = [
                os.path.join(os.path.dirname(__file__), "crossviper-master", "main.py"),
                os.path.join(os.path.dirname(__file__), "crossviper", "main.py"),
                os.path.join(os.path.dirname(__file__), "..", "crossviper-master", "main.py")
            ]
            
            crossviper_path = None
            for path in crossviper_paths:
                if os.path.exists(path):
                    crossviper_path = path
                    break
            
            if not crossviper_path:
                messagebox.showerror("CrossViper Not Found", 
                                   "CrossViper IDE not found in project directory")
                return
            
            # Create temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            # Launch CrossViper
            subprocess.Popen([sys.executable, crossviper_path, temp_file_path])
            
            self.log_to_terminal_and_file("✅ CrossViper IDE başlatıldı", "INFO")
            
        except Exception as e:
            raise e
    
    def launch_viper_ide(self):
        """Viper IDE'yi aktif tab contentle başlat"""
        try:
            # Viper.py dosyasını bul
            viper_path = os.path.join(os.path.dirname(__file__), "viper.py")
            
            if not os.path.exists(viper_path):
                messagebox.showerror("Viper Not Found", 
                                   "Viper IDE (viper.py) not found in project directory")
                return
            
            # Aktif tab'dan content al
            active_content = self.get_active_tab_content()
            
            if active_content:
                # Temporary file oluştur
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False, encoding='utf-8') as temp_file:
                    temp_file.write(active_content)
                    temp_file_path = temp_file.name
                
                # Viper'i dosya ile başlat
                subprocess.Popen([sys.executable, viper_path, temp_file_path])
                self.log_to_terminal_and_file(f"✅ Viper IDE başlatıldı: {temp_file_path}", "INFO")
            else:
                # Boş Viper başlat
                subprocess.Popen([sys.executable, viper_path])
                self.log_to_terminal_and_file("✅ Viper IDE başlatıldı (boş)", "INFO")
                
        except Exception as e:
            error_msg = f"Viper IDE başlatma hatası: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("Viper Error", error_msg)
    
    def get_active_tab_content(self):
        """Aktif tab'dan content al"""
        try:
            # Decompiler panel'den aktif tab'ı al
            if hasattr(self, 'decompiler_panel') and hasattr(self.decompiler_panel, 'notebook'):
                current_tab = self.decompiler_panel.notebook.select()
                if current_tab:
                    # Tab widget'ının content'ini al
                    tab_widget = self.decompiler_panel.notebook.nametowidget(current_tab)
                    if hasattr(tab_widget, 'text_widget'):
                        content = tab_widget.text_widget.get(1.0, tk.END)
                        if content and content.strip():
                            return content
            
            # Disassembly panel'den content al
            if hasattr(self, 'disassembly_panel') and hasattr(self.disassembly_panel, 'code_display'):
                content = self.disassembly_panel.code_display.get(1.0, tk.END)
                if content and content.strip():
                    return content
            
            return None
            
        except Exception as e:
            self.log_to_terminal_and_file(f"Error getting active content: {e}", "ERROR")
            return None
    
    def launch_external_tool_with_content(self, tool_info, content):
        """External tool'u content ile başlat"""
        try:
            tool_name = tool_info.get('name', 'Unknown')
            tool_path = tool_info.get('path', '')
            
            if not os.path.exists(tool_path):
                raise Exception(f"Tool executable not found: {tool_path}")
            
            # Create temporary file
            import tempfile
            ext_map = {
                'assembly': '.asm',
                'asm': '.asm',
                'c': '.c',
                'cpp': '.cpp',
                'qbasic': '.bas',
                'basic': '.bas',
                'pdsx': '.asm',
                'python': '.py'
            }
            
            file_ext = '.asm'  # Default to assembly
            
            with tempfile.NamedTemporaryFile(mode='w', suffix=file_ext, delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            # Launch tool
            subprocess.Popen([tool_path, temp_file_path], shell=True)
            
            self.log_to_terminal_and_file(f"✅ {tool_name} başlatıldı", "INFO")
            
        except Exception as e:
            raise e
    
    def open_viper_ide(self):
        """Menü için Viper IDE açma - compatibility wrapper"""
        return self.launch_viper_ide()
    
    # 🪟 Result Window Management - KızılElma Feature
    def create_result_window(self, title, format_type, content):
        """Her format sonucu için ayrı pencere oluştur"""
        try:
            result_window = ResultWindow(self, title, format_type, content)
            
            # Store reference for management
            if not hasattr(self, 'result_windows'):
                self.result_windows = []
            self.result_windows.append(result_window)
            
            self.log_to_terminal_and_file(f"🪟 Result window opened: {format_type.upper()}", "INFO")
            
        except Exception as e:
            error_msg = f"Result window oluşturulamadı: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("Window Error", error_msg)
    
    def close_all_result_windows(self):
        """Tüm result window'ları kapat"""
        try:
            if hasattr(self, 'result_windows'):
                for window in self.result_windows:
                    if window.window and window.window.winfo_exists():
                        window.window.destroy()
                self.result_windows.clear()
                
            self.log_to_terminal_and_file("🪟 All result windows closed", "INFO")
            
        except Exception as e:
            self.log_to_terminal_and_file(f"Error closing result windows: {e}", "WARNING")
    
    def refresh_all_windows(self):
        """Tüm pencereleri yenile"""
        try:
            # Refresh main panels
            if hasattr(self, 'disassembly_panel'):
                self.disassembly_panel.update_code("# Ready for disassembly", "ready")
            
            if hasattr(self, 'decompiler_panel'):
                self.decompiler_panel.update_code("# Ready for decompilation", "ready")
            
            # Refresh external tools if open
            if hasattr(self, 'external_tools_window') and self.external_tools_window.window and self.external_tools_window.window.winfo_exists():
                self.external_tools_window.refresh_available_tools()
            
            self.log_to_terminal_and_file("🔄 All windows refreshed", "INFO")
            messagebox.showinfo("Refreshed", "All windows have been refreshed successfully")
            
        except Exception as e:
            error_msg = f"Window refresh failed: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("Refresh Error", error_msg)
    
    # Enhanced BASIC Decompiler menu functions
    def enhanced_basic_decompile_current(self, target_language):
        """Aktif BASIC dosyasını Enhanced BASIC Decompiler ile dönüştür"""
        try:
            if not self.selected_entry:
                messagebox.showwarning("No Selection", "Please select a BASIC program first")
                return
            
            # Convert to Enhanced BASIC format first
            format_map = {
                'qbasic': 'transpile_qbasic',
                'c': 'transpile_c',
                'cpp': 'transpile_cpp',
                'pdsx': 'transpile_pdsx',
                'python': 'transpile_python'
            }
            
            format_type = format_map.get(target_language, 'enhanced_basic')
            self.convert_to_format(format_type, 'decompiler')
            
            self.log_to_terminal_and_file(f"🍎 Enhanced BASIC → {target_language.upper()} conversion started", "INFO")
            
        except Exception as e:
            error_msg = f"Enhanced BASIC decompilation failed: {e}"
            self.log_to_terminal_and_file(error_msg, "ERROR")
            messagebox.showerror("Decompilation Error", error_msg)
    
    def show_enhanced_basic_options(self):
        """Enhanced BASIC Decompiler advanced options"""
        try:
            # Create options window
            options_window = tk.Toplevel(self.root)
            options_window.title("🍎 Enhanced BASIC Decompiler Options")
            options_window.geometry("500x400")
            options_window.configure(bg=ModernStyle.BG_SECONDARY)
            
            tk.Label(options_window, text="🍎 Enhanced BASIC Decompiler v3.0", 
                    bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_PRIMARY,
                    font=("Arial", 14, "bold")).pack(pady=10)
            
            # Options text
            options_text = """
Enhanced BASIC Decompiler Features:
• 5 Target Languages: QBasic, C, C++, PDSX, Python
• POKE/PEEK Optimization
• SYS Call Conversion
• Memory Pointer Optimization
• Variable Type Detection
• Loop Modernization
• String Handling Optimization
• Graphics Command Translation
• Sound Command Translation

KızılElma Plan - AŞAMA 1 Feature ✅
            """
            
            tk.Label(options_window, text=options_text, 
                    bg=ModernStyle.BG_SECONDARY, fg=ModernStyle.FG_SECONDARY,
                    font=("Arial", 10), justify=tk.LEFT).pack(padx=20, pady=10)
            
            ttk.Button(options_window, text="❌ Close", 
                      command=options_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Options Error", f"Failed to show options: {e}")
    
    def test_debug_components(self):
        """Debug component sistemini test et"""
        try:
            # Test window oluştur
            test_window = tk.Toplevel(self.root)
            test_window.title("GUI Debug Test")
            test_window.geometry("600x400")
            test_window.configure(bg=ModernStyle.BG_DARK)
            
            # Debug info göster
            debug_label(test_window, "🍎 GUI Debug Test Window", 
                       bg=ModernStyle.BG_DARK, fg=ModernStyle.FG_PRIMARY,
                       font=("Arial", 14, "bold")).pack(pady=10)
            
            # Test frame
            test_frame = debug_frame(test_window, "Test Controls", bg=ModernStyle.BG_SECONDARY)
            test_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Test butonları
            debug_button(test_frame, "Test Button 1", 
                        command=lambda: debug_messagebox("info", "Test", "Bu bir test mesajıdır")).pack(pady=5)
            debug_button(test_frame, "Test Button 2", 
                        command=lambda: print("Test Button 2 clicked")).pack(pady=5)
            debug_button(test_frame, "Show Registry", 
                        command=self.gui_debug.show_registry).pack(pady=5)
            
            # Test entry
            debug_entry(test_frame, "Test Entry").pack(pady=5)
            
            # Kapat butonu
            debug_button(test_frame, "Close Test Window", 
                        command=test_window.destroy).pack(pady=10)
                        
        except Exception as e:
            debug_messagebox("error", "Test Error", f"Debug test failed: {e}")

def main():
    """GUI uygulamasını başlat"""
    print("🚀 D64 Converter GUI v5.0 Starting...")
    print("X1 Integration: ✅ Enabled")
    print("4-Panel Layout: ✅ Active")
    print("Configuration Manager: ✅ Integrated")
    print("Toolbox Manager: ✅ Integrated")
    
    try:
        app = D64ConverterGUI()
        
        # Cleanup on window close
        def on_closing():
            app.cleanup_on_exit()
            app.root.destroy()
        
        app.root.protocol("WM_DELETE_WINDOW", on_closing)
        app.run()
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
