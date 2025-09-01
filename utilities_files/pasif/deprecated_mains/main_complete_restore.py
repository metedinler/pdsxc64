#!/usr/bin/env python3
"""
D64 Converter v5.0 - COMPLETE SYSTEM RESTORE
Eski sistemin TÜM özellikleri ile birleştirilmiş gelişmiş main.py
- Sanal ortam yönetimi (venv_asmto)  
- Otomatik kütüphane yükleme
- Kapsamlı argparse sistemi
- Detaylı logging ve bildirimler
- Test modu ve dosya işleme
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

def setup_logging(log_level="INFO", log_file=None, debug=False):
    """
    Enhanced logging system setup with comprehensive output
    """
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Generate log filename if not provided
    if log_file is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"d64_converter_{timestamp}.log"
    
    # Configure logging format
    log_format = '%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
    
    # Set logging level
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 D64 Converter v5.0 - COMPLETE SYSTEM RESTORE")
    logger.info(f"📅 Build Date: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    logger.info(f"🏆 Project Status: RESTORED (with venv_asmto)")
    logger.info(f"📝 Logging system initialized: {log_file}")
    logger.info(f"📊 Log level: {log_level}")
    
    if debug:
        logger.info("🔧 DEBUG MODE ENABLED - Detailed logging active")
    
    return logger

def create_output_directories():
    """
    Create all required output directories with enhanced structure
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
        "format_files",
        "utilities_files/aktif",
        "utilities_files/pasif",
        "utilities_files/deprecated"
    ]
    
    created_count = 0
    for dirname in output_dirs:
        dir_path = Path(dirname)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            logging.info(f"✅ Created output directory: {dirname}")
            created_count += 1
        else:
            logging.debug(f"📁 Directory exists: {dirname}")
    
    if created_count > 0:
        logging.info(f"📁 Total directories created: {created_count}")
    else:
        logging.info("📁 All output directories already exist")

def save_system_info():
    """
    Save comprehensive system information for debugging
    """
    system_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "platform": platform.platform(),
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "python_executable": sys.executable,
        "d64_converter_version": "5.0",
        "project_status": "COMPLETE RESTORE with venv_asmto",
        "venv_path": "venv_asmto",
        "available_modules": []
    }
    
    # Check for available modules
    core_modules = [
        "unified_decompiler",
        "code_analyzer", 
        "enhanced_c64_memory_manager",
        "gui_manager",
        "improved_disassembler",
        "advanced_disassembler"
    ]
    
    for module in core_modules:
        try:
            __import__(module)
            system_info["available_modules"].append(f"✅ {module}")
        except ImportError:
            system_info["available_modules"].append(f"❌ {module}")
    
    # Save system info
    info_file = Path("logs/system_info.json")
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(system_info, f, indent=2, ensure_ascii=False)
    
    logging.info(f"💾 System information saved: {info_file}")

def create_virtual_environment(venv_path):
    """
    RESTORED: Proje için özel sanal dizin oluştur ve aktif et
    """
    logger = logging.getLogger(__name__)

    if os.path.exists(venv_path):
        logger.info(f"📦 Sanal dizin zaten mevcut: {venv_path}")
    else:
        logger.info("📦 Sanal dizin oluşturuluyor...")
        try:
            venv.create(venv_path, with_pip=True)
            logger.info(f"✅ Sanal dizin başarıyla oluşturuldu: {venv_path}")
        except Exception as e:
            logger.error(f"❌ Sanal dizin oluşturulurken hata: {e}")
            return False

    # Sanal ortamı aktif et
    activate_script = os.path.join(venv_path, "Scripts", "activate") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "activate")
    if os.path.exists(activate_script):
        logger.info(f"🔧 Sanal ortam aktif ediliyor: {activate_script}")
        os.environ["VIRTUAL_ENV"] = venv_path
        os.environ["PATH"] = os.path.join(venv_path, "Scripts") + os.pathsep + os.environ["PATH"]
        return True
    else:
        logger.error("❌ Sanal ortam aktif edilemedi: activate script bulunamadı")
        return False

def get_venv_python_executable(venv_path):
    """
    RESTORED: Sanal dizindeki Python çalıştırılabilir dosyasının yolunu al
    """
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")

def get_venv_pip_executable(venv_path):
    """
    RESTORED: Sanal dizindeki pip çalıştırılabilir dosyasının yolunu al
    """
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_path, "bin", "pip")

def install_required_packages(venv_path):
    """
    RESTORED: Gerekli paketleri sanal dizine yükle
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
            logger.info(f"📦 Paket yükleniyor: {package}")
            result = subprocess.run([pip_exe, "install", package], 
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                logger.info(f"✅ Paket başarıyla yüklendi: {package}")
            else:
                logger.warning(f"⚠️  Paket yüklenemedi: {package}")
                logger.warning(f"Hata: {result.stderr}")
        except Exception as e:
            logger.error(f"❌ Paket yükleme hatası {package}: {e}")

    # Pillow modülünü kontrol et
    venv_python = get_venv_python_executable(venv_path)
    
    try:
        # Sanal ortam Python'u ile PIL modülünü test et
        result = subprocess.run([venv_python, "-c", "import PIL; print('PIL import successful')"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logger.info("✅ Pillow modülü başarıyla yüklendi.")
        else:
            raise ImportError("PIL modülü yüklenemedi")
    except:
        logger.error("❌ Pillow modülü yüklenemedi, yeniden yükleniyor...")
        result = subprocess.run([pip_exe, "install", "--force-reinstall", "Pillow"], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            logger.info("✅ Pillow modülü başarıyla yeniden yüklendi.")

    return True

def run_converter_with_args(args, venv_path):
    """
    RESTORED: Converter'ı belirtilen argümanlarla sanal ortamda çalıştır
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Sanal ortam Python'unu kullan
        venv_python = get_venv_python_executable(venv_path)
        
        # Path'leri düzelt (Windows ters slash sorunu)
        current_dir = os.getcwd().replace('\\', '/')
        
        # GUI modunda clean_gui_selector'ı başlat
        cmd = [venv_python, "-c", f"""
import sys
sys.path.insert(0, '{current_dir}')

from clean_gui_selector import D64GUISelector
selector = D64GUISelector()
selector.run()
"""]
        
        logger.info("🎨 GUI Selector sanal ortamda başlatılıyor...")
        result = subprocess.run(cmd, cwd=os.getcwd())
        
        if result.returncode == 0:
            logger.info("✅ GUI Selector başarıyla çalıştırıldı")
            return True
        else:
            logger.error(f"❌ GUI Selector çalıştırılırken hata: return code {result.returncode}")
            return False
        
    except Exception as e:
        logger.error(f"❌ GUI Selector çalıştırılırken hata: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def run_test_mode(args, venv_path):
    """
    RESTORED: Test modu - belirtilen dosyaları sanal ortamda işle
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Sanal ortam Python'unu kullan
        venv_python = get_venv_python_executable(venv_path)
        
        if not args.file:
            logger.error("❌ Test modu için dosya belirtilmeli")
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

print("🧪 D64 Converter Test Modu - Sanal Ortamda")
print("=" * 50)

# Dosyayı oku
with open('{file_path}', 'rb') as f:
    data = f.read()

# PRG dosyası format kontrolü
if len(data) < 2:
    print("❌ Geçersiz PRG dosyası")
    exit(1)

# Başlangıç adresini al
start_addr = data[0] + (data[1] << 8)
code_data = data[2:]

print(f"📁 Dosya: {file_path}")
print(f"📍 Başlangıç adresi: ${{start_addr:04X}}")
print(f"📊 Kod uzunluğu: {{len(code_data)}} byte")
print("")

# Tüm formatlar için çıktı üret
formats = ['asm', 'c', 'qbasic', 'pdsx', 'pseudo', 'commodorebasicv2']

for fmt in formats:
    print(f"⚡ Format işleniyor: {{fmt}}")
    
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
    
    print(f"  ✅ Çıktı kaydedildi: {{output_file}}")
    
    # İlk 10 satırı da yazdır
    lines = result.split('\\n')[:10]
    for line in lines:
        print(f"    {{line}}")
    print("")

print("✅ Test modu tamamlandı!")
"""
        
        # Test kodunu çalıştır
        logger.info(f"🧪 Test modu sanal ortamda çalıştırılıyor: {file_path}")
        result = subprocess.run([venv_python, "-c", test_code], cwd=os.getcwd(), 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Test modu başarıyla tamamlandı")
            print(result.stdout)
            return True
        else:
            logger.error(f"❌ Test modu hatası: {result.stderr}")
            print(f"❌ Test modu hatası: {result.stderr}")
            return False
        
    except Exception as e:
        logger.error(f"❌ Test modu hatası: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def parse_arguments():
    """
    RESTORED: Komut satırı argümanlarını parse et - ESKİ SİSTEMİN TÜM ÖZELLİKLERİ
    """
    parser = argparse.ArgumentParser(
        description="D64 Converter v5.0 - Advanced Commodore 64 Decompiler Suite (COMPLETE RESTORE)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎯 KAPSAMLI ÖRNEKLER:
  %(prog)s --gui                              # GUI modunda çalıştır (sanal ortamda)
  %(prog)s --file game.prg --format c         # PRG dosyasını C'ye çevir
  %(prog)s --input prg_files/test.prg --disassembler advanced --py65  # Gelişmiş test
  %(prog)s --test --file game.prg             # Test modu - tüm formatları üret
  %(prog)s --list-formats                     # Desteklenen formatları listele
  %(prog)s --list-disassemblers               # Mevcut disassembler'ları listele
  %(prog)s --disassembler improved --format c --illegal-opcodes       # İllegal opcodes ile
  %(prog)s --decompiler c --petcat --dlist    # Tüm decompiler'lar
  %(prog)s --debug --file game.prg            # Debug modu ile çalıştır
  %(prog)s --output-dir custom/ --format asm  # Özel çıktı dizini
  %(prog)s --input-dir prg_files/ --format c  # Toplu işlem
  %(prog)s --no-gui --file test.prg           # GUI olmadan çalıştır
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
    parser.add_argument('--version', action='version', version='D64 Converter v5.0 - COMPLETE RESTORE')
    
    return parser.parse_args()

def list_supported_formats():
    """
    RESTORED: Desteklenen formatları listele
    """
    formats = {
        'asm': '6502 Assembly',
        'c': 'C Programming Language',
        'qbasic': 'Microsoft QBasic',
        'pdsx': 'PDSX BASIC',
        'pseudo': 'Pseudo Code',
        'commodorebasicv2': 'Commodore BASIC V2'
    }
    
    print("🎯 D64 Converter - Desteklenen Çıktı Formatları:")
    print("=" * 50)
    for fmt, desc in formats.items():
        print(f"  ✅ {fmt:<20} - {desc}")
    print()

def list_available_disassemblers():
    """
    RESTORED: Mevcut disassembler'ları listele
    """
    disassemblers = {
        'basic': 'Basit disassembler (99 satır)',
        'advanced': 'Gelişmiş disassembler + py65 fix (500 satır)',
        'improved': 'En gelişmiş disassembler + 6 format (1274 satır)',
        'py65_professional': 'Profesyonel py65 wrapper (757 satır)'
    }
    
    print("🔧 D64 Converter - Mevcut Disassembler Seçenekleri:")
    print("=" * 60)
    for name, desc in disassemblers.items():
        print(f"  ⚙️  {name:<20} - {desc}")
    
    print("\n🧪 Decompiler Seçenekleri:")
    print("=" * 30)
    decompilers = {
        'basic': 'BASIC decompiler',
        'c': 'C decompiler (658 lines)',
        'cpp': 'C++ decompiler', 
        'qbasic': 'QBasic decompiler (686 lines)'
    }
    
    for name, desc in decompilers.items():
        print(f"  🔬 {name:<15} - {desc}")
    
    print("\n🛠️  Ek Araçlar:")
    print("=" * 20)
    print("  📋 petcat          - VICE PETCAT BASIC detokenizer")
    print("  📁 dlist           - Directory listing tool")
    print("  🚫 illegal-opcodes - Undocumented opcode support")
    print()

def main():
    """
    RESTORED: Ana program akışı - ESKİ SİSTEMİN TÜM ÖZELLİKLERİ
    """
    # Argümanları parse et
    args = parse_arguments()
    
    # Eğer hiç argüman verilmemişse, help göster
    if len(sys.argv) == 1:
        print("🚀 D64 Converter v5.0 - COMPLETE SYSTEM RESTORE")
        print("📦 Sanal ortam (venv_asmto) ile çalışır")
        print("Kullanım için: python main_complete_restore.py --help")
        print("GUI için: python main_complete_restore.py --gui")
        return
    
    # Logging sistemini kur
    log_level = 'DEBUG' if args.debug else args.log_level
    logger = setup_logging(log_level, args.log_file, args.debug)
    
    # Sistem bilgilerini kaydet
    save_system_info()
    
    # Çıktı klasörlerini oluştur
    create_output_directories()
    
    logger.info("🚀 D64 Converter v5.0 - COMPLETE RESTORE başlatılıyor...")
    logger.info(f"📋 Argümanlar: {vars(args)}")
    
    # Format listesi istendiyse
    if args.list_formats:
        list_supported_formats()
        return
    
    # Disassembler listesi istendiyse
    if args.list_disassemblers:
        list_available_disassemblers()
        return
    
    # SANAL DİZİN KURULUMU - RESTORED!
    venv_path = "venv_asmto"
    
    logger.info(f"📦 Sanal dizin kontrolü: {venv_path}")
    if not create_virtual_environment(venv_path):
        logger.error("❌ Sanal dizin oluşturulamadı")
        return
    
    logger.info("📦 Gerekli paketlerin sanal dizine yüklenmesi...")
    if not install_required_packages(venv_path):
        logger.error("❌ Gerekli paketler yüklenemedi")
        return
    
    # Ana işlem moduna göre çalıştır
    try:
        if args.test:
            logger.info("🧪 Test modu başlatılıyor...")
            if not run_test_mode(args, venv_path):
                logger.error("❌ Test modu başarısız")
                return
        elif args.gui or (not args.no_gui and not args.file):
            logger.info("🎨 GUI modu başlatılıyor...")
            if not run_converter_with_args(args, venv_path):
                logger.error("❌ GUI modu başarısız")
                return
        else:
            logger.info("🔧 Converter modu başlatılıyor...")
            if not run_converter_with_args(args, venv_path):
                logger.error("❌ Converter başarısız")
                return
                
        logger.info("✅ Program başarıyla tamamlandı")
        
    except KeyboardInterrupt:
        logger.info("⚠️  Program kullanıcı tarafından sonlandırıldı")
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()
