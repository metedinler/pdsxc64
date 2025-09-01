#!/usr/bin/env python3
"""
Basit PNG sprite oluşturucu - C64 demo için
"""

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

import os

def create_sample_sprite():
    """C64 tarzı basit sprite oluştur"""
    if not PIL_AVAILABLE:
        print("PIL/Pillow bulunamadı, sprite oluşturulamıyor")
        return False
    
    # 24x21 C64 sprite boyutu (height artırıldı)
    width, height = 24, 25
    
    # Şeffaf arka plan ile resim oluştur
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Basit uzay gemisi sprite'ı çiz
    # Ana gövde (mavi)
    draw.rectangle([8, 15, 15, 20], fill=(0, 100, 255, 255))
    
    # Kanatlar (açık mavi)
    draw.rectangle([4, 17, 7, 19], fill=(100, 150, 255, 255))
    draw.rectangle([16, 17, 19, 19], fill=(100, 150, 255, 255))
    
    # Burun (beyaz)
    draw.rectangle([11, 10, 12, 14], fill=(255, 255, 255, 255))
    
    # Motor ateşi (kırmızı-sarı)
    draw.rectangle([10, 21, 13, 21], fill=(255, 255, 0, 255))  # Sarı
    draw.rectangle([11, 22, 12, 22], fill=(255, 128, 0, 255))  # Turuncu
    draw.rectangle([11, 23, 12, 23], fill=(255, 0, 0, 255))    # Kırmızı
    
    # Pencere (sarı)
    draw.rectangle([10, 12, 13, 13], fill=(255, 255, 0, 255))
    
    # Sprite'ı kaydet
    sprite_path = "demo_sprite.png"
    img.save(sprite_path)
    print(f"Demo sprite oluşturuldu: {sprite_path}")
    return True

def create_c64_palette_sprite():
    """C64 renk paletini kullanan sprite"""
    if not PIL_AVAILABLE:
        return False
    
    # C64 renk paleti
    c64_colors = [
        (0, 0, 0),        # Siyah
        (255, 255, 255),  # Beyaz
        (136, 57, 50),    # Kırmızı
        (103, 182, 189),  # Camgöbeği
        (139, 63, 150),   # Mor
        (85, 160, 73),    # Yeşil
        (64, 49, 141),    # Mavi
        (191, 206, 114),  # Sarı
        (139, 84, 41),    # Turuncu
        (87, 66, 0),      # Kahverengi
        (184, 105, 98),   # Açık kırmızı
        (80, 80, 80),     # Koyu gri
        (120, 120, 120),  # Orta gri
        (148, 224, 137),  # Açık yeşil
        (120, 105, 196),  # Açık mavi
        (159, 159, 159)   # Açık gri
    ]
    
    width, height = 24, 21
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # C64 tarzı karakter (smiley)
    # Yüz (sarı)
    draw.ellipse([6, 6, 17, 17], fill=c64_colors[7] + (255,))
    
    # Gözler (siyah)
    draw.rectangle([9, 9, 10, 10], fill=c64_colors[0] + (255,))
    draw.rectangle([13, 9, 14, 10], fill=c64_colors[0] + (255,))
    
    # Ağız (kırmızı)
    draw.arc([9, 11, 14, 14], 0, 180, fill=c64_colors[2] + (255,))
    
    sprite_path = "c64_smiley_sprite.png"
    img.save(sprite_path)
    print(f"C64 smiley sprite oluşturuldu: {sprite_path}")
    return True

if __name__ == "__main__":
    print("C64 Demo Sprite'ları oluşturuluyor...")
    
    success1 = create_sample_sprite()
    success2 = create_c64_palette_sprite()
    
    if success1 or success2:
        print("Demo sprite'ları hazır!")
        print("PDSX demo'sunda kullanabilirsiniz.")
    else:
        print("Sprite oluşturulamadı - PIL/Pillow gerekli")
