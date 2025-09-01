# 🚀 D64 CONVERTER - NIHAI YENIDEN YAPILANMA PLANI (THE ULTIMATE RESTRUCTURING PLAN) v1.0

**Belge Kodu (Document Code):** `SON_PLAN_25`  
**Tarih (Date):** 25 Temmuz 2025 (July 25, 2025)  
**Durum (Status):** Onay Bekliyor (Awaiting Approval)  
**Proje (Project):** KızılElma Geliştirme Stüdyosu (RedApple Development Studio)

---

## 🎯 **BÖLÜM 1: MEVCUT DURUM ANALİZİ VE TEMEL FELSEFE (PART 1: CURRENT STATE ANALYSIS AND CORE PHILOSOPHY)**

### **1.1. Mevcut Durum Tespiti (Current State Assessment)**

Mevcut sistem, 79'dan fazla Python modülü içeren, organik olarak büyümüş ve bu büyüme sürecinde farklı geliştirme aşamalarından kalma kod parçacıklarını barındıran karmaşık bir yapıya sahiptir (The current system has a complex structure, containing more than 79 Python modules, which has grown organically and retains code fragments from different development stages). Bu durum, kod tekrarına (code repetition), bakım zorluklarına (maintenance difficulties) ve performans sorunlarına (performance issues) yol açmaktadır. Özellikle disk okuma (disk reading), disassembler ve decompiler sistemlerinde, benzer görevleri yapan çok sayıda modül bulunmaktadır (Especially in disk reading, disassembler, and decompiler systems, there are multiple modules performing similar tasks).

### **1.2. Yeniden Yapılanma Felsefesi (Restructuring Philosophy)**

Temel felsefemiz, "Tek Sorumluluk Prensibi" (Single Responsibility Principle) ve "Modüler Tasarım" (Modular Design) ilkelerine dayalı, temiz, verimli ve genişletilebilir bir mimari oluşturmaktır (Our core philosophy is to create a clean, efficient, and extensible architecture based on the "Single Responsibility Principle" and "Modular Design" principles). Yazılmış olan **her bir değerli kod satırını (every single valuable line of code)** kaybetmeden, bu kodları mantıksal olarak doğru modüllere entegre ederek (by integrating this code into logically correct modules without loss), gelecekteki geliştirmeler için sağlam bir temel oluşturacağız (we will build a solid foundation for future development).

**Ana Hedefler (Main Objectives):**
1.  **Kod Şişkinliğini Ortadan Kaldırmak (Eliminate Code Bloat):** Fonksiyonel olarak çakışan modülleri birleştirmek (Consolidate functionally overlapping modules).
2.  **Performansı Artırmak (Increase Performance):** Gereksiz importları ve kod tekrarını engelleyerek sistemin yüklenme ve çalışma hızını artırmak (Increase system load and execution speed by preventing unnecessary imports and code duplication).
3.  **Bakım Kolaylığı Sağlamak (Ensure Ease of Maintenance):** Her modülün net ve tek bir göreve odaklanmasını sağlamak (Ensure each module focuses on a clear and single task).
4.  **Genişletilebilirliği Artırmak (Enhance Extensibility):** Yeni özelliklerin (sıkıştırılmış formatlar, yeni decompiler'lar) sisteme kolayca entegre edilebilmesini sağlamak (Enable easy integration of new features like compressed formats or new decompilers).

---

## 📂 **BÖLÜM 2: YENİ PROJE DİZİN YAPISI (PART 2: NEW PROJECT DIRECTORY STRUCTURE)**

Sistemin temelini oluşturacak olan yeni, mantıksal ve hiyerarşik dizin yapısı aşağıda tanımlanmıştır (The new, logical, and hierarchical directory structure that will form the foundation of the system is defined below).

```
d64_converter_v2/
├── core/
│   ├── __init__.py
│   ├── main_engine.py             # Ana sistem motoru (Main system engine)
│   ├── disk_services.py           # Disk okuma ve analiz (Disk reading and analysis)
│   ├── program_analyzer.py        # Hibrit program analizi (Hybrid program analysis)
│   ├── memory_services.py         # Hafıza yönetimi (Memory management)
│   └── configuration_manager.py   # Konfigürasyon yönetimi (Configuration management)
│
├── processing/
│   ├── __init__.py
│   ├── disassembler_engine.py     # 4-motorlu disassembler (4-engine disassembler)
│   ├── decompiler_engine.py       # Birleşik decompiler (Unified decompiler)
│   ├── transpiler_engine.py       # Assembly'den dönüşüm (Transpilation from Assembly)
│   └── basic_handler.py           # BASIC dil işlemleri (BASIC language operations)
│
├── formats/
│   ├── __init__.py
│   ├── sprite_handler.py          # Sprite format işlemleri (Sprite format operations)
│   ├── sid_handler.py             # SID format işlemleri (SID format operations)
│   └── compression_handler.py     # Sıkıştırılmış formatlar (Compressed formats)
│
├── resources/
│   ├── memory_maps/
│   │   ├── c64_memory_map.json
│   │   ├── kernal_routines.json
│   │   └── basic_rom.json
│   ├── opcodes/
│   │   ├── 6502_opcodes.json
│   │   └── 6510_illegal_opcodes.json
│   └── tokens/
│       └── basic_v2_tokens.json
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py             # Ana GUI penceresi (Main GUI window)
│   ├── widgets/                   # Özel GUI bileşenleri (Custom GUI widgets)
│   └── style.py                   # GUI stil dosyası (GUI style file)
│
├── external_tools/
│   ├── __init__.py
│   ├── petcat/
│   └── py65/
│
├── logs/
│   └── app.log
│
├── output/                        # Tüm çıktı dosyaları (All output files)
│   ├── prg/
│   ├── asm/
│   ├── c/
│   └── qbasic/
│
├── tests/
│   ├── __init__.py
│   ├── test_disk_services.py
│   └── test_disassembler.py
│
├── main.py                        # Ana giriş noktası (Main entry point)
└── README.md
```

---

## 🧩 **BÖLÜM 3: MODÜL KONSOLİDASYON PLANI (PART 3: MODULE CONSOLIDATION PLAN)**

Bu bölümde, mevcut 79+ modülün nasıl 12 ana modüle konsolide edileceği, hangi sınıf, metot ve fonksiyonların nereden alınacağı **kesin olarak** belirtilmiştir (In this section, it is **precisely** specified how the existing 79+ modules will be consolidated into 12 main modules, and which classes, methods, and functions will be taken from where).

### **3.1. `core/disk_services.py` - Birleşik Disk Servisleri (Unified Disk Services)**

Bu modül, tüm disk okuma, format tespiti ve dosya çıkarma işlemlerinden sorumlu olacaktır (This module will be responsible for all disk reading, format detection, and file extraction operations).

-   **Kaynak Modüller (Source Modules):** `d64_reader.py`, `enhanced_d64_reader.py`, `enhanced_disk_reader.py`
-   **Sorumluluklar (Responsibilities):**
    -   Desteklenen 19 disk formatını okumak (Reading the 19 supported disk formats).
    -   Dosya sistemini analiz etmek ve dizin listelemek (Analyzing the file system and listing directories).
    -   PRG, SEQ, USR gibi temel dosya türlerini çıkarmak (Extracting basic file types like PRG, SEQ, USR).
    -   Sıkıştırılmış formatları tespit etmek ve `compression_handler`'a yönlendirmek (Detecting compressed formats and forwarding to `compression_handler`).

-   **Taşınacak Bileşenler (Components to be Migrated):**
    -   **Sınıf (Class): `UnifiedDiskReader`** (Yeni oluşturulacak - To be newly created)
        -   **Metotlar (Methods):**
            -   `detect_format(file_path)`: `enhanced_disk_reader.py`'den `identify_format` metodu temel alınacak (Based on the `identify_format` method from `enhanced_disk_reader.py`).
            -   `read_directory(disk_data, format_info)`: `enhanced_d64_reader.py`'den `read_directory_d64`, `read_t64_directory`, `read_tap_directory` metotları birleştirilecek (Methods `read_directory_d64`, `read_t64_directory`, `read_tap_directory` from `enhanced_d64_reader.py` will be combined).
            -   `extract_file(file_entry)`: `d64_reader.py`'den `extract_prg_file`, `extract_seq_file`, `extract_usr_file` fonksiyonları birleştirilecek (Functions `extract_prg_file`, `extract_seq_file`, `extract_usr_file` from `d64_reader.py` will be combined).
            -   `get_disk_geometry(format_info)`: `enhanced_disk_reader.py`'deki `DiskInfo` ve geometri sabitleri kullanılacak (The `DiskInfo` and geometry constants from `enhanced_disk_reader.py` will be used).
    -   **Fallback Mekanizması (Fallback Mechanism):** `d64_reader.py`'nin basit ve güvenilir okuma fonksiyonları, `UnifiedDiskReader` içindeki gelişmiş metotlar başarısız olduğunda kullanılmak üzere bir alt katman olarak entegre edilecek (The simple and reliable reading functions of `d64_reader.py` will be integrated as a lower layer to be used when the advanced methods in `UnifiedDiskReader` fail).

### **3.2. `core/program_analyzer.py` - Gelişmiş Program Analizcisi (Advanced Program Analyzer)**

Bu modül, bir programın yapısını (BASIC, Assembly, Hibrit) analiz etmekten sorumlu olacaktır (This module will be responsible for analyzing the structure of a program - BASIC, Assembly, Hybrid).

-   **Kaynak Modüller (Source Modules):** `hybrid_program_analyzer.py`, `enhanced_d64_reader.py`
-   **Sorumluluklar (Responsibilities):**
    -   Bir PRG dosyasının hibrit olup olmadığını tespit etmek (Detecting if a PRG file is hybrid).
    -   BASIC ve Assembly kod bloklarının başlangıç ve bitiş adreslerini bulmak (Finding the start and end addresses of BASIC and Assembly code blocks).
    -   `SYS` çağrılarını ve hafıza erişimlerini (POKE/PEEK) analiz etmek (Analyzing `SYS` calls and memory accesses - POKE/PEEK).

-   **Taşınacak Bileşenler (Components to be Migrated):**
    -   **Sınıf (Class): `HybridProgramAnalyzer`** (`hybrid_program_analyzer.py`'den alınacak - To be taken from `hybrid_program_analyzer.py`).
        -   **Metotlar (Methods):**
            -   `analyze_prg_data(prg_data)`: Ana analiz metodu olarak kalacak (Will remain as the main analysis method).
            -   `find_basic_end(data)`: `enhanced_d64_reader.py`'deki `_find_basic_end` metodu ile birleştirilip geliştirilecek (Will be combined and improved with the `_find_basic_end` method from `enhanced_d64_reader.py`).
            -   `extract_sys_call_info(data)`: Mevcut haliyle taşınacak (Will be migrated as is).
            -   `generate_disassembly_plan(analysis)`: Mevcut haliyle taşınacak (Will be migrated as is).

### **3.3. `core/memory_services.py` - Merkezi Hafıza Servisleri (Centralized Memory Services)**

Bu modül, C64 hafıza haritası, KERNAL rutinleri, BASIC ROM ve Zero Page adresleri gibi tüm statik hafıza bilgilerini yönetecektir (This module will manage all static memory information such as the C64 memory map, KERNAL routines, BASIC ROM, and Zero Page addresses).

-   **Kaynak Modüller (Source Modules):** `c64_memory_manager.py`, `enhanced_c64_memory_manager.py`, `hybrid_program_analyzer.py`
-   **Sorumluluklar (Responsibilities):**
    -   `resources/` dizinindeki JSON dosyalarından hafıza haritalarını yüklemek (Loading memory maps from JSON files in the `resources/` directory).
    -   Belirli bir hafıza adresinin ne anlama geldiğini (örn: `$D020` -> Border Color) döndürmek (Returning the meaning of a specific memory address, e.g., `$D020` -> Border Color).
    -   Disassembler ve decompiler için sembolik isimler sağlamak (Providing symbolic names for the disassembler and decompiler).

-   **Taşınacak Bileşenler (Components to be Migrated):**
    -   **Sınıf (Class): `C64MemoryManager`** (`enhanced_c64_memory_manager.py`'den alınacak - To be taken from `enhanced_c64_memory_manager.py`).
        -   **Metotlar (Methods):**
            -   `load_memory_maps()`: Tüm JSON dosyalarını tek seferde yükleyecek şekilde güncellenecek (Will be updated to load all JSON files at once).
            -   `get_address_info(address)`: `hybrid_program_analyzer.py`'deki `get_memory_name` fonksiyonu ile birleştirilecek (Will be combined with the `get_memory_name` function from `hybrid_program_analyzer.py`).
            -   `get_label_for_address(address)`: Disassembler için etiket üreten yeni bir metot (A new method to generate labels for the disassembler).

### **3.4. `processing/disassembler_engine.py` - Birleşik Disassembler Motoru (Unified Disassembler Engine)**

Bu modül, mevcut 4 farklı disassembler motorunu tek bir arayüz altında birleştirecektir (This module will unify the 4 existing disassembler engines under a single interface).

-   **Kaynak Modüller (Source Modules):** `disassembler.py`, `advanced_disassembler.py`, `improved_disassembler.py`, `py65_professional_disassembler.py`
-   **Sorumluluklar (Responsibilities):**
    -   Kullanıcının seçtiği motoru (basic, advanced, improved, py65) kullanarak disassembly yapmak (Performing disassembly using the user-selected engine - basic, advanced, improved, py65).
    -   `memory_services`'ten aldığı bilgilerle koda yorumlar ve etiketler eklemek (Adding comments and labels to the code with information from `memory_services`).
    -   Illegal opcode'ları desteklemek (Supporting illegal opcodes).

-   **Taşınacak Bileşenler (Components to be Migrated):**
    -   **Sınıf (Class): `DisassemblerEngine`** (Yeni oluşturulacak - To be newly created)
        -   **Metot (Method): `disassemble(code, engine_type='py65_professional', options={})`**
            -   Bu metot, `engine_type` parametresine göre ilgili disassembler sınıfını (`BasicDisassembler`, `AdvancedDisassembler` vb.) çağıracak bir "fabrika" (factory) görevi görecektir (This method will act as a "factory" that calls the relevant disassembler class (`BasicDisassembler`, `AdvancedDisassembler`, etc.) based on the `engine_type` parameter).
    -   **Sınıflar (Classes):**
        -   `BasicDisassembler`: `disassembler.py`'den.
        -   `AdvancedDisassembler`: `advanced_disassembler.py`'den.
        -   `ImprovedDisassembler`: `improved_disassembler.py`'den.
        -   `Py65Disassembler`: `py65_professional_disassembler.py`'den.
        -   Her sınıf, ortak bir `IDisassembler` arayüzünü (interface) uygulayacak şekilde standardize edilecek (Each class will be standardized to implement a common `IDisassembler` interface).

### **3.5. `processing/transpiler_engine.py` - Birleşik Dönüştürücü Motoru (Unified Transpiler Engine)**

Bu modül, disassembler çıktısını alıp C, QBasic, PDSX gibi yüksek seviyeli dillere dönüştürecektir (This module will take the disassembler output and transpile it into high-level languages like C, QBasic, PDSX).

-   **Kaynak Modüller (Source Modules):** `parser.py`, `c64bas_transpiler_c.py`, `c64bas_transpiler_qbasic.py`, `pdsXv12.py`
-   **Sorumluluklar (Responsibilities):**
    -   Assembly kodunu satır satır ayrıştırmak (Parsing the Assembly code line by line).
    -   Assembly komutlarını hedef dilin (target language) yapılarına çevirmek (Translating Assembly instructions into the structures of the target language).
    -   Hafıza haritası bilgilerini kullanarak değişkenler ve fonksiyonlar oluşturmak (Creating variables and functions using memory map information).

-   **Taşınacak Bileşenler (Components to be Migrated):**
    -   **Sınıf (Class): `TranspilerEngine`** (Yeni oluşturulacak - To be newly created)
        -   **Metot (Method): `transpile(assembly_code, target_language)`**
            -   `target_language`'a göre ilgili transpiler'ı çağıracak (Will call the relevant transpiler based on `target_language`).
    -   **Sınıf (Class): `AssemblyParser`** (`parser.py`'den `CodeEmitter` ve `parse_line` mantığı alınacak - Logic from `CodeEmitter` and `parse_line` in `parser.py` will be taken).
    -   **Sınıf (Class): `CTranspiler`** (`c64bas_transpiler_c.py`'den mantık alınacak - Logic will be taken from `c64bas_transpiler_c.py`).
    -   **Sınıf (Class): `QBasicTranspiler`** (`c64bas_transpiler_qbasic.py`'den mantık alınacak - Logic will be taken from `c64bas_transpiler_qbasic.py`).

---

## 🏭 **BÖLÜM 4: İMALAT PLANI VE GELİŞTİRME ODAKLARI (PART 4: MANUFACTURING PLAN AND DEVELOPMENT FOCUS)**

### **4.1. Odak 1: Akıllı Disassembly ve Kod Yorumlama (Focus 1: Intelligent Disassembly and Code Interpretation)**

Disassembly süreci, sadece makine kodunu Assembly'e çevirmekle kalmayacak, aynı zamanda kodu "anlamlandıracaktır" (The disassembly process will not only convert machine code to Assembly but will also "make sense" of the code).

-   **Eylem Planı (Action Plan):**
    1.  **Etiket Üretimi (Label Generation):** `disassembler_engine`, bir JMP veya JSR komutu gördüğünde, hedef adresi `memory_services`'e soracaktır (When the `disassembler_engine` sees a JMP or JSR instruction, it will query the target address from `memory_services`). Eğer adres bilinen bir KERNAL veya BASIC rutini ise (örn: `$FFD2` - CHROUT), kod `JSR $FFD2` yerine `JSR CHROUT` olarak üretilecektir (If the address is a known KERNAL or BASIC routine, e.g., `$FFD2` - CHROUT, the code will be generated as `JSR CHROUT` instead of `JSR $FFD2`).
    2.  **Değişken Üretimi (Variable Generation):** LDA, STA gibi hafıza erişim komutlarında, eğer adres bilinen bir Zero Page değişkeni veya donanım register'ı ise (örn: `$D011` - Screen Control Register), kod `STA $D011` yerine `STA V_SCR_CTRL_REG_1` gibi anlamlı bir etiketle üretilecektir (In memory access instructions like LDA, STA, if the address is a known Zero Page variable or hardware register, e.g., `$D011` - Screen Control Register, the code will be generated with a meaningful label like `STA V_SCR_CTRL_REG_1` instead of `STA $D011`).
    3.  **Otomatik Yorumlama (Automatic Commenting):** `disassembler_engine`, `memory_services`'i kullanarak, donanım register'larına yapılan atamalara otomatik yorumlar ekleyecektir (The `disassembler_engine` will use `memory_services` to add automatic comments to assignments made to hardware registers). Örnek (Example): `LDA #%00011011 ; Y-scroll ve 25 satır modunu etkinleştir (Enable Y-scroll and 25-line mode)`.

### **4.2. Odak 2: Kusursuz Disk Okuma ve Deşifreleme (Focus 2: Flawless Disk Reading and Deciphering)**

Disk okuma sistemi, standart formatların yanı sıra, sıkıştırılmış ve kopya korumalı diskleri de anlayabilmelidir (The disk reading system must be able to understand not only standard formats but also compressed and copy-protected disks).

-   **Eylem Planı (Action Plan):**
    1.  **`formats/compression_handler.py` Modülünün Oluşturulması (Creation of the `formats/compression_handler.py` Module):** Bu modül, Exomizer, Pucrunch gibi popüler sıkıştırma formatlarını açmak için özel fonksiyonlar içerecektir (This module will contain special functions to decompress popular compression formats like Exomizer, Pucrunch).
    2.  **`disk_services` Entegrasyonu (Integration with `disk_services`):** `disk_services` modülü, bir PRG dosyasını okuduğunda, dosyanın başlangıcındaki "sihirli baytları" (magic bytes) kontrol ederek sıkıştırılmış olup olmadığını anlayacak ve eğer öyleyse `compression_handler`'a delege edecektir (When the `disk_services` module reads a PRG file, it will understand if it is compressed by checking the "magic bytes" at the beginning of the file, and if so, delegate it to the `compression_handler`).
    3.  **Turbo Loader Analizi (Turbo Loader Analysis):** TAP ve T64 formatları için, standart KERNAL yükleme rutinleri dışındaki hızlı yükleyici (fast loader) kod blokları tespit edilecek ve bu bloklar özel olarak analiz edilecektir (For TAP and T64 formats, fast loader code blocks outside the standard KERNAL loading routines will be detected and analyzed specially).

### **4.3. Odak 3: Hafıza Haritası Destekli Transpiler/Decompiler (Focus 3: Memory-Map-Aware Transpiler/Decompiler)**

Transpiler ve Decompiler motorları, sadece Assembly komutlarını değil, aynı zamanda `disassembler_engine` tarafından üretilen etiketleri ve yorumları da kullanarak daha "insan-okunur" (human-readable) kod üretecektir (The Transpiler and Decompiler engines will generate more "human-readable" code by using not only the Assembly instructions but also the labels and comments produced by the `disassembler_engine`).

-   **Eylem Planı (Action Plan):**
    1.  **Sembolik Değişken Kullanımı (Use of Symbolic Variables):** `transpiler_engine`, `V_BORDER_COLOR` gibi bir etiket gördüğünde, bunu C dilinde `unsigned char* V_BORDER_COLOR = (unsigned char*)0xD020;` gibi bir tanıma dönüştürecektir (When the `transpiler_engine` sees a label like `V_BORDER_COLOR`, it will convert it into a C definition like `unsigned char* V_BORDER_COLOR = (unsigned char*)0xD020;`).
    2.  **Fonksiyon Çağrılarının Dönüşümü (Transformation of Function Calls):** `JSR CHROUT` komutu, C dilinde doğrudan `putchar()` fonksiyonuna veya eşdeğer bir yapıya dönüştürülebilir (The `JSR CHROUT` instruction can be directly converted to the `putchar()` function or an equivalent structure in C).
    3.  **Döngü ve Koşul Yapılarının Tanınması (Recognition of Loop and Conditional Structures):** `decompiler_engine`, belirli Assembly kalıplarını (örn: `CMP`, `BNE` ile oluşturulan döngüler) tanıyarak bunları `for` veya `while` döngülerine dönüştürecektir (The `decompiler_engine` will recognize specific Assembly patterns, e.g., loops created with `CMP`, `BNE`, and convert them into `for` or `while` loops).

---

Bu plan, D64 Converter projesini dağınık bir kod tabanından (from a scattered codebase), endüstri standardı bir geliştirme stüdyosuna (to an industry-standard development studio) dönüştürmek için gereken tüm adımları **net, kesin ve ayrıntılı** bir şekilde ortaya koymaktadır (This plan lays out all the necessary steps to transform the D64 Converter project from a scattered codebase to an industry-standard development studio in a **clear, precise, and detailed** manner).
