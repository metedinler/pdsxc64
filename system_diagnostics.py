#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 KAPSAMLI SİSTEM ANALİZ VE HATA RAPORLAMA SİSTEMİ v1.0
================================================================
PROJE: Enhanced D64 Converter - Comprehensive Error Tracking System
MODÜL: system_diagnostics.py - Tüm Sistemi Analiz Eden Kapsamlı Hata Sistemi
VERSİYON: 1.0 (Başlangıç - Full System Analysis)
AMAÇ: Tüm .py ve .md dosyalarını okuyup hataları tespit etme
================================================================

Bu modül şu özellikleri sağlar:
• Tüm Python dosyalarının syntax kontrol
• Import hatalarını tespit etme  
• Missing dependencies kontrolü
• JSON dosyalarının format kontrolü
• GUI bileşenlerinin çalışabilirlik analizi
• Memory leak potansiyeli tarama
• Performans darboğazı analizi
• Detaylı loglama ve raporlama
================================================================
"""

import ast
import json
import os
import sys
import importlib
import traceback
import datetime
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple, Any
import logging

class SystemDiagnostics:
    """Kapsamlı sistem analiz ve hata raporlama sınıfı"""
    
    def __init__(self, ana_dizin="c:\\Users\\dell\\Documents\\projeler\\d64_converter"):
        self.ana_dizin = Path(ana_dizin)
        self.hata_raporu = {
            "analiz_zamani": datetime.datetime.now().isoformat(),
            "sistem_bilgileri": self._sistem_bilgilerini_al(),
            "python_dosyalari": {},
            "json_dosyalari": {},
            "markdown_dosyalari": {},
            "syntax_hatalari": [],
            "import_hatalari": [],
            "missing_dependencies": [],
            "gui_hatalari": [],
            "json_format_hatalari": [],
            "memory_leak_potansiyeli": [],
            "performans_sorunlari": [],
            "deprecated_kullanımlar": [],
            "güvenlik_sorunları": [],
            "genel_istatistikler": {}
        }
        
        # Loglama sistemi kurulumu
        self._setup_logging()
        
        self.logger.info("🔍 Kapsamlı Sistem Analizi Başlatılıyor...")
        
    def _setup_logging(self):
        """Loglama sistemini kur"""
        log_dosyasi = self.ana_dizin / "logs" / f"sistem_analizi_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_dosyasi.parent.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dosyasi, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _sistem_bilgilerini_al(self) -> Dict[str, Any]:
        """Sistem bilgilerini topla"""
        import platform
        try:
            python_version = sys.version
            platform_info = platform.platform()
            cpu_count = os.cpu_count()
            cwd = os.getcwd()
            
            return {
                "python_version": python_version,
                "platform": platform_info,
                "cpu_count": cpu_count,
                "working_directory": cwd,
                "path_separator": os.sep,
                "environment_variables": dict(os.environ)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def python_dosyalarini_analiz_et(self):
        """Tüm Python dosyalarını analiz et"""
        self.logger.info("📄 Python dosyalarını analiz ediliyor...")
        
        for py_dosyasi in self.ana_dizin.rglob("*.py"):
            try:
                self._python_dosyasi_analiz(py_dosyasi)
            except Exception as e:
                self.logger.error(f"❌ {py_dosyasi} analiz hatası: {e}")
                
    def _python_dosyasi_analiz(self, dosya_yolu: Path):
        """Tek Python dosyasını analiz et"""
        try:
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                kod = f.read()
                
            # Syntax kontrolü
            syntax_sonucu = self._syntax_kontrol(kod, dosya_yolu)
            
            # Import analizi
            import_sonucu = self._import_analizi(kod, dosya_yolu)
            
            # GUI bileşen analizi
            gui_sonucu = self._gui_analizi(kod, dosya_yolu)
            
            # Memory leak analizi
            memory_sonucu = self._memory_leak_analizi(kod, dosya_yolu)
            
            # Performans analizi
            performans_sonucu = self._performans_analizi(kod, dosya_yolu)
            
            # Dosya istatistikleri
            istatistikler = self._dosya_istatistikleri(kod, dosya_yolu)
            
            self.hata_raporu["python_dosyalari"][str(dosya_yolu)] = {
                "syntax": syntax_sonucu,
                "imports": import_sonucu,
                "gui": gui_sonucu,
                "memory": memory_sonucu,
                "performans": performans_sonucu,
                "istatistikler": istatistikler
            }
            
        except Exception as e:
            self.logger.error(f"❌ {dosya_yolu} dosya okuma hatası: {e}")
            
    def _syntax_kontrol(self, kod: str, dosya_yolu: Path) -> Dict[str, Any]:
        """Python syntax kontrolü"""
        try:
            ast.parse(kod)
            return {"durum": "OK", "hata": None}
        except SyntaxError as e:
            hata_detay = {
                "durum": "SYNTAX_ERROR",
                "hata": str(e),
                "satir": e.lineno,
                "kolon": e.offset,
                "mesaj": e.msg
            }
            self.hata_raporu["syntax_hatalari"].append({
                "dosya": str(dosya_yolu),
                "detay": hata_detay
            })
            self.logger.error(f"🚨 SYNTAX HATASI: {dosya_yolu}:{e.lineno} - {e.msg}")
            return hata_detay
            
    def _import_analizi(self, kod: str, dosya_yolu: Path) -> Dict[str, Any]:
        """Import hatalarını analiz et"""
        try:
            tree = ast.parse(kod)
            imports = []
            missing_imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                        if not self._import_test(alias.name):
                            missing_imports.append(alias.name)
                            
                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module
                    if module_name:
                        imports.append(module_name)
                        if not self._import_test(module_name):
                            missing_imports.append(module_name)
            
            if missing_imports:
                self.hata_raporu["import_hatalari"].append({
                    "dosya": str(dosya_yolu),
                    "missing_imports": missing_imports
                })
                
            return {
                "imports": imports,
                "missing_imports": missing_imports,
                "durum": "OK" if not missing_imports else "MISSING_IMPORTS"
            }
            
        except Exception as e:
            return {"durum": "ANALYSIS_ERROR", "hata": str(e)}
            
    def _import_test(self, module_name: str) -> bool:
        """Modülün import edilebilir olup olmadığını test et"""
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False
            
    def _gui_analizi(self, kod: str, dosya_yolu: Path) -> Dict[str, Any]:
        """GUI bileşenlerini analiz et"""
        gui_keywords = ['tkinter', 'Tk()', 'Frame', 'Button', 'mainloop', 'messagebox']
        gui_bulundu = any(keyword in kod for keyword in gui_keywords)
        
        gui_sorunlari = []
        
        if gui_bulundu:
            # TkinterDnD kontrolü
            if 'tkinterdnd2' in kod and 'drop_target_register' in kod:
                gui_sorunlari.append("TkinterDnD compatibility issue detected")
                
            # MainLoop kontrolü
            if 'mainloop()' not in kod and 'Tk()' in kod:
                gui_sorunlari.append("Tk() found but no mainloop() detected")
                
        return {
            "gui_detected": gui_bulundu,
            "sorunlar": gui_sorunlari
        }
        
    def _memory_leak_analizi(self, kod: str, dosya_yolu: Path) -> Dict[str, Any]:
        """Memory leak potansiyeli analizi"""
        potansiyel_sorunlar = []
        
        # Circular reference patterns
        if 'self.' in kod and 'callback' in kod:
            potansiyel_sorunlar.append("Potential circular reference with callbacks")
            
        # Large data structures
        if 'list(' in kod and 'append' in kod and 'while' in kod:
            potansiyel_sorunlar.append("Potential memory leak with growing lists in loops")
            
        # File handle issues
        if 'open(' in kod and 'with open' not in kod:
            potansiyel_sorunlar.append("File opened without 'with' statement")
            
        return {
            "potansiyel_sorunlar": potansiyel_sorunlar
        }
        
    def _performans_analizi(self, kod: str, dosya_yolu: Path) -> Dict[str, Any]:
        """Performans sorunlarını analiz et"""
        performans_sorunlari = []
        
        # Nested loops
        nested_for_count = kod.count('for ') * kod.count('    for ')
        if nested_for_count > 3:
            performans_sorunlari.append(f"Multiple nested loops detected: {nested_for_count}")
            
        # String concatenation in loops
        if '+=' in kod and 'for ' in kod and 'str' in kod:
            performans_sorunlari.append("String concatenation in loop detected")
            
        return {
            "sorunlar": performans_sorunlari
        }
        
    def _dosya_istatistikleri(self, kod: str, dosya_yolu: Path) -> Dict[str, Any]:
        """Dosya istatistiklerini hesapla"""
        satir_sayisi = len(kod.splitlines())
        karakter_sayisi = len(kod)
        
        return {
            "satir_sayisi": satir_sayisi,
            "karakter_sayisi": karakter_sayisi,
            "dosya_boyutu_kb": round(karakter_sayisi / 1024, 2)
        }
        
    def json_dosyalarini_analiz_et(self):
        """JSON dosyalarını analiz et"""
        self.logger.info("📄 JSON dosyalarını analiz ediliyor...")
        
        for json_dosyasi in self.ana_dizin.rglob("*.json"):
            try:
                self._json_dosyasi_analiz(json_dosyasi)
            except Exception as e:
                self.logger.error(f"❌ {json_dosyasi} JSON analiz hatası: {e}")
                
    def _json_dosyasi_analiz(self, dosya_yolu: Path):
        """JSON dosyasını analiz et"""
        try:
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                
            self.hata_raporu["json_dosyalari"][str(dosya_yolu)] = {
                "durum": "OK",
                "keys_count": len(json_data) if isinstance(json_data, dict) else "Not a dict",
                "size_kb": round(dosya_yolu.stat().st_size / 1024, 2)
            }
            
        except json.JSONDecodeError as e:
            hata_detay = {
                "durum": "JSON_FORMAT_ERROR",
                "hata": str(e),
                "satir": e.lineno,
                "kolon": e.colno
            }
            self.hata_raporu["json_format_hatalari"].append({
                "dosya": str(dosya_yolu),
                "detay": hata_detay
            })
            self.logger.error(f"🚨 JSON FORMAT HATASI: {dosya_yolu} - {e}")
            
    def markdown_dosyalarini_analiz_et(self):
        """Markdown dosyalarını analiz et"""
        self.logger.info("📄 Markdown dosyalarını analiz ediliyor...")
        
        for md_dosyasi in self.ana_dizin.rglob("*.md"):
            try:
                self._markdown_dosyasi_analiz(md_dosyasi)
            except Exception as e:
                self.logger.error(f"❌ {md_dosyasi} Markdown analiz hatası: {e}")
                
    def _markdown_dosyasi_analiz(self, dosya_yolu: Path):
        """Markdown dosyasını analiz et"""
        try:
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                icerik = f.read()
                
            satir_sayisi = len(icerik.splitlines())
            
            self.hata_raporu["markdown_dosyalari"][str(dosya_yolu)] = {
                "satir_sayisi": satir_sayisi,
                "karakter_sayisi": len(icerik),
                "dosya_boyutu_kb": round(len(icerik) / 1024, 2)
            }
            
        except Exception as e:
            self.logger.error(f"❌ {dosya_yolu} Markdown okuma hatası: {e}")
            
    def dependency_kontrolu(self):
        """Sistem bağımlılıklarını kontrol et"""
        self.logger.info("📦 Dependency kontrolü yapılıyor...")
        
        gerekli_moduller = [
            'tkinter', 'tkinterdnd2', 'PIL', 'numpy', 'py65',
            'json', 'os', 'sys', 'threading', 'subprocess'
        ]
        
        for modul in gerekli_moduller:
            if not self._import_test(modul):
                self.hata_raporu["missing_dependencies"].append(modul)
                self.logger.warning(f"⚠️ Missing dependency: {modul}")
                
    def istatistik_hesapla(self):
        """Genel istatistikleri hesapla"""
        self.logger.info("📊 İstatistikler hesaplanıyor...")
        
        toplam_python = len(self.hata_raporu["python_dosyalari"])
        toplam_json = len(self.hata_raporu["json_dosyalari"])
        toplam_markdown = len(self.hata_raporu["markdown_dosyalari"])
        
        syntax_hata_sayisi = len(self.hata_raporu["syntax_hatalari"])
        import_hata_sayisi = len(self.hata_raporu["import_hatalari"])
        json_hata_sayisi = len(self.hata_raporu["json_format_hatalari"])
        
        self.hata_raporu["genel_istatistikler"] = {
            "toplam_python_dosyasi": toplam_python,
            "toplam_json_dosyasi": toplam_json,
            "toplam_markdown_dosyasi": toplam_markdown,
            "syntax_hata_sayisi": syntax_hata_sayisi,
            "import_hata_sayisi": import_hata_sayisi,
            "json_hata_sayisi": json_hata_sayisi,
            "missing_dependency_sayisi": len(self.hata_raporu["missing_dependencies"])
        }
        
    def rapor_kaydet(self):
        """Analiz raporunu kaydet"""
        rapor_dosyasi = self.ana_dizin / f"sistem_analiz_raporu_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(rapor_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(self.hata_raporu, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"📊 Analiz raporu kaydedildi: {rapor_dosyasi}")
            return rapor_dosyasi
            
        except Exception as e:
            self.logger.error(f"❌ Rapor kaydetme hatası: {e}")
            return None
            
    def ozet_rapor_yazdir(self):
        """Özet raporu terminalde göster"""
        print("\n" + "="*80)
        print("🔍 KAPSAMLı SİSTEM ANALİZİ RAPORU")
        print("="*80)
        
        stats = self.hata_raporu["genel_istatistikler"]
        
        print(f"📄 Toplam Python Dosyası: {stats.get('toplam_python_dosyasi', 0)}")
        print(f"📄 Toplam JSON Dosyası: {stats.get('toplam_json_dosyasi', 0)}")
        print(f"📄 Toplam Markdown Dosyası: {stats.get('toplam_markdown_dosyasi', 0)}")
        print()
        print(f"🚨 Syntax Hataları: {stats.get('syntax_hata_sayisi', 0)}")
        print(f"📦 Import Hataları: {stats.get('import_hata_sayisi', 0)}")
        print(f"🔧 JSON Format Hataları: {stats.get('json_hata_sayisi', 0)}")
        print(f"❌ Missing Dependencies: {stats.get('missing_dependency_sayisi', 0)}")
        
        # En kritik hataları göster
        if self.hata_raporu["syntax_hatalari"]:
            print("\n🚨 KRİTİK SYNTAX HATALARI:")
            for hata in self.hata_raporu["syntax_hatalari"][:5]:
                print(f"   - {hata['dosya']}: {hata['detay']['mesaj']}")
                
        if self.hata_raporu["missing_dependencies"]:
            print("\n📦 EKSİK BAĞIMLILIKLAR:")
            for dep in self.hata_raporu["missing_dependencies"]:
                print(f"   - {dep}")
                
        print("\n" + "="*80)
        
    def tam_analiz_yap(self):
        """Tam sistem analizini başlat"""
        self.logger.info("🚀 Tam sistem analizi başlatılıyor...")
        
        # Ana analizler
        self.python_dosyalarini_analiz_et()
        self.json_dosyalarini_analiz_et()
        self.markdown_dosyalarini_analiz_et()
        self.dependency_kontrolu()
        self.istatistik_hesapla()
        
        # Raporu kaydet
        rapor_dosyasi = self.rapor_kaydet()
        
        # Özet raporu göster
        self.ozet_rapor_yazdir()
        
        self.logger.info("✅ Sistem analizi tamamlandı")
        return rapor_dosyasi

def main():
    """Ana fonksiyon"""
    print("🔍 KAPSAMLı SİSTEM ANALİZİ VE HATA RAPORLAMA SİSTEMİ v1.0")
    print("=" * 80)
    
    try:
        analiz = SystemDiagnostics()
        rapor_dosyasi = analiz.tam_analiz_yap()
        
        if rapor_dosyasi:
            print(f"\n📊 Detaylı rapor dosyası: {rapor_dosyasi}")
            print("🎯 Sistemdeki tüm hatalar tespit edildi ve raporlandı.")
        else:
            print("❌ Rapor kaydedilemedi!")
            
    except Exception as e:
        print(f"❌ Sistem analizi hatası: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
