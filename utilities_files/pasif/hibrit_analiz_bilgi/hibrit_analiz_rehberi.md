# 🧠 HİBRİT BASIC + ASSEMBLY ANALİZ REHBERİ

## Neden "Hibrit"?
Commodore 64 programları tek bir .PRG dosyasında hem BASIC hem de makine dili içerir:

- **BASIC kısmı**: tokenize (ön işlemden geçmiş)
- **Assembly (machine code) kısmı**: çoğunlukla SYS 2061 gibi bir çağrıyla başlatılır

### Yapı:
```
[2 byte load address] + [tokenized BASIC] + [raw machine code (6502)]
```

## ✅ BİLİYORUZ:
| Alan | Açıklama |
|------|----------|
| BASIC parser | d64 ve ProgramFile ile tokenize/detokenize |
| 6502 disassembler | dis6502, capstone, py65tools, vs. |
| SYS tespiti | BASIC içinde SYS xxxx komutları |
| Memory Map | $0801 (2049) BASIC start, $C000+ genelde ASM |

## ❌ EKSİKLER ve ÇÖZÜMLERİ:

### 1. Makine dili kısmının konumunu tam bulmak
**Sorun**: BASIC kodu bittikten sonra gelen verinin nereden itibaren makine kodu olduğuna karar vermek gerekiyor.

**Çözüm**: BASIC satırlarının kaç bayt sürdüğünü bul ve kalan kısmı ASM olarak kabul et.

```python
def split_prg(prg_path):
    with open(prg_path, 'rb') as f:
        data = f.read()

    load_addr = int.from_bytes(data[:2], 'little')
    content = data[2:]

    # BASIC için ProgramFile kullan
    from d64 import ProgramFile
    from io import BytesIO

    pf = ProgramFile(BytesIO(content))
    basic_len = pf.size  # BASIC alanının uzunluğu

    basic_segment = content[:basic_len]
    asm_segment = content[basic_len:]
    asm_addr = load_addr + basic_len

    return basic_segment, asm_segment, asm_addr
```

### 2. BASIC'ten makine dili adresini çıkarma
**Sorun**: Programcının yazdığı SYS çağrısını yakalamak gerekiyor.

**Çözüm**: Detokenized BASIC satırlarında SYS varsa, oradaki adres disassembler için başlangıç olabilir.

```python
import re

def find_sys_address(basic_text):
    lines = basic_text.splitlines()
    for line in lines:
        match = re.search(r'SYS\s+(\d+)', line.upper())
        if match:
            return int(match.group(1))
    return None
```

### 3. Tam Entegre Python Akışı:
```python
# 1. PRG çıkar, BASIC/ASM ayır
load_addr, basic_bytes, asm_bytes = split_prg('MYPROG.PRG')
basic_source = detokenize_basic(basic_bytes)

# 2. SYS adresini bul
sys_addr = find_sys_address(basic_source)
start_addr = sys_addr or load_addr + len(basic_bytes)

# 3. Disassembler ile kodu bas
disassemble_asm(asm_bytes, start_addr)
```

## 🔜 Sonraki Adımlar:
- Komut rangesına göre otomatik başlangıç/bit tahmini
- CALL bayt verisi / BRANCH target tespiti
- Bellek haritasına göre static analiz
- Tam entegre "üretici / disassembler" Python modülü yazımı

---
*Bu bilgi enhanced_d64_reader.py dosyasından aktarılmıştır.*

Harika, şimdi sana hibrit BASIC + Assembly PRG dosyalarının nasıl disassemble edileceğini daha teknik ve detaylı biçimde açıklıyorum. Amacımız, Commodore 64’te BASIC içinde gömülü makine dili bölümlerini doğru ayırmak, adreslemek ve her kısmı doğru araçlarla işlemek.

🧠 NEDEN “HIBRIT”?
Commodore 64 programları tek bir .PRG dosyasında hem BASIC hem de makine dili içerir. Bu dosyalar:

BASIC kısmı tokenize (ön işlemden geçmiş)

Assembly (machine code) kısmı: çoğunlukla SYS 2061 gibi bir çağrıyla başlatılır

Yapı:
css
Kopyala
Düzenle
[2 byte load address] + [tokenized BASIC] + [raw machine code (6502)]
✅ BİLİYORUZ:
Alan	Açıklama
BASIC parser	d64 ve ProgramFile ile tokenize/detokenize
6502 disassembler	dis6502, capstone, py65tools, vs.
SYS tespiti	BASIC içinde SYS xxxx komutları
Memory Map	$0801 (2049) BASIC start, $C000+ genelde ASM

❌ EKSİKLER (Şimdi Açıklıyoruz)
1. ❌ Makine dili kısmının konumunu tam bulmak
🔍 Sorun:
BASIC kodu bittikten sonra gelen verinin nereden itibaren makine kodu olduğuna karar vermek gerekiyor.

✅ Çözüm:
BASIC satırlarının kaç bayt sürdüğünü bul ve kalan kısmı ASM olarak kabul et.

📌 Python Örneği:
python
Kopyala
Düzenle
def split_prg(prg_path):
    with open(prg_path, 'rb') as f:
        data = f.read()

    load_addr = int.from_bytes(data[:2], 'little')
    content = data[2:]

    # BASIC için ProgramFile kullan
    from d64 import ProgramFile
    from io import BytesIO

    pf = ProgramFile(BytesIO(content))
    basic_len = pf.size  # BASIC alanının uzunluğu

    basic_segment = content[:basic_len]
    asm_segment = content[basic_len:]
    asm_addr = load_addr + basic_len

    return basic_segment, asm_segment, asm_addr
2. ❌ BASIC’ten makine dili adresini çıkarma
🔍 Sorun:
Programcının yazdığı SYS çağrısını yakalamak gerekiyor.

✅ Çözüm:
Detokenized BASIC satırlarında SYS varsa, oradaki adres disassembler için başlangıç olabilir.

📌 Python Örneği:
python
Kopyala
Düzenle
import re

def find_sys_address(basic_text):
    lines = basic_text.splitlines()
    for line in lines:
        match = re.search(r'SYS\s+(\d+)', line.upper())
        if match:
            return int(match.group(1))
    return None
3. ❌ Track/Sector gerçeği (disk içi geometri)
🔍 Sorun:
.D64 dosyası sektörlerden oluşur (683 sektör). PRG dosyaları bunlara dağılmıştır ama çoğu kullanıcı düz dosya gibi okur.

✅ Çözüm:
Genelde buna ihtiyaç ancak “raw sector level” analiz yaparken olur (örneğin kopya koruma, loader sistemleri).

Python'da bu yok ama lib1541img gibi C/C++ kütüphaneler bu erişimi sağlar.
Alternatif olarak:

Vice emulatoru ile monitor modunda track/sector verisine erişebilirsin

cc1541, DirMaster ile elle inceleme

4. ❌ PRG dosyasındaki segmentleri ayırma
🔍 Sorun:
Assembler kodu bazen veri içerir, yani doğrudan disassemble edilemez.

✅ Çözüm:
SYS adresini disassembler için giriş noktası kabul et

Komutları takip ederek geçerli kodu çıkar

Hatalı opcode'ları (örneğin ASCII metin olan alanlar) tanı ve ayır

📌 İleri Seviye Python Yaklaşımı:
python
Kopyala
Düzenle
# Disassembler; sadece geçerli opcode takip eder
from dis6502 import Dis6502, Memory

def disassemble_asm(asm_bytes, start_addr):
    mem = Memory()
    mem.load_bytes(start_addr, asm_bytes)
    dis = Dis6502()
    dis.disasm(mem, pc=start_addr)
    for addr, inst in dis.instructions.items():
        print(f"${addr:04X}: {inst}")
🔚 ÖZET: HİBRİT PRG DOSYASI NASIL ANALİZ EDİLİR?
Aşama	Açıklama
1. PRG’yi oku	İlk 2 byte yükleme adresi
2. BASIC’i ayrıştır	ProgramFile ile token boyunu belirle
3. SYS ara	BASIC içinde SYS tespiti
4. ASM disassemble	start = SYS adresi veya BASIC sonrası
5. Memory map uygula	$C000+, $E000 loader vb. bölgeler
6. Sektör analizi (opsiyonel)	Track/Sector için lib1541img veya hex inceleme

Python kullanarak Commodore disk imajlarıyla çalışmak istersen, işte sana iki güçlü kütüphane:

---

## 🐍 1. **d64** (PyPI modülü)

* `.d64`, `.d71`, `.d80`, `.d81`, `.d82` gibi tabanlı disk imajlarını okuma/yazma imkânı sağlar ([style64.org][1], [pypi.org][2]).
* Directory (dosya listesi) görüntüleme, BASIC programları çıkarma (`ProgramFile` ile listleme), PRG dosyalarını ayıklama gibi fonksiyonlar içeriyor:

```python
from d64 import DiskImage, ProgramFile

with DiskImage('test.d64') as img:
    for line in img.directory():
        print(line)  # Dosya listesi

    with img.path("METEOR").open() as f:
        p = ProgramFile(f)
    for l in p.list():
        print(l)  # BASIC satırları
```

---

## 🧩 2. **d64py** (GitLab projesi)

* Python ile hem `.d64` imajlarını okuma/yazma hem de GEOS dosyalarını çözümleme imkânı sunar ([lyonlabs.org][3]).
* Daha aktif güncellenen, API dostu bir sürüm; Disk Wrangler gibi araçlara temel oluşturuyor.

---

## 🔍 Kıyaslama

| Özellik         | d64 (PyPI)                     | d64py (GitLab)    |
| --------------- | ------------------------------ | ----------------- |
| Disk imaj okuma | ✅                              | ✅                 |
| Disk imaj yazma | Kısmen (beta/yazma destekli) ✅ | ✅                 |
| BASIC extract   | ✅ (`ProgramFile`)              | –                 |
| GEOS desteği    | ❌                              | ✅ (GEOS çıkarımı) |
| Disassembler    | ❌ (binary ayıklanır)           | ❌                 |

---

## 🛠️ Disassembly İçin Ne Yapmalı?

Bu kütüphaneler doğrudan assembly disassembly yapmıyor; ama iş akışı şöyle olabilir:

1. `d64` veya `d64py` ile disk imajından `PRG` (binary) dosyalarını ayıkla.
2. Ayrılan `.prg` dosyasını Python script veya CLI ile `py65`, `capstone`, `distorm` gibi disassembler’larla işle.

Örnek bir sistem:

* `PRG → 6502'ye özel disassembler script → okunur Assembly dosyası` formatı.

---

### 🧭 Özet ve İlerisi

* **Disk imajı işlemleri**: `d64` (PyPI) ve `d64py` (GitLab) ile yapılabilir.
* **BASIC kod çıkarımı**: `d64` + `ProgramFile`.
* **Disassembly**: ayıklanan `.prg` dosyasını başka araçlarla işlemek gerek.



[1]: https://style64.org/dirmaster/documentation/?utm_source=chatgpt.com "DirMaster/Style Documentation (v3.0.0)"
[2]: https://pypi.org/project/d64/?utm_source=chatgpt.com "d64 - PyPI"
[3]: https://www.lyonlabs.org/commodore/?utm_source=chatgpt.com "Cenbe's Commodore 64 Pages - Lyon Labs"
