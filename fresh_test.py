#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fresh PDSX Test - Yeni Session
"""

import sys
import importlib

def fresh_test():
    print("Fresh PDSX Test Başlatılıyor...")
    
    # Cache temizle
    if 'pdsxv12xNEW' in sys.modules:
        del sys.modules['pdsxv12xNEW']
        print("✓ Eski modül cache temizlendi")
    
    try:
        # Fresh import
        import pdsxv12xNEW
        importlib.reload(pdsxv12xNEW)
        print("✓ Modül yeniden yüklendi")
        
        from pdsxv12xNEW import pdsXInterpreter
        print("✓ Fresh import başarılı")
        
        interpreter = pdsXInterpreter()
        print("✓ Interpreter oluşturuldu")
        
        # Metodların varlığını kontrol et
        methods = [method for method in dir(interpreter) if 'initialize' in method.lower()]
        print(f"Initialize metodları: {methods}")
        
        # _initialize_libx_gui metodunun var olup olmadığını kontrol et
        if hasattr(interpreter, '_initialize_libx_gui'):
            print("✅ _initialize_libx_gui metodu bulundu!")
            
            # Metodu çağır
            interpreter._initialize_libx_gui()
            print("✓ Metod çağrıldı")
            
            # LibX GUI'nin var olup olmadığını kontrol et
            if hasattr(interpreter, 'libx_gui') and interpreter.libx_gui is not None:
                print("✓ LibX GUI başarıyla oluşturuldu")
                print(f"  GUI tipi: {type(interpreter.libx_gui)}")
            else:
                print("✗ LibX GUI oluşturulamadı")
                
        else:
            print("❌ _initialize_libx_gui metodu hala bulunamadı")
        
        print("✅ Fresh test tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fresh_test()
