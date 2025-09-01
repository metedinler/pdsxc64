#!/usr/bin/env python3
"""
D64 Converter GUI Demo
Minimal GUI launcher with error handling

This demo safely launches the GUI with fallback options
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def launch_gui():
    """Launch main GUI safely with enhanced error reporting"""
    try:
        print("🚀 Launching D64 Converter GUI...")
        print("📋 Attempting to import GUI manager...")
        
        # Import GUI manager
        from gui_manager import D64ConverterGUI
        print("✅ GUI manager imported successfully")
        
        print("🎨 Creating GUI application...")
        app = D64ConverterGUI()
        print("✅ GUI application created successfully")
        
        print("🚀 Starting GUI main loop...")
        app.run()
        print("✅ GUI completed successfully")
        
    except ImportError as e:
        # Import error - show detailed information
        error_msg = f"❌ Could not import GUI components: {e}"
        print(error_msg)
        
        # Terminal'de göster
        print("\n🔧 IMPORT ERROR DETAILS:")
        print(f"   Error: {e}")
        print(f"   Module: gui_manager")
        
        # Check file existence
        import os
        if os.path.exists("gui_manager.py"):
            print("   ✅ gui_manager.py file exists")
        else:
            print("   ❌ gui_manager.py file missing!")
        
        # Import traceback
        import traceback
        print(f"\nFull traceback:\n{traceback.format_exc()}")
        
        # Fallback message
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Import Error", 
                           f"Could not import GUI components:\n{e}\n\n"
                           "Please ensure all dependencies are installed.\n\n"
                           f"Full error: {traceback.format_exc()}")
        root.destroy()
        
    except Exception as e:
        # General error handling with detailed output
        error_msg = f"❌ GUI initialization failed: {e}"
        print(error_msg)
        
        # Terminal'de detaylı hata
        print("\n🔧 GUI INITIALIZATION ERROR:")
        print(f"   Error: {e}")
        print(f"   Type: {type(e).__name__}")
        
        # Full traceback
        import traceback
        full_traceback = traceback.format_exc()
        print(f"\nFull traceback:\n{full_traceback}")
        
        # System info
        import sys
        import os
        print(f"\nSystem Information:")
        print(f"   Python version: {sys.version}")
        print(f"   Working directory: {os.getcwd()}")
        
        # Check tkinter
        try:
            import tkinter as tk_test
            print(f"   ✅ Tkinter available")
        except ImportError:
            print(f"   ❌ Tkinter not available!")
        
        # Fallback message dialog
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("GUI Error", 
                               f"GUI initialization failed:\n{e}\n\n"
                               "Check console for detailed error messages.\n\n"
                               f"Error type: {type(e).__name__}")
            root.destroy()
        except:
            # If even messagebox fails
            print("❌ Could not show error dialog - tkinter completely unavailable")

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    launch_gui()
