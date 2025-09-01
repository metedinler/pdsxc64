"""
GUI Test - Disassembler Selection
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    # Import our main app
    from d64_converter import D64ConverterApp
    
    print("✅ d64_converter import başarılı")
    
    # Create test window
    root = tk.Tk()
    root.title("D64 Converter - GUI Test")
    
    # Create app instance
    app = D64ConverterApp(root)
    
    print("✅ GUI app oluşturuldu")
    print(f"📝 Disassembler seçimi: {app.disassembler_var.get()}")
    print(f"🔬 Illegal opcodes: {app.use_illegal_opcodes.get()}")
    print(f"🧠 Memory analysis: {app.memory_analysis.get()}")
    print(f"💾 Save intermediate: {app.save_intermediate.get()}")
    print(f"📁 Auto format dirs: {app.auto_format_dirs.get()}")
    print(f"📋 Recent files count: {len(app.recent_files)}")
    
    # Test GUI elements
    if hasattr(app, 'disassembler_var'):
        print("✅ Disassembler selection variable OK")
    if hasattr(app, 'recent_combo'):
        print("✅ Recent files combobox OK")
    else:
        print("⚠️ Recent files combobox missing")
        
    print("\n🚀 GUI test tamamlandı - GUI başlatılabilir")
    
    # Don't actually start GUI, just test creation
    root.destroy()
    
except Exception as e:
    print(f"❌ GUI test hatası: {e}")
    import traceback
    traceback.print_exc()
