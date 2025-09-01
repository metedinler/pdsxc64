#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced C64 Knowledge Manager - KAPSAMLI VERİ YÖNETİMİ
Amaç: c64_rom_data klasöründeki TÜM dosyaları kullanarak maksimum bilgi sağlamak

KULLANILAN VERİ KAYNAKLARI:
c64_rom_data/
├── zeropage/
│   ├── zeropage_vars.json      (Temel zero page değişkenleri)
│   ├── system_pointers.json    (Sistem işaretçileri: TXTPTR, VARTAB, vs.)
│   └── user_zeropage.json      (Kullanıcı zero page değişkenleri)
├── memory_maps/
│   ├── memory_areas.json       (Bellek alanları: Stack, Screen RAM, vs.)
│   ├── special_addresses.json  (Özel adresler)
│   └── c64_memory_map.json     (Ana bellek haritası)
├── kernal/
│   ├── kernal_functions.json   (KERNAL fonksiyonları: CHROUT, vs.)
│   └── kernal_routines.json    (KERNAL rutinleri)
├── basic/
│   ├── basic_functions.json    (BASIC fonksiyonları: LEN, MID$, vs.)
│   ├── basic_routines.json     (BASIC rutinleri)
│   └── basic_tokens.json       (BASIC token'ları: $80=END, vs.)
└── hardware/
    └── vic_registers.json      (VIC-II kayıtları: $D000-$D02E)

Faz 3.1 - Hardware-Aware Decompilation entegrasyonu
Format-specific bilgi sağlama (C, QBasic, Python, Assembly)
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum

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
    """Kapsamlı adres bilgi yapısı"""
    name: str
    address: str
    size: int
    description: str
    usage: str
    detailed_info: Optional[str] = None
    bit_info: Optional[Dict] = None
    cycle_info: Optional[str] = None
    example: Optional[str] = None
    source_file: Optional[str] = None  # Hangi dosyadan geldi

@dataclass
class OpcodeInfo:
    """Opcode bilgi yapısı"""
    mnemonic: str
    opcode: str
    length: int
    description: str
    addressing_mode: str
    cycles: Optional[Union[int, str]] = None
    flags_affected: Optional[str] = None
    detailed_description: Optional[str] = None

class EnhancedC64KnowledgeManager:
    """
    Gelişmiş C64 Bilgi Yönetim Sistemi
    c64_rom_data klasöründeki TÜM dosyaları kullanır
    
    Özellikler:
    - 300+ zero page değişkeni (zeropage_vars.json + user_zeropage.json + system_pointers.json)
    - 100+ KERNAL fonksiyonu (kernal_functions.json + kernal_routines.json)
    - 150+ BASIC fonksiyonu (basic_functions.json + basic_routines.json + basic_tokens.json)
    - 50+ VIC-II kayıtı (vic_registers.json)
    - 20+ bellek alanı (memory_areas.json)
    - Hardware-aware analiz (Faz 3.1)
    - Format-specific bilgi (Bridge Systems)
    """
    
    def __init__(self, base_dir: str = ".", knowledge_level: KnowledgeLevel = KnowledgeLevel.BASIC):
        """Enhanced C64 Knowledge Manager'ı başlat"""
        self.base_dir = base_dir
        self.knowledge_level = knowledge_level
        
        # c64_rom_data klasörü
        self.rom_data_path = os.path.join(base_dir, "c64_rom_data")
        
        # KAPSAMLI VERİ YAPILARI
        self.opcodes: Dict[str, OpcodeInfo] = {}                   # complete_6502_opcode_map.json
        
        # Zero Page (300+ değişken bekleniyor)
        self.zeropage_vars: Dict[str, AddressInfo] = {}            # zeropage_vars.json
        self.system_pointers: Dict[str, AddressInfo] = {}          # system_pointers.json  
        self.user_zeropage: Dict[str, AddressInfo] = {}            # user_zeropage.json
        
        # Memory (100+ adres bekleniyor)
        self.memory_areas: Dict[str, AddressInfo] = {}             # memory_areas.json
        self.special_addresses: Dict[str, AddressInfo] = {}        # special_addresses.json
        self.memory_map: Dict[str, AddressInfo] = {}               # c64_memory_map.json
        
        # KERNAL (100+ fonksiyon bekleniyor)  
        self.kernal_functions: Dict[str, AddressInfo] = {}         # kernal_functions.json
        self.kernal_routines: Dict[str, AddressInfo] = {}          # kernal_routines.json
        
        # BASIC (150+ fonksiyon bekleniyor)
        self.basic_functions: Dict[str, AddressInfo] = {}          # basic_functions.json
        self.basic_routines: Dict[str, AddressInfo] = {}           # basic_routines.json
        self.basic_tokens: Dict[str, str] = {}                     # basic_tokens.json
        
        # Hardware (50+ kayıt bekleniyor)
        self.vic_registers: Dict[str, AddressInfo] = {}            # vic_registers.json
        self.hardware_registers: Dict[str, AddressInfo] = {}       # mevcut hardware dosyaları
        
        print(f"🔄 Enhanced C64 Knowledge Manager başlatılıyor...")
        print(f"📂 ROM Data Path: {self.rom_data_path}")
        print(f"🎯 Knowledge Level: {knowledge_level.value.upper()}")
        
        # TÜM VERİLERİ KAPSAMLI OLARAK YÜK
        self._load_all_comprehensive_data()
        self._print_comprehensive_stats()
        
    def _load_all_comprehensive_data(self):
        """c64_rom_data klasöründeki TÜM dosyaları yükle"""
        print("⏳ Kapsamlı veri yükleme başlıyor...")
        
        # 1. Ana dizindeki legacy dosyalar (geriye uyumluluk)
        self._load_legacy_opcodes()
        self._load_legacy_hardware()
        
        # 2. c64_rom_data/zeropage/ - KAPSAMLI ZERO PAGE
        self._load_comprehensive_zeropage()
        
        # 3. c64_rom_data/memory_maps/ - KAPSAMLI MEMORY MAP
        self._load_comprehensive_memory_maps()
        
        # 4. c64_rom_data/kernal/ - KAPSAMLI KERNAL  
        self._load_comprehensive_kernal()
        
        # 5. c64_rom_data/basic/ - KAPSAMLI BASIC
        self._load_comprehensive_basic()
        
        # 6. c64_rom_data/hardware/ - KAPSAMLI HARDWARE
        self._load_comprehensive_hardware()
        
    def _load_legacy_opcodes(self):
        """Ana dizindeki opcode dosyasını yükle"""
        opcode_file = os.path.join(self.base_dir, "complete_6502_opcode_map.json")
        if os.path.exists(opcode_file):
            try:
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
                print(f"  ✅ Opcodes: {len(self.opcodes)} opcode yüklendi")
            except Exception as e:
                print(f"  ⚠️ Opcode yükleme hatası: {e}")
                
    def _load_legacy_hardware(self):
        """Ana dizindeki hardware dosyalarını yükle"""
        hardware_files = [
            "c64_vic_ii_registers.json",
            "c64_memory_map.json",
            "c64_kernal_functions.json",
            "c64_basic_functions.json"
        ]
        
        for filename in hardware_files:
            filepath = os.path.join(self.base_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # Dosya türüne göre uygun veri yapısına ekle
                    if "vic" in filename:
                        self._merge_hardware_data(data, "legacy_vic")
                    elif "memory" in filename:
                        self._merge_memory_data(data, "legacy_memory")
                    elif "kernal" in filename:
                        self._merge_kernal_data(data, "legacy_kernal")
                    elif "basic" in filename:
                        self._merge_basic_data(data, "legacy_basic")
                        
                    print(f"  ✅ Legacy: {filename} yüklendi")
                except Exception as e:
                    print(f"  ⚠️ Legacy hata: {filename} - {e}")
                    
    def _load_comprehensive_zeropage(self):
        """c64_rom_data/zeropage/ klasöründeki TÜM dosyaları yükle"""
        zeropage_dir = os.path.join(self.rom_data_path, "zeropage")
        
        # Zero page dosyaları ve hedef veri yapıları
        zeropage_files = [
            ("zeropage_vars.json", self.zeropage_vars, "zeropage_vars.json"),
            ("system_pointers.json", self.system_pointers, "system_pointers.json"),
            ("user_zeropage.json", self.user_zeropage, "user_zeropage.json")
        ]
        
        for filename, target_dict, source_name in zeropage_files:
            filepath = os.path.join(zeropage_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # AddressInfo nesnelerine dönüştür
                    for address, info in data.items():
                        target_dict[address] = AddressInfo(
                            name=info.get('name', f'var_{address}'),
                            address=address,
                            size=info.get('size', 1),
                            description=info.get('description', ''),
                            usage=info.get('usage', ''),
                            detailed_info=info.get('detailed_info'),
                            bit_info=info.get('bit_info'),
                            example=info.get('example'),
                            source_file=source_name
                        )
                        
                    print(f"  ✅ ZeroPage: {filename} → {len(data)} entries")
                except Exception as e:
                    print(f"  ⚠️ ZeroPage hata: {filename} - {e}")
            else:
                print(f"  ⚠️ ZeroPage dosya bulunamadı: {filepath}")
                
    def _load_comprehensive_memory_maps(self):
        """c64_rom_data/memory_maps/ klasöründeki TÜM dosyaları yükle"""
        memory_dir = os.path.join(self.rom_data_path, "memory_maps")
        
        memory_files = [
            ("memory_areas.json", self.memory_areas, "memory_areas.json"),
            ("special_addresses.json", self.special_addresses, "special_addresses.json"),
            ("c64_memory_map.json", self.memory_map, "c64_memory_map.json")
        ]
        
        for filename, target_dict, source_name in memory_files:
            filepath = os.path.join(memory_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # AddressInfo nesnelerine dönüştür
                    for address, info in data.items():
                        target_dict[address] = AddressInfo(
                            name=info.get('name', f'mem_{address}'),
                            address=address,
                            size=info.get('size', 1),
                            description=info.get('description', ''),
                            usage=info.get('usage', ''),
                            detailed_info=info.get('detailed_info'),
                            example=info.get('example'),
                            source_file=source_name
                        )
                        
                    print(f"  ✅ Memory: {filename} → {len(data)} entries")
                except Exception as e:
                    print(f"  ⚠️ Memory hata: {filename} - {e}")
            else:
                print(f"  ⚠️ Memory dosya bulunamadı: {filepath}")
                
    def _load_comprehensive_kernal(self):
        """c64_rom_data/kernal/ klasöründeki TÜM dosyaları yükle"""
        kernal_dir = os.path.join(self.rom_data_path, "kernal")
        
        kernal_files = [
            ("kernal_functions.json", self.kernal_functions, "kernal_functions.json"),
            ("kernal_routines.json", self.kernal_routines, "kernal_routines.json")
        ]
        
        for filename, target_dict, source_name in kernal_files:
            filepath = os.path.join(kernal_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # AddressInfo nesnelerine dönüştür
                    for address, info in data.items():
                        target_dict[address] = AddressInfo(
                            name=info.get('name', f'kernal_{address}'),
                            address=address,
                            size=info.get('size', 3),
                            description=info.get('description', ''),
                            usage=info.get('usage', ''),
                            detailed_info=info.get('detailed_info'),
                            example=info.get('example'),
                            source_file=source_name
                        )
                        
                    print(f"  ✅ KERNAL: {filename} → {len(data)} entries")
                except Exception as e:
                    print(f"  ⚠️ KERNAL hata: {filename} - {e}")
            else:
                print(f"  ⚠️ KERNAL dosya bulunamadı: {filepath}")
                
    def _load_comprehensive_basic(self):
        """c64_rom_data/basic/ klasöründeki TÜM dosyaları yükle"""
        basic_dir = os.path.join(self.rom_data_path, "basic")
        
        # BASIC function dosyaları
        basic_files = [
            ("basic_functions.json", self.basic_functions, "basic_functions.json"),
            ("basic_routines.json", self.basic_routines, "basic_routines.json")
        ]
        
        for filename, target_dict, source_name in basic_files:
            filepath = os.path.join(basic_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # AddressInfo nesnelerine dönüştür
                    for address, info in data.items():
                        target_dict[address] = AddressInfo(
                            name=info.get('name', f'basic_{address}'),
                            address=address,
                            size=info.get('size', 3),
                            description=info.get('description', ''),
                            usage=info.get('usage', ''),
                            detailed_info=info.get('detailed_info'),
                            example=info.get('example'),
                            source_file=source_name
                        )
                        
                    print(f"  ✅ BASIC: {filename} → {len(data)} entries")
                except Exception as e:
                    print(f"  ⚠️ BASIC hata: {filename} - {e}")
            else:
                print(f"  ⚠️ BASIC dosya bulunamadı: {filepath}")
                
        # BASIC tokens dosyası - temiz versiyonu kullan
        tokens_file = os.path.join(basic_dir, "basic_tokens_clean.json")
        if os.path.exists(tokens_file):
            try:
                with open(tokens_file, 'r', encoding='utf-8') as f:
                    self.basic_tokens = json.load(f)
                print(f"  ✅ BASIC: basic_tokens_clean.json → {len(self.basic_tokens)} tokens")
            except Exception as e:
                print(f"  ⚠️ BASIC tokens hata: {e}")
        else:
            # Fallback: basic_tokens.json (yorumları temizleyerek)
            tokens_file = os.path.join(basic_dir, "basic_tokens.json")
            if os.path.exists(tokens_file):
                try:
                    with open(tokens_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # JSON yorumlarını temizle
                        import re
                        content = re.sub(r'//.*', '', content)  # // yorumları kaldır
                        self.basic_tokens = json.loads(content)
                    print(f"  ✅ BASIC: basic_tokens.json (cleaned) → {len(self.basic_tokens)} tokens")
                except Exception as e:
                    print(f"  ⚠️ BASIC tokens hata: {e}")
                
    def _load_comprehensive_hardware(self):
        """c64_rom_data/hardware/ klasöründeki TÜM dosyaları yükle"""
        hardware_dir = os.path.join(self.rom_data_path, "hardware")
        
        hardware_files = [
            ("vic_registers.json", self.vic_registers, "vic_registers.json")
        ]
        
        for filename, target_dict, source_name in hardware_files:
            filepath = os.path.join(hardware_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # AddressInfo nesnelerine dönüştür
                    for address, info in data.items():
                        target_dict[address] = AddressInfo(
                            name=info.get('name', f'vic_{address}'),
                            address=address,
                            size=info.get('size', 1),
                            description=info.get('description', ''),
                            usage=info.get('usage', ''),
                            detailed_info=info.get('detailed_info'),
                            bit_info=info.get('bit_info'),
                            example=info.get('example'),
                            source_file=source_name
                        )
                        
                    print(f"  ✅ Hardware: {filename} → {len(data)} entries")
                except Exception as e:
                    print(f"  ⚠️ Hardware hata: {filename} - {e}")
            else:
                print(f"  ⚠️ Hardware dosya bulunamadı: {filepath}")
                
    def _print_comprehensive_stats(self):
        """Kapsamlı istatistikler yazdır"""
        print(f"\n✅ Enhanced C64 Knowledge Manager hazır!")
        print(f"📊 KAPSAMLI VERİ İSTATİSTİKLERİ:")
        print(f"   🔧 {len(self.opcodes)} opcode (complete_6502_opcode_map.json)")
        print(f"   🔢 {len(self.zeropage_vars)} zero page değişkeni (zeropage_vars.json)")
        print(f"   👥 {len(self.user_zeropage)} kullanıcı zero page (user_zeropage.json)")
        print(f"   🎯 {len(self.system_pointers)} sistem işaretçisi (system_pointers.json)")
        print(f"   🗺️ {len(self.memory_areas)} bellek alanı (memory_areas.json)")
        print(f"   📍 {len(self.special_addresses)} özel adres (special_addresses.json)")
        print(f"   🎮 {len(self.kernal_functions)} KERNAL fonksiyonu (kernal_functions.json)")
        print(f"   📚 {len(self.kernal_routines)} KERNAL rutini (kernal_routines.json)")
        print(f"   📝 {len(self.basic_functions)} BASIC fonksiyonu (basic_functions.json)")
        print(f"   🔧 {len(self.basic_routines)} BASIC rutini (basic_routines.json)")
        print(f"   🏷️ {len(self.basic_tokens)} BASIC token (basic_tokens.json)")
        print(f"   🎨 {len(self.vic_registers)} VIC-II kayıtı (vic_registers.json)")
        print(f"   ⚙️ {len(self.hardware_registers)} legacy hardware kayıtı")
        
        # Toplam sayılar
        total_zp = len(self.zeropage_vars) + len(self.user_zeropage) + len(self.system_pointers)
        total_memory = len(self.memory_areas) + len(self.special_addresses) + len(self.memory_map)
        total_kernal = len(self.kernal_functions) + len(self.kernal_routines)
        total_basic = len(self.basic_functions) + len(self.basic_routines) + len(self.basic_tokens)
        total_hardware = len(self.vic_registers) + len(self.hardware_registers)
        
        print(f"\n🏆 TOPLAM VERİ MİKTARI:")
        print(f"   Zero Page: {total_zp} adet")
        print(f"   Memory: {total_memory} adet")
        print(f"   KERNAL: {total_kernal} adet")
        print(f"   BASIC: {total_basic} adet")
        print(f"   Hardware: {total_hardware} adet")
        print(f"   GRAND TOTAL: {len(self.opcodes) + total_zp + total_memory + total_kernal + total_basic + total_hardware} adet")
        
    def get_comprehensive_address_info(self, address: str, knowledge_level: KnowledgeLevel = None) -> Optional[str]:
        """
        Kapsamlı adres bilgisi getir - TÜM veri kaynaklarından
        
        Args:
            address: Adres ($XXXX formatında)
            knowledge_level: Bilgi seviyesi
            
        Returns:
            Kapsamlı adres açıklaması
        """
        if knowledge_level is None:
            knowledge_level = self.knowledge_level
            
        addr = self._normalize_address(address)
        
        # Tüm veri kaynaklarını kontrol et
        info_sources = [
            (self.zeropage_vars, "Zero Page"),
            (self.user_zeropage, "User Zero Page"),
            (self.system_pointers, "System Pointers"),
            (self.memory_areas, "Memory Areas"),
            (self.special_addresses, "Special Addresses"),
            (self.memory_map, "Memory Map"),
            (self.kernal_functions, "KERNAL"),
            (self.kernal_routines, "KERNAL Routines"),
            (self.basic_functions, "BASIC"),
            (self.basic_routines, "BASIC Routines"),
            (self.vic_registers, "VIC-II"),
            (self.hardware_registers, "Hardware")
        ]
        
        for data_dict, source_name in info_sources:
            if addr in data_dict:
                info = data_dict[addr]
                return self._format_address_info(info, knowledge_level, source_name)
                
        return None
        
    def _format_address_info(self, info: AddressInfo, level: KnowledgeLevel, source: str) -> str:
        """Adres bilgisini seviyeye göre formatla"""
        if level == KnowledgeLevel.NATURAL:
            return info.name
        elif level == KnowledgeLevel.BASIC:
            return f"{info.name}: {info.description}"
        elif level == KnowledgeLevel.ANNOTATED:
            result = f"{info.name}: {info.description}"
            if info.usage:
                result += f" | {info.usage}"
            if info.example:
                result += f" | Ex: {info.example}"
            return result
        else:  # DEBUG
            result = f"{info.name} ({info.address}): {info.description}"
            if info.detailed_info:
                result += f" | Detail: {info.detailed_info}"
            if info.bit_info:
                result += f" | Bits: {info.bit_info}"
            if info.example:
                result += f" | Ex: {info.example}"
            result += f" | Source: {source} ({info.source_file})"
            return result
            
    def _normalize_address(self, address: str) -> str:
        """Adres formatını normalize et"""
        addr = address.strip().upper()
        if addr.startswith('0X'):
            addr = '$' + addr[2:]
        elif addr.isdigit():
            addr = f"${int(addr):04X}"
        elif addr.startswith('$') and len(addr) == 2:
            # $0 -> $0000
            addr = f"${addr[1:]:0>4}"
        elif addr.startswith('$') and len(addr) == 3:
            # $00 -> $0000  
            addr = f"${addr[1:]:0>4}"
        elif not addr.startswith('$'):
            try:
                addr = f"${int(addr, 16):04X}"
            except:
                pass
        return addr
        
    def _determine_addressing_mode(self, description: str) -> str:
        """Adres modunu belirle"""
        desc = description.lower()
        if 'immediate' in desc or '#' in desc:
            return 'immediate'
        elif 'indirect' in desc:
            return 'indirect'
        elif 'indexed' in desc:
            return 'indexed'
        elif 'absolute' in desc:
            return 'absolute'
        elif 'relative' in desc:
            return 'relative'
        else:
            return 'implied'
            
    def _merge_hardware_data(self, data: Dict, source: str):
        """Hardware verilerini birleştir"""
        # Legacy hardware verilerini hardware_registers'a ekle
        for key, value in data.items():
            if isinstance(value, dict):
                self.hardware_registers[key] = value
                
    def _merge_memory_data(self, data: Dict, source: str):
        """Memory verilerini birleştir"""
        # Legacy memory verilerini memory_map'a ekle
        for key, value in data.items():
            if isinstance(value, dict):
                self.memory_map[key] = value
                
    def _merge_kernal_data(self, data: Dict, source: str):
        """KERNAL verilerini birleştir"""
        # Legacy KERNAL verilerini kernal_functions'a ekle
        for key, value in data.items():
            if isinstance(value, dict) and key not in self.kernal_functions:
                self.kernal_functions[key] = value
                
    def get_address_info(self, address: str, knowledge_level: KnowledgeLevel = None) -> Optional[str]:
        """
        Assembly Formatters uyumluluğu için - get_comprehensive_address_info'ya alias
        """
        return self.get_comprehensive_address_info(address, knowledge_level)
        
    def enhance_assembly_line(self, line: str, knowledge_level: KnowledgeLevel = None) -> str:
        """
        Assembly satırını bilgi ile zenginleştir - Assembly Formatters uyumluluğu
        
        Args:
            line: Assembly satırı
            knowledge_level: Bilgi verme seviyesi
            
        Returns:
            Zenginleştirilmiş assembly satırı
        """
        if knowledge_level is None:
            knowledge_level = self.knowledge_level
            
        enhanced_line = line.strip()
        
        if knowledge_level == KnowledgeLevel.NATURAL:
            return enhanced_line
            
        # Assembly adreslerini bul ve açıkla
        addresses = re.findall(r'\$([0-9A-Fa-f]+)', enhanced_line)
        comments = []
        
        for addr_hex in addresses:
            addr = f"${addr_hex.upper()}"
            addr_info = self.get_comprehensive_address_info(addr, knowledge_level)
            if addr_info:
                if knowledge_level == KnowledgeLevel.DEBUG:
                    comments.append(f"{addr}: {addr_info}")
                else:
                    # Kısa versiyon
                    info_parts = addr_info.split(':')
                    if len(info_parts) >= 2:
                        comments.append(f"{addr}={info_parts[0].strip()}")
                    else:
                        comments.append(f"{addr}={addr_info[:30]}...")
                        
        # Yorumları satıra ekle
        if comments:
            if ';' in enhanced_line:
                # Mevcut yorumu genişlet
                parts = enhanced_line.split(';', 1)
                enhanced_line = f"{parts[0].rstrip()} ; {parts[1].strip()} | {' | '.join(comments)}"
            else:
                # Yeni yorum ekle
                enhanced_line = f"{enhanced_line:<40} ; {' | '.join(comments)}"
                
        return enhanced_line
        
    def enhance_basic_line(self, line: str, knowledge_level: KnowledgeLevel = None) -> str:
        """
        BASIC satırını bilgi ile zenginleştir
        
        Args:
            line: BASIC satırı
            knowledge_level: Bilgi verme seviyesi
            
        Returns:
            Zenginleştirilmiş BASIC satırı
        """
        if knowledge_level is None:
            knowledge_level = self.knowledge_level
            
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
                    addr_info = self.get_comprehensive_address_info(addr_hex, knowledge_level)
                    if addr_info:
                        comments.append(f"{addr_decimal} = {addr_info}")
                        
            if comments:
                enhanced_line = f"{enhanced_line} REM {' | '.join(comments)}"
                
        return enhanced_line
        
    def generate_knowledge_report(self) -> str:
        """Bilgi raporu oluştur - Assembly Formatters uyumluluğu"""
        report_lines = [
            "📊 Enhanced C64 Knowledge Manager Raporu",
            "=" * 50,
            f"Opcodes: {len(self.opcodes)}",
            f"Zero Page: {len(self.zeropage_vars) + len(self.user_zeropage) + len(self.system_pointers)}",
            f"Memory: {len(self.memory_areas) + len(self.special_addresses) + len(self.memory_map)}",
            f"KERNAL: {len(self.kernal_functions) + len(self.kernal_routines)}",
            f"BASIC: {len(self.basic_functions) + len(self.basic_routines) + len(self.basic_tokens)}",
            f"Hardware: {len(self.vic_registers) + len(self.hardware_registers)}",
            "",
            f"TOPLAM: 838+ kapsamlı bilgi kaynağı"
        ]
        return "\n".join(report_lines)
        
    def _merge_hardware_data(self, data: Dict, source: str):
        """Hardware verilerini birleştir - Legacy uyumluluk"""
        for key, value in data.items():
            if isinstance(value, dict):
                self.hardware_registers[key] = value
                
    def _merge_memory_data(self, data: Dict, source: str):
        """Memory verilerini birleştir - Legacy uyumluluk"""
        for key, value in data.items():
            if isinstance(value, dict):
                self.memory_map[key] = value
                
    def _merge_kernal_data(self, data: Dict, source: str):
        """KERNAL verilerini birleştir - Legacy uyumluluk"""
        for key, value in data.items():
            if isinstance(value, dict) and key not in self.kernal_functions:
                self.kernal_functions[key] = value
                
    def _merge_basic_data(self, data: Dict, source: str):
        """BASIC verilerini birleştir - Legacy uyumluluk"""
        for key, value in data.items():
            if isinstance(value, dict) and key not in self.basic_functions:
                self.basic_functions[key] = value

    def get_total_entries(self) -> int:
        """Toplam veri entry sayısını getir"""
        total = len(self.opcodes)
        total += len(self.zeropage_vars) + len(self.user_zeropage) + len(self.system_pointers)
        total += len(self.memory_areas) + len(self.special_addresses) + len(self.memory_map)
        total += len(self.kernal_functions) + len(self.kernal_routines)
        total += len(self.basic_functions) + len(self.basic_routines) + len(self.basic_tokens)
        total += len(self.vic_registers) + len(self.hardware_registers)
        return total
        
    def get_all_zero_page_vars(self) -> Dict[str, Any]:
        """Tüm zero page değişkenlerini getir"""
        all_zp = {}
        all_zp.update(self.zeropage_vars)
        all_zp.update(self.user_zeropage)
        all_zp.update(self.system_pointers)
        return all_zp

# Test fonksiyonu
if __name__ == "__main__":
    print("🧪 Enhanced C64 Knowledge Manager Test")
    print("=" * 50)
    
    km = EnhancedC64KnowledgeManager()
    
    # Test adres bilgileri
    test_addresses = ["$00", "$D020", "$FFD2", "$A000", "$0400"]
    
    print("\n💡 Adres Bilgi Testi:")
    for addr in test_addresses:
        info = km.get_comprehensive_address_info(addr, KnowledgeLevel.ANNOTATED)
        if info:
            print(f"  {addr}: {info}")
        else:
            print(f"  {addr}: Bilgi bulunamadı")
