"""
Enhanced C64 Knowledge Manager - Kapsamlı Commodore 64 Bilgi Yönetim Sistemi
Bu modül, C64 sistemi hakkındaki tüm bilgileri organize eder ve
farklı seviyelerde açıklama sunar.

Faz 3.1 - Hardware-Aware Decompilation için geliştirildi
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class AnnotationLevel(Enum):
    """Açıklama seviyelerini tanımlar"""
    MINIMAL = "minimal"
    BASIC = "basic" 
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"
    EDUCATIONAL = "educational"

class FormatType(Enum):
    """Format türlerini tanımlar"""
    ASSEMBLY = "assembly"
    BASIC = "basic"
    C = "c"
    QBASIC = "qbasic"
    PYTHON = "python"

@dataclass
class AnnotationConfig:
    """Açıklama konfigürasyonu"""
    level: AnnotationLevel
    target_format: FormatType
    include_examples: bool = False
    include_transpile: bool = False
    include_opcodes: bool = False
    include_timing: bool = False

class EnhancedC64KnowledgeManager:
    """
    Gelişmiş C64 bilgi yönetim sistemi
    
    Özellikler:
    - Aşamalı bilgi verme (minimal → comprehensive)
    - Format-aware açıklamalar
    - KERNAL, BASIC, VIC-II, SID bilgileri
    - Assembly opcode referansları
    - Transpilation bilgileri
    - Hardware-aware analiz
    """
    
    def __init__(self, data_directory: str = "."):
        """
        Enhanced C64 Knowledge Manager'ı başlatır
        
        Args:
            data_directory: JSON dosyalarının bulunduğu dizin
        """
        self.data_dir = data_directory
        self.data_cache = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Tüm JSON veri dosyalarını yükler"""
        data_files = {
            'kernal': 'c64_kernal_functions.json',
            'basic': 'c64_basic_functions.json', 
            'vic_ii': 'c64_vic_ii_registers.json',
            'memory_map': 'c64_memory_map.json',
            'opcodes': 'complete_6502_opcode_map.json'
        }
        
        for key, filename in data_files.items():
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.data_cache[key] = json.load(f)
                    print(f"✅ {filename} yüklendi")
                except Exception as e:
                    print(f"⚠️ {filename} yüklenemedi: {e}")
            else:
                print(f"⚠️ {filename} bulunamadı")
    
    def get_address_info(self, address: int, config: AnnotationConfig) -> Dict[str, Any]:
        """
        Bellek adresi hakkında bilgi verir
        
        Args:
            address: Bellek adresi (örn: 0xD000)
            config: Açıklama konfigürasyonu
            
        Returns:
            Adres hakkında bilgi sözlüğü
        """
        info = {
            'address': f"${address:04X}",
            'decimal': address,
            'type': 'unknown',
            'description': '',
            'category': '',
            'annotations': []
        }
        
        # VIC-II kayıtları kontrol et
        if 0xD000 <= address <= 0xD02E:
            vic_info = self._get_vic_ii_info(address, config)
            if vic_info:
                info.update(vic_info)
                info['type'] = 'vic_ii_register'
        
        # SID kayıtları kontrol et
        elif 0xD400 <= address <= 0xD7FF:
            info['type'] = 'sid_register'
            info['description'] = 'SID Sound Interface Device'
            info['category'] = 'audio'
        
        # Color RAM kontrol et
        elif 0xD800 <= address <= 0xDBFF:
            info['type'] = 'color_ram'
            info['description'] = 'Color RAM (Nibble)'
            info['category'] = 'video'
        
        # CIA kayıtları kontrol et
        elif 0xDC00 <= address <= 0xDCFF or 0xDD00 <= address <= 0xDDFF:
            info['type'] = 'cia_register'
            if 0xDC00 <= address <= 0xDCFF:
                info['description'] = 'CIA #1 - Keyboard, Joystick'
            else:
                info['description'] = 'CIA #2 - Serial Port, RS-232'
            info['category'] = 'io'
        
        # KERNAL fonksiyonları kontrol et
        elif 0xE000 <= address <= 0xFFFF:
            kernal_info = self._get_kernal_info(address, config)
            if kernal_info:
                info.update(kernal_info)
                info['type'] = 'kernal_function'
        
        # BASIC ROM kontrol et
        elif 0xA000 <= address <= 0xBFFF:
            info['type'] = 'basic_rom'
            info['description'] = 'BASIC ROM alanı'
            info['category'] = 'system'
        
        # Zero Page kontrol et
        elif 0x0000 <= address <= 0x00FF:
            info['type'] = 'zero_page'
            info['description'] = 'Zero Page - Hızlı erişim alanı'
            info['category'] = 'memory'
            # Zero page özel adresleri
            zp_info = self._get_zero_page_info(address)
            if zp_info:
                info.update(zp_info)
        
        # Stack alanı
        elif 0x0100 <= address <= 0x01FF:
            info['type'] = 'stack'
            info['description'] = 'Stack alanı (6502 processor stack)'
            info['category'] = 'memory'
        
        # RAM alanı
        elif 0x0200 <= address <= 0x9FFF:
            info['type'] = 'ram'
            info['description'] = 'RAM alanı'
            info['category'] = 'memory'
            
            # Özel RAM alanları
            if 0x0400 <= address <= 0x07FF:
                info['description'] = 'Default Screen Memory'
                info['category'] = 'video'
            elif 0x0800 <= address <= 0x9FFF:
                info['description'] = 'BASIC Program Area / User RAM'
                info['category'] = 'program'
        
        return info
    
    def _get_vic_ii_info(self, address: int, config: AnnotationConfig) -> Optional[Dict[str, Any]]:
        """VIC-II kayıt bilgisini getirir"""
        if 'vic_ii' not in self.data_cache:
            return None
            
        vic_data = self.data_cache['vic_ii'].get('c64_vic_ii_registers', {})
        registers = vic_data.get('registers', {})
        
        addr_key = f"0x{address:04X}"
        if addr_key in registers:
            reg_info = registers[addr_key]
            
            result = {
                'name': reg_info.get('name', ''),
                'description': reg_info.get('description', ''),
                'category': reg_info.get('category', ''),
                'type': reg_info.get('type', ''),
                'annotations': []
            }
            
            # Açıklama seviyesine göre bilgi ekle
            if config.level.value in ['detailed', 'comprehensive', 'educational']:
                if 'bit_meaning' in reg_info:
                    result['bit_meanings'] = reg_info['bit_meaning']
                if 'usage' in reg_info:
                    result['usage'] = reg_info['usage']
            
            if config.level.value in ['comprehensive', 'educational']:
                if 'assembly_comment' in reg_info:
                    result['assembly_comment'] = reg_info['assembly_comment']
                if 'c_equivalent' in reg_info:
                    result['c_equivalent'] = reg_info['c_equivalent']
            
            return result
            
        return None
    
    def _get_kernal_info(self, address: int, config: AnnotationConfig) -> Optional[Dict[str, Any]]:
        """KERNAL fonksiyon bilgisini getirir"""
        if 'kernal' not in self.data_cache:
            return None
            
        kernal_data = self.data_cache['kernal'].get('c64_kernal_functions', {})
        functions = kernal_data.get('functions', {})
        
        addr_key = f"0x{address:04X}"
        if addr_key in functions:
            func_info = functions[addr_key]
            
            result = {
                'name': func_info.get('name', ''),
                'description': func_info.get('description', ''),
                'category': func_info.get('category', ''),
                'annotations': []
            }
            
            # Açıklama seviyesine göre bilgi ekle
            if config.level.value in ['detailed', 'comprehensive', 'educational']:
                if 'parameters' in func_info:
                    result['parameters'] = func_info['parameters']
                if 'returns' in func_info:
                    result['returns'] = func_info['returns']
                if 'usage' in func_info:
                    result['usage'] = func_info['usage']
            
            if config.level.value in ['comprehensive', 'educational'] and config.include_opcodes:
                if 'opcodes' in func_info:
                    result['opcodes'] = func_info['opcodes']
            
            return result
            
        return None
    
    def _get_zero_page_info(self, address: int) -> Optional[Dict[str, Any]]:
        """Zero page özel adres bilgisini getirir"""
        zero_page_addresses = {
            0x00: {'name': 'Direction register', 'description': 'Processor port direction'},
            0x01: {'name': 'Processor port', 'description': 'Memory configuration'},
            0x14: {'name': 'KERNAL IRQ', 'description': 'IRQ vector low byte'},
            0x15: {'name': 'KERNAL IRQ', 'description': 'IRQ vector high byte'},
            0x22: {'name': 'BASIC start', 'description': 'Start of BASIC program'},
            0x2A: {'name': 'BASIC vars', 'description': 'Start of BASIC variables'},
            0x2C: {'name': 'BASIC arrays', 'description': 'Start of BASIC arrays'},
            0x2E: {'name': 'BASIC strings', 'description': 'Start of BASIC strings'},
            0x30: {'name': 'BASIC top', 'description': 'Top of BASIC memory'},
            0x37: {'name': 'BASIC line', 'description': 'Current BASIC line number'},
            0x39: {'name': 'BASIC pointer', 'description': 'Current BASIC line pointer'},
            0x91: {'name': 'Color under cursor', 'description': 'Color under cursor'},
            0x90: {'name': 'Keyboard matrix', 'description': 'Keyboard decode table'},
        }
        
        if address in zero_page_addresses:
            return zero_page_addresses[address]
        
        return None
    
    def get_basic_token_info(self, token: int, config: AnnotationConfig) -> Dict[str, Any]:
        """
        BASIC token hakkında bilgi verir
        
        Args:
            token: BASIC token numarası
            config: Açıklama konfigürasyonu
            
        Returns:
            Token hakkında bilgi sözlüğü
        """
        if 'basic' not in self.data_cache:
            return {'error': 'BASIC data not loaded'}
        
        basic_data = self.data_cache['basic'].get('c64_basic_functions', {})
        
        # Token'ı ara
        for cmd_name, cmd_info in basic_data.get('commands', {}).items():
            if cmd_info.get('token') == token:
                return self._format_basic_info(cmd_name, cmd_info, config)
        
        for func_name, func_info in basic_data.get('functions', {}).items():
            if func_info.get('token') == token:
                return self._format_basic_info(func_name, func_info, config)
        
        return {'error': f'Token {token} not found'}
    
    def _format_basic_info(self, name: str, info: Dict, config: AnnotationConfig) -> Dict[str, Any]:
        """BASIC bilgisini formatlar"""
        result = {
            'name': name,
            'token': info.get('token'),
            'hex': info.get('hex'),
            'description': info.get('description', ''),
            'category': info.get('category', ''),
            'annotations': []
        }
        
        # Açıklama seviyesine göre bilgi ekle
        if config.level.value in ['detailed', 'comprehensive', 'educational']:
            if 'syntax' in info:
                result['syntax'] = info['syntax']
        
        if config.level.value in ['comprehensive', 'educational'] and config.include_examples:
            if 'examples' in info:
                result['examples'] = info['examples']
        
        if config.include_transpile:
            transpile_key = f'transpile_{config.target_format.value}'
            if transpile_key in info:
                result['transpile_to'] = info[transpile_key]
        
        return result
    
    def generate_address_comment(self, address: int, config: AnnotationConfig) -> str:
        """
        Bellek adresi için yorum satırı oluşturur
        
        Args:
            address: Bellek adresi
            config: Açıklama konfigürasyonu
            
        Returns:
            Yorum satırı string'i
        """
        info = self.get_address_info(address, config)
        
        if config.target_format == FormatType.ASSEMBLY:
            comment_prefix = "; "
        elif config.target_format == FormatType.C:
            comment_prefix = "// "
        elif config.target_format == FormatType.PYTHON:
            comment_prefix = "# "
        else:
            comment_prefix = "REM "
        
        # Temel yorum
        comment = f"{comment_prefix}${address:04X}"
        
        if config.level.value == 'minimal':
            return comment
        
        if 'name' in info and info['name']:
            comment += f" - {info['name']}"
        
        if config.level.value in ['basic', 'detailed'] and 'description' in info:
            comment += f" ({info['description']})"
        
        if config.level.value in ['comprehensive', 'educational']:
            if 'usage' in info:
                comment += f" | Kullanım: {info['usage']}"
            if 'assembly_comment' in info:
                comment += f" {info['assembly_comment']}"
        
        return comment
    
    def get_hardware_aware_analysis(self, data: bytes, start_address: int = 0x0801) -> Dict[str, Any]:
        """
        Hardware-aware kod analizi yapar - Faz 3.1 özelliği
        
        Args:
            data: Analiz edilecek veri
            start_address: Başlangıç adresi
            
        Returns:
            Hardware-aware analiz sonuçları
        """
        analysis = {
            'hardware_accesses': {
                'vic_ii': [],
                'sid': [],
                'cia': [],
                'color_ram': []
            },
            'kernal_calls': [],
            'basic_tokens': [],
            'zero_page_usage': [],
            'memory_patterns': [],
            'statistics': {}
        }
        
        # Her byte'ı analiz et
        for i, byte in enumerate(data):
            current_addr = start_address + i
            
            # Hardware register erişimi kontrol et
            if byte in [0x8D, 0xAD, 0x8C, 0xAC]:  # STA/LDA/STY/LDY absolute
                if i + 2 < len(data):
                    target_addr = (data[i + 2] << 8) | data[i + 1]
                    
                    # VIC-II erişimi
                    if 0xD000 <= target_addr <= 0xD02E:
                        config = AnnotationConfig(AnnotationLevel.COMPREHENSIVE, FormatType.ASSEMBLY)
                        vic_info = self.get_address_info(target_addr, config)
                        analysis['hardware_accesses']['vic_ii'].append({
                            'address': current_addr,
                            'operation': 'write' if byte in [0x8D, 0x8C] else 'read',
                            'target': target_addr,
                            'register_info': vic_info
                        })
                    
                    # SID erişimi
                    elif 0xD400 <= target_addr <= 0xD7FF:
                        analysis['hardware_accesses']['sid'].append({
                            'address': current_addr,
                            'operation': 'write' if byte in [0x8D, 0x8C] else 'read',
                            'target': target_addr
                        })
                    
                    # CIA erişimi
                    elif (0xDC00 <= target_addr <= 0xDCFF) or (0xDD00 <= target_addr <= 0xDDFF):
                        analysis['hardware_accesses']['cia'].append({
                            'address': current_addr,
                            'operation': 'write' if byte in [0x8D, 0x8C] else 'read',
                            'target': target_addr
                        })
            
            # KERNAL çağrısı kontrol et (JSR $XXX)
            if byte == 0x20 and i + 2 < len(data):  # JSR opcode
                target_addr = (data[i + 2] << 8) | data[i + 1]
                if 0xE000 <= target_addr <= 0xFFFF:
                    config = AnnotationConfig(AnnotationLevel.COMPREHENSIVE, FormatType.ASSEMBLY)
                    kernal_info = self.get_address_info(target_addr, config)
                    if kernal_info.get('type') == 'kernal_function':
                        analysis['kernal_calls'].append({
                            'address': current_addr,
                            'target': target_addr,
                            'function': kernal_info
                        })
            
            # Zero page erişimi kontrol et
            if byte in [0x85, 0xA5, 0x84, 0xA4]:  # STA/LDA/STY/LDY zero page
                if i + 1 < len(data):
                    zp_addr = data[i + 1]
                    zp_info = self._get_zero_page_info(zp_addr)
                    if zp_info:
                        analysis['zero_page_usage'].append({
                            'address': current_addr,
                            'operation': 'write' if byte in [0x85, 0x84] else 'read',
                            'zp_address': zp_addr,
                            'info': zp_info
                        })
            
            # BASIC token kontrol et
            if 0x80 <= byte <= 0xFF:
                config = AnnotationConfig(AnnotationLevel.BASIC, FormatType.ASSEMBLY)
                token_info = self.get_basic_token_info(byte, config)
                if 'error' not in token_info:
                    analysis['basic_tokens'].append({
                        'address': current_addr,
                        'token': byte,
                        'info': token_info
                    })
        
        # İstatistikleri hesapla
        analysis['statistics'] = {
            'total_bytes': len(data),
            'vic_ii_accesses': len(analysis['hardware_accesses']['vic_ii']),
            'sid_accesses': len(analysis['hardware_accesses']['sid']),
            'cia_accesses': len(analysis['hardware_accesses']['cia']),
            'kernal_calls': len(analysis['kernal_calls']),
            'zero_page_usage': len(analysis['zero_page_usage']),
            'basic_tokens': len(analysis['basic_tokens'])
        }
        
        return analysis

# Kolay kullanım için global instance
enhanced_knowledge_manager = None

def get_enhanced_knowledge_manager(data_directory: str = ".") -> EnhancedC64KnowledgeManager:
    """Global enhanced knowledge manager instance'ını getirir"""
    global enhanced_knowledge_manager
    if enhanced_knowledge_manager is None:
        enhanced_knowledge_manager = EnhancedC64KnowledgeManager(data_directory)
    return enhanced_knowledge_manager

def annotate_address_enhanced(address: int, level: str = "basic", target_format: str = "assembly") -> str:
    """
    Gelişmiş adres açıklama fonksiyonu
    
    Args:
        address: Bellek adresi
        level: Açıklama seviyesi (minimal, basic, detailed, comprehensive, educational)
        target_format: Hedef format (assembly, c, python, etc.)
        
    Returns:
        Açıklama string'i
    """
    km = get_enhanced_knowledge_manager()
    config = AnnotationConfig(
        level=AnnotationLevel(level),
        target_format=FormatType(target_format)
    )
    return km.generate_address_comment(address, config)

if __name__ == "__main__":
    # Test kodu
    print("🔍 Enhanced C64 Knowledge Manager Test - Faz 3.1")
    print("=" * 50)
    
    km = EnhancedC64KnowledgeManager(".")
    
    # VIC-II test
    config = AnnotationConfig(AnnotationLevel.COMPREHENSIVE, FormatType.ASSEMBLY)
    vic_info = km.get_address_info(0xD000, config)
    print(f"VIC-II $D000: {vic_info}")
    
    # KERNAL test
    kernal_info = km.get_address_info(0xFFD2, config)
    print(f"KERNAL $FFD2: {kernal_info}")
    
    # Zero page test
    zp_info = km.get_address_info(0x01, config)
    print(f"Zero Page $01: {zp_info}")
    
    # BASIC token test
    basic_info = km.get_basic_token_info(153, config)  # PRINT token
    print(f"BASIC Token 153: {basic_info}")
    
    # Yorum satırı test
    comment = km.generate_address_comment(0xD020, config)
    print(f"Comment: {comment}")
    
    # Hardware-aware analysis test
    test_data = bytes([0x20, 0xD2, 0xFF, 0x8D, 0x20, 0xD0])  # JSR $FFD2, STA $D020
    hw_analysis = km.get_hardware_aware_analysis(test_data)
    print(f"Hardware Analysis: {hw_analysis}")
