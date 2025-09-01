# PAGE Visual Designer Kullanım Kılavuzu

## PAGE nedir?
PAGE (Python Automatic GUI Generator), Tkinter GUI'leri için visual designer'dır.

## Kurulum
```bash
# PAGE zaten kurulu, şu konumda:
C:/Users/dell/Documents/projeler/D64Gelıstırme/venv_asmto/page/page.py
```

## Kullanım Adımları

### 1. PAGE'i Başlatın
```bash
cd C:/Users/dell/Documents/projeler/D64Gelıstırme
python venv_asmto/page/page.py
```

### 2. Proje Dosyalarını Açın
PAGE başladıktan sonra:
- **File > Open** menüsünden Python dosyası seçin
- Test için: `page_test_gui.py`
- Ana proje için: `d64_converter_gui_page.py`

### 3. Visual Editing
- Sağ taraftaki widget palette'den widget'ları sürükleyin
- Properties panel'den özelliklerini düzenleyin
- Layout manager'ları kullanın (pack, grid, place)

### 4. Kod Üretimi
- PAGE otomatik olarak Python kodu üretir
- **Generate > Python Code** ile kodu görüntüleyin
- Değişiklikler otomatik kaydedilir

## D64 Converter için Önerilen Layout

### Ana Pencere Yapısı
```
┌─────────────────────────────────────────┐
│ Menu Bar + Toolbar                      │
├─────────────────┬───────────────────────┤
│ File Directory  │ Disassembly Results   │
│ (Listbox)       │ (ScrolledText)        │
├─────────────────┼───────────────────────┤
│ Console Output  │ Decompiler Results    │
│ (ScrolledText)  │ (ScrolledText)        │
├─────────────────┴───────────────────────┤
│ Status Bar + Progress                   │
└─────────────────────────────────────────┘
```

## Widget Önerileri

### 1. File Directory Panel (Sol Üst)
- **LabelFrame**: "📁 File Directory"
- **Listbox**: Dosya listesi
- **Scrollbar**: Kaydırma çubuğu
- **Frame**: Butonlar için
- **Button**: "Load D64", "Load PRG", "Find Files"

### 2. Disassembly Panel (Sağ Üst)
- **LabelFrame**: "⚙️ Disassembly Results"
- **ScrolledText**: Kod görüntüleme
- **Frame**: Format butonları
- **Button**: "Assembly", "C", "QBasic", "BASIC"

### 3. Console Panel (Sol Alt)
- **LabelFrame**: "💬 Console Output"
- **ScrolledText**: Log mesajları
- **Frame**: Kontrol butonları
- **Button**: "Clear"
- **Checkbutton**: "Auto-scroll"

### 4. Decompiler Panel (Sağ Alt)
- **LabelFrame**: "🔄 Decompiler Results"
- **ScrolledText**: Decompiler çıktısı
- **Frame**: Decompiler butonları
- **Button**: "C Decompiler", "C++", "QBasic"

## PAGE Dosyaları

### Mevcut Dosyalar
1. **page_test_gui.py** - Basit test GUI
2. **d64_converter_gui_page.py** - Ana D64 Converter GUI
3. **launch_page_gui.py** - GUI başlatıcı

### Test Etme
```bash
# Test GUI'yi çalıştır
python page_test_gui.py

# Ana GUI'yi çalıştır
python launch_page_gui.py

# Direct GUI
python d64_converter_gui_page.py
```

## PAGE ile Düzenleme

### Adım 1: PAGE Başlat
```bash
python venv_asmto/page/page.py
```

### Adım 2: Dosya Aç
- File > Open
- `page_test_gui.py` veya `d64_converter_gui_page.py` seçin

### Adım 3: Visual Düzenleme
- Widget palette'den widget ekleyin
- Properties ile özelliklerini değiştirin
- Layout'u düzenleyin

### Adım 4: Test Et
- Generate > Test ile test edin
- File > Save ile kaydedin

## Önemli Notlar

1. **Backup Dosyalar**: PAGE backup dosyası oluşturur (.bak)
2. **Kod Koruma**: Mevcut fonksiyonlar korunur
3. **Widget İsimleri**: Anlamlı isimler kullanın
4. **Layout**: Grid layout önerilir (responsive)
5. **Colors**: Dark theme için renk kodları mevcutta

## Hata Giderme

### PAGE Açılmıyor
```bash
# Python path kontrolü
python -c "import tkinter; print('Tkinter OK')"

# PAGE dosya kontrolü
ls venv_asmto/page/page.py
```

### Widget Görnmüyor
- Grid weights ayarlayın
- sticky="nsew" kullanın
- expand=True ekleyin

### Kod Kayboluyor
- Backup dosyalarını kontrol edin (.bak)
- Git commit'lerini kontrol edin

## Sonuç

PAGE ile D64 Converter GUI'yi visual olarak düzenleyebilirsiniz:
1. Widget'ları sürükle-bırak ile ekleyin
2. Properties ile renkler/boyutlar ayarlayın  
3. Layout'u grid ile düzenleyin
4. Test edin ve kaydedin

PAGE, Tkinter GUI'leri için mükemmel bir visual designer'dır!
