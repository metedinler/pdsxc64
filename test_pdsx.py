#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDSX Test Dosyası - GUI ve Interpreter testi
"""

def test_pdsx_basic():
    """Temel PDSX interpreter testi"""
    print("=== PDSX Temel Test ===")
    
    try:
        from pdsxv12xNEW import pdsXInterpreter
        print("✓ pdsXInterpreter import edildi")
        
        interpreter = pdsXInterpreter()
        print("✓ Interpreter oluşturuldu")
        
        # Basit bir komut test et
        result = interpreter.execute_command('PRINT "Hello PDSX!"')
        print(f"✓ PRINT komutu çalıştırıldı: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ Hata: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdsx_gui():
    """PDSX GUI testi"""
    print("\n=== PDSX GUI Test ===")
    
    try:
        from pdsxv12xNEW import pdsXInterpreter
        interpreter = pdsXInterpreter()
        print("✓ Interpreter oluşturuldu")
        
        # GUI'yi başlat
        interpreter._initialize_libx_gui()
        print("✓ GUI başlatıldı")
        
        # libx_gui atribute'unu kontrol et
        if hasattr(interpreter, 'libx_gui') and interpreter.libx_gui:
            print("✓ libx_gui nesnesi mevcut")
            
            # Basit bir GUI komutu test et
            result = interpreter.libx_gui.parse_gui_command('WINDOW "Test Window", 400, 300')
            print(f"✓ WINDOW komutu çalıştırıldı: {result}")
            
            return True
        else:
            print("✗ libx_gui nesnesi bulunamadı")
            return False
        
    except Exception as e:
        print(f"✗ GUI Hatası: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_libx_gui_direct():
    """LibX GUI'yi doğrudan test et"""
    print("\n=== LibX GUI Doğrudan Test ===")
    
    try:
        from libx_guiX import LibXGuiX
        print("✓ LibXGuiX import edildi")
        
        gui = LibXGuiX()
        print("✓ LibXGuiX oluşturuldu")
        
        # Basit komut test et
        result = gui.parse_gui_command('WINDOW "Test Direct", 300, 200')
        print(f"✓ GUI komutu çalıştırıldı: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ LibX GUI Hatası: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("PDSX v12X Test Suite")
    print("=" * 50)
    
    # Testleri çalıştır
    test1 = test_pdsx_basic()
    test2 = test_pdsx_gui()
    test3 = test_libx_gui_direct()
    
    print("\n" + "=" * 50)
    print("Test Sonuçları:")
    print(f"Temel Test: {'✓ BAŞARILI' if test1 else '✗ BAŞARISIZ'}")
    print(f"GUI Test: {'✓ BAŞARILI' if test2 else '✗ BAŞARISIZ'}")
    print(f"LibX GUI Test: {'✓ BAŞARILI' if test3 else '✗ BAŞARISIZ'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 Tüm testler başarılı!")
    else:
        print("\n⚠️  Bazı testler başarısız oldu.")
