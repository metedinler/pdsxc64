#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDSX Sınıf Debug
"""

def debug_pdsx_class():
    print("PDSX Sınıf Debug Başlatılıyor...")
    
    try:
        from pdsxv12xNEW import pdsXInterpreter
        print("✓ Import başarılı")
        
        # Sınıfın metodlarını listele
        interpreter = pdsXInterpreter()
        print("✓ Interpreter oluşturuldu")
        
        # Dir ile tüm metodları göster
        methods = [method for method in dir(interpreter) if method.startswith('_initialize')]
        print(f"_initialize ile başlayan metodlar: {methods}")
        
        # libx ile ilgili metodları göster
        libx_methods = [method for method in dir(interpreter) if 'libx' in method.lower()]
        print(f"'libx' içeren metodlar: {libx_methods}")
        
        # GUI ile ilgili metodları göster
        gui_methods = [method for method in dir(interpreter) if 'gui' in method.lower()]
        print(f"'gui' içeren metodlar: {gui_methods}")
        
        # Tüm private metodları göster (debug için)
        private_methods = [method for method in dir(interpreter) if method.startswith('_') and not method.startswith('__')]
        print(f"Private metodlar (sayı): {len(private_methods)}")
        
        # _initialize_libx_gui metodunun var olup olmadığını kontrol et
        if hasattr(interpreter, '_initialize_libx_gui'):
            print("✓ _initialize_libx_gui metodu var")
            try:
                method = getattr(interpreter, '_initialize_libx_gui')
                print(f"  Metod tipi: {type(method)}")
                print(f"  Callable: {callable(method)}")
            except Exception as e:
                print(f"  Metod kontrolünde hata: {e}")
        else:
            print("✗ _initialize_libx_gui metodu yok")
        
        print("✅ Debug tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_pdsx_class()
