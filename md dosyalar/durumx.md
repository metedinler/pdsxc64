# 🚦 Proje Durum Raporu (durum.md)

Bu belge, proje kök dizinindeki tüm `.py` dosyalarının görev tanımlarını, `main.py` ve `main_optimized.py` çalıştırıldığında izlenen süreçleri ve erişilen modülleri, ayrıca modüller arası bağımlılık analizine dayalı gerekli ve gereksiz modülleri listeler.

---

## 1. Modül Envanteri ve Görev Tanımları

Aşağıda, proje kök dizinindeki her `.py` dosyasının kısa görev tanımı bulunmaktadır:

- `advanced_disassembler.py`  
  Gelişmiş disassembler motorunun implementasyonu. Daha karmaşık komut grupları ve illegal opcode desteği içerir.

- `assembly_formatters.py`  
  Disassembler çıktısını ve assembly kodlarını belirli formata oturtmak için helper fonksiyonları barındırır.

- `basic_detokenizer.py`  
  BASIC tokenlarını okumak ve insan tarafından okunabilir kod metnine dönüştürmek için detokenizer.

- `c1541_python_emulator.py`  
  C1541 disk sürücüsü komutlarını simüle eden Python emülatör.

- `c64bas_transpiler_c.py`  
  Disassembler çıktısını C diline dönüştürmek için transpiler (temel versiyon).

- `c64bas_transpiler_c_temel.py`  
  İlk taslak C transpiler; `c64bas_transpiler_c.py` öncesi basit implementasyon.

- `c64bas_transpiler_qbasic.py`  
  Disassembler çıktısını QBasic diline dönüştüren transpiler.

- `c64_basic_parser.py`  
  BASIC kod parçacıklarını analiz eden ve token sırasını ayrıştıran parser.

- `c64_basic_parser_new.py`  
  `c64_basic_parser.py` üzerine güncellemeler içeren yeni BASIC parser.

- `c64_memory_manager.py`  
  C64 hafıza haritası ve donanım register adreslerini yöneten basit manager.

- `code_analyzer.py`  
  Assembly ve BASIC kodu üzerinde desen analizi, illegal opcode tespiti ve istatistik oluşturma.

- `configuration_manager.py`  
  Program parametreleri, kullanıcı ayarları ve config dosya yönetimi.

- `database_manager.py`  
  İşlem sonuçlarını SQLite veya JSON formatında saklamak için DB erişim katmanı.

- `d64_reader.py`  
  D64 disk imajı okuma ve temel dosya çıkarma fonksiyonları.

- `decompiler.py`  
  Genel decompiler arayüzü; farklı decompiler motorlarını callback ile yönetir.

- `decompiler_c.py`  
  Decompiler çıktısını C diline çeviren modül.

- `decompiler_cpp.py`  
  Decompiler çıktısını C++ diline çevirmek için örnek implementasyon.

- `decompiler_c_2.py`  
  `decompiler_c.py` üzerinde iyileştirme içerir.

- `decompiler_qbasic.py`  
  Decompiler çıktısını QBasic koduna dönüştüren modül.

- `disassembler.py`  
  Temel disassembler motoru; 6502 komutlarını string listesine dönüştürür.

- `enhanced_basic_decompiler.py`  
  İlk BASIC decompiler taslağı; basit token dönüşümleri yapar.

- `enhanced_c64_memory_manager.py`  
  Geliştirilmiş C64 hafıza yönetimi; JSON kaynaklardan dinamik yükleme.

- `enhanced_d64_reader.py`  
  Gelişmiş D64 okuma; Exomizer gibi sıkıştırma format desteği içerir.

- `enhanced_disk_reader.py`  
  Tüm disk formatlarını (D64, T64, G64) destekleyen üst seviye disk okuyucu.

- `gui.py`  
  Basit Tkinter tabanlı GUI arayüzü (önceki versiyon).

- `gui_debug_system.py`  
  GUI bileşenlerine debug kodları ekleyen sistem.

- `gui_demo.py`  
  GUI örnek uygulması; tasarım gösterimi amaçlı.

- `gui_manager.py`  
  X1 GUI entegrasyonu ve debug özellikli ana GUI yöneticisi.

- `gui_styles.py`  
  GUI renk, font ve tema tanımlamalarını içerir.

- `illegal_opcode_analyzer.py`  
  Koddaki illegal 6502 opcode kullanımını tespit eden analizör.

- `improved_disassembler.py`  
  `disassembler.py` üzerine performans ve yorum ekleme iyileştirmeleri.

- `memory_manager.py`  
  `c64_memory_manager.py` alternatifi, farklı veri yapıları kullanır.

- `module_analyzer.py`  
  Modüller arası bağımlılık analizi yapan script.

- `opcode_generator.py`  
  6502 opcode tablosu ve illegal opcode üreticisi.

- `opcode_manager.py`  
  JSON tabanlı opcode yönetimi ve sorgulama fonksiyonları.

- `opcode_manager_simple.py`  
  Basit opcode sorgulama fonksiyonlarını içerir.

- `parser.py`  
  Genel purpose lexer/parser; assembly satırlarını token'a böler.

- `pdsXv12.py`  
  PDSX decompiler için destek dosyaları ve transform fonksiyonları.

- `pdsXv12_minimal.py`  
  `pdsXv12.py`'nin hafifletilmiş versiyonu.

- `petcat_detokenizer.py`  
  Petcat tarafından oluşturulmuş BASIC listelerini detokenize eden araç.

- `program_organizer.py`  
  Proje dosya yapısını analiz edip rapor çıkaran script.

- `py65_professional_disassembler.py`  
  Py65 tabanlı profesyonel disassembler entegrasyonu.

- `quick_test.py`  
  Farklı modül ve fonksiyon testlerinin hızlı doğrulamasını sağlar.

- `sid_converter.py`  
  SID müzik dosyalarını PCM formatına dönüştürme aracı.

- `simple_analyzer.py`  
  Küçük çaplı kod analiz görevleri için util fonksiyonları.

- `sprite.py`  
  Sprite verilerini işleyen temel kütüphane.

- `sprite_converter.py`  
  Sprite formatları arasında dönüştürme desteği.

- `system_diagnostics.py`  
  Ortam ve bağımlılık kontrolleri, eksik modüller raporu.

- `system_repair.py`  
  Eksik paketleri kurma ve yapılandırma onarımları yapar.

- `tool_command_generator.py`  
  Komut satırı için dinamik yardımcı komut oluşturucu.

- `toolbox_manager.py`  
  Harici geliştirici araçları yönetme paneli.

- `ultimate_cleanup.py`  
  Eski ve gereksiz dosyaları temizleyen script.

- `unified_decompiler.py`  
  Farklı decompiler motorlarını tek bir arayüz altına alan wrapper.

- `main.py`  
  Süper birleşik ana giriş noktası: tüm modülleri otomatik yükler ve CLI sunar.

- `main_minimal.py`  
  Sadece temel okuma ve disassembler işlevlerini içeren minimal CLI.

- `main_optimized.py`  
  `main.py` mantığından performans ve yavaş açılan modülleri atarak optimize edilmiş sürüm.

- `main_unified.py`  
  `main.py` ile `main_optimized.py` arasında orta seviye birleşik giriş noktası.

## 2. `main.py` Çalışma Süreçleri ve Erişilen Modüller

1. `load_core_modules()` çağrılır:
   - Aşağıdaki modüller dinamik import edilir ve kullanıma hazır hale gelir:
     - `unified_decompiler`, `code_analyzer`, `enhanced_c64_memory_manager`, `gui_manager`, `improved_disassembler`, `advanced_disassembler`,
       `c64bas_transpiler_c_temel`, `enhanced_d64_reader`, `database_manager`,
       `d64_reader`, `disassembler`, `parser`, `c64_basic_parser`,
       `sid_converter`, `sprite_converter`, `clean_gui_selector`
2. `print_banner()` ile ANSI renkli banner görüntülenir.
3. `setup_enhanced_logging()` ile renkli ve timestamp’li logging yapılandırılır.
4. `create_virtual_environment()` sanal ortam kontrolü ve gerekirse paket yükleme yapılır.
5. CLI argümanları parse edilerek ana uygulama akışı başlatılır.

## 3. `main_optimized.py` Çalışma Süreçleri ve Erişilen Modüller

1. `check_and_activate_venv()` ile `venv_asmto` kontrol edilir, varsa aktif edilir.
2. Yoksa `create_venv_if_needed()` sanal ortam ve paket yükleme işlemleri yapılır.
3. `launch_application()` ile:
   - `memory_manager.memory_optimizer` başlatılır.
   - `configuration_manager.ConfigurationManager` yüklenir ve çalıştırılır.
4. Hata durumunda `launch_gui_fallback()` ile:
   - `gui_manager.D64ConverterGUI` kullanılarak GUI başlatılır.

**Erişilen ana modüller:**
```text
memory_manager, configuration_manager, gui_manager, subprocess, tkinter
```

## 4. Gerekli ve Gereksiz Modüller

**4.1. Gerekli Modüller**
Aşağıdakiler doğrudan ana giriş noktalarında kullanılır:
```text
unified_decompiler.py, code_analyzer.py, enhanced_c64_memory_manager.py,
gui_manager.py, improved_disassembler.py, advanced_disassembler.py,
c64bas_transpiler_c_temel.py, enhanced_d64_reader.py, database_manager.py,
d64_reader.py, disassembler.py, parser.py, c64_basic_parser.py,
sid_converter.py, sprite_converter.py, clean_gui_selector.py,
memory_manager.py, configuration_manager.py, main.py, main_optimized.py
```

**4.2. Gereksiz Modüller**
Ana giriş noktalarında kullanılmayan veya bağımlılığı olmayan modüller:
```text
add_pseudo.py, assembly_formatters.py, basic_detokenizer.py,
c1541_python_emulator.py, c64bas_transpiler_c.py, c64bas_transpiler_qbasic.py,
c64_basic_parser_new.py, module_analyzer.py, opcode_generator.py,
opcode_manager.py, opcode_manager_simple.py, pdsXv12.py,
pdsXv12_minimal.py, petcat_detokenizer.py, program_organizer.py,
quick_test.py, simple_analyzer.py, system_diagnostics.py,
system_repair.py, toolbox_manager.py, ultimate_cleanup.py
```
