#!/usr/bin/env python3
"""
GUI Styles and Themes - Separated from gui_manager.py
Modern light/dark theme system
"""

import os

class ModernStyle:
    """Modern theme system - Light/Dark mode support"""
    
    def __init__(self, dark_mode=None):
        # Environment'tan tema al
        if dark_mode is None:
            theme = os.environ.get('GUI_THEME', 'light').lower()
            dark_mode = (theme == 'dark')
        
        if dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
    
    def apply_light_theme(self):
        """Light theme colors"""
        # Ana renkler
        self.BG_PRIMARY = "#ffffff"       # Ana arkaplan - beyaz
        self.BG_DARK = "#ffffff"          # Ana arkaplan - beyaz (alias)
        self.BG_SECONDARY = "#f8f9fa"     # İkincil arkaplan - açık gri
        self.BG_TERTIARY = "#e9ecef"      # Üçüncül arkaplan - orta gri
        
        # Metin renkleri
        self.FG_PRIMARY = "#212529"       # Ana metin - koyu siyah
        self.FG_SECONDARY = "#495057"     # İkincil metin - orta gri
        self.FG_ACCENT = "#0d6efd"        # Vurgu rengi - mavi
        
        # Status renkleri
        self.FG_SUCCESS = "#198754"       # Başarı - yeşil
        self.FG_WARNING = "#fd7e14"       # Uyarı - turuncu
        self.FG_ERROR = "#dc3545"         # Hata - kırmızı
        
        # Syntax highlighting
        self.SYNTAX_KEYWORD = "#0000ff"   # Mavi - anahtar kelimeler
        self.SYNTAX_STRING = "#008000"    # Yeşil - string'ler
        self.SYNTAX_COMMENT = "#808080"   # Gri - yorumlar
        self.SYNTAX_NUMBER = "#ff0000"    # Kırmızı - sayılar
        self.SYNTAX_OPERATOR = "#000000"  # Siyah - operatörler
    
    def apply_dark_theme(self):
        """Dark theme colors"""
        # Ana renkler
        self.BG_PRIMARY = "#1e1e1e"       # Ana arkaplan - koyu gri
        self.BG_DARK = "#1e1e1e"          # Ana arkaplan - koyu gri
        self.BG_SECONDARY = "#2d2d30"     # İkincil arkaplan - orta koyu
        self.BG_TERTIARY = "#3c3c3c"      # Üçüncül arkaplan - açık koyu
        
        # Metin renkleri
        self.FG_PRIMARY = "#ffffff"       # Ana metin - beyaz
        self.FG_SECONDARY = "#cccccc"     # İkincil metin - açık gri
        self.FG_ACCENT = "#569cd6"        # Vurgu rengi - açık mavi
        
        # Status renkleri
        self.FG_SUCCESS = "#4ec9b0"       # Başarı - teal
        self.FG_WARNING = "#ffcc02"       # Uyarı - sarı
        self.FG_ERROR = "#f44747"         # Hata - kırmızı
        
        # Syntax highlighting
        self.SYNTAX_KEYWORD = "#569cd6"   # Açık mavi - anahtar kelimeler
        self.SYNTAX_STRING = "#ce9178"    # Turuncu - string'ler
        self.SYNTAX_COMMENT = "#6a9955"   # Yeşil - yorumlar
        self.SYNTAX_NUMBER = "#b5cea8"    # Açık yeşil - sayılar
        self.SYNTAX_OPERATOR = "#d4d4d4"  # Açık gri - operatörler
    
    @staticmethod
    def create_light_style():
        """Light theme instance oluştur"""
        return ModernStyle(dark_mode=False)
    
    @staticmethod
    def create_dark_style():
        """Dark theme instance oluştur"""
        return ModernStyle(dark_mode=True)

# Global style instance
ModernStyle = ModernStyle()  # Environment'a göre otomatik tema seçimi
