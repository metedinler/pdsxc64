# D64 Converter - Gelişim Planı

## 🎯 MEVCUT DURUM ANALİZİ (17 Temmuz 2025)

### ✅ TAMAMLANAN BAŞARI KRİTERLERİ:
1. **Sistem Tamamen Fonksiyonel**: Tüm kritik hatalar çözüldü
2. **4 Disassembler Aktif**: basic, advanced, improved, py65_professional 
3. **py65 Import Conflict Çözüldü**: PY65_AVAILABLE=True her iki modülde de
4. **Sprite Converter Fixed**: Null byte corruption çözüldü  
5. **File Organization Complete**: Pasif dosyalar utilities_files/pasif/ altında
6. **15+ Argparse Parameters**: CLI interface tam gelişmiş
7. **6 Output Formats**: asm, c, qbasic, pdsx, pseudo, commodorebasicv2
8. **Illegal Opcode Support**: 100 undocumented opcodes detected
9. **C64 Memory Manager**: ROM routine detection, KERNAL calls
10. **GUI Import Chain Working**: d64_converter başarıyla loads all dependencies

---

## 🚀 GELİŞTİRİLECEK ÖNCELİKLER

### **Priority 1: GUI Enhancements (Immediate)**

#### 1.1 Disassembler Selection Interface
```python
# d64_converter.py içinde eklenecek
self.disassembler_var = tk.StringVar(value="improved")
disassembler_frame = ttk.LabelFrame(settings_frame, text="Disassembler Selection")

# Radio button options
disassembler_options = [
    ("Basic", "basic", "Basit disassembler (99 satır)"),
    ("Advanced", "advanced", "Gelişmiş disassembler + py65 fix (500 satır)"), 
    ("Improved", "improved", "En gelişmiş disassembler + 6 format (1206 satır)"),
    ("Professional", "py65_professional", "Profesyonel py65 wrapper (756 satır)")
]

for text, value, description in disassembler_options:
    rb = ttk.Radiobutton(disassembler_frame, text=f"{text} - {description}", 
                        variable=self.disassembler_var, value=value)
```

#### 1.2 Enhanced Checkbox System
```python
# Illegal opcode detection checkbox - zaten var, geliştirilecek
self.use_illegal_opcodes = tk.BooleanVar(value=False)
illegal_cb = ttk.Checkbutton(settings_frame, text="Illegal Opcode Detection", 
                            variable=self.use_illegal_opcodes)

# Yeni eklenecekler:
self.memory_analysis = tk.BooleanVar(value=True)
self.save_intermediate = tk.BooleanVar(value=False) 
self.auto_format_dirs = tk.BooleanVar(value=True)
```

#### 1.3 Recent Files History
```python
# Son açılan dosyaları kaydet/yükle
self.recent_files = []
self.load_recent_files()

def add_recent_file(self, filepath):
    if filepath in self.recent_files:
        self.recent_files.remove(filepath)
    self.recent_files.insert(0, filepath)
    self.recent_files = self.recent_files[:10]  # Son 10 dosya
    self.save_recent_files()
    self.update_recent_menu()
```

### **Priority 2: Format Directory System (High)**

#### 2.1 Auto Format Directory Creation
```bash
format_files/
├── asm_files/
│   ├── basic/           # basic disassembler çıktıları
│   ├── advanced/        # advanced disassembler çıktıları  
│   ├── improved/        # improved disassembler çıktıları
│   └── py65_professional/
├── c_files/
│   ├── improved/        # ImprovedDisassembler C outputs
│   └── decompiler/      # decompiler_c.py outputs
├── qbasic_files/
├── pdsx_files/
├── pseudo_files/
├── commodorebasic_files/
└── logs/
    ├── conversion_history.xlsx  # Excel tablosu
    └── operation_log.txt
```

#### 2.2 File Naming Convention
```python
# Format: diskimaji__program_adi.uzanti
def generate_output_filename(self, source_file, program_name, format_type, disassembler):
    disk_name = Path(source_file).stem  # test.d64 -> test
    safe_program = re.sub(r'[^\w\-_]', '_', program_name)
    return f"{disk_name}__{safe_program}.{format_type}"
    # Örnek: test__spaceinvaders.c, test__jumpman.asm
```

### **Priority 3: Operation History & Logging (Medium)**

#### 3.1 Excel Operations Log
```python
import pandas as pd

class OperationLogger:
    def __init__(self):
        self.log_file = "logs/conversion_history.xlsx"
        self.operations = []
    
    def log_conversion(self, source_file, program_name, format_type, 
                      disassembler, success, file_size, duration):
        operation = {
            'timestamp': datetime.now(),
            'source_file': source_file,
            'program_name': program_name,
            'format': format_type,
            'disassembler': disassembler,
            'success': success,
            'output_size': file_size,
            'duration_ms': duration,
            'illegal_opcodes_found': self.illegal_count
        }
        self.operations.append(operation)
        self.save_to_excel()
```

### **Priority 4: Advanced GUI Features (Medium)**

#### 4.1 File Search Dialog
```python
def open_file_search_dialog(self):
    search_window = tk.Toplevel(self.root)
    search_window.title("Find C64 Files")
    search_window.geometry("800x600")
    
    # Search criteria
    file_types = ["*.d64", "*.d71", "*.d81", "*.prg", "*.t64"]
    search_paths = ["C:\\", "D:\\", os.path.expanduser("~")]
    
    # Results table with preview
    results_tree = ttk.Treeview(search_window, columns=('path', 'size', 'modified'))
```

#### 4.2 Tab-based Save System  
```python
def save_active_tab(self):
    """Aktif sekmeyi kaydet - zaten var, geliştirilecek"""
    current_tab = self.output_notebook.select()
    tab_text = self.output_notebook.tab(current_tab, "text")
    
    # Format directory'sine kaydet
    format_name = tab_text.lower()
    disassembler = self.disassembler_var.get()
    output_dir = f"format_files/{format_name}_files/{disassembler}/"
    os.makedirs(output_dir, exist_ok=True)
```

---

## 🔧 TEKNİK DETAYLAR

### GUI Enhancement Code Integration
```python
# d64_converter.py içine eklenecek metodlar:

def setup_enhanced_settings_frame(self):
    """Gelişmiş ayarlar paneli"""
    settings_frame = ttk.LabelFrame(self.main_frame, text="Conversion Settings")
    
    # Disassembler selection
    self.setup_disassembler_selection(settings_frame)
    
    # Advanced options
    self.setup_advanced_options(settings_frame)
    
    # Recent files menu
    self.setup_recent_files_menu()

def integrate_format_directories(self):
    """Format directory sistemini entegre et"""
    self.format_dirs = {
        'asm': 'asm_files',
        'c': 'c_files', 
        'qbasic': 'qbasic_files',
        'pdsx': 'pdsx_files',
        'pseudo': 'pseudo_files',
        'commodorebasicv2': 'commodorebasic_files'
    }
    
    for format_type, dir_name in self.format_dirs.items():
        for disassembler in ['basic', 'advanced', 'improved', 'py65_professional']:
            os.makedirs(f"format_files/{dir_name}/{disassembler}/", exist_ok=True)
```

### Operation History Integration
```python
# main.py argparse'a eklenecek
parser.add_argument('--save-history', action='store_true', 
                   help='Excel tablosuna işlem geçmişi kaydet')
parser.add_argument('--history-file', default='logs/conversion_history.xlsx',
                   help='İşlem geçmişi Excel dosyası')
```

---

## 📈 BAŞARI KRİTERLERİ

### Phase 1 (Immediate - 1-2 gün):
- [ ] Disassembler selection radio buttons implemented
- [ ] Enhanced illegal opcode checkbox with status display  
- [ ] Recent files menu working
- [ ] Basic format directory auto-creation

### Phase 2 (High Priority - 3-5 gün):
- [ ] Complete format directory system with subfolders
- [ ] File naming convention: diskimaji__program.ext
- [ ] Tab-based save system with format awareness
- [ ] Operation logging to Excel table

### Phase 3 (Medium Priority - 1 hafta):
- [ ] File search dialog with preview
- [ ] Advanced checkbox options (memory analysis, auto-format dirs)
- [ ] Conversion history viewer in GUI
- [ ] Performance metrics display

---

## 🎯 NEXT IMMEDIATE ACTIONS

1. **GUI Enhancement Start**: Disassembler selection interface implementation
2. **Format Directory Setup**: Auto-creation with disassembler subfolders
3. **Recent Files System**: Load/save/display recent file history
4. **Excel Logging**: Operations history with timestamps and metrics

**Ready to proceed with Priority 1 implementations!**
