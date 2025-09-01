# d64_converter.py
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from pathlib import Path
from d64_reader import (read_image, read_directory, read_t64_directory, read_tap_directory,
                       extract_prg_file, extract_t64_prg, extract_tap_prg, extract_p00_prg)
from advanced_disassembler import AdvancedDisassembler, Disassembler
from parser import CodeEmitter, parse_line, load_instruction_map
from c64_basic_parser import C64BasicParser
from sprite_converter import SpriteConverter
from sid_converter import SIDConverter
import logging

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
        
        # Sürükle-bırak desteği
        if TkinterDnD:
            self.setup_drag_drop()
    
    def setup_gui(self):
        """GUI bileşenlerini oluştur"""
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dosya seçimi
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)
        tk.Label(file_frame, text="D64/D71/D81/TAP Dosyası:").pack(side=tk.LEFT)
        tk.Entry(file_frame, textvariable=self.d64_path, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Dosya Seç", command=self.select_file).pack(side=tk.LEFT, padx=5)
        
        # Seçenekler
        options_frame = tk.Frame(main_frame)
        options_frame.pack(pady=5)
        
        tk.Checkbutton(options_frame, text="Illegal Opcode'ları Kullan", 
                      variable=self.use_illegal_opcodes,
                      command=self.update_disassembler).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(options_frame, text="py65 Disassembler (Eski)", 
                      variable=self.use_py65_disassembler,
                      command=self.update_disassembler).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(options_frame, text="Gelişmiş Disassembler", 
                      variable=self.use_advanced_disassembler,
                      command=self.update_disassembler).pack(side=tk.LEFT, padx=5)
        
        # Dosya listesi
        self.tree = ttk.Treeview(main_frame, columns=("Filename", "Track/Addr", "Sector/Offset", "Size"), show="headings")
        self.tree.heading("Filename", text="Dosya Adı")
        self.tree.heading("Track/Addr", text="Track/Addr")
        self.tree.heading("Sector/Offset", text="Sector/Offset")
        self.tree.heading("Size", text="Boyut")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Çıktı sekmeler
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Text widget'ları
        self.asm_text = tk.Text(self.notebook, wrap=tk.WORD, font=("Courier", 10))
        self.c_text = tk.Text(self.notebook, wrap=tk.WORD, font=("Courier", 10))
        self.qbasic_text = tk.Text(self.notebook, wrap=tk.WORD, font=("Courier", 10))
        self.pdsx_text = tk.Text(self.notebook, wrap=tk.WORD, font=("Courier", 10))
        self.commodore_text = tk.Text(self.notebook, wrap=tk.WORD, font=("Courier", 10))
        self.pseudo_text = tk.Text(self.notebook, wrap=tk.WORD, font=("Courier", 10))
        self.basic_text = tk.Text(self.notebook, wrap=tk.WORD, font=("Courier", 10))
        
        # Sekmeleri ekle
        self.notebook.add(self.asm_text, text="Assembly")
        self.notebook.add(self.c_text, text="C")
        self.notebook.add(self.qbasic_text, text="QBasic")
        self.notebook.add(self.pdsx_text, text="PDSX")
        self.notebook.add(self.commodore_text, text="Commodore BASIC V2")
        self.notebook.add(self.pseudo_text, text="Pseudo-Code")
        self.notebook.add(self.basic_text, text="C64 BASIC")
        
        # Butonlar
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=5)
        
        # İlk satır
        button_row1 = tk.Frame(button_frame)
        button_row1.pack(pady=2)
        tk.Button(button_row1, text="Disk İçeriğini Yenile", 
                 command=self.refresh_disk_content, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_row1, text="Seçili Dosyaları Çevir", 
                 command=self.convert_selected_files, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_row1, text="Tümünü Çevir", 
                 command=self.convert_all_files, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        
        # İkinci satır
        button_row2 = tk.Frame(button_frame)
        button_row2.pack(pady=2)
        tk.Button(button_row2, text="Assembly'yi Kaydet", 
                 command=self.save_assembly, bg="#9C27B0", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_row2, text="C Kodunu Kaydet", 
                 command=self.save_c_code, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_row2, text="Tümünü Kaydet", 
                 command=self.save_all_outputs, bg="#795548", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_frame = tk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=5)
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır - Disk dosyası seçin")
        tk.Label(self.status_frame, textvariable=self.status_var, 
                relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)
        
        # Event bindings
        self.tree.bind("<Double-1>", self.on_file_double_click)
        
        # Tema
        self.root.configure(bg="#2E2E2E")
        style = ttk.Style()
        style.configure("Treeview", background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E")
        style.configure("Treeview.Heading", background="#4A4A4A", foreground="white")
    
    def setup_logging(self):
        """Logging'i ayarla"""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    def setup_drag_drop(self):
        """Sürükle-bırak özelliğini ayarla"""
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind('<<Drop>>', self.on_drop)
    
    def on_drop(self, event):
        """Sürükle-bırak olayını işle"""
        files = self.tree.tk.splitlist(event.data)
        for file_path in files:
            if file_path.lower().endswith(('.d64', '.d71', '.d81', '.d84', '.tap', '.t64', '.p00')):
                self.d64_path.set(file_path)
                self.load_image(file_path)
                break
    
    def update_disassembler(self):
        """Disassembler ayarlarını güncelle"""
        logging.info(f"Disassembler güncellendi: Advanced={self.use_advanced_disassembler.get()}, py65={self.use_py65_disassembler.get()}, Illegal={self.use_illegal_opcodes.get()}")
    
    def select_file(self):
        """Dosya seç"""
        file_path = filedialog.askopenfilename(
            filetypes=[("C64 Files", "*.d64 *.d71 *.d81 *.d84 *.tap *.t64 *.p00")]
        )
        if file_path:
            self.d64_path.set(file_path)
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """Disk imajını yükle"""
        try:
            self.status_var.set("Disk dosyası yükleniyor...")
            disk_data, ext = read_image(file_path)
            
            if ext in (".d64", ".d71", ".d81", ".d84"):
                self.entries = read_directory(disk_data, ext)
            elif ext == ".t64":
                self.entries = read_t64_directory(disk_data)
            elif ext == ".tap":
                self.entries = read_tap_directory(disk_data)
            else:
                self.entries = []
            
            self.update_file_list()
            self.status_var.set(f"Disk yüklendi: {len(self.entries)} dosya bulundu")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Disk yüklenirken hata: {e}")
            self.status_var.set("Hata!")
    
    def update_file_list(self):
        """Dosya listesini güncelle"""
        # Eski verileri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Yeni verileri ekle
        for entry in self.entries:
            self.tree.insert("", "end", values=(
                entry["filename"],
                entry.get("track", entry.get("address", "N/A")),
                entry.get("sector", entry.get("offset", "N/A")),
                entry.get("size", "N/A")
            ))
    
    def on_file_double_click(self, event):
        """Dosyaya çift tıklandığında"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            filename = item["values"][0]
            
            # Dosyayı bul
            entry = next((e for e in self.entries if e["filename"] == filename), None)
            if entry:
                self.convert_single_file(entry)
    
    def convert_single_file(self, entry):
        """Tek dosyayı çevir"""
        try:
            self.status_var.set(f"Çeviriliyor: {entry['filename']}")
            
            # PRG verisini çıkar
            disk_data, ext = read_image(self.d64_path.get())
            
            if ext in (".d64", ".d71", ".d81", ".d84"):
                prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
            elif ext == ".t64":
                prg_data = extract_t64_prg(disk_data, entry["offset"], entry.get("size", 1000))
            elif ext == ".tap":
                prg_data = extract_tap_prg(disk_data, entry["offset"], entry.get("size", 1000))
            else:
                prg_data = disk_data[entry["offset"]:]
            
            if not prg_data or len(prg_data) < 2:
                messagebox.showerror("Hata", "PRG verisi okunamadı")
                return
            
            # BASIC mı kontrol et
            is_basic = self.is_basic_program(prg_data)
            
            if is_basic:
                self.convert_basic_program(prg_data, entry["filename"])
            else:
                self.convert_assembly_program(prg_data, entry["filename"])
            
            self.status_var.set(f"Çevirildi: {entry['filename']}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Çevirme hatası: {e}")
            self.status_var.set("Hata!")
    
    def is_basic_program(self, prg_data):
        """BASIC program mı kontrol et"""
        if len(prg_data) < 4:
            return False
        
        # BASIC programlar genellikle $0801'de başlar
        start_addr = prg_data[0] + (prg_data[1] << 8)
        return start_addr == 0x0801
    
    def convert_basic_program(self, prg_data, filename):
        """BASIC programı çevir"""
        try:
            # BASIC detokenize
            basic_lines = self.basic_parser.detokenize(prg_data)
            
            # Sonuçları göster
            self.asm_text.delete(1.0, tk.END)
            self.asm_text.insert(tk.END, "BASIC Program - Assembly N/A")
            
            # BASIC
            self.basic_text.delete(1.0, tk.END)
            self.basic_text.insert(tk.END, "\n".join(basic_lines))
            
            # Çeviriler
            self.c_text.delete(1.0, tk.END)
            self.c_text.insert(tk.END, self.basic_parser.transpile(basic_lines, "c"))
            
            self.qbasic_text.delete(1.0, tk.END)
            self.qbasic_text.insert(tk.END, self.basic_parser.transpile(basic_lines, "qbasic"))
            
            self.pdsx_text.delete(1.0, tk.END)
            self.pdsx_text.insert(tk.END, self.basic_parser.transpile(basic_lines, "pdsx"))
            
            self.commodore_text.delete(1.0, tk.END)
            self.commodore_text.insert(tk.END, "\n".join(basic_lines))
            
            self.pseudo_text.delete(1.0, tk.END)
            self.pseudo_text.insert(tk.END, "BASIC Program - Pseudo-code N/A")
            
        except Exception as e:
            messagebox.showerror("Hata", f"BASIC çeviri hatası: {e}")
    
    def convert_assembly_program(self, prg_data, filename):
        """Assembly programı çevir"""
        try:
            # Start address
            start_addr = prg_data[0] + (prg_data[1] << 8)
            code_data = prg_data[2:]
            
            # Disassembler seç
            if self.use_advanced_disassembler.get():
                disasm = AdvancedDisassembler(start_addr, code_data, 
                                            use_py65=self.use_py65_disassembler.get())
            else:
                disasm = Disassembler(start_addr, code_data)
            
            # Disassemble
            asm_lines = disasm.disassemble()
            
            # Assembly'yi göster
            self.asm_text.delete(1.0, tk.END)
            self.asm_text.insert(tk.END, "\n".join(asm_lines))
            
            # BASIC boş
            self.basic_text.delete(1.0, tk.END)
            self.basic_text.insert(tk.END, "Assembly Program - BASIC N/A")
            
            # Çeviriler (sadece gelişmiş disassembler'da)
            if self.use_advanced_disassembler.get() and hasattr(disasm, 'to_c'):
                self.c_text.delete(1.0, tk.END)
                self.c_text.insert(tk.END, "\n".join(disasm.to_c(asm_lines)))
                
                self.qbasic_text.delete(1.0, tk.END)
                self.qbasic_text.insert(tk.END, "\n".join(disasm.to_qbasic(asm_lines)))
                
                self.pdsx_text.delete(1.0, tk.END)
                self.pdsx_text.insert(tk.END, "\n".join(disasm.to_pdsx(asm_lines)))
                
                self.commodore_text.delete(1.0, tk.END)
                self.commodore_text.insert(tk.END, "\n".join(disasm.to_commodore_basic_v2(asm_lines)))
                
                self.pseudo_text.delete(1.0, tk.END)
                self.pseudo_text.insert(tk.END, "\n".join(disasm.to_pseudo(asm_lines)))
            else:
                # Basit çeviriler
                self.c_text.delete(1.0, tk.END)
                self.c_text.insert(tk.END, "// Assembly program - C çevirisi için gelişmiş disassembler kullanın")
                
                self.qbasic_text.delete(1.0, tk.END)
                self.qbasic_text.insert(tk.END, "' Assembly program - QBasic çevirisi için gelişmiş disassembler kullanın")
                
                self.pdsx_text.delete(1.0, tk.END)
                self.pdsx_text.insert(tk.END, "// Assembly program - PDSX çevirisi için gelişmiş disassembler kullanın")
                
                self.commodore_text.delete(1.0, tk.END)
                self.commodore_text.insert(tk.END, "REM Assembly program - Commodore BASIC çevirisi için gelişmiş disassembler kullanın")
                
                self.pseudo_text.delete(1.0, tk.END)
                self.pseudo_text.insert(tk.END, "// Assembly program - Pseudo-code çevirisi için gelişmiş disassembler kullanın")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Assembly çeviri hatası: {e}")
    
    def refresh_disk_content(self):
        """Disk içeriğini yenile"""
        if self.d64_path.get():
            self.load_image(self.d64_path.get())
        else:
            messagebox.showwarning("Uyarı", "Önce bir disk dosyası seçin!")
    
    def convert_selected_files(self):
        """Seçili dosyaları çevir"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Dosya seçin!")
            return
        
        # İlk seçili dosyayı çevir
        item = self.tree.item(selection[0])
        filename = item["values"][0]
        entry = next((e for e in self.entries if e["filename"] == filename), None)
        if entry:
            self.convert_single_file(entry)
    
    def convert_all_files(self):
        """Tüm dosyaları çevir"""
        if not self.entries:
            messagebox.showwarning("Uyarı", "Dosya bulunamadı!")
            return
        
        # İlk dosyayı çevir (örnek)
        self.convert_single_file(self.entries[0])
    
    def save_assembly(self):
        """Assembly kodunu kaydet"""
        content = self.asm_text.get(1.0, tk.END)
        if content.strip():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".asm",
                filetypes=[("Assembly files", "*.asm"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(content)
                self.status_var.set(f"Assembly kaydedildi: {file_path}")
    
    def save_c_code(self):
        """C kodunu kaydet"""
        content = self.c_text.get(1.0, tk.END)
        if content.strip():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".c",
                filetypes=[("C files", "*.c"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(content)
                self.status_var.set(f"C kodu kaydedildi: {file_path}")
    
    def save_all_outputs(self):
        """Tüm çıktıları kaydet"""
        directory = filedialog.askdirectory()
        if directory:
            try:
                # Assembly
                asm_content = self.asm_text.get(1.0, tk.END)
                if asm_content.strip():
                    with open(os.path.join(directory, "output.asm"), 'w') as f:
                        f.write(asm_content)
                
                # C
                c_content = self.c_text.get(1.0, tk.END)
                if c_content.strip():
                    with open(os.path.join(directory, "output.c"), 'w') as f:
                        f.write(c_content)
                
                # QBasic
                qbasic_content = self.qbasic_text.get(1.0, tk.END)
                if qbasic_content.strip():
                    with open(os.path.join(directory, "output.qbasic"), 'w') as f:
                        f.write(qbasic_content)
                
                # PDSX
                pdsx_content = self.pdsx_text.get(1.0, tk.END)
                if pdsx_content.strip():
                    with open(os.path.join(directory, "output.pdsx"), 'w') as f:
                        f.write(pdsx_content)
                
                # Commodore BASIC
                commodore_content = self.commodore_text.get(1.0, tk.END)
                if commodore_content.strip():
                    with open(os.path.join(directory, "output.commodore.bas"), 'w') as f:
                        f.write(commodore_content)
                
                # Pseudo
                pseudo_content = self.pseudo_text.get(1.0, tk.END)
                if pseudo_content.strip():
                    with open(os.path.join(directory, "output.pseudo"), 'w') as f:
                        f.write(pseudo_content)
                
                # BASIC
                basic_content = self.basic_text.get(1.0, tk.END)
                if basic_content.strip():
                    with open(os.path.join(directory, "output.basic"), 'w') as f:
                        f.write(basic_content)
                
                self.status_var.set(f"Tüm çıktılar kaydedildi: {directory}")
                
            except Exception as e:
                messagebox.showerror("Hata", f"Kaydetme hatası: {e}")

def main():
    root = tk.Tk()
    app = D64ConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
