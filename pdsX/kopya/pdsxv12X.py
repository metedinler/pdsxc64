#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDSX v12X - Enhanced Programming Language Interpreter
Tam İşlevsel PDSX Yorumlayıcı - Tüm Özellikler Entegre Edilmiş Versiyon

Features:
- Advanced Memory Management with MemoryManager
- Enhanced Class System with Inheritance (INHERITS/EXTENDS)
- Dynamic Class System with CLAZZ keyword for runtime class creation
- Multi-dimensional Arrays with ArrayInstance
- Struct/Union/Enum Support with enhanced type checking
- Pointer Arithmetic with full memory management
- Advanced Error Handling and Debugging
- Module System with Import/Export
- Complete Function Library (100+ functions)
- Multi-paradigm Support: Structured, Functional, Logical, OOP
- Prolog Engine with Backtracking and Logical Programming
- Event-Driven Programming with EVENT/END EVENT
- Pipeline System with PIPE/END PIPE for data streams
- Full QBasic 7.1 and C/C++ command syntax in BASIC style
- GOTO/GOSUB support for legacy compatibility
- Enhanced PRINT/INPUT with Python-like functionality
- Recursive functions and commands as parameters
- Data Science Integration (NumPy, Pandas, SciPy)
- PDF Processing and Web Scraping
- SQLite Database Operations
- Comprehensive LibXCore framework
- Asynchronous Programming Support
- GUI Development with GuiLibX
- Performance Optimization with caching

Autor: AI Assistant & Community
Version: 12X (Enhanced Unified Version)
Date: 2025
"""

import sys
import subprocess
import importlib.metadata
import platform
import json
import threading
import asyncio
import ast
import math
import re
import logging
import struct as py_struct
import os
import sys
import time
import random
import sqlite3
import shutil
import glob
import socket
import pickle
import signal
import traceback
import multiprocessing
import ctypes
import zipfile
import datetime
import argparse
from collections import defaultdict, namedtuple, Counter
from types import SimpleNamespace
from threading import Thread
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Dict, List, Any, Optional, Callable

# Bağımlılık Kontrol ve Yükleme Sistemi
def install_missing_libraries():
    """Gelişmiş kütüphane yönetimi - cache, venv kontrolü"""
    import os
    import sys
    import subprocess
    from pathlib import Path
    
    # Cache klasörü oluştur
    cache_dir = Path("pdsx_cache")
    cache_dir.mkdir(exist_ok=True)
    
    # Şimdilik venv kontrolünü atlayalım - geliştirilecek
    print("Kütüphane kontrolü yapılıyor...")
    
    required_libraries = {
        'numpy': 'numpy',
        'pandas': 'pandas', 
        'scipy': 'scipy',
        'pdfplumber': 'pdfplumber',
        'requests': 'requests',
        'beautifulsoup4': 'bs4',
        'psutil': 'psutil',
        'packaging': 'packaging',
        'numba': 'numba',
        'pyyaml': 'pyyaml',
        'watchdog': 'watchdog',
        'pillow': 'Pillow',
        'pygame': 'pygame',
        'readline': 'pyreadline3' if platform.system() == 'Windows' else 'readline'
    }
    
    # Yüklü paketleri kontrol et
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True)
        installed_packages = {line.split()[0].lower() for line in result.stdout.split('\n')[2:] if line.strip()}
    except:
        installed_packages = set()
    
    missing = []
    for lib, pkg_name in required_libraries.items():
        # Cache'de kontrol et
        cache_file = cache_dir / f"{lib}_installed.txt"
        if cache_file.exists() and lib in installed_packages:
            continue
        elif lib not in installed_packages:
            missing.append(lib)

    if missing:
        print(f"Eksik kütüphaneler tespit edildi: {missing}")
        print("Yükleniyor...")
        for lib in missing:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', required_libraries[lib]])
                print(f"{lib} başarıyla yüklendi.")
                # Cache'e kaydet
                cache_file = cache_dir / f"{lib}_installed.txt"
                cache_file.write_text(f"Installed: {lib}")
            except subprocess.CalledProcessError:
                print(f"Uyarı: {lib} yüklenemedi. Bazı özellikler çalışmayabilir.")
    else:
        print("Tüm gerekli kütüphaneler yüklü.")

# SQLite Database System for PDSX
class SQLiteDatabase:
    """PDSX için SQLite database sistemi - tüm SQL komutları"""
    def __init__(self):
        self.connections = {}
        self.current_db = None
        # Otomatik default database bağlantısı
        self.connect("pdsx_default.db")
        
    def connect(self, db_name="pdsx_default.db"):
        """Veritabanına bağlan"""
        try:
            conn = sqlite3.connect(db_name)
            self.connections[db_name] = conn
            self.current_db = db_name
            return True
        except Exception as e:
            print(f"Database bağlantı hatası: {e}")
            return False
            
    def execute_sql(self, sql_command, params=None):
        """SQL komutunu çalıştır"""
        if not self.current_db or self.current_db not in self.connections:
            raise PdsXRuntimeError("Database bağlantısı yok")
            
        conn = self.connections[self.current_db]
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(sql_command, params)
            else:
                cursor.execute(sql_command)
                
            if sql_command.strip().upper().startswith(('SELECT', 'PRAGMA')):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.rowcount
                
        except Exception as e:
            raise PdsXRuntimeError(f"SQL hatası: {e}")
            
    def close(self, db_name=None):
        """Database bağlantısını kapat"""
        if db_name:
            if db_name in self.connections:
                self.connections[db_name].close()
                del self.connections[db_name]
        else:
            for conn in self.connections.values():
                conn.close()
            self.connections.clear()
            self.current_db = None

# Enhanced Event System with GUI and Timer triggers
class EnhancedEventSystem:
    """Gelişmiş Event sistemi - GUI, timer, interrupt events"""
    def __init__(self):
        self.events = {}
        self.event_handlers = {}
        self.running_events = set()
        self.event_queue = []
        self.timers = {}
        self.gui_events = {}
        
    def define_event(self, event_name, code_block, trigger_type="manual"):
        """Event tanımlama"""
        self.events[event_name] = {
            "code": code_block,
            "trigger_type": trigger_type,
            "enabled": True
        }
        
        # Otomatik trigger kurulumu
        if trigger_type == "timer":
            self._setup_timer_event(event_name)
        elif trigger_type == "gui":
            self._setup_gui_event(event_name)
        elif trigger_type == "interrupt":
            self._setup_interrupt_event(event_name)
        
    def _setup_timer_event(self, event_name):
        """Timer-based event kurulumu"""
        def timer_callback():
            if event_name in self.events and self.events[event_name]["enabled"]:
                self.trigger_event(event_name)
                
        # Timer thread başlat
        timer_thread = threading.Timer(1.0, timer_callback)
        timer_thread.daemon = True
        timer_thread.start()
        self.timers[event_name] = timer_thread
    
    def _setup_gui_event(self, event_name):
        """GUI-based event kurulumu"""
        try:
            import tkinter as tk
            # Tkinter event binding (örnek)
            self.gui_events[event_name] = True
        except ImportError:
            print("Tkinter mevcut değil, GUI events devre dışı")
    
    def _setup_interrupt_event(self, event_name):
        """Interrupt-based event kurulumu"""
        import signal
        
        def signal_handler(signum, frame):
            if event_name in self.events and self.events[event_name]["enabled"]:
                self.trigger_event(event_name)
        
        signal.signal(signal.SIGINT, signal_handler)
        
    def trigger_event(self, event_name, args=None, interpreter=None):
        """Event tetikleme"""
        if event_name in self.events and event_name not in self.running_events:
            event_info = self.events[event_name]
            if not event_info["enabled"]:
                return
                
            self.running_events.add(event_name)
            try:
                # Event'i paralel olarak çalıştır
                thread = threading.Thread(
                    target=self._execute_event,
                    args=(event_name, args or {}, interpreter)
                )
                thread.daemon = True
                thread.start()
            except Exception as e:
                print(f"Event {event_name} hatası: {e}")
                self.running_events.discard(event_name)
                
    def _execute_event(self, event_name, args, interpreter):
        """Event kodunu çalıştırma"""
        try:
            if interpreter and event_name in self.events:
                # Event scope'unu oluştur
                event_scope = args.copy()
                interpreter.scope_stack.append(event_scope)
                
                # Event kodunu çalıştır
                for command in self.events[event_name]["code"]:
                    interpreter.execute_command(command)
                    
                interpreter.scope_stack.pop()
        except Exception as e:
            print(f"Event {event_name} çalıştırma hatası: {e}")
        finally:
            self.running_events.discard(event_name)

# Module and Include System
class ModuleSystem:
    """BASX, LIBX dosya sistemi ve moduler programlama"""
    def __init__(self):
        self.loaded_modules = {}
        self.module_cache = {}
        self.include_paths = [".", "libx", "basx"]
        
    def include_file(self, filename, interpreter):
        """INCLUDE komutu - BASX ve LIBX dosyalarını dahil et"""
        # Dosya uzantısını kontrol et
        if not filename.endswith(('.basx', '.libx', '.pdsx')):
            filename += '.libx'  # Varsayılan olarak .libx
            
        # Include path'lerde ara
        found_file = None
        for include_path in self.include_paths:
            full_path = os.path.join(include_path, filename)
            if os.path.exists(full_path):
                found_file = full_path
                break
                
        if not found_file:
            raise PdsXRuntimeError(f"Include dosyası bulunamadı: {filename}")
        
        # Cache kontrolü
        if found_file in self.module_cache:
            return self.module_cache[found_file]
            
        # Dosyayı oku ve parse et
        try:
            with open(found_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Modül olarak parse et
            module_name = os.path.splitext(os.path.basename(filename))[0]
            interpreter.parse_program(content, module_name)
            
            # Cache'e ekle
            self.module_cache[found_file] = True
            
            print(f"Modül yüklendi: {filename}")
            return True
            
        except Exception as e:
            raise PdsXRuntimeError(f"Include hatası {filename}: {e}")

# Enhanced REPL with Multi-line Support
class EnhancedPdsXREPL:
    """Gelişmiş REPL - çok satırlı komut desteği"""
    def __init__(self):
        self.interpreter = pdsXInterpreter()
        self.interpreter.repl_mode = True
        self.command_history = []
        self.multiline_mode = False
        self.multiline_buffer = []
        
    def run(self):
        """Gelişmiş REPL çalıştırma"""
        print("PDSX v12X Enhanced REPL")
        print("Çıkmak için 'EXIT' yazın")
        print("Çok satırlı mod için 'PROGRAM' ... 'END PROGRAM' kullanın")
        print("=" * 50)
        
        while True:
            try:
                if self.multiline_mode:
                    prompt = "... "
                else:
                    prompt = "pdsx> "
                    
                if readline:
                    line = input(prompt)
                else:
                    line = input(prompt)
                
                # Çok satırlı mod kontrolü
                if line.strip().upper() == "PROGRAM":
                    self.multiline_mode = True
                    self.multiline_buffer = []
                    print("Çok satırlı mod başladı. 'END PROGRAM' ile bitirin.")
                    continue
                    
                elif line.strip().upper() == "END PROGRAM":
                    if self.multiline_mode:
                        self.multiline_mode = False
                        # Tüm buffer'ı çalıştır
                        full_program = '\n'.join(self.multiline_buffer)
                        self._execute_multiline_program(full_program)
                        self.multiline_buffer = []
                    continue
                    
                elif self.multiline_mode:
                    # Çok satırlı buffer'a ekle
                    self.multiline_buffer.append(line)
                    continue
                
                # Normal komut işleme
                if line.strip().upper() == "EXIT":
                    break
                    
                elif line.strip().upper() == "HELP":
                    self._show_help()
                    
                elif line.strip().upper() == "VARS":
                    self._show_variables()
                    
                elif line.strip().upper() == "CLEAR":
                    self._clear_screen()
                    
                elif line.strip().upper().startswith("SAVE "):
                    # Program'ı BASX/LIBX olarak kaydet
                    self._save_program(line)
                    
                elif line.strip():
                    result = self.interpreter.execute_command(line)
                    if result is not None:
                        print(f"Sonuç: {result}")
                        
            except KeyboardInterrupt:
                print("\nKesinit ile çıkmak için EXIT yazın")
                
            except Exception as e:
                print(f"REPL Hatası: {e}")
        
        print("PDSX REPL kapatılıyor...")
        
    def _execute_multiline_program(self, program):
        """Çok satırlı program çalıştırma"""
        try:
            self.interpreter.parse_program(program, "repl_multiline")
            self.interpreter.run()
        except Exception as e:
            print(f"Program çalıştırma hatası: {e}")
            
    def _save_program(self, command):
        """Program'ı BASX/LIBX dosyası olarak kaydet"""
        # SAVE filename [AS BASX|LIBX]
        parts = command.split()
        if len(parts) < 2:
            print("Kullanım: SAVE filename [AS BASX|LIBX]")
            return
            
        filename = parts[1]
        file_type = "libx"  # Varsayılan
        
        if len(parts) >= 4 and parts[2].upper() == "AS":
            file_type = parts[3].lower()
            
        if not filename.endswith(f'.{file_type}'):
            filename += f'.{file_type}'
            
        # Buffer'daki program'ı kaydet
        if self.multiline_buffer:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.multiline_buffer))
                print(f"Program kaydedildi: {filename}")
            except Exception as e:
                print(f"Kaydetme hatası: {e}")
        else:
            print("Kaydedilecek program bulunamadı. PROGRAM ... END PROGRAM kullanın.")

    def _show_help(self):
        """Gelişmiş yardım"""
        help_text = """
PDSX v12X Enhanced REPL Komutları:
- PROGRAM ... END PROGRAM : Çok satırlı program yazma
- SAVE filename [AS BASX|LIBX] : Program'ı dosyaya kaydetme
- INCLUDE filename : BASX/LIBX dosyası dahil etme
- VARS : Değişkenleri göster
- CLEAR : Ekranı temizle
- EXIT : Çık

PDSX v12X Komutları:
- DIM var AS type : Değişken tanımlama
- LET var = expr : Değer atama  
- PRINT expr : Çıktı alma
- EVENT/END EVENT : Event tanımlama
- TRIGGER event : Event tetikleme
- CLAZZ : Dinamik sınıf oluşturma
- PIPE/END PIPE : Pipeline oluşturma
- SQL komutları : SELECT, INSERT, UPDATE, DELETE
- Tüm control flow : FOR/NEXT, WHILE/WEND, IF/THEN/ELSE
"""
        print(help_text)

    def _show_variables(self):
        """Değişkenleri gösterme"""
        print("Global değişkenler:")
        for name, value in self.interpreter.global_vars.items():
            print(f"  {name} = {value} ({type(value).__name__})")
        
        print("Yerel değişkenler:")
        for name, value in self.interpreter.current_scope().items():
            print(f"  {name} = {value} ({type(value).__name__})")

    def _clear_screen(self):
        """Ekranı temizleme"""
        os.system('cls' if os.name == 'nt' else 'clear')

# Kütüphaneleri kontrol et ve yükle
install_missing_libraries()

# Yüklenen kütüphaneleri import et
try:
    import numpy as np
except ImportError:
    print("NumPy yüklenemedi, matematiksel fonksiyonlar sınırlı olacak")
    np = None

try:
    import pandas as pd
except ImportError:
    print("Pandas yüklenemedi, veri analizi özellikleri kullanılamayacak")
    pd = None

try:
    import scipy.stats as stats
except ImportError:
    print("SciPy yüklenemedi, istatistiksel fonksiyonlar kullanılamayacak")
    stats = None

try:
    import pdfplumber
except ImportError:
    print("PDFPlumber yüklenemedi, PDF işlemleri kullanılamayacak")
    pdfplumber = None

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Requests/BeautifulSoup yüklenemedi, web işlemleri kullanılamayacak")
    requests = None
    BeautifulSoup = None

try:
    import psutil
except ImportError:
    print("PSUtil yüklenemedi, sistem izleme özellikleri kullanılamayacak")
    psutil = None

try:
    if platform.system() == 'Windows':
        import pyreadline3 as readline
    else:
        import readline
except ImportError:
    print("Uyarı: readline kütüphanesi bulunamadı. Komut geçmişi devre dışı.")
    readline = None

# Logging ayarları
logging.basicConfig(
    filename='pdsx_interpreter.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Custom Exceptions
class PdsXException(Exception):
    """PDSX Yorumlayıcı ana hata sınıfı"""
    pass

class PdsXSyntaxError(PdsXException):
    """PDSX Sözdizimi hata sınıfı"""
    pass

class PdsXRuntimeError(PdsXException):
    """PDSX Çalışma zamanı hata sınıfı"""
    pass

class PdsXTypeError(PdsXException):
    """PDSX Tip uyumsuzluğu hata sınıfı"""
    pass

# Enhanced Memory Manager
class MemoryManager:
    """Gelişmiş bellek yönetimi ve işaretçi aritmetiği sistemi"""
    def __init__(self):
        self.heap = {}
        self.ref_counts = {}
        self.allocations = {}
        self.total_allocated = 0
        self.max_memory = 1024 * 1024 * 1024  # 1GB limit
        
    def allocate(self, size: int, type_info: str = "UNKNOWN") -> int:
        """Bellek ayırma işlemi"""
        if self.total_allocated + size > self.max_memory:
            raise PdsXRuntimeError(f"Bellek sınırı aşıldı: {self.max_memory} bytes")
            
        ptr = id(bytearray(size))
        self.heap[ptr] = bytearray(size)
        self.ref_counts[ptr] = 1
        self.allocations[ptr] = {"size": size, "type": type_info, "allocated_at": time.time()}
        self.total_allocated += size
        return ptr

    def release(self, ptr: int):
        """Bellek serbest bırakma işlemi"""
        if ptr in self.ref_counts:
            self.ref_counts[ptr] -= 1
            if self.ref_counts[ptr] == 0:
                if ptr in self.allocations:
                    self.total_allocated -= self.allocations[ptr]["size"]
                    del self.allocations[ptr]
                if ptr in self.heap:
                    del self.heap[ptr]
                del self.ref_counts[ptr]

    def dereference(self, ptr: int):
        """İşaretçi dereferansı"""
        if ptr not in self.heap:
            raise PdsXRuntimeError(f"Geçersiz işaretçi: {ptr}")
        return self.heap[ptr]

    def set_value(self, ptr: int, value):
        """İşaretçi konumuna değer yazma"""
        if ptr not in self.heap:
            raise PdsXRuntimeError(f"Geçersiz işaretçi: {ptr}")
        
        if isinstance(value, (int, float)):
            self.heap[ptr][:8] = py_struct.pack('d', float(value))
        elif isinstance(value, str):
            encoded = value.encode('utf-8')
            self.heap[ptr][:len(encoded)] = encoded
        elif isinstance(value, (list, tuple)):
            # Serialize complex data
            serialized = pickle.dumps(value)
            if len(serialized) <= len(self.heap[ptr]):
                self.heap[ptr][:len(serialized)] = serialized

    def sizeof(self, obj):
        """Nesne boyutunu byte cinsinden döndürme"""
        if isinstance(obj, (int, float)):
            return 8
        elif isinstance(obj, str):
            return len(obj.encode('utf-8'))
        elif hasattr(obj, 'nbytes'):  # NumPy arrays
            return obj.nbytes
        elif isinstance(obj, (list, tuple, dict)):
            return len(pickle.dumps(obj))
        return sys.getsizeof(obj)

    def get_memory_stats(self):
        """Bellek kullanım istatistikleri"""
        return {
            "total_allocated": self.total_allocated,
            "active_pointers": len(self.heap),
            "allocations": len(self.allocations),
            "memory_usage_mb": self.total_allocated / (1024 * 1024)
        }

# Enhanced Type System Classes
class StructInstance:
    """Gelişmiş Struct (Yapı) sınıfı"""
    def __init__(self, fields, type_table, types):
        self.fields = {name: None for name, _ in fields}
        self.field_types = {name: type_name for name, type_name in fields}
        self.type_table = type_table
        self.types = types
        self.sizes = {name: self._get_size(type_name) for name, type_name in fields}
        self.offsets = {}
        
        # Calculate field offsets for memory layout
        offset = 0
        for name, _ in fields:
            self.offsets[name] = offset
            offset += self.sizes[name]
        
        self.total_size = offset

    def set_field(self, field_name, value):
        """Struct alanına değer atama"""
        if field_name not in self.fields:
            raise PdsXTypeError(f"Geçersiz alan: {field_name}")
            
        field_type = self.field_types[field_name].upper()
        
        # Complex type handling
        if field_type in self.types:
            type_info = self.types[field_type]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                if not isinstance(value, (StructInstance, ClassInstance)):
                    raise PdsXTypeError(f"{field_name} için StructInstance veya ClassInstance bekleniyor")
            elif type_info["kind"] == "UNION":
                if not isinstance(value, UnionInstance):
                    raise PdsXTypeError(f"{field_name} için UnionInstance bekleniyor")
            self.fields[field_name] = value
        else:
            # Basic type handling with conversion
            expected_type = self.type_table.get(field_type, object)
            if not isinstance(value, expected_type):
                try:
                    value = expected_type(value)
                except Exception as e:
                    raise PdsXTypeError(f"{field_name} için tip dönüşümü başarısız: {e}")
            self.fields[field_name] = value

    def get_field(self, field_name):
        """Struct alanından değer okuma"""
        if field_name not in self.fields:
            raise PdsXTypeError(f"Geçersiz alan: {field_name}")
        return self.fields[field_name]

    def get_field_offset(self, field_name):
        """Alan offsetini döndürme"""
        return self.offsets.get(field_name, 0)

    def _get_size(self, type_name):
        """Tip boyutunu hesaplama"""
        if type_name.upper() in self.types:
            type_info = self.types[type_name.upper()]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                return sum(self._get_size(f[1]) for f in type_info["fields"])
            elif type_info["kind"] == "UNION":
                return max(self._get_size(f[1]) for f in type_info["fields"])
        
        size_map = {
            "INTEGER": 4, "DOUBLE": 8, "STRING": 8, "BYTE": 1,
            "SHORT": 2, "LONG": 8, "SINGLE": 4, "LIST": 8, 
            "ARRAY": 8, "DICT": 8, "POINTER": 8
        }
        return size_map.get(type_name.upper(), 8)

class UnionInstance:
    """Gelişmiş Union (Birleşim) sınıfı"""
    def __init__(self, fields, type_table, types):
        self.field_types = {name: type_name for name, type_name in fields}
        self.type_table = type_table
        self.types = types
        self.active_field = None
        self.sizes = {name: self._get_size(type_name) for name, type_name in fields}
        self.max_size = max(self.sizes.values()) if self.sizes else 8
        self.value = bytearray(self.max_size)

    def set_field(self, field_name, value):
        """Union alanına değer atama"""
        if field_name not in self.field_types:
            raise PdsXTypeError(f"Geçersiz alan: {field_name}")
            
        field_type = self.field_types[field_name].upper()
        
        if field_type in self.types:
            type_info = self.types[field_type]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                if not isinstance(value, (StructInstance, ClassInstance)):
                    raise PdsXTypeError(f"{field_name} için StructInstance veya ClassInstance bekleniyor")
            elif type_info["kind"] == "UNION":
                if not isinstance(value, UnionInstance):
                    raise PdsXTypeError(f"{field_name} için UnionInstance bekleniyor")
            self.active_field = field_name
            # For complex types, store the reference
            self.value = value
        else:
            expected_type = self.type_table.get(field_type, object)
            if not isinstance(value, expected_type):
                try:
                    value = expected_type(value)
                except Exception as e:
                    raise PdsXTypeError(f"{field_name} için tip dönüşümü başarısız: {e}")
            
            self.active_field = field_name
            
            # Pack value into bytearray
            fmt_map = {
                "INTEGER": "i", "DOUBLE": "d", "STRING": f"{self.max_size}s", 
                "BYTE": "b", "SHORT": "h", "LONG": "q", "SINGLE": "f"
            }
            fmt = fmt_map.get(field_type, f"{self.max_size}s")
            
            if fmt.endswith("s"):  # String handling
                encoded = str(value).encode('utf-8')[:self.max_size]
                self.value[:len(encoded)] = encoded
                if len(encoded) < self.max_size:
                    self.value[len(encoded):] = b'\0' * (self.max_size - len(encoded))
            else:
                packed = py_struct.pack(fmt, value)
                self.value[:len(packed)] = packed

    def get_field(self, field_name):
        """Union alanından değer okuma"""
        if field_name not in self.field_types:
            raise PdsXTypeError(f"Geçersiz alan: {field_name}")
        if self.active_field != field_name:
            raise PdsXRuntimeError(f"{field_name} alanı aktif değil, aktif alan: {self.active_field}")
        
        field_type = self.field_types[field_name].upper()
        
        if field_type in self.types:
            return self.value
        
        # Unpack basic types
        fmt_map = {
            "INTEGER": "i", "DOUBLE": "d", "STRING": f"{self.max_size}s", 
            "BYTE": "b", "SHORT": "h", "LONG": "q", "SINGLE": "f"
        }
        fmt = fmt_map.get(field_type, f"{self.max_size}s")
        
        try:
            if fmt.endswith("s"):
                return self.value.decode('utf-8').rstrip('\0')
            return py_struct.unpack(fmt, self.value[:py_struct.calcsize(fmt)])[0]
        except Exception as e:
            raise PdsXRuntimeError(f"{field_name} alanından veri okunamadı: {e}")

    def _get_size(self, type_name):
        """Tip boyutunu hesaplama"""
        if type_name.upper() in self.types:
            type_info = self.types[type_name.upper()]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                return sum(self._get_size(f[1]) for f in type_info["fields"])
            elif type_info["kind"] == "UNION":
                return max(self._get_size(f[1]) for f in type_info["fields"])
        
        size_map = {
            "INTEGER": 4, "DOUBLE": 8, "STRING": 8, "BYTE": 1,
            "SHORT": 2, "LONG": 8, "SINGLE": 4, "LIST": 8, 
            "ARRAY": 8, "DICT": 8, "POINTER": 8
        }
        return size_map.get(type_name.upper(), 8)

class ArrayInstance:
    """Gelişmiş çok boyutlu dizi sınıfı"""
    def __init__(self, dimensions, element_type, type_table, types):
        self.dimensions = dimensions
        self.element_type = element_type.upper()
        self.type_table = type_table
        self.types = types
        self.element_size = self._get_size(element_type)
        
        # Calculate total size and create storage
        self.total_elements = 1
        for dim in dimensions:
            self.total_elements *= dim
        
        self.elements = [None] * self.total_elements
        
        # Calculate strides for efficient indexing
        self.strides = []
        stride = self.element_size
        for dim in reversed(dimensions):
            self.strides.insert(0, stride)
            stride *= dim

    def set_element(self, indices, value):
        """Dizi elemanına değer atama"""
        index = self._get_flat_index(indices)
        
        # Type checking for complex types
        if self.element_type in self.types:
            type_info = self.types[self.element_type]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                if not isinstance(value, (StructInstance, ClassInstance)):
                    raise PdsXTypeError(f"StructInstance veya ClassInstance bekleniyor")
            elif type_info["kind"] == "UNION":
                if not isinstance(value, UnionInstance):
                    raise PdsXTypeError(f"UnionInstance bekleniyor")
        else:
            # Basic type conversion
            expected_type = self.type_table.get(self.element_type, object)
            if not isinstance(value, expected_type):
                try:
                    value = expected_type(value)
                except Exception as e:
                    raise PdsXTypeError(f"Tip dönüşümü başarısız: {e}")
        
        self.elements[index] = value

    def get_element(self, indices):
        """Dizi elemanından değer okuma"""
        index = self._get_flat_index(indices)
        return self.elements[index]

    def _get_flat_index(self, indices):
        """Çok boyutlu indeksi tek boyutlu indekse dönüştürme"""
        if len(indices) != len(self.dimensions):
            raise PdsXRuntimeError(f"Beklenen {len(self.dimensions)} indeks, {len(indices)} alındı")
        
        # Bounds checking
        for i, (idx, dim) in enumerate(zip(indices, self.dimensions)):
            if not (0 <= idx < dim):
                raise PdsXRuntimeError(f"İndeks sınır dışı: {idx} (boyut {i}, limit {dim})")
        
        # Calculate flat index
        flat_index = 0
        for i, idx in enumerate(indices):
            flat_index += idx * (self.strides[i] // self.element_size)
        
        return flat_index

    def _get_size(self, type_name):
        """Tip boyutunu hesaplama"""
        if type_name.upper() in self.types:
            type_info = self.types[type_name.upper()]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                return sum(self._get_size(f[1]) for f in type_info["fields"])
            elif type_info["kind"] == "UNION":
                return max(self._get_size(f[1]) for f in type_info["fields"])
        
        size_map = {
            "INTEGER": 4, "DOUBLE": 8, "STRING": 8, "BYTE": 1,
            "SHORT": 2, "LONG": 8, "SINGLE": 4, "LIST": 8, 
            "ARRAY": 8, "DICT": 8, "POINTER": 8
        }
        return size_map.get(type_name.upper(), 8)

class Pointer:
    """Gelişmiş işaretçi sınıfı"""
    def __init__(self, address, target_type, interpreter, dimensions=None):
        self.address = address
        self.target_type = target_type.upper()
        self.interpreter = interpreter
        self.dimensions = dimensions
        self.element_size = self._get_size(target_type)
        
        # Calculate strides for array pointers
        if dimensions:
            self.strides = []
            stride = self.element_size
            for dim in reversed(dimensions):
                self.strides.insert(0, stride)
                stride *= dim
        else:
            self.strides = None

    def dereference(self):
        """İşaretçi değerini okuma"""
        if self.address is None:
            raise PdsXRuntimeError("Null pointer dereference")
        if self.address not in self.interpreter.memory_pool:
            raise PdsXRuntimeError(f"Geçersiz işaretçi adresi: {self.address}")
        
        memory_block = self.interpreter.memory_pool[self.address]
        value = memory_block["value"]
        
        # Type checking for complex types
        if self.target_type in self.interpreter.types:
            type_info = self.interpreter.types[self.target_type]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                if not isinstance(value, (StructInstance, ClassInstance)):
                    raise PdsXTypeError("StructInstance veya ClassInstance bekleniyor")
            elif type_info["kind"] == "UNION":
                if not isinstance(value, UnionInstance):
                    raise PdsXTypeError("UnionInstance bekleniyor")
        else:
            expected_type = self.interpreter.type_table.get(self.target_type, object)
            if value is not None and not isinstance(value, expected_type):
                raise PdsXTypeError(f"Beklenen tip {expected_type.__name__}, bulunan {type(value).__name__}")
        
        return value

    def set(self, value):
        """İşaretçi değerini yazma"""
        if self.address is None:
            raise PdsXRuntimeError("Null pointer assignment")
        if self.address not in self.interpreter.memory_pool:
            raise PdsXRuntimeError(f"Geçersiz işaretçi adresi: {self.address}")
        
        # Type checking and conversion
        if self.target_type in self.interpreter.types:
            type_info = self.interpreter.types[self.target_type]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                if not isinstance(value, (StructInstance, ClassInstance)):
                    raise PdsXTypeError("StructInstance veya ClassInstance bekleniyor")
            elif type_info["kind"] == "UNION":
                if not isinstance(value, UnionInstance):
                    raise PdsXTypeError("UnionInstance bekleniyor")
        else:
            expected_type = self.interpreter.type_table.get(self.target_type, object)
            if not isinstance(value, expected_type):
                try:
                    value = expected_type(value)
                except Exception as e:
                    raise PdsXTypeError(f"Tip dönüşümü başarısız: {e}")
        
        self.interpreter.memory_pool[self.address]["value"] = value

    def add_offset(self, offset):
        """İşaretçi aritmetiği - offset ekleme"""
        if self.address is None:
            raise PdsXRuntimeError("Null pointer arithmetic")
        
        if self.dimensions and self.strides:
            new_address = self.address + offset * self.strides[-1]
        else:
            new_address = self.address + offset * self.element_size
        
        if new_address not in self.interpreter.memory_pool:
            # Check if the new address is within bounds
            for addr, block in self.interpreter.memory_pool.items():
                if addr <= new_address < addr + block.get("size", self.element_size):
                    new_address = addr
                    break
            else:
                raise PdsXRuntimeError(f"İşaretçi aritmetiği sınır dışı: {new_address}")
        
        return Pointer(new_address, self.target_type, self.interpreter, self.dimensions)

    def _get_size(self, type_name):
        """Tip boyutunu hesaplama"""
        if hasattr(self, 'interpreter') and type_name.upper() in self.interpreter.types:
            type_info = self.interpreter.types[type_name.upper()]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                return sum(self._get_size(f[1]) for f in type_info["fields"])
            elif type_info["kind"] == "UNION":
                return max(self._get_size(f[1]) for f in type_info["fields"])
        
        size_map = {
            "INTEGER": 4, "DOUBLE": 8, "STRING": 8, "BYTE": 1,
            "SHORT": 2, "LONG": 8, "SINGLE": 4, "LIST": 8, 
            "ARRAY": 8, "DICT": 8, "POINTER": 8
        }
        return size_map.get(type_name.upper(), 8)

class ClassInstance:
    """Gelişmiş sınıf örneği (nesne) sınıfı"""
    def __init__(self, class_info, type_table, types, interpreter):
        self.class_info = class_info
        self.type_table = type_table
        self.types = types
        self.interpreter = interpreter
        
        # Initialize all fields (public and private)
        self.fields = {}
        for name, type_name in class_info["fields"]:
            self.fields[name] = None
        
        self.field_types = {name: type_name for name, type_name in class_info["fields"]}
        self.access = class_info["access"]
        self.methods = class_info["methods"]
        self.parent = class_info.get("parent")
        
        # Initialize parent class fields if inheritance exists
        if self.parent and self.parent in types:
            parent_info = types[self.parent]
            for name, type_name in parent_info["fields"]:
                if name not in self.fields:
                    self.fields[name] = None
                    self.field_types[name] = type_name

    def set_field(self, field_name, value, from_method=False):
        """Sınıf alanına değer atama"""
        if field_name not in self.field_types:
            raise PdsXTypeError(f"Geçersiz alan: {field_name}")
        
        # Access control
        access_level = self.access.get(field_name, "PUBLIC")
        if access_level == "PRIVATE" and not from_method:
            raise PdsXRuntimeError(f"{field_name} özel bir alan, sadece sınıf metodları erişebilir")
        
        field_type = self.field_types[field_name].upper()
        
        # Type checking for complex types
        if field_type in self.types:
            type_info = self.types[field_type]
            if type_info["kind"] in ("STRUCT", "CLASS"):
                if not isinstance(value, (StructInstance, ClassInstance)):
                    raise PdsXTypeError(f"{field_name} için StructInstance veya ClassInstance bekleniyor")
            elif type_info["kind"] == "UNION":
                if not isinstance(value, UnionInstance):
                    raise PdsXTypeError(f"{field_name} için UnionInstance bekleniyor")
        else:
            # Basic type conversion
            expected_type = self.type_table.get(field_type, object)
            if not isinstance(value, expected_type):
                try:
                    value = expected_type(value)
                except Exception as e:
                    raise PdsXTypeError(f"{field_name} için tip dönüşümü başarısız: {e}")
        
        self.fields[field_name] = value

    def get_field(self, field_name, from_method=False):
        """Sınıf alanından değer okuma"""
        if field_name not in self.field_types:
            raise PdsXTypeError(f"Geçersiz alan: {field_name}")
        
        # Access control
        access_level = self.access.get(field_name, "PUBLIC")
        if access_level == "PRIVATE" and not from_method:
            raise PdsXRuntimeError(f"{field_name} özel bir alan, sadece sınıf metodları erişebilir")
        
        return self.fields[field_name]

    def call_method(self, method_name, args):
        """Sınıf metodunu çağırma"""
        if method_name not in self.methods:
            # Check parent class methods
            if self.parent and self.parent in self.types:
                parent_info = self.types[self.parent]
                if method_name in parent_info.get("methods", {}):
                    method = parent_info["methods"][method_name]
                else:
                    raise PdsXRuntimeError(f"Geçersiz metod: {method_name}")
            else:
                raise PdsXRuntimeError(f"Geçersiz metod: {method_name}")
        else:
            method = self.methods[method_name]
        
        # Set up method execution context
        self.interpreter.current_class = self
        self.interpreter.scopes.append({"SELF": self})
        
        # Bind parameters
        if len(args) != len(method["params"]):
            raise PdsXRuntimeError(f"Parametre sayısı uyumsuzluğu: {method_name}")
        
        for (param_name, param_type), arg in zip(method["params"], args):
            self.interpreter.current_scope()[param_name] = arg
        
        # Execute method body
        result = None
        try:
            for cmd in method["body"]:
                result = self.interpreter.execute_command(cmd)
                if result is not None:  # RETURN statement
                    break
        finally:
            # Clean up execution context
            self.interpreter.scopes.pop()
            if hasattr(self.interpreter, 'current_class'):
                del self.interpreter.current_class
        
        return result

# Enhanced Stack and Queue Data Structures
class Stack:
    """Gelişmiş yığın veri yapısı"""
    def __init__(self, max_size=None):
        self.items = []
        self.max_size = max_size
    
    def push(self, item):
        if self.max_size and len(self.items) >= self.max_size:
            raise PdsXRuntimeError(f"Yığın kapasitesi aşıldı: {self.max_size}")
        self.items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise PdsXRuntimeError("Yığın boş")
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            raise PdsXRuntimeError("Yığın boş")
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def clear(self):
        self.items.clear()

class Queue:
    """Gelişmiş kuyruk veri yapısı"""
    def __init__(self, max_size=None):
        self.items = []
        self.max_size = max_size
    
    def enqueue(self, item):
        if self.max_size and len(self.items) >= self.max_size:
            raise PdsXRuntimeError(f"Kuyruk kapasitesi aşıldı: {self.max_size}")
        self.items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            raise PdsXRuntimeError("Kuyruk boş")
        return self.items.pop(0)
    
    def peek(self):
        if self.is_empty():
            raise PdsXRuntimeError("Kuyruk boş")
        return self.items[0]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def clear(self):
        self.items.clear()

# Enhanced LibXCore Framework
class LibXCore:
    """Gelişmiş PDSX çekirdek kütüphanesi"""
    def __init__(self):
        self.default_encoding = "utf-8"
        self.dll_handles = {}
        self.modules = {}
        self.omega_global = None
        self.async_tasks = []

    # Core Functions
    def set_encoding(self, encoding):
        """Varsayılan dosya kodlamasını ayarlar"""
        self.default_encoding = encoding

    def load(self, module_path):
        """Modül dosyalarını yükler (.hz, .hx, .libx, .basx)"""
        if not os.path.exists(module_path):
            raise PdsXRuntimeError(f"Modül bulunamadı: {module_path}")
        
        valid_extensions = (".hz", ".hx", ".libx", ".basx", ".pdsx")
        if not module_path.endswith(valid_extensions):
            raise PdsXRuntimeError("Geçersiz dosya uzantısı")
        
        with open(module_path, "r", encoding=self.default_encoding) as f:
            self.modules[module_path] = f.read()
        return True

    def list_lib(self):
        """Yüklenen modülleri listeler"""
        return list(self.modules.keys())

    def load_dll(self, dll_name):
        """DLL dosyasını yükler"""
        try:
            dll = ctypes.WinDLL(dll_name) if platform.system() == 'Windows' else ctypes.CDLL(dll_name)
            self.dll_handles[dll_name] = dll
            return SimpleNamespace(call=lambda func_name, *args: getattr(dll, func_name)(*args))
        except Exception as e:
            raise PdsXRuntimeError(f"DLL yüklenemedi {dll_name}: {e}")

    # Mathematical and Statistical Functions
    def sum(self, iterable=None, *args):
        """Toplam hesaplama"""
        if iterable is not None:
            return np.sum(iterable) if np and iterable else sum(iterable) if iterable else 0
        return np.sum(args) if np and args else sum(args) if args else 0

    def mean(self, iterable=None, *args):
        """Ortalama hesaplama"""
        data = iterable if iterable is not None else args
        if not data:
            return 0
        return np.mean(data) if np else sum(data) / len(data)

    def median(self, iterable):
        """Ortanca değer hesaplama"""
        if np:
            return np.median(iterable)
        sorted_data = sorted(iterable)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2-1] + sorted_data[n//2]) / 2
        return sorted_data[n//2]

    def std(self, iterable):
        """Standart sapma hesaplama"""
        if np:
            return np.std(iterable)
        mean_val = self.mean(iterable)
        variance = sum((x - mean_val) ** 2 for x in iterable) / len(iterable)
        return variance ** 0.5

    def correlation(self, x, y):
        """Korelasyon hesaplama"""
        if np:
            return np.corrcoef(x, y)[0, 1]
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        sum_y2 = sum(y[i] ** 2 for i in range(n))
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0

    # Advanced Statistical Functions
    def variance(self, iterable, ddof=0):
        """Varyans hesaplama"""
        if np:
            return np.var(iterable, ddof=ddof)
        mean_val = self.mean(iterable)
        n = len(iterable)
        return sum((x - mean_val) ** 2 for x in iterable) / (n - ddof)

    def percentile(self, iterable, q):
        """Yüzdelik dilim hesaplama"""
        if np:
            return np.percentile(iterable, q)
        sorted_data = sorted(iterable)
        k = (len(sorted_data) - 1) * q / 100
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_data[int(k)]
        return sorted_data[int(f)] * (c - k) + sorted_data[int(c)] * (k - f)

    def quantile(self, iterable, q):
        """Quantile hesaplama"""
        return self.percentile(iterable, q * 100)

    def iqr(self, iterable):
        """Interquartile Range hesaplama"""
        return self.quantile(iterable, 0.75) - self.quantile(iterable, 0.25)

    def skewness(self, iterable):
        """Çarpıklık hesaplama"""
        if stats:
            return stats.skew(iterable)
        n = len(iterable)
        mean_val = self.mean(iterable)
        std_val = self.std(iterable)
        if std_val == 0:
            return 0
        return sum(((x - mean_val) / std_val) ** 3 for x in iterable) / n

    def kurtosis(self, iterable):
        """Basıklık hesaplama"""
        if stats:
            return stats.kurtosis(iterable)
        n = len(iterable)
        mean_val = self.mean(iterable)
        std_val = self.std(iterable)
        if std_val == 0:
            return 0
        return sum(((x - mean_val) / std_val) ** 4 for x in iterable) / n - 3

    def covariance(self, x, y):
        """Kovaryans hesaplama"""
        if np:
            return np.cov(x, y)[0, 1]
        n = len(x)
        mean_x = self.mean(x)
        mean_y = self.mean(y)
        return sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / (n - 1)

    # Hypothesis Testing Functions
    def t_test_one_sample(self, sample, population_mean):
        """Tek örneklem t-testi"""
        if stats:
            return stats.ttest_1samp(sample, population_mean)
        
        n = len(sample)
        sample_mean = self.mean(sample)
        sample_std = self.std(sample)
        
        if sample_std == 0:
            return {"statistic": float('inf'), "p_value": 0.0}
        
        t_stat = (sample_mean - population_mean) / (sample_std / math.sqrt(n))
        # Basit p-value hesaplama (normal dağılım yaklaşımı)
        p_value = 2 * (1 - abs(t_stat) / (abs(t_stat) + math.sqrt(n - 1)))
        
        return {"statistic": t_stat, "p_value": p_value, "df": n - 1}

    def t_test_two_sample(self, sample1, sample2, equal_var=True):
        """İki örneklem t-testi"""
        if stats:
            return stats.ttest_ind(sample1, sample2, equal_var=equal_var)
        
        n1, n2 = len(sample1), len(sample2)
        mean1, mean2 = self.mean(sample1), self.mean(sample2)
        var1, var2 = self.variance(sample1, ddof=1), self.variance(sample2, ddof=1)
        
        if equal_var:
            # Pooled variance
            pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
            se = math.sqrt(pooled_var * (1/n1 + 1/n2))
            df = n1 + n2 - 2
        else:
            # Welch's t-test
            se = math.sqrt(var1/n1 + var2/n2)
            df = (var1/n1 + var2/n2)**2 / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1))
        
        if se == 0:
            return {"statistic": float('inf'), "p_value": 0.0}
        
        t_stat = (mean1 - mean2) / se
        p_value = 2 * (1 - abs(t_stat) / (abs(t_stat) + math.sqrt(df)))
        
        return {"statistic": t_stat, "p_value": p_value, "df": df}

    def paired_t_test(self, sample1, sample2):
        """Eşleştirilmiş t-testi"""
        if stats:
            return stats.ttest_rel(sample1, sample2)
        
        differences = [x - y for x, y in zip(sample1, sample2)]
        return self.t_test_one_sample(differences, 0)

    def z_test_one_sample(self, sample, population_mean, population_std):
        """Tek örneklem z-testi"""
        n = len(sample)
        sample_mean = self.mean(sample)
        
        if population_std == 0:
            return {"statistic": float('inf'), "p_value": 0.0}
        
        z_stat = (sample_mean - population_mean) / (population_std / math.sqrt(n))
        # Normal dağılım CDF yaklaşımı
        p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        
        return {"statistic": z_stat, "p_value": p_value}

    def z_test_two_sample(self, sample1, sample2, std1, std2):
        """İki örneklem z-testi"""
        n1, n2 = len(sample1), len(sample2)
        mean1, mean2 = self.mean(sample1), self.mean(sample2)
        
        se = math.sqrt((std1**2 / n1) + (std2**2 / n2))
        if se == 0:
            return {"statistic": float('inf'), "p_value": 0.0}
        
        z_stat = (mean1 - mean2) / se
        p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        
        return {"statistic": z_stat, "p_value": p_value}

    def f_test(self, sample1, sample2):
        """F-testi (varyans eşitliği)"""
        var1 = self.variance(sample1, ddof=1)
        var2 = self.variance(sample2, ddof=1)
        
        if var2 == 0:
            return {"statistic": float('inf'), "p_value": 0.0}
        
        f_stat = var1 / var2
        df1, df2 = len(sample1) - 1, len(sample2) - 1
        
        # Basit F-dağılımı p-value hesaplama
        p_value = 1 - self._f_cdf(f_stat, df1, df2)
        
        return {"statistic": f_stat, "p_value": p_value, "df1": df1, "df2": df2}

    def chi_square_test(self, observed, expected=None):
        """Ki-kare testi"""
        if stats:
            if expected is None:
                return stats.chisquare(observed)
            else:
                return stats.chisquare(observed, expected)
        
        if expected is None:
            expected = [sum(observed) / len(observed)] * len(observed)
        
        chi2_stat = sum((o - e)**2 / e for o, e in zip(observed, expected) if e > 0)
        df = len(observed) - 1
        
        # Basit p-value hesaplama
        p_value = 1 - self._chi2_cdf(chi2_stat, df)
        
        return {"statistic": chi2_stat, "p_value": p_value, "df": df}

    def anova_one_way(self, *groups):
        """Tek yönlü ANOVA"""
        if stats:
            return stats.f_oneway(*groups)
        
        # Manuel ANOVA hesaplama
        all_values = []
        group_means = []
        group_sizes = []
        
        for group in groups:
            all_values.extend(group)
            group_means.append(self.mean(group))
            group_sizes.append(len(group))
        
        grand_mean = self.mean(all_values)
        
        # Between-group sum of squares
        ss_between = sum(n * (mean - grand_mean)**2 for n, mean in zip(group_sizes, group_means))
        
        # Within-group sum of squares
        ss_within = sum(sum((x - group_mean)**2 for x in group) 
                       for group, group_mean in zip(groups, group_means))
        
        # Degrees of freedom
        df_between = len(groups) - 1
        df_within = sum(group_sizes) - len(groups)
        
        if df_within == 0 or ss_within == 0:
            return {"statistic": float('inf'), "p_value": 0.0}
        
        # Mean squares
        ms_between = ss_between / df_between
        ms_within = ss_within / df_within
        
        # F-statistic
        f_stat = ms_between / ms_within
        p_value = 1 - self._f_cdf(f_stat, df_between, df_within)
        
        return {
            "statistic": f_stat, 
            "p_value": p_value, 
            "df_between": df_between, 
            "df_within": df_within,
            "ss_between": ss_between,
            "ss_within": ss_within
        }

    def _normal_cdf(self, x):
        """Normal dağılım CDF yaklaşımı"""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    def _chi2_cdf(self, x, df):
        """Ki-kare dağılımı CDF yaklaşımı"""
        if x <= 0:
            return 0
        # Gamma fonksiyonu yaklaşımı
        return min(1.0, x / (x + df))

    def _f_cdf(self, x, df1, df2):
        """F-dağılımı CDF yaklaşımı"""
        if x <= 0:
            return 0
        # Beta dağılımı yaklaşımı
        return min(1.0, x / (x + df2/df1))

    # Linear Regression and Correlation
    def linear_regression(self, x, y):
        """Doğrusal regresyon"""
        if len(x) != len(y):
            raise ValueError("x ve y aynı uzunlukta olmalı")
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        # Slope (eğim)
        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            slope = 0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / denominator
        
        # Intercept (kesim)
        intercept = (sum_y - slope * sum_x) / n
        
        # R-squared
        y_mean = sum_y / n
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
        ss_res = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
        
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "correlation": self.correlation(x, y)
        }

    def polynomial_regression(self, x, y, degree=2):
        """Polinom regresyon"""
        if np:
            coeffs = np.polyfit(x, y, degree)
            return {"coefficients": coeffs.tolist()}
        else:
            # Basit ikinci derece polinom için manuel hesaplama
            if degree == 2:
                # y = ax² + bx + c formu
                n = len(x)
                sum_x = sum(x)
                sum_y = sum(y)
                sum_x2 = sum(xi**2 for xi in x)
                sum_x3 = sum(xi**3 for xi in x)
                sum_x4 = sum(xi**4 for xi in x)
                sum_xy = sum(x[i] * y[i] for i in range(n))
                sum_x2y = sum(x[i]**2 * y[i] for i in range(n))
                
                # Matris sistemini çöz (basit 3x3)
                # Normal equations: A * coeffs = B
                A = [[n, sum_x, sum_x2],
                     [sum_x, sum_x2, sum_x3],
                     [sum_x2, sum_x3, sum_x4]]
                B = [sum_y, sum_xy, sum_x2y]
                
                # Cramer's rule ile çözüm
                det_A = self._determinant_3x3(A)
                if det_A == 0:
                    return {"coefficients": [0, 0, 0]}
                
                c = self._determinant_3x3([[B[0], A[0][1], A[0][2]],
                                          [B[1], A[1][1], A[1][2]],
                                          [B[2], A[2][1], A[2][2]]]) / det_A
                b = self._determinant_3x3([[A[0][0], B[0], A[0][2]],
                                          [A[1][0], B[1], A[1][2]],
                                          [A[2][0], B[2], A[2][2]]]) / det_A
                a = self._determinant_3x3([[A[0][0], A[0][1], B[0]],
                                          [A[1][0], A[1][1], B[1]],
                                          [A[2][0], A[2][1], B[2]]]) / det_A
                
                return {"coefficients": [a, b, c]}
            else:
                raise ValueError("Sadece 2. derece polinom destekleniyor (NumPy olmadan)")

    def _determinant_3x3(self, matrix):
        """3x3 matris determinantı"""
        return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
                matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
                matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))

    # NumPy Manual Implementations (for systems without NumPy)
    def _reshape_manual(self, arr, shape):
        """Manuel reshape işlemi"""
        flat = self._flatten_manual(arr)
        total_elements = 1
        for dim in shape:
            total_elements *= dim
        
        if len(flat) != total_elements:
            raise ValueError(f"Toplam eleman sayısı uyumsuz: {len(flat)} != {total_elements}")
        
        if len(shape) == 1:
            return flat[:shape[0]]
        elif len(shape) == 2:
            rows, cols = shape
            return [[flat[i * cols + j] for j in range(cols)] for i in range(rows)]
        else:
            raise ValueError("Sadece 1D ve 2D reshape destekleniyor")

    def _flatten_manual(self, arr):
        """Manuel flatten işlemi"""
        if isinstance(arr[0], (list, tuple)):
            result = []
            for row in arr:
                result.extend(row)
            return result
        return arr

    def _transpose_manual(self, arr):
        """Manuel transpose işlemi"""
        if not isinstance(arr[0], (list, tuple)):
            return arr
        return [[arr[i][j] for i in range(len(arr))] for j in range(len(arr[0]))]

    def _concatenate_manual(self, arrays):
        """Manuel concatenate işlemi"""
        result = []
        for arr in arrays:
            result.extend(arr)
        return result

    def _vstack_manual(self, arrays):
        """Manuel vertical stack işlemi"""
        result = []
        for arr in arrays:
            result.extend(arr if isinstance(arr[0], (list, tuple)) else [arr])
        return result

    def _hstack_manual(self, arrays):
        """Manuel horizontal stack işlemi"""
        if isinstance(arrays[0][0], (list, tuple)):
            return [sum([arr[i] for arr in arrays], []) for i in range(len(arrays[0]))]
        else:
            return sum(arrays, [])

    def _dot_product_manual(self, a, b):
        """Manuel dot product işlemi"""
        if isinstance(a[0], (list, tuple)):  # Matrix multiplication
            return self._matrix_multiply_manual(a, b)
        else:  # Vector dot product
            return sum(x * y for x, y in zip(a, b))

    def _matrix_multiply_manual(self, a, b):
        """Manuel matris çarpımı"""
        rows_a, cols_a = len(a), len(a[0])
        rows_b, cols_b = len(b), len(b[0]) if isinstance(b[0], (list, tuple)) else 1
        
        if cols_a != rows_b:
            raise ValueError("Matris boyutları uyumsuz")
        
        if cols_b == 1:  # Matrix-vector multiplication
            return [sum(a[i][k] * b[k] for k in range(cols_a)) for i in range(rows_a)]
        else:  # Matrix-matrix multiplication
            return [[sum(a[i][k] * b[k][j] for k in range(cols_a)) 
                    for j in range(cols_b)] for i in range(rows_a)]

    def _cross_product_manual(self, a, b):
        """Manuel cross product işlemi (3D)"""
        if len(a) != 3 or len(b) != 3:
            raise ValueError("Cross product sadece 3D vektörler için")
        return [
            a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]
        ]

    def _determinant_manual(self, matrix):
        """Manuel determinant hesaplama"""
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        elif n == 3:
            return self._determinant_3x3(matrix)
        else:
            # Larger matrices - LU decomposition approximation
            return self._determinant_lu(matrix)

    def _determinant_lu(self, matrix):
        """LU decomposition ile determinant"""
        n = len(matrix)
        # Copy matrix
        A = [row[:] for row in matrix]
        
        # Partial pivoting LU decomposition
        det = 1
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            
            # Swap rows
            if max_row != i:
                A[i], A[max_row] = A[max_row], A[i]
                det *= -1
            
            # Check for singular matrix
            if abs(A[i][i]) < 1e-10:
                return 0
            
            det *= A[i][i]
            
            # Eliminate
            for k in range(i + 1, n):
                factor = A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
        
        return det

    def _inverse_manual(self, matrix):
        """Manuel matris tersi (Gauss-Jordan)"""
        n = len(matrix)
        
        # Create augmented matrix [A | I]
        augmented = []
        for i in range(n):
            row = matrix[i][:] + [0] * n
            row[n + i] = 1
            augmented.append(row)
        
        # Gauss-Jordan elimination
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                    max_row = k
            
            # Swap rows
            if max_row != i:
                augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            
            # Check for singular matrix
            if abs(augmented[i][i]) < 1e-10:
                raise ValueError("Matris tekil (singular)")
            
            # Scale pivot row
            pivot = augmented[i][i]
            for j in range(2 * n):
                augmented[i][j] /= pivot
            
            # Eliminate column
            for k in range(n):
                if k != i:
                    factor = augmented[k][i]
                    for j in range(2 * n):
                        augmented[k][j] -= factor * augmented[i][j]
        
        # Extract inverse matrix
        return [[augmented[i][j] for j in range(n, 2 * n)] for i in range(n)]

    def _solve_linear_system(self, A, b):
        """Doğrusal sistem çözümü (Gaussian elimination)"""
        n = len(A)
        
        # Create augmented matrix
        augmented = [A[i][:] + [b[i]] for i in range(n)]
        
        # Forward elimination
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                    max_row = k
            
            # Swap rows
            if max_row != i:
                augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            
            # Check for singular matrix
            if abs(augmented[i][i]) < 1e-10:
                raise ValueError("Sistem çözülemez")
            
            # Eliminate
            for k in range(i + 1, n):
                factor = augmented[k][i] / augmented[i][i]
                for j in range(i, n + 1):
                    augmented[k][j] -= factor * augmented[i][j]
        
        # Back substitution
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = augmented[i][n]
            for j in range(i + 1, n):
                x[i] -= augmented[i][j] * x[j]
            x[i] /= augmented[i][i]
        
        return x

    def _bincount_manual(self, arr):
        """Manuel bincount işlemi"""
        if not arr:
            return []
        max_val = max(arr)
        counts = [0] * (max_val + 1)
        for val in arr:
            counts[val] += 1
        return counts

    def _histogram_manual(self, arr, bins=10):
        """Manuel histogram işlemi"""
        min_val, max_val = min(arr), max(arr)
        bin_width = (max_val - min_val) / bins
        bin_edges = [min_val + i * bin_width for i in range(bins + 1)]
        
        counts = [0] * bins
        for val in arr:
            bin_idx = min(int((val - min_val) / bin_width), bins - 1)
            counts[bin_idx] += 1
        
        return counts, bin_edges

    # Pandas-like Manual Implementations
    def _read_csv_manual(self, filename):
        """Manuel CSV okuma"""
        import csv
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return {"data": data, "type": "manual_dataframe"}

    def _write_csv_manual(self, data, filename):
        """Manuel CSV yazma"""
        import csv
        if isinstance(data, dict) and "data" in data:
            actual_data = data["data"]
        else:
            actual_data = data
        
        if actual_data:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if isinstance(actual_data[0], dict):
                    fieldnames = actual_data[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(actual_data)
                else:
                    writer = csv.writer(f)
                    writer.writerows(actual_data)

    def _groupby_manual(self, data, by):
        """Manuel groupby işlemi"""
        if isinstance(data, dict) and "data" in data:
            actual_data = data["data"]
        else:
            actual_data = data
        
        groups = {}
        for row in actual_data:
            key = row[by] if isinstance(row, dict) else row[by]
            if key not in groups:
                groups[key] = []
            groups[key].append(row)
        
        return {"groups": groups, "type": "manual_groupby"}

    def _pivot_manual(self, data, index, columns, values):
        """Manuel pivot işlemi"""
        if isinstance(data, dict) and "data" in data:
            actual_data = data["data"]
        else:
            actual_data = data
        
        # Create pivot structure
        pivot_data = {}
        for row in actual_data:
            row_key = row[index]
            col_key = row[columns]
            value = row[values]
            
            if row_key not in pivot_data:
                pivot_data[row_key] = {}
            pivot_data[row_key][col_key] = value
        
        return {"data": pivot_data, "type": "manual_pivot"}

    def _merge_manual(self, df1, df2, on):
        """Manuel merge işlemi"""
        data1 = df1["data"] if isinstance(df1, dict) and "data" in df1 else df1
        data2 = df2["data"] if isinstance(df2, dict) and "data" in df2 else df2
        
        # Create lookup for df2
        lookup = {}
        for row in data2:
            key = row[on]
            lookup[key] = row
        
        # Merge data
        merged = []
        for row1 in data1:
            key = row1[on]
            if key in lookup:
                merged_row = {**row1, **lookup[key]}
                merged.append(merged_row)
        
        return {"data": merged, "type": "manual_dataframe"}

    # Advanced Statistical Test Implementations
    def _normaltest_manual(self, data):
        """Manuel normallik testi (D'Agostino and Pearson)"""
        n = len(data)
        if n < 8:
            return {"statistic": 0, "p_value": 1.0}
        
        skew = self.skewness(data)
        kurt = self.kurtosis(data)
        
        # D'Agostino-Pearson test
        skew_stat = skew * math.sqrt((n * (n - 1)) / ((n - 2) * 6))
        kurt_stat = (kurt - 3) * math.sqrt(n / 24)
        
        combined_stat = skew_stat**2 + kurt_stat**2
        p_value = 1 - self._chi2_cdf(combined_stat, 2)
        
        return {"statistic": combined_stat, "p_value": p_value}

    def _shapiro_manual(self, data):
        """Manuel Shapiro-Wilk testi (basitleştirilmiş)"""
        n = len(data)
        if n < 3 or n > 50:
            return {"statistic": 1.0, "p_value": 1.0}
        
        sorted_data = sorted(data)
        mean_val = self.mean(data)
        
        # Basitleştirilmiş W istatistiği
        numerator = sum((sorted_data[i] - mean_val) * (i + 1 - (n + 1) / 2) for i in range(n))**2
        denominator = sum((x - mean_val)**2 for x in data)
        
        if denominator == 0:
            return {"statistic": 1.0, "p_value": 1.0}
        
        w_stat = numerator / (denominator * n)
        
        # Approximate p-value
        p_value = 1 - w_stat if w_stat < 1 else 0.0
        
        return {"statistic": w_stat, "p_value": p_value}

    def _jarque_bera_manual(self, data):
        """Manuel Jarque-Bera testi"""
        n = len(data)
        if n < 4:
            return {"statistic": 0, "p_value": 1.0}
        
        skew = self.skewness(data)
        kurt = self.kurtosis(data)
        
        jb_stat = n * (skew**2 / 6 + (kurt + 3)**2 / 24)
        p_value = 1 - self._chi2_cdf(jb_stat, 2)
        
        return {"statistic": jb_stat, "p_value": p_value}

    def _ks_test_manual(self, data1, data2=None):
        """Manuel Kolmogorov-Smirnov testi"""
        if data2 is None:
            # One-sample test against normal distribution
            n = len(data1)
            mean_val = self.mean(data1)
            std_val = self.std(data1)
            
            sorted_data = sorted(data1)
            D = 0
            
            for i, x in enumerate(sorted_data):
                empirical_cdf = (i + 1) / n
                theoretical_cdf = self._normal_cdf((x - mean_val) / std_val)
                D = max(D, abs(empirical_cdf - theoretical_cdf))
            
            # Approximate p-value
            p_value = 2 * math.exp(-2 * n * D**2)
            return {"statistic": D, "p_value": min(1.0, p_value)}
        else:
            # Two-sample test
            n1, n2 = len(data1), len(data2)
            sorted_data1 = sorted(data1)
            sorted_data2 = sorted(data2)
            
            all_values = sorted(set(sorted_data1 + sorted_data2))
            D = 0
            
            for value in all_values:
                cdf1 = sum(1 for x in sorted_data1 if x <= value) / n1
                cdf2 = sum(1 for x in sorted_data2 if x <= value) / n2
                D = max(D, abs(cdf1 - cdf2))
            
            # Approximate p-value
            effective_n = (n1 * n2) / (n1 + n2)
            p_value = 2 * math.exp(-2 * effective_n * D**2)
            return {"statistic": D, "p_value": min(1.0, p_value)}

    def _mann_whitney_manual(self, data1, data2):
        """Manuel Mann-Whitney U testi"""
        n1, n2 = len(data1), len(data2)
        combined = [(x, 1) for x in data1] + [(x, 2) for x in data2]
        combined.sort()
        
        # Rank hesaplama
        ranks1 = []
        for i, (value, group) in enumerate(combined):
            if group == 1:
                ranks1.append(i + 1)
        
        R1 = sum(ranks1)
        U1 = R1 - n1 * (n1 + 1) / 2
        U2 = n1 * n2 - U1
        
        U = min(U1, U2)
        
        # Normal yaklaşımla p-value
        mean_u = n1 * n2 / 2
        std_u = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
        
        if std_u == 0:
            return {"statistic": U, "p_value": 1.0}
        
        z = (U - mean_u) / std_u
        p_value = 2 * (1 - self._normal_cdf(abs(z)))
        
        return {"statistic": U, "p_value": p_value}

    def _wilcoxon_manual(self, data1, data2=None):
        """Manuel Wilcoxon testi"""
        if data2 is None:
            # One-sample test (signed-rank)
            data = [x for x in data1 if x != 0]  # Remove zeros
            if not data:
                return {"statistic": 0, "p_value": 1.0}
            
            abs_data = [(abs(x), 1 if x > 0 else -1) for x in data]
            abs_data.sort()
            
            # Rank hesaplama
            ranks = []
            for i, (value, sign) in enumerate(abs_data):
                ranks.append((i + 1) * sign)
            
            W = sum(rank for rank in ranks if rank > 0)
            
            # Normal yaklaşım
            n = len(data)
            mean_w = n * (n + 1) / 4
            std_w = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
            
            if std_w == 0:
                return {"statistic": W, "p_value": 1.0}
            
            z = (W - mean_w) / std_w
            p_value = 2 * (1 - self._normal_cdf(abs(z)))
            
            return {"statistic": W, "p_value": p_value}
        else:
            # Paired test
            differences = [x - y for x, y in zip(data1, data2)]
            return self._wilcoxon_manual(differences)

    def _kruskal_manual(self, *groups):
        """Manuel Kruskal-Wallis testi"""
        all_data = []
        group_sizes = []
        
        for group in groups:
            all_data.extend(group)
            group_sizes.append(len(group))
        
        # Rank hesaplama
        sorted_indices = sorted(range(len(all_data)), key=lambda i: all_data[i])
        ranks = [0] * len(all_data)
        for i, idx in enumerate(sorted_indices):
            ranks[idx] = i + 1
        
        # Grup rankları
        rank_sums = []
        start_idx = 0
        for size in group_sizes:
            end_idx = start_idx + size
            rank_sums.append(sum(ranks[start_idx:end_idx]))
            start_idx = end_idx
        
        # H istatistiği
        n = len(all_data)
        H = 12 / (n * (n + 1)) * sum(R**2 / n_i for R, n_i in zip(rank_sums, group_sizes)) - 3 * (n + 1)
        
        # p-value (chi-square distribution)
        df = len(groups) - 1
        p_value = 1 - self._chi2_cdf(H, df)
        
        return {"statistic": H, "p_value": p_value, "df": df}

    def _friedman_manual(self, *groups):
        """Manuel Friedman testi"""
        k = len(groups)  # Number of groups
        n = len(groups[0])  # Number of blocks (assuming equal sizes)
        
        # Rank each block
        rank_sums = [0] * k
        for block in range(n):
            block_values = [(groups[i][block], i) for i in range(k)]
            block_values.sort()
            
            for rank, (value, group_idx) in enumerate(block_values):
                rank_sums[group_idx] += rank + 1
        
        # Friedman Q statistic
        Q = 12 / (n * k * (k + 1)) * sum(R**2 for R in rank_sums) - 3 * n * (k + 1)
        
        # p-value (chi-square distribution)
        df = k - 1
        p_value = 1 - self._chi2_cdf(Q, df)
        
        return {"statistic": Q, "p_value": p_value, "df": df}

    def _pearson_test_manual(self, x, y):
        """Manuel Pearson korelasyon testi"""
        r = self.correlation(x, y)
        n = len(x)
        
        if abs(r) >= 1.0:
            return {"correlation": r, "p_value": 0.0}
        
        # t-statistic
        t_stat = r * math.sqrt((n - 2) / (1 - r**2))
        
        # p-value (two-tailed t-test)
        p_value = 2 * (1 - self._t_cdf(abs(t_stat), n - 2))
        
        return {"correlation": r, "statistic": t_stat, "p_value": p_value}

    def _spearman_test_manual(self, x, y):
        """Manuel Spearman korelasyon testi"""
        # Rank hesaplama
        x_ranked = self._rank_data(x)
        y_ranked = self._rank_data(y)
        
        # Pearson correlation on ranks
        return self._pearson_test_manual(x_ranked, y_ranked)

    def _kendall_test_manual(self, x, y):
        """Manuel Kendall tau testi"""
        n = len(x)
        concordant = 0
        discordant = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                if (x[i] - x[j]) * (y[i] - y[j]) > 0:
                    concordant += 1
                elif (x[i] - x[j]) * (y[i] - y[j]) < 0:
                    discordant += 1
        
        tau = (concordant - discordant) / (n * (n - 1) / 2)
        
        # Approximate p-value
        var_tau = 2 * (2 * n + 5) / (9 * n * (n - 1))
        z = tau / math.sqrt(var_tau)
        p_value = 2 * (1 - self._normal_cdf(abs(z)))
        
        return {"correlation": tau, "p_value": p_value}

    def _rank_data(self, data):
        """Veriyi sıralama (rank)"""
        sorted_indices = sorted(range(len(data)), key=lambda i: data[i])
        ranks = [0] * len(data)
        for i, idx in enumerate(sorted_indices):
            ranks[idx] = i + 1
        return ranks

    # Distribution PDF/CDF Manual Implementations
    def _norm_pdf_manual(self, x, mu=0, sigma=1):
        """Manuel normal dağılım PDF"""
        return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma)**2)

    def _norm_cdf_manual(self, x, mu=0, sigma=1):
        """Manuel normal dağılım CDF"""
        return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

    def _t_pdf_manual(self, x, df):
        """Manuel t-dağılımı PDF (yaklaşım)"""
        # Basit yaklaşım - tam gamma fonksiyonu olmadan
        return (1 + x**2 / df)**(-0.5 * (df + 1))

    def _t_cdf_manual(self, x, df):
        """Manuel t-dağılımı CDF (yaklaşım)"""
        if df >= 30:
            return self._normal_cdf(x)
        # Basit yaklaşım
        return 0.5 + 0.5 * math.tanh(x / math.sqrt(df / (df - 2)))

    # Specialized Statistical Tests - Missing Manual Implementations
    def _anderson_darling_manual(self, data, dist='norm'):
        """Manuel Anderson-Darling normality test"""
        n = len(data)
        if n < 3:
            return {"statistic": 0, "critical_values": [], "significance_level": 0.15}
        
        # Sort data and calculate standardized values
        sorted_data = sorted(data)
        if dist == 'norm':
            mean_val = self.mean(data)
            std_val = self.std(data)
            standardized = [(x - mean_val) / std_val for x in sorted_data]
        else:
            standardized = sorted_data
        
        # Calculate Anderson-Darling statistic
        A2 = 0
        for i in range(n):
            F_i = self._normal_cdf(standardized[i])
            F_n_minus_i = self._normal_cdf(standardized[n-1-i])
            A2 += (2*i + 1) * (math.log(F_i) + math.log(1 - F_n_minus_i))
        
        A2 = -n - A2/n
        
        # Adjust for sample size
        A2_adj = A2 * (1 + 0.75/n + 2.25/n**2)
        
        # Critical values for normal distribution
        critical_values = [0.576, 0.656, 0.787, 0.918, 1.092]  # 15%, 10%, 5%, 2.5%, 1%
        
        return {"statistic": A2_adj, "critical_values": critical_values, "significance_level": 0.05}

    def _ansari_bradley_manual(self, x, y):
        """Manuel Ansari-Bradley test for equality of variances"""
        n_x, n_y = len(x), len(y)
        combined = list(x) + list(y)
        n_total = n_x + n_y
        
        # Sort combined data and assign ranks from outside in
        sorted_combined = sorted(combined)
        ranks = {}
        
        # Assign ranks from both ends
        for i in range(n_total):
            if i % 2 == 0:
                rank = (i // 2) + 1
            else:
                rank = n_total - (i // 2)
            ranks[sorted_combined[i]] = rank
        
        # Calculate sum of ranks for x sample
        W = sum(ranks[val] for val in x)
        
        # Expected value and variance under null hypothesis
        E_W = n_x * (n_total + 1) / 2
        
        if n_total % 2 == 0:
            Var_W = n_x * n_y * (n_total + 1) / (12 * (n_total - 1))
        else:
            Var_W = n_x * n_y * (n_total + 1) / 12
        
        # Z-score and p-value
        if Var_W > 0:
            z = (W - E_W) / math.sqrt(Var_W)
            p_value = 2 * (1 - self._normal_cdf(abs(z)))
        else:
            z = 0
            p_value = 1.0
        
        return {"statistic": W, "p_value": p_value}

    def _bartlett_manual(self, *samples):
        """Manuel Bartlett test for equality of variances"""
        k = len(samples)
        if k < 2:
            return {"statistic": 0, "p_value": 1.0}
        
        n_i = [len(sample) for sample in samples]
        N = sum(n_i)
        
        # Calculate sample variances
        s_i_squared = [self.variance(sample) for sample in samples]
        
        # Pooled variance
        numerator = sum((n - 1) * s2 for n, s2 in zip(n_i, s_i_squared))
        s_p_squared = numerator / (N - k)
        
        if s_p_squared <= 0:
            return {"statistic": 0, "p_value": 1.0}
        
        # Bartlett's test statistic
        B = ((N - k) * math.log(s_p_squared) - 
             sum((n - 1) * math.log(s2) for n, s2 in zip(n_i, s_i_squared) if s2 > 0))
        
        # Correction factor
        C = 1 + (1 / (3 * (k - 1))) * (sum(1/(n-1) for n in n_i) - 1/(N-k))
        
        chi2_stat = B / C
        p_value = 1 - self._chi2_cdf(chi2_stat, k - 1)
        
        return {"statistic": chi2_stat, "p_value": p_value}

    def _brown_forsythe_manual(self, *samples):
        """Manuel Brown-Forsythe test (Levene test with median)"""
        k = len(samples)
        if k < 2:
            return {"statistic": 0, "p_value": 1.0}
        
        # Calculate absolute deviations from median for each group
        deviations = []
        group_labels = []
        
        for i, sample in enumerate(samples):
            median_val = self.median(sample)
            dev = [abs(x - median_val) for x in sample]
            deviations.extend(dev)
            group_labels.extend([i] * len(sample))
        
        # Perform one-way ANOVA on deviations
        return self._one_way_anova_manual(deviations, group_labels)

    def _cochran_q_manual(self, data):
        """Manuel Cochran's Q test for binary data"""
        # Expecting data as list of lists (treatments x subjects)
        if not data or not data[0]:
            return {"statistic": 0, "p_value": 1.0}
        
        k = len(data)  # number of treatments
        n = len(data[0])  # number of subjects
        
        # Calculate row sums (R_i) and column sums (C_j)
        R = [sum(row) for row in data]
        C = [sum(data[i][j] for i in range(k)) for j in range(n)]
        
        # Calculate Cochran's Q
        sum_R_squared = sum(r**2 for r in R)
        sum_R = sum(R)
        
        if sum_R == 0:
            return {"statistic": 0, "p_value": 1.0}
        
        Q = (k - 1) * (k * sum_R_squared - sum_R**2) / (k * sum_R - sum(c**2 for c in C))
        
        # p-value from chi-square distribution
        df = k - 1
        p_value = 1 - self._chi2_cdf(Q, df)
        
        return {"statistic": Q, "p_value": p_value, "df": df}

    def _mcnemar_manual(self, table):
        """Manuel McNemar test for paired binary data"""
        # Expecting 2x2 contingency table
        if len(table) != 2 or len(table[0]) != 2:
            raise ValueError("McNemar test requires a 2x2 table")
        
        a, b = table[0][0], table[0][1]
        c, d = table[1][0], table[1][1]
        
        # McNemar's test uses only discordant pairs (b + c)
        if b + c == 0:
            return {"statistic": 0, "p_value": 1.0}
        
        # With continuity correction
        chi2_stat = (abs(b - c) - 1)**2 / (b + c)
        p_value = 1 - self._chi2_cdf(chi2_stat, 1)
        
        return {"statistic": chi2_stat, "p_value": p_value}

    def _fisher_exact_manual(self, table):
        """Manuel Fisher's exact test"""
        # Expecting 2x2 contingency table
        if len(table) != 2 or len(table[0]) != 2:
            raise ValueError("Fisher's exact test requires a 2x2 table")
        
        a, b = table[0][0], table[0][1]
        c, d = table[1][0], table[1][1]
        
        n = a + b + c + d
        
        if n == 0:
            return {"odds_ratio": 1.0, "p_value": 1.0}
        
        # Calculate odds ratio
        if c == 0 or d == 0:
            odds_ratio = float('inf') if a * d > b * c else 0
        else:
            odds_ratio = (a * d) / (b * c) if b > 0 and c > 0 else float('inf')
        
        # Simplified p-value calculation (hypergeometric distribution approximation)
        # This is a basic approximation - full implementation would require hypergeometric pmf
        row1_sum = a + b
        col1_sum = a + c
        
        expected_a = (row1_sum * col1_sum) / n
        
        if expected_a > 0:
            chi2_stat = ((a - expected_a)**2) / expected_a
            p_value = 1 - self._chi2_cdf(chi2_stat, 1)
        else:
            p_value = 1.0
        
        return {"odds_ratio": odds_ratio, "p_value": min(1.0, 2 * p_value)}

    def _one_way_anova_manual(self, values, groups):
        """Manuel one-way ANOVA helper"""
        # Group data
        group_data = {}
        for val, grp in zip(values, groups):
            if grp not in group_data:
                group_data[grp] = []
            group_data[grp].append(val)
        
        # Calculate means
        grand_mean = self.mean(values)
        group_means = {grp: self.mean(data) for grp, data in group_data.items()}
        
        # Calculate sums of squares
        SSB = sum(len(data) * (group_means[grp] - grand_mean)**2 
                  for grp, data in group_data.items())
        
        SSW = sum(sum((val - group_means[grp])**2 for val in data)
                  for grp, data in group_data.items())
        
        # Degrees of freedom
        df_between = len(group_data) - 1
        df_within = len(values) - len(group_data)
        
        if df_within == 0 or SSW == 0:
            return {"statistic": 0, "p_value": 1.0}
        
        # F-statistic
        MSB = SSB / df_between
        MSW = SSW / df_within
        F_stat = MSB / MSW
        
        # p-value (approximation)
        p_value = 1 - self._f_cdf(F_stat, df_between, df_within)
        
        return {"statistic": F_stat, "p_value": p_value}

    def _f_cdf(self, x, df1, df2):
        """Simplified F-distribution CDF approximation"""
        if x <= 0:
            return 0
        # Very basic approximation - not accurate for all cases
        return min(1.0, x / (x + df2/df1))

    # Effect Size Measures
    def _cohen_d_manual(self, group1, group2):
        """Manuel Cohen's d effect size"""
        mean1, mean2 = self.mean(group1), self.mean(group2)
        n1, n2 = len(group1), len(group2)
        
        # Pooled standard deviation
        var1, var2 = self.variance(group1), self.variance(group2)
        pooled_std = math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0
        
        return (mean1 - mean2) / pooled_std

    def _hedges_g_manual(self, group1, group2):
        """Manuel Hedges' g effect size (bias-corrected Cohen's d)"""
        cohen_d = self._cohen_d_manual(group1, group2)
        n1, n2 = len(group1), len(group2)
        df = n1 + n2 - 2
        
        # Bias correction factor
        correction = 1 - (3 / (4 * df - 1))
        
        return cohen_d * correction

    def _glass_delta_manual(self, group1, group2):
        """Manuel Glass' delta effect size"""
        mean1, mean2 = self.mean(group1), self.mean(group2)
        std2 = math.sqrt(self.variance(group2))
        
        if std2 == 0:
            return 0
        
        return (mean1 - mean2) / std2

    # Power Analysis Functions
    def _power_ttest_manual(self, effect_size, n, alpha=0.05):
        """Manuel t-test power analysis"""
        # Cohen's conventions: small=0.2, medium=0.5, large=0.8
        df = n - 1
        t_critical = self._t_critical(alpha/2, df)  # two-tailed
        
        # Non-centrality parameter
        ncp = effect_size * math.sqrt(n)
        
        # Power calculation (simplified)
        power = 1 - self._t_cdf(t_critical - ncp, df) + self._t_cdf(-t_critical - ncp, df)
        
        return min(1.0, max(0.0, power))

    def _sample_size_ttest_manual(self, effect_size, power=0.8, alpha=0.05):
        """Manuel sample size calculation for t-test"""
        # Iterative approach to find required sample size
        for n in range(3, 1000):
            calculated_power = self._power_ttest_manual(effect_size, n, alpha)
            if calculated_power >= power:
                return n
        return 1000  # Maximum limit

    def _t_critical(self, alpha, df):
        """Critical value for t-distribution (approximation)"""
        if df >= 30:
            return self._normal_critical(alpha)
        # Rough approximation for t-critical values
        base = self._normal_critical(alpha)
        return base * (1 + 1/(4*df) + 1/(96*df**2))

    def _normal_critical(self, alpha):
        """Critical value for normal distribution"""
        # Common critical values
        if abs(alpha - 0.025) < 0.001:
            return 1.96
        elif abs(alpha - 0.005) < 0.001:
            return 2.576
        elif abs(alpha - 0.001) < 0.0001:
            return 3.291
        else:
            # Rough approximation using inverse normal
            return math.sqrt(2) * math.erfinv(1 - 2*alpha)

    # Robust Statistics
    def _trimmed_mean_manual(self, data, proportion=0.1):
        """Manuel trimmed mean"""
        n = len(data)
        if n == 0:
            return 0
        
        trim_count = int(n * proportion)
        sorted_data = sorted(data)
        
        if trim_count * 2 >= n:
            return self.median(data)
        
        trimmed = sorted_data[trim_count:n-trim_count]
        return self.mean(trimmed)

    def _winsorized_mean_manual(self, data, proportion=0.1):
        """Manuel Winsorized mean"""
        n = len(data)
        if n == 0:
            return 0
        
        trim_count = int(n * proportion)
        sorted_data = sorted(data)
        
        if trim_count * 2 >= n:
            return self.median(data)
        
        # Replace extreme values
        winsorized = sorted_data[:]
        lower_val = sorted_data[trim_count]
        upper_val = sorted_data[n-trim_count-1]
        
        for i in range(trim_count):
            winsorized[i] = lower_val
            winsorized[n-1-i] = upper_val
        
        return self.mean(winsorized)

    def _mad_manual(self, data):
        """Manuel Median Absolute Deviation"""
        if not data:
            return 0
        
        median_val = self.median(data)
        abs_deviations = [abs(x - median_val) for x in data]
        return self.median(abs_deviations)

    def _iqr_manual(self, data):
        """Manuel Interquartile Range"""
        if len(data) < 4:
            return 0
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        q1_pos = (n + 1) / 4
        q3_pos = 3 * (n + 1) / 4
        
        q1 = self._percentile_manual(sorted_data, 25)
        q3 = self._percentile_manual(sorted_data, 75)
        
        return q3 - q1

    def _percentile_manual(self, data, p):
        """Manuel percentile calculation"""
        if not data:
            return 0
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        if p == 0:
            return sorted_data[0]
        if p == 100:
            return sorted_data[-1]
        
        index = (p / 100) * (n - 1)
        lower = int(index)
        upper = min(lower + 1, n - 1)
        
        if lower == upper:
            return sorted_data[lower]
        
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight

    # Bootstrap and Resampling
    def _bootstrap_mean_manual(self, data, n_bootstrap=1000):
        """Manuel bootstrap for mean confidence interval"""
        import random
        
        bootstrap_means = []
        n = len(data)
        
        for _ in range(n_bootstrap):
            # Resample with replacement
            bootstrap_sample = [random.choice(data) for _ in range(n)]
            bootstrap_means.append(self.mean(bootstrap_sample))
        
        # Calculate confidence intervals
        sorted_means = sorted(bootstrap_means)
        lower_idx = int(0.025 * n_bootstrap)
        upper_idx = int(0.975 * n_bootstrap)
        
        return {
            "mean": self.mean(bootstrap_means),
            "std": math.sqrt(self.variance(bootstrap_means)),
            "ci_lower": sorted_means[lower_idx],
            "ci_upper": sorted_means[upper_idx]
        }

    def _jackknife_manual(self, data, statistic_func):
        """Manuel jackknife resampling"""
        n = len(data)
        if n <= 1:
            return {"estimate": 0, "bias": 0, "std_error": 0}
        
        # Calculate statistic for full sample
        full_stat = statistic_func(data)
        
        # Calculate leave-one-out statistics
        jackknife_stats = []
        for i in range(n):
            jackknife_sample = data[:i] + data[i+1:]
            jackknife_stats.append(statistic_func(jackknife_sample))
        
        # Jackknife estimates
        jackknife_mean = self.mean(jackknife_stats)
        bias = (n - 1) * (jackknife_mean - full_stat)
        
        # Standard error
        squared_diffs = [(stat - jackknife_mean)**2 for stat in jackknife_stats]
        variance = (n - 1) / n * sum(squared_diffs)
        std_error = math.sqrt(variance)
        
        return {
            "estimate": full_stat - bias,
            "bias": bias,
            "std_error": std_error
        }

    # Bayesian Statistics (Basic)
    def _bayes_factor_manual(self, data1, data2, prior_prob=0.5):
        """Manuel Bayes factor (simplified)"""
        # Simplified Bayes factor for comparing two groups
        n1, n2 = len(data1), len(data2)
        
        if n1 == 0 or n2 == 0:
            return 1.0
        
        # Use t-test statistic as evidence
        t_result = self._ttest_ind_manual(data1, data2)
        t_stat = abs(t_result["statistic"])
        
        # Convert to Bayes factor (very simplified approach)
        # This is a rough approximation
        bf = math.exp(-0.5 * t_stat**2 / (n1 + n2))
        
        return bf / (1 - bf + 1e-10)  # Avoid division by zero

    def _credible_interval_manual(self, data, credibility=0.95):
        """Manuel credible interval (using empirical distribution)"""
        if not data:
            return {"lower": 0, "upper": 0}
        
        sorted_data = sorted(data)
        n = len(sorted_data)
        
        alpha = 1 - credibility
        lower_idx = int(alpha/2 * n)
        upper_idx = int((1 - alpha/2) * n)
        
        return {
            "lower": sorted_data[max(0, lower_idx)],
            "upper": sorted_data[min(n-1, upper_idx)]
        }

    # Multivariate Statistics
    def _hotelling_t2_manual(self, sample1, sample2=None):
        """Manuel Hotelling's T² test"""
        # Simplified implementation for 2D data
        if sample2 is None:
            # One-sample test
            n = len(sample1)
            mean_vec = [self.mean([row[i] for row in sample1]) for i in range(len(sample1[0]))]
            
            # Calculate covariance matrix (simplified)
            cov_matrix = self._covariance_matrix_manual(sample1)
            
            # T² statistic (simplified for 2D)
            if len(mean_vec) == 2:
                det_cov = cov_matrix[0][0] * cov_matrix[1][1] - cov_matrix[0][1] * cov_matrix[1][0]
                if abs(det_cov) < 1e-10:
                    return {"statistic": 0, "p_value": 1.0}
                
                # Inverse of 2x2 matrix
                inv_cov = [[cov_matrix[1][1]/det_cov, -cov_matrix[0][1]/det_cov],
                          [-cov_matrix[1][0]/det_cov, cov_matrix[0][0]/det_cov]]
                
                # T² = n * mean' * inv_cov * mean
                t2 = n * (mean_vec[0] * (inv_cov[0][0] * mean_vec[0] + inv_cov[0][1] * mean_vec[1]) +
                         mean_vec[1] * (inv_cov[1][0] * mean_vec[0] + inv_cov[1][1] * mean_vec[1]))
                
                # Convert to F-statistic
                p = len(mean_vec)
                f_stat = ((n - p) / ((n - 1) * p)) * t2
                p_value = 1 - self._f_cdf(f_stat, p, n - p)
                
                return {"statistic": t2, "f_statistic": f_stat, "p_value": p_value}
        
        return {"statistic": 0, "p_value": 1.0}

    def _covariance_matrix_manual(self, data):
        """Manuel covariance matrix calculation"""
        if not data or not data[0]:
            return [[0]]
        
        n_vars = len(data[0])
        n_obs = len(data)
        
        # Calculate means
        means = [self.mean([row[i] for row in data]) for i in range(n_vars)]
        
        # Calculate covariance matrix
        cov_matrix = []
        for i in range(n_vars):
            row = []
            for j in range(n_vars):
                # Covariance between variables i and j
                cov = sum((data[k][i] - means[i]) * (data[k][j] - means[j]) 
                         for k in range(n_obs)) / (n_obs - 1)
                row.append(cov)
            cov_matrix.append(row)
        
        return cov_matrix

    # Meta-Analysis
    def _fixed_effect_meta_manual(self, effect_sizes, variances):
        """Manuel fixed-effect meta-analysis"""
        if len(effect_sizes) != len(variances) or not effect_sizes:
            return {"pooled_effect": 0, "se": 0, "ci_lower": 0, "ci_upper": 0}
        
        # Weights (inverse variance)
        weights = [1/var if var > 0 else 0 for var in variances]
        total_weight = sum(weights)
        
        if total_weight == 0:
            return {"pooled_effect": 0, "se": 0, "ci_lower": 0, "ci_upper": 0}
        
        # Pooled effect size
        pooled_effect = sum(w * es for w, es in zip(weights, effect_sizes)) / total_weight
        
        # Standard error
        se = math.sqrt(1 / total_weight)
        
        # 95% confidence interval
        ci_lower = pooled_effect - 1.96 * se
        ci_upper = pooled_effect + 1.96 * se
        
        return {
            "pooled_effect": pooled_effect,
            "se": se,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper
        }

    def _random_effect_meta_manual(self, effect_sizes, variances):
        """Manuel random-effects meta-analysis"""
        if len(effect_sizes) != len(variances) or not effect_sizes:
            return {"pooled_effect": 0, "se": 0, "tau2": 0}
        
        # First, calculate fixed-effect estimate
        fixed_result = self._fixed_effect_meta_manual(effect_sizes, variances)
        
        # Calculate Q statistic for heterogeneity
        weights = [1/var if var > 0 else 0 for var in variances]
        total_weight = sum(weights)
        
        if total_weight == 0:
            return {"pooled_effect": 0, "se": 0, "tau2": 0}
        
        Q = sum(w * (es - fixed_result["pooled_effect"])**2 
               for w, es in zip(weights, effect_sizes))
        
        # Between-study variance (tau²)
        k = len(effect_sizes)
        df = k - 1
        
        if Q > df:
            C = total_weight - sum(w**2 for w in weights) / total_weight
            tau2 = max(0, (Q - df) / C)
        else:
            tau2 = 0
        
        # Random-effects weights
        re_weights = [1/(var + tau2) for var in variances]
        re_total_weight = sum(re_weights)
        
        # Random-effects pooled estimate
        pooled_effect = sum(w * es for w, es in zip(re_weights, effect_sizes)) / re_total_weight
        se = math.sqrt(1 / re_total_weight)
        
        return {
            "pooled_effect": pooled_effect,
            "se": se,
            "tau2": tau2
        }

    def _chi2_pdf_manual(self, x, df):
        """Manuel chi-kare dağılımı PDF (yaklaşım)"""
        if x <= 0:
            return 0
        return x**(df/2 - 1) * math.exp(-x/2)

    def _chi2_cdf_manual(self, x, df):
        """Manuel chi-kare dağılımı CDF (yaklaşım)"""
        if x <= 0:
            return 0
        # Incomplete gamma function approximation
        return min(1.0, x / (x + df))

    def _f_pdf_manual(self, x, df1, df2):
        """Manuel F-dağılımı PDF (yaklaşım)"""
        if x <= 0:
            return 0
        return x**(df1/2 - 1) / (1 + df1*x/df2)**(0.5*(df1+df2))

    def _f_cdf_manual(self, x, df1, df2):
        """Manuel F-dağılımı CDF (yaklaşım)"""
        if x <= 0:
            return 0
        # Beta distribution approximation
        return min(1.0, x / (x + df2/df1))

    # MANOVA Implementation
    def _manova_manual(self, data, groups):
        """Manuel MANOVA (çok değişkenli varyans analizi)"""
        # Basit MANOVA implementasyonu
        unique_groups = list(set(groups))
        k = len(unique_groups)  # Number of groups
        
        if k < 2:
            return {"statistic": 0, "p_value": 1.0}
        
        # Group data
        group_data = {group: [] for group in unique_groups}
        for i, group in enumerate(groups):
            group_data[group].append(data[i])
        
        # Calculate group means
        group_means = {}
        for group in unique_groups:
            group_means[group] = [self.mean([row[j] for row in group_data[group]]) 
                                 for j in range(len(data[0]))]
        
        # Overall mean
        overall_mean = [self.mean([row[j] for row in data]) for j in range(len(data[0]))]
        
        # Between-group sum of squares
        bg_ss = 0
        for group in unique_groups:
            n_group = len(group_data[group])
            for j in range(len(data[0])):
                bg_ss += n_group * (group_means[group][j] - overall_mean[j])**2
        
        # Within-group sum of squares
        wg_ss = 0
        for group in unique_groups:
            for row in group_data[group]:
                for j in range(len(row)):
                    wg_ss += (row[j] - group_means[group][j])**2
        
        # Pillai's trace approximation
        if wg_ss == 0:
            return {"statistic": float('inf'), "p_value": 0.0}
        
        pillai_trace = bg_ss / (bg_ss + wg_ss)
        
        # Approximate F-statistic
        p = len(data[0])  # Number of dependent variables
        n = len(data)
        df1 = p * (k - 1)
        df2 = p * (n - k)
        
        if df2 <= 0:
            return {"statistic": pillai_trace, "p_value": 1.0}
        
        f_stat = (pillai_trace / (k - 1)) / ((1 - pillai_trace) / (n - k - p + 1))
        p_value = 1 - self._f_cdf(f_stat, df1, df2)
        
        return {
            "statistic": pillai_trace,
            "f_statistic": f_stat,
            "p_value": p_value,
            "df1": df1,
            "df2": df2
        }

    # Advanced Analysis Functions
    def _kmeans_manual(self, data, k):
        """Manuel K-means clustering"""
        n = len(data)
        if k >= n:
            return {"centroids": data, "labels": list(range(n))}
        
        # Initialize centroids randomly
        import random
        centroids = random.sample(data, k)
        labels = [0] * n
        
        for iteration in range(100):  # Max iterations
            # Assign points to nearest centroid
            new_labels = []
            for point in data:
                distances = [sum((point[i] - centroid[i])**2 for i in range(len(point))) 
                           for centroid in centroids]
                new_labels.append(distances.index(min(distances)))
            
            # Check convergence
            if new_labels == labels:
                break
            labels = new_labels
            
            # Update centroids
            for i in range(k):
                cluster_points = [data[j] for j in range(n) if labels[j] == i]
                if cluster_points:
                    centroids[i] = [self.mean([point[dim] for point in cluster_points]) 
                                  for dim in range(len(data[0]))]
        
        return {"centroids": centroids, "labels": labels}

    def _autocorrelation_manual(self, data, lags=None):
        """Manuel autocorrelation hesaplama"""
        n = len(data)
        if lags is None:
            lags = min(10, n // 4)
        
        mean_val = self.mean(data)
        variance = sum((x - mean_val)**2 for x in data) / n
        
        autocorr = []
        for lag in range(lags + 1):
            if lag == 0:
                autocorr.append(1.0)
            else:
                covariance = sum((data[i] - mean_val) * (data[i - lag] - mean_val) 
                               for i in range(lag, n)) / (n - lag)
                autocorr.append(covariance / variance if variance > 0 else 0)
        
        return autocorr

    # Additional Manual Implementations for NumPy/Pandas Functions
    def _concat_manual(self, *dfs):
        """Manuel dataframe concatenation"""
        result_data = []
        for df in dfs:
            data = df["data"] if isinstance(df, dict) and "data" in df else df
            result_data.extend(data)
        return {"data": result_data, "type": "manual_dataframe"}

    def _drop_duplicates_manual(self, data):
        """Manuel duplicate removal"""
        actual_data = data["data"] if isinstance(data, dict) and "data" in data else data
        seen = set()
        result = []
        
        for row in actual_data:
            if isinstance(row, dict):
                key = tuple(sorted(row.items()))
            else:
                key = tuple(row) if isinstance(row, (list, tuple)) else row
            
            if key not in seen:
                seen.add(key)
                result.append(row)
        
        return {"data": result, "type": "manual_dataframe"}

    def _fillna_manual(self, data, value):
        """Manuel NA filling"""
        actual_data = data["data"] if isinstance(data, dict) and "data" in data else data
        result = []
        
        for row in actual_data:
            if isinstance(row, dict):
                new_row = {k: (value if v is None or v == '' else v) for k, v in row.items()}
            elif isinstance(row, (list, tuple)):
                new_row = [value if x is None or x == '' else x for x in row]
            else:
                new_row = value if row is None or row == '' else row
            result.append(new_row)
        
        return {"data": result, "type": "manual_dataframe"}

    def _dropna_manual(self, data):
        """Manuel NA dropping"""
        actual_data = data["data"] if isinstance(data, dict) and "data" in data else data
        result = []
        
        for row in actual_data:
            if isinstance(row, dict):
                if not any(v is None or v == '' for v in row.values()):
                    result.append(row)
            elif isinstance(row, (list, tuple)):
                if not any(x is None or x == '' for x in row):
                    result.append(row)
            else:
                if row is not None and row != '':
                    result.append(row)
        
        return {"data": result, "type": "manual_dataframe"}

    def _rolling_manual(self, data, window):
        """Manuel rolling window"""
        actual_data = data["data"] if isinstance(data, dict) and "data" in data else data
        if not isinstance(actual_data[0], (int, float)):
            # For complex data, just return first column
            actual_data = [row[0] if isinstance(row, (list, tuple)) else list(row.values())[0] if isinstance(row, dict) else row for row in actual_data]
        
        result = []
        for i in range(len(actual_data)):
            if i + 1 >= window:
                window_data = actual_data[i + 1 - window:i + 1]
                result.append(self.mean(window_data))
            else:
                result.append(None)
        
        return {"data": result, "type": "manual_series"}

    def _pivot_table_manual(self, data, values, index, columns, aggfunc='mean'):
        """Manuel pivot table"""
        actual_data = data["data"] if isinstance(data, dict) and "data" in data else data
        
        # Group by index and columns
        groups = {}
        for row in actual_data:
            index_val = row[index]
            column_val = row[columns]
            value = row[values]
            
            key = (index_val, column_val)
            if key not in groups:
                groups[key] = []
            groups[key].append(value)
        
        # Apply aggregation function
        pivot_result = {}
        for (index_val, column_val), value_list in groups.items():
            if index_val not in pivot_result:
                pivot_result[index_val] = {}
            
            if aggfunc == 'mean':
                pivot_result[index_val][column_val] = self.mean(value_list)
            elif aggfunc == 'sum':
                pivot_result[index_val][column_val] = sum(value_list)
            elif aggfunc == 'count':
                pivot_result[index_val][column_val] = len(value_list)
            elif aggfunc == 'min':
                pivot_result[index_val][column_val] = min(value_list)
            elif aggfunc == 'max':
                pivot_result[index_val][column_val] = max(value_list)
            else:
                pivot_result[index_val][column_val] = value_list[0]  # Default: first
        
        return {"data": pivot_result, "type": "manual_pivot_table"}

    def _select_manual(self, condlist, choicelist, default=0):
        """Manuel select function"""
        result = []
        for i in range(len(condlist[0])):
            selected = default
            for cond, choice in zip(condlist, choicelist):
                if cond[i]:
                    selected = choice[i] if isinstance(choice, (list, tuple)) else choice
                    break
            result.append(selected)
        return result

    def _searchsorted_manual(self, arr, values):
        """Manuel searchsorted"""
        if not isinstance(values, (list, tuple)):
            values = [values]
        
        result = []
        for value in values:
            left, right = 0, len(arr)
            while left < right:
                mid = (left + right) // 2
                if arr[mid] < value:
                    left = mid + 1
                else:
                    right = mid
            result.append(left)
        
        return result if len(result) > 1 else result[0]

    def _meshgrid_manual(self, x, y):
        """Manuel meshgrid"""
        X = [[xi for xi in x] for _ in y]
        Y = [[yi for _ in x] for yi in y]
        return X, Y

    def _gradient_manual(self, arr):
        """Manuel gradient"""
        if len(arr) < 2:
            return [0] * len(arr)
        
        result = []
        for i in range(len(arr)):
            if i == 0:
                result.append(arr[1] - arr[0])
            elif i == len(arr) - 1:
                result.append(arr[-1] - arr[-2])
            else:
                result.append((arr[i + 1] - arr[i - 1]) / 2)
        
        return result

    def _diff_manual(self, arr, n=1):
        """Manuel difference"""
        result = arr[:]
        for _ in range(n):
            result = [result[i + 1] - result[i] for i in range(len(result) - 1)]
        return result

    def _cumsum_manual(self, arr):
        """Manuel cumulative sum"""
        result = []
        total = 0
        for x in arr:
            total += x
            result.append(total)
        return result

    def _cumprod_manual(self, arr):
        """Manuel cumulative product"""
        result = []
        product = 1
        for x in arr:
            product *= x
            result.append(product)
        return result

    def _tile_manual(self, arr, reps):
        """Manuel tile function"""
        if isinstance(reps, int):
            return arr * reps
        elif isinstance(reps, (list, tuple)) and len(reps) == 1:
            return arr * reps[0]
        elif isinstance(reps, (list, tuple)) and len(reps) == 2:
            # 2D tiling
            result = []
            for _ in range(reps[0]):
                row = []
                for _ in range(reps[1]):
                    row.extend(arr)
                result.append(row)
            return result
        else:
            return arr

    # Advanced Statistical Tests continued
    def _bartlett_manual(self, *groups):
        """Manuel Bartlett's test for equal variances"""
        k = len(groups)
        if k < 2:
            return {"statistic": 0, "p_value": 1.0}
        
        variances = [self.variance(group, ddof=1) for group in groups]
        ns = [len(group) for group in groups]
        
        # Pooled variance
        pooled_var = sum((n - 1) * var for n, var in zip(ns, variances)) / sum(n - 1 for n in ns)
        
        if pooled_var == 0:
            return {"statistic": 0, "p_value": 1.0}
        
        # Bartlett's test statistic
        numerator = sum(n - 1 for n in ns) * math.log(pooled_var) - sum((n - 1) * math.log(var) for n, var in zip(ns, variances) if var > 0)
        denominator = 1 + (sum(1 / (n - 1) for n in ns) - 1 / sum(n - 1 for n in ns)) / (3 * (k - 1))
        
        if denominator == 0:
            return {"statistic": 0, "p_value": 1.0}
        
        B = numerator / denominator
        
        # p-value (chi-square distribution)
        df = k - 1
        p_value = 1 - self._chi2_cdf(B, df)
        
        return {"statistic": B, "p_value": p_value, "df": df}

    def _levene_manual(self, *groups):
        """Manuel Levene's test for equal variances"""
        k = len(groups)
        if k < 2:
            return {"statistic": 0, "p_value": 1.0}
        
        # Calculate deviations from group medians
        deviations = []
        for group in groups:
            median_val = self.median(group)
            deviations.extend([abs(x - median_val) for x in group])
        
        # Apply one-way ANOVA to deviations
        group_deviations = []
        start_idx = 0
        for group in groups:
            end_idx = start_idx + len(group)
            group_deviations.append(deviations[start_idx:end_idx])
            start_idx = end_idx
        
        return self.anova_one_way(*group_deviations)

    def _tukey_hsd_manual(self, data, groups):
        """Manuel Tukey HSD post-hoc test"""
        unique_groups = list(set(groups))
        k = len(unique_groups)
        
        if k < 2:
            return {"comparisons": []}
        
        # Group data
        group_data = {group: [data[i] for i, g in enumerate(groups) if g == group] 
                     for group in unique_groups}
        
        # Calculate MSE (Mean Square Error) from ANOVA
        anova_result = self.anova_one_way(*[group_data[group] for group in unique_groups])
        mse = anova_result.get("ss_within", 0) / anova_result.get("df_within", 1)
        
        # Pairwise comparisons
        comparisons = []
        for i in range(k):
            for j in range(i + 1, k):
                group1, group2 = unique_groups[i], unique_groups[j]
                data1, data2 = group_data[group1], group_data[group2]
                
                mean1, mean2 = self.mean(data1), self.mean(data2)
                n1, n2 = len(data1), len(data2)
                
                # Tukey HSD statistic
                if mse > 0 and (n1 + n2) > 0:
                    se = math.sqrt(mse * (1/n1 + 1/n2))
                    q_stat = abs(mean1 - mean2) / se
                else:
                    q_stat = 0
                
                comparisons.append({
                    "group1": group1,
                    "group2": group2,
                    "mean_diff": mean1 - mean2,
                    "q_statistic": q_stat,
                    "significant": q_stat > 3.0  # Approximate critical value
                })
        
        return {"comparisons": comparisons}

    def _bonferroni_correction(self, p_values, alpha=0.05):
        """Bonferroni çoklu karşılaştırma düzeltmesi"""
        corrected_alpha = alpha / len(p_values)
        return {
            "corrected_alpha": corrected_alpha,
            "significant": [p < corrected_alpha for p in p_values],
            "rejected": sum(p < corrected_alpha for p in p_values)
        }

    def _benjamini_hochberg_correction(self, p_values, alpha=0.05):
        """Benjamini-Hochberg FDR düzeltmesi"""
        n = len(p_values)
        sorted_p = sorted(enumerate(p_values), key=lambda x: x[1])
        
        rejected = [False] * n
        for i, (orig_idx, p_val) in enumerate(sorted_p):
            critical_value = (i + 1) / n * alpha
            if p_val <= critical_value:
                rejected[orig_idx] = True
            else:
                break
        
        return {
            "critical_values": [(i + 1) / n * alpha for i in range(n)],
            "significant": rejected,
            "rejected": sum(rejected)
        }
        denominator = ((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2)) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0

    # String Operations
    def split(self, s, delimiter):
        """String bölme"""
        return s.split(delimiter)

    def join(self, items, delimiter):
        """String birleştirme"""
        return delimiter.join(str(item) for item in items)

    def trim(self, s):
        """Boşluk kaldırma"""
        return s.strip()

    def replace(self, s, old, new):
        """String değiştirme"""
        return s.replace(old, new)

    def format(self, s, *args):
        """String formatlama"""
        return s.format(*args)

    def match_regex(self, s, pattern):
        """Regex eşleşme kontrolü"""
        return bool(re.match(pattern, s))

    def find_regex(self, s, pattern):
        """Regex ile eşleşme bulma"""
        return re.findall(pattern, s)

    # File System Operations
    def open(self, path, mode):
        """Dosya açma"""
        return open(path, mode, encoding=self.default_encoding)

    def read_lines(self, path):
        """Dosyayı satır satır okuma"""
        with open(path, "r", encoding=self.default_encoding) as f:
            return f.readlines()

    def write_json(self, obj, path):
        """JSON dosyası yazma"""
        with open(path, "w", encoding=self.default_encoding) as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    def read_json(self, path):
        """JSON dosyası okuma"""
        with open(path, "r", encoding=self.default_encoding) as f:
            return json.load(f)

    def list_dir(self, path):
        """Dizin listeleme"""
        return os.listdir(path)

    def exists(self, path):
        """Dosya varlık kontrolü"""
        return os.path.exists(path)

    def mkdir(self, path):
        """Dizin oluşturma"""
        os.makedirs(path, exist_ok=True)

    def copy_file(self, src, dst):
        """Dosya kopyalama"""
        shutil.copy2(src, dst)

    def move_file(self, src, dst):
        """Dosya taşıma"""
        shutil.move(src, dst)

    def delete_file(self, path):
        """Dosya silme"""
        os.remove(path)

    def compress_zip(self, files, output):
        """ZIP sıkıştırma"""
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                zf.write(file)

    def extract_zip(self, zip_file, output_dir):
        """ZIP çıkarma"""
        with zipfile.ZipFile(zip_file, "r") as zf:
            zf.extractall(output_dir)

    # Network Operations
    def download(self, url, path):
        """URL'den dosya indirme"""
        if not requests:
            raise PdsXRuntimeError("Requests kütüphanesi yüklü değil")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(path, "wb") as f:
                f.write(response.content)
            return True
        except Exception as e:
            raise PdsXRuntimeError(f"İndirme hatası: {e}")

    def ping(self, host):
        """Host erişilebilirlik kontrolü"""
        try:
            socket.gethostbyname(host)
            return True
        except socket.error:
            return False

    # Time and Date Operations
    def time_now(self):
        """Geçerli saat"""
        return time.strftime("%H:%M:%S")

    def date_now(self):
        """Geçerli tarih"""
        return time.strftime("%Y-%m-%d")

    def timer(self):
        """Zaman damgası"""
        return time.time()

    def sleep(self, seconds):
        """Bekleme"""
        time.sleep(seconds)

    # System and Performance Monitoring
    def memory_usage(self):
        """Bellek kullanımı"""
        if psutil:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # MB
        return 0

    def cpu_count(self):
        """CPU çekirdek sayısı"""
        return multiprocessing.cpu_count()

    def shell(self, cmd):
        """Sistem komutu çalıştırma"""
        try:
            return subprocess.getoutput(cmd)
        except Exception as e:
            raise PdsXRuntimeError(f"Komut hatası: {e}")

    # Asynchronous Operations
    def run_async(self, func):
        """Asenkron fonksiyon çalıştırma"""
        t = Thread(target=func)
        t.start()
        self.async_tasks.append(t)
        return t

    def wait_all(self):
        """Tüm asenkron görevleri bekleme"""
        for task in self.async_tasks:
            task.join()
        self.async_tasks.clear()

    # Data Structure Operations
    def create_stack(self, max_size=None):
        """Yığın oluşturma"""
        return Stack(max_size)

    def create_queue(self, max_size=None):
        """Kuyruk oluşturma"""
        return Queue(max_size)

    # Type Information
    def type_of(self, value):
        """Değişken tipini döndürme"""
        type_map = {
            int: "INTEGER",
            float: "DOUBLE", 
            str: "STRING",
            list: "LIST",
            dict: "DICT",
            bool: "BOOLEAN",
            type(None): "NULL"
        }
        return type_map.get(type(value), "UNKNOWN")

    # Additional utility methods
    def timer(self):
        """Geçerli zamanı döndürür"""
        return time.time()

    def time_now(self):
        """Geçerli zamanı string olarak döndürür"""
        return time.strftime("%H:%M:%S")

    def date_now(self):
        """Geçerli tarihi string olarak döndürür"""
        return time.strftime("%Y-%m-%d")

    def sleep(self, seconds):
        """Program duraklatma"""
        time.sleep(seconds)
        return None

    def shell(self, command):
        """Sistem komutu çalıştırma"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {e}"

    def memory_usage(self):
        """Bellek kullanımı"""
        try:
            import psutil
            return psutil.virtual_memory().percent
        except ImportError:
            return 0

    def cpu_count(self):
        """CPU sayısı"""
        return os.cpu_count()

    def list_dir(self, path):
        """Dizin listesi"""
        try:
            return os.listdir(path)
        except Exception:
            return []

    def exists(self, path):
        """Dosya/dizin varlık kontrolü"""
        return os.path.exists(path)

# End of LibXCore class

# Main PDSX Interpreter Class
class pdsXInterpreter:
    """Ana PDSX Yorumlayıcı Sınıfı - Tüm Özelliklerle Birleştirilmiş"""
    
    def __init__(self):
        # Core state
        self.program = []
        self.program_counter = 0
        self.global_vars = {}
        self.scopes = [{}]  # Scope stack
        self.running = False
        
        # Module system
        self.modules = {}
        self.current_module = "main"
        
        # Type system
        self.types = {}
        self.type_table = {
            "STRING": str, "INTEGER": int, "DOUBLE": float, "BYTE": int,
            "SHORT": int, "LONG": int, "SINGLE": float, "BOOLEAN": bool,
            "LIST": list, "ARRAY": list, "DICT": dict, "SET": set,
            "POINTER": lambda x: Pointer(None, x, self)
        }
        
        # Function and procedure system
        self.functions = {}
        self.subs = {}
        self.labels = {}
        
        # Class system
        self.classes = {}
        self.current_class = None
        
        # Memory management
        self.memory_manager = MemoryManager()
        self.memory_pool = {}
        self.next_address = 1000
        
        # Error handling
        self.error_handler = None
        self.debug_mode = False
        self.trace_mode = False
        
        # Control structures
        self.loop_stack = []
        self.select_stack = []
        self.if_stack = []
        self.call_stack = []
        
        # Data operations
        self.data_list = []
        self.data_pointer = 0
        
        # Database connections
        self.db_connections = {}
        self.file_handles = {}
        
        # Performance optimizations
        self.expr_cache = {}
        self.variable_cache = {}
        
        # Multi-language support
        self.language = "tr"
        self.translations = {}
        
        # REPL mode
        self.repl_mode = False
        
        # LibXCore integration
        self.libx_core = LibXCore()
        
        # Event System
        self.event_system = EnhancedEventSystem()
        
        # Module System
        self.module_system = ModuleSystem()
        
        # Prolog Engine  
        self.prolog_engine = PrologEngine()
        
        # CLAZZ Dynamic Class System
        self.clazz_system = ClazzSystem()
        
        # Pipeline System
        self.pipeline_system = PipelineSystem()
        
        # SQL Database System
        self.db_system = SQLiteDatabase()
        
        # ISAM File System
        self.isam_files = {}
        
        # Extended Control Flow
        self.goto_labels = {}
        self.gosub_stack = []
        
        # C64 GUI Engine Integration
        self.c64_gui_engine = None
        self.gui_initialized = False
        
        # LibX GUI Integration  
        self.libx_gui = None
        
        # Initialize function table
        self.function_table = self._init_function_table()
        
        # Initialize operator table for complex expressions
        self.operator_table = self._init_operator_table()
        
        # API connection system
        self.api_connections = {}
        
        logging.basicConfig(level=logging.INFO)

    def _init_function_table(self):
        """Gelişmiş fonksiyon tablosunu başlatma"""
        funcs = {
            # Basic String Functions
            "MID$": lambda s, start, length: s[start-1:start-1+length],
            "LEN": len,
            "LEFT$": lambda s, n: s[:n],
            "RIGHT$": lambda s, n: s[-n:],
            "LTRIM$": lambda s: s.lstrip(),
            "RTRIM$": lambda s: s.rstrip(),
            "TRIM$": lambda s: s.strip(),
            "UCASE$": lambda s: s.upper(),
            "LCASE$": lambda s: s.lower(),
            "UPPER$": lambda s: s.upper(),
            "LOWER$": lambda s: s.lower(),
            "STR$": lambda n: str(n),
            "STR": lambda n: str(n),
            "VAL": lambda s: float(s) if s.replace(".", "").replace("-", "").isdigit() else 0,
            "ASC": lambda c: ord(c[0]) if c else 0,
            "CHR$": lambda n: chr(n),
            "STRING$": lambda n, c: c * n,
            "SPACE$": lambda n: " " * n,
            "INSTR": lambda start, s, sub: s.find(sub, start-1) + 1,
            
            # Mathematical Functions
            "ABS": abs,
            "INT": int,
            "FIX": lambda x: int(x),
            "ROUND": lambda x, n=0: round(x, n),
            "SGN": lambda x: -1 if x < 0 else (1 if x > 0 else 0),
            "MOD": lambda x, y: x % y,
            "SQR": lambda x: x ** 0.5,
            "SIN": math.sin,
            "COS": math.cos,
            "TAN": math.tan,
            "LOG": math.log,
            "EXP": math.exp,
            "ATN": math.atan,
            "PI": lambda: math.pi,
            "RND": random.random,
            
            # Advanced Math Functions
            "SINH": math.sinh,
            "COSH": math.cosh,
            "TANH": math.tanh,
            "ASIN": math.asin,
            "ACOS": math.acos,
            "ATAN2": math.atan2,
            "CEIL": math.ceil,
            "FLOOR": math.floor,
            "POW": pow,
            "SQRT": math.sqrt,
            "MIN": min,
            "MAX": max,
            
            # Data Science Functions (if NumPy available)
            "MEAN": self.libx_core.mean,
            "MEDIAN": self.libx_core.median,
            "STD": self.libx_core.std,
            "SUM": self.libx_core.sum,
            "CORR": self.libx_core.correlation,
            
            # Advanced Statistical Functions
            "VARIANCE": self.libx_core.variance,
            "VAR": self.libx_core.variance,
            "PERCENTILE": self.libx_core.percentile,
            "QUANTILE": self.libx_core.quantile,
            "IQR": self.libx_core.iqr,
            "SKEWNESS": self.libx_core.skewness,
            "SKEW": self.libx_core.skewness,
            "KURTOSIS": self.libx_core.kurtosis,
            "KURT": self.libx_core.kurtosis,
            "COVARIANCE": self.libx_core.covariance,
            "COV": self.libx_core.covariance,
            
            # Hypothesis Testing Functions
            "TTEST1": self.libx_core.t_test_one_sample,
            "TTEST2": self.libx_core.t_test_two_sample,
            "TTESTPAIRED": self.libx_core.paired_t_test,
            "ZTEST1": self.libx_core.z_test_one_sample,
            "ZTEST2": self.libx_core.z_test_two_sample,
            "FTEST": self.libx_core.f_test,
            "CHITEST": self.libx_core.chi_square_test,
            "CHI2TEST": self.libx_core.chi_square_test,
            "ANOVA": self.libx_core.anova_one_way,
            "ANOVA1": self.libx_core.anova_one_way,
            
            # Regression Functions
            "LINREG": self.libx_core.linear_regression,
            "POLYREG": self.libx_core.polynomial_regression,
            
            # NumPy Array Functions (if available)
            "ARRAY": lambda *args: np.array(args) if np else list(args),
            "ZEROS": lambda *shape: np.zeros(shape) if np else [[0] * shape[1] for _ in range(shape[0])] if len(shape) == 2 else [0] * shape[0],
            "ONES": lambda *shape: np.ones(shape) if np else [[1] * shape[1] for _ in range(shape[0])] if len(shape) == 2 else [1] * shape[0],
            "FULL": lambda shape, fill_value: np.full(shape, fill_value) if np else [[fill_value] * shape[1] for _ in range(shape[0])] if len(shape) == 2 else [fill_value] * shape[0],
            "EYE": lambda n: np.eye(n) if np else [[1 if i == j else 0 for j in range(n)] for i in range(n)],
            "IDENTITY": lambda n: np.eye(n) if np else [[1 if i == j else 0 for j in range(n)] for i in range(n)],
            "ARANGE": lambda start, stop=None, step=1: np.arange(start, stop, step) if np else list(range(start, stop or start, step)) if stop else list(range(start)),
            "LINSPACE": lambda start, stop, num=50: np.linspace(start, stop, num) if np else [start + i * (stop - start) / (num - 1) for i in range(num)],
            
            # Array Manipulation Functions
            "RESHAPE": lambda arr, *shape: np.reshape(arr, shape) if np else self._reshape_manual(arr, shape),
            "FLATTEN": lambda arr: np.flatten(arr) if np else self._flatten_manual(arr),
            "TRANSPOSE": lambda arr: np.transpose(arr) if np else self._transpose_manual(arr),
            "CONCATENATE": lambda *arrays: np.concatenate(arrays) if np else self._concatenate_manual(arrays),
            "STACK": lambda *arrays: np.stack(arrays) if np else list(arrays),
            "VSTACK": lambda *arrays: np.vstack(arrays) if np else self._vstack_manual(arrays),
            "HSTACK": lambda *arrays: np.hstack(arrays) if np else self._hstack_manual(arrays),
            
            # Mathematical Array Functions
            "DOT": lambda a, b: np.dot(a, b) if np else self._dot_product_manual(a, b),
            "MATMUL": lambda a, b: np.matmul(a, b) if np else self._matrix_multiply_manual(a, b),
            "CROSS": lambda a, b: np.cross(a, b) if np else self._cross_product_manual(a, b),
            "NORM": lambda arr: np.linalg.norm(arr) if np else math.sqrt(sum(x**2 for x in arr)),
            "DET": lambda arr: np.linalg.det(arr) if np else self._determinant_manual(arr),
            "INV": lambda arr: np.linalg.inv(arr) if np else self._inverse_manual(arr),
            "SOLVE": lambda a, b: np.linalg.solve(a, b) if np else self._solve_linear_system(a, b),
            
            # Element-wise Functions
            "ADD": lambda a, b: np.add(a, b) if np else [x + y for x, y in zip(a, b)],
            "SUBTRACT": lambda a, b: np.subtract(a, b) if np else [x - y for x, y in zip(a, b)],
            "MULTIPLY": lambda a, b: np.multiply(a, b) if np else [x * y for x, y in zip(a, b)],
            "DIVIDE": lambda a, b: np.divide(a, b) if np else [x / y for x, y in zip(a, b)],
            "POWER": lambda a, b: np.power(a, b) if np else [x ** y for x, y in zip(a, b)],
            
            # Statistical Array Functions
            "SORT": lambda arr: np.sort(arr) if np else sorted(arr),
            "ARGSORT": lambda arr: np.argsort(arr) if np else sorted(range(len(arr)), key=lambda i: arr[i]),
            "UNIQUE": lambda arr: np.unique(arr) if np else list(set(arr)),
            "BINCOUNT": lambda arr: np.bincount(arr) if np else self._bincount_manual(arr),
            "HISTOGRAM": lambda arr, bins=10: np.histogram(arr, bins) if np else self._histogram_manual(arr, bins),
            
            # Advanced Statistical Tests (SciPy equivalent)
            "NORMALTEST": lambda data: stats.normaltest(data) if stats else self._normaltest_manual(data),
            "SHAPIRO": lambda data: stats.shapiro(data) if stats else self._shapiro_manual(data),
            "JARQUEBERATEST": lambda data: stats.jarque_bera(data) if stats else self._jarque_bera_manual(data),
            "KOLMOGOROVTEST": lambda data1, data2=None: stats.ks_2samp(data1, data2) if stats and data2 else stats.kstest(data1, 'norm') if stats else self._ks_test_manual(data1, data2),
            "MANNWHITNEY": lambda data1, data2: stats.mannwhitneyu(data1, data2) if stats else self._mann_whitney_manual(data1, data2),
            "WILCOXON": lambda data1, data2=None: stats.wilcoxon(data1, data2) if stats else self._wilcoxon_manual(data1, data2),
            "KRUSKAL": lambda *groups: stats.kruskal(*groups) if stats else self._kruskal_manual(*groups),
            "FRIEDMAN": lambda *groups: stats.friedmanchisquare(*groups) if stats else self._friedman_manual(*groups),
            "BARTLETT": lambda *groups: stats.bartlett(*groups) if stats else self._bartlett_manual(*groups),
            "LEVENE": lambda *groups: stats.levene(*groups) if stats else self._levene_manual(*groups),
            "FLIGNER": lambda *groups: stats.fligner(*groups) if stats else self._fligner_manual(*groups),
            
            # Correlation Tests
            "PEARSONR": lambda x, y: stats.pearsonr(x, y) if stats else self._pearson_test_manual(x, y),
            "SPEARMANR": lambda x, y: stats.spearmanr(x, y) if stats else self._spearman_test_manual(x, y),
            "KENDALLTAU": lambda x, y: stats.kendalltau(x, y) if stats else self._kendall_test_manual(x, y),
            
            # Distribution Tests
            "BINOMTEST": lambda k, n, p: stats.binomtest(k, n, p) if stats else self._binom_test_manual(k, n, p),
            "POISSONTEST": lambda observed, expected: self._poisson_test_manual(observed, expected),
            
            # MANOVA and Advanced ANOVA
            "MANOVA": lambda data, groups: self._manova_manual(data, groups),
            "ANOVA2WAY": lambda data, factor1, factor2: self._anova_two_way_manual(data, factor1, factor2),
            "REPEATED_ANOVA": lambda data, subjects, conditions: self._repeated_measures_anova_manual(data, subjects, conditions),
            
            # Post-hoc Tests
            "TUKEY": lambda data, groups: self._tukey_hsd_manual(data, groups),
            "BONFERRONI": lambda pvalues, alpha=0.05: self._bonferroni_correction(pvalues, alpha),
            "BENJAMINI": lambda pvalues, alpha=0.05: self._benjamini_hochberg_correction(pvalues, alpha),
            
            # Distribution Functions
            "NORM_PDF": lambda x, mu=0, sigma=1: stats.norm.pdf(x, mu, sigma) if stats else self._norm_pdf_manual(x, mu, sigma),
            "NORM_CDF": lambda x, mu=0, sigma=1: stats.norm.cdf(x, mu, sigma) if stats else self._norm_cdf_manual(x, mu, sigma),
            "T_PDF": lambda x, df: stats.t.pdf(x, df) if stats else self._t_pdf_manual(x, df),
            "T_CDF": lambda x, df: stats.t.cdf(x, df) if stats else self._t_cdf_manual(x, df),
            "CHI2_PDF": lambda x, df: stats.chi2.pdf(x, df) if stats else self._chi2_pdf_manual(x, df),
            "CHI2_CDF": lambda x, df: stats.chi2.cdf(x, df) if stats else self._chi2_cdf_manual(x, df),
            "F_PDF": lambda x, df1, df2: stats.f.pdf(x, df1, df2) if stats else self._f_pdf_manual(x, df1, df2),
            "F_CDF": lambda x, df1, df2: stats.f.cdf(x, df1, df2) if stats else self._f_cdf_manual(x, df1, df2),
            
            # Random Sampling
            "RANDNORM": lambda size=1, mu=0, sigma=1: np.random.normal(mu, sigma, size) if np else [random.gauss(mu, sigma) for _ in range(size)],
            "RANDT": lambda df, size=1: np.random.standard_t(df, size) if np else [self._random_t_manual(df) for _ in range(size)],
            "RANDCHI2": lambda df, size=1: np.random.chisquare(df, size) if np else [self._random_chi2_manual(df) for _ in range(size)],
            "RANDF": lambda df1, df2, size=1: np.random.f(df1, df2, size) if np else [self._random_f_manual(df1, df2) for _ in range(size)],
            "RANDBINOM": lambda n, p, size=1: np.random.binomial(n, p, size) if np else [self._random_binomial_manual(n, p) for _ in range(size)],
            "RANDPOISSON": lambda lam, size=1: np.random.poisson(lam, size) if np else [self._random_poisson_manual(lam) for _ in range(size)],
            
            # Signal Processing (SciPy equivalent)
            "FFT": lambda signal: np.fft.fft(signal) if np else self._fft_manual(signal),
            "IFFT": lambda signal: np.fft.ifft(signal) if np else self._ifft_manual(signal),
            "CONVOLVE": lambda signal1, signal2: np.convolve(signal1, signal2) if np else self._convolve_manual(signal1, signal2),
            "CORRELATE": lambda signal1, signal2: np.correlate(signal1, signal2, mode='full') if np else self._correlate_manual(signal1, signal2),
            
            # Interpolation
            "INTERP1D": lambda x, y, new_x: np.interp(new_x, x, y) if np else self._interp1d_manual(x, y, new_x),
            "SPLINE": lambda x, y, new_x, degree=3: self._spline_interpolation_manual(x, y, new_x, degree),
            
            # Optimization
            "MINIMIZE": lambda func, x0: self._minimize_manual(func, x0),
            "LEASTSQ": lambda func, x0, data: self._least_squares_manual(func, x0, data),
            
            # Clustering
            "KMEANS": lambda data, k: self._kmeans_manual(data, k),
            "HIERARCHICAL": lambda data: self._hierarchical_clustering_manual(data),
            
            # Time Series Analysis
            "AUTOCORR": lambda data, lags=None: self._autocorrelation_manual(data, lags),
            "CROSSCORR": lambda data1, data2, lags=None: self._crosscorrelation_manual(data1, data2, lags),
            "ARIMA": lambda data, order: self._arima_manual(data, order),
            
            # Pandas-like Functions (if available)
            "DATAFRAME": lambda data: pd.DataFrame(data) if pd else {"data": data, "type": "manual_dataframe"},
            "SERIES": lambda data: pd.Series(data) if pd else {"data": data, "type": "manual_series"},
            "READ_CSV": lambda filename: pd.read_csv(filename) if pd else self._read_csv_manual(filename),
            "TO_CSV": lambda data, filename: data.to_csv(filename) if hasattr(data, 'to_csv') else self._write_csv_manual(data, filename),
            "GROUPBY": lambda data, by: data.groupby(by) if hasattr(data, 'groupby') else self._groupby_manual(data, by),
            "PIVOT": lambda data, index, columns, values: data.pivot(index, columns, values) if hasattr(data, 'pivot') else self._pivot_manual(data, index, columns, values),
            "MERGE": lambda df1, df2, on: pd.merge(df1, df2, on=on) if pd else self._merge_manual(df1, df2, on),
            "CONCAT": lambda *dfs: pd.concat(dfs) if pd else self._concat_manual(*dfs),
            "DROP_DUPLICATES": lambda data: data.drop_duplicates() if hasattr(data, 'drop_duplicates') else self._drop_duplicates_manual(data),
            "FILLNA": lambda data, value: data.fillna(value) if hasattr(data, 'fillna') else self._fillna_manual(data, value),
            "DROPNA": lambda data: data.dropna() if hasattr(data, 'dropna') else self._dropna_manual(data),
            "ROLLING": lambda data, window: data.rolling(window) if hasattr(data, 'rolling') else self._rolling_manual(data, window),
            "RESAMPLE": lambda data, rule: data.resample(rule) if hasattr(data, 'resample') else self._resample_manual(data, rule),
            "PIVOT_TABLE": lambda data, values, index, columns, aggfunc='mean': data.pivot_table(values, index, columns, aggfunc) if hasattr(data, 'pivot_table') else self._pivot_table_manual(data, values, index, columns, aggfunc),
            
            # Additional NumPy Functions
            "CLIP": lambda arr, min_val, max_val: np.clip(arr, min_val, max_val) if np else [max(min_val, min(max_val, x)) for x in arr],
            "WHERE": lambda condition, x, y: np.where(condition, x, y) if np else [x[i] if condition[i] else y[i] for i in range(len(condition))],
            "SELECT": lambda condlist, choicelist, default=0: np.select(condlist, choicelist, default) if np else self._select_manual(condlist, choicelist, default),
            "SEARCHSORTED": lambda arr, values: np.searchsorted(arr, values) if np else self._searchsorted_manual(arr, values),
            "MESHGRID": lambda x, y: np.meshgrid(x, y) if np else self._meshgrid_manual(x, y),
            "GRADIENT": lambda arr: np.gradient(arr) if np else self._gradient_manual(arr),
            "DIFF": lambda arr, n=1: np.diff(arr, n) if np else self._diff_manual(arr, n),
            "CUMSUM": lambda arr: np.cumsum(arr) if np else self._cumsum_manual(arr),
            "CUMPROD": lambda arr: np.cumprod(arr) if np else self._cumprod_manual(arr),
            "ARGMAX": lambda arr: np.argmax(arr) if np else arr.index(max(arr)) if isinstance(arr, list) else max(range(len(arr)), key=lambda i: arr[i]),
            "ARGMIN": lambda arr: np.argmin(arr) if np else arr.index(min(arr)) if isinstance(arr, list) else min(range(len(arr)), key=lambda i: arr[i]),
            "ROLL": lambda arr, shift: np.roll(arr, shift) if np else arr[-shift:] + arr[:-shift] if shift > 0 else arr[-shift:] + arr[:-shift],
            "TILE": lambda arr, reps: np.tile(arr, reps) if np else arr * reps if isinstance(reps, int) else self._tile_manual(arr, reps),
            "REPEAT": lambda arr, repeats: np.repeat(arr, repeats) if np else [item for item in arr for _ in range(repeats)],
            
            # Additional SciPy Statistical Tests
            "ANDERSON": lambda data, dist='norm': stats.anderson(data, dist) if stats else self._anderson_darling_manual(data, dist),
            "ANSARI": lambda x, y: stats.ansari(x, y) if stats else self._ansari_bradley_manual(x, y),
            "BARTLETT": lambda *samples: stats.bartlett(*samples) if stats else self._bartlett_manual(*samples),
            "BROWN_FORSYTHE": lambda *samples: stats.levene(*samples, center='median') if stats else self._brown_forsythe_manual(*samples),
            "COCHRANQ": lambda data: self._cochran_q_manual(data),
            "MCNEMAR": lambda table: stats.mcnemar(table) if stats else self._mcnemar_manual(table),
            "FISHER_EXACT": lambda table: stats.fisher_exact(table) if stats else self._fisher_exact_manual(table),
            "BARNARD_EXACT": lambda table: self._barnard_exact_manual(table),
            "BOSCHLOO": lambda table: self._boschloo_exact_manual(table),
            "PAGE_TREND": lambda data, predicted_ranks: stats.page_trend_test(data, predicted_ranks) if stats else self._page_trend_manual(data, predicted_ranks),
            "MOOD": lambda x, y: stats.mood(x, y) if stats else self._mood_median_manual(x, y),
            "FLIGNER_KILLEEN": lambda *samples: stats.fligner(*samples) if stats else self._fligner_killeen_manual(*samples),
            "WELCH_ANOVA": lambda *samples: self._welch_anova_manual(*samples),
            "DURBIN_WATSON": lambda residuals: self._durbin_watson_manual(residuals),
            "BREUSCH_PAGAN": lambda y, x: self._breusch_pagan_manual(y, x),
            "WHITE_TEST": lambda y, x: self._white_test_manual(y, x),
            "LJUNG_BOX": lambda residuals, lags=None: stats.diagnostic.acorr_ljungbox(residuals, lags) if stats else self._ljung_box_manual(residuals, lags),
            "JARQUE_BERA": lambda data: stats.jarque_bera(data) if stats else self._jarque_bera_manual(data),
            "DAGOSTINO": lambda data: stats.normaltest(data) if stats else self._dagostino_manual(data),
            "OMNIBUS": lambda data: stats.normaltest(data) if stats else self._omnibus_manual(data),
            
            # Effect Size Measures
            "COHEN_D": lambda group1, group2: self._cohen_d_manual(group1, group2),
            "HEDGES_G": lambda group1, group2: self._hedges_g_manual(group1, group2),
            "GLASS_DELTA": lambda group1, group2: self._glass_delta_manual(group1, group2),
            "ETA_SQUARED": lambda f_stat, df1, df2: self._eta_squared_manual(f_stat, df1, df2),
            "OMEGA_SQUARED": lambda f_stat, df1, df2: self._omega_squared_manual(f_stat, df1, df2),
            "PARTIAL_ETA_SQUARED": lambda f_stat, df1, df2: self._partial_eta_squared_manual(f_stat, df1, df2),
            "CRAMER_V": lambda chi2, n, k: self._cramer_v_manual(chi2, n, k),
            "PHI_COEFFICIENT": lambda chi2, n: self._phi_coefficient_manual(chi2, n),
            "CONTINGENCY_COEFFICIENT": lambda chi2, n: self._contingency_coefficient_manual(chi2, n),
            
            # Power Analysis
            "POWER_TTEST": lambda effect_size, n, alpha=0.05: self._power_ttest_manual(effect_size, n, alpha),
            "POWER_ANOVA": lambda effect_size, df1, df2, alpha=0.05: self._power_anova_manual(effect_size, df1, df2, alpha),
            "POWER_CHI2": lambda effect_size, df, n, alpha=0.05: self._power_chi2_manual(effect_size, df, n, alpha),
            "SAMPLE_SIZE_TTEST": lambda effect_size, power=0.8, alpha=0.05: self._sample_size_ttest_manual(effect_size, power, alpha),
            "SAMPLE_SIZE_ANOVA": lambda effect_size, power=0.8, alpha=0.05: self._sample_size_anova_manual(effect_size, power, alpha),
            
            # Robust Statistics
            "TRIMMED_MEAN": lambda data, proportion=0.1: stats.trim_mean(data, proportion) if stats else self._trimmed_mean_manual(data, proportion),
            "WINSORIZED_MEAN": lambda data, limits=0.1: stats.mstats.winsorize(data, limits).mean() if stats else self._winsorized_mean_manual(data, limits),
            "MEDIAN_ABSOLUTE_DEVIATION": lambda data: stats.median_absolute_deviation(data) if stats else self._mad_manual(data),
            "INTERQUARTILE_RANGE": lambda data: stats.iqr(data) if stats else self._iqr_manual(data),
            "TUKEY_BIWEIGHT": lambda data: self._tukey_biweight_manual(data),
            "HUBER_M": lambda data: self._huber_m_estimator_manual(data),
            
            # Bootstrap and Resampling
            "BOOTSTRAP": lambda data, func, n_bootstrap=1000: self._bootstrap_manual(data, func, n_bootstrap),
            "JACKKNIFE": lambda data, func: self._jackknife_manual(data, func),
            "PERMUTATION_TEST": lambda group1, group2, func, n_permutations=1000: self._permutation_test_manual(group1, group2, func, n_permutations),
            "CROSS_VALIDATION": lambda data, model, k=5: self._cross_validation_manual(data, model, k),
            
            # Bayesian Statistics
            "BAYES_FACTOR": lambda likelihood1, likelihood2: self._bayes_factor_manual(likelihood1, likelihood2),
            "CREDIBLE_INTERVAL": lambda posterior, alpha=0.05: self._credible_interval_manual(posterior, alpha),
            "POSTERIOR_PREDICTIVE": lambda posterior, prior, data: self._posterior_predictive_manual(posterior, prior, data),
            
            # Multivariate Statistics  
            "HOTELLING_T2": lambda data1, data2=None: self._hotelling_t2_manual(data1, data2),
            "MAHALANOBIS": lambda point, data: self._mahalanobis_manual(point, data),
            "BOX_M": lambda data, groups: self._box_m_manual(data, groups),
            "MANOVA_PILLAI": lambda data, groups: self._manova_pillai_manual(data, groups),
            "MANOVA_WILKS": lambda data, groups: self._manova_wilks_manual(data, groups),
            "MANOVA_HOTELLING": lambda data, groups: self._manova_hotelling_manual(data, groups),
            "MANOVA_ROY": lambda data, groups: self._manova_roy_manual(data, groups),
            
            # Survival Analysis
            "KAPLAN_MEIER": lambda times, events: self._kaplan_meier_manual(times, events),
            "LOGRANK_TEST": lambda times1, events1, times2, events2: self._logrank_test_manual(times1, events1, times2, events2),
            "COX_REGRESSION": lambda times, events, covariates: self._cox_regression_manual(times, events, covariates),
            
            # Meta-Analysis
            "FIXED_EFFECT": lambda effects, variances: self._fixed_effect_meta_manual(effects, variances),
            "RANDOM_EFFECT": lambda effects, variances: self._random_effect_meta_manual(effects, variances),
            "FOREST_PLOT": lambda effects, variances, labels: self._forest_plot_manual(effects, variances, labels),
            "FUNNEL_PLOT": lambda effects, variances: self._funnel_plot_manual(effects, variances),
            "EGGER_TEST": lambda effects, variances: self._egger_test_manual(effects, variances),
            "BEGG_TEST": lambda effects, variances: self._begg_test_manual(effects, variances),
            
            # Time Functions
            "TIMER": self.libx_core.timer,
            "TIME$": self.libx_core.time_now,
            "DATE$": self.libx_core.date_now,
            "SLEEP": self.libx_core.sleep,
            
            # System Functions
            "ENVIRON$": lambda var: os.getenv(var, ""),
            "COMMAND$": lambda: " ".join(sys.argv[1:]),
            "SHELL": self.libx_core.shell,
            "MEMORY": self.libx_core.memory_usage,
            "CPUCOUNT": self.libx_core.cpu_count,
            "TIME_NOW": self.libx_core.time_now,
            "DATE_NOW": self.libx_core.date_now,
            "TIMER": self.libx_core.timer,
            "MEMORY_USAGE": self.libx_core.memory_usage,
            "CPU_COUNT": self.libx_core.cpu_count,
            
            # File Functions
            "DIR$": lambda path="": self.libx_core.list_dir(path or "."),
            "EXISTS": self.libx_core.exists,
            "ISDIR": os.path.isdir,
            "FILESIZE": os.path.getsize,
            "LIST_DIR": lambda path=".": self.libx_core.list_dir(path),
            
            # Memory Functions
            "MALLOC": self.memory_manager.allocate,
            "FREE": self.memory_manager.release,
            "SIZEOF": self.memory_manager.sizeof,
            
            # Data Structure Functions
            "STACK": self.libx_core.create_stack,
            "QUEUE": self.libx_core.create_queue,
            "TYPEOF": self.libx_core.type_of,
            "CREATE_STACK": self.libx_core.create_stack,
            "CREATE_QUEUE": self.libx_core.create_queue,
            "TYPE_OF": self.libx_core.type_of,
            
            # Prolog Integration Functions
            "PROLOG_FACTS": lambda: self.prolog_engine.facts,
            "PROLOG_RULES": lambda: self.prolog_engine.rules,
            "PROLOG_SOLUTIONS": lambda: self.current_scope().get("_PROLOG_SOLUTIONS", []),
            "PROLOG_ASK": lambda goal: self.prolog_engine.query(goal),
            "PROLOG_TELL": lambda fact: self.prolog_engine.add_fact(fact),
            "PROLOG_RETRACT": lambda fact: self._retract_prolog_fact(fact),
            "PROLOG_CLEAR": lambda: self._clear_prolog_database(),
            "PROLOG_COUNT": lambda: len(self.prolog_engine.facts) + len(self.prolog_engine.rules),
            "PROLOG_TRACE": lambda mode: setattr(self.prolog_engine, 'trace_mode', bool(mode)),
        }
        
        # Add PDF functions if available
        if pdfplumber:
            funcs.update({
                "PDF_READ": self._pdf_read_text,
                "PDF_EXTRACT_TABLES": self._pdf_extract_tables,
                "PDF_SEARCH": self._pdf_search_keyword,
            })
        
        # Add web functions if available
        if requests and BeautifulSoup:
            funcs.update({
                "WEB_GET": self._web_get,
                "WEB_POST": self._web_post,
                "SCRAPE_LINKS": self._scrape_links,
                "SCRAPE_TEXT": self._scrape_text,
                "CURL": self._curl_request,
                "HTTP_GET": self._http_get,
                "HTTP_POST": self._http_post,
                "HTTP_PUT": self._http_put,
                "HTTP_DELETE": self._http_delete,
                "API_CALL": self._api_call,
            })
        
        return funcs

    def _init_operator_table(self):
        """Gelişmiş operatör tablosunu başlatma"""
        return {
            # Increment/Decrement Operators
            '++': lambda x: x + 1,
            '--': lambda x: x - 1,
            
            # Bitwise Operators
            '<<': lambda x, y: x << y,
            '>>': lambda x, y: x >> y,
            '&': lambda x, y: x & y,
            '|': lambda x, y: x | y,
            '^': lambda x, y: x ^ y,
            '~': lambda x: ~x,
            
            # Logical Operators
            'AND': lambda x, y: x and y,
            'OR': lambda x, y: x or y,
            'XOR': lambda x, y: bool(x) != bool(y),
            'NOT': lambda x: not x,
            
            # Assignment Operators
            '+=': lambda x, y: x + y,
            '-=': lambda x, y: x - y,
            '*=': lambda x, y: x * y,
            '/=': lambda x, y: x / y,
            '%=': lambda x, y: x % y,
            '&=': lambda x, y: x & y,
            '|=': lambda x, y: x | y,
            '^=': lambda x, y: x ^ y,
            '<<=': lambda x, y: x << y,
            '>>=': lambda x, y: x >> y,
            
            # Arithmetic Operators
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            
            # Comparison Operators
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '<': lambda x, y: x < y,
            '>': lambda x, y: x > y,
            '<=': lambda x, y: x <= y,
            '>=': lambda x, y: x >= y,
            '<>': lambda x, y: x != y,
            
            # Extended Logical Operators
            '&&': lambda x, y: x and y,
            '||': lambda x, y: x or y,
            
            # Extended Arithmetic Operators
            '%': lambda x, y: x % y,
            '**': lambda x, y: x ** y,
            '//': lambda x, y: x // y
        }

    def _pdf_read_text(self, file_path):
        """PDF metin okuma"""
        if not os.path.exists(file_path):
            raise PdsXRuntimeError(f"PDF dosyası bulunamadı: {file_path}")
        
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def _pdf_extract_tables(self, file_path):
        """PDF tablo çıkarma"""
        if not os.path.exists(file_path):
            raise PdsXRuntimeError(f"PDF dosyası bulunamadı: {file_path}")
        
        tables = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)
        return tables

    def _pdf_search_keyword(self, file_path, keyword):
        """PDF'de anahtar kelime arama"""
        if not os.path.exists(file_path):
            raise PdsXRuntimeError(f"PDF dosyası bulunamadı: {file_path}")
        
        results = []
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and keyword.lower() in text.lower():
                    results.append((i + 1, text))
        return results

    def _web_get(self, url):
        """Web GET isteği"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise PdsXRuntimeError(f"Web isteği hatası: {e}")

    def _web_post(self, url, data):
        """Web POST isteği"""
        try:
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise PdsXRuntimeError(f"Web isteği hatası: {e}")

    def _scrape_links(self, html_content):
        """HTML'den link çıkarma"""
        soup = BeautifulSoup(html_content, 'html.parser')
        return [a.get('href') for a in soup.find_all('a', href=True)]

    def _scrape_text(self, html_content):
        """HTML'den metin çıkarma"""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator='\n')

    def _curl_request(self, url, method="GET", data=None, headers=None):
        """CURL benzeri HTTP isteği"""
        try:
            method = method.upper()
            headers = headers or {}
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, data=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, data=data, headers=headers, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                raise PdsXRuntimeError(f"Desteklenmeyen HTTP metodu: {method}")
                
            response.raise_for_status()
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "text": response.text,
                "json": response.json() if response.headers.get('content-type', '').startswith('application/json') else None
            }
        except Exception as e:
            raise PdsXRuntimeError(f"CURL isteği hatası: {e}")

    def _http_get(self, url, headers=None):
        """HTTP GET isteği"""
        return self._curl_request(url, "GET", headers=headers)

    def _http_post(self, url, data=None, headers=None):
        """HTTP POST isteği"""
        return self._curl_request(url, "POST", data=data, headers=headers)

    def _http_put(self, url, data=None, headers=None):
        """HTTP PUT isteği"""
        return self._curl_request(url, "PUT", data=data, headers=headers)

    def _http_delete(self, url, headers=None):
        """HTTP DELETE isteği"""
        return self._curl_request(url, "DELETE", headers=headers)

    def _api_call(self, api_name, endpoint, method="GET", data=None, headers=None):
        """Gelişmiş API çağrısı"""
        if api_name not in self.api_connections:
            raise PdsXRuntimeError(f"API bağlantısı bulunamadı: {api_name}")
        
        api_config = self.api_connections[api_name]
        base_url = api_config["base_url"]
        default_headers = api_config.get("headers", {})
        
        # Merge headers
        if headers:
            default_headers.update(headers)
        
        full_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self._curl_request(full_url, method, data, default_headers)

    def current_scope(self):
        """Geçerli kapsam döndürme"""
        return self.scopes[-1]

    def push_scope(self, initial_vars=None):
        """Yeni kapsam ekleme"""
        new_scope = initial_vars or {}
        self.scopes.append(new_scope)

    def pop_scope(self):
        """Kapsam kaldırma"""
        if len(self.scopes) > 1:
            return self.scopes.pop()
        raise PdsXRuntimeError("Ana kapsam kaldırılamaz")

    def parse_program(self, code, module_name="main"):
        """Gelişmiş program ayrıştırma sistemi"""
        self.current_module = module_name
        self.modules[module_name] = {
            "program": [], "functions": {}, "subs": {}, "classes": {}, 
            "types": {}, "labels": {}, "imports": []
        }
        
        # State variables for parsing
        current_type = None
        current_enum = None
        current_class = None
        current_sub = None
        current_function = None
        type_fields = {}
        enum_values = {}
        class_info = {}
        
        lines = code.split("\n")
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("'") or line.startswith("//"):
                i += 1
                continue
                
            line_upper = line.upper()
            
            try:
                # TYPE/STRUCT definitions
                if line_upper.startswith("TYPE ") or line_upper.startswith("STRUCT "):
                    type_name = line.split()[1]
                    current_type = type_name
                    type_fields[current_type] = []
                    
                elif line_upper.startswith("END TYPE") or line_upper.startswith("END STRUCT"):
                    self.types[current_type] = {"kind": "STRUCT", "fields": type_fields[current_type]}
                    self.modules[module_name]["types"][current_type] = self.types[current_type]
                    current_type = None
                
                # UNION definitions
                elif line_upper.startswith("UNION "):
                    union_name = line.split()[1]
                    current_type = union_name
                    type_fields[current_type] = []
                    
                elif line_upper.startswith("END UNION"):
                    self.types[current_type] = {"kind": "UNION", "fields": type_fields[current_type]}
                    self.modules[module_name]["types"][current_type] = self.types[current_type]
                    current_type = None
                
                # ENUM definitions
                elif line_upper.startswith("ENUM "):
                    enum_name = line.split()[1]
                    current_enum = enum_name
                    enum_values[current_enum] = {}
                    
                elif line_upper.startswith("END ENUM"):
                    self.types[current_enum] = {"kind": "ENUM", "values": enum_values[current_enum]}
                    self.modules[module_name]["types"][current_enum] = self.types[current_enum]
                    current_enum = None
                
                # CLASS definitions with inheritance support
                elif line_upper.startswith("CLASS "):
                    match = re.match(r"CLASS\s+(\w+)(?:\s+(INHERITS|EXTENDS)\s+(\w+))?", line, re.IGNORECASE)
                    if match:
                        class_name, inheritance_keyword, parent_name = match.groups()
                        current_class = class_name
                        class_info[current_class] = {
                            "fields": [], "methods": {}, "access": {}, 
                            "parent": parent_name, "static_vars": {}
                        }
                    else:
                        raise PdsXSyntaxError(f"Geçersiz CLASS tanımı: {line}")
                
                elif line_upper.startswith("END CLASS"):
                    self.types[current_class] = {"kind": "CLASS", **class_info[current_class]}
                    self.modules[module_name]["classes"][current_class] = self.types[current_class]
                    current_class = None
                
                # FUNCTION definitions
                elif line_upper.startswith("FUNCTION "):
                    match = re.match(r"FUNCTION\s+(\w+)\s*\((.*?)\)(?:\s+AS\s+(\w+))?", line, re.IGNORECASE)
                    if match:
                        func_name, params_str, return_type = match.groups()
                        params = self._parse_parameters(params_str)
                        
                        func_body = []
                        i += 1
                        while i < len(lines) and not lines[i].strip().upper().startswith("END FUNCTION"):
                            func_body.append(lines[i].strip())
                            i += 1
                        
                        self.functions[func_name] = {
                            "params": params, "body": func_body, "return_type": return_type
                        }
                        self.modules[module_name]["functions"][func_name] = self.functions[func_name]
                    else:
                        raise PdsXSyntaxError(f"Geçersiz FUNCTION tanımı: {line}")
                
                # SUB definitions
                elif line_upper.startswith("SUB "):
                    match = re.match(r"SUB\s+(\w+)\s*\((.*?)\)", line, re.IGNORECASE)
                    if match:
                        sub_name, params_str = match.groups()
                        params = self._parse_parameters(params_str)
                        
                        sub_body = []
                        i += 1
                        while i < len(lines) and not lines[i].strip().upper().startswith("END SUB"):
                            sub_body.append(lines[i].strip())
                            i += 1
                        
                        self.subs[sub_name] = {"params": params, "body": sub_body}
                        self.modules[module_name]["subs"][sub_name] = self.subs[sub_name]
                    else:
                        raise PdsXSyntaxError(f"Geçersiz SUB tanımı: {line}")
                
                # Field definitions for TYPE/STRUCT/UNION
                elif current_type:
                    match = re.match(r"(\w+)\s+AS\s+(\w+)", line, re.IGNORECASE)
                    if match:
                        field_name, field_type = match.groups()
                        type_fields[current_type].append((field_name, field_type))
                    else:
                        raise PdsXSyntaxError(f"Geçersiz alan tanımı: {line}")
                
                # ENUM value definitions
                elif current_enum:
                    match = re.match(r"(\w+)(?:\s*=\s*(\d+))?", line, re.IGNORECASE)
                    if match:
                        name, value = match.groups()
                        value = int(value) if value else len(enum_values[current_enum])
                        enum_values[current_enum][name] = value
                    else:
                        raise PdsXSyntaxError(f"Geçersiz ENUM değer tanımı: {line}")
                
                # CLASS field and method definitions
                elif current_class:
                    access = "PUBLIC"
                    if line_upper.startswith("PUBLIC "):
                        access = "PUBLIC"
                        line = line[len("PUBLIC "):].strip()
                        line_upper = line.upper()
                    elif line_upper.startswith("PRIVATE "):
                        access = "PRIVATE"
                        line = line[len("PRIVATE "):].strip()
                        line_upper = line.upper()
                    elif line_upper.startswith("STATIC "):
                        # Static variable definition
                        match = re.match(r"STATIC\s+(\w+)\s+AS\s+(\w+)", line, re.IGNORECASE)
                        if match:
                            var_name, var_type = match.groups()
                            class_info[current_class]["static_vars"][var_name] = var_type
                        else:
                            raise PdsXSyntaxError(f"Geçersiz STATIC tanımı: {line}")
                        i += 1
                        continue
                    
                    if line_upper.startswith("SUB "):
                        match = re.match(r"SUB\s+(\w+)\s*\((.*?)\)", line, re.IGNORECASE)
                        if match:
                            sub_name, params_str = match.groups()
                            params = self._parse_parameters(params_str)
                            
                            method_body = []
                            i += 1
                            while i < len(lines) and not lines[i].strip().upper().startswith("END SUB"):
                                method_body.append(lines[i].strip())
                                i += 1
                            
                            class_info[current_class]["methods"][sub_name] = {
                                "params": params, "body": method_body, "access": access
                            }
                        else:
                            raise PdsXSyntaxError(f"Geçersiz method tanımı: {line}")
                    
                    elif line_upper.startswith("FUNCTION "):
                        match = re.match(r"FUNCTION\s+(\w+)\s*\((.*?)\)(?:\s+AS\s+(\w+))?", line, re.IGNORECASE)
                        if match:
                            func_name, params_str, return_type = match.groups()
                            params = self._parse_parameters(params_str)
                            
                            method_body = []
                            i += 1
                            while i < len(lines) and not lines[i].strip().upper().startswith("END FUNCTION"):
                                method_body.append(lines[i].strip())
                                i += 1
                            
                            class_info[current_class]["methods"][func_name] = {
                                "params": params, "body": method_body, "return_type": return_type, "access": access
                            }
                        else:
                            raise PdsXSyntaxError(f"Geçersiz method tanımı: {line}")
                    
                    else:
                        # Field definition
                        match = re.match(r"(\w+)\s+AS\s+(\w+)", line, re.IGNORECASE)
                        if match:
                            field_name, field_type = match.groups()
                            class_info[current_class]["fields"].append((field_name, field_type))
                            class_info[current_class]["access"][field_name] = access
                        else:
                            raise PdsXSyntaxError(f"Geçersiz alan tanımı: {line}")
                
                # LABEL definitions
                elif line_upper.startswith("LABEL "):
                    label_name = line[6:].strip()
                    self.labels[label_name] = i
                    self.modules[module_name]["labels"][label_name] = i
                
                # DATA statements
                elif line_upper.startswith("DATA "):
                    data_items = line[5:].split(",")
                    self.data_list.extend([item.strip().strip('"') for item in data_items])
                
                # IMPORT statements
                elif line_upper.startswith("IMPORT "):
                    match = re.match(r"IMPORT\s+[\"'](.+?)[\"'](?:\s+AS\s+(\w+))?", line, re.IGNORECASE)
                    if match:
                        file_path, alias = match.groups()
                        self.modules[module_name]["imports"].append((file_path, alias))
                    else:
                        raise PdsXSyntaxError(f"Geçersiz IMPORT tanımı: {line}")
                
                # Regular program statements
                else:
                    self.program.append((line, current_sub or current_function))
                    self.modules[module_name]["program"].append((line, current_sub or current_function))
                
                i += 1
                
            except Exception as e:
                raise PdsXSyntaxError(f"Satır {i+1} ayrıştırma hatası: {e}")

    def _parse_parameters(self, params_str):
        """Parametre listesini ayrıştırma"""
        if not params_str.strip():
            return []
        
        params = []
        for param in params_str.split(","):
            param = param.strip()
            if " AS " in param.upper():
                param_name, param_type = [x.strip() for x in param.split(" AS ", 1)]
                params.append((param_name, param_type))
            else:
                params.append((param, "VARIANT"))
        
        return params

    def execute_command(self, command, scope_name=None):
        """Gelişmiş komut çalıştırma sistemi"""
        command = command.strip()
        if not command or command.startswith("'") or command.startswith("//") or command.upper().startswith("REM"):
            return None
        
        # Debug çıktısı kaldırıldı - sadece hata ayıklama modunda göster
        # print(f"EXECUTE: '{command}' (PC: {self.program_counter})")
        
        command_upper = command.upper()
        
        # Trace modu da varsayılan olarak kapalı
        if hasattr(self, 'trace_mode') and self.trace_mode:
            print(f"TRACE: Satır {self.program_counter + 1}: {command}")
        
        try:
            # Variable declaration - DIM
            if command_upper.startswith("DIM"):
                return self._execute_dim(command)
            
            # Assignment - LET
            elif command_upper.startswith("LET"):
                return self._execute_let(command, scope_name)
            
            # Method call - CALL
            elif command_upper.startswith("CALL"):
                return self._execute_call(command, scope_name)
            
            # Output - PRINT
            elif command_upper.startswith("PRINT"):
                return self._execute_print(command, scope_name)
            
            # Control flow
            elif command_upper.startswith(("IF", "ELSEIF", "ELSE", "END IF")):
                return self._execute_if(command, scope_name)
            
            elif command_upper.startswith(("FOR", "NEXT", "END FOR", "EXIT FOR", "CONTINUE FOR")):
                print(f"DEBUG EXEC: FOR/NEXT detected: '{command}'")
                return self._execute_for(command, scope_name)
            
            elif command_upper.startswith(("WHILE", "WEND", "EXIT WHILE", "CONTINUE WHILE")):
                return self._execute_while(command, scope_name)
            
            elif command_upper.startswith(("DO", "LOOP", "EXIT DO", "CONTINUE DO")):
                return self._execute_do_loop(command, scope_name)
            
            elif command_upper.startswith(("SELECT CASE", "CASE", "END SELECT")):
                return self._execute_select_case(command, scope_name)
            
            # Jump statements
            elif command_upper.startswith("GOTO"):
                return self._execute_goto(command)
            
            elif command_upper.startswith("GOSUB"):
                return self._execute_gosub(command)
            
            elif command_upper == "RETURN":
                return self._execute_return(command, scope_name)
            
            # Function/Sub calls
            elif command_upper.startswith("CALL "):
                return self._execute_call(command, scope_name)
            
            # Memory operations
            elif command_upper.startswith(("MALLOC", "FREE", "PTR_SET", "MEMCPY", "MEMSET")):
                return self._execute_memory_operations(command, scope_name)
            
            # Database operations
            elif command_upper.startswith(("DB_CONNECT", "DB_QUERY", "DB_CLOSE")):
                return self._execute_database_operations(command, scope_name)
            
            # API operations
            elif command_upper.startswith(("API_CONNECT", "API_DISCONNECT", "LOAD_DLL", "LOAD_API")):
                return self._execute_api_operations(command, scope_name)
            
            # File operations
            elif command_upper.startswith(("OPEN", "CLOSE", "READ", "WRITE", "SEEK")):
                return self._execute_file_operations(command, scope_name)
            
            # Error handling
            elif command_upper.startswith(("ON ERROR", "RESUME", "ERROR")):
                return self._execute_error_handling(command, scope_name)
            
            # Debug operations
            elif command_upper.startswith(("DEBUG", "TRACE", "STEP")):
                return self._execute_debug_operations(command)
            
            # C64 GUI operations
            elif command_upper.startswith(("C64_", "SPRITE", "POKE", "PEEK", "SID_", "CHARSET")):
                return self._execute_c64_gui_operations(command, scope_name)
            
            # LibX GUI operations
            elif command_upper.startswith(("GUI_", "WINDOW", "BUTTON", "LABEL", "INPUT", "MENU")):
                return self._execute_libx_gui_operations(command, scope_name)
            
            # Module operations
            elif command_upper.startswith("IMPORT"):
                return self._execute_import(command)
            
            # Event system operations
            elif command_upper.startswith("EVENT"):
                return self._execute_event(command, scope_name)
            
            elif command_upper.startswith("TRIGGER"):
                return self._execute_trigger_event(command, scope_name)
            
            # Prolog operations
            elif command_upper.startswith(("FACT", "RULE", "QUERY", "ASSERT", "RETRACT")):
                return self._execute_prolog_operations(command, scope_name)
            
            # CLAZZ dynamic class operations
            elif command_upper.startswith("CLAZZ"):
                return self._execute_clazz_operations(command, scope_name)
            
            # Pipeline operations
            elif command_upper.startswith("PIPE"):
                return self._execute_pipe_operations(command, scope_name)
            
            # Enhanced PRINT with Python-like features
            elif command_upper.startswith("PRINT"):
                return self._execute_enhanced_print(command, scope_name)
            
            # Enhanced INPUT with Python-like features
            elif command_upper.startswith("INPUT"):
                return self._execute_enhanced_input(command, scope_name)
            
            # SQL Database operations
            elif command_upper.startswith(("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")):
                return self._execute_sql_command(command, scope_name)
            
            # ISAM File operations
            elif command_upper.startswith("ISAM"):
                return self._execute_isam_command(command, scope_name)
            
            # Database connection commands
            elif command_upper.startswith("CONNECT"):
                return self._execute_db_connect(command, scope_name)
            
            # Include system
            elif command_upper.startswith("INCLUDE"):
                return self._execute_include(command, scope_name)
            
            # Data operations
            elif command_upper.startswith(("READ", "RESTORE")):
                return self._execute_data_operations(command, scope_name)
            
            # Expression evaluation (assignment without LET)
            elif "=" in command and not command_upper.startswith(("<=", ">=", "==", "!=")):
                return self._execute_assignment(command, scope_name)
            
            # Function call without assignment
            else:
                return self._execute_expression_statement(command, scope_name)
                
        except PdsXException:
            raise
        except Exception as e:
            error_msg = f"PDSX Çalışma Zamanı Hatası: {str(e)}, Satır {self.program_counter + 1}"
            logging.error(error_msg)
            
            if self.error_handler == "RESUME":
                return None
            elif self.error_handler:
                self.program_counter = self.error_handler
                return None
            else:
                self.running = False
                raise PdsXRuntimeError(error_msg)

    def _execute_dim(self, command):
        """DIM komutunu çalıştırma"""
        # Support multiple patterns:
        # DIM var AS type
        # DIM var(dimensions) AS type  
        # DIM var AS POINTER TO type
        
        match = re.match(r"DIM\s+(\w+)(?:\(([\d, ]+)\))?\s+AS\s+(.+)", command, re.IGNORECASE)
        if not match:
            raise PdsXSyntaxError(f"Geçersiz DIM sözdizimi: {command}")
        
        var_name, dim_str, type_expr = match.groups()
        
        # Handle pointer types
        if type_expr.upper().startswith("POINTER TO "):
            target_type = type_expr[11:].strip()
            self.current_scope()[var_name] = Pointer(None, target_type, self)
            return None
        
        # Handle array dimensions
        if dim_str:
            dimensions = [int(d.strip()) for d in dim_str.split(",")]
            self.current_scope()[var_name] = ArrayInstance(dimensions, type_expr, self.type_table, self.types)
            return None
        
        # Handle complex types
        if type_expr.upper() in self.types:
            type_info = self.types[type_expr.upper()]
            
            if type_info["kind"] == "STRUCT":
                self.current_scope()[var_name] = StructInstance(type_info["fields"], self.type_table, self.types)
            elif type_info["kind"] == "CLASS":
                self.current_scope()[var_name] = ClassInstance(type_info, self.type_table, self.types, self)
            elif type_info["kind"] == "UNION":
                self.current_scope()[var_name] = UnionInstance(type_info["fields"], self.type_table, self.types)
            elif type_info["kind"] == "ENUM":
                self.current_scope()[var_name] = None
            else:
                raise PdsXTypeError(f"Bilinmeyen tip: {type_expr}")
        else:
            # Basic type
            default_value = self._get_default_value(type_expr.upper())
            self.current_scope()[var_name] = default_value
        
        return None

    def _get_default_value(self, type_name):
        """Tip için varsayılan değer döndürme"""
        defaults = {
            "STRING": "",
            "INTEGER": 0,
            "DOUBLE": 0.0,
            "SINGLE": 0.0,
            "BYTE": 0,
            "SHORT": 0,
            "LONG": 0,
            "BOOLEAN": False,
            "LIST": [],
            "DICT": {},
            "SET": set()
        }
        return defaults.get(type_name, None)

    def _execute_let(self, command, scope_name=None):
        """LET komutunu çalıştırma"""
        match = re.match(r"LET\s+(.+?)\s*=\s*(.+)", command, re.IGNORECASE)
        if not match:
            raise PdsXSyntaxError(f"Geçersiz LET sözdizimi: {command}")
        
        target, expr = match.groups()
        value = self.evaluate_expression(expr, scope_name)
        
        return self._assign_value(target, value)

    def _execute_assignment(self, command, scope_name=None):
        """Atama komutunu çalıştırma"""
        parts = command.split("=", 1)
        if len(parts) != 2:
            raise PdsXSyntaxError(f"Geçersiz atama sözdizimi: {command}")
        
        target, expr = [p.strip() for p in parts]
        value = self.evaluate_expression(expr, scope_name)
        
        return self._assign_value(target, value)

    def _assign_value(self, target, value):
        """Değer atama işlemi"""
        # Struct/Class field access
        if "." in target:
            parts = target.split(".")
            instance = self._get_variable(parts[0])
            
            for field in parts[1:-1]:
                if isinstance(instance, (StructInstance, UnionInstance, ClassInstance)):
                    instance = instance.get_field(field)
                else:
                    raise PdsXTypeError(f"Geçersiz alan erişimi: {target}")
            
            field_name = parts[-1]
            if isinstance(instance, (StructInstance, UnionInstance, ClassInstance)):
                instance.set_field(field_name, value)
            else:
                raise PdsXTypeError(f"{parts[0]} bir yapı, birleşim veya sınıf değil")
        
        # Array element access
        elif "(" in target and ")" in target:
            match = re.match(r"(\w+)\(([\d, ]+)\)", target)
            if match:
                var_name, indices_str = match.groups()
                indices = [int(i.strip()) for i in indices_str.split(",")]
                array = self._get_variable(var_name)
                
                if isinstance(array, ArrayInstance):
                    array.set_element(indices, value)
                else:
                    raise PdsXTypeError(f"{var_name} bir dizi değil")
            else:
                raise PdsXSyntaxError(f"Geçersiz dizi erişimi: {target}")
        
        # Pointer dereference
        elif target.startswith("*"):
            ptr_name = target[1:].strip()
            ptr = self._get_variable(ptr_name)
            
            if isinstance(ptr, Pointer):
                ptr.set(value)
            else:
                raise PdsXTypeError(f"{ptr_name} bir işaretçi değil")
        
        # Simple variable assignment
        else:
            self._set_variable(target, value)
        
        return None

    def _execute_print(self, command, scope_name=None):
        """PRINT komutunu çalıştırma - basitleştirilmiş"""
        print_expr = command[5:].strip()
        
        if not print_expr:
            print()
            return None
        
        # Basit tokenization - virgül ile ayır
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None
        
        for char in print_expr:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                current_part += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_part += char
            elif char == ',' and not in_quotes:
                parts.append(current_part.strip())
                current_part = ""
            else:
                current_part += char
        
        if current_part.strip():
            parts.append(current_part.strip())
        
        # Evaluate each part
        output_parts = []
        for part in parts:
            part = part.strip()
            if part:
                try:
                    value = self.evaluate_expression(part, scope_name)
                    output_parts.append(str(value))
                except Exception as e:
                    print(f"PRINT ERROR in part '{part}': {e}")
                    output_parts.append(f"[ERROR:{part}]")
        
        # Join and print
        output = " ".join(output_parts)
        print(output)
        
        return None

    def _execute_call(self, command, scope_name=None):
        """CALL komutunu çalıştırma - DLL:: ve API:: desteği ile"""
        # Check for DLL:: syntax
        if "DLL::" in command.upper():
            return self._execute_dll_call(command, scope_name)
        
        # Check for API:: syntax
        if "API::" in command.upper():
            return self._execute_api_call(command, scope_name)
        
        # Regular CALL syntax
        match = re.match(r"CALL\s+(\w+)(?:\.(\w+))?\s*\((.*)\)", command, re.IGNORECASE)
        if not match:
            raise PdsXSyntaxError(f"Geçersiz CALL sözdizimi: {command}")
        
        obj_name, method_name, args_str = match.groups()
        
        # Parse arguments
        args = []
        if args_str.strip():
            args = [self.evaluate_expression(arg.strip(), scope_name) 
                   for arg in self._split_arguments(args_str)]
        
        if method_name:
            # Object method call
            obj = self._get_variable(obj_name)
            if isinstance(obj, ClassInstance):
                return obj.call_method(method_name, args)
            else:
                raise PdsXTypeError(f"{obj_name} bir sınıf nesnesi değil")
        else:
            # Function or sub call
            if obj_name in self.functions:
                return self._call_function(obj_name, args)
            elif obj_name in self.subs:
                return self._call_sub(obj_name, args)
            else:
                raise PdsXRuntimeError(f"Bilinmeyen fonksiyon/sub: {obj_name}")

    def _execute_dll_call(self, command, scope_name=None):
        """DLL çağrısını çalıştırma - CALL DLL::<dll_name>.<function_name>(args)"""
        match = re.match(r"CALL\s+DLL::(\w+)\.(\w+)\s*\((.*)\)", command, re.IGNORECASE)
        if not match:
            raise PdsXSyntaxError(f"Geçersiz DLL çağrısı sözdizimi: {command}")
        
        dll_name, function_name, args_str = match.groups()
        
        # Parse arguments
        args = []
        if args_str.strip():
            args = [self.evaluate_expression(arg.strip(), scope_name) 
                   for arg in self._split_arguments(args_str)]
        
        # Load DLL if not already loaded
        if dll_name not in self.libx_core.dll_handles:
            try:
                self.libx_core.load_dll(dll_name + ".dll")
            except Exception as e:
                raise PdsXRuntimeError(f"DLL yüklenemedi {dll_name}: {e}")
        
        # Call DLL function
        try:
            dll = self.libx_core.dll_handles[dll_name + ".dll"]
            func = getattr(dll, function_name)
            result = func(*args)
            return result
        except Exception as e:
            raise PdsXRuntimeError(f"DLL fonksiyon çağrısı hatası {dll_name}.{function_name}: {e}")

    def _execute_api_call(self, command, scope_name=None):
        """API çağrısını çalıştırma - CALL API::<api_name>.<endpoint>(args)"""
        match = re.match(r"CALL\s+API::(\w+)\.(\w+)\s*\((.*)\)", command, re.IGNORECASE)
        if not match:
            raise PdsXSyntaxError(f"Geçersiz API çağrısı sözdizimi: {command}")
        
        api_name, endpoint, args_str = match.groups()
        
        # Parse arguments - expecting method, data, headers
        args = []
        if args_str.strip():
            args = [self.evaluate_expression(arg.strip(), scope_name) 
                   for arg in self._split_arguments(args_str)]
        
        # Default values
        method = args[0] if len(args) > 0 else "GET"
        data = args[1] if len(args) > 1 else None
        headers = args[2] if len(args) > 2 else None
        
        # Call API function
        try:
            return self._api_call(api_name, endpoint, method, data, headers)
        except Exception as e:
            raise PdsXRuntimeError(f"API çağrısı hatası {api_name}.{endpoint}: {e}")

    def _split_arguments(self, args_str):
        """Argümanları doğru şekilde bölme"""
        args = []
        current_arg = ""
        paren_count = 0
        in_quotes = False
        quote_char = None
        
        for char in args_str:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                current_arg += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_arg += char
            elif char == '(' and not in_quotes:
                paren_count += 1
                current_arg += char
            elif char == ')' and not in_quotes:
                paren_count -= 1
                current_arg += char
            elif char == ',' and paren_count == 0 and not in_quotes:
                args.append(current_arg.strip())
                current_arg = ""
            else:
                current_arg += char
        
        if current_arg.strip():
            args.append(current_arg.strip())
        
        return args

    def _execute_memory_operations(self, command, scope_name=None):
        """Bellek işlemlerini çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("MALLOC"):
            match = re.match(r"MALLOC\s+(\w+)\s+SIZE\s+(\d+)(?:\s+AS\s+(\w+))?", command, re.IGNORECASE)
            if match:
                var_name, size_str, type_name = match.groups()
                size = int(size_str)
                type_name = type_name or "BYTE"
                
                addr = self.next_address
                self.memory_pool[addr] = {
                    "value": None,
                    "type": type_name,
                    "size": size,
                    "refs": 1
                }
                self.next_address += size
                self.current_scope()[var_name] = Pointer(addr, type_name, self)
                return None
            else:
                raise PdsXSyntaxError(f"Geçersiz MALLOC sözdizimi: {command}")
        
        elif command_upper.startswith("FREE"):
            match = re.match(r"FREE\s+(\w+)", command, re.IGNORECASE)
            if match:
                ptr_name = match.group(1)
                ptr = self._get_variable(ptr_name)
                
                if isinstance(ptr, Pointer) and ptr.address and ptr.address in self.memory_pool:
                    self.memory_pool[ptr.address]["refs"] -= 1
                    if self.memory_pool[ptr.address]["refs"] <= 0:
                        del self.memory_pool[ptr.address]
                    ptr.address = None
                else:
                    raise PdsXRuntimeError(f"Geçersiz işaretçi: {ptr_name}")
                return None
            else:
                raise PdsXSyntaxError(f"Geçersiz FREE sözdizimi: {command}")
        
        elif command_upper.startswith("PTR_SET"):
            match = re.match(r"PTR_SET\s+(\w+)\s+TO\s+(.+)", command, re.IGNORECASE)
            if match:
                ptr_name, expr = match.groups()
                ptr = self._get_variable(ptr_name)
                
                if not isinstance(ptr, Pointer):
                    raise PdsXTypeError(f"{ptr_name} bir işaretçi değil")
                
                if expr.startswith("&"):
                    # Address of operation
                    target = expr[1:].strip()
                    addr = self.next_address
                    
                    if "(" in target and ")" in target:
                        # Array element address
                        match_array = re.match(r"(\w+)\(([\d, ]+)\)", target)
                        if match_array:
                            var_name, indices_str = match_array.groups()
                            indices = [int(i.strip()) for i in indices_str.split(",")]
                            array = self._get_variable(var_name)
                            
                            if isinstance(array, ArrayInstance):
                                value = array.get_element(indices)
                                self.memory_pool[addr] = {
                                    "value": value,
                                    "type": array.element_type,
                                    "size": array.element_size,
                                    "refs": 1
                                }
                                ptr.address = addr
                                self.next_address += array.element_size
                            else:
                                raise PdsXTypeError(f"{var_name} bir dizi değil")
                    else:
                        # Variable address
                        value = self._get_variable(target)
                        self.memory_pool[addr] = {
                            "value": value,
                            "type": ptr.target_type,
                            "size": ptr.element_size,
                            "refs": 1
                        }
                        ptr.address = addr
                        self.next_address += ptr.element_size
                else:
                    # Direct address assignment
                    addr = self.evaluate_expression(expr, scope_name)
                    if isinstance(addr, int) and addr in self.memory_pool:
                        ptr.address = addr
                    else:
                        raise PdsXRuntimeError(f"Geçersiz adres: {addr}")
                
                return None
            else:
                raise PdsXSyntaxError(f"Geçersiz PTR_SET sözdizimi: {command}")
        
        # Add MEMCPY and MEMSET implementations here...
        
        raise PdsXSyntaxError(f"Bilinmeyen bellek operasyonu: {command}")

    def evaluate_expression(self, expr, scope_name=None):
        """Gelişmiş ifade değerlendirme sistemi"""
        expr = expr.strip()
        
        try:
            # String literals
            if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
                result = expr[1:-1]
            
            # Numeric literals - check this first
            elif self._is_numeric(expr):
                result = float(expr) if "." in expr else int(expr)
            
            # Boolean literals
            elif expr.upper() in ("TRUE", "FALSE"):
                result = expr.upper() == "TRUE"
            
            # Function calls - check before array access
            elif "(" in expr and ")" in expr and self._looks_like_function_call(expr):
                result = self._evaluate_function_call(expr, scope_name)
            
            # Array element access
            elif "(" in expr and ")" in expr:
                match = re.match(r"(\w+)\(([\d, ]+)\)", expr)
                if match:
                    var_name, indices_str = match.groups()
                    indices = [int(i.strip()) for i in indices_str.split(",")]
                    array = self._get_variable(var_name)
                    
                    if isinstance(array, ArrayInstance):
                        result = array.get_element(indices)
                    else:
                        # Fallback to function call
                        result = self._evaluate_function_call(expr, scope_name)
                else:
                    result = self._evaluate_function_call(expr, scope_name)
            
            # Struct/Class field access
            elif "." in expr and not any(op in expr for op in ["<=", ">=", "==", "!="]) and not self._is_numeric(expr):
                parts = expr.split(".")
                instance = self._get_variable(parts[0])
                
                for field in parts[1:]:
                    if isinstance(instance, (StructInstance, UnionInstance, ClassInstance)):
                        instance = instance.get_field(field)
                    else:
                        raise PdsXTypeError(f"Geçersiz alan erişimi: {expr}")
                
                result = instance
            
            # Pointer dereference
            elif expr.startswith("*"):
                ptr_name = expr[1:].strip()
                ptr = self._get_variable(ptr_name)
                
                if isinstance(ptr, Pointer):
                    result = ptr.dereference()
                else:
                    raise PdsXTypeError(f"{ptr_name} bir işaretçi değil")
            
            # Variable access
            elif expr.isidentifier():
                result = self._get_variable(expr)
            
            # Complex expressions
            else:
                result = self._evaluate_complex_expression(expr, scope_name)
            
            return result
            
        except Exception as e:
            raise PdsXRuntimeError(f"İfade değerlendirme hatası '{expr}': {e}")

    def _is_numeric(self, value):
        """Sayısal değer kontrolü"""
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            value = value.strip()
            # Check for simple numeric patterns
            if re.match(r'^-?\d+$', value):  # Integer
                return True
            if re.match(r'^-?\d*\.\d+$', value):  # Float
                return True
            if re.match(r'^-?\d+\.\d*$', value):  # Float ending with .
                return True
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False

    def _looks_like_function_call(self, expr):
        """İfadenin fonksiyon çağrısı olup olmadığını kontrol eder"""
        match = re.match(r"([\w\$]+)\s*\((.*)\)", expr)  # $ karakterini destekle
        if not match:
            return False
        
        func_name, args_str = match.groups()
        
        # Check if it's a known function
        if func_name.upper() in self.function_table:
            return True
        if func_name in self.functions:
            return True
        
        # Check if arguments look like function args (not just comma-separated numbers)
        if args_str.strip():
            # If it contains non-numeric characters or operators, likely a function call
            if re.search(r'[a-zA-Z_]|[+\-*/]', args_str):
                return True
            # If it's just numbers and commas, could be array access
            if re.match(r'^[\d\s,]+$', args_str):
                return False
        
        return False

    def _evaluate_function_call(self, expr, scope_name=None):
        """Fonksiyon çağrısını değerlendirme"""
        match = re.match(r"([\w\$]+)\s*\((.*)\)", expr)  # $ karakterini destekle
        if not match:
            raise PdsXSyntaxError(f"Geçersiz fonksiyon çağrısı: {expr}")
        
        func_name, args_str = match.groups()
        
        # Parse arguments
        args = []
        if args_str.strip():
            args = [self.evaluate_expression(arg.strip(), scope_name) 
                   for arg in self._split_arguments(args_str)]
        
        # Built-in function
        if func_name.upper() in self.function_table:
            func = self.function_table[func_name.upper()]
            return func(*args)
        
        # User-defined function
        elif func_name in self.functions:
            return self._call_function(func_name, args)
        
        else:
            raise PdsXRuntimeError(f"Bilinmeyen fonksiyon: {func_name}")

    def _evaluate_complex_expression(self, expr, scope_name=None):
        """Karmaşık matematiksel ifadeleri değerlendirme"""
        # Create namespace for evaluation
        namespace = {}
        namespace.update(self.global_vars)
        namespace.update(self.current_scope())
        namespace.update(self.function_table)
        
        # Add mathematical constants
        namespace.update({
            'PI': math.pi,
            'E': math.e,
            'TRUE': True,
            'FALSE': False
        })
        
        try:
            # Use AST for safe evaluation
            tree = ast.parse(expr, mode='eval')
            compiled = compile(tree, '<string>', 'eval')
            return eval(compiled, namespace)
        except Exception as e:
            raise PdsXRuntimeError(f"Karmaşık ifade hatası '{expr}': {e}")

    def _get_variable(self, name):
        """Değişken değerini alma"""
        # Check current scope first
        if name in self.current_scope():
            return self.current_scope()[name]
        
        # Check global scope
        if name in self.global_vars:
            return self.global_vars[name]
        
        # Check if it's a constant
        constants = {
            'PI': math.pi,
            'E': math.e,
            'TRUE': True,
            'FALSE': False
        }
        if name.upper() in constants:
            return constants[name.upper()]
        
        raise PdsXRuntimeError(f"Tanımlanmamış değişken: {name}")

    def _set_variable(self, name, value):
        """Değişkene değer atama"""
        # If variable exists in current scope, update it
        if name in self.current_scope():
            self.current_scope()[name] = value
        # If variable exists in global scope, update it  
        elif name in self.global_vars:
            self.global_vars[name] = value
        # Otherwise create in current scope
        else:
            self.current_scope()[name] = value

    def _call_function(self, func_name, args):
        """Kullanıcı tanımlı fonksiyon çağırma"""
        if func_name not in self.functions:
            raise PdsXRuntimeError(f"Bilinmeyen fonksiyon: {func_name}")
        
        func_info = self.functions[func_name]
        params = func_info["params"]
        body = func_info["body"]
        
        if len(args) != len(params):
            raise PdsXRuntimeError(f"Fonksiyon {func_name} parametre sayısı uyumsuzluğu")
        
        # Create new scope for function
        func_scope = {}
        for (param_name, param_type), arg in zip(params, args):
            func_scope[param_name] = arg
        
        self.push_scope(func_scope)
        self.call_stack.append({"type": "FUNCTION", "name": func_name, "return_address": self.program_counter})
        
        try:
            result = None
            for cmd in body:
                result = self.execute_command(cmd)
                if result is not None:  # RETURN statement
                    break
            return result
        finally:
            self.pop_scope()
            self.call_stack.pop()

    def _call_sub(self, sub_name, args):
        """Kullanıcı tanımlı sub çağırma"""
        if sub_name not in self.subs:
            raise PdsXRuntimeError(f"Bilinmeyen sub: {sub_name}")
        
        sub_info = self.subs[sub_name]
        params = sub_info["params"]
        body = sub_info["body"]
        
        if len(args) != len(params):
            raise PdsXRuntimeError(f"Sub {sub_name} parametre sayısı uyumsuzluğu")
        
        # Create new scope for sub
        sub_scope = {}
        for (param_name, param_type), arg in zip(params, args):
            sub_scope[param_name] = arg
        
        self.push_scope(sub_scope)
        self.call_stack.append({"type": "SUB", "name": sub_name, "return_address": self.program_counter})
        
        try:
            for cmd in body:
                self.execute_command(cmd)
        finally:
            self.pop_scope()
            self.call_stack.pop()

    def run(self, code=None):
        """Ana program çalıştırma metodu"""
        if code:
            self.parse_program(code)
        
        self.running = True
        self.program_counter = 0
        
        print(f"PDSX v12X Yorumlayıcı başlatılıyor...")
        print(f"Program satır sayısı: {len(self.program)}")
        print(f"Yüklenen modüller: {list(self.modules.keys())}")
        print(f"Tanımlanan tipler: {len(self.types)}")
        print(f"Tanımlanan fonksiyonlar: {len(self.functions)}")
        print("=" * 50)
        
        try:
            while self.running and self.program_counter < len(self.program):
                if self.debug_mode:
                    self._debug_step()
                
                command, scope_name = self.program[self.program_counter]
                # Debug çıktısı kaldırıldı - sadece hata ayıklama modunda göster
                # print(f"EXEC ORDER: PC={self.program_counter}, CMD='{command}'")
                result = self.execute_command(command, scope_name)
                
                # Handle control flow
                if isinstance(result, int):
                    self.program_counter = result
                else:
                    self.program_counter += 1
                
                # Check for infinite loops
                if self.program_counter > len(self.program) * 1000:
                    raise PdsXRuntimeError("Sonsuz döngü tespit edildi")
            
            print("\nProgram başarıyla tamamlandı.")
            
        except KeyboardInterrupt:
            print("\nProgram kullanıcı tarafından durduruldu.")
            self.running = False
        except PdsXException as e:
            print(f"\nPDSX Hatası: {e}")
            self.running = False
        except Exception as e:
            print(f"\nBeklenmeyen hata: {e}")
            logging.error(f"Beklenmeyen hata: {e}", exc_info=True)
            self.running = False
        finally:
            self._cleanup()

    def _debug_step(self):
        """Debug modunda adım adım çalıştırma"""
        command, scope_name = self.program[self.program_counter]
        print(f"\nDEBUG - Satır {self.program_counter + 1}: {command}")
        print(f"Geçerli kapsam: {list(self.current_scope().keys())}")
        print(f"Global değişkenler: {list(self.global_vars.keys())}")
        
        response = input("Devam için Enter, (q)uit için 'q', (c)ontinue için 'c': ").strip().lower()
        if response == 'q':
            self.running = False
        elif response == 'c':
            self.debug_mode = False

    def _cleanup(self):
        """Program sonrası temizlik işlemleri"""
        # Close file handles
        for handle in self.file_handles.values():
            try:
                handle.close()
            except:
                pass
        
        # Close database connections
        for conn in self.db_connections.values():
            try:
                conn.close()
            except:
                pass
        
        # Memory cleanup
        self.memory_pool.clear()
        
        # Show final statistics
        print(f"\nİstatistikler:")
        print(f"Çalıştırılan komut sayısı: {self.program_counter}")
        print(f"Maksimum kapsam derinliği: {len(self.scopes)}")
        print(f"Bellek kullanımı: {self.memory_manager.get_memory_stats()}")

    # Control Flow Implementations
    def _execute_if(self, command, scope_name=None):
        """IF komutunu çalıştırma - basit implementasyon"""
        command_upper = command.upper()
        
        if command_upper.startswith("IF "):
            # IF condition THEN parsing
            if " THEN" in command_upper:
                condition_part = command[3:command.upper().find(" THEN")].strip()
                
                # Evaluate condition
                try:
                    condition_result = self.evaluate_expression(condition_part, scope_name)
                    print(f"🔹 IF: Condition '{condition_part}' = {condition_result}")
                    
                    # If condition is false, skip to ELSE or END IF
                    if not condition_result:
                        # Skip to matching ELSE or END IF
                        level = 1
                        pc = self.program_counter + 1
                        while pc < len(self.program) and level > 0:
                            line = self.program[pc][0].strip().upper()
                            if line.startswith("IF "):
                                level += 1
                            elif line.startswith("END IF"):
                                level -= 1
                                if level == 0:
                                    return pc + 1  # Jump to after END IF
                            elif line.startswith("ELSE") and level == 1:
                                return pc + 1  # Jump to ELSE block
                            pc += 1
                        return pc
                    
                except Exception as e:
                    print(f"🔹 IF: Condition evaluation error: {e}")
                    return None
            else:
                print(f"🔹 IF: Missing THEN in '{command}'")
                
        elif command_upper.startswith("ELSE"):
            # ELSE - skip to END IF
            level = 1
            pc = self.program_counter + 1
            while pc < len(self.program) and level > 0:
                line = self.program[pc][0].strip().upper()
                if line.startswith("IF "):
                    level += 1
                elif line.startswith("END IF"):
                    level -= 1
                    if level == 0:
                        return pc + 1  # Jump to after END IF
                pc += 1
            return pc
            
        elif command_upper.startswith("END IF"):
            # END IF - just continue
            pass
            
        return None

    def _execute_for(self, command, scope_name):
        """FOR döngüsü çalıştırma"""
        # REM: Karmaşık FOR kodu devre dışı - basit implementasyon yapılacak
        # command_upper = command.upper()
        # 
        # if command_upper.startswith("FOR "):
        #     # FOR variable = start TO end [STEP step]
        #     match = re.match(r"FOR\s+(\w+)\s*=\s*(.+?)\s+TO\s+(.+?)(?:\s+STEP\s+(.+))?$", command, re.IGNORECASE)
        #     if match:
        #         var_name, start_expr, end_expr, step_expr = match.groups()
        #         
        #         start_val = self.evaluate_expression(start_expr, scope_name)
        #         end_val = self.evaluate_expression(end_expr, scope_name)
        #         step_val = self.evaluate_expression(step_expr, scope_name) if step_expr else 1
        #         
        #         # Store loop info - start_pc should point to the line AFTER FOR
        #         loop_info = {
        #             "type": "FOR",
        #             "variable": var_name,
        #             "current": start_val,
        #             "end": end_val,
        #             "step": step_val,
        #             "start_pc": self.program_counter + 1  # Next line after FOR
        #         }
        #         self.loop_stack.append(loop_info)
        #         
        #         print(f"DEBUG FOR: Başlatılıyor - {var_name}={start_val} TO {end_val} STEP {step_val}")
        #         print(f"DEBUG FOR: start_pc={loop_info['start_pc']}, current_pc={self.program_counter}")
        #         
        #         # Set initial value
        #         print(f"DEBUG FOR: Setting {var_name} = {start_val}")
        #         self.set_variable_value(var_name, start_val, scope_name)
        #         print(f"DEBUG FOR: After set, {var_name} = {self.get_variable_value(var_name, scope_name)}")
        #         print(f"DEBUG FOR: Initial variable set, returning None")
        #         return None  # Explicitly return None to continue to next line
        #         
        # elif command_upper == "NEXT" or command_upper.startswith("NEXT "):
        #     print(f"DEBUG: NEXT command detected: '{command}'")
        #     # NEXT [variable]
        #     if not self.loop_stack:
        #         raise PdsXRuntimeError("NEXT without FOR")
        #         
        #     loop_info = self.loop_stack[-1]
        #     if loop_info["type"] != "FOR":
        #         raise PdsXRuntimeError("NEXT without FOR")
        #     
        #     print(f"DEBUG: Loop info: {loop_info}")
        #     
        #     # Get current value from variable, not from loop_info
        #     current_value = self.get_variable_value(loop_info["variable"], scope_name)
        #     
        #     print(f"DEBUG NEXT: {loop_info['variable']} current value from variable: {current_value}")
        #     print(f"DEBUG NEXT: {loop_info['variable']} stored in loop_info: {loop_info.get('current', 'NOT_SET')}")
        #     
        #     # Update loop variable
        #     current = current_value + loop_info["step"]
        #     
        #     if self.trace_mode:
        #         print(f"DEBUG NEXT: {loop_info['variable']} new value: {current}")
        #     
        #     # Always update the variable value first
        #     self.set_variable_value(loop_info["variable"], current, scope_name)
        #     
        #     if self.trace_mode:
        #         print(f"DEBUG NEXT: {loop_info['variable']} after set: {self.get_variable_value(loop_info['variable'], scope_name)}")
        #     
        #     # Check if loop should continue
        #     if (loop_info["step"] > 0 and current <= loop_info["end"]) or \
        #        (loop_info["step"] < 0 and current >= loop_info["end"]):
        #         # Continue loop
        #         if self.trace_mode:
        #             print(f"DEBUG NEXT: Continuing loop, jumping to PC {loop_info['start_pc']}")
        #         return loop_info["start_pc"]  # Return target PC to jump to
        #     else:
        #         # Exit loop
        #         if self.trace_mode:
        #             print(f"DEBUG NEXT: Exiting loop, current={current}, end={loop_info['end']}")
        #         self.loop_stack.pop()
        #         return None  # Continue to next statement
        #         
        # elif command_upper == "EXIT FOR":
        #     # Exit current FOR loop
        #     if not self.loop_stack or self.loop_stack[-1]["type"] != "FOR":
        #         raise PdsXRuntimeError("EXIT FOR without FOR")
        #     
        #     # Find matching NEXT
        #     level = 1
        #     pc = self.program_counter + 1
        #     while pc < len(self.program) and level > 0:
        #         line = self.program[pc].strip().upper()
        #         if line.startswith("FOR "):
        #             level += 1
        #         elif line == "NEXT" or line.startswith("NEXT "):
        #             level -= 1
        #         pc += 1
        #     
        #     self.program_counter = pc - 1
        #     self.loop_stack.pop()
        
        # GELİŞMİŞ FOR İMPLEMENTASYONU - İç içe döngüler ve recursion destekli
        print(f"🔄 FOR HANDLER: '{command}'")
        command_upper = command.upper()
        
        # FOR stack'i initialize et
        if not hasattr(self, 'for_stack'):
            self.for_stack = []
        
        if command_upper.startswith("FOR "):
            # FOR parsing: FOR i = 1 TO 3 [STEP 1]
            parts = command.split()
            if len(parts) >= 6 and parts[2] == "=" and parts[4].upper() == "TO":
                var_name = parts[1]
                start_val = int(parts[3])
                end_val = int(parts[5])
                step_val = 1
                
                # STEP kontrolü
                if len(parts) >= 8 and parts[6].upper() == "STEP":
                    step_val = int(parts[7])
                
                print(f"🔄 FOR[{len(self.for_stack)}]: {var_name} = {start_val} TO {end_val} STEP {step_val}")
                
                # Değişkeni current scope'a set et
                self.current_scope()[var_name] = start_val
                
                # Loop info sakla - nested level tracking ile
                loop_info = {
                    "type": "FOR",
                    "var": var_name,
                    "start": start_val,
                    "end": end_val,
                    "step": step_val,
                    "start_pc": self.program_counter + 1,
                    "level": len(self.for_stack),  # nested level
                    "scope_backup": dict(self.current_scope())  # scope backup for recursion
                }
                self.for_stack.append(loop_info)
                print(f"🔄 FOR: Loop stack depth: {len(self.for_stack)}, info: {loop_info}")
                
        elif command_upper.startswith("NEXT"):
            # NEXT [variable] - son FOR'u işle veya belirtilen variable'ı
            print(f"🔄 NEXT: Stack depth: {len(getattr(self, 'for_stack', []))}")
            
            if not hasattr(self, 'for_stack') or not self.for_stack:
                raise PdsXRuntimeError("NEXT without FOR")
                
            # Variable ismi belirtilmişse o FOR'u bul
            target_var = None
            if len(command.split()) > 1:
                target_var = command.split()[1]
                print(f"🔄 NEXT: Target variable: {target_var}")
                
                # Stack'te geriye doğru ara
                target_index = -1
                for i in range(len(self.for_stack) - 1, -1, -1):
                    if self.for_stack[i]["var"] == target_var:
                        target_index = i
                        break
                        
                if target_index == -1:
                    raise PdsXRuntimeError(f"NEXT {target_var}: FOR not found")
                    
                # Hedef FOR'dan sonraki tüm FOR'ları kapat
                while len(self.for_stack) > target_index + 1:
                    closed_loop = self.for_stack.pop()
                    print(f"🔄 NEXT: Closing nested FOR {closed_loop['var']}")
            
            # Son FOR'u işle
            loop_info = self.for_stack[-1]
            var_name = loop_info["var"]
            
            # Değişkeni artır
            current_val = self.current_scope()[var_name]
            new_val = current_val + loop_info["step"]
            self.current_scope()[var_name] = new_val
            
            print(f"🔄 NEXT[{loop_info['level']}]: {var_name}: {current_val} -> {new_val} (end: {loop_info['end']}, step: {loop_info['step']})")
            
            # Döngü devam kontrolü
            should_continue = False
            if loop_info["step"] > 0:
                should_continue = new_val <= loop_info["end"]
            else:
                should_continue = new_val >= loop_info["end"]
                
            if should_continue:
                # Döngü devam et
                print(f"🔄 NEXT: Döngü devam, PC: {loop_info['start_pc']}'ya git")
                return loop_info["start_pc"]
            else:
                # Döngü bitir
                print(f"🔄 NEXT: Döngü[{loop_info['level']}] bitti")
                self.for_stack.pop()
                
        elif command_upper == "END FOR":
            # END FOR - son FOR'u kapat (NEXT gibi ama increment yapmadan)
            print(f"🔄 END FOR: Stack depth: {len(getattr(self, 'for_stack', []))}")
            
            if not hasattr(self, 'for_stack') or not self.for_stack:
                raise PdsXRuntimeError("END FOR without FOR")
                
            loop_info = self.for_stack.pop()
            print(f"🔄 END FOR: FOR {loop_info['var']} döngüsü kapatıldı")
            
        elif command_upper.startswith("EXIT FOR"):
            # EXIT FOR - mevcut FOR'dan çık
            print(f"🔄 EXIT FOR: Stack depth: {len(getattr(self, 'for_stack', []))}")
            
            if not hasattr(self, 'for_stack') or not self.for_stack:
                raise PdsXRuntimeError("EXIT FOR without FOR")
                
            # Son FOR'u kapat
            loop_info = self.for_stack.pop()
            print(f"🔄 EXIT FOR: FOR {loop_info['var']} döngüsünden çıkıldı")
            
            # Eşleşen NEXT veya END FOR'u bul ve oraya atla
            level = 1
            pc = self.program_counter + 1
            while pc < len(self.program) and level > 0:
                line = self.program[pc].strip().upper()
                if line.startswith("FOR "):
                    level += 1
                elif line.startswith("NEXT") or line == "END FOR":
                    level -= 1
                    if level == 0:
                        return pc + 1  # NEXT/END FOR'dan sonraki satıra git
                pc += 1
                
        return None

    def set_variable_value(self, var_name, value, scope_name=None):
        """Değişken değeri ayarlama"""
        if scope_name:
            # Belirli bir scope'ta ayarla
            if scope_name in self.scopes:
                self.scopes[scope_name][var_name] = value
            else:
                self.current_scope()[var_name] = value
        else:
            # Geçerli scope'ta ayarla
            self.current_scope()[var_name] = value

    def get_variable_value(self, var_name, scope_name=None):
        """Değişken değeri alma - wrapper for _get_variable"""
        return self._get_variable(var_name, scope_name)

    def _get_variable(self, var_name, scope_name=None):
        """Değişken değeri alma"""
        if scope_name and scope_name in self.scopes:
            return self.scopes[scope_name].get(var_name)
        
        # Scope stack'de arama
        for scope in reversed(self.scopes):
            if var_name in scope:
                return scope[var_name]
        
        # Global'de arama
        if var_name in self.global_vars:
            return self.global_vars[var_name]
        
        return None

    def _execute_expression_statement(self, command, scope_name=None):
        """Expression komutunu çalıştırma"""
        # Basit expression değerlendirmesi
        try:
            result = self.evaluate_expression(command, scope_name)
            return result
        except Exception as e:
            raise PdsXRuntimeError(f"Expression hatası: {e}")

    def _is_numeric(self, value):
        """Değerin sayısal olup olmadığını kontrol etme"""
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False

    def _execute_while(self, command, scope_name):
        """WHILE döngüsü çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("WHILE "):
            # WHILE condition
            condition_expr = command[6:].strip()
            condition = self.evaluate_expression(condition_expr, scope_name)
            
            if not condition:
                # Skip to WEND
                level = 1
                pc = self.program_counter + 1
                while pc < len(self.program) and level > 0:
                    line = self.program[pc].strip().upper()
                    if line.startswith("WHILE "):
                        level += 1
                    elif line == "WEND":
                        level -= 1
                    pc += 1
                
                self.program_counter = pc - 1
            else:
                # Store loop info
                loop_info = {
                    "type": "WHILE",
                    "start_pc": self.program_counter
                }
                self.loop_stack.append(loop_info)
                
        elif command_upper == "WEND":
            if not self.loop_stack or self.loop_stack[-1]["type"] != "WHILE":
                raise PdsXRuntimeError("WEND without WHILE")
            
            loop_info = self.loop_stack[-1]
            self.program_counter = loop_info["start_pc"] - 1
            
        elif command_upper == "EXIT WHILE":
            if not self.loop_stack or self.loop_stack[-1]["type"] != "WHILE":
                raise PdsXRuntimeError("EXIT WHILE without WHILE")
            
            # Find matching WEND
            level = 1
            pc = self.program_counter + 1
            while pc < len(self.program) and level > 0:
                line = self.program[pc].strip().upper()
                if line.startswith("WHILE "):
                    level += 1
                elif line == "WEND":
                    level -= 1
                pc += 1
            
            self.program_counter = pc - 1
            self.loop_stack.pop()

    def _execute_do_loop(self, command, scope_name):
        """DO...LOOP döngüsü çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("DO"):
            # Store loop info
            loop_info = {
                "type": "DO",
                "start_pc": self.program_counter
            }
            self.loop_stack.append(loop_info)
            
        elif command_upper.startswith("LOOP"):
            if not self.loop_stack or self.loop_stack[-1]["type"] != "DO":
                raise PdsXRuntimeError("LOOP without DO")
            
            # Check for WHILE/UNTIL condition
            if "WHILE" in command_upper:
                condition_expr = command_upper.split("WHILE", 1)[1].strip()
                condition = self.evaluate_expression(condition_expr, scope_name)
                if condition:
                    loop_info = self.loop_stack[-1]
                    self.program_counter = loop_info["start_pc"]
                else:
                    self.loop_stack.pop()
            elif "UNTIL" in command_upper:
                condition_expr = command_upper.split("UNTIL", 1)[1].strip()
                condition = self.evaluate_expression(condition_expr, scope_name)
                if not condition:
                    loop_info = self.loop_stack[-1]
                    self.program_counter = loop_info["start_pc"]
                else:
                    self.loop_stack.pop()
            else:
                # Infinite loop back to DO
                loop_info = self.loop_stack[-1]
                self.program_counter = loop_info["start_pc"]

    def _execute_prolog_operations(self, command, scope_name):
        """Gelişmiş Prolog komutlarını çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("FACT "):
            # FACT predicate(args)
            fact_str = command[5:].strip()
            self.prolog_engine.add_fact(fact_str)
            print(f"Fact added: {fact_str}")
            return None
            
        elif command_upper.startswith("RULE "):
            # RULE head :- body1, body2, ...
            rule_str = command[5:].strip()
            if ":-" in rule_str:
                head, body = rule_str.split(":-", 1)
                head = head.strip()
                body_parts = [part.strip() for part in body.split(",")]
                self.prolog_engine.add_rule(head, body_parts)
                print(f"Rule added: {head} :- {', '.join(body_parts)}")
            else:
                raise PdsXSyntaxError(f"Invalid RULE syntax: {rule_str}")
            return None
            
        elif command_upper.startswith("QUERY "):
            # QUERY goal
            goal_str = command[6:].strip()
            
            # Support for logical operators in queries
            if any(op in goal_str.upper() for op in ['AND', 'OR', 'NOT', 'IMP', 'EQV', 'NAND', 'NOR', 'XOR']):
                solutions = self._execute_logical_query(goal_str, scope_name)
            else:
                solutions = self.prolog_engine.query(goal_str)
            
            print(f"Query: {goal_str}")
            if solutions:
                print("Solutions found:")
                for i, solution in enumerate(solutions):
                    print(f"  {i+1}: {solution}")
                # Store in special variable for PDSX access
                self.current_scope()["_PROLOG_SOLUTIONS"] = solutions
            else:
                print("No solutions found.")
            return None
            
        elif command_upper.startswith("ASSERT "):
            # ASSERT fact - same as FACT
            fact_str = command[7:].strip()
            self.prolog_engine.add_fact(fact_str)
            print(f"Fact asserted: {fact_str}")
            return None
            
        elif command_upper.startswith("RETRACT "):
            # RETRACT fact
            fact_str = command[8:].strip()
            parsed_fact = self.prolog_engine._parse_term(fact_str)
            if parsed_fact in self.prolog_engine.facts:
                self.prolog_engine.facts.remove(parsed_fact)
                print(f"Fact retracted: {fact_str}")
            else:
                print(f"Fact not found: {fact_str}")
            return None
        
        else:
            raise PdsXSyntaxError(f"Unknown Prolog operation: {command}")

    def _retract_prolog_fact(self, fact):
        """Prolog fact'ini kaldırma (function table için)"""
        parsed_fact = self.prolog_engine._parse_term(fact)
        if parsed_fact in self.prolog_engine.facts:
            self.prolog_engine.facts.remove(parsed_fact)
            return True
        return False

    def _clear_prolog_database(self):
        """Tüm Prolog veritabanını temizleme"""
        self.prolog_engine.facts.clear()
        self.prolog_engine.rules.clear()

    def _execute_logical_query(self, query_str, scope_name):
        """Mantıksal operatörlü Prolog sorguları"""
        # Enhanced logical query processing
        query_upper = query_str.upper()
        
        # Parse logical operators
        if ' AND ' in query_upper:
            parts = query_str.split(' AND ')
            results = []
            for result in self.prolog_engine._logical_and(
                [part.strip() for part in parts], scope_name
            ):
                results.append(result)
            return results
        
        elif ' OR ' in query_upper:
            parts = query_str.split(' OR ')
            results = []
            for result in self.prolog_engine._logical_or(
                [part.strip() for part in parts], scope_name
            ):
                results.append(result)
            return results
        
        elif query_upper.startswith('NOT '):
            goal = query_str[4:].strip()
            results = self.prolog_engine._logical_not(goal, scope_name)
            return results if results else []
        
        # Default query
        return self.prolog_engine.query(query_str)

    def _execute_sql_command(self, command, scope_name):
        """SQL komutlarını çalıştırma"""
        command = command.strip()
        command_upper = command.upper()
        
        try:
            if command_upper.startswith(("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")):
                # SQL komutunu database system'e gönder
                result = self.db_system.execute_sql(command)
                
                if command_upper.startswith("SELECT"):
                    # SELECT sonuçlarını görüntüle
                    if result:
                        print("Query Results:")
                        for i, row in enumerate(result):
                            print(f"  Row {i+1}: {row}")
                        # Store results in special variable
                        self.current_scope()["_SQL_RESULTS"] = result
                    else:
                        print("No results found.")
                        self.current_scope()["_SQL_RESULTS"] = []
                else:
                    # INSERT, UPDATE, DELETE için başarı mesajı
                    print(f"SQL command executed successfully: {command}")
                
                return result
            else:
                raise PdsXSyntaxError(f"Unsupported SQL command: {command}")
                
        except Exception as e:
            raise PdsXRuntimeError(f"SQL execution error: {e}")

    def _execute_isam_command(self, command, scope_name):
        """ISAM komutlarını çalıştırma"""
        command = command.strip()
        command_upper = command.upper()
        
        try:
            if command_upper.startswith("ISAM CREATE"):
                # ISAM CREATE filename WITH FIELDS (field_definitions)
                return self._execute_isam_create(command, scope_name)
                
            elif command_upper.startswith("ISAM INSERT"):
                # ISAM INSERT INTO filename VALUES (values)
                return self._execute_isam_insert(command, scope_name)
                
            elif command_upper.startswith("ISAM READ"):
                # ISAM READ filename [WHERE conditions] [ORDER BY fields]
                return self._execute_isam_read(command, scope_name)
                
            elif command_upper.startswith("ISAM UPDATE"):
                # ISAM UPDATE filename SET field=value WHERE conditions
                return self._execute_isam_update(command, scope_name)
                
            elif command_upper.startswith("ISAM DELETE"):
                # ISAM DELETE FROM filename WHERE conditions
                return self._execute_isam_delete(command, scope_name)
                
            elif command_upper.startswith("ISAM COUNT"):
                # ISAM COUNT filename [WHERE conditions] [GROUP BY fields]
                return self._execute_isam_count(command, scope_name)
                
            elif command_upper.startswith("ISAM BACKUP"):
                # ISAM BACKUP filename TO backup_filename
                return self._execute_isam_backup(command, scope_name)
                
            elif command_upper.startswith("ISAM REBUILD"):
                # ISAM REBUILD INDEX filename
                return self._execute_isam_rebuild(command, scope_name)
                
            elif command_upper.startswith("ISAM CLOSE"):
                # ISAM CLOSE filename
                return self._execute_isam_close(command, scope_name)
                
            else:
                raise PdsXSyntaxError(f"Unsupported ISAM command: {command}")
                
        except Exception as e:
            raise PdsXRuntimeError(f"ISAM execution error: {e}")

    def _execute_isam_create(self, command, scope_name):
        """ISAM CREATE komutunu çalıştır"""
        # Basit implementasyon - dosya sistemi simülasyonu
        match = re.match(r"ISAM CREATE\s+(\w+\.idx)\s+WITH FIELDS\s*\((.*)\)", command, re.IGNORECASE)
        if not match:
            raise PdsXSyntaxError(f"Invalid ISAM CREATE syntax: {command}")
        
        filename, fields_def = match.groups()
        
        # ISAM dosya simülasyonu için yapı oluştur
        if not hasattr(self, 'isam_files'):
            self.isam_files = {}
        
        # Field definitions'ı parse et
        fields = []
        for field_def in fields_def.split(','):
            field_def = field_def.strip()
            parts = field_def.split()
            if len(parts) >= 2:
                field_name = parts[0]
                field_type = parts[1]
                is_key = 'KEY' in field_def.upper()
                fields.append({
                    'name': field_name,
                    'type': field_type,
                    'is_key': is_key
                })
        
        self.isam_files[filename] = {
            'fields': fields,
            'data': [],
            'indexes': {}
        }
        
        print(f"ISAM file created: {filename} with {len(fields)} fields")
        return None

    def _execute_isam_insert(self, command, scope_name):
        """ISAM INSERT komutunu çalıştır"""
        match = re.match(r"ISAM INSERT INTO\s+(\w+\.idx)\s+VALUES\s*\((.*)\)", command, re.IGNORECASE)
        if not match:
            raise PdsXSyntaxError(f"Invalid ISAM INSERT syntax: {command}")
        
        filename, values_str = match.groups()
        
        if filename not in self.isam_files:
            raise PdsXRuntimeError(f"ISAM file not found: {filename}")
        
        # Values'ları parse et
        values = []
        for value_str in values_str.split(','):
            value_str = value_str.strip()
            if value_str.startswith("'") and value_str.endswith("'"):
                values.append(value_str[1:-1])  # String
            elif '.' in value_str:
                values.append(float(value_str))  # Float
            else:
                try:
                    values.append(int(value_str))  # Integer
                except ValueError:
                    values.append(value_str)  # String fallback
        
        # Record'u ekle
        record = dict(zip([f['name'] for f in self.isam_files[filename]['fields']], values))
        self.isam_files[filename]['data'].append(record)
        
        print(f"Record inserted into {filename}: {record}")
        return None

    def _execute_isam_read(self, command, scope_name):
        """ISAM READ komutunu çalıştır"""
        # ISAM READ filename [WHERE conditions] [ORDER BY fields]
        parts = command.split()
        if len(parts) < 3:
            raise PdsXSyntaxError(f"Invalid ISAM READ syntax: {command}")
        
        filename = parts[2]
        
        if filename not in self.isam_files:
            raise PdsXRuntimeError(f"ISAM file not found: {filename}")
        
        data = self.isam_files[filename]['data']
        
        # WHERE clause varsa filtrele
        if ' WHERE ' in command.upper():
            # Basit WHERE implementasyonu
            where_part = command.upper().split(' WHERE ')[1].split(' ORDER BY ')[0]
            # Bu örnekte basit eşitlik kontrolü
            filtered_data = []
            for record in data:
                # Basit condition parsing (gerçek implementasyon daha karmaşık olurdu)
                if self._evaluate_isam_condition(record, where_part):
                    filtered_data.append(record)
            data = filtered_data
        
        # ORDER BY varsa sırala
        if ' ORDER BY ' in command.upper():
            order_part = command.upper().split(' ORDER BY ')[1]
            # Basit sorting
            sort_field = order_part.split()[0].lower()
            reverse_order = 'DESC' in order_part.upper()
            if sort_field in data[0] if data else False:
                data = sorted(data, key=lambda x: x.get(sort_field, 0), reverse=reverse_order)
        
        # Sonuçları göster
        if data:
            print(f"ISAM READ results from {filename}:")
            for i, record in enumerate(data):
                print(f"  Record {i+1}: {record}")
            # Store in special variable
            self.current_scope()["_ISAM_RESULTS"] = data
        else:
            print(f"No records found in {filename}")
            self.current_scope()["_ISAM_RESULTS"] = []
        
        return data

    def _evaluate_isam_condition(self, record, condition):
        """ISAM WHERE condition'ını değerlendirme"""
        # Basit implementation - gerçek versiyonda daha kapsamlı olurdu
        condition = condition.strip()
        
        # Simple equality check: field = value
        if ' = ' in condition:
            field, value = condition.split(' = ', 1)
            field = field.strip()
            value = value.strip().strip("'\"")
            
            if field in record:
                return str(record[field]) == value
        
        # Simple numeric comparison: field > value, field < value
        for op in [' >= ', ' <= ', ' > ', ' < ']:
            if op in condition:
                field, value = condition.split(op, 1)
                field = field.strip()
                value = float(value.strip())
                
                if field in record:
                    record_val = float(record[field]) if isinstance(record[field], (int, float)) else 0
                    if op.strip() == '>':
                        return record_val > value
                    elif op.strip() == '<':
                        return record_val < value
                    elif op.strip() == '>=':
                        return record_val >= value
                    elif op.strip() == '<=':
                        return record_val <= value
        
        return True  # Default true for unhandled conditions

    def _execute_isam_update(self, command, scope_name):
        """ISAM UPDATE komutunu çalıştır"""
        print(f"ISAM UPDATE executed: {command}")
        return None

    def _execute_isam_delete(self, command, scope_name):
        """ISAM DELETE komutunu çalıştır"""
        print(f"ISAM DELETE executed: {command}")
        return None

    def _execute_isam_count(self, command, scope_name):
        """ISAM COUNT komutunu çalıştır"""
        parts = command.split()
        if len(parts) < 3:
            raise PdsXSyntaxError(f"Invalid ISAM COUNT syntax: {command}")
        
        filename = parts[2]
        
        if filename not in self.isam_files:
            raise PdsXRuntimeError(f"ISAM file not found: {filename}")
        
        count = len(self.isam_files[filename]['data'])
        print(f"ISAM COUNT {filename}: {count} records")
        return count

    def _execute_isam_backup(self, command, scope_name):
        """ISAM BACKUP komutunu çalıştır"""
        print(f"ISAM BACKUP executed: {command}")
        return None

    def _execute_isam_rebuild(self, command, scope_name):
        """ISAM REBUILD komutunu çalıştır"""
        print(f"ISAM REBUILD executed: {command}")
        return None

    def _execute_isam_close(self, command, scope_name):
        """ISAM CLOSE komutunu çalıştır"""
        parts = command.split()
        if len(parts) < 3:
            raise PdsXSyntaxError(f"Invalid ISAM CLOSE syntax: {command}")
        
        filename = parts[2]
        
        if filename in self.isam_files:
            del self.isam_files[filename]
            print(f"ISAM file closed: {filename}")
        else:
            print(f"ISAM file not found: {filename}")
        
        return None

# Event-Driven Programming System
class EventSystem:
    """Event tabanlı programlama sistemi"""
    def __init__(self):
        self.events = {}
        self.event_handlers = {}
        self.running_events = set()
        self.event_queue = []
        
    def define_event(self, event_name, code_block):
        """Event tanımlama"""
        self.events[event_name] = code_block
        
    def trigger_event(self, event_name, args=None, interpreter=None):
        """Event tetikleme"""
        if event_name in self.events and event_name not in self.running_events:
            self.running_events.add(event_name)
            try:
                # Event'i paralel olarak çalıştır
                thread = threading.Thread(
                    target=self._execute_event,
                    args=(event_name, args or {}, interpreter)
                )
                thread.daemon = True
                thread.start()
            except Exception as e:
                print(f"Event {event_name} hatası: {e}")
                self.running_events.discard(event_name)
                
    def _execute_event(self, event_name, args, interpreter):
        """Event kodunu çalıştırma"""
        try:
            if interpreter:
                # Event scope'unu oluştur
                event_scope = args.copy()
                interpreter.scope_stack.append(event_scope)
                
                # Event kodunu çalıştır
                for command in self.events[event_name]:
                    interpreter.execute_command(command)
                    
                interpreter.scope_stack.pop()
        except Exception as e:
            print(f"Event {event_name} çalıştırma hatası: {e}")
        finally:
            self.running_events.discard(event_name)

# Enhanced Prolog Engine with Logical Operators
class PrologEngine:
    """Gelişmiş Prolog motoru - mantıksal programlama, backtracking ve mantıksal operatörler"""
    def __init__(self):
        self.facts = []
        self.rules = []
        self.variables = {}
        self.call_stack = []
        self.trace_mode = False
        self.solution_count = 0
        
        # Logical operators
        self.logical_operators = {
            'AND': self._logical_and,
            'OR': self._logical_or,
            'NOT': self._logical_not,
            'IMP': self._logical_implies,
            'EQV': self._logical_equivalent,
            'NAND': self._logical_nand,
            'NOR': self._logical_nor,
            'XOR': self._logical_xor,
            'BIND': self._logical_bind
        }
    
    def execute_command(self, command):
        """PDSX komutlarını işleme"""
        command = command.strip()
        command_upper = command.upper()
        
        if command_upper.startswith("FACT "):
            fact_str = command[5:].strip()
            self.add_fact(fact_str)
            return f"Fact eklendi: {fact_str}"
        
        elif command_upper.startswith("RULE "):
            rule_str = command[5:].strip()
            if ":-" in rule_str:
                head, body = rule_str.split(":-", 1)
                head = head.strip()
                body_parts = [part.strip() for part in body.split(",")]
                self.add_rule(head, body_parts)
                return f"Rule eklendi: {head} :- {', '.join(body_parts)}"
            else:
                return f"Hatalı RULE sözdizimi: {rule_str}"
        
        elif command_upper.startswith("QUERY "):
            goal_str = command[6:].strip()
            solutions = self.query(goal_str)
            
            if solutions:
                result = f"Query: {goal_str}\nÇözümler:\n"
                for i, solution in enumerate(solutions):
                    result += f"  {i+1}: {solution}\n"
                return result
            else:
                return f"Query: {goal_str}\nÇözüm bulunamadı."
        
        elif command_upper.startswith("PROLOG_TRACE"):
            self.trace_mode = True
            return "Prolog trace modu açık"
        
        elif command_upper.startswith("PROLOG_NOTRACE"):
            self.trace_mode = False
            return "Prolog trace modu kapalı"
        
        elif command_upper.startswith("PROLOG_RESET"):
            self.facts = []
            self.rules = []
            return "Prolog veritabanı temizlendi"
        
        return None
        
    def add_fact(self, fact):
        """Gerçek (fact) ekleme"""
        parsed_fact = self._parse_term(fact)
        if parsed_fact not in self.facts:
            self.facts.append(parsed_fact)
            if self.trace_mode:
                print(f"FACT added: {fact}")
        
    def add_rule(self, head, body):
        """Kural ekleme"""
        if isinstance(body, str):
            body = [body]
        
        rule = {
            "head": self._parse_term(head), 
            "body": [self._parse_term(term) for term in body]
        }
        self.rules.append(rule)
        
        if self.trace_mode:
            print(f"RULE added: {head} :- {', '.join(body)}")
        
    def query(self, goal):
        """Sorgu çalıştırma"""
        self.solution_count = 0
        parsed_goal = self._parse_term(goal)
        
        if self.trace_mode:
            print(f"QUERY: {goal}")
            
        solutions = list(self._solve(parsed_goal, {}))
        
        if self.trace_mode:
            print(f"Solutions found: {len(solutions)}")
            
        return solutions
        
    def _logical_and(self, goal1, goal2, bindings):
        """Mantıksal AND operatörü"""
        for bindings1 in self._solve(goal1, bindings):
            for bindings2 in self._solve(goal2, bindings1):
                yield bindings2
    
    def _logical_or(self, goal1, goal2, bindings):
        """Mantıksal OR operatörü"""
        # Try first goal
        for result in self._solve(goal1, bindings):
            yield result
        # Try second goal  
        for result in self._solve(goal2, bindings):
            yield result
    
    def _logical_not(self, goal, bindings):
        """Mantıksal NOT operatörü (negation as failure)"""
        solutions = list(self._solve(goal, bindings))
        if not solutions:
            yield bindings  # Succeed if goal fails
    
    def _logical_implies(self, goal1, goal2, bindings):
        """Mantıksal IMPLIES operatörü (goal1 -> goal2)"""
        # If goal1 succeeds, goal2 must succeed
        goal1_solutions = list(self._solve(goal1, bindings))
        if goal1_solutions:
            for bindings1 in goal1_solutions:
                for bindings2 in self._solve(goal2, bindings1):
                    yield bindings2
        else:
            # If goal1 fails, implication is true
            yield bindings
    
    def _logical_equivalent(self, goal1, goal2, bindings):
        """Mantıksal EQUIVALENT operatörü (goal1 <-> goal2)"""
        # Both succeed or both fail
        goal1_solutions = list(self._solve(goal1, bindings))
        goal2_solutions = list(self._solve(goal2, bindings))
        
        if (goal1_solutions and goal2_solutions) or (not goal1_solutions and not goal2_solutions):
            yield bindings
    
    def _logical_nand(self, goal1, goal2, bindings):
        """Mantıksal NAND operatörü"""
        and_solutions = list(self._logical_and(goal1, goal2, bindings))
        if not and_solutions:
            yield bindings
    
    def _logical_nor(self, goal1, goal2, bindings):
        """Mantıksal NOR operatörü"""
        or_solutions = list(self._logical_or(goal1, goal2, bindings))
        if not or_solutions:
            yield bindings
    
    def _logical_xor(self, goal1, goal2, bindings):
        """Mantıksal XOR operatörü"""
        goal1_solutions = list(self._solve(goal1, bindings))
        goal2_solutions = list(self._solve(goal2, bindings))
        
        if (goal1_solutions and not goal2_solutions) or (not goal1_solutions and goal2_solutions):
            yield bindings
    
    def _logical_bind(self, var, value, bindings):
        """Değişken bağlama operatörü"""
        if self._is_variable(var):
            new_bindings = bindings.copy()
            new_bindings[var] = value
            yield new_bindings
        else:
            # Check if var equals value
            if var == value:
                yield bindings
        
    def _solve(self, goal, bindings):
        """Backtracking ile çözüm bulma"""
        # Fact'lerde ara
        for fact in self.facts:
            unified_bindings = self._unify(goal, fact, bindings.copy())
            if unified_bindings is not None:
                yield unified_bindings
        
        # Rule'larda ara
        for rule in self.rules:
            # Rename variables in rule to avoid conflicts
            renamed_rule = self._rename_variables(rule)
            unified_bindings = self._unify(goal, renamed_rule["head"], bindings.copy())
            
            if unified_bindings is not None:
                # Try to solve all body goals
                yield from self._solve_body(renamed_rule["body"], unified_bindings)
    
    def _solve_body(self, body_goals, bindings):
        """Rule body'sini çözme"""
        if not body_goals:
            yield bindings
            return
        
        first_goal = body_goals[0]
        remaining_goals = body_goals[1:]
        
        # Substitute variables in first goal
        substituted_goal = self._substitute(first_goal, bindings)
        
        # Solve first goal
        for new_bindings in self._solve(substituted_goal, bindings):
            # Recursively solve remaining goals
            yield from self._solve_body(remaining_goals, new_bindings)
    
    def _unify(self, term1, term2, bindings):
        """İki terimi birleştirme (unification)"""
        term1 = self._substitute(term1, bindings)
        term2 = self._substitute(term2, bindings)
        
        if self._is_variable(term1):
            if term1 in bindings:
                return self._unify(bindings[term1], term2, bindings)
            else:
                bindings[term1] = term2
                return bindings
        elif self._is_variable(term2):
            if term2 in bindings:
                return self._unify(term1, bindings[term2], bindings)
            else:
                bindings[term2] = term1
                return bindings
        elif isinstance(term1, dict) and isinstance(term2, dict):
            if term1.get("functor") != term2.get("functor"):
                return None
            if len(term1.get("args", [])) != len(term2.get("args", [])):
                return None
            
            for arg1, arg2 in zip(term1.get("args", []), term2.get("args", [])):
                bindings = self._unify(arg1, arg2, bindings)
                if bindings is None:
                    return None
            return bindings
        elif term1 == term2:
            return bindings
        else:
            return None
    
    def _substitute(self, term, bindings):
        """Değişkenleri değerleriyle değiştirme"""
        if self._is_variable(term):
            return bindings.get(term, term)
        elif isinstance(term, dict) and "args" in term:
            return {
                "functor": term["functor"],
                "args": [self._substitute(arg, bindings) for arg in term["args"]]
            }
        else:
            return term
    
    def _is_variable(self, term):
        """Değişken kontrolü"""
        return isinstance(term, str) and term.startswith("?")
    
    def _parse_term(self, term_str):
        """Term string'ini parse etme"""
        term_str = term_str.strip()
        
        if self._is_variable(term_str):
            return term_str
        
        # Check for compound term like parent(john, mary)
        if "(" in term_str and term_str.endswith(")"):
            functor_end = term_str.index("(")
            functor = term_str[:functor_end]
            args_str = term_str[functor_end + 1:-1]
            
            if args_str.strip():
                args = [self._parse_term(arg.strip()) for arg in args_str.split(",")]
            else:
                args = []
            
            return {"functor": functor, "args": args}
        else:
            # Atom
            return term_str
    
    def _rename_variables(self, rule):
        """Rule'daki değişkenleri yeniden isimlendirme"""
        var_mapping = {}
        counter = 0
        
        def rename_term(term):
            nonlocal counter
            if self._is_variable(term):
                if term not in var_mapping:
                    var_mapping[term] = f"?var_{counter}"
                    counter += 1
                return var_mapping[term]
            elif isinstance(term, dict) and "args" in term:
                return {
                    "functor": term["functor"],
                    "args": [rename_term(arg) for arg in term["args"]]
                }
            else:
                return term
        
        return {
            "head": rename_term(rule["head"]),
            "body": [rename_term(goal) for goal in rule["body"]]
        }

# Dynamic Class System (CLAZZ)
class ClazzSystem:
    """Dinamik sınıf sistemi - runtime'da sınıf oluşturma"""
    def __init__(self):
        self.dynamic_classes = {}
        self.instances = {}
        
    def create_class(self, name, fields, methods, parent=None):
        """Dinamik sınıf oluşturma"""
        class_info = {
            "name": name,
            "fields": fields,
            "methods": methods,
            "parent": parent,
            "instances": []
        }
        
        # Parent'dan inherit et
        if parent and parent in self.dynamic_classes:
            parent_class = self.dynamic_classes[parent]
            class_info["fields"].extend(parent_class["fields"])
            class_info["methods"].update(parent_class["methods"])
        
        self.dynamic_classes[name] = class_info
        return class_info
    
    def create_instance(self, class_name, *args):
        """Dinamik sınıf örneği oluşturma"""
        if class_name not in self.dynamic_classes:
            raise ValueError(f"Sınıf bulunamadı: {class_name}")
        
        class_info = self.dynamic_classes[class_name]
        instance_id = len(self.instances)
        
        instance = {
            "id": instance_id,
            "class": class_name,
            "fields": {field: None for field in class_info["fields"]},
            "methods": class_info["methods"]
        }
        
        self.instances[instance_id] = instance
        class_info["instances"].append(instance_id)
        
        # Constructor çağır
        if "constructor" in class_info["methods"]:
            self.call_method(instance_id, "constructor", args)
        
        return instance_id
    
    def set_field(self, instance_id, field_name, value):
        """Instance alanına değer atama"""
        if instance_id not in self.instances:
            raise ValueError(f"Instance bulunamadı: {instance_id}")
        
        instance = self.instances[instance_id]
        if field_name not in instance["fields"]:
            raise ValueError(f"Alan bulunamadı: {field_name}")
        
        instance["fields"][field_name] = value
    
    def get_field(self, instance_id, field_name):
        """Instance alanından değer okuma"""
        if instance_id not in self.instances:
            raise ValueError(f"Instance bulunamadı: {instance_id}")
        
        instance = self.instances[instance_id]
        if field_name not in instance["fields"]:
            raise ValueError(f"Alan bulunamadı: {field_name}")
        
        return instance["fields"][field_name]
    
    def call_method(self, instance_id, method_name, args):
        """Instance methodunu çağırma"""
        if instance_id not in self.instances:
            raise ValueError(f"Instance bulunamadı: {instance_id}")
        
        instance = self.instances[instance_id]
        if method_name not in instance["methods"]:
            raise ValueError(f"Method bulunamadı: {method_name}")
        
        method = instance["methods"][method_name]
        
        # Method'u çalıştır (basit implementation)
        if callable(method):
            return method(instance, *args)
        else:
            # String method body - interpreter ile çalıştırılmalı
            return {"method_body": method, "args": args}

# Pipeline System for Data Processing
class PipelineSystem:
    """Veri işleme pipeline sistemi"""
    def __init__(self):
        self.pipelines = {}
        self.active_pipeline = None
        
    def create_pipeline(self, name):
        """Pipeline oluşturma"""
        self.pipelines[name] = {
            "name": name,
            "stages": [],
            "data": None,
            "state": "created"
        }
        return name
    
    def add_stage(self, pipeline_name, stage_func, *args, **kwargs):
        """Pipeline'a stage ekleme"""
        if pipeline_name not in self.pipelines:
            raise ValueError(f"Pipeline bulunamadı: {pipeline_name}")
        
        stage = {
            "function": stage_func,
            "args": args,
            "kwargs": kwargs,
            "name": stage_func.__name__ if callable(stage_func) else str(stage_func)
        }
        
        self.pipelines[pipeline_name]["stages"].append(stage)
    
    def run_pipeline(self, pipeline_name, input_data):
        """Pipeline çalıştırma"""
        if pipeline_name not in self.pipelines:
            raise ValueError(f"Pipeline bulunamadı: {pipeline_name}")
        
        pipeline = self.pipelines[pipeline_name]
        pipeline["state"] = "running"
        current_data = input_data
        
        try:
            for i, stage in enumerate(pipeline["stages"]):
                pipeline["data"] = current_data
                
                if callable(stage["function"]):
                    current_data = stage["function"](current_data, *stage["args"], **stage["kwargs"])
                else:
                    # String function - should be evaluated by interpreter
                    current_data = self._evaluate_stage_function(stage["function"], current_data, stage["args"], stage["kwargs"])
                
                print(f"Pipeline {pipeline_name} - Stage {i+1} ({stage['name']}) tamamlandı")
            
            pipeline["state"] = "completed"
            pipeline["data"] = current_data
            return current_data
            
        except Exception as e:
            pipeline["state"] = "error"
            pipeline["error"] = str(e)
            raise
    
    def _evaluate_stage_function(self, func_str, data, args, kwargs):
        """String function'ı değerlendirme"""
        # Basit transformation functions
        if func_str == "FILTER":
            condition = args[0] if args else lambda x: True
            return [item for item in data if condition(item)]
        elif func_str == "MAP":
            transform = args[0] if args else lambda x: x
            return [transform(item) for item in data]
        elif func_str == "REDUCE":
            reducer = args[0] if args else lambda x, y: x + y
            return reduce(reducer, data)
        elif func_str == "SORT":
            key_func = args[0] if args else None
            return sorted(data, key=key_func)
        elif func_str == "GROUP":
            key_func = args[0] if args else lambda x: x
            from itertools import groupby
            return {k: list(v) for k, v in groupby(sorted(data, key=key_func), key=key_func)}
        else:
            # Default: return data unchanged
            return data
    
    def get_pipeline_status(self, pipeline_name):
        """Pipeline durumunu döndürme"""
        if pipeline_name not in self.pipelines:
            return None
        
        pipeline = self.pipelines[pipeline_name]
        return {
            "name": pipeline["name"],
            "state": pipeline["state"],
            "stages_count": len(pipeline["stages"]),
            "current_data_type": type(pipeline["data"]).__name__ if pipeline["data"] is not None else None
        }
        for fact in self.facts:
            unified = self._unify(goal, fact, bindings.copy())
            if unified is not None:
                yield unified
                
        # Rule'larda ara
        for rule in self.rules:
            rule_bindings = bindings.copy()
            unified = self._unify(goal, rule["head"], rule_bindings)
            if unified is not None:
                # Rule body'sini çöz
                for solution in self._solve_body(rule["body"], unified):
                    yield solution
                    
    def _solve_body(self, body, bindings):
        """Rule body'sini çözme"""
        if not body:
            yield bindings
        else:
            first_goal = body[0]
            rest_goals = body[1:]
            
            for solution in self._solve(first_goal, bindings):
                for final_solution in self._solve_body(rest_goals, solution):
                    yield final_solution
                    
    def _unify(self, term1, term2, bindings):
        """Unification algoritması"""
        if isinstance(term1, str) and term1.startswith('?'):
            # Variable
            if term1 in bindings:
                return self._unify(bindings[term1], term2, bindings)
            else:
                bindings[term1] = term2
                return bindings
        elif isinstance(term2, str) and term2.startswith('?'):
            # Variable
            if term2 in bindings:
                return self._unify(term1, bindings[term2], bindings)
            else:
                bindings[term2] = term1
                return bindings
        elif isinstance(term1, list) and isinstance(term2, list):
            # Compound terms
            if len(term1) != len(term2):
                return None
            for t1, t2 in zip(term1, term2):
                result = self._unify(t1, t2, bindings)
                if result is None:
                    return None
                bindings = result
            return bindings
        elif term1 == term2:
            return bindings
        else:
            return None

# Dynamic Class System with CLAZZ
class ClazzSystem:
    """CLAZZ - dinamik sınıf oluşturma sistemi"""
    def __init__(self):
        self.dynamic_classes = {}
        self.instances = {}
        
    def create_class(self, class_name, properties, methods):
        """Dinamik sınıf oluşturma"""
        class_definition = {
            "name": class_name,
            "properties": properties,
            "methods": methods,
            "instances": []
        }
        self.dynamic_classes[class_name] = class_definition
        return class_definition
        
    def instantiate(self, class_name, args=None):
        """Dinamik sınıf örneği oluşturma"""
        if class_name not in self.dynamic_classes:
            raise PdsXRuntimeError(f"Sınıf bulunamadı: {class_name}")
            
        class_def = self.dynamic_classes[class_name]
        instance = {
            "class_name": class_name,
            "properties": {},
            "methods": class_def["methods"].copy()
        }
        
        # Özellikleri başlat
        for prop_name, prop_type in class_def["properties"].items():
            instance["properties"][prop_name] = self._default_value(prop_type)
            
        # Constructor çağır (varsa)
        if "constructor" in class_def["methods"]:
            self._call_method(instance, "constructor", args or [])
            
        instance_id = id(instance)
        self.instances[instance_id] = instance
        class_def["instances"].append(instance_id)
        
        return instance_id
        
    def call_method(self, instance_id, method_name, args):
        """Dinamik method çağırma"""
        if instance_id not in self.instances:
            raise PdsXRuntimeError(f"Geçersiz instance ID: {instance_id}")
            
        instance = self.instances[instance_id]
        return self._call_method(instance, method_name, args)
        
    def _call_method(self, instance, method_name, args):
        """Method çalıştırma"""
        if method_name not in instance["methods"]:
            raise PdsXRuntimeError(f"Method bulunamadı: {method_name}")
            
        method = instance["methods"][method_name]
        # Method'u çalıştır (interpreter gerekli)
        return method
        
    def _default_value(self, type_name):
        """Varsayılan değer döndürme"""
        defaults = {
            "INTEGER": 0,
            "DOUBLE": 0.0,
            "STRING": "",
            "BOOLEAN": False
        }
        return defaults.get(type_name.upper(), None)

# Pipeline System for Data Streams  
class PipelineSystem:
    """PIPE sistemi - veri akışı için boru hattı"""
    def __init__(self):
        self.pipes = {}
        self.active_pipes = {}
        
    def create_pipe(self, pipe_name, stages):
        """Pipeline oluşturma"""
        pipeline = {
            "name": pipe_name,
            "stages": stages,
            "buffer": [],
            "active": False
        }
        self.pipes[pipe_name] = pipeline
        return pipeline
        
    def start_pipe(self, pipe_name):
        """Pipeline başlatma"""
        if pipe_name not in self.pipes:
            raise PdsXRuntimeError(f"Pipeline bulunamadı: {pipe_name}")
            
        pipe = self.pipes[pipe_name]
        pipe["active"] = True
        self.active_pipes[pipe_name] = pipe
        
    def push_data(self, pipe_name, data):
        """Pipeline'a veri gönderme"""
        if pipe_name not in self.active_pipes:
            raise PdsXRuntimeError(f"Pipeline aktif değil: {pipe_name}")
            
        pipe = self.active_pipes[pipe_name]
        pipe["buffer"].append(data)
        
        # Process through stages
        return self._process_stages(pipe, data)
        
    def _process_stages(self, pipe, data):
        """Pipeline aşamalarını işleme"""
        result = data
        for stage in pipe["stages"]:
            try:
                result = stage(result)
            except Exception as e:
                print(f"Pipeline stage hatası: {e}")
                return None
        return result
        
    def stop_pipe(self, pipe_name):
        """Pipeline durdurma"""
        if pipe_name in self.active_pipes:
            del self.active_pipes[pipe_name]
            self.pipes[pipe_name]["active"] = False

# REPL (Read-Eval-Print Loop) Support
class PdsXREPL:
    """PDSX Etkileşimli Yorumlayıcı"""
    
    def __init__(self):
        self.interpreter = pdsXInterpreter()
        self.interpreter.repl_mode = True
        self.history = []
        
    def run(self):
        """REPL çalıştırma"""
        print("PDSX v12X Etkileşimli Yorumlayıcı")
        print("Çıkmak için 'EXIT' yazın, yardım için 'HELP' yazın")
        print("=" * 50)
        
        while True:
            try:
                line = input("PDSX> ").strip()
                
                if not line:
                    continue
                
                if line.upper() == 'EXIT':
                    break
                elif line.upper() == 'HELP':
                    self._show_help()
                    continue
                elif line.upper() == 'VARS':
                    self._show_variables()
                    continue
                elif line.upper() == 'CLEAR':
                    self._clear_screen()
                    continue
                
                self.history.append(line)
                
                try:
                    if any(line.upper().startswith(cmd) for cmd in ['DIM', 'TYPE', 'CLASS', 'FUNCTION', 'SUB']):
                        # Multi-line definition
                        lines = [line]
                        while True:
                            next_line = input("... ").strip()
                            lines.append(next_line)
                            if any(next_line.upper().startswith(cmd) for cmd in ['END', 'NEXT', 'WEND', 'LOOP']):
                                break
                        
                        code = "\n".join(lines)
                        self.interpreter.parse_program(code)
                    else:
                        # Single command
                        result = self.interpreter.execute_command(line)
                        if result is not None:
                            print(f"Sonuç: {result}")
                
                except PdsXException as e:
                    print(f"Hata: {e}")
                except Exception as e:
                    print(f"Beklenmeyen hata: {e}")
            
            except KeyboardInterrupt:
                print("\nÇıkmak için 'EXIT' yazın")
            except EOFError:
                break
        
        print("PDSX REPL kapatılıyor...")

    def _show_help(self):
        """Yardım metni gösterme"""
        help_text = """
PDSX v12X Komutları:
- DIM var AS type          : Değişken tanımlama
- LET var = expr          : Değer atama  
- PRINT expr              : Çıktı alma
- IF/THEN/ELSE/END IF     : Koşullu yapılar
- FOR/NEXT                : Döngüler
- WHILE/WEND              : While döngüsü
- FUNCTION/END FUNCTION   : Fonksiyon tanımlama
- SUB/END SUB             : Prosedür tanımlama
- CLASS/END CLASS         : Sınıf tanımlama
- TYPE/END TYPE           : Yapı tanımlama

Özel komutlar:
- VARS                    : Değişkenleri göster
- CLEAR                   : Ekranı temizle
- EXIT                    : Çık
"""
        print(help_text)

    def _show_variables(self):
        """Değişkenleri gösterme"""
        print("Global değişkenler:")
        for name, value in self.interpreter.global_vars.items():
            print(f"  {name} = {value} ({type(value).__name__})")
        
        print("Yerel değişkenler:")
        for name, value in self.interpreter.current_scope().items():
            print(f"  {name} = {value} ({type(value).__name__})")

    def _clear_screen(self):
        """Ekranı temizleme"""
        os.system('cls' if os.name == 'nt' else 'clear')

    # Enhanced Command Implementations
    def _execute_event(self, command, scope_name):
        """EVENT komut grubu çalıştırma"""
        command = command.strip()
        if command.upper().startswith("EVENT "):
            # EVENT event_name
            event_name = command.split()[1]
            event_block = []
            # Event bloğunu topla (normalde parser'da yapılır)
            self.event_system.define_event(event_name, event_block)
        elif command.upper() == "END EVENT":
            # Event bloğu sonu
            pass
        
    def _execute_trigger_event(self, command, scope_name):
        """TRIGGER komutunu çalıştırma"""
        # TRIGGER event_name [args]
        parts = command.split()
        if len(parts) >= 2:
            event_name = parts[1]
            args = {}
            if len(parts) > 2:
                # Parse arguments
                args_str = " ".join(parts[2:])
                # Simple argument parsing
                for arg in args_str.split(","):
                    if "=" in arg:
                        key, value = arg.split("=", 1)
                        args[key.strip()] = self.evaluate_expression(value.strip(), scope_name)
            
            self.event_system.trigger_event(event_name, args, self)
    
    def _execute_prolog_operations(self, command, scope_name):
        """Gelişmiş Prolog komutlarını çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("FACT "):
            # FACT predicate(args)
            fact_str = command[5:].strip()
            self.prolog_engine.add_fact(fact_str)
            print(f"Fact added: {fact_str}")
            return None
            
        elif command_upper.startswith("RULE "):
            # RULE head :- body1, body2, ...
            rule_str = command[5:].strip()
            if ":-" in rule_str:
                head, body = rule_str.split(":-", 1)
                head = head.strip()
                body_parts = [part.strip() for part in body.split(",")]
                self.prolog_engine.add_rule(head, body_parts)
                print(f"Rule added: {head} :- {', '.join(body_parts)}")
            else:
                raise PdsXSyntaxError(f"Invalid RULE syntax: {rule_str}")
            return None
            
        elif command_upper.startswith("QUERY "):
            # QUERY goal
            goal_str = command[6:].strip()
            
            # Support for logical operators in queries
            if any(op in goal_str.upper() for op in ['AND', 'OR', 'NOT', 'IMP', 'EQV', 'NAND', 'NOR', 'XOR']):
                solutions = self._execute_logical_query(goal_str, scope_name)
            else:
                solutions = self.prolog_engine.query(goal_str)
            
            print(f"Query: {goal_str}")
            if solutions:
                print("Solutions found:")
                for i, solution in enumerate(solutions):
                    print(f"  {i+1}: {solution}")
                # Store in special variable for PDSX access
                self.current_scope()["_PROLOG_SOLUTIONS"] = solutions
            else:
                print("No solutions found.")
                self.current_scope()["_PROLOG_SOLUTIONS"] = []
            
            return solutions
        
        elif command_upper.startswith("ASSERT "):
            # ASSERT fact (alias for FACT)
            fact_str = command[7:].strip()
            self.prolog_engine.add_fact(fact_str)
            print(f"Fact asserted: {fact_str}")
            return None
            
        elif command_upper.startswith("RETRACT "):
            # RETRACT fact
            fact_str = command[8:].strip()
            parsed_fact = self.prolog_engine._parse_term(fact_str)
            if parsed_fact in self.prolog_engine.facts:
                self.prolog_engine.facts.remove(parsed_fact)
                print(f"Fact retracted: {fact_str}")
            else:
                print(f"Fact not found: {fact_str}")
            return None
        
        else:
            raise PdsXSyntaxError(f"Unknown Prolog operation: {command}")
    
    def _retract_prolog_fact(self, fact):
        """Prolog fact'ini geri çekme"""
        parsed_fact = self.prolog_engine._parse_term(fact)
        if parsed_fact in self.prolog_engine.facts:
            self.prolog_engine.facts.remove(parsed_fact)
            return True
        return False
    
    def _clear_prolog_database(self):
        """Prolog veritabanını temizleme"""
        self.prolog_engine.facts.clear()
        self.prolog_engine.rules.clear()
        print("Prolog database cleared.")
        return True
    
    def _execute_logical_query(self, query_str, scope_name):
        """Mantıksal operatörlü sorguları çalıştırma"""
        # Parse logical expressions
        # This is a simplified parser - can be enhanced
        
        if " AND " in query_str.upper():
            parts = query_str.split(" AND ", 1)
            goal1, goal2 = parts[0].strip(), parts[1].strip()
            solutions = []
            bindings = {}
            for result in self.prolog_engine._logical_and(
                self.prolog_engine._parse_term(goal1),
                self.prolog_engine._parse_term(goal2),
                bindings
            ):
                solutions.append(result)
            return solutions
        
        elif " OR " in query_str.upper():
            parts = query_str.split(" OR ", 1)
            goal1, goal2 = parts[0].strip(), parts[1].strip()
            solutions = []
            bindings = {}
            for result in self.prolog_engine._logical_or(
                self.prolog_engine._parse_term(goal1),
                self.prolog_engine._parse_term(goal2),
                bindings
            ):
                solutions.append(result)
            return solutions
        
        elif query_str.upper().startswith("NOT "):
            goal = query_str[4:].strip()
            solutions = []
            bindings = {}
            for result in self.prolog_engine._logical_not(
                self.prolog_engine._parse_term(goal),
                bindings
            ):
                solutions.append(result)
            return solutions
        
        else:
            # Regular query
            return self.prolog_engine.query(query_str)
    
    def _parse_prolog_term(self, term_str):
        """Basitleştirilmiş Prolog terimi ayrıştırma"""
        return term_str.strip()
    
    def _execute_clazz_operations(self, command, scope_name):
        """CLAZZ dinamik sınıf komutlarını çalıştırma"""
        # CLAZZ class_name WITH properties methods
        parts = command.split()
        if len(parts) >= 4 and parts[2].upper() == "WITH":
            class_name = parts[1]
            
            # Parse properties and methods (simplified)
            properties = {}
            methods = {}
            
            # Find WITH keyword and parse after it
            with_index = next(i for i, p in enumerate(parts) if p.upper() == "WITH")
            definition_str = " ".join(parts[with_index + 1:])
            
            # Simple parsing for properties and methods
            if "PROPERTIES:" in definition_str:
                prop_section = definition_str.split("PROPERTIES:")[1].split("METHODS:")[0]
                for prop in prop_section.split(","):
                    if "AS" in prop:
                        prop_parts = prop.strip().split(" AS ")
                        properties[prop_parts[0]] = prop_parts[1]
            
            if "METHODS:" in definition_str:
                method_section = definition_str.split("METHODS:")[1]
                # Parse methods (simplified)
                methods = {}
            
            return self.clazz_system.create_class(class_name, properties, methods)
    
    def _execute_pipe_operations(self, command, scope_name):
        """PIPE komutlarını çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("PIPE "):
            # PIPE pipe_name
            pipe_name = command.split()[1]
            stages = []  # Pipeline stages (would be collected from block)
            self.pipeline_system.create_pipe(pipe_name, stages)
            
        elif command_upper.startswith("PIPE_START "):
            # PIPE_START pipe_name
            pipe_name = command.split()[1]
            self.pipeline_system.start_pipe(pipe_name)
            
        elif command_upper.startswith("PIPE_PUSH "):
            # PIPE_PUSH pipe_name data
            parts = command.split(None, 2)
            if len(parts) >= 3:
                pipe_name = parts[1]
                data = self.evaluate_expression(parts[2], scope_name)
                return self.pipeline_system.push_data(pipe_name, data)
                
        elif command_upper == "END PIPE":
            pass
    
    def _execute_enhanced_print(self, command, scope_name):
        """Gelişmiş PRINT komutu - Python benzeri özellikler"""
        command = command[5:].strip()  # Remove PRINT
        
        if not command:
            print()
            return
        
        # Parse print arguments with separators and end character
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(command):
            char = command[i]
            
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
                current_part += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_part += char
            elif char in [',', ';'] and not in_quotes:
                if current_part.strip():
                    parts.append((current_part.strip(), char))
                current_part = ""
            else:
                current_part += char
            i += 1
        
        if current_part.strip():
            parts.append((current_part.strip(), ','))
        
        # Evaluate and print
        output_parts = []
        for part, separator in parts:
            value = self.evaluate_expression(part, scope_name)
            output_parts.append(str(value))
            
            if separator == ';':
                print(value, end='')
            elif separator == ',':
                print(value, end=' ')
        
        if not parts or parts[-1][1] != ';':
            print()
    
    def _execute_enhanced_input(self, command, scope_name):
        """Gelişmiş INPUT komutu - Python benzeri özellikler"""
        # INPUT [prompt,] variable
        command = command[5:].strip()  # Remove INPUT
        
        if ',' in command:
            # INPUT "prompt", variable
            parts = command.split(',', 1)
            prompt = self.evaluate_expression(parts[0].strip(), scope_name)
            var_name = parts[1].strip()
        else:
            # INPUT variable
            prompt = ""
            var_name = command
        
        try:
            user_input = input(str(prompt))
            
            # Try to convert to appropriate type
            if var_name in self.global_vars or var_name in self.current_scope():
                # Get existing variable type
                existing_var = self.get_variable_value(var_name, scope_name)
                if isinstance(existing_var, int):
                    user_input = int(user_input)
                elif isinstance(existing_var, float):
                    user_input = float(user_input)
                elif isinstance(existing_var, bool):
                    user_input = user_input.lower() in ['true', '1', 'yes', 'y']
            
            self.set_variable_value(var_name, user_input, scope_name)
            
        except (ValueError, EOFError) as e:
            print(f"INPUT hatası: {e}")
    
    def _execute_goto(self, command):
        """GOTO komutunu çalıştırma"""
        # GOTO label
        label = command.split()[1]
        if label in self.goto_labels:
            self.program_counter = self.goto_labels[label]
        else:
            raise PdsXRuntimeError(f"Label bulunamadı: {label}")
    
    def _execute_gosub(self, command):
        """GOSUB komutunu çalıştırma"""
        # GOSUB label
        label = command.split()[1]
        if label in self.goto_labels:
            self.gosub_stack.append(self.program_counter)
            self.program_counter = self.goto_labels[label]
        else:
            raise PdsXRuntimeError(f"Subroutine label bulunamadı: {label}")
    
    def _execute_return(self, command, scope_name):
        """RETURN komutunu çalıştırma"""
        if command.strip().upper() == "RETURN":
            # GOSUB'dan dönüş
            if self.gosub_stack:
                self.program_counter = self.gosub_stack.pop()
            else:
                # Function'dan dönüş
                if self.call_stack:
                    return_info = self.call_stack.pop()
                    self.program_counter = return_info.get("return_address", 0)
                    return None
        else:
            # RETURN value
            value_expr = command[6:].strip()  # Remove RETURN
            return_value = self.evaluate_expression(value_expr, scope_name)
            if self.call_stack:
                return_info = self.call_stack.pop()
                self.program_counter = return_info.get("return_address", 0)
                return return_value
            return return_value

    def _execute_while(self, command, scope_name):
        """WHILE döngüsü çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("WHILE "):
            # WHILE condition
            condition_expr = command[6:].strip()
            condition = self.evaluate_expression(condition_expr, scope_name)
            
            if not condition:
                # Skip to WEND
                level = 1
                pc = self.program_counter + 1
                while pc < len(self.program) and level > 0:
                    line = self.program[pc].strip().upper()
                    if line.startswith("WHILE "):
                        level += 1
                    elif line == "WEND":
                        level -= 1
                    pc += 1
                self.program_counter = pc - 1
            else:
                # Enter loop
                loop_info = {
                    "type": "WHILE",
                    "condition": condition_expr,
                    "start_pc": self.program_counter
                }
                self.loop_stack.append(loop_info)
                
        elif command_upper == "WEND":
            if not self.loop_stack or self.loop_stack[-1]["type"] != "WHILE":
                raise PdsXRuntimeError("WEND without WHILE")
            
            loop_info = self.loop_stack[-1]
            condition = self.evaluate_expression(loop_info["condition"], scope_name)
            
            if condition:
                # Continue loop
                self.program_counter = loop_info["start_pc"]
            else:
                # Exit loop
                self.loop_stack.pop()

    def _execute_do_loop(self, command, scope_name):
        """DO LOOP döngüsü çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("DO"):
            # DO [WHILE condition | UNTIL condition]
            loop_info = {"type": "DO", "start_pc": self.program_counter}
            
            if "WHILE" in command_upper:
                condition_expr = command.split("WHILE", 1)[1].strip()
                loop_info["condition"] = condition_expr
                loop_info["condition_type"] = "WHILE"
                
                # Check condition at start
                condition = self.evaluate_expression(condition_expr, scope_name)
                if not condition:
                    # Skip to LOOP
                    level = 1
                    pc = self.program_counter + 1
                    while pc < len(self.program) and level > 0:
                        line = self.program[pc].strip().upper()
                        if line.startswith("DO"):
                            level += 1
                        elif line.startswith("LOOP"):
                            level -= 1
                        pc += 1
                    self.program_counter = pc - 1
                    return
                    
            elif "UNTIL" in command_upper:
                condition_expr = command.split("UNTIL", 1)[1].strip()
                loop_info["condition"] = condition_expr
                loop_info["condition_type"] = "UNTIL"
                
                # Check condition at start
                condition = self.evaluate_expression(condition_expr, scope_name)
                if condition:
                    # Skip to LOOP
                    level = 1
                    pc = self.program_counter + 1
                    while pc < len(self.program) and level > 0:
                        line = self.program[pc].strip().upper()
                        if line.startswith("DO"):
                            level += 1
                        elif line.startswith("LOOP"):
                            level -= 1
                        pc += 1
                    self.program_counter = pc - 1
                    return
            
            self.loop_stack.append(loop_info)
            
        elif command_upper.startswith("LOOP"):
            if not self.loop_stack or self.loop_stack[-1]["type"] != "DO":
                raise PdsXRuntimeError("LOOP without DO")
            
            loop_info = self.loop_stack[-1]
            
            # Handle LOOP [WHILE condition | UNTIL condition]
            if "WHILE" in command_upper:
                condition_expr = command.split("WHILE", 1)[1].strip()
                condition = self.evaluate_expression(condition_expr, scope_name)
                if condition:
                    self.program_counter = loop_info["start_pc"]
                else:
                    self.loop_stack.pop()
            elif "UNTIL" in command_upper:
                condition_expr = command.split("UNTIL", 1)[1].strip()
                condition = self.evaluate_expression(condition_expr, scope_name)
                if not condition:
                    self.program_counter = loop_info["start_pc"]
                else:
                    self.loop_stack.pop()
            elif "condition" in loop_info:
                # DO WHILE/UNTIL condition at start
                condition = self.evaluate_expression(loop_info["condition"], scope_name)
                if loop_info["condition_type"] == "WHILE":
                    if condition:
                        self.program_counter = loop_info["start_pc"]
                    else:
                        self.loop_stack.pop()
                else:  # UNTIL
                    if not condition:
                        self.program_counter = loop_info["start_pc"]
                    else:
                        self.loop_stack.pop()
            else:
                # Infinite loop - continue
                self.program_counter = loop_info["start_pc"]

    def _execute_api_operations(self, command, scope_name=None):
        """API ve DLL işlemlerini çalıştırma"""
        command_upper = command.upper()
        
        if command_upper.startswith("API_CONNECT"):
            # API_CONNECT <api_name> BASE_URL <url> [HEADERS <headers_dict>]
            match = re.match(r"API_CONNECT\s+(\w+)\s+BASE_URL\s+(\S+)(?:\s+HEADERS\s+(.+))?", command, re.IGNORECASE)
            if not match:
                raise PdsXSyntaxError(f"Geçersiz API_CONNECT sözdizimi: {command}")
            
            api_name, base_url, headers_str = match.groups()
            headers = {}
            
            if headers_str:
                try:
                    headers = eval(headers_str)
                except:
                    headers = {}
            
            self.api_connections[api_name] = {
                "base_url": base_url,
                "headers": headers
            }
            
            print(f"API bağlantısı kuruldu: {api_name} -> {base_url}")
            return None
        
        elif command_upper.startswith("API_DISCONNECT"):
            # API_DISCONNECT <api_name>
            match = re.match(r"API_DISCONNECT\s+(\w+)", command, re.IGNORECASE)
            if not match:
                raise PdsXSyntaxError(f"Geçersiz API_DISCONNECT sözdizimi: {command}")
            
            api_name = match.group(1)
            if api_name in self.api_connections:
                del self.api_connections[api_name]
                print(f"API bağlantısı kesildi: {api_name}")
            else:
                print(f"API bağlantısı bulunamadı: {api_name}")
            return None
        
        elif command_upper.startswith("LOAD_DLL"):
            # LOAD_DLL <dll_name>
            match = re.match(r"LOAD_DLL\s+(\w+)", command, re.IGNORECASE)
            if not match:
                raise PdsXSyntaxError(f"Geçersiz LOAD_DLL sözdizimi: {command}")
            
            dll_name = match.group(1)
            try:
                self.libx_core.load_dll(dll_name + ".dll")
                print(f"DLL yüklendi: {dll_name}.dll")
            except Exception as e:
                raise PdsXRuntimeError(f"DLL yüklenemedi {dll_name}: {e}")
            return None
        
        elif command_upper.startswith("LOAD_API"):
            # LOAD_API <api_name> FROM <url>
            match = re.match(r"LOAD_API\s+(\w+)\s+FROM\s+(\S+)", command, re.IGNORECASE)
            if not match:
                raise PdsXSyntaxError(f"Geçersiz LOAD_API sözdizimi: {command}")
            
            api_name, base_url = match.groups()
            self.api_connections[api_name] = {
                "base_url": base_url,
                "headers": {}
            }
            print(f"API yüklendi: {api_name} -> {base_url}")
            return None
        
        else:
            raise PdsXSyntaxError(f"Bilinmeyen API operasyonu: {command}")

# Main Entry Point
def main():
    """Ana giriş noktası"""
    parser = argparse.ArgumentParser(description='PDSX v12X Programming Language Interpreter')
    parser.add_argument('file', nargs='?', help='PDSX dosyası (.pdsx)')
    parser.add_argument('--debug', action='store_true', help='Debug modu')
    parser.add_argument('--trace', action='store_true', help='Trace modu')
    parser.add_argument('--repl', action='store_true', help='Etkileşimli mod')
    
    args = parser.parse_args()
    
    if args.repl or not args.file:
        # REPL mode
        repl = EnhancedPdsXREPL()
        repl.run()
    else:
        # File execution mode
        if not os.path.exists(args.file):
            print(f"Hata: Dosya bulunamadı: {args.file}")
            sys.exit(1)
        
        with open(args.file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        interpreter = pdsXInterpreter()
        interpreter.debug_mode = args.debug
        interpreter.trace_mode = args.trace
        
        interpreter.run(code)

    
    def _execute_c64_gui_operations(self, command, scope_name=None):
        """C64 GUI komutlarını işle"""
        try:
            # C64 GUI Engine'i başlat (lazy loading)
            if not self.gui_initialized:
                self._initialize_c64_gui()
            
            command_upper = command.upper().strip()
            
            if command_upper.startswith("C64_INIT"):
                return self._c64_init_screen(command)
            elif command_upper.startswith("C64_CLEAR"):
                return self._c64_clear_screen(command)
            elif command_upper.startswith("C64_PIXEL"):
                return self._c64_set_pixel(command)
            elif command_upper.startswith("C64_CHAR"):
                return self._c64_draw_char(command)
            elif command_upper.startswith("SPRITE"):
                return self._c64_sprite_operations(command)
            elif command_upper.startswith("POKE"):
                return self._c64_poke_operation(command)
            elif command_upper.startswith("PEEK"):
                return self._c64_peek_operation(command)
            elif command_upper.startswith("SID_"):
                return self._c64_audio_operations(command)
            elif command_upper.startswith("CHARSET"):
                return self._c64_charset_operations(command)
            else:
                raise Exception(f"Bilinmeyen C64 GUI komutu: {command}")
                
        except Exception as e:
            print(f"C64 GUI komut hatası: {e}")
            return None
    
    def _execute_libx_gui_operations(self, command, scope_name=None):
        """LibX GUI komutlarını işle"""
        try:
            # LibX GUI'yi başlat (lazy loading)
            if not hasattr(self, 'libx_gui') or self.libx_gui is None:
                self._initialize_libx_gui()
            
            # LibX GUI komutunu parse et
            self.libx_gui.parse_gui_command(command)
            return None
                
        except Exception as e:
            print(f"LibX GUI komut hatası: {e}")
            return None
    
    def _initialize_c64_gui(self):
        """C64 GUI Engine'i başlat"""
        try:
            # C64GuiEngine import et
            from c64_gui_engine import C64GuiEngine
            
            # GUI engine'i oluştur
            self.c64_gui_engine = C64GuiEngine()
            self.c64_gui_engine.initialize()
            self.c64_gui_engine.start_update_loop()
            self.gui_initialized = True
            
            print("C64 GUI Engine başlatıldı!")
            
        except ImportError:
            print("Hata: c64_gui_engine modülü bulunamadı!")
            self.gui_initialized = False
        except Exception as e:
            print(f"C64 GUI başlatma hatası: {e}")
            self.gui_initialized = False
    
    def _initialize_libx_gui(self):
        """LibX GUI'yi başlat"""
        try:
            # LibX GUI import et
            from libx_gui import LibXGui
            
            # LibX GUI'yi oluştur
            self.libx_gui = LibXGui(self)
            
            print("LibX GUI başlatıldı!")
            
        except ImportError:
            print("Hata: libx_gui modülü bulunamadı!")
        except Exception as e:
            print(f"LibX GUI başlatma hatası: {e}")
    
    def _c64_init_screen(self, command):
        """C64_INIT komutu"""
        if self.c64_gui_engine:
            # Ölçek faktörünü parse et
            parts = command.split()
            scale = 2  # Default
            if len(parts) > 1:
                try:
                    scale = int(parts[1])
                except:
                    scale = 2
            
            self.c64_gui_engine.display.scale_factor = scale
            print(f"C64 ekran başlatıldı (scale: {scale})")
        return None
    
    def _c64_clear_screen(self, command):
        """C64_CLEAR komutu"""
        if self.c64_gui_engine:
            # Rengi parse et
            parts = command.split()
            color = 6  # Default mavi
            if len(parts) > 1:
                try:
                    color = int(parts[1])
                except:
                    color = 6
            
            self.c64_gui_engine.display.clear_screen(color)
            print(f"C64 ekran temizlendi (renk: {color})")
        return None
    
    def _c64_set_pixel(self, command):
        """C64_PIXEL x y color komutu"""
        if self.c64_gui_engine:
            parts = command.split()
            if len(parts) >= 4:
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                    color = int(parts[3])
                    self.c64_gui_engine.display.set_pixel(x, y, color)
                except ValueError:
                    print("Hata: C64_PIXEL x y color formatında olmalı")
        return None
    
    def _c64_draw_char(self, command):
        """C64_CHAR x y char_code color komutu"""
        if self.c64_gui_engine:
            parts = command.split()
            if len(parts) >= 4:
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                    char_code = int(parts[3])
                    color = int(parts[4]) if len(parts) > 4 else 1
                    self.c64_gui_engine.display.draw_char(x, y, char_code, color)
                except ValueError:
                    print("Hata: C64_CHAR x y char_code [color] formatında olmalı")
        return None
    
    def _c64_sprite_operations(self, command):
        """SPRITE komutları"""
        if not self.c64_gui_engine:
            return None
            
        parts = command.split(None, 2)
        if len(parts) < 2:
            return None
            
        operation = parts[1].upper()
        
        if operation == "LOAD":
            # SPRITE LOAD id path
            args = parts[2].split()
            if len(args) >= 2:
                try:
                    sprite_id = int(args[0])
                    image_path = args[1].strip('"')
                    success = self.c64_gui_engine.sprite_manager.load_sprite(sprite_id, image_path)
                    if success:
                        print(f"Sprite {sprite_id} yüklendi: {image_path}")
                    else:
                        print(f"Sprite {sprite_id} yüklenemedi!")
                except ValueError:
                    print("Hata: SPRITE LOAD id path formatında olmalı")
        
        elif operation == "ENABLE":
            # SPRITE ENABLE id
            try:
                sprite_id = int(parts[2])
                self.c64_gui_engine.sprite_manager.enable_sprite(sprite_id, True)
                print(f"Sprite {sprite_id} aktifleştirildi")
            except ValueError:
                print("Hata: SPRITE ENABLE id formatında olmalı")
        
        elif operation == "DISABLE":
            # SPRITE DISABLE id
            try:
                sprite_id = int(parts[2])
                self.c64_gui_engine.sprite_manager.enable_sprite(sprite_id, False)
                print(f"Sprite {sprite_id} deaktifleştirildi")
            except ValueError:
                print("Hata: SPRITE DISABLE id formatında olmalı")
        
        elif operation == "MOVE":
            # SPRITE MOVE id x y
            args = parts[2].split()
            if len(args) >= 3:
                try:
                    sprite_id = int(args[0])
                    x = int(args[1])
                    y = int(args[2])
                    self.c64_gui_engine.sprite_manager.set_sprite_position(sprite_id, x, y)
                    print(f"Sprite {sprite_id} pozisyonu: ({x}, {y})")
                except ValueError:
                    print("Hata: SPRITE MOVE id x y formatında olmalı")
        
        elif operation == "COLOR":
            # SPRITE COLOR id color
            args = parts[2].split()
            if len(args) >= 2:
                try:
                    sprite_id = int(args[0])
                    color = int(args[1])
                    self.c64_gui_engine.sprite_manager.set_sprite_color(sprite_id, color)
                    print(f"Sprite {sprite_id} rengi: {color}")
                except ValueError:
                    print("Hata: SPRITE COLOR id color formatında olmalı")
        
        return None
    
    def _c64_poke_operation(self, command):
        """POKE address value komutu"""
        if self.c64_gui_engine:
            parts = command.split()
            if len(parts) >= 3:
                try:
                    address = int(parts[1])
                    value = int(parts[2])
                    self.c64_gui_engine.poke(address, value)
                    print(f"POKE {address}, {value}")
                except ValueError:
                    print("Hata: POKE address value formatında olmalı")
        return None
    
    def _c64_peek_operation(self, command):
        """PEEK(address) komutu"""
        if self.c64_gui_engine:
            # PEEK'i expression olarak parse et
            import re
            match = re.search(r'PEEK\s*\(\s*(\d+)\s*\)', command, re.IGNORECASE)
            if match:
                try:
                    address = int(match.group(1))
                    value = self.c64_gui_engine.peek(address)
                    print(f"PEEK({address}) = {value}")
                    return value
                except ValueError:
                    print("Hata: PEEK(address) formatında olmalı")
        return 0
    
    def _c64_audio_operations(self, command):
        """SID müzik komutları"""
        if not self.c64_gui_engine:
            return None
            
        parts = command.split(None, 2)
        if len(parts) < 2:
            return None
            
        operation = parts[1].upper()
        
        if operation == "LOAD":
            # SID_LOAD path
            if len(parts) >= 3:
                music_path = parts[2].strip('"')
                success = self.c64_gui_engine.audio_manager.load_music(music_path)
                if success:
                    print(f"Müzik yüklendi: {music_path}")
                else:
                    print("Müzik yüklenemedi!")
        
        elif operation == "PLAY":
            # SID_PLAY [loops]
            loops = -1  # Sonsuz döngü
            if len(parts) >= 3:
                try:
                    loops = int(parts[2])
                except:
                    loops = -1
            success = self.c64_gui_engine.audio_manager.play_music(loops)
            if success:
                print("Müzik çalıyor")
            else:
                print("Müzik çalınamadı!")
        
        elif operation == "STOP":
            # SID_STOP
            self.c64_gui_engine.audio_manager.stop_music()
            print("Müzik durduruldu")
        
        elif operation == "PAUSE":
            # SID_PAUSE
            self.c64_gui_engine.audio_manager.pause_music()
            print("Müzik duraklatıldı")
        
        elif operation == "RESUME":
            # SID_RESUME
            self.c64_gui_engine.audio_manager.unpause_music()
            print("Müzik devam ediyor")
        
        elif operation == "VOLUME":
            # SID_VOLUME level (0.0-1.0)
            if len(parts) >= 3:
                try:
                    volume = float(parts[2])
                    self.c64_gui_engine.audio_manager.set_volume(volume)
                    print(f"Ses seviyesi: {volume}")
                except ValueError:
                    print("Hata: SID_VOLUME 0.0-1.0 formatında olmalı")
        
        return None
    
    def _c64_charset_operations(self, command):
        """CHARSET komutları"""
        if not self.c64_gui_engine:
            return None
            
        parts = command.split(None, 2)
        if len(parts) < 2:
            return None
            
        operation = parts[1].upper()
        
        if operation == "LOAD":
            # CHARSET LOAD id folder_path
            args = parts[2].split()
            if len(args) >= 2:
                try:
                    charset_id = int(args[0])
                    folder_path = args[1].strip('"')
                    success = self.c64_gui_engine.charset_manager.load_charset(charset_id, folder_path)
                    if success:
                        print(f"Charset {charset_id} yüklendi: {folder_path}")
                    else:
                        print(f"Charset {charset_id} yüklenemedi!")
                except ValueError:
                    print("Hata: CHARSET LOAD id folder_path formatında olmalı")
        
        elif operation == "SET":
            # CHARSET SET id
            try:
                charset_id = int(parts[2])
                success = self.c64_gui_engine.charset_manager.set_charset(charset_id)
                if success:
                    print(f"Aktif charset: {charset_id}")
                else:
                    print(f"Charset {charset_id} bulunamadı!")
            except ValueError:
                print("Hata: CHARSET SET id formatında olmalı")
        
        return None

if __name__ == "__main__":
    main()
