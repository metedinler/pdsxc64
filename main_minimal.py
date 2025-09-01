#!/usr/bin/env python3
"""
D64 Converter v5.0 - MINIMAL MAIN ENTRY POINT
Optimized Memory Management & Virtual Environment Integration
"""

import os
import sys
import gc
import weakref
from pathlib import Path

# VIRTUAL ENVIRONMENT AUTO-ACTIVATION
def ensure_venv_environment():
    """Virtual environment otomatik aktivasyonu - venv_asmto"""
    venv_path = Path(__file__).parent / "venv_asmto"
    
    if venv_path.exists():
        # Windows için Python executable path
        venv_python = venv_path / "Scripts" / "python.exe"
        
        if venv_python.exists() and str(venv_python) != sys.executable:
            print(f"🔄 Virtual environment otomatik aktivasyonu: {venv_path}")
            
            # Yeniden başlat venv ile
            import subprocess
            args = [str(venv_python)] + sys.argv
            subprocess.run(args)
            sys.exit(0)
        else:
            print(f"✅ Virtual environment aktif: {venv_path}")
    else:
        print(f"⚠️ Virtual environment bulunamadı: {venv_path}")
        # Virtual environment oluştur
        create_virtual_environment()

def create_virtual_environment():
    """Virtual environment oluştur"""
    import venv
    import subprocess
    
    venv_path = "venv_asmto"
    print(f"📦 Virtual environment oluşturuluyor: {venv_path}")
    
    try:
        venv.create(venv_path, with_pip=True)
        
        # Gerekli kütüphaneleri yükle
        pip_path = Path(venv_path) / "Scripts" / "pip.exe"
        packages = ["tkinterdnd2", "py65", "pillow", "numpy"]
        
        for package in packages:
            print(f"📦 Installing: {package}")
            subprocess.run([str(pip_path), "install", package], check=True)
            
        print(f"✅ Virtual environment hazır: {venv_path}")
        
    except Exception as e:
        print(f"❌ Virtual environment hatası: {e}")

# MEMORY OPTIMIZATION
class MemoryManager:
    """RAM optimizasyonu ve garbage collection"""
    
    def __init__(self):
        self.modules_registry = weakref.WeakSet()
        
    def register_module(self, module):
        """Modül kaydı"""
        self.modules_registry.add(module)
    
    def cleanup_unused_modules(self):
        """Kullanılmayan modülleri temizle"""
        gc.collect()
        
        # sys.modules'dan kullanılmayan modülleri kaldır
        unused_modules = []
        for module_name in list(sys.modules.keys()):
            if module_name.startswith(('test_', '__pycache__')):
                unused_modules.append(module_name)
        
        for module_name in unused_modules:
            if module_name in sys.modules:
                del sys.modules[module_name]
                
        gc.collect()
        print(f"🧹 Cleaned {len(unused_modules)} unused modules")
    
    def get_memory_usage(self):
        """Memory kullanımını göster"""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        return memory_info.rss / 1024 / 1024  # MB

# MINIMAL LAUNCHER
class MinimalLauncher:
    """Minimal launcher - sadece gerekli modülleri yükler"""
    
    def __init__(self):
        self.memory_manager = MemoryManager()
        
    def launch_configuration_manager(self):
        """Configuration Manager başlat"""
        try:
            print("🔧 Configuration Manager yükleniyor...")
            from configuration_manager import ConfigurationManager
            
            config_manager = ConfigurationManager()
            self.memory_manager.register_module(config_manager)
            
            config_manager.run()
            
        except ImportError as e:
            print(f"❌ Configuration Manager yüklenemedi: {e}")
            self.launch_gui_fallback()
        
    def launch_gui_fallback(self):
        """GUI fallback - Configuration Manager başarısız olursa"""
        try:
            print("🎨 GUI Manager yükleniyor...")
            from gui_manager import D64ConverterGUI
            import tkinter as tk
            
            root = tk.Tk()
            app = D64ConverterGUI(root)
            self.memory_manager.register_module(app)
            
            root.mainloop()
            
        except Exception as e:
            print(f"❌ GUI başlatma hatası: {e}")
    
    def cleanup_and_exit(self):
        """Temizlik ve çıkış"""
        print("🧹 Memory cleanup...")
        self.memory_manager.cleanup_unused_modules()
        sys.exit(0)

def main():
    """Minimal main entry point"""
    try:
        # Virtual environment kontrolü
        ensure_venv_environment()
        
        # Launcher başlat
        launcher = MinimalLauncher()
        
        # Argüman kontrolü
        if len(sys.argv) > 1:
            if "--gui" in sys.argv:
                launcher.launch_gui_fallback()
            elif "--config" in sys.argv:
                launcher.launch_configuration_manager()
            else:
                launcher.launch_configuration_manager()  # Default
        else:
            launcher.launch_configuration_manager()  # Default
            
    except KeyboardInterrupt:
        print("\n👋 Program sonlandırıldı")
        launcher.cleanup_and_exit()
    except Exception as e:
        print(f"❌ Program hatası: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
