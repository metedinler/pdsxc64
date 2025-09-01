import re
import json
import logging
from datetime import datetime

# Loglama ayarları
logging.basicConfig(
    filename=f'decompiler_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# C64 KERNAL fonksiyonları haritası
KERNAL_MAP = {
    0xFFD2: 'CHROUT',
    0xFFCF: 'CHRIN',
    0xFFE4: 'GETIN',
    0xFFCC: 'CLRCHN',
    0xFFC9: 'CHKIN',
    0xFFC6: 'CHKOUT'
}

# AST Node sınıfı
class ASTNode:
    def __init__(self, node_type, children=None, value=None, label=None, params=None):
        self.type = node_type  # 'program', 'switch', 'for', 'while', 'function', 'struct', 'assign', 'expr'
        self.children = children or []
        self.value = value
        self.label = label
        self.params = params or []

# Decompiler sınıfı
class Decompiler:
    def __init__(self, disassembly_file, memory_map_file='memory_map.json'):
        logging.debug(f"Decompiler başlatılıyor: {disassembly_file}")
        try:
            self.disassembly_lines = self.load_disassembly(disassembly_file)
            self.memory_map = self.load_memory_map(memory_map_file)
            self.opcode_map = self.load_opcode_map()
            self.ast = ASTNode('program')
            self.labels = {}
            self.variables = {}
            self.functions = {}
            self.zeropage_vars = {}
            self.jump_tables = {}
            self.recursive_calls = set()
            self.line_number = 0  # C'de satır numarası kullanılmaz, ama izleme için tutuyoruz
        except Exception as e:
            logging.critical(f"Decompiler başlatma hatası: {str(e)}")
            raise

    def load_memory_map(self, memory_map_file):
        """memory_map.json'dan hafıza haritasını yükle"""
        logging.debug(f"Hafıza haritası yükleniyor: {memory_map_file}")
        try:
            with open(memory_map_file, 'r') as f:
                data = json.load(f)
                return {int(k, 16) if k.startswith('0x') else int(k): v for k, v in data.items()}
        except FileNotFoundError:
            logging.error(f"Hafıza haritası dosyası bulunamadı: {memory_map_file}")
            return {}
        except Exception as e:
            logging.critical(f"Hafıza haritası yükleme hatası: {str(e)}")
            raise

    def load_opcode_map(self):
        """opcode_map.json'dan opcode eşdeğerlerini yükle"""
        logging.debug("Opcode haritası yükleniyor")
        try:
            with open('opcode_map.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error("Opcode haritası dosyası bulunamadı")
            return []
        except Exception as e:
            logging.critical(f"Opcode haritası yükleme hatası: {str(e)}")
            raise

    def load_disassembly(self, disassembly_file):
        """Disassembly dosyasını satır satır oku"""
        logging.debug(f"Disassembly dosyası yükleniyor: {disassembly_file}")
        try:
            with open(disassembly_file, 'r') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith(';')]
            return lines
        except Exception as e:
            logging.critical(f"Disassembly dosyası yükleme hatası: {str(e)}")
            raise

    def parse_disassembly(self):
        """Disassembly satırlarını analiz et ve talimat listesi oluştur"""
        logging.debug("Disassembly satırları analiz ediliyor")
        try:
            instructions = []
            for line in self.disassembly_lines:
                match = re.match(r'\$([0-9A-F]{4})(?:\s+[0-9A-F]{2})*\s*([A-Z]+)\s*(.*)', line)
                if match:
                    addr = int(match.group(1), 16)
                    opcode = match.group(2)
                    operand = match.group(3).strip() if match.group(3) else ''
                    if operand.startswith('$'):
                        operand = int(operand.replace('$', ''), 16)
                    instructions.append((addr, opcode, operand))
                    if opcode in ['JMP', 'BNE', 'BEQ', 'JSR']:
                        if isinstance(operand, int):
                            if operand in self.memory_map:
                                self.labels[operand] = self.memory_map[operand]
                            elif operand not in self.labels:
                                self.labels[operand] = f"label_{operand:04x}"
                            if opcode == 'JSR' and operand == addr:
                                self.recursive_calls.add(operand)
                    if opcode == 'JSR' and isinstance(operand, int):
                        self.functions[operand] = f"func_{operand:04x}"
                    if isinstance(operand, int) and 0x00 <= operand <= 0xFF:
                        self.zeropage_vars[operand] = f"zvar_{operand:02x}"
                    if opcode == 'JMP' and isinstance(operand, str) and '),Y' in operand:
                        self.jump_tables[addr] = operand
            logging.info(f"Toplam {len(instructions)} talimat ayrıştırıldı")
            return instructions
        except Exception as e:
            logging.critical(f"Disassembly ayrıştırma hatası: {str(e)}")
            raise

    def build_cfg(self, instructions):
        """Kontrol akış grafiği oluştur"""
        logging.debug("CFG oluşturuluyor")
        try:
            blocks = []
            current_block = []
            for instr in instructions:
                addr, op, operand = instr
                current_block.append(instr)
                if op in ['JMP', 'BNE', 'BEQ', 'RTS']:
                    blocks.append((current_block[0][0], addr, current_block))
                    current_block = []
            if current_block:
                blocks.append((current_block[0][0], current_block[-1][0], current_block))
            logging.info(f"Toplam {len(blocks)} blok oluşturuldu")
            return blocks
        except Exception as e:
            logging.critical(f"CFG oluşturma hatası: {str(e)}")
            raise

    def detect_struct(self, block):
        """Struct pattern'larını tespit et"""
        try:
            if len(block) > 1 and all(b[1] in ['LDA', 'STA'] for b in block) and all(
                isinstance(b[2], int) and abs(b[2] - block[i-1][2]) == 1 for i, b in enumerate(block[1:], 1) if isinstance(b[2], int)
            ):
                return 'struct', block[0][2], len(block)
            return None, None, None
        except Exception as e:
            logging.error(f"Struct tespit hatası: {str(e)}")
            return None, None, None

    def detect_macro(self, blocks):
        """Makro pattern'larını tespit et"""
        try:
            for i, block in enumerate(blocks):
                for j, other_block in enumerate(blocks[i+1:], i+1):
                    if block[2] == other_block[2]:
                        return 'macro', block[2], f"macro_{i}"
            return None, None, None
        except Exception as e:
            logging.error(f"Macro tespit hatası: {str(e)}")
            return None, None, None

    def detect_unrolled_loop(self, blocks):
        """Döngü açma pattern'larını tespit et"""
        try:
            if len(blocks) > 1 and all(b[2] == blocks[0][2] for b in blocks[1:]):
                return 'loop', blocks[0][2], len(blocks)
            return None, None, None
        except Exception as e:
            logging.error(f"Unrolled loop tespit hatası: {str(e)}")
            return None, None, None

    def detect_bit_field(self, block):
        """Bit alanı pattern'larını tespit et"""
        try:
            if any(b[1] in ['AND', 'ORA', 'ASL', 'LSR'] for b in block):
                return 'bit_field', block[0][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Bit field tespit hatası: {str(e)}")
            return None, None, None

    def detect_global_var(self, block):
        """Global/statik değişken pattern'larını tespit et"""
        try:
            if any(isinstance(b[2], int) and b[2] >= 0x1000 for b in block if b[1] in ['LDA', 'STA']):
                return 'global_var', block[0][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Global değişken tespit hatası: {str(e)}")
            return None, None, None

    def detect_pointer(self, block):
        """Pointer aritmetiği pattern'larını tespit et"""
        try:
            if any(b[1] in ['LDA', 'STA'] and isinstance(b[2], str) and '),Y' in b[2] for b in block):
                return 'pointer', block[0][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Pointer tespit hatası: {str(e)}")
            return None, None, None

    def detect_timer(self, block):
        """Zamanlayıcı pattern'larını tespit et"""
        try:
            if any(b[1] == 'STA' and b[2] in ['$DC05', '$DC04'] for b in block):
                return 'timer', None, None
            return None, None, None
        except Exception as e:
            logging.error(f"Zamanlayıcı tespit hatası: {str(e)}")
            return None, None, None

    def detect_event_handler(self, block):
        """Olay işleyici pattern'larını tespit et"""
        try:
            if any(b[1] == 'LDA' and b[2] == '$DC00' for b in block):
                return 'event_handler', None, None
            return None, None, None
        except Exception as e:
            logging.error(f"Olay işleyici tespit hatası: {str(e)}")
            return None, None, None

    def detect_nested_if(self, block):
        """İç içe IF pattern'larını tespit et"""
        try:
            nested_ifs = []
            for i, instr in enumerate(block):
                if instr[1] == 'CMP' and i + 1 < len(block) and block[i+1][1] in ['BNE', 'BEQ']:
                    nested_ifs.append((instr[2], block[i+1][2]))
            return 'nested_if', nested_ifs, None
        except Exception as e:
            logging.error(f"İç içe IF tespit hatası: {str(e)}")
            return None, None, None

    def match_pattern(self, block):
        """Blok içindeki kontrol yapılarını tanı"""
        logging.debug(f"Pattern eşleştirme: {block[0][0]:04x}")
        try:
            struct_pat, struct_addr, struct_len = self.detect_struct(block)
            if struct_pat:
                return struct_pat, struct_addr, struct_len
            macro_pat, macro_block, macro_name = self.detect_macro([block])
            if macro_pat:
                return macro_pat, macro_block, macro_name
            loop_pat, loop_block, loop_count = self.detect_unrolled_loop([block])
            if loop_pat:
                return loop_pat, loop_block, loop_count
            bit_field_pat, bit_field_addr, _ = self.detect_bit_field(block)
            if bit_field_pat:
                return bit_field_pat, bit_field_addr, None
            global_var_pat, global_var_addr, _ = self.detect_global_var(block)
            if global_var_pat:
                return global_var_pat, global_var_addr, None
            pointer_pat, pointer_addr, _ = self.detect_pointer(block)
            if pointer_pat:
                return pointer_pat, pointer_addr, None
            timer_pat, _, _ = self.detect_timer(block)
            if timer_pat:
                return timer_pat, None, None
            event_handler_pat, _, _ = self.detect_event_handler(block)
            if event_handler_pat:
                return event_handler_pat, None, None
            nested_if_pat, nested_ifs, _ = self.detect_nested_if(block)
            if nested_if_pat:
                return nested_if_pat, nested_ifs, None
            if len(block) >= 3:
                cmp_indices = [i for i, b in enumerate(block) if b[1] == 'CMP']
                beq_indices = [i for i, b in enumerate(block) if b[1] == 'BEQ']
                if len(cmp_indices) > 1 and len(beq_indices) > 1:
                    return 'switch', block[cmp_indices[0]][2], [block[i][2] for i in beq_indices]
                elif block[0][1] == 'LDX' and any(b[1] == 'CPX' for b in block) and any(b[1] == 'INX' for b in block):
                    return 'for_inc', None, None
                elif block[0][1] == 'LDX' and any(b[1] == 'CPX' for b in block) and any(b[1] == 'DEX' for b in block):
                    return 'for_dec', None, None
                elif any(b[1] == 'CMP' for b in block) and any(b[1] == 'BNE' for b in block) and any(b[1] == 'JMP' for b in block):
                    return 'while', block[[i for i, b in enumerate(block) if b[1] == 'CMP'][0]][2], block[[i for i, b in enumerate(block) if b[1] == 'JMP'][0]][2]
                elif any(b[1] == 'CMP' for b in block) and any(b[1] == 'BEQ' for b in block) and any(b[1] == 'JMP' for b in block):
                    return 'do_while', block[[i for i, b in enumerate(block) if b[1] == 'CMP'][0]][2], block[[i for i, b in enumerate(block) if b[1] == 'JMP'][0]][2]
            if any(b[1] == 'PHA' for b in block) and any(b[1] == 'JSR' for b in block):
                return 'function_call', block[[i for i, b in enumerate(block) if b[1] == 'JSR'][0]][2], None
            if any(b[1] == 'BRK' for b in block):
                return 'interrupt', None, None
            return None, None, None
        except Exception as e:
            logging.error(f"Pattern eşleştirme hatası: {str(e)}")
            return None, None, None

    def translate_instruction(self, instr):
        """Tek bir talimatı C'ye çevir"""
        logging.debug(f"Talimat çevriliyor: {instr}")
        try:
            addr, op, operand = instr
            if op == 'LDA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"a = memory[{val}];" if isinstance(operand, int) else f"a = {val};")
            elif op == 'STA':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"memory[{var}] = a;")
            elif op == 'LDX':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"x = memory[{val}];" if isinstance(operand, int) else f"x = {val};")
            elif op == 'STX':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"memory[{var}] = x;")
            elif op == 'LDY':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"y = memory[{val}];" if isinstance(operand, int) else f"y = {val};")
            elif op == 'STY':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"memory[{var}] = y;")
            elif op == 'JSR' and isinstance(operand, int):
                if operand in self.functions:
                    params = [n.value for n in self.ast.children if n.type == 'assign' and 'push(a)' in n.value][-1:]
                    return ASTNode('function_call', value=f"{self.functions[operand]}({', '.join(params)});" if params else f"{self.functions[operand]}();")
                elif operand in KERNAL_MAP:
                    return ASTNode('kernal_call', value=f"{KERNAL_MAP[operand]}();")
            elif op == 'RTS':
                return ASTNode('return', value="return;")
            elif op == 'INX':
                return ASTNode('assign', value="x++;")
            elif op == 'DEX':
                return ASTNode('assign', value="x--;")
            elif op == 'PHA':
                return ASTNode('assign', value="/* push(a); */")
            elif op == 'PLA':
                return ASTNode('assign', value="a = pop();")
            elif op == 'LDA' and isinstance(operand, str) and ',X' in operand:
                addr = int(operand.split(',')[0].replace('$', ''), 16)
                var = self.variables.get(addr, f"array_{addr:04x}")
                return ASTNode('assign', value=f"a = memory[{var} + x];")
            elif op == 'LDA' and isinstance(operand, str) and ',Y' in operand:
                addr = int(operand.split(',')[0].replace('$', ''), 16)
                var = self.variables.get(addr, f"array_{addr:04x}")
                return ASTNode('assign', value=f"a = memory[{var} + y];")
            elif op == 'AND':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"a &= {val};")
            elif op == 'ORA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"a |= {val};")
            elif op == 'ASL':
                return ASTNode('assign', value="a <<= 1;")
            elif op == 'LSR':
                return ASTNode('assign', value="a >>= 1;")
            elif op == 'ADC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"a += {val};")
            elif op == 'SBC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"a -= {val};")
            elif op == 'BRK':
                return ASTNode('interrupt', value="/* Interrupt */")
            elif op == 'SEI':
                return ASTNode('raw', value="/* Disable Interrupts */")
            elif op == 'CLI':
                return ASTNode('raw', value="/* Enable Interrupts */")
            return ASTNode('raw', value=f"/* {op} {operand} */")
        except Exception as e:
            logging.error(f"Talimat çevirme hatası: {str(e)}")
            return ASTNode('raw', value=f"/* ERROR: {op} {operand} */")

    def build_ast(self, blocks):
        """CFG'den AST oluştur"""
        logging.debug("AST oluşturuluyor")
        try:
            macro_pat, macro_block, macro_name = self.detect_macro(blocks)
            loop_pat, loop_block, loop_count = self.detect_unrolled_loop(blocks)
            for start_addr, end_addr, block in blocks:
                pattern, cond_val, target = self.match_pattern(block)
                for instr in block:
                    addr, op, operand = instr
                    if isinstance(operand, int) and operand in self.memory_map:
                        var_name = self.memory_map[operand].split('(')[0].replace(' ', '_').lower()
                        self.variables[operand] = var_name
                    elif isinstance(operand, int) and operand not in self.variables:
                        self.variables[operand] = f"var_{operand:04x}"
                if pattern == 'struct':
                    struct_name = f"struct_{cond_val:04x}"
                    fields = [f"uint8_t field{i};" for i in range(target)]
                    self.ast.children.append(
                        ASTNode('struct_def', value=f"struct {struct_name} {{\n    " + "\n    ".join(fields) + "\n};")
                    )
                    for i, instr in enumerate(block):
                        if instr[1] == 'LDA':
                            self.ast.children.append(ASTNode('assign', value=f"{struct_name}.field{i} = memory[0x{instr[2]:04x}];"))
                        elif instr[1] == 'STA':
                            self.ast.children.append(ASTNode('assign', value=f"memory[0x{instr[2]:04x}] = {struct_name}.field{i};"))
                elif pattern == 'macro':
                    self.ast.children.append(ASTNode('function', value=f"void {macro_name}(void)", children=[self.translate_instruction(b) for b in macro_block]))
                elif pattern == 'loop':
                    init = f"int i = 1;"
                    cond = f"i <= {loop_count}"
                    incr = "i++;"
                    body = [self.translate_instruction(b) for b in loop_block]
                    self.ast.children.append(
                        ASTNode('for', [
                            ASTNode('assign', value=init),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=incr),
                            ASTNode('block', body)
                        ])
                    )
                elif pattern == 'bit_field':
                    self.ast.children.append(ASTNode('assign', value=f"uint8_t bitfield_{cond_val:04x} = a & 0x{cond_val:02x};"))
                elif pattern == 'global_var':
                    self.ast.children.append(ASTNode('global_var', value=f"uint8_t var_{cond_val:04x};"))
                elif pattern == 'pointer':
                    addr = int(cond_val.split('),')[0].replace('(', ''), 16) if isinstance(cond_val, str) else cond_val
                    self.ast.children.append(ASTNode('assign', value=f"uint8_t *ptr_{addr:04x} = &memory[0x{addr:04x} + y];"))
                elif pattern == 'timer':
                    self.ast.children.append(ASTNode('function', value="void timer_handler(void)", children=[self.translate_instruction(b) for b in block]))
                elif pattern == 'event_handler':
                    self.ast.children.append(ASTNode('function', value="void joystick_handler(void)", children=[self.translate_instruction(b) for b in block]))
                elif pattern == 'nested_if':
                    if_nodes = []
                    for cond, target in cond_val:
                        then_block = [b for b in block if b[2] == target or b[1] not in ['CMP', 'BNE', 'BEQ']]
                        else_block = [b for b in block if b[2] != target and b[1] not in ['CMP', 'BNE', 'BEQ']]
                        target_addr = int(target.replace('$', ''), 16) if isinstance(target, str) else target
                        if_nodes.append(
                            ASTNode('if', [
                                ASTNode('expr', value=f"a == {self.variables.get(cond, self.zeropage_vars.get(cond, f'0x{cond:04x}'))}"),
                                ASTNode('block', [self.translate_instruction(b) for b in then_block]),
                                ASTNode('block', [self.translate_instruction(b) for b in else_block])
                            ], label=self.labels.get(target_addr))
                        )
                    self.ast.children.append(ASTNode('nested_if', if_nodes))
                elif pattern == 'switch':
                    cases = []
                    for beq_target in target:
                        target_addr = int(beq_target.replace('$', ''), 16) if isinstance(beq_target, str) else beq_target
                        case_block = [b for b in block if b[2] == beq_target or b[1] not in ['CMP', 'BEQ']]
                        cases.append(ASTNode('case', [self.translate_instruction(b) for b in case_block], value=cond_val))
                    self.ast.children.append(
                        ASTNode('switch', cases, value=f"a == {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, f'0x{cond_val:04x}'))}")
                    )
                elif pattern == 'for_inc':
                    init = f"x = {self.variables.get(block[0][2], self.zeropage_vars.get(block[0][2], f'0x{block[0][2]:04x}'))};" if isinstance(block[0][2], int) else f"x = {block[0][2]};"
                    cond_idx = next(i for i, b in enumerate(block) if b[1] == 'CPX')
                    cond = f"x < {self.variables.get(block[cond_idx][2], self.zeropage_vars.get(block[cond_idx][2], f'0x{block[cond_idx][2]:04x}'))}" if isinstance(block[cond_idx][2], int) else f"x < {block[cond_idx][2]}"
                    incr = "x++;"
                    body = [b for b in block if b[1] not in ['LDX', 'CPX', 'INX', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('break', value="break;"))
                    self.ast.children.append(
                        ASTNode('for', [
                            ASTNode('assign', value=init),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=incr),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ])
                    )
                elif pattern == 'for_dec':
                    init = f"x = {self.variables.get(block[0][2], self.zeropage_vars.get(block[0][2], f'0x{block[0][2]:04x}'))};" if isinstance(block[0][2], int) else f"x = {block[0][2]};"
                    cond_idx = next(i for i, b in enumerate(block) if b[1] == 'CPX')
                    cond = f"x >= {self.variables.get(block[cond_idx][2], self.zeropage_vars.get(block[cond_idx][2], f'0x{block[cond_idx][2]:04x}'))}" if isinstance(block[cond_idx][2], int) else f"x >= {block[cond_idx][2]}"
                    decr = "x--;"
                    body = [b for b in block if b[1] not in ['LDX', 'CPX', 'DEX', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('break', value="break;"))
                    self.ast.children.append(
                        ASTNode('for', [
                            ASTNode('assign', value=init),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=decr),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ])
                    )
                elif pattern == 'while':
                    cond = f"a == {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, f'0x{cond_val:04x}'))}" if isinstance(cond_val, int) else f"a == {cond_val}"
                    body = [b for b in block if b[1] not in ['CMP', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('break', value="break;"))
                    target_addr = int(target.replace('$', ''), 16) if isinstance(target, str) else target
                    self.ast.children.append(
                        ASTNode('while', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], label=self.labels.get(target_addr))
                    )
                elif pattern == 'do_while':
                    cond = f"a != {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, f'0x{cond_val:04x}'))}" if isinstance(cond_val, int) else f"a != {cond_val}"
                    body = [b for b in block if b[1] not in ['CMP', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('break', value="break;"))
                    target_addr = int(target.replace('$', ''), 16) if isinstance(target, str) else target
                    self.ast.children.append(
                        ASTNode('do_while', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], label=self.labels.get(target_addr))
                    )
                elif pattern == 'function_call':
                    self.ast.children.append(ASTNode('function_call', value=f"{self.functions[cond_val]}();" if cond_val in self.functions else f"/* JSR {cond_val} */", params=[self.translate_instruction(b) for b in block if b[1] == 'PHA']))
                elif pattern == 'interrupt':
                    self.ast.children.append(ASTNode('function', value="void interrupt_handler(void)", children=[self.translate_instruction(b) for b in block]))
                else:
                    for instr in block:
                        self.ast.children.append(self.translate_instruction(instr))
        except Exception as e:
            logging.critical(f"AST oluşturma hatası: {str(e)}")
            raise

    def emit_code(self):
        """AST'den C kodu üret"""
        logging.debug("C kodu üretiliyor")
        try:
            lines = [
                '#include <stdint.h>',
                'uint8_t a, x, y;',
                'uint8_t memory[0x10000];',
                'void CHROUT(uint8_t);',
                'void CHRIN(void);',
                'void GETIN(void);',
                'void CLRCHN(void);',
                'void CHKIN(void);',
                'void CHKOUT(void);'
            ]
            # Struct ve global değişken tanımları
            for node in self.ast.children:
                if node.type == 'struct_def':
                    lines.append(node.value)
                elif node.type == 'global_var':
                    lines.append(node.value)
            # Fonksiyon tanımları
            for addr, func_name in self.functions.items():
                lines.append(f"void {func_name}({'void' if addr not in self.recursive_calls else 'void /* recursive */'}) {{")
                self.line_number += 1
            # Ana fonksiyon
            lines.append("int main() {")
            self.line_number += 1
            for node in self.ast.children:
                if node.type == 'switch':
                    cond = node.value
                    lines.append(f"    switch ({cond.split('==')[0].strip()}) {{")
                    self.line_number += 1
                    for case in node.children:
                        lines.append(f"    case {case.value}:")
                        self.line_number += 1
                        for stmt in case.children:
                            lines.append(f"        {stmt.value}")
                            self.line_number += 1
                        lines.append("        break;")
                        self.line_number += 1
                    lines.append("    }")
                    self.line_number += 1
                elif node.type == 'nested_if':
                    for if_node in node.children:
                        cond = if_node.children[0].value
                        then_block = [n.value for n in if_node.children[1].children]
                        else_block = [n.value for n in if_node.children[2].children]
                        lines.append(f"    if ({cond}) {{")
                        self.line_number += 1
                        for stmt in then_block:
                            lines.append(f"        {stmt}")
                            self.line_number += 1
                        if else_block:
                            lines.append("    } else {")
                            self.line_number += 1
                            for stmt in else_block:
                                lines.append(f"        {stmt}")
                                self.line_number += 1
                        lines.append("    }")
                        self.line_number += 1
                elif node.type == 'for':
                    init = node.children[0].value
                    cond = node.children[1].value
                    incr = node.children[2].value
                    body = [n.value for n in node.children[3].children]
                    lines.append(f"    for ({init} {cond}; {incr}) {{")
                    self.line_number += 1
                    for stmt in body:
                        lines.append(f"        {stmt}")
                        self.line_number += 1
                    lines.append("    }")
                    self.line_number += 1
                elif node.type == 'while':
                    cond = node.children[0].value
                    body = [n.value for n in node.children[1].children]
                    lines.append(f"    while ({cond}) {{")
                    self.line_number += 1
                    for stmt in body:
                        lines.append(f"        {stmt}")
                        self.line_number += 1
                    lines.append("    }")
                    self.line_number += 1
                elif node.type == 'do_while':
                    cond = node.children[0].value
                    body = [n.value for n in node.children[1].children]
                    lines.append("    do {")
                    self.line_number += 1
                    for stmt in body:
                        lines.append(f"        {stmt}")
                        self.line_number += 1
                    lines.append(f"    }} while ({cond});")
                    self.line_number += 1
                elif node.type == 'function_call':
                    lines.append(f"    {node.value}")
                    self.line_number += 1
                    for param in node.params:
                        lines.append(f"    /* Parameter: {param.value} */")
                        self.line_number += 1
                elif node.type == 'return':
                    lines.append(f"    {node.value}")
                    self.line_number += 1
                elif node.type == 'break':
                    lines.append(f"    {node.value}")
                    self.line_number += 1
                elif node.type == 'assign':
                    lines.append(f"    {node.value}")
                    self.line_number += 1
                elif node.type == 'raw':
                    lines.append(f"    {node.value}")
                    self.line_number += 1
                elif node.type == 'function':
                    lines.append(f"{node.value} {{")
                    self.line_number += 1
                    for stmt in node.children:
                        lines.append(f"    {stmt.value}")
                        self.line_number += 1
                    lines.append("}")
                    self.line_number += 1
                elif node.type == 'kernal_call':
                    lines.append(f"    {node.value}")
                    self.line_number += 1
            lines.append("    return 0;")
            lines.append("}")
            logging.info("C kodu başarıyla üretildi")
            return '\n'.join(lines)
        except Exception as e:
            logging.critical(f"Kod üretme hatası: {str(e)}")
            raise

    def decompile(self):
        """Decompile işlemini gerçekleştir"""
        logging.debug("Decompile işlemi başlatılıyor")
        try:
            instructions = self.parse_disassembly()
            blocks = self.build_cfg(instructions)
            self.build_ast(blocks)
            return self.emit_code()
        except Exception as e:
            logging.critical(f"Decompile işlemi hatası: {str(e)}")
            raise