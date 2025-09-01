
import re

# 6502 Opcode Tanımları: JSON'dan dinamik yükleniyor
import os
import json
from data_loader import DataLoader

# Load complete 6502 opcode map and build mnemonic lookup
loader = DataLoader(os.path.dirname(__file__))
opcode_data = loader.load_directory('.').get('complete_6502_opcode_map', {})
# Build mapping of mnemonic to raw opcode entries
OPCODES = {}
for hex_str, info in opcode_data.items():
    mnemonic = info.get('mnemonic', '')
    if mnemonic:
        # Initialize list if not present
        OPCODES.setdefault(mnemonic, []).append({
            'hex': hex_str,
            'length': info.get('length', 1),
            'description': info.get('description', '')
        })

class AssemblyParser:
    def __init__(self, filename):
        self.filename = filename
        self.instructions = []
        self.labels = {}

    def parse(self):
        """Assembly dosyasını oku ve talimatları ayrıştır."""
        with open(self.filename, 'r') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith(';'):
                continue  # Boş satır veya yorum

            # Etiket kontrolü
            if line.endswith(':'):
                label = line[:-1].strip()
                self.labels[label] = len(self.instructions)
                continue

            # Talimat ayrıştırma (örn. LDA #$10)
            match = re.match(r'(\w+)\s+([#$%]?[\w\d]+)?', line)
            if match:
                opcode, operand = match.groups()
                if opcode in OPCODES:
                    instr = {'opcode': opcode, 'operand': operand, 'line': line_num}
                    self.instructions.append(instr)
                else:
                    print(f"Hata: Tanınmayan opcode '{opcode}' - Satır: {line_num}")

    def get_instructions(self):
        """Ayrıştırılmış talimatları döndür."""
        return self.instructions

    def get_labels(self):
        """Tanımlı etiketleri döndür."""
        return self.labels

# Test
if __name__ == "__main__":
    parser = AssemblyParser("test.asm")
    parser.parse()
    for instr in parser.get_instructions():
        print(f"{instr['opcode']} {instr['operand']} (Satır: {instr['line']})")
    print("Etiketler:", parser.get_labels())
