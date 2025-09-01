#!/usr/bin/env python3
"""
Simple test GUI for PAGE
PAGE visual designer ile bu dosyayı açıp düzenleyebilirsiniz.
"""

import tkinter as tk
from tkinter import ttk, messagebox

def create_simple_gui():
    """Create a simple GUI that PAGE can edit"""
    
    # Main window
    root = tk.Tk()
    root.title("D64 Converter - PAGE Test")
    root.geometry("800x600")
    root.configure(bg='#2b2b2b')
    
    # Main frame
    main_frame = tk.Frame(root, bg='#2b2b2b')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Title
    title_label = tk.Label(main_frame, text="D64 Converter - PAGE Edition", 
                          bg='#2b2b2b', fg='white', font=('Arial', 16, 'bold'))
    title_label.pack(pady=10)
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg='#2b2b2b')
    button_frame.pack(pady=20)
    
    # Buttons
    btn_open = tk.Button(button_frame, text="Open File", 
                        command=lambda: messagebox.showinfo("Test", "Open File clicked!"),
                        bg='#4c4c4c', fg='white', font=('Arial', 12))
    btn_open.pack(side=tk.LEFT, padx=10)
    
    btn_convert = tk.Button(button_frame, text="Convert", 
                           command=lambda: messagebox.showinfo("Test", "Convert clicked!"),
                           bg='#4c4c4c', fg='white', font=('Arial', 12))
    btn_convert.pack(side=tk.LEFT, padx=10)
    
    btn_analyze = tk.Button(button_frame, text="Analyze", 
                           command=lambda: messagebox.showinfo("Test", "Analyze clicked!"),
                           bg='#4c4c4c', fg='white', font=('Arial', 12))
    btn_analyze.pack(side=tk.LEFT, padx=10)
    
    # Text area
    text_frame = tk.Frame(main_frame, bg='#2b2b2b')
    text_frame.pack(fill=tk.BOTH, expand=True, pady=20)
    
    text_area = tk.Text(text_frame, bg='#1e1e1e', fg='white', 
                       font=('Consolas', 10), wrap=tk.WORD)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    # Insert sample text
    sample_text = """D64 Converter - PAGE Edition Test

Bu GUI PAGE visual designer ile düzenlenebilir.

PAGE kullanım adımları:
1. PAGE'i başlatın
2. Bu Python dosyasını açın (page_test_gui.py)
3. Visual editor ile widget'ları düzenleyin
4. Kodları otomatik güncellenir

Test butonları:
- Open File: Dosya açma dialogu
- Convert: Dönüştürme işlemi
- Analyze: Analiz fonksiyonu

Bu text area'yı da PAGE ile düzenleyebilirsiniz.
"""
    
    text_area.insert(1.0, sample_text)
    
    # Status bar
    status_bar = tk.Label(root, text="Ready - PAGE Test GUI", 
                         bg='#4c4c4c', fg='white', relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    return root

def main():
    """Main function"""
    print("🎯 PAGE Test GUI Starting...")
    print("📐 Open this file in PAGE visual designer")
    print("🔧 File: page_test_gui.py")
    
    root = create_simple_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
