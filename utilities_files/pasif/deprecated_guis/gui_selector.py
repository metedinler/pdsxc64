"""
D64 Converter - GUI Selector & Launcher
Eski ve yeni GUI arasında seçim yapma sistemi
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class GUISelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D64 Converter - GUI Seçici")
        self.root.geometry("700x500")  # Boyut artırıldı
        self.root.resizable(True, True)  # Yeniden boyutlandırılabilir
        
        # Center window
        self.center_window()
        
        self.setup_gui()
        
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"700x500+{x}+{y}")
    
    def setup_gui(self):
        """GUI seçici arayüzü"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2C3E50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="D64 Converter", 
                              font=("Arial", 24, "bold"), 
                              fg="white", bg="#2C3E50")
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(header_frame, text="Professional C64 Disassembler Suite", 
                                 font=("Arial", 10), 
                                 fg="#BDC3C7", bg="#2C3E50")
        subtitle_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # GUI Options
        options_frame = tk.LabelFrame(main_frame, text="GUI Interface Selection", 
                                     font=("Arial", 12, "bold"), bg="white")
        options_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Original/Classic GUI
        classic_frame = tk.Frame(options_frame, bg="white", relief=tk.RAISED, bd=2)
        classic_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        tk.Label(classic_frame, text="🎨 Classic GUI (Original)", 
                font=("Arial", 14, "bold"), bg="white", fg="#2980B9").pack(anchor=tk.W, padx=15, pady=10)
        
        classic_features = [
            "✓ TAB-based disassembler layout",
            "✓ Enhanced file list with type detection", 
            "✓ Start address display ($HEX + decimal)",
            "✓ Content analysis (BASIC/Machine/Data)",
            "✓ Processed files history (Excel-style)",
            "✓ PETCAT integration for BASIC detokenization",
            "✓ File search system"
        ]
        
        for feature in classic_features:
            tk.Label(classic_frame, text=feature, font=("Arial", 9), 
                    bg="white", fg="#34495E").pack(anchor=tk.W, padx=25, pady=1)
        
        tk.Button(classic_frame, text="🚀 Launch Classic GUI", 
                 command=self.launch_classic_gui,
                 bg="#3498DB", fg="white", font=("Arial", 12, "bold"),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=15)
        
        # Enhanced/New GUI  
        enhanced_frame = tk.Frame(options_frame, bg="white", relief=tk.RAISED, bd=2)
        enhanced_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        tk.Label(enhanced_frame, text="⚡ Enhanced GUI (Modern)", 
                font=("Arial", 14, "bold"), bg="white", fg="#27AE60").pack(anchor=tk.W, padx=15, pady=10)
        
        enhanced_features = [
            "✓ Radio button disassembler selection",
            "✓ Advanced checkboxes (illegal opcodes, memory analysis)",
            "✓ Recent files integration",
            "✓ Enhanced directory structure (24 subfolders)",
            "✓ Smart format detection",
            "✓ Auto-save with disassembler awareness",
            "✓ Professional py65 integration"
        ]
        
        for feature in enhanced_features:
            tk.Label(enhanced_frame, text=feature, font=("Arial", 9), 
                    bg="white", fg="#34495E").pack(anchor=tk.W, padx=25, pady=1)
        
        tk.Button(enhanced_frame, text="⚡ Launch Enhanced GUI", 
                 command=self.launch_enhanced_gui,
                 bg="#27AE60", fg="white", font=("Arial", 12, "bold"),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=15)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#ECF0F1", height=60)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        info_text = "Both GUIs share the same core functionality and button layout"
        tk.Label(footer_frame, text=info_text, font=("Arial", 9, "italic"), 
                bg="#ECF0F1", fg="#7F8C8D").pack(pady=10)
        
        # Exit button - boyutlandırma düzeltildi
        tk.Button(footer_frame, text="❌ Exit", command=self.root.quit,
                 bg="#E74C3C", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=1).pack(side=tk.RIGHT, padx=15, pady=5)
        
    def launch_classic_gui(self):
        """Classic GUI'yi başlat"""
        try:
            self.root.withdraw()  # Ana pencereyi gizle
            
            # Classic GUI'yi import et ve başlat
            import tkinter as tk
            from gui_restored import D64ConverterRestoredGUI
            
            classic_root = tk.Tk()  # Yeni root window
            classic_root.title("D64 Converter - Classic GUI")
            app = D64ConverterRestoredGUI(classic_root)
            
            # Kapanma işlevi
            def on_classic_close():
                classic_root.destroy()
                self.root.deiconify()  # Ana pencereyi geri göster
            
            classic_root.protocol("WM_DELETE_WINDOW", on_classic_close)
            classic_root.mainloop()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Hata", f"Classic GUI başlatılamadı: {e}")
            self.root.deiconify()
    
    def launch_enhanced_gui(self):
        """Enhanced GUI'yi başlat"""
        try:
            self.root.withdraw()  # Ana pencereyi gizle
            
            # Enhanced GUI'yi import et ve başlat  
            import tkinter as tk
            from d64_converter import D64ConverterApp
            
            enhanced_root = tk.Tk()  # Yeni root window
            enhanced_root.title("D64 Converter - Enhanced GUI")
            app = D64ConverterApp(enhanced_root)
            
            # Kapanma işlevi
            def on_enhanced_close():
                enhanced_root.destroy()
                self.root.deiconify()  # Ana pencereyi geri göster
            
            enhanced_root.protocol("WM_DELETE_WINDOW", on_enhanced_close)
            enhanced_root.mainloop()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Hata", f"Enhanced GUI başlatılamadı: {e}")
            self.root.deiconify()
    
    def run(self):
        """GUI seçiciyi çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🎯 D64 Converter GUI Selector başlatılıyor...")
    selector = GUISelector()
    selector.run()
