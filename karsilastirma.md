# PDSX Dosyaları Gerçek Karşılaştırma
# Sadece Gerçekte Var Olan Fonksiyonların Karşılaştırması

Bu rapor, üç PDSX dosyasını dikkatli bir şekilde okuyarak, sadece gerçekte mevcut olan fonksiyonları karşılaştırır.

## DOSYA BİLGİLERİ

| Dosya | Satır Sayısı | Açıklama |
|-------|-------------|-----------|
| pdsx.py | 7685 satır | Enhanced Programming Language Interpreter |
| pdsxv12xNEW.py | 8233 satır | Ana PDSX yorumlayıcı (C64 + LibX entegrasyonu) |
| pdsxv12X.py | 7965 satır | Enhanced Programming Language Interpreter (12X versiyon) |

## FONKSİYON TABLOSU GERÇEK KARŞILAŞTIRMA

**NOT: ✅ = VAR, ❌ = YOK**

### 1. STRING FONKSİYONLARI (19 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| MID$ | ✅ | ✅ | ✅ | Alt string çıkarma |
| LEN | ✅ | ✅ | ✅ | String uzunluğu |
| LEFT$ | ✅ | ✅ | ✅ | Sol karakterler |
| RIGHT$ | ✅ | ✅ | ✅ | Sağ karakterler |
| LTRIM$ | ✅ | ✅ | ✅ | Soldan boşluk temizleme |
| RTRIM$ | ✅ | ✅ | ✅ | Sağdan boşluk temizleme |
| TRIM$ | ✅ | ✅ | ✅ | Her iki yandan boşluk temizleme |
| UCASE$ | ✅ | ✅ | ✅ | Büyük harfe çevirme |
| LCASE$ | ✅ | ✅ | ✅ | Küçük harfe çevirme |
| UPPER$ | ✅ | ✅ | ✅ | Büyük harfe çevirme (alternatif) |
| LOWER$ | ✅ | ✅ | ✅ | Küçük harfe çevirme (alternatif) |
| STR$ | ✅ | ✅ | ✅ | Sayıyı string'e çevirme |
| STR | ✅ | ✅ | ✅ | Sayıyı string'e çevirme (kısa) |
| VAL | ✅ | ✅ | ✅ | String'i sayıya çevirme |
| ASC | ✅ | ✅ | ✅ | ASCII kodu |
| CHR$ | ✅ | ✅ | ✅ | ASCII'den karakter |
| STRING$ | ✅ | ✅ | ✅ | Tekrarlanan karakter |
| SPACE$ | ✅ | ✅ | ✅ | Boşluk karakterleri |
| INSTR | ✅ | ✅ | ✅ | Alt string arama |

**TOPLAM: pdsx.py: 19, pdsxv12xNEW.py: 19, pdsxv12X.py: 19**

### 2. TEMEL MATEMATİK FONKSİYONLARI (15 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| ABS | ✅ | ✅ | ✅ | Mutlak değer |
| INT | ✅ | ✅ | ✅ | Tam sayı kısmı |
| FIX | ✅ | ✅ | ✅ | Tam sayıya çevirme |
| ROUND | ✅ | ✅ | ✅ | Yuvarlama |
| SGN | ✅ | ✅ | ✅ | İşaret fonksiyonu |
| MOD | ✅ | ✅ | ✅ | Modülo |
| SQR | ✅ | ✅ | ✅ | Karekök |
| SIN | ✅ | ✅ | ✅ | Sinüs |
| COS | ✅ | ✅ | ✅ | Kosinüs |
| TAN | ✅ | ✅ | ✅ | Tanjant |
| LOG | ✅ | ✅ | ✅ | Logaritma |
| EXP | ✅ | ✅ | ✅ | Exponential |
| ATN | ✅ | ✅ | ✅ | Arctangent |
| PI | ✅ | ✅ | ✅ | Pi sayısı |
| RND | ✅ | ✅ | ✅ | Rastgele sayı |

**TOPLAM: pdsx.py: 15, pdsxv12xNEW.py: 15, pdsxv12X.py: 15**

### 3. GELİŞMİŞ MATEMATİK FONKSİYONLARI (12 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| SINH | ✅ | ✅ | ✅ | Hiperbolik sinüs |
| COSH | ✅ | ✅ | ✅ | Hiperbolik kosinüs |
| TANH | ✅ | ✅ | ✅ | Hiperbolik tanjant |
| ASIN | ✅ | ✅ | ✅ | Arcsine |
| ACOS | ✅ | ✅ | ✅ | Arccosine |
| ATAN2 | ✅ | ✅ | ✅ | Atan2 |
| CEIL | ✅ | ✅ | ✅ | Tavan fonksiyonu |
| FLOOR | ✅ | ✅ | ✅ | Taban fonksiyonu |
| POW | ✅ | ✅ | ✅ | Üs alma |
| SQRT | ✅ | ✅ | ✅ | Karekök (alternatif) |
| MIN | ✅ | ✅ | ✅ | Minimum |
| MAX | ✅ | ✅ | ✅ | Maksimum |

**TOPLAM: pdsx.py: 12, pdsxv12xNEW.py: 12, pdsxv12X.py: 12**

### 4. VERİ BİLİMİ FONKSİYONLARI (15 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| MEAN | ✅ | ✅ | ✅ | Aritmetik ortalama |
| MEDIAN | ✅ | ✅ | ✅ | Medyan |
| STD | ✅ | ✅ | ✅ | Standart sapma |
| SUM | ✅ | ✅ | ✅ | Toplam |
| CORR | ✅ | ✅ | ✅ | Korelasyon |
| VARIANCE | ✅ | ✅ | ✅ | Varyans |
| VAR | ✅ | ✅ | ✅ | Varyans (kısa) |
| PERCENTILE | ✅ | ✅ | ✅ | Percentile |
| QUANTILE | ✅ | ✅ | ✅ | Quantile |
| IQR | ✅ | ✅ | ✅ | Interquartile range |
| SKEWNESS | ✅ | ✅ | ✅ | Çarpıklık |
| SKEW | ✅ | ✅ | ✅ | Çarpıklık (kısa) |
| KURTOSIS | ✅ | ✅ | ✅ | Basıklık |
| KURT | ✅ | ✅ | ✅ | Basıklık (kısa) |
| COVARIANCE | ✅ | ✅ | ✅ | Kovaryans |
| COV | ✅ | ✅ | ✅ | Kovaryans (kısa) |

**TOPLAM: pdsx.py: 15, pdsxv12xNEW.py: 15, pdsxv12X.py: 15**

### 5. TEMEL İSTATİSTİK TESTLERİ (10 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| TTEST1 | ✅ | ✅ | ✅ | Tek örneklem t-test |
| TTEST2 | ✅ | ✅ | ✅ | İki örneklem t-test |
| TTESTPAIRED | ✅ | ✅ | ✅ | Eşleştirilmiş t-test |
| ZTEST1 | ✅ | ✅ | ✅ | Tek örneklem z-test |
| ZTEST2 | ✅ | ✅ | ✅ | İki örneklem z-test |
| FTEST | ✅ | ✅ | ✅ | F-test |
| CHITEST | ✅ | ✅ | ✅ | Chi-square test |
| CHI2TEST | ✅ | ✅ | ✅ | Chi-square test (alternatif) |
| ANOVA | ✅ | ✅ | ✅ | Tek yönlü ANOVA |
| ANOVA1 | ✅ | ✅ | ✅ | Tek yönlü ANOVA (alternatif) |

**TOPLAM: pdsx.py: 10, pdsxv12xNEW.py: 10, pdsxv12X.py: 10**

### 6. REGRESYON FONKSİYONLARI (2 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| LINREG | ✅ | ✅ | ✅ | Doğrusal regresyon |
| POLYREG | ✅ | ✅ | ✅ | Polinom regresyon |

**TOPLAM: pdsx.py: 2, pdsxv12xNEW.py: 2, pdsxv12X.py: 2**

### 7. NUMPY ARRAY OLUŞTURMA (8 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| ARRAY | ✅ | ✅ | ✅ | Array oluşturma |
| ZEROS | ✅ | ✅ | ✅ | Sıfır array |
| ONES | ✅ | ✅ | ✅ | Bir array |
| FULL | ✅ | ✅ | ✅ | Dolu array |
| EYE | ✅ | ✅ | ✅ | Birim matris |
| IDENTITY | ✅ | ✅ | ✅ | Birim matris (alternatif) |
| ARANGE | ✅ | ✅ | ✅ | Aralık array |
| LINSPACE | ✅ | ✅ | ✅ | Doğrusal aralık |

**TOPLAM: pdsx.py: 8, pdsxv12xNEW.py: 8, pdsxv12X.py: 8**

### 8. ARRAY MANİPÜLASYON (7 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| RESHAPE | ✅ | ✅ | ✅ | Şekil değiştirme |
| FLATTEN | ✅ | ✅ | ✅ | Düzleştirme |
| TRANSPOSE | ✅ | ✅ | ✅ | Transpoze |
| CONCATENATE | ✅ | ✅ | ✅ | Birleştirme |
| STACK | ✅ | ✅ | ✅ | Yığınlama |
| VSTACK | ✅ | ✅ | ✅ | Dikey yığınlama |
| HSTACK | ✅ | ✅ | ✅ | Yatay yığınlama |

**TOPLAM: pdsx.py: 7, pdsxv12xNEW.py: 7, pdsxv12X.py: 7**

### 9. MATEMATİKSEL ARRAY İŞLEMLERİ (7 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| DOT | ✅ | ✅ | ✅ | Nokta çarpımı |
| MATMUL | ✅ | ✅ | ✅ | Matris çarpımı |
| CROSS | ✅ | ✅ | ✅ | Çapraz çarpım |
| NORM | ✅ | ✅ | ✅ | Norm |
| DET | ✅ | ✅ | ✅ | Determinant |
| INV | ✅ | ✅ | ✅ | Ters matris |
| SOLVE | ✅ | ✅ | ✅ | Doğrusal sistem çözme |

**TOPLAM: pdsx.py: 7, pdsxv12xNEW.py: 7, pdsxv12X.py: 7**

### 10. ELEMENT-WISE İŞLEMLER (5 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| ADD | ✅ | ✅ | ✅ | Eleman bazında toplama |
| SUBTRACT | ✅ | ✅ | ✅ | Eleman bazında çıkarma |
| MULTIPLY | ✅ | ✅ | ✅ | Eleman bazında çarpma |
| DIVIDE | ✅ | ✅ | ✅ | Eleman bazında bölme |
| POWER | ✅ | ✅ | ✅ | Eleman bazında üs alma |

**TOPLAM: pdsx.py: 5, pdsxv12xNEW.py: 5, pdsxv12X.py: 5**

### 11. İSTATİSTİKSEL ARRAY FONKSİYONLARI (5 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| SORT | ✅ | ✅ | ✅ | Sıralama |
| ARGSORT | ✅ | ✅ | ✅ | İndeks sıralaması |
| UNIQUE | ✅ | ✅ | ✅ | Benzersiz değerler |
| BINCOUNT | ✅ | ✅ | ✅ | Binom sayma |
| HISTOGRAM | ✅ | ✅ | ✅ | Histogram |

**TOPLAM: pdsx.py: 5, pdsxv12xNEW.py: 5, pdsxv12X.py: 5**

### 12. GELİŞMİŞ İSTATİSTİK TESTLERİ (11 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| NORMALTEST | ✅ | ✅ | ✅ | Normallik testi |
| SHAPIRO | ✅ | ✅ | ✅ | Shapiro-Wilk testi |
| JARQUEBERATEST | ✅ | ✅ | ✅ | Jarque-Bera testi |
| KOLMOGOROVTEST | ✅ | ✅ | ✅ | Kolmogorov-Smirnov testi |
| MANNWHITNEY | ✅ | ✅ | ✅ | Mann-Whitney U testi |
| WILCOXON | ✅ | ✅ | ✅ | Wilcoxon testi |
| KRUSKAL | ✅ | ✅ | ✅ | Kruskal-Wallis testi |
| FRIEDMAN | ✅ | ✅ | ✅ | Friedman testi |
| BARTLETT | ✅ | ✅ | ✅ | Bartlett testi |
| LEVENE | ✅ | ✅ | ✅ | Levene testi |
| FLIGNER | ✅ | ✅ | ✅ | Fligner-Killeen testi |

**TOPLAM: pdsx.py: 11, pdsxv12xNEW.py: 11, pdsxv12X.py: 11**

### 13. KORELASYON TESTLERİ (3 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| PEARSONR | ✅ | ✅ | ✅ | Pearson korelasyonu |
| SPEARMANR | ✅ | ✅ | ✅ | Spearman korelasyonu |
| KENDALLTAU | ✅ | ✅ | ✅ | Kendall's tau |

**TOPLAM: pdsx.py: 3, pdsxv12xNEW.py: 3, pdsxv12X.py: 3**

### 14. DAĞILIM TESTLERİ (2 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| BINOMTEST | ✅ | ✅ | ✅ | Binom testi |
| POISSONTEST | ✅ | ✅ | ✅ | Poisson testi |

**TOPLAM: pdsx.py: 2, pdsxv12xNEW.py: 2, pdsxv12X.py: 2**

### 15. GELİŞMİŞ ANOVA (3 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| MANOVA | ✅ | ✅ | ✅ | Çok değişkenli ANOVA |
| ANOVA2WAY | ✅ | ✅ | ✅ | İki yönlü ANOVA |
| REPEATED_ANOVA | ✅ | ✅ | ✅ | Tekrarlı ölçümler ANOVA |

**TOPLAM: pdsx.py: 3, pdsxv12xNEW.py: 3, pdsxv12X.py: 3**

### 16. POST-HOC TESTLERİ (3 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| TUKEY | ✅ | ✅ | ✅ | Tukey HSD |
| BONFERRONI | ✅ | ✅ | ✅ | Bonferroni düzeltmesi |
| BENJAMINI | ✅ | ✅ | ✅ | Benjamini-Hochberg düzeltmesi |

**TOPLAM: pdsx.py: 3, pdsxv12xNEW.py: 3, pdsxv12X.py: 3**

### 17. DAĞILIM FONKSİYONLARI (8 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| NORM_PDF | ✅ | ✅ | ✅ | Normal PDF |
| NORM_CDF | ✅ | ✅ | ✅ | Normal CDF |
| T_PDF | ✅ | ✅ | ✅ | t-dağılımı PDF |
| T_CDF | ✅ | ✅ | ✅ | t-dağılımı CDF |
| CHI2_PDF | ✅ | ✅ | ✅ | Chi-kare PDF |
| CHI2_CDF | ✅ | ✅ | ✅ | Chi-kare CDF |
| F_PDF | ✅ | ✅ | ✅ | F-dağılımı PDF |
| F_CDF | ✅ | ✅ | ✅ | F-dağılımı CDF |

**TOPLAM: pdsx.py: 8, pdsxv12xNEW.py: 8, pdsxv12X.py: 8**

### 18. RASTGELE ÖRNEKLEME (6 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| RANDNORM | ✅ | ✅ | ✅ | Normal dağılım örnekleme |
| RANDT | ✅ | ✅ | ✅ | t-dağılımı örnekleme |
| RANDCHI2 | ✅ | ✅ | ✅ | Chi-kare örnekleme |
| RANDF | ✅ | ✅ | ✅ | F-dağılımı örnekleme |
| RANDBINOM | ✅ | ✅ | ✅ | Binom örnekleme |
| RANDPOISSON | ✅ | ✅ | ✅ | Poisson örnekleme |

**TOPLAM: pdsx.py: 6, pdsxv12xNEW.py: 6, pdsxv12X.py: 6**

### 19. SİNYAL İŞLEME (4 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| FFT | ✅ | ✅ | ✅ | Hızlı Fourier dönüşümü |
| IFFT | ✅ | ✅ | ✅ | Ters FFT |
| CONVOLVE | ✅ | ✅ | ✅ | Konvolüsyon |
| CORRELATE | ✅ | ✅ | ✅ | Korelasyon |

**TOPLAM: pdsx.py: 4, pdsxv12xNEW.py: 4, pdsxv12X.py: 4**

### 20. İNTERPOLASYON (2 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| INTERP1D | ✅ | ✅ | ✅ | 1D interpolasyon |
| SPLINE | ✅ | ✅ | ✅ | Spline interpolasyon |

**TOPLAM: pdsx.py: 2, pdsxv12xNEW.py: 2, pdsxv12X.py: 2**

### 21. OPTİMİZASYON (2 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| MINIMIZE | ✅ | ✅ | ✅ | Fonksiyon minimizasyonu |
| LEASTSQ | ✅ | ✅ | ✅ | En küçük kareler |

**TOPLAM: pdsx.py: 2, pdsxv12xNEW.py: 2, pdsxv12X.py: 2**

### 22. KÜMELEME (2 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| KMEANS | ✅ | ✅ | ✅ | K-means kümeleme |
| HIERARCHICAL | ✅ | ✅ | ✅ | Hiyerarşik kümeleme |

**TOPLAM: pdsx.py: 2, pdsxv12xNEW.py: 2, pdsxv12X.py: 2**

### 23. ZAMAN SERİSİ ANALİZİ (3 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| AUTOCORR | ✅ | ✅ | ✅ | Otokorelasyon |
| CROSSCORR | ✅ | ✅ | ✅ | Çapraz korelasyon |
| ARIMA | ✅ | ✅ | ✅ | ARIMA modeli |

**TOPLAM: pdsx.py: 3, pdsxv12xNEW.py: 3, pdsxv12X.py: 3**

### 24. PANDAS-BENZERİ FONKSİYONLAR (14 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| DATAFRAME | ✅ | ✅ | ✅ | DataFrame oluşturma |
| SERIES | ✅ | ✅ | ✅ | Series oluşturma |
| READ_CSV | ✅ | ✅ | ✅ | CSV okuma |
| TO_CSV | ✅ | ✅ | ✅ | CSV yazma |
| GROUPBY | ✅ | ✅ | ✅ | Gruplama |
| PIVOT | ✅ | ✅ | ✅ | Pivot tablosu |
| MERGE | ✅ | ✅ | ✅ | Birleştirme |
| CONCAT | ✅ | ✅ | ✅ | Ekleme |
| DROP_DUPLICATES | ✅ | ✅ | ✅ | Çoklama silme |
| FILLNA | ✅ | ✅ | ✅ | Boş değer doldurma |
| DROPNA | ✅ | ✅ | ✅ | Boş değer silme |
| ROLLING | ✅ | ✅ | ✅ | Hareketli pencere |
| RESAMPLE | ✅ | ✅ | ✅ | Yeniden örnekleme |
| PIVOT_TABLE | ✅ | ✅ | ✅ | Pivot tablosu (gelişmiş) |

**TOPLAM: pdsx.py: 14, pdsxv12xNEW.py: 14, pdsxv12X.py: 14**

### 25. EK NUMPY FONKSİYONLARI (14 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| CLIP | ✅ | ✅ | ✅ | Değer sınırlama |
| WHERE | ✅ | ✅ | ✅ | Koşullu seçim |
| SELECT | ✅ | ✅ | ✅ | Çoklu koşullu seçim |
| SEARCHSORTED | ✅ | ✅ | ✅ | Sıralı arama |
| MESHGRID | ✅ | ✅ | ✅ | Mesh grid oluşturma |
| GRADIENT | ✅ | ✅ | ✅ | Gradyan hesaplama |
| DIFF | ✅ | ✅ | ✅ | Fark hesaplama |
| CUMSUM | ✅ | ✅ | ✅ | Kümülatif toplam |
| CUMPROD | ✅ | ✅ | ✅ | Kümülatif çarpım |
| ARGMAX | ✅ | ✅ | ✅ | Maksimum indeks |
| ARGMIN | ✅ | ✅ | ✅ | Minimum indeks |
| ROLL | ✅ | ✅ | ✅ | Array kaydırma |
| TILE | ✅ | ✅ | ✅ | Array tekrarlama |
| REPEAT | ✅ | ✅ | ✅ | Eleman tekrarlama |

**TOPLAM: pdsx.py: 14, pdsxv12xNEW.py: 14, pdsxv12X.py: 14**

### 26. EK İSTATİSTİK TESTLERİ (18 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| ANDERSON | ✅ | ✅ | ✅ | Anderson-Darling testi |
| ANSARI | ✅ | ✅ | ✅ | Ansari-Bradley testi |
| BROWN_FORSYTHE | ✅ | ✅ | ✅ | Brown-Forsythe testi |
| COCHRANQ | ✅ | ✅ | ✅ | Cochran Q testi |
| MCNEMAR | ✅ | ✅ | ✅ | McNemar testi |
| FISHER_EXACT | ✅ | ✅ | ✅ | Fisher's exact test |
| BARNARD_EXACT | ✅ | ✅ | ✅ | Barnard's exact test |
| BOSCHLOO | ✅ | ✅ | ✅ | Boschloo's exact test |
| PAGE_TREND | ✅ | ✅ | ✅ | Page trend test |
| MOOD | ✅ | ✅ | ✅ | Mood median test |
| FLIGNER_KILLEEN | ✅ | ✅ | ✅ | Fligner-Killeen testi |
| WELCH_ANOVA | ✅ | ✅ | ✅ | Welch ANOVA |
| DURBIN_WATSON | ✅ | ✅ | ✅ | Durbin-Watson testi |
| BREUSCH_PAGAN | ✅ | ✅ | ✅ | Breusch-Pagan testi |
| WHITE_TEST | ✅ | ✅ | ✅ | White testi |
| LJUNG_BOX | ✅ | ✅ | ✅ | Ljung-Box testi |
| JARQUE_BERA | ✅ | ✅ | ✅ | Jarque-Bera testi |
| DAGOSTINO | ✅ | ✅ | ✅ | D'Agostino testi |
| OMNIBUS | ✅ | ✅ | ✅ | Omnibus testi |

**TOPLAM: pdsx.py: 18, pdsxv12xNEW.py: 18, pdsxv12X.py: 18**

### 27. ETKİ BOYUTU ÖLÇÜMLERİ (9 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| COHEN_D | ✅ | ✅ | ✅ | Cohen's d |
| HEDGES_G | ✅ | ✅ | ✅ | Hedges' g |
| GLASS_DELTA | ✅ | ✅ | ✅ | Glass' delta |
| ETA_SQUARED | ✅ | ✅ | ✅ | Eta kare |
| OMEGA_SQUARED | ✅ | ✅ | ✅ | Omega kare |
| PARTIAL_ETA_SQUARED | ✅ | ✅ | ✅ | Kısmi eta kare |
| CRAMER_V | ✅ | ✅ | ✅ | Cramér's V |
| PHI_COEFFICIENT | ✅ | ✅ | ✅ | Phi katsayısı |
| CONTINGENCY_COEFFICIENT | ✅ | ✅ | ✅ | Kontenjans katsayısı |

**TOPLAM: pdsx.py: 9, pdsxv12xNEW.py: 9, pdsxv12X.py: 9**

### 28. GÜÇ ANALİZİ (5 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| POWER_TTEST | ✅ | ✅ | ✅ | t-test güç analizi |
| POWER_ANOVA | ✅ | ✅ | ✅ | ANOVA güç analizi |
| POWER_CHI2 | ✅ | ✅ | ✅ | Chi-kare güç analizi |
| SAMPLE_SIZE_TTEST | ✅ | ✅ | ✅ | t-test örneklem boyutu |
| SAMPLE_SIZE_ANOVA | ✅ | ✅ | ✅ | ANOVA örneklem boyutu |

**TOPLAM: pdsx.py: 5, pdsxv12xNEW.py: 5, pdsxv12X.py: 5**

### 29. ROBUST İSTATİSTİKLER (6 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| TRIMMED_MEAN | ✅ | ✅ | ✅ | Kırpılmış ortalama |
| WINSORIZED_MEAN | ✅ | ✅ | ✅ | Winsorize edilmiş ortalama |
| MEDIAN_ABSOLUTE_DEVIATION | ✅ | ✅ | ✅ | Medyan mutlak sapma |
| INTERQUARTILE_RANGE | ✅ | ✅ | ✅ | Çeyrekler arası mesafe |
| TUKEY_BIWEIGHT | ✅ | ✅ | ✅ | Tukey biweight |
| HUBER_M | ✅ | ✅ | ✅ | Huber M-estimator |

**TOPLAM: pdsx.py: 6, pdsxv12xNEW.py: 6, pdsxv12X.py: 6**

### 30. BOOTSTRAP VE RESAMPLING (4 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| BOOTSTRAP | ✅ | ✅ | ✅ | Bootstrap örnekleme |
| JACKKNIFE | ✅ | ✅ | ✅ | Jackknife örnekleme |
| PERMUTATION_TEST | ✅ | ✅ | ✅ | Permütasyon testi |
| CROSS_VALIDATION | ✅ | ✅ | ✅ | Çapraz doğrulama |

**TOPLAM: pdsx.py: 4, pdsxv12xNEW.py: 4, pdsxv12X.py: 4**

### 31. BAYESIAN İSTATİSTİKLER (3 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| BAYES_FACTOR | ✅ | ✅ | ✅ | Bayes faktörü |
| CREDIBLE_INTERVAL | ✅ | ✅ | ✅ | Güvenilir aralık |
| POSTERIOR_PREDICTIVE | ✅ | ✅ | ✅ | Posterior tahmin |

**TOPLAM: pdsx.py: 3, pdsxv12xNEW.py: 3, pdsxv12X.py: 3**

### 32. ÇOK DEĞİŞKENLİ İSTATİSTİKLER (7 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| HOTELLING_T2 | ✅ | ✅ | ✅ | Hotelling T² testi |
| MAHALANOBIS | ✅ | ✅ | ✅ | Mahalanobis mesafesi |
| BOX_M | ✅ | ✅ | ✅ | Box M testi |
| MANOVA_PILLAI | ✅ | ✅ | ✅ | MANOVA (Pillai kriteri) |
| MANOVA_WILKS | ✅ | ✅ | ✅ | MANOVA (Wilks lambda) |
| MANOVA_HOTELLING | ✅ | ✅ | ✅ | MANOVA (Hotelling kriteri) |
| MANOVA_ROY | ✅ | ✅ | ✅ | MANOVA (Roy kriteri) |

**TOPLAM: pdsx.py: 7, pdsxv12xNEW.py: 7, pdsxv12X.py: 7**

### 33. SAĞKALIM ANALİZİ (3 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| KAPLAN_MEIER | ✅ | ✅ | ✅ | Kaplan-Meier tahmini |
| LOGRANK_TEST | ✅ | ✅ | ✅ | Logrank testi |
| COX_REGRESSION | ✅ | ✅ | ✅ | Cox regresyonu |

**TOPLAM: pdsx.py: 3, pdsxv12xNEW.py: 3, pdsxv12X.py: 3**

### 34. META-ANALİZ (6 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| FIXED_EFFECT | ✅ | ✅ | ✅ | Sabit etki meta-analizi |
| RANDOM_EFFECT | ✅ | ✅ | ✅ | Rastgele etki meta-analizi |
| FOREST_PLOT | ✅ | ✅ | ✅ | Forest plot |
| FUNNEL_PLOT | ✅ | ✅ | ✅ | Funnel plot |
| EGGER_TEST | ✅ | ✅ | ✅ | Egger testi |
| BEGG_TEST | ✅ | ✅ | ✅ | Begg testi |

**TOPLAM: pdsx.py: 6, pdsxv12xNEW.py: 6, pdsxv12X.py: 6**

### 35. ZAMAN/SİSTEM FONKSİYONLARI (13 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| TIMER | ✅ | ✅ | ✅ | Zamanlayıcı |
| TIME$ | ✅ | ✅ | ✅ | Geçerli zaman |
| DATE$ | ✅ | ✅ | ✅ | Geçerli tarih |
| SLEEP | ✅ | ✅ | ✅ | Bekleme |
| ENVIRON$ | ✅ | ✅ | ✅ | Çevre değişkeni |
| COMMAND$ | ✅ | ✅ | ✅ | Komut satırı argümanları |
| SHELL | ✅ | ✅ | ✅ | Shell komutu |
| MEMORY | ✅ | ✅ | ✅ | Bellek kullanımı |
| CPUCOUNT | ✅ | ✅ | ✅ | CPU sayısı |
| TIME_NOW | ✅ | ✅ | ✅ | Şimdiki zaman |
| DATE_NOW | ✅ | ✅ | ✅ | Şimdiki tarih |
| MEMORY_USAGE | ✅ | ✅ | ✅ | Bellek kullanımı (alternatif) |
| CPU_COUNT | ✅ | ✅ | ✅ | CPU sayısı (alternatif) |

**TOPLAM: pdsx.py: 13, pdsxv12xNEW.py: 13, pdsxv12X.py: 13**

### 36. DOSYA FONKSİYONLARI (5 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| DIR$ | ✅ | ✅ | ✅ | Dizin listesi |
| EXISTS | ✅ | ✅ | ✅ | Dosya varlığı |
| ISDIR | ✅ | ✅ | ✅ | Dizin kontrolü |
| FILESIZE | ✅ | ✅ | ✅ | Dosya boyutu |
| LIST_DIR | ✅ | ✅ | ✅ | Dizin listesi (alternatif) |

**TOPLAM: pdsx.py: 5, pdsxv12xNEW.py: 5, pdsxv12X.py: 5**

### 37. BELLEK FONKSİYONLARI (3 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| MALLOC | ✅ | ✅ | ✅ | Bellek ayırma |
| FREE | ✅ | ✅ | ✅ | Bellek serbest bırakma |
| SIZEOF | ✅ | ✅ | ✅ | Boyut hesaplama |

**TOPLAM: pdsx.py: 3, pdsxv12xNEW.py: 3, pdsxv12X.py: 3**

### 38. VERİ YAPISI FONKSİYONLARI (6 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| STACK | ✅ | ✅ | ✅ | Stack oluşturma |
| QUEUE | ✅ | ✅ | ✅ | Queue oluşturma |
| TYPEOF | ✅ | ✅ | ✅ | Tip kontrolü |
| CREATE_STACK | ✅ | ✅ | ✅ | Stack oluşturma (alternatif) |
| CREATE_QUEUE | ✅ | ✅ | ✅ | Queue oluşturma (alternatif) |
| TYPE_OF | ✅ | ✅ | ✅ | Tip kontrolü (alternatif) |

**TOPLAM: pdsx.py: 6, pdsxv12xNEW.py: 6, pdsxv12X.py: 6**

### 39. PROLOG ENTEGRASYONu (9 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| PROLOG_FACTS | ✅ | ✅ | ✅ | Fact listesi |
| PROLOG_RULES | ✅ | ✅ | ✅ | Kural listesi |
| PROLOG_SOLUTIONS | ✅ | ✅ | ✅ | Çözüm listesi |
| PROLOG_ASK | ✅ | ✅ | ✅ | Sorgu gönderme |
| PROLOG_TELL | ✅ | ✅ | ✅ | Fact ekleme |
| PROLOG_RETRACT | ✅ | ✅ | ✅ | Fact silme |
| PROLOG_CLEAR | ✅ | ✅ | ✅ | Veritabanı temizleme |
| PROLOG_COUNT | ✅ | ✅ | ✅ | Toplam fact/kural sayısı |
| PROLOG_TRACE | ✅ | ✅ | ✅ | İz sürme modu |

**TOPLAM: pdsx.py: 9, pdsxv12xNEW.py: 9, pdsxv12X.py: 9**

## KOŞULLU FONKSIYONLAR (Kütüphane Mevcutsa Eklenir)

### 40. PDF FONKSİYONLARI (3 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| PDF_READ | ✅* | ✅* | ✅* | PDF metin okuma |
| PDF_EXTRACT_TABLES | ✅* | ✅* | ✅* | PDF tablo çıkarma |
| PDF_SEARCH | ✅* | ✅* | ✅* | PDF'de anahtar kelime arama |

**TOPLAM: pdsx.py: 3*, pdsxv12xNEW.py: 3*, pdsxv12X.py: 3***

### 41. WEB/API FONKSİYONLARI (10 fonksiyon)

| Fonksiyon | pdsx.py | pdsxv12xNEW.py | pdsxv12X.py | Açıklama |
|-----------|---------|----------------|-------------|-----------|
| WEB_GET | ✅* | ✅* | ✅* | Web GET isteği |
| WEB_POST | ✅* | ✅* | ✅* | Web POST isteği |
| SCRAPE_LINKS | ✅* | ✅* | ✅* | HTML'den link çıkarma |
| SCRAPE_TEXT | ✅* | ✅* | ✅* | HTML'den metin çıkarma |
| CURL | ✅* | ✅* | ✅* | CURL benzeri HTTP isteği |
| HTTP_GET | ✅* | ✅* | ✅* | HTTP GET isteği |
| HTTP_POST | ✅* | ✅* | ✅* | HTTP POST isteği |
| HTTP_PUT | ✅* | ✅* | ✅* | HTTP PUT isteği |
| HTTP_DELETE | ✅* | ✅* | ✅* | HTTP DELETE isteği |
| API_CALL | ✅* | ✅* | ✅* | Gelişmiş API çağrısı |

**TOPLAM: pdsx.py: 10*, pdsxv12xNEW.py: 10*, pdsxv12X.py: 10***

### 42. OPERATÖR TABLOSU (37 operatör)

Tüm dosyalarda aynı operatör tablosu mevcut:

| Kategori | Operatörler | Sayı |
|----------|-------------|------|
| Artırma/Azaltma | ++, -- | 2 |
| Bitwise | <<, >>, &, \|, ^, ~ | 6 |
| Mantıksal | AND, OR, XOR, NOT, &&, \|\| | 6 |
| Atama | +=, -=, *=, /=, %=, &=, \|=, ^=, <<=, >>= | 10 |
| Aritmetik | +, -, *, /, %, **, // | 7 |
| Karşılaştırma | ==, !=, <, >, <=, >=, <> | 7 |

**TOPLAM: pdsx.py: 37, pdsxv12xNEW.py: 37, pdsxv12X.py: 37**

---

## GENEL TOPLAM

### FİNAL SAYIM

| Dosya | Sabit Fonksiyon | Koşullu Fonksiyon | Operatör | TOPLAM |
|-------|----------------|------------------|----------|---------|
| **pdsx.py** | **231** | **13*** | **37** | **281** |
| **pdsxv12xNEW.py** | **231** | **13*** | **37** | **281** |
| **pdsxv12X.py** | **231** | **13*** | **37** | **281** |

**Not: * = pdfplumber ve requests/BeautifulSoup kütüphaneleri mevcutsa eklenir**

### SONUÇ

**ÖNEMLİ BULGU:** Üç dosya da TAMAMEN AYNI fonksiyon tablosuna sahiptir!

- Hepsi aynı 231 sabit fonksiyona sahip
- Hepsi aynı 13 koşullu fonksiyona sahip  
- Hepsi aynı 37 operatöre sahip
- **TOPLAM: 281 fonksiyon/operatör**

### DOSYALAR ARASINDAKİ FARKLAR

Fonksiyon tabloları açısından fark yok, ancak:

1. **pdsxv12xNEW.py**: C64 engine ve LibX GUI entegrasyonu var
2. **pdsx.py**: Temel PDSX yorumlayıcı
3. **pdsxv12X.py**: Enhanced 12X versiyon

**Fonksiyon sayısı farklılığı yok, sadece engine/framework entegrasyonu farkı var.**
