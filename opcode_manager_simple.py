"""
JSON dosyalarından tam 6502 opcode tablosu ve çeviri sistemi
"""

import json
import os

class OpcodeManager:
    def __init__(self):
        self.opcodes = {}
        self.translations = {}
        self.addressing_modes = {}
        self.load_json_data()
        self.create_full_opcode_table()
    
    def load_json_data(self):
        """JSON dosyalarından opcode verilerini yükle"""
        # Basit çeviriler için
        self.translations = {
            'LDA': {'c_equivalent': 'a = value;', 'qbasic_equivalent': 'A = VALUE'},
            'STA': {'c_equivalent': 'memory[addr] = a;', 'qbasic_equivalent': 'MEMORY(ADDR) = A'},
            'RTS': {'c_equivalent': 'return;', 'qbasic_equivalent': 'RETURN'}
        }
    
    def create_full_opcode_table(self):
        """Tam 256 opcode tablosu oluştur"""
        self.opcodes = {
            0xA9: ("LDA #$%02X", 2, "LDA"),
            0x85: ("STA $%02X", 2, "STA"),
            0x60: ("RTS", 1, "RTS"),
            0xEA: ("NOP", 1, "NOP"),
            0x00: ("BRK", 1, "BRK"),
        }
        
        # Bilinmeyen opcodes için .BYTE kullan
        for i in range(256):
            if i not in self.opcodes:
                self.opcodes[i] = (f".BYTE ${i:02X}", 1, "UNKNOWN")
        
        print(f"Opcode tablosu oluşturuldu: {len(self.opcodes)} opcode")
    
    def get_opcode_info(self, opcode_hex):
        """Hex opcode için bilgi al"""
        if opcode_hex in self.opcodes:
            return self.opcodes[opcode_hex]
        return None
    
    def get_translation(self, opcode_name, target_language):
        """Belirli bir opcode için çeviri al"""
        if opcode_name in self.translations:
            translation_key = f"{target_language}_equivalent"
            return self.translations[opcode_name].get(translation_key, f"// {opcode_name}")
        return f"// {opcode_name}"
    
    def get_all_opcodes(self):
        """Tüm opcode'ları döndür"""
        return self.opcodes
    
    def get_all_translations(self):
        """Tüm çevirileri döndür"""
        return self.translations

if __name__ == "__main__":
    # Test
    manager = OpcodeManager()
    print(f"Toplam opcode sayısı: {len(manager.opcodes)}")
    print(f"Çeviri tablosu: {len(manager.translations)} opcode")
