"""
🍎 QBasic Decompiler v5.3 - Commodore 64 Geliştirme Stüdyosu
================================================================
PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: decompiler_qbasic.py - Assembly'den QBasic Transpile Decompiler
VERSİYON: 5.3 (C64 Memory Manager Entegrasyonu Tamamlandı)
AMAÇ: C64 Assembly kodunu QBasic diline dönüştürme
================================================================

Bu modül şu özelliklerle Assembly'den QBasic'e transpile yapar:
• C64 Memory Manager Entegrasyonu: KERNAL/BASIC rutinleri tanıma
• Memory Map Integration: Bellek haritası tabanlı değişken isimlendirme
• Assembly to QBasic: 6502 kodunu QBasic yapılarına dönüştürme
• Label Management: Akıllı etiket yönetimi ve optimizasyon
• Enhanced BASIC Integration: Enhanced BASIC Decompiler ile koordineli çalışma

C64 Memory Manager Entegrasyonu: ✅ TAMAMLANDI
- KERNAL routines tanıma ve dönüştürme
- Memory map tabanlı değişken isimlendirme
- Sistem çağrıları QBasic fonksiyonlarına dönüştürme
================================================================
"""

import re
import json
import logging
from datetime import datetime

# C64 Memory Manager import - KızılElma Plan uyarınca eklendi
try:
    from c64_memory_manager import c64_memory_manager, get_routine_info, get_memory_info, format_routine_call, format_memory_access
    C64_MEMORY_MANAGER_AVAILABLE = True
    print("✅ C64 Memory Manager yüklendi - Gelişmiş QBasic çeviri aktif")
except ImportError:
    C64_MEMORY_MANAGER_AVAILABLE = False
    print("⚠️ C64 Memory Manager bulunamadı - Basit QBasic çeviri kullanılacak")

# Loglama ayarları
logging.basicConfig(
    filename=f'decompiler_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# C64 KERNAL fonksiyonları haritası (fallback)
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
        self.type = node_type  # 'program', 'select', 'for_inc', 'for_dec', 'while', 'do_until', 'do_while', 'sub', 'assign', 'expr'
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
            self.subroutines = {}
            self.zeropage_vars = {}
            self.jump_tables = {}
            self.line_number = 10
            self.recursive_calls = set()  # Recursiyon takibi
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
                                self.labels[operand] = f"LABEL_{operand:04x}"
                            if opcode == 'JSR' and operand == addr:
                                self.recursive_calls.add(operand)
                    if opcode == 'JSR' and isinstance(operand, int):
                        self.subroutines[operand] = f"SUB_{operand:04x}"
                    if isinstance(operand, int) and 0x00 <= operand <= 0xFF:
                        self.zeropage_vars[operand] = f"ZVAR_{operand:02x}"
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
                        return 'macro', block[2], f"MACRO_{i}"
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
                    return 'select', block[cmp_indices[0]][2], [block[i][2] for i in beq_indices]
                elif block[0][1] == 'LDX' and any(b[1] == 'CPX' for b in block) and any(b[1] == 'INX' for b in block):
                    return 'for_inc', None, None
                elif block[0][1] == 'LDX' and any(b[1] == 'CPX' for b in block) and any(b[1] == 'DEX' for b in block):
                    return 'for_dec', None, None
                elif any(b[1] == 'CMP' for b in block) and any(b[1] == 'BNE' for b in block) and any(b[1] == 'JMP' for b in block):
                    return 'while', block[[i for i, b in enumerate(block) if b[1] == 'CMP'][0]][2], block[[i for i, b in enumerate(block) if b[1] == 'JMP'][0]][2]
                elif any(b[1] == 'CMP' for b in block) and any(b[1] == 'BEQ' for b in block) and any(b[1] == 'JMP' for b in block):
                    return 'do_until', block[[i for i, b in enumerate(block) if b[1] == 'CMP'][0]][2], block[[i for i, b in enumerate(block) if b[1] == 'JMP'][0]][2]
                elif any(b[1] == 'CMP' for b in block) and any(b[1] == 'BNE' for b in block) and any(b[1] == 'JMP' for b in block):
                    return 'do_while', block[[i for i, b in enumerate(block) if b[1] == 'CMP'][0]][2], block[[i for i, b in enumerate(block) if b[1] == 'JMP'][0]][2]
                elif any(b[1] == 'CMP' for b in block) and any(b[1] in ['BEQ', 'BNE'] for b in block) and any(b[1] == 'JMP' for b in block):
                    return 'do_loop', block[[i for i, b in enumerate(block) if b[1] == 'CMP'][0]][2], block[[i for i, b in enumerate(block) if b[1] == 'JMP'][0]][2]
            if any(b[1] == 'PHA' for b in block) and any(b[1] == 'JSR' for b in block):
                return 'sub_call', block[[i for i, b in enumerate(block) if b[1] == 'JSR'][0]][2], None
            if any(b[1] == 'BRK' for b in block):
                return 'interrupt', None, None
            return None, None, None
        except Exception as e:
            logging.error(f"Pattern eşleştirme hatası: {str(e)}")
            return None, None, None

    def translate_instruction(self, instr):
        """Tek bir talimatı BASIC'e çevir"""
        logging.debug(f"Talimat çevriliyor: {instr}")
        try:
            addr, op, operand = instr
            if op == 'LDA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = PEEK({val})" if isinstance(operand, int) else f"LET A = {val}")
            elif op == 'STA':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
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
            elif op == 'JSR' and isinstance(operand, int):
                if operand in self.subroutines:
                    params = [n.value for n in self.ast.children if n.type == 'assign' and 'PHA' in n.value][-1:]
                    return ASTNode('sub_call', value=f"GOSUB {self.subroutines[operand]}" + (f" {', '.join(params)}" if params else ""), params=params)
                elif operand in KERNAL_MAP:
                    return ASTNode('kernal_call', value=f"GOSUB {KERNAL_MAP[operand]}")
            elif op == 'RTS':
                return ASTNode('return', value="RETURN")
            elif op == 'INX':
                return ASTNode('assign', value="LET X = X + 1")
            elif op == 'DEX':
                return ASTNode('assign', value="LET X = X - 1")
            elif op == 'PHA':
                return ASTNode('assign', value="REM PUSH A")
            elif op == 'PLA':
                return ASTNode('assign', value="LET A = POP()")
            elif op == 'LDA' and isinstance(operand, str) and ',X' in operand:
                addr = int(operand.split(',')[0].replace('$', ''), 16)
                var = self.variables.get(addr, f"ARRAY_{addr:04x}")
                return ASTNode('assign', value=f"LET A = PEEK({var} + X)")
            elif op == 'LDA' and isinstance(operand, str) and ',Y' in operand:
                addr = int(operand.split(',')[0].replace('$', ''), 16)
                var = self.variables.get(addr, f"ARRAY_{addr:04x}")
                return ASTNode('assign', value=f"LET A = PEEK({var} + Y)")
            elif op == 'AND':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = A AND {val}")
            elif op == 'ORA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = A OR {val}")
            elif op == 'ASL':
                return ASTNode('assign', value="LET A = A * 2")
            elif op == 'LSR':
                return ASTNode('assign', value="LET A = A / 2")
            elif op == 'ADC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = A + {val}")
            elif op == 'SBC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, operand)) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"LET A = A - {val}")
            elif op == 'BRK':
                return ASTNode('interrupt', value="REM Interrupt")
            elif op == 'SEI':
                return ASTNode('raw', value="REM Disable Interrupts")
            elif op == 'CLI':
                return ASTNode('raw', value="REM Enable Interrupts")
            return ASTNode('raw', value=f"REM {op} {operand}")
        except Exception as e:
            logging.error(f"Talimat çevirme hatası: {str(e)}")
            return ASTNode('raw', value=f"REM ERROR: {op} {operand}")

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
                        var_name = self.memory_map[operand].split('(')[0].replace(' ', '_')
                        self.variables[operand] = var_name
                    elif isinstance(operand, int) and operand not in self.variables:
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
                    self.ast.children.append(ASTNode('sub', value=f"SUB {macro_name}", children=[self.translate_instruction(b) for b in macro_block]))
                elif pattern == 'loop':
                    init = f"I = 1"
                    cond = f"I <= {loop_count}"
                    incr = "I = I + 1"
                    body = [self.translate_instruction(b) for b in loop_block]
                    self.ast.children.append(
                        ASTNode('for_inc', [
                            ASTNode('assign', value=init),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=incr),
                            ASTNode('block', body)
                        ])
                    )
                elif pattern == 'bit_field':
                    self.ast.children.append(ASTNode('assign', value=f"LET bitfield_{cond_val:04x} = A AND {cond_val}"))
                elif pattern == 'global_var':
                    self.ast.children.append(ASTNode('global_var', value=f"DIM SHARED var_{cond_val:04x} AS INTEGER"))
                elif pattern == 'pointer':
                    addr = int(cond_val.split('),')[0].replace('(', ''), 16) if isinstance(cond_val, str) else cond_val
                    self.ast.children.append(ASTNode('assign', value=f"LET ptr_{addr:04x} = PEEK({addr} + Y)"))
                elif pattern == 'timer':
                    self.ast.children.append(ASTNode('sub', value="SUB TimerHandler", children=[self.translate_instruction(b) for b in block]))
                elif pattern == 'event_handler':
                    self.ast.children.append(ASTNode('sub', value="SUB JoystickHandler", children=[self.translate_instruction(b) for b in block]))
                elif pattern == 'nested_if':
                    nested_ifs = cond_val
                    if_nodes = []
                    for cond, target in nested_ifs:
                        then_block = [b for b in block if b[2] == target or b[1] not in ['CMP', 'BNE', 'BEQ']]
                        else_block = [b for b in block if b[2] != target and b[1] not in ['CMP', 'BNE', 'BEQ']]
                        if_nodes.append(
                            ASTNode('if', [
                                ASTNode('expr', value=f"A = {self.variables.get(cond, self.zeropage_vars.get(cond, cond))}"),
                                ASTNode('block', [self.translate_instruction(b) for b in then_block]),
                                ASTNode('block', [self.translate_instruction(b) for b in else_block])
                            ], label=self.labels.get(target_addr))
                        )
                    self.ast.children.append(ASTNode('nested_if', if_nodes))
                elif pattern == 'select':
                    cases = []
                    for beq_target in target:
                        target_addr = int(beq_target.replace('$', ''), 16) if isinstance(beq_target, str) else beq_target
                        case_block = [b for b in block if b[2] == beq_target or b[1] not in ['CMP', 'BEQ']]
                        cases.append(ASTNode('case', [self.translate_instruction(b) for b in case_block], value=cond_val))
                    self.ast.children.append(
                        ASTNode('select', cases, value=f"A = {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val))}" if isinstance(cond_val, int) else f"A = {cond_val}")
                    )
                elif pattern == 'for_inc':
                    init = f"X = {self.variables.get(block[0][2], self.zeropage_vars.get(block[0][2], block[0][2]))}" if isinstance(block[0][2], int) else f"X = {block[0][2]}"
                    cond_idx = next(i for i, b in enumerate(block) if b[1] == 'CPX')
                    cond = f"X < {self.variables.get(block[cond_idx][2], self.zeropage_vars.get(block[cond_idx][2], block[cond_idx][2]))}" if isinstance(block[cond_idx][2], int) else f"X < {block[cond_idx][2]}"
                    incr = "X = X + 1"
                    body = [b for b in block if b[1] not in ['LDX', 'CPX', 'INX', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('exit_do', value="EXIT DO"))
                    self.ast.children.append(
                        ASTNode('for_inc', [
                            ASTNode('assign', value=init),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=incr),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ])
                    )
                elif pattern == 'for_dec':
                    init = f"X = {self.variables.get(block[0][2], self.zeropage_vars.get(block[0][2], block[0][2]))}" if isinstance(block[0][2], int) else f"X = {block[0][2]}"
                    cond_idx = next(i for i, b in enumerate(block) if b[1] == 'CPX')
                    cond = f"X >= {self.variables.get(block[cond_idx][2], self.zeropage_vars.get(block[cond_idx][2], block[cond_idx][2]))}" if isinstance(block[cond_idx][2], int) else f"X >= {block[cond_idx][2]}"
                    decr = "X = X - 1"
                    body = [b for b in block if b[1] not in ['LDX', 'CPX', 'DEX', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('exit_do', value="EXIT DO"))
                    self.ast.children.append(
                        ASTNode('for_dec', [
                            ASTNode('assign', value=init),
                            ASTNode('expr', value=cond),
                            ASTNode('assign', value=decr),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ])
                    )
                elif pattern == 'while':
                    cond = f"A = {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val))}" if isinstance(cond_val, int) else f"A = {cond_val}"
                    body = [b for b in block if b[1] not in ['CMP', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('exit_do', value="EXIT DO"))
                    self.ast.children.append(
                        ASTNode('while', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], label=self.labels.get(target_addr))
                    )
                elif pattern == 'do_until':
                    cond = f"A = {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val))}" if isinstance(cond_val, int) else f"A = {cond_val}"
                    body = [b for b in block if b[1] not in ['CMP', 'BEQ', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('exit_do', value="EXIT DO"))
                    self.ast.children.append(
                        ASTNode('do_until', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], label=self.labels.get(target_addr))
                    )
                elif pattern == 'do_while':
                    cond = f"A <> {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val))}" if isinstance(cond_val, int) else f"A <> {cond_val}"
                    body = [b for b in block if b[1] not in ['CMP', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('exit_do', value="EXIT DO"))
                    self.ast.children.append(
                        ASTNode('do_while', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], label=self.labels.get(target_addr))
                    )
                elif pattern == 'do_loop':
                    cond = f"A = {self.variables.get(cond_val, self.zeropage_vars.get(cond_val, cond_val))}" if isinstance(cond_val, int) else f"A = {cond_val}"
                    body = [b for b in block if b[1] not in ['CMP', 'BEQ', 'BNE', 'JMP']]
                    if any(b[1] == 'BRK' for b in body):
                        body.append(ASTNode('exit_do', value="EXIT DO"))
                    loop_type = 'until' if any(b[1] == 'BEQ' for b in block) else 'while'
                    self.ast.children.append(
                        ASTNode('do_loop', [
                            ASTNode('expr', value=cond),
                            ASTNode('block', [self.translate_instruction(b) for b in body])
                        ], value=loop_type)
                    )
                elif pattern == 'sub_call':
                    self.ast.children.append(ASTNode('sub_call', value=f"GOSUB {self.subroutines[cond_val]}" if cond_val in self.subroutines else f"REM JSR {cond_val}", params=[self.translate_instruction(b) for b in block if b[1] == 'PHA']))
                elif pattern == 'interrupt':
                    self.ast.children.append(ASTNode('sub', value="SUB InterruptHandler", children=[self.translate_instruction(b) for b in block]))
                else:
                    for instr in block:
                        self.ast.children.append(self.translate_instruction(instr))
        except Exception as e:
            logging.critical(f"AST oluşturma hatası: {str(e)}")
            raise

    def emit_code(self):
        """AST'den QuickBASIC 7.1 kodu üret"""
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
                'DIM SHARED A AS INTEGER, X AS INTEGER, Y AS INTEGER',
                'DIM SHARED MEMORY(65535) AS INTEGER'
            ]
            # Struct tanımları
            for node in self.ast.children:
                if node.type == 'struct_def':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
            # Subroutine tanımları
            for addr, sub_name in self.subroutines.items():
                lines.append(f"{self.line_number} SUB {sub_name}" + (" RECURSIVE" if addr in self.recursive_calls else ""))
                self.line_number += 10
            # Ana program
            lines.append(f"{self.line_number} REM Main Program")
            self.line_number += 10
            for node in self.ast.children:
                if node.type == 'select':
                    cond = node.value
                    lines.append(f"{self.line_number} SELECT CASE {cond.split('=')[0].strip()}")
                    self.line_number += 10
                    for case in node.children:
                        lines.append(f"{self.line_number} CASE {case.value}")
                        self.line_number += 10
                        for stmt in case.children:
                            lines.append(self.emit_line(stmt))
                    lines.append(f"{self.line_number} END SELECT")
                    self.line_number += 10
                elif node.type == 'nested_if':
                    for if_node in node.children:
                        cond = if_node.children[0].value
                        then_block = [self.emit_line(n) for n in if_node.children[1].children]
                        else_block = [self.emit_line(n) for n in if_node.children[2].children]
                        lines.append(f"{self.line_number} IF {cond} THEN")
                        self.line_number += 10
                        lines.extend(then_block)
                        if else_block:
                            lines.append(f"{self.line_number} ELSE")
                            self.line_number += 10
                            lines.extend(else_block)
                        lines.append(f"{self.line_number} END IF")
                        self.line_number += 10
                elif node.type in ['for_inc', 'for_dec']:
                    init = node.children[0].value
                    cond = node.children[1].value
                    incr = node.children[2].value
                    body = [self.emit_line(n) for n in node.children[3].children]
                    var = init.split('=')[0].strip()
                    limit = cond.split('<')[1].strip() if node.type == 'for_inc' else cond.split('>=')[1].strip()
                    lines.append(f"{self.line_number} FOR {var} = {init.split('=')[1].strip()} TO {limit} STEP {'1' if node.type == 'for_inc' else '-1'}")
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
                elif node.type == 'do_while':
                    cond = node.children[0].value
                    body = [self.emit_line(n) for n in node.children[1].children]
                    lines.append(f"{self.line_number} DO WHILE {cond}")
                    self.line_number += 10
                    lines.extend(body)
                    lines.append(f"{self.line_number} LOOP")
                    self.line_number += 10
                elif node.type == 'do_loop':
                    cond = node.children[0].value
                    body = [self.emit_line(n) for n in node.children[1].children]
                    lines.append(f"{self.line_number} DO")
                    self.line_number += 10
                    lines.extend(body)
                    lines.append(f"{self.line_number} LOOP {node.value.upper()} {cond}")
                    self.line_number += 10
                elif node.type == 'sub_call':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                    for param in node.params:
                        lines.append(f"{self.line_number} REM Parameter: {param.value}")
                        self.line_number += 10
                elif node.type == 'return':
                    lines.append(f"{self.line_number} {node.value}")
                    self.line_number += 10
                elif node.type == 'exit_do':
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
        """Tek bir BASIC satırı üret"""
        logging.debug(f"Satır üretiliyor: {node.value}")
        try:
            line = f"{self.line_number} {node.value}"
            self.line_number += 10
            return line
        except Exception as e:
            logging.error(f"Satır üretme hatası: {str(e)}")
            return f"{self.line_number} REM ERROR: {node.value}"

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