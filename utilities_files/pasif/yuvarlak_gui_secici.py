"""
Yuvarlak GUI Seçici - Eski GUI'leri Geri Getirme
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

class YuvarlakGUISecici:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D64 Converter - Yuvarlak GUI Seçici")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Seçim değişkenleri
        self.gui_var = tk.StringVar(value="eski")
        
        self.setup_gui()
        
    def setup_gui(self):
        """GUI bileşenlerini oluştur"""
        # Ana başlık
        title_label = tk.Label(self.root, text="D64 Converter GUI Seçici", 
                              font=("Arial", 18, "bold"), 
                              bg="#f0f0f0", fg="#2c3e50")
        title_label.pack(pady=20)
        
        # Alt başlık
        subtitle = tk.Label(self.root, text="Hangi GUI'yi kullanmak istiyorsunuz?", 
                           font=("Arial", 12), 
                           bg="#f0f0f0", fg="#34495e")
        subtitle.pack(pady=10)
        
        # Ana seçim çerçevesi
        main_frame = tk.Frame(self.root, bg="#ffffff", relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # GUI seçim başlığı
        gui_title = tk.Label(main_frame, text="GUI Versiyonu Seçin:", 
                            font=("Arial", 14, "bold"), 
                            bg="#ffffff", fg="#2c3e50")
        gui_title.pack(pady=20)
        
        # Yuvarlak radio buttonlar için frame
        radio_frame = tk.Frame(main_frame, bg="#ffffff")
        radio_frame.pack(pady=20)
        
        # Eski GUI seçeneği
        eski_frame = tk.Frame(radio_frame, bg="#ffffff")
        eski_frame.pack(pady=15)
        
        tk.Radiobutton(eski_frame, text="🔄 Eski GUI (Yedeklerden)", 
                      variable=self.gui_var, value="eski",
                      font=("Arial", 12, "bold"), 
                      bg="#ffffff", fg="#27ae60",
                      selectcolor="#e8f5e8",
                      command=self.update_description).pack(side=tk.LEFT)
        
        # Klasik GUI seçeneği  
        klasik_frame = tk.Frame(radio_frame, bg="#ffffff")
        klasik_frame.pack(pady=15)
        
        tk.Radiobutton(klasik_frame, text="📊 Klasik GUI (Horizontal Layout)", 
                      variable=self.gui_var, value="klasik",
                      font=("Arial", 12, "bold"), 
                      bg="#ffffff", fg="#3498db",
                      selectcolor="#e3f2fd",
                      command=self.update_description).pack(side=tk.LEFT)
        
        # Enhanced GUI seçeneği
        enhanced_frame = tk.Frame(radio_frame, bg="#ffffff")
        enhanced_frame.pack(pady=15)
        
        tk.Radiobutton(enhanced_frame, text="⚡ Enhanced GUI (Modern)", 
                      variable=self.gui_var, value="enhanced",
                      font=("Arial", 12, "bold"), 
                      bg="#ffffff", fg="#9b59b6",
                      selectcolor="#f3e5f5",
                      command=self.update_description).pack(side=tk.LEFT)
        
        # Açıklama alanı
        self.desc_frame = tk.Frame(main_frame, bg="#f8f9fa", relief=tk.SUNKEN, bd=1)
        self.desc_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.desc_label = tk.Label(self.desc_frame, text="", 
                                  font=("Arial", 10), 
                                  bg="#f8f9fa", fg="#2c3e50",
                                  wraplength=500, justify=tk.LEFT)
        self.desc_label.pack(pady=15)
        
        # Düğmeler
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, pady=20)
        
        # Başlat düğmesi
        self.start_btn = tk.Button(button_frame, text="🚀 GUI Başlat", 
                                  command=self.launch_gui,
                                  font=("Arial", 14, "bold"),
                                  bg="#27ae60", fg="white",
                                  width=15, height=2,
                                  relief=tk.RAISED, bd=3)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        # Çıkış düğmesi
        tk.Button(button_frame, text="❌ Çıkış", 
                 command=self.root.quit,
                 font=("Arial", 12), 
                 bg="#e74c3c", fg="white",
                 width=10, height=2,
                 relief=tk.RAISED, bd=3).pack(side=tk.RIGHT, padx=10)
        
        # İlk açıklama
        self.update_description()
        
    def update_description(self):
        """Seçime göre açıklama güncelle"""
        descriptions = {
            "eski": """🔄 ESKİ GUI (Yedeklerden Geri Getirilen)
            
• Orijinal tasarım ve düzen
• Alışık olduğunuz eski arayüz
• Yedekler klasöründen geri getirildi
• Basit ve tanıdık kullanım
• 14.07.2025 tarihli yedek versiyon""",
            
            "klasik": """📊 KLASİK GUI (Horizontal Layout)
            
• Sekme tabanlı modern düzen
• Solda genişletilmiş disk içeriği
• Sağda dikey düğme dizilimi
• Dosya önizleme sistemi
• Gelişmiş sütun düzeni""",
            
            "enhanced": """⚡ ENHANCED GUI (Modern)
            
• Radio button seçimler
• Gelişmiş checkbox'lar
• Son dosyalar entegrasyonu
• 24 klasör yapısı desteği
• py65 professional desteği"""
        }
        
        selected = self.gui_var.get()
        self.desc_label.configure(text=descriptions.get(selected, ""))
        
    def launch_gui(self):
        """Seçili GUI'yi başlat"""
        try:
            self.root.withdraw()
            
            selected = self.gui_var.get()
            
            if selected == "eski":
                # Yedeklerden geri getirilen eski GUI
                from eski_gui import D64ConverterGUI
                new_root = tk.Toplevel()
                app = D64ConverterGUI(new_root)
                
            elif selected == "klasik":
                # Horizontal layout klasik GUI
                from gui_restored import D64ConverterRestoredGUI
                new_root = tk.Toplevel()
                app = D64ConverterRestoredGUI(new_root)
                
            else:  # enhanced
                # Modern enhanced GUI
                from d64_converter import D64ConverterApp
                new_root = tk.Toplevel()
                app = D64ConverterApp(new_root)
            
            def on_close():
                new_root.destroy()
                self.root.deiconify()
            
            new_root.protocol("WM_DELETE_WINDOW", on_close)
            
        except Exception as e:
            messagebox.showerror("Hata", f"GUI başlatılamadı: {e}")
            self.root.deiconify()
    
    def run(self):
        """Çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🔄 Yuvarlak GUI Seçici başlatılıyor...")
    selector = YuvarlakGUISecici()
    selector.run()
