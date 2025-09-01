
```python
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
    0xFFD2: ('CHROUT', 65490),
    0xFFCF: ('CHRIN', 65487),
    0xFFE4: ('GETIN', 65508),
    0xFFCC: ('CLRCHN', 65484),
    0xFFC9: ('CHKIN', 65481),
    0xFFC6: ('CHKOUT', 65478),
    0xFFD5: ('LOAD', 65493),
    0xFFD8: ('SAVE', 65496),
    0xFFDB: ('SETTIM', 65499),
    0xFFDE: ('RDTIM', 65502),
    0xFFE1: ('STOP', 65505),
    0xFFE7: ('CLALL', 65511),
    0xFFEA: ('UDTIM', 65514),
    0xFFED: ('SCREEN', 65517),
    0xFFF0: ('PLOT', 65520),
    0xFFF3: ('IOBASE', 65523)
}

# AST Node sınıfı
class ASTNode:
    def __init__(self, node_type, children=None, value=None, label=None, params=None):
        self.type = node_type  # 'program', 'if', 'for', 'goto', 'gosub', 'assign', 'command', 'kernal_call'
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
            self.defined_addresses = {
                'SID': 53248,  # $D000
                'VIC': 54272,  # $D400
                'CIA1': 56320,  # $DC00
                'CIA2': 56576,  # $DD00
                'BAS_PRG_PTR': 122,  # $7A
                'VAR_PTR': 95,  # $5F
                'KEYBOARD_BUFFER': 631,  # $0277
                # Örnek özel adres (kullanıcı tanımlı)
                'KERIM': 57344  # $DFC0
            }
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
                match = re.match(r'([A-Z_]+)?:?\s*\$?([0-9A-F]{4})?\s*([A-Z]+)\s*(\S.*)?', line)
                if match:
                    label, addr, opcode, operand = match.groups()
                    addr = int(addr, 16) if addr else None
                    operand = operand.strip() if operand else ''
                    if operand.startswith('$'):
                        operand = operand.replace('$', '')
                        if ',' in operand or '),Y' in operand or '),X' in operand:
                            operand = operand.split(',')[0].replace('(', '').replace(')', '')
                        operand = int(operand, 16)
                    elif operand.startswith('#$'):
                        operand = int(operand.replace('#$', ''), 16)
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
                        self.zeropage_vars[operand] = self.special_addresses.get((operand, operand), {}).get('name', f"Z{operand:02x}")
                    if isinstance(operand, int) and operand >= 0xD000:
                        self.variables[operand] = self.io_registers.get(operand, {}).get('name', f"IO_{operand:04x}")
                    if opcode == 'JMP' and isinstance(operand, str) and '),Y' in operand:
                        self.jump_tables[addr] = operand
                    if opcode in ['LDA', 'STA'] and isinstance(operand, int) and operand in self.tokens:
                        self.variables[operand] = self.tokens[operand]
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

    def detect_for_loop(self, block):
        try:
            if len(block) >= 4 and block[0][1] in ['LDX', 'LDY'] and any(b[1] in ['CPX', 'CPY'] for b in block) and any(b[1] in ['INX', 'DEX', 'INY', 'DEY'] for b in block) and any(b[1] == 'BNE' for b in block):
                var = 'X' if block[0][1] == 'LDX' else 'Y'
                init_val = block[0][2]
                cond_idx = next(i for i, b in enumerate(block) if b[1] in ['CPX', 'CPY'])
                limit = block[cond_idx][2]
                incr = 1 if block[0][1] in ['INX', 'INY'] else -1
                target = next(b[2] for b in block if b[1] == 'BNE')
                return 'for', var, init_val, limit, incr, target
            return None, None, None, None, None, None
        except Exception as e:
            logging.error(f"FOR döngüsü tespit hatası: {str(e)}")
            return None, None, None, None, None, None

    def detect_if(self, block):
        try:
            cmp_idx = next((i for i, b in enumerate(block) if b[1] == 'CMP'), None)
            if cmp_idx is not None and cmp_idx + 1 < len(block) and block[cmp_idx+1][1] in ['BEQ', 'BNE']:
                cond_val = block[cmp_idx][2]
                target = block[cmp_idx+1][2]
                return 'if', cond_val, target
            return None, None, None
        except Exception as e:
            logging.error(f"IF tespit hatası: {str(e)}")
            return None, None, None

    def match_pattern(self, block):
        logging.debug(f"Pattern eşleştirme: {block[0][0]:04x}")
        try:
            for_pat, var, init_val, limit, incr, target = self.detect_for_loop(block)
            if for_pat:
                return for_pat, var, (init_val, limit, incr, target)
            if_pat, cond_val, target = self.detect_if(block)
            if if_pat:
                return if_pat, cond_val, target
            if any(b[1] == 'JSR' for b in block):
                jsr_idx = next(i for i, b in enumerate(block) if b[1] == 'JSR')
                return 'gosub', block[jsr_idx][2], None
            if any(b[1] == 'JMP' for b in block):
                jmp_idx = next(i for i, b in enumerate(block) if b[1] == 'JMP')
                return 'goto', block[jmp_idx][2], None
            if any(b[1] in ['LDA', 'STA'] and isinstance(b[2], int) and b[2] in self.tokens for b in block):
                token_idx = next(i for i, b in enumerate(block) if b[1] in ['LDA', 'STA'] and isinstance(b[2], int) and b[2] in self.tokens)
                return 'command', self.tokens[block[token_idx][2]], None
            return None, None, None
        except Exception as e:
            logging.error(f"Pattern eşleştirme hatası: {str(e)}")
            return None, None, None

    def translate_instruction(self, instr):
        logging.debug(f"Talimat çevriliyor: {instr}")
        try:
            addr, op, operand, label = instr
            addr_str = f"${addr:04x}" if addr is not None else ""
            if op == 'LDA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, self.defined_addresses.get(str(operand), operand))) if isinstance(operand, int) else operand
                if isinstance(operand, str) and '),Y' in operand:
                    base_addr = int(operand.split(',')[0].replace('(', ''), 16)
                    val = f"(PEEK({base_addr})*256)+PEEK({base_addr+1})+Y"
                elif isinstance(operand, str) and ',X' in operand:
                    base_addr = int(operand.split(',')[0].replace('$', ''), 16)
                    val = f"{base_addr}+X"
                return ASTNode('assign', value=f"A={val if isinstance(val, str) else f'PEEK({val})'}", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'STA':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, self.defined_addresses.get(str(operand), operand))) if isinstance(operand, int) else operand
                if isinstance(operand, str) and '),Y' in operand:
                    base_addr = int(operand.split(',')[0].replace('(', ''), 16)
                    var = f"(PEEK({base_addr})*256)+PEEK({base_addr+1})+Y"
                elif isinstance(operand, str) and ',X' in operand:
                    base_addr = int(operand.split(',')[0].replace('$', ''), 16)
                    var = f"{base_addr}+X"
                return ASTNode('assign', value=f"POKE {var},A", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'LDX':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"X={val if isinstance(val, str) else f'PEEK({val})'}", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'STX':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"POKE {var},X", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'LDY':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"Y={val if isinstance(val, str) else f'PEEK({val})'}", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'STY':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"POKE {var},Y", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'JSR':
                if operand in self.routines:
                    routine = self.routines[operand]
                    return ASTNode('gosub', value=f"GOSUB {routine['name']}", params=[f"REM {addr_str} {op} ${operand:04x}"])
                elif operand in KERNAL_MAP:
                    return ASTNode('kernal_call', value=f"SYS {KERNAL_MAP[operand][1]}", params=[f"REM {addr_str} {op} ${operand:04x} {KERNAL_MAP[operand][0]}"])
                else:
                    return ASTNode('gosub', value=f"GOSUB SUB_{operand:04x}", params=[f"REM {addr_str} {op} ${operand:04x}"])
            elif op == 'JMP':
                return ASTNode('goto', value=f"GOTO {self.labels.get(operand, f'LABEL_{operand:04x}')}", params=[f"REM {addr_str} {op} ${operand:04x}"])
            elif op == 'RTS':
                return ASTNode('return', value="RETURN", params=[f"REM {addr_str} {op}"])
            elif op == 'INX':
                return ASTNode('assign', value="X=X+1", params=[f"REM {addr_str} {op}"])
            elif op == 'DEX':
                return ASTNode('assign', value="X=X-1", params=[f"REM {addr_str} {op}"])
            elif op == 'INY':
                return ASTNode('assign', value="Y=Y+1", params=[f"REM {addr_str} {op}"])
            elif op == 'DEY':
                return ASTNode('assign', value="Y=Y-1", params=[f"REM {addr_str} {op}"])
            elif op == 'CMP':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('expr', value=f"A={val if isinstance(val, str) else f'PEEK({val})'}", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'BEQ':
                return ASTNode('if', value=f"IF A=0 THEN GOTO {self.labels.get(operand, f'LABEL_{operand:04x}')}", params=[f"REM {addr_str} {op} ${operand:04x}"])
            elif op == 'BNE':
                return ASTNode('if', value=f"IF A<>0 THEN GOTO {self.labels.get(operand, f'LABEL_{operand:04x}')}", params=[f"REM {addr_str} {op} ${operand:04x}"])
            elif op == 'ADC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"A=A+{val if isinstance(val, str) else f'PEEK({val})'}", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'SBC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"A=A-{val if isinstance(val, str) else f'PEEK({val})'}", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'AND':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"A=A AND {val if isinstance(val, str) else f'PEEK({val})'}", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'ORA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"A=A OR {val if isinstance(val, str) else f'PEEK({val})'}", params=[f"REM {addr_str} {op} ${operand:04x}" if isinstance(operand, int) else f"REM {addr_str} {op} {operand}"])
            elif op == 'ASL':
                return ASTNode('assign', value="A=A*2", params=[f"REM {addr_str} {op}"])
            elif op == 'LSR':
                return ASTNode('assign', value="A=A/2", params=[f"REM {addr_str} {op}"])
            elif op == 'SEI':
                return ASTNode('assign', value="REM SEI", params=[f"REM {addr_str} Disable Interrupts"])
            elif op == 'CLI':
                return ASTNode('assign', value="REM CLI", params=[f"REM {addr_str} Enable Interrupts"])
            elif op == 'BRK':
                return ASTNode('assign', value="REM BRK", params=[f"REM {addr_str} Interrupt"])
            return ASTNode('assign', value=f"REM {op} {operand}", params=[f"REM {addr_str} {op} {operand}"])
        except Exception as e:
            logging.error(f"Talimat çevirme hatası: {str(e)}")
            return ASTNode('assign', value=f"REM ERROR: {op} {operand}", params=[f"REM {addr_str} ERROR"])

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
                        elif operand in self.defined_addresses:
                            var_name = self.defined_addresses[str(operand)]
                            self.variables[operand] = var_name
                        elif operand not in self.variables:
                            self.variables[operand] = f"V{operand:04x}"
                if pattern == 'for':
                    var, init_val, limit, incr, target = cond_val
                    init = f"{var}={init_val if isinstance(init_val, str) else f'PEEK({init_val})'}"
                    cond = f"{var}<={limit if isinstance(limit, str) else f'PEEK({limit})'}" if incr > 0 else f"{var}>={limit if isinstance(limit, str) else f'PEEK({limit})'}"
                    incr_stmt = f"{var}={var}+{incr}"
                    body = [b for b in block if b[1] not in ['LDX', 'LDY', 'CPX', 'CPY', 'INX', 'DEX', 'INY', 'DEY', 'BNE']]
                    self.ast.children.append(
                        ASTNode('for', [
                            ASTNode('assign', value=init, params=[f"REM {block[0][0]:04x} {block[0][1]} ${block[0][2]:04x}"]),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=incr_stmt),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], label=self.labels.get(target))
                    )
                elif pattern == 'if':
                    cond = f"A={self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val)) if isinstance(cond_val, int) else cond_val}"
                    then_block = [b for b in block if b[2] == target or b[1] not in ['CMP', 'BEQ', 'BNE']]
                    self.ast.children.append(
                        ASTNode('if', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in then_block])
                        ], label=self.labels.get(target))
                    )
                elif pattern == 'gosub':
                    self.ast.children.append(ASTNode('gosub', value=f"GOSUB {self.subroutines.get(cond_val, f'SUB_{cond_val:04x}')}", params=[f"REM {block[0][0]:04x} JSR ${cond_val:04x}"]))
                elif pattern == 'goto':
                    self.ast.children.append(ASTNode('goto', value=f"GOTO {self.labels.get(cond_val, f'LABEL_{cond_val:04x}')}", params=[f"REM {block[0][0]:04x} JMP ${cond_val:04x}"]))
                elif pattern == 'command':
                    self.ast.children.append(ASTNode('command', value=cond_val, params=[f"REM {block[0][0]:04x} Token {cond_val}"]))
                else:
                    for instr in block:
                        self.ast.children.append(self.translate_instruction(instr))
        except Exception as e:
            logging.critical(f"AST oluşturma hatası: {str(e)}")
            raise

    def emit_code(self):
        logging.debug("Commodore BASIC V2 kodu üretiliyor")
        try:
            lines = [
                '0 REM C64 BASIC Dekompilasyonu',
                '10 VIC=53248:REM $D000 VIC-II',
                '20 SID=54272:REM $D400 SID',
                '30 CIA1=56320:REM $DC00 CIA1',
                '40 CIA2=56576:REM $DD00 CIA2',
                '50 BAS_PRG_PTR=122:REM $7A-$7B Program Isaretcisi',
                '60 VAR_PTR=95:REM $5F-$60 Degisken Isaretcisi',
                '70 KEYBOARD_BUFFER=631:REM $0277 Klavye Kuyrugu',
                '80 KERIM=57344:REM $DFC0 Kullanici Tanimli Rutin'
            ]
            for addr, (name, sys_addr) in KERNAL_MAP.items():
                lines.append(f"{self.line_number} {name}={sys_addr}:REM ${addr:04x} {name}")
                self.line_number += 10
            for addr, sub_name in self.subroutines.items():
                lines.append(f"{self.line_number} REM {sub_name}")
                self.line_number += 10
            lines.append(f"{self.line_number} REM Ana Program")
            self.line_number += 10
            for node in self.ast.children:
                if node.type == 'for':
                    init = node.children[0].value
                    cond = node.children[1].value
                    incr = node.children[2].value
                    body = [self.emit_line(n) for n in node.children[3].children]
                    var = init.split('=')[حن0].strip()
                    limit = cond.split('<=')[1].strip() if '<=' in cond else cond.split('>=')[1].strip()
                    lines.append(f"{self.line_number} {var}={init.split('=')[1].strip()} TO {limit} STEP {incr.split('=')[1].split('+')[1]}")
                    self.line_number += 10
                    lines.extend(body)
                    lines.append(f"{self.line_number} NEXT {var}")
                    self.line_number += 10
                    lines.extend(node.children[0].params + node.children[2].params)
                elif node.type == 'if':
                    cond = node.children[0].value
                    then_block = [self.emit_line(n) for n in node.children[1].children]
                    lines.append(f"{self.line_number} IF {cond} THEN GOTO {node.label}")
                    self.line_number += 10
                    lines.extend(then_block)
                elif node.type == 'gosub':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                    lines.extend(node.params)
                elif node.type == 'goto':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                    lines.extend(node.params)
                elif node.type == 'command':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                    lines.extend(node.params)
                elif node.type == 'assign':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                    lines.extend(node.params)
                elif node.type == 'kernal_call':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                    lines.extend(node.params)
                elif node.type == 'return':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                    lines.extend(node.params)
            for addr, sub_name in self.subroutines.items():
                lines.append(f"{self.line_number} RETURN:REM {sub_name} Sonu")
                self.line_number += 10
            logging.info("Commodore BASIC V2 kodu başarıyla üretildi")
            return '\n'.join(lines)
        except Exception as e:
            logging.critical(f"Kod üretme hatası: {str(e)}")
            raise

    def emit_line(self, node):
        logging.debug(f"Satır üretiliyor: {node.value}")
        try:
            line = f"{self.line_number} {node.value}"
            self.line_number += 10
            for param in node.params:
                lines.append(f"{self.line_number} {param}")
                self.line_number += 10
            return line
        except Exception as e:
            logging.error(f"Satır üretme hatası: {str(e)}")
            return f"{self.line_number} REM ERROR: {node.value}"

    def decompile(self):
        logging.debug("Decompile işlemi başlatılıyor")
        try:
            instructions = self.parse_disassembly()
            if not instructions:
                logging.error("Boş veya geçersiz disassembly dosyası")
                raise ValueError("Disassembly dosyası boş veya geçersiz")
            blocks = self.build_cfg(instructions)
            if not blocks:
                logging.error("CFG oluşturulamadı")
                raise ValueError("Kontrol akış grafiği oluşturulamadı")
            self.build_ast(blocks)
            if not self.ast.children:
                logging.error("AST oluşturulmadı")
                raise ValueError("AST boş")
            return self.emit_code()
        except Exception as e:
            logging.critical(f"Decompile işlemi hatası: {str(e)}")
            raise
```

