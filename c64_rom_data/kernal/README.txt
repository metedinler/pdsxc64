C64 KERNAL ROM Disassembly Dosyaları
=====================================

Bu klasöre aşağıdaki dosyaları indirip koyun:

1. KERNAL ROM Disassembly:
   - Dosya adı: kernal.asm veya kernal-disasm.txt
   - Kaynak: https://github.com/mist64/c64rom/blob/master/kernal.s
   - İçerik: C64 KERNAL'ın tam disassembly kodu
   - Kullanım: System call'ları tanıma ve çeviri için

2. KERNAL Rutinleri:
   - Dosya adı: kernal_routines.json
   - İçerik: KERNAL fonksiyonlarının adresleri ve açıklamaları
   - Format: {"address": {"name": "routine_name", "description": "açıklama", "parameters": []}}

3. I/O Register Map:
   - Dosya adı: io_registers.json
   - İçerik: I/O registerlarının adresleri ve işlevleri
   - Format: {"address": {"name": "register_name", "bits": {...}}}

Örnek KERNAL Çağrıları:
- $FFD2 (CHROUT) -> print_char() çevirisi
- $FFCF (CHRIN) -> input_char() çevirisi
- $FFE4 (GETIN) -> get_key() çevirisi

Ekran Silme Örneği:
- JSR $E544 (CLRSCR) -> clear_screen() çevirisi
- "C64 KERNAL'den ekran silme rutini çağrıldı"
