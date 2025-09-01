#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enhanced_c64_memory_manager import enhanced_c64_memory_manager as mgr

print('=== YÜKLENEN DATABASE İSTATİSTİKLERİ ===')
print(f'KERNAL routines: {len(mgr.kernal_routines)} adet')
print(f'BASIC routines: {len(mgr.basic_routines)} adet') 
print(f'C64 Labels: {len(mgr.c64_labels)} adet')
print(f'Zero Page vars: {len(mgr.zeropage_vars)} adet')
print(f'I/O registers: {len(mgr.io_registers)} adet')
print(f'Unified lookup: {len(mgr.unified_lookup)} adet')
print()

print('=== ÖRNEK KERNAL RUTİNLERİ ===')
for addr_str, info in list(mgr.kernal_routines.items())[:10]:
    try:
        addr = int(addr_str)
        print(f'${addr:04X} → {info.get("name", "unknown")}')
    except ValueError:
        print(f'{addr_str} → {info.get("name", "unknown")} (invalid format)')
print()

print('=== ÖRNEK BASIC RUTİNLERİ ===') 
for addr_str, info in list(mgr.basic_routines.items())[:10]:
    try:
        addr = int(addr_str)
        print(f'${addr:04X} → {info.get("name", "unknown")}')
    except ValueError:
        print(f'{addr_str} → {info.get("name", "unknown")} (invalid format)')
print()

print('=== POPÜLER ADRESLER ===')
test_addresses = [0xFFD2, 0xFFCF, 0xFFE4, 0xE544, 0x0400, 0xD800]
for addr in test_addresses:
    var_name = mgr.get_smart_variable_name(addr)
    translation = mgr.get_format_translation(addr, 'c', 'read')
    print(f'${addr:04X} → {var_name} → {translation}')
