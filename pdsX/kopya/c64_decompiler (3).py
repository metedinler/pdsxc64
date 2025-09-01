
import re
import json
import logging
from datetime import datetime
import uuid

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
    0xFFC6: 'CHKOUT',
    0xFFD5: 'LOAD',
    0xFFD8: 'SAVE',
    0xFFDB: 'SETTIM',
    0xFFDE: 'RDTIM',
    0xFFE1: 'STOP',
    0xFFE7: 'CLALL',
    0xFFEA: 'UDTIM',
    0xFFED: 'SCREEN',
    0xFFF0: 'PLOT',
    0xFFF3: 'IOBASE'
}

# AST Node sınıfı
class ASTNode:
    def __init__(self, node_type, children=None, value=None, label=None, params=None):
        self.type = node_type  # 'program', 'select', 'for', 'while', 'do_until', 'sub', 'assign', 'expr', 'goto', 'gosub', 'data', 'read'
        self.children = children or []
        self.value = value
        self.label = label
        self.params = params or []

# Decompiler sınıfı
class Decompiler:
    def __init__(self, disassembly_file, memory_map_file='c64_memory_map.json', tokens_file='basic_tokens.json', routines_file='basic_routines.json', kernal_routines_file='kernal_routines.json', io_registers_file='io_registers.json', special_addresses_file='special_addresses.json'):
        logging.debug(f"Decompiler başlatılıyor: {disassembly_file}")
        try:
            self.disassembly_lines = self.load_disassembly(disassembly_file)
            self.memory_map = self.load_memory_map(memory_map_file)
            self.tokens = self.load_tokens(tokens_file)
            self.routines = self.load_routines(routines_file)
            self.kernal_routines = self.load_routines(kernal_routines_file)
            self.io_registers = self.load_io_registers(io_registers_file)
            self.special_addresses = self.load_special_addresses(special_addresses_file)
            self.opcode_map = self.load_opcode_map()
            self.ast = ASTNode('program')
            self.labels = {}
            self.variables = {}
            self.subroutines = {}
            self.zeropage_vars = {}
            self.jump_tables = {}
            self.line_number = 10
            self.recursive_calls = set()
        except Exception as e:
            logging.critical(f"Decompiler başlatma hatası: {str(e)}")
            raise

    def load_memory_map(self, memory_map_file):
        logging.debug(f"Hafıza haritası yükleniyor: {memory_map_file}")
        try:
            with open(memory_map_file, 'r') as f:
                data = json.load(f)
                return {int(k, 16) if k.startswith('$') else int(k): v for k, v in data.items()}
        except FileNotFoundError:
            logging.error(f"Hafıza haritası dosyası bulunamadı: {memory_map_file}")
            return {}
        except Exception as e:
            logging.critical(f"Hafıza haritası yükleme hatası: {str(e)}")
            raise

    def load_tokens(self, tokens_file):
        logging.debug(f"Token haritası yükleniyor: {tokens_file}")
        try:
            with open(tokens_file, 'r') as f:
                data = json.load(f)
                return {int(k.replace('$', ''), 16): v for k, v in data.items()}
        except FileNotFoundError:
            logging.error(f"Token dosyası bulunamadı: {tokens_file}")
            return {}
        except Exception as e:
            logging.critical(f"Token yükleme hatası: {str(e)}")
            raise

    def load_routines(self, routines_file):
        logging.debug(f"Rutin haritası yükleniyor: {routines_file}")
        try:
            with open(routines_file, 'r') as f:
                data = json.load(f)
                return {int(k.replace('$', ''), 16): v for k, v in data.items()}
        except FileNotFoundError:
            logging.error(f"Rutin dosyası bulunamadı: {routines_file}")
            return {}
        except Exception as e:
            logging.critical(f"Rutin yükleme hatası: {str(e)}")
            raise

    def load_io_registers(self, io_registers_file):
        logging.debug(f"I/O register haritası yükleniyor: {io_registers_file}")
        try:
            with open(io_registers_file, 'r') as f:
                data = json.load(f)
                return {int(k.replace('$', ''), 16) if '-' not in k else (int(k.split('-')[0].replace('$', ''), 16), int(k.split('-')[1].replace('$', ''), 16)): v for k, v in data.items()}
        except FileNotFoundError:
            logging.error(f"I/O register dosyası bulunamadı: {io_registers_file}")
            return {}
        except Exception as e:
            logging.critical(f"I/O register yükleme hatası: {str(e)}")
            raise

    def load_special_addresses(self, special_addresses_file):
        logging.debug(f"Özel adres haritası yükleniyor: {special_addresses_file}")
        try:
            with open(special_addresses_file, 'r') as f:
                data = json.load(f)
                return {k if '-' not in k else (int(k.split('-')[0].replace('$', ''), 16), int(k.split('-')[1].replace('$', ''), 16)): v for k, v in data.items()}
        except FileNotFoundError:
            logging.error(f"Özel adres dosyası bulunamadı: {special_addresses_file}")
            return {}
        except Exception as e:
            logging.critical(f"Özel adres yükleme hatası: {str(e)}")
            raise

    def load_opcode_map(self):
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
        logging.debug(f"Disassembly dosyası yükleniyor: {disassembly_file}")
        try:
            with open(disassembly_file, 'r') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith(';')]
            return lines
        except Exception as e:
            logging.critical(f"Disassembly dosyası yükleme hatası: {str(e)}")
            raise

    def parse_disassembly(self):
        logging.debug("Disassembly satırları analiz ediliyor")
        try:
            instructions = []
            for line in self.disassembly_lines:
                match = re.match(r'([A-Z_]+):?\s*\$?([0-9A-F]{4})?\s*([A-Z]+)\s*(\S.*)?', line)
                if match:
                    label, addr, opcode, operand = match.groups()
                    addr = int(addr, 16) if addr else None
                    operand = operand.strip() if operand else ''
                    if operand.startswith('$'):
                        operand = operand.replace('$', '')
                        if ',' in operand:
                            operand = operand.split(',')[0]
                        operand = int(operand, 16)
                    instructions.append((addr, opcode, operand, label))
                    if opcode in ['JMP', 'BNE', 'BEQ', 'JSR']:
                        if isinstance(operand, int):
                            if operand in self.routines:
                                self.labels[operand] = self.routines[operand]['name']
                            elif operand in self.kernal_routines:
                                self.labels[operand] = self.kernal_routines[operand]['name']
                            elif operand not in self.labels:
                                self.labels[operand] = f"LABEL_{operand:04x}"
                            if opcode == 'JSR' and operand == addr:
                                self.recursive_calls.add(operand)
                    if opcode == 'JSR' and isinstance(operand, int):
                        self.subroutines[operand] = self.routines.get(operand, {}).get('name', f"SUB_{operand:04x}")
                    if isinstance(operand, int) and 0x00 <= operand <= 0xFF:
                        self.zeropage_vars[operand] = self.special_addresses.get((operand, operand), {}).get('name', f"ZVAR_{operand:02x}")
                    if isinstance(operand, int) and operand >= 0xD000:
                        self.variables[operand] = self.io_registers.get(operand, {}).get('name', f"IO_{operand:04x}")
                    if opcode == 'JMP' and isinstance(operand, str) and '),Y' in operand:
                        self.jump_tables[addr] = operand
            logging.info(f"Toplam {len(instructions)} talimat ayrıştırıldı")
            return instructions
        except Exception as e:
            logging.critical(f"Disassembly ayrıştırma hatası: {str(e)}")
            raise

    def build_cfg(self, instructions):
        logging.debug("CFG oluşturuluyor")
        try:
            blocks = []
            current_block = []
            for instr in instructions:
                addr, op, operand, label = instr
                current_block.append(instr)
                if op in ['JMP', 'BNE', 'BEQ', 'RTS', 'RTI']:
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
        try:
            for i, block in enumerate(blocks):
                for j, other_block in enumerate(blocks[i+1:], i+1):
                    if block[2] == other_block[2]:
                        return 'macro', block[2], f"MACRO_{i}"
            return None, None, None
        except Exception as e:
            logging.error(f"Macro tespit hatası: {str(e)}")
            return None, None, None

    def detect_unrolled_loop(self, blocks):
        try:
            if len(blocks) > 1 and all(b[2] == blocks[0][2] for b in blocks[1:]):
                return 'loop', blocks[0][2], len(blocks)
            return None, None, None
        except Exception as e:
            logging.error(f"Unrolled loop tespit hatası: {str(e)}")
            return None, None, None

    def detect_bit_field(self, block):
        try:
            if any(b[1] in ['AND', 'ORA', 'ASL', 'LSR'] for b in block):
                return 'bit_field', block[0][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Bit field tespit hatası: {str(e)}")
            return None, None, None

    def detect_global_var(self, block):
        try:
            if any(isinstance(b[2], int) and b[2] >= 0x1000 for b in block if b[1] in ['LDA', 'STA']):
                return 'global_var', block[0][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Global değişken tespit hatası: {str(e)}")
            return None, None, None

    def detect_pointer(self, block):
        try:
            if any(b[1] in ['LDA', 'STA'] and isinstance(b[2], str) and '),Y' in b[2] for b in block):
                return 'pointer', block[0][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Pointer tespit hatası: {str(e)}")
            return None, None, None

    def detect_timer(self, block):
        try:
            if any(b[1] == 'STA' and b[2] in ['$DC04', '$DC05', '$DD04', '$DD05'] for b in block):
                return 'timer', None, None
            return None, None, None
        except Exception as e:
            logging.error(f"Zamanlayıcı tespit hatası: {str(e)}")
            return None, None, None

    def detect_event_handler(self, block):
        try:
            if any(b[1] == 'LDA' and b[2] == '$DC00' for b in block):
                return 'event_handler', None, None
            return None, None, None
        except Exception as e:
            logging.error(f"Olay işleyici tespit hatası: {str(e)}")
            return None, None, None

    def detect_nested_if(self, block):
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
                bne_indices = [i for i, b in enumerate(block) if b[1] == 'BNE']
                if len(cmp_indices) >= 1 and len(beq_indices) >= 1:
                    return 'if', block[cmp_indices[0]][2], block[beq_indices[0]][2]
                elif block[0][1] == 'LDX' and any(b[1] == 'CPX' for b in block) and any(b[1] == 'INX' for b in block):
                    return 'for_inc', None, None
                elif block[0][1] == 'LDX' and any(b[1] == 'CPX' for b in block) and any(b[1] == 'DEX' for b in block):
                    return 'for_dec', None, None
                elif any(b[1] == 'CMP' for b in block) and any(b[1] == 'BNE' for b in block) and any(b[1] == 'JMP' for b in block):
                    return 'while', block[[i for i, b in enumerate(block) if b[1] == 'CMP'][0]][2], block[[i for i, b in enumerate(block) if b[1] == 'JMP'][0]][2]
                elif any(b[1] == 'CMP' for b in block) and any(b[1] == 'BEQ' for b in block) and any(b[1] == 'JMP' for b in block):
                    return 'do_until', block[[i for i, b in enumerate(block) if b[1] == 'CMP'][0]][2], block[[i for i, b in enumerate(block) if b[1] == 'JMP'][0]][2]
            if any(b[1] == 'JSR' for b in block):
                jsr_idx = next(i for i, b in enumerate(block) if b[1] == 'JSR')
                return 'sub_call', block[jsr_idx][2], None
            if any(b[1] == 'JMP' for b in block):
                jmp_idx = next(i for i, b in enumerate(block) if b[1] == 'JMP')
                return 'goto', block[jmp_idx][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Pattern eşleştirme hatası: {str(e)}")
            return None, None, None

    def translate_instruction(self, instr):
        logging.debug(f"Talimat çevriliyor: {instr}")
        try:
            addr, op, operand, label = instr
            if op == 'LDA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, self.io_registers.get(operand, {}).get('name', operand))) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = PEEK({val})" if isinstance(operand, int) else f"LET A = {val}")
            elif op == 'STA':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, self.io_registers.get(operand, {}).get('name', operand))) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"POKE {var}, A")
            elif op == 'LDX':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET X = PEEK({val})" if isinstance(operand, int) else f"LET X = {val}")
            elif op == 'STX':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"POKE {var}, X")
            elif op == 'LDY':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET Y = PEEK({val})" if isinstance(operand, int) else f"LET Y = {val}")
            elif op == 'STY':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"POKE {var}, Y")
            elif op == 'JSR':
                if operand in self.routines:
                    routine = self.routines[operand]
                    params = [p['description'] for p in routine['parameters']]
                    return ASTNode('sub_call', value=f"GOSUB {routine['name']}" + (f" {', '.join(params)}" if params else ""))
                elif operand in KERNAL_MAP:
                    return ASTNode('kernal_call', value=f"GOSUB {KERNAL_MAP[operand]}")
                else:
                    return ASTNode('sub_call', value=f"GOSUB SUB_{operand:04x}")
            elif op == 'JMP':
                return ASTNode('goto', value=f"GOTO {self.labels.get(operand, f'LABEL_{operand:04x}')}") if isinstance(operand, int) else ASTNode('goto', value=f"GOTO {operand}")
            elif op == 'RTS':
                return ASTNode('return', value="RETURN")
            elif op == 'INX':
                return ASTNode('assign', value="LET X = X + 1")
            elif op == 'DEX':
                return ASTNode('assign', value="LET X = X - 1")
            elif op == 'INY':
                return ASTNode('assign', value="LET Y = Y + 1")
            elif op == 'DEY':
                return ASTNode('assign', value="LET Y = Y - 1")
            elif op == 'PHA':
                return ASTNode('assign', value="REM PUSH A")
            elif op == 'PLA':
                return ASTNode('assign', value="LET A = POP()")
            elif op == 'CMP':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('expr', value=f"A = {val}")
            elif op == 'BEQ':
                return ASTNode('if', value=f"IF A = 0 THEN GOTO {self.labels.get(operand, f'LABEL_{operand:04x}')}") if isinstance(operand, int) else ASTNode('if', value=f"IF A = 0 THEN GOTO {operand}")
            elif op == 'BNE':
                return ASTNode('if', value=f"IF A <> 0 THEN GOTO {self.labels.get(operand, f'LABEL_{operand:04x}')}") if isinstance(operand, int) else ASTNode('if', value=f"IF A <> 0 THEN GOTO {operand}")
            elif op == 'ADC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = A + {val}")
            elif op == 'SBC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = A - {val}")
            elif op == 'ASL':
                return ASTNode('assign', value="LET A = A * 2")
            elif op == 'LSR':
                return ASTNode('assign', value="LET A = A / 2")
            elif op == 'AND':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = A AND {val}")
            elif op == 'ORA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = A OR {val}")
            elif op == 'SEI':
                return ASTNode('raw', value="REM Disable Interrupts")
            elif op == 'CLI':
                return ASTNode('raw', value="REM Enable Interrupts")
            elif op == 'BRK':
                return ASTNode('interrupt', value="REM Interrupt")
            return ASTNode('raw', value=f"REM {op} {operand}")
        except Exception as e:
            logging.error(f"Talimat çevirme hatası: {str(e)}")
            return ASTNode('raw', value=f"REM ERROR: {op} {operand}")

    def build_ast(self, blocks):
        logging.debug("AST oluşturuluyor")
        try:
            for start_addr, end_addr, block in blocks:
                pattern, cond_val, target = self.match_pattern(block)
                for instr in block:
                    addr, op, operand, label = instr
                    if isinstance(operand, int):
                        if operand in self.memory_map:
                            var_name = self.memory_map[operand]['name'].replace(' ', '_')
                            self.variables[operand] = var_name
                        elif operand in self.special_addresses:
                            var_name = self.special_addresses[operand]['name']
                            self.variables[operand] = var_name
                        elif operand in self.io_registers:
                            var_name = self.io_registers[operand]['name']
                            self.variables[operand] = var_name
                        elif operand not in self.variables:
                            self.variables[operand] = f"VAR_{operand:04x}"
                if pattern == 'struct':
                    struct_name = f"STRUCT_{cond_val:04x}"
                    fields = [f"field{i} AS INTEGER" for i in range(target)]
                    self.ast.children.append(
                        ASTNode('struct_def', value=f"TYPE {struct_name}\n    " + "\n    ".join(fields) + "\nEND TYPE")
                    )
                    for i, instr in enumerate(block):
                        if instr[1] == 'LDA':
                            self.ast.children.append(ASTNode('assign', value=f"LET {struct_name}.field{i} = PEEK({instr[2]})"))
                        elif instr[1] == 'STA':
                            self.ast.children.append(ASTNode('assign', value=f"POKE {instr[2]}, {struct_name}.field{i}"))
                elif pattern == 'macro':
                    self.ast.children.append(ASTNode('sub', value=f"SUB {cond_val}", children=[self.translate_instruction(b) for b in block]))
                elif pattern == 'loop':
                    init = f"I = 1"
                    cond = f"I <= {loop_count}"
                    incr = "I = I + 1"
                    body = [self.translate_instruction(b) for b in block]
                    self.ast.children.append(
                        ASTNode('for_inc', [
                            ASTNode('assign', value=init),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=incr),
                            ASTNode('block', body)
                        ])
                    )
                elif pattern == 'if':
                    cond = f"A = {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val))}" if isinstance(cond_val, int) else f"A = {cond_val}"
                    then_block = [b for b in block if b[2] == target or b[1] not in ['CMP', 'BEQ', 'BNE']]
                    else_block = [b for b in block if b[2] != target and b[1] not in ['CMP', 'BEQ', 'BNE']]
                    self.ast.children.append(
                        ASTNode('if', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in then_block]),
                            ASTNode('block', [self.translate_instruction(b) for b in else_block])
                        ], label=self.labels.get(target))
                    )
                elif pattern == 'for_inc':
                    init = f"X = {self.variables.get(block[0][2], self.zeropage_vars.get(block[0][2], block[0][2]))}" if isinstance(block[0][2], int) else f"X = {block[0][2]}"
                    cond_idx = next(i for i, b in enumerate(block) if b[1] == 'CPX')
                    cond = f"X < {self.variables.get(block[cond_idx][2], self.zeropage_vars.get(block[cond_idx][2], block[cond_idx][2]))}" if isinstance(block[cond_idx][2], int) else f"X < {block[cond_idx][2]}"
                    incr = "X = X + 1"
                    body = [b for b in block if b[1] not in ['LDX', 'CPX', 'INX', 'BNE', 'JMP']]
                    self.ast.children.append(
                        ASTNode('for_inc', [
                            ASTNode('assign', value=init),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=incr),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ])
                    )
                elif pattern == 'while':
                    cond = f"A <> {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val))}" if isinstance(cond_val, int) else f"A <> {cond_val}"
                    body = [b for b in block if b[1] not in ['CMP', 'BNE', 'JMP']]
                    self.ast.children.append(
                        ASTNode('while', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], label=self.labels.get(target))
                    )
                elif pattern == 'do_until':
                    cond = f"A = {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val))}" if isinstance(cond_val, int) else f"A = {cond_val}"
                    body = [b for b in block if b[1] not in ['CMP', 'BEQ', 'JMP']]
                    self.ast.children.append(
                        ASTNode('do_until', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], label=self.labels.get(target))
                    )
                elif pattern == 'sub_call':
                    self.ast.children.append(ASTNode('sub_call', value=f"GOSUB {self.subroutines.get(cond_val, f'SUB_{cond_val:04x}')}" if isinstance(cond_val, int) else f"GOSUB {cond_val}"))
                elif pattern == 'goto':
                    self.ast.children.append(ASTNode('goto', value=f"GOTO {self.labels.get(cond_val, f'LABEL_{cond_val:04x}')}" if isinstance(cond_val, int) else f"GOTO {cond_val}"))
                else:
                    for instr in block:
                        self.ast.children.append(self.translate_instruction(instr))
        except Exception as e:
            logging.critical(f"AST oluşturma hatası: {str(e)}")
            raise

    def emit_code(self):
        logging.debug("QuickBASIC kodu üretiliyor")
        try:
            lines = [
                'REM Generated by 6502 Decompiler for QuickBASIC 7.1',
                'DECLARE SUB CHROUT (Char%)',
                'DECLARE SUB CHRIN ()',
                'DECLARE SUB GETIN ()',
                'DECLARE SUB CLRCHN ()',
                'DECLARE SUB CHKIN ()',
                'DECLARE SUB CHKOUT ()',
                'DECLARE SUB LOAD ()',
                'DECLARE SUB SAVE ()',
                'DECLARE SUB SETTIM ()',
                'DECLARE SUB RDTIM ()',
                'DECLARE SUB STOP ()',
                'DECLARE SUB CLALL ()',
                'DECLARE SUB UDTIM ()',
                'DECLARE SUB SCREEN ()',
                'DECLARE SUB PLOT ()',
                'DECLARE SUB IOBASE ()',
                'DIM SHARED A AS INTEGER, X AS INTEGER, Y AS INTEGER',
                'DIM SHARED MEMORY(65535) AS INTEGER'
            ]
            for node in self.ast.children:
                if node.type == 'struct_def':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
            for addr, sub_name in self.subroutines.items():
                lines.append(f"{self.line_number} SUB {sub_name}" + (" RECURSIVE" if addr in self.recursive_calls else ""))
                self.line_number += 10
            lines.append(f"{self.line_number} REM Main Program")
            self.line_number += 10
            for node in self.ast.children:
                if node.type == 'if':
                    cond = node.children[0].value
                    then_block = [self.emit_line(n) for n in node.children[1].children]
                    else_block = [self.emit_line(n) for n in node.children[2].children]
                    lines.append(f"{self.line_number} IF {cond} THEN")
                    self.line_number += 10
                    lines.extend(then_block)
                    if else_block:
                        lines.append(f"{self.line_number} ELSE")
                        self.line_number += 10
                        lines.extend(else_block)
                    lines.append(f"{self.line_number} END IF")
                    self.line_number += 10
                elif node.type == 'for_inc':
                    init = node.children[0].value
                    cond = node.children[1].value
                    incr = node.children[2].value
                    body = [self.emit_line(n) for n in node.children[3].children]
                    var = init.split('=')[0].strip()
                    limit = cond.split('<')[1].strip()
                    lines.append(f"{self.line_number} FOR {var} = {init.split('=')[1].strip()} TO {limit} STEP 1")
                    self.line_number += 10
                    lines.extend(body)
                    lines.append(f"{self.line_number} NEXT {var}")
                    self.line_number += 10
                elif node.type == 'while':
                    cond = node.children[0].value
                    body = [self.emit_line(n) for n in node.children[1].children]
                    lines.append(f"{self.line_number} WHILE {cond}")
                    self.line_number += 10
                    lines.extend(body)
                    lines.append(f"{self.line_number} WEND")
                    self.line_number += 10
                elif node.type == 'do_until':
                    cond = node.children[0].value
                    body = [self.emit_line(n) for n in node.children[1].children]
                    lines.append(f"{self.line_number} DO")
                    self.line_number += 10
                    lines.extend(body)
                    lines.append(f"{self.line_number} LOOP UNTIL {cond}")
                    self.line_number += 10
                elif node.type == 'sub_call':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                elif node.type == 'goto':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                elif node.type == 'assign':
                    lines.append(self.emit_line(node))
                elif node.type == 'raw':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                elif node.type == 'sub':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                    for stmt in node.children:
                        lines.append(self.emit_line(stmt))
                elif node.type == 'kernal_call':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
            for addr, sub_name in self.subroutines.items():
                lines.append(f"{self.line_number} END SUB")
                self.line_number += 10
            logging.info("QuickBASIC kodu başarıyla üretildi")
            return '\n'.join(lines)
        except Exception as e:
            logging.critical(f"Kod üretme hatası: {str(e)}")
            raise

    def emit_line(self, node):
        logging.debug(f"Satır üretiliyor: {node.value}")
        try:
            line = f"{self.line_number} {node.value}"
            self.line_number += 10
            return line
        except Exception as e:
            logging.error(f"Satır üretme hatası: {str(e)}")
            return f"{self.line_number} REM ERROR: {node.value}"

    def decompile(self):
        logging.debug("Decompile işlemi başlatılıyor")
        try:
            instructions = self.parse_disassembly()
            blocks = self.build_cfg(instructions)
            self.build_ast(blocks)
            return self.emit_code()
        except Exception as e:
            logging.critical(f"Decompile işlemi hatası: {str(e)}")
            raise
