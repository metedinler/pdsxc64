C64 Zero Page Dosyaları
======================

Bu klasöre aşağıdaki dosyaları indirip koyun:

1. Zero Page Variables:
   - Dosya adı: zeropage_vars.json
   - Kaynak: https://www.c64-wiki.com/wiki/Zeropage
   - İçerik: $00-$FF zero page değişkenlerinin tanımları
   - Format: {"address": {"name": "var_name", "size": X, "description": "açıklama", "usage": "kullanım"}}

2. System Pointers:
   - Dosya adı: system_pointers.json
   - İçerik: BASIC ve KERNAL sistem pointer'ları
   - Örnekler: TXTTAB, VARTAB, ARYTAB

3. User Variables:
   - Dosya adı: user_zeropage.json
   - İçerik: Kullanıcının kullanabileceği zero page adresleri
   - Adresler: $02, $03, $05-$8F (free for user)

4. Special pointers

Önemli Zero Page Adresleri:
- $00-$01: Processor port and data direction
- $02-$8F: Free for user programs
- $90-$FF: KERNAL and BASIC workspace

Decompiler Kullanımı:
- LDA $02 -> "user_var1 = A" (eğer $02 kullanıcı değişkeni ise)
- LDA $91 -> "status = A" (KERNAL STATUS register)
- LDA $7A -> "basic_ptr = A" (BASIC text pointer)

Bit Haritaları:
- $00: Processor port (bits 0-2: memory configuration)
- $01: Data direction register
