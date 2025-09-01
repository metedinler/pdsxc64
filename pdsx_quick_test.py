#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hızlı PDSX Test - GUI Integration Debug
"""

def quick_pdsx_test():
    print("Hızlı PDSX Test Başlatılıyor...")
    
    try:
        from pdsxv12xNEW import pdsXInterpreter
        print("✓ Import başarılı")
        
        interpreter = pdsXInterpreter()
        print("✓ Interpreter oluşturuldu")
        
        # Basit matematiğsel işlem
        result = interpreter.execute_command('PRINT 2 + 2')
        print(f"✓ Matematik: {result}")
        
        # String işlemi  
        result = interpreter.execute_command('PRINT "Merhaba PDSX!"')
        print(f"✓ String: {result}")
        
        # GUI başlatma
        try:
            interpreter._initialize_libx_gui()
            print("✓ GUI başlatıldı")
            
            if hasattr(interpreter, 'libx_gui') and interpreter.libx_gui is not None:
                print("✓ GUI nesnesi mevcut")
                print(f"  GUI tipi: {type(interpreter.libx_gui)}")
                
                # GUI komutunu test et
                gui_result = interpreter.execute_command('GUI WINDOW "Test" 400 300')
                print(f"✓ GUI komutu: {gui_result}")
                
            else:
                print("✗ GUI nesnesi bulunamadı")
                
        except Exception as e:
            print(f"✗ GUI hatası: {e}")
            import traceback
            traceback.print_exc()
        
        print("✅ Test tamamlandı!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_pdsx_test()
