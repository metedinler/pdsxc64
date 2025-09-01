#!/usr/bin/env python3
"""
GUI Debug System - Separated from gui_manager.py
🍎 GUI Debug Helper - Component tracking system
"""

import os
import tkinter as tk
from tkinter import messagebox, filedialog

class GUIDebugHelper:
    """🍎 GUI Debug Helper - GUI componentlerine kod atama sistemi"""
    
    def __init__(self):
        self.debug_mode = False
        self.gui_component_counter = 1
        self.component_registry = {}
        
        # 🍎 Environment variable ile debug mode başlatma
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
        """Widget'ı registry'e kaydet"""
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

# Global GUI debug helper
gui_debug = GUIDebugHelper()

# 🍎 GUI Debug Wrapper Functions
def debug_button(parent, debug_name="Button", text="", **kwargs):
    """Debug-enabled Button wrapper"""
    try:
        original_text = text
        debug_text = gui_debug.format_text_with_debug("BUTTON", text)
        
        btn = tk.Button(parent, text=debug_text, **kwargs)
        
        # Widget'ı registry'e kaydet
        code = gui_debug.register_component(btn, "Button", original_text)
        
        if gui_debug.debug_mode:
            gui_debug.log_component(code, "created")
        return btn
    except Exception as e:
        print(f"❌ Debug button creation error: {e}")
        # Fallback
        safe_kwargs = {k: v for k, v in kwargs.items() if k != 'font'}
        return tk.Button(parent, text=text, **safe_kwargs)

def debug_label(parent, debug_name="Label", text="", **kwargs):
    """Debug-enabled Label wrapper"""
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
    kwargs.pop('debug_name', None)
    
    frame = tk.Frame(parent, **kwargs)
    
    # Widget'ı registry'e kaydet
    code = gui_debug.register_component(frame, "Frame", "")
    
    if gui_debug.debug_mode:
        gui_debug.log_component(code, "created")
        if 'bg' in kwargs:
            title_label = tk.Label(frame, text=f"[{code}]", 
                                 bg=kwargs['bg'], fg="#666666", font=("Arial", 8))
            title_label.pack(side=tk.TOP, anchor=tk.W)
    return frame

def safe_messagebox(msg_type, title, message):
    """Safe messagebox that works in both debug and normal mode"""
    try:
        debug_title = gui_debug.format_text_with_debug("MESSAGEBOX", title)
        
        if msg_type == "info":
            return messagebox.showinfo(debug_title, message)
        elif msg_type == "warning":
            return messagebox.showwarning(debug_title, message)
        elif msg_type == "error":
            return messagebox.showerror(debug_title, message)
        elif msg_type == "question":
            return messagebox.askyesno(debug_title, message)
    except Exception as e:
        print(f"❌ Messagebox error: {e}")
        # Fallback to standard messagebox
        if msg_type == "info":
            return messagebox.showinfo(title, message)
        elif msg_type == "warning":
            return messagebox.showwarning(title, message)
        elif msg_type == "error":
            return messagebox.showerror(title, message)
        elif msg_type == "question":
            return messagebox.askyesno(title, message)
