#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def create_test_prg():
    """Test için basit bir PRG dosyası oluştur"""
    
    # Basit bir C64 programı:
    # LDA #$01    ; A = 1
    # STA $D020   ; Border color = A
    # LDA #$0E    ; A = 14 (light blue)
    # STA $D021   ; Background color = A
    # RTS         ; Return
    
    prg_data = bytes([
        0x00, 0x08,        # Start address: $0800
        0xA9, 0x01,        # LDA #$01
        0x8D, 0x20, 0xD0,  # STA $D020
        0xA9, 0x0E,        # LDA #$0E  
        0x8D, 0x21, 0xD0,  # STA $D021
        0x60               # RTS
    ])
    
    # PRG dosyasını kaydet
    with open('test_program.prg', 'wb') as f:
        f.write(prg_data)
    
    print("Test PRG dosyası oluşturuldu: test_program.prg")
    print(f"Dosya boyutu: {len(prg_data)} bytes")
    
    return 'test_program.prg'

if __name__ == "__main__":
    create_test_prg()
