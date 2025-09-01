# 🎨 PyGubu Designer ile GUI Manager Düzenleme Rehberi

## 📋 1. PyGubu Designer Açma
1. PyGubu Designer'ı başlat: `C:/Users/dell/Documents/projeler/d64_converter/venv_pygubu/Scripts/pygubu-designer.exe`
2. Mevcut UI dosyasını aç: `gui_designs/d64_converter_main.ui`

## 🔧 2. Temel Düzenleme İşlemleri

### A) Widget Ekleme:
1. Sol panelden widget türünü seç (Button, Label, Frame, etc.)
2. Ana tasarım alanına sürükle
3. Sağ panelde özelliklerini düzenle

### B) Mevcut Widget'ları Düzenleme:
1. Widget'a tıkla
2. Sağ panelden özelliklerini değiştir:
   - **text**: Buton yazısı
   - **command**: Fonksiyon bağlantısı (kod tarafında)
   - **font**: Yazı tipi
   - **background/foreground**: Renkler
   - **width/height**: Boyutlar

### C) Layout Düzenleme:
1. Widget'ı seç
2. **Layout** sekmesinden yerleşim ayarları:
   - **manager**: pack, grid, place
   - **side**: left, right, top, bottom
   - **fill**: x, y, both
   - **expand**: true/false
   - **padx/pady**: Boşluklar

## 🎯 3. D64 Converter İçin Önemli Widget'lar

### Mevcut Widget ID'leri:
- `main_window`: Ana pencere
- `left_panel`: Sol panel (dosya listesi)
- `right_panel`: Sağ panel (çıktı alanı)
- `open_file_btn`: Dosya aç butonu
- `hybrid_analysis_btn`: Hibrit analiz butonu
- `disassemble_btn`: Disassemble butonu
- `transpile_btn`: Transpile butonu
- `format_combo`: Format seçimi
- `engine_combo`: Engine seçimi
- `target_lang_combo`: Hedef dil seçimi
- `file_tree`: Dosya listesi
- `disassembly_output`: Çıktı alanı

### Yeni Widget Ekleme:
1. Widget ekle ve ID ver (örn: `new_button`)
2. GUI Manager'da yeni widget'ı kaydet:

```python
# gui_manager.py'de _get_pygubu_widget_references() fonksiyonuna ekle:
'new_button', # Yeni widget ID'si
```

## 🚀 4. Pratik Düzenleme Örnekleri

### A) Buton Yerini Değiştirme:
1. PyGubu'da butonu seç
2. Layout → manager: pack
3. Layout → side: left/right/top/bottom
4. Layout → padx/pady: boşluk ayarla

### B) Buton Rengini Değiştirme:
1. Butonu seç
2. Widget → background: #4CAF50 (yeşil)
3. Widget → foreground: white

### C) Yeni Panel Ekleme:
1. Frame widget'ı ekle
2. ID ver: `new_panel`
3. İçine butonlar ekle
4. Layout ayarla

### D) Font Değiştirme:
1. Widget'ı seç
2. Widget → font: "Arial 12 bold"

## 💾 5. Değişiklikleri Kaydetme ve Test Etme

### Kaydetme:
1. PyGubu Designer'da: File → Save
2. UI dosyası otomatik güncellenir

### Test Etme:
```powershell
# Hızlı test
python quick_gui_test.py

# Tam test
python test_pygubu_integration.py
```

## 🎨 6. Önerilen İyileştirmeler

### A) Ana Butonları Yeniden Düzenle:
- Dosya işlemleri: Sol üst
- Analiz butonları: Orta
- Çıktı işlemleri: Sağ alt

### B) Renk Şeması:
- Ana butonlar: Yeşil (#4CAF50)
- İkincil butonlar: Mavi (#2196F3)
- Uyarı butonları: Turuncu (#FF9800)
- Tehlike butonları: Kırmızı (#F44336)

### C) İkon Ekleme:
- 📂 Dosya aç
- 🔧 Disassemble
- 🔄 Transpile
- 💾 Kaydet
- 🚀 Çalıştır

## ⚡ 7. Hızlı Düzeltmeler

### Problem: Buton görünmüyor
Çözüm: Layout → fill: x, expand: true

### Problem: Yazı çok küçük
Çözüm: Widget → font: "Arial 12"

### Problem: Buton çalışmıyor
Çözüm: ID'nin GUI Manager'da tanımlı olduğunu kontrol et

## 🎯 8. İdeal Layout Önerisi

```
┌─────────────────────────────────────────┐
│ [📂 Dosya Aç] [🔍 Analiz] [⚙️ Ayarlar]  │
├──────────────┬──────────────────────────┤
│              │ 🔧 Disassembly           │
│ 📁 Dosyalar  │ ┌─────────────────────┐  │
│ • game.prg   │ │                     │  │
│ • loader.prg │ │ Assembly Çıktısı    │  │
│ • music.sid  │ │                     │  │
│              │ └─────────────────────┘  │
│              │ [🚀 Disassemble]         │
│              │                          │
│              │ 🔄 Transpile             │
│              │ ┌─────────────────────┐  │
│              │ │                     │  │
│              │ │ C/Python Çıktısı    │  │
│              │ │                     │  │
│              │ └─────────────────────┘  │
│              │ [🔄 Transpile]           │
└──────────────┴──────────────────────────┘
│ 🚀 Ready     Progress: ████████░░ 80%   │
└─────────────────────────────────────────┘
```

## 🎉 Başlangıç İçin Öneriler:

1. **İlk**: Mevcut butonların yerini düzenle
2. **İkinci**: Renkleri değiştir
3. **Üçüncü**: Font boyutlarını ayarla
4. **Dördüncü**: Yeni butonlar ekle
5. **Beşinci**: Panel düzenlemesi yap
