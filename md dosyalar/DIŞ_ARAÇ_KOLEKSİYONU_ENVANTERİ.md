# 🔧 DIŞ ARAÇ KOLEKSİYONU ENVANTERİ
> **Analiz Tarihi:** 26 Temmuz 2025  
> **Proje:** D64 Converter - KızılElma Geliştirme Stüdyosu  
> **Durum:** configuration_manager.py ile entegre edildi

---

## 📊 **SİSTEMDE KURULU ARAÇLAR**

### ✅ **KURULU VE ÇALIŞIR DURUMDA**
| Araç | Konum | Versiyon | Durum |
|------|-------|----------|-------|
| **Python** | `C:\Program Files\Python313\python.exe` | 3.13.x | ✅ Aktif |
| **VS Code** | `C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd` | Latest | ✅ Aktif |

### ❌ **SİSTEM PATH'İNDE BULUNAMAYAN**
- 64tass, acme, dasm, kickass, ca65, xa, cc65, oscar64, qbasic, crossviper, x64, vice

---

## 📁 **ÇALIŞMA ORTAMINDAKİ ARAÇ KAYNAKLARI**

### 🔨 **ASSEMBLER'LAR (Kaynak Kod + Executable)**

#### **1. 64TASS (Turbo Assembler)**
- **📂 Kaynak:** `disaridan kullanilacak ornek programlar\64tass-src\`
- **📝 Durum:** Kaynak kod mevcut (C dilinde), derlenmemiş
- **⚙️ Dosyalar:** 64tass.c, main.c, opcodes.c, 60+ modül
- **🎯 Kullanım:** C derleyicisi ile derlenebilir

#### **2. ACME Cross-Assembler**
- **📂 Kaynak:** `disaridan kullanilacak ornek programlar\acme-main\`
- **📝 Durum:** Kaynak kod mevcut (C dilinde), derlenmemiş
- **⚙️ Dosyalar:** Multiple directories, build system
- **🎯 Kullanım:** Make/GCC ile derlenebilir

#### **3. DASM 6502 Assembler**
- **📂 Executable:** `disaridan kullanilacak ornek programlar\dasm.exe` ✅
- **📂 Win64:** `disaridan kullanilacak ornek programlar\dasm-2.20.14.1-win-x64\dasm.exe` ✅
- **📂 Kaynak:** `disaridan kullanilacak ornek programlar\dasm-master\`
- **📝 Durum:** **ÇALIŞIR DURUMDA** - DASM 2.20.14.1
- **🎯 Kullanım:** Doğrudan kullanılabilir

#### **4. KickAss Assembler**
- **📝 Durum:** ❌ Kaynak kod yok, executable yok
- **🎯 Not:** Java tabanlı, .jar dosyası gerekli

#### **5. CC65 Compiler Suite**
- **📂 Kaynak:** `disaridan kullanilacak ornek programlar\cc65-snapshot-win32\`
- **📝 Durum:** **TAM PAKETLİ** - Windows snapshot
- **⚙️ Dosyalar:**
  - `bin\ca65.exe` ✅ (Assembler)
  - `bin\cc65.exe` ✅ (C Compiler)
  - `bin\cl65.exe` ✅ (Linker)
  - `bin\da65.exe` ✅ (Disassembler)
  - Complete libraries ve include files
- **🎯 Kullanım:** Doğrudan kullanılabilir

#### **6. Mad Assembler**
- **📂 Kaynak:** `disaridan kullanilacak ornek programlar\Mad-Assembler-2.1.6\`
- **📝 Durum:** Pascal kaynak kodu mevcut
- **🎯 Kullanım:** Free Pascal ile derlenebilir

#### **7. Oscar64 C Compiler**
- **📂 Kaynak:** `disaridan kullanilacak ornek programlar\oscar64-main\`
- **📝 Durum:** Kaynak kod mevcut
- **🎯 Kullanım:** Derlenmesi gerekiyor

---

### 🖥️ **IDE VE GELİŞTİRME ARAÇLARI**

#### **1. CrossViper IDE**
- **📂 Kaynak:** `crossviper-master\`
- **📝 Durum:** Python tabanlı, kaynak kod mevcut
- **⚙️ Dosyalar:** crossviper.py, codeeditor.py, configuration.py
- **🎯 Kullanım:** Python ile çalıştırılabilir

#### **2. Relaunch64**
- **📂 Executable:** `disaridan kullanilacak ornek programlar\Relaunch64.exe` ✅
- **📝 Durum:** Çalışır durumda
- **🎯 Kullanım:** C64 geliştirme IDE'si

---

### 🎮 **EMÜLATÖRLEr**
- **📝 Durum:** ❌ Hiçbiri kurulu değil
- **🎯 Gereksinim:** VICE, CCS64, Hoxs64 kurulumu gerekli

---

### 🗃️ **ROM VE VERİ KAYNAKLARI**

#### **C64 ROM Data Collection**
- **📂 Konum:** `c64_rom_data\`
- **📊 İçerik:**
  - `basic\` - BASIC ROM routines ve token'lar ✅
    - `basic_tokens.json` - Token definitions
    - `basic_routines.json` - BASIC subroutines
    - Assembly source files (25+ dosya)
  - `kernal\` - KERNAL ROM routines ✅
    - `kernal_routines.json` - KERNAL call definitions
    - `io_registers.json` - I/O register mappings
    - Assembly source files (20+ dosya)
  - `memory_maps\` - Memory layout definitions ✅
    - `c64_memory_map.json` - Complete memory map
    - `special_addresses.json` - Important addresses
  - `zeropage\` - Zero page definitions

---

## ⚙️ **CONFIGURATION MANAGER ENTEGRASYONu**

### **📋 Desteklenen Araçlar (basic_tools.json)**
```json
Assemblers: 64tass, acme, dasm, kickass, ca65, xa, yeniassembler
Compilers: cc65, oscar64
Interpreters: python, qbasic  
IDEs: vscode, crossviper
Emulators: vice, ccs64
```

### **📋 Genişletilmiş Araçlar (extended_tools.json)**
```json
Extended Assemblers: tmpx, crass, ophis, BeebAsm, as65, xasm, mads, asmx
Extended Compilers: llvm-mos, z88dk, vbcc, ugbasic, millfork
```

### **🔍 Tespit Edilen Çalışır Araçlar**
| Araç | Konum | Durum |
|------|-------|-------|
| **DASM** | `disaridan kullanilacak ornek programlar\dasm.exe` | ✅ Çalışır |
| **CC65 Suite** | `disaridan kullanilacak ornek programlar\cc65-snapshot-win32\bin\` | ✅ Çalışır |
| **Relaunch64** | `disaridan kullanilacak ornek programlar\Relaunch64.exe` | ✅ Çalışır |
| **CrossViper** | `crossviper-master\crossviper.py` | ✅ Python ile çalışır |

---

## 🎯 **ÖNCELİKLENDİRİLMİŞ ARAÇ KURULUM PLANI**

### **🔴 YÜKSEK ÖNCELİK (Hemen)**
1. **DASM** - ✅ Hazır, path'e eklenmeli
2. **CC65** - ✅ Hazır, path'e eklenmeli  
3. **64TASS** - Kaynak var, derlenmeli
4. **ACME** - Kaynak var, derlenmeli

### **🟡 ORTA ÖNCELİK (1-2 hafta)**
5. **KickAss** - Java tabanlı, .jar indirilmeli
6. **Oscar64** - Kaynak var, derlenmeli
7. **VICE Emulator** - İndirilip kurulmalı

### **🟢 DÜŞÜK ÖNCELİK (İsteğe bağlı)**
8. Mad Assembler, Ophis, XA vs.
9. Diğer emülatörler (CCS64, Hoxs64)

---

## 💡 **KULLANIM ÖNERİLERİ**

### **Anında Kullanılabilir**
```batch
# DASM Assembly
"disaridan kullanilacak ornek programlar\dasm.exe" source.asm -osource.prg

# CC65 C Compilation  
"disaridan kullanilacak ornek programlar\cc65-snapshot-win32\bin\cl65.exe" -t c64 source.c

# CrossViper IDE
python crossviper-master\crossviper.py
```

### **Path Ekleme (Önerilen)**
```batch
set PATH=%PATH%;c:\Users\dell\Documents\projeler\d64_converter\disaridan kullanilacak ornek programlar
set PATH=%PATH%;c:\Users\dell\Documents\projeler\d64_converter\disaridan kullanilacak ornek programlar\cc65-snapshot-win32\bin
```

---

## 📈 **GENEL DEĞERLENDİRME**

### ✅ **GÜÇLÜ YANLAR**
- Çok kapsamlı araç koleksiyonu
- Anahtar araçlar (DASM, CC65) çalışır durumda
- Zengin ROM/veri kaynakları
- configuration_manager.py ile otomatik tespit sistemi

### ⚠️ **İYİLEŞTİRME GEREKENLer**  
- Çoğu araç system PATH'inde değil
- Kaynak kodları derlenmemiş
- Emülatör eksikliği
- Java dependency'leri kurulu değil

### 🎯 **SONUÇ**
Proje, C64 geliştirme için **gerekli tüm araçlara sahip** ancak çoğu **kurulum/derleme bekliyor**. Configuration Manager'ın tespit sistemi ile birlikte, araçlar otomatik olarak tanımlanıp kullanıma hazır hale getirilebilir.