#!/usr/bin/env python3
"""
PyGubu Designer Hızlı Başlatıcı
D64 Converter GUI düzenleme aracı
"""

import subprocess
import sys
import os
from pathlib import Path

def start_pygubu_designer():
    """PyGubu Designer'ı başlat ve UI dosyasını aç"""
    
    print("🎨 PyGubu Designer başlatılıyor...")
    
    # UI dosyasının yolu
    ui_file = Path(__file__).parent / "gui_designs" / "d64_converter_main.ui"
    
    try:
        # PyGubu Designer'ı başlat
        if ui_file.exists():
            print(f"📂 UI dosyası bulundu: {ui_file}")
            
            # Designer'ı UI dosyası ile aç
            subprocess.Popen([
                sys.executable, "-m", "pygubu.designer", 
                str(ui_file)
            ])
            
            print("✅ PyGubu Designer açıldı!")
            print("\n📝 KULLANIM REHBERİ:")
            print("1. Sol panelden widget'ları seçin")
            print("2. Sağ panelde Layout ve Widget sekmelerini kullanın")
            print("3. row/column ile pozisyon ayarlayın")
            print("4. bg/fg ile renkleri değiştirin")
            print("5. File → Save ile kaydedin")
            print("6. Preview → Test Interface ile test edin")
            
        else:
            print(f"❌ UI dosyası bulunamadı: {ui_file}")
            
            # Boş designer başlat
            subprocess.Popen([
                sys.executable, "-m", "pygubu.designer"
            ])
            
            print("✅ Boş PyGubu Designer açıldı!")
            print("💡 File → New ile yeni UI oluşturabilirsiniz")
            
    except FileNotFoundError:
        print("❌ PyGubu Designer bulunamadı!")
        print("🔧 Kurulum: pip install pygubu-designer")
        
    except Exception as e:
        print(f"❌ Başlatma hatası: {e}")

if __name__ == "__main__":
    start_pygubu_designer()
