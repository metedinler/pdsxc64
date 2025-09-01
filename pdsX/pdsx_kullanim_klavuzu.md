# PDSX v12X Kullanım Kılavuzu

## Genel Bakış

PDSX v12X, güçlü ve çok yönlü bir programlama dili yorumlayıcısıdır. Modern programlama özelliklerini klasik BASIC sözdizimi ile birleştirerek, hem başlangıç hem de ileri düzey programcılar için ideal bir ortam sunar.

### Ana Özellikler

- **Güçlü Matematiksel İşlemler**: 200+ matematiksel fonksiyon
- **İstatistiksel Analiz**: LibXCore ile 60+ istatistiksel fonksiyon
- **String İşleme**: Kapsamlı metin işleme fonksiyonları
- **Sistem Entegrasyonu**: Dosya, bellek ve sistem fonksiyonları
- **Kontrol Yapıları**: FOR, WHILE, DO-LOOP, IF-THEN-ELSE
- **Veri Yapıları**: Diziler, listeler, sözlükler
- **Bellek Yönetimi**: Otomatik ve manuel bellek kontrolü
- **Modül Sistemi**: Kod organizasyonu ve yeniden kullanım

---

## TEMEL KOMUTLAR

### PRINT - Çıktı Verme
**Amaç**: Ekrana metin veya değişken değerleri yazdırmak
```pdsx
PRINT "Merhaba Dünya!"
PRINT "Sayı:", 42
PRINT "Sonuç: " + STR(25 * 4)
```

### REM - Yorum Satırları
**Amaç**: Kodda açıklama eklemek
```pdsx
REM Bu bir yorum satırıdır
PRINT "Program çalışıyor"  REM Satır sonu yorumu
```

### END - Program Sonlandırma
**Amaç**: Program çalışmasını sonlandırmak
```pdsx
PRINT "Program bitti"
END
```

### DIM - Değişken Tanımlama
**Amaç**: Değişkenleri belirli tiplerle tanımlamak
```pdsx
DIM sayı AS INTEGER
DIM isim AS STRING
DIM liste AS LIST
```

### LET - Değer Atama
**Amaç**: Değişkenlere değer atamak
```pdsx
LET x = 10
LET isim = "Ahmet"
LET sonuç = x * 2
```

---

## KONTROL YAPILARI

### IF-THEN-ELSE - Koşullu Çalıştırma
**Amaç**: Koşula göre farklı kodları çalıştırmak
```pdsx
x = 15
IF x > 10 THEN
    PRINT "Büyük sayı"
ELSEIF x = 10 THEN
    PRINT "Eşit sayı"
ELSE
    PRINT "Küçük sayı"
END IF
```

### FOR-NEXT - Döngü
**Amaç**: Belirli sayıda tekrarlama yapmak
```pdsx
FOR i = 1 TO 10
    PRINT "Sayım:", i
NEXT i

REM STEP ile atlama
FOR i = 0 TO 20 STEP 2
    PRINT i
NEXT i

REM İç içe döngüler
FOR i = 1 TO 3
    FOR j = 1 TO 3
        PRINT i * j
    NEXT j
NEXT i
```

### WHILE-WEND - Koşullu Döngü
**Amaç**: Koşul doğru olduğu sürece tekrarlamak
```pdsx
sayac = 0
WHILE sayac < 5
    PRINT "Sayaç:", sayac
    sayac = sayac + 1
WEND
```

### DO-LOOP - Esnek Döngü
**Amaç**: Çeşitli koşullarla döngü oluşturmak
```pdsx
DO
    x = x + 1
    PRINT x
LOOP UNTIL x >= 10

DO WHILE x < 20
    x = x + 1
    PRINT x
LOOP
```

---

## MATEMATİKSEL FONKSİYONLAR

### Temel Matematik
```pdsx
PRINT ABS(-15)        REM Mutlak değer: 15
PRINT SQRT(25)        REM Karekök: 5
PRINT POWER(2, 3)     REM Üs alma: 8
PRINT MOD(10, 3)      REM Mod işlemi: 1
PRINT SGN(-5)         REM İşaret: -1
PRINT MIN(5, 3, 8)    REM Minimum: 3
PRINT MAX(5, 3, 8)    REM Maksimum: 8
```

### Trigonometrik Fonksiyonlar
```pdsx
PRINT SIN(1.57)       REM Sinüs
PRINT COS(0)          REM Kosinüs: 1
PRINT TAN(0.785)      REM Tanjant
PRINT ASIN(1)         REM Ters sinüs
PRINT ACOS(0)         REM Ters kosinüs
PRINT ATAN(1)         REM Ters tanjant
```

### Logaritmik ve Üstel
```pdsx
PRINT LOG(10)         REM Doğal logaritma
PRINT EXP(1)          REM e üssü: 2.718...
PRINT PI()            REM Pi sayısı: 3.14159...
```

### Yuvarlama Fonksiyonları
```pdsx
PRINT ROUND(3.7, 0)   REM Yuvarlama: 4
PRINT CEIL(3.2)       REM Yukarı yuvarlama: 4
PRINT FLOOR(3.8)      REM Aşağı yuvarlama: 3
PRINT INT(3.9)        REM Tam sayı kısmı: 3
PRINT FIX(3.9)        REM Sıfıra doğru yuvarlama: 3
```

---

## STRING FONKSİYONLARI

### Temel String İşlemleri
```pdsx
REM Uzunluk
PRINT LEN("Merhaba")               REM 7

REM Alt string alma
PRINT LEFT$("Merhaba", 3)          REM "Mer"
PRINT RIGHT$("Merhaba", 3)         REM "aba"
PRINT MID$("Merhaba", 2, 3)        REM "erh"

REM Büyük/küçük harf
PRINT UPPER$("merhaba")            REM "MERHABA"
PRINT LOWER$("MERHABA")            REM "merhaba"
PRINT UCASE$("merhaba")            REM "MERHABA"
PRINT LCASE$("MERHABA")            REM "merhaba"
```

### String Temizleme
```pdsx
PRINT TRIM$("  boşluk  ")          REM "boşluk"
PRINT LTRIM$("  sol")              REM "sol"
PRINT RTRIM$("sağ  ")              REM "sağ"
```

### String Oluşturma
```pdsx
PRINT STRING$(5, "*")              REM "*****"
PRINT SPACE$(10)                   REM 10 boşluk
PRINT STR$(123)                    REM "123"
PRINT CHR$(65)                     REM "A"
```

### String Arama
```pdsx
PRINT INSTR(1, "Merhaba", "ba")    REM 6
PRINT ASC("A")                     REM 65
```

### Tip Dönüşümü
```pdsx
PRINT VAL("123.45")                REM 123.45
PRINT STR(456)                     REM "456"
```

---

## İSTATİSTİKSEL FONKSİYONLAR (LibXCore)

### Temel İstatistikler
```pdsx
veri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

PRINT MEAN(veri)                   REM Ortalama: 5.5
PRINT MEDIAN(veri)                 REM Medyan: 5.5
PRINT STD(veri)                    REM Standart sapma
PRINT VARIANCE(veri)               REM Varyans
PRINT SUM(veri)                    REM Toplam: 55
```

### Dağılım İstatistikleri
```pdsx
PRINT MIN(veri)                    REM Minimum: 1
PRINT MAX(veri)                    REM Maksimum: 10
PRINT PERCENTILE(veri, 25)         REM 25. yüzdelik
PRINT QUANTILE(veri, 0.75)         REM 0.75 kantil
PRINT IQR(veri)                    REM Çeyrekler arası genişlik
PRINT SKEWNESS(veri)               REM Çarpıklık
PRINT KURTOSIS(veri)               REM Basıklık
```

### Korelasyon ve Kovaryans
```pdsx
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

PRINT CORR(x, y)                   REM Korelasyon: 1.0
PRINT COVARIANCE(x, y)             REM Kovaryans
```

### Hipotez Testleri
```pdsx
grup1 = [12, 15, 18, 20, 22]
grup2 = [14, 16, 19, 21, 23]

PRINT TTEST2(grup1, grup2)         REM İki örneklem t-testi
PRINT FTEST(grup1, grup2)          REM F-testi (varyans eşitliği)
PRINT ZTEST1(grup1, 18)            REM Tek örneklem z-testi
```

### Regresyon Analizi
```pdsx
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

sonuç = LINREG(x, y)               REM Doğrusal regresyon
PRINT sonuç["slope"]               REM Eğim
PRINT sonuç["intercept"]           REM Kesim noktası
PRINT sonuç["r_squared"]           REM R-kare değeri
```

---

## SİSTEM FONKSİYONLARI

### Zaman ve Tarih
```pdsx
PRINT TIME_NOW()                   REM Şimdiki zaman
PRINT DATE_NOW()                   REM Şimdiki tarih
PRINT TIMER()                      REM Unix zaman damgası
SLEEP(2)                           REM 2 saniye bekle
```

### Sistem Bilgileri
```pdsx
PRINT CPU_COUNT()                  REM İşlemci sayısı
PRINT MEMORY_USAGE()               REM Bellek kullanımı (%)
PRINT ENVIRON$("PATH")             REM Çevre değişkeni
PRINT COMMAND$()                   REM Komut satırı argümanları
```

### Dosya Sistemi
```pdsx
PRINT EXISTS("dosya.txt")          REM Dosya var mı?
PRINT ISDIR("klasör")              REM Klasör mü?
PRINT FILESIZE("dosya.txt")        REM Dosya boyutu
dosyalar = LIST_DIR(".")           REM Dizin listesi
```

### Sistem Komutları
```pdsx
sonuç = SHELL("dir")               REM Sistem komutu çalıştır
PRINT sonuç                        REM Komut çıktısı
```

---

## VERİ YAPILARI

### Diziler
```pdsx
DIM sayılar(10) AS INTEGER         REM 10 elemanlı dizi
sayılar(1) = 42
PRINT sayılar(1)

DIM matris(3, 3) AS DOUBLE         REM 3x3 matris
matris(1, 1) = 1.5
```

### Listeler
```pdsx
liste = [1, 2, 3, 4, 5]
PRINT LEN(liste)                   REM Uzunluk: 5
liste.append(6)                    REM Eleman ekleme
```

### Stack ve Queue
```pdsx
yığın = CREATE_STACK()             REM Yığın oluştur
kuyruk = CREATE_QUEUE()            REM Kuyruk oluştur

PRINT TYPE_OF(yığın)               REM Tip bilgisi
```

---

## BELLEK YÖNETİMİ

### Bellek Tahsisi
```pdsx
ptr = MALLOC(1024)                 REM 1024 byte tahsis et
FREE(ptr)                          REM Belleği serbest bırak
boyut = SIZEOF("INTEGER")          REM Tip boyutu
```

### Pointer İşlemleri
```pdsx
DIM ptr AS POINTER TO INTEGER
ptr = MALLOC(4)
*ptr = 42                          REM Pointer üzerinden değer atama
PRINT *ptr                         REM Değeri oku
```

---

## MATH ve ARRAY FONKSİYONLARI

### Dizi Oluşturma
```pdsx
REM Sıfır matrisi
zeros_mat = ZEROS(3, 3)

REM Birim matrisi  
identity_mat = IDENTITY(3)

REM Aralık oluşturma
sayılar = ARANGE(0, 10, 2)         REM [0, 2, 4, 6, 8]

REM Lineer aralık
lin_space = LINSPACE(0, 1, 5)      REM [0, 0.25, 0.5, 0.75, 1]
```

### Dizi İşlemleri
```pdsx
dizi1 = [1, 2, 3]
dizi2 = [4, 5, 6]

REM Eleman bazında işlemler
toplam = ADD(dizi1, dizi2)         REM [5, 7, 9]
fark = SUBTRACT(dizi1, dizi2)      REM [-3, -3, -3]
çarpım = MULTIPLY(dizi1, dizi2)    REM [4, 10, 18]

REM Matris işlemleri
dot_product = DOT(dizi1, dizi2)    REM İç çarpım
```

### İstatistiksel Dizi İşlemleri
```pdsx
veri = [5, 2, 8, 1, 9, 3]

PRINT SORT(veri)                   REM Sıralama
PRINT UNIQUE(veri)                 REM Tekrarsız değerler
sıra = ARGSORT(veri)               REM Sıralama indeksleri
```

---

## DOSYA İŞLEMLERİ

### CSV Okuma/Yazma
```pdsx
REM CSV okuma
veri = READ_csv("veri.csv")

REM CSV yazma
TO_CSV(veri, "çıktı.csv")
```

### PDF İşlemleri
```pdsx
REM PDF metin okuma
metin = PDF_READ("döküman.pdf")

REM PDF'de arama
sonuçlar = PDF_SEARCH("döküman.pdf", "anahtar")
```

---

## GELİŞMİŞ İSTATİSTİK

### Normallik Testleri
```pdsx
veri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

PRINT NORMALTEST(veri)             REM D'Agostino normallik testi
PRINT SHAPIRO(veri)                REM Shapiro-Wilk testi
PRINT JARQUEBERATEST(veri)         REM Jarque-Bera testi
```

### Karşılaştırma Testleri
```pdsx
grup1 = [12, 15, 18, 20, 22]
grup2 = [14, 16, 19, 21, 23]

PRINT MANNWHITNEY(grup1, grup2)    REM Mann-Whitney U testi
PRINT WILCOXON(grup1, grup2)       REM Wilcoxon testi
PRINT KOLMOGOROVTEST(grup1, grup2) REM Kolmogorov-Smirnov testi
```

### ANOVA Testleri
```pdsx
grup1 = [1, 2, 3]
grup2 = [4, 5, 6]  
grup3 = [7, 8, 9]

PRINT ANOVA(grup1, grup2, grup3)   REM Tek yönlü ANOVA
PRINT KRUSKAL(grup1, grup2, grup3) REM Kruskal-Wallis testi
```

### Korelasyon Testleri
```pdsx
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

PRINT PEARSONR(x, y)               REM Pearson korelasyon
PRINT SPEARMANR(x, y)              REM Spearman korelasyon
PRINT KENDALLTAU(x, y)             REM Kendall's tau
```

---

## SİNYAL İŞLEME

### Fourier Dönüşümü
```pdsx
sinyal = [1, 2, 3, 4, 5]

fft_sonuç = FFT(sinyal)            REM Hızlı Fourier dönüşümü
ifft_sonuç = IFFT(fft_sonuç)       REM Ters FFT
```

### Konvolüsyon
```pdsx
sinyal1 = [1, 2, 3]
sinyal2 = [0.5, 0.5]

konvolüsyon = CONVOLVE(sinyal1, sinyal2)
korelasyon = CORRELATE(sinyal1, sinyal2)
```

---

## ZAMAN SERİSİ ANALİZİ

### Otokorelasyon
```pdsx
zaman_serisi = [1, 2, 1, 2, 1, 2, 1, 2]

oto_kor = AUTOCORR(zaman_serisi, 3)    REM 3 gecikmeye kadar
çapraz_kor = CROSSCORR(zaman_serisi, [2, 1, 2, 1])
```

### Hareketli Ortalama
```pdsx
veri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pencere = ROLLING(veri, 3)              REM 3 periyotluk pencere
```

---

## KÜMELEME ANALİZİ

### K-Means
```pdsx
veri_noktaları = [[1, 2], [2, 1], [8, 9], [9, 8]]
küme_sayısı = 2

sonuç = KMEANS(veri_noktaları, küme_sayısı)
PRINT sonuç["labels"]                   REM Küme etiketleri
PRINT sonuç["centers"]                  REM Küme merkezleri
```

### Hiyerarşik Kümeleme
```pdsx
veri = [[1, 2], [3, 4], [5, 6]]
dendogram = HIERARCHICAL(veri)
```

---

## ETKİ BOYUTU ÖLÇÜMLERİ

### Cohen's d
```pdsx
grup1 = [1, 2, 3, 4, 5]
grup2 = [3, 4, 5, 6, 7]

d = COHEN_D(grup1, grup2)              REM Cohen's d
g = HEDGES_G(grup1, grup2)             REM Hedges' g
delta = GLASS_DELTA(grup1, grup2)      REM Glass' delta
```

### ANOVA Etki Boyutları
```pdsx
f_değeri = 5.2
df1 = 2
df2 = 27

eta_kare = ETA_SQUARED(f_değeri, df1, df2)
omega_kare = OMEGA_SQUARED(f_değeri, df1, df2)
```

---

## GÜÇ ANALİZİ

### T-Test Güç Analizi
```pdsx
etki_boyutu = 0.5
örneklem_boyutu = 30
alfa = 0.05

güç = POWER_TTEST(etki_boyutu, örneklem_boyutu, alfa)
PRINT "İstatistiksel güç:", güç

REM Gerekli örneklem boyutu
gerekli_n = SAMPLE_SIZE_TTEST(etki_boyutu, 0.8, alfa)
PRINT "Gerekli n:", gerekli_n
```

---

## BOOTSTRAP ve YENİDEN ÖRNEKLEME

### Bootstrap
```pdsx
veri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

REM Bootstrap güven aralığı
bootstrap_sonuç = BOOTSTRAP(veri, MEAN, 1000)
PRINT "Bootstrap ortalama:", bootstrap_sonuç["mean"]
PRINT "Güven aralığı:", bootstrap_sonuç["confidence_interval"]
```

### Permütasyon Testi
```pdsx
grup1 = [1, 2, 3, 4, 5]
grup2 = [6, 7, 8, 9, 10]

perm_sonuç = PERMUTATION_TEST(grup1, grup2, MEAN, 1000)
PRINT "P-değeri:", perm_sonuç["p_value"]
```

---

## RASTGELE SAYI ÜRETİMİ

### Dağılım Örneklemleri
```pdsx
REM Normal dağılım
normal_sayılar = RANDNORM(10, 0, 1)    REM 10 adet, μ=0, σ=1

REM t-dağılımı
t_sayılar = RANDT(5, 10)               REM df=5, 10 adet

REM Ki-kare dağılımı
chi2_sayılar = RANDCHI2(3, 10)         REM df=3, 10 adet

REM F-dağılımı
f_sayılar = RANDF(2, 5, 10)            REM df1=2, df2=5, 10 adet
```

---

## ÇOKLU KARŞILAŞTIRMA DÜZELTMELERİ

### P-Değeri Düzeltmeleri
```pdsx
p_değerleri = [0.01, 0.02, 0.03, 0.04, 0.05]

REM Bonferroni düzeltmesi
bonf_sonuç = BONFERRONI(p_değerleri, 0.05)

REM Benjamini-Hochberg düzeltmesi
bh_sonuç = BENJAMINI(p_değerleri, 0.05)

PRINT "Düzeltilmiş p-değerleri:", bonf_sonuç
```

---

## İNTERPOLASYON

### Doğrusal İnterpolasyon
```pdsx
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
yeni_x = [1.5, 2.5, 3.5]

interpole_y = INTERP1D(x, y, yeni_x)
PRINT "İnterpolasyon sonucu:", interpole_y
```

### Spline İnterpolasyon
```pdsx
spline_y = SPLINE(x, y, yeni_x, 3)     REM 3. derece spline
```

---

## OPTİMİZASYON

### Fonksiyon Minimizasyonu
```pdsx
REM f(x) = x^2 + 2x + 1 fonksiyonunu minimize et
minimum = MINIMIZE("x**2 + 2*x + 1", [-1])
PRINT "Minimum noktası:", minimum["x"]
PRINT "Minimum değer:", minimum["fun"]
```

---

## VERİ TABLOSU İŞLEMLERİ

### DataFrame Benzeri İşlemler
```pdsx
REM Veri tablosu oluşturma
veri = {
    "isim": ["Ali", "Ayşe", "Mehmet"],
    "yaş": [25, 30, 35],
    "maaş": [3000, 4000, 5000]
}

df = DATAFRAME(veri)

REM Gruplama
yaş_grupları = GROUPBY(df, "yaş")

REM Birleştirme
df2 = DATAFRAME({"isim": ["Ali", "Veli"], "şehir": ["Ankara", "İstanbul"]})
birleşik = MERGE(df, df2, "isim")
```

---

## MATRİS İŞLEMLERİ

### Temel Matris Operasyonları
```pdsx
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]

REM Matris çarpımı
C = MATMUL(A, B)

REM Determinant
det_A = DET(A)

REM Ters matris
A_inv = INV(A)

REM Doğrusal denklem sistemi çözümü (Ax = b)
b = [1, 2]
x = SOLVE(A, b)
```

### Özvektör ve Özdeğer
```pdsx
REM Özdeğer ve özvektör hesaplama
matris = [[4, 2], [1, 3]]
öz_sonuç = EIGENVALUE(matris)
PRINT "Özdeğerler:", öz_sonuç["values"]
PRINT "Özvektörler:", öz_sonuç["vectors"]
```

---

## HATA YÖNETİMİ

### Try-Catch Benzeri Yapı
```pdsx
ON ERROR GOTO hata_yakalayıcı

REM Hatalı işlem
sonuç = 10 / 0

PRINT "Bu satır çalışmaz"
END

hata_yakalayıcı:
PRINT "Hata yakalandı: Sıfıra bölme"
RESUME NEXT
```

---

## MODÜL SİSTEMİ

### Modül İçe Aktarma
```pdsx
IMPORT "matematik_modülü.pdsx" AS mat

REM Modül fonksiyonu kullanma
sonuç = mat.özel_fonksiyon(10, 20)
```

---

## DEBUG ve İZLEME

### Debug Modları
```pdsx
DEBUG ON                           REM Debug modunu aç
TRACE ON                           REM İzleme modunu aç

FOR i = 1 TO 5
    PRINT "Döngü:", i
    STEP                           REM Adım adım çalıştır
NEXT i

DEBUG OFF
TRACE OFF
```

---

## ÖRNEKLİK PROGRAMLAR

### Basit Hesap Makinesi
```pdsx
PRINT "Basit Hesap Makinesi"
INPUT "Birinci sayıyı girin: ", a
INPUT "İkinci sayıyı girin: ", b
INPUT "İşlem (+, -, *, /): ", işlem

SELECT CASE işlem
CASE "+"
    sonuç = a + b
CASE "-"
    sonuç = a - b
CASE "*"
    sonuç = a * b
CASE "/"
    IF b <> 0 THEN
        sonuç = a / b
    ELSE
        PRINT "Sıfıra bölme hatası!"
        END
    END IF
END SELECT

PRINT "Sonuç:", sonuç
```

### İstatistiksel Analiz Örneği
```pdsx
REM Veri seti oluşturma
veri = [12, 15, 18, 20, 22, 25, 28, 30, 32, 35]

PRINT "=== İSTATİSTİKSEL ANALİZ ==="
PRINT "Veri sayısı:", LEN(veri)
PRINT "Ortalama:", MEAN(veri)
PRINT "Medyan:", MEDIAN(veri)
PRINT "Standart Sapma:", STD(veri)
PRINT "Minimum:", MIN(veri)
PRINT "Maksimum:", MAX(veri)

REM Normallik testi
normal_test = NORMALTEST(veri)
PRINT "Normallik testi p-değeri:", normal_test["p_value"]

IF normal_test["p_value"] > 0.05 THEN
    PRINT "Veri normal dağılıma uygun"
ELSE
    PRINT "Veri normal dağılıma uygun değil"
END IF
```

### Matris İşlemleri Örneği
```pdsx
REM 3x3 matris oluşturma
A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

PRINT "=== MATRİS İŞLEMLERİ ==="
PRINT "A Matrisi:", A
PRINT "B Matrisi:", B

REM Matris toplama
C = ADD(A, B)
PRINT "A + B =", C

REM Matris çarpımı
D = MATMUL(A, B)
PRINT "A * B =", D

REM Determinant
det_A = DET(A)
PRINT "det(A) =", det_A
```

---

## PERFORMANS İPUÇLARI

1. **Değişken Tiplerinizi Belirtin**: `DIM` komutu ile tip tanımlaması performansı artırır
2. **Döngülerde Veri Yapılarını Optimize Edin**: Büyük veri setlerinde uygun veri yapılarını kullanın
3. **Fonksiyon Çağrılarını Minimize Edin**: Tekrarlanan hesaplamaları değişkenlerde saklayın
4. **Bellek Yönetimini Dikkatli Yapın**: Büyük veri yapılarını kullanım sonrası temizleyin

---

## YAYGIN HATALAR ve ÇÖZÜMLERİ

### Sözdizimi Hataları
```pdsx
REM YANLIŞ
IF x = 10
    PRINT "On"
END

REM DOĞRU
IF x = 10 THEN
    PRINT "On"  
END IF
```

### Tip Hataları
```pdsx
REM YANLIŞ
sayı = "123"
sonuç = sayı + 10  REM String + sayı hatası

REM DOĞRU
sayı = VAL("123")  REM String'i sayıya çevir
sonuç = sayı + 10
```

---

## KOMUT ve FONKSİYON REFERANSI

### TEMEL KOMUTLAR

| Komut | Amaç | Açıklama |
|-------|------|----------|
| `PRINT` | Çıktı verme | Ekrana metin, sayı veya değişken değerleri yazdırır |
| `REM` | Yorum ekleme | Kodda açıklama satırları için kullanılır |
| `END` | Program sonlandırma | Programın çalışmasını bitirir |
| `DIM` | Değişken tanımlama | Değişkenleri belirli tiplerle tanımlar |
| `LET` | Değer atama | Değişkenlere değer atar |
| `INPUT` | Kullanıcı girişi | Kullanıcıdan veri almak için kullanılır |
| `IF-THEN-ELSE` | Koşullu çalıştırma | Koşula göre farklı kodları çalıştırır |
| `FOR-NEXT` | Döngü | Belirli sayıda tekrarlama yapar |
| `WHILE-WEND` | Koşullu döngü | Koşul doğru olduğu sürece tekrarlar |
| `DO-LOOP` | Esnek döngü | Çeşitli koşullarla döngü oluşturur |
| `SELECT CASE` | Çoklu seçim | Birden fazla koşulu kontrol eder |
| `GOTO` | Atlama | Belirtilen etikete atlar |
| `GOSUB` | Alt program çağırma | Alt programa gider ve geri döner |
| `RETURN` | Geri dönüş | Alt programdan ana programa döner |

### MATEMATİKSEL FONKSİYONLAR

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `ABS(x)` | Mutlak değer | Sayının mutlak değerini döndürür |
| `SQRT(x)` | Karekök | Sayının karekökünü hesaplar |
| `POWER(x,y)` | Üs alma | x'in y'inci kuvvetini hesaplar |
| `MOD(x,y)` | Mod işlemi | x'in y'ye bölümünden kalanı verir |
| `SGN(x)` | İşaret | Sayının işaretini döndürür (-1, 0, 1) |
| `MIN(x,y,...)` | Minimum | En küçük değeri bulur |
| `MAX(x,y,...)` | Maksimum | En büyük değeri bulur |
| `SIN(x)` | Sinüs | Açının sinüsünü hesaplar |
| `COS(x)` | Kosinüs | Açının kosinüsünü hesaplar |
| `TAN(x)` | Tanjant | Açının tanjantını hesaplar |
| `ASIN(x)` | Ters sinüs | Ark sinüsü hesaplar |
| `ACOS(x)` | Ters kosinüs | Ark kosinüsü hesaplar |
| `ATAN(x)` | Ters tanjant | Ark tanjantı hesaplar |
| `LOG(x)` | Doğal logaritma | Doğal logaritma hesaplar |
| `EXP(x)` | Üstel fonksiyon | e'nin x'inci kuvvetini hesaplar |
| `PI()` | Pi sayısı | Pi sabitini döndürür |
| `ROUND(x,n)` | Yuvarlama | Sayıyı n ondalık basamağa yuvarlar |
| `CEIL(x)` | Yukarı yuvarlama | En yakın büyük tam sayıya yuvarlar |
| `FLOOR(x)` | Aşağı yuvarlama | En yakın küçük tam sayıya yuvarlar |
| `INT(x)` | Tam sayı kısmı | Sayının tam sayı kısmını alır |
| `FIX(x)` | Sıfıra yuvarlama | Sıfıra doğru yuvarlar |

### STRING FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `LEN(s)` | Uzunluk | String'in karakter sayısını döndürür |
| `LEFT$(s,n)` | Sol kısım | String'in sol tarafından n karakter alır |
| `RIGHT$(s,n)` | Sağ kısım | String'in sağ tarafından n karakter alır |
| `MID$(s,start,len)` | Orta kısım | String'in belirtilen kısmını alır |
| `UPPER$(s)` | Büyük harf | Tüm harfleri büyük yapar |
| `LOWER$(s)` | Küçük harf | Tüm harfleri küçük yapar |
| `UCASE$(s)` | Büyük harf | Tüm harfleri büyük yapar |
| `LCASE$(s)` | Küçük harf | Tüm harfleri küçük yapar |
| `TRIM$(s)` | Boşluk temizleme | Baş ve sondaki boşlukları siler |
| `LTRIM$(s)` | Sol boşluk temizleme | Soldaki boşlukları siler |
| `RTRIM$(s)` | Sağ boşluk temizleme | Sağdaki boşlukları siler |
| `STRING$(n,c)` | Tekrar | Karakteri n kez tekrarlar |
| `SPACE$(n)` | Boşluk | n adet boşluk üretir |
| `STR$(n)` | Sayıdan string | Sayıyı string'e çevirir |
| `CHR$(n)` | ASCII karakter | ASCII kodundan karakter üretir |
| `INSTR(start,s,sub)` | Arama | String içinde alt string arar |
| `ASC(c)` | ASCII kodu | Karakterin ASCII kodunu verir |
| `VAL(s)` | String'den sayı | String'i sayıya çevirir |

### İSTATİSTİKSEL FONKSİYONLAR

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `MEAN(data)` | Aritmetik ortalama | Verilerin ortalamasını hesaplar |
| `MEDIAN(data)` | Medyan | Verilerin medyanını bulur |
| `STD(data)` | Standart sapma | Standart sapmayı hesaplar |
| `VARIANCE(data)` | Varyans | Varyansı hesaplar |
| `SUM(data)` | Toplam | Verilerin toplamını hesaplar |
| `MIN(data)` | Minimum | En küçük değeri bulur |
| `MAX(data)` | Maksimum | En büyük değeri bulur |
| `PERCENTILE(data,p)` | Yüzdelik | p'inci yüzdelik değeri bulur |
| `QUANTILE(data,q)` | Kantil | q kantilini hesaplar |
| `IQR(data)` | Çeyrekler arası genişlik | 75. ve 25. yüzdelik farkı |
| `SKEWNESS(data)` | Çarpıklık | Dağılımın çarpıklığını ölçer |
| `KURTOSIS(data)` | Basıklık | Dağılımın basıklığını ölçer |
| `CORR(x,y)` | Korelasyon | İki değişken arasındaki ilişkiyi ölçer |
| `COVARIANCE(x,y)` | Kovaryans | İki değişkenin kovaryansını hesaplar |

### HİPOTEZ TESTLERİ

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `TTEST1(data,mu)` | Tek örneklem t-testi | Bir grubun ortalamasını test eder |
| `TTEST2(x,y)` | İki örneklem t-testi | İki grubun ortalamasını karşılaştırır |
| `TTESTPAIRED(x,y)` | Eşleştirilmiş t-testi | Eşleştirilmiş verileri karşılaştırır |
| `ZTEST1(data,mu)` | Tek örneklem z-testi | Büyük örneklem ortalama testi |
| `ZTEST2(x,y)` | İki örneklem z-testi | İki büyük grubun karşılaştırması |
| `FTEST(x,y)` | F-testi | Varyans eşitliğini test eder |
| `CHITEST(obs,exp)` | Ki-kare testi | Bağımsızlık testini yapar |
| `ANOVA(...)` | Tek yönlü ANOVA | Çok gruplu ortalama karşılaştırması |
| `NORMALTEST(data)` | Normallik testi | Verilerin normal dağılıma uygunluğu |
| `SHAPIRO(data)` | Shapiro-Wilk testi | Normallik testi (küçük örneklem) |
| `MANNWHITNEY(x,y)` | Mann-Whitney U | Parametrik olmayan karşılaştırma |
| `WILCOXON(x,y)` | Wilcoxon testi | Parametrik olmayan eşleştirilmiş test |
| `KRUSKAL(...)` | Kruskal-Wallis | Parametrik olmayan çok grup testi |

### SİSTEM FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `TIME_NOW()` | Şimdiki zaman | Geçerli zamanı döndürür |
| `DATE_NOW()` | Şimdiki tarih | Geçerli tarihi döndürür |
| `TIMER()` | Zaman damgası | Unix zaman damgasını verir |
| `SLEEP(n)` | Bekleme | n saniye bekler |
| `CPU_COUNT()` | İşlemci sayısı | Sistem işlemci sayısını verir |
| `MEMORY_USAGE()` | Bellek kullanımı | Bellek kullanım yüzdesini verir |
| `EXISTS(path)` | Dosya varlığı | Dosya/klasörün varlığını kontrol eder |
| `ISDIR(path)` | Klasör kontrolü | Path'in klasör olup olmadığını kontrol eder |
| `FILESIZE(path)` | Dosya boyutu | Dosyanın boyutunu byte olarak verir |
| `LIST_DIR(path)` | Dizin listesi | Klasördeki dosyaları listeler |
| `SHELL(cmd)` | Sistem komutu | Sistem komutunu çalıştırır |
| `ENVIRON$(var)` | Çevre değişkeni | Sistem çevre değişkenini okur |
| `COMMAND$()` | Komut satırı | Komut satırı argümanlarını verir |

### BELLEK YÖNETİMİ

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `MALLOC(size)` | Bellek tahsisi | Bellek alanı tahsis eder |
| `FREE(ptr)` | Bellek serbest bırakma | Tahsis edilen belleği serbest bırakır |
| `SIZEOF(type)` | Tip boyutu | Veri tipinin boyutunu verir |
| `CREATE_STACK()` | Yığın oluşturma | Stack veri yapısı oluşturur |
| `CREATE_QUEUE()` | Kuyruk oluşturma | Queue veri yapısı oluşturur |
| `TYPE_OF(var)` | Tip kontrolü | Değişkenin tipini döndürür |

### DİZİ ve MATRİS FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `ZEROS(n,m)` | Sıfır matrisi | n×m boyutunda sıfır matrisi oluşturur |
| `ONES(n,m)` | Bir matrisi | n×m boyutunda bir matrisi oluşturur |
| `IDENTITY(n)` | Birim matris | n×n birim matris oluşturur |
| `ARANGE(start,stop,step)` | Aralık | Belirtilen aralıkta dizi oluşturur |
| `LINSPACE(start,stop,num)` | Lineer aralık | Eşit aralıklı sayı dizisi oluşturur |
| `ADD(a,b)` | Dizi toplama | İki diziyi eleman eleman toplar |
| `SUBTRACT(a,b)` | Dizi çıkarma | İki diziyi eleman eleman çıkarır |
| `MULTIPLY(a,b)` | Dizi çarpma | İki diziyi eleman eleman çarpar |
| `DIVIDE(a,b)` | Dizi bölme | İki diziyi eleman eleman böler |
| `DOT(a,b)` | İç çarpım | İki dizinin iç çarpımını hesaplar |
| `MATMUL(a,b)` | Matris çarpımı | İki matrisin çarpımını hesaplar |
| `DET(matrix)` | Determinant | Matrisin determinantını hesaplar |
| `INV(matrix)` | Ters matris | Matrisin tersini hesaplar |
| `SOLVE(A,b)` | Denklem çözümü | Ax=b doğrusal denklem sistemini çözer |
| `SORT(array)` | Sıralama | Diziyi küçükten büyüğe sıralar |
| `UNIQUE(array)` | Tekrarsız değerler | Dizideki tekrarsız değerleri döndürür |
| `ARGSORT(array)` | Sıralama indeksleri | Sıralama için gereken indeksleri verir |

### İLERİ İSTATİSTİK FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `LINREG(x,y)` | Doğrusal regresyon | İki değişken arasında doğrusal model kurar |
| `POLYREG(x,y,degree)` | Polinom regresyon | Polinom regresyon modeli oluşturur |
| `PEARSONR(x,y)` | Pearson korelasyon | Pearson korelasyon katsayısını hesaplar |
| `SPEARMANR(x,y)` | Spearman korelasyon | Spearman sıra korelasyonunu hesaplar |
| `KENDALLTAU(x,y)` | Kendall's tau | Kendall tau korelasyonunu hesaplar |
| `COHEN_D(x,y)` | Cohen's d | Etki boyutunu (Cohen's d) hesaplar |
| `HEDGES_G(x,y)` | Hedges' g | Düzeltilmiş etki boyutunu hesaplar |
| `ETA_SQUARED(f,df1,df2)` | Eta kare | ANOVA etki boyutunu hesaplar |
| `POWER_TTEST(effect,n,alpha)` | İstatistiksel güç | T-testi için güç analizi yapar |
| `BOOTSTRAP(data,func,n)` | Bootstrap | Bootstrap yöntemiyle güven aralığı hesaplar |

### SİNYAL İŞLEME FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `FFT(signal)` | Hızlı Fourier dönüşümü | Sinyalin frekans domenine çevirir |
| `IFFT(signal)` | Ters FFT | Frekans domeninden zaman domenine çevirir |
| `CONVOLVE(x,y)` | Konvolüsyon | İki sinyalin konvolüsyonunu hesaplar |
| `CORRELATE(x,y)` | Çapraz korelasyon | İki sinyalin çapraz korelasyonunu hesaplar |
| `AUTOCORR(data,lags)` | Otokorelasyon | Sinyalin otokorelasyonunu hesaplar |

### ZAMAN SERİSİ FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `ROLLING(data,window)` | Hareketli pencere | Hareketli pencere istatistikleri |
| `CROSSCORR(x,y,lags)` | Çapraz korelasyon | İki zaman serisinin çapraz korelasyonu |
| `ARIMA(data,order)` | ARIMA modeli | Zaman serisi için ARIMA modeli kurar |

### KÜMELEME FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `KMEANS(data,k)` | K-means kümeleme | Verileri k kümeye ayırır |
| `HIERARCHICAL(data)` | Hiyerarşik kümeleme | Hiyerarşik kümeleme yapar |

### RASTGELE SAYI ÜRETİMİ

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `RND()` | Rastgele sayı | 0-1 arası rastgele sayı üretir |
| `RANDNORM(n,mu,sigma)` | Normal dağılım | Normal dağılımdan rastgele sayılar |
| `RANDT(df,n)` | t-dağılımı | t-dağılımından rastgele sayılar |
| `RANDCHI2(df,n)` | Ki-kare dağılımı | Ki-kare dağılımından rastgele sayılar |
| `RANDF(df1,df2,n)` | F-dağılımı | F-dağılımından rastgele sayılar |

### VERİ TABLOSU FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `DATAFRAME(data)` | Veri çerçevesi | Pandas benzeri veri yapısı oluşturur |
| `GROUPBY(df,column)` | Gruplama | Belirtilen sütuna göre gruplar |
| `MERGE(df1,df2,on)` | Birleştirme | İki veri çerçevesini birleştirir |
| `PIVOT(df,index,cols,vals)` | Pivot tablo | Verileri pivot tablosuna çevirir |
| `READ_CSV(file)` | CSV okuma | CSV dosyasını okur |
| `TO_CSV(data,file)` | CSV yazma | Verileri CSV dosyasına yazar |

### DOSYA İŞLEMLERİ

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `PDF_READ(file)` | PDF okuma | PDF dosyasından metin çıkarır |
| `PDF_SEARCH(file,keyword)` | PDF arama | PDF'de anahtar kelime arar |
| `WEB_GET(url)` | Web isteği | HTTP GET isteği gönderir |
| `WEB_POST(url,data)` | Web POST | HTTP POST isteği gönderir |

### OPTİMİZASYON FONKSİYONLARI

| Fonksiyon | Amaç | Açıklama |
|-----------|------|----------|
| `MINIMIZE(func,x0)` | Fonksiyon minimizasyonu | Fonksiyonun minimum noktasını bulur |
| `INTERP1D(x,y,new_x)` | Doğrusal interpolasyon | Noktalar arası değer tahmin eder |
| `SPLINE(x,y,new_x,degree)` | Spline interpolasyon | Spline interpolasyon yapar |

### DEBUG ve HATA YÖNETİMİ

| Komut/Fonksiyon | Amaç | Açıklama |
|-----------------|------|----------|
| `DEBUG ON/OFF` | Debug modu | Hata ayıklama modunu açar/kapatır |
| `TRACE ON/OFF` | İzleme modu | Kod izleme modunu açar/kapatır |
| `STEP` | Adım adım | Programı tek adımda çalıştırır |
| `ON ERROR GOTO` | Hata yakalama | Hata durumunda belirtilen yere atlar |
| `RESUME NEXT` | Devam etme | Hatadan sonra bir sonraki satırdan devam eder |

### MODÜL SİSTEMİ

| Komut | Amaç | Açıklama |
|-------|------|----------|
| `IMPORT "file" AS name` | Modül içe aktarma | Başka dosyaları programa dahil eder |
| `INCLUDE "file"` | Dosya dahil etme | Dosya içeriğini programa ekler |

---

Bu referans, PDSX v12X'in tüm komut ve fonksiyonlarının kapsamlı listesidir. Her fonksiyon için kısa açıklama ve amaç belirtilmiştir. Detaylı kullanım örnekleri için kılavuzun ilgili bölümlerine bakabilirsiniz.

---

Bu kılavuz PDSX v12X'in temel ve ileri özelliklerini kapsamaktadır. Her fonksiyon ve komut için örnekler verilmiş, kullanım amaçları açıklanmıştır. PDSX'in güçlü matematik, istatistik ve sistem entegrasyon yetenekleri ile karmaşık veri analizi ve hesaplama görevlerini kolayca gerçekleştirebilirsiniz.
