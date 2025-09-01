#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def add_pseudo_equivalents():
    """opcode_map.json dosyasına pseudo_equivalent alanı ekle"""
    
    json_path = 'opcode_map.json'
    
    # Dosyayı yükle
    with open(json_path, 'r', encoding='utf-8') as f:
        opcodes = json.load(f)
    
    # Her opcode için pseudo_equivalent ekle
    for opcode in opcodes:
        if 'pseudo_equivalent' not in opcode:
            # C equivalent'i varsa onu kullan, yoksa basit bir çeviri yap
            c_equiv = opcode.get('c_equivalent', '')
            if c_equiv:
                # C syntax'ından pseudo syntax'a çevir
                pseudo = c_equiv.replace('mem[address]', 'memory[addr]')
                pseudo = pseudo.replace('mem[', 'memory[')
                pseudo = pseudo.replace('];', ']')
                pseudo = pseudo.replace(';', '')
                pseudo = pseudo.replace('goto', 'jump to')
                pseudo = pseudo.replace('if (', 'if ')
                pseudo = pseudo.replace(')', '')
                pseudo = pseudo.replace('{', ':')
                pseudo = pseudo.replace('}', '')
                pseudo = pseudo.replace('/* ', '')
                pseudo = pseudo.replace(' */', '')
                pseudo = pseudo.replace('//', '')
                pseudo = pseudo.strip()
                
                if not pseudo:
                    pseudo = f"// {opcode['opcode']}"
                    
                opcode['pseudo_equivalent'] = pseudo
            else:
                opcode['pseudo_equivalent'] = f"// {opcode['opcode']}"
    
    # Dosyayı kaydet
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(opcodes, f, ensure_ascii=False, indent=4)
    
    print(f"pseudo_equivalent alanı {len(opcodes)} opcode için eklendi")

if __name__ == "__main__":
    add_pseudo_equivalents()
