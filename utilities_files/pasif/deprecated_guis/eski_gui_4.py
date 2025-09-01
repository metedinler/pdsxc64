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
                       extract_prg_file, extract_t64_prg, extract_tap_prg, extract_p00_prg,
                       extract_seq_file, extract_usr_file, extract_del_file)
from enhanced_d64_reader import (enhanced_read_image, enhanced_read_directory, enhanced_extract_prg)
from c1541_python_emulator import (enhanced_c1541_read_image, enhanced_c1541_read_directory, 
                                   enhanced_c1541_extract_prg, enhanced_c1541_get_disk_info)
from advanced_disassembler import AdvancedDisassembler, Disassembler
from improved_disassembler import ImprovedDisassembler
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
        
        # Logging sistemi
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("D64ConverterApp başlatılıyor...")
        
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
        
        # Çıktı klasörlerini oluştur
        self.setup_output_directories()
        
        self.setup_gui()
        
        self.logger.info("D64ConverterApp başarıyla başlatıldı")
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
        
        ttk.Label(file_frame, text="C64 Dosyası (D64/D71/D81/D84/T64/TAP/PRG/P00/G64/LNX/LYNX/CRT/BIN):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.d64_path, width=60).grid(row=0, column=1, padx=(10, 0))
        ttk.Button(file_frame, text="Seç", command=self.select_file).grid(row=0, column=2, padx=(10, 0))
        ttk.Button(file_frame, text="Dosya Bul", command=self.find_files).grid(row=0, column=3, padx=(5, 0))
        
        # Dosya türü bilgisi
        info_label = ttk.Label(file_frame, text="💡 İpucu: Dosya seçim dialogunda 'All C64 Files' seçeneğini kullanın veya Windows'da Dosya Gezgini > Görünüm > Dosya adı uzantıları'nı etkinleştirin", 
                              font=('Arial', 8), foreground='blue')
        info_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
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
        
        # Format seçimi kaldırıldı - her format kendi butonuna sahip
        
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
        
        # Dördüncü grup - Kaydetme
        group4 = ttk.LabelFrame(button_frame, text="Kaydetme", padding="5")
        group4.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(group4, text="Aktif Sekmeyi Kaydet", command=self.save_active_tab).grid(row=0, column=0, padx=2)
        ttk.Button(group4, text="Tüm Sekmeleri Kaydet", command=self.save_all_tabs).grid(row=0, column=1, padx=2)
        ttk.Button(group4, text="Çıktı Klasörünü Aç", command=self.open_output_folder).grid(row=0, column=2, padx=2)
        
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

    def setup_output_directories(self):
        """Çıktı klasörlerini oluştur"""
        self.output_dirs = {
            'Assembly': Path("asm_files"),
            'C': Path("c_files"),
            'QBasic': Path("qbasic_files"),
            'PDSX': Path("pdsx_files"),
            'Pseudo': Path("pseudo_files"),
            'BASIC': Path("basic_files")
        }
        
        for dir_path in self.output_dirs.values():
            dir_path.mkdir(exist_ok=True)
            
    def get_current_filename(self):
        """Şu anki seçili dosyadan filename al"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            return item['values'][0]
        return "output"
    
    def save_active_tab(self):
        """Aktif sekmeyi kaydet"""
        try:
            current_tab = self.notebook.tab(self.notebook.select(), "text")
            text_widget = self.output_tabs[current_tab]
            content = text_widget.get(1.0, tk.END).strip()
            
            if not content:
                messagebox.showwarning("Uyarı", "Kaydedilecek içerik yok!")
                return
            
            filename = self.get_current_filename()
            
            # Dosya uzantısını belirle
            extensions = {
                'Assembly': '.asm',
                'C': '.c',
                'QBasic': '.bas',
                'PDSX': '.pdx',
                'Pseudo': '.txt',
                'BASIC': '.bas'
            }
            
            ext = extensions.get(current_tab, '.txt')
            output_dir = self.output_dirs[current_tab]
            file_path = output_dir / f"{filename}{ext}"
            
            # Dosyayı kaydet
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.status_var.set(f"{current_tab} kaydedildi: {file_path}")
            messagebox.showinfo("Başarılı", f"Dosya kaydedildi:\n{file_path}")
            
        except Exception as e:
            self.status_var.set(f"Kaydetme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")
    
    def save_all_tabs(self):
        """Tüm sekmeleri kaydet"""
        try:
            filename = self.get_current_filename()
            saved_files = []
            
            extensions = {
                'Assembly': '.asm',
                'C': '.c',
                'QBasic': '.bas',
                'PDSX': '.pdx',
                'Pseudo': '.txt',
                'BASIC': '.bas'
            }
            
            for tab_name, text_widget in self.output_tabs.items():
                content = text_widget.get(1.0, tk.END).strip()
                
                if content:  # Sadece içerik varsa kaydet
                    ext = extensions.get(tab_name, '.txt')
                    output_dir = self.output_dirs[tab_name]
                    file_path = output_dir / f"{filename}{ext}"
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    saved_files.append(str(file_path))
            
            if saved_files:
                self.status_var.set(f"{len(saved_files)} dosya kaydedildi")
                messagebox.showinfo("Başarılı", f"{len(saved_files)} dosya kaydedildi:\n" + "\n".join(saved_files))
            else:
                messagebox.showwarning("Uyarı", "Kaydedilecek içerik yok!")
                
        except Exception as e:
            self.status_var.set(f"Kaydetme hatası: {str(e)}")
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")
    
    def open_output_folder(self):
        """Çıktı klasörünü aç"""
        try:
            import subprocess
            import platform
            
            # İşletim sistemine göre komut
            if platform.system() == "Windows":
                subprocess.run(['explorer', '.'], check=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', '.'], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', '.'], check=True)
                
        except Exception as e:
            messagebox.showerror("Hata", f"Klasör açma hatası: {str(e)}")

    def find_files(self):
        """Bilgisayardaki C64 dosyalarını bul ve listele"""
        def find_c64_files():
            """C64 dosyalarını arayan thread fonksiyonu"""
            try:
                supported_extensions = ['.d64', '.d71', '.d81', '.d84', '.t64', '.tap', '.prg', '.p00', '.g64', '.lnx', '.lynx', '.crt', '.bin']
                found_files = []
                
                # Arama dizinleri
                search_dirs = [
                    os.path.expanduser("~\\Downloads"),
                    os.path.expanduser("~\\Documents"),
                    os.path.expanduser("~\\Desktop"),
                    "C:\\",
                    "D:\\",
                    "E:\\"
                ]
                
                self.root.after(0, lambda: self.status_var.set("C64 dosyaları aranıyor..."))
                
                for search_dir in search_dirs:
                    if os.path.exists(search_dir):
                        print(f"Aranıyor: {search_dir}")
                        try:
                            for root_dir, dirs, files in os.walk(search_dir):
                                for file in files:
                                    ext = os.path.splitext(file)[1].lower()
                                    if ext in supported_extensions:
                                        full_path = os.path.join(root_dir, file)
                                        found_files.append(full_path)
                                        if len(found_files) >= 20:  # İlk 20 dosya
                                            break
                                if len(found_files) >= 20:
                                    break
                        except PermissionError:
                            continue
                    
                    if len(found_files) >= 20:
                        break
                
                self.root.after(0, lambda: self.show_found_files(found_files))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"Dosya arama hatası: {str(e)}"))
        
        # Thread'de ara
        threading.Thread(target=find_c64_files, daemon=True).start()
    
    def show_found_files(self, files):
        """Bulunan dosyaları göster"""
        if not files:
            self.status_var.set("C64 dosyası bulunamadı")
            messagebox.showinfo("Dosya Bulunamadı", "Hiç C64 dosyası bulunamadı.\n\nDesteklenen formatlar: D64, D71, D81, D84, T64, TAP, PRG, P00, G64, LNX, LYNX, CRT, BIN")
            return
        
        self.status_var.set(f"{len(files)} C64 dosyası bulundu")
        
        # Dosya seçim penceresi
        file_window = tk.Toplevel(self.root)
        file_window.title("Bulunan C64 Dosyaları")
        file_window.geometry("600x400")
        file_window.grab_set()
        
        tk.Label(file_window, text=f"Bulunan C64 dosyaları ({len(files)} adet):").pack(pady=10)
        
        # Listbox
        listbox_frame = tk.Frame(file_window)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Dosyaları listele
        for file_path in files:
            filename = os.path.basename(file_path)
            ext = os.path.splitext(filename)[1].upper()
            size = os.path.getsize(file_path)
            listbox.insert(tk.END, f"{filename} ({ext}, {size} bytes) - {file_path}")
        
        # Buton çerçevesi
        button_frame = tk.Frame(file_window)
        button_frame.pack(pady=10)
        
        def select_from_list():
            selection = listbox.curselection()
            if selection:
                selected_file = files[selection[0]]
                self.d64_path.set(selected_file)
                self.status_var.set("Dosya seçildi, yükleniyor...")
                file_window.destroy()
                
                # Dosyayı yükle
                threading.Thread(target=self.load_image, args=(selected_file,), daemon=True).start()
            else:
                messagebox.showwarning("Seçim Yok", "Lütfen bir dosya seçin")
        
        tk.Button(button_frame, text="Seç", command=select_from_list).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="İptal", command=file_window.destroy).pack(side=tk.LEFT, padx=5)

    def select_file(self):
        """Dosya seçim dialogu"""
        try:
            self.logger.info("=== DOSYA SEÇİM DİALOGU BAŞLADI ===")
            self.status_var.set("Dosya seçim dialogu açılıyor...")
            
            # Windows için daha iyi dosya filtreleri
            file_types = [
                ('D64 Disk Files', '*.d64'),
                ('D71 Disk Files', '*.d71'),
                ('D81 Disk Files', '*.d81'),
                ('D84 Disk Files', '*.d84'),
                ('T64 Tape Files', '*.t64'),
                ('TAP Tape Files', '*.tap'),
                ('PRG Program Files', '*.prg'),
                ('P00 Program Files', '*.p00'),
                ('G64 GCR Files', '*.g64'),
                ('LNX Archive Files', '*.lnx'),
                ('LYNX Archive Files', '*.lynx'),
                ('CRT Cartridge Files', '*.crt'),
                ('BIN Binary Files', '*.bin'),
                ('All Files', '*.*')
            ]
            
            self.logger.info("Dosya seçim dialogu açılıyor...")
            
            # Dosya seçim dialogu - hata yakalama ile
            file_path = None
            try:
                file_path = filedialog.askopenfilename(
                    title="Commodore 64 File Selector - Select D64, D71, D81, D84, T64, TAP, PRG, P00, G64, LNX, LYNX, CRT, BIN",
                    filetypes=file_types,
                    initialdir=os.path.expanduser("~\\Downloads"),  # Downloads klasörünü varsayılan yap
                    defaultextension=".d64"
                )
                self.logger.info(f"Dialog sonucu: {file_path}")
            except Exception as dialog_error:
                self.logger.error(f"Dosya dialog hatası: {dialog_error}")
                self.status_var.set("Dosya seçim dialogu hatası")
                return
            
            if file_path:
                self.logger.info(f"Dosya seçildi: {file_path}")
                
                # Dosya kontrolü
                if not os.path.exists(file_path):
                    self.logger.error(f"Dosya mevcut değil: {file_path}")
                    messagebox.showerror("Dosya Hatası", f"Dosya bulunamadı: {file_path}")
                    return
                
                try:
                    file_size = os.path.getsize(file_path)
                    self.logger.info(f"Dosya uzantısı: {os.path.splitext(file_path)[1]}")
                    self.logger.info(f"Dosya boyutu: {file_size} bytes")
                    
                    self.d64_path.set(file_path)
                    self.status_var.set("Dosya seçildi, yükleniyor...")
                    
                    # Threading olmadan önce test et
                    self.logger.info("Dosya yükleme başlatılıyor...")
                    self.load_image(file_path)
                    
                except Exception as file_error:
                    self.logger.error(f"Dosya işleme hatası: {file_error}")
                    import traceback
                    self.logger.error(traceback.format_exc())
                    messagebox.showerror("Dosya Hatası", f"Dosya işlenemedi: {file_error}")
                    
            else:
                self.logger.info("Dosya seçimi iptal edildi")
                self.status_var.set("Dosya seçimi iptal edildi")
                
            self.logger.info("=== DOSYA SEÇİM DİALOGU TAMAMLANDI ===")
                
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"DOSYA SEÇİM HATASI: {error_msg}")
            self.logger.error(f"Hata tipi: {type(e).__name__}")
            import traceback
            self.logger.error(traceback.format_exc())
            try:
                messagebox.showerror("Dosya Seçim Hatası", f"Dosya seçim hatası: {error_msg}")
            except:
                self.logger.error("MessageBox gösterilemiyor")
            self.status_var.set("Dosya seçimi başarısız")

    def load_image(self, file_path):
        """Disk imajını yükle - Gelişmiş okuyucularla"""
        try:
            print(f"=== LOAD_IMAGE BAŞLADI: {file_path} ===")
            
            # GUI thread'ine status güncellemesi gönder
            self.root.after(0, lambda: self.status_var.set("Disk dosyası yükleniyor..."))
            print(f"Dosya yükleniyor: {file_path}")
            
            # Dosya mevcut mu kontrol et
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
            
            # Dosya uzantısını al
            ext = Path(file_path).suffix.lower()
            print(f"Dosya uzantısı: {ext}")
            
            # Desteklenen uzantıları kontrol et
            supported_extensions = ['.d64', '.d71', '.d81', '.d84', '.t64', '.tap', '.prg', '.p00', '.g64', '.lnx', '.lynx', '.crt', '.bin']
            if ext not in supported_extensions:
                print(f"Desteklenmeyen uzantı: {ext}")
                self.root.after(0, lambda: self.status_var.set(f"Desteklenmeyen dosya uzantısı: {ext}"))
                return
                
            # Önce enhanced_c1541_read_image ile dene
            if ext in ['.d64', '.d71', '.d81', '.d84']:
                try:
                    print("C1541 emülatörü deneniyor...")
                    disk_data, ext = enhanced_c1541_read_image(file_path)
                    if disk_data:
                        self.entries = enhanced_c1541_read_directory(disk_data, ext)
                        print(f"C1541 ile {len(self.entries)} dosya bulundu")
                        if self.entries:
                            self.root.after(0, self.update_file_list)
                            
                            # Disk bilgilerini al
                            try:
                                disk_info = enhanced_c1541_get_disk_info(disk_data, ext)
                                if disk_info:
                                    self.root.after(0, lambda: self.status_var.set(f"Disk: {disk_info['disk_name']} (ID: {disk_info['disk_id']}) - {len(self.entries)} dosya"))
                                else:
                                    self.root.after(0, lambda: self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu"))
                            except Exception as disk_info_error:
                                print(f"Disk bilgisi alınırken hata: {disk_info_error}")
                                self.root.after(0, lambda: self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu"))
                            
                            print("=== LOAD_IMAGE BAŞARILI (C1541) ===")
                            return
                except Exception as e:
                    print(f"enhanced_c1541_read_image hatası: {e}")
                    import traceback
                    traceback.print_exc()
                    
            # Fallback: enhanced_read_image ile dene
            try:
                print("Enhanced reader deneniyor...")
                disk_data, ext = enhanced_read_image(file_path)
                if disk_data:
                    self.entries = enhanced_read_directory(disk_data, ext)
                    print(f"Enhanced reader ile {len(self.entries)} dosya bulundu")
                    if self.entries:
                        self.root.after(0, self.update_file_list)
                        self.root.after(0, lambda: self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu"))
                        print("=== LOAD_IMAGE BAŞARILI (Enhanced) ===")
                        return
            except Exception as e:
                print(f"enhanced_read_image hatası: {e}")
                import traceback
                traceback.print_exc()
                
            # Fallback: read_image ile dene
            try:
                print("Basic reader deneniyor...")
                disk_data, ext = read_image(file_path)
                if disk_data:
                    # Uzantıya göre directory okuma
                    if ext == '.t64':
                        self.entries = read_t64_directory(disk_data)
                    elif ext == '.tap':
                        self.entries = read_tap_directory(disk_data)
                    elif ext == '.prg':
                        # PRG dosyası için tek entry oluştur
                        self.entries = [{
                            'filename': Path(file_path).stem,
                            'type': 'PRG',
                            'track': 0,
                            'sector': 0,
                            'size': len(disk_data),
                            'data': disk_data
                        }]
                    elif ext == '.p00':
                        # P00 dosyası için tek entry oluştur
                        self.entries = [{
                            'filename': Path(file_path).stem,
                            'type': 'PRG',
                            'track': 0,
                            'sector': 0,
                            'size': len(disk_data) - 26,  # P00 header size
                            'data': disk_data
                        }]
                    else:
                        self.entries = read_directory(disk_data, ext)
                    
                    print(f"Basic reader ile {len(self.entries)} dosya bulundu")
                    if self.entries:
                        self.root.after(0, self.update_file_list)
                        self.root.after(0, lambda: self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu"))
                        print("=== LOAD_IMAGE BAŞARILI (Basic) ===")
                        return
            except Exception as e:
                print(f"read_image hatası: {e}")
                import traceback
                traceback.print_exc()
                
            # Hiçbir okuyucu çalışmadı
            print("Hiçbir okuyucu çalışmadı")
            self.root.after(0, lambda: self.status_var.set("Disk dosyası okunamadı"))
            self.entries = []
            
        except Exception as e:
            error_msg = str(e)
            print(f"LOAD_IMAGE GENEL HATASI: {error_msg}")
            print(f"Hata tipi: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            
            self.root.after(0, lambda: self.status_var.set(f"Hata: {error_msg}"))
            self.entries = []
            self.root.after(0, lambda: messagebox.showerror("Hata", f"Dosya yükleme hatası: {error_msg}"))
            
        finally:
            print("=== LOAD_IMAGE TAMAMLANDI ===")
            self.root.after(0, self.update_file_list)

    def update_file_list(self):
        """Dosya listesini güncelle"""
        # Mevcut öğeleri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yeni öğeleri ekle
        for entry in self.entries:
            filename = entry.get('filename', 'UNKNOWN')
            # C1541 emülatörü 'type' kullanırken d64_reader 'file_type' kullanıyor
            file_type = entry.get('type', entry.get('file_type', 'UNKNOWN'))
            track = entry.get('track', 0)
            sector = entry.get('sector', 0)
            # C1541 emülatörü 'size' kullanırken d64_reader 'size_blocks' kullanıyor
            size = entry.get('size', entry.get('size_blocks', 0))
            
            self.tree.insert('', 'end', values=(filename, file_type, track, sector, size))
        
        print(f"Dosya listesi güncellendi: {len(self.entries)} dosya")  # Debug
        
        # İlk dosyayı göster
        if self.entries:
            print(f"İlk dosya yapısı: {self.entries[0]}")  # Debug

    def convert_to_specific_format(self, format_code, tab_name):
        """Belirli bir formata dönüştür ve sadece o sekmesini güncelle"""
        selection = self.tree.selection()
        if not selection:
            # Seçim yoksa ilk dosyayı al
            if self.entries:
                selected_entry = self.entries[0]
                print(f"Seçim yok, ilk dosya kullanılıyor: {selected_entry.get('filename')}")
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin")
                return
        else:
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
        
        self.status_var.set(f"Dosya {tab_name} formatına dönüştürülüyor: {selected_entry.get('filename')}")
        print(f"Dönüştürülecek dosya: {selected_entry}, Format: {format_code}")
        
        # Threading ile dönüştürme
        threading.Thread(target=self._convert_specific_format_thread, 
                        args=(selected_entry, format_code, tab_name), daemon=True).start()

    def _convert_specific_format_thread(self, entry, format_code, tab_name):
        """Thread içinde belirli format dönüştürme"""
        try:
            # PRG dosyasını çıkart
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.status_var.set("PRG verisi çıkarılamadı"))
                return
            
            print(f"PRG verisi çıkarıldı: {len(prg_data)} byte")
            
            # PRG dosyasından start_address ve code'u çıkar
            if len(prg_data) < 2:
                self.root.after(0, lambda: self.status_var.set("Geçersiz PRG verisi"))
                return
                
            start_address = prg_data[0] + (prg_data[1] << 8)
            code_data = prg_data[2:]
            
            print(f"Start address: ${start_address:04X}, Code size: {len(code_data)} bytes")
            
            # Format'a göre disassemble et
            
            if format_code == 'asm':
                # Assembly için disassemble
                disassembler = AdvancedDisassembler(
                    start_address=start_address,
                    code=code_data,
                    use_py65=self.use_py65_disassembler.get(),
                    use_illegal_opcodes=self.use_illegal_opcodes.get(),
                    output_format=format_code
                )
                
                if self.use_py65_disassembler.get():
                    result_code = disassembler.disassemble_py65(prg_data)
                else:
                    result_code = disassembler.disassemble_simple(prg_data)
            else:
                # Diğer formatlar için yeni ImprovedDisassembler kullan
                improved_disassembler = ImprovedDisassembler(
                    start_address=start_address,
                    code=code_data,
                    output_format=format_code
                )
                
                result_code = improved_disassembler.disassemble_to_format(prg_data)
            
            print(f"{tab_name} kod oluşturuldu: {len(result_code)} karakter")
            
            # Sadece ilgili sekmesini güncelle
            self.root.after(0, self._update_specific_tab, tab_name, result_code)
            
        except Exception as e:
            error_msg = str(e)
            print(f"_convert_specific_format_thread hatası: {error_msg}")
            self.root.after(0, lambda msg=error_msg: self.status_var.set(f"Hata: {msg}"))

    def _update_specific_tab(self, tab_name, content):
        """Belirli bir sekmesini güncelle"""
        try:
            self.output_tabs[tab_name].delete(1.0, tk.END)
            self.output_tabs[tab_name].insert(tk.END, content)
            
            # İlgili sekmesine geç
            for i, tab_id in enumerate(self.notebook.tabs()):
                if self.notebook.tab(tab_id, "text") == tab_name:
                    self.notebook.select(tab_id)
                    break
            
            self.status_var.set(f"{tab_name} formatına dönüştürme tamamlandı")
            print(f"{tab_name} sekmesi güncellendi")
            
        except Exception as e:
            self.status_var.set(f"Sekme güncelleme hatası: {str(e)}")
            print(f"_update_specific_tab hatası: {e}")

    def convert_single_file(self):
        """Tüm formatları bir kerede dönüştür (eski fonksiyon)"""
        selection = self.tree.selection()
        if not selection:
            # Seçim yoksa ilk dosyayı al
            if self.entries:
                selected_entry = self.entries[0]
                print(f"Seçim yok, ilk dosya kullanılıyor: {selected_entry.get('filename')}")  # Debug
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin")
                return
        else:
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
        
        self.status_var.set(f"Dosya dönüştürülüyor: {selected_entry.get('filename')}")
        print(f"Dönüştürülecek dosya: {selected_entry}")  # Debug
        
        # Threading ile dönüştürme
        threading.Thread(target=self._convert_single_file_thread, args=(selected_entry,), daemon=True).start()
        """Seçili dosyayı dönüştür"""
        selection = self.tree.selection()
        if not selection:
            # Seçim yoksa ilk dosyayı al
            if self.entries:
                selected_entry = self.entries[0]
                print(f"Seçim yok, ilk dosya kullanılıyor: {selected_entry.get('filename')}")  # Debug
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir dosya seçin")
                return
        else:
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
        
        self.status_var.set(f"Dosya dönüştürülüyor: {selected_entry.get('filename')}")
        print(f"Dönüştürülecek dosya: {selected_entry}")  # Debug
        
        # Threading ile dönüştürme
        threading.Thread(target=self._convert_single_file_thread, args=(selected_entry,), daemon=True).start()

    def _convert_single_file_thread(self, entry):
        """Thread içinde dosya dönüştürme"""
        try:
            # PRG dosyasını çıkart
            prg_data = self.extract_prg_data(entry)
            if not prg_data:
                self.root.after(0, lambda: self.status_var.set("PRG verisi çıkarılamadı"))
                return
            
            print(f"PRG verisi çıkarıldı: {len(prg_data)} byte")  # Debug
            
            # PRG dosyasından start_address ve code'u çıkar
            if len(prg_data) < 2:
                self.root.after(0, lambda: self.status_var.set("Geçersiz PRG verisi"))
                return
                
            start_address = prg_data[0] + (prg_data[1] << 8)
            code_data = prg_data[2:]
            
            print(f"Start address: ${start_address:04X}, Code size: {len(code_data)} bytes")  # Debug
            
            # Disassemble et
            disassembler = AdvancedDisassembler(
                start_address=start_address,
                code=code_data,
                use_py65=self.use_py65_disassembler.get(),
                use_illegal_opcodes=self.use_illegal_opcodes.get(),
                output_format=self.output_format.get()
            )
            
            if self.use_py65_disassembler.get():
                assembly_code = disassembler.disassemble_py65(prg_data)
            else:
                assembly_code = disassembler.disassemble_simple(prg_data)
            
            print(f"Assembly kod oluşturuldu: {len(assembly_code)} karakter")  # Debug
            
            # Tüm dillere çevir
            self.root.after(0, self._update_all_outputs, assembly_code, prg_data, start_address, code_data)
            
        except Exception as e:
            error_msg = str(e)
            print(f"_convert_single_file_thread hatası: {error_msg}")  # Debug
            self.root.after(0, lambda msg=error_msg: self.status_var.set(f"Hata: {msg}"))

    def _update_all_outputs(self, assembly_code, prg_data, start_address, code_data):
        """Tüm çıktı sekmelerini güncelle"""
        try:
            print(f"Assembly kod uzunluğu: {len(assembly_code)}")  # Debug
            
            # Assembly
            self.output_tabs['Assembly'].delete(1.0, tk.END)
            self.output_tabs['Assembly'].insert(tk.END, assembly_code)
            print("Assembly sekmesi güncellendi")  # Debug
            
            # Diğer formatlar için ImprovedDisassembler kullan
            for format_name, format_code in [('C', 'c'), ('QBasic', 'qbasic'), ('PDSX', 'pdsx'), 
                                           ('Pseudo', 'pseudo'), ('BASIC', 'commodorebasicv2')]:
                improved_disassembler = ImprovedDisassembler(
                    start_address=start_address,
                    code=code_data,
                    output_format=format_code
                )
                
                result_code = improved_disassembler.disassemble_to_format(prg_data)
                self.output_tabs[format_name].delete(1.0, tk.END)
                self.output_tabs[format_name].insert(tk.END, result_code)
                print(f"{format_name} kodu uzunluğu: {len(result_code)}")  # Debug
            
            self.status_var.set("Dönüştürme tamamlandı")
            print("Tüm sekmeler güncellendi")  # Debug
            
        except Exception as e:
            self.status_var.set(f"Çıktı güncelleme hatası: {str(e)}")
            print(f"_update_all_outputs hatası: {e}")  # Debug

    def extract_prg_data(self, entry):
        """PRG verisini çıkart"""
        try:
            disk_path = self.d64_path.get()
            if not disk_path:
                return None
            
            ext = Path(disk_path).suffix.lower()
            print(f"PRG çıkarma: {entry.get('filename')}, ext: {ext}")  # Debug
            
            # C1541 emülatörü ile dene
            try:
                disk_data, ext = enhanced_c1541_read_image(disk_path)
                if disk_data:
                    prg_data = enhanced_c1541_extract_prg(disk_data, ext, entry)
                    if prg_data:
                        print(f"C1541 ile PRG çıkarıldı: {len(prg_data)} byte")  # Debug
                        return prg_data
            except Exception as e:
                print(f"C1541 extract hatası: {e}")
            
            # Enhanced reader ile dene
            try:
                disk_data, ext = enhanced_read_image(disk_path)
                if disk_data:
                    prg_data = enhanced_extract_prg(disk_data, ext, entry)
                    if prg_data:
                        print(f"Enhanced reader ile PRG çıkarıldı: {len(prg_data)} byte")  # Debug
                        return prg_data
            except Exception as e:
                print(f"Enhanced extract hatası: {e}")
            
            # Basic reader ile dene
            try:
                disk_data, ext = read_image(disk_path)
                if disk_data:
                    if ext == '.t64':
                        # T64 için offset ve size parametreleri gerekli
                        if 'offset' in entry and 'size' in entry:
                            return extract_t64_prg(disk_data, entry['offset'], entry['size'])
                    elif ext == '.tap':
                        # TAP için offset ve size parametreleri gerekli
                        if 'offset' in entry and 'size' in entry:
                            return extract_tap_prg(disk_data, entry['offset'], entry['size'])
                    elif ext == '.p00':
                        return extract_p00_prg(disk_data)
                    else:
                        # D64/D71/D81/D84 için track/sector gerekli
                        if 'track' in entry and 'sector' in entry:
                            file_type = entry.get('file_type', entry.get('type', 'PRG'))
                            if 'SEQ' in file_type:
                                return extract_seq_file(disk_data, entry['track'], entry['sector'], ext)
                            elif 'USR' in file_type:
                                return extract_usr_file(disk_data, entry['track'], entry['sector'], ext)
                            elif 'DEL' in file_type:
                                return extract_del_file(disk_data, entry['track'], entry['sector'], ext)
                            else:
                                return extract_prg_file(disk_data, entry['track'], entry['sector'], ext)
            except Exception as e:
                print(f"Basic extract hatası: {e}")
            
            return None
            
        except Exception as e:
            print(f"PRG çıkarma hatası: {e}")
            return None

    # Dönüştürme fonksiyonları
    def convert_to_assembly(self):
        """Assembly'e dönüştür"""
        self.convert_to_specific_format('asm', 'Assembly')

    def convert_to_c(self):
        """C'ye dönüştür"""
        self.convert_to_specific_format('c', 'C')

    def convert_to_qbasic(self):
        """QBasic'e dönüştür"""
        self.convert_to_specific_format('qbasic', 'QBasic')

    def convert_to_pdsx(self):
        """PDSX'e dönüştür"""
        self.convert_to_specific_format('pdsx', 'PDSX')

    def convert_to_pseudo(self):
        """Pseudo koda dönüştür"""
        self.convert_to_specific_format('pseudo', 'Pseudo')

    def convert_to_basic(self):
        """BASIC'e dönüştür"""
        self.convert_to_specific_format('commodorebasicv2', 'BASIC')

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

    # Eski update_output_format metodları kaldırıldı - artık her format kendi metoduna sahip

def main():
    # TkinterDnD desteği varsa onu kullan
    if TkinterDnD:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    # Hata yakalama
    try:
        app = D64ConverterApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Kritik hata: {e}")
        import traceback
        traceback.print_exc()
        input("Devam etmek için Enter tuşuna basın...")

if __name__ == "__main__":
    main()
