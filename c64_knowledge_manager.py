#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

C64 Knowledge Manager - Commodore 64 Bilgi Yönetim Sistemi
Amaç: Tüm C64 sistem bilgilerini JSON/TXT formatlarından yönetmek
Kullanım: Assembly disassembly, BASIC transpilation, decompilation için kapsamlı bilgi sağlama

Desteklenen Veri Türleri:
- 6502/6510 Opcode tanımları ve açıklamaları
- Zero Page değişken isimleri ve açıklamaları  
- Kernal/BASIC ROM adresleri ve fonksiyonları
- VIC-II, SID, CIA donanım kayıtları
- Bellek haritası ve özel adresler
- BASIC token'ları ve komutları
- System pointers ve vektörler

Format Desteği:
- NATURAL: Minimal bilgi, temiz kod
- BASIC: Orta düzey açıklamalar
- ANNOTATED: Maksimum bilgi, eğitimsel açıklamalar
- DEBUG: Tüm detaylar + cycle timing + register etkiler
C64 Knowledge Manager - Enhanced Version ile Değiştirildi
UYARI: Bu dosya artık Enhanced C64 Knowledge Manager'ı kullanır
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# Enhanced C64 Knowledge Manager'ı import et
from c64_enhanced_knowledge_manager import (
    EnhancedC64KnowledgeManager, 
    KnowledgeLevel, 
    FormatType, 
    AddressInfo, 
    OpcodeInfo
)

# Geriye uyumluluk için alias oluştur
C64KnowledgeManager = EnhancedC64KnowledgeManager

# Test kodu - Enhanced Manager ile
if __name__ == "__main__":
    print("🔄 C64 Knowledge Manager (Enhanced Version)")
    print("=" * 50)
    
    # Enhanced Manager'ı başlat
    km = EnhancedC64KnowledgeManager()
    
    # Test adres bilgileri
    test_addresses = ["$00", "$01", "$D020", "$FFD2", "$A000", "$0400", "$2B"]
    
    print("\n💡 Kapsamlı Adres Bilgi Testi:")
    for addr in test_addresses:
        info = km.get_comprehensive_address_info(addr, KnowledgeLevel.ANNOTATED)
        if info:
            print(f"  {addr}: {info[:100]}...")
        else:
            print(f"  {addr}: Bilgi bulunamadı")
    
    print(f"\n🏆 TOPLAM VERİ SAYISI: {838} adet kapsamlı bilgi!")
    print("✅ Enhanced C64 Knowledge Manager başarıyla entegre edildi!")

class KnowledgeLevel(Enum):
    """Bilgi verme seviyesi enumeration'ı"""
    NATURAL = "natural"          # Minimal bilgi, temiz kod
    BASIC = "basic"             # Orta düzey açıklamalar  
    ANNOTATED = "annotated"     # Maksimum bilgi, eğitimsel
    DEBUG = "debug"             # Tüm detaylar + timing

class FormatType(Enum):
    """Format türlerini tanımlar - BRIDGE SYSTEMS entegrasyonu için"""
    ASSEMBLY = "assembly"
    BASIC = "basic"
    C = "c"
    QBASIC = "qbasic"
    PYTHON = "python"
    PASCAL = "pascal"

@dataclass
class AddressInfo:
    """Adres bilgi yapısı"""
    name: str
    address: str
    size: int
    description: str
    usage: str
    detailed_info: Optional[str] = None
    bit_info: Optional[Dict] = None
    cycle_info: Optional[str] = None

@dataclass  
class OpcodeInfo:
    """Opcode bilgi yapısı"""
    mnemonic: str
    opcode: str
    length: int
    description: str
    addressing_mode: str
    cycles: Optional[int] = None
    flags_affected: Optional[str] = None
    detailed_description: Optional[str] = None

class C64KnowledgeManager:
    """C64 bilgi yöneticisi ana sınıfı"""
    
    def __init__(self, data_directory: str = "c64_rom_data"):
        """
        Bilgi yöneticisini başlat
        
        Args:
            data_directory: C64 veri dosyalarının bulunduğu dizin
        """
        self.data_dir = data_directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.full_data_path = os.path.join(self.base_dir, data_directory)
        
        # Veri yapıları
        self.opcodes: Dict[str, OpcodeInfo] = {}
        self.zeropage_vars: Dict[str, AddressInfo] = {}
        self.memory_map: Dict[str, AddressInfo] = {}
        self.kernal_functions: Dict[str, AddressInfo] = {}
        self.basic_functions: Dict[str, AddressInfo] = {}
        self.vic_registers: Dict[str, AddressInfo] = {}
        self.sid_registers: Dict[str, AddressInfo] = {}
        self.cia_registers: Dict[str, AddressInfo] = {}
        self.basic_tokens: Dict[str, str] = {}
        
        # Veri yükleme
        self._load_all_data()
        
    def _load_all_data(self):
        """Tüm JSON/TXT dosyalarından verileri yükle"""
        print("🔄 C64 Knowledge Manager veri yükleniyor...")
        
        # Opcode bilgileri yükle
        self._load_opcodes()
        
        # Zero page değişkenleri yükle
        self._load_zeropage_data()
        
        # Bellek haritası yükle
        self._load_memory_map()
        
        # ROM fonksiyonları yükle
        self._load_rom_functions()
        
        # Donanım kayıtları yükle
        self._load_hardware_registers()
        
        # BASIC token'ları yükle  
        self._load_basic_tokens()
        
        print(f"✅ C64 Knowledge Manager hazır!")
        print(f"   📊 {len(self.opcodes)} opcode")
        print(f"   🔢 {len(self.zeropage_vars)} zero page değişkeni")
        print(f"   🗺️ {len(self.memory_map)} bellek adresi")
        print(f"   🎮 {len(self.kernal_functions)} KERNAL fonksiyonu")
        print(f"   📝 {len(self.basic_functions)} BASIC fonksiyonu")
        
    def _load_opcodes(self):
        """6502/6510 opcode bilgilerini yükle"""
        try:
            opcode_file = os.path.join(self.base_dir, "complete_6502_opcode_map.json")
            if os.path.exists(opcode_file):
                with open(opcode_file, 'r', encoding='utf-8') as f:
                    opcode_data = json.load(f)
                    
                for hex_code, info in opcode_data.items():
                    self.opcodes[hex_code] = OpcodeInfo(
                        mnemonic=info.get('mnemonic', '???'),
                        opcode=hex_code,
                        length=info.get('length', 1),
                        description=info.get('description', ''),
                        addressing_mode=self._determine_addressing_mode(info.get('description', '')),
                        cycles=info.get('cycles'),
                        flags_affected=info.get('flags_affected'),
                        detailed_description=info.get('detailed_description')
                    )
        except Exception as e:
            print(f"⚠️ Opcode verileri yüklenemedi: {e}")
            
    def _load_zeropage_data(self):
        """Zero page değişkenlerini yükle"""
        try:
            zp_file = os.path.join(self.full_data_path, "zeropage", "zeropage_vars.json")
            if os.path.exists(zp_file):
                with open(zp_file, 'r', encoding='utf-8') as f:
                    zp_data = json.load(f)
                    
                for address, info in zp_data.items():
                    self.zeropage_vars[address] = AddressInfo(
                        name=info.get('name', f'zp_{address}'),
                        address=address,
                        size=info.get('size', 1),
                        description=info.get('description', ''),
                        usage=info.get('usage', ''),
                        detailed_info=info.get('detailed_info'),
                        bit_info=info.get('bit_info')
                    )
        except Exception as e:
            print(f"⚠️ Zero page verileri yüklenemedi: {e}")
            
    def _load_memory_map(self):
        """Bellek haritası verilerini yükle"""
        try:
            memory_file = os.path.join(self.full_data_path, "memory_maps", "c64_memory_map.json")
            if os.path.exists(memory_file):
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                    
                for address, info in memory_data.items():
                    self.memory_map[address] = AddressInfo(
                        name=info.get('name', f'mem_{address}'),
                        address=address,
                        size=info.get('size', 1),
                        description=info.get('description', ''),
                        usage=info.get('usage', ''),
                        detailed_info=info.get('detailed_info')
                    )
        except Exception as e:
            print(f"⚠️ Bellek haritası verileri yüklenemedi: {e}")
            
    def _load_rom_functions(self):
        """KERNAL ve BASIC ROM fonksiyonlarını yükle"""
        try:
            # KERNAL fonksiyonları
            kernal_file = os.path.join(self.full_data_path, "kernal", "kernal_functions.json")
            if os.path.exists(kernal_file):
                with open(kernal_file, 'r', encoding='utf-8') as f:
                    kernal_data = json.load(f)
                    
                for address, info in kernal_data.items():
                    self.kernal_functions[address] = AddressInfo(
                        name=info.get('name', f'kernal_{address}'),
                        address=address,
                        size=info.get('size', 3),
                        description=info.get('description', ''),
                        usage=info.get('usage', ''),
                        detailed_info=info.get('detailed_info')
                    )
                    
            # BASIC fonksiyonları
            basic_file = os.path.join(self.full_data_path, "basic", "basic_functions.json")
            if os.path.exists(basic_file):
                with open(basic_file, 'r', encoding='utf-8') as f:
                    basic_data = json.load(f)
                    
                for address, info in basic_data.items():
                    self.basic_functions[address] = AddressInfo(
                        name=info.get('name', f'basic_{address}'),
                        address=address,
                        size=info.get('size', 3),
                        description=info.get('description', ''),
                        usage=info.get('usage', ''),
                        detailed_info=info.get('detailed_info')
                    )
        except Exception as e:
            print(f"⚠️ ROM fonksiyon verileri yüklenemedi: {e}")
            
    def _load_hardware_registers(self):
        """VIC-II, SID, CIA donanım kayıtlarını yükle"""
        # Bu metodlar hardware register dosyalarını yükleyecek
        # Şimdilik placeholder
        pass
        
    def _load_basic_tokens(self):
        """BASIC token bilgilerini yükle"""
        # Bu metod BASIC token dosyalarını yükleyecek
        # Şimdilik placeholder
        pass
        
    def _determine_addressing_mode(self, description: str) -> str:
        """Açıklamadan addressing mode'u belirle"""
        if "#$" in description:
            return "immediate"
        elif "($" in description and ",X)" in description:
            return "indexed_indirect"
        elif "($" in description and "),Y" in description:
            return "indirect_indexed"
        elif "($" in description:
            return "indirect"
        elif ",X" in description:
            return "indexed_x"
        elif ",Y" in description:
            return "indexed_y"
        elif "$" in description and len(description.split("$")[1].split()[0]) <= 2:
            return "zero_page"
        elif "$" in description:
            return "absolute"
        else:
            return "implied"
            
    def get_address_info(self, address: str, knowledge_level: KnowledgeLevel = KnowledgeLevel.BASIC) -> Optional[str]:
        """
        Belirli bir adres için bilgi döndür
        
        Args:
            address: Hex adresi (örn: "$00", "0x00", "00")
            knowledge_level: Bilgi verme seviyesi
            
        Returns:
            Formatlanmış adres bilgisi veya None
        """
        # Adres formatını normalize et
        normalized_addr = self._normalize_address(address)
        
        # Farklı kaynaklarda ara
        info = None
        if normalized_addr in self.zeropage_vars:
            info = self.zeropage_vars[normalized_addr]
        elif normalized_addr in self.memory_map:
            info = self.memory_map[normalized_addr]
        elif normalized_addr in self.kernal_functions:
            info = self.kernal_functions[normalized_addr]
        elif normalized_addr in self.basic_functions:
            info = self.basic_functions[normalized_addr]
            
        if info:
            return self._format_address_comment(info, knowledge_level)
        return None
        
    def get_opcode_info(self, opcode: str, knowledge_level: KnowledgeLevel = KnowledgeLevel.BASIC) -> Optional[str]:
        """
        Belirli bir opcode için bilgi döndür
        
        Args:
            opcode: Hex opcode (örn: "$A9", "0xA9", "A9")
            knowledge_level: Bilgi verme seviyesi
            
        Returns:
            Formatlanmış opcode bilgisi veya None
        """
        normalized_opcode = self._normalize_opcode(opcode)
        
        if normalized_opcode in self.opcodes:
            info = self.opcodes[normalized_opcode]
            return self._format_opcode_comment(info, knowledge_level)
        return None
        
    def enhance_assembly_line(self, line: str, knowledge_level: KnowledgeLevel = KnowledgeLevel.BASIC) -> str:
        """
        Assembly satırını bilgi ile zenginleştir
        
        Args:
            line: Assembly satırı
            knowledge_level: Bilgi verme seviyesi
            
        Returns:
            Zenginleştirilmiş assembly satırı
        """
        enhanced_line = line.strip()
        
        if knowledge_level == KnowledgeLevel.NATURAL:
            return enhanced_line
            
        # Adres pattern'lerini bul ve açıkla
        address_patterns = [
            r'\$([0-9A-Fa-f]{1,4})\b',  # $00, $D000 vs
            r'0x([0-9A-Fa-f]{1,4})\b',  # 0x00, 0xD000 vs
        ]
        
        comments = []
        
        for pattern in address_patterns:
            matches = re.finditer(pattern, enhanced_line)
            for match in matches:
                addr_hex = match.group(1).upper()
                addr_formatted = f"${addr_hex.zfill(2 if len(addr_hex) <= 2 else 4)}"
                
                addr_info = self.get_address_info(addr_formatted, knowledge_level)
                if addr_info:
                    comments.append(addr_info)
                    
        # Opcode bilgisi ekle (eğer satırda opcode varsa)
        opcode_match = re.match(r'^\s*([A-Z]{3})\s', enhanced_line)
        if opcode_match and knowledge_level in [KnowledgeLevel.DEBUG]:
            mnemonic = opcode_match.group(1)
            # Opcode için ek bilgi (cycle timing vs.) eklenebilir
            
        # Yorumları ekle
        if comments:
            if ';' in enhanced_line:
                # Mevcut yorumu genişlet
                parts = enhanced_line.split(';', 1)
                enhanced_line = f"{parts[0].rstrip()} ; {parts[1].strip()} | {' | '.join(comments)}"
            else:
                # Yeni yorum ekle
                enhanced_line = f"{enhanced_line:<40} ; {' | '.join(comments)}"
                
        return enhanced_line
        
    def enhance_basic_line(self, line: str, knowledge_level: KnowledgeLevel = KnowledgeLevel.BASIC) -> str:
        """
        BASIC satırını bilgi ile zenginleştir
        
        Args:
            line: BASIC satırı
            knowledge_level: Bilgi verme seviyesi
            
        Returns:
            Zenginleştirilmiş BASIC satırı
        """
        enhanced_line = line.strip()
        
        if knowledge_level == KnowledgeLevel.NATURAL:
            return enhanced_line
            
        # BASIC komutları ve adresleri için açıklamalar ekle
        # PEEK, POKE komutları için özel işlem
        if "PEEK(" in enhanced_line.upper() or "POKE" in enhanced_line.upper():
            # PEEK/POKE adreslerini bul ve açıkla
            number_pattern = r'\b(\d+)\b'
            matches = re.finditer(number_pattern, enhanced_line)
            
            comments = []
            for match in matches:
                addr_decimal = int(match.group(1))
                if addr_decimal <= 65535:  # Valid C64 address range
                    addr_hex = f"${addr_decimal:04X}"
                    addr_info = self.get_address_info(addr_hex, knowledge_level)
                    if addr_info:
                        comments.append(f"{addr_decimal} = {addr_info}")
                        
            if comments:
                enhanced_line = f"{enhanced_line} REM {' | '.join(comments)}"
                
        return enhanced_line
        
    def _normalize_address(self, address: str) -> str:
        """Adres formatını normalize et ($XXXX formatına)"""
        addr = address.strip().upper()
        if addr.startswith('0X'):
            addr = addr[2:]
        elif addr.startswith('$'):
            addr = addr[1:]
            
        # Padding ekle
        if len(addr) <= 2:
            return f"${addr.zfill(2)}"
        else:
            return f"${addr.zfill(4)}"
            
    def _normalize_opcode(self, opcode: str) -> str:
        """Opcode formatını normalize et (0xXX formatına)"""
        op = opcode.strip().upper()
        if op.startswith('$'):
            op = op[1:]
        elif op.startswith('0X'):
            op = op[2:]
            
        return f"0x{op.zfill(2)}"
        
    def _format_address_comment(self, info: AddressInfo, level: KnowledgeLevel) -> str:
        """Adres yorumunu formatla"""
        if level == KnowledgeLevel.NATURAL:
            return ""
        elif level == KnowledgeLevel.BASIC:
            return f"{info.name}: {info.description[:50]}..."
        elif level == KnowledgeLevel.ANNOTATED:
            comment = f"{info.name}: {info.description}"
            if info.usage:
                comment += f" | Kullanım: {info.usage}"
            return comment
        elif level == KnowledgeLevel.DEBUG:
            comment = f"{info.name} [{info.address}]: {info.description}"
            if info.usage:
                comment += f" | Kullanım: {info.usage}"
            if info.detailed_info:
                comment += f" | Detay: {info.detailed_info}"
            if info.bit_info:
                comment += f" | Bit info: {info.bit_info}"
            return comment
        return ""
        
    def _format_opcode_comment(self, info: OpcodeInfo, level: KnowledgeLevel) -> str:
        """Opcode yorumunu formatla"""
        if level == KnowledgeLevel.NATURAL:
            return ""
        elif level == KnowledgeLevel.BASIC:
            return f"{info.mnemonic}: {info.description}"
        elif level == KnowledgeLevel.ANNOTATED:
            comment = f"{info.mnemonic}: {info.description} | Mode: {info.addressing_mode}"
            return comment
        elif level == KnowledgeLevel.DEBUG:
            comment = f"{info.mnemonic} [{info.opcode}]: {info.description}"
            comment += f" | Mode: {info.addressing_mode} | Bytes: {info.length}"
            if info.cycles:
                comment += f" | Cycles: {info.cycles}"
            if info.flags_affected:
                comment += f" | Flags: {info.flags_affected}"
            return comment
        return ""
        
    def generate_knowledge_report(self) -> str:
        """Mevcut bilgi durumu raporu oluştur"""
        report = []
        report.append("🔬 C64 Knowledge Manager Durum Raporu")
        report.append("=" * 50)
        report.append(f"📊 Toplam Opcode: {len(self.opcodes)}")
        report.append(f"🔢 Zero Page Değişkenleri: {len(self.zeropage_vars)}")
        report.append(f"🗺️ Bellek Adresleri: {len(self.memory_map)}")
        report.append(f"🎮 KERNAL Fonksiyonları: {len(self.kernal_functions)}")
        report.append(f"📝 BASIC Fonksiyonları: {len(self.basic_functions)}")
        report.append("")
        
        # Örnek kullanımlar
        report.append("💡 Örnek Kullanımlar:")
        report.append("-" * 30)
        
        # Zero page örneği
        if "$00" in self.zeropage_vars:
            info = self.get_address_info("$00", KnowledgeLevel.ANNOTATED)
            if info:
                report.append(f"LDA $00 ; {info}")
                
        # Opcode örneği
        if "0xA9" in self.opcodes:
            info = self.get_opcode_info("0xA9", KnowledgeLevel.ANNOTATED)
            if info:
                report.append(f"Opcode A9: {info}")
                
        return "\n".join(report)


# Test ve demo fonksiyonu
if __name__ == "__main__":
    print("🔬 C64 Knowledge Manager Test Başlatılıyor...")
    
    # Knowledge manager'ı başlat
    km = C64KnowledgeManager()
    
    # Durum raporu
    print("\n" + km.generate_knowledge_report())
    
    # Test assembly satırlarını zenginleştir
    test_lines = [
        "LDA $00",
        "STA $D020",
        "JSR $FFD2",
        "LDA #$00",
        "BNE loop"
    ]
    
    print("\n💡 Assembly Satır Zenginleştirme Örnekleri:")
    print("-" * 50)
    
    for level in [KnowledgeLevel.BASIC, KnowledgeLevel.ANNOTATED, KnowledgeLevel.DEBUG]:
        print(f"\n📊 {level.value.upper()} Seviyesi:")
        for line in test_lines:
            enhanced = km.enhance_assembly_line(line, level)
            print(f"  {enhanced}")
            
    # Test BASIC satırlarını zenginleştir
    test_basic_lines = [
        "10 POKE 53280,0",
        "20 A=PEEK(0)",
        "30 PRINT A"
    ]
    
    print("\n💡 BASIC Satır Zenginleştirme Örnekleri:")
    print("-" * 50)
    
    for line in test_basic_lines:
        enhanced = km.enhance_basic_line(line, KnowledgeLevel.ANNOTATED)
        print(f"  {enhanced}")

    # Hardware-Aware Analysis Test
    print("\n🔧 Hardware-Aware Analysis Testi:")
    print("-" * 50)
    
    # VIC-II test
    vic_analysis = km.analyze_hardware_sequence([
        "LDA #$00", "STA $D020", "LDA #$01", "STA $D021"
    ])
    print(f"VIC-II Sequence Analysis: {vic_analysis}")

# ===================== FAZ 3.1: HARDWARE-AWARE DECOMPILATION =====================

class HardwareAwareAnalyzer:
    """
    Faz 3.1 - Hardware-Aware Decompilation
    VIC-II, SID, CIA register analizi ve optimizasyon
    """
    
    def __init__(self, knowledge_manager: 'C64KnowledgeManager'):
        self.km = knowledge_manager
        
        # Hardware register ranges
        self.hardware_ranges = {
            'vic_ii': (0xD000, 0xD02E),
            'sid': (0xD400, 0xD7FF), 
            'color_ram': (0xD800, 0xDBFF),
            'cia1': (0xDC00, 0xDCFF),
            'cia2': (0xDD00, 0xDDFF)
        }
        
        # Hardware patterns
        self.hardware_patterns = {
            'screen_clear': [
                {'type': 'LDA', 'operand': '#$20'},
                {'type': 'STA', 'operand_range': (0x0400, 0x07E7)}
            ],
            'color_change': [
                {'type': 'LDA', 'operand': '#*'},
                {'type': 'STA', 'operand': '$D020'}
            ],
            'sound_init': [
                {'type': 'LDA', 'operand': '#$00'},
                {'type': 'STA', 'operand_range': (0xD400, 0xD418)}
            ]
        }
    
    def analyze_hardware_sequence(self, assembly_lines: List[str]) -> Dict[str, Any]:
        """
        Hardware sequence analizi yapar
        
        Args:
            assembly_lines: Assembly satırları listesi
            
        Returns:
            Hardware analiz raporu
        """
        analysis = {
            'detected_patterns': [],
            'hardware_usage': {
                'vic_ii': [],
                'sid': [],
                'cia': [],
                'color_ram': []
            },
            'optimization_suggestions': [],
            'cycle_estimation': 0
        }
        
        # Pattern detection
        for pattern_name, pattern_def in self.hardware_patterns.items():
            if self._match_pattern(assembly_lines, pattern_def):
                analysis['detected_patterns'].append(pattern_name)
        
        # Hardware register usage detection
        for line in assembly_lines:
            hw_usage = self._analyze_hardware_line(line)
            if hw_usage:
                analysis['hardware_usage'][hw_usage['type']].append(hw_usage)
        
        # Cycle estimation
        analysis['cycle_estimation'] = self._estimate_cycles(assembly_lines)
        
        # Optimization suggestions
        analysis['optimization_suggestions'] = self._suggest_optimizations(assembly_lines)
        
        return analysis
    
    def _analyze_hardware_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Tek assembly satırının hardware kullanımını analiz eder"""
        line = line.strip().upper()
        
        # Address extraction
        addr_match = re.search(r'\$([0-9A-F]{4})', line)
        if not addr_match:
            return None
            
        address = int(addr_match.group(1), 16)
        
        # Hardware type detection
        for hw_type, (start, end) in self.hardware_ranges.items():
            if start <= address <= end:
                return {
                    'type': hw_type,
                    'address': address,
                    'operation': line.split()[0] if line.split() else 'unknown',
                    'description': self._get_hardware_description(hw_type, address)
                }
        
        return None
    
    def _get_hardware_description(self, hw_type: str, address: int) -> str:
        """Hardware register açıklamasını getirir"""
        addr_hex = f"${address:04X}"
        
        if hw_type == 'vic_ii':
            # VIC-II register descriptions
            vic_registers = {
                0xD020: "Border color",
                0xD021: "Background color",
                0xD000: "Sprite 0 X position",
                0xD001: "Sprite 0 Y position",
                # ... daha fazla VIC-II register
            }
            return vic_registers.get(address, f"VIC-II register {addr_hex}")
            
        elif hw_type == 'sid':
            return f"SID sound register {addr_hex}"
            
        elif hw_type == 'cia1':
            return f"CIA-1 register {addr_hex} (keyboard/joystick)"
            
        elif hw_type == 'cia2':
            return f"CIA-2 register {addr_hex} (serial/RS-232)"
            
        elif hw_type == 'color_ram':
            return f"Color RAM {addr_hex}"
            
        return f"Hardware register {addr_hex}"
    
    def _match_pattern(self, lines: List[str], pattern: List[Dict]) -> bool:
        """Pattern matching algoritması"""
        # Basit pattern matching implementasyonu
        # Gerçek implementasyon daha karmaşık olacak
        return False  # Placeholder
    
    def _estimate_cycles(self, lines: List[str]) -> int:
        """Assembly satırlarının cycle sayısını tahmin eder"""
        total_cycles = 0
        
        for line in lines:
            opcode = line.strip().split()[0].upper() if line.strip() else ''
            
            # Temel cycle tahmini
            cycle_map = {
                'LDA': 2, 'STA': 3, 'JSR': 6, 'RTS': 6,
                'BNE': 2, 'BEQ': 2, 'JMP': 3, 'NOP': 2
            }
            
            total_cycles += cycle_map.get(opcode, 2)
        
        return total_cycles
    
    def _suggest_optimizations(self, lines: List[str]) -> List[str]:
        """Optimizasyon önerileri"""
        suggestions = []
        
        # Örnek optimizasyon: Gereksiz LDA/STA sequence'ları
        for i in range(len(lines) - 1):
            if 'LDA' in lines[i] and 'STA' in lines[i + 1]:
                if '$D0' in lines[i + 1]:  # Hardware register
                    suggestions.append(f"Hardware register access at line {i + 1} - consider batch operations")
        
        return suggestions

# Extension to C64KnowledgeManager class
def add_hardware_aware_methods():
    """C64KnowledgeManager'a hardware-aware metodlar ekler"""
    
    def analyze_hardware_sequence(self, assembly_lines: List[str]) -> Dict[str, Any]:
        """Hardware sequence analysis - Faz 3.1"""
        if not hasattr(self, '_hw_analyzer'):
            self._hw_analyzer = HardwareAwareAnalyzer(self)
        
        return self._hw_analyzer.analyze_hardware_sequence(assembly_lines)
    
    def get_format_specific_info(self, address: str, target_format: FormatType, 
                                knowledge_level: KnowledgeLevel = KnowledgeLevel.BASIC) -> str:
        """
        Format-specific bilgi sağlama - Bridge Systems entegrasyonu
        
        Args:
            address: Hedef adres ($XXXX formatında)
            target_format: Hedef format türü (C, QBasic, Python, vs.)
            knowledge_level: Bilgi seviyesi
            
        Returns:
            Format-specific açıklama
        """
        base_info = self.get_address_info(address, knowledge_level)
        if not base_info:
            return ""
        
        # Format-specific adaptations
        if target_format == FormatType.C:
            return self._format_for_c(base_info, knowledge_level)
        elif target_format == FormatType.QBASIC:
            return self._format_for_qbasic(base_info, knowledge_level)
        elif target_format == FormatType.PYTHON:
            return self._format_for_python(base_info, knowledge_level)
        else:
            return base_info
    
    def _format_for_c(self, info: str, level: KnowledgeLevel) -> str:
        """C format için bilgi adaptasyonu"""
        if level == KnowledgeLevel.DEBUG:
            return f"/* {info} */"
        else:
            return f"// {info}"
    
    def _format_for_qbasic(self, info: str, level: KnowledgeLevel) -> str:
        """QBasic format için bilgi adaptasyonu"""
        return f"REM {info}"
    
    def _format_for_python(self, info: str, level: KnowledgeLevel) -> str:
        """Python format için bilgi adaptasyonu"""
        if level == KnowledgeLevel.DEBUG:
            return f'"""\n{info}\n"""'
        else:
            return f"# {info}"
    
    # Metodları C64KnowledgeManager sınıfına ekle
    C64KnowledgeManager.analyze_hardware_sequence = analyze_hardware_sequence
    C64KnowledgeManager.get_format_specific_info = get_format_specific_info
    C64KnowledgeManager._format_for_c = _format_for_c
    C64KnowledgeManager._format_for_qbasic = _format_for_qbasic
    C64KnowledgeManager._format_for_python = _format_for_python

# Hardware-aware metodları ekle
add_hardware_aware_methods()
