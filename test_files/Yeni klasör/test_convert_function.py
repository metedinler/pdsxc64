#!/usr/bin/env python3
"""
Test convert_to_specific_format functionality
"""
import tkinter as tk
from tkinter import ttk
import os

def test_convert_function():
    """Test convert_to_specific_format with a real file"""
    try:
        from d64_converter import D64ConverterApp
        
        print("🔍 Testing convert_to_specific_format")
        print("=" * 50)
        
        # Test GUI oluştur
        root = tk.Tk()
        root.withdraw()  # Pencereyi gizle
        
        app = D64ConverterApp(root)
        
        # Test .d64 dosyası yükle
        test_file = "test.d64"
        if os.path.exists(test_file):
            print(f"✅ Test dosyası bulundu: {test_file}")
            
            # Dosyayı manuel olarak load et
            from d64_reader import read_image
            
            try:
                data = read_image(test_file)
                entries = data  # read_image direkt entries döndürür
                
                if entries and isinstance(entries, list):
                    print(f"✅ Dosya okundu: {len(entries)} entry bulundu")
                    
                    # App'e entries'i ata
                    app.entries = entries
                    app.update_file_list()
                    
                    # İlk entry'yi test et
                    first_entry = app.entries[0]
                    print(f"📁 Test entry: {first_entry.get('filename', 'Unknown')}")
                    
                    # Test convert_to_assembly
                    print("\n🔄 Test: convert_to_assembly")
                    try:
                        app.convert_to_assembly()
                        print("✅ convert_to_assembly başarılı")
                    except Exception as e:
                        print(f"❌ convert_to_assembly hatası: {e}")
                        import traceback
                        traceback.print_exc()
                    
                    # Test convert_to_petcat
                    print("\n🔄 Test: convert_to_petcat")
                    try:
                        app.convert_to_petcat()
                        print("✅ convert_to_petcat başarılı")
                    except Exception as e:
                        print(f"❌ convert_to_petcat hatası: {e}")
                        import traceback
                        traceback.print_exc()
                        
                else:
                    print("❌ Dosya entries'e yüklenemedi - veri formatı hatalı")
                    
            except Exception as e:
                print(f"❌ Dosya okuma hatası: {e}")
                import traceback
                traceback.print_exc()
                
        else:
            print(f"❌ Test dosyası bulunamadı: {test_file}")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Test hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_convert_function()
