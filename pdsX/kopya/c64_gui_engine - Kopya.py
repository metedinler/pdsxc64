#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C64 GUI Engine - Commodore 64 Emülasyon GUI Sistemi
PDSX v12X entegrasyonu için özel C64 görsel ve ses emülasyonu

Özellikler:
- 320x200 C64 ekran emülasyonu
- 8 sprite yönetimi (PNG/BMP)
- 8x8 karakter seti sistemi
- SID müzik player
- POKE/PEEK memory emülasyonu
- C64 16 renk paleti
"""

import tkinter as tk
from tkinter import Canvas, PhotoImage
import pygame
import numpy as np
from PIL import Image, ImageTk
import os
import threading
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# C64 Renk Paleti (16 renk)
C64_COLORS = {
    0: "#000000",  # Siyah
    1: "#FFFFFF",  # Beyaz
    2: "#880000",  # Kırmızı
    3: "#AAFFEE",  # Cyan
    4: "#CC44CC",  # Mor
    5: "#00CC55",  # Yeşil
    6: "#0000AA",  # Mavi
    7: "#EEEE77",  # Sarı
    8: "#DD8855",  # Turuncu
    9: "#664400",  # Kahverengi
    10: "#FF7777", # Açık Kırmızı
    11: "#333333", # Koyu Gri
    12: "#777777", # Gri
    13: "#AAFF66", # Açık Yeşil
    14: "#0088FF", # Açık Mavi
    15: "#BBBBBB"  # Açık Gri
}

@dataclass
class C64Sprite:
    """C64 Sprite yapısı"""
    id: int
    x: int = 0
    y: int = 0
    enabled: bool = False
    image_path: str = ""
    color: int = 1
    multicolor: bool = False
    priority: int = 0
    double_width: bool = False
    double_height: bool = False
    image_data: Optional[ImageTk.PhotoImage] = None

@dataclass
class C64Memory:
    """C64 Memory emülasyonu"""
    sprite_x: List[int]          # $D000-$D00F
    sprite_y: List[int]          # $D001-$D00F  
    sprite_enable: int           # $D015
    sprite_color: List[int]      # $D027-$D02E
    border_color: int            # $D020
    background_color: int        # $D021
    charset_bank: int            # Karakter seti bankası
    
    def __init__(self):
        self.sprite_x = [0] * 8
        self.sprite_y = [0] * 8  
        self.sprite_enable = 0
        self.sprite_color = [1] * 8
        self.border_color = 14      # Açık mavi
        self.background_color = 6   # Mavi
        self.charset_bank = 0

class C64Display:
    """C64 Ekran emülasyonu"""
    
    def __init__(self, parent_widget, scale_factor=2):
        self.width = 320
        self.height = 200
        self.scale_factor = scale_factor
        self.scaled_width = self.width * scale_factor
        self.scaled_height = self.height * scale_factor
        
        # Tkinter Canvas oluştur
        self.canvas = Canvas(
            parent_widget,
            width=self.scaled_width,
            height=self.scaled_height,
            bg=C64_COLORS[6]  # Mavi arka plan
        )
        
        # Pixel buffer
        self.pixel_buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.screen_image = None
        
        # Karakter modu
        self.char_mode = True
        self.char_width = 40
        self.char_height = 25
        self.char_buffer = np.zeros((self.char_height, self.char_width), dtype=int)
        self.color_buffer = np.zeros((self.char_height, self.char_width), dtype=int)
        
    def clear_screen(self, color=6):
        """Ekranı temizle"""
        self.pixel_buffer.fill(0)
        rgb = self._hex_to_rgb(C64_COLORS[color])
        self.pixel_buffer[:, :] = rgb
        
    def set_pixel(self, x: int, y: int, color: int):
        """Tek pixel ayarla"""
        if 0 <= x < self.width and 0 <= y < self.height:
            rgb = self._hex_to_rgb(C64_COLORS[color])
            self.pixel_buffer[y, x] = rgb
            
    def draw_char(self, char_x: int, char_y: int, char_code: int, color: int = 1):
        """Karakter çiz (8x8)"""
        if 0 <= char_x < self.char_width and 0 <= char_y < self.char_height:
            self.char_buffer[char_y, char_x] = char_code
            self.color_buffer[char_y, char_x] = color
            
    def update_display(self):
        """Ekranı güncelle"""
        # Pixel buffer'ı PIL Image'e çevir
        image = Image.fromarray(self.pixel_buffer, 'RGB')
        
        # Ölçeklendir
        if self.scale_factor != 1:
            image = image.resize(
                (self.scaled_width, self.scaled_height), 
                Image.NEAREST
            )
        
        # Tkinter PhotoImage'e çevir
        self.screen_image = ImageTk.PhotoImage(image)
        
        # Canvas'a çiz
        self.canvas.delete("screen")
        self.canvas.create_image(
            0, 0, 
            anchor=tk.NW, 
            image=self.screen_image, 
            tags="screen"
        )
        
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Hex rengi RGB'ye çevir"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class C64SpriteManager:
    """C64 Sprite yöneticisi"""
    
    def __init__(self, display: C64Display):
        self.display = display
        self.sprites = [C64Sprite(i) for i in range(8)]
        self.sprite_images = {}
        
    def load_sprite(self, sprite_id: int, image_path: str) -> bool:
        """Sprite resmini yükle"""
        if not (0 <= sprite_id < 8):
            return False
            
        try:
            if os.path.exists(image_path):
                # PIL ile yükle ve boyutlandır
                image = Image.open(image_path)
                image = image.resize((24, 21), Image.NEAREST)
                
                # Tkinter PhotoImage'e çevir
                self.sprite_images[sprite_id] = ImageTk.PhotoImage(image)
                self.sprites[sprite_id].image_path = image_path
                self.sprites[sprite_id].image_data = self.sprite_images[sprite_id]
                return True
        except Exception as e:
            print(f"Sprite yükleme hatası: {e}")
        return False
        
    def set_sprite_position(self, sprite_id: int, x: int, y: int):
        """Sprite pozisyonunu ayarla"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].x = x
            self.sprites[sprite_id].y = y
            
    def enable_sprite(self, sprite_id: int, enabled: bool = True):
        """Sprite'ı aktif/pasif yap"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].enabled = enabled
            
    def set_sprite_color(self, sprite_id: int, color: int):
        """Sprite rengini ayarla"""
        if 0 <= sprite_id < 8 and 0 <= color < 16:
            self.sprites[sprite_id].color = color
            
    def draw_sprites(self):
        """Tüm aktif sprite'ları çiz"""
        self.display.canvas.delete("sprites")
        
        for sprite in self.sprites:
            if sprite.enabled and sprite.image_data:
                # Ölçeklenmiş pozisyon hesapla
                scaled_x = sprite.x * self.display.scale_factor
                scaled_y = sprite.y * self.display.scale_factor
                
                self.display.canvas.create_image(
                    scaled_x, scaled_y,
                    anchor=tk.NW,
                    image=sprite.image_data,
                    tags="sprites"
                )

class C64AudioManager:
    """C64 Müzik çalar (SID emülasyonu)"""
    
    def __init__(self):
        self.pygame_mixer_init = False
        self.current_music = None
        self.is_playing = False
        self.volume = 0.7
        
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame_mixer_init = True
        except Exception as e:
            print(f"Pygame mixer init hatası: {e}")
            
    def load_music(self, file_path: str) -> bool:
        """Müzik dosyası yükle (.mp3, .wav, .ogg)"""
        if not self.pygame_mixer_init:
            return False
            
        try:
            if os.path.exists(file_path):
                pygame.mixer.music.load(file_path)
                self.current_music = file_path
                return True
        except Exception as e:
            print(f"Müzik yükleme hatası: {e}")
        return False
        
    def play_music(self, loops=-1):
        """Müziği çal (loops: -1 = sonsuz döngü)"""
        if self.pygame_mixer_init and self.current_music:
            try:
                pygame.mixer.music.play(loops)
                self.is_playing = True
                return True
            except Exception as e:
                print(f"Müzik çalma hatası: {e}")
        return False
        
    def stop_music(self):
        """Müziği durdur"""
        if self.pygame_mixer_init:
            pygame.mixer.music.stop()
            self.is_playing = False
            
    def pause_music(self):
        """Müziği duraklat"""
        if self.pygame_mixer_init:
            pygame.mixer.music.pause()
            
    def unpause_music(self):
        """Müzik duraklatmayı kaldır"""
        if self.pygame_mixer_init:
            pygame.mixer.music.unpause()
            
    def set_volume(self, volume: float):
        """Ses düzeyini ayarla (0.0-1.0)"""
        if self.pygame_mixer_init:
            self.volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(self.volume)

class C64CharsetManager:
    """C64 Karakter seti yöneticisi"""
    
    def __init__(self):
        self.charset_images = {}
        self.current_charset = 0
        self.char_size = (8, 8)
        
    def load_charset(self, charset_id: int, folder_path: str) -> bool:
        """Karakter seti yükle (256 adet 8x8 PNG)"""
        try:
            charset = {}
            for i in range(256):
                char_file = os.path.join(folder_path, f"char_{i:03d}.png")
                if os.path.exists(char_file):
                    image = Image.open(char_file)
                    image = image.resize(self.char_size, Image.NEAREST)
                    charset[i] = ImageTk.PhotoImage(image)
                    
            if charset:
                self.charset_images[charset_id] = charset
                return True
        except Exception as e:
            print(f"Charset yükleme hatası: {e}")
        return False
        
    def set_charset(self, charset_id: int):
        """Aktif karakter setini değiştir"""
        if charset_id in self.charset_images:
            self.current_charset = charset_id
            return True
        return False
        
    def get_char_image(self, char_code: int) -> Optional[ImageTk.PhotoImage]:
        """Karakter resmini al"""
        if self.current_charset in self.charset_images:
            return self.charset_images[self.current_charset].get(char_code)
        return None

class C64GuiEngine:
    """Ana C64 GUI Engine"""
    
    def __init__(self, parent_widget=None):
        self.parent = parent_widget or tk.Tk()
        self.running = False
        
        # C64 bileşenleri
        self.display = C64Display(self.parent, scale_factor=2)
        self.sprite_manager = C64SpriteManager(self.display)
        self.audio_manager = C64AudioManager()
        self.charset_manager = C64CharsetManager()
        self.memory = C64Memory()
        
        # Update thread
        self.update_thread = None
        self.update_running = False
        
    def initialize(self):
        """Engine'i başlat"""
        self.display.canvas.pack()
        self.display.clear_screen(self.memory.background_color)
        self.display.update_display()
        
    def start_update_loop(self):
        """Güncelleme döngüsünü başlat"""
        if not self.update_running:
            self.update_running = True
            self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.update_thread.start()
            
    def stop_update_loop(self):
        """Güncelleme döngüsünü durdur"""
        self.update_running = False
        
    def _update_loop(self):
        """Ana güncelleme döngüsü (60 FPS)"""
        while self.update_running:
            try:
                # Ekranı güncelle
                self.display.update_display()
                
                # Sprite'ları çiz
                self.sprite_manager.draw_sprites()
                
                # 60 FPS için bekleme
                time.sleep(1/60)
                
            except Exception as e:
                print(f"Update loop hatası: {e}")
                
    def poke(self, address: int, value: int):
        """C64 POKE komutu emülasyonu"""
        # VIC-II registerleri
        if 0xD000 <= address <= 0xD00F:  # Sprite X pozisyonları
            sprite_id = (address - 0xD000) // 2
            if sprite_id < 8:
                self.memory.sprite_x[sprite_id] = value
                self.sprite_manager.set_sprite_position(
                    sprite_id, 
                    self.memory.sprite_x[sprite_id], 
                    self.memory.sprite_y[sprite_id]
                )
                
        elif 0xD001 <= address <= 0xD00F and (address - 0xD001) % 2 == 0:  # Sprite Y pozisyonları
            sprite_id = (address - 0xD001) // 2
            if sprite_id < 8:
                self.memory.sprite_y[sprite_id] = value
                self.sprite_manager.set_sprite_position(
                    sprite_id,
                    self.memory.sprite_x[sprite_id], 
                    self.memory.sprite_y[sprite_id]
                )
                
        elif address == 0xD015:  # Sprite enable register
            self.memory.sprite_enable = value
            for i in range(8):
                enabled = (value & (1 << i)) != 0
                self.sprite_manager.enable_sprite(i, enabled)
                
        elif address == 0xD020:  # Border color
            self.memory.border_color = value & 0x0F
            
        elif address == 0xD021:  # Background color
            self.memory.background_color = value & 0x0F
            self.display.clear_screen(self.memory.background_color)
            
        elif 0xD027 <= address <= 0xD02E:  # Sprite colors
            sprite_id = address - 0xD027
            if sprite_id < 8:
                self.memory.sprite_color[sprite_id] = value & 0x0F
                self.sprite_manager.set_sprite_color(sprite_id, value & 0x0F)
                
    def peek(self, address: int) -> int:
        """C64 PEEK komutu emülasyonu"""
        if 0xD000 <= address <= 0xD00F:
            sprite_id = (address - 0xD000) // 2
            if sprite_id < 8:
                return self.memory.sprite_x[sprite_id]
                
        elif address == 0xD015:
            return self.memory.sprite_enable
            
        elif address == 0xD020:
            return self.memory.border_color
            
        elif address == 0xD021:
            return self.memory.background_color
            
        elif 0xD027 <= address <= 0xD02E:
            sprite_id = address - 0xD027
            if sprite_id < 8:
                return self.memory.sprite_color[sprite_id]
                
        return 0
        
    def get_display_widget(self):
        """Display widget'ını döndür"""
        return self.display.canvas

# Test kodu
if __name__ == "__main__":
    root = tk.Tk()
    root.title("C64 GUI Engine Test")
    
    engine = C64GuiEngine(root)
    engine.initialize()
    engine.start_update_loop()
    
    # Test sprite yükle
    # engine.sprite_manager.load_sprite(0, "test_sprite.png")
    # engine.poke(0xD015, 1)  # Sprite 0'ı aktifleştir
    # engine.poke(0xD000, 100)  # X pozisyon
    # engine.poke(0xD001, 100)  # Y pozisyon
    
    root.mainloop()
    engine.stop_update_loop()
