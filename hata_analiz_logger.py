#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍎 Hata Analiz Logger v5.3 - Commodore 64 Geliştirme Stüdyosu
================================================================
PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: hata_analiz_logger.py - Kapsamlı Hata Analizi ve Loglama Sistemi
VERSİYON: 5.3 (Kapsamlı GUI İzleme ve Hata Analizi)
AMAÇ: Her işlemi, hatayı, GUI etkileşimini, terminal çıktısını loglama
================================================================

Bu modül şu özelliklerle kapsamlı loglama yapar:
• GUI Etkileşim Takibi: Her butona tıklama, disk seçimi, dosya seçimi
• Terminal Output Loglama: Tüm terminal çıktıları ve hata mesajları
• Program Çıktı Analizi: Disassembly, decompile sonuçları
• JSON Tabanlı Loglama: Zaman damgalı detaylı kayıtlar
• Otomatik Backup Sistemi: .bak dosyaları ve klasör yönetimi
• Boyut Kontrolü: 10MB limit ve otomatik temizlik
================================================================
"""

import json
import os
import shutil
import datetime
import threading
import traceback
from pathlib import Path

class HataAnalizLogger:
    """Kapsamlı hata analizi ve loglama sistemi"""
    
    def __init__(self, ana_dizin="c:\\Users\\dell\\Documents\\projeler\\d64_converter"):
        self.ana_dizin = Path(ana_dizin)
        self.hata_analiz_dosyasi = self.ana_dizin / "hataanaliz.json"
        self.hata_analiz_klasoru = self.ana_dizin / "hataanaliz"
        self.mevcut_session = None
        self.lock = threading.Lock()
        
        # Klasör oluştur
        self._klasor_olustur()
        
        # Önceki dosyayı backup yap
        self._onceki_dosya_backup()
        
        # Yeni session başlat
        self._yeni_session_baslat()
    
    def _klasor_olustur(self):
        """Hata analiz klasörünü oluştur"""
        try:
            self.hata_analiz_klasoru.mkdir(exist_ok=True)
            print(f"✅ Hata analiz klasörü hazır: {self.hata_analiz_klasoru}")
        except Exception as e:
            print(f"❌ Hata analiz klasörü oluşturulamadı: {e}")
    
    def _onceki_dosya_backup(self):
        """Önceki hataanaliz.json dosyasını backup yap"""
        try:
            if self.hata_analiz_dosyasi.exists():
                # Önceki .bak dosyasını hataanaliz klasörüne taşı
                bak_dosyasi = self.ana_dizin / "hataanaliz.bak"
                if bak_dosyasi.exists():
                    zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    hedef_dosya = self.hata_analiz_klasoru / f"hataanaliz_{zaman_damgasi}.json"
                    shutil.move(str(bak_dosyasi), str(hedef_dosya))
                    print(f"✅ Önceki .bak dosyası taşındı: {hedef_dosya}")
                
                # Mevcut dosyayı .bak yap
                shutil.copy2(str(self.hata_analiz_dosyasi), str(bak_dosyasi))
                print(f"✅ Mevcut dosya backup yapıldı: {bak_dosyasi}")
        except Exception as e:
            print(f"⚠️ Backup işlemi hatası: {e}")
    
    def _yeni_session_baslat(self):
        """Yeni loglama session'ı başlat"""
        try:
            baslangic_zamani = datetime.datetime.now()
            self.mevcut_session = {
                "session_info": {
                    "baslangic_zamani": baslangic_zamani.isoformat(),
                    "program_versiyonu": "Enhanced D64 Converter v5.3",
                    "kizilelma_plan_durumu": "AŞAMA 1 - Hibrit Analiz Entegrasyonu Tamamlandı",
                    "session_id": baslangic_zamani.strftime("%Y%m%d_%H%M%S"),
                    "python_versiyonu": self._python_versiyon_al(),
                    "isletim_sistemi": self._os_bilgi_al()
                },
                "terminal_ciktilari": [],
                "gui_etkilesimleri": [],
                "disk_imaji_islemleri": [],
                "program_dosya_islemleri": [],
                "disassembly_islemleri": [],
                "decompile_islemleri": [],
                "hatalar": [],
                "performans_metrikleri": [],
                "memory_kullanimi": [],
                "sistem_durum": "BAŞLATILIYOR"
            }
            
            # İlk log
            self.log_terminal("🍎 Hata Analiz Logger v5.3 başlatıldı")
            self.log_terminal(f"📅 Session ID: {self.mevcut_session['session_info']['session_id']}")
            self.log_terminal(f"💾 Log dosyası: {self.hata_analiz_dosyasi}")
            
            self._dosya_kaydet()
            
        except Exception as e:
            print(f"❌ Session başlatma hatası: {e}")
            traceback.print_exc()
    
    def _python_versiyon_al(self):
        """Python versiyon bilgisini al"""
        try:
            import sys
            return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        except:
            return "Bilinmiyor"
    
    def _os_bilgi_al(self):
        """İşletim sistemi bilgisini al"""
        try:
            import platform
            return f"{platform.system()} {platform.release()} {platform.architecture()[0]}"
        except:
            return "Bilinmiyor"
    
    def log_terminal(self, mesaj, seviye="INFO"):
        """Terminal çıktısını logla"""
        try:
            with self.lock:
                zaman = datetime.datetime.now().isoformat()
                log_entry = {
                    "zaman": zaman,
                    "seviye": seviye,
                    "mesaj": str(mesaj),
                    "thread": threading.current_thread().name
                }
                
                self.mevcut_session["terminal_ciktilari"].append(log_entry)
                
                # Konsola da yazdır
                print(f"[{zaman}] [{seviye}] {mesaj}")
                
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ Terminal log hatası: {e}")
    
    def log_gui_etkileskim(self, etkileskim_turu, detaylar):
        """GUI etkileşimini logla"""
        try:
            with self.lock:
                zaman = datetime.datetime.now().isoformat()
                log_entry = {
                    "zaman": zaman,
                    "etkileskim_turu": etkileskim_turu,
                    "detaylar": detaylar
                }
                
                self.mevcut_session["gui_etkilesimleri"].append(log_entry)
                self.log_terminal(f"🖱️ GUI: {etkileskim_turu} - {detaylar}")
                
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ GUI etkileşim log hatası: {e}")
    
    def log_disk_imaji(self, dosya_yolu, islem_turu, sonuc, detaylar=None):
        """Disk imajı işlemini logla"""
        try:
            with self.lock:
                zaman = datetime.datetime.now().isoformat()
                log_entry = {
                    "zaman": zaman,
                    "dosya_yolu": str(dosya_yolu),
                    "islem_turu": islem_turu,
                    "sonuc": sonuc,
                    "detaylar": detaylar or {}
                }
                
                self.mevcut_session["disk_imaji_islemleri"].append(log_entry)
                self.log_terminal(f"💾 Disk: {islem_turu} - {dosya_yolu} - {sonuc}")
                
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ Disk imajı log hatası: {e}")
    
    def log_program_dosya(self, dosya_adi, dosya_turu, boyut, adres_bilgisi, analiz_sonucu=None):
        """Program dosyası seçimini logla"""
        try:
            with self.lock:
                zaman = datetime.datetime.now().isoformat()
                log_entry = {
                    "zaman": zaman,
                    "dosya_adi": dosya_adi,
                    "dosya_turu": dosya_turu,
                    "boyut": boyut,
                    "adres_bilgisi": adres_bilgisi,
                    "analiz_sonucu": analiz_sonucu
                }
                
                self.mevcut_session["program_dosya_islemleri"].append(log_entry)
                self.log_terminal(f"📄 Program: {dosya_adi} ({dosya_turu}) - {boyut} bytes - ${adres_bilgisi}")
                
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ Program dosya log hatası: {e}")
    
    def log_disassembly(self, disassembler_turu, girdi_boyutu, cikti_boyutu, sure, hata=None):
        """Disassembly işlemini logla"""
        try:
            with self.lock:
                zaman = datetime.datetime.now().isoformat()
                log_entry = {
                    "zaman": zaman,
                    "disassembler_turu": disassembler_turu,
                    "girdi_boyutu": girdi_boyutu,
                    "cikti_boyutu": cikti_boyutu,
                    "sure_saniye": sure,
                    "hata": hata,
                    "basarili": hata is None
                }
                
                self.mevcut_session["disassembly_islemleri"].append(log_entry)
                durum = "✅ BAŞARILI" if hata is None else f"❌ HATA: {hata}"
                self.log_terminal(f"⚙️ Disassembly: {disassembler_turu} - {girdi_boyutu}→{cikti_boyutu} bytes - {sure:.2f}s - {durum}")
                
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ Disassembly log hatası: {e}")
    
    def log_decompile(self, decompiler_turu, hedef_dil, girdi_boyutu, cikti_boyutu, sure, hata=None):
        """Decompile işlemini logla"""
        try:
            with self.lock:
                zaman = datetime.datetime.now().isoformat()
                log_entry = {
                    "zaman": zaman,
                    "decompiler_turu": decompiler_turu,
                    "hedef_dil": hedef_dil,
                    "girdi_boyutu": girdi_boyutu,
                    "cikti_boyutu": cikti_boyutu,
                    "sure_saniye": sure,
                    "hata": hata,
                    "basarili": hata is None
                }
                
                self.mevcut_session["decompile_islemleri"].append(log_entry)
                durum = "✅ BAŞARILI" if hata is None else f"❌ HATA: {hata}"
                self.log_terminal(f"🔄 Decompile: {decompiler_turu}→{hedef_dil} - {girdi_boyutu}→{cikti_boyutu} bytes - {sure:.2f}s - {durum}")
                
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ Decompile log hatası: {e}")
    
    def log_hata(self, hata_turu, hata_mesaji, dosya=None, satir=None, stack_trace=None):
        """Hata logla"""
        try:
            with self.lock:
                zaman = datetime.datetime.now().isoformat()
                log_entry = {
                    "zaman": zaman,
                    "hata_turu": hata_turu,
                    "hata_mesaji": str(hata_mesaji),
                    "dosya": dosya,
                    "satir": satir,
                    "stack_trace": stack_trace or traceback.format_exc()
                }
                
                self.mevcut_session["hatalar"].append(log_entry)
                self.log_terminal(f"❌ HATA: {hata_turu} - {hata_mesaji}", "ERROR")
                
                if stack_trace:
                    self.log_terminal(f"📍 Stack Trace: {stack_trace}", "ERROR")
                
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ Hata log hatası: {e}")
    
    def log_performans(self, islem_adi, sure, memory_kullanimi=None):
        """Performans metriği logla"""
        try:
            with self.lock:
                zaman = datetime.datetime.now().isoformat()
                log_entry = {
                    "zaman": zaman,
                    "islem_adi": islem_adi,
                    "sure_saniye": sure,
                    "memory_kullanimi_mb": memory_kullanimi
                }
                
                self.mevcut_session["performans_metrikleri"].append(log_entry)
                
                memory_str = f" - {memory_kullanimi:.2f}MB" if memory_kullanimi else ""
                self.log_terminal(f"📊 Performans: {islem_adi} - {sure:.3f}s{memory_str}")
                
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ Performans log hatası: {e}")
    
    def sistem_durum_guncelle(self, yeni_durum):
        """Sistem durumunu güncelle"""
        try:
            with self.lock:
                self.mevcut_session["sistem_durum"] = yeni_durum
                self.log_terminal(f"🔄 Sistem Durumu: {yeni_durum}")
                self._dosya_kaydet()
        except Exception as e:
            print(f"❌ Sistem durum güncelleme hatası: {e}")
    
    def _dosya_kaydet(self):
        """JSON dosyasını kaydet"""
        try:
            # Son güncelleme zamanını ekle
            self.mevcut_session["session_info"]["son_guncelleme"] = datetime.datetime.now().isoformat()
            
            # JSON dosyasını kaydet
            with open(self.hata_analiz_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(self.mevcut_session, f, ensure_ascii=False, indent=2)
            
            # Klasör boyut kontrolü
            self._klasor_boyut_kontrol()
            
        except Exception as e:
            print(f"❌ Dosya kaydetme hatası: {e}")
    
    def _klasor_boyut_kontrol(self):
        """Hata analiz klasörünün boyutunu kontrol et ve temizle"""
        try:
            toplam_boyut = 0
            dosyalar = []
            
            # Klasördeki tüm dosyaları listele
            for dosya in self.hata_analiz_klasoru.glob("*.json"):
                boyut = dosya.stat().st_size
                toplam_boyut += boyut
                dosyalar.append((dosya, boyut, dosya.stat().st_mtime))
            
            # 10MB kontrolü (10 * 1024 * 1024 = 10485760 bytes)
            if toplam_boyut > 10485760:  # 10MB
                # En yeni 5 dosyayı tut, gerisini sil
                dosyalar.sort(key=lambda x: x[2], reverse=True)  # Oluşturma zamanına göre sırala
                
                tutulacak_dosyalar = dosyalar[:5]
                silinecek_dosyalar = dosyalar[5:]
                
                for dosya, _, _ in silinecek_dosyalar:
                    try:
                        dosya.unlink()
                        self.log_terminal(f"🗑️ Eski log dosyası silindi: {dosya.name}")
                    except Exception as e:
                        self.log_terminal(f"⚠️ Dosya silme hatası: {e}")
                
                yeni_toplam = sum(x[1] for x in tutulacak_dosyalar)
                self.log_terminal(f"📦 Klasör temizlendi: {len(silinecek_dosyalar)} dosya silindi, yeni boyut: {yeni_toplam/1024/1024:.2f}MB")
        
        except Exception as e:
            print(f"❌ Klasör boyut kontrol hatası: {e}")
    
    def session_sonlandir(self):
        """Session'ı sonlandır"""
        try:
            with self.lock:
                bitis_zamani = datetime.datetime.now()
                self.mevcut_session["session_info"]["bitis_zamani"] = bitis_zamani.isoformat()
                
                # Toplam istatistikler
                self.mevcut_session["session_istatistikleri"] = {
                    "toplam_terminal_loglari": len(self.mevcut_session["terminal_ciktilari"]),
                    "toplam_gui_etkilesimleri": len(self.mevcut_session["gui_etkilesimleri"]),
                    "toplam_disk_islemleri": len(self.mevcut_session["disk_imaji_islemleri"]),
                    "toplam_program_islemleri": len(self.mevcut_session["program_dosya_islemleri"]),
                    "toplam_disassembly_islemleri": len(self.mevcut_session["disassembly_islemleri"]),
                    "toplam_decompile_islemleri": len(self.mevcut_session["decompile_islemleri"]),
                    "toplam_hatalar": len(self.mevcut_session["hatalar"]),
                    "toplam_performans_metrikleri": len(self.mevcut_session["performans_metrikleri"])
                }
                
                self.sistem_durum_guncelle("SONLANDIRILDI")
                self.log_terminal("🏁 Hata Analiz Logger session sonlandırıldı")
                
                self._dosya_kaydet()
        
        except Exception as e:
            print(f"❌ Session sonlandırma hatası: {e}")


# Global logger instance
hata_logger = None

def init_hata_logger():
    """Global hata logger'ı başlat"""
    global hata_logger
    if hata_logger is None:
        hata_logger = HataAnalizLogger()
    return hata_logger

def get_hata_logger():
    """Global hata logger'ı al"""
    global hata_logger
    if hata_logger is None:
        hata_logger = init_hata_logger()
    return hata_logger

# Otomatik başlatma
if __name__ == "__main__":
    logger = init_hata_logger()
    logger.log_terminal("🍎 Hata Analiz Logger test modu başlatıldı")
    logger.log_gui_etkileskim("TEST_BUTONU", {"buton": "test", "konum": "ana_menu"})
    logger.log_disk_imaji("test.d64", "YUKLEME", "BAŞARILI", {"format": "D64", "boyut": 170240})
    logger.session_sonlandir()
    print("✅ Test tamamlandı!")
