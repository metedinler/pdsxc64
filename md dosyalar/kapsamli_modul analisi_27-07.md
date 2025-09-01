Şimdi sınıflandırmayı yapabilirim. Ana dizindeki .py dosyalarını okuduktan sonra amaçlarına göre sınıflandırıyorum:

# 📊 ANA DİZİN .PY DOSYALARI SINIFLANDIRMASI
## 🎯 1. ANA SİSTEM MOTOR DOSYALARI
* main.py (1,249 satır) - Ana başlatma ve modül yönetimi
* gui_manager.py (7,078 satır) - 4-panel GUI arayüzü
* configuration_manager.py (2,858 satır) - Sistem yapılandırması
* database_manager.py (521 satır) - Veritabanı yönetimi
## 🔧 2. DISASSEMBLER MOTOR SİSTEMİ (4 Motor)
* disassembler.py (124 satır) - "basic" motor - Basit ve güvenli
* advanced_disassembler.py (928 satır) - "advanced" motor - Gelişmiş özellikler
* improved_disassembler.py (1,428 satır) - "improved" motor - C64 Enhanced
* py65_professional_disassembler.py (935 satır) - "py65_professional" motor - py65 tabanlı
## 📀 3. DISK VE DOSYA OKUYUCULARI
* enhanced_d64_reader.py (1,069 satır) - Universal disk reader
* d64_reader.py (569 satır) - Standart D64 okuyucu
* c1541_python_emulator.py (342 satır) - C1541 emülatör
* data_loader.py - JSON veri yükleyici
## 🔄 4. TRANSPILER VE DECOMPILER SİSTEMİ
* unified_decompiler.py (431 satır) - Ana decompiler arayüzü
* enhanced_basic_decompiler.py (823 satır) - BASIC V2 to modern languages
* c64bas_transpiler_c_temel.py - Temel C transpiler
* c64bas_transpiler_qbasic.py - BASIC to QBasic transpiler
## 📊 5. PARSER VE ANALİZ SİSTEMLERİ
* hybrid_program_analyzer.py (906 satır) - BASIC+Assembly analiz
* code_analyzer.py (597 satır) - Gelişmiş pattern tanıma
* hybrid_disassembler.py - Hibrit disassembly
* c64_basic_parser.py (64 satır) - BASIC parser
* c64_basic_parser_new.py - Yeni BASIC parser
* parser.py - Genel parser
## 🧠 6. BELLEK VE OPCODE YÖNETİMİ
* enhanced_c64_memory_manager.py (250 satır) - C64 bellek yönetimi
* c64_memory_manager.py - Standart bellek yönetici
* memory_manager.py (182 satır) - Genel bellek optimizasyonu
* opcode_manager.py - Opcode yönetimi
* opcode_manager_simple.py - Basit opcode yönetimi
* opcode_generator.py - Opcode üretici
## 🎨 7. FORMAT VE ÇIKTI SİSTEMLERİ
* assembly_formatters.py (391 satır) - Assembly format sistemleri
* disassembly_formatter.py - Disassembly formatlayıcı
* assembly_parser_6502_opcodes.py (71 satır) - 6502 opcode parser
## 🔧 8. YARDİMCI VE DESTEK DOSYALARI
* basic_detokenizer.py (257 satır) - BASIC detokenizer
* petcat_detokenizer.py - PETCAT wrapper
* PETSCII2BASIC.py - PETSCII çevirici
* add_pseudo.py (52 satır) - Pseudo kod ekleyici
illegal_opcode_analyzer.py - Illegal opcode analizi
## 📦 9. ARAÇ VE UTILITY SİSTEMLERİ
* toolbox_manager.py - Araç kutusu yöneticisi
* tool_command_generator.py - Araç komutu üretici
* sprite.py / sprite_converter.py - Sprite işlemleri
* sid_converter.py - SID dosyası çevirici
* simple_analyzer.py - Basit analiz araçları
## 🔧 10. SİSTEM YÖNETİMİ VE BAKIM
* system_diagnostics.py - Sistem tanılama
* system_repair.py - Sistem onarımı
* ultimate_cleanup.py - Sistem temizleme
* final_project_status.py (40 satır) - Proje durumu
module_analyzer.py - Modül analizi
## 🧪 11. TEST VE GELİŞTİRME DOSYALARI
* create_test_files.py (62 satır) - Test dosyası oluşturucu
* test_*.py dosyaları (çoklu test dosyaları)
* quick_*.py dosyaları (hızlı test araçları)
## 🖥️ 12. GUI VE ARAYÜZ
* launch_page_gui.py (27 satır) - PAGE GUI başlatıcı
* launch_pygubu.py - PyGubu başlatıcı
* gui_*.py dosyaları (GUI destek dosyaları)
* d64_converter_main.py (336 satır) - Ana converter GUI
* d64_converter_gui_page.py - PAGE GUI implementasyonu
## 📝 13. LEGACY VE YEDEK DOSYALAR
* main_*.py dosyaları (main'in farklı versiyonları)
* gui_manager_copy.py - GUI yedek dosyası
* gui_manager_backup.py - GUI yedekleri
* enhanced_c64_memory_manager_*.py - Bellek yöneticisi versiyonları
* decompiler_*.py dosyaları (eski decompilerlar)
## 📈 GENEL DEĞERLENDİRME:

Toplam Ana Dizin .py Dosyası: ~80+ dosya

Aktif Kullanımdaki Ana Modüller:
```
* ✅ 4 Disassembler Motor Sistemi
* ✅ Universal Disk Reader
* ✅ GUI Manager (4-panel)
* ✅ Configuration Manager
* ✅ Enhanced BASIC Decompiler
* ✅ Hybrid Program Analyzer
```
Hazır Ama Entegre Edilmemiş:
```
* 🔄 Enhanced BASIC Decompiler
* 🔄 Code Analyzer (Pattern Recognition)
* 🔄 Assembly Formatters
* 🔄 Toolbox Manager
```
Test ve Geliştirme Aşamasında:

* 🧪 py65 Professional Disassembler
* 🧪 Sprite/SID Converters
* 🧪 Advanced Memory Manager

Bu sınıflandırma, D64 Converter v5.0'ın kapsamlı ve modüler yapısını gösteriyor. Sistem 13 farklı kategoride organize edilmiş, her kategorinin kendine özgü işlevleri var.