# PDSX v12X - C64 GUI System Documentation

## Genel Bakış

PDSX v12X, Commodore 64 tarzı retro programlama dili yorumlayıcısıdır. Bu sistem, modern Windows ortamında C64 programlarını çalıştırmak için tasarlanmış, kapsamlı C64 emülasyonu ve GUI özelliklerine sahiptir.

## Ana Sistem Bileşenleri

### 1. Ana Yorumlayıcı (`pdsxv12xNEW.py`)
- **Sınıf**: `pdsXInterpreter` (8230+ satır)
- **Özellikler**: 
  - Gelişmiş memory management
  - Dynamic class sistemi (CLAZZ)
  - Multi-dimensional arrays
  - Struct/Union/Enum desteği
  - Pointer arithmetic
  - Prolog engine
  - Event-driven programming
  - Pipeline sistemi
  - Data science entegrasyonu
  - GUI development framework

### 2. C64 GUI Engine (`c64_gui_engine.py`)
- **Sınıf**: `UniversalC64Engine` (1177 satır)
- **Özellikler**:
  - VIC-II uyumlu sprite sistemi
  - Collision detection
  - Real-time 60 FPS rendering
  - Multi-format sprite/sound desteği
  - Modern komut sistemi

### 3. LibX GUI Framework (`libx_guiX.py`)
- **Sınıf**: `LibXGuiX` (Python 3.13+ uyumlu)
- **Özellikler**:
  - Modern widget management
  - Enhanced layout systems
  - Threading-safe operations
  - Drag & Drop desteği

## C64 Komut Sistemi

### 1. Ekran İnitialization Komutları

#### C64_INIT
```pdsx
C64_INIT [mode]
```
- **Amaç**: C64 ekranını başlatır
- **Parametreler**: 
  - `mode`: Grafik modu (0=text, 1=bitmap vb.)
- **Örnek**: `C64_INIT 0`

#### C64_CLEAR
```pdsx
C64_CLEAR [color]
```
- **Amaç**: Ekranı temizler
- **Parametreler**:
  - `color`: Renk kodu (0-15, varsayılan: 6=mavi)
- **Örnek**: `C64_CLEAR 6`

### 2. Pixel ve Karakter Komutları

#### C64_PIXEL
```pdsx
C64_PIXEL x, y, color
```
- **Amaç**: Belirtilen koordinata pixel çizer
- **Parametreler**:
  - `x, y`: Koordinatlar
  - `color`: Renk kodu (0-15)
- **Örnek**: `C64_PIXEL 50, 50, 1`

#### C64_CHAR
```pdsx
C64_CHAR x, y, char_code [, color]
```
- **Amaç**: Belirtilen pozisyona karakter çizer
- **Parametreler**:
  - `x, y`: Karakter pozisyonu
  - `char_code`: ASCII karakter kodu
  - `color`: Renk (varsayılan: 1=beyaz)
- **Örnek**: `C64_CHAR 10, 5, 65, 2`

### 3. Sprite Sistemi

#### SPRITE LOAD
```pdsx
SPRITE LOAD sprite_id, "filename.png"
```
- **Amaç**: PNG dosyasını sprite olarak yükler
- **Desteklenen Formatlar**: PNG, BMP
- **Örnek**: `SPRITE LOAD 0, "mario.png"`

#### SPRITE MOVE
```pdsx
SPRITE MOVE sprite_id, x, y
```
- **Amaç**: Sprite'ı hareket ettirir
- **Örnek**: `SPRITE MOVE 0, 100, 100`

#### SPRITE ENABLE/DISABLE
```pdsx
SPRITE ENABLE sprite_id
SPRITE DISABLE sprite_id
```
- **Amaç**: Sprite'ı aktif/deaktif yapar
- **Örnek**: `SPRITE ENABLE 0`

#### SPRITE COLOR
```pdsx
SPRITE COLOR sprite_id, color
```
- **Amaç**: Sprite rengini değiştirir
- **Örnek**: `SPRITE COLOR 0, 1`

#### SPRITE SCALE
```pdsx
SPRITE SCALE sprite_id, width_factor, height_factor
```
- **Amaç**: Sprite boyutunu değiştirir
- **Örnek**: `SPRITE SCALE 0, 2.0, 1.5`

#### SPRITE ROTATE
```pdsx
SPRITE ROTATE sprite_id, angle
```
- **Amaç**: Sprite'ı döndürür
- **Örnek**: `SPRITE ROTATE 0, 45`

#### SPRITE EXPAND_X/EXPAND_Y
```pdsx
SPRITE EXPAND_X sprite_id, TRUE/FALSE
SPRITE EXPAND_Y sprite_id, TRUE/FALSE
```
- **Amaç**: VIC-II double width/height emülasyonu
- **Örnek**: `SPRITE EXPAND_X 0, TRUE`

#### SPRITE MULTICOLOR
```pdsx
SPRITE MULTICOLOR sprite_id, TRUE/FALSE
```
- **Amaç**: Multicolor modunu aktif/deaktif yapar
- **Örnek**: `SPRITE MULTICOLOR 0, TRUE`

#### SPRITE CREATE
```pdsx
SPRITE CREATE sprite_id, width, height, color
```
- **Amaç**: Programatik sprite oluşturur
- **Örnek**: `SPRITE CREATE 1, 24, 21, 14`

### 4. Memory Operasyonları

#### POKE #memory operasyonlari icin gereke bilir
```pdsx
POKE address, value
```
- **Amaç**: Memory adresine değer yazar
- **C64 Adresleri**: 
  - 53280 ($D020): Border color
  - 53281 ($D021): Background color
- **Örnek**: `POKE 53280, 1`

#### PEEK  #memory operasyonlari icin kullanilabilir
```pdsx
value = PEEK(address)
```
- **Amaç**: Memory adresinden değer okur
- **Örnek**: `border_color = PEEK(53280)`
#### MEMSET
```pdsx

MEMSET address, value, length
``` 
- **Amaç**: Memory bölgesini belirli bir değerle doldurur
- **Parametreler**:   
  - `address`: Başlangıç adresi
  - `value`: Doldurulacak değer
  - `length`: Uzunluk (byte cinsinden)
#### MEMCPY
```pdsx
MEMCPY dest_address, src_address, length
```
- **Amaç**: Memory bölgesini kopyalar
- **Parametreler**:
  - `dest_address`: Hedef adres
  - `src_address`: Kaynak adres
  - `length`: Kopyalanacak uzunluk (byte cinsinden)
- **Örnek**: `MEMCPY 1000, 2000, 256` 
#### MEMCMP
```pdsx
MEMCMP address1, address2, length
```
- **Amaç**: İki bellek bölgesini karşılaştırır
- **Parametreler**:
  - `address1`: İlk adres
  - `address2`: İkinci adres
  - `length`: Karşılaştırılacak uzunluk (byte cinsinden)
- **Örnek**: `result = MEMCMP(1000, 2000, 256)` 

### 5. SID Audio Sistemi

#### SID LOAD
```pdsx
SID LOAD "filename.mp3"
```
- **Amaç**: Müzik dosyası yükler
- **Desteklenen Formatlar**: MP3, WAV, SID
- **Örnek**: `SID LOAD "music.mp3"`

#### SID PLAY
```pdsx
SID PLAY [loops]
```
- **Amaç**: Müziği çalar
- **Parametreler**:
  - `loops`: Tekrar sayısı (-1=sonsuz)
- **Örnek**: `SID PLAY -1`

#### SID STOP/PAUSE/RESUME
```pdsx
SID STOP
SID PAUSE
SID RESUME
```
- **Amaç**: Müzik kontrolü
- **Örnek**: `SID STOP`

#### SID VOLUME
```pdsx
SID VOLUME level
```
- **Amaç**: Ses seviyesi ayarı
- **Parametreler**:
  - `level`: 0.0-1.0 arası
- **Örnek**: `SID VOLUME 0.5`

### 6. Screen Operasyonları

#### SCREEN BACKGROUND
```pdsx
SCREEN BACKGROUND color
```
- **Amaç**: Arka plan rengini ayarlar
- **Örnek**: `SCREEN BACKGROUND 6`

#### SCREEN BORDER
```pdsx
SCREEN BORDER color
```
- **Amaç**: Kenar rengini ayarlar
- **Örnek**: `SCREEN BORDER 14`

#### SCREEN PIXEL
```pdsx
SCREEN PIXEL x, y, color
```
- **Amaç**: Screen buffer'a pixel çizer
- **Örnek**: `SCREEN PIXEL 50, 50, 1`

### 7. Charset Sistemi

#### CHARSET LOAD
```pdsx
CHARSET LOAD charset_id, "folder_path"
```
- **Amaç**: Karakter seti yükler
- **Örnek**: `CHARSET LOAD 1, "c64_charset"`

#### CHARSET SET
```pdsx
CHARSET SET charset_id
```
- **Amaç**: Aktif karakter setini değiştirir
- **Örnek**: `CHARSET SET 1`

## LibX GUI Komutları

### Window Yönetimi

#### GUI_WINDOW_CREATE
```pdsx
GUI_WINDOW_CREATE "window_name", width, height, "title"
```
- **Amaç**: Pencere oluşturur
- **Örnek**: `GUI_WINDOW_CREATE "main", 800, 600, "PDSX App"`

#### GUI_WINDOW_SHOW/HIDE
```pdsx
GUI_WINDOW_SHOW "window_name"
GUI_WINDOW_HIDE "window_name"
```
- **Amaç**: Pencere görünürlüğü
- **Örnek**: `GUI_WINDOW_SHOW "main"`

### Widget'lar

#### GUI_BUTTON_ADD
```pdsx
GUI_BUTTON_ADD "window", "button_name", "text", x, y, width, height
```
- **Amaç**: Düğme ekler
- **Örnek**: `GUI_BUTTON_ADD "main", "btn1", "Click Me", 10, 10, 100, 30`

#### GUI_LABEL_ADD
```pdsx
GUI_LABEL_ADD "window", "label_name", "text", x, y
```
- **Amaç**: Etiket ekler
- **Örnek**: `GUI_LABEL_ADD "main", "lbl1", "Hello", 10, 50`

#### GUI_ENTRY_ADD
```pdsx
GUI_ENTRY_ADD "window", "entry_name", x, y, width, height
```
- **Amaç**: Giriş alanı ekler
- **Örnek**: `GUI_ENTRY_ADD "main", "txt1", 10, 100, 200, 25`

## C64 Renk Paleti

```
0:  Siyah (#000000)      8:  Turuncu (#DD8855)
1:  Beyaz (#FFFFFF)      9:  Kahverengi (#664400)
2:  Kırmızı (#880000)    10: Açık Kırmızı (#FF7777)
3:  Cyan (#AAFFEE)       11: Koyu Gri (#333333)
4:  Mor (#CC44CC)        12: Gri (#777777)
5:  Yeşil (#00CC55)      13: Açık Yeşil (#AAFF66)
6:  Mavi (#0000AA)       14: Açık Mavi (#0088FF)
7:  Sarı (#EEEE77)       15: Açık Gri (#BBBBBB)
```

## VIC-II Register Emülasyonu

### Memory Map
- `$D000-$D00F`: Sprite X/Y koordinatları
- `$D015`: Sprite enable register
- `$D020`: Border color
- `$D021`: Background color
- `$D027-$D02E`: Sprite colors

## Collision Detection

### Bounding Box
```pdsx
SPRITE COLLISION_TYPE sprite_id, "BOUNDING_BOX"
```

### Pixel Perfect
```pdsx
SPRITE COLLISION_TYPE sprite_id, "PIXEL_PERFECT"
```

## Event Sistemi

### Collision Events
```pdsx
EVENT collision_handler SPRITE_COLLISION 0, 1
    PRINT "Sprite 0 and 1 collided!"
END EVENT
```

## Kod Örnekleri

### Basit Sprite Demo
```pdsx
REM PDSX C64 Sprite Demo
C64_INIT 0
C64_CLEAR 6
SPRITE LOAD 0, "mario.png"
SPRITE MOVE 0, 100, 100
SPRITE ENABLE 0
SLEEP 1000
```

### Animasyon Örneği
```pdsx
REM Sprite Animation
FOR frame = 1 TO 100
    sprite_x = 50 + frame * 2
    sprite_y = 50 + SIN(frame * 0.1) * 20
    SPRITE MOVE 0, sprite_x, sprite_y
    SLEEP 50
NEXT frame
```

### GUI Entegrasyonu
```pdsx
REM C64 + Modern GUI
GUI_WINDOW_CREATE "c64win", 640, 480, "C64 Emulator"
C64_INIT 0
C64_CLEAR 6
SPRITE LOAD 0, "character.png"
GUI_WINDOW_SHOW "c64win"
```

## Test Sonuçlarından Tespit Edilen Hatalar

### 1. Unicode Encoding Hataları
- **Problem**: `'charmap' codec can't encode character '\U0001f539'`
- **Çözüm**: UTF-8 encoding kontrolü

### 2. Eksik Metodlar
- **Problem**: `'pdsXInterpreter' object has no attribute '_execute_libx_gui_operations'`
- **Durum**: Metod var ama sınıf dışında tanımlı

### 3. C64 Engine Metodları
- **Problem**: `UniversalC64Engine.initialize() takes 1 positional argument but 2 were given`
- **Çözüm**: API uyumluluğu kontrolü

### 4. Expression Parser Hataları
- **Problem**: `invalid syntax` hataları
- **Çözüm**: Comment parsing düzeltilmeli

## Sistem Gereksinimleri

### Python Kütüphaneleri
- Python 3.13+
- pygame (C64 graphics)
- tkinter (GUI)
- PIL/Pillow (image processing)
- numpy (matematik)
- pandas (data science)
- scipy (bilimsel hesaplama)

### Sistem Özellikleri
- Windows 10/11
- 4GB+ RAM
- DirectX uyumlu grafik kartı
- Ses kartı (SID emülasyonu)

Bu sistem, modern Windows ortamında authentic C64 programlama deneyimi sunmak için tasarlanmıştır. Transpiler ve decompiler araçları ile birlikte kullanıldığında, orijinal C64 programlarını Windows'ta çalıştırabilir.
