# D64 Converter - Kullanım Kılavuzu

## Program Hakkında

D64 Converter, Commodore 64 disk imajları (.d64) ve program dosyaları (.prg) için geliştirilmiş gelişmiş bir reverse engineering aracıdır. Program, 6502 Assembly kodunu çoklu programlama dillerine çevirebilen modern bir disassembler'dır.

## Temel Özellikler

### 🔄 Çoklu Format Desteği
- **Assembly (ASM)**: Geleneksel 6502 Assembly çıktısı
- **C Language**: Derlenebilir C kodu ile tam fonksiyon desteği
- **QBasic**: Microsoft QBasic uyumlu kod
- **PDSX BASIC**: Line number'lı BASIC format
- **Commodore BASIC V2**: Otantik C64 BASIC syntax'ı
- **Pseudo Code**: Okunabilir pseudo kod çıktısı

### 🎯 Gelişmiş Kod Üretimi
- **Gerçek C Kodu**: Derlenebilir, çalıştırılabilir C programları
- **Register Emulation**: 6502 registerlarının tam emülasyonu
- **Memory Management**: 64KB memory array ile tam bellek desteği
- **Stack Operations**: Proper stack push/pop fonksiyonları
- **Flag Operations**: Zero, Negative, Carry flag işlemleri
- **Helper Functions**: Utility fonksiyonlar ve type definitions

### 🖥️ Kullanıcı Arayüzü
- **Modern GUI**: Tkinter tabanlı kullanıcı dostu arayüz
- **Drag & Drop**: Dosya sürükle-bırak desteği
- **Tabbed Interface**: Her format için ayrı tab
- **Per-Format Conversion**: Her format için özel convert butonları
- **Real-time Preview**: Anlık kod önizlemesi

### 📁 Dosya Formatları
- **D64**: Commodore 64 disk imajları
- **PRG**: Program dosyaları
- **T64**: Tape imajları (gelecek sürüm)

## Dizin Yapısı

```
d64_converter/
├── main.py                     # Ana program başlatıcı
├── d64_converter.py           # GUI uygulaması
├── advanced_disassembler.py   # Gelişmiş disassembler
├── improved_disassembler.py   # Yeni kod üretim sistemi
├── opcode_manager.py          # Opcode ve çeviri yöneticisi
├── d64_reader.py             # D64 disk okuyucu
├── disassembler.py           # Temel disassembler
├── sprite_converter.py       # Sprite dönüştürücü
├── sid_converter.py          # SID müzik dönüştürücü
├── c64_basic_parser.py       # BASIC parser
├── parser.py                 # Genel parser
├── c64_memory_map.json       # C64 memory map
├── memory_map.json           # Genel memory map
├── opcode_map.json           # Opcode çevirileri
├── hex_opcode_map.json       # Hex opcode tablosu
├── venv_asmto/               # Sanal ortam dizini
├── logs/                     # Log dosyaları
├── asm_files/                # Assembly çıktıları
├── c_files/                  # C kodu çıktıları
├── qbasic_files/             # QBasic çıktıları
├── pdsx_files/               # PDSX BASIC çıktıları
├── pseudo_files/             # Pseudo kod çıktıları
├── commodorebasicv2_files/   # Commodore BASIC çıktıları
├── prg_files/                # PRG dosyaları
├── png_files/                # PNG çıktıları
├── sid_files/                # SID dosyaları
├── help/                     # Yardım dosyaları
│   ├── opcode.html
│   ├── opcode.json
│   ├── opcode.md
│   └── opcodeaciklama.md
└── README.md                 # İngilizce dokümantasyon
```

## Kullanılan Python Kütüphaneleri

### Ana Kütüphaneler
```python
import tkinter as tk              # GUI framework
import tkinter.ttk as ttk         # Modern widget'lar
import tkinterdnd2               # Drag & drop desteği
import PIL                       # Image processing
import numpy                     # Numerical operations
import json                      # JSON data handling
import subprocess                # Process management
import venv                      # Virtual environment
import argparse                  # Command line parsing
import logging                   # Logging system
import pathlib                   # Path operations
```

### Opsiyonel Kütüphaneler
```python
import py65                      # 6502 emulation (opsiyonel)
```

## Sanal Ortam Sistemi

Program otomatik olarak `venv_asmto` adlı sanal ortam oluşturur ve yönetir:

```
venv_asmto/
├── Scripts/                     # Windows executable'ları
│   ├── python.exe
│   ├── pip.exe
│   └── activate.bat
├── Lib/                         # Python kütüphaneleri
└── pyvenv.cfg                   # Sanal ortam yapılandırması
```

## Komut Satırı Kullanımı

### Temel Komutlar

```bash
# GUI modunda çalıştır (varsayılan)
python main.py

# Belirli dosya ile GUI başlat
python main.py --file game.prg

# Test modu - tüm formatları üret
python main.py --test --file game.prg

# Desteklenen formatları listele
python main.py --list-formats

# Debug modu ile çalıştır
python main.py --debug --file game.prg
```

### Argparse Parametreleri

#### Ana İşlem Modları
- `--gui`: GUI modunda çalıştır (varsayılan)
- `--test`: Test modu - tüm formatları üret
- `--no-gui`: GUI olmadan çalıştır

#### Dosya Seçenekleri
- `--file, -f`: İşlenecek dosya (D64, PRG, T64, vb.)
- `--format, -o`: Çıktı formatı (asm, c, qbasic, pdsx, pseudo, commodorebasicv2)

#### Sistem Seçenekleri
- `--debug`: Debug modu - detaylı logging
- `--log-level`: Log seviyesi (DEBUG, INFO, WARNING, ERROR)
- `--log-file`: Log dosyası (varsayılan: logs/timestamp.log)

#### Bilgi Seçenekleri
- `--list-formats`: Desteklenen formatları listele
- `--version`: Versiyon bilgisi

### Örnek Kullanımlar

```bash
# Basit GUI başlatma
python main.py

# Dosya ile GUI başlatma
python main.py --file "games/pacman.prg"

# Test modu - tüm formatları üret
python main.py --test --file "games/pacman.prg"

# Sadece C çıktısı üret
python main.py --file "games/pacman.prg" --format c

# Debug modu ile detaylı log
python main.py --debug --file "games/pacman.prg"

# Özel log dosyası ile çalıştır
python main.py --log-file "my_conversion.log" --file "games/pacman.prg"
```

## Yeni Kod Üretim Sistemi

### Improved Disassembler
Program, yeni `ImprovedDisassembler` sınıfını kullanarak çok daha kaliteli kod üretir:

#### C Kodu Özellikleri
- **Gerçek C Syntax**: Derlenebilir C kodu
- **Type Definitions**: `uint8_t`, `uint16_t` gibi proper types
- **Register Emulation**: Tam 6502 register set
- **Memory Array**: 64KB memory emulation
- **Stack Operations**: Proper stack push/pop
- **Flag Functions**: Zero, Negative flag operations
- **Helper Functions**: Utility fonksiyonlar

#### Örnek C Çıktısı
```c
// C64 6502 Assembly to C Conversion
// Generated by D64 Converter

#include <stdio.h>
#include <stdint.h>

// 6502 Registers
uint8_t a = 0;    // Accumulator
uint8_t x = 0;    // X Register
uint8_t y = 0;    // Y Register
uint8_t sp = 0xFF; // Stack Pointer
uint8_t status = 0; // Status Register

// Memory array
uint8_t memory[65536];

int main() {
    // Initialize memory
    for(int i = 0; i < 65536; i++) memory[i] = 0;
    
    // Program starts here
    a = 10; set_zero_flag(a); set_negative_flag(a);
    memory[1024] = a;
    a = a | 201; set_zero_flag(a); set_negative_flag(a);
    
    return 0;
}

// Helper functions
void set_zero_flag(uint8_t val) {
    if(val == 0) status |= 0x02;
    else status &= ~0x02;
}
```

#### QBasic Çıktısı
```basic
REM C64 6502 Assembly to QBasic Conversion
REM Generated by D64 Converter

DIM A AS INTEGER
DIM X AS INTEGER
DIM Y AS INTEGER
DIM MEMORY(65535) AS INTEGER

A = 10
MEMORY(1024) = A
A = A OR 201
```

#### Commodore BASIC V2 Çıktısı
```basic
10 REM C64 6502 ASSEMBLY TO COMMODORE BASIC V2
20 REM GENERATED BY D64 CONVERTER
50 A=0:X=0:Y=0:SP=255:ST=0
250 A=10
260 M(1024)=A
280 A=A OR 201
```

## Modül Açıklamaları

### Ana Modüller

#### `main.py`
- Ana program launcher
- Virtual environment yönetimi
- Argument parsing
- Logging sistem kurulumu
- Package installation

#### `d64_converter.py`
- GUI uygulaması
- Tkinter tabanlı arayüz
- Drag & drop desteği
- Per-format conversion
- Real-time preview

#### `advanced_disassembler.py`
- Gelişmiş disassembler
- Çoklu format desteği
- Memory map entegrasyonu
- py65 desteği (opsiyonel)

#### `improved_disassembler.py`
- Yeni kod üretim sistemi
- Kaliteli C kodu üretimi
- Proper syntax handling
- Format-specific optimization

#### `opcode_manager.py`
- Opcode tablosu yönetimi
- JSON dosya loading
- Çeviri sistemi
- Hex opcode mapping

### Yardımcı Modüller

#### `d64_reader.py`
- D64 disk imajı okuma
- File extraction
- Directory parsing

#### `disassembler.py`
- Temel disassembler
- Basit opcode table
- Legacy support

#### `sprite_converter.py`
- Sprite dönüştürme
- PNG çıktısı
- Grafik işleme

#### `sid_converter.py`
- SID müzik dönüştürme
- Audio processing

#### `c64_basic_parser.py`
- BASIC kod parsing
- Tokenization
- Syntax analysis

## Kurulum ve Başlatma

### Otomatik Kurulum
```bash
# Programı çalıştır - otomatik kurulum yapılır
python main.py
```

### Manuel Kurulum
```bash
# Sanal ortam oluştur
python -m venv venv_asmto

# Sanal ortamı aktifleştir (Windows)
venv_asmto\Scripts\activate

# Gerekli paketleri yükle
pip install tkinterdnd2 pillow numpy py65

# Programı çalıştır
python main.py
```

## Log Sistemi

Program detaylı logging sistemi kullanır:

### Log Dosyaları
- `logs/d64_converter_YYYYMMDD_HHMMSS.log`: Ana log
- `logs/system_info.json`: Sistem bilgileri

### Log Seviyeleri
- `DEBUG`: Detaylı debug bilgileri
- `INFO`: Genel bilgi mesajları
- `WARNING`: Uyarı mesajları
- `ERROR`: Hata mesajları

### Örnek Log Çıktısı
```
2025-07-16 02:00:49,985 - INFO - main:52 - Logging sistemi başlatıldı
2025-07-16 02:00:49,986 - INFO - main:53 - Log seviyesi: INFO
2025-07-16 02:00:50,612 - INFO - main:439 - D64 Converter başlatılıyor...
2025-07-16 02:00:50,613 - INFO - main:440 - Argümanlar: {'gui': True, 'test': False}
```

## Çıktı Formatları

### Assembly (ASM)
```assembly
$0801: LDA #$0A
$0803: STA $0400
$0806: RTS
```

### C Language
```c
a = 10; set_zero_flag(a); set_negative_flag(a);
memory[1024] = a;
return; // Return from subroutine
```

### QBasic
```basic
A = 10
MEMORY(1024) = A
RETURN
```

### PDSX BASIC
```basic
100 A = 10
110 MEMORY(1024) = A
120 RETURN
```

### Commodore BASIC V2
```basic
100 A=10
110 M(1024)=A
120 RETURN
```

### Pseudo Code
```
load_accumulator(10)
store_accumulator_to(memory[1024])
return_from_subroutine()
```

## Hata Giderme

### Yaygın Sorunlar

#### PIL Import Hatası
```bash
# Çözüm: Pillow'u yeniden yükle
pip install --force-reinstall Pillow
```

#### Sanal Ortam Hatası
```bash
# Çözüm: Sanal ortamı sil ve yeniden oluştur
rmdir /s venv_asmto
python main.py
```

#### GUI Açılmama
```bash
# Çözüm: Tkinter kurulumunu kontrol et
python -c "import tkinter; print('Tkinter OK')"
```

## Katkıda Bulunma

### Geliştirme Ortamı
```bash
# Repository'yi clone et
git clone [repository-url]
cd d64_converter

# Geliştirme için sanal ortam
python -m venv venv_dev
venv_dev\Scripts\activate

# Geliştirme paketlerini yükle
pip install -e .
pip install pytest black flake8
```

### Test Etme
```bash
# Tüm testleri çalıştır
python -m pytest

# Belirli test çalıştır
python main.py --test --file test_files/sample.prg
```

## Versiyon Geçmişi

### v1.0.0
- İlk stabil sürüm
- Çoklu format desteği
- Modern GUI
- Improved disassembler
- Proper C kod üretimi

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır.

## İletişim

Sorularınız ve önerileriniz için:
- GitHub Issues : metedinler
- Email: [zmetedinler@gmail.com]

---

*D64 Converter - Commodore 64 Assembly Reverse Engineering Tool*
*© 2025 - Modern 6502 Disassembler with Multi-Language Output*
