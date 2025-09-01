#!/usr/bin/env python3
"""
D64 Converter - Comprehensive Logging System
Tüm modüllerde kullanıcı etkileşimleri, hatalar, uyarılar, bilgiler loglanır

🎯 ÖZELLİKLER:
- Kullanıcı tıklamaları (button, menu, checkbox vb.)
- Hata mesajları (exception, error, warning)
- Dosya işlemleri (open, save, delete)
- Format dönüşümleri (assembly, basic, c vb.)
- GUI etkileşimleri (window open/close, tab change)
- Performance metrikleri (time, memory)
"""

import logging
import logging.handlers
import datetime
import os
import sys
import threading
import traceback
import functools
from pathlib import Path
from typing import Any, Dict, Optional
import json

class ComprehensiveLogger:
    """Kapsamlı logging sistemi - her şeyi loglar"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.logs_dir = self.base_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Thread-safe logging
        self.lock = threading.Lock()
        
        # Session bilgileri
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.user_actions = []
        
        # Setup loggers
        self._setup_loggers()
        
        print(f"📝 Comprehensive Logger başlatıldı")
        print(f"📁 Log klasörü: {self.logs_dir}")
        print(f"🆔 Session ID: {self.session_id}")
    
    def _setup_loggers(self):
        """Farklı tip loglar için logger'ları kur"""
        
        # Ana application logger
        self.app_logger = self._create_logger(
            name="d64_app",
            filename=f"d64_app_{self.session_id}.log",
            level=logging.DEBUG
        )
        
        # GUI events logger
        self.gui_logger = self._create_logger(
            name="d64_gui",
            filename=f"d64_gui_{self.session_id}.log", 
            level=logging.DEBUG
        )
        
        # Error logger (sadece hatalar)
        self.error_logger = self._create_logger(
            name="d64_errors",
            filename=f"d64_errors_{self.session_id}.log",
            level=logging.ERROR
        )
        
        # User actions logger
        self.action_logger = self._create_logger(
            name="d64_actions",
            filename=f"d64_actions_{self.session_id}.log",
            level=logging.INFO
        )
        
        # Performance logger
        self.perf_logger = self._create_logger(
            name="d64_performance",
            filename=f"d64_performance_{self.session_id}.log",
            level=logging.INFO
        )
    
    def _create_logger(self, name: str, filename: str, level: int):
        """Specific logger oluştur"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Önceki handler'ları temizle
        logger.handlers.clear()
        
        # File handler
        file_handler = logging.handlers.RotatingFileHandler(
            self.logs_dir / filename,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Thread-safe yapı
        logger.propagate = False
        
        return logger
    
    # ==========================================
    # KULLANICI ETKİLEŞİMLERİ
    # ==========================================
    
    def log_user_action(self, action_type: str, component: str, details: Dict[str, Any] = None):
        """Kullanıcı etkileşimini logla"""
        with self.lock:
            action_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'action_type': action_type,  # click, select, open, close, etc.
                'component': component,      # button_name, menu_item, etc.
                'details': details or {},
                'thread': threading.current_thread().name
            }
            
            self.user_actions.append(action_data)
            
            # Log mesajı
            msg = f"USER_ACTION | {action_type} | {component}"
            if details:
                msg += f" | {json.dumps(details, ensure_ascii=False)}"
            
            self.action_logger.info(msg)
            print(f"👆 {msg}")
    
    def log_button_click(self, button_name: str, button_text: str = None, **kwargs):
        """Button click logla"""
        details = {'button_text': button_text, **kwargs}
        self.log_user_action('BUTTON_CLICK', button_name, details)
    
    def log_menu_select(self, menu_path: str, **kwargs):
        """Menu seçimi logla"""
        self.log_user_action('MENU_SELECT', menu_path, kwargs)
    
    def log_file_operation(self, operation: str, file_path: str, **kwargs):
        """Dosya işlemi logla"""
        details = {'file_path': file_path, **kwargs}
        self.log_user_action('FILE_OPERATION', operation, details)
    
    def log_format_conversion(self, source_format: str, target_format: str, **kwargs):
        """Format dönüşümü logla"""
        details = {'source_format': source_format, 'target_format': target_format, **kwargs}
        self.log_user_action('FORMAT_CONVERSION', 'converter', details)
    
    # ==========================================
    # HATALAR VE UYARILAR
    # ==========================================
    
    def log_error(self, error_msg: str, exception: Exception = None, context: str = None):
        """Hata logla - hem console hem file"""
        with self.lock:
            # Stack trace al
            stack_trace = traceback.format_exc() if exception else None
            
            # Detaylı hata mesajı
            full_msg = f"ERROR | {context or 'Unknown'} | {error_msg}"
            if exception:
                full_msg += f" | Exception: {str(exception)}"
            if stack_trace:
                full_msg += f"\nStack Trace:\n{stack_trace}"
            
            # Log'a yaz
            self.error_logger.error(full_msg)
            self.app_logger.error(full_msg)
            
            # Console'a yazdır (renkli)
            print(f"🔴 HATA: {error_msg}")
            if exception:
                print(f"    ↳ Exception: {str(exception)}")
            if context:
                print(f"    ↳ Context: {context}")
    
    def log_warning(self, warning_msg: str, context: str = None):
        """Uyarı logla"""
        with self.lock:
            full_msg = f"WARNING | {context or 'Unknown'} | {warning_msg}"
            
            self.app_logger.warning(full_msg)
            print(f"⚠️ UYARI: {warning_msg}")
            if context:
                print(f"    ↳ Context: {context}")
    
    def log_info(self, info_msg: str, context: str = None):
        """Bilgi logla"""
        with self.lock:
            full_msg = f"INFO | {context or 'Unknown'} | {info_msg}"
            
            self.app_logger.info(full_msg)
            print(f"ℹ️ BİLGİ: {info_msg}")
    
    # ==========================================
    # GUI ETKİLEŞİMLERİ
    # ==========================================
    
    def log_gui_event(self, event_type: str, widget_info: str, **kwargs):
        """GUI eventi logla"""
        details = kwargs
        full_msg = f"GUI_EVENT | {event_type} | {widget_info}"
        if details:
            full_msg += f" | {json.dumps(details, ensure_ascii=False)}"
        
        self.gui_logger.info(full_msg)
        print(f"🖱️ GUI: {event_type} - {widget_info}")
    
    def log_window_operation(self, operation: str, window_name: str, **kwargs):
        """Window işlemi logla"""
        self.log_gui_event('WINDOW_OPERATION', f"{operation}:{window_name}", **kwargs)
    
    def log_tab_change(self, old_tab: str, new_tab: str, **kwargs):
        """Tab değişimi logla"""
        details = {'old_tab': old_tab, 'new_tab': new_tab, **kwargs}
        self.log_gui_event('TAB_CHANGE', 'notebook', details)
    
    # ==========================================
    # PERFORMANCE TRACKING
    # ==========================================
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """Performance metriği logla"""
        details = {'duration_ms': round(duration * 1000, 2), **kwargs}
        full_msg = f"PERFORMANCE | {operation} | {duration:.3f}s"
        if kwargs:
            full_msg += f" | {json.dumps(details, ensure_ascii=False)}"
        
        self.perf_logger.info(full_msg)
        
        # Yavaş işlemler için uyarı
        if duration > 2.0:  # 2 saniyeden uzun
            print(f"🐌 YAVAS: {operation} {duration:.2f}s sürdü")
    
    # ==========================================
    # DECORATOR FUNCTIONS
    # ==========================================
    
    def log_function_call(self, func_name: str = None):
        """Fonksiyon çağrılarını loglamak için decorator"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                name = func_name or f"{func.__module__}.{func.__name__}"
                
                start_time = datetime.datetime.now()
                self.log_info(f"Function BAŞLADI: {name}", "FUNCTION_CALL")
                
                try:
                    result = func(*args, **kwargs)
                    
                    duration = (datetime.datetime.now() - start_time).total_seconds()
                    self.log_performance(f"Function {name}", duration)
                    
                    return result
                    
                except Exception as e:
                    self.log_error(f"Function HATA: {name}", e, "FUNCTION_CALL")
                    raise
                    
            return wrapper
        return decorator
    
    def log_gui_callback(self, callback_name: str = None):
        """GUI callback'lerini loglamak için decorator"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                name = callback_name or f"GUI_CALLBACK:{func.__name__}"
                
                self.log_gui_event("CALLBACK_START", name)
                
                try:
                    result = func(*args, **kwargs)
                    self.log_gui_event("CALLBACK_SUCCESS", name)
                    return result
                    
                except Exception as e:
                    self.log_error(f"GUI Callback HATA: {name}", e, "GUI_CALLBACK")
                    raise
                    
            return wrapper
        return decorator
    
    # ==========================================
    # SESSION MANAGEMENT
    # ==========================================
    
    def get_session_summary(self):
        """Session özeti döndür"""
        return {
            'session_id': self.session_id,
            'total_actions': len(self.user_actions),
            'logs_directory': str(self.logs_dir),
            'recent_actions': self.user_actions[-10:] if self.user_actions else []
        }
    
    def save_session_summary(self):
        """Session özetini dosyaya kaydet"""
        summary_file = self.logs_dir / f"session_summary_{self.session_id}.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.get_session_summary(), f, indent=2, ensure_ascii=False)
        
        print(f"📊 Session özeti kaydedildi: {summary_file}")
    
    def cleanup(self):
        """Logger'ı temizle"""
        self.save_session_summary()
        
        # Tüm handler'ları kapat
        for logger in [self.app_logger, self.gui_logger, self.error_logger, 
                      self.action_logger, self.perf_logger]:
            for handler in logger.handlers:
                handler.close()

# ==========================================
# GLOBAL LOGGER INSTANCE
# ==========================================

# Global logger instance
_global_logger = None

def get_logger():
    """Global logger instance döndür"""
    global _global_logger
    if _global_logger is None:
        _global_logger = ComprehensiveLogger()
    return _global_logger

def init_logger(base_dir: str = None):
    """Logger'ı başlat"""
    global _global_logger
    _global_logger = ComprehensiveLogger(base_dir)
    return _global_logger

# Convenience functions
def log_user_action(action_type: str, component: str, details: Dict[str, Any] = None):
    """Kullanıcı etkileşimi logla"""
    get_logger().log_user_action(action_type, component, details)

def log_button_click(button_name: str, button_text: str = None, **kwargs):
    """Button click logla"""
    get_logger().log_button_click(button_name, button_text, **kwargs)

def log_error(error_msg: str, exception: Exception = None, context: str = None):
    """Hata logla"""
    get_logger().log_error(error_msg, exception, context)

def log_warning(warning_msg: str, context: str = None):
    """Uyarı logla"""
    get_logger().log_warning(warning_msg, context)

def log_info(info_msg: str, context: str = None):
    """Bilgi logla"""
    get_logger().log_info(info_msg, context)

def log_gui_event(event_type: str, widget_info: str, **kwargs):
    """GUI eventi logla"""
    get_logger().log_gui_event(event_type, widget_info, **kwargs)

def log_performance(operation: str, duration: float, **kwargs):
    """Performance logla"""
    get_logger().log_performance(operation, duration, **kwargs)

# ==========================================
# AUTO CLEANUP
# ==========================================

import atexit

def _cleanup_logger():
    """Program çıkışında logger'ı temizle"""
    global _global_logger
    if _global_logger:
        _global_logger.cleanup()

atexit.register(_cleanup_logger)

if __name__ == "__main__":
    # Test logging system
    logger = init_logger()
    
    # Test various log types
    log_info("Logger test başladı", "TEST")
    log_button_click("test_button", "Test Button")
    log_warning("Bu bir test uyarısıdır", "TEST")
    log_error("Bu bir test hatasıdır", context="TEST")
    log_performance("test_operation", 1.5)
    
    print("\n📝 Test tamamlandı. Log dosyalarını kontrol edin.")
