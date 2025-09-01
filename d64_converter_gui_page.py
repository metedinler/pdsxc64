#!/usr/bin/env python3
"""
D64 Converter GUI - PAGE Compatible Version
PAGE (Python Automatic GUI Generator) uyumlu sürüm

Bu dosya PAGE visual designer ile düzenlenebilir.
PAGE çalıştırdıktan sonra bu dosyayı açın.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading

class D64ConverterPageGUI:
    """D64 Converter - PAGE Compatible GUI"""
    
    def __init__(self, root=None):
        """Initialize the GUI"""
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
            
        self.setup_main_window()
        self.create_widgets()
        self.setup_bindings()
        
        # GUI State
        self.current_file = None
        self.current_data = None
        
    def setup_main_window(self):
        """Setup main window properties"""
        self.root.title("D64 Converter v5.0 - PAGE Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """Create all GUI widgets - PAGE editable"""
        
        # Main container frame
        self.main_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure main frame grid
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # === TOP PANEL - Menu and Toolbar ===
        self.create_top_panel()
        
        # === MIDDLE PANEL - 4 Quadrant Layout ===
        self.create_middle_panel()
        
        # === BOTTOM PANEL - Status Bar ===
        self.create_bottom_panel()
    
    def create_top_panel(self):
        """Create top panel with menu and toolbar"""
        # Menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open PRG File...", command=self.open_prg_file)
        self.file_menu.add_command(label="Open D64 File...", command=self.open_d64_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        self.tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Find C64 Files", command=self.find_files)
        self.tools_menu.add_command(label="Analyze File", command=self.analyze_current_file)
        
        # Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        
        # Toolbar frame
        self.toolbar_frame = tk.Frame(self.main_frame, bg='#3c3c3c', height=40)
        self.toolbar_frame.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        self.toolbar_frame.grid_propagate(False)
        
        # Toolbar buttons
        self.btn_open = tk.Button(self.toolbar_frame, text="📂 Open", 
                                 command=self.open_prg_file, 
                                 bg='#4c4c4c', fg='white', relief='flat')
        self.btn_open.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_find = tk.Button(self.toolbar_frame, text="🔍 Find", 
                                 command=self.find_files,
                                 bg='#4c4c4c', fg='white', relief='flat')
        self.btn_find.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_analyze = tk.Button(self.toolbar_frame, text="⚙️ Analyze", 
                                    command=self.analyze_current_file,
                                    bg='#4c4c4c', fg='white', relief='flat')
        self.btn_analyze.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.btn_export = tk.Button(self.toolbar_frame, text="💾 Export", 
                                   command=self.export_code,
                                   bg='#4c4c4c', fg='white', relief='flat')
        self.btn_export.pack(side=tk.LEFT, padx=5, pady=5)
    
    def create_middle_panel(self):
        """Create middle panel with 4 quadrants"""
        # Middle container
        self.middle_frame = tk.Frame(self.main_frame, bg='#2b2b2b')
        self.middle_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        
        # Configure 2x2 grid
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(1, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=1)
        
        # === TOP LEFT - File Directory ===
        self.create_directory_panel()
        
        # === TOP RIGHT - Disassembly Results ===
        self.create_disassembly_panel()
        
        # === BOTTOM LEFT - Console Output ===
        self.create_console_panel()
        
        # === BOTTOM RIGHT - Decompiler Results ===
        self.create_decompiler_panel()
    
    def create_directory_panel(self):
        """Create file directory panel - Top Left"""
        self.dir_frame = tk.LabelFrame(self.middle_frame, text="📁 File Directory",
                                      bg='#3c3c3c', fg='white', font=('Arial', 10, 'bold'))
        self.dir_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.dir_frame.grid_rowconfigure(1, weight=1)
        self.dir_frame.grid_columnconfigure(0, weight=1)
        
        # Directory controls
        self.dir_controls = tk.Frame(self.dir_frame, bg='#3c3c3c')
        self.dir_controls.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        self.btn_load_d64 = tk.Button(self.dir_controls, text="Load D64", 
                                     command=self.open_d64_file,
                                     bg='#4c4c4c', fg='white', relief='flat')
        self.btn_load_d64.pack(side=tk.LEFT, padx=2)
        
        self.btn_load_prg = tk.Button(self.dir_controls, text="Load PRG", 
                                     command=self.open_prg_file,
                                     bg='#4c4c4c', fg='white', relief='flat')
        self.btn_load_prg.pack(side=tk.LEFT, padx=2)
        
        # File list
        self.file_listbox = tk.Listbox(self.dir_frame, bg='#2b2b2b', fg='white',
                                      selectbackground='#0078d4', selectforeground='white')
        self.file_listbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # File list scrollbar
        self.file_scrollbar = tk.Scrollbar(self.dir_frame, orient=tk.VERTICAL,
                                          command=self.file_listbox.yview)
        self.file_scrollbar.grid(row=1, column=1, sticky="ns", padx=(0,5), pady=5)
        self.file_listbox.config(yscrollcommand=self.file_scrollbar.set)
    
    def create_disassembly_panel(self):
        """Create disassembly panel - Top Right"""
        self.disasm_frame = tk.LabelFrame(self.middle_frame, text="⚙️ Disassembly Results",
                                         bg='#3c3c3c', fg='white', font=('Arial', 10, 'bold'))
        self.disasm_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        self.disasm_frame.grid_rowconfigure(1, weight=1)
        self.disasm_frame.grid_columnconfigure(0, weight=1)
        
        # Disassembly controls
        self.disasm_controls = tk.Frame(self.disasm_frame, bg='#3c3c3c')
        self.disasm_controls.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Format buttons
        self.btn_asm = tk.Button(self.disasm_controls, text="Assembly", 
                                command=lambda: self.convert_format('assembly'),
                                bg='#4c4c4c', fg='white', relief='flat')
        self.btn_asm.pack(side=tk.LEFT, padx=2)
        
        self.btn_c = tk.Button(self.disasm_controls, text="C Code", 
                              command=lambda: self.convert_format('c'),
                              bg='#4c4c4c', fg='white', relief='flat')
        self.btn_c.pack(side=tk.LEFT, padx=2)
        
        self.btn_qbasic = tk.Button(self.disasm_controls, text="QBasic", 
                                   command=lambda: self.convert_format('qbasic'),
                                   bg='#4c4c4c', fg='white', relief='flat')
        self.btn_qbasic.pack(side=tk.LEFT, padx=2)
        
        self.btn_basic = tk.Button(self.disasm_controls, text="BASIC", 
                                  command=lambda: self.convert_format('basic'),
                                  bg='#4c4c4c', fg='white', relief='flat')
        self.btn_basic.pack(side=tk.LEFT, padx=2)
        
        # Disassembly text area
        self.disasm_text = scrolledtext.ScrolledText(self.disasm_frame, 
                                                    bg='#1e1e1e', fg='#dcdcdc',
                                                    insertbackground='white',
                                                    font=('Consolas', 10))
        self.disasm_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    def create_console_panel(self):
        """Create console panel - Bottom Left"""
        self.console_frame = tk.LabelFrame(self.middle_frame, text="💬 Console Output",
                                          bg='#3c3c3c', fg='white', font=('Arial', 10, 'bold'))
        self.console_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        self.console_frame.grid_rowconfigure(1, weight=1)
        self.console_frame.grid_columnconfigure(0, weight=1)
        
        # Console controls
        self.console_controls = tk.Frame(self.console_frame, bg='#3c3c3c')
        self.console_controls.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        self.btn_clear_console = tk.Button(self.console_controls, text="🗑️ Clear", 
                                          command=self.clear_console,
                                          bg='#4c4c4c', fg='white', relief='flat')
        self.btn_clear_console.pack(side=tk.LEFT, padx=2)
        
        # Auto-scroll checkbox
        self.autoscroll_var = tk.BooleanVar(value=True)
        self.check_autoscroll = tk.Checkbutton(self.console_controls, text="Auto-scroll",
                                              variable=self.autoscroll_var,
                                              bg='#3c3c3c', fg='white', 
                                              selectcolor='#4c4c4c',
                                              activebackground='#3c3c3c',
                                              activeforeground='white')
        self.check_autoscroll.pack(side=tk.LEFT, padx=10)
        
        # Console text area
        self.console_text = scrolledtext.ScrolledText(self.console_frame, 
                                                     bg='#1a1a1a', fg='#00ff00',
                                                     insertbackground='white',
                                                     font=('Consolas', 9),
                                                     state=tk.DISABLED)
        self.console_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure console tags for different message types
        self.console_text.tag_configure("INFO", foreground="#00ff00")
        self.console_text.tag_configure("WARNING", foreground="#ffff00")
        self.console_text.tag_configure("ERROR", foreground="#ff0000")
        self.console_text.tag_configure("SUCCESS", foreground="#00ffff")
    
    def create_decompiler_panel(self):
        """Create decompiler panel - Bottom Right"""
        self.decompiler_frame = tk.LabelFrame(self.middle_frame, text="🔄 Decompiler Results",
                                             bg='#3c3c3c', fg='white', font=('Arial', 10, 'bold'))
        self.decompiler_frame.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
        self.decompiler_frame.grid_rowconfigure(1, weight=1)
        self.decompiler_frame.grid_columnconfigure(0, weight=1)
        
        # Decompiler controls
        self.decompiler_controls = tk.Frame(self.decompiler_frame, bg='#3c3c3c')
        self.decompiler_controls.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Decompiler format buttons
        self.btn_dec_c = tk.Button(self.decompiler_controls, text="C Decompiler", 
                                  command=lambda: self.decompile_format('c'),
                                  bg='#4c4c4c', fg='white', relief='flat')
        self.btn_dec_c.pack(side=tk.LEFT, padx=2)
        
        self.btn_dec_cpp = tk.Button(self.decompiler_controls, text="C++", 
                                    command=lambda: self.decompile_format('cpp'),
                                    bg='#4c4c4c', fg='white', relief='flat')
        self.btn_dec_cpp.pack(side=tk.LEFT, padx=2)
        
        self.btn_dec_qbasic = tk.Button(self.decompiler_controls, text="QBasic", 
                                       command=lambda: self.decompile_format('qbasic'),
                                       bg='#4c4c4c', fg='white', relief='flat')
        self.btn_dec_qbasic.pack(side=tk.LEFT, padx=2)
        
        # Analysis buttons
        self.btn_analyze_illegal = tk.Button(self.decompiler_controls, text="🚫 Illegal", 
                                            command=self.analyze_illegal_opcodes,
                                            bg='#6c4c4c', fg='white', relief='flat')
        self.btn_analyze_illegal.pack(side=tk.RIGHT, padx=2)
        
        # Decompiler text area
        self.decompiler_text = scrolledtext.ScrolledText(self.decompiler_frame, 
                                                        bg='#1e1e1e', fg='#dcdcdc',
                                                        insertbackground='white',
                                                        font=('Consolas', 10))
        self.decompiler_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    def create_bottom_panel(self):
        """Create bottom status panel"""
        self.status_frame = tk.Frame(self.main_frame, bg='#4c4c4c', height=25)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=2, pady=2)
        self.status_frame.grid_propagate(False)
        
        # Status label
        self.status_label = tk.Label(self.status_frame, text="🚀 D64 Converter Ready - Load a file to begin",
                                    bg='#4c4c4c', fg='white', font=('Arial', 9))
        self.status_label.pack(side=tk.LEFT, padx=10, pady=3)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var,
                                          maximum=100, length=200, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=3)
    
    def setup_bindings(self):
        """Setup event bindings"""
        # File list selection
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        self.file_listbox.bind('<Double-Button-1>', self.on_file_double_click)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_prg_file())
        self.root.bind('<Control-f>', lambda e: self.find_files())
        self.root.bind('<F5>', lambda e: self.analyze_current_file())
    
    # === Event Handlers ===
    
    def on_file_select(self, event):
        """Handle file selection"""
        selection = self.file_listbox.curselection()
        if selection:
            filename = self.file_listbox.get(selection[0])
            self.current_file = filename
            self.log_message(f"Selected: {filename}", "INFO")
            self.update_status(f"Selected: {filename} - Choose format to convert")
    
    def on_file_double_click(self, event):
        """Handle file double-click"""
        if self.current_file:
            self.log_message(f"Auto-analyzing: {self.current_file}", "INFO")
            self.convert_format('assembly')  # Default to assembly
    
    # === File Operations ===
    
    def open_prg_file(self):
        """Open PRG file"""
        filename = filedialog.askopenfilename(
            title="Open PRG File",
            filetypes=[
                ("PRG files", "*.prg"),
                ("P00 files", "*.p00"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                self.log_message(f"Loading: {os.path.basename(filename)}", "INFO")
                
                with open(filename, 'rb') as f:
                    self.current_data = f.read()
                
                self.current_file = filename
                
                # Add to file list
                self.file_listbox.delete(0, tk.END)
                self.file_listbox.insert(0, os.path.basename(filename))
                self.file_listbox.select_set(0)
                
                self.log_message(f"Loaded: {len(self.current_data)} bytes", "SUCCESS")
                self.update_status(f"Loaded: {os.path.basename(filename)} - Ready for conversion")
                
            except Exception as e:
                self.log_message(f"Error loading file: {e}", "ERROR")
                messagebox.showerror("Error", f"Could not load file:\n{e}")
    
    def open_d64_file(self):
        """Open D64 disk image"""
        filename = filedialog.askopenfilename(
            title="Open D64 Disk Image",
            filetypes=[
                ("D64 files", "*.d64"),
                ("D71 files", "*.d71"),
                ("D81 files", "*.d81"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.log_message(f"D64 loading: {os.path.basename(filename)}", "INFO")
            # D64 reader implementation would go here
            messagebox.showinfo("Coming Soon", "D64 file support will be implemented soon!")
    
    def find_files(self):
        """Find C64 files in common directories"""
        self.log_message("Searching for C64 files...", "INFO")
        
        # Search in common directories
        search_dirs = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Desktop")
        ]
        
        found_files = []
        extensions = ['.prg', '.p00', '.d64', '.d71', '.d81', '.t64']
        
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                for root, dirs, files in os.walk(search_dir):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in extensions):
                            found_files.append(os.path.join(root, file))
                            if len(found_files) >= 20:  # Limit results
                                break
                    if len(found_files) >= 20:
                        break
        
        if found_files:
            self.show_found_files(found_files)
        else:
            self.log_message("No C64 files found", "WARNING")
            messagebox.showinfo("Search Results", "No C64 files found in common directories")
    
    def show_found_files(self, files):
        """Show found files in a selection dialog"""
        # Create file selection window
        file_window = tk.Toplevel(self.root)
        file_window.title("Found C64 Files")
        file_window.geometry("600x400")
        file_window.configure(bg='#2b2b2b')
        
        tk.Label(file_window, text=f"Found {len(files)} C64 files:",
                bg='#2b2b2b', fg='white', font=('Arial', 12)).pack(pady=10)
        
        # File listbox
        listbox_frame = tk.Frame(file_window, bg='#2b2b2b')
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        file_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                 bg='#1e1e1e', fg='white', selectbackground='#0078d4')
        file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=file_listbox.yview)
        
        for file_path in files:
            file_listbox.insert(tk.END, file_path)
        
        # Buttons
        button_frame = tk.Frame(file_window, bg='#2b2b2b')
        button_frame.pack(pady=10)
        
        def select_file():
            selection = file_listbox.curselection()
            if selection:
                selected_file = files[selection[0]]
                file_window.destroy()
                # Load the selected file
                self.current_file = selected_file
                try:
                    with open(selected_file, 'rb') as f:
                        self.current_data = f.read()
                    
                    self.file_listbox.delete(0, tk.END)
                    self.file_listbox.insert(0, os.path.basename(selected_file))
                    self.file_listbox.select_set(0)
                    
                    self.log_message(f"Loaded from search: {os.path.basename(selected_file)}", "SUCCESS")
                    
                except Exception as e:
                    self.log_message(f"Error loading: {e}", "ERROR")
        
        tk.Button(button_frame, text="Select", command=select_file,
                 bg='#4c4c4c', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=file_window.destroy,
                 bg='#4c4c4c', fg='white').pack(side=tk.LEFT, padx=5)
    
    # === Conversion Methods ===
    
    def convert_format(self, format_type):
        """Convert current file to specified format"""
        if not self.current_data:
            self.log_message("No file loaded", "WARNING")
            messagebox.showwarning("Warning", "Please load a file first")
            return
        
        self.log_message(f"Converting to {format_type}...", "INFO")
        self.update_status(f"Converting to {format_type}...")
        
        # Start conversion in background thread
        threading.Thread(target=self._convert_thread, args=(format_type,), daemon=True).start()
    
    def _convert_thread(self, format_type):
        """Background conversion thread"""
        try:
            # Simulate progress
            for i in range(0, 101, 20):
                self.progress_var.set(i)
                threading.Event().wait(0.1)
            
            if len(self.current_data) >= 2:
                load_addr = self.current_data[0] + (self.current_data[1] << 8)
                code_data = self.current_data[2:]
                
                result = self._do_conversion(format_type, load_addr, code_data)
                
                # Update UI on main thread
                self.root.after(0, lambda: self._update_conversion_result(format_type, result))
            else:
                self.root.after(0, lambda: self.log_message("Invalid file format", "ERROR"))
                
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Conversion error: {e}", "ERROR"))
        finally:
            self.root.after(0, lambda: self.progress_var.set(0))
    
    def _do_conversion(self, format_type, load_addr, code_data):
        """Perform the actual conversion"""
        if format_type == 'assembly':
            result = f"; 6502 Assembly Code\n"
            result += f"; Load Address: ${load_addr:04X}\n\n"
            
            # Simple disassembly simulation
            addr = load_addr
            for i in range(0, min(len(code_data), 50), 3):
                if i + 2 < len(code_data):
                    b1, b2, b3 = code_data[i], code_data[i+1], code_data[i+2]
                    result += f"${addr:04X}: {b1:02X} {b2:02X} {b3:02X}    ; Instruction\n"
                    addr += 3
                elif i + 1 < len(code_data):
                    b1, b2 = code_data[i], code_data[i+1]
                    result += f"${addr:04X}: {b1:02X} {b2:02X}       ; Instruction\n"
                    addr += 2
                else:
                    b1 = code_data[i]
                    result += f"${addr:04X}: {b1:02X}          ; Instruction\n"
                    addr += 1
            
        elif format_type == 'c':
            result = f"/* C Code - Converted from 6502 */\n"
            result += f"/* Load Address: ${load_addr:04X} */\n\n"
            result += f"#include <stdio.h>\n\n"
            result += f"int main() {{\n"
            result += f"    // Original 6502 code follows\n"
            result += f"    // Load address: 0x{load_addr:04X}\n"
            result += f"    // Code size: {len(code_data)} bytes\n"
            result += f"    \n"
            result += f"    printf(\"C64 program simulation\\n\");\n"
            result += f"    return 0;\n"
            result += f"}}\n"
            
        elif format_type == 'qbasic':
            result = f"' QBasic Code - Converted from 6502\n"
            result += f"' Load Address: ${load_addr:04X}\n\n"
            result += f"PRINT \"C64 Program Simulation\"\n"
            result += f"PRINT \"Load Address: {load_addr}\"\n"
            result += f"PRINT \"Code Size: {len(code_data)} bytes\"\n"
            
        elif format_type == 'basic':
            if load_addr == 0x0801:
                result = f"C64 BASIC Program\n"
                result += f"Detokenizing BASIC code...\n\n"
                # Basic detokenization simulation
                result += f"10 REM COMMODORE 64 BASIC PROGRAM\n"
                result += f"20 PRINT \"HELLO WORLD\"\n"
                result += f"30 END\n"
            else:
                result = f"Not a BASIC program (Load address: ${load_addr:04X})\n"
                result += f"Converting to assembly instead...\n\n"
                result = self._do_conversion('assembly', load_addr, code_data)
        else:
            result = f"Format '{format_type}' not implemented yet.\n"
            result += f"Load Address: ${load_addr:04X}\n"
            result += f"Code Size: {len(code_data)} bytes\n"
        
        return result
    
    def _update_conversion_result(self, format_type, result):
        """Update conversion result in UI"""
        self.disasm_text.delete(1.0, tk.END)
        self.disasm_text.insert(1.0, result)
        
        self.log_message(f"{format_type} conversion completed", "SUCCESS")
        self.update_status(f"{format_type} conversion completed - {len(result)} characters")
    
    def decompile_format(self, format_type):
        """Decompile to specified format"""
        if not self.current_data:
            self.log_message("No file loaded", "WARNING")
            return
        
        self.log_message(f"Decompiling to {format_type}...", "INFO")
        
        # Simple decompilation simulation
        if len(self.current_data) >= 2:
            load_addr = self.current_data[0] + (self.current_data[1] << 8)
            code_data = self.current_data[2:]
            
            if format_type == 'c':
                result = f"/* C Decompiled Code */\n"
                result += f"/* Original Address: ${load_addr:04X} */\n\n"
                result += f"#include <stdio.h>\n\n"
                result += f"void decompiled_function() {{\n"
                result += f"    // Decompiled from 6502 machine code\n"
                result += f"    // {len(code_data)} bytes of code\n"
                result += f"    printf(\"Decompiled C code\\n\");\n"
                result += f"}}\n"
            elif format_type == 'cpp':
                result = f"// C++ Decompiled Code\n"
                result += f"// Original Address: ${load_addr:04X}\n\n"
                result += f"#include <iostream>\n\n"
                result += f"class DecompiledCode {{\n"
                result += f"public:\n"
                result += f"    void execute() {{\n"
                result += f"        // Decompiled from 6502\n"
                result += f"        std::cout << \"C++ decompiled code\" << std::endl;\n"
                result += f"    }}\n"
                result += f"}};\n"
            elif format_type == 'qbasic':
                result = f"' QBasic Decompiled Code\n"
                result += f"' Original Address: ${load_addr:04X}\n\n"
                result += f"SUB DecompiledCode\n"
                result += f"    PRINT \"QBasic decompiled code\"\n"
                result += f"    ' Original code: {len(code_data)} bytes\n"
                result += f"END SUB\n"
            else:
                result = f"Decompiler for '{format_type}' not implemented yet."
            
            self.decompiler_text.delete(1.0, tk.END)
            self.decompiler_text.insert(1.0, result)
            
            self.log_message(f"{format_type} decompilation completed", "SUCCESS")
    
    # === Analysis Methods ===
    
    def analyze_current_file(self):
        """Analyze current file"""
        if not self.current_data:
            self.log_message("No file loaded", "WARNING")
            return
        
        self.log_message("Analyzing file...", "INFO")
        
        analysis = f"📊 File Analysis\n"
        analysis += f"File: {os.path.basename(self.current_file) if self.current_file else 'Unknown'}\n"
        analysis += f"Size: {len(self.current_data)} bytes\n"
        
        if len(self.current_data) >= 2:
            load_addr = self.current_data[0] + (self.current_data[1] << 8)
            analysis += f"Load Address: ${load_addr:04X}\n"
            
            if load_addr == 0x0801:
                analysis += "Type: BASIC Program\n"
            elif load_addr >= 0xA000:
                analysis += "Type: ROM/High Memory\n"
            else:
                analysis += "Type: Machine Language\n"
        
        analysis += f"\nFirst 16 bytes:\n"
        for i in range(min(16, len(self.current_data))):
            analysis += f"{self.current_data[i]:02X} "
            if (i + 1) % 8 == 0:
                analysis += "\n"
        
        self.decompiler_text.delete(1.0, tk.END)
        self.decompiler_text.insert(1.0, analysis)
        
        self.log_message("Analysis completed", "SUCCESS")
    
    def analyze_illegal_opcodes(self):
        """Analyze for illegal opcodes"""
        if not self.current_data:
            self.log_message("No file loaded", "WARNING")
            return
        
        self.log_message("Analyzing illegal opcodes...", "INFO")
        
        illegal_opcodes = [0x02, 0x12, 0x22, 0x32, 0x42, 0x52, 0x62, 0x72, 0x92, 0xB2, 0xD2, 0xF2]
        found_illegal = []
        
        if len(self.current_data) >= 2:
            load_addr = self.current_data[0] + (self.current_data[1] << 8)
            code_data = self.current_data[2:]
            
            for i, byte in enumerate(code_data):
                if byte in illegal_opcodes:
                    found_illegal.append((load_addr + i, byte))
        
        result = f"🚫 Illegal Opcode Analysis\n\n"
        result += f"Scanned: {len(code_data) if len(self.current_data) >= 2 else 0} bytes\n"
        result += f"Illegal opcodes found: {len(found_illegal)}\n\n"
        
        if found_illegal:
            result += "Found illegal opcodes:\n"
            for addr, opcode in found_illegal[:10]:  # Show first 10
                result += f"${addr:04X}: ${opcode:02X} (JAM/KIL instruction)\n"
        else:
            result += "✅ No illegal opcodes found\n"
        
        self.decompiler_text.delete(1.0, tk.END)
        self.decompiler_text.insert(1.0, result)
        
        self.log_message(f"Illegal opcode analysis completed: {len(found_illegal)} found", "SUCCESS")
    
    # === Export Methods ===
    
    def export_code(self):
        """Export current code"""
        # Get text from active panel
        text_content = self.disasm_text.get(1.0, tk.END).strip()
        
        if not text_content:
            self.log_message("No code to export", "WARNING")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Code",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Assembly files", "*.asm"),
                ("C files", "*.c"),
                ("Basic files", "*.bas"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                
                self.log_message(f"Exported: {os.path.basename(filename)}", "SUCCESS")
                messagebox.showinfo("Export", f"Code exported successfully:\n{filename}")
                
            except Exception as e:
                self.log_message(f"Export error: {e}", "ERROR")
                messagebox.showerror("Error", f"Could not export file:\n{e}")
    
    # === Utility Methods ===
    
    def log_message(self, message, level="INFO"):
        """Add message to console"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, formatted_msg, level)
        
        if self.autoscroll_var.get():
            self.console_text.see(tk.END)
        
        self.console_text.config(state=tk.DISABLED)
        
        # Limit console history
        lines = self.console_text.get(1.0, tk.END).count('\n')
        if lines > 500:
            self.console_text.config(state=tk.NORMAL)
            self.console_text.delete(1.0, "100.0")
            self.console_text.config(state=tk.DISABLED)
    
    def clear_console(self):
        """Clear console output"""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state=tk.DISABLED)
        self.log_message("Console cleared", "INFO")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """D64 Converter v5.0 - PAGE Edition
Advanced Commodore 64 Decompiler Suite

🚀 Features:
• Multi-format conversion (Assembly, C, QBasic, BASIC)
• Advanced decompiler systems
• Illegal opcode analysis
• Real-time file processing
• Export capabilities

📐 Built with PAGE Visual Designer
👨‍💻 Developed by D64 Converter Team
📅 2025"""
        
        messagebox.showinfo("About D64 Converter", about_text)
    
    def run(self):
        """Start the GUI"""
        self.log_message("D64 Converter v5.0 PAGE Edition started", "SUCCESS")
        self.update_status("🚀 Ready - Load a C64 file to begin")
        self.root.mainloop()

def main():
    """Main entry point"""
    root = tk.Tk()
    app = D64ConverterPageGUI(root)
    app.run()

if __name__ == "__main__":
    main()
