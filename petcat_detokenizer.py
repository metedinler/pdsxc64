#!/usr/bin/env python3
"""
Petcat Detokenizer Wrapper
VICE emülatörü ile gelen petcat aracını kullanarak BASIC detokenization
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path

class PetcatDetokenizer:
    def __init__(self):
        self.petcat_path = self.find_petcat()
        self.available = self.petcat_path is not None
        
    def find_petcat(self):
        """VICE entegrasyonu ile Petcat executable'ını bul"""
        print("[PETCAT] Petcat aranıyor...")
        
        # 1. VICE detector entegrasyonu - Global kontrol
        if 'VICE_DETECTOR' in globals():
            vice_detector = globals()['VICE_DETECTOR']
            if hasattr(vice_detector, 'vice_info'):
                petcat_path = vice_detector.vice_info.get('petcat_path')
                if petcat_path and os.path.exists(petcat_path):
                    print(f"[PETCAT] VICE global entegrasyonu: {petcat_path}")
                    return petcat_path
        
        # 2. VICE detector modülü dinamik yükleme
        try:
            from vice_detector import VICEDetector
            detector = VICEDetector()
            if detector.detect_vice():
                petcat_path = detector.vice_info.get('petcat_path')
                if petcat_path and os.path.exists(petcat_path):
                    print(f"[PETCAT] VICE detector modülü: {petcat_path}")
                    return petcat_path
        except Exception as e:
            print(f"[PETCAT] VICE detector yükleme hatası: {e}")
        
        # 3. Mevcut dizinde
        if os.path.exists("petcat.exe"):
            path = os.path.abspath("petcat.exe")
            print(f"[PETCAT] Mevcut dizinde bulundu: {path}")
            return path
        
        # 4. Configuration Manager entegrasyonu (VICE path)
        try:
            from configuration_manager import ConfigurationManager
            config_manager = ConfigurationManager()
            
            # VICE kurulum yolunu kontrol et
            if hasattr(config_manager, 'get_vice_path'):
                vice_base = config_manager.get_vice_path()
                if vice_base:
                    petcat_candidates = [
                        os.path.join(vice_base, 'bin', 'petcat.exe'),
                        os.path.join(vice_base, 'petcat.exe'),
                        os.path.join(vice_base, '..', 'bin', 'petcat.exe')  # bin klasörü üst dizinde
                    ]
                    
                    for candidate in petcat_candidates:
                        if os.path.exists(candidate):
                            print(f"[PETCAT] Configuration Manager entegrasyonu: {candidate}")
                            return candidate
                            
        except Exception as e:
            print(f"[PETCAT] Configuration Manager entegrasyonu hatası: {e}")
            
        # 5. Bilinen VICE path (log kayıtlarından)
        known_vice_path = r"C:\Users\dell\Downloads\commodore64 icin\GTK3VICE-3.9-win64\GTK3VICE-3.9-win64\bin\x64sc.exe"
        if os.path.exists(known_vice_path):
            vice_dir = os.path.dirname(known_vice_path)
            petcat_path = os.path.join(vice_dir, 'petcat.exe')
            if os.path.exists(petcat_path):
                print(f"[PETCAT] Bilinen VICE path'ten bulundu: {petcat_path}")
                return petcat_path
        # 6. Gelişmiş VICE kurulum dizinleri
        import platform
        system = platform.system().lower()
        
        if system == 'windows':
            # Windows için genişletilmiş arama
            drive_letters = ['C:', 'D:', 'E:', 'F:']
            base_paths = [
                r'\Program Files\WinVICE-3.8-x64\bin\petcat.exe',
                r'\Program Files\WinVICE-3.7-x64\bin\petcat.exe',
                r'\Program Files\WinVICE-3.6-x64\bin\petcat.exe',
                r'\Program Files\WinVICE\bin\petcat.exe',
                r'\Program Files\VICE\bin\petcat.exe',
                r'\Program Files (x86)\WinVICE-3.8-x64\bin\petcat.exe',
                r'\Program Files (x86)\WinVICE-3.7-x64\bin\petcat.exe',
                r'\Program Files (x86)\WinVICE\bin\petcat.exe',
                r'\Program Files (x86)\VICE\bin\petcat.exe',
                r'\VICE\bin\petcat.exe',
                r'\vice\petcat.exe',
                r'\tools\vice\petcat.exe'
            ]
            
            for drive in drive_letters:
                for base_path in base_paths:
                    full_path = drive + base_path
                    if os.path.exists(full_path):
                        print(f"[PETCAT] Windows'ta bulundu: {full_path}")
                        return full_path
        else:
            # Linux/macOS
            unix_paths = [
                "/usr/bin/petcat",
                "/usr/local/bin/petcat",
                "/opt/vice/bin/petcat",
                "/opt/homebrew/bin/petcat",
                f"/home/{os.getenv('USER', '')}/.local/bin/petcat"
            ]
            
            for path in unix_paths:
                if os.path.exists(path):
                    print(f"[PETCAT] Unix'te bulundu: {path}")
                    return path
        
        # 5. PATH'te ara - Windows
        try:
            result = subprocess.run(["where", "petcat"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                path = result.stdout.strip().split('\n')[0]
                print(f"[PETCAT] PATH'te bulundu (where): {path}")
                return path
        except:
            pass
        
        # 6. PATH'te ara - Unix
        try:
            result = subprocess.run(["which", "petcat"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                path = result.stdout.strip()
                print(f"[PETCAT] PATH'te bulundu (which): {path}")
                return path
        except:
            pass
        
        # 7. shutil.which ile sistem PATH
        import shutil
        petcat_path = shutil.which('petcat')
        if petcat_path:
            print(f"[PETCAT] shutil.which ile bulundu: {petcat_path}")
            return petcat_path
            
        petcat_path = shutil.which('petcat.exe')
        if petcat_path:
            print(f"[PETCAT] shutil.which ile bulundu (.exe): {petcat_path}")
            return petcat_path
        
        print("[PETCAT] ❌ Petcat bulunamadı!")
        return None
    
    def download_petcat(self):
        """Petcat'i indir (VICE'dan)"""
        # Bu method main.py'dan çağrılacak
        print("Petcat bulunamadı. VICE indirmesi gerekiyor...")
        print("VICE indirme bağlantısı: http://vice-emu.sourceforge.net/")
        return False
    
    def detokenize_prg(self, prg_data):
        """PRG verisini petcat ile detokenize et - Enhanced error handling"""
        if not self.available:
            error_msg = "ERROR: petcat bulunamadı. VICE emülatörü kurulu değil."
            print(f"[PETCAT] {error_msg}")
            return [error_msg]
        
        try:
            print(f"[PETCAT] Starting detokenization, data size: {len(prg_data)} bytes")
            
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(suffix='.prg', delete=False) as temp_prg:
                temp_prg.write(prg_data)
                temp_prg_path = temp_prg.name
            
            print(f"[PETCAT] Temp PRG created: {temp_prg_path}")
            
            # Çıktı dosyası
            temp_out_path = temp_prg_path + ".txt"
            
            # Petcat komutunu çalıştır - Çıktı dosyası ile
            cmd = [self.petcat_path, "-w2", "-o", temp_out_path, temp_prg_path]
            print(f"[PETCAT] Running command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            print(f"[PETCAT] Return code: {result.returncode}")
            if result.stdout:
                print(f"[PETCAT] STDOUT: {repr(result.stdout)}")
            if result.stderr:
                print(f"[PETCAT] STDERR: {result.stderr}")
            
            # Çıktı dosyasını kontrol et (petcat genelde dosyaya yazar)
            if result.returncode == 0 and os.path.exists(temp_out_path):
                # Dosyadan oku
                try:
                    with open(temp_out_path, 'r', encoding='ascii', errors='ignore') as f:
                        lines = f.readlines()
                    
                    print(f"[PETCAT] Successfully read {len(lines)} lines from output file")
                    
                    # Geçici dosyaları temizle
                    os.unlink(temp_prg_path)
                    os.unlink(temp_out_path)
                    
                    if lines:
                        clean_lines = []
                        for line in lines:
                            clean_line = line.rstrip()
                            if clean_line:
                                # PETSCII karakterleri ASCII'ye çevir
                                clean_line = self.petscii_to_ascii(clean_line)
                                if clean_line:
                                    clean_lines.append(clean_line)
                        return clean_lines if clean_lines else ["[PETCAT] Empty output after cleaning"]
                    else:
                        return ["[PETCAT] Output file was empty"]
                except Exception as read_error:
                    print(f"[PETCAT] File read error: {read_error}")
                    return [f"ERROR: Could not read output file: {read_error}"]
            elif result.stdout:
                # Stdout fallback
                lines = result.stdout.split('\n')
                print(f"[PETCAT] Using STDOUT as fallback: {len(lines)} lines")
                clean_lines = []
                for line in lines:
                    if line.strip():
                        clean_line = self.petscii_to_ascii(line.strip())
                        if clean_line:
                            clean_lines.append(clean_line)
                return clean_lines if clean_lines else ["[PETCAT] Empty STDOUT output"]
            else:
                # Hata durumu
                error_msg = result.stderr if result.stderr else f"Petcat failed with code {result.returncode}"
                print(f"[PETCAT] Command failed: {error_msg}")
                return [f"ERROR: {error_msg}"]
                
        except subprocess.TimeoutExpired:
            print("[PETCAT] Command timed out")
            return ["ERROR: Petcat timeout (30s)"]
        except Exception as e:
            print(f"[PETCAT] Exception occurred: {str(e)}")
            import traceback
            print(f"[PETCAT] Traceback: {traceback.format_exc()}")
            return [f"ERROR: Petcat exception: {str(e)}"]
        finally:
            # Geçici dosyaları temizle
            try:
                if 'temp_prg_path' in locals() and os.path.exists(temp_prg_path):
                    os.unlink(temp_prg_path)
                    print(f"[PETCAT] Cleaned temp PRG: {temp_prg_path}")
                if 'temp_out_path' in locals() and os.path.exists(temp_out_path):
                    os.unlink(temp_out_path)
                    print(f"[PETCAT] Cleaned temp output: {temp_out_path}")
            except Exception as cleanup_error:
                print(f"[PETCAT] Cleanup error: {cleanup_error}")

    def petscii_to_ascii(self, petscii_text):
        """PETSCII karakterlerini ASCII'ye çevir"""
        # Basit PETSCII-ASCII çevirisi
        translation_table = {
            'Ç': 'A', 'ü': 'B', 'é': 'C', 'â': 'D', 'ä': 'E', 'à': 'F', 'å': 'G', 'ç': 'H',
            'ê': 'I', 'ë': 'J', 'è': 'K', 'ï': 'L', 'î': 'M', 'ì': 'N', 'Ä': 'O', 'Å': 'P',
            'É': 'Q', 'æ': 'R', 'Æ': 'S', 'ô': 'T', 'ö': 'U', 'ò': 'V', 'û': 'W', 'ù': 'X',
            'ÿ': 'Y', 'Ö': 'Z',
            'È': 'H', 'Å': 'A', 'Ì': 'L', 'Ì': 'L', 'Ï': 'O',
            '—': 'PRINT'  # PRINT token özel çevirisi
        }
        
        result = petscii_text
        for petscii_char, ascii_char in translation_table.items():
            result = result.replace(petscii_char, ascii_char)
        
        # Kontrol karakterlerini temizle
        result = ''.join(char for char in result if ord(char) >= 32 or char in ['\n', '\t'])
        
        return result.strip()

    def tokenize_text(self, basic_text):
        """BASIC metnini tokenize et"""
        if not self.available:
            return None
        
        try:
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(mode='w', suffix='.bas', delete=False) as temp_bas:
                temp_bas.write(basic_text)
                temp_bas_path = temp_bas.name
            
            # Çıktı dosyası
            temp_prg_path = temp_bas_path + ".prg"
            
            # Petcat komutunu çalıştır
            cmd = [self.petcat_path, "-w2", "-o", temp_prg_path, "--", temp_bas_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(temp_prg_path):
                # PRG verisini oku
                with open(temp_prg_path, 'rb') as f:
                    prg_data = f.read()
                
                # Geçici dosyaları temizle
                os.unlink(temp_bas_path)
                os.unlink(temp_prg_path)
                
                return prg_data
            else:
                return None
                
        except Exception as e:
            return None
        finally:
            # Geçici dosyaları temizle
            try:
                if 'temp_bas_path' in locals():
                    os.unlink(temp_bas_path)
                if 'temp_prg_path' in locals() and os.path.exists(temp_prg_path):
                    os.unlink(temp_prg_path)
            except:
                pass

    def get_status(self):
        """Petcat durumunu al"""
        if self.available:
            return f"✅ Petcat available: {self.petcat_path}"
        else:
            return "❌ Petcat not found - VICE emulator required"

# Test function
def test_petcat():
    """Test petcat detokenizer"""
    print("🔍 Testing Petcat Detokenizer")
    
    detokenizer = PetcatDetokenizer()
    print(detokenizer.get_status())
    
    if detokenizer.available:
        # Test data: 10 PRINT "HELLO"
        test_data = bytes([
            0x01, 0x08,  # Load address $0801
            0x0B, 0x08,  # Next line address
            0x0A, 0x00,  # Line number 10
            0x99, 0x22,  # PRINT "
            0x48, 0x45, 0x4C, 0x4C, 0x4F,  # HELLO
            0x22, 0x00,  # " and line end
            0x00, 0x00   # Program end
        ])
        
        lines = detokenizer.detokenize_prg(test_data)
        print("Petcat Detokenization Result:")
        for line in lines:
            print(f"  {line}")
    else:
        print("Petcat not available for testing")

if __name__ == "__main__":
    test_petcat()
