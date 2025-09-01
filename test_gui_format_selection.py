#!/usr/bin/env python3
"""GUI Format Selection Test"""

import tkinter as tk
from tkinter import ttk

def test_format_selection():
    """Format seçim listesi test"""
    root = tk.Tk()
    root.title("Format Selection Test")
    root.geometry("400x300")
    
    # Assembly formatları listesi
    assembly_formats = {
        'tass': 'TASS - Turbo Assembler',
        'kickass': 'KickAssembler', 
        'dasm': 'DASM',
        'acme': 'ACME Assembler',
        'ca65': 'CA65 (cc65 Suite)',
        'css64': 'CSS64',
        'supermon': 'SuperMon',
        'native': 'Native 6502',
        'annotated': 'Annotated (Enhanced)',
        'structured': 'Structured (Control Flow)',
        'memory_mapped': 'Memory-Mapped',
        'debug_trace': 'Debug/Trace'
    }
    
    # Format seçimi
    tk.Label(root, text="🎯 Output Format:", font=("Arial", 10, "bold")).pack(pady=5)
    
    selected_format = tk.StringVar(value='DASM')
    format_combo = ttk.Combobox(root, textvariable=selected_format,
                               values=list(assembly_formats.values()),
                               state="readonly", width=30)
    format_combo.pack(pady=5)
    
    # Checkbox'lar
    tk.Label(root, text="⚙️ Options:", font=("Arial", 10, "bold")).pack(pady=5)
    
    use_illegal_opcodes = tk.BooleanVar(value=False)
    illegal_check = tk.Checkbutton(root, text="Use Illegal Opcodes", 
                                 variable=use_illegal_opcodes)
    illegal_check.pack(pady=2)
    
    enhanced_analysis = tk.BooleanVar(value=True)
    enhanced_check = tk.Checkbutton(root, text="Enhanced Analysis", 
                                  variable=enhanced_analysis)
    enhanced_check.pack(pady=2)
    
    # Test button
    def test_selection():
        selected_text = selected_format.get()
        # Format text'inden key'i bul
        format_key = 'dasm'  # default
        for key, value in assembly_formats.items():
            if value == selected_text:
                format_key = key
                break
        
        result = f"Selected Format: {format_key}\n"
        result += f"Illegal Opcodes: {use_illegal_opcodes.get()}\n"
        result += f"Enhanced Analysis: {enhanced_analysis.get()}"
        
        tk.messagebox.showinfo("Selection", result)
    
    tk.Button(root, text="Test Selection", command=test_selection).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_format_selection()
