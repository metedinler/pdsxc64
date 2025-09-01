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
        import pkg_resources
        system_info["installed_packages"] = [
            f"{pkg.project_name}=={pkg.version}" 
            for pkg in pkg_resources.working_set
        ]
    except Exception as e:
        logging.warning(f"Yüklü paketler alınamadı: {e}")
    
    # Sistem bilgilerini kaydet
    with open("logs/system_info.json", "w", encoding="utf-8") as f:
        json.dump(system_info, f, indent=2, ensure_ascii=False)
    
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

def check_and_install_package_in_venv(package_name, venv_path, import_name=None):
    """
    Sanal dizinde otomatik kütüphane kontrol ve yükleme fonksiyonu
    """
    if import_name is None:
        import_name = package_name
    
    python_exe = get_venv_python_executable(venv_path)
    pip_exe = get_venv_pip_executable(venv_path)
    
    # Sanal dizindeki Python ile kütüphane kontrolü
    try:
        result = subprocess.run([python_exe, "-c", f"import {import_name}"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"'{package_name}' kütüphanesi sanal dizinde zaten yüklü.")
            return True
    except:
        pass
    
    # Kütüphane yüklü değilse yükle
    print(f"'{package_name}' kütüphanesi sanal dizinde bulunamadı. Yükleniyor...")
    try:
        subprocess.check_call([pip_exe, "install", package_name])
        print(f"'{package_name}' sanal dizine başarıyla yüklendi!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"'{package_name}' sanal dizine yüklenirken hata oluştu: {e}")
        return False

def check_and_install_package(package_name, import_name=None):
    """
    Otomatik kütüphane kontrol ve yükleme fonksiyonu
    """
    if import_name is None:
        import_name = package_name
    
    # Kütüphane yüklü mü kontrol et
    spec = importlib.util.find_spec(import_name)
    if spec is None:
        print(f"'{package_name}' kütüphanesi bulunamadı. Yükleniyor...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"'{package_name}' başarıyla yüklendi!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"'{package_name}' yüklenirken hata oluştu: {e}")
            return False
    else:
        print(f"'{package_name}' kütüphanesi zaten yüklü.")
        return True

def install_required_packages(venv_path):
    """
    Sanal dizine gerekli paketleri kurar
    """
    python_exe = get_venv_python_executable(venv_path)
    required_packages = ["d64", "py65", "Pillow", "tkinterdnd2"]
    
    print(f"Gerekli paketler kuruluyor: {', '.join(required_packages)}")
    print("-" * 50)
    
    all_installed = True
    for package in required_packages:
        if not check_and_install_package_in_venv(package, venv_path):
            all_installed = False
    
    print("-" * 50)
    if all_installed:
        print("Tüm gerekli paketler sanal dizine başarıyla yüklendi!")
    else:
        print("Bazı paketler sanal dizine yüklenemedi.")
        return False, venv_path
    
    return True, venv_path

def run_program_in_venv(venv_path):
    """
    Programı sanal dizinde çalıştır
    """
    python_exe = get_venv_python_executable(venv_path)
    
    main_gui_script = os.path.join(os.getcwd(), "d64_converter.py")
    if not os.path.exists(main_gui_script):
        print(f"HATA: Ana GUI betiği bulunamadı: {main_gui_script}")
        return False
        
    print(f"Program sanal dizinde çalıştırılıyor: {main_gui_script}")
    print("=" * 50)
    
    try:
        # Hataları yakalamak için Popen ve communicate kullanalım
        process = subprocess.Popen([python_exe, main_gui_script], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   text=True,
                                   creationflags=subprocess.CREATE_NO_WINDOW) # Windows'ta konsol penceresini gizle

        # Programın başlaması için kısa bir süre bekle, sonra çıktıyı kontrol et
        try:
            stdout, stderr = process.communicate(timeout=5) # 5 saniye sonra zaman aşımına uğrar
            
            # Eğer program 5 saniye içinde kapanırsa, bir hata olduğunu varsayabiliriz.
            if stderr:
                print("GUI UYGULAMASINDA HATA OLUŞTU:")
                print(stderr)
                return False
            if stdout:
                print("GUI UYGULAMASI ÇIKTISI:")
                print(stdout)
            return True

        except subprocess.TimeoutExpired:
            # Eğer 5 saniye sonra hala çalışıyorsa, başarıyla başladığını varsayalım.
            print("GUI uygulaması başarıyla başlatıldı ve çalışıyor.")
            # process.kill() # Testten sonra GUI'yi açık bırakmak için bu satırı kaldırabiliriz.
            return True
        
    except Exception as e:
        print(f"Sanal dizinde program çalıştırılırken genel bir hata oluştu: {e}")
        return False

def main():
    """
    Ana program akışı
    """
    print("6502 Assembly Parser ve Converter")
    print("=" * 50)
    print("Sanal dizin ile izole çalışma ortamı hazırlanıyor...")
    
    venv_path = "venv_asmto"
    
    if not create_virtual_environment(venv_path):
        return
        
    if not install_required_packages(venv_path):
        return

    if not run_program_in_venv(venv_path):
        return

if __name__ == "__main__":
    main()