# 🔧 **DIŞ ARAÇ KOLEKSİYONU - DETAYLI ENVANTERİ**
## External Tools Collection - Comprehensive Inventory

**Konum:** `disaridan_kullanilacak_ornek_programlar/` klasörü  
**Toplam:** 100+ geliştirme aracı ve kütüphane  
**Durum:** Entegrasyona hazır, alt süreç köprü sistemi (subprocess bridge system) gerekli  
**Hedef:** Commodore 64 Geliştirme Stüdyosu ekosistemi entegrasyonu  

---

## 📁 **ANA ARAÇ KATEGORİLERİ**

### **🔨 ASSEMBLER ARAÇLARI**

#### **1. 64TASS (Turbo Assembler)**
**Konum:** `64tass-src/`  
**Açıklama:** Ultra hızlı 65xx serisi assembler  
**Özellikler:** 
- 6502/65C02/65816/65CE02/65DTV02 desteği
- Makro ve şartlı assembly (conditional assembly)
- Çoklu format çıktısı (multiple output formats)
- Hata raporlama sistemi (error reporting system)

**Entegrasyon parametreleri:**
```
Yürütülebilir: 64tass.exe
Komut şablonu: %executable% --ascii --case-sensitive %input% -o %output%
Desteklenen formatlar: .asm, .s
Çıktı formatları: PRG, BIN, D64
```

#### **2. ACME Cross-Assembler**
**Konum:** `acme-main/`  
**Açıklama:** Çapraz platform assembler (cross-platform assembler)  
**Özellikler:**
- Çoklu işlemci desteği (multi-processor support)
- Gelişmiş makro sistemi (advanced macro system)
- Sembol dosyası üretimi (symbol file generation)
- Pseudo-opcodes desteği

**Entegrasyon parametreleri:**
```
Yürütülebilir: acme.exe
Komut şablonu: %executable% --format cbm --outfile %output% %input%
Desteklenen formatlar: .asm, .a
Özel özellikler: Symbol export, listing files
```

#### **3. DASM Assembler**
**Konum:** `dasm-master/`  
**Açıklama:** Popüler 6502 assembler  
**Özellikler:**
- 6502/6507/6803 desteği
- Sembol tablosu üretimi (symbol table generation)
- Liste dosyası çıktısı (listing file output)
- Makro ve include desteği

**Entegrasyon parametreleri:**
```
Yürütülebilir: dasm.exe
Komut şablonu: %executable% %input% -f3 -o%output%
Çıktı formatları: BIN, PRG
Ek özellikler: -s%symbols% -l%listing%
```

#### **4. Mad Assembler**
**Konum:** `Mad-Assembler-2.1.6/`  
**Açıklama:** Gelişmiş özellikli assembler  
**Özellikler:**
- Atari ve C64 optimizasyonları
- Gelişmiş makro sistemi
- Şartlı derleme (conditional compilation)
- Hata ayıklama sembolleri (debugging symbols)

### **⚙️ DERLEYİCİLER (COMPILERS)**

#### **5. Oscar64 C Compiler**
**Konum:** `oscar64-main/`  
**Açıklama:** C64 için özelleştirilmiş C derleyicisi  
**Özellikler:**
- C89/C99 subset desteği
- C64 donanım optimizasyonları
- Inline assembly desteği
- Çeşitli bellek modelleri (memory models)

**Entegrasyon parametreleri:**
```
Yürütülebilir: oscar64.exe
Komut şablonu: %executable% -o=%output% %input%
Desteklenen formatlar: .c
Çıktı formatları: PRG, D64
Optimizasyon seviyeleri: -O0, -O1, -O2, -O3
```

#### **6. CC65 C Compiler Suite**
**Konum:** `cc65-main/` (ek araç)  
**Açıklama:** Tam C geliştirme ortamı  
**Özellikler:**
- C compiler (cl65)
- Assembler (ca65)
- Linker (ld65)
- Librarian (ar65)

### **💻 DEVELOPMENT ENVIRONMENTS**

#### **7. CrossViper IDE**
**Konum:** `crossviper-master/`  
**Açıklama:** Tam Python tabanlı geliştirme ortamı  
**Ana modüller:**
- `main.py` - IDE launcher
- `codeeditor.py` - Sözdizimi vurgulamalı editör (syntax highlighting editor)
- `configuration.py` - Konfigürasyon yöneticisi
- `terminal_window.py` - Terminal entegrasyonu

**Özellikler:**
- Çoklu dosya editörü (multi-file editor)
- Proje yönetimi (project management)
- Yapı sistemi entegrasyonu (build system integration)
- Terminal emülatörü (terminal emulator)

**Entegrasyon hedefleri:**
```
C64 proje şablonları ekleme
Assembly syntax highlighting optimizasyonu
Disassembler entegrasyonu
Memory map görüntüleyici ekleme
```

### **🔍 ANALİZ VE HATA AYIKLAMA ARAÇLARI**

#### **8. Python Disassemblator 6502/6510**
**Konum:** `Python Disassemblator 6502_6510/`  
**Açıklama:** Python tabanlı disassembler  
**Özellikler:**
- 6502/6510 opcode desteği
- Sembol tanıma (symbol recognition)
- Kod akış analizi (code flow analysis)
- Çoklu format çıktısı

#### **9. 6502Asm Assembler**
**Konum:** `6502Asm-main/`  
**Açıklama:** Minimal 6502 assembler  
**Özellikler:**
- Basit sözdizimi (simple syntax)
- Hızlı derleme (fast compilation)
- Eğitim amaçlı kullanım (educational use)

### **📚 KÜTÜPHANE VE INTERPRETER'LAR**

#### **10. CBM BASIC Interpreter**
**Konum:** `cbmbasic/`  
**Açıklama:** Commodore BASIC interpreter  
**Özellikler:**
- Tam Commodore BASIC v2.0 uyumluluğu
- Komut satırı kullanımı (command line usage)
- BASIC program yürütme
- Token analizi (token analysis)

**Entegrasyon hedefleri:**
```
BASIC program doğrulama (validation)
Token çevirisi (token translation)
Syntax checking
Test ortamı (testing environment)
```

---

## 🔗 **ENTEGRASYON STRATEJİSİ**

### **Alt Süreç Köprü Sistemi (Subprocess Bridge System)**

#### **Temel Mimari:**
```python
class DışAraçKöprüsü:
    def __init__(self):
        self.araç_veritabanı = self.yükle_araç_veritabanı()
        self.şablon_işleyici = ŞablonDeğişkenİşleyici()
        
    def araç_yürüt(self, araç_adı, giriş_dosyası, çıktı_dosyası):
        # Araç konfigürasyonu yükle
        # Şablon değişkenleri işle
        # Alt süreç başlat
        # Sonuç yakala ve işle
        pass
```

#### **Şablon Değişken Sistemi:**
```json
{
  "global_variables": {
    "%workspace%": "Aktif çalışma dizini",
    "%project_name%": "Proje adı",
    "%timestamp%": "Zaman damgası"
  },
  "file_variables": {
    "%input_file%": "Giriş dosyası tam yolu",
    "%output_file%": "Çıktı dosyası tam yolu",
    "%file_name%": "Dosya adı (uzantısız)",
    "%file_extension%": "Dosya uzantısı"
  },
  "assembler_variables": {
    "%symbols_file%": "Sembol dosyası yolu",
    "%listing_file%": "Liste dosyası yolu",
    "%optimization_level%": "Optimizasyon seviyesi"
  }
}
```

### **Konfigürasyon Yönetimi**

#### **Araç Tespit Sistemi:**
```python
def araçları_tespit_et():
    """Sistem üzerindeki mevcut araçları tespit et"""
    tespit_edilen_araçlar = {}
    
    for araç in STANDARt_ARAÇLAR:
        if araç_mevcut_mu(araç):
            tespit_edilen_araçlar[araç] = araç_bilgisi_al(araç)
    
    return tespit_edilen_araçlar
```

#### **Kurulum Yardımcısı:**
```python
def araç_kurulum_rehberi(araç_adı):
    """Belirli bir araç için kurulum rehberi göster"""
    rehber = KURULUM_REHBERLERİ[araç_adı]
    return {
        'indirme_linki': rehber['download_url'],
        'kurulum_adımları': rehber['installation_steps'],
        'test_komutu': rehber['test_command'],
        'konfigürasyon_örnegi': rehber['config_example']
    }
```

### **Hata İşleme ve Geri Bildirim**

#### **Hata Kategorileri:**
- **Araç Bulunamadı:** Sistemde yürütülebilir dosya mevcut değil
- **Konfigürasyon Hatası:** Geçersiz parametre veya yol
- **Derleme Hatası:** Kaynak kodda syntax veya logic hata
- **Sistem Hatası:** İzin, bellek veya dosya sistemi problemleri

#### **Kullanıcı Geri Bildirimi:**
```python
class Hataİşleyici:
    def hata_raporu_oluştur(self, hata_türü, hata_mesajı, öneriler):
        return {
            'hata_türü': hata_türü,
            'açıklama': hata_mesajı,
            'önerilen_çözümler': öneriler,
            'yardım_linki': self.yardım_linkini_oluştur(hata_türü),
            'hata_kodu': self.hata_kodu_üret()
        }
```

---

## 📊 **ARAÇ KALİTE DEĞERLENDİRMESİ**

### **Öncelik Matrisi:**

| Araç | Zorluk | Entegrasyon Süresi | Kullanıcı Fayda | Öncelik |
|------|--------|-------------------|------------------|---------|
| 64TASS | Kolay | 2 saat | Yüksek | 🟢 1 |
| ACME | Kolay | 2 saat | Yüksek | 🟢 1 |
| DASM | Kolay | 1 saat | Orta | 🟡 2 |
| Oscar64 | Orta | 4 saat | Çok Yüksek | 🟢 1 |
| CrossViper | Zor | 8 saat | Çok Yüksek | 🔴 3 |
| CBM BASIC | Kolay | 1 saat | Orta | 🟡 2 |

### **Entegrasyon Aşamaları:**

#### **Aşama 1 (1-2 Gün):** Temel Assembler'lar
- 64TASS, ACME, DASM entegrasyonu
- Basit komut şablonu sistemi
- Temel hata yakalama

#### **Aşama 2 (3-4 Gün):** Derleyici Entegrasyonu
- Oscar64 C compiler entegrasyonu
- Gelişmiş parametre sistemi
- Çoklu format desteği

#### **Aşama 3 (1 Hafta):** IDE Entegrasyonu
- CrossViper IDE tam entegrasyonu
- Proje şablonu sistemi
- Gelişmiş hata ayıklama

---

## 🎯 **KULLANIM SENARYOLARI**

### **Senaryo 1: Assembly Geliştirme**
1. Kullanıcı `.asm` dosyası oluşturur
2. Sistem otomatik olarak 64TASS'ı önerir
3. Tek tıkla derleme işlemi
4. Sonuç PRG dosyası otomatik test edilir

### **Senaryo 2: C Geliştirme**
1. Kullanıcı `.c` dosyası oluşturur
2. Oscar64 otomatik seçilir
3. C kod analizi ve uyarılar
4. C64 optimizasyonları uygulanır

### **Senaryo 3: Tam Proje Geliştirme**
1. CrossViper IDE başlatılır
2. C64 proje şablonu seçilir
3. Çoklu dosya editörü ile geliştirme
4. Entegre build sistemi ile derleme

---

## 🔧 **TEKNİK GEREKSINIMLER**

### **Sistem Gereksinimleri:**
- **Python 3.8+** - Temel interpreter
- **subprocess modülü** - Alt süreç yönetimi
- **json modülü** - Konfigürasyon yönetimi
- **pathlib modülü** - Dosya yolu işlemleri
- **tkinter** - GUI entegrasyonu

### **Dış Bağımlılıklar:**
- **Windows:** Win32 API erişimi
- **Linux:** bash shell erişimi
- **macOS:** POSIX shell erişimi

### **Güvenlik Gereksinimleri:**
- Komut enjeksiyonu koruması (command injection protection)
- Dosya sistemi erişim kontrolü
- Kullanıcı izin doğrulaması

---

**📋 Dosya Durumu:** Dış Araç Koleksiyonu - Entegrasyona Hazır  
**🔄 Son Güncellenme:** 25 Aralık 2024  
**✅ Entegrasyon Hedefi:** Alt süreç köprü sistemi ile tam otomasyon  
**🎯 İlk Hedef:** 64TASS, ACME, DASM temel entegrasyonu (2 gün içinde)
