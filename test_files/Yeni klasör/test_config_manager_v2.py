#!/usr/bin/env python3
"""
Test Configuration Manager functionality with run() method
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
        
        # Test run method exists
        if hasattr(config_manager, 'run'):
            print("✅ ConfigurationManager.run() method exists")
        else:
            print("❌ ConfigurationManager.run() method missing")
            
        # Test create_configuration_gui method exists
        if hasattr(config_manager, 'create_configuration_gui'):
            print("✅ ConfigurationManager.create_configuration_gui() method exists")
        else:
            print("❌ ConfigurationManager.create_configuration_gui() method missing")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 D64 Converter Configuration Manager Test v2")
    print("=" * 50)
    
    # Test Configuration Manager
    config_ok = test_config_manager()
    
    print("\n📊 Test Results:")
    print(f"Configuration Manager: {'✅ OK' if config_ok else '❌ FAILED'}")
    
    if config_ok:
        print("\n🎉 Configuration Manager should work with run() method!")
    else:
        print("\n⚠️  Configuration Manager test failed.")
