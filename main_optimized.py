#!/usr/bin/env python3
"""
D64 Converter v5.0 - ULTRA OPTIMIZED MAIN
✨ Virtual Environment Auto-Activation
🧹 Memory Management & Garbage Collection
📦 Modular Component Loading
"""

import os
import sys
from pathlib import Path

def check_and_activate_venv():
    """Virtual environment auto-activation - venv_asmto"""
    venv_path = Path(__file__).parent / "venv_asmto"
    
    if venv_path.exists():
        venv_python = venv_path / "Scripts" / "python.exe"
        
        if venv_python.exists() and str(venv_python) != sys.executable:
            print(f"🔄 Activating virtual environment: {venv_path}")
            
            import subprocess
            args = [str(venv_python)] + sys.argv
            subprocess.run(args)
            sys.exit(0)
        else:
            print(f"✅ Virtual environment active: {venv_path}")
            return True
    else:
        print(f"⚠️ Virtual environment not found: {venv_path}")
        create_venv_if_needed()
        return False

def create_venv_if_needed():
    """Create virtual environment if needed"""
    import venv
    import subprocess
    
    venv_path = "venv_asmto"
    print(f"📦 Creating virtual environment: {venv_path}")
    
    try:
        venv.create(venv_path, with_pip=True)
        
        # Install required packages
        pip_path = Path(venv_path) / "Scripts" / "pip.exe"
        packages = ["tkinterdnd2", "py65", "pillow", "numpy", "psutil"]
        
        for package in packages:
            print(f"📦 Installing: {package}")
            subprocess.run([str(pip_path), "install", package], check=True)
            
        print(f"✅ Virtual environment ready: {venv_path}")
        
        # Restart with venv
        venv_python = Path(venv_path) / "Scripts" / "python.exe"
        args = [str(venv_python)] + sys.argv
        subprocess.run(args)
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Virtual environment creation failed: {e}")

def launch_application():
    """Launch main application with memory optimization"""
    try:
        # Memory optimization başlat
        from memory_manager import memory_optimizer, register_module
        memory_optimizer.start_auto_cleanup(interval=300)  # 5 dakikada bir
        
        # Configuration Manager başlat (default)
        print("🔧 Starting Configuration Manager...")
        
        try:
            from configuration_manager import ConfigurationManager
            config_manager = ConfigurationManager()
            register_module(config_manager, "ConfigurationManager")
            
            # GUI Debug mode check
            if os.environ.get('GUI_DEBUG_MODE', '').lower() == 'true':
                print("🍎 GUI Debug Mode enabled via environment")
                if hasattr(config_manager, 'enable_gui_debug'):
                    config_manager.enable_gui_debug()
            
            config_manager.run()
            
        except ImportError as e:
            print(f"⚠️ Configuration Manager not available: {e}")
            print("🎨 Falling back to GUI Manager...")
            launch_gui_fallback()
            
    except Exception as e:
        print(f"❌ Application launch error: {e}")
        sys.exit(1)

def launch_gui_fallback():
    """GUI fallback if Configuration Manager fails"""
    try:
        from memory_manager import register_module
        from gui_manager import D64ConverterGUI
        import tkinter as tk
        
        print("🎨 Starting GUI Manager...")
        
        root = tk.Tk()
        app = D64ConverterGUI(root)
        register_module(app, "D64ConverterGUI")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ GUI fallback failed: {e}")
        sys.exit(1)

def main():
    """Ultra optimized main entry point"""
    try:
        print("🚀 D64 Converter v5.0 - Ultra Optimized")
        print("=" * 50)
        
        # 1. Virtual Environment Check
        if not check_and_activate_venv():
            return  # Will restart with venv
        
        # 2. Launch Application
        launch_application()
        
    except KeyboardInterrupt:
        print("\n👋 Program terminated by user")
        
        # Cleanup before exit
        try:
            from memory_manager import memory_optimizer
            memory_optimizer.stop_auto_cleanup()
            memory_optimizer.deep_cleanup()
        except:
            pass
            
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
