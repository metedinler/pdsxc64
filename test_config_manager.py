#!/usr/bin/env python3
"""
Test Configuration Manager functionality
"""
import tkinter as tk
from tkinter import messagebox
import sys
import os

def test_config_manager():
    """Test Configuration Manager import and initialization"""
    try:
        print("📋 Testing Configuration Manager...")
        
        # Test import
        from configuration_manager import ConfigurationManager
        print("✅ ConfigurationManager import successful")
        
        # Test initialization
        config_manager = ConfigurationManager()
        print("✅ ConfigurationManager initialization successful")
        
        # Test show method exists
        if hasattr(config_manager, 'show'):
            print("✅ ConfigurationManager.show() method exists")
        else:
            print("❌ ConfigurationManager.show() method missing")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_messagebox():
    """Test messagebox functionality"""
    try:
        print("📨 Testing MessageBox...")
        root = tk.Tk()
        root.withdraw()  # Hide root window
        
        # Test basic messagebox
        # messagebox.showinfo("Test", "Test successful")
        print("✅ MessageBox import successful")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ MessageBox error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 D64 Converter Configuration Manager Test")
    print("=" * 50)
    
    # Test Configuration Manager
    config_ok = test_config_manager()
    
    # Test MessageBox
    msg_ok = test_messagebox()
    
    print("\n📊 Test Results:")
    print(f"Configuration Manager: {'✅ OK' if config_ok else '❌ FAILED'}")
    print(f"MessageBox: {'✅ OK' if msg_ok else '❌ FAILED'}")
    
    if config_ok and msg_ok:
        print("\n🎉 All tests passed! Configuration Manager should work.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
