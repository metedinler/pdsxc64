#!/usr/bin/env python3
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from d64_converter import main
    print("D64 Converter başlatılıyor...")
    main()
except Exception as e:
    print(f"HATA: {e}")
    import traceback
    traceback.print_exc()
    input("Enter tuşuna basarak çıkın...")
