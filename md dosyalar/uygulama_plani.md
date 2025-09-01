# ⚔️ KIZILELMA OPERASYONU: UYGULAMA PLANI (OPERATION REDAPPLE: IMPLEMENTATION PLAN) v1.0

**Referans Belge (Reference Document):** `son_plan_25.md`  
**Tarih (Date):** 25 Temmuz 2025 (July 25, 2025)  
**Durum (Status):** Yürütülüyor (In Progress)  
**Proje (Project):** KızılElma Geliştirme Stüdyosu (RedApple Development Studio)

---

## 📜 **GİRİŞ (INTRODUCTION)**

Bu belge, `son_plan_25.md`'de tanımlanan mimari hedeflere ulaşmak için izlenecek teknik adımları, fazları ve görevleri ayrıntılı olarak listeler. Her faz, projenin temelden yukarıya doğru, modüler ve test edilebilir bir şekilde inşa edilmesini sağlayacak şekilde tasarlanmıştır.

---

## **FAZ 1: TEMEL ATMA VE İSKELETİN KURULMASI (PHASE 1: FOUNDATION AND SCAFFOLDING)**

**Amaç:** Yeni proje yapısını fiziksel olarak oluşturmak, kaynakları taşımak ve modül iskeletlerini hazırlamak. Bu fazda kod yazımından çok, proje hijyeni ve organizasyonuna odaklanılacaktır.

*   **Adım 1.1: Proje Kök Dizini Oluşturma**
    *   **Görev:** Ana proje dizininden bir seviye yukarıda, `d64_converter_v2` adında yeni bir klasör oluştur.
    *   **Komut (PowerShell):** `New-Item -ItemType Directory -Path "c:\Users\dell\Documents\projeler\d64_converter_v2"`
    *   **Doğrulama:** Yeni dizinin başarıyla oluşturulduğunu kontrol et.

*   **Adım 1.2: Hiyerarşik Dizin Yapısını Oluşturma**
    *   **Görev:** `son_plan_25.md` (Bölüm 2) içinde belirtilen tüm alt dizinleri (`core`, `processing`, `formats`, `resources`, `gui`, `external_tools`, `logs`, `output`, `tests`) oluştur. `resources` ve `output` içindeki alt dizinleri de (`memory_maps`, `opcodes`, `tokens`, `prg`, `asm`, `c`, `qbasic`) bu adımda oluştur.
    *   **Komut (PowerShell):**
        ```powershell
        $baseDir = "c:\Users\dell\Documents\projeler\d64_converter_v2"
        New-Item -ItemType Directory -Path "$baseDir\core"
        New-Item -ItemType Directory -Path "$baseDir\processing"
        New-Item -ItemType Directory -Path "$baseDir\formats"
        New-Item -ItemType Directory -Path "$baseDir\resources"
        New-Item -ItemType Directory -Path "$baseDir\resources\memory_maps"
        New-Item -ItemType Directory -Path "$baseDir\resources\opcodes"
        New-Item -ItemType Directory -Path "$baseDir\resources\tokens"
        New-Item -ItemType Directory -Path "$baseDir\gui"
        New-Item -ItemType Directory -Path "$baseDir\gui\widgets"
        New-Item -ItemType Directory -Path "$baseDir\external_tools"
        New-Item -ItemType Directory -Path "$baseDir\logs"
        New-Item -ItemType Directory -Path "$baseDir\output"
        New-Item -ItemType Directory -Path "$baseDir\output\prg"
        New-Item -ItemType Directory -Path "$baseDir\output\asm"
        New-Item -ItemType Directory -Path "$baseDir\output\c"
        New-Item -ItemType Directory -Path "$baseDir\output\qbasic"
        New-Item -ItemType Directory -Path "$baseDir\tests"
        ```
    *   **Doğrulama:** `tree /F` veya benzeri bir komutla dizin yapısının plana uygunluğunu kontrol et.

*   **Adım 1.3: Kaynak (Resource) Dosyalarını Taşıma**
    *   **Görev:** Mevcut `d64_converter` dizinindeki tüm `.json` kaynak dosyalarını yeni `d64_converter_v2/resources/` altındaki ilgili klasörlere taşı.
    *   **Detaylar:**
        *   `c64_memory_map.json`, `memory_map.json` -> `resources/memory_maps/c64_memory_map.json` (gerekirse birleştirilip temizlenerek)
        *   `kernal_routines.json`, `basic_rom.json` -> `resources/memory_maps/`
        *   `opcode_map.json`, `opcode.json` -> `resources/opcodes/6502_opcodes.json` (birleştirilip temizlenerek)
        *   `basic_v2_tokens.json` -> `resources/tokens/`
    *   **Doğrulama:** Tüm kaynak dosyaların yeni yerlerinde olduğunu ve eski konumda kalmadığını onayla.

*   **Adım 1.4: Python Paketlerini Başlatma**
    *   **Görev:** Python'un modülleri paket olarak tanıması için `core`, `processing`, `formats`, `gui`, `external_tools`, `tests` dizinlerinin her birine boş bir `__init__.py` dosyası ekle.
    *   **Komut (PowerShell):**
        ```powershell
        $dirs = @("core", "processing", "formats", "gui", "external_tools", "tests")
        foreach ($dir in $dirs) { New-Item -ItemType File -Path "c:\Users\dell\Documents\projeler\d64_converter_v2\$dir\__init__.py" }
        ```
    *   **Doğrulama:** Dosyaların oluşturulduğunu kontrol et.

*   **Adım 1.5: Modül İskelet Dosyalarını Oluşturma**
    *   **Görev:** Planda belirtilen tüm yeni `.py` modül dosyalarını ilgili dizinlerde boş olarak oluştur. Bu, projenin genel yapısını görmeyi kolaylaştırır.
    *   **Detaylar:** `core/main_engine.py`, `core/disk_services.py`, `processing/disassembler_engine.py`, vb. tüm dosyalar.
    *   **Doğrulama:** Tüm `.py` dosyalarının doğru dizinlerde ve boş olarak mevcut olduğunu onayla.

---

## **FAZ 2: ÇEKİRDEK SERVİSLERİN İNŞASI (PHASE 2: BUILDING THE CORE SERVICES)**

**Amaç:** Sistemin temel veri ve mantık sağlayıcılarını (`core` paketi) hayata geçirmek. Bu modüller, diğer tüm üst katman modüllerinin temelini oluşturacaktır.

*   **Adım 2.1: `core/memory_services.py` - Merkezi Hafıza Servisleri**
    *   **Görev:** C64 hafıza haritası, KERNAL/BASIC rutinleri ve adres etiketlemesi ile ilgili tüm mantığı bu modülde merkezileştir.
    *   **Alt Adımlar:**
        1.  `C64MemoryManager` sınıfını oluştur.
        2.  **Kaynak Kod:** `enhanced_c64_memory_manager.py`'deki sınıf yapısını temel al.
        3.  `load_memory_maps()` metodunu implemente et. Bu metot, `resources/memory_maps` ve `resources/opcodes` altındaki tüm ilgili JSON dosyalarını okuyup, verileri sınıf içindeki sözlüklerde (dictionaries) saklamalıdır.
        4.  `get_address_info(address)` metodunu implemente et. Bu metot, `hybrid_program_analyzer.py`'deki `get_memory_name` fonksiyonunun mantığını içermeli ve verilen bir adrese karşılık gelen sembolik ismi (örn: `$D020` -> `V_BORDER_COLOR`) ve açıklamasını döndürmelidir.
        5.  `get_label_for_address(address)` metodunu implemente et. Bu, `get_address_info`'ya benzer ancak özellikle disassembler için daha kısa ve temiz etiketler (`CHROUT`, `V_SCR_CTRL_REG_1` gibi) döndürmeye odaklanmalıdır.
    *   **Test:** Bu modül tamamlandığında, farklı adresler (`$FFD2`, `$D011`, `$0400`) için doğru etiket ve bilgileri döndürdüğünü doğrulayan birim testleri (`tests/test_memory_services.py`) yaz.

*   **Adım 2.2: `core/disk_services.py` - Birleşik Disk Servisleri**
    *   **Görev:** Tüm disk imajı okuma, format tanıma, dizin listeleme ve dosya çıkarma işlemlerini tek bir sınıfta birleştir.
    *   **Alt Adımlar:**
        1.  `UnifiedDiskReader` sınıfını oluştur.
        2.  `detect_format(file_path)` metodunu implemente et. **Kaynak Kod:** `enhanced_disk_reader.py`'deki `identify_format` metodunun mantığını temel al. Dosya uzantısı ve "sihirli bayt" kontrolü yapmalıdır.
        3.  `read_directory(disk_data, format_info)` metodunu implemente et. **Kaynak Kod:** `enhanced_d64_reader.py`'deki `read_directory_d64`, `read_t64_directory`, `read_tap_directory` gibi formatlara özel dizin okuma metotlarının mantığını, `format_info` parametresine göre dinamik olarak çalışacak şekilde birleştir.
        4.  `extract_file(file_entry)` metodunu implemente et. **Kaynak Kod:** `d64_reader.py`'deki `extract_prg_file`, `extract_seq_file` gibi basit dosya çıkarma fonksiyonlarını birleştir.
        5.  **Fallback Mekanizması:** Gelişmiş okuma metotlarında bir hata oluşması durumunda (try-except blokları ile), `d64_reader.py`'nin daha basit ve güvenilir okuma fonksiyonlarını çağıracak bir geri çekilme mantığı ekle.
    *   **Test:** `tests/test_disk_services.py` içinde farklı disk imajları (D64, T64, vb.) için dizin listeleme ve dosya çıkarma işlemlerinin doğru çalıştığını test et.

*   **Adım 2.3: `core/program_analyzer.py` - Gelişmiş Program Analizcisi**
    *   **Görev:** Bir PRG dosyasının içeriğini analiz ederek BASIC, Assembly veya hibrit yapısını, kod bloklarının sınırlarını ve önemli sistem çağrılarını tespit et.
    *   **Alt Adımlar:**
        1.  `HybridProgramAnalyzer` sınıfını `hybrid_program_analyzer.py`'den bu yeni dosyaya taşı.
        2.  `find_basic_end(data)` metodunu, `enhanced_d64_reader.py`'deki `_find_basic_end` metodunun daha sağlam mantığıyla birleştirerek geliştir.
        3.  `analyze_prg_data` metodunun, analiz sonucunda `memory_services`'i kullanarak `SYS` hedeflerine (`SYS 64738` -> `SYS (WARM_START)`) anlamlı etiketler eklemesini sağla.
        4.  `generate_disassembly_plan` metodunun çıktısının, `disassembler_engine` için bir "görev listesi" (örn: "BASIC bölümünü listele", "Adres $C000-$CFFF arasını disassemble et") oluşturacak şekilde standartlaştırılmasını sağla.
    *   **Test:** Farklı PRG dosyaları (sadece BASIC, sadece Assembly, hibrit) üzerinde analizlerin doğru sonuçlar verdiğini (doğru başlangıç/bitiş adresleri, doğru SYS çağrıları) test et.

---

## **FAZ 3: İŞLEM MOTORLARININ GELİŞTİRİLMESİ (PHASE 3: DEVELOPING THE PROCESSING ENGINES)**

**Amaç:** Ham veriyi anlamlı çıktılara dönüştüren ana işlem birimlerini (`processing` paketi) oluşturmak. Bu faz, projenin en karmaşık mantığını içerir.

*   **Adım 3.1: `processing/disassembler_engine.py` - Birleşik Disassembler Motoru**
    *   **Görev:** Mevcut 4 disassembler'ı tek bir "fabrika" sınıfı altında birleştirmek ve "Akıllı Disassembly" özelliklerini eklemek.
    *   **Alt Adımlar:**
        1.  Soyut bir `IDisassembler` arayüzü (ABC - Abstract Base Class kullanarak) tanımla. Bu arayüz, `disassemble_chunk(data, start_address)` gibi bir metot içermelidir.
        2.  `BasicDisassembler` (`disassembler.py`), `AdvancedDisassembler` (`advanced_disassembler.py`), `ImprovedDisassembler` (`improved_disassembler.py`) ve `Py65Disassembler` (`py65_professional_disassembler.py`) sınıflarını bu dosyaya taşı ve her birinin `IDisassembler` arayüzünü uygulamasını sağla.
        3.  `DisassemblerEngine` adında bir fabrika sınıfı oluştur.
        4.  `disassemble(code, engine_type, options)` adında bir metot oluştur. Bu metot, `engine_type`'a göre ilgili disassembler sınıfının bir örneğini oluşturup disassembly işlemini ona delege etmelidir.
        5.  **Akıllı Disassembly Entegrasyonu:** Disassembly döngüsü içinde, her bir komutun işleneni (operand) olan adresi (`JSR $FFD2`'deki `$FFD2` gibi) alıp `core.memory_services.get_label_for_address()` ile kontrol et. Eğer bir etiket varsa, çıktıyı `JSR CHROUT` şeklinde üret. Donanım register'larına yapılan erişimler için otomatik yorumlar ekle (`STA $D020` -> `STA BORDER_COLOR ; Ekran çerçeve rengini ayarla`).
    *   **Test:** `tests/test_disassembler.py` içinde, aynı kod parçasının 4 farklı motorla ve akıllı özellikler etkinleştirilmiş şekilde doğru çıktılar ürettiğini doğrula.

*   **Adım 3.2: `processing/transpiler_engine.py` - Birleşik Dönüştürücü Motoru**
    *   **Görev:** Disassembler çıktısını C ve QBasic gibi dillere çeviren mantığı birleştirmek.
    *   **Alt Adımlar:**
        1.  `TranspilerEngine` fabrika sınıfını oluştur.
        2.  `transpile(assembly_code, target_language)` metodunu oluştur.
        3.  `AssemblyParser` sınıfını `parser.py`'den taşıyıp modernize et. Bu sınıf, etiketli ve yorumlu assembly kodunu ayrıştırabilmelidir.
        4.  `CTranspiler` ve `QBasicTranspiler` sınıflarını ilgili kaynak modüllerden (`c64bas_transpiler_c.py`, `c64bas_transpiler_qbasic.py`) mantığı alarak oluştur.
        5.  **Hafıza Haritası Destekli Dönüşüm:** Transpiler'ların, `V_BORDER_COLOR` gibi sembolik etiketleri C'de `unsigned char* V_BORDER_COLOR = (unsigned char*)0xD020;` gibi doğru tanımlamalara çevirmesini sağla. `JSR CHROUT` gibi KERNAL çağrılarını, C'de `putchar()` gibi standart kütüphane fonksiyonlarına veya özel olarak oluşturulmuş `kernal_call("CHROUT")` gibi sarmalayıcı (wrapper) fonksiyonlara dönüştürmesini sağla.
    *   **Test:** Basit bir assembly programının (örneğin ekran rengini değiştiren) hem C hem de QBasic'e doğru şekilde çevrildiğini test et.

---

## **FAZ 4: ENTEGRASYON, GUI VE TAMAMLAMA (PHASE 4: INTEGRATION, GUI, AND COMPLETION)**

**Amaç:** Oluşturulan backend motorlarını birleştirmek, GUI'yi bağlamak ve projeyi son kullanıcı için hazır hale getirmek.

*   **Adım 4.1: `core/main_engine.py` - Ana Sistem Motoru**
    *   **Görev:** GUI ile backend servisleri arasında bir köprü görevi görecek olan ana motoru oluştur.
    *   **Alt Adımlar:**
        1.  `MainEngine` sınıfını oluştur.
        2.  `process_disk_image(file_path)` gibi üst seviye bir metot tanımla. Bu metot, sırasıyla `disk_services`, `program_analyzer`, `disassembler_engine` ve `transpiler_engine`'i çağırmalı ve sonuçları GUI'ye sunulacak formatta toplamalıdır.

*   **Adım 4.2: `gui/main_window.py` - Ana GUI Penceresi**
    *   **Görev:** Projenin ana arayüzünü oluşturmak ve olayları (buton tıklamaları vb.) `main_engine`'e bağlamak.
    *   **Alt Adımlar:**
        1.  Mevcut GUI kodundan (`main.py` veya benzeri) temel Tkinter pencere yapısını taşı.
        2.  "Dosya Aç" butonu tıklandığında `main_engine.process_disk_image()` metodunu çağırmasını sağla.
        3.  Sonuçları göstermek için metin kutuları, ağaç görünümleri (dizin listesi için) ve sekmeler (farklı çıktılar için) ekle.

*   **Adım 4.3: Eski Kodun Temizlenmesi**
    *   **Görev:** Yeni yapıya tamamen geçildiğinden ve tüm değerli kodların taşındığından emin olduktan sonra, eski 79+ Python dosyasını ve artık kullanılmayan diğer dosyaları projeden sil.
    *   **ÖNEMLİ:** Bu adımdan önce mutlaka projenin tamamının bir yedeğini al.

*   **Adım 4.4: `README.md`'nin Yazılması**
    *   **Görev:** Projenin yeni yapısını, nasıl kurulacağını, nasıl kullanılacağını ve temel özelliklerini anlatan kapsamlı bir `README.md` dosyası oluştur.

Bu plan, KızılElma hedefine ulaşmak için sistematik, ölçülebilir ve yönetilebilir bir yol sunmaktadır. Her fazın sonunda yapılacak testler, projenin sağlam temeller üzerinde ilerlemesini garanti altına alacaktır.
