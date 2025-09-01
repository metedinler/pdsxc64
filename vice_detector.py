#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VICE Emulator Detection and Management System
WinVICE/VICE emülatörünü otomatik tespit eden ve kurulan sistemi yöneten modül

Features:
- Otomatik VICE emülatör tespit
- Sistem yollarında arama
- Registry kontrolü (Windows)
- Kurulum doğrulama
- Petcat yolu tespiti
- C1541 yolu tespiti
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import winreg
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VICEDetector:
    """VICE Emülatör Tespit ve Yönetim Sistemi"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.vice_info = {
            'detected': False,
            'version': None,
            'path': None,
            'petcat_path': None,
            'c1541_path': None,
            'x64_path': None,
            'tools_available': []
        }
        
        # Olası VICE kurulum yolları
        self.common_paths = self._get_common_paths()
        
    def _get_common_paths(self) -> List[str]:
        """Sistemdeki olası VICE kurulum yolları"""
        paths = []
        
        if self.system == 'windows':
            # Windows ortak kurulum yolları
            drive_letters = ['C:', 'D:', 'E:', 'F:']
            base_paths = [
                r'\Program Files\WinVICE-3.8-x64',
                r'\Program Files\WinVICE-3.7-x64', 
                r'\Program Files\WinVICE-3.6-x64',
                r'\Program Files\WinVICE',
                r'\Program Files (x86)\WinVICE-3.8-x64',
                r'\Program Files (x86)\WinVICE-3.7-x64',
                r'\Program Files (x86)\WinVICE-3.6-x64',
                r'\Program Files (x86)\WinVICE',
                r'\vice',
                r'\tools\vice',
                r'\emulators\vice',
                r'\c64\vice'
            ]
            
            for drive in drive_letters:
                for base_path in base_paths:
                    full_path = drive + base_path
                    if os.path.exists(full_path):
                        paths.append(full_path)
                        
        elif self.system == 'linux':
            # Linux ortak kurulum yolları
            paths = [
                '/usr/bin',
                '/usr/local/bin', 
                '/opt/vice',
                '/usr/share/vice',
                '/home/' + os.getenv('USER', '') + '/.local/bin'
            ]
            
        elif self.system == 'darwin':
            # macOS ortak kurulum yolları
            paths = [
                '/Applications/VICE',
                '/usr/local/bin',
                '/opt/homebrew/bin'
            ]
            
        return paths
        
    def detect_vice(self) -> bool:
        """VICE emülatörünü tespit et"""
        logger.info("🔍 VICE emülatör tespiti başlatılıyor...")
        
        # 1. Sistem PATH'inde ara
        if self._check_system_path():
            return True
            
        # 2. Registry'de ara (Windows)
        if self.system == 'windows' and self._check_windows_registry():
            return True
            
        # 3. Ortak kurulum yollarında ara
        if self._check_common_paths():
            return True
            
        # 4. Manuel arama
        if self._manual_search():
            return True
            
        logger.warning("⚠️ VICE emülatörü bulunamadı!")
        return False
        
    def _check_system_path(self) -> bool:
        """Sistem PATH'inde VICE araçlarını kontrol et"""
        tools = ['petcat', 'c1541', 'x64']
        
        for tool in tools:
            if self.system == 'windows':
                tool += '.exe'
                
            path = shutil.which(tool)
            if path:
                logger.info(f"✅ {tool} bulundu: {path}")
                self.vice_info[f'{tool.replace(".exe", "")}_path'] = path
                self.vice_info['tools_available'].append(tool.replace('.exe', ''))
                
                if not self.vice_info['path']:
                    # İlk bulunan aracın dizinini ana yol olarak kullan
                    self.vice_info['path'] = os.path.dirname(path)
                    
        if self.vice_info['tools_available']:
            self.vice_info['detected'] = True
            logger.info(f"✅ VICE PATH'de tespit edildi: {self.vice_info['path']}")
            return True
            
        return False
        
    def _check_windows_registry(self) -> bool:
        """Windows Registry'de VICE kurulumunu kontrol et"""
        if self.system != 'windows':
            return False
            
        registry_keys = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        try:
            for reg_key in registry_keys:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        if 'vice' in subkey_name.lower() or 'winvice' in subkey_name.lower():
                            try:
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    if os.path.exists(install_location):
                                        self.vice_info['path'] = install_location
                                        self.vice_info['detected'] = True
                                        self._detect_tools_in_path(install_location)
                                        logger.info(f"✅ VICE Registry'de bulundu: {install_location}")
                                        return True
                            except:
                                continue
                                
        except Exception as e:
            logger.debug(f"Registry okuma hatası: {e}")
            
        return False
        
    def _check_common_paths(self) -> bool:
        """Ortak kurulum yollarında VICE'ı ara"""
        for path in self.common_paths:
            if os.path.exists(path):
                logger.info(f"🔍 Kontrol ediliyor: {path}")
                if self._detect_tools_in_path(path):
                    self.vice_info['path'] = path
                    self.vice_info['detected'] = True
                    logger.info(f"✅ VICE bulundu: {path}")
                    return True
                    
        return False
        
    def _manual_search(self) -> bool:
        """Manuel arama - kullanıcı bilinen yolları kontrol etsin"""
        logger.info("🔍 Manuel arama başlatılıyor...")
        
        # Kullanıcıdan VICE yolu isteme
        print("\n" + "="*60)
        print("🎮 VICE EMÜLATÖR TESPİT SİSTEMİ")
        print("="*60)
        print("VICE emülatörü otomatik olarak bulunamadı.")
        print("Lütfen VICE kurulum dizinini manuel olarak belirtin.")
        print("\nÖrnek yollar:")
        print("  Windows: C:\\Program Files\\WinVICE-3.8-x64")
        print("  Linux:   /usr/bin")
        print("  macOS:   /Applications/VICE")
        print("\nBoş bırakıp Enter'a basarsanız tespit atlanır.")
        
        user_path = input("\nVICE kurulum dizini: ").strip()
        
        if user_path and os.path.exists(user_path):
            if self._detect_tools_in_path(user_path):
                self.vice_info['path'] = user_path
                self.vice_info['detected'] = True
                logger.info(f"✅ Manuel VICE yolu kabul edildi: {user_path}")
                return True
            else:
                logger.warning(f"⚠️ Bu dizinde VICE araçları bulunamadı: {user_path}")
                
        return False
        
    def _detect_tools_in_path(self, base_path: str) -> bool:
        """Belirtilen dizinde VICE araçlarını tespit et"""
        tools = ['petcat', 'c1541', 'x64']
        found_tools = []
        
        # Alt dizinleri de kontrol et
        search_dirs = [base_path]
        for subdir in ['bin', 'tools', '.']:
            full_subdir = os.path.join(base_path, subdir)
            if os.path.exists(full_subdir):
                search_dirs.append(full_subdir)
                
        for search_dir in search_dirs:
            for tool in tools:
                tool_paths = [
                    os.path.join(search_dir, tool),
                    os.path.join(search_dir, tool + '.exe')
                ]
                
                for tool_path in tool_paths:
                    if os.path.exists(tool_path) and os.path.isfile(tool_path):
                        self.vice_info[f'{tool}_path'] = tool_path
                        found_tools.append(tool)
                        logger.info(f"  ✅ {tool} bulundu: {tool_path}")
                        break
                        
        self.vice_info['tools_available'] = found_tools
        return len(found_tools) > 0
        
    def get_vice_version(self) -> Optional[str]:
        """VICE sürümünü tespit et"""
        if not self.vice_info['detected']:
            return None
            
        # x64 ile sürüm tespiti
        x64_path = self.vice_info.get('x64_path')
        if x64_path:
            try:
                result = subprocess.run([x64_path, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    self.vice_info['version'] = version_line
                    return version_line
            except:
                pass
                
        # petcat ile sürüm tespiti
        petcat_path = self.vice_info.get('petcat_path')
        if petcat_path:
            try:
                result = subprocess.run([petcat_path, '-h'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 or result.stderr:
                    output = result.stderr or result.stdout
                    for line in output.split('\n'):
                        if 'petcat' in line.lower() and ('vice' in line.lower() or 'version' in line.lower()):
                            self.vice_info['version'] = line.strip()
                            return line.strip()
            except:
                pass
                
        return "Sürüm tespit edilemedi"
        
    def validate_installation(self) -> Dict[str, bool]:
        """VICE kurulumunu doğrula"""
        validation = {
            'petcat': False,
            'c1541': False, 
            'x64': False,
            'overall': False
        }
        
        if not self.vice_info['detected']:
            return validation
            
        # Her aracı test et
        for tool in ['petcat', 'c1541', 'x64']:
            tool_path = self.vice_info.get(f'{tool}_path')
            if tool_path and os.path.exists(tool_path):
                try:
                    # Kısa test komutu
                    test_args = {
                        'petcat': ['-h'],
                        'c1541': ['-h'], 
                        'x64': ['--help']
                    }
                    
                    result = subprocess.run([tool_path] + test_args[tool],
                                          capture_output=True, timeout=5)
                    validation[tool] = result.returncode in [0, 1]  # 0 veya 1 kabul edilebilir
                    
                except Exception as e:
                    logger.debug(f"{tool} test hatası: {e}")
                    validation[tool] = False
                    
        # Genel doğrulama - en az petcat ve c1541 çalışmalı
        validation['overall'] = validation['petcat'] and validation['c1541']
        
        return validation
        
    def get_report(self) -> str:
        """VICE tespit raporu oluştur"""
        lines = [
            "🎮 VICE EMÜLATÖR TESPİT RAPORU",
            "=" * 50
        ]
        
        if self.vice_info['detected']:
            lines.extend([
                f"✅ Durum: VICE Tespit Edildi",
                f"📂 Ana Dizin: {self.vice_info['path']}",
                f"📄 Sürüm: {self.get_vice_version() or 'Bilinmiyor'}",
                "",
                "🔧 Tespit Edilen Araçlar:"
            ])
            
            for tool in ['petcat', 'c1541', 'x64']:
                tool_path = self.vice_info.get(f'{tool}_path')
                if tool_path:
                    lines.append(f"  ✅ {tool}: {tool_path}")
                else:
                    lines.append(f"  ❌ {tool}: Bulunamadı")
                    
            # Doğrulama sonuçları
            validation = self.validate_installation()
            lines.extend([
                "",
                "🧪 Araç Doğrulama Testleri:"
            ])
            
            for tool, status in validation.items():
                if tool != 'overall':
                    icon = "✅" if status else "❌"
                    lines.append(f"  {icon} {tool}: {'Çalışıyor' if status else 'Hata'}")
                    
            overall_status = "✅ Hazır" if validation['overall'] else "❌ Sorunlu"
            lines.append(f"\n🎯 Genel Durum: {overall_status}")
            
        else:
            lines.extend([
                "❌ Durum: VICE Tespit Edilemedi",
                "",
                "💡 Öneriler:",
                "  1. VICE emülatörünü indirin: https://vice-emu.sourceforge.io/",
                "  2. Program Files dizinine kurun",
                "  3. PATH çevre değişkenine ekleyin",
                "  4. Bu programı yeniden çalıştırın"
            ])
            
        return "\n".join(lines)
        
    def install_vice_guide(self) -> str:
        """VICE kurulum rehberi"""
        guide = """
🎮 VICE EMÜLATÖR KURULUM REHBERİ
================================

1. VICE İNDİRME:
   - https://vice-emu.sourceforge.io/ adresine gidin
   - Windows için "WinVICE" bölümünden güncel sürümü indirin
   - Önerilen: WinVICE-3.8-x64-r44730.7z

2. KURULUM:
   - İndirilen arşivi açın
   - Çıkan dizini C:\\Program Files\\ altına kopyalayın
   - Örnek: C:\\Program Files\\WinVICE-3.8-x64\\

3. PATH AYARLAMA (İsteğe bağlı):
   - Başlat > "environ" arayın
   - "Sistem çevre değişkenlerini düzenle" açın
   - "Çevre Değişkenleri" butonuna tıklayın
   - PATH'e VICE bin dizinini ekleyin

4. TEST:
   - Bu programı yeniden çalıştırın
   - VICE otomatik tespit edilmelidir

🔧 PETCAT KULLANIMI:
   - BASIC programları için: petcat -2 program.prg
   - Assembly için: petcat -a program.prg
"""
        return guide

# Test fonksiyonu
if __name__ == "__main__":
    print("🧪 VICE Detector Test")
    print("=" * 30)
    
    detector = VICEDetector()
    
    print("\n🔍 VICE tespiti başlatılıyor...")
    success = detector.detect_vice()
    
    print("\n" + detector.get_report())
    
    if not success:
        print("\n" + detector.install_vice_guide())
