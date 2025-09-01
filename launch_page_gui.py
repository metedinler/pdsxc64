#!/usr/bin/env python3
"""
PAGE Launcher for D64 Converter GUI
Bu dosyayı PAGE ile açarak visual editing yapabilirsiniz.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our GUI
from d64_converter_gui_page import D64ConverterPageGUI

def launch_page_gui():
    """Launch the PAGE-compatible GUI"""
    import tkinter as tk
    
    print("🚀 Starting D64 Converter PAGE Edition...")
    print("📐 PAGE Visual Designer Compatible")
    print("🎯 4-Panel Layout: Directory | Disassembly | Console | Decompiler")
    
    root = tk.Tk()
    app = D64ConverterPageGUI(root)
    
    # Add sample data for testing
    app.log_message("PAGE Edition GUI initialized", "SUCCESS")
    app.log_message("To edit this GUI: Open d64_converter_gui_page.py in PAGE", "INFO")
    app.log_message("Ready for C64 file conversion and analysis", "INFO")
    
    app.run()

if __name__ == "__main__":
    launch_page_gui()
