#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sprite Converter for C64
C64 sprite verilerini PNG formatına çeviren modül
"""

import os
import logging
from pathlib import Path
from typing import List, Optional, Tuple

# PIL import - güvenli yükleme
try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
    print("✅ PIL (Pillow) yüklendi - Sprite conversion aktif")
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL (Pillow) bulunamadı - Sprite conversion devre dışı")

class SpriteConverter:
    """C64 Sprite Converter"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.sprite_width = 24
        self.sprite_height = 21
        self.colors = {
            0: (0, 0, 0),        # Black
            1: (255, 255, 255),  # White
            2: (136, 57, 50),    # Red
            3: (103, 182, 189),  # Cyan
            4: (139, 63, 150),   # Purple
            5: (85, 160, 73),    # Green
            6: (64, 49, 141),    # Blue
            7: (191, 206, 114),  # Yellow
            8: (139, 84, 41),    # Orange
            9: (87, 66, 0),      # Brown
            10: (184, 105, 98),  # Light Red
            11: (80, 80, 80),    # Dark Grey
            12: (120, 120, 120), # Grey
            13: (148, 224, 137), # Light Green
            14: (120, 105, 196), # Light Blue
            15: (159, 159, 159)  # Light Grey
        }
    
    def extract_sprite_data(self, data: bytes, offset: int = 0) -> Optional[bytes]:
        """C64 verilerinden sprite datasını çıkart"""
        if not PIL_AVAILABLE:
            self.logger.warning("PIL mevcut değil - sprite conversion yapılamaz")
            return None
        
        # C64 sprite: 63 byte (24x21 bit, 3 byte per row)
        sprite_size = 63
        
        if len(data) < offset + sprite_size:
            self.logger.error(f"Yetersiz veri: {len(data)} byte, gerekli: {offset + sprite_size}")
            return None
        
        return data[offset:offset + sprite_size]
    
    def sprite_to_png(self, sprite_data: bytes, output_path: str, 
                     color1: int = 1, color2: int = 0, multicolor: bool = False) -> bool:
        """Sprite verisini PNG formatına çevir"""
        if not PIL_AVAILABLE:
            self.logger.warning("PIL mevcut değil - PNG conversion yapılamaz")
            return False
        
        try:
            # Image oluştur
            scale = 8  # 8x büyütme
            img_width = self.sprite_width * scale
            img_height = self.sprite_height * scale
            
            img = Image.new('RGB', (img_width, img_height), self.colors[color2])
            draw = ImageDraw.Draw(img)
            
            # Sprite verilerini çözümle
            for y in range(self.sprite_height):
                row_offset = y * 3  # Her satır 3 byte
                if row_offset + 2 >= len(sprite_data):
                    break
                
                # 3 byte'ı birleştir (24 bit)
                byte1 = sprite_data[row_offset]
                byte2 = sprite_data[row_offset + 1] 
                byte3 = sprite_data[row_offset + 2]
                
                row_bits = (byte1 << 16) | (byte2 << 8) | byte3
                
                # Her bit için pixel çiz
                for x in range(self.sprite_width):
                    bit_pos = 23 - x  # MSB'den başla
                    if row_bits & (1 << bit_pos):
                        # Pixel aktif
                        pixel_color = self.colors[color1]
                        
                        # Büyütülmüş pixel çiz
                        x1 = x * scale
                        y1 = y * scale
                        x2 = x1 + scale
                        y2 = y1 + scale
                        
                        draw.rectangle([x1, y1, x2, y2], fill=pixel_color)
            
            # PNG olarak kaydet
            img.save(output_path, 'PNG')
            self.logger.info(f"Sprite PNG olarak kaydedildi: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Sprite PNG conversion hatası: {e}")
            return False
    
    def convert_prg_sprites(self, prg_data: bytes, output_dir: str = "png_files") -> List[str]:
        """PRG dosyasından sprite'ları çıkart ve PNG'ye çevir"""
        if not PIL_AVAILABLE:
            self.logger.warning("PIL mevcut değil - sprite conversion yapılamaz")
            return []
        
        # Çıktı dizinini oluştur
        Path(output_dir).mkdir(exist_ok=True)
        
        converted_files = []
        sprite_size = 63
        
        # PRG header'ı atla (2 byte)
        if len(prg_data) < 2:
            self.logger.error("Geçersiz PRG dosyası")
            return []
        
        code_data = prg_data[2:]
        
        # Olası sprite konumlarını ara
        for offset in range(0, len(code_data) - sprite_size + 1, sprite_size):
            sprite_data = code_data[offset:offset + sprite_size]
            
            # Sprite verisi olup olmadığını kontrol et
            if self.is_valid_sprite_data(sprite_data):
                sprite_num = offset // sprite_size
                output_file = os.path.join(output_dir, f"sprite_{sprite_num:03d}.png")
                
                if self.sprite_to_png(sprite_data, output_file):
                    converted_files.append(output_file)
        
        self.logger.info(f"{len(converted_files)} sprite PNG'ye çevrildi")
        return converted_files
    
    def is_valid_sprite_data(self, sprite_data: bytes) -> bool:
        """Sprite verisi geçerli mi kontrol et"""
        if len(sprite_data) != 63:
            return False
        
        # Tamamı 0 veya 255 değilse sprite olabilir
        zero_count = sprite_data.count(0)
        full_count = sprite_data.count(255)
        
        # En az %10 veri olmalı
        min_data = len(sprite_data) * 0.1
        data_count = len(sprite_data) - zero_count
        
        return data_count >= min_data and full_count < len(sprite_data) * 0.9
    
    def analyze_sprites(self, prg_data: bytes) -> dict:
        """PRG dosyasındaki sprite'ları analiz et"""
        analysis = {
            'total_sprites': 0,
            'valid_sprites': 0,
            'sprite_locations': [],
            'file_size': len(prg_data)
        }
        
        if len(prg_data) < 2:
            return analysis
        
        code_data = prg_data[2:]
        sprite_size = 63
        
        for offset in range(0, len(code_data) - sprite_size + 1, sprite_size):
            sprite_data = code_data[offset:offset + sprite_size]
            analysis['total_sprites'] += 1
            
            if self.is_valid_sprite_data(sprite_data):
                analysis['valid_sprites'] += 1
                analysis['sprite_locations'].append({
                    'offset': offset + 2,  # PRG header dahil
                    'sprite_num': offset // sprite_size,
                    'data_density': (len(sprite_data) - sprite_data.count(0)) / len(sprite_data)
                })
        
        self.logger.info(f"Sprite analizi: {analysis['valid_sprites']}/{analysis['total_sprites']} valid")
        return analysis

# Global instance
sprite_converter = SpriteConverter()

# Convenience functions
def convert_sprite_to_png(sprite_data: bytes, output_path: str, color1: int = 1, color2: int = 0) -> bool:
    """Sprite'ı PNG'ye çevir"""
    return sprite_converter.sprite_to_png(sprite_data, output_path, color1, color2)

def extract_sprites_from_prg(prg_data: bytes, output_dir: str = "png_files") -> List[str]:
    """PRG'den sprite'ları çıkart"""
    return sprite_converter.convert_prg_sprites(prg_data, output_dir)

def analyze_prg_sprites(prg_data: bytes) -> dict:
    """PRG sprite'larını analiz et"""
    return sprite_converter.analyze_sprites(prg_data)
