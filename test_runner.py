# PDSX v12X Test Runner
# Tüm test dosyalarını sırasıyla çalıştırır

import subprocess
import sys
import os

test_files = [
    "test_01_basic_commands.pdsx",
    "test_02_advanced_programming.pdsx", 
    "test_03_database_api.pdsx",
    "test_04_scientific_math.pdsx",
    "test_05_system_hardware.pdsx",
    "test_06_gui_c64_basic.pdsx",
    "test_07_advanced_graphics.pdsx",
    "test_08_games_interactive.pdsx",
    "test_09_advanced_integration.pdsx",
    "test_10_final_comprehensive.pdsx",
    "test_c64_comprehensive.pdsx"
]

def run_test(test_file):
    """Tek test dosyasını çalıştır"""
    print(f"\n{'='*60}")
    print(f"Test çalıştırılıyor: {test_file}")
    print(f"{'='*60}")
    
    try:
        # Test dosyasını çalıştır (30 saniye timeout)
        result = subprocess.run(
            [sys.executable, "pdsxv12xNEW.py", f"testpdsx/{test_file}"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.getcwd()
        )
        
        print("📋 STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return Code: {result.returncode}")
        
        # PDSX hatası varsa test başarısız sayılır
        has_pdsx_error = "PDSX Hatası:" in result.stdout
        
        if result.returncode == 0 and not has_pdsx_error:
            print("Test başarıyla tamamlandı")
            return True
        else:
            if has_pdsx_error:
                print("Test başarısız - PDSX hatası tespit edildi")
            else:
                print("Test başarısız - Exit code != 0")
            return False
            
    except subprocess.TimeoutExpired:
        print("Test zaman aşımına uğradı (30 saniye)")
        return False
    except Exception as e:
        print(f"💥 Test çalıştırma hatası: {e}")
        return False

def main():
    """Ana test runner"""
    print("PDSX v12X Test Suite Başlatılıyor...")
    
    results = {}
    passed = 0
    failed = 0
    
    for test_file in test_files:
        success = run_test(test_file)
        results[test_file] = success
        
        if success:
            passed += 1
        else:
            failed += 1
    
    # Özet rapor
    print(f"\n{'='*60}")
    print(f"TEST SONUÇ ÖZETİ")
    print(f"{'='*60}")
    
    for test_file, success in results.items():
        status = "PASSED" if success else "FAILED"
        print(f"{test_file}: {status}")
    
    print(f"\nİstatistikler:")
    print(f"Başarılı: {passed}")
    print(f"Başarısız: {failed}")
    print(f"Toplam: {len(test_files)}")
    print(f"Başarı Oranı: {(passed/len(test_files)*100):.1f}%")

if __name__ == "__main__":
    main()
