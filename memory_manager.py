#!/usr/bin/env python3
"""
Memory Management and Optimization
RAM usage optimization and garbage collection
"""

import gc
import sys
import weakref
import threading
import time
from typing import Set, Dict, Any

class MemoryOptimizer:
    """Advanced memory optimization system"""
    
    def __init__(self):
        self.module_references: Set = weakref.WeakSet()
        self.gui_components: Dict[str, Any] = weakref.WeakValueDictionary()
        self.cleanup_thread = None
        self.auto_cleanup = True
        
    def register_module(self, module_obj, name: str = None):
        """Modül kaydı"""
        try:
            self.module_references.add(module_obj)
            if name:
                print(f"📦 Module registered: {name}")
        except Exception as e:
            print(f"⚠️ Module registration failed: {e}")
    
    def register_gui_component(self, component, name: str):
        """GUI component kaydı"""
        try:
            self.gui_components[name] = component
        except Exception as e:
            print(f"⚠️ GUI component registration failed: {e}")
    
    def cleanup_unused_modules(self) -> int:
        """Kullanılmayan modülleri temizle"""
        initial_count = len(sys.modules)
        
        # Test ve geçici modülleri temizle
        modules_to_remove = []
        for module_name in list(sys.modules.keys()):
            if any(prefix in module_name for prefix in [
                'test_', '__pycache__', '.test', '_test', 
                'pytest', 'unittest', 'doctest'
            ]):
                modules_to_remove.append(module_name)
        
        # Güvenli şekilde kaldır
        removed_count = 0
        for module_name in modules_to_remove:
            try:
                if module_name in sys.modules:
                    del sys.modules[module_name]
                    removed_count += 1
            except Exception as e:
                print(f"⚠️ Could not remove module {module_name}: {e}")
        
        # Garbage collection
        collected = gc.collect()
        
        print(f"🧹 Removed {removed_count} modules, collected {collected} objects")
        return removed_count
    
    def deep_cleanup(self):
        """Derin temizlik"""
        print("🧹 Deep memory cleanup starting...")
        
        # 1. Module cleanup
        removed_modules = self.cleanup_unused_modules()
        
        # 2. Force garbage collection
        for i in range(3):
            collected = gc.collect()
            print(f"🧹 GC round {i+1}: collected {collected} objects")
        
        # 3. GUI components cleanup
        expired_components = []
        for name, component in list(self.gui_components.items()):
            try:
                # Test if component is still alive
                if hasattr(component, 'winfo_exists'):
                    if not component.winfo_exists():
                        expired_components.append(name)
            except:
                expired_components.append(name)
        
        for name in expired_components:
            try:
                del self.gui_components[name]
            except:
                pass
        
        print(f"🧹 Deep cleanup completed: {removed_modules} modules, {len(expired_components)} GUI components")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Memory istatistikleri"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            stats = {
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'percent': process.memory_percent(),
                'modules_count': len(sys.modules),
                'registered_modules': len(self.module_references),
                'gui_components': len(self.gui_components),
                'gc_objects': len(gc.get_objects())
            }
            
            return stats
            
        except ImportError:
            return {
                'modules_count': len(sys.modules),
                'registered_modules': len(self.module_references),
                'gui_components': len(self.gui_components),
                'gc_objects': len(gc.get_objects())
            }
    
    def print_memory_stats(self):
        """Memory istatistiklerini yazdır"""
        stats = self.get_memory_stats()
        
        print("📊 MEMORY STATISTICS:")
        print("=" * 40)
        
        if 'rss_mb' in stats:
            print(f"RSS Memory: {stats['rss_mb']:.1f} MB")
            print(f"VMS Memory: {stats['vms_mb']:.1f} MB")
            print(f"Memory %: {stats['percent']:.1f}%")
        
        print(f"Modules: {stats['modules_count']}")
        print(f"Registered: {stats['registered_modules']}")
        print(f"GUI Components: {stats['gui_components']}")
        print(f"GC Objects: {stats['gc_objects']}")
        print("=" * 40)
    
    def start_auto_cleanup(self, interval: int = 300):
        """Otomatik temizlik başlat (5 dakikada bir)"""
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            return
        
        def cleanup_loop():
            while self.auto_cleanup:
                time.sleep(interval)
                if self.auto_cleanup:
                    self.cleanup_unused_modules()
        
        self.cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        print(f"🧹 Auto-cleanup started (every {interval}s)")
    
    def stop_auto_cleanup(self):
        """Otomatik temizliği durdur"""
        self.auto_cleanup = False
        print("🧹 Auto-cleanup stopped")

# Global memory optimizer
memory_optimizer = MemoryOptimizer()

def cleanup_memory():
    """Quick memory cleanup function"""
    return memory_optimizer.cleanup_unused_modules()

def deep_cleanup():
    """Deep memory cleanup function"""
    memory_optimizer.deep_cleanup()

def print_memory_stats():
    """Print memory statistics"""
    memory_optimizer.print_memory_stats()

def register_module(module_obj, name: str = None):
    """Register module for memory tracking"""
    memory_optimizer.register_module(module_obj, name)
