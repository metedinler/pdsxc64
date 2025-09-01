
import re

# 6502 Opcode Tanımları (örnek bir alt küme)
OPCODES = {
    'LDA': {'immediate': 0xA9, 'absolute': 0xAD, 'zp': 0xA5},
    'STA': {'absolute': 0x8D, 'zp': 0x85},
    'JMP': {'absolute': 0x4C},
    'JSR': {'absolute': 0x20}
}

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
