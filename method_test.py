#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basit Metod Test
"""

def test_method_existence():
    print("Metod varlık testi...")
    
    # Metod satır numarasını bulalım
    with open('pdsxv12xNEW.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # _initialize_libx_gui metodunu arayalım
    for i, line in enumerate(lines):
        if '_initialize_libx_gui' in line and 'def' in line:
            print(f"Metod bulundu satır {i+1}: {line.strip()}")
            
            # Önceki satırları kontrol et (indentation için)
            for j in range(max(0, i-5), i):
                print(f"  {j+1}: {repr(lines[j])}")
            
            # Sonraki satırları kontrol et
            for j in range(i, min(len(lines), i+5)):
                print(f"  {j+1}: {repr(lines[j])}")
                
            # Indentation analizi
            method_indent = len(line) - len(line.lstrip())
            print(f"Metod indentation: {method_indent} space")
            
            # Sınıf tanımını arayalım
            for k in range(i-1, -1, -1):
                if lines[k].strip().startswith('class '):
                    class_indent = len(lines[k]) - len(lines[k].lstrip())
                    print(f"Sınıf bulundu satır {k+1}: {lines[k].strip()}")
                    print(f"Sınıf indentation: {class_indent} space")
                    print(f"Metod sınıf içinde mi: {method_indent > class_indent}")
                    break
                elif lines[k].strip() and not lines[k].startswith(' ') and not lines[k].startswith('#'):
                    print(f"Sınıf dışı tanım bulundu satır {k+1}: {lines[k].strip()}")
                    break
            break
    else:
        print("❌ _initialize_libx_gui metodu bulunamadı!")

if __name__ == "__main__":
    test_method_existence()
