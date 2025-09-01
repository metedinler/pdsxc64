#pdsXv12u.py

#Ultimate Professional Development System

#Program: pdsXv12u

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

import requests

import pdfplumber

import numpy as np

import pandas as pd

import psutil

from types import SimpleNamespace

from datetime import datetime

from bs4 import BeautifulSoup

from collections import defaultdict, namedtuple

from packaging import version

from threading import Thread

import multiprocessing

import subprocess

import importlib.metadata

import argparse

from abc import ABC, abstractmethod

# Dependency Management

def install_missing_libraries():
    """Check and install required dependencies."""
    required = {

    'numpy': 'numpy', 'pandas': 'pandas', 'scipy': 'scipy',

    'psutil': 'psutil', 'pdfplumber': 'pdfplumber', 'bs4': 'beautifulsoup4',

    'requests': 'requests', 'packaging': 'packaging'

}

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

install_missing_libraries()

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

Yapılar (Struct ve Union)

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

Pointer Sınıfı

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

LibXCore Temel Sınıfı

class LibXCore:

def __init__(self, interpreter):

    self.interpreter = interpreter

    self.default_encoding = "utf-8"

    self.supported_encodings = [

        "utf-8", "cp1254", "iso-8859-9", "ascii", "utf-16", "utf-32",

        "cp1252", "iso-8859-1", "windows-1250", "latin-9",

        "cp932", "gb2312", "gbk", "euc-kr", "cp1251", "iso-8859-5",

        "cp1256", "iso-8859-6", "cp874", "iso-8859-7", "cp1257", "iso-8859-8"

    ]

    self.metadata = {"libx_core": {"version": "1.0.0", "dependencies": []}}

    self.stacks = {}

    self.queues = {}

    self.pipes = {}

    self.databases = {}

    self.pipe_id_counter = 0



# Genel yardımcı metodlar...

def omega(self, *args):

    params = args[:-1]

    expr = args[-1]

    return lambda *values: eval(expr, {p: v for p, v in zip(params, values)})



def list_lib(self, lib_name):

    module = self.interpreter.modules.get(lib_name, {})

    return {"functions": list(module.get("functions", {}).keys()),

            "classes": list(module.get("classes", {}).keys())}



def each(self, func, iterable):

    for item in iterable:

        func(item)



def select(self, func, iterable):

    return [item for item in iterable if func(item)]



def insert(self, collection, value, index=None, key=None):

    if isinstance(collection, list):

        if index is None:

            collection.append(value)

        else:

            collection.insert(index, value)

    elif isinstance(collection, dict):

        if key is None:

            raise Exception("DICT için anahtar gerekli")

        collection[key] = value

    else:

        raise Exception("Geçersiz veri tipi")



def remove(self, collection, index=None, key=None):

    if isinstance(collection, list):

        if index is None:

            raise Exception("Liste için indeks gerekli")

        collection.pop(index)

    elif isinstance(collection, dict):

        if key is None:

            raise Exception("DICT için anahtar gerekli")

        collection.pop(key, None)

    else:

        raise Exception("Geçersiz veri tipi")



def pop(self, collection):

    if isinstance(collection, list):

        return collection.pop()

    raise Exception("Yalnızca liste için geçerli")



def clear(self, collection):

    if isinstance(collection, (list, dict)):

        collection.clear()

    else:

        raise Exception("Geçersiz veri tipi")



def slice(self, iterable, start, end=None):

    return iterable[start:end]



def keys(self, obj):

    if isinstance(obj, dict):

        return list(obj.keys())

    raise Exception("Yalnızca DICT için geçerli")



def time_now(self):

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



def date_now(self):

    return datetime.now().strftime("%Y-%m-%d")



def timer(self):

    return time.time()



def random_int(self, min_val, max_val):

    return random.randint(min_val, max_val)



def assert_(self, condition, message):

    if not condition:

        raise Exception(f"Assert hatası: {message}")



def log(self, message, level="INFO", target=None):

    log_message = f"[{level}] {message}"

    if target:

        with open(target, "a", encoding=self.default_encoding) as f:

            f.write(log_message + "\n")

    else:

        print(log_message)



def ifthen(self, condition, value1, value2):

    return value1 if condition else value2



def exists(self, path):

    return os.path.exists(path)



def mkdir(self, path):

    os.makedirs(path, exist_ok=True)



def getenv(self, name):

    return os.getenv(name)



def exit(self, code):

    sys.exit(code)



def join_path(self, *parts):

    return os.path.join(*parts)



def copy_file(self, src, dst):

    shutil.copy(src, dst)



def move_file(self, src, dst):

    shutil.move(src, dst)



def delete_file(self, path):

    os.remove(path)



def floor(self, x):

    return math.floor(x)



def ceil(self, x):

    return math.ceil(x)



def split(self, s, sep):

    return s.split(sep)



def join(self, iterable, sep):

    return sep.join(iterable)



def read_lines(self, path):

    with open(path, "r", encoding=self.default_encoding) as f:

        return f.readlines()



def write_json(self, obj, path):

    with open(path, "w", encoding=self.default_encoding) as f:

        json.dump(obj, f)



def read_json(self, path):

    with open(path, "r", encoding=self.default_encoding) as f:

        return json.load(f)



def list_dir(self, path):

    return os.listdir(path)



def ping(self, host):

    try:

        socket.gethostbyname(host)

        return True

    except socket.error:

        return False

def sum(self, iterable):

    return sum(iterable)



def mean(self, iterable):

    return sum(iterable) / len(iterable) if iterable else 0



def min(self, iterable):

    return min(iterable) if iterable else None



def max(self, iterable):

    return max(iterable) if iterable else None



def round(self, x, digits=0):

    return round(x, digits)



def trim(self, s):

    return s.strip()



def replace(self, s, old, new):

    return s.replace(old, new)



def format(self, s, *args):

    return s.format(*args)



def trace(self):

    return traceback.format_stack()



def try_catch(self, block, handler):

    try:

        return block()

    except Exception as e:

        return handler(str(e))



def sleep(self, seconds):

    time.sleep(seconds)



def date_diff(self, date1, date2, unit="days"):

    d1 = datetime.strptime(date1, "%Y-%m-%d")

    d2 = datetime.strptime(date2, "%Y-%m-%d")

    delta = d2 - d1

    if unit == "days":

        return delta.days

    elif unit == "seconds":

        return delta.total_seconds()

    raise Exception("Geçersiz birim")



async def run_async(self, func):

    return await asyncio.to_thread(func)



def wait(self, tasks):

    for t in tasks:

        t.join()



def merge(self, col1, col2):

    if isinstance(col1, list) and isinstance(col2, list):

        return col1 + col2

    elif isinstance(col1, dict) and isinstance(col2, dict):

        return {**col1, **col2}

    raise Exception("Geçersiz veri tipi")



def sort(self, iterable, key=None):

    return sorted(iterable, key=key)



def memory_usage(self):

    process = psutil.Process()

    return process.memory_info().rss / 1024 / 1024



def cpu_count(self):

    return multiprocessing.cpu_count()



def type_of(self, value):

    if isinstance(value, int):

        return "INTEGER"

    elif isinstance(value, float):

        return "FLOAT"

    elif isinstance(value, str):

        return "STRING"

    elif isinstance(value, list):

        return "LIST"

    elif isinstance(value, dict):

        return "DICT"

    return "UNKNOWN"



def is_empty(self, collection):

    return len(collection) == 0



def len(self, obj):

    return len(obj)



def val(self, s):

    try:

        return int(s)

    except ValueError:

        try:

            return float(s)

        except ValueError:

            raise Exception(f"Geçersiz değer: {s}")



def str(self, value):

    return str(value)



def listfile(self, path, pattern="*"):

    files = glob.glob(os.path.join(path, pattern))

    return [{"name": f, "metadata": {"compressed": f.endswith(".hz")}} for f in files]



def stack(self):

    stack_id = id([])

    self.stacks[stack_id] = []

    return stack_id



def push(self, stack_id, item):

    if stack_id in self.stacks:

        self.stacks[stack_id].append(item)

    else:

        raise Exception("Geçersiz yığın")



def pop(self, stack_id):

    if stack_id in self.stacks and self.stacks[stack_id]:

        return self.stacks[stack_id].pop()

    raise Exception("Yığın boş veya geçersiz")



def queue(self):

    queue_id = id([])

    self.queues[queue_id] = []

    return queue_id



def enqueue(self, queue_id, item):

    if queue_id in self.queues:

        self.queues[queue_id].append(item)

    else:

        raise Exception("Geçersiz kuyruk")



def dequeue(self, queue_id):

    if queue_id in self.queues and self.queues[queue_id]:

        return self.queues[queue_id].pop(0)

    raise Exception("Kuyruk boş veya geçersiz")



def map(self, func, iterable):

    return [func(x) for x in iterable]



def filter(self, func, iterable):

    return [x for x in iterable if func(x)]



def reduce(self, func, iterable, initial):

    result = initial

    for x in iterable:

        result = func(result, x)

    return result



def load_hz(self, path):

    with open(path, "r", encoding=self.default_encoding) as f:

        return f.read()



def open(self, file_path, mode, encoding="utf-8"):

    return open(file_path, mode, encoding=encoding)



def load_dll(self, dll_name):

    try:

        return ctypes.WinDLL(dll_name)

    except Exception as e:

        logging.error(f"DLL yükleme hatası: {dll_name}, {e}")

        raise Exception(f"DLL yükleme hatası: {e}")



def load_api(self, url):

    return SimpleNamespace(

        ask=lambda query: requests.post(url, json={"query": query}).json().get("response", "")

    )



def version(self, lib_name):

    return self.metadata.get(lib_name, {}).get("version", "unknown")



def require_version(self, lib_name, required_version):

    current = self.version(lib_name)

    if not self._check_version(current, required_version):

        raise Exception(f"Versiyon uyumsuzluğu: {lib_name} {required_version} gerekli, {current} bulundu")



def _check_version(self, current, required):

    return version.parse(current) >= version.parse(required)



def set_encoding(self, encoding):

    if encoding in self.supported_encodings:

        self.default_encoding = encoding

    else:

        raise Exception(f"Desteklenmeyen encoding: {encoding}")



async def async_wait(self, seconds):

    await asyncio.sleep(seconds)



def pdf_read_text(self, file_path):

    if not os.path.exists(file_path):

        return "PDF bulunamadı"

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            text += page.extract_text() or ''

    return text



def pdf_extract_tables(self, file_path):

    if not os.path.exists(file_path):

        return []

    tables = []

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_tables = page.extract_tables()

            tables.extend(page_tables)

    return tables



def web_get(self, url):

    try:

        response = requests.get(url)

        return response.text

    except Exception as e:

        return f"Hata: {e}"



def database_open(self, name, path=":memory:"):

    conn = sqlite3.connect(path)

    self.databases[name] = conn



def database_close(self, name):

    if name in self.databases:

        self.databases[name].close()

        del self.databases[name]



def database_execute(self, name, sql, params=None):

    if name not in self.databases:

        raise Exception("Database açık değil")

    cur = self.databases[name].cursor()

    cur.execute(sql, params or [])

    self.databases[name].commit()



def database_query(self, name, sql, params=None):

    if name not in self.databases:

        raise Exception("Database açık değil")

    cur = self.databases[name].cursor()

    cur.execute(sql, params or [])

    return cur.fetchall()



def save_pipe(self, pipe_id, file_path, compressed=False):

    if pipe_id not in self.pipes:

        raise Exception("Boru hattı bulunamadı")

    data = self.pipes[pipe_id]

    if compressed:

        import gzip

        with gzip.open(file_path, "wt", encoding="utf-8") as f:

            json.dump(data, f)

    else:

        with open(file_path, "w", encoding="utf-8") as f:

            json.dump(data, f)



def load_pipe(self, file_path, compressed=False):

    if compressed:

        import gzip

        with gzip.open(file_path, "rt", encoding="utf-8") as f:

            data = json.load(f)

    else:

        with open(file_path, "r", encoding="utf-8") as f:

            data = json.load(f)

    pipe_id = self.pipe_id_counter

    self.pipes[pipe_id] = data

    self.pipe_id_counter += 1

    return pipe_id

# Event Sistemi - Gelişmiş

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

# Interpreter'de Event Manager Entegrasyonu

class pdsXv12: # pdsXv11 kalıtımı kaldırıldı

def __init__(self):

    # super().__init__() # Bu satır kaldırıldı

    self.global_vars = {}

    self.scopes = [{}]

    self.event_manager = EventManager()

    self.pipe_storage = {}

    self.databases = {}

    self.pipe_id_counter = 0

    self.pipes = {}

    self.auto_database = None

    self.memory_pool = {}

    self.variable_cache = {}

    self.shared_vars = {}

    self.modules = {"libx_core": {"functions": {}}}

    self.type_table = {

        "INTEGER": int, "DOUBLE": float, "STRING": str, "BYTE": int,

        "SHORT": int, "LONG": int, "SINGLE": float, "LIST": list, "ARRAY": list, "DICT": dict

    }



def define_event(self, trigger_expr, action_expr, priority=0, delay=0):

    trigger = lambda: self.evaluate_expression(trigger_expr)

    action = lambda: self.execute_command(action_expr)

    return self.event_manager.add_event(trigger, action, priority=priority, delay=delay)



def process_all_events(self):

    self.event_manager.process_events()



def save_pipeline(self, varname, filename, compressed=False):

    if varname not in self.current_scope():

        raise Exception("Boru hattı bulunamadı")

    data = self.current_scope()[varname]

    if compressed:

        import gzip

        with gzip.open(filename, "wt", encoding="utf-8") as f:

            json.dump(data, f)

    else:

        with open(filename, "w", encoding="utf-8") as f:

            json.dump(data, f)



def load_pipeline(self, filename, compressed=False):

    if compressed:

        import gzip

        with gzip.open(filename, "rt", encoding="utf-8") as f:

            data = json.load(f)

    else:

        with open(filename, "r", encoding="utf-8") as f:

            data = json.load(f)

    varname = f"pipe_{self.pipe_id_counter}"

    self.current_scope()[varname] = data

    self.pipe_id_counter += 1

    return varname



def open_database(self, name, path=":memory:"):

    conn = sqlite3.connect(path)

    self.databases[name] = conn

    if self.auto_database is None:

        self.auto_database = name



def close_database(self, name):

    if name in self.databases:

        self.databases[name].close()

        del self.databases[name]

        if self.auto_database == name:

            self.auto_database = None



def exec_sql(self, sql, params=None, db=None):

    if db is None:

        db = self.auto_database

    if db not in self.databases:

        raise Exception(f"Database bulunamadı: {db}")

    cur = self.databases[db].cursor()

    cur.execute(sql, params or [])

    self.databases[db].commit()



def query_sql(self, sql, params=None, db=None):

    if db is None:

        db = self.auto_database

    if db not in self.databases:

        raise Exception(f"Database bulunamadı: {db}")

    cur = self.databases[db].cursor()

    cur.execute(sql, params or [])

    return cur.fetchall()



def sql_pipeline(self, sql, db=None, map_func=None, filter_func=None):

    rows = self.query_sql(sql, db=db)

    if map_func:

        rows = [map_func(row) for row in rows]

    if filter_func:

        rows = [row for row in rows if filter_func(row)]

    return rows

# Yardımcı Utilities

def safe_eval(expr, interpreter):

    try:

        return eval(expr, {"__builtins__": None}, interpreter.global_vars)

    except Exception as e:

        print(f"Değerlendirme hatası: {expr} -> {e}")

        return None

# Interpreter Ekstra Fonksiyonlar

def patch_interpreter(interpreter):

    def list_databases():

        return list(interpreter.databases.keys())

    interpreter.list_databases = list_databases

# pdsXv12 Ana Yapı Başlatıcı

class pdsXv12Final(pdsXv12):

def __init__(self):

    super().__init__()



def delay(self, seconds):

    time.sleep(seconds)

# Yeni Ana Çalıştırıcı

def main():

parser = argparse.ArgumentParser(description='pdsXv12 Ultimate Interpreter')

parser.add_argument('file', nargs='?', help='Çalıştırılacak dosya')

parser.add_argument('-i', '--interactive', action='store_true', help='Etkileşimli mod')

parser.add_argument('--save-state', action='store_true', help='Çıkarken state kaydet')

parser.add_argument('--load-state', action='store_true', help='Başlarken state yükle')

args = parser.parse_args()



interpreter = pdsXv12Final()

if args.load_state:

    interpreter.load_state()



if args.file:

    with open(args.file, 'r', encoding='utf-8') as f:

        code = f.read()

    # interpreter.run(code) # run metodu pdsXv12'de tanımlı değil, bu yüzden yoruma alındı



if args.interactive or not args.file:

    # interpreter.repl() # repl metodu pdsXv12'de tanımlı değil, bu yüzden yoruma alındı

    print("Etkileşimli mod şu anda desteklenmiyor.")



if args.save_state:

    interpreter.save_state()

if __name__ == "__main__":

main()

#pdsXv12 Ultimate Interpreter