#!/usr/bin/env python3
"""
D64 Converter GUI - PyGubu Designer Integration
Bu dosya PyGubu Designer ile oluşturulan UI'yi yükler ve mevcut 
D64ConverterGUI sınıfı ile entegre eder.
"""

import tkinter as tk
import tkinter.ttk as ttk
import pygubu
import os
from pathlib import Path

class D64ConverterGUIBuilder:
    """PyGubu Designer ile oluşturulan GUI'yi yönetir"""
    
    def __init__(self, master=None):
        self.master = master
        self.builder = pygubu.Builder()
        
        # UI dosyasının yolunu belirle
        ui_file = Path(__file__).parent / "gui_designs" / "d64_converter_main.ui"
        
        if not ui_file.exists():
            raise FileNotFoundError(f"UI dosyası bulunamadı: {ui_file}")
        
        # UI dosyasını yükle
        self.builder.add_from_file(str(ui_file))
        
        # Ana pencereyi oluştur
        self.main_window = self.builder.get_object('main_window', master)
        
        # Widget referanslarını al
        self.widgets = {}
        self._get_widget_references()
        
        # Event handler'ları bağla
        self._connect_events()
        
        # Treeview sütunlarını yapılandır
        self._setup_treeview()
    
    def _get_widget_references(self):
        """Tüm widget referanslarını al"""
        widget_ids = [
            'file_tree', 'open_file_btn', 'hybrid_analysis_btn',
            'format_combo', 'engine_combo', 'disassemble_btn',
            'target_lang_combo', 'transpile_btn',
            'disassembly_output'
        ]
        
        for widget_id in widget_ids:
            try:
                self.widgets[widget_id] = self.builder.get_object(widget_id)
                print(f"✅ Widget bulundu: {widget_id}")
            except Exception as e:
                print(f"⚠️ Widget bulunamadı: {widget_id} - {e}")
    
    def _connect_events(self):
        """Event handler'ları bağla"""
        # Buton event'leri
        if 'open_file_btn' in self.widgets:
            self.widgets['open_file_btn'].configure(command=self.on_open_file)
        
        if 'hybrid_analysis_btn' in self.widgets:
            self.widgets['hybrid_analysis_btn'].configure(command=self.on_hybrid_analysis)
        
        if 'disassemble_btn' in self.widgets:
            self.widgets['disassemble_btn'].configure(command=self.on_disassemble)
        
        if 'transpile_btn' in self.widgets:
            self.widgets['transpile_btn'].configure(command=self.on_transpile)
    
    def _setup_treeview(self):
        """Listbox'ı dosya listesi için yapılandır"""
        if 'file_tree' not in self.widgets:
            print("⚠️ file_tree widget'ı bulunamadı")
            return
        
        # Listbox'ı dosya isimleri ile doldur (test için)
        listbox = self.widgets['file_tree']
        test_files = [
            "📁 DISK.D64",
            "  📄 GAME.PRG (BASIC)",
            "  📄 LOADER.PRG (ML)",
            "  📄 SPRITES.PRG (DATA)",
            "  📄 MUSIC.SID"
        ]
        
        for file_entry in test_files:
            listbox.insert('end', file_entry)
        
        print("✅ Dosya listesi yüklendi")
    
    def on_open_file(self):
        """Dosya açma event handler"""
        print("📂 Dosya açma fonksiyonu çağrıldı")
        # Buraya mevcut gui_manager.py'deki dosya açma kodunu entegre edeceksiniz
    
    def on_hybrid_analysis(self):
        """Hibrit analiz event handler"""
        print("🔍 Hibrit analiz fonksiyonu çağrıldı")
        # Buraya hibrit analiz kodunu entegre edeceksiniz
    
    def on_disassemble(self):
        """Disassembly event handler"""
        format_value = self.widgets['format_combo'].get() if 'format_combo' in self.widgets else "ACME"
        engine_value = self.widgets['engine_combo'].get() if 'engine_combo' in self.widgets else "Advanced"
        
        print(f"🔧 Disassembly başlatıldı - Format: {format_value}, Engine: {engine_value}")
        
        # Test çıktısı ekle
        if 'disassembly_output' in self.widgets:
            output_text = f"""
; D64 Converter - Disassembly Output
; Format: {format_value} | Engine: {engine_value}
; Generated: {self._get_timestamp()}

*=$C000        ; Program start address

MAIN:
    LDA #$00   ; Load accumulator with 0
    STA $D020  ; Set border color
    STA $D021  ; Set background color
    
LOOP:
    INC $D020  ; Increment border color
    JMP LOOP   ; Jump to loop
    
; End of disassembly
"""
            self.widgets['disassembly_output'].delete(1.0, 'end')
            self.widgets['disassembly_output'].insert(1.0, output_text)
    
    def _get_timestamp(self):
        """Zaman damgası al"""
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def on_transpile(self):
        """Transpile event handler"""
        target_lang = self.widgets['target_lang_combo'].get() if 'target_lang_combo' in self.widgets else "C"
        
        print(f"🔄 Transpile başlatıldı - Target: {target_lang}")
        # Buraya transpile kodunu entegre edeceksiniz
    
    def show(self):
        """GUI'yi göster"""
        if self.main_window:
            self.main_window.deiconify()
    
    def hide(self):
        """GUI'yi gizle"""
        if self.main_window:
            self.main_window.withdraw()

def main():
    """PyGubu Designer GUI'sini test et"""
    root = tk.Tk()
    root.withdraw()  # Ana root penceresini gizle
    
    try:
        app = D64ConverterGUIBuilder(root)
        app.show()
        
        # Entry widget'larına varsayılan değerler ata
        if 'format_combo' in app.widgets:
            app.widgets['format_combo'].insert(0, "ACME")
        if 'engine_combo' in app.widgets:
            app.widgets['engine_combo'].insert(0, "Advanced")
        if 'target_lang_combo' in app.widgets:
            app.widgets['target_lang_combo'].insert(0, "C")
        
        print("✅ PyGubu GUI başarıyla yüklendi!")
        print("💡 Test etmek için butonlara tıklayın.")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ GUI yüklenirken hata: {e}")
        root.destroy()

if __name__ == "__main__":
    main()
