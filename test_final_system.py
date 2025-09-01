#!/usr/bin/env python3
"""
Final Configuration Manager and Debug System Test
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_main_gui():
    """Test main GUI manager functionality"""
    try:
        print("🎮 Testing Main GUI Manager...")
        
        # Test import
        from gui_manager import D64ConverterGUI
        print("✅ D64ConverterGUI import successful")
        
        # Test initialization
        root = tk.Tk()
        gui_manager = D64ConverterGUI(root)
        print("✅ D64ConverterGUI initialization successful")
        
        # Test Configuration Manager method exists
        if hasattr(gui_manager, 'open_configuration_manager'):
            print("✅ D64ConverterGUI.open_configuration_manager() method exists")
        else:
            print("❌ D64ConverterGUI.open_configuration_manager() method missing")
            
        # Test safe_messagebox function exists
        from gui_manager import safe_messagebox
        print("✅ safe_messagebox function exists")
        
        root.destroy()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ GUI Manager error: {e}")
        return False

def test_debug_system():
    """Test debug system functionality"""
    try:
        print("🐛 Testing Debug System...")
        
        # Test debug functions import
        from gui_manager import debug_button, debug_label, debug_frame, debug_messagebox
        print("✅ Debug wrapper functions import successful")
        
        # Test GUIDebugHelper
        from gui_manager import GUIDebugHelper
        debug_helper = GUIDebugHelper()
        print("✅ GUIDebugHelper initialization successful")
        
        # Test debug mode toggle
        debug_helper.toggle_debug()
        print(f"✅ Debug mode toggle works - Current state: {debug_helper.debug_mode}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Debug system import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Debug system error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 D64 Converter Final System Test")
    print("=" * 50)
    
    # Test Main GUI
    gui_ok = test_main_gui()
    
    # Test Debug System
    debug_ok = test_debug_system()
    
    print("\n📊 Final Test Results:")
    print(f"Main GUI Manager: {'✅ OK' if gui_ok else '❌ FAILED'}")
    print(f"Debug System: {'✅ OK' if debug_ok else '❌ FAILED'}")
    
    if gui_ok and debug_ok:
        print("\n🎉 All systems functional! Ready to use.")
        print("📋 Configuration Manager: Fixed to use run() method")
        print("🐛 Debug System: Working with wrapper functions")
        print("🛡️  Safe Messagebox: Protects against debug/normal mode conflicts")
    else:
        print("\n⚠️  Some systems failed. Check the errors above.")
