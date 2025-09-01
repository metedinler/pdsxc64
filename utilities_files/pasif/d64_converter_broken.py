# d64_converter.py
import tkinter as tk
from tkinter i        # Options frame
        options_frame = tk.Frame(main_frame)
        options_frame.pack(pady=5)
        
        # Illegal Opcode Checkbox
        tk.Checkbutton(options_frame, text="Illegal Opcode'ları Kullan", variable=self.use_illegal_opcodes,
                       command=self.update_disassembler).pack(side=tk.LEFT, padx=5)
        
        # py65 Disassembler Checkbox
        tk.Checkbutton(options_frame, text="py65 Disassembler (Eski)", variable=self.use_py65_disassembler,
                       command=self.update_disassembler).pack(side=tk.LEFT, padx=5)rt filedialog, ttk, messagebox
import os
from pathlib import Path
from d64_reader import (read_image, read_directory, read_t64_directory, read_tap_directory,
                       extract_prg_file, extract_t64_prg, extract_tap_prg, extract_p00_prg)
from disassembler import Disassembler
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

# Logging yapılandırması
logging.basicConfig(filename='logs/d64_converter.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class D64ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("D64 to Pseudo/pdsX/QBasic64/C Converter")
        self.root.geometry("1200x800")
        
        self.d64_path = tk.StringVar()
        self.use_illegal_opcodes = tk.BooleanVar(value=False)
        self.use_py65_disassembler = tk.BooleanVar(value=False)  # py65 seçeneği
        self.entries = []
        self.disassembler = None  # Disassembler'ı dinamik olarak oluşturacağız
        self.basic_parser = C64BasicParser()
        self.sprite_converter = SpriteConverter()
        self.sid_converter = SIDConverter()
        self.selected_files = []

        # Sürükle-bırak
        if TkinterDnD:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.handle_drop)

        # Ana Çerçeve
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dosya Seçici
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X)
        tk.Label(file_frame, text="Dosya (D64/D71/D81/D84/TAP/T64/P00):").pack(side=tk.LEFT)
        tk.Entry(file_frame, textvariable=self.d64_path, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(file_frame, text="Dosya Seç", command=self.select_file).pack(side=tk.LEFT, padx=5)

        # Illegal Opcode Checkbox
        tk.Checkbutton(main_frame, text="Illegal Opcode’ları Kullan", variable=self.use_illegal_opcodes,
                       command=self.update_disassembler).pack(pady=5)

        # Dosya Listesi
        self.tree = ttk.Treeview(main_frame, columns=("Filename", "Track/Addr", "Sector/Offset", "Size"), show="headings")
        self.tree.heading("Filename", text="Dosya Adı")
        self.tree.heading("Track/Addr", text="Track/Addr")
        self.tree.heading("Sector/Offset", text="Sector/Offset")
        self.tree.heading("Size", text="Boyut (Blok)")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_file_select)
        self.tree.configure(selectmode="extended")

        # Çıktı Sekmeleri
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        self.asm_text = tk.Text(self.notebook, wrap=tk.WORD, height=15)
        self.pseudo_text = tk.Text(self.notebook, wrap=tk.WORD, height=15)
        self.pdsx_text = tk.Text(self.notebook, wrap=tk.WORD, height=15)
        self.qbasic_text = tk.Text(self.notebook, wrap=tk.WORD, height=15)
        self.c_text = tk.Text(self.notebook, wrap=tk.WORD, height=15)
        self.basic_text = tk.Text(self.notebook, wrap=tk.WORD, height=15)

        self.notebook.add(self.asm_text, text="Assembly")
        self.notebook.add(self.pseudo_text, text="Pseudo-Code")
        self.notebook.add(self.pdsx_text, text="pdsX BASIC")
        self.notebook.add(self.qbasic_text, text="QBasic64")
        self.notebook.add(self.c_text, text="C")
        self.notebook.add(self.basic_text, text="C64 BASIC")

        # Düğmeler
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=5)
        
        # İlk satır - Ana işlevler
        button_row1 = tk.Frame(button_frame)
        button_row1.pack(pady=2)
        tk.Button(button_row1, text="Disk İçeriğini Yenile", command=self.refresh_disk_content, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_row1, text="Seçili Dosyaları Çevir", command=self.convert_selected_files, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_row1, text="Tümünü Çevir", command=self.convert_all_files, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        
        # İkinci satır - Kaydetme ve çıkarma işlevleri  
        button_row2 = tk.Frame(button_frame)
        button_row2.pack(pady=2)
        tk.Button(button_row2, text="Çıktıları Kaydet", command=self.save_outputs).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row2, text="Sprite PNG Çıkar", command=self.extract_sprites).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row2, text="SID Çıkar", command=self.extract_sid).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row2, text="Hata Logunu Göster", command=self.show_log).pack(side=tk.LEFT, padx=5)

        # Status Bar
        self.status_frame = tk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=5)
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır - Disk dosyası seçin")
        tk.Label(self.status_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)

        # Tema
        self.root.configure(bg="#2E2E2E")
        style = ttk.Style()
        style.configure("Treeview", background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E")
        style.configure("Treeview.Heading", background="#4A4A4A", foreground="white")

    def refresh_disk_content(self):
        """Disk içeriğini yenile ve BAM bilgilerini göster"""
        if not self.d64_path.get():
            messagebox.showwarning("Uyarı", "Önce bir disk dosyası seçin!")
            return
            
        try:
            self.load_image(self.d64_path.get())
            messagebox.showinfo("Başarılı", f"Disk içeriği yenilendi. {len(self.entries)} dosya bulundu.")
            logging.info(f"Disk içeriği yenilendi: {len(self.entries)} dosya")
        except Exception as e:
            messagebox.showerror("Hata", f"Disk içeriği yenilenemedi: {e}")
            logging.error(f"Disk yenileme hatası: {e}")

    def convert_selected_files(self):
        """Seçili dosyaları çevir"""
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Çevirmek için dosya(lar) seçin!")
            return
            
        try:
            # Seçili dosyalar için otomatik çeviri yap
            converted_count = 0
            for index in self.selected_files:
                entry = self.entries[index]
                self.process_single_file(entry)
                converted_count += 1
                
            messagebox.showinfo("Başarılı", f"{converted_count} dosya başarıyla çevrildi!")
            logging.info(f"{converted_count} dosya çevrildi")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya çevirme hatası: {e}")
            logging.error(f"Çevirme hatası: {e}")

    def convert_all_files(self):
        """Tüm .PRG dosyalarını çevir"""
        if not self.entries:
            messagebox.showwarning("Uyarı", "Çevirmek için önce disk yükleyin!")
            return
            
        # Onay al
        if not messagebox.askyesno("Onay", f"{len(self.entries)} dosyayı çevirmek istediğinizden emin misiniz?"):
            return
            
        try:
            # Tüm dosyalar için otomatik çeviri yap
            converted_count = 0
            for entry in self.entries:
                self.process_single_file(entry)
                converted_count += 1
                
            messagebox.showinfo("Başarılı", f"{converted_count} dosya başarıyla çevrildi!")
            logging.info(f"Tüm dosyalar çevrildi: {converted_count}")
        except Exception as e:
            messagebox.showerror("Hata", f"Toplu çevirme hatası: {e}")
            logging.error(f"Toplu çevirme hatası: {e}")

    def process_single_file(self, entry):
        """Tek dosyayı işle ve çevir"""
        try:
            disk_data, ext = read_image(self.d64_path.get())
            if ext in (".d64", ".d71", ".d81", ".d84"):
                prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
            elif ext == ".t64":
                prg_data = extract_t64_prg(disk_data, entry["offset"], entry.get("size", 1000))
            elif ext == ".tap":
                prg_data = extract_tap_prg(disk_data, entry["offset"], entry["size"])
            elif ext == ".p00":
                prg_data = extract_p00_prg(disk_data)
            else:
                raise ValueError("Desteklenmeyen dosya formatı")

            # C64 BASIC kontrolü
            is_basic = len(prg_data) > 4 and prg_data[2] == 0xA9 and prg_data[4] == 0x8D
            
            if is_basic:
                # BASIC dosyası işleme
                basic_lines = self.basic_parser.detokenize(prg_data)
                self.basic_text.delete(1.0, tk.END)
                self.basic_text.insert(tk.END, "\n".join(basic_lines) if basic_lines else "Hata: C64 BASIC çevrilemedi")

                # pdsX çevirisi
                pdsx_output = self.basic_parser.transpile(basic_lines, "pdsx")
                self.pdsx_text.delete(1.0, tk.END)
                self.pdsx_text.insert(tk.END, pdsx_output or "Hata: pdsX çevrilemedi")

                # QBasic64 çevirisi
                qbasic_output = self.basic_parser.transpile(basic_lines, "qbasic")
                self.qbasic_text.delete(1.0, tk.END)
                self.qbasic_text.insert(tk.END, qbasic_output or "Hata: QBasic64 çevrilemedi")

                # C çevirisi
                c_output = self.basic_parser.transpile(basic_lines, "c")
                self.c_text.delete(1.0, tk.END)
                self.c_text.insert(tk.END, c_output or "Hata: C çevrilemedi")

                # Assembly ve Pseudo boş
                self.asm_text.delete(1.0, tk.END)
                self.asm_text.insert(tk.END, "C64 BASIC programı, assembly kullanılmadı")
                self.pseudo_text.delete(1.0, tk.END)
                self.pseudo_text.insert(tk.END, "C64 BASIC programı, pseudo-kod kullanılmadı")
            else:
                # Assembly dosyası işleme
                if len(prg_data) >= 2:
                    start_addr = prg_data[0] + (prg_data[1] << 8)
                    code_data = prg_data[2:]
                    disasm = Disassembler(start_addr, code_data)
                    asm_lines = disasm.disassemble()
                else:
                    asm_lines = ["Hata: PRG dosyası çok küçük"]
                
                self.asm_text.delete(1.0, tk.END)
                self.asm_text.insert(tk.END, "\n".join(asm_lines) if asm_lines else "Hata: Disassemble edilemedi")

                # Pseudo-Code çevirisi
                pseudo_emitter = CodeEmitter("pseudo", self.use_illegal_opcodes.get())
                for i, line in enumerate(asm_lines):
                    parsed = parse_line(line)
                    if parsed:
                        pseudo_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                self.pseudo_text.delete(1.0, tk.END)
                self.pseudo_text.insert(tk.END, pseudo_emitter.get_output() or "Hata: Pseudo-kod çevrilemedi")

                # pdsX çevirisi
                pdsx_emitter = CodeEmitter("pdsx", self.use_illegal_opcodes.get())
                for i, line in enumerate(asm_lines):
                    parsed = parse_line(line)
                    if parsed:
                        pdsx_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                self.pdsx_text.delete(1.0, tk.END)
                self.pdsx_text.insert(tk.END, pdsx_emitter.get_output() or "Hata: pdsX çevrilemedi")

                # QBasic64 çevirisi
                qbasic_emitter = CodeEmitter("qbasic", self.use_illegal_opcodes.get())
                for i, line in enumerate(asm_lines):
                    parsed = parse_line(line)
                    if parsed:
                        qbasic_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                self.qbasic_text.delete(1.0, tk.END)
                self.qbasic_text.insert(tk.END, qbasic_emitter.get_output() or "Hata: QBasic64 çevrilemedi")

                # C çevirisi
                c_emitter = CodeEmitter("c", self.use_illegal_opcodes.get())
                for i, line in enumerate(asm_lines):
                    parsed = parse_line(line)
                    if parsed:
                        c_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                c_lines = [
                    "#include <stdio.h>",
                    "void main() {",
                    "    unsigned char a, x, y, carry, overflow, decimal;",
                    "    unsigned char *screen_mem = (unsigned char*)0x0400;",
                    "    unsigned char *color_ram = (unsigned char*)0xD800;",
                    "    unsigned char *basic_rom = (unsigned char*)0xA000;",
                    "    unsigned char *kernal_rom = (unsigned char*)0xE000;",
                    ""
                ] + c_emitter.get_output().splitlines() + ["}"]
                self.c_text.delete(1.0, tk.END)
                self.c_text.insert(tk.END, "\n".join(c_lines))

                # C64 BASIC sekmesi boş
                self.basic_text.delete(1.0, tk.END)
                self.basic_text.insert(tk.END, "Assembly programı, C64 BASIC kullanılmadı")

            logging.info(f"Dosya işlendi: {entry['filename']}")
            
        except Exception as e:
            logging.error(f"Dosya işleme hatası ({entry['filename']}): {e}")
            raise e

    def handle_drop(self, event):
        file_path = event.data
        if file_path.endswith((".d64", ".d71", ".d81", ".d84", ".tap", ".t64", ".p00")):
            self.d64_path.set(file_path)
            self.load_image(file_path)
        else:
            messagebox.showwarning("Uyarı", "Desteklenen formatlar: .d64, .d71, .d81, .d84, .tap, .t64, .p00")
            logging.warning(f"Geçersiz dosya sürükle-bırak: {file_path}")

    def update_disassembler(self):
        # Disassembler'ı güncelle - şimdilik illegal opcodes kullanmıyoruz
        logging.info("Disassembler güncellendi: Illegal opcodes = %s", self.use_illegal_opcodes.get())

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("C64 Files", "*.d64 *.d71 *.d81 *.d84 *.tap *.t64 *.p00")])
        if file_path:
            self.d64_path.set(file_path)
            self.load_image(file_path)

    def load_image(self, file_path):
        try:
            self.status_var.set("Disk yükleniyor...")
            disk_data, ext = read_image(file_path)
            if ext in (".d64", ".d71", ".d81", ".d84"):
                self.entries = read_directory(disk_data, ext)
                self.tree.delete(*self.tree.get_children())
                for entry in self.entries:
                    self.tree.insert("", tk.END, values=(
                        entry["filename"],
                        entry["track"],
                        entry["sector"],
                        entry["size_blocks"]
                    ))
                self.status_var.set(f"{ext.upper()} yüklendi: {len(self.entries)} dosya - Directory Track/Sector okundu")
            elif ext == ".t64":
                self.entries = read_t64_directory(disk_data)
                self.tree.delete(*self.tree.get_children())
                for entry in self.entries:
                    self.tree.insert("", tk.END, values=(
                        entry["filename"],
                        f"${entry['start_addr']:04X}",
                        entry["offset"],
                        entry.get("size", "-")
                    ))
                self.status_var.set(f"T64 yüklendi: {len(self.entries)} dosya")
            elif ext == ".tap":
                self.entries = read_tap_directory(disk_data)
                self.tree.delete(*self.tree.get_children())
                for entry in self.entries:
                    self.tree.insert("", tk.END, values=(
                        entry["filename"],
                        entry.get("type", "TAP"),
                        entry["offset"],
                        entry["size"]
                    ))
                self.status_var.set(f"TAP yüklendi: {len(self.entries)} program")
            elif ext == ".p00":
                filename = Path(file_path).stem
                self.entries = [{"filename": filename, "offset": 26, "type": "P00"}]
                self.tree.delete(*self.tree.get_children())
                for entry in self.entries:
                    self.tree.insert("", tk.END, values=(
                        entry["filename"],
                        entry["type"],
                        entry["offset"],
                        "-"
                    ))
                self.status_var.set("P00 dosyası yüklendi")
            logging.info(f"Dosya yüklendi: {file_path}")
        except Exception as e:
            logging.error(f"Dosya yükleme hatası: {e}")
            self.status_var.set(f"Hata: {e}")
            messagebox.showerror("Hata", f"Dosya yüklenemedi: {e}")

    def on_file_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        self.selected_files = [self.tree.index(item) for item in selected]
        
        self.status_var.set(f"{len(self.selected_files)} dosya seçildi - Çeviriliyor...")
        
        index = self.selected_files[0]
        entry = self.entries[index]
        
        try:
            disk_data, ext = read_image(self.d64_path.get())
            if ext in (".d64", ".d71", ".d81", ".d84"):
                prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
            elif ext == ".t64":
                prg_data = extract_t64_prg(disk_data, entry["offset"], entry.get("size", 1000))
            elif ext == ".tap":
                prg_data = extract_tap_prg(disk_data, entry["offset"], entry["size"])
            elif ext == ".p00":
                prg_data = extract_p00_prg(disk_data)
            else:
                raise ValueError("Desteklenmeyen dosya formatı")

            # C64 BASIC kontrolü
            is_basic = len(prg_data) > 4 and prg_data[2] == 0xA9 and prg_data[4] == 0x8D
            if is_basic:
                basic_lines = self.basic_parser.detokenize(prg_data)
                self.basic_text.delete(1.0, tk.END)
                self.basic_text.insert(tk.END, "\n".join(basic_lines) if basic_lines else "Hata: C64 BASIC çevrilemedi")
                self.current_basic_output = "\n".join(basic_lines)

                # pdsX
                pdsx_output = self.basic_parser.transpile(basic_lines, "pdsx")
                self.pdsx_text.delete(1.0, tk.END)
                self.pdsx_text.insert(tk.END, pdsx_output or "Hata: pdsX çevrilemedi")
                self.current_pdsx_output = pdsx_output

                # QBasic64
                qbasic_output = self.basic_parser.transpile(basic_lines, "qbasic")
                self.qbasic_text.delete(1.0, tk.END)
                self.qbasic_text.insert(tk.END, qbasic_output or "Hata: QBasic64 çevrilemedi")
                self.current_qbasic_output = qbasic_output

                # C
                c_output = self.basic_parser.transpile(basic_lines, "c")
                self.c_text.delete(1.0, tk.END)
                self.c_text.insert(tk.END, c_output or "Hata: C çevrilemedi")
                self.current_c_output = c_output

                # Assembly ve Pseudo boş bırakılır
                self.asm_text.delete(1.0, tk.END)
                self.asm_text.insert(tk.END, "C64 BASIC programı, assembly kullanılmadı")
                self.pseudo_text.delete(1.0, tk.END)
                self.pseudo_text.insert(tk.END, "C64 BASIC programı, pseudo-kod kullanılmadı")
                
                self.status_var.set(f"C64 BASIC dosyası çevrildi: {entry['filename']}")
            else:
                # Assembly
                if len(prg_data) >= 2:
                    start_addr = prg_data[0] + (prg_data[1] << 8)
                    code_data = prg_data[2:]
                    disasm = Disassembler(start_addr, code_data)
                    asm_lines = disasm.disassemble()
                else:
                    asm_lines = ["Hata: PRG dosyası çok küçük"]
                
                self.asm_text.delete(1.0, tk.END)
                self.asm_text.insert(tk.END, "\n".join(asm_lines) if asm_lines else "Hata: Disassemble edilemedi")
                self.current_asm_lines = asm_lines

                # Pseudo-Code
                pseudo_emitter = CodeEmitter("pseudo", self.use_illegal_opcodes.get())
                for i, line in enumerate(asm_lines):
                    parsed = parse_line(line)
                    if parsed:
                        pseudo_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                self.pseudo_text.delete(1.0, tk.END)
                self.pseudo_text.insert(tk.END, pseudo_emitter.get_output() or "Hata: Pseudo-kod çevrilemedi")
                self.current_pseudo_output = pseudo_emitter.get_output()

                # pdsX
                pdsx_emitter = CodeEmitter("pdsx", self.use_illegal_opcodes.get())
                for i, line in enumerate(asm_lines):
                    parsed = parse_line(line)
                    if parsed:
                        pdsx_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                self.pdsx_text.delete(1.0, tk.END)
                self.pdsx_text.insert(tk.END, pdsx_emitter.get_output() or "Hata: pdsX çevrilemedi")
                self.current_pdsx_output = pdsx_emitter.get_output()

                # QBasic64
                qbasic_emitter = CodeEmitter("qbasic", self.use_illegal_opcodes.get())
                for i, line in enumerate(asm_lines):
                    parsed = parse_line(line)
                    if parsed:
                        qbasic_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                self.qbasic_text.delete(1.0, tk.END)
                self.qbasic_text.insert(tk.END, qbasic_emitter.get_output() or "Hata: QBasic64 çevrilemedi")
                self.current_qbasic_output = qbasic_emitter.get_output()

                # C
                c_emitter = CodeEmitter("c", self.use_illegal_opcodes.get())
                for i, line in enumerate(asm_lines):
                    parsed = parse_line(line)
                    if parsed:
                        c_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                c_lines = [
                    "#include <stdio.h>",
                    "void main() {",
                    "    unsigned char a, x, y, carry, overflow, decimal;",
                    "    unsigned char *screen_mem = (unsigned char*)0x0400;",
                    "    unsigned char *color_ram = (unsigned char*)0xD800;",
                    "    unsigned char *basic_rom = (unsigned char*)0xA000;",
                    "    unsigned char *kernal_rom = (unsigned char*)0xE000;",
                    ""
                ] + c_emitter.get_output().splitlines() + ["}"]
                self.c_text.delete(1.0, tk.END)
                self.c_text.insert(tk.END, "\n".join(c_lines))
                self.current_c_output = "\n".join(c_lines)

                # C64 BASIC sekmesi boş
                self.basic_text.delete(1.0, tk.END)
                self.basic_text.insert(tk.END, "Assembly programı, C64 BASIC kullanılmadı")

                self.status_var.set(f"Assembly dosyası çevrildi: {entry['filename']} ({len(asm_lines)} satır)")

            self.current_filename = entry["filename"]
            logging.info(f"Dosya işlendi: {entry['filename']}")
        except Exception as e:
            logging.error(f"Dosya işleme hatası: {e}")
            self.status_var.set(f"Hata: {e}")
            messagebox.showerror("Hata", f"Dosya işlenemedi: {e}")

    def extract_sprites(self):
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Önce dosya(lar) seçin!")
            return
        output_dir = filedialog.askdirectory()
        if output_dir:
            try:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                for index in self.selected_files:
                    entry = self.entries[index]
                    disk_data, ext = read_image(self.d64_path.get())
                    if ext in (".d64", ".d81"):
                        prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
                    elif ext == ".t64":
                        prg_data = extract_t64_prg(disk_data, entry["offset"], 1000)
                    else:
                        prg_data = disk_data[entry["offset"]:]
                    # Örnek sprite verisi (basitçe son 64 bayt)
                    sprite_data = prg_data[-64:]
                    self.sprite_converter.convert_sprite(sprite_data, os.path.join(output_dir, f"{entry['filename']}_sprite.png"))
                messagebox.showinfo("Başarılı", "Sprite’lar PNG’ye çevrildi!")
                logging.info(f"Sprite’lar PNG’ye çevrildi: {output_dir}")
            except Exception as e:
                logging.error(f"Sprite çıkarma hatası: {e}")
                messagebox.showerror("Hata", f"Sprite çıkarma başarısız: {e}")

    def extract_sid(self):
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Önce dosya(lar) seçin!")
            return
        output_dir = filedialog.askdirectory()
        if output_dir:
            try:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                for index in self.selected_files:
                    entry = self.entries[index]
                    disk_data, ext = read_image(self.d64_path.get())
                    if ext in (".d64", ".d81"):
                        prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
                    elif ext == ".t64":
                        prg_data = extract_t64_prg(disk_data, entry["offset"], 1000)
                    else:
                        prg_data = disk_data[entry["offset"]:]
                    # Örnek SID verisi (basitçe son 1000 bayt)
                    sid_data = prg_data[-1000:]
                    self.sid_converter.convert_to_sid(sid_data, os.path.join(output_dir, f"{entry['filename']}.sid"))
                messagebox.showinfo("Başarılı", "SID dosyaları oluşturuldu!")
                logging.info(f"SID dosyaları oluşturuldu: {output_dir}")
            except Exception as e:
                logging.error(f"SID çıkarma hatası: {e}")
                messagebox.showerror("Hata", f"SID çıkarma başarısız: {e}")

    def save_outputs(self):
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Önce dosya(lar) seçin!")
            return
        output_dir = filedialog.askdirectory()
        if output_dir:
            try:
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                for index in self.selected_files:
                    entry = self.entries[index]
                    disk_data, ext = read_image(self.d64_path.get())
                    if ext in (".d64", ".d81"):
                        prg_data = extract_prg_file(disk_data, entry["track"], entry["sector"], ext)
                    elif ext == ".t64":
                        prg_data = extract_t64_prg(disk_data, entry["offset"], 1000)
                    else:
                        prg_data = disk_data[entry["offset"]:]
                    
                    is_basic = prg_data[2] == 0xA9 and prg_data[4] == 0x8D
                    if is_basic:
                        basic_lines = self.basic_parser.detokenize(prg_data)
                        with open(os.path.join(output_dir, f"{entry['filename']}.bas"), "w") as f:
                            f.write("\n".join(basic_lines))
                        with open(os.path.join(output_dir, f"{entry['filename']}.pdsx"), "w") as f:
                            f.write(self.basic_parser.transpile(basic_lines, "pdsx"))
                        with open(os.path.join(output_dir, f"{entry['filename']}.qbasic"), "w") as f:
                            f.write(self.basic_parser.transpile(basic_lines, "qbasic"))
                        with open(os.path.join(output_dir, f"{entry['filename']}.c"), "w") as f:
                            f.write(self.basic_parser.transpile(basic_lines, "c"))
                    else:
                        if len(prg_data) >= 2:
                            start_addr = prg_data[0] + (prg_data[1] << 8)
                            code_data = prg_data[2:]
                            disasm = Disassembler(start_addr, code_data)
                            asm_lines = disasm.disassemble()
                        else:
                            asm_lines = ["Hata: PRG dosyası çok küçük"]
                        
                        with open(os.path.join(output_dir, f"{entry['filename']}.asm"), "w") as f:
                            f.write("\n".join(asm_lines))

                        pseudo_emitter = CodeEmitter("pseudo", self.use_illegal_opcodes.get())
                        for i, line in enumerate(asm_lines):
                            parsed = parse_line(line)
                            if parsed:
                                pseudo_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                        with open(os.path.join(output_dir, f"{entry['filename']}.pseudo"), "w") as f:
                            f.write(pseudo_emitter.get_output())

                        pdsx_emitter = CodeEmitter("pdsx", self.use_illegal_opcodes.get())
                        for i, line in enumerate(asm_lines):
                            parsed = parse_line(line)
                            if parsed:
                                pdsx_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                        with open(os.path.join(output_dir, f"{entry['filename']}.pdsx"), "w") as f:
                            f.write(pdsx_emitter.get_output())

                        qbasic_emitter = CodeEmitter("qbasic", self.use_illegal_opcodes.get())
                        for i, line in enumerate(asm_lines):
                            parsed = parse_line(line)
                            if parsed:
                                qbasic_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                        with open(os.path.join(output_dir, f"{entry['filename']}.qbasic"), "w") as f:
                            f.write(qbasic_emitter.get_output())

                        c_emitter = CodeEmitter("c", self.use_illegal_opcodes.get())
                        for i, line in enumerate(asm_lines):
                            parsed = parse_line(line)
                            if parsed:
                                c_emitter.emit_opcode(parsed[0], parsed[1], parsed[2], asm_lines, i)
                        c_lines = [
                            "#include <stdio.h>",
                            "void main() {",
                            "    unsigned char a, x, y, carry, overflow, decimal;",
                            "    unsigned char *screen_mem = (unsigned char*)0x0400;",
                            "    unsigned char *color_ram = (unsigned char*)0xD800;",
                            "    unsigned char *basic_rom = (unsigned char*)0xA000;",
                            "    unsigned char *kernal_rom = (unsigned char*)0xE000;",
                            ""
                        ] + c_emitter.get_output().splitlines() + ["}"]
                        with open(os.path.join(output_dir, f"{entry['filename']}.c"), "w") as f:
                            f.write("\n".join(c_lines))
                
                messagebox.showinfo("Başarılı", "Çıktılar kaydedildi!")
                logging.info(f"Çıktılar kaydedildi: {output_dir}")
            except Exception as e:
                logging.error(f"Kaydetme hatası: {e}")
                messagebox.showerror("Hata", f"Kaydetme başarısız: {e}")

    def show_log(self):
        try:
            with open('logs/d64_converter.log', 'r') as f:
                log_content = f.read()
            log_window = tk.Toplevel(self.root)
            log_window.title("Hata Logu")
            log_window.geometry("600x400")
            log_text = tk.Text(log_window, wrap=tk.WORD)
            log_text.insert(tk.END, log_content)
            log_text.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            logging.error(f"Log gösterilemedi: {e}")
            messagebox.showerror("Hata", f"Log gösterilemedi: {e}")

def main():
    root = tk.Tk() if not TkinterDnD else TkinterDnD.Tk()
    app = D64ConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()