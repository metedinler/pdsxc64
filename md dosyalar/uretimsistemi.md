# 🍎 C64 6502 Assembly → BASIC v2.0 Decompiler Üretim Sistemi
## Enhanced D64 Converter v5.3 - Tersine Mühendislik Rehberi

---

## 🎯 **DECOMPILER SİSTEMİNİN TEMEL MİMARİSİ**

### **Sistem Amacı:**
6502 assembly kodunu (disassemble edilmiş) → Commodore 64 BASIC v2.0 koduna dönüştürmek için kapsamlı decompiler sistemi

### **Temel İş Akışı:**
```
Binary Program → Disassemble → Pattern Recognition → Token Analysis → BASIC Reconstruction
```

---

## 📚 **KAYNAK MODÜL ANALİZİ VE KULLANIM ALANLARI**

### **1. TOKEN SİSTEMİ KAYNAKLARI**

#### **A) CBMBASIC Token Database**
**Kaynak:** `cbmbasic/cbmbasic.c` (satır 150-300)
**Amaç:** BASIC komutlarının binary token karşılıklarını belirlemek

**Token Tablosu Çıkarımı:**
```c
// cbmbasic.c - satır 185-250
#define TOKEN_END       0x00    // Program sonu
#define TOKEN_FOR       0x81    // FOR döngüsü
#define TOKEN_DATA      0x83    // DATA ifadesi
#define TOKEN_INPUT     0x84    // INPUT komutu
#define TOKEN_DIM       0x86    // DIM komutu (array tanımlama)
#define TOKEN_READ      0x87    // READ komutu
#define TOKEN_LET       0x88    // LET assignment
#define TOKEN_GOTO      0x89    // GOTO dallanma
#define TOKEN_RUN       0x8A    // RUN komutu
#define TOKEN_IF        0x8B    // IF koşullu
#define TOKEN_RESTORE   0x8C    // RESTORE komutu
#define TOKEN_GOSUB     0x8D    // GOSUB alt program
#define TOKEN_RETURN    0x8E    // RETURN alt programdan dönüş
#define TOKEN_REM       0x8F    // REM yorum
#define TOKEN_STOP      0x90    // STOP komutu
#define TOKEN_ON        0x91    // ON komutu
#define TOKEN_WAIT      0x92    // WAIT komutu
#define TOKEN_LOAD      0x93    // LOAD komutu
#define TOKEN_SAVE      0x94    // SAVE komutu
#define TOKEN_VERIFY    0x95    // VERIFY komutu
#define TOKEN_DEF       0x96    // DEF FN fonksiyon tanımı
#define TOKEN_POKE      0x97    // POKE memory yazma
#define TOKEN_PRINT     0x99    // PRINT ekrana yazma
#define TOKEN_CONT      0x9A    // CONT devam
#define TOKEN_LIST      0x9B    // LIST listele
#define TOKEN_CLR       0x9C    // CLR temizle
#define TOKEN_CMD       0x9D    // CMD komutu
#define TOKEN_SYS       0x9E    // SYS makine dili çağrı
#define TOKEN_OPEN      0x9F    // OPEN dosya aç
#define TOKEN_CLOSE     0xA0    // CLOSE dosya kapat
#define TOKEN_GET       0xA1    // GET karakter al
#define TOKEN_NEW       0xA2    // NEW yeni program
```

**Decompiler İçin Kullanım:**
Assembly kodunda bu token değerlerini arayarak BASIC komutlarını tanımlayacağız.

#### **B) Python Disassembler Token Patterns**
**Kaynak:** `Python Disassemblator 6502_6510/opcodes6502-6510.txt`
**Amaç:** Assembly pattern → BASIC command mapping için

---

## 🔍 **BASIC KOMUT PATTERN ANALİZİ**

### **1. PRINT KOMUTU PATTERN ANALİZİ**

#### **BASIC Kod:**
```basic
10 PRINT "HELLO WORLD"
```

#### **Tokenized Format:**
```
0A 00 99 22 48 45 4C 4C 4F 20 57 4F 52 4C 44 22 00
```
- `0A 00` = Satır numarası (10)
- `99` = PRINT token
- `22` = String başlangıç (")
- `48 45 4C 4C 4F 20 57 4F 52 4C 44` = "HELLO WORLD" ASCII
- `22` = String bitiş (")
- `00` = Satır sonu

**Kaynak Referans:** 
- `cbmbasic/cbmbasic.c` (satır 1850-1920) - PRINT komutu implementasyonu
- `Austro-Blitz-Decompiler_V32/decompilerv32.bas` (satır 250-280) - Token tanıma algoritması

#### **Assembly Pattern Recognition:**
```assembly
; PRINT komutunun assembly karşılığı
LDA #$99        ; PRINT token yükle
STA $XXXX       ; Bellek konumuna yaz
LDA #$22        ; String delimiter
STA $XXXX+1
; String karakterleri sırayla yazılır
LDA #$48        ; 'H'
STA $XXXX+2
LDA #$45        ; 'E'
STA $XXXX+3
; ... devam
```

**Decompiler Pattern:**
```python
def detect_print_pattern(assembly_bytes):
    """PRINT komutu pattern tanıma"""
    if (assembly_bytes[0] == 0xA9 and    # LDA immediate
        assembly_bytes[1] == 0x99):      # PRINT token
        return "PRINT", extract_string_literal(assembly_bytes[2:])
```

---

### **2. FOR-NEXT DÖNGÜ PATTERN ANALİZİ**

#### **BASIC Kod:**
```basic
10 FOR I=1 TO 10
20 PRINT I
30 NEXT I
```

#### **Tokenized Format:**
```
# Satır 10
0A 00 81 49 B2 31 A4 31 30 00
# Satır 20  
14 00 99 49 00
# Satır 30
1E 00 82 49 00
```

**Token Analizi:**
- `81` = FOR token
- `49` = Değişken 'I' ASCII
- `B2` = '=' assignment
- `31` = '1' ASCII
- `A4` = TO token
- `31 30` = '10' ASCII
- `82` = NEXT token

**Kaynak Referans:**
- `cbmbasic/cbmbasic.c` (satır 2100-2350) - FOR loop implementasyonu
- `64tass-src/opcodes.c` (satır 450-500) - Loop pattern definitions

#### **Assembly Pattern:**
```assembly
; FOR I=1 TO 10 assembly karşılığı
LDA #$01        ; Başlangıç değeri 1
STA $FB         ; I değişkenine ata (varsayılan $FB)
LDA #$0A        ; Bitiş değeri 10
STA $FC         ; Limit değişkenine ata

loop_start:
    ; Döngü gövdesi (PRINT I)
    LDA $FB     ; I değişkenini yükle
    JSR PRINT_NUM ; Sayı yazdır
    
    INC $FB     ; I++
    LDA $FB     ; I değerini kontrol et
    CMP $FC     ; Limit ile karşılaştır
    BCC loop_start ; Eğer küçükse devam
    BEQ loop_start ; Eğer eşitse de devam
```

**Decompiler Pattern:**
```python
def detect_for_loop_pattern(assembly_bytes):
    """FOR-NEXT döngü pattern tanıma"""
    patterns = {
        'init_sequence': [0xA9, None, 0x85, None],  # LDA #value, STA var
        'loop_increment': [0xE6, None],             # INC var
        'loop_compare': [0xA5, None, 0xC5, None],   # LDA var, CMP limit
        'loop_branch': [0x90, None]                 # BCC loop_start
    }
    
    if match_pattern_sequence(assembly_bytes, patterns):
        return extract_for_loop_structure(assembly_bytes)
```

---

### **3. IF-THEN KOŞULLU PATTERN ANALİZİ**

#### **BASIC Kod:**
```basic
10 IF A>5 THEN PRINT "BIG"
```

#### **Tokenized Format:**
```
0A 00 8B 41 B1 35 A7 99 22 42 49 47 22 00
```
- `8B` = IF token
- `41` = 'A' değişken
- `B1` = '>' karşılaştırma
- `35` = '5' sayı
- `A7` = THEN token
- `99` = PRINT token

**Kaynak Referans:**
- `cbmbasic/cbmbasic.c` (satır 2800-3000) - IF-THEN implementasyonu
- `GCC-6502-bits/tests/if_statements.c` (satır 25-50) - Koşullu derleme örnekleri

#### **Assembly Pattern:**
```assembly
; IF A>5 THEN pattern
LDA A_VAR       ; A değişkenini yükle ($xx)
CMP #$05        ; 5 ile karşılaştır
BCC skip_then   ; Eğer küçükse THEN bloğunu atla
BEQ skip_then   ; Eğer eşitse de atla

; THEN bloğu
LDA #$99        ; PRINT token
; String yazdırma kodu...

skip_then:
```

**Decompiler Pattern:**
```python
def detect_if_then_pattern(assembly_bytes):
    """IF-THEN koşullu pattern tanıma"""
    # LDA variable, CMP immediate, Branch pattern
    if (assembly_bytes[0] == 0xA5 and    # LDA zero page
        assembly_bytes[2] == 0xC9 and    # CMP immediate
        assembly_bytes[4] in [0x90, 0xB0, 0xF0, 0xD0]):  # Branch instructions
        
        variable = assembly_bytes[1]
        compare_value = assembly_bytes[3]
        branch_type = assembly_bytes[4]
        
        return construct_if_statement(variable, compare_value, branch_type)
```

---

### **4. POKE/PEEK BELLEK İŞLEMLERİ PATTERN**

#### **BASIC Kod:**
```basic
10 POKE 53280,0  ' Ekran rengi
20 A=PEEK(53280)
```

#### **Assembly Pattern:**
```assembly
; POKE 53280,0
LDA #$00        ; Değer 0
STA $D020       ; 53280 = $D020 (border color)

; A=PEEK(53280)
LDA $D020       ; Bellek konumunu oku
STA A_VAR       ; A değişkenine ata
```

**Kaynak Referans:**
- `cbmbasic/cbmbasic.c` (satır 3200-3350) - POKE/PEEK implementasyonu
- `c64_memory_map.json` - Bellek haritası referansları

**Decompiler Pattern:**
```python
def detect_poke_peek_pattern(assembly_bytes):
    """POKE/PEEK pattern tanıma"""
    # POKE pattern: LDA immediate + STA absolute
    if (assembly_bytes[0] == 0xA9 and    # LDA #value
        assembly_bytes[2] == 0x8D):      # STA absolute
        
        value = assembly_bytes[1]
        address = (assembly_bytes[4] << 8) | assembly_bytes[3]
        return f"POKE {address},{value}"
    
    # PEEK pattern: LDA absolute + STA variable
    elif (assembly_bytes[0] == 0xAD and  # LDA absolute
          assembly_bytes[3] == 0x85):    # STA zero page
        
        address = (assembly_bytes[2] << 8) | assembly_bytes[1]
        variable = assembly_bytes[4]
        return f"{get_variable_name(variable)}=PEEK({address})"
```

---

### **5. ARRAY (DIM) İŞLEMLERİ PATTERN**

#### **BASIC Kod:**
```basic
10 DIM A(10)
20 A(5)=100
30 PRINT A(5)
```

#### **Assembly Pattern:**
```assembly
; DIM A(10) - Array allocation
LDA #$0A        ; Array size 10
STA ARRAY_SIZE
JSR ALLOC_ARRAY ; Array allocation routine

; A(5)=100 - Array assignment
LDX #$05        ; Index 5
LDA #$64        ; Value 100
STA ARRAY_BASE,X ; Store in array

; PRINT A(5) - Array access
LDX #$05        ; Index 5
LDA ARRAY_BASE,X ; Load from array
JSR PRINT_NUM   ; Print number
```

**Kaynak Referans:**
- `cbmbasic/cbmbasic.c` (satır 3800-4100) - Array handling
- `Mad-Pascal-1.7.3/src/arrays.pas` (satır 100-200) - Array implementation patterns

**Decompiler Pattern:**
```python
def detect_array_pattern(assembly_bytes):
    """Array işlemleri pattern tanıma"""
    # Array allocation pattern
    if detect_alloc_array_call(assembly_bytes):
        size = assembly_bytes[1]  # LDA immediate value
        return f"DIM {get_array_name()}({size})"
    
    # Array assignment: LDX + LDA + STA indexed
    elif (assembly_bytes[0] == 0xA2 and    # LDX immediate (index)
          assembly_bytes[2] == 0xA9 and    # LDA immediate (value)
          assembly_bytes[4] == 0x9D):      # STA absolute,X
        
        index = assembly_bytes[1]
        value = assembly_bytes[3]
        array_base = (assembly_bytes[6] << 8) | assembly_bytes[5]
        return f"{get_array_name()}({index})={value}"
```

---

## 🧮 **MATEMATİKSEL İFADE PATTERN ANALİZİ**

### **1. Toplama/Çıkarma İşlemleri**

#### **BASIC Kod:**
```basic
10 A=B+C
20 D=E-F
```

#### **Assembly Pattern:**
```assembly
; A=B+C
LDA B_VAR       ; B değişkenini yükle
CLC             ; Carry flag temizle
ADC C_VAR       ; C ile topla
STA A_VAR       ; A'ya sonucu ata

; D=E-F
LDA E_VAR       ; E değişkenini yükle
SEC             ; Carry flag set (borrowing için)
SBC F_VAR       ; F'yi çıkar
STA D_VAR       ; D'ye sonucu ata
```

**Kaynak Referans:**
- `6502.org_ Source_ Fast Multiplication.html` - Matematiksel algoritma patterns
- `cbmbasic/cbmbasic.c` (satır 4500-4800) - Mathematical operations

**Decompiler Pattern:**
```python
def detect_math_operations(assembly_bytes):
    """Matematiksel işlem pattern tanıma"""
    # Addition pattern: LDA + CLC + ADC + STA
    if (assembly_bytes[0] == 0xA5 and    # LDA zero page
        assembly_bytes[2] == 0x18 and    # CLC
        assembly_bytes[3] == 0x65 and    # ADC zero page
        assembly_bytes[5] == 0x85):      # STA zero page
        
        var1 = assembly_bytes[1]
        var2 = assembly_bytes[4]
        result = assembly_bytes[6]
        return f"{get_var_name(result)}={get_var_name(var1)}+{get_var_name(var2)}"
    
    # Subtraction pattern: LDA + SEC + SBC + STA
    elif (assembly_bytes[0] == 0xA5 and  # LDA zero page
          assembly_bytes[2] == 0x38 and  # SEC
          assembly_bytes[3] == 0xE5 and  # SBC zero page
          assembly_bytes[5] == 0x85):    # STA zero page
        
        var1 = assembly_bytes[1]
        var2 = assembly_bytes[4]
        result = assembly_bytes[6]
        return f"{get_var_name(result)}={get_var_name(var1)}-{get_var_name(var2)}"
```

---

### **2. Çarpma İşlemleri (Shift-Add Algorithm)**

#### **BASIC Kod:**
```basic
10 A=B*C
```

#### **Assembly Pattern (Shift-Add Çarpma):**
```assembly
; A=B*C (8-bit multiply)
LDA #$00        ; Sonucu temizle
STA RESULT_LO
STA RESULT_HI
LDX #$08        ; 8 bit için

multiply_loop:
    LSR B_VAR   ; B'yi sağa kaydır
    BCC skip_add ; Eğer carry yoksa atla
    
    LDA RESULT_LO
    CLC
    ADC C_VAR   ; C'yi ekle
    STA RESULT_LO
    BCC no_carry
    INC RESULT_HI ; Carry varsa high byte'ı artır
    
no_carry:
skip_add:
    ASL C_VAR   ; C'yi sola kaydır (x2)
    DEX         ; Sayacı azalt
    BNE multiply_loop ; Devam et

    LDA RESULT_LO
    STA A_VAR   ; Sonucu A'ya ata
```

**Kaynak Referans:**
- `6502.org_ Source_ Fast Multiplication.html` - Optimized multiplication
- `GCC-6502-bits/tests/multiply.c` (satır 15-40) - GCC multiplication patterns

**Decompiler Pattern:**
```python
def detect_multiplication_pattern(assembly_bytes):
    """Çarpma algoritması pattern tanıma"""
    # Shift-add multiplication signature
    patterns = [
        0xA9, 0x00,  # LDA #0
        0x85, None,  # STA result
        0xA2, 0x08,  # LDX #8
        # Loop markers
        0x46, None,  # LSR variable
        0x90, None,  # BCC skip
        0x18,        # CLC
        0x65, None,  # ADC variable
        0x06, None,  # ASL variable
        0xCA,        # DEX
        0xD0, None   # BNE loop
    ]
    
    if match_pattern_sequence(assembly_bytes, patterns):
        return extract_multiply_variables(assembly_bytes)
```

---

## 📊 **DEĞİŞKEN YÖNETİMİ VE PATTERN ANALİZİ**

### **1. Sayısal Değişkenler (Integer Variables)**

#### **BASIC Değişken Sistemi:**
- A-Z: Tek karakterli integer değişkenler
- A0-Z9: İki karakterli integer değişkenler
- A(n): Integer arrays

#### **Bellek Düzeni:**
```
$FB-$FE: Floating point accumulator
$14-$18: Temporary integer storage
$0200-$03FF: Variable storage area
```

**Kaynak Referans:**
- `cbmbasic/cbmbasic.c` (satır 800-1000) - Variable storage system
- `c64_memory_map.json` - Variable memory layout

#### **Assembly Pattern:**
```assembly
; A=10
LDA #$0A        ; Değer 10
STA $14         ; A değişkeni için geçici alan

; B=A
LDA $14         ; A değişkenini oku
STA $15         ; B değişkenine ata
```

**Decompiler Pattern:**
```python
def detect_variable_assignment(assembly_bytes):
    """Değişken atama pattern tanıma"""
    # Immediate to variable: LDA #value + STA variable
    if (assembly_bytes[0] == 0xA9 and    # LDA immediate
        assembly_bytes[2] == 0x85):      # STA zero page
        
        value = assembly_bytes[1]
        var_addr = assembly_bytes[3]
        var_name = get_variable_name(var_addr)
        return f"{var_name}={value}"
    
    # Variable to variable: LDA var1 + STA var2
    elif (assembly_bytes[0] == 0xA5 and  # LDA zero page
          assembly_bytes[2] == 0x85):    # STA zero page
        
        source_var = get_variable_name(assembly_bytes[1])
        dest_var = get_variable_name(assembly_bytes[3])
        return f"{dest_var}={source_var}"
```

---

### **2. String Değişkenler**

#### **BASIC String Sistemi:**
- A$-Z$: String değişkenler
- String descriptor: 3 byte (length, low addr, high addr)

#### **Assembly Pattern:**
```assembly
; A$="HELLO"
LDA #$05        ; String uzunluğu
STA $FD         ; String descriptor length
LDA #<STRING_DATA ; String data low byte
STA $FE
LDA #>STRING_DATA ; String data high byte
STA $FF

STRING_DATA:
.byte "HELLO"
```

**Kaynak Referans:**
- `cbmbasic/cbmbasic.c` (satır 5000-5300) - String handling
- `Austro-Blitz-Decompiler_V32/decompilerv32.bas` (satır 180-220) - String detection

---

## 🔄 **DECOMPİLE PATTERN ENGINE MİMARİSİ**

### **Ana Decompiler Sınıfı:**
```python
class BasicDecompiler:
    def __init__(self):
        self.token_db = self.load_token_database()
        self.pattern_engine = PatternEngine()
        self.variable_tracker = VariableTracker()
        self.memory_map = self.load_memory_map()
    
    def decompile_assembly_to_basic(self, assembly_bytes):
        """Ana decompile fonksiyonu"""
        # 1. Token analizi
        tokens = self.extract_tokens(assembly_bytes)
        
        # 2. Pattern recognition
        patterns = self.pattern_engine.analyze(assembly_bytes)
        
        # 3. BASIC reconstruction
        basic_lines = self.reconstruct_basic(tokens, patterns)
        
        return basic_lines
```

### **Pattern Engine:**
```python
class PatternEngine:
    def __init__(self):
        self.patterns = {
            'print': PrintPattern(),
            'for_loop': ForLoopPattern(),
            'if_then': IfThenPattern(),
            'assignment': AssignmentPattern(),
            'math_ops': MathOperationsPattern(),
            'array_ops': ArrayPattern(),
            'poke_peek': PokepeekPattern()
        }
    
    def analyze(self, assembly_bytes):
        """Assembly kodunu analiz et"""
        detected_patterns = []
        
        for pattern_name, pattern_class in self.patterns.items():
            matches = pattern_class.find_matches(assembly_bytes)
            detected_patterns.extend(matches)
        
        return detected_patterns
```

---

## 🎯 **PATTERN MATCHING ALGORİTMALARI**

### **1. Sequence Pattern Matcher:**
```python
def match_pattern_sequence(assembly_bytes, pattern):
    """Dizi pattern eşleştirme"""
    pattern_pos = 0
    assembly_pos = 0
    
    while assembly_pos < len(assembly_bytes) and pattern_pos < len(pattern):
        if pattern[pattern_pos] is None:  # Wildcard
            pattern_pos += 1
            assembly_pos += 1
        elif assembly_bytes[assembly_pos] == pattern[pattern_pos]:
            pattern_pos += 1
            assembly_pos += 1
        else:
            # Pattern eşleşmedi, baştan başla
            pattern_pos = 0
            assembly_pos += 1
    
    return pattern_pos == len(pattern)
```

### **2. Token Extractor:**
```python
def extract_basic_tokens(assembly_bytes):
    """BASIC tokenlerini çıkar"""
    tokens = []
    i = 0
    
    while i < len(assembly_bytes):
        # LDA immediate pattern arama
        if assembly_bytes[i] == 0xA9:  # LDA immediate
            token_value = assembly_bytes[i + 1]
            
            if token_value in BASIC_TOKENS:
                token_name = BASIC_TOKENS[token_value]
                tokens.append({
                    'address': i,
                    'token': token_value,
                    'name': token_name
                })
        i += 1
    
    return tokens
```

---

## 📋 **DECOMPILER IMPLEMENTATION PLAN**

### **Aşama 1: Token Database Oluşturma**
**Kaynak Dosyalar:**
- `cbmbasic/cbmbasic.c` (satır 150-300) - Token definitions
- `Austro-Blitz-Decompiler_V32/decompilerv32.bas` (satır 80-110) - Compiler detection

**Görevler:**
1. Tüm BASIC token değerlerini çıkar
2. Token → komut ismi mapping oluştur
3. Derleyici imza veritabanı entegrasyonu

### **Aşama 2: Pattern Library Oluşturma**
**Kaynak Dosyalar:**
- `6502.org_ Source_ Fast Multiplication.html` - Math patterns
- `GCC-6502-bits/tests/` klasörü - Compilation patterns
- `64tass-src/opcodes.c` - Opcode patterns

**Görevler:**
1. Her BASIC komut için assembly pattern tanımla
2. Matematiksel işlem patternlerini kodla
3. Kontrol yapısı patternlerini tanımla

### **Aşama 3: Variable Tracking Sistemi**
**Kaynak Dosyalar:**
- `cbmbasic/cbmbasic.c` (satır 800-1200) - Variable management
- `c64_memory_map.json` - Memory layout

**Görevler:**
1. Değişken bellek konumlarını map et
2. Variable type detection (integer/string/array)
3. Variable lifetime tracking

### **Aşama 4: Reconstruction Engine**
**Kaynak Dosyalar:**
- `Python Disassemblator 6502_6510/Disassemblator6502_6510.py` - Disassembly logic
- `NESHLA/compiler.c` - High-level construct handling

**Görevler:**
1. Pattern → BASIC command reconstruction
2. Line number generation
3. Code formatting ve optimization

---

## 🚀 **GELİŞMİŞ DECOMPILE TEKNİKLERİ**

### **1. Derleyici İmza Tanıma (Compiler Fingerprinting)**
**Kaynak:** `Austro-Blitz-Decompiler_V32/decompilerv32.bas` (satır 80-110)

```python
def detect_compiler_signature(assembly_bytes):
    """Derleyici tipini belirle"""
    signatures = {
        0x1E88: "AustroSpeed 1E 88/Blitz",
        0x1D09: "AustroSpeed 1E v1",
        0x164B: "Austro-Comp E1",
        0x165F: "Austro-Comp E1 v2"
    }
    
    # Runtime signature kontrolü
    if len(assembly_bytes) > 0x27:
        signature = (assembly_bytes[0x27] << 8) | assembly_bytes[0x26]
        return signatures.get(signature, "Unknown Compiler")
```

### **2. Control Flow Reconstruction**
**Kaynak:** `NESHLA/compiler.c` (satır 200-400) - Control flow analysis

```python
def reconstruct_control_flow(assembly_bytes):
    """Kontrol akışını yeniden inşa et"""
    # Branch instruction analizi
    branches = find_branch_instructions(assembly_bytes)
    
    # Loop detection
    loops = detect_loop_structures(branches)
    
    # Conditional detection
    conditionals = detect_if_structures(branches)
    
    return {
        'loops': loops,
        'conditionals': conditionals,
        'subroutines': find_subroutines(assembly_bytes)
    }
```

---

## 📊 **DECOMPILER OUTPUT FORMAT**

### **Generated BASIC Code Structure:**
```basic
10 REM DECOMPILED BY ENHANCED D64 CONVERTER v5.3
20 REM ORIGINAL COMPILER: AustroSpeed 1E 88/Blitz
30 REM DECOMPILE DATE: [timestamp]
40 REM
50 FOR I=1 TO 10
60   PRINT "VALUE: ";I
70 NEXT I
80 A=PEEK(53280)
90 POKE 53280,0
100 IF A>5 THEN PRINT "BIG VALUE"
110 END
```

---

## 🎯 **SONUÇ VE UYGULAMABİLİRLİK**

Bu sistem, elimizdeki kaynakları kullanarak:

1. **Token Tablosu** (`cbmbasic/cbmbasic.c`) → BASIC komut tanıma
2. **Pattern Library** (`6502.org` math sources) → Assembly pattern recognition  
3. **Compiler Detection** (`Austro-Blitz-Decompiler`) → Derleyici özel optimizasyonlar
4. **Variable Tracking** (`c64_memory_map.json`) → Değişken yönetimi
5. **Reconstruction Engine** (Tüm kaynaklar) → BASIC kod yeniden inşası

Bu sistemle, **6502 assembly kodlarından Commodore 64 BASIC v2.0 koduna** başarılı decompile işlemi gerçekleştireceğiz! 🍎🚀

**Kritik Başarı Faktörleri:**
- Pattern matching accuracy
- Variable type detection precision  
- Control flow reconstruction quality
- Compiler-specific optimization handling

Enhanced D64 Converter v5.3 bu sistemle **dünya standartında** decompiler kapasitesine kavuşacak! 🌟
