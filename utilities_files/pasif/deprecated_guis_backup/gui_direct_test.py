"""
Direkt GUI Test - D64 Converter
"""
import tkinter as tk
import sys
import os

# Projeyi path'e ekle
sys.path.insert(0, os.getcwd())

def test_gui_direct():
    """GUI'yi direkt test et"""
    try:
        print("🚀 GUI direkt test başlatılıyor...")
        
        # Import test
        from d64_converter import D64ConverterApp
        print("✅ D64ConverterApp import başarılı")
        
        # Root window oluştur
        root = tk.Tk()
        root.title("D64 Converter - Direkt Test")
        root.geometry("1200x800")
        
        # App oluştur
        print("🔧 D64ConverterApp oluşturuluyor...")
        app = D64ConverterApp(root)
        print("✅ App başarıyla oluşturuldu")
        
        # GUI bilgilerini göster
        print(f"📊 GUI Bilgileri:")
        print(f"   - Disassembler: {app.disassembler_var.get()}")
        print(f"   - Illegal opcodes: {app.use_illegal_opcodes.get()}")
        print(f"   - Memory analysis: {app.memory_analysis.get()}")
        print(f"   - Auto format dirs: {app.auto_format_dirs.get()}")
        
        # Pencereyi görünür yap
        root.deiconify()
        root.lift()
        root.focus_set()
        
        print("🖥️ GUI gösteriliyor...")
        print("📝 Pencereyi kapatmak için X butonuna tıklayın")
        
        # Ana döngü
        root.mainloop()
        
        print("✅ GUI test tamamlandı")
        return True
        
    except Exception as e:
        print(f"❌ GUI test hatası: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gui_direct()
    if success:
        print("🎉 GUI başarıyla çalıştı!")
    else:
        print("💥 GUI çalıştırılamadı!")
