# C Dili Komutları ve Fonksiyonları - Decompiler Rehberi
## Assembly Kodun C Diline Çevirimi İçin

### 📋 C DİLİ TEMEL YAPILARI

#### **1. Değişken Tanımları:**
```c
// Temel veri tipleri:
char a;                    // 8-bit signed integer (-128 to 127)
unsigned char b;           // 8-bit unsigned integer (0 to 255)  
short c;                   // 16-bit signed integer
unsigned short d;          // 16-bit unsigned integer
int e;                     // 32-bit signed integer
unsigned int f;            // 32-bit unsigned integer
long g;                    // 32/64-bit signed integer
unsigned long h;           // 32/64-bit unsigned integer

// Array tanımları:
char buffer[256];          // 256 byte array
unsigned char memory[65536]; // 64KB memory array
int registers[8];          // Register array

// Pointer tanımları:
char *ptr;                 // Character pointer
unsigned char *mem_ptr;    // Memory pointer
void *generic_ptr;         // Generic pointer

// Sabit tanımları:
const int SCREEN_START = 0x0400;
const int COLOR_START = 0xD800;
const int BASIC_START = 0x0801;

#define SCREEN_WIDTH 40
#define SCREEN_HEIGHT 25
#define MEMORY_SIZE 65536
```

#### **2. Kontrol Yapıları:**
```c
// Koşullu ifadeler:
if (condition) {
    statements;
} else if (condition2) {
    statements;
} else {
    statements;
}

// Switch-case:
switch (variable) {
    case value1:
        statements;
        break;
    case value2:
        statements;
        break;
    default:
        statements;
        break;
}

// Döngüler:
for (int i = 0; i < 10; i++) {
    statements;
}

while (condition) {
    statements;
}

do {
    statements;
} while (condition);

// Ternary operator:
result = (condition) ? value_if_true : value_if_false;
```

#### **3. Fonksiyon Tanımları:**
```c
// Fonksiyon prototipi:
int function_name(int param1, char param2);

// Fonksiyon implementasyonu:
int add_numbers(int a, int b) {
    return a + b;
}

// Void fonksiyon:
void print_character(char c) {
    putchar(c);
}

// Pointer parametreli fonksiyon:
void modify_memory(unsigned char *address, unsigned char value) {
    *address = value;
}

// Main fonksiyon:
int main(int argc, char *argv[]) {
    // Program başlangıcı
    return 0;
}
```

#### **4. Bellek İşlemleri:**
```c
// Bellek erişimi:
unsigned char read_memory(unsigned short address) {
    return memory[address];
}

void write_memory(unsigned short address, unsigned char value) {
    memory[address] = value;
}

// Pointer aritmetiği:
ptr++;                     // Pointer'ı bir sonraki elemana taşı
ptr--;                     // Pointer'ı bir önceki elemana taşı
*ptr = value;              // Pointer'ın gösterdiği yere değer yaz
value = *ptr;              // Pointer'ın gösterdiği yerden değer oku

// Dinamik bellek yönetimi:
char *buffer = malloc(1024);   // 1KB bellek ayır
free(buffer);                  // Belleği serbest bırak
```

---

### 🔧 ASSEMBLY → C ÇEVİRİ KURALLARI

#### **1. Register Simülasyonu:**
```c
// 6502 CPU registers simulation:
typedef struct {
    unsigned char A;           // Accumulator
    unsigned char X;           // X register  
    unsigned char Y;           // Y register
    unsigned char P;           // Processor status
    unsigned char S;           // Stack pointer
    unsigned short PC;         // Program counter
} CPU_Registers;

// Status flags:
typedef struct {
    unsigned char carry:1;     // Carry flag
    unsigned char zero:1;      // Zero flag
    unsigned char interrupt:1; // Interrupt disable
    unsigned char decimal:1;   // Decimal mode
    unsigned char brk:1;       // Break flag
    unsigned char unused:1;    // Unused bit
    unsigned char overflow:1;  // Overflow flag
    unsigned char negative:1;  // Negative flag
} CPU_Flags;

CPU_Registers cpu;
CPU_Flags flags;
unsigned char memory[65536];   // 64KB memory
```

#### **2. Memory Access Çevirileri:**
```assembly
; Assembly → C Translation:

LDA $0400    →  cpu.A = memory[0x0400];           // Load from screen memory
STA $0400    →  memory[0x0400] = cpu.A;           // Store to screen memory
LDA #65      →  cpu.A = 65;                      // Immediate load
LDX #10      →  cpu.X = 10;                      // X register load
LDY #5       →  cpu.Y = 5;                       // Y register load

; Indexed addressing:
LDA $0400,X  →  cpu.A = memory[0x0400 + cpu.X];  // Absolute,X
LDA $0400,Y  →  cpu.A = memory[0x0400 + cpu.Y];  // Absolute,Y
STA $10,X    →  memory[0x10 + cpu.X] = cpu.A;    // Zero page,X
```

#### **3. KERNAL Call Çevirileri:**
```assembly
; KERNAL Routines → C function calls:

JSR $FFD2    →  putchar(cpu.A);                  // CHROUT
JSR $FFCF    →  cpu.A = getchar();               // CHRIN
JSR $FFE4    →  cpu.A = get_key();               // GETIN
JSR $E544    →  clear_screen();                  // CLRSCR
JSR $FFBA    →  set_cursor(cpu.X, cpu.Y);        // SETLFS

// Custom functions implementation:
void clear_screen(void) {
    memset(&memory[0x0400], 32, 1000);  // Fill screen with spaces
    memset(&memory[0xD800], 14, 1000);  // Set default color
}

int get_key(void) {
    // Keyboard scanning implementation
    return scan_keyboard();
}
```

#### **4. BASIC ROM Rutinleri:**
```assembly
JSR $A871    →  result = strlen(string_ptr);     // String length
JSR $B7F7    →  cpu.A = atoi(string_ptr);        // String to number
JSR $B391    →  sprintf(buffer, "%d", cpu.A);    // Number to string
JSR $AEFD    →  cpu.A = (char)cpu.A;             // Number to character
JSR $B79E    →  cpu.A = (unsigned char)*string_ptr; // Character to number
```

#### **5. Program Flow Control:**
```assembly
JMP $C000    →  goto label_C000;                 // Unconditional jump
JSR $C000    →  subroutine_C000();               // Function call
RTS          →  return;                          // Return from function
BEQ $C000    →  if (flags.zero) goto label_C000; // Branch if equal
BNE $C000    →  if (!flags.zero) goto label_C000; // Branch if not equal
BCC $C000    →  if (!flags.carry) goto label_C000; // Branch if carry clear
BCS $C000    →  if (flags.carry) goto label_C000;  // Branch if carry set
```

#### **6. Arithmetic Operations:**
```assembly
CLC          →  flags.carry = 0;                 // Clear carry
SEC          →  flags.carry = 1;                 // Set carry
ADC #10      →  cpu.A = add_with_carry(cpu.A, 10); // Add with carry
SBC #5       →  cpu.A = sub_with_borrow(cpu.A, 5);  // Subtract with borrow
INC A        →  cpu.A++; update_flags(cpu.A);    // Increment accumulator
DEC A        →  cpu.A--; update_flags(cpu.A);    // Decrement accumulator
ASL A        →  cpu.A = arithmetic_shift_left(cpu.A); // Shift left
LSR A        →  cpu.A = logical_shift_right(cpu.A);   // Shift right

// Helper functions:
unsigned char add_with_carry(unsigned char a, unsigned char b) {
    unsigned short result = a + b + flags.carry;
    flags.carry = (result > 255) ? 1 : 0;
    flags.zero = ((result & 0xFF) == 0) ? 1 : 0;
    flags.negative = ((result & 0x80) != 0) ? 1 : 0;
    return (unsigned char)(result & 0xFF);
}
```

---

### 📊 C DİLİ STANDART KÜTÜPHANE FONKSİYONLARI

#### **1. Stdio.h - Giriş/Çıkış:**
```c
#include <stdio.h>

// Karakter I/O:
int putchar(int c);           // Karakter yazdır  
int getchar(void);            // Karakter oku
int puts(const char *s);      // String yazdır
char *gets(char *s);          // String oku (deprecated)

// Formatlanmış I/O:
int printf(const char *format, ...);     // Formatlanmış yazdır
int scanf(const char *format, ...);      // Formatlanmış oku
int sprintf(char *str, const char *format, ...); // String'e formatla
int sscanf(const char *str, const char *format, ...); // String'den parse

// Dosya işlemleri:
FILE *fopen(const char *filename, const char *mode);
int fclose(FILE *stream);
int fread(void *ptr, size_t size, size_t count, FILE *stream);
int fwrite(const void *ptr, size_t size, size_t count, FILE *stream);
```

#### **2. String.h - String İşlemleri:**
```c
#include <string.h>

size_t strlen(const char *s);                    // String uzunluğu
char *strcpy(char *dest, const char *src);       // String kopyala
char *strcat(char *dest, const char *src);       // String birleştir
int strcmp(const char *s1, const char *s2);      // String karşılaştır
char *strchr(const char *s, int c);              // Karakter ara
char *strstr(const char *haystack, const char *needle); // Substring ara

void *memset(void *s, int c, size_t n);          // Bellek doldur
void *memcpy(void *dest, const void *src, size_t n); // Bellek kopyala
int memcmp(const void *s1, const void *s2, size_t n); // Bellek karşılaştır
```

#### **3. Stdlib.h - Genel Yardımcılar:**
```c
#include <stdlib.h>

// Bellek yönetimi:
void *malloc(size_t size);           // Bellek ayır
void free(void *ptr);                // Belleği serbest bırak
void *calloc(size_t count, size_t size); // Sıfırlanmış bellek ayır
void *realloc(void *ptr, size_t size);   // Bellek boyutunu değiştir

// String dönüşümleri:
int atoi(const char *str);           // String'i int'e çevir
long atol(const char *str);          // String'i long'a çevir
double atof(const char *str);        // String'i double'a çevir

// Rastgele sayılar:
int rand(void);                      // Rastgele sayı üret
void srand(unsigned int seed);       // Rastgele sayı tohumu

// Program kontrolü:
void exit(int status);               // Programı sonlandır
void abort(void);                    // Programı zorla sonlandır
```

#### **4. Math.h - Matematiksel Fonksiyonlar:**
```c
#include <math.h>

// Trigonometrik fonksiyonlar:
double sin(double x);                // Sinüs
double cos(double x);                // Kosinüs  
double tan(double x);                // Tanjant
double asin(double x);               // Arksinüs
double acos(double x);               // Arkkosinüs
double atan(double x);               // Arktanjant

// Logaritma ve üs:
double exp(double x);                // e üzeri x
double log(double x);                // Doğal logaritma
double log10(double x);              // 10 tabanında logaritma
double pow(double x, double y);      // x üzeri y
double sqrt(double x);               // Karekök

// Diğer:
double fabs(double x);               // Mutlak değer
double ceil(double x);               // Yukarı yuvarla
double floor(double x);              // Aşağı yuvarla
double fmod(double x, double y);     // Kalan işlemi
```

---

### 🎯 DECOMPILER UYGULAMA ÖRNEKLERİ

#### **Örnek 1: Basit Karakter Yazdırma**
```assembly
; Assembly Input:
        LDA #65      ; Load 'A' character  
        JSR $FFD2    ; Print character
        RTS          ; Return

; C Output:
#include <stdio.h>

int main() {
    unsigned char A;
    
    A = 65;              // LDA #65
    putchar(A);          // JSR $FFD2
    return 0;            // RTS
}
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

; C Output:
#include <stdio.h>

int main() {
    unsigned char X, A;
    
    X = 10;                    // LDX #10
    while (X != 0) {           // LOOP/BNE structure
        A = 42;                // LDA #42
        putchar(A);            // JSR $FFD2
        X--;                   // DEX
    }
    return 0;                  // RTS
}
```

#### **Örnek 3: Memory İşlemleri**
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

; C Output:
#include <stdio.h>

unsigned char memory[65536];

int main() {
    unsigned char A;
    
    A = memory[0x0400];        // LDA $0400
    if (A == 65) {             // CMP #65 / BEQ
        A = 49;                // Load '1'
    } else {
        A = 48;                // Load '0'  
    }
    putchar(A);                // JSR $FFD2
    return 0;
}
```

#### **Örnek 4: Subroutine Çağrısı**
```assembly
; Assembly Input:
MAIN:   LDA #65      ; Load parameter
        JSR PRINT_A  ; Call subroutine
        RTS          ; Return from main

PRINT_A: JSR $FFD2   ; Print character
         RTS         ; Return from subroutine

; C Output:
#include <stdio.h>

void print_character(unsigned char c) {
    putchar(c);                // JSR $FFD2
}                              // RTS

int main() {
    unsigned char A;
    
    A = 65;                    // LDA #65
    print_character(A);        // JSR PRINT_A
    return 0;                  // RTS
}
```

---

### 🔧 GELİŞMİŞ ÇEVİRİ TEKNİKLERİ

#### **1. Makro Tanımları:**
```c
// 6502 instruction simulation macros:
#define LDA_IMM(val) (cpu.A = (val))
#define LDA_ABS(addr) (cpu.A = memory[addr])
#define STA_ABS(addr) (memory[addr] = cpu.A)
#define LDX_IMM(val) (cpu.X = (val))
#define LDY_IMM(val) (cpu.Y = (val))

#define UPDATE_ZERO_FLAG(val) (flags.zero = ((val) == 0) ? 1 : 0)
#define UPDATE_NEGATIVE_FLAG(val) (flags.negative = ((val) & 0x80) ? 1 : 0)

// Memory access macros:
#define SCREEN_MEMORY(offset) memory[0x0400 + (offset)]
#define COLOR_MEMORY(offset) memory[0xD800 + (offset)]
#define BASIC_MEMORY(offset) memory[0x0801 + (offset)]
```

#### **2. Struct Kullanımı:**
```c
// C64 system simulation:
typedef struct {
    unsigned char screen[1000];    // Screen memory
    unsigned char color[1000];     // Color memory
    unsigned char basic[38000];    // BASIC memory
    unsigned char stack[256];      // Stack memory
    CPU_Registers cpu;             // CPU registers
    CPU_Flags flags;               // CPU flags
} C64_System;

C64_System c64;

// Functions for system access:
void poke_screen(int offset, unsigned char value) {
    c64.screen[offset] = value;
}

unsigned char peek_screen(int offset) {
    return c64.screen[offset];
}
```

#### **3. Function Pointer Kullanımı:**
```c
// KERNAL function table simulation:
typedef void (*kernal_function)(void);

kernal_function kernal_table[256] = {
    [0xD2] = chrout_function,      // $FFD2
    [0xCF] = chrin_function,       // $FFCF
    [0xE4] = getin_function,       // $FFE4
    // ... other KERNAL functions
};

void call_kernal(unsigned char function_code) {
    if (kernal_table[function_code]) {
        kernal_table[function_code]();
    }
}
```

#### **4. Optimizasyon İpuçları:**
```c
// İnline functions for performance:
static inline void set_zero_flag(unsigned char value) {
    flags.zero = (value == 0) ? 1 : 0;
}

static inline void set_negative_flag(unsigned char value) {
    flags.negative = (value & 0x80) ? 1 : 0;
}

// Bit manipulation macros:
#define SET_BIT(reg, bit) ((reg) |= (1 << (bit)))
#define CLEAR_BIT(reg, bit) ((reg) &= ~(1 << (bit)))
#define TEST_BIT(reg, bit) (((reg) >> (bit)) & 1)
```

Bu belge sayesinde 6502 assembly kodunu C diline profesyonel şekilde dönüştürebiliriz! 🎯
