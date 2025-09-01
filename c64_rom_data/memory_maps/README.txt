C64 Memory Map Dosyaları
========================

Bu klasöre aşağıdaki dosyaları indirip koyun:

1. Genel Memory Map:
   - Dosya adı: c64_memory_map.json
   - Kaynak veriler: https://www.c64-wiki.com/wiki/Memory_Map
   - İçerik: C64'ün tam memory layout'u
   - Format: {"start_addr": {"end_addr": X, "name": "bölge_adı", "description": "açıklama"}}

2. Detaylı Memory Areas:
   - Dosya adı: memory_areas.json
   - İçerik: Her memory bölgesinin detaylı açıklaması
   - Özellikler: RAM, ROM, I/O areas

3. Special Addresses:
   - Dosya adı: special_addresses.json
   - İçerik: Özel amaçlı memory adresleri
   - Örnekler: Screen memory, color RAM, sprite pointers

Kaynak URL'ler:
- https://sta.c64.org/cbm64mem.html (Detaylı memory haritası)
- https://www.c64-wiki.com/wiki/Memory_Map (Genel yapı)

Kullanım:
- $0400-$07E7: Screen Memory -> "SCREEN[position]" 
- $D800-$DBE7: Color RAM -> "COLOR[position]"
- $D000-$D3FF: VIC-II -> "VIC.register"
