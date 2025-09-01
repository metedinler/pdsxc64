#!/usr/bin/env python3
"""
Hızlı GUI Test ve Düzenleme Aracı
"""

import tkinter as tk
from tkinter import ttk
import sys
from pathlib import Path

def create_quick_gui_editor():
    """Hızlı GUI düzenleme aracı"""
    
    # Ana pencere
    root = tk.Tk()
    root.title("D64 Converter - Quick GUI Editor")
    root.geometry("800x600")
    root.configure(bg='#2b2b2b')
    
    # Stil
    style = ttk.Style()
    style.theme_use('clam')
    
    # Ana frame
    main_frame = tk.Frame(root, bg='#2b2b2b')
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Başlık
    title_label = tk.Label(
        main_frame,
        text="🎨 D64 Converter GUI Editor",
        bg='#2b2b2b',
        fg='#ffffff',
        font=('Segoe UI', 16, 'bold')
    )
    title_label.pack(pady=(0, 20))
    
    # Toolbar frame
    toolbar_frame = tk.Frame(main_frame, bg='#404040', relief='raised', bd=1)
    toolbar_frame.pack(fill='x', pady=(0, 10))
    
    # Toolbar butonları - DÜZENLENEBİLİR!
    toolbar_buttons = [
        ("📁 Open File", "#1a73e8"),
        ("⚙️ Settings", "#ff6b35"), 
        ("💾 Save All", "#28a745"),
        ("❓ Help", "#6f42c1")
    ]
    
    for i, (text, color) in enumerate(toolbar_buttons):
        btn = tk.Button(
            toolbar_frame,
            text=text,
            bg=color,
            fg='white',
            font=('Segoe UI', 10),
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=8,
            command=lambda t=text: print(f"Clicked: {t}")
        )
        btn.grid(row=0, column=i, padx=5, pady=5, sticky='w')
    
    # Ana içerik alanı
    content_frame = tk.Frame(main_frame, bg='#2b2b2b')
    content_frame.pack(fill='both', expand=True)
    
    # Sol panel - Dosya ağacı
    left_frame = tk.Frame(content_frame, bg='#353535', width=300)
    left_frame.pack(side='left', fill='y', padx=(0, 10))
    left_frame.pack_propagate(False)
    
    tk.Label(
        left_frame,
        text="📁 File Explorer",
        bg='#353535',
        fg='#ffffff',
        font=('Segoe UI', 12, 'bold')
    ).pack(pady=10)
    
    # Dosya listesi
    file_listbox = tk.Listbox(
        left_frame,
        bg='#404040',
        fg='#ffffff',
        selectbackground='#1a73e8',
        font=('Consolas', 10),
        relief='flat',
        borderwidth=0
    )
    file_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    # Test dosyaları
    test_files = [
        "📁 MYDISK.D64",
        "📄 GAME.PRG",
        "📄 LOADER.PRG", 
        "📄 SPRITES.PRG",
        "📄 MUSIC.SID",
        "📄 CHARSET.PRG"
    ]
    
    for file_name in test_files:
        file_listbox.insert('end', file_name)
    
    # Sağ panel - Çıktı alanı
    right_frame = tk.Frame(content_frame, bg='#353535')
    right_frame.pack(side='right', fill='both', expand=True)
    
    tk.Label(
        right_frame,
        text="💻 Disassembly Output",
        bg='#353535',
        fg='#ffffff',
        font=('Segoe UI', 12, 'bold')
    ).pack(pady=10)
    
    # Çıktı metin alanı
    output_text = tk.Text(
        right_frame,
        bg='#1e1e1e',
        fg='#ffffff',
        insertbackground='#ffffff',
        font=('Consolas', 10),
        relief='flat',
        borderwidth=0,
        wrap='none'
    )
    output_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    # Test çıktısı
    test_output = """
; D64 Converter - Professional Decompiler
; Generated: 2025-07-27 14:30:00

*=$0801        ; BASIC Start
BASIC_START:
    .WORD $080B    ; Next line
    .WORD $000A    ; Line 10
    .BYTE $9E      ; SYS token
    .TEXT "2064"   ; SYS 2064
    .BYTE $00      ; End line
    
*=$0810        ; ML Start
MAIN_PROGRAM:
    LDA #$00       ; Clear A
    STA $D020      ; Border black
    STA $D021      ; Background black
    
GAME_LOOP:
    JSR $FFE4      ; Get key
    BEQ GAME_LOOP  ; No key = loop
    RTS            ; Return
"""
    
    output_text.insert('1.0', test_output)
    
    # Alt panel - Kontroller
    bottom_frame = tk.Frame(main_frame, bg='#404040', height=60)
    bottom_frame.pack(fill='x', pady=(10, 0))
    bottom_frame.pack_propagate(False)
    
    # Action butonları - DÜZENLENEBİLİR!
    action_buttons = [
        ("🔍 Analyze", "#17a2b8"),
        ("⚙️ Disassemble", "#ffc107"),
        ("🔄 Transpile", "#28a745"),
        ("📊 Report", "#dc3545")
    ]
    
    for i, (text, color) in enumerate(action_buttons):
        btn = tk.Button(
            bottom_frame,
            text=text,
            bg=color,
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            borderwidth=0,
            padx=25,
            pady=10,
            command=lambda t=text: print(f"Action: {t}")
        )
        btn.grid(row=0, column=i, padx=10, pady=10, sticky='w')
    
    # Bilgi labeli
    info_label = tk.Label(
        main_frame,
        text="💡 Bu bir düzenlenebilir GUI prototipidir. Buton renklerini ve pozisyonlarını değiştirebilirsiniz!",
        bg='#2b2b2b',
        fg='#888888',
        font=('Segoe UI', 9)
    )
    info_label.pack(pady=10)
    
    # Düzenleme talimatları
    instructions = tk.Text(
        main_frame,
        height=4,
        bg='#1e1e1e',
        fg='#00ff00',
        font=('Consolas', 9),
        relief='flat',
        borderwidth=0
    )
    instructions.pack(fill='x', pady=(10, 0))
    
    instruction_text = """
# DÜZENLEME TALİMATLARI:
# 1. PyGubu Designer'ı aç: pygubu-designer
# 2. gui_designs/d64_converter_improved.ui dosyasını yükle
# 3. Butonları sürükle-bırak ile taşı
# 4. Renkleri Properties panelinden değiştir
"""
    instructions.insert('1.0', instruction_text)
    instructions.config(state='disabled')
    
    return root

def main():
    """Ana fonksiyon"""
    print("🎨 Quick GUI Editor Starting...")
    print("=" * 40)
    print("✅ Creating interactive GUI prototype")
    print("💡 This shows how your GUI could look")
    print("🔧 Use PyGubu Designer for actual editing")
    print()
    
    # GUI'yi oluştur ve göster
    app = create_quick_gui_editor()
    
    print("🚀 GUI Editor Window Opened!")
    print("   • Close window to exit")
    print("   • Try clicking the buttons")
    print("   • See console for click events")
    
    app.mainloop()
    
    print("\n🎉 Quick GUI Editor Closed!")

if __name__ == "__main__":
    main()
