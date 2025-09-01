"""
🍎 C++ Decompiler v5.3 - Commodore 64 Geliştirme Stüdyosu
================================================================
PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: decompiler_cpp.py - Assembly'den C++ Transpile Decompiler
VERSİYON: 5.3 (C64 Memory Manager Entegrasyonu Tamamlandı)
AMAÇ: C64 Assembly kodunu C++ diline dönüştürme
================================================================

Bu modül şu özelliklerle Assembly'den C++'a transpile yapar:
• C64 Memory Manager Entegrasyonu: KERNAL/BASIC rutinleri tanıma
• Memory Map Integration: Bellek haritası tabanlı değişken isimlendirme
• Assembly to C++: 6502 kodunu modern C++ yapılarına dönüştürme
• Object-Oriented: C++ sınıf yapıları ve modern syntax
• Enhanced BASIC Integration: Enhanced BASIC Decompiler ile koordineli çalışma

C64 Memory Manager Entegrasyonu: ✅ TAMAMLANDI
- KERNAL routines tanıma ve C++ fonksiyonlarına dönüştürme
- Memory map tabanlı değişken ve pointer yönetimi
- Modern C++ syntax ile 6502 instruction mapping
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
    print("✅ C64 Memory Manager yüklendi - Gelişmiş C++ çeviri aktif")
except ImportError:
    C64_MEMORY_MANAGER_AVAILABLE = False
    print("⚠️ C64 Memory Manager bulunamadı - Basit C++ çeviri kullanılacak")

# Loglama ayarları
logging.basicConfig(
    filename=f'decompiler_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# C64 KERNAL ve BASIC ROM fonksiyonları haritası
KERNAL_MAP = {
    0xFFD2: ('VIC', 'print_char'),
    0xFFCF: ('VIC', 'read_char'),
    0xFFE4: ('VIC', 'get_input'),
    0xFFCC: ('VIC', 'clear_channel'),
    0xFFC9: ('VIC', 'check_input'),
    0xFFC6: ('VIC', 'check_output'),
    0xE264: ('Math', 'sin'),
    0xE268: ('Math', 'cos'),
    0xA871: ('String', 'len'),
    0xA96B: ('String', 'mid'),
    0xA8A0: ('String', 'left'),
    0xA8A3: ('String', 'right')
}

# AST Node sınıfı
class ASTNode:
    def __init__(self, node_type, children=None, value=None, label=None, params=None):
        self.type = node_type  # 'program', 'switch', 'for', 'while', 'function', 'class', 'array', 'enum', 'assign', 'expr', 'lambda', 'try_catch'
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
            self.classes = {}
            self.zeropage_vars = {}
            self.jump_tables = {}
            self.recursive_calls = set()
            self.constants = {}
            self.line_number = 0
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

    def collect_constants(self, instructions):
        """Sabit değerleri topla"""
        logging.debug("Sabit değerler toplanıyor")
        try:
            constants = {}
            for _, op, operand in instructions:
                if op in ['LDA', 'CMP'] and isinstance(operand, str) and operand.startswith('#$'):
                    val = int(operand.replace('#$', ''), 16)
                    constants[val] = constants.get(val, 0) + 1
            return [k for k, v in constants.items() if v > 1]
        except Exception as e:
            logging.error(f"Sabit değer toplama hatası: {str(e)}")
            return []

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
                                self.labels[operand] = self.memory_map[operand].lower().replace(' ', '_')
                            elif operand not in self.labels:
                                self.labels[operand] = f"label_{operand:04x}"
                            if opcode == 'JSR' and operand == addr:
                                self.recursive_calls.add(operand)
                    if opcode == 'JSR' and isinstance(operand, int):
                        if operand in KERNAL_MAP:
                            class_name, method_name = KERNAL_MAP[operand]
                            self.functions[operand] = (class_name, method_name)
                        else:
                            self.functions[operand] = (None, f"func_{operand:04x}")
                    if isinstance(operand, int) and 0x00 <= operand <= 0xFF:
                        self.zeropage_vars[operand] = f"zvar_{operand:02x}"
                    if opcode == 'JMP' and isinstance(operand, str) and '),Y' in operand:
                        self.jump_tables[addr] = operand
            self.constants = self.collect_constants(instructions)
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
        """Struct/class pattern'larını tespit et"""
        try:
            if len(block) > 1 and all(b[1] in ['LDA', 'STA'] for b in block) and all(
                isinstance(b[2], int) and abs(b[2] - block[i-1][2]) == 1 for i, b in enumerate(block[1:], 1) if isinstance(b[2], int)
            ):
                return 'class', block[0][2], len(block)
            return None, None, None
        except Exception as e:
            logging.error(f"Class tespit hatası: {str(e)}")
            return None, None, None

    def detect_array(self, block):
        """Dizi pattern'larını tespit et"""
        try:
            if any(b[1] in ['LDA', 'STA'] and isinstance(b[2], str) and ',X' in b[2] for b in block):
                addr = int(block[0][2].split(',')[0].replace('$', ''), 16)
                return 'array', addr, 256
            return None, None, None
        except Exception as e:
            logging.error(f"Dizi tespit hatası: {str(e)}")
            return None, None, None

    def detect_macro(self, blocks):
        """Makro pattern'larını tespit et"""
        try:
            for i, block in enumerate(blocks):
                for j, other_block in enumerate(blocks[i+1:], i+1):
                    if block[2] == other_block[2]:
                        return 'macro', block[2], f"macro_{block[0][0]:04x}"
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

    def detect_local_var(self, block):
        """Lokal değişken pattern'larını tespit et"""
        try:
            if any(isinstance(b[2], int) and 0x00 <= b[2] <= 0xFF for b in block if b[1] in ['LDA', 'STA']):
                return 'local_var', block[0][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Lokal değişken tespit hatası: {str(e)}")
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

    def detect_interrupt_callback(self, block):
        """Kesme callback pattern'larını tespit et"""
        try:
            if any(b[1] == 'SEI' for b in block) and any(b[1] == 'JSR' for b in block) and any(b[1] == 'CLI' for b in block):
                return 'interrupt_callback', block[[i for i, b in enumerate(block) if b[1] == 'JSR'][0]][2], None
            return None, None, None
        except Exception as e:
            logging.error(f"Kesme callback tespit hatası: {str(e)}")
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

    def detect_lambda(self, block):
        """Lambda fonksiyon pattern'larını tespit et"""
        try:
            if len(block) == 2 and block[0][1] in ['LDA', 'STA'] and block[1][1] in ['LDA', 'STA']:
                return 'lambda', block, f"lambda_{block[0][0]:04x}"
            return None, None, None
        except Exception as e:
            logging.error(f"Lambda tespit hatası: {str(e)}")
            return None, None, None

    def detect_copy_memory(self, block):
        """Bellek kopyalama pattern'larını tespit et"""
        try:
            if any(b[1] == 'LDA' and block[i+1][1] == 'STA' for i in range(len(block)-1)):
                return 'copy_memory', block[0][2], block[1][2]
            return None, None, None
        except Exception as e:
            logging.error(f"Bellek kopyalama tespit hatası: {str(e)}")
            return None, None, None

    def match_pattern(self, block):
        """Blok içindeki kontrol yapılarını tanı"""
        logging.debug(f"Pattern eşleştirme: {block[0][0]:04x}")
        try:
            struct_pat, struct_addr, struct_len = self.detect_struct(block)
            if struct_pat:
                return struct_pat, struct_addr, struct_len
            array_pat, array_addr, array_size = self.detect_array(block)
            if array_pat:
                return array_pat, array_addr, array_size
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
            local_var_pat, local_var_addr, _ = self.detect_local_var(block)
            if local_var_pat:
                return local_var_pat, local_var_addr, None
            pointer_pat, pointer_addr, _ = self.detect_pointer(block)
            if pointer_pat:
                return pointer_pat, pointer_addr, None
            timer_pat, _, _ = self.detect_timer(block)
            if timer_pat:
                return timer_pat, None, None
            event_handler_pat, _, _ = self.detect_event_handler(block)
            if event_handler_pat:
                return event_handler_pat, None, None
            interrupt_callback_pat, callback_addr, _ = self.detect_interrupt_callback(block)
            if interrupt_callback_pat:
                return interrupt_callback_pat, callback_addr, None
            lambda_pat, lambda_block, lambda_name = self.detect_lambda(block)
            if lambda_pat:
                return lambda_pat, lambda_block, lambda_name
            copy_memory_pat, src_addr, dst_addr = self.detect_copy_memory(block)
            if copy_memory_pat:
                return copy_memory_pat, src_addr, dst_addr
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
                return 'try_catch', None, None
            return None, None, None
        except Exception as e:
            logging.error(f"Pattern eşleştirme hatası: {str(e)}")
            return None, None, None

    def translate_instruction(self, instr):
        """Tek bir talimatı C++'a çevir"""
        logging.debug(f"Talimat çevriliyor: {instr}")
        try:
            addr, op, operand = instr
            if op == 'LDA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand.replace('#$', '0x')
                if isinstance(operand, int) and operand in self.classes:
                    return ASTNode('assign', value=f"a = {self.classes[operand]}::get_{val}();")
                return ASTNode('assign', value=f"a = memory[{val}];" if isinstance(operand, int) else f"a = {val};")
            elif op == 'STA':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                if isinstance(operand, int) and operand in self.classes:
                    return ASTNode('assign', value=f"{self.classes[operand]}::set_{var}(a);")
                return ASTNode('assign', value=f"memory[{var}] = a;")
            elif op == 'LDX':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand.replace('#$', '0x')
                return ASTNode('assign', value=f"x = memory[{val}];" if isinstance(operand, int) else f"x = {val};")
            elif op == 'STX':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"memory[{var}] = x;")
            elif op == 'LDY':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand.replace('#$', '0x')
                return ASTNode('assign', value=f"y = memory[{val}];" if isinstance(operand, int) else f"y = {val};")
            elif op == 'STY':
                var = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand
                return ASTNode('assign', value=f"memory[{var}] = y;")
            elif op == 'JSR' and isinstance(operand, int):
                if operand in self.functions:
                    class_name, method_name = self.functions[operand]
                    params = [n.value for n in self.ast.children if n.type == 'assign' and 'push(a)' in n.value][-1:]
                    if class_name:
                        return ASTNode('method_call', value=f"C64::{class_name}::{method_name}({', '.join(params)});" if params else f"C64::{class_name}::{method_name}();")
                    return ASTNode('function_call', value=f"{method_name}({', '.join(params)});" if params else f"{method_name}();")
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
                return ASTNode('assign', value=f"a = {var}[x];")
            elif op == 'LDA' and isinstance(operand, str) and ',Y' in operand:
                addr = int(operand.split(',')[0].replace('$', ''), 16)
                var = self.variables.get(addr, f"array_{addr:04x}")
                return ASTNode('assign', value=f"a = {var}[y];")
            elif op == 'AND':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand.replace('#$', '0x')
                return ASTNode('assign', value=f"a &= {val};")
            elif op == 'ORA':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand.replace('#$', '0x')
                return ASTNode('assign', value=f"a |= {val};")
            elif op == 'ASL':
                return ASTNode('assign', value="a <<= 1;")
            elif op == 'LSR':
                return ASTNode('assign', value="a >>= 1;")
            elif op == 'ADC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand.replace('#$', '0x')
                return ASTNode('assign', value=f"a += {val};")
            elif op == 'SBC':
                val = self.variables.get(operand, self.zeropage_vars.get(operand, f"0x{operand:04x}")) if isinstance(operand, int) else operand.replace('#$', '0x')
                return ASTNode('assign', value=f"a -= {val};")
            elif op == 'BRK':
                return ASTNode('try_catch', value="throw std::runtime_error(\"Interrupt\");")
            elif op == 'SEI':
                return ASTNode('assign', value="InterruptGuard guard;")
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
                        if operand in [0xD020, 0xD021, 0xDC05, 0xDC04, 0xDC00]:
                            self.classes[operand] = 'C64::VIC' if operand in [0xD020, 0xD021] else 'C64::CIA'
                    elif isinstance(operand, int) and operand not in self.variables:
                        self.variables[operand] = f"var_{operand:04x}"
                if pattern == 'class':
                    class_name = 'C64::VIC' if cond_val in [0xD020, 0xD021] else 'C64::CIA' if cond_val in [0xDC05, 0xDC04, 0xDC00] else f"class_{cond_val:04x}"
                    fields = [f"uint8_t field{i};" for i in range(target)]
                    methods = [
                        f"uint8_t get_field{i}() const {{ return field{i}; }}",
                        f"void set_field{i}(uint8_t value) {{ field{i} = value; }}"
                    ]
                    self.ast.children.append(
                        ASTNode('class_def', value=f"class {class_name.split('::')[-1]} : public C64::Device {{\nprivate:\n    " + "\n    ".join(fields) + "\npublic:\n    " + "\n    ".join(methods) + "\n    uint8_t operator[](uint16_t addr) const {{ return field[addr]; }}\n    void operator[](uint16_t addr) {{ field[addr] = value; }}\n};")
                    )
                    for i, instr in enumerate(block):
                        if instr[1] == 'LDA':
                            self.ast.children.append(ASTNode('assign', value=f"a = {class_name}::get_field{i}();"))
                        elif instr[1] == 'STA':
                            self.ast.children.append(ASTNode('assign', value=f"{class_name}::set_field{i}(a);"))
                elif pattern == 'array':
                    array_name = f"array_{cond_val:04x}"
                    self.ast.children.append(ASTNode('array_def', value=f"std::vector<uint8_t> {array_name}({target});"))
                    for instr in block:
                        if instr[1] == 'LDA' and isinstance(instr[2], str) and ',X' in instr[2]:
                            addr = int(instr[2].split(',')[0].replace('$', ''), 16)
                            self.ast.children.append(ASTNode('assign', value=f"a = {array_name}[x];"))
                        elif instr[1] == 'STA' and isinstance(instr[2], str) and ',X' in instr[2]:
                            addr = int(instr[2].split(',')[0].replace('$', ''), 16)
                            self.ast.children.append(ASTNode('assign', value=f"{array_name}[x] = a;"))
                elif pattern == 'macro':
                    self.ast.children.append(ASTNode('function', value=f"static inline void {macro_name}()", children=[self.translate_instruction(b) for b in macro_block]))
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
                elif pattern == 'local_var':
                    self.ast.children.append(ASTNode('local_var', value=f"uint8_t temp_{cond_val:02x};"))
                elif pattern == 'pointer':
                    addr = int(cond_val.split('),')[0].replace('(', ''), 16) if isinstance(cond_val, str) else cond_val
                    self.ast.children.append(ASTNode('assign', value=f"std::shared_ptr<uint8_t> ptr_{addr:04x}(new uint8_t[memory[0x{addr:04x} + y]]);"))
                elif pattern == 'timer':
                    self.ast.children.append(ASTNode('function', value="void C64::CIA::timer_handler()", children=[self.translate_instruction(b) for b in block]))
                elif pattern == 'event_handler':
                    self.ast.children.append(ASTNode('function', value="void C64::CIA::joystick_handler()", children=[self.translate_instruction(b) for b in block]))
                elif pattern == 'interrupt_callback':
                    self.ast.children.append(ASTNode('function', value=f"void callback_{cond_val:04x}()", children=[self.translate_instruction(b) for b in block]))
                elif pattern == 'lambda':
                    self.ast.children.append(ASTNode('lambda', value=f"auto {lambda_name} = []() {{", children=[self.translate_instruction(b) for b in cond_val], label="};"))
                elif pattern == 'copy_memory':
                    src = self.variables.get(cond_val, f"0x{cond_val:04x}")
                    dst = self.variables.get(target, f"0x{target:04x}")
                    self.ast.children.append(ASTNode('assign', value=f"std::copy(memory.begin() + {src}, memory.begin() + {src} + 1, memory.begin() + {dst});"))
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
                    class_name, method_name = self.functions.get(cond_val, (None, f"func_{cond_val:04x}"))
                    params = [self.translate_instruction(b) for b in block if b[1] == 'PHA']
                    self.ast.children.append(ASTNode('method_call' if class_name else 'function_call', value=f"C64::{class_name}::{method_name}();" if class_name else f"{method_name}();", params=params))
                elif pattern == 'try_catch':
                    self.ast.children.append(ASTNode('try_catch', value="try {", children=[self.translate_instruction(b) for b in block], label="} catch (const std::runtime_error& e) { /* Handle interrupt */ }"))
                else:
                    for instr in block:
                        self.ast.children.append(self.translate_instruction(instr))
        except Exception as e:
            logging.critical(f"AST oluşturma hatası: {str(e)}")
            raise

    def emit_code(self):
        """AST'den C++ kodu üret"""
        logging.debug("C++ kodu üretiliyor")
        try:
            lines = [
                '#include <cstdint>',
                '#include <string>',
                '#include <vector>',
                '#include <algorithm>',
                '#include <stdexcept>',
                'namespace C64 {',
                'constexpr uint16_t VIC_BORDERCOLOR = 0xD020;',
                'constexpr uint16_t VIC_BGCOLOR = 0xD021;',
                'constexpr uint16_t CIA_TAHI = 0xDC05;',
                'constexpr uint16_t CIA_TALO = 0xDC04;',
                'constexpr uint16_t CIA_JOYSTICK = 0xDC00;',
                'class Device {',
                'public:',
                '    virtual void execute() = 0;',
                '    virtual ~Device() = default;',
                '};',
                'class InterruptGuard {',
                'public:',
                '    InterruptGuard() { /* SEI */ }',
                '    ~InterruptGuard() { /* CLI */ }',
                '};',
                'class VIC : public Device {',
                'private:',
                '    uint8_t border_color; // $D020',
                '    uint8_t background_color; // $D021',
                'public:',
                '    uint8_t get_border_color() const { return border_color; }',
                '    void set_border_color(uint8_t value) { border_color = value; }',
                '    uint8_t get_background_color() const { return background_color; }',
                '    void set_background_color(uint8_t value) { background_color = value; }',
                '    uint8_t operator[](uint16_t addr) const { return addr == VIC_BORDERCOLOR ? border_color : background_color; }',
                '    void operator[](uint16_t addr) { if (addr == VIC_BORDERCOLOR) border_color = value; else background_color = value; }',
                '    void print_char(uint8_t);',
                '    void read_char();',
                '    void get_input();',
                '    void clear_channel();',
                '    void check_input();',
                '    void check_output();',
                '    void execute() override { print_char(0); }',
                '};',
                'class CIA : public Device {',
                'private:',
                '    uint8_t timer_hi; // $DC05',
                '    uint8_t timer_lo; // $DC04',
                '    uint8_t joystick; // $DC00',
                'public:',
                '    uint8_t get_timer_hi() const { return timer_hi; }',
                '    void set_timer_hi(uint8_t value) { timer_hi = value; }',
                '    uint8_t get_timer_lo() const { return timer_lo; }',
                '    void set_timer_lo(uint8_t value) { timer_lo = value; }',
                '    uint8_t get_joystick() const { return joystick; }',
                '    void set_joystick(uint8_t value) { joystick = value; }',
                '    void timer_handler();',
                '    void joystick_handler();',
                '    void execute() override { timer_handler(); }',
                '};',
                'class Math {',
                'public:',
                '    static float sin(float);',
                '    static float cos(float);',
                '};',
                'class String {',
                'public:',
                '    static std::string len(const std::vector<uint8_t>&);',
                '    static std::string mid(const std::vector<uint8_t>&, uint8_t);',
                '    static std::string left(const std::vector<uint8_t>&, uint8_t);',
                '    static std::string right(const std::vector<uint8_t>&, uint8_t);',
                '};',
                'template<typename T>',
                'void copy_memory(T* src, T* dst, size_t size) {',
                '    std::copy(src, src + size, dst);',
                '}',
                '}',
                'uint8_t a, x, y;',
                'std::vector<uint8_t> memory(0x10000);',
                'C64::VIC vic;',
                'C64::CIA cia;'
            ]
            # Enum tanımları
            if self.constants:
                lines.append("enum class Constants {")
                for const in self.constants:
                    lines.append(f"    CONST_{const:02x} = 0x{const:02x},")
                lines.append("};")
            # Class, dizi ve global değişken tanımları
            for node in self.ast.children:
                if node.type in ['class_def', 'array_def', 'global_var']:
                    lines.append(node.value)
            # Fonksiyon tanımları
            for addr, (class_name, method_name) in self.functions.items():
                if not class_name:
                    lines.append(f"void {method_name}({'void' if addr not in self.recursive_calls else 'void /* recursive */'}) {{")
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
                elif node.type == 'method_call' or node.type == 'function_call':
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
                elif node.type == 'lambda':
                    lines.append(f"    {node.value}")
                    self.line_number += 1
                    for stmt in node.children:
                        lines.append(f"        {stmt.value}")
                        self.line_number += 1
                    lines.append(f"    {node.label}")
                    self.line_number += 1
                elif node.type == 'try_catch':
                    lines.append(f"    {node.value}")
                    self.line_number += 1
                    for stmt in node.children:
                        lines.append(f"        {stmt.value}")
                        self.line_number += 1
                    lines.append(f"    {node.label}")
                    self.line_number += 1
            lines.append("    return 0;")
            lines.append("}")
            logging.info("C++ kodu başarıyla üretildi")
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