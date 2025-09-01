#pdsXv12.py - Ultimate Professional Development System
#Program: pdsXv12
#Author: Mete Dinler (fikir) & ChatGPT (programlama)

import os
import sys
import time
import math
import glob
import json
import ast
import re
import shutil
import random
import socket
import struct
import logging
import ctypes
import threading
import asyncio
import sqlite3
from types import SimpleNamespace
from datetime import datetime
from collections import defaultdict, namedtuple
from threading import Thread
import multiprocessing
import subprocess
import importlib.metadata
import argparse
from abc import ABC, abstractmethod

# İsteğe bağlı kütüphaneler
try:
    import requests
except ImportError:
    requests = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import psutil
except ImportError:
    psutil = None

try:
    from packaging import version
except ImportError:
    version = None

# Dependency Management  
def install_missing_libraries():
    """Check and install required dependencies."""
    required = {
        'requests': 'requests', 'packaging': 'packaging'
    }
    
    try:
        installed = {pkg.metadata['Name'].lower() for pkg in importlib.metadata.distributions()}
        missing = [lib for lib, pkg in required.items() if lib not in installed]
        
        if missing:
            print(f"Eksik kütüphaneler yükleniyor: {missing}")
            for lib in missing:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", required[lib]])
                    print(f"{lib} kuruldu.")
                except subprocess.CalledProcessError:
                    print(f"Hata: {lib} yüklenemedi, elle kurun.")
    except Exception as e:
        print(f"Kütüphane kontrolü atlandı: {e}")

# İsteğe bağlı olarak yükle
try:
    install_missing_libraries()
except:
    pass

# Loglama Ayarları
logging.basicConfig(filename='interpreter_errors.log', level=logging.ERROR,
                   format='%(asctime)s - %(message)s')

# Yardımcı Sınıflar
class ClassDef:
    def __init__(self, name, parent=None, abstract=False, interfaces=None):
        self.name = name
        self.parent = parent
        self.abstract = abstract
        self.interfaces = interfaces if interfaces else []
        self.constructor = None
        self.destructor = None
        self.methods = {}
        self.static_vars = {}
        self.is_mixin = False

class InterfaceDef:
    def __init__(self, name):
        self.name = name
        self.methods = []

class MethodDef:
    def __init__(self, name, body, params, private=False):
        self.name = name
        self.body = body
        self.params = params
        self.private = private

# Hafıza Yönetimi
class MemoryManager:
    def __init__(self):
        self.heap = {}
        self.ref_counts = {}

    def allocate(self, size: int):
        ptr = id(bytearray(size))
        self.heap[ptr] = bytearray(size)
        self.ref_counts[ptr] = 1
        return ptr

    def release(self, ptr: int):
        if ptr in self.ref_counts:
            self.ref_counts[ptr] -= 1
            if self.ref_counts[ptr] == 0:
                del self.heap[ptr]
                del self.ref_counts[ptr]

    def dereference(self, ptr: int):
        return self.heap.get(ptr, None)

    def set_value(self, ptr: int, value):
        if ptr in self.heap:
            if isinstance(value, (int, float)):
                self.heap[ptr][:] = struct.pack('d', float(value))
            elif isinstance(value, str):
                self.heap[ptr][:] = value.encode()

    def sizeof(self, obj):
        if isinstance(obj, (int, float)):
            return 8
        elif isinstance(obj, str):
            return len(obj.encode())
        elif isinstance(obj, (list, np.ndarray)):
            return obj.nbytes if hasattr(obj, 'nbytes') else len(obj) * 8
        return 0

# Yapılar (Struct ve Union)
class StructInstance:
    def __init__(self, fields, type_table):
        self.fields = {name: None for name, _ in fields}
        self.field_types = {name: type_name for name, type_name in fields}
        self.type_table = type_table
        self.sizes = {name: self._get_size(type_name) for name, type_name in fields}
        self.offsets = {}
        offset = 0
        for name in self.fields:
            self.offsets[name] = offset
            offset += self.sizes[name]

    def set_field(self, field_name, value):
        if field_name not in self.fields:
            raise ValueError(f"Geçersiz alan: {field_name}")
        expected_type = self.type_table.get(self.field_types[field_name].upper(), object)
        if not isinstance(value, expected_type):
            try:
                value = expected_type(value)
            except:
                raise TypeError(f"{field_name} için beklenen tip {expected_type.__name__}, ancak {type(value).__name__} alındı")
        self.fields[field_name] = value

    def get_field(self, field_name):
        if field_name not in self.fields:
            raise ValueError(f"Geçersiz alan: {field_name}")
        return self.fields[field_name]

    def _get_size(self, type_name):
        size_map = {
            "INTEGER": 4, "DOUBLE": 8, "STRING": 8, "BYTE": 1,
            "SHORT": 2, "LONG": 8, "SINGLE": 4, "LIST": 8, "ARRAY": 8, "DICT": 8
        }
        return size_map.get(type_name.upper(), 8)

class UnionInstance:
    def __init__(self, fields, type_table):
        self.field_types = {name: type_name for name, type_name in fields}
        self.type_table = type_table
        self.active_field = None
        self.value = bytearray(8)
        self.sizes = {name: self._get_size(type_name) for name, type_name in fields}

    def set_field(self, field_name, value):
        if field_name not in self.field_types:
            raise ValueError(f"Geçersiz alan: {field_name}")
        expected_type = self.type_table.get(self.field_types[field_name].upper(), object)
        if not isinstance(value, expected_type):
            try:
                value = expected_type(value)
            except:
                raise TypeError(f"{field_name} için beklenen tip {expected_type.__name__}, ancak {type(value).__name__} alındı")
        self.active_field = field_name
        fmt = {"INTEGER": "i", "DOUBLE": "d", "STRING": "8s", "BYTE": "b",
               "SHORT": "h", "LONG": "q", "SINGLE": "f"}.get(self.field_types[field_name].upper(), "8s")
        if fmt == "8s":
            value = str(value).encode('utf-8')[:8].ljust(8, b'\0')
        else:
            value = struct.pack(fmt, value)
        self.value[:len(value)] = value

    def get_field(self, field_name):
        if field_name not in self.field_types:
            raise ValueError(f"Geçersiz alan: {field_name}")
        if self.active_field != field_name:
            raise ValueError(f"{field_name} alanı aktif değil")
        fmt = {"INTEGER": "i", "DOUBLE": "d", "STRING": "8s", "BYTE": "b",
               "SHORT": "h", "LONG": "q", "SINGLE": "f"}.get(self.field_types[field_name].upper(), "8s")
        try:
            if fmt == "8s":
                return self.value.decode('utf-8').rstrip('\0')
            return struct.unpack(fmt, self.value[:self.sizes[field_name]])[0]
        except:
            raise ValueError(f"{field_name} alanından veri okunamadı")

    def _get_size(self, type_name):
        size_map = {
            "INTEGER": 4, "DOUBLE": 8, "STRING": 8, "BYTE": 1,
            "SHORT": 2, "LONG": 8, "SINGLE": 4, "LIST": 8, "ARRAY": 8, "DICT": 8
        }
        return size_map.get(type_name.upper(), 8)

# Pointer Sınıfı
class Pointer:
    def __init__(self, address, target_type, interpreter):
        self.address = address
        self.target_type = target_type
        self.interpreter = interpreter

    def dereference(self):
        if self.address not in self.interpreter.memory_pool:
            raise ValueError(f"Geçersiz işaretçi adresi: {self.address}")
        value = self.interpreter.memory_pool[self.address]["value"]
        expected_type = self.interpreter.type_table.get(self.target_type.upper(), object)
        if not isinstance(value, expected_type):
            raise TypeError(f"Beklenen tip {expected_type.__name__}, ancak {type(value).__name__} bulundu")
        return value

    def set(self, value):
        if self.address not in self.interpreter.memory_pool:
            raise ValueError(f"Geçersiz işaretçi adresi: {self.address}")
        expected_type = self.interpreter.type_table.get(self.target_type.upper(), object)
        if not isinstance(value, expected_type):
            try:
                value = expected_type(value)
            except:
                raise TypeError(f"Beklenen tip {expected_type.__name__}, ancak {type(value).__name__} alındı")
        self.interpreter.memory_pool[self.address]["value"] = value

    def add_offset(self, offset):
        new_address = self.address + offset
        if new_address not in self.interpreter.memory_pool:
            raise ValueError(f"Geçersiz işaretçi aritmetiği: {new_address}")
        return Pointer(new_address, self.target_type, self.interpreter)

# Event Sistemi
class Event:
    def __init__(self, event_id, trigger, action, priority=0, enabled=True, delay=0):
        self.event_id = event_id
        self.trigger = trigger
        self.action = action
        self.priority = priority
        self.enabled = enabled
        self.delay = delay
        self.last_trigger_time = 0

class EventManager:
    def __init__(self):
        self.events = {}
        self.max_events = 64
        self.active_limit = 32

    def add_event(self, trigger, action, priority=0, delay=0):
        if len(self.events) >= self.max_events:
            raise Exception("Maksimum event sayısına ulaşıldı")
        event_id = len(self.events)
        event = Event(event_id, trigger, action, priority, enabled=True, delay=delay)
        self.events[event_id] = event
        return event_id

    def remove_event(self, event_id):
        if event_id in self.events:
            del self.events[event_id]

    def enable_event(self, event_id):
        if event_id in self.events:
            self.events[event_id].enabled = True

    def disable_event(self, event_id):
        if event_id in self.events:
            self.events[event_id].enabled = False

    def trigger_event(self, event_id):
        if event_id in self.events:
            event = self.events[event_id]
            if event.enabled:
                now = time.time()
                if now - event.last_trigger_time >= event.delay:
                    event.action()
                    event.last_trigger_time = now

    def process_events(self):
        active_events = [e for e in self.events.values() if e.enabled]
        active_events.sort(key=lambda e: e.priority)
        for event in active_events[:self.active_limit]:
            if event.trigger():
                self.trigger_event(event.event_id)

    def clear(self):
        self.events.clear()

# Ana Interpreter Sınıfı
class pdsXv12:
    def __init__(self):
        self.global_vars = {}
        self.scopes = [{}]
        self.event_manager = EventManager()
        self.memory_pool = {}
        self.variable_cache = {}
        self.shared_vars = {}
        self.modules = {"libx_core": {"functions": {}}}
        self.type_table = {
            "INTEGER": int, "DOUBLE": float, "STRING": str, "BYTE": int,
            "SHORT": int, "LONG": int, "SINGLE": float, "LIST": list, "ARRAY": list, "DICT": dict
        }
        
    def current_scope(self):
        return self.scopes[-1] if self.scopes else {}

    def evaluate_expression(self, expr):
        try:
            return eval(expr, {"__builtins__": None}, {**self.global_vars, **self.current_scope()})
        except Exception as e:
            print(f"Expression hatası: {expr} -> {e}")
            return None

    def execute_command(self, cmd):
        try:
            exec(cmd, {"__builtins__": None}, {**self.global_vars, **self.current_scope()})
        except Exception as e:
            print(f"Komut hatası: {cmd} -> {e}")

    def load_file(self, filepath):
        """Dosya yükleme (.pdsx, .basx, .libx)"""
        if not os.path.exists(filepath):
            print(f"Dosya bulunamadı: {filepath}")
            return False
            
        ext = os.path.splitext(filepath)[1].lower()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if ext == '.pdsx':
                return self.execute_pdsx(content)
            elif ext == '.basx':
                return self.execute_basx(content)
            elif ext == '.libx':
                return self.execute_libx(content)
            else:
                # Genel kod dosyası olarak çalıştır
                self.execute_command(content)
                return True
                
        except Exception as e:
            print(f"Dosya yükleme hatası {filepath}: {e}")
            return False

    def execute_pdsx(self, content):
        """PDSX dosya formatını çalıştır"""
        print("PDSX dosyası çalıştırılıyor...")
        try:
            # Tüm içeriği tek seferde çalıştır
            exec(content, {"__builtins__": __builtins__}, {**self.global_vars, **self.current_scope()})
            return True
        except Exception as e:
            print(f"PDSX dosya hatası: {e}")
            return False
    
    def execute_basx(self, content):
        """BASX dosya formatını çalıştır"""
        print("BASX dosyası çalıştırılıyor...")
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    self.process_basx_line(line)
                except Exception as e:
                    print(f"BASX Satır {line_num} hatası: {e}")
        return True
    
    def execute_libx(self, content):
        """LIBX dosya formatını çalıştır"""
        print("LIBX kütüphanesi yükleniyor...")
        try:
            exec(content, {"__builtins__": None}, self.global_vars)
            print("LIBX kütüphanesi başarıyla yüklendi.")
            return True
        except Exception as e:
            print(f"LIBX yükleme hatası: {e}")
            return False

    def process_pdsx_line(self, line):
        """PDSX komutlarını işle"""
        if '=' in line:
            # Değişken ataması
            var, value = line.split('=', 1)
            var = var.strip()
            value = value.strip()
            self.current_scope()[var] = self.evaluate_expression(value)
        else:
            # Komut çalıştır
            self.execute_command(line)

    def process_basx_line(self, line):
        """BASX komutlarını işle"""
        # BASIC benzeri komutlar
        if line.upper().startswith('PRINT '):
            expr = line[6:].strip()
            result = self.evaluate_expression(expr)
            print(result)
        elif line.upper().startswith('LET '):
            # LET VAR = VALUE
            assignment = line[4:].strip()
            if '=' in assignment:
                var, value = assignment.split('=', 1)
                var = var.strip()
                value = value.strip()
                self.current_scope()[var] = self.evaluate_expression(value)
        else:
            # Genel komut
            self.execute_command(line)

    def repl(self):
        """Çok satırlı REPL ortamı"""
        print("pdsXv12 REPL - Çok satırlı mod")
        print("Çıkmak için 'exit' yazın, yardım için 'help' yazın")
        print("Çok satırlı mod: Boş satır ile komutları bitirin")
        
        while True:
            try:
                # Çok satırlı input toplama
                lines = []
                print(">>> ", end="")
                
                while True:
                    line = input()
                    if line.strip() == "":
                        break
                    lines.append(line)
                    print("... ", end="")
                
                if not lines:
                    continue
                    
                command = '\n'.join(lines)
                command = command.strip()
                
                if command.lower() == 'exit':
                    print("pdsXv12 REPL kapatılıyor...")
                    break
                elif command.lower() == 'help':
                    self.show_help()
                elif command.lower() == 'vars':
                    self.show_variables()
                elif command.startswith('load '):
                    filepath = command[5:].strip()
                    self.load_file(filepath)
                elif command.startswith('save '):
                    self.save_state(command[5:].strip())
                else:
                    # Komut çalıştır
                    if '=' in command and not any(op in command for op in ['==', '!=', '>=', '<=']):
                        # Değişken ataması
                        self.process_pdsx_line(command)
                    else:
                        # Expression veya komut
                        result = self.evaluate_expression(command)
                        if result is not None:
                            print(f"Sonuç: {result}")
                        
            except KeyboardInterrupt:
                print("\nCtrl+C - Çıkmak için 'exit' yazın")
            except EOFError:
                print("\nREPL kapatılıyor...")
                break
            except Exception as e:
                print(f"Hata: {e}")

    def show_help(self):
        """Yardım mesajları"""
        help_text = """
pdsXv12 Komutları:
- exit: REPL'den çık
- help: Bu yardım mesajını göster
- vars: Değişkenleri listele
- load <dosya>: .pdsx, .basx, .libx dosyası yükle
- save <dosya>: Mevcut durumu kaydet

Dosya Formatları:
- .pdsx: pdsX komut dosyaları
- .basx: BASIC benzeri komut dosyaları  
- .libx: Python kütüphane dosyaları

Örnekler:
- x = 10 + 5
- print(x)
- load example.pdsx
- load mylib.libx
"""
        print(help_text)

    def show_variables(self):
        """Değişkenleri göster"""
        print("Global Değişkenler:")
        for k, v in self.global_vars.items():
            print(f"  {k} = {v}")
        print("Local Değişkenler:")
        for k, v in self.current_scope().items():
            print(f"  {k} = {v}")

    def save_state(self, filepath=None):
        """Durumu kaydet"""
        if filepath is None:
            filepath = "pdsxv12_state.json"
        
        state = {
            'global_vars': self.global_vars,
            'scopes': self.scopes,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, default=str)
            print(f"Durum kaydedildi: {filepath}")
        except Exception as e:
            print(f"Kaydetme hatası: {e}")

    def load_state(self, filepath=None):
        """Durumu yükle"""
        if filepath is None:
            filepath = "pdsxv12_state.json"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            self.global_vars = state.get('global_vars', {})
            self.scopes = state.get('scopes', [{}])
            print(f"Durum yüklendi: {filepath}")
            return True
        except Exception as e:
            print(f"Yükleme hatası: {e}")
            return False

class pdsXv12Final(pdsXv12):
    def __init__(self):
        super().__init__()

    def delay(self, seconds):
        time.sleep(seconds)

def main():
    """Ana çalıştırıcı"""
    parser = argparse.ArgumentParser(description='pdsXv12 Ultimate Interpreter')
    parser.add_argument('file', nargs='?', help='Çalıştırılacak dosya (.pdsx, .basx, .libx)')
    parser.add_argument('-i', '--interactive', action='store_true', help='Etkileşimli REPL modu')
    parser.add_argument('--save-state', help='Çıkarken state kaydet')
    parser.add_argument('--load-state', help='Başlarken state yükle')
    args = parser.parse_args()

    interpreter = pdsXv12Final()
    
    # State yükleme
    if args.load_state:
        interpreter.load_state(args.load_state)

    # Dosya çalıştırma
    if args.file:
        print(f"Dosya çalıştırılıyor: {args.file}")
        interpreter.load_file(args.file)

    # REPL modu
    if args.interactive or not args.file:
        interpreter.repl()

    # State kaydetme
    if args.save_state:
        interpreter.save_state(args.save_state)

if __name__ == "__main__":
    main()

#pdsXv12 Ultimate Interpreter
