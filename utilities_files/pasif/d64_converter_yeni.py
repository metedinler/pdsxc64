import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import os
import sys
import threading
import time
import logging

# Kendi modüllerimiz
from d64_reader import (read_image, read_directory, read_t64_directory, read_tap_directory,
                       extract_prg_file, extract_t64_prg, extract_tap_prg, extract_p00_prg)
from enhanced_d64_reader import (enhanced_read_image, enhanced_read_directory, enhanced_extract_prg)
from c1541_python_emulator import (enhanced_c1541_read_image, enhanced_c1541_read_directory, 
                                   enhanced_c1541_extract_prg, enhanced_c1541_get_disk_info)
from advanced_disassembler import AdvancedDisassembler, Disassembler
from parser import CodeEmitter, parse_line, load_instruction_map
from c64_basic_parser import C64BasicParser
from sprite_converter import SpriteConverter
from sid_converter import SIDConverter

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    TkinterDnD = None
    DND_FILES = None

class D64ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("D64 Converter - Gelişmiş Disassembler")
        self.root.geometry("1200x800")
        
        # Değişkenler
        self.d64_path = tk.StringVar()
        self.use_illegal_opcodes = tk.BooleanVar(value=False)
        self.use_py65_disassembler = tk.BooleanVar(value=False)
        self.use_advanced_disassembler = tk.BooleanVar(value=True)
        self.entries = []
        self.basic_parser = C64BasicParser()
        self.sprite_converter = SpriteConverter()
        self.sid_converter = SIDConverter()
        self.selected_files = []
        
        self.setup_gui()
        self.setup_logging()
        
        # Sürükle-bırak desteği - opsiyonel
        if TkinterDnD and DND_FILES:
            try:
                self.setup_drag_drop()
            except Exception as e:
                print(f"Sürükle-bırak desteği başlatılamadı: {e}")
        else:
            print("Sürükle-bırak desteği yok - sadece dosya seçim butonu kullanılacak")

    def setup_gui(self):
        # Ana stil ayarları
        style = ttk.Style()
        style.theme_use('clam')
        
        # Treeview için özel stil
        style.configure("Treeview", 
                       background="white",
                       foreground="black",
                       fieldbackground="white",
                       font=('Courier', 10))
        style.configure("Treeview.Heading", 
                       background="lightgray",
                       foreground="black",
                       font=('Courier', 10, 'bold'))
        style.map('Treeview', background=[('selected', 'lightblue')])
        
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Dosya seçim bölümü
        file_frame = ttk.LabelFrame(main_frame, text="Dosya Seçimi", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(file_frame, text="D64/D71/D81/T64/TAP Dosyası:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.d64_path, width=60).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(file_frame, text="Seç", command=self.select_file).grid(row=0, column=2, padx=(10, 0))
        
        # Dosya listesi
        list_frame = ttk.LabelFrame(main_frame, text="Dosya Listesi", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Treeview ile dosya listesi
        columns = ('Name', 'Type', 'Track', 'Sector', 'Size')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Sütun başlıkları
        self.tree.heading('Name', text='Dosya Adı')
        self.tree.heading('Type', text='Tip')
        self.tree.heading('Track', text='Track')
        self.tree.heading('Sector', text='Sector')
        self.tree.heading('Size', text='Boyut')
        
        # Sütun genişlikleri
        self.tree.column('Name', width=200, minwidth=150)
        self.tree.column('Type', width=60, minwidth=50)
        self.tree.column('Track', width=80, minwidth=60)
        self.tree.column('Sector', width=80, minwidth=60)
        self.tree.column('Size', width=100, minwidth=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Seçenekler
        options_frame = ttk.LabelFrame(main_frame, text="Seçenekler", padding="10")
        options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(options_frame, text="Illegal Opcode'ları Kullan", 
                       variable=self.use_illegal_opcodes).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="py65 Disassembler Kullan", 
                       variable=self.use_py65_disassembler).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Checkbutton(options_frame, text="Gelişmiş Disassembler Kullan", 
                       variable=self.use_advanced_disassembler).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        # Butonlar - tek satır
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # İlk grup
        group1 = ttk.LabelFrame(button_frame, text="Dönüştürme", padding="5")
        group1.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(group1, text="Assembly'e Çevir", command=self.convert_to_assembly).grid(row=0, column=0, padx=2)
        ttk.Button(group1, text="C'ye Çevir", command=self.convert_to_c).grid(row=0, column=1, padx=2)
        ttk.Button(group1, text="QBasic'e Çevir", command=self.convert_to_qbasic).grid(row=0, column=2, padx=2)
        
        # İkinci grup
        group2 = ttk.LabelFrame(button_frame, text="Analiz", padding="5")
        group2.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(group2, text="PDSX'e Çevir", command=self.convert_to_pdsx).grid(row=0, column=0, padx=2)
        ttk.Button(group2, text="Pseudo'ya Çevir", command=self.convert_to_pseudo).grid(row=0, column=1, padx=2)
        ttk.Button(group2, text="BASIC'e Çevir", command=self.convert_to_basic).grid(row=0, column=2, padx=2)
        
        # Üçüncü grup
        group3 = ttk.LabelFrame(button_frame, text="Özellikler", padding="5")
        group3.grid(row=0, column=2, sticky=(tk.W, tk.E))
        
        ttk.Button(group3, text="Sprite Çevir", command=self.convert_sprite).grid(row=0, column=0, padx=2)
        ttk.Button(group3, text="SID Çevir", command=self.convert_sid).grid(row=0, column=1, padx=2)
        ttk.Button(group3, text="Tek Dosya Çevir", command=self.convert_single_file).grid(row=0, column=2, padx=2)
        
        # Notebook için farklı çıktılar
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Çıktı sekmeleri
        self.output_tabs = {}
        tab_names = ['Assembly', 'C', 'QBasic', 'PDSX', 'Pseudo', 'BASIC']
        for tab_name in tab_names:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            
            text_widget = tk.Text(frame, wrap=tk.WORD, font=('Courier', 10))
            scrollbar_text = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar_text.set)
            
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            scrollbar_text.grid(row=0, column=1, sticky=(tk.N, tk.S))
            
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            
            self.output_tabs[tab_name] = text_widget
        
        # Durum çubuğu
        self.status_var = tk.StringVar(value="Hazır")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Grid ağırlıkları
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

    def setup_logging(self):
        """Logging sistemini ayarla"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'd64_converter.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)

    def select_file(self):
        """Dosya seçim dialogu"""
        file_types = [
            ('Commodore 64 Disk Files', '*.d64 *.d71 *.d81 *.d84'),
            ('Commodore 64 Tape Files', '*.t64 *.tap'),
            ('Commodore 64 Program Files', '*.prg *.p00'),
            ('Commodore 64 GCR Files', '*.g64'),
            ('Tüm Dosyalar', '*.*')
        ]
        
        file_path = filedialog.askopenfilename(
            title="Commodore 64 Dosyası Seç",
            filetypes=file_types
        )
        
        if file_path:
            self.d64_path.set(file_path)
            print(f"Dosya seçildi: {file_path}")  # Debug
            self.load_image(file_path)

    def load_image(self, file_path):
        """Disk imajını yükle - Gelişmiş okuyucularla"""
        try:
            self.status_var.set("Disk dosyası yükleniyor...")
            print(f"Dosya yükleniyor: {file_path}")  # Debug
            
            # Dosya uzantısını al
            ext = Path(file_path).suffix.lower()
            print(f"Dosya uzantısı: {ext}")  # Debug
            
            # Önce enhanced_c1541_read_image ile dene
            try:
                print("C1541 emülatörü deneniyor...")  # Debug
                disk_data, ext = enhanced_c1541_read_image(file_path)
                if disk_data:
                    self.entries = enhanced_c1541_read_directory(disk_data, ext)
                    print(f"C1541 ile {len(self.entries)} dosya bulundu")  # Debug
                    if self.entries:
                        self.update_file_list()
                        
                        # Disk bilgilerini al
                        disk_info = enhanced_c1541_get_disk_info(disk_data, ext)
                        if disk_info:
                            self.status_var.set(f"Disk: {disk_info['disk_name']} (ID: {disk_info['disk_id']}) - {len(self.entries)} dosya")
                        else:
                            self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu")
                        return
            except Exception as e:
                print(f"enhanced_c1541_read_image hatası: {e}")
                
            # Fallback: enhanced_read_image ile dene
            try:
                print("Enhanced reader deneniyor...")  # Debug
                disk_data, ext = enhanced_read_image(file_path)
                if disk_data:
                    self.entries = enhanced_read_directory(disk_data, ext)
                    print(f"Enhanced reader ile {len(self.entries)} dosya bulundu")  # Debug
                    if self.entries:
                        self.update_file_list()
                        self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu")
                        return
            except Exception as e:
                print(f"enhanced_read_image hatası: {e}")
                
            # Fallback: read_image ile dene
            try:
                print("Basic reader deneniyor...")  # Debug
                disk_data, ext = read_image(file_path)
                if disk_data:
                    # Uzantıya göre directory okuma
                    if ext == '.t64':
                        self.entries = read_t64_directory(disk_data)
                    elif ext == '.tap':
                        self.entries = read_tap_directory(disk_data)
                    else:
                        self.entries = read_directory(disk_data, ext)
                    
                    print(f"Basic reader ile {len(self.entries)} dosya bulundu")  # Debug
                    if self.entries:
                        self.update_file_list()
                        self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu")
                        return
            except Exception as e:
                print(f"read_image hatası: {e}")
                
            # Hiçbir okuyucu çalışmadı
            self.status_var.set("Disk dosyası okunamadı")
            self.entries = []
            print("Hiçbir okuyucu çalışmadı")  # Debug
            
        except Exception as e:
            self.status_var.set(f"Hata: {str(e)}")
            self.entries = []
            print(f"load_image genel hatası: {e}")
            
        finally:
            self.update_file_list()

    def update_file_list(self):
        """Dosya listesini güncelle"""
        # Mevcut öğeleri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yeni öğeleri ekle
        for entry in self.entries:
            filename = entry.get('filename', 'UNKNOWN')
            file_type = entry.get('type', 'UNKNOWN')
            track = entry.get('track', 0)
            sector = entry.get('sector', 0)
            size = entry.get('size', 0)
            
            self.tree.insert('', 'end', values=(filename, file_type, track, sector, size))
        
        print(f"Dosya listesi güncellendi: {len(self.entries)} dosya")  # Debug

    def convert_single_file(self):
        """Seçili dosyayı dönüştür"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin")
            return
        
        item = self.tree.item(selection[0])
        filename = item['values'][0]
        
        # Dosyayı bul
        selected_entry = None
        for entry in self.entries:
            if entry.get('filename') == filename:
                selected_entry = entry
                break
        
        if not selected_entry:
            messagebox.showerror("Hata", "Seçili dosya bulunamadı")
            return
        
        self.status_var.set(f"Dosya dönüştürülüyor: {filename}")
        
        # Threading ile dönüştürme
        threading.Thread(target=self._convert_single_file_thread, args=(selected_entry,), daemon=True).start()

    def _convert_single_file_thread(self, entry):
        """Thread içinde dosya dönüştürme"""
        try:
            # PRG dosyasını çıkart
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.status_var.set("PRG verisi çıkarılamadı")
                return
            
            # Disassemble et
            disassembler = AdvancedDisassembler(use_illegal_opcodes=self.use_illegal_opcodes.get())
            
            if self.use_py65_disassembler.get():
                assembly_code = disassembler.disassemble_py65(prg_data)
            else:
                assembly_code = disassembler.disassemble_simple(prg_data)
            
            # Tüm dillere çevir
            self.root.after(0, self._update_all_outputs, assembly_code, disassembler)
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Hata: {str(e)}"))

    def _update_all_outputs(self, assembly_code, disassembler):
        """Tüm çıktı sekmelerini güncelle"""
        try:
            # Assembly
            self.output_tabs['Assembly'].delete(1.0, tk.END)
            self.output_tabs['Assembly'].insert(tk.END, assembly_code)
            
            # C
            c_code = disassembler.convert_to_language(assembly_code, 'c')
            self.output_tabs['C'].delete(1.0, tk.END)
            self.output_tabs['C'].insert(tk.END, c_code)
            
            # QBasic
            qbasic_code = disassembler.convert_to_language(assembly_code, 'qbasic')
            self.output_tabs['QBasic'].delete(1.0, tk.END)
            self.output_tabs['QBasic'].insert(tk.END, qbasic_code)
            
            # PDSX
            pdsx_code = disassembler.convert_to_language(assembly_code, 'pdsx')
            self.output_tabs['PDSX'].delete(1.0, tk.END)
            self.output_tabs['PDSX'].insert(tk.END, pdsx_code)
            
            # Pseudo
            pseudo_code = disassembler.convert_to_language(assembly_code, 'pseudo')
            self.output_tabs['Pseudo'].delete(1.0, tk.END)
            self.output_tabs['Pseudo'].insert(tk.END, pseudo_code)
            
            # BASIC
            basic_code = disassembler.convert_to_language(assembly_code, 'commodore_basic_v2')
            self.output_tabs['BASIC'].delete(1.0, tk.END)
            self.output_tabs['BASIC'].insert(tk.END, basic_code)
            
            self.status_var.set("Dönüştürme tamamlandı")
            
        except Exception as e:
            self.status_var.set(f"Çıktı güncelleme hatası: {str(e)}")

    def extract_prg_data(self, entry):
        """PRG verisini çıkart"""
        try:
            disk_path = self.d64_path.get()
            if not disk_path:
                return None
            
            ext = Path(disk_path).suffix.lower()
            
            # C1541 emülatörü ile dene
            try:
                disk_data, ext = enhanced_c1541_read_image(disk_path)
                if disk_data:
                    return enhanced_c1541_extract_prg(disk_data, ext, entry)
            except Exception as e:
                print(f"C1541 extract hatası: {e}")
            
            # Enhanced reader ile dene
            try:
                disk_data, ext = enhanced_read_image(disk_path)
                if disk_data:
                    return enhanced_extract_prg(disk_data, ext, entry)
            except Exception as e:
                print(f"Enhanced extract hatası: {e}")
            
            # Basic reader ile dene
            try:
                disk_data, ext = read_image(disk_path)
                if disk_data:
                    if ext == '.t64':
                        return extract_t64_prg(disk_data, entry)
                    elif ext == '.tap':
                        return extract_tap_prg(disk_data, entry)
                    elif ext == '.p00':
                        return extract_p00_prg(disk_data, entry)
                    else:
                        return extract_prg_file(disk_data, entry)
            except Exception as e:
                print(f"Basic extract hatası: {e}")
            
            return None
            
        except Exception as e:
            print(f"PRG çıkarma hatası: {e}")
            return None

    # Dönüştürme fonksiyonları
    def convert_to_assembly(self):
        """Assembly'e dönüştür"""
        self.convert_single_file()

    def convert_to_c(self):
        """C'ye dönüştür"""
        self.convert_single_file()

    def convert_to_qbasic(self):
        """QBasic'e dönüştür"""
        self.convert_single_file()

    def convert_to_pdsx(self):
        """PDSX'e dönüştür"""
        self.convert_single_file()

    def convert_to_pseudo(self):
        """Pseudo koda dönüştür"""
        self.convert_single_file()

    def convert_to_basic(self):
        """BASIC'e dönüştür"""
        self.convert_single_file()

    def convert_sprite(self):
        """Sprite dönüştür"""
        messagebox.showinfo("Bilgi", "Sprite dönüştürme özelliği henüz aktif değil")

    def convert_sid(self):
        """SID dönüştür"""
        messagebox.showinfo("Bilgi", "SID dönüştürme özelliği henüz aktif değil")

    def setup_drag_drop(self):
        """Sürükle-bırak desteği"""
        if TkinterDnD and DND_FILES:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        """Dosya sürüklendiğinde"""
        files = self.root.tk.splitlist(event.data)
        if files:
            self.d64_path.set(files[0])
            self.load_image(files[0])

def main():
    # TkinterDnD desteği varsa onu kullan
    if TkinterDnD:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    app = D64ConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
