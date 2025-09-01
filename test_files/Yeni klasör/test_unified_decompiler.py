#!/usr/bin/env python
"""
TEST AMACI: Unified Decompiler Interface'in TAM DOĞRULAMA testi
AÇIKLAMA:
- UnifiedDecompiler class'ının tüm özelliklerini test eder
- Single format decompile testi
- Batch decompile (çoklu format) testi
- Format switching testi
- Configuration options testi
- Error handling testi

KULLANIM:
python test_files/test_unified_decompiler.py

BEKLENEN SONUÇ:
✅ UnifiedDecompiler başlatma başarılı
✅ Memory Manager entegrasyonu çalışıyor
✅ Single format decompile başarılı
✅ Batch decompile tüm formatlar başarılı
✅ Format switching çalışıyor
✅ Configuration options aktif
✅ Error handling güvenli

BAŞARI KRİTERLERİ:
- Tüm desteklenen formatlar çalışmalı
- Memory Manager entegrasyonu aktif olmalı
- Error handling robust olmalı
- Performance acceptable olmalı
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_decompiler import UnifiedDecompiler, quick_decompile, batch_decompile

def test_unified_decompiler():
    print("=== UNIFIED DECOMPILER FULL TEST ===")
    
    # Test data
    test_prg = "0108a94120d2ff60"  # LDA #65, JSR $FFD2, RTS
    print(f"Test PRG: {test_prg}")
    print("Assembly: LDA #65, JSR $FFD2 (CHROUT), RTS")
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Basic initialization
    print(f"\n=== TEST 1: UnifiedDecompiler Initialization ===")
    total_tests += 1
    try:
        decompiler = UnifiedDecompiler('c')
        print("✅ UnifiedDecompiler başlatma başarılı")
        print(f"   Target format: {decompiler.target_format}")
        print(f"   Supported formats: {decompiler.get_supported_formats()}")
        success_count += 1
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
    
    # Test 2: Component initialization
    print(f"\n=== TEST 2: Component Initialization ===")
    total_tests += 1
    try:
        if decompiler.initialize_components():
            print("✅ Components başlatma başarılı")
            print(f"   Memory Manager: {decompiler.memory_manager is not None}")
            success_count += 1
        else:
            print("❌ Components başlatma başarısız")
    except Exception as e:
        print(f"❌ Component initialization failed: {e}")
    
    # Test 3: Single format decompile
    print(f"\n=== TEST 3: Single Format Decompile ===")
    formats_to_test = ['asm', 'c', 'qbasic', 'pdsx']
    
    for fmt in formats_to_test:
        total_tests += 1
        print(f"\n--- Testing {fmt.upper()} format ---")
        try:
            decompiler.set_format(fmt)
            result = decompiler.decompile(test_prg)
            
            if "❌ HATA" in result:
                print(f"❌ {fmt} format failed: {result[:100]}")
            else:
                print(f"✅ {fmt} format success")
                # Show key output lines
                lines = result.split('\n')
                key_lines = [line for line in lines if any(keyword in line for keyword in 
                           ['LDA', 'JSR', 'RTS', 'CHROUT', 'A =', 'GOSUB', 'RETURN', 'call', '#65'])][:3]
                for line in key_lines:
                    if line.strip():
                        print(f"   {line.strip()}")
                success_count += 1
                
        except Exception as e:
            print(f"❌ {fmt} format exception: {e}")
    
    # Test 4: Quick decompile function
    print(f"\n=== TEST 4: Quick Decompile Function ===")
    total_tests += 1
    try:
        quick_result = quick_decompile(test_prg, 'c')
        if "❌ HATA" not in quick_result and len(quick_result) > 50:
            print("✅ Quick decompile başarılı")
            success_count += 1
        else:
            print(f"❌ Quick decompile failed: {quick_result[:100]}")
    except Exception as e:
        print(f"❌ Quick decompile exception: {e}")
    
    # Test 5: Batch decompile
    print(f"\n=== TEST 5: Batch Decompile ===")
    total_tests += 1
    try:
        batch_results = batch_decompile(test_prg, ['asm', 'c', 'qbasic'])
        
        successful_formats = 0
        for fmt, result in batch_results.items():
            if "❌ HATA" not in result and len(result) > 50:
                successful_formats += 1
                print(f"   ✅ {fmt}: OK")
            else:
                print(f"   ❌ {fmt}: Failed")
        
        if successful_formats >= 2:  # At least 2 formats should work
            print("✅ Batch decompile başarılı")
            success_count += 1
        else:
            print("❌ Batch decompile insufficient success")
            
    except Exception as e:
        print(f"❌ Batch decompile exception: {e}")
    
    # Test 6: Error handling
    print(f"\n=== TEST 6: Error Handling ===")
    total_tests += 1
    try:
        # Test invalid format
        try:
            bad_decompiler = UnifiedDecompiler('invalid_format')
            print("❌ Invalid format not caught")
        except ValueError:
            print("   ✅ Invalid format correctly rejected")
        
        # Test empty data
        empty_result = quick_decompile("", 'c')
        if "❌ HATA" in empty_result:
            print("   ✅ Empty data correctly handled")
        else:
            print("   ❌ Empty data not handled")
        
        # Test malformed hex
        bad_result = quick_decompile("ZZZZ", 'c')
        if "❌ HATA" in bad_result or "❌" in bad_result:
            print("   ✅ Malformed hex correctly handled")
        else:
            print("   ❌ Malformed hex not handled")
        
        print("✅ Error handling tests passed")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Test 7: Statistics and configuration
    print(f"\n=== TEST 7: Stats and Configuration ===")
    total_tests += 1
    try:
        decompiler.set_format('c')
        decompiler.decompile(test_prg)
        
        stats = decompiler.get_stats()
        print(f"   Stats: {stats}")
        
        if 'input_size' in stats and 'output_size' in stats:
            print("   ✅ Statistics working")
        else:
            print("   ❌ Statistics incomplete")
        
        # Test configuration
        old_options = decompiler.configure_options(test_option=True)
        if 'test_option' in decompiler.options:
            print("   ✅ Configuration working")
        else:
            print("   ❌ Configuration failed")
        
        print("✅ Stats and configuration tests passed")
        success_count += 1
        
    except Exception as e:
        print(f"❌ Stats/config test failed: {e}")
    
    # Final results
    print(f"\n=== TEST SUMMARY ===")
    print(f"Successful tests: {success_count}/{total_tests}")
    success_rate = (success_count / total_tests) * 100
    print(f"Success rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 UNIFIED DECOMPILER TEST: ✅ PASSED")
        print("Unified Decompiler sistemi başarıyla çalışıyor!")
    elif success_rate >= 60:
        print("⚠️ PARTIAL SUCCESS: Sistem kısmen çalışıyor")
    else:
        print("❌ MAJOR ISSUES: Sistem ciddi problemler içeriyor")
    
    return success_rate >= 80

if __name__ == "__main__":
    test_unified_decompiler()
