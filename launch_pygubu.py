"""
launch_pygubu.py
Bu betik, pygubu-designer'ı başlatır.
Sanal ortam kurulu olmalı.
"""

import subprocess
import sys
import os

def main():
    # Sanal ortam Scripts klasörünü belirle
    if sys.platform == "win32":
        designer_path = os.path.join("venv_pygubu", "Scripts", "pygubu-designer.exe")
    else:
        designer_path = os.path.join("venv_pygubu", "bin", "pygubu-designer")

    # Eğer exe dosyası varsa doğrudan çalıştır
    if os.path.exists(designer_path):
        print(f"PyGubu Designer başlatılıyor: {designer_path}")
        subprocess.run([designer_path], shell=True)
    else:
        # Alternatif: modül olarak çalıştır
        print("PyGubu Designer exe bulunamadı, modül olarak başlatılıyor...")
        subprocess.run([sys.executable, "-m", "pygubu"])

if __name__ == "__main__":
    main()