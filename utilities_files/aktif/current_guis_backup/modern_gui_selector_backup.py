"""
D64 Converter - Modern GUI Selector
Professional dark theme with gradient effects
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class ModernGUISelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D64 Converter - GUI Selection")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Modern dark theme colors
        self.colors = {
            'bg_primary': '#1e1e2e',      # Dark purple
            'bg_secondary': '#313244',     # Lighter purple
            'accent': '#89b4fa',          # Blue
            'accent_hover': '#74c7ec',    # Cyan
            'text_primary': '#cdd6f4',    # Light gray
            'text_secondary': '#bac2de',  # Medium gray
            'success': '#a6e3a1',         # Green
            'warning': '#f9e2af',         # Yellow
            'error': '#f38ba8'            # Red
        }
        
        # Set theme
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Center window
        self.center_window()
        
        # Setup GUI
        self.setup_modern_gui()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
    
    def setup_modern_gui(self):
        """Setup modern dark theme GUI"""
        # Header with gradient effect
        header_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="D64 CONVERTER", 
                              font=("Segoe UI", 32, "bold"), 
                              fg=self.colors['accent'], 
                              bg=self.colors['bg_secondary'])
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Professional C64 Disassembler Suite", 
                                 font=("Segoe UI", 12), 
                                 fg=self.colors['text_secondary'], 
                                 bg=self.colors['bg_secondary'])
        subtitle_label.pack()
        
        # Main content area
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Options frame
        options_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Classic GUI Option (Klasik GUI - gui_restored.py)
        self.create_gui_option(options_frame, 
                              "🎨 KLASIK GUI", 
                              "Advanced File Analysis & Tabbed Interface",
                              [
                                  "✓ TAB-based disassembler output layout",
                                  "✓ Enhanced file list with content detection", 
                                  "✓ Start address display ($HEX + decimal)",
                                  "✓ Real-time file content preview",
                                  "✓ Processed files history system",
                                  "✓ PETCAT BASIC detokenization",
                                  "✓ Integrated search functionality"
                              ],
                              self.colors['success'],
                              self.launch_classic_gui,
                              0)
        
        # X1 GUI Option (X1 GUI - d64_converterX1.py)
        self.create_gui_option(options_frame,
                              "⚡ X1 GUI", 
                              "Most Advanced GUI - Professional X Series",
                              [
                                  "✓ 2630 lines of advanced code",
                                  "✓ Enhanced disassembler integration",
                                  "✓ Multi-threading decompiler support",
                                  "✓ Professional logging system",
                                  "✓ Advanced C code generation",
                                  "✓ Complete format support (6 formats)",
                                  "✓ Premium X series features"
                              ],
                              self.colors['accent'],
                              self.launch_x1_gui,
                              1)
        
        # Eski GUI v3 Option (eski_gui_3.py)
        self.create_gui_option(options_frame,
                              "📅 ESKİ GUI v3", 
                              "Stable Legacy Version",
                              [
                                  "✓ 87KB proven stable codebase",
                                  "✓ Legacy interface compatibility",
                                  "✓ Tested and reliable functions",
                                  "✓ 16.07.2025 stable release",
                                  "✓ Compatible with older workflows",
                                  "✓ Time-tested features",
                                  "✓ Backup-proven reliability"
                              ],
                              self.colors['warning'],
                              self.launch_eski_gui_v3,
                              2)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=80)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        info_label = tk.Label(footer_frame, 
                             text="3 Active GUI Options: X1 (Advanced), Klasik (Tabbed), Eski v3 (Stable Legacy)",
                             font=("Segoe UI", 10, "italic"), 
                             fg=self.colors['text_secondary'], 
                             bg=self.colors['bg_secondary'])
        info_label.pack(pady=10)
        
        # Exit button
        exit_btn = tk.Button(footer_frame, 
                            text="❌ Exit Application", 
                            command=self.root.quit,
                            bg=self.colors['error'], 
                            fg="white", 
                            font=("Segoe UI", 11, "bold"),
                            relief=tk.FLAT,
                            padx=20, pady=8)
        exit_btn.pack(side=tk.RIGHT, padx=20, pady=15)
        
    def create_gui_option(self, parent, title, subtitle, features, color, command, row):
        """Create a modern GUI option card"""
        # Main card frame
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief=tk.FLAT, bd=0)
        card_frame.grid(row=row, column=0, sticky="ew", pady=15, padx=20)
        
        # Configure grid weights
        parent.grid_columnconfigure(0, weight=1)
        
        # Content frame with padding
        content_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # Title
        title_label = tk.Label(content_frame, 
                              text=title, 
                              font=("Segoe UI", 18, "bold"), 
                              fg=color, 
                              bg=self.colors['bg_secondary'])
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Subtitle
        subtitle_label = tk.Label(content_frame, 
                                 text=subtitle, 
                                 font=("Segoe UI", 12), 
                                 fg=self.colors['text_secondary'], 
                                 bg=self.colors['bg_secondary'])
        subtitle_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Features
        for feature in features:
            feature_label = tk.Label(content_frame, 
                                   text=feature, 
                                   font=("Segoe UI", 10), 
                                   fg=self.colors['text_primary'], 
                                   bg=self.colors['bg_secondary'])
            feature_label.pack(anchor=tk.W, pady=1, padx=20)
        
        # Launch button
        launch_btn = tk.Button(content_frame, 
                              text=f"🚀 Launch {title.split()[1]} GUI", 
                              command=command,
                              bg=color, 
                              fg="white", 
                              font=("Segoe UI", 14, "bold"),
                              relief=tk.FLAT,
                              padx=30, pady=12)
        launch_btn.pack(pady=20)
        
        # Hover effects
        def on_enter(e):
            launch_btn.configure(bg=self.colors['accent_hover'])
        def on_leave(e):
            launch_btn.configure(bg=color)
            
        launch_btn.bind("<Enter>", on_enter)
        launch_btn.bind("<Leave>", on_leave)
        
    def launch_classic_gui(self):
        """Launch Klasik GUI - gui_restored.py"""
        try:
            self.root.withdraw()
            
            import tkinter as tk
            from gui_restored import D64ConverterRestoredGUI
            
            classic_root = tk.Toplevel()
            app = D64ConverterRestoredGUI(classic_root)
            
            def on_close():
                classic_root.destroy()
                self.root.deiconify()
            
            classic_root.protocol("WM_DELETE_WINDOW", on_close)
            
        except Exception as e:
            messagebox.showerror("Error", f"Klasik GUI launch failed: {e}")
            self.root.deiconify()
    
    def launch_x1_gui(self):
        """Launch X1 GUI - d64_converterX1.py"""
        try:
            self.root.withdraw()
            
            import tkinter as tk
            from d64_converterX1 import D64ConverterApp
            
            x1_root = tk.Toplevel()
            app = D64ConverterApp(x1_root)
            
            def on_close():
                x1_root.destroy()
                self.root.deiconify()
            
            x1_root.protocol("WM_DELETE_WINDOW", on_close)
            
        except Exception as e:
            messagebox.showerror("Error", f"X1 GUI launch failed: {e}")
            self.root.deiconify()
    
    def launch_eski_gui_v3(self):
        """Launch Eski GUI v3 - eski_gui_3.py"""
        try:
            self.root.withdraw()
            
            import tkinter as tk
            from eski_gui_3 import D64ConverterApp
            
            eski_root = tk.Toplevel()
            app = D64ConverterApp(eski_root)
            
            def on_close():
                eski_root.destroy()
                self.root.deiconify()
            
            eski_root.protocol("WM_DELETE_WINDOW", on_close)
            
        except Exception as e:
            messagebox.showerror("Error", f"Eski GUI v3 launch failed: {e}")
            self.root.deiconify()
    
    def run(self):
        """Run the GUI selector"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🎯 Modern D64 Converter GUI Selector starting...")
    selector = ModernGUISelector()
    selector.run()
