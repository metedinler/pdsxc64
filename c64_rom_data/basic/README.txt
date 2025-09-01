C64 BASIC ROM Disassembly Dosyaları
=====================================

Bu klasöre aşağıdaki dosyaları indirip koyun:

1. BASIC ROM Disassembly:
   - Dosya adı: basic.asm veya basic-disasm.txt
   - Kaynak: https://github.com/mist64/c64rom/blob/master/basic.s
   - İçerik: C64 BASIC interpreter'ın tam disassembly kodu
   - Kullanım: BASIC komutları tanıma ve çeviri için

2. BASIC Token Tablosu:
   - Dosya adı: basic_tokens.json
   - İçerik: BASIC keyword'lerin token değerleri
   - Format: {"token_value": "keyword", ...}

3. BASIC Rutinleri:
   - Dosya adı: basic_routines.json
   - İçerik: BASIC fonksiyonlarının adresleri ve açıklamaları
   - Format: {"address": {"name": "routine_name", "description": "açıklama"}}

Örnek Kullanım:
- $A871 adresinde STRING LENGTH rutini çağrıldığında
- Decompiler bu bilgiyi kullanarak "LEN(string)" çevirisi yapacak
