#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C64 Memory Map and ROM Routine Manager
C64 KERNAL, BASIC, Memory Map ve Zero Page bilgilerini yöneten modül

🍎 C64 Memory Map and ROM Routine Manager v5.3 - Commodore 64 Geliştirme Stüdyosu
================================================================
PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: c64_memory_manager.py - C64 Memory Map ve ROM Routine Manager  
VERSİYON: 5.3 (C64 ROM Data Full Integration - KERNAL + BASIC + Memory Maps)
AMAÇ: C64 KERNAL, BASIC, Memory Map ve Zero Page bilgilerini yönetme
================================================================

Bu modül şu özelliklerle C64 sistem bilgilerini yönetir:
• KERNAL Routines: C64 KERNAL sistem çağrıları ve rutinleri
• BASIC Routines: C64 BASIC V2 rutinleri ve token sistemi
• Memory Map: Tam C64 bellek haritası (Zero Page, I/O, ROM/RAM)
• Special Addresses: Sistem pointerleri ve özel adresler
• ROM Data Integration: c64_rom_data klasöründen otomatik yükleme

C64 ROM Data Klasörü Entegrasyonu:
- memory_maps/c64_memory_map.json (15 memory regions)
- kernal_routines/*.json (KERNAL system calls)
- basic_routines/*.json (BASIC V2 tokens and routines)
================================================================
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

class C64MemoryMapManager:
    """C64 Memory Map ve ROM rutinlerini yöneten sınıf"""
    
    def __init__(self, rom_data_dir="c64_rom_data"):
        self.rom_data_dir = Path(rom_data_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Data containers
        self.kernal_routines = {}
        self.basic_routines = {}
        self.memory_map = {}
        self.zeropage_vars = {}
        self.io_registers = {}
        self.special_addresses = {}
        self.c64_labels = {}             # Yeni: 9187 lines C64 labels database
        self.basic_tokens = {}           # Yeni: BASIC token database  
        self.system_pointers = {}        # Yeni: System pointer database
        self.unified_lookup = {}         # Yeni: Unified address lookup
        
        # Load all data
        self.load_all_data()
    
    def load_all_data(self):
        """Tüm C64 ROM ve memory map verilerini yükle"""
        try:
            self.load_kernal_routines()
            self.load_basic_routines()
            self.load_memory_map()
            self.load_zeropage_data()
            self.load_io_registers()
            # self.load_c64_labels()           # Şimdilik devre dışı - Enhanced version'da
            # self.load_basic_tokens()         # Şimdilik devre dışı - Enhanced version'da
            # self.load_system_pointers()      # Şimdilik devre dışı - Enhanced version'da
            self.logger.info("C64 Memory Map data başarıyla yüklendi")
        except Exception as e:
            self.logger.error(f"C64 Memory Map data yükleme hatası: {e}")
    
    def load_kernal_routines(self):
        """KERNAL rutinlerini yükle"""
        kernal_file = self.rom_data_dir / "kernal" / "kernal_routines.json"
        if kernal_file.exists():
            with open(kernal_file, 'r', encoding='utf-8') as f:
                self.kernal_routines = json.load(f)
        else:
            # Varsayılan KERNAL rutinleri
            self.kernal_routines = {
                "65490": {  # $FFD2
                    "name": "CHROUT",
                    "description": "Karakter çıktısı",
                    "c_equivalent": "putchar(A)",
                    "qbasic_equivalent": "PRINT CHR$(A)",
                    "parameters": ["A: output character"],
                    "comment_tr": "Ekrana karakter yazdır",
                    "comment_en": "Output character to current device"
                },
                "65487": {  # $FFCF  
                    "name": "CHRIN",
                    "description": "Karakter girişi",
                    "c_equivalent": "A = getchar()",
                    "qbasic_equivalent": "A = ASC(INPUT$(1))",
                    "parameters": ["return: A = input character"],
                    "comment_tr": "Klavyeden karakter oku",
                    "comment_en": "Input character from current device"
                },
                "65508": {  # $FFE4
                    "name": "GETIN", 
                    "description": "Klavye tarama",
                    "c_equivalent": "A = kbhit() ? getch() : 0",
                    "qbasic_equivalent": "A = INKEY$",
                    "parameters": ["return: A = key code or 0"],
                    "comment_tr": "Tuşa basılmışsa oku",
                    "comment_en": "Get character from keyboard queue"
                },
                "58692": {  # $E544
                    "name": "CLRSCR",
                    "description": "Ekran silme",
                    "c_equivalent": "clear_screen()",
                    "qbasic_equivalent": "CLS",
                    "parameters": [],
                    "comment_tr": "Ekranı temizle",
                    "comment_en": "Clear screen"
                }
            }
    
    def load_basic_routines(self):
        """BASIC rutinlerini yükle"""
        basic_file = self.rom_data_dir / "basic" / "basic_routines.json"
        if basic_file.exists():
            with open(basic_file, 'r', encoding='utf-8') as f:
                self.basic_routines = json.load(f)
        else:
            # Varsayılan BASIC rutinleri
            self.basic_routines = {
                "43121": {  # $A871
                    "name": "STRING_LENGTH",
                    "description": "String uzunluğu",
                    "c_equivalent": "strlen(string)",
                    "qbasic_equivalent": "LEN(string$)",
                    "parameters": ["string pointer"],
                    "comment_tr": "String uzunluğunu hesapla",
                    "comment_en": "Calculate string length"
                },
                "43371": {  # $A96B
                    "name": "MID_STRING",
                    "description": "String ortası",
                    "c_equivalent": "substr(string, start, length)",
                    "qbasic_equivalent": "MID$(string$, start, length)",
                    "parameters": ["string pointer", "start", "length"],
                    "comment_tr": "String'in bir kısmını al",
                    "comment_en": "Extract substring"
                }
            }
    
    def load_memory_map(self):
        """Memory map verilerini yükle"""
        memory_file = self.rom_data_dir / "memory_maps" / "c64_memory_map.json"
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                self.memory_map = json.load(f)
        else:
            # Varsayılan memory map
            self.memory_map = {
                "1024": {  # $0400
                    "end_addr": 2023,  # $07E7
                    "name": "SCREEN_MEMORY",
                    "description": "Screen RAM",
                    "c_equivalent": "screen",
                    "qbasic_equivalent": "SCREEN",
                    "comment_tr": "Ekran belleği",
                    "comment_en": "Default screen memory"
                },
                "55296": {  # $D800
                    "end_addr": 56295,  # $DBE7
                    "name": "COLOR_RAM",
                    "description": "Color RAM",
                    "c_equivalent": "color",
                    "qbasic_equivalent": "COLOR",
                    "comment_tr": "Renk belleği",
                    "comment_en": "Color memory"
                }
            }
    
    def load_zeropage_data(self):
        """Zero page verilerini yükle"""
        zp_file = self.rom_data_dir / "zeropage" / "zeropage_vars.json"
        if zp_file.exists():
            with open(zp_file, 'r', encoding='utf-8') as f:
                self.zeropage_vars = json.load(f)
        else:
            # Varsayılan zero page değişkenleri
            self.zeropage_vars = {
                "2": {
                    "name": "USER_VAR1",
                    "size": 1,
                    "description": "User variable 1",
                    "c_equivalent": "user_var1",
                    "qbasic_equivalent": "UserVar1",
                    "comment_tr": "Kullanıcı değişkeni 1",
                    "comment_en": "User variable 1"
                },
                "122": {  # $7A
                    "name": "TXTPTR",
                    "size": 2,
                    "description": "BASIC text pointer",
                    "c_equivalent": "basic_text_ptr",
                    "qbasic_equivalent": "BasicTextPtr",
                    "comment_tr": "BASIC metin pointer'ı",
                    "comment_en": "Pointer to current BASIC statement"
                }
            }
    
    def load_io_registers(self):
        """I/O register verilerini yükle"""
        io_file = self.rom_data_dir / "kernal" / "io_registers.json"
        if io_file.exists():
            with open(io_file, 'r', encoding='utf-8') as f:
                self.io_registers = json.load(f)
        else:
            # Varsayılan I/O registerları
            self.io_registers = {
                "53280": {  # $D020
                    "name": "BORDER_COLOR",
                    "description": "Border color",
                    "bits": "0-3: color",
                    "c_equivalent": "border_color",
                    "qbasic_equivalent": "BorderColor",
                    "comment_tr": "Çerçeve rengi",
                    "comment_en": "Screen border color"
                }
            }
    
    def get_routine_info(self, address: int) -> Optional[Dict[str, Any]]:
        """Adres için rutin bilgisini al"""
        addr_str = str(address)
        
        # KERNAL rutini ara
        if addr_str in self.kernal_routines:
            routine = self.kernal_routines[addr_str].copy()
            routine['type'] = 'kernal'
            return routine
        
        # BASIC rutini ara
        if addr_str in self.basic_routines:
            routine = self.basic_routines[addr_str].copy()
            routine['type'] = 'basic'
            return routine
        
        return None
    
    def get_memory_info(self, address: int) -> Optional[Dict[str, Any]]:
        """Adres için memory bilgisini al"""
        addr_str = str(address)
        
        # Zero page değişkeni ara
        if address < 256 and addr_str in self.zeropage_vars:
            var_info = self.zeropage_vars[addr_str].copy()
            var_info['type'] = 'zeropage'
            return var_info
        
        # I/O register ara
        if addr_str in self.io_registers:
            io_info = self.io_registers[addr_str].copy()
            io_info['type'] = 'io_register'
            return io_info
        
        # Memory area ara
        for start_addr_str, area_info in self.memory_map.items():
            start_addr = int(start_addr_str)
            end_addr = area_info.get('end_addr', start_addr)
            if start_addr <= address <= end_addr:
                area = area_info.copy()
                area['type'] = 'memory_area'
                area['offset'] = address - start_addr
                return area
        
        return None
    
    def format_routine_call(self, address: int, output_format: str = 'c') -> str:
        """Rutin çağrısını belirtilen formatta formatla"""
        routine_info = self.get_routine_info(address)
        if not routine_info:
            return f"unknown_routine_{address:04X}()"
        
        if output_format == 'c':
            return routine_info.get('c_equivalent', f"{routine_info['name'].lower()}()")
        elif output_format == 'qbasic':
            return routine_info.get('qbasic_equivalent', routine_info['name'])
        elif output_format == 'pseudo':
            return f"call {routine_info['name']} // {routine_info.get('comment_tr', routine_info['description'])}"
        else:
            return routine_info['name']
    
    def format_memory_access(self, address: int, output_format: str = 'c') -> str:
        """Memory erişimini belirtilen formatta formatla"""
        memory_info = self.get_memory_info(address)
        if not memory_info:
            return f"memory[{address:04X}]"
        
        if output_format == 'c':
            if memory_info['type'] == 'memory_area' and 'offset' in memory_info:
                return f"{memory_info.get('c_equivalent', 'memory')}[{memory_info['offset']}]"
            return memory_info.get('c_equivalent', f"mem_{address:04X}")
        elif output_format == 'qbasic':
            if memory_info['type'] == 'memory_area' and 'offset' in memory_info:
                return f"{memory_info.get('qbasic_equivalent', 'MEMORY')}({memory_info['offset']})"
            return memory_info.get('qbasic_equivalent', f"MEM({address})")
        elif output_format == 'pseudo':
            return f"{memory_info['name']} // {memory_info.get('comment_tr', memory_info['description'])}"
        else:
            return memory_info['name']

# Global instance
c64_memory_manager = C64MemoryMapManager()

# Kolay kullanım fonksiyonları
def get_routine_info(address: int) -> Optional[Dict[str, Any]]:
    """Rutin bilgisini al"""
    return c64_memory_manager.get_routine_info(address)

def get_memory_info(address: int) -> Optional[Dict[str, Any]]:
    """Memory bilgisini al"""
    return c64_memory_manager.get_memory_info(address)

def format_routine_call(address: int, output_format: str = 'c') -> str:
    """Rutin çağrısını formatla"""
    return c64_memory_manager.format_routine_call(address, output_format)

def format_memory_access(address: int, output_format: str = 'c') -> str:
    """Memory erişimini formatla"""
    return c64_memory_manager.format_memory_access(address, output_format)
