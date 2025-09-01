#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
libx_guiX.py - PDSX v12X Enhanced GUI Library
Python 3.13+ Compatible Version
Advanced GUI Development Framework for PDSX

Enhanced Features:
- Python 3.13+ compatibility with modern type hints
- Enhanced widget management and event system
- Advanced layout management (Grid, Pack, Place)
- Custom widget creation and styling
- Threading-safe GUI operations
- Drag & Drop support
- Modern dialog systems
- Canvas and drawing capabilities
- Enhanced error handling and logging

Author: AI Assistant (Converted from original by xAI/Grok 3)
Version: 2.0.1 (Corrected and Enhanced)
Date: August 1, 2025
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
from typing import Any, Callable, Dict, Optional, List, Union, Tuple
import logging
from threading import Thread, Lock
from pathlib import Path
import re
import json
import time
from dataclasses import dataclass, field
from enum import Enum

# Python version check - now supports 3.8+
if sys.version_info < (3, 8):
    print("[PDSX-GUI] UYARI: Bu modül Python 3.8+ için optimize edilmiştir.")
    print("[PDSX-GUI] Mevcut versiyon:", sys.version)

# Enhanced logging configuration
logging.basicConfig(
    filename="pdsx_gui.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding='utf-8'
)
log = logging.getLogger("pdsx_gui")

class PdsXGuiException(Exception):
    """PDSX GUI özel hata sınıfı"""
    pass

class LayoutType(Enum):
    """Layout yönetim türleri"""
    PLACE = "place"
    PACK = "pack"
    GRID = "grid"

class WidgetState(Enum):
    """Widget durumları"""
    NORMAL = "normal"
    DISABLED = "disabled"
    ACTIVE = "active"
    READONLY = "readonly"

@dataclass
class WidgetInfo:
    """Widget bilgi sınıfı"""
    widget: tk.Widget
    widget_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    events: Dict[str, str] = field(default_factory=dict)
    layout_info: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

@dataclass
class WindowInfo:
    """Pencere bilgi sınıfı"""
    window: tk.Toplevel
    title: str
    width: int
    height: int
    widgets: Dict[str, WidgetInfo] = field(default_factory=dict)
    layout_type: LayoutType = LayoutType.PLACE
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

class EnhancedWindowManager:
    """Gelişmiş pencere yöneticisi"""
    
    def __init__(self, interpreter=None):
        self.interpreter = interpreter
        self.windows: Dict[str, WindowInfo] = {}
        self.root: Optional[tk.Tk] = None
        self.lock = Lock()
        self.themes = {
            'default': {'bg': '#f0f0f0', 'fg': '#000000'},
            'dark': {'bg': '#2e2e2e', 'fg': '#ffffff'},
            'blue': {'bg': '#4a90e2', 'fg': '#ffffff'},
            'green': {'bg': '#50c878', 'fg': '#000000'}
        }
        self.current_theme = 'default'
        self._drag_data = {"x": 0, "y": 0, "widget": None}  # rem: Drag & Drop desteği için
        
        # Initialize root if not exists
        self._ensure_root()
        
    def _ensure_root(self):
        """Root window'u garanti et"""
        if self.root is None:
            self.root = tk.Tk()
            self.root.withdraw()  # Hide root by default
            
    def create_window(self, name: str, width: int, height: int, 
                     title: str = "", resizable: bool = True, 
                     layout: LayoutType = LayoutType.PLACE) -> bool:
        """Gelişmiş pencere oluşturma"""
        with self.lock:
            name_upper = name.upper()
            if name_upper in self.windows:
                raise PdsXGuiException(f"Pencere zaten mevcut: {name}")
            
            try:
                self._ensure_root()
                window = tk.Toplevel(self.root)
                window.title(title or name)
                window.geometry(f"{width}x{height}")
                window.resizable(resizable, resizable)
                
                # Apply theme
                theme = self.themes[self.current_theme]
                window.configure(bg=theme['bg'])
                
                # Create window info
                window_info = WindowInfo(
                    window=window,
                    title=title or name,
                    width=width,
                    height=height,
                    layout_type=layout
                )
                
                self.windows[name_upper] = window_info
                
                log.info(f"Pencere oluşturuldu: {name} ({width}x{height})")
                return True
                
            except Exception as e:
                log.error(f"Pencere oluşturma hatası: {e}")
                raise PdsXGuiException(f"Pencere oluşturma hatası: {e}")
    
    def enable_drag(self, window_name: str, widget_name: str) -> bool:
        """Bir widget'ı sürüklenebilir yapar"""
        with self.lock:
            widget_info = self._get_widget(window_name, widget_name)
            if not widget_info:
                raise PdsXGuiException(f"Widget bulunamadı: {window_name}.{widget_name}")

            widget = widget_info.widget
            widget.bind("<ButtonPress-1>", self._drag_start)
            widget.bind("<ButtonRelease-1>", self._drag_stop)
            widget.bind("<B1-Motion>", self._drag_motion)
            log.info(f"Sürükleme etkinleştirildi: {window_name}.{widget_name}")
            return True

    def _drag_start(self, event):
        """rem: Sürükleme başlangıcı"""
        widget = event.widget
        self._drag_data["widget"] = widget
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _drag_stop(self, event):
        """rem: Sürükleme sonu"""
        self._drag_data["widget"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def _drag_motion(self, event):
        """rem: Sürükleme hareketi"""
        widget = self._drag_data["widget"]
        if widget:
            x = widget.winfo_x() - self._drag_data["x"] + event.x
            y = widget.winfo_y() - self._drag_data["y"] + event.y
            widget.place(x=x, y=y)
    
    def add_button(self, window_name: str, widget_name: str, text: str, 
                   x: int = 0, y: int = 0, width: int = 100, height: int = 30,
                   command: Optional[str] = None, style: Optional[Dict] = None) -> bool:
        """Gelişmiş düğme ekleme"""
        return self._add_widget(
            window_name, widget_name, 'button',
            lambda parent: tk.Button(parent, text=text, 
                                   command=lambda: self._execute_command(command) if command else None),
            x, y, width, height, style
        )
    
    def add_label(self, window_name: str, widget_name: str, text: str,
                  x: int = 0, y: int = 0, width: int = 100, height: int = 30,
                  style: Optional[Dict] = None) -> bool:
        """Gelişmiş etiket ekleme"""
        return self._add_widget(
            window_name, widget_name, 'label',
            lambda parent: tk.Label(parent, text=text),
            x, y, width, height, style
        )
    
    def add_entry(self, window_name: str, widget_name: str, 
                  x: int = 0, y: int = 0, width: int = 100, height: int = 30,
                  placeholder: str = "", style: Optional[Dict] = None) -> bool:
        """Gelişmiş giriş alanı ekleme"""
        def create_entry(parent):
            entry = tk.Entry(parent)
            if placeholder:
                entry.insert(0, placeholder)
                entry.configure(fg='gray')
                
                def on_focus_in(event):
                    if entry.get() == placeholder:
                        entry.delete(0, tk.END)
                        entry.configure(fg='black')
                
                def on_focus_out(event):
                    if not entry.get():
                        entry.insert(0, placeholder)
                        entry.configure(fg='gray')
                
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<FocusOut>', on_focus_out)
            
            return entry
            
        return self._add_widget(
            window_name, widget_name, 'entry',
            create_entry, x, y, width, height, style
        )
    
    def add_listbox(self, window_name: str, widget_name: str,
                    items: List[str] = None, x: int = 0, y: int = 0, 
                    width: int = 150, height: int = 100,
                    style: Optional[Dict] = None) -> bool:
        """Liste kutusu ekleme"""
        def create_listbox(parent):
            listbox = tk.Listbox(parent)
            if items:
                for item in items:
                    listbox.insert(tk.END, item)
            return listbox
            
        return self._add_widget(
            window_name, widget_name, 'listbox',
            create_listbox, x, y, width, height, style
        )
    
    def add_text(self, window_name: str, widget_name: str,
                 x: int = 0, y: int = 0, width: int = 200, height: int = 100,
                 text: str = "", style: Optional[Dict] = None) -> bool:
        """Çok satırlı metin alanı ekleme"""
        def create_text(parent):
            text_widget = tk.Text(parent)
            if text:
                text_widget.insert(tk.END, text)
            return text_widget
            
        return self._add_widget(
            window_name, widget_name, 'text',
            create_text, x, y, width, height, style
        )
    
    def add_canvas(self, window_name: str, widget_name: str,
                   x: int = 0, y: int = 0, width: int = 300, height: int = 200,
                   bg: str = 'white', style: Optional[Dict] = None) -> bool:
        """Canvas (çizim alanı) ekleme"""
        return self._add_widget(
            window_name, widget_name, 'canvas',
            lambda parent: tk.Canvas(parent, bg=bg),
            x, y, width, height, style
        )
    
    def add_frame(self, window_name: str, widget_name: str,
                  x: int = 0, y: int = 0, width: int = 200, height: int = 150,
                  relief: str = 'flat', borderwidth: int = 1,
                  style: Optional[Dict] = None) -> bool:
        """Çerçeve ekleme"""
        return self._add_widget(
            window_name, widget_name, 'frame',
            lambda parent: tk.Frame(parent, relief=relief, borderwidth=borderwidth),
            x, y, width, height, style
        )
    
    def add_checkbutton(self, window_name: str, widget_name: str, text: str,
                        x: int = 0, y: int = 0, width: int = 100, height: int = 30,
                        command: Optional[str] = None, style: Optional[Dict] = None) -> bool:
        """Onay kutusu ekleme"""
        def create_checkbutton(parent):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(parent, text=text, variable=var,
                               command=lambda: self._execute_command(command) if command else None)
            cb.var = var  # Store reference to variable
            return cb
            
        return self._add_widget(
            window_name, widget_name, 'checkbutton',
            create_checkbutton, x, y, width, height, style
        )
    
    def add_radiobutton(self, window_name: str, widget_name: str, text: str,
                        value: Any, variable_name: str,
                        x: int = 0, y: int = 0, width: int = 100, height: int = 30,
                        command: Optional[str] = None, style: Optional[Dict] = None) -> bool:
        """Radyo düğmesi ekleme"""
        def create_radiobutton(parent):
            # Shared variable management
            if not hasattr(self, '_radio_vars'):
                self._radio_vars = {}
            if variable_name not in self._radio_vars:
                self._radio_vars[variable_name] = tk.StringVar()
            
            var = self._radio_vars[variable_name]
            rb = tk.Radiobutton(parent, text=text, value=value, variable=var,
                               command=lambda: self._execute_command(command) if command else None)
            rb.var = var
            return rb
            
        return self._add_widget(
            window_name, widget_name, 'radiobutton',
            create_radiobutton, x, y, width, height, style
        )
    
    def add_scale(self, window_name: str, widget_name: str,
                  from_: float = 0, to: float = 100, orient: str = 'horizontal',
                  x: int = 0, y: int = 0, width: int = 150, height: int = 30,
                  command: Optional[str] = None, style: Optional[Dict] = None) -> bool:
        """Kaydırıcı ekleme"""
        return self._add_widget(
            window_name, widget_name, 'scale',
            lambda parent: tk.Scale(parent, from_=from_, to=to, orient=orient,
                                  command=lambda val: self._execute_command(command) if command else None),
            x, y, width, height, style
        )
    
    def add_progressbar(self, window_name: str, widget_name: str,
                        x: int = 0, y: int = 0, width: int = 200, height: int = 20,
                        maximum: float = 100, style: Optional[Dict] = None) -> bool:
        """İlerleme çubuğu ekleme (ttk)"""
        return self._add_widget(
            window_name, widget_name, 'progressbar',
            lambda parent: ttk.Progressbar(parent, maximum=maximum),
            x, y, width, height, style
        )
    
    def add_menu(self, window_name: str, menu_name: str, 
                 items: List[Dict[str, Any]]) -> bool:
        """Gelişmiş menü ekleme"""
        with self.lock:
            window_info = self._get_window(window_name)
            if not window_info:
                raise PdsXGuiException(f"Pencere bulunamadı: {window_name}")
            
            try:
                menubar = window_info.window.nametowidget(window_info.window['menu']) if window_info.window['menu'] else tk.Menu(window_info.window)
                menu = tk.Menu(menubar, tearoff=0)
                
                for item in items:
                    label = item.get("label", "")
                    command = item.get("command", "")
                    separator = item.get("separator", False)
                    submenu = item.get("submenu", None)
                    
                    if separator:
                        menu.add_separator()
                    elif submenu:
                        self._add_submenu(menu, label, submenu)
                    else:
                        menu.add_command(
                            label=label,
                            command=lambda cmd=command: self._execute_command(cmd) if cmd else None
                        )
                
                menubar.add_cascade(label=menu_name, menu=menu)
                window_info.window.config(menu=menubar)
                
                log.debug(f"Menü eklendi: {window_name}.{menu_name}")
                return True
                
            except Exception as e:
                log.error(f"Menü ekleme hatası: {e}")
                raise PdsXGuiException(f"Menü ekleme hatası: {e}")
    
    def _add_submenu(self, parent_menu: tk.Menu, label: str, items: List[Dict]):
        """Alt menü ekleme"""
        submenu = tk.Menu(parent_menu, tearoff=0)
        for item in items:
            item_label = item.get("label", "")
            command = item.get("command", "")
            submenu.add_command(
                label=item_label,
                command=lambda cmd=command: self._execute_command(cmd) if cmd else None
            )
        parent_menu.add_cascade(label=label, menu=submenu)
    
    def _add_widget(self, window_name: str, widget_name: str, widget_type: str,
                    widget_factory: Callable, x: int, y: int, width: int, height: int,
                    style: Optional[Dict] = None) -> bool:
        """Genel widget ekleme metodu"""
        with self.lock:
            window_info = self._get_window(window_name)
            if not window_info:
                raise PdsXGuiException(f"Pencere bulunamadı: {window_name}")
            
            widget_name_upper = widget_name.upper()
            if widget_name_upper in window_info.widgets:
                raise PdsXGuiException(f"Widget zaten mevcut: {widget_name}")
            
            try:
                widget = widget_factory(window_info.window)
                
                # Apply style
                if style:
                    self._apply_style(widget, style)
                else:
                    # Apply theme
                    theme = self.themes[self.current_theme]
                    if hasattr(widget, 'configure'):
                        widget.configure(bg=theme.get('bg', '#f0f0f0'), 
                                       fg=theme.get('fg', '#000000'))
                
                # Layout management
                if window_info.layout_type == LayoutType.PLACE:
                    widget.place(x=x, y=y, width=width, height=height)
                elif window_info.layout_type == LayoutType.PACK:
                    widget.pack(padx=x, pady=y)
                elif window_info.layout_type == LayoutType.GRID:
                    row, col = divmod(len(window_info.widgets), 3)  # Simple grid layout
                    widget.grid(row=row, column=col, padx=x, pady=y)
                
                # Store widget info
                widget_info = WidgetInfo(
                    widget=widget,
                    widget_type=widget_type,
                    properties=style or {},
                    layout_info={'x': x, 'y': y, 'width': width, 'height': height}
                )
                
                window_info.widgets[widget_name_upper] = widget_info
                
                log.debug(f"Widget eklendi: {window_name}.{widget_name} ({widget_type})")
                return True
                
            except Exception as e:
                log.error(f"Widget ekleme hatası: {e}")
                raise PdsXGuiException(f"Widget ekleme hatası: {e}")
    
    def _apply_style(self, widget: tk.Widget, style: Dict[str, Any]):
        """Widget'a stil uygulama"""
        if hasattr(widget, 'configure'):
            widget.configure(**style)
    
    def _get_window(self, window_name: str) -> Optional[WindowInfo]:
        """Pencere bilgisini al"""
        return self.windows.get(window_name.upper())
    
    def _get_widget(self, window_name: str, widget_name: str) -> Optional[WidgetInfo]:
        """Widget bilgisini al"""
        window_info = self._get_window(window_name)
        if window_info:
            return window_info.widgets.get(widget_name.upper())
        return None
    
    def _execute_command(self, command: str):
        """Komut çalıştırma"""
        if command and self.interpreter:
            try:
                self.interpreter.execute_command(command)
            except Exception as e:
                log.error(f"Komut çalıştırma hatası: {e}")
    
    def show_window(self, window_name: str) -> bool:
        """Pencereyi göster"""
        with self.lock:
            window_info = self._get_window(window_name)
            if not window_info:
                raise PdsXGuiException(f"Pencere bulunamadı: {window_name}")
            
            try:
                window_info.window.deiconify()
                window_info.window.lift()
                log.debug(f"Pencere gösterildi: {window_name}")
                return True
            except Exception as e:
                log.error(f"Pencere gösterme hatası: {e}")
                raise PdsXGuiException(f"Pencere gösterme hatası: {e}")
    
    def hide_window(self, window_name: str) -> bool:
        """Pencereyi gizle"""
        with self.lock:
            window_info = self._get_window(window_name)
            if not window_info:
                raise PdsXGuiException(f"Pencere bulunamadı: {window_name}")
            
            try:
                window_info.window.withdraw()
                log.debug(f"Pencere gizlendi: {window_name}")
                return True
            except Exception as e:
                log.error(f"Pencere gizleme hatası: {e}")
                raise PdsXGuiException(f"Pencere gizleme hatası: {e}")
    
    def close_window(self, window_name: str) -> bool:
        """Pencereyi kapat"""
        with self.lock:
            window_info = self._get_window(window_name)
            if not window_info:
                raise PdsXGuiException(f"Pencere bulunamadı: {window_name}")
            
            try:
                window_info.window.destroy()
                del self.windows[window_name.upper()]
                log.debug(f"Pencere kapatıldı: {window_name}")
                return True
            except Exception as e:
                log.error(f"Pencere kapatma hatası: {e}")
                raise PdsXGuiException(f"Pencere kapatma hatası: {e}")
    
    def bind_event(self, window_name: str, widget_name: str, 
                   event: str, handler: str) -> bool:
        """Widget'a olay bağlama"""
        with self.lock:
            widget_info = self._get_widget(window_name, widget_name)
            if not widget_info:
                raise PdsXGuiException(f"Widget bulunamadı: {window_name}.{widget_name}")
            
            try:
                tk_event = self._map_event(event)
                widget_info.widget.bind(
                    tk_event, 
                    lambda e: self._execute_command(handler)
                )
                widget_info.events[event] = handler
                log.debug(f"Olay bağlandı: {window_name}.{widget_name}, {event}")
                return True
            except Exception as e:
                log.error(f"Olay bağlama hatası: {e}")
                raise PdsXGuiException(f"Olay bağlama hatası: {e}")
    
    def set_theme(self, theme_name: str):
        """Tema değiştirme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            # Apply to all existing windows
            for window_info in self.windows.values():
                theme = self.themes[theme_name]
                window_info.window.configure(bg=theme['bg'])
                for widget_info in window_info.widgets.values():
                    if hasattr(widget_info.widget, 'configure'):
                        widget_info.widget.configure(
                            bg=theme.get('bg', '#f0f0f0'),
                            fg=theme.get('fg', '#000000')
                        )
    
    def _map_event(self, event: str) -> str:
        """Olay adını Tkinter formatına çevirme"""
        event_map = {
            "CLICK": "<Button-1>",
            "RIGHT_CLICK": "<Button-3>",
            "DOUBLE_CLICK": "<Double-Button-1>",
            "KEY_PRESS": "<Key>",
            "ENTER": "<Return>",
            "ESCAPE": "<Escape>",
            "FOCUS_IN": "<FocusIn>",
            "FOCUS_OUT": "<FocusOut>",
            "MOUSE_ENTER": "<Enter>",
            "MOUSE_LEAVE": "<Leave>",
            "KEY_UP": "<KeyRelease>",
            "MOUSE_MOVE": "<Motion>"
        }
        return event_map.get(event.upper(), event)
    
    def run_mainloop(self):
        """Ana GUI döngüsünü başlat"""
        if self.root:
            try:
                self.root.mainloop()
                log.info("GUI ana döngüsü başlatıldı")
            except Exception as e:
                log.error(f"GUI çalıştırma hatası: {e}")
                raise PdsXGuiException(f"GUI çalıştırma hatası: {e}")

class LibXGuiX:
    """Enhanced PDSX GUI Library - Main Interface"""
    
    def __init__(self, interpreter=None):
        self.interpreter = interpreter
        self.window_manager = EnhancedWindowManager(interpreter)
        self.gui_thread: Optional[Thread] = None
        self._gui_initialized = False  # rem: GUI thread durumu takibi
        self.metadata = {
            "libx_gui": {
                "version": "2.0.1",
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
                "dependencies": ["tkinter", "threading"],
                "features": [
                    "Enhanced widget management",
                    "Modern layout systems", 
                    "Theme support",
                    "Advanced event handling",
                    "Thread-safe operations",
                    "Canvas drawing support",
                    "Dialog systems",
                    "Drag & Drop support"  # rem: Sürükle-bırak desteği eklendi
                ]
            }
        }
    
    def parse_gui_command(self, command: str) -> bool:
        """Gelişmiş GUI komut ayrıştırma"""
        if not command or not command.strip():
            return False
            
        command = command.strip()
        command_upper = command.upper()
        
        try:
            # WINDOW commands
            if command_upper.startswith("WINDOW "):
                return self._parse_window_command(command)
            
            # WIDGET commands
            elif any(command_upper.startswith(widget + " ") for widget in 
                    ["BUTTON", "LABEL", "ENTRY", "INPUT", "LISTBOX", "TEXT", 
                     "CANVAS", "FRAME", "CHECKBUTTON", "RADIOBUTTON", "SCALE", "PROGRESSBAR"]):
                return self._parse_widget_command(command)
            
            # MENU commands
            elif command_upper.startswith("MENU "):
                return self._parse_menu_command(command)
            
            # WINDOW control commands
            elif command_upper.startswith(("SHOW", "HIDE", "CLOSE")):
                return self._parse_window_control_command(command)
            
            # EVENT commands
            elif command_upper.startswith("BIND "):
                return self._parse_bind_command(command)
            
            # THEME commands
            elif command_upper.startswith("THEME "):
                return self._parse_theme_command(command)
            
            # DIALOG commands
            elif command_upper.startswith(("MSGBOX ", "FILEDIALOG ", "COLORPICKER ")):
                return self._parse_dialog_command(command)
            
            # RUN command
            elif command_upper == "RUN":
                self.start_gui_thread()
                return True
            
            # rem: DRAG_SUPPORT komutu - widget'ları sürüklenebilir yapar
            elif command_upper.startswith("DRAG_SUPPORT "):
                return self._parse_drag_command(command)
            
            else:
                raise PdsXGuiException(f"Bilinmeyen GUI komutu: {command}")
                
        except Exception as e:
            log.error(f"GUI komut ayrıştırma hatası: '{command}' -> {e}", exc_info=True)
            # rem: Kullanıcıya doğrudan hata mesajı göster
            try:
                messagebox.showerror("GUI Komut Hatası", f"Komut işlenirken bir hata oluştu:\n\n{command}\n\nHata: {e}")
            except tk.TclError:
                # rem: GUI henüz hazır değilse konsola yazdır
                print(f"** GUI HATA (MessageBox gösterilemedi): {e} **")
            return False
    
    def _parse_window_command(self, command: str) -> bool:
        """WINDOW komutlarını ayrıştır - PDSX syntax: WINDOW "title", width, height"""
        
        # rem: GUI thread'ini başlat
        self._ensure_gui_thread()
        
        # PDSX Syntax: WINDOW "My Window", 400, 300
        pdsx_match = re.match(r'WINDOW\s+"([^"]+)"\s*,\s*(\d+)\s*,\s*(\d+)', command, re.IGNORECASE)
        if pdsx_match:
            title, width_str, height_str = pdsx_match.groups()
            width = int(width_str)
            height = int(height_str)
            name = "main_window"  # rem: Varsayılan pencere ismi
            
            log.info(f"PDSX WINDOW komutu: title='{title}', width={width}, height={height}")
            
            # rem: Thread-safe pencere oluşturma
            def create_window():
                result = self.window_manager.create_window(
                    name, width, height, title, True, LayoutType.PLACE
                )
                if result:
                    self.window_manager.show_window(name)
            
            self.window_manager.root.after(10, create_window)
            return True
        
        # Original LibX Syntax: WINDOW name WIDTH=400 HEIGHT=300 TITLE="My Window" LAYOUT=PLACE
        original_match = re.match(
            r"WINDOW\s+(\w+)(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?(?:\s+TITLE=\"([^\"]*)\")?"
            r"(?:\s+LAYOUT=(\w+))?(?:\s+RESIZABLE=(TRUE|FALSE))?",
            command, re.IGNORECASE
        )
        
        if original_match:
            name, width, height, title, layout, resizable = original_match.groups()
            width = int(width) if width else 400
            height = int(height) if height else 300
            title = title or name
            layout_type = LayoutType(layout.lower()) if layout else LayoutType.PLACE
            resizable_bool = resizable != "FALSE" if resizable else True
            
            # rem: Thread-safe pencere oluşturma
            def create_window():
                result = self.window_manager.create_window(
                    name, width, height, title, resizable_bool, layout_type
                )
                if result:
                    self.window_manager.show_window(name)
            
            self.window_manager.root.after(10, create_window)
            return True
        
        raise PdsXGuiException("WINDOW komutu sözdizimi hatası")
    
    def _parse_widget_command(self, command: str) -> bool:
        """Widget komutlarını ayrıştır"""
        # Parse different widget types
        parts = command.split()
        widget_type = parts[0].upper()
        
        if widget_type == "BUTTON":
            return self._parse_button_command(command)
        elif widget_type == "LABEL":
            return self._parse_label_command(command)
        elif widget_type in ["ENTRY", "INPUT"]:
            return self._parse_entry_command(command)
        elif widget_type == "LISTBOX":
            return self._parse_listbox_command(command)
        elif widget_type == "TEXT":
            return self._parse_text_command(command)
        elif widget_type == "CANVAS":
            return self._parse_canvas_command(command)
        elif widget_type == "LISTBOX":
            return self._parse_listbox_command(command)
        elif widget_type == "FRAME":
            return self._parse_frame_command(command)
        elif widget_type == "CHECKBUTTON":
            return self._parse_checkbutton_command(command)
        elif widget_type == "RADIOBUTTON":
            return self._parse_radiobutton_command(command)
        elif widget_type == "SCALE":
            return self._parse_scale_command(command)
        elif widget_type == "PROGRESSBAR":
            return self._parse_progressbar_command(command)
        # Add more widget types...
        
        return False
    
    def _parse_button_command(self, command: str) -> bool:
        """BUTTON komutunu ayrıştır - PDSX syntax: BUTTON "text", x, y, width, height"""
        
        # PDSX Syntax: BUTTON "Sprite Test", 50, 400, 150, 30
        pdsx_match = re.match(r'BUTTON\s+"([^"]+)"\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', command, re.IGNORECASE)
        if pdsx_match:
            text, x_str, y_str, width_str, height_str = pdsx_match.groups()
            x, y, width, height = int(x_str), int(y_str), int(width_str), int(height_str)
            
            # rem: Varsayılan pencere ve widget ismi kullan
            window_name = "main_window"
            widget_name = f"button_{x}_{y}"  # rem: Konum tabanlı benzersiz isim
            
            log.info(f"PDSX BUTTON komutu: text='{text}', x={x}, y={y}, w={width}, h={height}")
            
            # rem: Thread-safe widget ekleme
            def add_widget():
                return self.window_manager.add_button(
                    window_name, widget_name, text, x, y, width, height, None
                )
            
            self.window_manager.root.after(10, add_widget)
            return True
        
        # Original LibX Syntax: BUTTON window_name widget_name "text" X=10 Y=20 WIDTH=100 HEIGHT=30 COMMAND="print('clicked')"
        original_match = re.match(
            r"BUTTON\s+(\w+)\s+(\w+)\s+\"([^\"]*)\""
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+COMMAND=\"([^\"]*)\")?"
            , command, re.IGNORECASE
        )
        
        if original_match:
            window_name, widget_name, text, x, y, width, height, cmd = original_match.groups()
            
            # rem: Thread-safe widget ekleme
            def add_widget():
                return self.window_manager.add_button(
                    window_name, widget_name, text,
                    int(x) if x else 0, int(y) if y else 0,
                    int(width) if width else 100, int(height) if height else 30,
                    cmd
                )
            
            self.window_manager.root.after(10, add_widget)
            return True
        
        raise PdsXGuiException("BUTTON komutu sözdizimi hatası")
    
    def _parse_label_command(self, command: str) -> bool:
        """LABEL komutunu ayrıştır"""
        match = re.match(
            r"LABEL\s+(\w+)\s+(\w+)\s+\"([^\"]*)\""
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, text, x, y, width, height = match.groups()
            return self.window_manager.add_label(
                window_name, widget_name, text,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 100, int(height) if height else 30
            )
        
        raise PdsXGuiException("LABEL komutu sözdizimi hatası")
    
    def _parse_entry_command(self, command: str) -> bool:
        """ENTRY/INPUT komutunu ayrıştır"""
        match = re.match(
            r"(?:ENTRY|INPUT)\s+(\w+)\s+(\w+)"
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+PLACEHOLDER=\"([^\"]*)\")?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, x, y, width, height, placeholder = match.groups()
            return self.window_manager.add_entry(
                window_name, widget_name,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 100, int(height) if height else 30,
                placeholder or ""
            )
        
        raise PdsXGuiException("ENTRY komutu sözdizimi hatası")
    
    def _parse_canvas_command(self, command: str) -> bool:
        """CANVAS komutunu ayrıştır"""
        # CANVAS window_name widget_name X=x Y=y WIDTH=w HEIGHT=h BG="color"
        match = re.match(
            r"CANVAS\s+(\w+)\s+(\w+)"
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+BG=\"([^\"]*)\")?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, x, y, width, height, bg_color = match.groups()
            return self.window_manager.add_canvas(
                window_name, widget_name,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 200, int(height) if height else 150,
                bg_color or "#ffffff"
            )
        
        raise PdsXGuiException("CANVAS komutu sözdizimi hatası")
    
    def _parse_text_command(self, command: str) -> bool:
        """TEXT komutunu ayrıştır"""
        # TEXT window_name widget_name X=x Y=y WIDTH=w HEIGHT=h TEXT="content"
        match = re.match(
            r"TEXT\s+(\w+)\s+(\w+)"
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+TEXT=\"([^\"]*)\")?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, x, y, width, height, text_content = match.groups()
            return self.window_manager.add_text(
                window_name, widget_name,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 200, int(height) if height else 100,
                text_content or ""
            )
        
        raise PdsXGuiException("TEXT komutu sözdizimi hatası")
    
    def _parse_listbox_command(self, command: str) -> bool:
        """LISTBOX komutunu ayrıştır"""
        # LISTBOX window_name widget_name X=x Y=y WIDTH=w HEIGHT=h ITEMS=["item1","item2"]
        match = re.match(
            r"LISTBOX\s+(\w+)\s+(\w+)"
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+ITEMS=(\[.*?\]))?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, x, y, width, height, items_str = match.groups()
            items = []
            if items_str:
                try:
                    items = json.loads(items_str)
                except json.JSONDecodeError:
                    raise PdsXGuiException("LISTBOX ITEMS formatı bozuk (JSON bekleniyor)")
            
            return self.window_manager.add_listbox(
                window_name, widget_name, items,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 150, int(height) if height else 100
            )
        
        raise PdsXGuiException("LISTBOX komutu sözdizimi hatası")
    
    def _parse_frame_command(self, command: str) -> bool:
        """FRAME komutunu ayrıştır"""
        # FRAME window_name widget_name X=x Y=y WIDTH=w HEIGHT=h RELIEF=flat BORDERWIDTH=1
        match = re.match(
            r"FRAME\s+(\w+)\s+(\w+)"
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+RELIEF=(\w+))?(?:\s+BORDERWIDTH=(\d+))?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, x, y, width, height, relief, borderwidth = match.groups()
            return self.window_manager.add_frame(
                window_name, widget_name,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 200, int(height) if height else 150,
                relief or 'flat', int(borderwidth) if borderwidth else 1
            )
        
        raise PdsXGuiException("FRAME komutu sözdizimi hatası")
    
    def _parse_checkbutton_command(self, command: str) -> bool:
        """CHECKBUTTON komutunu ayrıştır"""
        # CHECKBUTTON window_name widget_name "text" X=x Y=y WIDTH=w HEIGHT=h COMMAND="handler"
        match = re.match(
            r"CHECKBUTTON\s+(\w+)\s+(\w+)\s+\"([^\"]*)\""
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+COMMAND=\"([^\"]*)\")?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, text, x, y, width, height, cmd = match.groups()
            return self.window_manager.add_checkbutton(
                window_name, widget_name, text,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 100, int(height) if height else 30,
                cmd
            )
        
        raise PdsXGuiException("CHECKBUTTON komutu sözdizimi hatası")
    
    def _parse_radiobutton_command(self, command: str) -> bool:
        """RADIOBUTTON komutunu ayrıştır"""
        # RADIOBUTTON window_name widget_name "text" VALUE="value" VAR="variable" X=x Y=y WIDTH=w HEIGHT=h COMMAND="handler"
        match = re.match(
            r"RADIOBUTTON\s+(\w+)\s+(\w+)\s+\"([^\"]*)\""
            r"\s+VALUE=\"([^\"]*)\"\s+VAR=\"(\w+)\""
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+COMMAND=\"([^\"]*)\")?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, text, value, var_name, x, y, width, height, cmd = match.groups()
            return self.window_manager.add_radiobutton(
                window_name, widget_name, text, value, var_name,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 100, int(height) if height else 30,
                cmd
            )
        
        raise PdsXGuiException("RADIOBUTTON komutu sözdizimi hatası")
    
    def _parse_scale_command(self, command: str) -> bool:
        """SCALE komutunu ayrıştır"""
        # SCALE window_name widget_name FROM=0 TO=100 ORIENT=horizontal X=x Y=y WIDTH=w HEIGHT=h COMMAND="handler"
        match = re.match(
            r"SCALE\s+(\w+)\s+(\w+)"
            r"(?:\s+FROM=([\d\.]+))?(?:\s+TO=([\d\.]+))?(?:\s+ORIENT=(\w+))?"
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+COMMAND=\"([^\"]*)\")?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, from_val, to_val, orient, x, y, width, height, cmd = match.groups()
            return self.window_manager.add_scale(
                window_name, widget_name,
                float(from_val) if from_val else 0, float(to_val) if to_val else 100,
                orient or 'horizontal',
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 150, int(height) if height else 30,
                cmd
            )
        
        raise PdsXGuiException("SCALE komutu sözdizimi hatası")
    
    def _parse_progressbar_command(self, command: str) -> bool:
        """PROGRESSBAR komutunu ayrıştır"""
        # PROGRESSBAR window_name widget_name X=x Y=y WIDTH=w HEIGHT=h MAX=100
        match = re.match(
            r"PROGRESSBAR\s+(\w+)\s+(\w+)"
            r"(?:\s+X=(\d+))?(?:\s+Y=(\d+))?(?:\s+WIDTH=(\d+))?(?:\s+HEIGHT=(\d+))?"
            r"(?:\s+MAX=([\d\.]+))?"
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, x, y, width, height, maximum = match.groups()
            return self.window_manager.add_progressbar(
                window_name, widget_name,
                int(x) if x else 0, int(y) if y else 0,
                int(width) if width else 200, int(height) if height else 20,
                float(maximum) if maximum else 100
            )
        
        raise PdsXGuiException("PROGRESSBAR komutu sözdizimi hatası")
    
    def _parse_window_control_command(self, command: str) -> bool:
        """Pencere kontrol komutlarını ayrıştır"""
        parts = command.split()
        
        # Tek SHOW, HIDE, CLOSE komutlarını destekle (varsayılan pencere)
        if len(parts) == 1:
            action = parts[0].upper()
            if action in ["SHOW", "HIDE", "CLOSE"]:
                # Varsayılan pencere ismini kullan (ilk pencere)
                window_names = list(self.window_manager.windows.keys())
                if window_names:
                    window_name = window_names[0]  # İlk pencereyi kullan
                else:
                    log.warning("Hiç pencere tanımlanmamış")
                    return False
            else:
                raise PdsXGuiException("Bilinmeyen pencere kontrol komutu")
        elif len(parts) == 2:
            action, window_name = parts
            action = action.upper()
        else:
            raise PdsXGuiException("Pencere kontrol komutu sözdizimi hatası")
        
        if action == "SHOW":
            return self.window_manager.show_window(window_name)
        elif action == "HIDE":
            return self.window_manager.hide_window(window_name)
        elif action == "CLOSE":
            return self.window_manager.close_window(window_name)
        
        return False
    
    def _parse_bind_command(self, command: str) -> bool:
        """BIND komutunu ayrıştır"""
        # BIND window_name widget_name EVENT="CLICK" HANDLER="button_clicked"
        match = re.match(
            r"BIND\s+(\w+)\s+(\w+)\s+EVENT=\"([^\"]*)\"\s+HANDLER=\"([^\"]*)\""
            , command, re.IGNORECASE
        )
        
        if match:
            window_name, widget_name, event, handler = match.groups()
            return self.window_manager.bind_event(window_name, widget_name, event, handler)
        
        raise PdsXGuiException("BIND komutu sözdizimi hatası")
    
    def _parse_theme_command(self, command: str) -> bool:
        """THEME komutunu ayrıştır"""
        # THEME dark
        match = re.match(r"THEME\s+(\w+)", command, re.IGNORECASE)
        if match:
            theme_name = match.group(1).lower()
            self.window_manager.set_theme(theme_name)
            return True
        
        raise PdsXGuiException("THEME komutu sözdizimi hatası")
    
    def _parse_dialog_command(self, command: str) -> bool:
        """Dialog komutlarını ayrıştır"""
        command_upper = command.upper()
        
        if command_upper.startswith("MSGBOX "):
            # MSGBOX "message" TITLE="title" TYPE=INFO
            match = re.match(
                r"MSGBOX\s+\"([^\"]*)\""
                r"(?:\s+TITLE=\"([^\"]*)\")?"
                r"(?:\s+TYPE=(\w+))?"
                , command, re.IGNORECASE
            )
            if match:
                message, title, msg_type = match.groups()
                title = title or "Bilgi"
                msg_type = (msg_type or "info").lower()
                
                if msg_type == "info":
                    messagebox.showinfo(title, message)
                elif msg_type == "warning":
                    messagebox.showwarning(title, message)
                elif msg_type == "error":
                    messagebox.showerror(title, message)
                elif msg_type == "question":
                    messagebox.askyesno(title, message)
                
                return True
        
        elif command_upper.startswith("FILEDIALOG "):
            # FILEDIALOG OPEN VAR=filename
            match = re.match(
                r"FILEDIALOG\s+(OPEN|SAVE)\s+VAR=(\w+)"
                r"(?:\s+TITLE=\"([^\"]*)\")?"
                r"(?:\s+FILETYPES=\"([^\"]*)\")?"
                , command, re.IGNORECASE
            )
            if match:
                action, var_name, title, filetypes = match.groups()
                title = title or "Dosya Seç"
                
                if action.upper() == "OPEN":
                    filename = filedialog.askopenfilename(title=title)
                else:
                    filename = filedialog.asksaveasfilename(title=title)
                
                # Store result in interpreter variable
                if self.interpreter and filename:
                    self.interpreter.set_variable(var_name, filename)
                
                return True
        
        return False
    
    def _parse_menu_command(self, command: str) -> bool:
        """MENU komutunu ayrıştır"""
        # MENU window_name "menu_name" [items]
        try:
            import json
            # Extract window name, menu name and items
            match = re.match(r'MENU\s+(\w+)\s+"([^"]+)"\s+(\[.*\])', command, re.IGNORECASE)
            if match:
                window_name, menu_name, items_str = match.groups()
                items = json.loads(items_str)
                
                return self.window_manager.add_menu(window_name, menu_name, items)
            
            raise PdsXGuiException("MENU komutu sözdizimi hatası")
        except json.JSONDecodeError as e:
            raise PdsXGuiException(f"MENU items JSON hatası: {e}")
        except Exception as e:
            raise PdsXGuiException(f"MENU komutu hatası: {e}")
    
    def _parse_drag_command(self, command: str) -> bool:
        """DRAG_SUPPORT komutunu ayrıştır"""
        # rem: DRAG_SUPPORT window.widget şeklinde kullanılır
        match = re.match(r"DRAG_SUPPORT\s+(\w+)\.(\w+)", command, re.IGNORECASE)
        if match:
            window_name, widget_name = match.groups()
            return self.window_manager.enable_drag(window_name, widget_name)
        
        raise PdsXGuiException("DRAG_SUPPORT komutu sözdizimi hatası: DRAG_SUPPORT pencere.widget şeklinde olmalı")
    
    def start_gui_thread(self) -> None:
        """rem: GUI thread'ini güvenli bir şekilde başlatır"""
        with self.window_manager.lock:
            if self.gui_thread and self.gui_thread.is_alive():
                return  # rem: Zaten çalışıyor
                
            log.info("GUI thread başlatılıyor...")
            self.window_manager._ensure_root()
            self.gui_thread = Thread(target=self._run_gui_mainloop, daemon=True)
            self.gui_thread.start()
            self._gui_initialized = True
            log.info("GUI thread başlatıldı.")
    
    def _run_gui_mainloop(self):
        """rem: GUI ana döngüsünü ayrı thread'de çalıştırır"""
        try:
            self.window_manager.run_mainloop()
        except Exception as e:
            log.error(f"GUI thread hatası: {e}")
    
    def _ensure_gui_thread(self):
        """rem: GUI thread'inin hazır olduğundan emin olur"""
        if not self._gui_initialized:
            self.start_gui_thread()
            # rem: Thread'in başlamasını bekle
            import time
            time.sleep(0.1)
    
    def get_widget_value(self, window_name: str, widget_name: str) -> Any:
        """Widget değerini al"""
        widget_info = self.window_manager._get_widget(window_name, widget_name)
        if not widget_info:
            raise PdsXGuiException(f"Widget bulunamadı: {window_name}.{widget_name}")
        
        widget = widget_info.widget
        widget_type = widget_info.widget_type
        
        if widget_type == 'entry':
            return widget.get()
        elif widget_type == 'text':
            return widget.get("1.0", tk.END).strip()
        elif widget_type == 'checkbutton':
            return widget.var.get()
        elif widget_type == 'radiobutton':
            return widget.var.get()
        elif widget_type == 'scale':
            return widget.get()
        elif widget_type == 'listbox':
            selection = widget.curselection()
            return [widget.get(i) for i in selection]
        
        return None
    
    def set_widget_value(self, window_name: str, widget_name: str, value: Any) -> bool:
        """Widget değerini ayarla"""
        widget_info = self.window_manager._get_widget(window_name, widget_name)
        if not widget_info:
            raise PdsXGuiException(f"Widget bulunamadı: {window_name}.{widget_name}")
        
        widget = widget_info.widget
        widget_type = widget_info.widget_type
        
        try:
            if widget_type == 'entry':
                widget.delete(0, tk.END)
                widget.insert(0, str(value))
            elif widget_type == 'text':
                widget.delete("1.0", tk.END)
                widget.insert("1.0", str(value))
            elif widget_type == 'label':
                widget.configure(text=str(value))
            elif widget_type == 'checkbutton':
                widget.var.set(bool(value))
            elif widget_type == 'scale':
                widget.set(float(value))
            elif widget_type == 'progressbar':
                widget['value'] = float(value)
            
            return True
        except Exception as e:
            log.error(f"Widget değer ayarlama hatası: {e}")
            return False

# Alias for backward compatibility
LibXGui = LibXGuiX

def main():
    """Test function"""
    print("LibXGuiX - PDSX Enhanced GUI Library v2.0.1")
    print(f"Python version: {sys.version}")
    print("Bu modül PDSX v12X ile birlikte kullanılır.")

if __name__ == "__main__":
    main()
