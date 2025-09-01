# PDSx-BASIC Komutları ve Fonksiyonları - Decompiler Rehberi
## Disassembler'dan Gelen Kodun PDSx-BASIC'e Çevirimi İçin

### 📋 PDSx-BASIC TEMEL KOMUTLARI

#### **1. Değişken İşlemleri:**
```pdsx
LET A = 10           ; Değişken ataması
LET B$ = "HELLO"     ; String değişkeni
LET C(10) = 255      ; Array elemanı ataması
DIM A(100)           ; Array tanımı
DIM B$(50)           ; String array tanımı
```

#### **2. Ekran ve I/O Komutları:**
```pdsx
PRINT "HELLO"        ; Ekrana yazdır
PRINT A, B, C        ; Çoklu değişken yazdır
INPUT "Enter: "; A   ; Kullanıcıdan giriş al
INPUT A$             ; String girişi
POKE 1024, 65        ; Memory'ye değer yaz (A karakteri)
PEEK(1024)           ; Memory'den değer oku
```

#### **3. Program Akış Kontrolü:**
```pdsx
GOTO 100            ; Satır 100'e atla
GOSUB 200           ; Alt rutine git
RETURN              ; Alt rutinden dön
IF A > 10 THEN 150   ; Koşullu atlama
IF A = 0 THEN PRINT "ZERO"
FOR I = 1 TO 10     ; Döngü başlat
NEXT I              ; Döngü sonu
END                 ; Program sonu
STOP                ; Program durdur
```

#### **4. Data İşlemleri:**
```pdsx
DATA 10, 20, 30, "HELLO"
READ A, B, C, D$
RESTORE             ; DATA işaretçisini sıfırla
```

#### **5. Dosya İşlemleri:**
```pdsx
OPEN 1, 8, 1, "FILENAME"
PRINT#1, "DATA"
INPUT#1, A$
CLOSE 1
LOAD "PROGRAM", 8
SAVE "PROGRAM", 8
VERIFY "PROGRAM", 8
```

---

### 🔧 DECOMPILER ÇEVİRİ KURALLARI

#### **Assembly → PDSx Çevirisi:**

**1. Memory Access Çevirileri:**
```assembly
LDA $0400    →  10 PRINT CHR$(PEEK(1024))
STA $0400    →  20 POKE 1024, A
LDA #65      →  30 LET A = 65
```

**2. KERNAL Call Çevirileri:**
```assembly
JSR $FFD2    →  40 PRINT CHR$(A);    ; CHROUT
JSR $FFCF    →  50 GET A$            ; CHRIN  
JSR $FFE4    →  60 GET A$            ; GETIN
JSR $E544    →  70 PRINT CHR$(147);  ; CLRSCR (Clear screen)
```

**3. BASIC Rutinleri:**
```assembly
JSR $A871    →  80 LET L = LEN(A$)   ; String length
JSR $B7F7    →  90 LET A = VAL(A$)   ; String to number
JSR $B391    →  100 LET A$ = STR$(A) ; Number to string
```

**4. Program Flow:**
```assembly
JMP $C000    →  110 GOTO 200
JSR $C000    →  120 GOSUB 300  
RTS          →  130 RETURN
```

#### **Adres → Satır Numarası Dönüşümü:**
```python
def address_to_line_number(address):
    """Assembly adresini PDSx satır numarasına çevir"""
    base_line = 10
    increment = 10
    offset = (address - 0x0801) // 4  # BASIC start address
    return base_line + (offset * increment)
```

#### **Memory Map → PDSx Değişkenler:**
```python
MEMORY_TO_PDSX = {
    0x0400: "SCREEN_START",    # Screen memory
    0xD000: "SPRITE0_X",       # Sprite 0 X coordinate  
    0xD800: "COLOR_RAM",       # Color memory
    0x007A: "TXTPTR_LO",       # BASIC text pointer low
    0x007B: "TXTPTR_HI",       # BASIC text pointer high
}

def memory_access_to_pdsx(address, operation):
    if address in MEMORY_TO_PDSX:
        var_name = MEMORY_TO_PDSX[address]
        if operation == "LDA":
            return f"LET A = {var_name}"
        elif operation == "STA":
            return f"LET {var_name} = A"
    else:
        if operation == "LDA":
            return f"LET A = PEEK({address})"
        elif operation == "STA":
            return f"POKE {address}, A"
```

---

### 📊 PDSx-BASIC FONKSIYONLAR

#### **Matematiksel Fonksiyonlar:**
```pdsx
ABS(X)              ; Mutlak değer
ATN(X)              ; Arktanjant
COS(X)              ; Kosinüs
EXP(X)              ; e üzeri X
FRE(X)              ; Serbest bellek
INT(X)              ; Tam sayı kısmı
LOG(X)              ; Doğal logaritma
RND(X)              ; Rastgele sayı
SGN(X)              ; İşaret (-1, 0, 1)
SIN(X)              ; Sinüs
SQR(X)              ; Karekök
TAN(X)              ; Tanjant
```

#### **String Fonksiyonları:**
```pdsx
ASC(A$)             ; İlk karakterin ASCII değeri
CHR$(X)             ; ASCII'den karaktere
LEFT$(A$, N)        ; Soldan N karakter
LEN(A$)             ; String uzunluğu
MID$(A$, N, M)      ; Ortadan M karakter
RIGHT$(A$, N)       ; Sağdan N karakter
STR$(X)             ; Sayıyı stringe çevir
VAL(A$)             ; Stringi sayıya çevir
```

#### **Sistem Fonksiyonları:**
```pdsx
PEEK(ADDRESS)       ; Memory okuma
POKE ADDRESS, VALUE ; Memory yazma
USR(X)              ; Kullanıcı rutini çağır
SYS(ADDRESS)        ; Makine kodu çağır
FRE(0)              ; Serbest bellek miktarı
POS(0)              ; Cursor pozisyonu
```

---

### 🎯 DECOMPILER UYGULAMA ÖRNEKLERİ

#### **Örnek 1: Basit Program**
```assembly
; Assembly Input:
LDA #65      ; Load 'A' character
JSR $FFD2    ; Print character
RTS          ; Return

; PDSx Output:
10 REM Converted from Assembly
20 LET A = 65
30 PRINT CHR$(A);
40 END
```

#### **Örnek 2: Döngü Yapısı**
```assembly
; Assembly Input:
LDX #10      ; Loop counter
LDA #42      ; Load '*' character
JSR $FFD2    ; Print character  
DEX          ; Decrement counter
BNE $C002    ; Branch if not zero

; PDSx Output:
10 REM Loop Example
20 FOR I = 1 TO 10
30 PRINT "*";
40 NEXT I
50 END
```

#### **Örnek 3: Memory İşlemleri**
```assembly
; Assembly Input:
LDA $0400    ; Read screen memory
CMP #65      ; Compare with 'A'
BEQ $C010    ; Branch if equal
STA $D800    ; Store to color memory

; PDSx Output:
10 REM Memory Operations
20 LET A = PEEK(1024)
30 IF A = 65 THEN GOTO 60
40 POKE 55296, A
50 GOTO 70
60 REM Equal condition
70 END
```

---

### 🔧 GELİŞMİŞ ÇEVİRİ KURALLARI

#### **1. Register Simülasyonu:**
```pdsx
; A, X, Y register'ları PDSx değişkenleri olarak:
LET A = 0    ; Accumulator
LET X = 0    ; X Register  
LET Y = 0    ; Y Register
LET P = 0    ; Processor Status
LET S = 255  ; Stack Pointer
```

#### **2. Flag İşlemleri:**
```pdsx
; Processor flags simulation:
LET CARRY = 0     ; Carry flag
LET ZERO = 0      ; Zero flag  
LET NEGATIVE = 0  ; Negative flag
LET OVERFLOW = 0  ; Overflow flag
```

#### **3. Stack İşlemleri:**
```pdsx
; Stack operations:
GOSUB 9000    ; PHA (Push A)
RETURN        ; PLA (Pull A)
```

#### **4. Addressing Modes:**
```pdsx
; Immediate:     LDA #$10 → LET A = 16
; Zero Page:     LDA $10  → LET A = PEEK(16)  
; Absolute:      LDA $1000 → LET A = PEEK(4096)
; Indexed:       LDA $1000,X → LET A = PEEK(4096 + X)
; Indirect:      JMP ($1000) → GOTO PEEK(4096) + PEEK(4097) * 256
```

Bu belge sayesinde assembly kodunu PDSx-BASIC formatına dönüştürebiliriz! 🎯
