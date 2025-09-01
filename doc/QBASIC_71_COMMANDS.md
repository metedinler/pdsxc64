# QBasic 7.1 Komutları ve Fonksiyonları - Decompiler Rehberi
## Assembly Kodun QBasic 7.1'e Çevirimi İçin

### 📋 QBASIC 7.1 TEMEL KOMUTLARI

#### **1. Değişken İşlemleri:**
```qbasic
DIM A AS INTEGER           ' Tamsayı değişken
DIM B AS SINGLE           ' Ondalık sayı değişken  
DIM C AS STRING           ' String değişken
DIM D AS LONG             ' Uzun tamsayı
DIM E(100) AS INTEGER     ' Tamsayı array
DIM F$(50) AS STRING      ' String array

A = 10                    ' Değer ataması
B! = 3.14                 ' Single precision
C$ = "HELLO WORLD"        ' String ataması
D& = 32000                ' Long integer
```

#### **2. Ekran ve I/O Komutları:**
```qbasic
PRINT "Hello World"       ' Ekrana yazdır
PRINT A, B, C            ' Çoklu değişken yazdır
PRINT A; B; C            ' Boşluksuz yazdır
PRINT USING "##.##"; A   ' Formatlanmış yazdır

INPUT "Enter number: ", A ' Kullanıcıdan sayı al
INPUT "Enter text: ", A$  ' Kullanıcıdan string al
LINE INPUT A$            ' Tüm satırı al

CLS                      ' Ekranı temizle
LOCATE row, col          ' Cursor konumlandır
COLOR foreground, background ' Renk ayarla
```

#### **3. Program Akış Kontrolü:**
```qbasic
' Koşullu İfadeler:
IF condition THEN
    statements
ELSEIF condition THEN  
    statements
ELSE
    statements
END IF

' Select Case:
SELECT CASE variable
CASE value1
    statements
CASE value2 TO value3
    statements  
CASE IS > value4
    statements
CASE ELSE
    statements
END SELECT

' Döngüler:
FOR I = 1 TO 10 STEP 1
    statements
NEXT I

WHILE condition
    statements
WEND

DO WHILE condition
    statements
LOOP

DO
    statements
LOOP UNTIL condition
```

#### **4. Subroutines ve Functions:**
```qbasic
' Subroutine çağrısı:
GOSUB SubroutineName
RETURN

' Function tanımı:
FUNCTION FunctionName (parameter AS type) AS type
    statements
    FunctionName = return_value
END FUNCTION

' Sub procedure tanımı:
SUB SubName (parameter AS type)
    statements
END SUB

' Program sonlandırma:
END
STOP
SYSTEM
```

#### **5. Dosya İşlemleri:**
```qbasic
OPEN "filename" FOR INPUT AS #1    ' Okuma için aç
OPEN "filename" FOR OUTPUT AS #1   ' Yazma için aç
OPEN "filename" FOR APPEND AS #1   ' Ekleme için aç

INPUT #1, variable                 ' Dosyadan oku
PRINT #1, data                     ' Dosyaya yaz
LINE INPUT #1, text$               ' Satır oku

CLOSE #1                           ' Dosya kapat
EOF(1)                             ' Dosya sonu kontrolü
```

---

### 🔧 ASSEMBLY → QBASIC ÇEVİRİ KURALLARI

#### **1. Memory Access Çevirileri:**
```assembly
; Assembly → QBasic Translation:

LDA $0400    →  A = PEEK(&H400)        ' Screen memory read
STA $0400    →  POKE &H400, A          ' Screen memory write
LDA #65      →  A = 65                 ' Immediate load
LDX #10      →  X = 10                 ' X register load
LDY #5       →  Y = 5                  ' Y register load

; Memory-mapped I/O:
LDA $D000    →  A = INP(&HD000)        ' VIC register read
STA $D000    →  OUT &HD000, A          ' VIC register write
LDA $D800    →  A = PEEK(&HD800)       ' Color RAM read
STA $D800    →  POKE &HD800, A         ' Color RAM write
```

#### **2. KERNAL Call Çevirileri:**
```assembly
; KERNAL Routines → QBasic equivalents:

JSR $FFD2    →  PRINT CHR$(A);         ' CHROUT (character output)
JSR $FFCF    →  A$ = INPUT$(1)         ' CHRIN (character input)
JSR $FFE4    →  A$ = INKEY$            ' GETIN (get key)
JSR $E544    →  CLS                    ' CLRSCR (clear screen)
JSR $FFE1    →  ' STOP key check (custom function needed)
JSR $FFBA    →  LOCATE Y + 1, X + 1    ' SETLFS (set cursor)
```

#### **3. BASIC ROM Rutinleri:**
```assembly
JSR $A871    →  L = LEN(A$)            ' String length
JSR $B7F7    →  A = VAL(A$)            ' String to number
JSR $B391    →  A$ = STR$(A)           ' Number to string
JSR $AEFD    →  A$ = CHR$(A)           ' Number to character
JSR $B79E    →  A = ASC(A$)            ' Character to number
```

#### **4. Program Flow Control:**
```assembly
JMP $C000    →  GOTO LineNumber        ' Unconditional jump
JSR $C000    →  GOSUB LineNumber       ' Subroutine call
RTS          →  RETURN                 ' Return from subroutine
BEQ $C000    →  IF A = 0 THEN GOTO LineNumber
BNE $C000    →  IF A <> 0 THEN GOTO LineNumber
BCC $C000    →  IF CARRY = 0 THEN GOTO LineNumber
BCS $C000    →  IF CARRY = 1 THEN GOTO LineNumber
```

#### **5. Arithmetic Operations:**
```assembly
CLC          →  CARRY = 0              ' Clear carry
SEC          →  CARRY = 1              ' Set carry
ADC #10      →  A = A + 10 + CARRY     ' Add with carry
SBC #5       →  A = A - 5 - (1-CARRY)  ' Subtract with borrow
INC A        →  A = A + 1              ' Increment
DEC A        →  A = A - 1              ' Decrement
ASL A        →  A = A * 2              ' Arithmetic shift left
LSR A        →  A = A \ 2              ' Logical shift right
```

---

### 📊 QBASIC 7.1 FONKSIYONLAR

#### **Matematiksel Fonksiyonlar:**
```qbasic
ABS(x)               ' Mutlak değer
ATN(x)               ' Arktanjant (radyan)
COS(x)               ' Kosinüs (radyan)
SIN(x)               ' Sinüs (radyan)  
TAN(x)               ' Tanjant (radyan)
EXP(x)               ' e üzeri x
LOG(x)               ' Doğal logaritma
SQR(x)               ' Karekök
SGN(x)               ' İşaret (-1, 0, 1)
INT(x)               ' Tam sayı kısmı
FIX(x)               ' Sıfıra doğru yuvarla
RND                  ' 0-1 arası rastgele
RANDOMIZE            ' Rastgele sayı tohumu
```

#### **String Fonksiyonları:**
```qbasic
ASC(string$)         ' İlk karakterin ASCII değeri
CHR$(ascii_code)     ' ASCII koddan karaktere
LEFT$(string$, n)    ' Soldan n karakter
RIGHT$(string$, n)   ' Sağdan n karakter  
MID$(string$, start, length) ' Ortadan karakter
LEN(string$)         ' String uzunluğu
LTRIM$(string$)      ' Sol boşlukları sil
RTRIM$(string$)      ' Sağ boşlukları sil
UCASE$(string$)      ' Büyük harfe çevir
LCASE$(string$)      ' Küçük harfe çevir
STR$(number)         ' Sayıyı stringe çevir
VAL(string$)         ' Stringi sayıya çevir
SPACE$(n)            ' n adet boşluk
STRING$(n, char$)    ' n adet karakter
INSTR(start, string$, substring$) ' Substring arama
```

#### **Sistem Fonksiyonları:**
```qbasic
PEEK(address)        ' Memory okuma
POKE address, value  ' Memory yazma
INP(port)            ' Port okuma
OUT port, value      ' Port yazma
VARPTR(variable)     ' Değişken adresi
VARSEG(variable)     ' Değişken segment
FRE(-1)              ' Serbest bellek
TIMER                ' Saniye sayacı
DATE$                ' Sistem tarihi
TIME$                ' Sistem saati
```

#### **Ekran ve Grafik Fonksiyonları:**
```qbasic
SCREEN mode          ' Grafik modu ayarla
PSET (x, y), color   ' Pixel çiz
LINE (x1, y1)-(x2, y2), color ' Çizgi çiz
CIRCLE (x, y), radius, color   ' Daire çiz
PAINT (x, y), color  ' Alan doldur
POINT(x, y)          ' Pixel rengi oku
CSRLIN               ' Cursor satırı
POS(0)               ' Cursor sütunu
```

---

### 🎯 DECOMPILER UYGULAMA ÖRNEKLERİ

#### **Örnek 1: Basit Karakter Yazdırma**
```assembly
; Assembly Input:
        LDA #65      ; Load 'A' character
        JSR $FFD2    ; Print character
        RTS          ; Return

; QBasic Output:
DIM A AS INTEGER
A = 65
PRINT CHR$(A);
END
```

#### **Örnek 2: Döngü Yapısı**
```assembly
; Assembly Input:
        LDX #10      ; Loop counter
LOOP:   LDA #42      ; Load '*' character  
        JSR $FFD2    ; Print character
        DEX          ; Decrement counter
        BNE LOOP     ; Branch if not zero
        RTS

; QBasic Output:
DIM I AS INTEGER
DIM CHAR AS INTEGER
FOR I = 1 TO 10
    CHAR = 42
    PRINT CHR$(CHAR);
NEXT I
END
```

#### **Örnek 3: Koşullu Dallanma**
```assembly
; Assembly Input:
        LDA $0400    ; Read screen memory
        CMP #65      ; Compare with 'A'
        BEQ EQUAL    ; Branch if equal
        JMP NOTEQUAL ; Jump if not equal
EQUAL:  LDA #49      ; Load '1'
        JMP DONE
NOTEQUAL: LDA #48    ; Load '0'  
DONE:   JSR $FFD2    ; Print result
        RTS

; QBasic Output:
DIM A AS INTEGER
DIM RESULT AS INTEGER
A = PEEK(&H400)
IF A = 65 THEN
    RESULT = 49
ELSE
    RESULT = 48
END IF
PRINT CHR$(RESULT);
END
```

#### **Örnek 4: Memory İşlemleri**
```assembly
; Assembly Input:
        LDA #147     ; Clear screen character
        JSR $FFD2    ; Clear screen
        LDA #1       ; White color
        STA $D800    ; Set color memory
        LDA #65      ; 'A' character
        STA $0400    ; Set screen memory
        RTS

; QBasic Output:
DIM CHAR AS INTEGER
DIM COLOR AS INTEGER
CLS                                ' Clear screen
COLOR = 1
POKE &HD800, COLOR                ' Set color
CHAR = 65  
POKE &H400, CHAR                  ' Set screen character
END
```

---

### 🔧 GELİŞMİŞ ÇEVİRİ KURALLARI

#### **1. Register Simülasyonu:**
```qbasic
' 6502 Registers as QBasic variables:
DIM A AS INTEGER      ' Accumulator (0-255)
DIM X AS INTEGER      ' X Register (0-255)
DIM Y AS INTEGER      ' Y Register (0-255)
DIM P AS INTEGER      ' Processor Status Register
DIM S AS INTEGER      ' Stack Pointer (usually 255)
DIM PC AS INTEGER     ' Program Counter

' Status Flags:
DIM CARRY AS INTEGER     ' Carry flag (0 or 1)
DIM ZERO AS INTEGER      ' Zero flag (0 or 1)
DIM NEGATIVE AS INTEGER  ' Negative flag (0 or 1)
DIM OVERFLOW AS INTEGER  ' Overflow flag (0 or 1)
DIM DECIMAL AS INTEGER   ' Decimal mode flag (0 or 1)
DIM INTERRUPT AS INTEGER ' Interrupt disable flag (0 or 1)
```

#### **2. Addressing Mode Çevirileri:**
```qbasic
' Immediate:        LDA #$10    → A = &H10
' Zero Page:        LDA $10     → A = PEEK(&H10)
' Zero Page,X:      LDA $10,X   → A = PEEK(&H10 + X)
' Absolute:         LDA $1000   → A = PEEK(&H1000)
' Absolute,X:       LDA $1000,X → A = PEEK(&H1000 + X)
' Absolute,Y:       LDA $1000,Y → A = PEEK(&H1000 + Y)
' Indirect,X:       LDA ($10,X) → A = PEEK(PEEK(&H10 + X) + PEEK(&H11 + X) * 256)
' Indirect,Y:       LDA ($10),Y → A = PEEK(PEEK(&H10) + PEEK(&H11) * 256 + Y)
```

#### **3. Stack İşlemleri:**
```qbasic
' Stack simulation:
DIM STACK(255) AS INTEGER
DIM SP AS INTEGER
SP = 255

SUB PUSH (value AS INTEGER)
    STACK(SP) = value
    SP = SP - 1
END SUB

FUNCTION PULL AS INTEGER
    SP = SP + 1
    PULL = STACK(SP)
END FUNCTION

' PHA → CALL PUSH(A)
' PLA → A = PULL
' PHP → CALL PUSH(P)
' PLP → P = PULL
```

#### **4. Branch Instruction Çevirileri:**
```qbasic
' Branch conditions:
' BEQ → IF ZERO = 1 THEN GOTO
' BNE → IF ZERO = 0 THEN GOTO  
' BCC → IF CARRY = 0 THEN GOTO
' BCS → IF CARRY = 1 THEN GOTO
' BPL → IF NEGATIVE = 0 THEN GOTO
' BMI → IF NEGATIVE = 1 THEN GOTO
' BVC → IF OVERFLOW = 0 THEN GOTO  
' BVS → IF OVERFLOW = 1 THEN GOTO
```

#### **5. Optimizasyon Önerileri:**
```qbasic
' Memory access optimization:
' Sık kullanılan adresleri değişken olarak sakla:
DIM SCREEN_START AS LONG
DIM COLOR_START AS LONG
SCREEN_START = &H400
COLOR_START = &HD800

' Döngü optimizasyonu:
' Assembly loop'ları FOR...NEXT'e çevir
' Counter register'ı döngü değişkeni yap

' Subroutine optimizasyonu:  
' JSR/RTS çiftlerini SUB/END SUB'a çevir
' Parametre geçişini global değişkenlerle simüle et
```

Bu belge sayesinde 6502 assembly kodunu QBasic 7.1'e dönüştürebiliriz! 🎯
