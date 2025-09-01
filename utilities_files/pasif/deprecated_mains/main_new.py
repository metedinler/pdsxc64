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
        "prg_files"
    ]
    
    for dirname in output_dirs:
        Path(dirname).mkdir(exist_ok=True)
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
                              capture_output=True, text=True)
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
    Proje için özel sanal dizin oluştur
    """
    logger = logging.getLogger(__name__)
    
    if os.path.exists(venv_path):
        logger.info(f"Sanal dizin zaten mevcut: {venv_path}")
        return True
    
    logger.info("Sanal dizin oluşturuluyor...")
    try:
        venv.create(venv_path, with_pip=True)
        logger.info(f"Sanal dizin başarıyla oluşturuldu: {venv_path}")
        return True
    except Exception as e:
        logger.error(f"Sanal dizin oluşturulurken hata: {e}")
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
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Paket başarıyla yüklendi: {package}")
            else:
                logger.warning(f"Paket yüklenemedi: {package}")
                logger.warning(f"Hata: {result.stderr}")
        except Exception as e:
            logger.error(f"Paket yükleme hatası {package}: {e}")
    
    return True

def run_converter_with_args(args):
    """
    Converter'ı belirtilen argümanlarla çalıştır
    """
    logger = logging.getLogger(__name__)
    
    try:
        # D64 Converter'ı import et
        from d64_converter import D64ConverterApp
        import tkinter as tk
        
        # Tkinter root penceresi
        root = tk.Tk()
        
        # Converter uygulamasını başlat
        app = D64ConverterApp(root)
        
        # Eğer dosya belirtilmişse, otomatik yükle
        if args.file:
            logger.info(f"Dosya otomatik yükleniyor: {args.file}")
            app.d64_path.set(args.file)
            app.load_image(args.file)
        
        # Eğer çıktı formatı belirtilmişse ayarla
        if args.format:
            logger.info(f"Çıktı formatı ayarlandı: {args.format}")
            app.output_format.set(args.format)
        
        # GUI'yi başlat
        if not args.no_gui:
            logger.info("GUI başlatılıyor...")
            root.mainloop()
        
        logger.info("Converter başarıyla çalıştırıldı")
        return True
        
    except Exception as e:
        logger.error(f"Converter çalıştırılırken hata: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def run_test_mode(args):
    """
    Test modu - belirtilen dosyaları işle
    """
    logger = logging.getLogger(__name__)
    
    try:
        from advanced_disassembler import AdvancedDisassembler
        
        if not args.file:
            logger.error("Test modu için dosya belirtilmeli")
            return False
        
        # Dosyayı oku
        with open(args.file, 'rb') as f:
            data = f.read()
        
        # PRG dosyası format kontrolü
        if len(data) < 2:
            logger.error("Geçersiz PRG dosyası")
            return False
        
        # Başlangıç adresini al
        start_addr = data[0] + (data[1] << 8)
        code_data = data[2:]
        
        logger.info(f"Dosya: {args.file}")
        logger.info(f"Başlangıç adresi: ${start_addr:04X}")
        logger.info(f"Kod uzunluğu: {len(code_data)} byte")
        
        # Tüm formatlar için çıktı üret
        formats = ['asm', 'c', 'qbasic', 'pdsx', 'pseudo', 'commodorebasicv2']
        
        for fmt in formats:
            logger.info(f"Format işleniyor: {fmt}")
            
            disasm = AdvancedDisassembler(start_addr, code_data, output_format=fmt)
            result = disasm.disassemble_simple(data)
            
            # Dosya adını hazırla
            source_name = Path(args.file).stem
            
            # Çıktıyı dosyaya kaydet
            output_dir = Path(f"{fmt}_files")
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / f"{source_name}.{fmt}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            
            logger.info(f"Çıktı kaydedildi: {output_file}")
            
            # İlk 20 satırı da log'a yazdır
            lines = result.split('\n')[:20]
            for line in lines:
                logger.info(f"  {line}")
        
        return True
        
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
  %(prog)s --gui                          # GUI modunda çalıştır
  %(prog)s --file game.prg --format c     # PRG dosyasını C'ye çevir
  %(prog)s --test --file game.prg         # Test modu - tüm formatları üret
  %(prog)s --list-formats                 # Desteklenen formatları listele
  %(prog)s --debug --file game.prg        # Debug modu ile çalıştır
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
    parser.add_argument('--format', '-o', type=str,
                       choices=['asm', 'c', 'qbasic', 'pdsx', 'pseudo', 'commodorebasicv2'],
                       help='Çıktı formatı')
    
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

def main():
    """
    Ana program akışı
    """
    # Argümanları parse et
    args = parse_arguments()
    
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
            if not run_test_mode(args):
                logger.error("Test modu başarısız")
                return
        else:
            logger.info("Converter modu başlatılıyor...")
            if not run_converter_with_args(args):
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
