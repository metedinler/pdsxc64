| Opcode | İşlev | Adresleme Modları | C Karşılığı | QBasic Karşılığı | pdsX BASIC Karşılığı | Commodore BASIC V2 Karşılığı |
| ADC | Akkümülatöre bellekteki değeri carry ile ekle | Immediate, Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | a = a + value + carry; | LET A = A + VALUE + CARRY | LET a = a + value | A = A + VALUE + C |
| AND | Akkümülatör ile bellekteki değerin mantıksal VE'sini al | Immediate, Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | a = a & value; | LET A = A AND VALUE | LET a = a AND value | A = A AND VALUE |
| ASL | Akkümülatörü veya bellekteki değeri sola kaydır (carry'ye at) | Accumulator, Zero Page, Zero Page,X, Absolute, Absolute,X | value = value << 1; | LET VALUE = VALUE * 2 | LET value = value * 2 | VALUE = VALUE * 2 |
| BCC | Carry bayrağı temizse dallan | Relative | if (!carry) goto label; | IF CARRY = 0 THEN GOTO label | IF carry = 0 THEN GOTO label | IF NOT C THEN GOTO label |
| BCS | Carry bayrağı set ise dallan | Relative | if (carry) goto label; | IF CARRY = 1 THEN GOTO label | IF carry = 1 THEN GOTO label | IF C THEN GOTO label |
| BEQ | Sonuç sıfır ise dallan | Relative | if (zero) goto label; | IF ZERO_FLAG = 1 THEN GOTO label | IF zero = 1 THEN GOTO label | IF Z THEN GOTO label |
| BIT | Akkümülatör ile bellekteki değerin bit testi | Zero Page, Absolute | if (a & value) { /* set flags */ } | IF (A AND VALUE) THEN REM Set flags | IF a AND value THEN | IF (A AND VALUE) THEN REM Set flags |
| BMI | Negatif bayrağı set ise dallan | Relative | if (negative) goto label; | IF NEGATIVE_FLAG = 1 THEN GOTO label | IF negative = 1 THEN GOTO label | IF S THEN GOTO label |
| BNE | Sonuç sıfır değilse dallan | Relative | if (!zero) goto label; | IF ZERO_FLAG = 0 THEN GOTO label | IF zero = 0 THEN GOTO label | IF NOT Z THEN GOTO label |
| BPL | Negatif bayrağı temizse dallan | Relative | if (!negative) goto label; | IF NEGATIVE_FLAG = 0 THEN GOTO label | IF negative = 0 THEN GOTO label | IF NOT S THEN GOTO label |
| BRK | Kesme (interrupt) oluştur | Implied | exit(1); /* or trigger interrupt handler */ | END | STOP | END |
| BVC | Overflow bayrağı temizse dallan | Relative | if (!overflow) goto label; | IF OVERFLOW_FLAG = 0 THEN GOTO label | IF overflow = 0 THEN GOTO label | IF NOT V THEN GOTO label |
| BVS | Overflow bayrağı set ise dallan | Relative | if (overflow) goto label; | IF OVERFLOW_FLAG = 1 THEN GOTO label | IF overflow = 1 THEN GOTO label | IF V THEN GOTO label |
| CLC | Carry bayrağını temizle | Implied | carry = 0; | CARRY = 0 | — | REM CLC (C=0) |
| CLD | Decimal mod bayrağını temizle | Implied | decimal_mode = 0; | DECIMAL_MODE = 0 | — | REM CLD (D=0) |
| CLI | Kesme devre dışı bırakma bayrağını temizle (kesmeleri etkinleştir) | Implied | interrupt_disable = 0; | INTERRUPTS_ENABLED = 1 | — | REM CLI (I=0) |
| CLV | Overflow bayrağını temizle | Implied | overflow = 0; | OVERFLOW_FLAG = 0 | — | REM CLV (V=0) |
| CMP | Akkümülatörü bellekteki değerle karşılaştır | Immediate, Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | if (a == value) { /* set flags */ } | IF A = VALUE THEN REM Set flags | IF a = value THEN | IF A = VALUE THEN REM Set flags |
| CPX | X register'ı bellekteki değerle karşılaştır | Immediate, Zero Page, Absolute | if (x == value) { /* set flags */ } | IF XREG = VALUE THEN REM Set flags | IF x = value THEN | IF X = VALUE THEN REM Set flags |
| CPY | Y register'ı bellekteki değerle karşılaştır | Immediate, Zero Page, Absolute | if (y == value) { /* set flags */ } | IF YREG = VALUE THEN REM Set flags | IF y = value THEN | IF Y = VALUE THEN REM Set flags |
| DEC | Bellekteki değeri azalt | Zero Page, Zero Page,X, Absolute, Absolute,X | mem[address]--; | POKE ADDRESS, PEEK(ADDRESS) - 1 | POKE address, PEEK(address) - 1 | POKE ADDRESS, PEEK(ADDRESS) - 1 |
| DEX | X register'ı azalt | Implied | x--; | LET XREG = XREG - 1 | LET x = x - 1 | X = X - 1 |
| DEY | Y register'ı azalt | Implied | y--; | LET YREG = YREG - 1 | LET y = y - 1 | Y = Y - 1 |
| EOR | Akkümülatör ile bellekteki değerin mantıksal XOR'unu al | Immediate, Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | a = a ^ value; | LET A = A XOR VALUE | LET a = a XOR value | A = A XOR VALUE |
| INC | Bellekteki değeri artır | Zero Page, Zero Page,X, Absolute, Absolute,X | mem[address]++; | POKE ADDRESS, PEEK(ADDRESS) + 1 | POKE address, PEEK(address) + 1 | POKE ADDRESS, PEEK(ADDRESS) + 1 |
| INX | X register'ı artır | Implied | x++; | LET XREG = XREG + 1 | LET x = x + 1 | X = X + 1 |
| INY | Y register'ı artır | Implied | y++; | LET YREG = YREG + 1 | LET y = y + 1 | Y = Y + 1 |
| JMP | Belirtilen adrese atla | Absolute, Indirect | goto label; | GOTO label | GOTO label | GOTO label |
| JSR | Alt programa atla (mevcut adresi stack'e kaydet) | Absolute | func(); | GOSUB label | CALL func | GOSUB label |
| LDA | Akkümülatöre bellekteki değeri yükle | Immediate, Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | a = value; | LET A = VALUE | LET a = value | A = VALUE |
| LDX | X register'a bellekteki değeri yükle | Immediate, Zero Page, Zero Page,Y, Absolute, Absolute,Y | x = value; | LET XREG = VALUE | LET x = value | X = VALUE |
| LDY | Y register'a bellekteki değeri yükle | Immediate, Zero Page, Zero Page,X, Absolute, Absolute,X | y = value; | LET YREG = VALUE | LET y = value | Y = VALUE |
| LSR | Akkümülatörü veya bellekteki değeri sağa kaydır (0'ı sola ekle) | Accumulator, Zero Page, Zero Page,X, Absolute, Absolute,X | value = value >> 1; | LET VALUE = INT(VALUE / 2) | LET value = value / 2 | VALUE = INT(VALUE / 2) |
| NOP | İşlem yapma | Implied | ; | REM | — | REM |
| ORA | Akkümülatör ile bellekteki değerin mantıksal VEYA'sını al | Immediate, Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | `a = a | value;` | LET A = A OR VALUE | LET a = a OR value |
| PHA | Akkümülatörü stack'e koy | Implied | push(a); | CALL PushA(A) | PUSH a | REM PHA |
| PHP | İşlemci Durum register'ını stack'e koy | Implied | push(status_register); | CALL PushStatus(STATUS_REGISTER) | PUSH status | REM PHP |
| PLA | Stack'ten değeri Akkümülatöre al | Implied | a = pop(); | A = CALL PopA() | POP a | REM PLA |
| PLP | Stack'ten değeri İşlemci Durum register'ına al | Implied | status_register = pop(); | STATUS_REGISTER = CALL PopStatus() | POP status | REM PLP |
| ROL | Akkümülatörü veya bellekteki değeri carry ile sola döndür | Accumulator, Zero Page, Zero Page,X, Absolute, Absolute,X | `value = (value << 1) | carry;` | LET VALUE = (VALUE * 2) OR CARRY | LET value = (value * 2) + carry |
| ROR | Akkümülatörü veya bellekteki değeri carry ile sağa döndür | Accumulator, Zero Page, Zero Page,X, Absolute, Absolute,X | `value = (value >> 1) | (carry << 7);` | LET VALUE = INT(VALUE / 2) OR (CARRY * 128) | LET value = (value / 2) + (carry * 128) |
| RTI | Kesme rutininden dön | Implied | return_from_interrupt(); | RETURN_FROM_INTERRUPT | RETURN_FROM_INTERRUPT | REM RTI |
| RTS | Alt programdan dön | Implied | return; | RETURN | RETURN | RETURN |
| SBC | Akkümülatörden bellekteki değeri borrow ile çıkar | Immediate, Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | a = a - value - (1 - carry); | LET A = A - VALUE - (1 - CARRY) | LET a = a - value | A = A - VALUE - (1 - C) |
| SEC | Carry bayrağını set et | Implied | carry = 1; | CARRY = 1 | — | REM SEC (C=1) |
| SED | Decimal mod bayrağını set et | Implied | decimal_mode = 1; | DECIMAL_MODE = 1 | — | REM SED (D=1) |
| SEI | Kesme devre dışı bırakma bayrağını set et (kesmeleri devre dışı bırak) | Implied | interrupt_disable = 1; | INTERRUPTS_ENABLED = 0 | — | REM SEI (I=1) |
| STA | Akkümülatörü belleğe yaz | Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | mem[address] = a; | POKE ADDRESS, A | POKE address, a | POKE ADDRESS, A |
| STX | X register'ı belleğe yaz | Zero Page, Zero Page,Y, Absolute | mem[address] = x; | POKE ADDRESS, XREG | POKE address, x | POKE ADDRESS, X |
| STY | Y register'ı belleğe yaz | Zero Page, Zero Page,X, Absolute | mem[address] = y; | POKE ADDRESS, YREG | POKE address, y | POKE ADDRESS, Y |
| TAX | Akkümülatörü X register'a kopyala | Implied | x = a; | LET XREG = A | LET x = a | X = A |
| TAY | Akkümülatörü Y register'a kopyala | Implied | y = a; | LET YREG = A | LET y = a | Y = A |
| TSX | Stack işaretçisini X register'a kopyala | Implied | x = sp; | LET XREG = SP | LET x = sp | X = SP |
| TXA | X register'ı Akkümülatöre kopyala | Implied | a = x; | LET A = XREG | LET a = x | A = X |
| TXS | X register'ı Stack işaretçisine kopyala | Implied | sp = x; | LET SP = XREG | LET sp = x | SP = X |
| TYA | Y register'ı Akkümülatöre kopyala | Implied | a = y; | LET A = YREG | LET a = y | A = Y |
| ALR | Illegal: AND sonra LSR | Immediate | a = (a & value) >> 1; | A = INT((A AND VALUE) / 2) | LET a = (a AND value) / 2 | REM ALR (A=INT((A AND V)/2)) |
| ANC | Illegal: AND sonra C bayrağını A'nın 7. bitine ayarla | Immediate | a = a & value; carry = (a >> 7) & 1; | A = A AND VALUE : CARRY = (A AND 128) / 128 | LET a = a AND value : REM CARRY = (a AND 128) / 128 | REM ANC (A=A AND V, C=A.7) |
| ARR | Illegal: AND sonra ROR | Immediate | `a = a & value; a = (a >> 1) | (carry << 7);` | A = A AND VALUE : A = INT(A / 2) OR (CARRY * 128) | LET a = a AND value : LET a = (a / 2) + (carry * 128) |
| AXS | Illegal: (A AND X) sonucunu belleğe yaz | Immediate, Zero Page, Zero Page,Y, Absolute, Absolute,Y | mem[address] = a & x; | POKE ADDRESS, A AND XREG | POKE address, a AND x | POKE ADDRESS, A AND X |
| DCP | Illegal: Bellekteki değeri azalt sonra Akkümülatör ile karşılaştır | Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | mem[address]--; if (a == mem[address]) { /* set flags */ } | POKE ADDRESS, PEEK(ADDRESS) - 1 : IF A = PEEK(ADDRESS) THEN REM Set flags | POKE address, PEEK(address) - 1 : IF a = PEEK(address) THEN | POKE ADDR, PEEK(ADDR)-1 : REM CMP A with new value |
| ISC | Illegal: Bellekteki değeri artır sonra Akkümülatörden çıkar (borrow ile) | Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | mem[address]++; a = a - mem[address] - (1 - carry); | POKE ADDRESS, PEEK(ADDRESS) + 1 : A = A - PEEK(ADDRESS) - (1 - CARRY) | POKE address, PEEK(address) + 1 : LET a = a - PEEK(address) | POKE ADDR, PEEK(ADDR)+1 : REM SBC A with new value |
| LAX | Illegal: Bellekteki değeri Akkümülatöre ve X register'a yükle | Immediate, Zero Page, Zero Page,Y, Absolute, Absolute,Y, Indirect,X, Indirect,Y | a = value; x = value; | A = VALUE : XREG = VALUE | LET a = value : LET x = value | A = VALUE : X = VALUE |
| RLA | Illegal: Bellekteki değeri carry ile sola döndür sonra Akkümülatör ile VE'sini al | Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | `value = (value << 1) | carry; a = a & value;` | VALUE = (VALUE * 2) OR CARRY : A = A AND VALUE | LET value = (value * 2) + carry : LET a = a AND value |
| RRA | Illegal: Bellekteki değeri carry ile sağa döndür sonra Akkümülatöre ekle (carry ile) | Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | `value = (value >> 1) | (carry << 7); a = a + value + carry;` | VALUE = INT(VALUE / 2) OR (CARRY * 128) : A = A + VALUE + CARRY | LET value = (value / 2) + (carry * 128) : LET a = a + value |
| SLO | Illegal: Bellekteki değeri sola kaydır sonra Akkümülatör ile VEYA'sını al | Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | `value = value << 1; a = a | value;` | VALUE = VALUE * 2 : A = A OR VALUE | LET value = value * 2 : LET a = a OR value |
| SRE | Illegal: Bellekteki değeri sağa kaydır sonra Akkümülatör ile XOR'unu al | Zero Page, Zero Page,X, Absolute, Absolute,X, Absolute,Y, Indirect,X, Indirect,Y | value = value >> 1; a = a ^ value; | VALUE = INT(VALUE / 2) : A = A XOR VALUE | LET value = value / 2 : LET a = a XOR value | REM SRE (LSR then EOR) |
| SHX | Illegal: X register'ı belleğe yaz (adresin yüksek baytı ile AND'lenmiş) | Absolute,Y | mem[address] = x & ((address >> 8) + 1); | POKE ADDRESS, XREG AND (INT(ADDRESS / 256) + 1) | POKE address, x AND (INT(address / 256) + 1) | REM SHX (X AND (HI_ADDR+1) to MEM) |
| SHY | Illegal: Y register'ı belleğe yaz (adresin yüksek baytı ile AND'lenmiş) | Absolute,X | mem[address] = y & ((address >> 8) + 1); | POKE ADDRESS, YREG AND (INT(ADDRESS / 256) + 1) | POKE address, y AND (INT(address / 256) + 1) | REM SHY (Y AND (HI_ADDR+1) to MEM) |
| TAS | Illegal: (A AND X) sonucunu SP'ye yaz, sonra SP'yi belleğe yaz (adresin yüksek baytı ile AND'lenmiş) | Absolute,Y | sp = a & x; mem[address] = sp & ((address >> 8) + 1); | SP = A AND XREG : POKE ADDRESS, SP AND (INT(ADDRESS / 256) + 1) | LET sp = a AND x : POKE address, sp AND (INT(address / 256) + 1) | REM TAS ((A AND X) to SP, then (SP AND (HI_ADDR+1)) to MEM) |
| LAS | Illegal: Bellekteki değeri ve SP'yi AND'le, sonucu A, X ve SP'ye yükle | Absolute,Y | a = value & sp; x = a; sp = a; | VALUE = VALUE AND SP : A = VALUE : XREG = VALUE : SP = VALUE | LET value = value AND sp : LET a = value : LET x = value : LET sp = value | REM LAS ((MEM AND SP) to A,X,SP) |