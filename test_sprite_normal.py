#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sprite Test - Normal Mode (Debug OFF)
"""
import sys
import os

# Add path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdsxv12X import pdsXInterpreter

def test_sprite_normal():
    """Test sprite loading functionality - normal mode"""
    print("🧪 Sprite Normal Test başlatılıyor...")
    
    interpreter = pdsXInterpreter()
    interpreter.debug_mode = False  # Normal mode
    
    test_code = """
    PRINT "Test başlıyor"
    SCREEN BACKGROUND 6
    PRINT "Background ayarlandı"
    SPRITE LOAD 0, "demo_sprite.png"
    PRINT "Sprite yüklendi"
    SPRITE MOVE 0, 100, 100
    PRINT "Sprite konumlandırıldı"
    SPRITE ENABLE 0
    PRINT "Sprite aktif edildi"
    PRINT "Test tamamlandı"
    """
    
    interpreter.run(test_code)

if __name__ == "__main__":
    test_sprite_normal()
