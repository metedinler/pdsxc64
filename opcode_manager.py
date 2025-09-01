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
        try:
            # Hex opcode map dosyasını yükle
            hex_map_path = os.path.join(os.path.dirname(__file__), 'hex_opcode_map.json')
            if os.path.exists(hex_map_path):
                with open(hex_map_path, 'r', encoding='utf-8') as f:
                    hex_data = json.load(f)
                    print(f"Hex opcode map yüklendi: {len(hex_data)} opcode")

                    # Hex string'leri int'e çevir ve opcode tablosuna ekle
                    for hex_str, opcode_info in hex_data.items():
                        hex_value = int(hex_str, 16)
                        mnemonic = opcode_info['mnemonic']
                        length = opcode_info['length']
                        description = opcode_info['description']

                        # Format string'ini oluştur
                        if length == 1:
                            format_str = mnemonic
                        elif length == 2:
                            format_str = f"{mnemonic} $%02X"
                        elif length == 3:
                            format_str = f"{mnemonic} $%04X"
                        else:
                            format_str = f"{mnemonic} ???"

                        self.opcodes[hex_value] = (format_str, length, mnemonic)

        except Exception as e:
            print(f"Hex opcode map yüklenirken hata: {e}")

        # Opcode çevirileri için opcode_map.json dosyasını yükle
        opcode_map_path = os.path.join(os.path.dirname(__file__), 'opcode_map.json')
        if os.path.exists(opcode_map_path):
            with open(opcode_map_path, 'r', encoding='utf-8') as f:
                translation_data = json.load(f)

                # Çevirileri yükle
                for opcode_info in translation_data:
                    opcode_name = opcode_info['opcode']
                    self.translations[opcode_name] = {
                        'c_equivalent': opcode_info.get('c_equivalent', f'{opcode_name}();'),
                        'qbasic_equivalent': opcode_info.get('qbasic_equivalent', f'REM {opcode_name}'),
                        'pdsx_equivalent': opcode_info.get('pdsx_equivalent', f'REM {opcode_name}'),
                        'pseudo_equivalent': opcode_info.get('pseudo_equivalent', f'// {opcode_name}'),
                        'commodorebasicv2_equivalent': opcode_info.get('commodorebasicv2_equivalent', f'REM {opcode_name}')
                    }

                print(f"Opcode çevirileri yüklendi: {len(self.translations)} opcode")

    def create_full_opcode_table(self):
        """Tam 256 opcode tablosu oluştur"""
        # JSON'dan yüklenen opcode'lar zaten self.opcodes'a eklendi
        # Bilinmeyen opcodes için .BYTE kullan
        for i in range(256):
            if i not in self.opcodes:
                self.opcodes[i] = (f".BYTE ${i:02X}", 1, "UNKNOWN")
        
        print(f"Tam 6502 opcode tablosu tamamlandı: {len(self.opcodes)} opcode")
    
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
