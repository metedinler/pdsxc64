"""
D64 Converter - Basit GUI Selector (Test)
"""

import tkinter as tk
from tkinter import messagebox

def launch_classic():
    """Classic GUI'yi başlat"""
    print("🎨 Classic GUI başlatılıyor...")
    try:
        import subprocess
        subprocess.run(["python", "gui_restored.py"])
    except Exception as e:
        messagebox.showerror("Hata", f"Classic GUI başlatılamadı: {e}")

def launch_enhanced():
    """Enhanced GUI'yi başlat"""
    print("⚡ Enhanced GUI başlatılıyor...")
    try:
        import subprocess
        subprocess.run(["python", "d64_converter.py"])
    except Exception as e:
        messagebox.showerror("Hata", f"Enhanced GUI başlatılamadı: {e}")

# Ana pencere
root = tk.Tk()
root.title("D64 Converter - GUI Seçici")
root.geometry("500x300")
root.configure(bg="#2C3E50")

# Header
header = tk.Label(root, text="D64 Converter", 
                 font=("Arial", 20, "bold"), 
                 fg="white", bg="#2C3E50")
header.pack(pady=20)

subtitle = tk.Label(root, text="Professional C64 Disassembler Suite", 
                   font=("Arial", 10), 
                   fg="#BDC3C7", bg="#2C3E50")
subtitle.pack()

# Düğmeler frame
buttons_frame = tk.Frame(root, bg="#2C3E50")
buttons_frame.pack(expand=True, fill=tk.BOTH, pady=30)

# Classic GUI düğmesi
classic_btn = tk.Button(buttons_frame, 
                       text="🎨 Classic GUI\n(TAB-based, File Analysis)",
                       command=launch_classic,
                       bg="#3498DB", fg="white", 
                       font=("Arial", 12, "bold"),
                       width=25, height=3,
                       relief=tk.RAISED, bd=5)
classic_btn.pack(pady=10)

# Enhanced GUI düğmesi  
enhanced_btn = tk.Button(buttons_frame,
                        text="⚡ Enhanced GUI\n(Radio buttons, Advanced)",
                        command=launch_enhanced,
                        bg="#27AE60", fg="white",
                        font=("Arial", 12, "bold"),
                        width=25, height=3,
                        relief=tk.RAISED, bd=5)
enhanced_btn.pack(pady=10)

# Exit düğmesi
exit_btn = tk.Button(buttons_frame,
                    text="❌ Exit",
                    command=root.quit,
                    bg="#E74C3C", fg="white",
                    font=("Arial", 10, "bold"),
                    width=15, height=1)
exit_btn.pack(pady=20)

print("🎯 GUI Selector başlatılıyor...")
root.mainloop()
