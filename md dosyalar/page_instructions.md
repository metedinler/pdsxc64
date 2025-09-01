# PAGE ile D64 Converter Projesi

## 🎯 PAGE Projesi Oluşturma Adımları

### 1. PAGE Designer'ı Başlat
```cmd
cd venv_asmto/page
python page.py
```

### 2. Yeni Proje Oluştur
- File → New
- Proje adı: `d64_converter_gui`
- Dosya türü: `.tcl` seçin

### 3. GUI Elemanlarını Ekle

#### Ana Pencere Ayarları:
- Title: "D64 Converter v5.0"
- Size: 1200x800
- Background: #2b2b2b

#### Panel Yapısı (4 Bölüm):

**1. Sol Üst - Directory Panel:**
- Widget: LabelFrame
- Text: "📂 Dizin İçeriği" 
- Position: place(x=10, y=50, width=590, height=350)
- İçinde: Listbox + Scrollbar

**2. Sağ Üst - Disassembly Panel:**
- Widget: LabelFrame  
- Text: "⚙️ Disassembly"
- Position: place(x=610, y=50, width=580, height=350)
- İçinde: Button Frame + Text Widget

**3. Sol Alt - Console Panel:**
- Widget: LabelFrame
- Text: "📟 Console"
- Position: place(x=10, y=410, width=590, height=350)
- İçinde: Text Widget (read-only)

**4. Sağ Alt - Decompiler Panel:**
- Widget: LabelFrame
- Text: "🔄 Decompiler" 
- Position: place(x=610, y=410, width=580, height=350)
- İçinde: Button Frame + Text Widget

### 4. Menü Çubuğu Ekle
- Dosya → Aç, Çıkış
- Araçlar → Format Dönüştürücüleri

### 5. Python Kod Üret
- Generate → Python Support Module
- Dosya adı: `d64_converter_gui_support.py`

### 6. Tamamlanan Dosyalar:
- ✅ `d64_converter_gui.tcl` (PAGE tarafından oluşturulan)
- ✅ `d64_converter_gui_support.py` (PAGE tarafından oluşturulan)
- ✅ `d64_converter_main.py` (zaten mevcut)

## 🚀 Çalıştırma

### Doğrudan Python GUI:
```cmd
python d64_converter_main.py
```

### PAGE Designer ile düzenleme:
```cmd
cd venv_asmto/page
python page.py
File → Open → d64_converter_gui.tcl
```

## 💡 PAGE Workflow

1. **Tasarım**: PAGE ile görsel tasarım
2. **Kod Üretimi**: PAGE → Generate Python
3. **Fonksiyon Ekleme**: Support dosyasına logic ekle
4. **Test**: Python ile çalıştır
5. **Düzenleme**: PAGE'e geri dön, cycle devam eder

Bu şekilde PAGE'in doğru workflow'u ile çalışmış olursunuz!
