"""
GUI Test Script - TkinterDnD sorununu çöz
"""
import sys
import os

# Test.prg dosyasını oluştur
def create_test_prg():
    print("📄 test.prg dosyası oluşturuluyor...")
    prg_data = bytes([
        0x00, 0x08,        # Start address: $0800
        0xA9, 0x01,        # LDA #$01
        0x8D, 0x20, 0xD0,  # STA $D020
        0xA9, 0x0E,        # LDA #$0E
        0x8D, 0x21, 0xD0,  # STA $D021
        0x60               # RTS
    ])
    
    with open('test.prg', 'wb') as f:
        f.write(prg_data)
    print(f"✅ test.prg oluşturuldu: {len(prg_data)} bytes")

def test_gui_safe():
    """GUI'yi güvenli şekilde test et"""
    try:
        # Test dosyasını oluştur
        create_test_prg()
        
        # Import test
        print("🔍 d64_converter import test ediliyor...")
        
        # TkinterDnD olmadan import test
        import tkinter as tk
        print("✅ tkinter import başarılı")
        
        # Ana modülü import et
        sys.path.insert(0, os.getcwd())
        
        print("🔍 d64_converter modülü import ediliyor...")
        from d64_converter import D64ConverterApp
        print("✅ d64_converter import başarılı")
        
        # GUI test - TkinterDnD olmadan
        print("🖥️ GUI test başlatılıyor...")
        root = tk.Tk()
        root.title("D64 Converter - Test Mode")
        root.geometry("800x600")
        
        # App instance oluştur
        print("🔧 D64ConverterApp instance oluşturuluyor...")
        app = D64ConverterApp(root)
        
        print("✅ GUI başarıyla oluşturuldu!")
        print("📝 Disassembler seçimi:", app.disassembler_var.get())
        print("🔬 Illegal opcodes:", app.use_illegal_opcodes.get())
        print("🧠 Memory analysis:", app.memory_analysis.get())
        
        # GUI'yi kısa süre göster
        print("🚀 GUI gösteriliyor (5 saniye)...")
        root.after(5000, root.quit)  # 5 saniye sonra kapat
        root.mainloop()
        
        root.destroy()
        print("✅ GUI test tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ GUI test hatası: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_mode():
    """CLI modunu test et"""
    try:
        print("🔧 CLI test başlatılıyor...")
        
        # CLI test komutu
        import subprocess
        result = subprocess.run([
            'python', 'main.py', 
            '--no-gui', 
            '--file', 'test.prg', 
            '--format', 'asm',
            '--disassembler', 'improved'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ CLI test başarılı!")
            print("Çıktı:", result.stdout[:200])
        else:
            print("❌ CLI test hatası:")
            print("Stderr:", result.stderr[:200])
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ CLI test hatası: {e}")
        return False

if __name__ == "__main__":
    print("🚀 D64 Converter Test Suite")
    print("="*50)
    
    # Test.prg oluştur
    create_test_prg()
    
    # GUI test
    gui_success = test_gui_safe()
    
    # CLI test
    cli_success = test_cli_mode()
    
    print("\n" + "="*50)
    print("📊 TEST SONUÇLARI:")
    print(f"📄 Test dosyası: {'✅' if os.path.exists('test.prg') else '❌'}")
    print(f"🖥️ GUI test: {'✅' if gui_success else '❌'}")
    print(f"🔧 CLI test: {'✅' if cli_success else '❌'}")
    
    if gui_success and cli_success:
        print("\n🎉 Tüm testler başarılı!")
    else:
        print("\n⚠️ Bazı testler başarısız!")
