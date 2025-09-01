#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C64 Memory Manager - Enhanced memory management for C64 systems
"""
import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

class EnhancedC64MemoryManager:
    """Enhanced C64 Memory Manager with ROM/RAM mapping"""
    
    def __init__(self):
        self.basic_tokens = {}
        self.rom_data_dir = Path(__file__).parent / "rom_data"
        self.memory_map = {}
        self.load_basic_tokens()
    
    def load_basic_tokens(self):
        """BASIC Token veritabanını yükle - Türkçe açıklamalı"""
        tokens_file = self.rom_data_dir / "basic" / "basic_tokens_clean.json"
        if tokens_file.exists():
            try:
                with open(tokens_file, 'r', encoding='utf-8') as f:
                    self.basic_tokens = json.load(f)
                self.logger.info(f"BASIC Tokens yüklendi: {len(self.basic_tokens)} entry")
            except Exception as e:
                self.logger.error(f"BASIC Tokens yükleme hatası: {e}")
                self.basic_tokens = {}
        else:
            self.basic_tokens = {}
        
        """
        ROM DATA Full Integration
        C64 KERNAL, BASIC, Memory Map ve Zero Page bilgilerini yöneten gelişmiş modül
        Enhanced C64 Memory Manager 
        v5.3 - Commodore 64 Geliştirme Stüdyosu
        ================================================================
        PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
        MODÜL: enhanced_c64_memory_manager.py - Enhanced C64 Memory Manager
        VERSİYON: 5.3 (C64 ROM DATA Full Integration + 9187 Lines C64 Labels Database)
        AMAÇ: C64 Memory Manager'ın gelişmiş versiyonu - kapsamlı ROM DATA entegrasyonu
        ================================================================

        Bu modül şu özelliklerle C64 Memory Manager'ı genişletir:
        • 9187 Lines C64 Labels Database: Kapsamlı adres etiketleme sistemi
        • Enhanced BASIC Tokens: Türkçe açıklama destekli token veritabanı
        • System Pointers: Gelişmiş sistem pointer yönetimi
        • Unified Address Lookup: Birleşik adres arama motoru
        • ROM DATA Full Integration: Tüm c64_rom_data klasörü entegrasyonu

        Extends: c64_memory_manager.py (base class)
        """
================================================================
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

# Orijinal c64_memory_manager'ı import et
from c64_memory_manager import C64MemoryMapManager

class EnhancedC64MemoryManager(C64MemoryMapManager):
    """C64 Memory Manager'ın gelişmiş versiyonu - ROM DATA entegrasyonu ile"""
    
    def __init__(self, rom_data_dir="c64_rom_data"):
        super().__init__(rom_data_dir)
        
        # Enhanced data containers
        self.c64_labels = {}             # 9187 lines C64 labels database
        self.basic_tokens = {}           # BASIC token database  
        self.system_pointers = {}        # System pointer database
        self.unified_lookup = {}         # Unified address lookup
        
        # Load enhanced data
        self.load_enhanced_data()
    
    def load_enhanced_data(self):
        """Gelişmiş veri setlerini yükle"""
        try:
            self.load_c64_labels()
            self.load_basic_tokens()
            self.load_system_pointers()
            self.build_unified_lookup()
            self.logger.info("Enhanced C64 Memory Manager data yüklendi")
        except Exception as e:
            self.logger.error(f"Enhanced data yükleme hatası: {e}")
    
    def load_c64_labels(self):
        """C64 Labels database'ini yükle (9187 entries)"""
        labels_file = self.rom_data_dir / "eski" / "c64labels.json"
        if labels_file.exists():
            try:
                with open(labels_file, 'r', encoding='utf-8') as f:
                    self.c64_labels = json.load(f)
                self.logger.info(f"C64 Labels yüklendi: {len(self.c64_labels)} entry")
            except Exception as e:
                self.logger.error(f"C64 Labels yükleme hatası: {e}")
                self.c64_labels = {}
        else:
            self.c64_labels = {}
    
    def load_basic_tokens(self):
        """BASIC token database'ini yükle"""
        tokens_file = self.rom_data_dir / "eski" / "basic_tokens.json"
        if tokens_file.exists():
            try:
                with open(tokens_file, 'r', encoding='utf-8') as f:
                    self.basic_tokens = json.load(f)
                self.logger.info(f"BASIC Tokens yüklendi: {len(self.basic_tokens)} entry")
            except Exception as e:
                self.logger.error(f"BASIC Tokens yükleme hatası: {e}")
                self.basic_tokens = {}
        else:
            self.basic_tokens = {}
    
    def load_system_pointers(self):
        """System pointer database'ini yükle"""
        pointers_file = self.rom_data_dir / "eski" / "system_pointers.json"
        if pointers_file.exists():
            try:
                with open(pointers_file, 'r', encoding='utf-8') as f:
                    self.system_pointers = json.load(f)
                self.logger.info(f"System Pointers yüklendi: {len(self.system_pointers)} entry")
            except Exception as e:
                self.logger.error(f"System Pointers yükleme hatası: {e}")
                self.system_pointers = {}
        else:
            self.system_pointers = {}
    
    def build_unified_lookup(self):
        """Tüm database'leri unified lookup table'a birleştir"""
        self.unified_lookup = {}
        
        # KERNAL routines (highest priority)
        for addr_str, info in self.kernal_routines.items():
            try:
                # Parse address string formats
                addr_str = str(addr_str).strip()
                if addr_str.startswith('$'):
                    address = int(addr_str[1:], 16)
                elif addr_str.startswith('0x'):
                    address = int(addr_str, 16)
                elif addr_str.isdigit():
                    address = int(addr_str)
                else:
                    # Try to parse as hex without prefix
                    try:
                        address = int(addr_str, 16)
                    except ValueError:
                        continue  # Skip invalid formats
                
                self.unified_lookup[address] = {
                    'name': info.get('name', f'KERNAL_{address:04X}') if isinstance(info, dict) else str(info),
                    'type': 'kernal_routine',
                    'description': info.get('description', '') if isinstance(info, dict) else '',
                    'c_equivalent': info.get('c_equivalent', '') if isinstance(info, dict) else '',
                    'qbasic_equivalent': info.get('qbasic_equivalent', '') if isinstance(info, dict) else '',
                    'pdsx_equivalent': info.get('qbasic_equivalent', '') if isinstance(info, dict) else '',  # PDSx = QBasic for now
                    'comment': info.get('comment_tr', '') if isinstance(info, dict) else '',
                    'priority': 10
                }
            except (ValueError, KeyError, AttributeError) as e:
                self.logger.debug(f"Skipping invalid KERNAL entry: {addr_str} - {e}")
                continue
        
        # BASIC routines  
        for addr_str, info in self.basic_routines.items():
            try:
                # Parse address string formats
                addr_str = str(addr_str).strip()
                if addr_str.startswith('$'):
                    address = int(addr_str[1:], 16)
                elif addr_str.startswith('0x'):
                    address = int(addr_str, 16)
                elif addr_str.isdigit():
                    address = int(addr_str)
                else:
                    # Try to parse as hex without prefix
                    try:
                        address = int(addr_str, 16)
                    except ValueError:
                        continue  # Skip invalid formats
                
                if address not in self.unified_lookup:  # Don't override KERNAL
                    self.unified_lookup[address] = {
                        'name': info.get('name', f'BASIC_{address:04X}') if isinstance(info, dict) else str(info),
                        'type': 'basic_routine',
                        'description': info.get('description', '') if isinstance(info, dict) else '',
                        'c_equivalent': info.get('c_equivalent', '') if isinstance(info, dict) else '',
                        'qbasic_equivalent': info.get('qbasic_equivalent', '') if isinstance(info, dict) else '',
                        'pdsx_equivalent': info.get('qbasic_equivalent', '') if isinstance(info, dict) else '',
                        'comment': info.get('comment_tr', '') if isinstance(info, dict) else '',
                        'priority': 9
                    }
            except (ValueError, KeyError, AttributeError) as e:
                self.logger.debug(f"Skipping invalid BASIC entry: {addr_str} - {e}")
                continue
        
        # C64 Labels (comprehensive database)
        for addr_str, info in self.c64_labels.items():
            try:
                # Parse address string formats
                addr_str = str(addr_str).strip()  # Ensure string and strip whitespace
                if addr_str.startswith('$'):
                    address = int(addr_str[1:], 16)
                elif addr_str.startswith('0x'):
                    address = int(addr_str, 16)
                elif addr_str.isdigit():
                    address = int(addr_str)
                else:
                    # Try to parse as hex without prefix
                    try:
                        address = int(addr_str, 16)
                    except ValueError:
                        continue  # Skip invalid formats
                
                # Only add if not already set with higher priority
                if address not in self.unified_lookup:
                    name = info.get('name', f'ADDR_{address:04X}') if isinstance(info, dict) else str(info)
                    self.unified_lookup[address] = {
                        'name': name,
                        'type': info.get('type', 'memory_location') if isinstance(info, dict) else 'memory_location',
                        'description': info.get('description', '') if isinstance(info, dict) else '',
                        'c_equivalent': self._generate_c_name(name),
                        'qbasic_equivalent': f'PEEK({address})',
                        'pdsx_equivalent': f'PEEK({address})',
                        'comment': info.get('comment', '') if isinstance(info, dict) else '',
                        'priority': 8
                    }
            except (ValueError, KeyError, AttributeError) as e:
                self.logger.debug(f"Skipping invalid address entry: {addr_str} - {e}")
                continue
        
        # Zero page variables
        for addr_str, info in self.zeropage_vars.items():
            address = int(addr_str)
            if address not in self.unified_lookup:  # Don't override higher priority
                self.unified_lookup[address] = {
                    'name': info.get('name', f'ZP_{address:02X}'),
                    'type': 'zeropage_var',
                    'description': info.get('description', ''),
                    'c_equivalent': info.get('c_equivalent', f'zp_{address:02x}'),
                    'qbasic_equivalent': info.get('qbasic_equivalent', f'ZP{address}'),
                    'pdsx_equivalent': info.get('qbasic_equivalent', f'ZP{address}'),
                    'comment': info.get('comment_tr', ''),
                    'priority': 7
                }
        
        # I/O Registers
        for addr_str, info in self.io_registers.items():
            address = int(addr_str)
            if address not in self.unified_lookup:
                self.unified_lookup[address] = {
                    'name': info.get('name', f'IO_{address:04X}'),
                    'type': 'io_register',
                    'description': info.get('description', ''),
                    'c_equivalent': info.get('c_equivalent', f'io_reg_{address:04x}'),
                    'qbasic_equivalent': info.get('qbasic_equivalent', f'PEEK({address})'),
                    'pdsx_equivalent': info.get('qbasic_equivalent', f'PEEK({address})'),
                    'comment': info.get('comment_tr', ''),
                    'priority': 6
                }
        
        self.logger.info(f"Unified lookup table oluşturuldu: {len(self.unified_lookup)} address")
    
    def _generate_c_name(self, original_name: str) -> str:
        """C dili için geçerli değişken ismi oluştur"""
        if not original_name:
            return "unknown_var"
        
        # C naming conventions
        c_name = original_name.lower()
        c_name = c_name.replace(' ', '_')
        c_name = c_name.replace('-', '_')
        c_name = c_name.replace('.', '_')
        c_name = c_name.replace('$', '_')
        
        # Remove invalid characters
        import re
        c_name = re.sub(r'[^a-zA-Z0-9_]', '_', c_name)
        
        # Ensure it starts with letter or underscore
        if c_name and c_name[0].isdigit():
            c_name = f"var_{c_name}"
        
        return c_name if c_name else "unnamed_var"
    
    def get_smart_variable_name(self, address: int, access_type: str = 'read') -> str:
        """Adrese göre akıllı değişken ismi üret"""
        if not self.unified_lookup:
            self.build_unified_lookup()
        
        if address in self.unified_lookup:
            info = self.unified_lookup[address]
            return info['name']
        
        # Fallback: Synthetic name generation based on memory regions
        if 0x0000 <= address <= 0x00FF:
            return f"zp_{address:02X}"
        elif 0x0100 <= address <= 0x01FF:
            return f"stack_{address:02X}"
        elif 0x0200 <= address <= 0x02FF:
            return f"user_{address:03X}"
        elif 0x0400 <= address <= 0x07E7:
            return f"screen_{address - 0x0400:03X}"
        elif 0x0800 <= address <= 0x9FFF:
            return f"ram_{address:04X}"
        elif 0xA000 <= address <= 0xBFFF:
            return f"basic_rom_{address:04X}"
        elif 0xC000 <= address <= 0xCFFF:
            return f"ram_c_{address:04X}"
        elif 0xD000 <= address <= 0xDFFF:
            return f"io_{address:04X}"
        elif 0xE000 <= address <= 0xFFFF:
            return f"kernal_rom_{address:04X}"
        else:
            return f"addr_{address:04X}"
    
    def get_format_translation(self, address: int, target_format: str, access_type: str = 'read') -> str:
        """Format-specific çeviri al"""
        if not self.unified_lookup:
            self.build_unified_lookup()
        
        if address in self.unified_lookup:
            info = self.unified_lookup[address]
            
            if target_format == 'c':
                base = info.get('c_equivalent', f'memory[{address}]')
                if access_type == 'read':
                    return base
                else:  # write
                    return f"{base} = "
                    
            elif target_format in ['qbasic', 'pdsx']:
                if access_type == 'read':
                    return info.get('qbasic_equivalent', f'PEEK({address})')
                else:  # write  
                    return f"POKE {address}, "
                    
            elif target_format == 'pseudo':
                name = info['name']
                if access_type == 'read':
                    return f"READ {name}"
                else:
                    return f"WRITE {name}"
        
        # Fallback translations
        if target_format == 'c':
            var_name = self.get_smart_variable_name(address)
            if access_type == 'read':
                return f"memory[0x{address:04X}] /* {var_name} */"
            else:
                return f"memory[0x{address:04X}] /* {var_name} */ = "
        elif target_format in ['qbasic', 'pdsx']:
            if access_type == 'read':
                return f"PEEK({address})"
            else:
                return f"POKE {address}, "
        else:
            var_name = self.get_smart_variable_name(address)
            if access_type == 'read':
                return f"READ {var_name}"
            else:
                return f"WRITE {var_name}"
    
    def get_instruction_translation(self, instruction: str, operand: int = None, target_format: str = 'c') -> str:
        """Instruction çevirisini al"""
        if instruction == 'JSR' and operand:
            if operand in self.unified_lookup:
                info = self.unified_lookup[operand]
                if info['type'] in ['kernal_routine', 'basic_routine']:
                    if target_format == 'c':
                        c_equiv = info.get('c_equivalent', '')
                        if c_equiv:
                            return c_equiv
                        else:
                            return f"call_routine_{info['name']}()"
                    elif target_format in ['qbasic', 'pdsx']:
                        qb_equiv = info.get('qbasic_equivalent', '')
                        if qb_equiv:
                            return qb_equiv
                        else:
                            return f"GOSUB {info['name']}"
            
            # Fallback for unknown JSR
            if target_format == 'c':
                return f"call_routine_0x{operand:04X}()"
            else:
                return f"GOSUB {operand}"
        
        # Default handling for other instructions
        return ""
    
    def format_memory_access(self, address: int, access_type: str = 'read', output_format: str = 'c') -> str:
        """Memory erişimini formatla"""
        return self.get_format_translation(address, output_format, access_type)
    
    def get_address_info(self, address: int) -> Dict[str, Any]:
        """Adres hakkında detaylı bilgi al"""
        if not self.unified_lookup:
            self.build_unified_lookup()
        
        if address in self.unified_lookup:
            return self.unified_lookup[address]
        
        # Generate synthetic info
        return {
            'name': self.get_smart_variable_name(address),
            'type': 'unknown',
            'description': f'Memory location at ${address:04X}',
            'c_equivalent': f'memory[0x{address:04X}]',
            'qbasic_equivalent': f'PEEK({address})',
            'pdsx_equivalent': f'PEEK({address})',
            'comment': f'Address ${address:04X}',
            'priority': 0
        }


# Enhanced manager instance
enhanced_c64_memory_manager = EnhancedC64MemoryManager()

# Enhanced API functions
def get_enhanced_routine_info(address: int) -> Optional[Dict[str, Any]]:
    """Enhanced rutin bilgisini al"""
    return enhanced_c64_memory_manager.get_address_info(address)

def get_smart_variable_name(address: int, access_type: str = 'read') -> str:
    """Akıllı değişken ismi al"""
    return enhanced_c64_memory_manager.get_smart_variable_name(address, access_type)

def get_format_translation(address: int, target_format: str, access_type: str = 'read') -> str:
    """Format-specific çeviri al"""
    return enhanced_c64_memory_manager.get_format_translation(address, target_format, access_type)

def get_instruction_translation(instruction: str, operand: int = None, target_format: str = 'c') -> str:
    """Instruction çevirisini al"""
    return enhanced_c64_memory_manager.get_instruction_translation(instruction, operand, target_format)
