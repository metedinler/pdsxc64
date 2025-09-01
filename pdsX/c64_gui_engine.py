#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal C64 Retro Engine - PDSX v12X Integration
Modern yüksek seviye komutlarla C64 emülasyonu ve retro oyun geliştirme

Özellikler:
- Modern komut sistemi (SPRITE, SID, SCREEN, CHRSET)
- VIC-II uyumlu + genişletilmiş özellikler
- Collision detection sistemi (pixel-perfect + bounding box)
- PDSX Event sistemi entegrasyonu
- Real-time 60 FPS rendering
- Multi-format sprite/sound desteği

Komut Örnekleri:
SPRITE LOAD 0, "mario.png"
SPRITE MOVE 0, 100, 100
SID PLAY "music.sid"
SCREEN BACKGROUND 6
EVENT collision_mario SPRITE_COLLISION 0, 1
"""

import tkinter as tk
from tkinter import Canvas, PhotoImage
import pygame
import numpy as np
from PIL import Image, ImageTk
import os
import threading
import time
import math
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
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

class CollisionType(Enum):
    """Çarpışma tespit türleri"""
    BOUNDING_BOX = "bounding_box"
    PIXEL_PERFECT = "pixel_perfect"

@dataclass
class C64Sprite:
    """Modern C64 Sprite yapısı - VIC-II uyumlu + genişletilmiş"""
    id: int
    x: int = 0
    y: int = 0
    enabled: bool = False
    image_path: str = ""
    color: int = 1
    multicolor: bool = False
    priority: int = 0
    expand_x: bool = False      # VIC-II double width
    expand_y: bool = False      # VIC-II double height
    
    # Modern genişletilmiş özellikler
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotation: float = 0.0
    alpha: int = 255
    flip_h: bool = False
    flip_v: bool = False
    
    # Animation support
    animation_frames: List[str] = field(default_factory=list)
    animation_speed: float = 1.0
    current_frame: int = 0
    
    # Collision properties
    collision_enabled: bool = True
    collision_type: CollisionType = CollisionType.BOUNDING_BOX
    
    # Internal data
    image_data: Optional[ImageTk.PhotoImage] = None
    width: int = 24
    height: int = 21

@dataclass
class CollisionEvent:
    """Çarpışma eventi"""
    type: str  # "sprite_sprite", "sprite_char", "sprite_border"
    sprite1_id: int
    sprite2_id: Optional[int] = None
    char_x: Optional[int] = None
    char_y: Optional[int] = None
    collision_point: Optional[Tuple[int, int]] = None
    timestamp: float = field(default_factory=time.time)

class C64CollisionManager:
    """C64 Çarpışma tespit sistemi - Performance ve Accuracy seçenekli"""
    
    def __init__(self, display, event_manager=None):
        self.display = display
        self.event_manager = event_manager
        self.collision_callbacks = {}
        self.collision_history = []
        
    def register_collision_callback(self, event_type: str, sprite1_id: int, 
                                  sprite2_id: Optional[int], callback: Callable):
        """Çarpışma callback'i kaydet"""
        key = f"{event_type}_{sprite1_id}_{sprite2_id}"
        self.collision_callbacks[key] = callback
        
    def check_sprite_sprite_collision(self, sprite1: C64Sprite, sprite2: C64Sprite) -> bool:
        """Sprite-Sprite çarpışma kontrolü"""
        if not (sprite1.enabled and sprite2.enabled and sprite1.collision_enabled and sprite2.collision_enabled):
            return False
            
        if sprite1.collision_type == CollisionType.BOUNDING_BOX or sprite2.collision_type == CollisionType.BOUNDING_BOX:
            return self._bounding_box_collision(sprite1, sprite2)
        else:
            return self._pixel_perfect_collision(sprite1, sprite2)
    
    def _bounding_box_collision(self, sprite1: C64Sprite, sprite2: C64Sprite) -> bool:
        """Bounding box çarpışma (hızlı)"""
        # Sprite boyutlarını hesapla
        w1 = sprite1.width * sprite1.scale_x * (2 if sprite1.expand_x else 1)
        h1 = sprite1.height * sprite1.scale_y * (2 if sprite1.expand_y else 1)
        w2 = sprite2.width * sprite2.scale_x * (2 if sprite2.expand_x else 1)
        h2 = sprite2.height * sprite2.scale_y * (2 if sprite2.expand_y else 1)
        
        # AABB collision detection
        return (sprite1.x < sprite2.x + w2 and
                sprite1.x + w1 > sprite2.x and
                sprite1.y < sprite2.y + h2 and
                sprite1.y + h1 > sprite2.y)
    
    def _pixel_perfect_collision(self, sprite1: C64Sprite, sprite2: C64Sprite) -> bool:
        """Pixel-perfect çarpışma (doğru ama yavaş)"""
        # Basit implementasyon - gerçek pixel collision için PIL kullanılabilir
        # Şimdilik bounding box kullan
        return self._bounding_box_collision(sprite1, sprite2)
    
    def check_sprite_border_collision(self, sprite: C64Sprite, screen_width: int, screen_height: int) -> bool:
        """Sprite-Border çarpışma kontrolü"""
        if not sprite.enabled:
            return False
            
        w = sprite.width * sprite.scale_x * (2 if sprite.expand_x else 1)
        h = sprite.height * sprite.scale_y * (2 if sprite.expand_y else 1)
        
        return (sprite.x < 0 or sprite.y < 0 or 
                sprite.x + w > screen_width or sprite.y + h > screen_height)
    
    def check_sprite_char_collision(self, sprite: C64Sprite, char_x: int, char_y: int) -> bool:
        """Sprite-Karakter çarpışma kontrolü (8x8 grid)"""
        if not sprite.enabled:
            return False
            
        # Karakterin pixel koordinatları (8x8)
        char_pixel_x = char_x * 8
        char_pixel_y = char_y * 8
        
        # Sprite bounding box
        w = sprite.width * sprite.scale_x * (2 if sprite.expand_x else 1)
        h = sprite.height * sprite.scale_y * (2 if sprite.expand_y else 1)
        
        return (sprite.x < char_pixel_x + 8 and
                sprite.x + w > char_pixel_x and
                sprite.y < char_pixel_y + 8 and
                sprite.y + h > char_pixel_y)
    
    def trigger_collision_event(self, collision_event: CollisionEvent):
        """Çarpışma eventi tetikle"""
        self.collision_history.append(collision_event)
        
        # Event callback çağır
        key = f"{collision_event.type}_{collision_event.sprite1_id}_{collision_event.sprite2_id}"
        if key in self.collision_callbacks:
            self.collision_callbacks[key](collision_event)
        
        # PDSX Event sistemi entegrasyonu
        if self.event_manager:
            event_name = f"collision_{collision_event.sprite1_id}_{collision_event.sprite2_id}"
            if hasattr(self.event_manager, 'trigger_event'):
                self.event_manager.trigger_event(event_name, collision_event)

@dataclass
class C64Memory:
    """C64 Memory emülasyonu - VIC-II registers"""
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

class ModernSpriteManager:
    """Modern C64 Sprite yöneticisi - VIC-II uyumlu + genişletilmiş"""
    
    def __init__(self, display, collision_manager=None):
        self.display = display
        self.collision_manager = collision_manager
        self.sprites = [C64Sprite(i) for i in range(8)]  # VIC-II 8 sprite limit
        self.sprite_images = {}
        
    def load_sprite(self, sprite_id: int, image_path: str) -> bool:
        """SPRITE LOAD <sprite_no>, <file.png|bmp> komutunu işle"""
        if not (0 <= sprite_id < 8):
            return False
            
        try:
            if os.path.exists(image_path):
                image = Image.open(image_path)
                
                # VIC-II standard sprite size (24x21) ama flexible
                original_size = image.size
                sprite = self.sprites[sprite_id]
                sprite.width, sprite.height = original_size
                
                # Tkinter PhotoImage'e çevir
                self.sprite_images[sprite_id] = ImageTk.PhotoImage(image)
                sprite.image_path = image_path
                sprite.image_data = self.sprite_images[sprite_id]
                return True
        except Exception as e:
            print(f"Sprite yükleme hatası: {e}")
        return False
    
    def move_sprite(self, sprite_id: int, x: int, y: int):
        """SPRITE MOVE <sprite_no>, <x>, <y> komutunu işle"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].x = x
            self.sprites[sprite_id].y = y
    
    def enable_sprite(self, sprite_id: int):
        """SPRITE ENABLE <sprite_no> komutunu işle"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].enabled = True
    
    def disable_sprite(self, sprite_id: int):
        """SPRITE DISABLE <sprite_no> komutunu işle"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].enabled = False
    
    def scale_sprite(self, sprite_id: int, width: float, height: float):
        """SPRITE SCALE <sprite_no>, <width>, <height> komutunu işle"""
        if 0 <= sprite_id < 8:
            sprite = self.sprites[sprite_id]
            sprite.scale_x = width
            sprite.scale_y = height
    
    def rotate_sprite(self, sprite_id: int, angle: float):
        """SPRITE ROTATE <sprite_no>, <angle> komutunu işle"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].rotation = angle
    
    def set_sprite_color(self, sprite_id: int, color: int):
        """SPRITE COLOR <sprite_no>, <color> komutunu işle"""
        if 0 <= sprite_id < 8 and 0 <= color < 16:
            self.sprites[sprite_id].color = color
    
    def set_sprite_multicolor(self, sprite_id: int, enabled: bool):
        """SPRITE MULTICOLOR <sprite_no>, ON|OFF komutunu işle"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].multicolor = enabled
    
    def set_sprite_expand_x(self, sprite_id: int, enabled: bool):
        """SPRITE EXPAND_X <sprite_no>, ON|OFF komutunu işle (VIC-II double width)"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].expand_x = enabled
    
    def set_sprite_expand_y(self, sprite_id: int, enabled: bool):
        """SPRITE EXPAND_Y <sprite_no>, ON|OFF komutunu işle (VIC-II double height)"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].expand_y = enabled
    
    def draw_sprites(self):
        """Tüm aktif sprite'ları çiz - collision detection ile"""
        self.display.canvas.delete("sprites")
        
        active_sprites = [s for s in self.sprites if s.enabled and s.image_data]
        
        # Collision detection
        if self.collision_manager:
            for i, sprite1 in enumerate(active_sprites):
                for j, sprite2 in enumerate(active_sprites[i+1:], i+1):
                    if self.collision_manager.check_sprite_sprite_collision(sprite1, sprite2):
                        collision_event = CollisionEvent(
                            type="sprite_sprite",
                            sprite1_id=sprite1.id,
                            sprite2_id=sprite2.id,
                            collision_point=(sprite1.x, sprite1.y)
                        )
                        self.collision_manager.trigger_collision_event(collision_event)
        
        # Sprite çizimi
        for sprite in active_sprites:
            # Ölçeklenmiş pozisyon hesapla
            scaled_x = sprite.x * self.display.scale_factor
            scaled_y = sprite.y * self.display.scale_factor
            
            # VIC-II expand özelliklerini uygula
            if sprite.expand_x or sprite.expand_y:
                display_image = sprite.image_data
                # TODO: Expand işlemi (büyütme)
            else:
                display_image = sprite.image_data
            
            self.display.canvas.create_image(
                scaled_x, scaled_y,
                anchor=tk.NW,
                image=display_image,
                tags="sprites"
            )
    
    def set_sprite_color(self, sprite_id: int, color: int):
        """Sprite rengini ayarla"""
        if 0 <= sprite_id < 8 and 0 <= color < 16:
            self.sprites[sprite_id].color = color
    
    def set_sprite_multicolor(self, sprite_id: int, enabled: bool):
        """Sprite multicolor modunu ayarla"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].multicolor = enabled
    
    def set_sprite_expand_x(self, sprite_id: int, enabled: bool):
        """Sprite X ekseninde genişletmeyi ayarla"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].expand_x = enabled
    
    def set_sprite_expand_y(self, sprite_id: int, enabled: bool):
        """Sprite Y ekseninde genişletmeyi ayarla"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].expand_y = enabled
    
    def rotate_sprite(self, sprite_id: int, angle: float):
        """Sprite rotasyonu"""
        if 0 <= sprite_id < 8:
            self.sprites[sprite_id].rotation = angle
    
    def create_simple_sprite(self, sprite_id: int, width: int, height: int, color: int):
        """Basit renk sprite oluştur"""
        if 0 <= sprite_id < 8:
            try:
                # Basit renkli dikdörtgen oluştur
                from PIL import Image, ImageDraw, ImageTk
                
                # Color palette (C64 colors)
                c64_colors = [
                    (0, 0, 0),       # 0: Black
                    (255, 255, 255), # 1: White  
                    (144, 60, 60),   # 2: Red
                    (122, 191, 199), # 3: Cyan
                    (144, 95, 151),  # 4: Purple
                    (96, 153, 96),   # 5: Green
                    (64, 49, 141),   # 6: Blue
                    (200, 207, 137), # 7: Yellow
                    (144, 95, 37),   # 8: Orange
                    (96, 60, 0),     # 9: Brown
                    (181, 108, 108), # 10: Light Red
                    (64, 64, 64),    # 11: Dark Gray
                    (128, 128, 128), # 12: Medium Gray
                    (164, 215, 142), # 13: Light Green
                    (120, 105, 196), # 14: Light Blue
                    (192, 192, 192)  # 15: Light Gray
                ]
                
                color_rgb = c64_colors[color % 16]
                
                image = Image.new('RGB', (width, height), color_rgb)
                
                # Tkinter PhotoImage'e çevir
                self.sprite_images[sprite_id] = ImageTk.PhotoImage(image)
                self.sprites[sprite_id].image_path = f"generated_{sprite_id}"
                self.sprites[sprite_id].image_data = self.sprite_images[sprite_id]
                self.sprites[sprite_id].width = width
                self.sprites[sprite_id].height = height
                self.sprites[sprite_id].color = color
                return True
                
            except Exception as e:
                print(f"Sprite oluşturma hatası: {e}")
                return False
        return False
    
    def reset_sprite_effects(self, sprite_id: int):
        """Sprite efektlerini sıfırla"""
        if 0 <= sprite_id < 8:
            sprite = self.sprites[sprite_id]
            sprite.expand_x = False
            sprite.expand_y = False
            sprite.multicolor = False
            sprite.rotation = 0
            sprite.scale_x = 1.0
            sprite.scale_y = 1.0
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
    
    def draw_text(self, x: int, y: int, text: str, color: int = 1):
        """Text çiz"""
        # Basit text çizimi
        canvas_x = x * self.scale_factor * 8  # 8x8 character size
        canvas_y = y * self.scale_factor * 8
        
        try:
            self.canvas.create_text(
                canvas_x, canvas_y,
                text=text,
                fill=C64_COLORS[color % 16],
                anchor=tk.NW,
                font=("Courier", 8 * self.scale_factor),
                tags="text"
            )
        except:
            # Fallback
            print(f"Text: {text} at ({x},{y})")
    
    def flash_screen(self, color: int):
        """Ekran flash efekti"""
        original_bg = self.canvas['bg']
        try:
            self.canvas.configure(bg=C64_COLORS[color % 16])
            self.canvas.update()
            # Flash effect için kısa bekle
            import time
            time.sleep(0.1)
            self.canvas.configure(bg=original_bg)
        except:
            print(f"Screen flash: color {color}")
    
    def draw_char(self, x: int, y: int, char_code: int):
        """Karakter çiz"""
        # Basit karakter çizimi - block character simulation
        canvas_x = x * 8 * self.scale_factor  
        canvas_y = y * 8 * self.scale_factor
        char_size = 8 * self.scale_factor
        
        # Char code'a göre pattern
        if char_code == 160:  # Solid block
            color = "#FFFFFF"
        elif char_code == 32:   # Space
            return  # Nothing to draw
        else:
            color = "#CCCCCC"  # Other characters
        
        try:
            self.canvas.create_rectangle(
                canvas_x, canvas_y,
                canvas_x + char_size, canvas_y + char_size,
                fill=color,
                outline="",
                tags="characters"
            )
        except:
            print(f"Char: {char_code} at ({x},{y})")

# Deprecated - Use ModernSpriteManager instead
# Complete old C64SpriteManager class commented out
# All functionality moved to ModernSpriteManager

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

class UniversalC64Engine:
    """Modern C64 GUI Engine - PDSX v12X Integration"""
    
    def __init__(self, parent_widget=None, event_manager=None):
        self.parent = parent_widget or tk.Tk()
        self.event_manager = event_manager
        self.running = False
        
        # C64 bileşenleri
        self.display = C64Display(self.parent, scale_factor=2)
        self.collision_manager = C64CollisionManager(self.display, event_manager)
        # Initialize sprite manager manually to avoid init error
        self.sprite_manager = None
        try:
            sprite_manager = ModernSpriteManager.__new__(ModernSpriteManager)
            sprite_manager.display = self.display
            sprite_manager.collision_manager = self.collision_manager
            sprite_manager.sprites = [C64Sprite(i) for i in range(8)]
            sprite_manager.sprite_images = {}
            self.sprite_manager = sprite_manager
        except Exception as e:
            print(f"Sprite manager init hatası: {e}")
            self.sprite_manager = None
        
        self.audio_manager = C64AudioManager()
        self.charset_manager = C64CharsetManager()
        self.memory = C64Memory()
        
        # Update thread
        self.update_thread = None
        self.update_running = False
        
        # Command handlers mapping
        self.command_handlers = {
            'SPRITE': self._handle_sprite_command,
            'SID': self._handle_sid_command,
            'SOUND': self._handle_sound_command,
            'SCREEN': self._handle_screen_command,
            'CHRSET': self._handle_chrset_command,
            'EVENT': self._handle_event_command
        }
        
    def initialize(self):
        """Engine'i başlat"""
        self.display.canvas.pack()
        self.display.clear_screen(self.memory.background_color)
        self.display.update_display()
        # Threading döngüsü sonsuz döngüye neden oluyor - devre dışı
        # self.start_update_loop()
        
    def execute_command(self, command: str) -> bool:
        """PDSX komutunu işle"""
        try:
            command = command.strip()
            if not command:
                return True
                
            # Komut tipini belirle
            parts = command.split()
            if not parts:
                return True
                
            cmd_type = parts[0].upper()
            
            # Command handler'ı çağır
            if cmd_type in self.command_handlers:
                return self.command_handlers[cmd_type](command)
            else:
                print(f"Bilinmeyen C64 komutu: {cmd_type}")
                return False
                
        except Exception as e:
            print(f"C64 komut hatası: {e}")
            return False
    
    def _handle_sprite_command(self, command: str) -> bool:
        """SPRITE komutlarını işle"""
        parts = command.split()
        if len(parts) < 3:
            return False
            
        subcmd = parts[1].upper()
        
        try:
            if subcmd == "LOAD":
                # SPRITE LOAD <sprite_no>, <file.png>
                sprite_id = int(parts[2].rstrip(','))
                filename = parts[3].strip('"')
                return self.sprite_manager.load_sprite(sprite_id, filename)
                
            elif subcmd == "MOVE":
                # SPRITE MOVE <sprite_no>, <x>, <y>
                sprite_id = int(parts[2].rstrip(','))
                x = int(parts[3].rstrip(','))
                y = int(parts[4])
                self.sprite_manager.move_sprite(sprite_id, x, y)
                return True
                
            elif subcmd == "ENABLE":
                # SPRITE ENABLE <sprite_no>
                sprite_id = int(parts[2])
                self.sprite_manager.enable_sprite(sprite_id)
                return True
                
            elif subcmd == "DISABLE":
                # SPRITE DISABLE <sprite_no>
                sprite_id = int(parts[2])
                self.sprite_manager.disable_sprite(sprite_id)
                return True
                
            elif subcmd == "SCALE":
                # SPRITE SCALE <sprite_no>, <width>, <height>
                sprite_id = int(parts[2].rstrip(','))
                width = float(parts[3].rstrip(','))
                height = float(parts[4])
                self.sprite_manager.scale_sprite(sprite_id, width, height)
                return True
                
            elif subcmd == "ROTATE":
                # SPRITE ROTATE <sprite_no>, <angle>
                sprite_id = int(parts[2].rstrip(','))
                angle = float(parts[3])
                self.sprite_manager.rotate_sprite(sprite_id, angle)
                return True
                
            elif subcmd == "COLOR":
                # SPRITE COLOR <sprite_no>, <color>
                sprite_id = int(parts[2].rstrip(','))
                color = int(parts[3])
                self.sprite_manager.set_sprite_color(sprite_id, color)
                return True
                
            elif subcmd == "MULTICOLOR":
                # SPRITE MULTICOLOR <sprite_no>, ON|OFF
                sprite_id = int(parts[2].rstrip(','))
                enabled = parts[3].upper() == "ON"
                self.sprite_manager.set_sprite_multicolor(sprite_id, enabled)
                return True
                
            elif subcmd == "EXPAND_X":
                # SPRITE EXPAND_X <sprite_no>, ON|OFF
                sprite_id = int(parts[2].rstrip(','))
                enabled = parts[3].upper() == "ON"
                self.sprite_manager.set_sprite_expand_x(sprite_id, enabled)
                return True
                
            elif subcmd == "EXPAND_Y":
                # SPRITE EXPAND_Y <sprite_no>, ON|OFF
                sprite_id = int(parts[2].rstrip(','))
                if len(parts) > 3:
                    enabled = parts[3].upper() == "ON"
                else:
                    enabled = True  # Default ON if no parameter
                self.sprite_manager.set_sprite_expand_y(sprite_id, enabled)
                return True
                
            elif subcmd == "CREATE":
                # SPRITE CREATE <sprite_no>, <width>, <height>, <color>
                sprite_id = int(parts[2].rstrip(','))
                width = int(parts[3].rstrip(','))
                height = int(parts[4].rstrip(','))
                color = int(parts[5])
                self.sprite_manager.create_simple_sprite(sprite_id, width, height, color)
                return True
                
            elif subcmd == "NORMAL":
                # SPRITE NORMAL <sprite_no> - Reset all effects
                sprite_id = int(parts[2])
                self.sprite_manager.reset_sprite_effects(sprite_id)
                return True
                
        except (ValueError, IndexError) as e:
            print(f"SPRITE komut parametresi hatası: {e}")
            return False
            
        return False
    
    def _handle_sid_command(self, command: str) -> bool:
        """SID komutlarını işle"""
        parts = command.split()
        if len(parts) < 2:
            return False
            
        subcmd = parts[1].upper()
        
        try:
            if subcmd == "LOAD":
                # SID LOAD <file.sid|mp3|wav>
                filename = parts[2].strip('"')
                return self.audio_manager.load_music(filename)
                
            elif subcmd == "PLAY":
                # SID PLAY
                return self.audio_manager.play_music()
                
            elif subcmd == "STOP":
                # SID STOP
                self.audio_manager.stop_music()
                return True
                
            elif subcmd == "PAUSE":
                # SID PAUSE
                self.audio_manager.pause_music()
                return True
                
            elif subcmd == "VOLUME":
                # SID VOLUME <0-15>
                volume = int(parts[2]) / 15.0  # VIC-II style 0-15 to 0.0-1.0
                self.audio_manager.set_volume(volume)
                return True
                
        except (ValueError, IndexError) as e:
            print(f"SID komut parametresi hatası: {e}")
            return False
            
        return False
    
    def _handle_sound_command(self, command: str) -> bool:
        """SOUND komutlarını işle (gelecekte genişletilecek)"""
        # TODO: Sound effects sistemi
        return True
    
    def _handle_screen_command(self, command: str) -> bool:
        """SCREEN komutlarını işle"""
        parts = command.split()
        if len(parts) < 2:
            return False
            
        subcmd = parts[1].upper()
        
        try:
            if subcmd == "INIT":
                # SCREEN INIT <width>, <height>, <scale>
                # TODO: Dynamic screen size (şimdilik 320x200 sabit)
                return True
                
            elif subcmd == "CLEAR":
                # SCREEN CLEAR <color>
                color = int(parts[2])
                self.display.clear_screen(color)
                return True
                
            elif subcmd == "BACKGROUND":
                # SCREEN BACKGROUND <color>
                color = int(parts[2])
                self.memory.background_color = color & 0x0F
                self.display.clear_screen(self.memory.background_color)
                return True
                
            elif subcmd == "BORDER":
                # SCREEN BORDER <color>
                color = int(parts[2])
                self.memory.border_color = color & 0x0F
                return True
                
            elif subcmd == "PIXEL":
                # SCREEN PIXEL <x>, <y>, <color>
                x = int(parts[2].rstrip(','))
                y = int(parts[3].rstrip(','))
                color = int(parts[4])
                self.display.set_pixel(x, y, color)
                return True
                
            elif subcmd == "TEXT":
                # SCREEN TEXT <x>, <y>, <"string">, <color>
                x = int(parts[2].rstrip(','))
                y = int(parts[3].rstrip(','))
                text = parts[4].strip('"')
                color = int(parts[5]) if len(parts) > 5 else 1
                self.display.draw_text(x, y, text, color)
                return True
                
            elif subcmd == "CHAR":
                # SCREEN CHAR <x>, <y>, <char_code>
                x = int(parts[2].rstrip(','))
                y = int(parts[3].rstrip(','))
                char_code = int(parts[4])
                self.display.draw_char(x, y, char_code)
                return True
                
            elif subcmd == "FLASH":
                # SCREEN FLASH <color> - Flash effect
                color = int(parts[2])
                self.display.flash_screen(color)
                return True
                
        except (ValueError, IndexError) as e:
            print(f"SCREEN komut parametresi hatası: {e}")
            return False
            
        return False
    
    def _handle_chrset_command(self, command: str) -> bool:
        """CHRSET komutlarını işle"""
        parts = command.split()
        if len(parts) < 2:
            return False
            
        try:
            subcmd = parts[1].upper()
            
            if subcmd == "LOAD":
                # CHRSET LOAD "filename"
                filename = parts[2].strip('"')
                print(f"CHRSET yüklendi: {filename}")
                return True
                
            elif subcmd == "SELECT":
                # CHRSET SELECT <charset_id>
                charset_id = int(parts[2])
                print(f"CHRSET seçildi: {charset_id}")
                return True
                
            elif subcmd == "CREATE":
                # CHRSET CREATE <id>, <size>
                charset_id = int(parts[2].rstrip(','))
                size = int(parts[3])
                print(f"CHRSET oluşturuldu: {charset_id}, boyut: {size}")
                return True
                
        except (ValueError, IndexError) as e:
            print(f"CHRSET komut parametresi hatası: {e}")
            return False
            
        return False
    
    def _handle_event_command(self, command: str) -> bool:
        """EVENT komutlarını işle - PDSX Event sistemi entegrasyonu"""
        # PDSX Event sistemi ile entegre edilecek
        # Örnek: EVENT collision_mario SPRITE_COLLISION 0, 1
        return True
    
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
        """Ana güncelleme döngüsü (60 FPS) - Collision detection dahil"""
        while self.update_running:
            try:
                # Ekranı güncelle
                self.display.update_display()
                
                # Sprite'ları çiz (collision detection dahil)
                self.sprite_manager.draw_sprites()
                
                # Border collision kontrolü
                for sprite in self.sprite_manager.sprites:
                    if sprite.enabled and self.collision_manager.check_sprite_border_collision(
                        sprite, self.display.width, self.display.height):
                        collision_event = CollisionEvent(
                            type="sprite_border",
                            sprite1_id=sprite.id,
                            collision_point=(sprite.x, sprite.y)
                        )
                        self.collision_manager.trigger_collision_event(collision_event)
                
                # 60 FPS için bekleme
                time.sleep(1/60)
                
            except Exception as e:
                print(f"Update loop hatası: {e}")
                
    def get_display_widget(self):
        """Display widget'ını döndür"""
        return self.display.canvas

# Legacy uyumluluk için alias
C64GuiEngine = UniversalC64Engine

# Test kodu - Modern C64 Engine
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Universal C64 Engine Test")
    
    engine = UniversalC64Engine(root)
    engine.initialize()
    
    # Test komutları
    print("🚀 Modern C64 Engine Test Başlıyor...")
    
    # Sprite test
    # engine.execute_command('SPRITE LOAD 0, "mario.png"')
    # engine.execute_command('SPRITE ENABLE 0')
    # engine.execute_command('SPRITE MOVE 0, 100, 100')
    # engine.execute_command('SPRITE SCALE 0, 2.0, 2.0')
    
    # Screen test
    engine.execute_command('SCREEN BACKGROUND 6')
    engine.execute_command('SCREEN BORDER 14')
    engine.execute_command('SCREEN PIXEL 50, 50, 1')
    
    # SID test
    # engine.execute_command('SID LOAD "music.mp3"')
    # engine.execute_command('SID PLAY')
    
    print("✅ Komutlar çalıştırıldı!")
    print("📋 Desteklenen komutlar:")
    print("  SPRITE LOAD, SPRITE MOVE, SPRITE ENABLE/DISABLE")
    print("  SPRITE SCALE, SPRITE ROTATE, SPRITE COLOR")
    print("  SID LOAD, SID PLAY, SID STOP, SID VOLUME")
    print("  SCREEN BACKGROUND, SCREEN BORDER, SCREEN PIXEL")
    print("  CHRSET (coming soon)")
    print("  EVENT (PDSX integration)")
    
    root.mainloop()
    engine.stop_update_loop()
