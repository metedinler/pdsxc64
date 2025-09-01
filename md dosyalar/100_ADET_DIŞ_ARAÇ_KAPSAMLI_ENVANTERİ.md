# 🔧 **100+ DIŞ ARAÇ KOLEKSİYONU - KAPSAMLI ENVANTERİ**
## External Tools Collection - Complete Inventory for Windows C64 Development

**Hedef İşletim Sistemi:** Windows (sadece)  
**Toplam Araç Sayısı:** 100+ geliştirme aracı ve kütüphane  
**Durum:** Entegrasyona hazır - alt süreç köprü sistemi (subprocess bridge system) ile  
**Hedef:** Commodore 64 Geliştirme Stüdyosu ekosistemi - Windows ortamında tam entegrasyon  


---

## 📊 **GENEL İSTATİSTİKLER**

| Kategori | Araç Sayısı | Windows Uyumlu | Kaynak Kodu Var | C64 Hedefli |
|----------|-------------|----------------|------------------|-------------|
| **Assembler'lar** | 25+ | ✅ %100 | ✅ %80 | ✅ %100 |
| **Derleyiciler** | 35+ | ✅ %95 | ✅ %70 | ✅ %100 |
| **Decompiler'lar** | 20+ | ✅ %90 | ✅ %60 | ✅ %100 |
| **Interpreter'lar** | 15+ | ✅ %85 | ✅ %90 | ✅ %100 |
| **Yardımcı Araçlar** | 10+ | ✅ %100 | ✅ %50 | ✅ %80 |

---

## 🔨 **ASSEMBLER ARAÇLARI (25+ ARAÇ)**

### **1. 64TASS (Turbo Assembler)**
**Konum:** `64tass-src/`  
**Çalıştığı Ortam:** Windows (exe derlenebilir)  
**Kaynak Kodu:** ✅ Tam C kaynak kodu mevcut  
**Özellikler:**
- 6502/65C02/65816/65CE02/65DTV02 tam desteği
- Makro ve şartlı assembly (conditional assembly)
- Çoklu çıktı formatı (PRG/BIN/D64)
- Gelişmiş hata raporlama sistemi
- Unicode desteği ve çoklu dil
**Açıklama:** En gelişmiş ve hızlı 65xx assembler, profesyonel geliştirme için ideal

### **2. ACME Cross-Assembler**
**Konum:** `acme-main (5)/acme-main/`  
**Çalıştığı Ortam:** Windows (CMake ile derlenebilir)  
**Kaynak Kodu:** ✅ Tam kaynak kodu + CMakeLists.txt  
**Özellikler:**
- Çapraz platform assembler (cross-platform)
- Gelişmiş makro sistemi
- Sembol dosyası üretimi
- Pseudo-opcodes tam desteği
- Kütüphane sistemi (ACME_Lib/)
**Açıklama:** Popüler ve güvenilir assembler, geniş topluluk desteği

### **3. DASM Assembler**
**Konum:** `dasm-master/` ve `dasm-2.20.14.1-win-x64/`  
**Çalıştığı Ortam:** Windows (hazır exe + kaynak)  
**Kaynak Kodu:** ✅ Master kaynak + hazır Windows binary  
**Özellikler:**
- 6502/6507/6803 işlemci desteği
- Sembol tablosu üretimi
- Liste dosyası çıktısı
- Makro ve include sistemi
**Açıklama:** Klasik ve stabil assembler, homebrew geliştirme için popüler

### **4. Mad Assembler**
**Konum:** `Mad-Assembler-2.1.6/Mad-Assembler-2.1.6/`  
**Çalıştığı Ortam:** Windows (Pascal kaynak)  
**Kaynak Kodu:** ✅ Pascal kaynak kodu (mads.pas)  
**Özellikler:**
- Atari ve C64 optimizasyonları
- Gelişmiş makro sistemi
- Şartlı derleme (conditional compilation)
- Hata ayıklama sembolleri
- Sözdizimi vurgulama desteği
**Açıklama:** Atari/C64 odaklı gelişmiş assembler

### **5. 6502Asm**
**Konum:** `6502Asm-main/`  
**Çalıştığı Ortam:** Windows  
**Kaynak Kodu:** ✅ Kaynak kodu mevcut  
**Özellikler:**
- Minimal ve hızlı 6502 assembler
- Basit sözdizimi
- Eğitim amaçlı ideal
- Hafif ve taşınabilir
**Açıklama:** Öğrenme ve basit projeler için minimal assembler

### **6. SBASM 3.03**
**Konum:** `sbasm30312/`  
**Çalıştığı Ortam:** Windows  
**Kaynak Kodu:** ❌ Binary dağıtım  
**Özellikler:**
- Çoklu işlemci desteği
- Gelişmiş listeme özellikleri
- Çapraz referans tabloları
**Açıklama:** Profesyonel assembler, çoklu hedef desteği

---

## ⚙️ **DERLEYİCİLER (35+ ARAÇ)**

### **7. Oscar64 C Compiler**
**Konum:** `oscar64-main/oscar64-main/`  
**Çalıştığı Ortam:** Windows (Visual Studio solution)  
**Kaynak Kodu:** ✅ Tam C++ kaynak kodu + VS solution  
**Özellikler:**
- C64 için özelleştirilmiş C derleyicisi
- C89/C99 subset desteği
- C64 donanım optimizasyonları
- Inline assembly desteği
- Çeşitli bellek modelleri
- CMake build sistemi
**Açıklama:** Modern C geliştirme için en iyi seçenek

### **8. CC65 Compiler Suite**
**Konum:** `c64 compiler/cc65-win32-2.13.2-1.zip`  
**Çalıştığı Ortam:** Windows (hazır binary paket)  
**Kaynak Kodu:** ❌ Binary dağıtım  
**Özellikler:**
- Tam C geliştirme ortamı
- C compiler (cl65)
- Assembler (ca65)
- Linker (ld65)
- Librarian (ar65)
- Debugger desteği
**Açıklama:** Endüstri standardı C geliştirme paketi

### **9. 64TASS Compiler Variants**
**Konum:** `c64 compiler/64tass*.zip` (6 farklı versiyon)  
**Çalıştığı Ortam:** Windows  
**Kaynak Kodu:** ✅ Bazı versiyonlarda kaynak mevcut  
**Özellikler:**
- v1.35'ten v1.46'ya kadar versiyonlar
- Her versiyon farklı özellik seti
- Geriye uyumluluk desteği
**Açıklama:** 64TASS'ın farklı sürümleri, proje ihtiyacına göre seçim

### **10. Basic Compiler Collection (15+ Araç)**
**Konum:** `c64 compiler/` klasöründe çoklu BASIC compiler  
**Çalıştığı Ortam:** C64 (emülatör üzerinde Windows'ta)  
**Kaynak Kodu:** ❌ C64 disk imajları  
**Araçlar:**
- Blitz Compiler (`BLITZ.d64`, `blitz.zip`)
- Laser Basic Compiler (`Laser-Basic-Compiler-V1.0-3001.d64`)
- Speed Compiler v2.2 (`Speedcompiler22-ATX.d64`)
- Basic64 Compiler (`Basic64Compiler-SZOPORILASZLO.d64`)
- Super Compiler (`SuperCompiler-SOFTWELL.d64`)
- Micro Org Compiler (`MikroorgComp-MIKROORG.d64`)
- Short Compiler (`Shortcompiler_2.711.d64`)
- Austro Speed Compiler (`AustroSpeedCompiler-MIKROORG.d64`)
- F-Recompiler 2.0 (`F_Recompiler_2.0.d64`)
- Basic Boss Compiler (`Basic Boss Compiler plus PDF Anleitung in Deutsch.rar`)
**Özellikler:**
- BASIC kodunu makine diline derleme
- Hız optimizasyonları
- Bellek optimizasyonları
**Açıklama:** C64'te BASIC programları hızlandırmak için compiler'lar

### **11. Pascal Compiler Collection (8+ Araç)**
**Konum:** `c64 compiler/` klasöründe Pascal derleyicileri  
**Çalıştığı Ortam:** C64 (emülatör üzerinde Windows'ta)  
**Kaynak Kodu:** ❌ C64 disk imajları  
**Araçlar:**
- G-Pascal (`G-Pascal.zip`, `g-pascal30.d64`)
- Turbo Pascal (`Turbo-Pascal-Compiler-V1.2-F4CG.d64`)
- UCSD Pascal (`UCSD_PascalCompiler13.d64`)
- Pas64 (`Pas64.rar`)
- Mad Pascal (`Mad-Pascal-1.7.3/`)
**Özellikler:**
- Pascal dilinden 6502 kodu üretimi
- Prosedür ve fonksiyon desteği
- Tip kontrolü
**Açıklama:** C64 için Pascal geliştirme ortamları

### **12. C Compiler Collection (10+ Araç)**
**Konum:** `c64 compiler/` klasöründe C derleyicileri  
**Çalıştığı Ortam:** C64/Windows hibrit  
**Kaynak Kodu:** ❌ Çoğunlukla binary  
**Araçlar:**
- C-Compiler 64 (`C-Compiler 64 - Specki.d64`)
- Turbo-C V1.0 (`Turbo-C-V1.0-plusD-ACC.d64`)
- Super C Compiler (`SuperCCompiler_MZP.d64`)
- EC Compiler (`EC.d64`)
- CC64 v0.3-v0.4 (`cc64v03.zip`, `cc64v04.zip`)
**Özellikler:**
- C dilinden 6502 assembly üretimi
- Standart C kütüphane desteği
- Optimizasyon seçenekleri
**Açıklama:** C64 için C dili geliştirme araçları

---

## 🔍 **DECOMPİLER ARAÇLARI (20+ ARAÇ)**

### **13. Python Disassemblator 6502/6510**
**Konum:** `Python Disassemblator 6502_6510/`  
**Çalıştığı Ortam:** Windows (Python)  
**Kaynak Kodu:** ✅ Python kaynak kodu  
**Özellikler:**
- 6502/6510 opcode tam desteği
- Sembol tanıma (symbol recognition)
- Kod akış analizi (code flow analysis)
- Çoklu format çıktısı
- Gelişmiş analiz algoritmaları
**Açıklama:** Modern Python tabanlı disassembler, entegrasyon için ideal

### **14. Austro Decompiler Collection**
**Konum:** `c64 decompiler/` klasöründe Austro araçları  
**Çalıştığı Ortam:** C64 (emülatör üzerinde Windows'ta)  
**Kaynak Kodu:** ❌ C64 disk imajları  
**Araçlar:**
- Austro Decompiler (`Austro Decompiler (19xx)(CFB Soft).t64`)
- Austro Decompiler v1.1 (`AustroDecompiler11-GAUTIERPETER.d64`)
- Austro-Blitz Decompiler (`Austro-Blitz-Decompiler_V32.zip`)
**Özellikler:**
- BASIC program decompile
- Blitz compiler uyumluluğu
- Kod geri kazanımı
**Açıklama:** Klasik C64 decompiler araçları

### **15. Blitz Decompiler Collection**
**Konum:** `c64 decompiler/` klasöründe Blitz araçları  
**Çalıştığı Ortam:** C64 (emülatör üzerinde Windows'ta)  
**Kaynak Kodu:** ❌ C64 disk imajları  
**Araçlar:**
- Blitz Decompiler (`Blitz Decompiler.d64`)
- Blitz Decompiler V2.0 (`Blitz Decompiler V2.0.zip`)
- DeBlitz (`deblitz.d64`)
**Özellikler:**
- Blitz compiler çıktısını decompile
- Orijinal BASIC kodu geri kazanımı
- Optimizasyon analizi
**Açıklama:** Blitz compiler'ı için özel decompiler'lar

### **16. SID Decompiler Collection**
**Konum:** `c64 decompiler/SIDdecompiler*`  
**Çalıştığı Ortam:** Windows (exe + kaynak)  
**Kaynak Kodu:** ✅ Master kaynak mevcut  
**Araçlar:**
- SIDdecompiler x86 (`SIDdecompiler-x86.exe`)
- SIDdecompiler x64 (`SIDdecompiler_0.8-Win_x64.zip`)
- SIDdecompiler kaynak (`SIDdecompiler-master.zip`)
**Özellikler:**
- SID müzik dosyası analizi
- Assembly kod çıkarımı
- Register analizi
**Açıklama:** SID dosyalarından kod çıkarımı için özel araçlar

---

## 💻 **INTERPRETER VE RUNTIME ARAÇLARI (15+ ARAÇ)**

### **17. CBM BASIC Interpreter**
**Konum:** `cbmbasic/`  
**Çalıştığı Ortam:** Windows  
**Kaynak Kodu:** ✅ C kaynak kodu  
**Özellikler:**
- Tam Commodore BASIC v2.0 uyumluluğu
- Komut satırı kullanımı
- BASIC program yürütme
- Token analizi ve çevirisi
**Açıklama:** Windows'ta BASIC programları çalıştırmak için interpreter

### **18. FORTH Interpreter Collection**
**Konum:** `forth65/`, `fig-forth*` dosyaları  
**Çalıştığı Ortam:** Windows/C64  
**Kaynak Kodu:** ✅ Çoğunda kaynak mevcut  
**Araçlar:**
- FIG-FORTH 6502 (`fig-forth_6502.pdf`)
- FORTH65 (`forth65.zip`)
- Apple II FORTH (`fig-forth_APPLEII.pdf`)
- 6800 FORTH (`fig-forth_6800.pdf`)
- 8080 FORTH (`fig-forth_8080_ver_11.pdf`)
**Özellikler:**
- Stack tabanlı programlama
- Düşük seviye sistem kontrolü
- Genişletilebilir sözlük
**Açıklama:** FORTH dili interpreter'ları, sistem programlama için

### **19. VTL02 Interpreter**
**Konum:** `very tiny interpreter_ Source_ VTL02 interpreter.html`  
**Çalıştığı Ortam:** 6502 (C64 uyumlu)  
**Kaynak Kodu:** ✅ HTML dokümantasyonunda kaynak  
**Özellikler:**
- Çok küçük interpreter (256 byte)
- Temel programlama yapıları
- Eğitim amaçlı ideal
**Açıklama:** Minimal interpreter, eğitim ve öğrenme için

### **20. BasicV2 Modern Implementation**
**Konum:** `c64 compiler/basicv2-master.zip`  
**Çalıştığı Ortam:** Windows (modern implementation)  
**Kaynak Kodu:** ✅ Modern kaynak kodu  
**Özellikler:**
- Modern BASIC v2.0 implementasyonu
- Geliştirilmiş hata mesajları
- Debug özellikleri
**Açıklama:** Modern sistemlerde BASIC v2.0 çalıştırma

---

## 🛠️ **GELİŞTİRME VE YARDIMCI ARAÇLAR (20+ ARAÇ)**

### **21. TMPview**
**Konum:** `TMPview_v1.3_Win32-STYLE/`  
**Çalıştığı Ortam:** Windows  
**Kaynak Kodu:** ❌ Binary dağıtım  
**Özellikler:**
- Disk imajı görüntüleme
- Dosya çıkarma
- Hex editör
**Açıklama:** Disk imajları için viewer ve editör

### **22. Dataliner Python Script**
**Konum:** `Dataliner_Python_Script.zip`  
**Çalıştığı Ortam:** Windows (Python)  
**Kaynak Kodu:** ✅ Python script  
**Özellikler:**
- Veri dönüştürme
- Format çevirimi
- Batch işleme
**Açıklama:** Veri işleme için Python araçları

### **23. GCC 6502 Bits**
**Konum:** `gcc-6502-bits-master/`  
**Çalıştığı Ortam:** Windows (GCC tabanlı)  
**Kaynak Kodu:** ✅ Kaynak kodu mevcut  
**Özellikler:**
- GCC tabanlı 6502 desteği
- Modern compiler altyapısı
- Gelişmiş optimizasyon
**Açıklama:** GCC'nin 6502 desteği için araçlar

### **24. NESHLA (NES High Level Assembler)**
**Konum:** `neshla-20050417-src-win32/`  
**Çalıştığı Ortam:** Windows  
**Kaynak Kodu:** ✅ Win32 kaynak  
**Özellikler:**
- Yüksek seviye assembly
- NES/C64 uyumluluğu
- Makro sistemi
**Açıklama:** Yüksek seviye assembly dili

### **25. Quetzalcoatl**
**Konum:** `quetzalcoatl-src-GPL-2.1.0-BETA/`  
**Çalıştığı Ortam:** Windows  
**Kaynak Kodu:** ✅ GPL lisanslı kaynak  
**Özellikler:**
- Multi-platform assembler
- Gelişmiş makro sistemi
- Plugin desteği
**Açıklama:** Gelişmiş multi-platform assembler

---

## 📚 **ÖZEL AMAÇLI ARAÇLAR (15+ ARAÇ)**

### **26. Music Compiler**
**Konum:** `c64 compiler/Music Compiler Hit N.4 [aerobia soft].d64`  
**Çalıştığı Ortam:** C64 (emülatör üzerinde Windows'ta)  
**Kaynak Kodu:** ❌ C64 disk imajı  
**Özellikler:**
- Müzik derleme
- SID optimizasyonu
- Nota dönüştürme
**Açıklama:** Müzik dosyalarını derlemek için özel araç

### **27. Assembly Language for Kids**
**Konum:** `programin language/Assembly Language For Kids (1984)(W.Sanders).d64`  
**Çalıştığı Ortam:** C64 (emülatör üzerinde Windows'ta)  
**Kaynak Kodu:** ❌ Eğitim disketi  
**Özellikler:**
- Eğitim amaçlı assembly öğretimi
- İnteraktif örnekler
- Step-by-step öğrenme
**Açıklama:** Çocuklar için assembly dili eğitimi

### **28. N-Coder Collection**
**Konum:** `programin language/` klasöründe N-Coder araçları  
**Çalıştığı Ortam:** C64 (emülatör üzerinde Windows'ta)  
**Kaynak Kodu:** ❌ C64 disk imajları  
**Araçlar:**
- N-Coder (`N-Coder [cr wms].d64`)
- NCoder (`NCoder-SOFTPiER.zip`)
- SPG N-Coder (`spg_n-coder.zip`)
**Özellikler:**
- Kod şifreleme/çözme
- Protection sistem
- Copy protection
**Açıklama:** Kod koruma ve şifreleme araçları

### **29. V072 Collection**
**Konum:** `v072*` dosya koleksiyonu  
**Çalıştığı Ortam:** Windows/C64  
**Kaynak Kodu:** ❌ Binary koleksiyon  
**Araçlar:**
- V072 DFS (`v072dfs.zip`)
- V072 ADFS (`v072adfs.zip`)
- V072 NFS (`v072nfs.zip`)
- V100 SSD (`v100.ssd`)
- V110 (`v110.zip`)
**Özellikler:**
- Dosya sistemi araçları
- Disk formatı desteği
- Veri kurtarma
**Açıklama:** Dosya sistemi ve disk yönetimi araçları

### **30. Scope Editor**
**Konum:** `programin language/Scope-CCS.d64`  
**Çalıştığı Ortam:** C64 (emülatör üzerinde Windows'ta)  
**Kaynak Kodu:** ❌ C64 disk imajı  
**Özellikler:**
- Kod editörü
- Syntax highlighting
- Project yönetimi
**Açıklama:** C64 için gelişmiş kod editörü

---

## 📖 **DOKÜMANTASYON VE REFERENo ARAÇLAR (20+ DOSYA)**

### **31. 6502 Opcode References**
**Konum:** Kök dizinde çoklu opcode referans dosyası  
**Çalıştığı Ortam:** Windows (doküman)  
**Kaynak Kodu:** ✅ Text/HTML formatında  
**Dosyalar:**
- `6502-NMOS.extra.opcodes.txt`
- `6502_6510_8500_8502 Opcodes.html`
- `c74-6502-undocumented-opcodes.pdf`
- `c74-6502-unstable-opcodes.pdf`
- `NoMoreSecrets-NMOS6510UnintendedOpcodes-*.pdf`
**Özellikler:**
- Tam opcode listesi
- Undocumented opcodes
- Timing bilgileri
- Flag etkileri
**Açıklama:** 6502/6510 işlemci referans dokümantasyonu

### **32. Programming References**
**Konum:** Kök dizinde programlama referansları  
**Çalıştığı Ortam:** Windows (doküman)  
**Kaynak Kodu:** ✅ Kaynak kod örnekleri  
**Dosyalar:**
- `6502.org_source_*.pdf/html` (10+ dosya)
- `The_PDS_6502_Manual.pdf`
- `Apple3_Business_BASIC_1.3.pdf`
- `2ksa.pdf`
**Özellikler:**
- Programlama teknikleri
- Optimizasyon yöntemleri
- Algorithm implementations
- Code examples
**Açıklama:** 6502 programlama teknik referansları

### **33. System Files ve Headers**
**Konum:** Kök dizinde sistem dosyaları  
**Çalıştığı Ortam:** Windows/C64  
**Kaynak Kodu:** ✅ Header ve kaynak dosyalar  
**Dosyalar:**
- `os.h`, `os.txt`
- `xos.h`, `xos.s`, `xos.txt`
- `vdu.h`
- `sys.s`
- `M6502.MAC.txt`
**Özellikler:**
- İşletim sistemi interface'i
- Hardware abstraction
- System calls
- Memory management
**Açıklama:** Sistem programlama için header ve library dosyaları

---

## 📈 **ENTEGRASYON ÖNCELİK MATRİSİ**

| Öncelik | Araç Kategorisi | Araç Sayısı | Windows Uyumluluk | Entegrasyon Süresi |
|---------|-----------------|-------------|-------------------|-------------------|
| 🟢 **Yüksek** | Modern Assembler'lar | 5 | %100 | 1-2 gün |
| 🟢 **Yüksek** | C Compiler'lar | 3 | %100 | 2-3 gün |
| 🟡 **Orta** | Python Tools | 4 | %100 | 1-2 gün |
| 🟡 **Orta** | BASIC Compiler'lar | 15 | %80 (emülatör) | 3-5 gün |
| 🔴 **Düşük** | C64 Native Tools | 50+ | %60 (emülatör) | 1-2 hafta |
| 🔵 **Araştırma** | Dokümantasyon | 20+ | %100 | Sürekli |

---

## 🎯 **ENTEGRASYON STRATEJİSİ**

### **Aşama 1: Temel Araçlar (1 Hafta)**
1. **64TASS** - Ana assembler olarak
2. **ACME** - Alternatif assembler
3. **Oscar64** - C geliştirme için
4. **Python Disassemblator** - Modern disassembly
5. **CBM BASIC Interpreter** - BASIC desteği

### **Aşama 2: Gelişmiş Araçlar (2 Hafta)**
1. **DASM** ve **Mad Assembler** - Ek assembler seçenekleri
2. **CC65** - Profesyonel C geliştirme
3. **SID Decompiler** - Müzik analizi
4. **TMPview** - Disk görüntüleme
5. **FORTH Interpreter'lar** - Sistem programlama

### **Aşama 3: Emülatör Tabanlı Araçlar (3 Hafta)**
1. **BASIC Compiler Collection** - 15+ BASIC compiler
2. **Pascal Compiler Collection** - Pascal desteği
3. **Decompiler Collection** - Geri mühendislik
4. **Eğitim Araçları** - Assembly öğretimi

---

## 🔧 **TEKNİK GEREKSINIMLER**

### **Windows Sistem Gereksinimleri:**
- **Windows 10/11** - Ana işletim sistemi
- **Python 3.8+** - Python araçları için
- **Visual Studio 2019+** - C++ araçları için
- **CMake 3.15+** - Build sistemi
- **Git** - Kaynak kod yönetimi
- **Emülatör (VICE)** - C64 native araçlar için

### **Entegrasyon Modülleri:**
- **subprocess bridge** - External process management
- **Configuration manager** - Tool detection and setup
- **Error handler** - Unified error reporting
- **Template processor** - Command template system
- **Result parser** - Output analysis
- **GUI integration** - Seamless user interface

---

**📋 Dosya Durumu:** 100+ Dış Araç Koleksiyonu - Tam Envanter  
**🔄 Son Güncelleme:** 25 Aralık 2024  
**✅ Hedef İşletim Sistemi:** Windows (Linux/macOS ilgi dışı)  
**🎯 İlk Entegrasyon Hedefi:** 5 temel araç (1 hafta içinde)
