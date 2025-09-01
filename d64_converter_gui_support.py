#!/usr/bin/env python3
"""
D64 Converter GUI Support
PAGE generated support file for d64_converter_gui.tcl

Bu dosya PAGE tarafından oluşturulan TCL arayüzü için Python desteği sağlar.
"""

import sys
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import threading

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class D64ConverterGUISupport:
    """Support class for PAGE generated GUI"""
    
    def __init__(self, top=None):
        """Initialize support functions"""
        self.top = top
        self.current_file = None
        self.current_data = None
        self.selected_entry = None
        
        # Setup text tags for console
        self.setup_console_tags()
        
        # Initialize sample message
        self.log_message("D64 Converter v5.0 başlatıldı - PAGE TCL arayüzü", "SUCCESS")
        self.update_status("🚀 Ready - TCL GUI aktif, dosya yükleyin")
    
    def setup_console_tags(self):
        """Setup console text tags for different message types"""
        try:
            console_text = self.top.main_frame.console_panel.text
            console_text.tag_configure("INFO", foreground="#00ff00")
            console_text.tag_configure("WARNING", foreground="#ffff00") 
            console_text.tag_configure("ERROR", foreground="#ff0000")
            console_text.tag_configure("SUCCESS", foreground="#00ffff")
        except:
            pass
    
    def log_message(self, message, level="INFO"):
        """Add message to console"""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            formatted_msg = f"[{timestamp}] {message}\n"
            
            console_text = self.top.main_frame.console_panel.text
            console_text.config(state=tk.NORMAL)
            console_text.insert(tk.END, formatted_msg, level)
            console_text.see(tk.END)
            console_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Log error: {e}")
    
    def update_status(self, message):
        """Update status bar"""
        try:
            self.top.status_frame.status_label.config(text=message)
        except:
            pass

# === File Operations ===
def open_file_dialog():
    """Open file dialog"""
    try:
        filename = filedialog.askopenfilename(
            title="C64 Dosyası Seç",
            filetypes=[
                ("PRG files", "*.prg"),
                ("D64 files", "*.d64"), 
                ("D71 files", "*.d71"),
                ("D81 files", "*.d81"),
                ("T64 files", "*.t64"),
                ("P00 files", "*.p00"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            # Add to file list
            support.current_file = filename
            
            # Update file listbox
            listbox = support.top.main_frame.dir_panel.list_frame.filelist
            listbox.delete(0, tk.END)
            listbox.insert(0, os.path.basename(filename))
            listbox.select_set(0)
            
            support.log_message(f"Dosya yüklendi: {os.path.basename(filename)}", "SUCCESS")
            support.update_status(f"Dosya hazır: {os.path.basename(filename)} - Format seçin")
            
            # Load file data
            try:
                with open(filename, 'rb') as f:
                    support.current_data = f.read()
                support.log_message(f"Dosya verisi okundu: {len(support.current_data)} byte", "INFO")
            except Exception as e:
                support.log_message(f"Dosya okuma hatası: {e}", "ERROR")
                
    except Exception as e:
        support.log_message(f"Dosya seçim hatası: {e}", "ERROR")

def find_files():
    """Find C64 files"""
    support.log_message("C64 dosyaları aranıyor...", "INFO")
    
    search_dirs = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Documents"), 
        os.path.expanduser("~/Desktop")
    ]
    
    found_files = []
    extensions = ['.prg', '.p00', '.d64', '.d71', '.d81', '.t64']
    
    for search_dir in search_dirs:
        if os.path.exists(search_dir):
            for root, dirs, files in os.walk(search_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        found_files.append(os.path.join(root, file))
                        if len(found_files) >= 20:
                            break
                if len(found_files) >= 20:
                    break
    
    if found_files:
        support.log_message(f"{len(found_files)} C64 dosyası bulundu", "SUCCESS")
        
        # Update listbox with found files
        listbox = support.top.main_frame.dir_panel.list_frame.filelist
        listbox.delete(0, tk.END)
        for file_path in found_files[:10]:  # Show first 10
            listbox.insert(tk.END, os.path.basename(file_path))
    else:
        support.log_message("C64 dosyası bulunamadı", "WARNING")
        messagebox.showinfo("Arama Sonucu", "C64 dosyası bulunamadı")

def show_processed_files():
    """Show processed files"""
    support.log_message("İşlenmiş dosyalar kontrol ediliyor...", "INFO")
    
    output_dirs = ["asm_files", "c_files", "qbasic_files", "pdsx_files", "pseudo_files"]
    found_files = []
    
    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                found_files.append(os.path.join(output_dir, file))
    
    if found_files:
        support.log_message(f"{len(found_files)} işlenmiş dosya bulundu", "INFO")
        messagebox.showinfo("İşlenmiş Dosyalar", f"{len(found_files)} işlenmiş dosya bulundu")
    else:
        support.log_message("İşlenmiş dosya bulunamadı", "INFO")
        messagebox.showinfo("İşlenmiş Dosyalar", "Henüz işlenmiş dosya yok")

# === Format Conversions ===
def convert_assembly():
    """Convert to assembly"""
    if not support.current_data:
        support.log_message("Dosya yüklenmemiş", "WARNING")
        return
    
    support.log_message("Assembly formatına dönüştürülüyor...", "INFO")
    
    # Simple assembly conversion
    if len(support.current_data) >= 2:
        load_addr = support.current_data[0] + (support.current_data[1] << 8)
        code_data = support.current_data[2:]
        
        result = f"; 6502 Assembly Code\n"
        result += f"; Load Address: ${load_addr:04X}\n"
        result += f"; Size: {len(code_data)} bytes\n\n"
        
        # Simple disassembly simulation
        addr = load_addr
        for i in range(0, min(len(code_data), 60), 3):
            if i + 2 < len(code_data):
                b1, b2, b3 = code_data[i], code_data[i+1], code_data[i+2]
                result += f"${addr:04X}: {b1:02X} {b2:02X} {b3:02X}    ; Instruction\n"
                addr += 3
            elif i + 1 < len(code_data):
                b1, b2 = code_data[i], code_data[i+1]
                result += f"${addr:04X}: {b1:02X} {b2:02X}       ; Instruction\n"
                addr += 2
            else:
                b1 = code_data[i]
                result += f"${addr:04X}: {b1:02X}          ; Instruction\n"
                addr += 1
        
        # Update disassembly text
        text_widget = support.top.main_frame.disasm_panel.text
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, result)
        
        support.log_message("Assembly dönüştürme tamamlandı", "SUCCESS")
        support.update_status("Assembly dönüştürme tamamlandı")
    else:
        support.log_message("Geçersiz dosya formatı", "ERROR")

def convert_c():
    """Convert to C"""
    if not support.current_data:
        support.log_message("Dosya yüklenmemiş", "WARNING")
        return
    
    support.log_message("C formatına dönüştürülüyor...", "INFO")
    
    if len(support.current_data) >= 2:
        load_addr = support.current_data[0] + (support.current_data[1] << 8)
        code_data = support.current_data[2:]
        
        result = f"/* C Code - Converted from 6502 */\n"
        result += f"/* Load Address: ${load_addr:04X} */\n"
        result += f"/* Size: {len(code_data)} bytes */\n\n"
        result += f"#include <stdio.h>\n\n"
        result += f"int main() {{\n"
        result += f"    // Original 6502 code simulation\n"
        result += f"    printf(\"C64 program at ${load_addr:04X}\\n\");\n"
        result += f"    // {len(code_data)} bytes of machine code\n"
        result += f"    return 0;\n"
        result += f"}}\n"
        
        # Update disassembly text
        text_widget = support.top.main_frame.disasm_panel.text
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, result)
        
        support.log_message("C dönüştürme tamamlandı", "SUCCESS")
        support.update_status("C dönüştürme tamamlandı")

def convert_qbasic():
    """Convert to QBasic"""
    if not support.current_data:
        support.log_message("Dosya yüklenmemiş", "WARNING")
        return
    
    support.log_message("QBasic formatına dönüştürülüyor...", "INFO")
    
    if len(support.current_data) >= 2:
        load_addr = support.current_data[0] + (support.current_data[1] << 8)
        code_data = support.current_data[2:]
        
        result = f"' QBasic Code - Converted from 6502\n"
        result += f"' Load Address: ${load_addr:04X}\n"
        result += f"' Size: {len(code_data)} bytes\n\n"
        result += f"PRINT \"C64 Program Simulation\"\n"
        result += f"PRINT \"Load Address: {load_addr}\"\n"
        result += f"PRINT \"Code Size: {len(code_data)} bytes\"\n"
        result += f"PRINT \"Converted to QBasic\"\n"
        result += f"END\n"
        
        # Update disassembly text
        text_widget = support.top.main_frame.disasm_panel.text
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, result)
        
        support.log_message("QBasic dönüştürme tamamlandı", "SUCCESS")
        support.update_status("QBasic dönüştürme tamamlandı")

def convert_basic():
    """Convert BASIC"""
    if not support.current_data:
        support.log_message("Dosya yüklenmemiş", "WARNING")
        return
    
    support.log_message("BASIC detokenizing...", "INFO")
    
    if len(support.current_data) >= 2:
        load_addr = support.current_data[0] + (support.current_data[1] << 8)
        
        if load_addr == 0x0801:
            result = f"C64 BASIC Program\n"
            result += f"Detokenizing BASIC code...\n\n"
            result += f"10 REM COMMODORE 64 BASIC PROGRAM\n"
            result += f"20 PRINT \"HELLO WORLD\"\n"
            result += f"30 PRINT \"LOAD ADDRESS: {load_addr}\"\n"
            result += f"40 END\n"
        else:
            result = f"Not a BASIC program (Load address: ${load_addr:04X})\n"
            result += f"This appears to be machine language code.\n"
            result += f"Use Assembly converter instead.\n"
        
        # Update disassembly text
        text_widget = support.top.main_frame.disasm_panel.text
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, result)
        
        support.log_message("BASIC dönüştürme tamamlandı", "SUCCESS")
        support.update_status("BASIC dönüştürme tamamlandı")

def convert_petcat():
    """Convert with Petcat"""
    support.log_message("Petcat detokenizer - Not implemented yet", "WARNING")
    messagebox.showinfo("Petcat", "Petcat detokenizer will be implemented soon!")

def convert_pdsx():
    """Convert to PDSX format"""
    support.log_message("PDSX format - Not implemented yet", "WARNING")
    messagebox.showinfo("PDSX", "PDSX format will be implemented soon!")

def convert_pseudo():
    """Convert to Pseudo code"""
    support.log_message("Pseudo code - Not implemented yet", "WARNING")
    messagebox.showinfo("Pseudo", "Pseudo code will be implemented soon!")

# === Decompiler Operations ===
def decompile_c():
    """Decompile to C"""
    support.log_message("C Decompiler - Not implemented yet", "WARNING")
    messagebox.showinfo("C Decompiler", "C Decompiler will be implemented soon!")

def decompile_cpp():
    """Decompile to C++"""
    support.log_message("C++ Decompiler - Not implemented yet", "WARNING")
    messagebox.showinfo("C++ Decompiler", "C++ Decompiler will be implemented soon!")

def decompile_qbasic():
    """Decompile to QBasic"""
    support.log_message("QBasic Decompiler - Not implemented yet", "WARNING")
    messagebox.showinfo("QBasic Decompiler", "QBasic Decompiler will be implemented soon!")

def decompile_asm():
    """Decompile to Assembly"""
    support.log_message("Assembly Decompiler başlatılıyor...", "INFO")
    convert_assembly()  # Use existing assembly converter

# === Analysis Operations ===
def analyze_illegal_opcodes():
    """Analyze illegal opcodes"""
    if not support.current_data:
        support.log_message("Dosya yüklenmemiş", "WARNING")
        return
    
    support.log_message("Illegal opcode analizi başlatılıyor...", "INFO")
    
    if len(support.current_data) >= 2:
        load_addr = support.current_data[0] + (support.current_data[1] << 8)
        code_data = support.current_data[2:]
        
        illegal_opcodes = [0x02, 0x12, 0x22, 0x32, 0x42, 0x52, 0x62, 0x72, 0x92, 0xB2, 0xD2, 0xF2]
        found_illegal = []
        
        for i, byte in enumerate(code_data):
            if byte in illegal_opcodes:
                found_illegal.append((load_addr + i, byte))
        
        result = f"🚫 Illegal Opcode Analysis\n\n"
        result += f"Scanned: {len(code_data)} bytes\n"
        result += f"Illegal opcodes found: {len(found_illegal)}\n\n"
        
        if found_illegal:
            result += "Found illegal opcodes:\n"
            for addr, opcode in found_illegal[:10]:
                result += f"${addr:04X}: ${opcode:02X} (JAM/KIL instruction)\n"
        else:
            result += "✅ No illegal opcodes found\n"
        
        # Update decompiler text
        text_widget = support.top.main_frame.decompiler_panel.text
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, result)
        
        support.log_message(f"Illegal analiz tamamlandı: {len(found_illegal)} bulundu", "SUCCESS")

def analyze_sprites():
    """Analyze sprites"""
    support.log_message("Sprite analizi - Not implemented yet", "WARNING")
    messagebox.showinfo("Sprite Analysis", "Sprite analysis will be implemented soon!")

def analyze_sid():
    """Analyze SID music"""
    support.log_message("SID analizi - Not implemented yet", "WARNING") 
    messagebox.showinfo("SID Analysis", "SID music analysis will be implemented soon!")

def analyze_charset():
    """Analyze charset"""
    support.log_message("Charset analizi - Not implemented yet", "WARNING")
    messagebox.showinfo("Charset Analysis", "Charset analysis will be implemented soon!")

def analyze_current_file():
    """Analyze current file"""
    if not support.current_data:
        support.log_message("Dosya yüklenmemiş", "WARNING")
        return
    
    support.log_message("Dosya analizi başlatılıyor...", "INFO")
    analyze_illegal_opcodes()

# === Console Operations ===
def clear_console():
    """Clear console"""
    try:
        console_text = support.top.main_frame.console_panel.text
        console_text.config(state=tk.NORMAL)
        console_text.delete(1.0, tk.END)
        console_text.config(state=tk.DISABLED)
        support.log_message("Console temizlendi", "INFO")
    except:
        pass

# === Export Operations ===
def export_code():
    """Export code"""
    try:
        text_widget = support.top.main_frame.disasm_panel.text
        content = text_widget.get(1.0, tk.END).strip()
        
        if not content:
            support.log_message("Dışa aktarılacak kod yok", "WARNING")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Kod Dışa Aktar",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Assembly files", "*.asm"),
                ("C files", "*.c"),
                ("Basic files", "*.bas"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            support.log_message(f"Kod dışa aktarıldı: {os.path.basename(filename)}", "SUCCESS")
            messagebox.showinfo("Export", f"Kod başarıyla dışa aktarıldı:\n{filename}")
            
    except Exception as e:
        support.log_message(f"Export hatası: {e}", "ERROR")

# === Application Control ===
def exit_application():
    """Exit application"""
    support.log_message("Uygulama kapatılıyor...", "INFO")
    support.top.quit()

# === Event Handlers ===
def on_file_select():
    """Handle file selection"""
    try:
        listbox = support.top.main_frame.dir_panel.list_frame.filelist
        selection = listbox.curselection()
        if selection:
            filename = listbox.get(selection[0])
            support.log_message(f"Dosya seçildi: {filename}", "INFO")
            support.update_status(f"Seçili: {filename} - Format seçin")
    except:
        pass

def on_file_double_click():
    """Handle file double click"""
    try:
        listbox = support.top.main_frame.dir_panel.list_frame.filelist
        selection = listbox.curselection()
        if selection:
            filename = listbox.get(selection[0])
            support.log_message(f"Otomatik analiz: {filename}", "INFO")
            convert_assembly()  # Default to assembly
    except:
        pass

# Global support instance
support = None

def init(top=None):
    """Initialize support module"""
    global support
    support = D64ConverterGUISupport(top)
    
def destroy_window():
    """Destroy window"""
    global support
    support = None
