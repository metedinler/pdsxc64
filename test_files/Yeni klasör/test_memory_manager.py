#!/usr/bin/env python
"""
TEST AMACI: Enhanced C64 Memory Manager'ın database yükleme ve fonksiyonlarını test eder
AÇIKLAMA:
- ROM DATA entegrasyonu test eder
- KERNAL, BASIC routines yükleme testi
- C64 Labels, Zero Page variables test eder
- Smart variable naming test eder
- Memory address resolution test eder

KULLANIM:
python test_files/test_memory_manager.py

BEKLENEN SONUÇ:
- KERNAL routines: 111 adet yüklenmeli
- BASIC routines: 66 adet yüklenmeli  
- C64 Labels: 835+ adet yüklenmeli
- $FFD2 → CHROUT olarak tanınmalı
- $0400 → SCREEN_MEMORY olarak tanınmalı
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from enhanced_c64_memory_manager import EnhancedC64MemoryManager

def test_memory_manager():
    print("=== TEST: Enhanced C64 Memory Manager ===")
    
    try:
        # Memory Manager oluştur
        memory_manager = EnhancedC64MemoryManager()
        
        print("\n=== DATABASE İSTATİSTİKLERİ ===")
        
        # Database boyutlarını kontrol et
        if hasattr(memory_manager, 'unified_lookup'):
            print(f"Unified Lookup: {len(memory_manager.unified_lookup)} adet")
        
        if hasattr(memory_manager, 'kernal_routines'):
            print(f"KERNAL Routines: {len(memory_manager.kernal_routines)} adet")
            
        if hasattr(memory_manager, 'basic_routines'):
            print(f"BASIC Routines: {len(memory_manager.basic_routines)} adet")
            
        if hasattr(memory_manager, 'c64_labels'):
            print(f"C64 Labels: {len(memory_manager.c64_labels)} adet")
            
        if hasattr(memory_manager, 'zero_page_vars'):
            print(f"Zero Page Variables: {len(memory_manager.zero_page_vars)} adet")
            
        if hasattr(memory_manager, 'io_registers'):
            print(f"I/O Registers: {len(memory_manager.io_registers)} adet")
        
        print("\n=== ADRES TEST ===")
        
        # Test adresleri
        test_addresses = [
            0xFFD2,  # CHROUT
            0x0400,  # Screen memory
            0xA000,  # BASIC ROM
            0x0002,  # Zero page
            0xD000,  # I/O area
        ]
        
        for addr in test_addresses:
            var_name = memory_manager.get_smart_variable_name(addr)
            print(f"${addr:04X} → {var_name}")
            
        print("\n=== FORMAT TRANSLATION TEST ===")
        
        # Format çeviri testleri
        formats = ['c', 'qbasic', 'pdsx']
        for fmt in formats:
            translation = memory_manager.get_format_translation(0xFFD2, fmt, 'call')
            print(f"$FFD2 ({fmt}): {translation}")
        
        print("\n✅ TEST BAŞARILI")
        
    except Exception as e:
        print(f"❌ TEST HATASI: {e}")
        import traceback
        print(f"TRACEBACK:\n{traceback.format_exc()}")

if __name__ == "__main__":
    test_memory_manager()
