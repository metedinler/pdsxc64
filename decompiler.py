import re

class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.type = node_type  # 'program', 'if', 'for', 'assign', etc.
        self.children = children or []
        self.value = value  # Condition, body, etc.

class Decompiler:
    def __init__(self, disassembly_file, target_lang='c'):
        self.disassembly_lines = self.load_disassembly(disassembly_file)
        self.target_lang = target_lang
        self.ast = ASTNode('program')
        self.labels = {}  # Address -> label mapping
        self.symbols = {}  # Symbol table from py65.asm

    def load_disassembly(self, disassembly_file):
        """Dosyadan disassembly satırlarını yükle"""
        with open(disassembly_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith(';')]
        return lines

    def parse_disassembly(self):
        """Disassembly satırlarını parse et ve talimat listesi oluştur"""
        instructions = []
        for line in self.disassembly_lines:
            # Gelismis diassembler Format .asm format: $0801: ROL $08
            # py65 Diassembler Format     .asm format: $0801  26 08       ROL $08
            match = re.match(r'\$([0-9A-F]{4})(?:\s+[0-9A-F]{2})*\s*([A-Z]+)\s*(.*)', line)
            if match:
                addr = int(match.group(1), 16)
                opcode = match.group(2)
                operand = match.group(3).strip() if match.group(3) else ''
                instructions.append((addr, opcode, operand))
                if opcode in ['JMP', 'BNE', 'BEQ']:
                    if operand.startswith('$'):
                        target = int(operand.replace('$', ''), 16)
                        self.labels[addr] = f"label_{target:04x}"
        return instructions

    def build_cfg(self, instructions):
        """Kontrol akış grafiği oluştur"""
        blocks = []
        current_block = []
        for instr in instructions:
            addr, op, operand = instr
            current_block.append(instr)
            if op in ['JMP', 'BNE', 'BEQ', 'RTS']:
                blocks.append(current_block)
                current_block = []
        if current_block:
            blocks.append(current_block)
        return blocks

    def match_pattern(self, block):
        """Bloktaki pattern'ları tanı"""
        if len(block) >= 3:
            if block[0][1] == 'CMP' and block[1][1] in ['BNE', 'BEQ']:
                return 'if', block[0][2], block[1][2]
            elif block[0][1] == 'LDX' and any(b[1] == 'CPX' for b in block) and any(b[1] == 'INX' for b in block):
                return 'for', None, None
        return None, None, None

    def build_ast(self, blocks):
        """CFG'den AST oluştur"""
        for block in blocks:
            pattern, cond_val, target = self.match_pattern(block)
            if pattern == 'if':
                cond = f"a == {cond_val}"
                then_block = block[2:]
                target_addr = int(target.replace('$', ''), 16)
                self.ast.children.append(
                    ASTNode('if', [
                        ASTNode('expr', value=cond),
                        ASTNode('block', [ASTNode('assign', value=f"{instr[1]} {instr[2]}") for instr in then_block])
                    ])
                )
            elif pattern == 'for':
                init = f"x = {block[0][2]}"
                cond_idx = next(i for i, b in enumerate(block) if b[1] == 'CPX')
                cond = f"x < {block[cond_idx][2]}"
                incr = "x++"
                body = [b for b in block if b[1] not in ['LDX', 'CPX', 'INX', 'BNE', 'JMP']]
                self.ast.children.append(
                    ASTNode('for', [
                        ASTNode('assign', value=init),
                        ASTNode('expr', value=cond),
                        ASTNode('assign', value=incr),
                        ASTNode('block', [ASTNode('assign', value=f"{instr[1]} {instr[2]}") for instr in body])
                    ])
                )
            else:
                for instr in block:
                    if instr[1] == 'LDA':
                        self.ast.children.append(ASTNode('assign', value=f"a = {instr[2]}"))
                    elif instr[1] == 'STA':
                        self.ast.children.append(ASTNode('assign', value=f"memory[{instr[2]}] = a"))

    def emit_code(self):
        """AST'den C kodu üret"""
        lines = ['#include <stdint.h>', 'uint8_t a, x;', 'uint8_t memory[0x10000];', 'int main() {']
        for node in self.ast.children:
            if node.type == 'if':
                cond = node.children[0].value
                then = ' '.join(n.value for n in node.children[1].children)
                lines.append(f"    if ({cond}) {{ {then}; }}")
            elif node.type == 'for':
                init = node.children[0].value
                cond = node.children[1].value
                incr = node.children[2].value
                body = ' '.join(n.value for n in node.children[3].children)
                lines.append(f"    for ({init}; {cond}; {incr}) {{ {body}; }}")
            elif node.type == 'assign':
                lines.append(f"    {node.value};")
        lines.append('    return 0;\n}')
        return '\n'.join(lines)

    def decompile(self):
        """Decompile işlemini gerçekleştir"""
        instructions = self.parse_disassembly()
        blocks = self.build_cfg(instructions)
        self.build_ast(blocks)
        return self.emit_code()

# Kullanım örneği
if __name__ == "__main__":
    decompiler = Decompiler('BLOCK OUT.asm')
    c_code = decompiler.decompile()
    print(c_code)