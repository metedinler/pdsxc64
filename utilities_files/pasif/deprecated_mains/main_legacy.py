#!/usr/bin/env python3
"""
D64 Converter - 6502 Assembly Reverse Compiler
Gelişmiş komut satırı arayüzü ve tam logging sistemi
"""

import subprocess
import sys
import importlib.util
import os
import venv
import platform
import argparse
import logging
import datetime
import json
import shutil
from pathlib import Path

def setup_logging(log_level="INFO", log_file=None):
    """
    Detaylı logging sistemi kurulumu
    """
    # Logs klasörünü oluştur
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Log dosyası ismi
    if log_file is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"d64_converter_{timestamp}.log"
    
    # Logging formatı
    log_format = '%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
    
    # Logging seviyesi
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Geçersiz log seviyesi: {log_level}')
    
    # Root logger'ı yapılandır
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging sistemi başlatıldı: {log_file}")
    logger.info(f"Log seviyesi: {log_level}")
    
    return logger

def create_output_directories():
    """
    Çıktı klasörlerini oluştur
    """
    output_dirs = [
        "asm_files",
        "c_files", 
        "qbasic_files",
        "pdsx_files",
        "pseudo_files",
        "commodore_basic_files",
        "logs",
        "png_files",
        "sid_files",
        "prg_files",
        "test_files",
        "utilities_files/aktif",
        "utilities_files/pasif"
    ]
    
    for dirname in output_dirs:
        Path(dirname).mkdir(parents=True, exist_ok=True)
        logging.info(f"Çıktı klasörü oluşturuldu: {dirname}")

def save_system_info():
    """
    Sistem bilgilerini kaydet
    """
    system_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "platform": platform.platform(),
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "python_executable": sys.executable,
        "environment_variables": dict(os.environ),
        "installed_packages": []
    }
    
    try:
        # Yüklü paketleri al
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            system_info["installed_packages"] = result.stdout.split('\n')
    except Exception as e:
        logging.warning(f"Yüklü paketler alınamadı: {e}")
    
    # Sistem bilgilerini kaydet
    with open("logs/system_info.json", "w", encoding="utf-8") as f:
        json.dump(system_info, f, indent=2, ensure_ascii=False)
    
    logging.info("Sistem bilgileri kaydedildi: logs/system_info.json")

def create_virtual_environment(venv_path):
    """
    Proje için özel sanal dizin oluştur ve aktif et
    """
    logger = logging.getLogger(__name__)

    if os.path.exists(venv_path):
        logger.info(f"Sanal dizin zaten mevcut: {venv_path}")
    else:
        logger.info("Sanal dizin oluşturuluyor...")
        try:
            venv.create(venv_path, with_pip=True)
            logger.info(f"Sanal dizin başarıyla oluşturuldu: {venv_path}")
        except Exception as e:
            logger.error(f"Sanal dizin oluşturulurken hata: {e}")
            return False

    # Sanal ortamı aktif et
    activate_script = os.path.join(venv_path, "Scripts", "activate") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "activate")
    if os.path.exists(activate_script):
        logger.info(f"Sanal ortam aktif ediliyor: {activate_script}")
        os.environ["VIRTUAL_ENV"] = venv_path
        os.environ["PATH"] = os.path.join(venv_path, "Scripts") + os.pathsep + os.environ["PATH"]
        return True
    else:
        logger.error("Sanal ortam aktif edilemedi: activate script bulunamadı")
        return False

def get_venv_python_executable(venv_path):
    """
    Sanal dizindeki Python çalıştırılabilir dosyasının yolunu al
    """
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")

def get_venv_pip_executable(venv_path):
    """
    Sanal dizindeki pip çalıştırılabilir dosyasının yolunu al
    """
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_path, "bin", "pip")

def install_required_packages(venv_path):
    """
    Gerekli paketleri sanal dizine yükle
    """
    logger = logging.getLogger(__name__)

    packages = [
        "tkinterdnd2",
        "py65",
        "pillow",
        "numpy"
    ]

    pip_exe = get_venv_pip_executable(venv_path)

    for package in packages:
        try:
            logger.info(f"Paket yükleniyor: {package}")
            result = subprocess.run([pip_exe, "install", package], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                logger.info(f"Paket başarıyla yüklendi: {package}")
            else:
                logger.warning(f"Paket yüklenemedi: {package}")
                logger.warning(f"Hata: {result.stderr}")
        except Exception as e:
            logger.error(f"Paket yükleme hatası {package}: {e}")

    # Pillow modülünü kontrol et
    venv_python = get_venv_python_executable(venv_path)
    
    try:
        # Sanal ortam Python'u ile PIL modülünü test et
        result = subprocess.run([venv_python, "-c", "import PIL; print('PIL import successful')"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logger.info("Pillow modülü başarıyla yüklendi.")
        else:
            raise ImportError("PIL modülü yüklenemedi")
    except:
        logger.error("Pillow modülü yüklenemedi, yeniden yükleniyor...")
        result = subprocess.run([pip_exe, "install", "--force-reinstall", "Pillow"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logger.info("Pillow modülü başarıyla yeniden yüklendi.")
            # Tekrar test et
            result = subprocess.run([venv_python, "-c", "import PIL; print('PIL import successful')"], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                logger.info("Pillow modülü test başarılı.")
            else:
                logger.error("Pillow modülü yeniden yüklenmesine rağmen çalışmıyor.")
        else:
            logger.error("Pillow modülü yeniden yüklenemedi.")
            logger.error(f"Hata: {result.stderr}")

    return True

def run_converter_with_args(args, venv_path):
    """
    Converter'ı belirtilen argümanlarla çalıştır
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Sanal ortam Python'unu kullan
        venv_python = get_venv_python_executable(venv_path)
        
        # Path'leri düzelt (Windows ters slash sorunu)
        current_dir = os.getcwd().replace('\\', '/')
        
        # Temiz GUI Selector'ı başlat
        cmd = [venv_python, "-c", f"""
import sys
sys.path.insert(0, '{current_dir}')

from clean_gui_selector import D64GUISelector
selector = D64GUISelector()
selector.run()
"""]
        
        logger.info("GUI Selector başlatılıyor...")
        result = subprocess.run(cmd, cwd=os.getcwd())
        
        if result.returncode == 0:
            logger.info("GUI Selector başarıyla çalıştırıldı")
            return True
        else:
            logger.error(f"GUI Selector çalıştırılırken hata: return code {result.returncode}")
            return False
        
    except Exception as e:
        logger.error(f"GUI Selector çalıştırılırken hata: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def run_test_mode(args, venv_path):
    """
    Test modu - belirtilen dosyaları işle
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Sanal ortam Python'unu kullan
        venv_python = get_venv_python_executable(venv_path)
        
        if not args.file:
            logger.error("Test modu için dosya belirtilmeli")
            return False
        
        # Path'leri düzelt (Windows ters slash sorunu)
        current_dir = os.getcwd().replace('\\', '/')
        file_path = args.file.replace('\\', '/')
        
        # Test kodunu sanal ortamda çalıştır
        test_code = f"""
import sys
sys.path.insert(0, '{current_dir}')
from advanced_disassembler import AdvancedDisassembler
from pathlib import Path

# Dosyayı oku
with open('{file_path}', 'rb') as f:
    data = f.read()

# PRG dosyası format kontrolü
if len(data) < 2:
    print("Geçersiz PRG dosyası")
    exit(1)

# Başlangıç adresini al
start_addr = data[0] + (data[1] << 8)
code_data = data[2:]

print(f"Dosya: {file_path}")
print(f"Başlangıç adresi: ${{start_addr:04X}}")
print(f"Kod uzunluğu: {{len(code_data)}} byte")

# Tüm formatlar için çıktı üret
formats = ['asm', 'c', 'qbasic', 'pdsx', 'pseudo', 'commodorebasicv2']

for fmt in formats:
    print(f"Format işleniyor: {{fmt}}")
    
    disasm = AdvancedDisassembler(start_addr, code_data, output_format=fmt)
    result = disasm.disassemble_simple(data)
    
    # Dosya adını hazırla
    source_name = Path('{file_path}').stem
    
    # Çıktıyı dosyaya kaydet
    output_dir = Path(f"{{fmt}}_files")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"{{source_name}}.{{fmt}}"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Çıktı kaydedildi: {{output_file}}")
    
    # İlk 20 satırı da yazdır
    lines = result.split('\\n')[:20]
    for line in lines:
        print(f"  {{line}}")
"""
        
        # Test kodunu çalıştır
        result = subprocess.run([venv_python, "-c", test_code], cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            logger.info("Test modu başarıyla tamamlandı")
            print(result.stdout)
            return True
        else:
            logger.error(f"Test modu hatası: {result.stderr}")
            return False
        
    except Exception as e:
        logger.error(f"Test modu hatası: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def parse_arguments():
    """
    Komut satırı argümanlarını parse et
    """
    parser = argparse.ArgumentParser(
        description="D64 Converter - 6502 Assembly Reverse Compiler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  %(prog)s --gui                              # GUI modunda çalıştır
  %(prog)s --file game.prg --format c         # PRG dosyasını C'ye çevir
  %(prog)s --input prg_files/test.prg --disassembler advanced --py65  # Gelişmiş test
  %(prog)s --test --file game.prg             # Test modu - tüm formatları üret
  %(prog)s --list-formats                     # Desteklenen formatları listele
  %(prog)s --disassembler improved --format c --illegal-opcodes       # İllegal opcodes ile
  %(prog)s --decompiler c --petcat --dlist    # Tüm decompiler'lar
  %(prog)s --debug --file game.prg            # Debug modu ile çalıştır
  %(prog)s --output-dir custom/ --format asm  # Özel çıktı dizini
        """
    )
    
    # Ana işlem modu
    parser.add_argument('--gui', action='store_true', 
                       help='GUI modunda çalıştır (varsayılan)')
    parser.add_argument('--test', action='store_true',
                       help='Test modu - tüm formatları üret')
    parser.add_argument('--no-gui', action='store_true',
                       help='GUI olmadan çalıştır')
    
    # Dosya seçenekleri
    parser.add_argument('--file', '-f', type=str,
                       help='İşlenecek dosya (D64, PRG, T64, vb.)')
    parser.add_argument('--input', '-i', type=str,
                       help='Giriş dosyası veya dizini')
    parser.add_argument('--input-dir', type=str,
                       help='Giriş dizini (toplu işlem için)')
    parser.add_argument('--format', '-o', type=str,
                       choices=['asm', 'c', 'qbasic', 'pdsx', 'pseudo', 'commodorebasicv2'],
                       help='Çıktı formatı')
    parser.add_argument('--output-dir', type=str,
                       help='Çıktı dizini (varsayılan: format_files/)')
    
    # Disassembler seçenekleri
    parser.add_argument('--disassembler', '-d', type=str,
                       choices=['basic', 'advanced', 'improved', 'py65_professional'],
                       default='improved', help='Disassembler seçimi')
    parser.add_argument('--py65', action='store_true',
                       help='py65 library kullan (professional mode)')
    parser.add_argument('--illegal-opcodes', action='store_true',
                       help='Illegal/undocumented opcodes destekle')
    
    # Decompiler seçenekleri  
    parser.add_argument('--decompiler', type=str,
                       choices=['basic', 'c', 'cpp', 'qbasic'],
                       help='Decompiler seçimi')
    parser.add_argument('--petcat', action='store_true',
                       help='PETCAT BASIC decompiler kullan')
    parser.add_argument('--dlist', action='store_true',
                       help='DLIST directory lister kullan')
    
    # Sistem seçenekleri
    parser.add_argument('--debug', action='store_true',
                       help='Debug modu - detaylı logging')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Log seviyesi')
    parser.add_argument('--log-file', type=str,
                       help='Log dosyası (varsayılan: logs/timestamp.log)')
    
    # Bilgi seçenekleri
    parser.add_argument('--list-formats', action='store_true',
                       help='Desteklenen formatları listele')
    parser.add_argument('--list-disassemblers', action='store_true',
                       help='Mevcut disassembler\'ları listele')
    parser.add_argument('--version', action='version', version='D64 Converter 1.0')
    
    return parser.parse_args()

def list_supported_formats():
    """
    Desteklenen formatları listele
    """
    formats = {
        'asm': '6502 Assembly',
        'c': 'C Programming Language',
        'qbasic': 'Microsoft QBasic',
        'pdsx': 'PDSX BASIC',
        'pseudo': 'Pseudo Code',
        'commodorebasicv2': 'Commodore BASIC V2'
    }
    
    print("Desteklenen Çıktı Formatları:")
    print("=" * 40)
    for fmt, desc in formats.items():
        print(f"  {fmt:<20} - {desc}")
    print()

def list_available_disassemblers():
    """
    Mevcut disassembler'ları listele
    """
    disassemblers = {
        'basic': 'Basit disassembler (99 satır)',
        'advanced': 'Gelişmiş disassembler + py65 fix (500 satır)',
        'improved': 'En gelişmiş disassembler + 6 format (1206 satır)',
        'py65_professional': 'Profesyonel py65 wrapper (756 satır)'
    }
    
    print("Mevcut Disassembler Seçenekleri:")
    print("=" * 50)
    for name, desc in disassemblers.items():
        print(f"  {name:<20} - {desc}")
    
    print("\nDecompiler Seçenekleri:")
    print("=" * 30)
    decompilers = {
        'basic': 'BASIC decompiler',
        'c': 'C decompiler',
        'cpp': 'C++ decompiler', 
        'qbasic': 'QBasic decompiler'
    }
    
    for name, desc in decompilers.items():
        print(f"  {name:<15} - {desc}")
    
    print("\nEk Araçlar:")
    print("=" * 20)
    print("  petcat          - VICE PETCAT BASIC detokenizer")
    print("  dlist           - Directory listing tool")
    print("  illegal-opcodes - Undocumented opcode support")
    print()

def main():
    """
    Ana program akışı
    """
    # Argümanları parse et
    args = parse_arguments()
    
    # Eğer hiç argüman verilmemişse, help göster
    if len(sys.argv) == 1:
        print("D64 Converter - 6502 Assembly Reverse Compiler")
        print("Kullanım için: python main.py --help")
        print("GUI için: python main.py --gui")
        return
    
    # Logging sistemini kur
    log_level = 'DEBUG' if args.debug else args.log_level
    logger = setup_logging(log_level, args.log_file)
    
    # Sistem bilgilerini kaydet
    save_system_info()
    
    # Çıktı klasörlerini oluştur
    create_output_directories()
    
    logger.info("D64 Converter başlatılıyor...")
    logger.info(f"Argümanlar: {vars(args)}")
    
    # Format listesi istendiyse
    if args.list_formats:
        list_supported_formats()
        return
    
    # Disassembler listesi istendiyse
    if args.list_disassemblers:
        list_available_disassemblers()
        return
    
    # Sanal dizin kurulumu
    venv_path = "venv_asmto"
    
    if not create_virtual_environment(venv_path):
        logger.error("Sanal dizin oluşturulamadı")
        return
    
    if not install_required_packages(venv_path):
        logger.error("Gerekli paketler yüklenemedi")
        return
    
    # Ana işlem moduna göre çalıştır
    try:
        if args.test:
            logger.info("Test modu başlatılıyor...")
            if not run_test_mode(args, venv_path):
                logger.error("Test modu başarısız")
                return
        elif args.gui:
            logger.info("GUI modu başlatılıyor...")
            if not run_converter_with_args(args, venv_path):
                logger.error("GUI modu başarısız")
                return
        else:
            logger.info("Converter modu başlatılıyor...")
            if not run_converter_with_args(args, venv_path):
                logger.error("Converter başarısız")
                return
                
        logger.info("Program başarıyla tamamlandı")
        
    except KeyboardInterrupt:
        logger.info("Program kullanıcı tarafından sonlandırıldı")
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()
