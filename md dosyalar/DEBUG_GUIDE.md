# 🍎 Advanced Disassembler + GUI Debug Guide v5.4

## 🚀 Component Reference Codes

Artık her component'e kısa kodla referans verebilirsiniz!

### 📋 Ana Componentler (Disassembler)
| Kod | Component | Açıklama |
|-----|-----------|----------|
| **D1** | AdvancedDisassembler | Ana sınıf |
| **D2** | disassemble_simple() | Basit disassembly (dış kullanım) |
| **D3** | disassemble_py65() | py65 disassembly (dış kullanım) |
| **D4** | disassemble() | Format seçimli ana disassembly |

### 🎯 Format-Specific Disassemblers
| Kod | Component | Format |
|-----|-----------|--------|
| **D5** | _disassemble_asm() | Native Assembly |
| **D6** | _disassemble_tass() | TASS |
| **D7** | _disassemble_kickassembler() | KickAssembler |
| **D8** | _disassemble_cc64() | CC64 |

### 🔧 İç Disassemblers
| Kod | Component | Açıklama |
|-----|-----------|----------|
| **D9** | _disassemble_simple() | İç basit disassembly |
| **D10** | _disassemble_py65() | İç py65 disassembly |

### 🌍 Translation System
| Kod | Component | Hedef |
|-----|-----------|-------|
| **D11** | translate_instruction() | Çeviri motoru |
| **D16** | to_c() | C çevirisi |
| **D17** | to_qbasic() | QBasic çevirisi |
| **D18** | to_pdsx() | PDSX çevirisi |
| **D19** | to_commodore_basic_v2() | CBM Basic çevirisi |
| **D20** | to_pseudo() | Pseudo-code çevirisi |

### 🗺️ Memory Management
| Kod | Component | Açıklama |
|-----|-----------|----------|
| **D12** | load_memory_map() | Memory map yükleyici |
| **D13** | get_memory_info() | Memory bilgi alıcı |
| **D14** | get_memory_label() | Memory label alıcı |
| **D15** | convert_to_language() | Dil çevirici |

## 🎨 GUI Debug System (YENİ!)

### 🍎 GUI Component Codes
| Kod | Component | Açıklama |
|-----|-----------|----------|
| **G1-G99** | GUI Elementleri | Butonlar, Frame'ler, Label'lar |
| **G100+** | Windows/Dialogs | Pencereler, Message box'lar |

### 📱 GUI Debug Features
- **Otomatik kod atama**: Her GUI öğesine otomatik G1, G2, G3... kodları
- **Debug mode toggle**: GUI debug modunu açma/kapama
- **Component registry**: Tüm GUI componentlerinin listesi
- **Debug wrapper functions**: Özel debug-enabled GUI fonksiyonları

### 🎯 GUI Debug Commands
```python
# GUI Debug kontrolü
gui_debug.enable_debug()      # GUI debug modunu aç
gui_debug.disable_debug()     # GUI debug modunu kapat  
gui_debug.toggle_debug()      # Toggle
gui_debug.show_registry()     # Component listesini göster

# GUI Debug wrapper functions
debug_button(parent, "Kapat", command=close_window)  # → "G1-Kapat"
debug_label(parent, "Başlık")                       # → "G2-Başlık"  
debug_frame(parent, "Ana Frame")                    # → "G3-Ana Frame"
debug_messagebox("info", "Başarı", "İşlem tamam")   # → "G4-Başarı", "G5-İşlem tamam"
```
| Kod | Component | Açıklama |
|-----|-----------|----------|
| **D12** | load_memory_map() | Memory map yükleyici |
| **D13** | get_memory_info() | Memory bilgi alıcı |
| **D14** | get_memory_label() | Memory label alıcı |
| **D15** | convert_to_language() | Dil çevirici |

## 🛠️ Debug Commands

### Temel Debug
```python
advanced = AdvancedDisassembler(0xC000, code)

# Debug info göster
advanced.debug_info()

# Debug mode toggle
advanced.debug_toggle()       # Aç/kapat
advanced.debug_toggle(True)   # Aç
advanced.debug_toggle(False)  # Kapat
```

### Test Commands
```python
# Opcode test
advanced.debug_test_opcodes(10)  # İlk 10 opcode

# Memory map sample
advanced.debug_memory_map_sample(5)  # İlk 5 entry

# Translation test
advanced.test_translation("LDA", "c")     # LDA -> C
advanced.test_translation("STA", "qbasic") # STA -> QBasic
```

## 💬 İletişim Örnekleri

Artık böyle söyleyebilirsiniz:

**Disassembler Componentleri:**
- **"D5'te problem var"** → Native Assembly disassembler'da sorun
- **"D11 çalışmıyor"** → Translation engine sorunu  
- **"D12 yüklemiyor"** → Memory map loading problemi
- **"D16'ya bak"** → C translation'a bakılsın
- **"D4'ü test et"** → Ana disassemble fonksiyonunu test et

**GUI Componentleri (YENİ!):**
- **"G5'te sorun var"** → 5. GUI component'te (buton/label/frame) problem
- **"G12 tıklanmıyor"** → 12. GUI elementine tıklama sorunu
- **"G108 açılmıyor"** → 108. pencere/dialog açılma problemi  
- **"GUI debug aç"** → Tools → GUI Debug → Enable GUI Debug
- **"Component registry göster"** → Tools → GUI Debug → Show Component Registry

## 🎯 Debug Output Formatları

Her component kendine özel debug çıktısı verir:

**Disassembler Debug:**
```
[D1] Start Address: $C000        ← Constructor info
[D4] 🚀 Format seçimli disassemble ← Main disassemble
[D5] 🎯 Native Assembly disassemble ← Format specific
[D11] 🔄 Çeviri: LDA -> c        ← Translation
[D12] ✅ Memory map yüklendi      ← Memory operations
[DEBUG] Debug mode: AÇIK         ← Debug controls
```

**GUI Debug (YENİ!):**
```
[GUI-DEBUG] 🟢 GUI Debug Mode AÇIK    ← GUI debug status
[G1] BUTTON created: 📂 Seç           ← Button creation
[G2] FRAME created: Directory Header   ← Frame creation
[G5] MESSAGEBOX displayed: Başarı      ← MessageBox display
[G12] BUTTON clicked: Kaydet          ← Button interaction
```

## 🚀 Hızlı Test

**Disassembler Test:**
```bash
python advanced_disassembler.py
```

**GUI Debug Test:**
1. GUI'yi başlat: `python main.py`
2. Menu: `Tools → GUI Debug → Enable GUI Debug`
3. Menu: `Tools → GUI Debug → Test Debug Components`
4. Butonları test et ve console'da [G1], [G2] kodlarını izle

Bu komutlar tüm componentleri test eder ve durumlarını gösterir!

## 🔧 Menu Yerleşimi

**GUI Debug Menu Location:**
```
Main Menu → Tools → 🍎 GUI Debug
├── 🟢 Enable GUI Debug
├── 🔴 Disable GUI Debug  
├── 🔄 Toggle GUI Debug
├── ──────────────────
├── 📋 Show Component Registry
└── 🎯 Test Debug Components
```

---
🍎 **KızılElma Development Studio** - Advanced Disassembler v5.4 + GUI Debug System
