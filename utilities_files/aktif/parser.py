# parser.py
import json
import re
import logging
from pdsXv12_minimal import StructInstance, UnionInstance, Pointer, pdsXv12Final

# Logging yapılandırması
logging.basicConfig(filename='logs/d64_converter.log', level=logging.ERROR)

# C64 Hafıza Haritası
MEMORY_MAP = {
    0x0400: "screen_mem",
    0xD800: "color_ram",
    0xA000: "basic_rom",
    0xE000: "kernal_rom",
    0xD000: "io_area",
    0xC000: "ram_area",
    0x0288: "cursor_pos",
    0xD012: "raster_line",
    0xD020: "border_color",
    0xD021: "background_color",
    0xD400: "sid_voice1_freq",
    0xD401: "sid_voice1_control",
    0xD418: "sid_volume",
    0xC100: "basic_input_buffer",
    0xFFFE: "irq_vector",
    0xFFD2: "chrout",
    0xFFCF: "getin",
    0xD800: "sprite_data"
}

# pdsXv12u Tip Tablosu
TYPE_TABLE = {
    "INTEGER": int,
    "DOUBLE": float,
    "STRING": str,
    "BYTE": int,
    "SHORT": int,
    "LONG": int,
    "SINGLE": float,
    "LIST": list,
    "ARRAY": list,
    "DICT": dict
}

class CodeEmitter:
    def __init__(self, output_type="pdsx", use_illegal_opcodes=False):
        self.output_type = output_type
        self.use_illegal_opcodes = use_illegal_opcodes
        self.lines = []
        self.labels = {}
        self.label_counter = 0
        self.loop_stack = []
        self.switch_cases = []
        self.data_table = []
        self.memory_pool = {}
        self.type_table = TYPE_TABLE
        self.interpreter = pdsXv12Final() if pdsXv12Final else None
        self.event_counter = 0
        self.pipe_counter = 0
        self.instruction_map = load_instruction_map()

    def get_label(self, address):
        address = int(address)
        if address in MEMORY_MAP:
            return MEMORY_MAP[address]
        if address not in self.labels:
            self.labels[address] = f"label_{self.label_counter}"
            self.label_counter += 1
        return self.labels[address]

    def emit_opcode(self, opcode, operand, address, asm_lines, index):
        """Verilen opcode'u hedef dile çevirir."""
        if opcode in self.instruction_map:
            rule = self.instruction_map[opcode]
            # Bu kısım, opcode_map.json'daki kurallara göre doldurulacak
            # Örnek:
            if self.output_type == "pdsx":
                line = rule.get("pdsx_equivalent", f"REM {opcode} {operand}")
                self.lines.append(line)
            elif self.output_type == "qbasic":
                line = rule.get("qbasic_equivalent", f"' {opcode} {operand}")
                self.lines.append(line)
            elif self.output_type == "c":
                line = rule.get("c_equivalent", f"// {opcode} {operand}")
                self.lines.append(line)
            else: # pseudo
                line = rule.get("pseudo_equivalent", f"; {opcode} {operand}")
                self.lines.append(line)
        else:
            self.lines.append(f"; bilinmeyen opcode: {opcode} {operand}")

    def get_output(self):
        """Oluşturulan kod çıktısını döndürür."""
        return "\n".join(self.lines)

    def detect_loop(self, opcode, operand, address):
        if opcode in ["BEQ", "BNE", "BCS", "BCC", "BMI", "BPL", "BVS", "BVC"]:
            try:
                target_addr = int(operand[1:], 16)
                if target_addr < address:
                    self.loop_stack.append((target_addr, address))
                    return f"loop_{len(self.loop_stack)}"
            except ValueError:
                pass
        return None

    def detect_switch(self, opcode, operand, address, asm_lines, index):
        if opcode == "CMP" and index + 1 < len(asm_lines):
            next_line = asm_lines[index + 1]
            next_parsed = parse_line(next_line)
            if next_parsed and next_parsed[0] in ["BEQ", "BNE"]:
                value = operand[2:] if operand.startswith("#$") else operand
                target_addr = next_parsed[1][1:] if next_parsed[1].startswith("$") else next_parsed[1]
                self.switch_cases.append((value, self.get_label(int(target_addr, 16))))
                return True
        return False

    def detect_data(self, asm_lines, index):
        if index + 1 < len(asm_lines):
            line = asm_lines[index]
            parsed = parse_line(line)
            if parsed and parsed[0] == "DCB":
                values = parsed[1].split(",")
                self.data_table.append((parsed[2], values))
                return True
        return False

    def detect_event(self, opcode, operand, address):
        if opcode == "JSR" and operand == "$FFFE":
            event_id = f"event_{self.event_counter}"
            self.event_counter += 1
            return event_id
        return None

    def emit_assign(self, register, value, mode):
        try:
            if mode == "immediate":
                value = int(value[2:], 16) if value.startswith("#$") else value
                if self.output_type == "pdsx":
                    self.lines.append(f"LET {register} = {value}")
                elif self.output_type == "qbasic":
                    self.lines.append(f"{register} = {value}")
                elif self.output_type == "c":
                    self.lines.append(f"{register} = {value};")
                else:
                    self.lines.append(f"{register} = {value}")
            elif mode == "absolute":
                var_name = self.get_label(int(value[1:], 16))
                if self.output_type == "pdsx":
                    self.lines.append(f"LET {register} = PEEK({var_name})")
                elif self.output_type == "qbasic":
                    self.lines.append(f"{register} = mem({var_name})")
                elif self.output_type == "c":
                    self.lines.append(f"{register} = {var_name};")
                else:
                    self.lines.append(f"{register} = mem[{var_name}]")
            elif mode == "indexed":
                base, offset = value.split(",")
                base_addr = int(base[1:], 16)
                offset_reg = offset.strip()
                var_name = self.get_label(base_addr)
                if self.output_type == "pdsx":
                    self.lines.append(f"LET {register} = PEEK({var_name} + {offset_reg})")
                elif self.output_type == "qbasic":
                    self.lines.append(f"{register} = mem({var_name} + {offset_reg})")
                elif self.output_type == "c":
                    self.lines.append(f"{register} = {var_name}[{offset_reg}];")
                else:
                    self.lines.append(f"{register} = mem[{var_name} + {offset_reg}]")
        except Exception as e:
            logging.error(f"Assign emit hatası: {e}")

    def emit_store(self, register, addr):
        try:
            if "," in addr:
                base, offset = addr.split(",")
                base_addr = int(base[1:], 16)
                offset_reg = offset.strip()
                var_name = self.get_label(base_addr)
                if self.output_type == "pdsx":
                    self.lines.append(f"POKE {var_name} + {offset_reg}, {register}")
                elif self.output_type == "qbasic":
                    self.lines.append(f"mem({var_name} + {offset_reg}) = {register}")
                elif self.output_type == "c":
                    self.lines.append(f"{var_name}[{offset_reg}] = {register};")
                else:
                    self.lines.append(f"mem[{var_name} + {offset_reg}] = {register}")
            else:
                var_name = self.get_label(int(addr[1:], 16))
                if self.output_type == "pdsx":
                    self.lines.append(f"POKE {var_name}, {register}")
                elif self.output_type == "qbasic":
                    self.lines.append(f"mem({var_name}) = {register}")
                elif self.output_type == "c":
                    self.lines.append(f"{var_name} = {register};")
                else:
                    self.lines.append(f"mem[{var_name}] = {register}")
        except Exception as e:
            logging.error(f"Store emit hatası: {e}")

    def emit_jump(self, label, condition=None):
        try:
            label_name = self.get_label(int(label[1:], 16))
            if self.output_type == "pdsx":
                if condition:
                    self.lines.append(f"IF {condition} THEN GOTO {label_name}")
                else:
                    self.lines.append(f"GOTO {label_name}")
            elif self.output_type == "qbasic":
                if condition:
                    self.lines.append(f"IF {condition} THEN GOTO {label_name}")
                else:
                    self.lines.append(f"GOTO {label_name}")
            elif self.output_type == "c":
                if condition:
                    self.lines.append(f"if ({condition}) goto {label_name};")
                else:
                    self.lines.append(f"goto {label_name};")
            else:
                if condition:
                    self.lines.append(f"if {condition} goto {label_name}")
                else:
                    self.lines.append(f"goto {label_name}")
        except Exception as e:
            logging.error(f"Jump emit hatası: {e}")

    def emit_switch(self, register):
        if self.switch_cases:
            if self.output_type == "pdsx":
                self.lines.append(f"SELECT CASE {register}")
                for value, label in self.switch_cases:
                    self.lines.append(f"CASE {value} GOTO {label}")
                self.lines.append("END SELECT")
            elif self.output_type == "qbasic":
                self.lines.append(f"SELECT CASE {register}")
                for value, label in self.switch_cases:
                    self.lines.append(f"CASE {value}: GOTO {label}")
                self.lines.append("END SELECT")
            elif self.output_type == "c":
                self.lines.append(f"switch ({register}) {{")
                for value, label in self.switch_cases:
                    self.lines.append(f"    case {value}: goto {label};")
                self.lines.append("}")
            else:
                self.lines.append(f"switch {register}:")
                for value, label in self.switch_cases:
                    self.lines.append(f"    case {value}: goto {label}")
            self.switch_cases = []

    def emit_data(self, address, values):
        if self.output_type == "pdsx":
            self.lines.append(f"DATA {', '.join(values)}")
        elif self.output_type == "qbasic":
            self.lines.append(f"DATA {', '.join(values)}")
        elif self.output_type == "c":
            self.lines.append(f"unsigned char data_{address:04X}[] = {{{', '.join(values)}}};")
        else:
            self.lines.append(f"data at {address:04X}: {', '.join(values)}")

    def emit_event(self, event_id, trigger, action):
        if self.output_type == "pdsx":
            self.lines.append(f"EVENT {event_id} TRIGGER {trigger}")
            self.lines.append(f"    {action}")
            self.lines.append("END EVENT")
        elif self.output_type == "qbasic":
            self.lines.append(f"SUB {event_id}")
            self.lines.append(f"    IF {trigger} THEN {action}")
            self.lines.append("END SUB")
        elif self.output_type == "c":
            self.lines.append(f"void {event_id}() {{")
            self.lines.append(f"    if ({trigger}) {{ {action}; }}")
            self.lines.append("}")
        else:
            pass # Pseudo-kod için özel bir şey yapmaya gerek yok

def parse_line(line):
    """Bir assembly satırını opcode, operand ve adrese ayırır."""
    match = re.match(r"\$([0-9A-Fa-f]+):\s+([A-Z]{3})\s*(.*)", line)
    if match:
        address = int(match.group(1), 16)
        opcode = match.group(2)
        operand = match.group(3).strip()
        return opcode, operand, address
    return None

def load_instruction_map():
    """opcode_map.json dosyasını yükler."""
    try:
        with open("opcode_map.json", "r") as f:
            # JSON içeriğini okurken yorumları yoksay
            content = "".join(line for line in f if not line.strip().startswith("//"))
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"opcode_map.json yüklenemedi: {e}")
        return {}
