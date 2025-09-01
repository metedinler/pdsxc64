#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced C64 Memory Manager v5.3
ROM DATA Full Integration - C64 KERNAL, BASIC, Memory Map ve Zero Page bilgilerini yöneten gelişmiş modül

PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: enhanced_c64_memory_manager.py - Enhanced C64 Memory Manager
VERSİYON: 5.3 (C64 ROM DATA Full Integration + 9187 Lines C64 Labels Database)
AMAÇ: C64 Memory Manager'ın gelişmiş versiyonu - kapsamlı ROM DATA entegrasyonu

Bu modül şu özelliklerle C64 Memory Manager'ı genişletir:
• 9187 Lines C64 Labels Database: Kapsamlı adres etiketleme sistemi
• Enhanced BASIC Tokens: Türkçe açıklama destekli token veritabanı
• System Pointers: Gelişmiş sistem pointer yönetimi
• Unified Address Lookup: Birleşik adres arama motoru
• ROM DATA Full Integration: Tüm c64_rom_data klasörü entegrasyonu

Extends: c64_memory_manager.py (base class)
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Logger kurulumu
logging.basicConfig(level=logging.INFO)

try:
    # Orijinal c64_memory_manager'ı import et
    from c64_memory_manager import C64MemoryMapManager
    BASE_CLASS = C64MemoryMapManager
except ImportError:
    # Eğer c64_memory_manager yoksa, basit base class kullan
    BASE_CLASS = object
    logging.warning("c64_memory_manager bulunamadı, basit base class kullanılıyor")


class EnhancedC64MemoryManager(BASE_CLASS):
    """C64 Memory Manager'ın gelişmiş versiyonu - ROM DATA entegrasyonu ile"""
    
    def __init__(self, rom_data_dir="c64_rom_data"):
        # Base class varsa initialize et
        if BASE_CLASS != object:
            super().__init__()
        
        self.logger = logging.getLogger(__name__)
        self.rom_data_dir = Path(rom_data_dir)
        
        # Enhanced data containers
        self.c64_labels = {}             # 9187 lines C64 labels database
        self.basic_tokens = {}           # BASIC token database  
        self.system_pointers = {}        # System pointer database
        self.unified_lookup = {}         # Unified address lookup
        
        # Load enhanced data
        self.load_basic_tokens()
        self.load_c64_labels()
        self.load_system_pointers()
        self.build_unified_lookup()
        
        self.logger.info("Enhanced C64 Memory Manager v5.3 başlatıldı")
    
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
            self.logger.warning("BASIC Tokens dosyası bulunamadı")
            self.basic_tokens = {}
    
    def load_c64_labels(self):
        """C64 Labels veritabanını yükle - 9187 lines"""
        labels_file = self.rom_data_dir / "labels" / "c64_labels.json"
        if labels_file.exists():
            try:
                with open(labels_file, 'r', encoding='utf-8') as f:
                    self.c64_labels = json.load(f)
                self.logger.info(f"C64 Labels yüklendi: {len(self.c64_labels)} entry")
            except Exception as e:
                self.logger.error(f"C64 Labels yükleme hatası: {e}")
                self.c64_labels = {}
        else:
            self.logger.warning("C64 Labels dosyası bulunamadı")
            self.c64_labels = {}
    
    def load_system_pointers(self):
        """System Pointers veritabanını yükle"""
        pointers_file = self.rom_data_dir / "system" / "system_pointers.json"
        if pointers_file.exists():
            try:
                with open(pointers_file, 'r', encoding='utf-8') as f:
                    self.system_pointers = json.load(f)
                self.logger.info(f"System Pointers yüklendi: {len(self.system_pointers)} entry")
            except Exception as e:
                self.logger.error(f"System Pointers yükleme hatası: {e}")
                self.system_pointers = {}
        else:
            self.logger.warning("System Pointers dosyası bulunamadı")
            self.system_pointers = {}
    
    def build_unified_lookup(self):
        """Birleşik adres arama motoru oluştur"""
        self.unified_lookup = {}
        
        # BASIC tokens ekle
        for token, info in self.basic_tokens.items():
            if isinstance(info, dict) and 'address' in info:
                addr = info['address']
                self.unified_lookup[addr] = {
                    'type': 'basic_token',
                    'token': token,
                    'info': info
                }
        
        # C64 labels ekle
        for label, info in self.c64_labels.items():
            if isinstance(info, dict) and 'address' in info:
                addr = info['address']
                if addr not in self.unified_lookup:
                    self.unified_lookup[addr] = {
                        'type': 'c64_label',
                        'label': label,
                        'info': info
                    }
        
        # System pointers ekle
        for pointer, info in self.system_pointers.items():
            if isinstance(info, dict) and 'address' in info:
                addr = info['address']
                if addr not in self.unified_lookup:
                    self.unified_lookup[addr] = {
                        'type': 'system_pointer',
                        'pointer': pointer,
                        'info': info
                    }
        
        self.logger.info(f"Unified Lookup oluşturuldu: {len(self.unified_lookup)} entry")
    
    def lookup_address(self, address: int) -> Optional[Dict[str, Any]]:
        """Adresi birleşik veritabanında ara"""
        # Hex string'i int'e çevir
        if isinstance(address, str):
            if address.startswith('$'):
                address = int(address[1:], 16)
            elif address.startswith('0x'):
                address = int(address, 16)
            else:
                try:
                    address = int(address)
                except ValueError:
                    return None
        
        return self.unified_lookup.get(address)
    
    def get_basic_token_info(self, token: str) -> Optional[Dict[str, Any]]:
        """BASIC token bilgisini getir"""
        return self.basic_tokens.get(token)
    
    def get_c64_label_info(self, label: str) -> Optional[Dict[str, Any]]:
        """C64 label bilgisini getir"""
        return self.c64_labels.get(label)
    
    def get_system_pointer_info(self, pointer: str) -> Optional[Dict[str, Any]]:
        """System pointer bilgisini getir"""
        return self.system_pointers.get(pointer)
    
    def get_memory_info(self, address: int) -> Dict[str, Any]:
        """Belirli bir adres için kapsamlı bilgi getir"""
        info = {
            'address': address,
            'hex': f"${address:04X}",
            'decimal': address,
            'found_in': []
        }
        
        # Unified lookup'ta ara
        lookup_result = self.lookup_address(address)
        if lookup_result:
            info['unified_lookup'] = lookup_result
            info['found_in'].append('unified_lookup')
        
        # Base class method varsa çağır
        if hasattr(super(), 'get_memory_info'):
            base_info = super().get_memory_info(address)
            if base_info:
                info['base_class'] = base_info
                info['found_in'].append('base_class')
        
        return info
    
    def export_enhanced_data(self, output_file: str):
        """Enhanced veriyi JSON olarak export et"""
        export_data = {
            'metadata': {
                'version': '5.3',
                'description': 'Enhanced C64 Memory Manager - ROM DATA Full Integration',
                'basic_tokens_count': len(self.basic_tokens),
                'c64_labels_count': len(self.c64_labels),
                'system_pointers_count': len(self.system_pointers),
                'unified_lookup_count': len(self.unified_lookup)
            },
            'basic_tokens': self.basic_tokens,
            'c64_labels': self.c64_labels,
            'system_pointers': self.system_pointers,
            'unified_lookup': self.unified_lookup
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Enhanced data exported to: {output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Export hatası: {e}")
            return False


# Global instance
enhanced_c64_memory_manager = EnhancedC64MemoryManager()

# Test fonksiyonu
def test_enhanced_memory_manager():
    """Enhanced Memory Manager'ı test et"""
    print("Enhanced C64 Memory Manager v5.3 Test")
    print("=" * 50)
    
    manager = EnhancedC64MemoryManager()
    
    # Test adresleri
    test_addresses = [0x0000, 0xA000, 0xE000, 0xFFFA]
    
    for addr in test_addresses:
        info = manager.get_memory_info(addr)
        print(f"Address ${addr:04X}: {info}")
    
    print("\nTest tamamlandı.")

if __name__ == "__main__":
    test_enhanced_memory_manager()
