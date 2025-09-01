char a = 5; a = a + 3;
char a = 10; a = a - 2;
int a = 100; a = a + 50;
int a = 200; a = a - 25;
char a = 4; a = a * 2;
int a = 128; a = a / 4;
char a = 7; a = a % 3;
char a = 10; a += 5;
int a = 1000; a -= 100;
char a = 15; a *= 3;
char a = 0x0F; a = a & 0x03;
char a = 0x0A; a = a | 0x05;
char a = 0x0C; a = a ^ 0x07;
char a = 0xFF; a = ~a;
int a = 0x1234; a = a & 0x00FF;
int a = 0x5678; a = a | 0x00AA;
int a = 0xABCD; a = a ^ 0xFFFF;
char a = 1; a = a && 0;
char a = 0; a = a || 1;
char a = 5; a = !a;
char a = 8; a = a << 2;
char a = 16; a = a >> 3;
int a = 256; a = a << 4;
int a = 1024; a = a >> 2;
char a = 0x80; a = a << 1;
char a = 0x01; a = a >> 1;
int a = 0x4000; a = a << 3;
int a = 0x8000; a = a >> 4;
char a = 32; a <<= 2;
char a = 64; a >>= 1;
char a; a = 42;
int a; a = 1000;
char a = 0; a = 255;
int a = 0; a = 65535;
char a; a = a;
char b = 10; char a = b;
int a = 0; a = 1234;
char a = 99; a = a + 0;
int a = 5000; a = a - 0;
char a = 0xAA; a = a;
char a = 5; if (a == 5) a = 10;
char a = 10; if (a != 8) a = 0;
int a = 100; if (a > 50) a = 1;
int a = 25; if (a < 30) a = 2;
char a = 3; if (a <= 3) a = 4;
char a = 0; while (a < 5) a++;
char a = 10; while (a > 0) a--;
for (char a = 0; a < 3; a++) a += 1;
char a = 5; if (a) a = 0;
int a = 100; if (a >= 100) a = 50;
char a = 5; char *p = &a; *p = 10;
int a = 100; int *p = &a; *p = 200;
char a = 0; char *p = &a; a = *p;
int *p; *p = 1234;
char a = 7; char *p = &a; p++;
int test() { char a = 5; a = a + 3; return a; }
int test() { char a = 10; a = a - 2; return a; }
int test() { char a = 4; a = a * 2; return a; }
int test() { char a = 8; a = a / 2; return a; }
int test() { char a = 7; a = a % 3; return a; }
int test() { char a = 10; a += 5; return a; }
int test() { char a = 15; a -= 3; return a; }
int test() { char a = 6; a *= 4; return a; }
int test() { char a = 20; a /= 5; return a; }
int test() { char a = 9; a %= 4; return a; }
int test() { char a = 0; a = a + 1; return a; }
int test() { char a = 255; a = a - 1; return a; }
int test() { char a = 3; a = a + 10; return a; }
int test() { char a = 50; a = a - 20; return a; }
int test() { char a = 2; a = a * 8; return a; }
int test() { char a = 16; a = a / 4; return a; }
int test() { char a = 12; a += 7; return a; }
int test() { char a = 30; a -= 10; return a; }
int test() { char a = 5; a *= 5; return a; }
int test() { char a = 25; a /= 5; return a; }
int test() { char a = 0x0F; a = a & 0x03; return a; }
int test() { char a = 0x0A; a = a | 0x05; return a; }
int test() { char a = 0x0C; a = a ^ 0x07; return a; }
int test() { char a = 0xFF; a = ~a; return a; }
int test() { char a = 0xAA; a = a & 0x55; return a; }
int test() { char a = 0x33; a = a | 0xCC; return a; }
int test() { char a = 0xF0; a = a ^ 0x0F; return a; }
int test() { char a = 0x00; a = ~a; return a; }
int test() { char a = 1; a = a && 1; return a; }
int test() { char a = 0; a = a || 1; return a; }
int test() { char a = 5; a = !a; return a; }
int test() { char a = 0xFF; a = a & 0xFF; return a; }
int test() { char a = 0x00; a = a | 0xFF; return a; }
int test() { char a = 0xAA; a = a ^ 0xAA; return a; }
int test() { char a = 0x11; a = a & 0x22; return a; }
int test() { char a = 0x44; a = a | 0x88; return a; }
int test() { char a = 0x99; a = a ^ 0x66; return a; }
int test() { char a = 0x80; a = ~a; return a; }
int test() { char a = 1; a = a && 0; return a; }
int test() { char a = 0; a = a || 0; return a; }
int test() { char a = 8; a = a << 2; return a; }
int test() { char a = 16; a = a >> 3; return a; }
int test() { char a = 4; a = a << 1; return a; }
int test() { char a = 32; a = a >> 2; return a; }
int test() { char a = 0x80; a = a << 1; return a; }
int test() { char a = 0x01; a = a >> 1; return a; }
int test() { char a = 64; a = a << 3; return a; }
int test() { char a = 128; a = a >> 4; return a; }
int test() { char a = 2; a <<= 2; return a; }
int test() { char a = 8; a >>= 1; return a; }
int test() { char a = 1; a = a << 4; return a; }
int test() { char a = 16; a = a >> 5; return a; }
int test() { char a = 3; a = a << 2; return a; }
int test() { char a = 24; a = a >> 3; return a; }
int test() { char a = 0x40; a = a << 2; return a; }
int test() { char a = 0x02; a = a >> 1; return a; }
int test() { char a = 10; a = a << 1; return a; }
int test() { char a = 100; a = a >> 2; return a; }
int test() { char a = 5; a <<= 3; return a; }
int test() { char a = 20; a >>= 4; return a; }
int test() { char a = 0; a = 42; return a; }
int test() { char a = 0; a = 255; return a; }
int test() { char a = 0; a = 0; return a; }
int test() { char a = 10; a = a; return a; }
int test() { char a = 99; a = 100; return a; }
int test() { char a = 50; a = 25; return a; }
int test() { char a = 0xAA; a = 0x55; return a; }
int test() { char a = 0; a = 1; return a; }
int test() { char a = 200; a = 150; return a; }
int test() { segínt test() { char a = 5; a = 5; return a; }
int test() { char a = 7; a = 3; return a; }
int test() { char a = 0xFF; a = 0x00; return a; }
int test() { char a = 1; a = 2; return a; }
int test() { char a = 30; a = 60; return a; }
int test() { char a = 0x33; a = 0xCC; return a; }
int test() { char a = 8; a = 16; return a; }
int test() { char a = 4; a = 8; return a; }
int test() { char a = 0; a = 128; return a; }
int test() { char a = 255; a = 0; return a; }
int test() { char a = 15; a = 30; return a; }
int test() { char a = 5; char *p = &a; *p = 10; return a; }
int test() { char a = 10; char *p = &a; *p = 20; return a; }
int test() { char a = 0; char *p = &a; *p = 1; return a; }
int test() { char a = 100; char *p = &a; *p = 50; return a; }
int test() { char a = 0xFF; char *p = &a; *p = 0x00; return a; }
int test() { char a = 7; char *p = &a; a = *p; return a; }
int test() { char a = 3; char *p = &a; *p += 1; return a; }
int test() { char a = 15; char *p = &a; *p -= 2; return a; }
int test() { char a = 4; char *p = &a; *p *= 2; return a; }
int test() { char a = 8; char *p = &a; *p /= 2; return a; }
int test() { char a = 5; if (a == 5) a = 10; return a; }
int test() { char a = 10; if (a != 8) a = 0; return a; }
int test() { char a = 3; if (a < 5) a = 1; return a; }
int test() { char a = 7; if (a > 2) a = 2; return a; }
int test() { char a = 4; if (a <= 4) a = 8; return a; }
int test() { char a = 6; if (a >= 6) a = 12; return a; }
int test() { char a = 0; if (a == 0) a = 255; return a; }
int test() { char a = 15; if (a != 0) a = 30; return a; }
int test() { char a = 20; if (a > 10) a = 5; return a; }
int test() { char a = 1; if (a < 2) a = 3; return a; }
int test() { char a = 20; a = a + 7; return a; }
int test() { char a = 15; a = a - 5; return a; }
int test() { char a = 3; a = a * 3; return a; }
int test() { char a = 12; a = a / 3; return a; }
int test() { char a = 10; a = a % 4; return a; }
int test() { char a = 25; a += 10; return a; }
int test() { char a = 30; a -= 15; return a; }
int test() { char a = 4; a *= 5; return a; }
int test() { char a = 18; a /= 2; return a; }
int test() { char a = 17; a %= 5; return a; }
int test() { char a = 0xAA; a = a & 0x0F; return a; }
int test() { char a = 0x55; a = a | 0xAA; return a; }
int test() { char a = 0x33; a = a ^ 0xCC; return a; }
int test() { char a = 0x00; a = ~a; return a; }
int test() { char a = 0xF0; a = a & 0xF0; return a; }
int test() { char a = 0x0F; a = a | 0xF0; return a; }
int test() { char a = 0xA5; a = a ^ 0x5A; return a; }
int test() { char a = 1; a = a && 0; return a; }
int test() { char a = 0; a = a || 1; return a; }
int test() { char a = 10; a = !a; return a; }
int test() { char a = 16; a = a << 3; return a; }
int test() { char a = 32; a = a >> 4; return a; }
int test() { char a = 4; a = a << 2; return a; }
int test() { char a = 64; a = a >> 3; return a; }
int test() { char a = 0x08; a = a << 1; return a; }
int test() { char a = 0x80; a = a >> 1; return a; }
int test() { char a = 2; a <<= 3; return a; }
int test() { char a = 128; a >>= 2; return a; }
int test() { char a = 3; a = a << 4; return a; }
int test() { char a = 100; a = a >> 5; return a; }
int test() { char a = 0; a = 100; return a; }
int test() { char a = 255; a = 0; return a; }
int test() { char a = 50; a = 75; return a; }
int test() { char a = 0xFF; a = 0xAA; return a; }
int test() { char a = 10; a = 20; return a; }
int test() { char a = 30; a = 15; return a; }
int test() { char a = 0x11; a = 0x22; return a; }
int test() { char a = 1; a = 255; return a; }
int test() { char a = 200; a = 100; return a; }
int test() { char a = 5; a = 50; return a; }
int test() { char a = 20; char *p = &a; *p = 30; return a; }
int test() { char a = 15; char *p = &a; *p = 5; return a; }
int test() { char a = 0xAA; char *p = &a; *p = 0x55; return a; }
int test() { char a = 7; char *p = &a; *p += 3; return a; }
int test() { char a = 10; char *p = &a; *p -= 2; return a; }
int test() { char a = 8; if (a == 8) a = 16; return a; }
int test() { char a = 12; if (a != 10) a = 0; return a; }
int test() { char a = 5; if (a < 10) a = 1; return a; }
int test() { char a = 15; if (a > 5) a = 2; return a; }
int test() { char a = 3; if (a <= 3) a = 6; return a; }
int test() { char a = 7; a = a + 4; return a; }          // adc #$04
int test() { char a = 12; a = a - 3; return a; }          // sbc #$03
int test() { char a = 6; a = a * 2; return a; }           // Çarpma için yazılım rutini
int test() { char a = 15; a = a / 3; return a; }          // Bölme için yazılım rutini
int test() { char a = 11; a = a % 5; return a; }          // Mod için yazılım rutini
int test() { char a = 9; a += 6; return a; }              // adc #$06
int test() { char a = 20; a -= 8; return a; }             // sbc #$08
int test() { char a = 5; a *= 4; return a; }              // Çarpma rutini
int test() { char a = 16; a /= 2; return a; }             // Bölme rutini
int test() { char a = 13; a %= 4; return a; }             // Mod rutini
int test() { char a = 0; a = a + 1; return a; }           // adc #$01
int test() { char a = 255; a = a - 1; return a; }         // sbc #$01
int test() { char a = 8; a = a + 10; return a; }          // adc #$0A
int test() { char a = 30; a = a - 15; return a; }         // sbc #$0F
int test() { char a = 4; a = a * 3; return a; }           // Çarpma rutini
int test() { char a = 18; a = a / 6; return a; }          // Bölme rutini
int test() { char a = 14; a += 7; return a; }             // adc #$07
int test() { char a = 25; a -= 10; return a; }            // sbc #$0A
int test() { char a = 3; a *= 6; return a; }              // Çarpma rutini
int test() { char a = 24; a /= 4; return a; }             // Bölme rutini
int test() { char a = 0x1F; a = a & 0x07; return a; }     // and #$07
int test() { char a = 0x0B; a = a | 0x04; return a; }     // ora #$04
int test() { char a = 0x0D; a = a ^ 0x06; return a; }     // eor #$06
int test() { char a = 0xFF; a = ~a; return a; }           // eor #$FF
int test() { char a = 0xCC; a = a & 0x33; return a; }     // and #$33
int test() { char a = 0x22; a = a | 0xDD; return a; }     // ora #$DD
int test() { char a = 0x99; a = a ^ 0x66; return a; }     // eor #$66
int test() { char a = 0x00; a = ~a; return a; }           // eor #$FF
int test() { char a = 1; a = a && 1; return a; }          // cmp ve dallanma
int test() { char a = 0; a = a || 1; return a; }          // cmp ve dallanma
int test() { char a = 7; a = !a; return a; }              // cmp #$00, beq
int test() { char a = 0xAA; a = a & 0xF0; return a; }     // and #$F0
int test() { char a = 0x55; a = a | 0x0F; return a; }     // ora #$0F
int test() { char a = 0x3C; a = a ^ 0xC3; return a; }     // eor #$C3
int test() { char a = 0x80; a = ~a; return a; }           // eor #$FF
int test() { char a = 2; a = a && 0; return a; }          // cmp ve dallanma
int test() { char a = 0; a = a || 0; return a; }          // cmp ve dallanma
int test() { char a = 15; a = !a; return a; }             // cmp #$00, beq
int test() { char a = 0xF0; a = a & 0x0F; return a; }     // and #$0F
int test() { char a = 0x0F; a = a | 0xF0; return a; }     // ora #$F0
int test() { char a = 10; a = a << 2; return a; }         // asl a (2 kez)
int test() { char a = 20; a = a >> 3; return a; }         // lsr a (3 kez)
int test() { char a = 5; a = a << 1; return a; }          // asl a
int test() { char a = 40; a = a >> 2; return a; }         // lsr a (2 kez)
int test() { char a = 0x10; a = a << 3; return a; }       // asl a (3 kez)
int test() { char a = 0x80; a = a >> 4; return a; }       // lsr a (4 kez)
int test() { char a = 3; a <<= 2; return a; }             // asl a (2 kez)
int test() { char a = 64; a >>= 1; return a; }            // lsr a
int test() { char a = 2; a = a << 4; return a; }          // asl a (4 kez)
int test() { char a = 128; a = a >> 5; return a; }        // lsr a (5 kez)
int test() { char a = 6; a = a << 3; return a; }          // asl a (3 kez)
int test() { char a = 32; a = a >> 2; return a; }         // lsr a (2 kez)
int test() { char a = 0x20; a = a << 1; return a; }       // asl a
int test() { char a = 0x40; a = a >> 1; return a; }       // lsr a
int test() { char a = 8; a <<= 4; return a; }             // asl a (4 kez)
int test() { char a = 100; a >>= 3; return a; }           // lsr a (3 kez)
int test() { char a = 4; a = a << 2; return a; }          // asl a (2 kez)
int test() { char a = 80; a = a >> 4; return a; }         // lsr a (4 kez)
int test() { char a = 7; a = a << 5; return a; }          // asl a (5 kez)
int test() { char a = 200; a = a >> 6; return a; }        // lsr a (6 kez)
int test() { char a = 0; a = 50; return a; }              // lda #$32, sta
int test() { char a = 255; a = 0; return a; }             // lda #$00, sta
int test() { char a = 10; a = 20; return a; }             // lda #$14, sta
int test() { char a = 0xFF; a = 0xAA; return a; }         // lda #$AA, sta
int test() { char a = 30; a = 15; return a; }             // lda #$0F, sta
int test() { char a = 0x11; a = 0x22; return a; }         // lda #$22, sta
int test() { char a = 1; a = 100; return a; }             // lda #$64, sta
int test() { char a = 200; a = 150; return a; }           // lda #$96, sta
int test() { char a = 5; a = 75; return a; }              // lda #$4B, sta
int test() { char a = 0; a = 255; return a; }             // lda #$FF, sta
int test() { char a = 50; a = 25; return a; }             // lda #$19, sta
int test() { char a = 0xAA; a = 0x55; return a; }         // lda #$55, sta
int test() { char a = 15; a = 30; return a; }             // lda #$1E, sta
int test() { char a = 0x33; a = 0xCC; return a; }         // lda #$CC, sta
int test() { char a = 8; a = 16; return a; }              // lda #$10, sta
int test() { char a = 4; a = 8; return a; }               // lda #$08, sta
int test() { char a = 0; a = 128; return a; }             // lda #$80, sta
int test() { char a = 255; a = 1; return a; }             // lda #$01, sta
int test() { char a = 20; a = 40; return a; }             // lda #$28, sta
int test() { char a = 100; a = 50; return a; }            // lda #$32, sta
int test() { char a = 10; char *p = &a; *p = 20; return a; }         // lda #<a, ldx #>a, sta (ptr),y
int test() { char a = 5; char *p = &a; *p = 15; return a; }          // lda #<a, ldx #>a, sta (ptr),y
int test() { char a = 0xAA; char *p = &a; *p = 0x55; return a; }     // lda #<a, ldx #>a, sta (ptr),y
int test() { char a = 7; char *p = &a; *p += 4; return a; }          // lda (ptr),y, adc #$04
int test() { char a = 12; char *p = &a; *p -= 3; return a; }         // lda (ptr),y, sbc #$03
int test() { char a = 8; char *p = &a; *p *= 2; return a; }          // Çarpma rutini
int test() { char a = 16; char *p = &a; *p /= 2; return a; }         // Bölme rutini
int test() { char a = 0; char *p = &a; *p = 100; return a; }         // lda #<a, ldx #>a, sta (ptr),y
int test() { char a = 255; char *p = &a; *p = 0; return a; }         // lda #<a, ldx #>a, sta (ptr),y
int test() { char a = 20; char *p = &a; *p &= 0x0F; return a; }      // lda (ptr),y, and #$0F
int test() { char a = 6; if (a == 6) a = 12; return a; }             // cmp #$06, beq
int test() { char a = 10; if (a != 5) a = 0; return a; }             // cmp #$05, bne
int test() { char a = 4; if (a < 8) a = 1; return a; }               // cmp #$08, bcc
int test() { char a = 15; if (a > 10) a = 2; return a; }             // cmp #$0A, bcs
int test() { char a = 3; if (a <= 3) a = 6; return a; }              // cmp #$03, beq veya bcc
int test() { char a = 7; if (a >= 5) a = 14; return a; }             // cmp #$05, bcs
int test() { char a = 0; if (a == 0) a = 255; return a; }            // cmp #$00, beq
int test() { char a = 20; if (a != 0) a = 40; return a; }            // cmp #$00, bne
int test() { char a = 5; if (a < 10) a = 3; return a; }              // cmp #$0A, bcc
int test() { char a = 12; if (a > 8) a = 4; return a; }              // cmp #$08, bcs
int test() { char a = 5; a = (a + 2) * 3; return a; }                // adc #$02, çarpma rutini
int test() { char a = 10; a = (a - 3) & 0x0F; return a; }            // sbc #$03, and #$0F
int test() { char a = 8; a = (a << 1) | 0x01; return a; }            // asl a, ora #$01
int test() { char a = 16; a = (a >> 2) + 4; return a; }              // lsr a (2 kez), adc #$04
int test() { char a = 0xAA; a = (a & 0xF0) ^ 0x0F; return a; }       // and #$F0, eor #$0F
int test() { char a = 7; a = (a + 5) % 3; return a; }                // adc #$05, mod rutini
int test() { char a = 12; a = (a * 2) >> 1; return a; }              // çarpma rutini, lsr a
int test() { char a = 20; a = (a / 4) + 2; return a; }               // bölme rutini, adc #$02
int test() { char a = 0; a = (a | 0x10) << 2; return a; }            // ora #$10, asl a (2 kez)
int test() { char a = 255; a = (a ^ 0xFF) & 0xAA; return a; }        // eor #$FF, and #$AA
int test() { char a = 6; a = (a + 1) * 2; return a; }                // adc #$01, çarpma rutini
int test() { char a = 15; a = (a - 5) | 0x03; return a; }            // sbc #$05, ora #$03
int test() { char a = 4; a = (a << 2) & 0xF0; return a; }            // asl a (2 kez), and #$F0
int test() { char a = 32; a = (a >> 3) ^ 0x07; return a; }           // lsr a (3 kez), eor #$07
int test() { char a = 10; a = (a + 3) / 2; return a; }               // adc #$03, bölme rutini
int test() { char a = 8; a = (a * 3) % 5; return a; }                // çarpma rutini, mod rutini
int test() { char a = 0x0F; a = (a | 0xF0) >> 1; return a; }         // ora #$F0, lsr a
int test() { char a = 0xAA; a = (a & 0x55) + 1; return a; }          // and #$55, adc #$01
int test() { char a = 5; a = (a << 1) ^ 0xFF; return a; }            // asl a, eor #$FF
int test() { char a = 20; a = (a - 2) * 2; return a; }               // sbc #$02, çarpma rutini
int test1() { char a = 3; a = a + 6; return a; }           // adc #$06
int test2() { char a = 14; a = a - 4; return a; }           // sbc #$04
int test3() { char a = 7; a = a * 3; return a; }            // Çarpma rutini
int test4() { char a = 18; a = a / 3; return a; }           // Bölme rutini
int test5() { char a = 13; a = a % 4; return a; }           // Mod rutini
int test6() { char a = 8; a += 5; return a; }               // adc #$05
int test7() { char a = 22; a -= 7; return a; }              // sbc #$07
int test8() { char a = 6; a *= 2; return a; }               // Çarpma rutini
int test9() { char a = 20; a /= 4; return a; }              // Bölme rutini
int test10() { char a = 11; a %= 3; return a; }             // Mod rutini
int test11() { char a = 1; a = a + 2; return a; }           // adc #$02
int test12() { char a = 255; a = a - 2; return a; }         // sbc #$02
int test13() { char a = 9; a = a + 8; return a; }           // adc #$08
int test14() { char a = 28; a = a - 10; return a; }         // sbc #$0A
int test15() { char a = 5; a = a * 5; return a; }           // Çarpma rutini
int test16() { char a = 24; a = a / 6; return a; }          // Bölme rutini
int test17() { char a = 15; a += 9; return a; }             // adc #$09
int test18() { char a = 30; a -= 12; return a; }            // sbc #$0C
int test19() { char a = 4; a *= 4; return a; }              // Çarpma rutini
int test20() { char a = 21; a /= 3; return a; }             // Bölme rutini
int test21() { char a = 0x2F; a = a & 0x0B; return a; }     // and #$0B
int test22() { char a = 0x09; a = a | 0x06; return a; }     // ora #$06
int test23() { char a = 0x0E; a = a ^ 0x05; return a; }     // eor #$05
int test24() { char a = 0xFF; a = ~a; return a; }           // eor #$FF
int test25() { char a = 0xBB; a = a & 0x44; return a; }     // and #$44
int test26() { char a = 0x11; a = a | 0xEE; return a; }     // ora #$EE
int test27() { char a = 0x88; a = a ^ 0x77; return a; }     // eor #$77
int test28() { char a = 0x00; a = ~a; return a; }           // eor #$FF
int test29() { char a = 1; a = a && 1; return a; }          // cmp, dallanma
int test30() { char a = 0; a = a || 1; return a; }          // cmp, dallanma
int test31() { char a = 8; a = !a; return a; }              // cmp #$00, beq
int test32() { char a = 0xCC; a = a & 0xF0; return a; }     // and #$F0
int test33() { char a = 0x33; a = a | 0x0F; return a; }     // ora #$0F
int test34() { char a = 0x4B; a = a ^ 0xB4; return a; }     // eor #$B4
int test35() { char a = 0x80; a = ~a; return a; }           // eor #$FF
int test36() { char a = 2; a = a && 0; return a; }          // cmp, dallanma
int test37() { char a = 0; a = a || 0; return a; }          // cmp, dallanma
int test38() { char a = 12; a = !a; return a; }             // cmp #$00, beq
int test39() { char a = 0xE0; a = a & 0x1F; return a; }     // and #$1F
int test40() { char a = 0x1E; a = a | 0xE1; return a; }     // ora #$E1
int test41() { char a = 12; a = a << 2; return a; }         // asl a (2 kez)
int test42() { char a = 24; a = a >> 3; return a; }         // lsr a (3 kez)
int test43() { char a = 6; a = a << 1; return a; }          // asl a
int test44() { char a = 48; a = a >> 2; return a; }         // lsr a (2 kez)
int test45() { char a = 0x20; a = a << 3; return a; }       // asl a (3 kez)
int test46() { char a = 0x80; a = a >> 4; return a; }       // lsr a (4 kez)
int test47() { char a = 4; a <<= 2; return a; }             // asl a (2 kez)
int test48() { char a = 96; a >>= 1; return a; }            // lsr a
int test49() { char a = 3; a = a << 4; return a; }          // asl a (4 kez)
int test50() { char a = 192; a = a >> 5; return a; }        // lsr a (5 kez)
int test51() { char a = 7; a = a << 3; return a; }          // asl a (3 kez)
int test52() { char a = 64; a = a >> 2; return a; }         // lsr a (2 kez)
int test53() { char a = 0x10; a = a << 1; return a; }       // asl a
int test54() { char a = 0x40; a = a >> 1; return a; }       // lsr a
int test55() { char a = 9; a <<= 4; return a; }             // asl a (4 kez)
int test56() { char a = 120; a >>= 3; return a; }           // lsr a (3 kez)
int test57() { char a = 5; a = a << 2; return a; }          // asl a (2 kez)
int test58() { char a = 88; a = a >> 4; return a; }         // lsr a (4 kez)
int test59() { char a = 8; a = a << 5; return a; }          // asl a (5 kez)
int test60() { char a = 240; a = a >> 6; return a; }        // lsr a (6 kez)
int test61() { char a = 0; a = 60; return a; }              // lda #$3C, sta
int test62() { char a = 255; a = 0; return a; }             // lda #$00, sta
int test63() { char a = 12; a = 24; return a; }             // lda #$18, sta
int test64() { char a = 0xFF; a = 0xBB; return a; }         // lda #$BB, sta
int test65() { char a = 25; a = 10; return a; }             // lda #$0A, sta
int test66() { char a = 0x22; a = 0x33; return a; }         // lda #$33, sta
int test67() { char a = 2; a = 120; return a; }             // lda #$78, sta
int test68() { char a = 200; a = 140; return a; }           // lda #$8C, sta
int test69() { char a = 6; a = 80; return a; }              // lda #$50, sta
int test70() { char a = 0; a = 200; return a; }             // lda #$C8, sta
int test71() { char a = 40; a = 20; return a; }             // lda #$14, sta
int test72() { char a = 0xAA; a = 0x44; return a; }         // lda #$44, sta
int test73() { char a = 18; a = 36; return a; }             // lda #$24, sta
int test74() { char a = 0x11; a = 0xDD; return a; }         // lda #$DD, sta
int test75() { char a = 9; a = 18; return a; }              // lda #$12, sta
int test76() { char a = 5; a = 10; return a; }              // lda #$0A, sta
int test77() { char a = 0; a = 150; return a; }             // lda #$96, sta
int test78() { char a = 255; a = 2; return a; }             // lda #$02, sta
int test79() { char a = 30; a = 60; return a; }             // lda #$3C, sta
int test80() { char a = 100; a = 40; return a; }            // lda #$28, sta
int test81() { char a = 12; char *p = &a; *p = 24; return a; }     // lda #<a, ldx #>a, sta (ptr),y
int test82() { char a = 6; char *p = &a; *p = 18; return a; }       // lda #<a, ldx #>a, sta (ptr),y
int test83() { char a = 0xCC; char *p = &a; *p = 0x33; return a; }  // lda #<a, ldx #>a, sta (ptr),y
int test84() { char a = 8; char *p = &a; *p += 5; return a; }       // lda (ptr),y, adc #$05
int test85() { char a = 15; char *p = &a; *p -= 3; return a; }      // lda (ptr),y, sbc #$03
int test86() { char a = 7; char *p = &a; *p *= 2; return a; }       // Çarpma rutini
int test87() { char a = 20; char *p = &a; *p /= 2; return a; }      // Bölme rutini
int test88() { char a = 0; char *p = &a; *p = 80; return a; }       // lda #<a, ldx #>a, sta (ptr),y
int test89() { char a = 255; char *p = &a; *p = 0; return a; }      // lda #<a, ldx #>a, sta (ptr),y
int test90() { char a = 10; char *p = &a; *p &= 0x0F; return a; }   // lda (ptr),y, and #$0F
int test91() { char a = 7; if (a == 7) a = 14; return a; }         // cmp #$07, beq
int test92() { char a = 12; if (a != 6) a = 0; return a; }         // cmp #$06, bne
int test93() { char a = 5; if (a < 10) a = 2; return a; }          // cmp #$0A, bcc
int test94() { char a = 15; if (a > 5) a = 3; return a; }          // cmp #$05, bcs
int test95() { char a = 4; if (a <= 4) a = 8; return a; }          // cmp #$04, beq veya bcc
int test96() { char a = 8; if (a >= 6) a = 16; return a; }         // cmp #$06, bcs
int test97() { char a = 0; if (a == 0) a = 200; return a; }        // cmp #$00, beq
int test98() { char a = 20; if (a != 0) a = 40; return a; }        // cmp #$00, bne
int test99() { char a = 6; if (a < 12) a = 1; return a; }          // cmp #$0C, bcc
int test100() { char a = 10; if (a > 7) a = 5; return a; }         // cmp #$07, bcs
int test1() { char a = 5; if (a == 5) a = 10; return a; }          // cmp #$05, beq
int test2() { char a = 10; if (a != 8) a = 0; return a; }           // cmp #$08, bne
int test3() { char a = 3; if (a < 6) a = 1; return a; }             // cmp #$06, bcc
int test4() { char a = 7; if (a > 4) a = 2; return a; }             // cmp #$04, bcs
int test5() { char a = 4; if (a <= 4) a = 8; return a; }            // cmp #$04, beq veya bcc
int test6() { char a = 6; if (a >= 5) a = 12; return a; }           // cmp #$05, bcs
int test7() { char a = 0; if (a == 0) a = 255; return a; }          // cmp #$00, beq
int test8() { char a = 15; if (a != 0) a = 30; return a; }          // cmp #$00, bne
int test9() { char a = 8; if (a < 10) a = 3; return a; }            // cmp #$0A, bcc
int test10() { char a = 12; if (a > 6) a = 4; return a; }           // cmp #$06, bcs
int test11() { char a = 9; if (a == 9) a = 18; return a; }          // cmp #$09, beq
int test12() { char a = 20; if (a != 15) a = 5; return a; }         // cmp #$0F, bne
int test13() { char a = 2; if (a < 5) a = 1; return a; }            // cmp #$05, bcc
int test14() { char a = 10; if (a > 7) a = 2; return a; }           // cmp #$07, bcs
int test15() { char a = 3; if (a <= 3) a = 6; return a; }           // cmp #$03, beq veya bcc
int test16() { char a = 7; if (a >= 4) a = 8; return a; }           // cmp #$04, bcs
int test17() { char a = 0; if (a == 0) a = 100; return a; }         // cmp #$00, beq
int test18() { char a = 25; if (a != 0) a = 50; return a; }         // cmp #$00, bne
int test19() { char a = 6; if (a < 12) a = 2; return a; }           // cmp #$0C, bcc
int test20() { char a = 14; if (a > 8) a = 3; return a; }           // cmp #$08, bcs
int test41() { char a = 0; for (char i = 0; i < 3; i++) a += 1; return a; }     // inc, cmp #$03, bne, adc #$01
int test42() { char a = 10; for (char i = 0; i < 2; i++) a -= 1; return a; }    // inc, cmp #$02, bne, sbc #$01
int test43() { char a = 5; for (char i = 0; i < 4; i++) a += 2; return a; }     // inc, cmp #$04, bne, adc #$02
int test44() { char a = 8; for (char i = 0; i < 3; i++) a -= 2; return a; }     // inc, cmp #$03, bne, sbc #$02
int test45() { char a = 0; for (char i = 0; i < 5; i++) a += 1; return a; }     // inc, cmp #$05, bne, adc #$01
int test46() { char a = 15; for (char i = 0; i < 2; i++) a -= 3; return a; }    // inc, cmp #$02, bne, sbc #$03
int test47() { char a = 3; for (char i = 0; i < 3; i++) a += 3; return a; }     // inc, cmp #$03, bne, adc #$03
int test48() { char a = 12; for (char i = 0; i < 4; i++) a -= 1; return a; }    // inc, cmp #$04, bne, sbc #$01
int test49() { char a = 0; for (char i = 0; i < 2; i++) a += 5; return a; }     // inc, cmp #$02, bne, adc #$05
int test50() { char a = 20; for (char i = 0; i < 3; i++) a -= 2; return a; }    // inc, cmp #$03, bne, sbc #$02
int test51() { char a = 1; for (char i = 0; i < 4; i++) a += 1; return a; }     // inc, cmp #$04, bne, adc #$01
int test52() { char a = 10; for (char i = 0; i < 2; i++) a -= 4; return a; }    // inc, cmp #$02, bne, sbc #$04
int test53() { char a = 5; for (char i = 0; i < 3; i++) a += 2; return a; }     // inc, cmp #$03, bne, adc #$02
int test54() { char a = 15; for (char i = 0; i < 5; i++) a -= 1; return a; }    // inc, cmp #$05, bne, sbc #$01
int test55() { char a = 0; for (char i = 0; i < 2; i++) a += 4; return a; }     // inc, cmp #$02, bne, adc #$04
int test56() { char a = 8; for (char i = 0; i < 3; i++) a -= 3; return a; }     // inc, cmp #$03, bne, sbc #$03
int test57() { char a = 4; for (char i = 0; i < 4; i++) a += 1; return a; }     // inc, cmp #$04, bne, adc #$01
int test58() { char a = 12; for (char i = 0; i < 2; i++) a -= 2; return a; }    // inc, cmp #$02, bne, sbc #$02
int test59() { char a = 0; for (char i = 0; i < 3; i++) a += 3; return a; }     // inc, cmp #$03, bne, adc #$03
int test60() { char a = 20; for (char i = 0; i < 4; i++) a -= 1; return a; }    // inc, cmp #$04, bne, sbc #$01
int test61() { char a = 0; while (a < 3) a += 1; return a; }        // cmp #$03, bcc, adc #$01, jmp
int test62() { char a = 10; while (a > 8) a -= 1; return a; }       // cmp #$08, bcs, sbc #$01, jmp
int test63() { char a = 5; while (a < 7) a += 1; return a; }        // cmp #$07, bcc, adc #$01, jmp
int test64() { char a = 12; while (a > 10) a -= 1; return a; }      // cmp #$0A, bcs, sbc #$01, jmp
int test65() { char a = 0; while (a < 4) a += 2; return a; }        // cmp #$04, bcc, adc #$02, jmp
int test66() { char a = 15; while (a > 12) a -= 2; return a; }      // cmp #$0C, bcs, sbc #$02, jmp
int test67() { char a = 3; while (a < 6) a += 1; return a; }        // cmp #$06, bcc, adc #$01, jmp
int test68() { char a = 8; while (a > 5) a -= 1; return a; }        // cmp #$05, bcs, sbc #$01, jmp
int test69() { char a = 0; while (a < 5) a += 1; return a; }        // cmp #$05, bcc, adc #$01, jmp
int test70() { char a = 20; while (a > 15) a -= 2; return a; }      // cmp #$0F, bcs, sbc #$02, jmp
int test71() { char a = 1; while (a < 3) a += 2; return a; }        // cmp #$03, bcc, adc #$02, jmp
int test72() { char a = 10; while (a > 7) a -= 1; return a; }       // cmp #$07, bcs, sbc #$01, jmp
int test73() { char a = 5; while (a < 8) a += 1; return a; }        // cmp #$08, bcc, adc #$01, jmp
int test74() { char a = 15; while (a > 10) a -= 2; return a; }      // cmp #$0A, bcs, sbc #$02, jmp
int test75() { char a = 0; while (a < 2) a += 3; return a; }        // cmp #$02, bcc, adc #$03, jmp
int test76() { char a = 8; while (a > 4) a -= 1; return a; }        // cmp #$04, bcs, sbc #$01, jmp
int test77() { char a = 4; while (a < 6) a += 1; return a; }        // cmp #$06, bcc, adc #$01, jmp
int test78() { char a = 12; while (a > 8) a -= 2; return a; }       // cmp #$08, bcs, sbc #$02, jmp
int test79() { char a = 0; while (a < 4) a += 1; return a; }        // cmp #$04, bcc, adc #$01, jmp
int test80() { char a = 20; while (a > 16) a -= 1; return a; }      // cmp #$10, bcs, sbc #$01, jmp
int test81() { char a = 0; do { a += 1; } while (a < 3); return a; }    // adc #$01, cmp #$03, bcc, jmp
int test82() { char a = 10; do { a -= 1; } while (a > 8); return a; }   // sbc #$01, cmp #$08, bcs, jmp
int test83() { char a = 5; do { a += 1; } while (a < 7); return a; }    // adc #$01, cmp #$07, bcc, jmp
int test84() { char a = 12; do { a -= 1; } while (a > 10); return a; }  // sbc #$01, cmp #$0A, bcs, jmp
int test85() { char a = 0; do { a += 2; } while (a < 4); return a; }    // adc #$02, cmp #$04, bcc, jmp
int test86() { char a = 15; do { a -= 2; } while (a > 12); return a; }  // sbc #$02, cmp #$0C, bcs, jmp
int test87() { char a = 3; do { a += 1; } while (a < 6); return a; }    // adc #$01, cmp #$06, bcc, jmp
int test88() { char a = 8; do { a -= 1; } while (a > 5); return a; }    // sbc #$01, cmp #$05, bcs, jmp
int test89() { char a = 0; do { a += 1; } while (a < 5); return a; }    // adc #$01, cmp #$05, bcc, jmp
int test90() { char a = 20; do { a -= 2; } while (a > 15); return a; }  // sbc #$02, cmp #$0F, bcs, jmp
int test91() { char a = 1; do { a += 2; } while (a < 3); return a; }    // adc #$02, cmp #$03, bcc, jmp
int test92() { char a = 10; do { a -= 1; } while (a > 7); return a; }   // sbc #$01, cmp #$07, bcs, jmp
int test93() { char a = 5; do { a += 1; } while (a < 8); return a; }    // adc #$01, cmp #$08, bcc, jmp
int test94() { char a = 15; do { a -= 2; } while (a > 10); return a; }  // sbc #$02, cmp #$0A, bcs, jmp
int test95() { char a = 0; do { a += 3; } while (a < 2); return a; }    // adc #$03, cmp #$02, bcc, jmp
int test96() { char a = 8; do { a -= 1; } while (a > 4); return a; }    // sbc #$01, cmp #$04, bcs, jmp
int test97() { char a = 4; do { a += 1; } while (a < 6); return a; }    // adc #$01, cmp #$06, bcc, jmp
int test98() { char a = 12; do { a -= 2; } while (a > 8); return a; }   // sbc #$02, cmp #$08, bcs, jmp
int test99() { char a = 0; do { a += 1; } while (a < 4); return a; }    // adc #$01, cmp #$04, bcc, jmp
int test100() { char a = 20; do { a -= 1; } while (a > 16); return a; } // sbc #$01, cmp #$10, bcs, jmp
int test101() { char a = 1; switch (a) { case 1: a = 2; break; case 2: a = 3; break; } return a; }          // cmp #$01, beq, jmp
int test102() { char a = 2; switch (a) { case 1: a = 3; break; case 2: a = 4; break; } return a; }          // cmp #$02, beq, jmp
int test103() { char a = 3; switch (a) { case 3: a = 6; break; case 4: a = 8; break; } return a; }          // cmp #$03, beq, jmp
int test104() { char a = 4; switch (a) { case 4: a = 8; break; case 5: a = 10; break; } return a; }         // cmp #$04, beq, jmp
int test105() { char a = 5; switch (a) { case 5: a = 10; break; case 6: a = 12; break; } return a; }        // cmp #$05, beq, jmp
int test106() { char a = 6; switch (a) { case 6: a = 12; break; case 7: a = 14; break; } return a; }        // cmp #$06, beq, jmp
int test107() { char a = 7; switch (a) { case 7: a = 14; break; case 8: a = 16; break; } return a; }        // cmp #$07, beq, jmp
int test108() { char a = 8; switch (a) { case 8: a = 16; break; case 9: a = 18; break; } return a; }        // cmp #$08, beq, jmp
int test109() { char a = 9; switch (a) { case 9: a = 18; break; case 10: a = 20; break; } return a; }       // cmp #$09, beq, jmp
int test110() { char a = 10; switch (a) { case 10: a = 20; break; case 11: a = 22; break; } return a; }     // cmp #$0A, beq, jmp
int test111() { char a = 1; switch (a) { case 1: a = 3; break; case 2: a = 4; break; case 3: a = 5; break; } return a; } // cmp #$01, beq, jmp
int test112() { char a = 2; switch (a) { case 2: a = 4; break; case 3: a = 6; break; case 4: a = 8; break; } return a; } // cmp #$02, beq, jmp
int test113() { char a = 3; switch (a) { case 3: a = 6; break; case 4: a = 8; break; case 5: a = 10; break; } return a; } // cmp #$03, beq, jmp
int test114() { char a = 4; switch (a) { case 4: a = 8; break; case 5: a = 10; break; case 6: a = 12; break; } return a; } // cmp #$04, beq, jmp
int test115() { char a = 5; switch (a) { case 5: a = 10; break; case 6: a = 12; break; case 7: a = 14; break; } return a; } // cmp #$05, beq, jmp
int test116() { char a = 6; switch (a) { case 6: a = 12; break; case 7: a = 14; break; case 8: a = 16; break; } return a; } // cmp #$06, beq, jmp
int test117() { char a = 7; switch (a) { case 7: a = 14; break; case 8: a = 16; break; case 9: a = 18; break; } return a; } // cmp #$07, beq, jmp
int test118() { char a = 8; switch (a) { case 8: a = 16; break; case 9: a = 18; break; case 10: a = 20; break; } return a; } // cmp #$08, beq, jmp
int test119() { char a = 9; switch (a) { case 9: a = 18; break; case 10: a = 20; break; case 11: a = 22; break; } return a; } // cmp #$09, beq, jmp
int test120() { char a = 10; switch (a) { case 10: a = 20; break; case 11: a = 22; break; case 12: a = 24; break; } return a; } // cmp #$0A, beq, jmp













