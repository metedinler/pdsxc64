# 🚀 PDSX PROGRAMLAMA DİLİ - KAPSAMLI ANALİZ RAPORU

## 📋 GENEL BAKIŞ

**PDSX**, projenin yazarı tarafından geliştirilen özel bir programlama dilidir. 10 gün önce transpiler geliştirirken karşılaşılan hatalar nedeniyle minimal bir format olarak oluşturulmuştur.

### 🎯 **PDSX VERSİYONLARI VE DOSYA YAPISI:**

1. **Ana Dizin:**
   - `pdsXv12.py` (611 satır) - Ultimate Professional Development System
   - `pdsXv12_minimal.py` (85 satır) - Minimal working version for d64_converter

2. **pdsX Klasörü:**
   - `pdsx_v10_manus.py` (1716 satır) - En kapsamlı versiyon
   - `pdsxv13xxmxx2.py` (2039 satır) - En gelişmiş versiyon, v13 
   - `pdsx chatgpt_grok_manus.py` (4164 satır) - ChatGPT+Grok işbirliği, EN BÜYÜK versiyon
   - `pdsv11.py` (2632 satır) - Versiyon 11, Grok tarafından yazıldı (27 Nisan 2025)
   - `pdsXv11c.py` - Versiyon 11c
   - `pdsXv11g.py` - Versiyon 11g
   - `pdsXv13u.py` - Versiyon 13u
   - `pdsX_v12chatgpt.py` - Versiyon 12 ChatGPT

### 🚀 **PDSX DOSYA BOYUTLARI VE GELİŞİM SÜRECİ**

#### **📊 Versiyon Karşılaştırması:**
1. **pdsXv12_minimal.py** (85 satır) - En minimal versiyon
2. **pdsXv12.py** (611 satır) - Temel sistem
3. **pdsx_v10_manus.py** (1716 satır) - İlk kapsamlı versiyon
4. **pdsxv13xxmxx2.py** (2039 satır) - v13 gelişmiş sistem
5. **pdsv11.py** (2632 satır) - Grok tarafından yazılan v11
6. **pdsx chatgpt_grok_manus.py** (4164 satır) - **EN KAPSAMLI**, ChatGPT+Grok işbirliği

#### **🎯 Geliştirici Katkıları:**
- **Mete Dinler (Proje Sahibi):** Temel konsept ve tasarım
- **ChatGPT:** Kodlama ve implementasyon
- **Grok:** v11 versiyonu (27 Nisan 2025) ve işbirliği versiyonu

#### **🔧 ChatGPT+Grok Versiyonu Özel Özellikleri (4164 satır):**
- **Gelişmiş Class Sistemi:** ClassInstance, field access control
- **Array İşlemleri:** ArrayInstance sınıfı ile güçlü dizi işlemleri
- **Enhanced Type System:** Daha güvenli tip kontrolü
- **Memory Management:** Gelişmiş hafıza yönetimi
- **Error Handling:** Kapsamlı hata yakalama sistemi

---

## 🔧 **PDSX v10 (1716 SATIR) - TEMEL SİSTEM**

### **🎪 TEMEL ÖZELLİKLER:**
- **Memory Manager** - Hafıza yönetimi ve pointer aritmetiği
- **Struct/Union/Pointer** sınıfları - Düşük seviye veri yapıları
- **Multi-paradigm** - Procedural, OOP, Functional programlama
- **Enhanced Function Table** - 100+ builtin fonksiyon
- **Data Science Integration** - NumPy, Pandas, SciPy desteği

### **📝 TEMEL KOMUTLAR:**

#### **VERİ TİPLERİ:**
```pdsx
DIM variable AS INTEGER
DIM name AS STRING
DIM score AS DOUBLE
DIM list_data AS LIST
DIM matrix AS ARRAY
DIM info AS DICT
```

#### **KONTROL YAPILARI:**
```pdsx
IF condition THEN statement
FOR variable = start TO end STEP increment
WHILE condition
DO WHILE condition
SELECT CASE expression
```

#### **ALT PROGRAMLAR:**
```pdsx
SUB SubroutineName(parameters)
FUNCTION FunctionName(parameters)
CALL SubroutineName
GOSUB LabelName
RETURN
```

#### **DOSYA İŞLEMLERİ:**
```pdsx
OPEN "filename" FOR INPUT AS #1
READ #1, variable
WRITE #1, data
CLOSE #1
```

### **🧮 MATEMATİKSEL FONKSİYONLAR:**
- **Temel:** `ABS`, `INT`, `SQR`, `SIN`, `COS`, `TAN`, `LOG`, `EXP`
- **Gelişmiş:** `SINH`, `COSH`, `TANH`, `ASINH`, `ACOSH`, `ATANH`
- **İstatistik:** `MEAN`, `MEDIAN`, `STD`, `VAR`, `PERCENTILE`
- **Linear Algebra:** `DOT`, `CROSS`, `NORM`, `INV`, `SOLVE`

### **📊 VERİ BİLİMİ FONKSİYONLARI:**
- **Pandas:** `DESCRIBE`, `GROUPBY`, `FILTER`, `SORT`, `MERGE`
- **NumPy:** `CONCATENATE`, `STACK`, `LINSPACE`, `ZEROS`, `ONES`
- **Statistics:** `TTEST`, `CHISQUARE`, `ANOVA`, `REGRESS`

### **📄 DOSYA OKUMA FONKSİYONLARI:**
- `PDF_READ_TEXT(filepath)` - PDF'den metin çıkarma
- `PDF_EXTRACT_TABLES(filepath)` - PDF'den tablo çıkarma
- `PDF_SEARCH_KEYWORD(filepath, keyword)` - PDF'de arama
- `TXT_SEARCH(filepath, keyword)` - Text dosyasında arama
- `WEB_GET(url)` - Web sayfası getirme
- `WEB_POST(url, data)` - POST request

---

## 🚀 **PDSX v13 (2039 SATIR) - EN GELİŞMİŞ SİSTEM**

### **🎪 YENİ ÖZELLİKLER:**

#### **🔧 GELIŞMIŞ VERİ TİPLERİ:**
```pdsx
DIM var AS FLOAT128        ' Çift hassasiyet float
DIM text AS STRING16       ' 16-bit string
DIM flag AS BOOLEAN        ' Boolean tip
DIM ptr AS POINTER TO INTEGER  ' Tip güvenli pointer
DIM value AS NULL          ' Null değer
DIM invalid AS NAN         ' Not-a-Number
```

#### **🏗️ YAPISAL PROGRAMLAMA:**
```pdsx
TYPE PersonStruct
    name AS STRING = "Unknown"
    age AS INTEGER = 0
    salary AS DOUBLE = 0.0
END TYPE

UNION DataUnion
    intValue AS INTEGER = 0
    floatValue AS SINGLE = 0.0
    stringValue AS STRING = ""
END UNION

ENUM StatusEnum
    PENDING = 1
    ACTIVE = 2
    DISABLED = 3
END ENUM
```

#### **🎯 NESNE YÖNELİMLİ PROGRAMLAMA:**
```pdsx
CLASS Animal EXTENDS Object
    PRIVATE name AS STRING
    STATIC count AS INTEGER = 0
    
    SUB Constructor(animalName AS STRING)
        name = animalName
        count = count + 1
    END SUB
    
    FUNCTION GetName() AS STRING
        RETURN name
    END FUNCTION
    
    PRIVATE SUB InternalMethod()
        ' Private metot
    END SUB
END CLASS

INTERFACE Drawable
    SUB Draw()
    FUNCTION GetSize() AS INTEGER
END INTERFACE

ABSTRACT CLASS Shape IMPLEMENTS Drawable
    ABSTRACT SUB CalculateArea()
END CLASS
```

#### **💾 VERİTABANI İŞLEMLERİ:**
```pdsx
OPEN DATABASE "mydatabase.db"
CREATE TABLE users (id INTEGER, name TEXT, email TEXT)
INSERT INTO users VALUES (1, 'John', 'john@email.com')
SELECT * FROM users WHERE id = 1
SQL RESULT TO ARRAY userArray
SQL RESULT TO DATAFRAME userDF
CLOSE DATABASE
```

#### **🔄 PİPELİNE SİSTEMİ:**
```pdsx
PIPE(
    "LOAD data.csv",
    "FILTER age > 25", 
    "GROUP BY department",
    "SAVE processed.csv"
) AS dataProcessing RETURN result
```

#### **⚡ ASYNC PROGRAMLAMA:**
```pdsx
ASYNC FUNCTION FetchData(url AS STRING)
    result = WEB_GET(url)
    RETURN result
END FUNCTION

task1 = ASYNC_CALL FetchData("http://api1.com")
task2 = ASYNC_CALL FetchData("http://api2.com")
AWAIT_ALL task1, task2
```

#### **🎮 OLAY YÖNETİMİ:**
```pdsx
ON SYSTEM EVENT timer_elapsed DO HandleTimer
ON SYSTEM EVENT file_changed DO HandleFileChange
ON SYSTEM EVENT mouse_clicked DO HandleClick
ON EVENT user.login WAIT DO ProcessLogin
ON INTERRUPT SIGINT DO GracefulShutdown
```

#### **🧮 PROLOG ENTEGRASYONU:**
```pdsx
FACT parent(tom, bob)
FACT parent(bob, ann)
RULE ancestor(X, Y) :- parent(X, Y)
RULE ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z)
QUERY ancestor(tom, ann)  ' Returns: Yes
```

#### **⚙️ ASSEMBLY ENTEGRASYOnu:**
```pdsx
ASM
    MOV AX, 1000
    ADD AX, 500
    MOV result, AX
END ASM
```

#### **🔧 DLL VE API YÖNETİMİ:**
```pdsx
dll = LOAD_DLL("user32.dll")
api = LOAD_API("https://api.openai.com/chat")
result = CALL API::GET "What is AI?"
```

### **📚 LİBX CORE FONKSİYONLARI:**

#### **🗂️ Koleksiyon İşlemleri:**
- `INSERT(collection, value, index, key)` - Eleman ekleme
- `REMOVE(collection, index, key)` - Eleman silme
- `POP(collection)` - Son eleman çıkarma
- `CLEAR(collection)` - Temizleme
- `SLICE(iterable, start, end)` - Parçalama
- `KEYS(dict)` - Anahtar listesi

#### **🕰️ Zaman ve Tarih:**
- `TIME_NOW()` - Şuanki zaman
- `DATE_NOW()` - Şuanki tarih
- `TIMER()` - Timestamp
- `DATE_DIFF(date1, date2, unit)` - Tarih farkı

#### **🎲 Random ve Matematik:**
- `RANDOM_INT(min, max)` - Rastgele tamsayı
- `FLOOR(x)`, `CEIL(x)` - Taban/tavan
- `ROUND(x, digits)` - Yuvarlama
- `MIN(iterable)`, `MAX(iterable)` - Min/Max

#### **📁 Dosya Sistemi:**
- `EXISTS(path)` - Dosya kontrolü
- `MKDIR(path)` - Klasör oluşturma
- `COPY_FILE(src, dst)` - Dosya kopyalama
- `MOVE_FILE(src, dst)` - Dosya taşıma
- `DELETE_FILE(path)` - Dosya silme
- `LIST_DIR(path)` - Klasör listeleme

#### **🌐 Ağ ve Web:**
- `PING(host)` - Ping atma
- `WEB_GET(url)` - HTTP GET
- `WEB_POST(url, data)` - HTTP POST

#### **🔧 Sistem İzleme:**
- `MEMORY_USAGE()` - Bellek kullanımı (MB)
- `CPU_COUNT()` - İşlemci çekirdek sayısı
- `SYSTEM(resource)` - Sistem kaynak bilgisi
  - `ram` - Kullanılabilir RAM
  - `cpu` - CPU kullanımı ve çekirdek sayısı
  - `gpu` - GPU bilgisi (pynvml gerekli)
  - `process` - Aktif işlem sayısı
  - `thread` - Aktif thread sayısı

#### **📦 Veri Yapıları:**
- `STACK()` - Yığın oluşturma
- `PUSH(stack_id, item)` - Yığına ekleme
- `POP(stack_id)` - Yığından çıkarma
- `QUEUE()` - Kuyruk oluşturma
- `ENQUEUE(queue_id, item)` - Kuyruğa ekleme
- `DEQUEUE(queue_id)` - Kuyruktan çıkarma

#### **🔄 Fonksiyonel Programlama:**
- `MAP(func, iterable)` - Haritalama
- `FILTER(func, iterable)` - Filtreleme
- `REDUCE(func, iterable, initial)` - İndirgeme
- `EACH(func, iterable)` - Her eleman için işlem
- `SELECT(func, iterable)` - Seçim

#### **🎭 Lambda Fonksiyonları:**
```pdsx
OMEGA(x, y, "x * y + 2")  ' Lambda fonksiyonu
FUNC x * x + 1            ' Kısa fonksiyon tanımı
GAMMA x, y, "x ** y"      ' Güçlü lambda
```

---

## 🎯 **PDSX KOMUT SETI TAM LİSTESİ**

### **📝 VERİ TANIMI VE ATAMA:**
- `DIM variable AS type [= value]` - Değişken tanımlama
- `LET variable = value` - Değer atama
- `GLOBAL variable AS type` - Global değişken
- `DIM SHARED scopes, variable AS type` - Paylaşımlı değişken
- `DEFINT`, `DEFSNG`, `DEFDBL`, `DEFSTR` - Varsayılan tipler

### **🔄 KONTROL AKIŞI:**
- `IF condition THEN statement [ELSE statement]` - Koşul
- `FOR variable = start TO end [STEP increment]` - Döngü
- `WHILE condition` / `WEND` - While döngüsü
- `DO [WHILE/UNTIL condition]` / `LOOP` - Do döngüsü
- `SELECT CASE expression` / `CASE value` / `END SELECT` - Switch
- `GOTO label` - Koşulsuz dallanma
- `GOSUB label` / `RETURN` - Alt program çağrısı
- `EXIT FOR`, `EXIT DO` - Döngüden çıkış
- `CONTINUE FOR`, `CONTINUE DO` - Döngü devamı

### **🏗️ YAPISAL PROGRAMLAMA:**
- `TYPE name` / `END TYPE` - Struct tanımı
- `UNION name` / `END UNION` - Union tanımı
- `ENUM name` / `END ENUM` - Enum tanımı
- `STRUCT name` / `END STRUCT` - Alternatif struct syntax

### **🎯 NESNE YÖNELİMLİ:**
- `CLASS name [EXTENDS parent]` / `END CLASS` - Sınıf tanımı
- `ABSTRACT CLASS name` - Soyut sınıf
- `INTERFACE name` / `END INTERFACE` - Arayüz
- `SUB name(params)` / `END SUB` - Metot tanımı
- `FUNCTION name(params)` / `END FUNCTION` - Fonksiyon
- `PRIVATE SUB/FUNCTION` - Özel metotlar
- `STATIC variable AS type` - Statik değişkenler
- `CALL object.method(params)` - Metot çağrısı
- `DESCRIBE classname` - Sınıf inceleme

### **📁 DOSYA İŞLEMLERİ:**
- `OPEN "file" FOR mode AS #num` - Dosya açma
- `CLOSE #num` - Dosya kapatma
- `PRINT #num, data` - Dosyaya yazma
- `WRITE #num, data` - Dosyaya yazma (quoted)
- `APPEND #num, data` - Dosyaya ekleme
- `INPUT #num, variable` - Dosyadan okuma
- `LINE INPUT #num, variable` - Satır okuma
- `READ #num, variable` - Veri okuma
- `SEEK #num, position` - Dosya konumu
- `GET #num, position, variable` - Binary okuma
- `PUT #num, position, data` - Binary yazma
- `LOCK #num` / `UNLOCK #num` - Dosya kilidi
- `KILL "filename"` - Dosya silme
- `NAME "old" AS "new"` - Dosya yeniden adlandırma
- `FILES "pattern"` - Dosya listesi
- `CHDIR "path"` - Klasör değiştirme
- `MKDIR "path"` - Klasör oluşturma
- `RMDIR "path"` - Klasör silme

### **💾 VERİTABANI:**
- `OPEN DATABASE "dbfile"` - Veritabanı açma
- `CREATE TABLE tablename (fields)` - Tablo oluşturma
- `INSERT INTO table VALUES (...)` - Veri ekleme
- `UPDATE table SET field=value WHERE condition` - Güncelleme
- `DELETE FROM table WHERE condition` - Silme
- `SELECT fields FROM table WHERE condition` - Sorgulama
- `SQL RESULT TO ARRAY variable` - Sonucu diziye çevirme
- `SQL RESULT TO STRUCT variable` - Sonucu struct'a çevirme
- `SQL RESULT TO DATAFRAME variable` - Sonucu DataFrame'e çevirme
- `CLOSE DATABASE` - Veritabanı kapatma
- `ET SQL AUTO ON/OFF` - Otomatik SQL modu

### **🎮 OLAY YÖNETİMİ:**
- `ON ERROR GOTO label` - Hata yönetimi
- `ON ERROR GOSUB label` - Hata alt programı
- `ON ERROR DO subname` - Hata handler
- `ON SYSTEM EVENT event DO handler` - Sistem olayları
- `ON EVENT event.name WAIT DO handler` - Olay bekleme
- `ON INTERRUPT signal DO handler` - Sinyal yakalama
- `RESUME` - Hata sonrası devam
- `RESUME NEXT` - Sonraki satıra devam
- `RESUME LABEL label` - Etikete devam

### **🧮 PROLOG VE LOGIC:**
- `FACT statement` - Gerçek ekleme
- `RULE head :- body` - Kural ekleme
- `QUERY goal` - Sorgu çalıştırma

### **⚡ ASYNC VE PARLELİZM:**
- `ASYNC FUNCTION name(params)` - Async fonksiyon
- `ASYNC_CALL function(params)` - Async çağrı
- `AWAIT task` - Task bekleme
- `AWAIT_ALL task1, task2, ...` - Tüm taskları bekleme

### **🔧 SİSTEM VE HATA AYIKLAMA:**
- `DEBUG ON/OFF` - Debug modu
- `TRACE ON/OFF` - İzleme modu
- `STEP DEBUG` - Adım adım debug
- `ASSERT condition` - Assertion
- `PERFORMANCE` - Performans bilgisi
- `SET LANGUAGE lang` - Dil ayarı
- `HELP [library]` - Yardım gösterme

### **📥 GİRDİ/ÇIKTI:**
- `PRINT expression [; expression ...]` - Yazdırma
- `INPUT ["prompt",] variable` - Girdi alma
- `LINE INPUT ["prompt",] variable` - Satır girdi
- `WRITE expression` - Quoted yazdırma
- `~ expr1; expr2; expr3` - Semicolon ile yazdırma
- `?? prompt` - Hızlı girdi (sonuç _input'a)

### **🗂️ MODÜL VE KÜTÜPHANE:**
- `IMPORT "filename" [AS name]` - Modül içe aktarma
- `COMPILE` - Bytecode'a derleme

### **🎭 ÖZE SYNTAX:**
- `:` - Tek satırda çoklu komut ayırıcı
- `/` - FOR ve IF komutlarında satır ayırıcı
- `FUNC expression` - Lambda fonksiyon (_func'a atanır)
- `GAMMA params, expression` - Gelişmiş lambda (_gamma'ya atanır)

### **🔧 BELLEk YÖNETİMİ:**
- `NEW(size)` - Bellek ayırma
- `DELETE(ptr)` - Bellek serbest bırakma
- `ADDR(variable)` - Adres alma
- `SIZEOF(object)` - Boyut hesaplama

---

## 📈 **PDSX KULLANIM ÖRNEKLERİ**

### **🎯 Basit Program:**
```pdsx
DIM name AS STRING
DIM age AS INTEGER

PRINT "Adınız: ";
INPUT name
PRINT "Yaşınız: ";
INPUT age

IF age >= 18 THEN
    PRINT name; " reşit"
ELSE
    PRINT name; " reşit değil"
END IF
```

### **🔄 Döngü Örneği:**
```pdsx
FOR i = 1 TO 10 STEP 2
    PRINT "Sayı: "; i
NEXT i

DIM counter AS INTEGER = 0
WHILE counter < 5
    PRINT "Counter: "; counter
    counter = counter + 1
WEND
```

### **🏗️ Struct Kullanımı:**
```pdsx
TYPE Point
    x AS DOUBLE = 0.0
    y AS DOUBLE = 0.0
END TYPE

DIM point1 AS Point
point1.x = 10.5
point1.y = 20.3
PRINT "Nokta: ("; point1.x; ","; point1.y; ")"
```

### **💾 Veritabanı Örneği:**
```pdsx
OPEN DATABASE "users.db"
CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, age INTEGER)
INSERT INTO users VALUES (1, 'Alice', 25)
INSERT INTO users VALUES (2, 'Bob', 30)
SELECT * FROM users WHERE age > 25
SQL RESULT TO ARRAY results
CLOSE DATABASE

FOR i = 0 TO LEN(results) - 1
    PRINT "User: "; results[i][1]; " Age: "; results[i][2]
NEXT i
```

---

## 🎯 **PDSX DEĞERLENDİRMESİ**

### **✅ GÜÇLÜ YANLAR:**
1. **Çok Paradigmalı:** Procedural, OOP, Functional, Logic programming
2. **Zengin Tip Sistemi:** NULL, NAN, custom types, generics
3. **Modern Özellikler:** Async/await, events, pipelines
4. **Data Science:** NumPy, Pandas, SciPy entegrasyonu
5. **Sistem Entegrasyonu:** DLL, API, Assembly, Database
6. **Kapsamlı Standart Kütüphane:** 200+ builtin fonksiyon

### **⚠️ ZAYIF YANLAR:**
1. **Karmaşık Syntax:** Çok fazla özellik, öğrenme eğrisi yüksek
2. **Performans:** Python tabanlı, native code değil
3. **Dokümantasyon:** Tam dokümantasyon eksik
4. **IDE Desteği:** Syntax highlighting ve intellisense yok
5. **Hata Mesajları:** Geliştirilebilir hata raporlama

### **📊 KULLANIM ALANLARI:**
- **Prototyping:** Hızlı prototip geliştirme
- **Data Science:** Veri analizi ve işleme
- **Automation:** Sistem otomasyonu
- **Educational:** Programlama öğretimi
- **Integration:** Farklı sistemleri birleştirme

---

## 🎭 **SONUÇ**

PDSX, **oldukça ambitious** bir programlama dili projesidir. Modern programlama dillerinin özelliklerini BASIC-benzeri syntax ile birleştirmeye çalışmaktadır. 

**En büyük değeri:** Çok farklı paradigmaları tek dil altında toplamış olması ve data science entegrasyonu.

**En büyük sorunu:** Karmaşık syntax ve eksik tooling desteği.

Bu dil, özellikle **rapid prototyping** ve **data science** projeleri için potansiyel taşımaktadır, ancak production kullanımı için daha fazla geliştirme ve dokümantasyon gereklidir.

Projenizde **unified_decompiler.py**'nin PDSX desteği vermesi mantıklıdır çünkü bu gerçekten çalışan bir dil implementasyonu vardır - sadece henüz tam olarak stabil değildir.
