"""
Gelişmiş C64 PRG dosyası disassembler
- Basit opcode table (yeni, güvenli)
- py65 tabanlı (eski, güçlü ama riskli)
- Çoklu dil çevirisi destekli
- Memory map entegrasyonu
"""

import json
import os
from opcode_manager import OpcodeManager
from improved_disassembler import ImprovedDisassembler

class AdvancedDisassembler:
    def __init__(self, start_address, code, use_py65=False, use_illegal_opcodes=False, output_format='asm'):
        self.start_address = start_address
        self.code = code
        self.use_py65 = use_py65
        self.use_illegal_opcodes = use_illegal_opcodes
        self.output_format = output_format  # 'asm', 'c', 'qbasic', 'pseudo'
        self.opcode_manager = OpcodeManager()
        self.opcodes = self.opcode_manager.get_all_opcodes()
        self.translations = self.opcode_manager.get_all_translations()
        self.memory_map = self.load_memory_map()
        
        # py65 desteği
        if use_py65:
            try:
                from py65.devices.mpu6502 import MPU
                from py65.memory import ObservableMemory
                from py65.disassembler import Disassembler as PY65Disassembler
                self.mpu = MPU()
                self.memory = ObservableMemory()
                self.py65_disassembler = PY65Disassembler(self.mpu, self.memory)
                self.py65_available = True
                print("py65 disassembler yüklendi")
            except ImportError as e:
                self.py65_available = False
                print(f"py65 kütüphanesi yüklenemedi: {e}")
        else:
            self.py65_available = False
    
    def load_memory_map(self):
        """Memory map'i yükle"""
        memory_map = {}
        json_path = os.path.join(os.path.dirname(__file__), "memory_map.json")
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # String hex değerlerini int'e çevir
                for hex_str, description in data.items():
                    if hex_str.startswith('0x'):
                        address = int(hex_str, 16)
                        memory_map[address] = description
                        
                print(f"Memory map yüklendi: {len(memory_map)} adres")
                
            except Exception as e:
                print(f"Memory map yükleme hatası: {e}")
                
        return memory_map
    
    def get_memory_info(self, address):
        """Belirli bir adres için memory map bilgisi al"""
        if address in self.memory_map:
            return self.memory_map[address]
        return None
    
    def translate_instruction(self, opcode_name, operand_value=None, operand_2=None):
        """Instruction'ı belirtilen formata çevir"""
        if self.output_format == 'asm':
            return None  # Assembly format için çeviri yok
        
        # Çeviri tablosunda varsa kullan
        if opcode_name in self.translations:
            # Format'a göre doğru key'i kullan
            if self.output_format == 'c':
                translation_key = 'c_equivalent'
            elif self.output_format == 'qbasic':
                translation_key = 'qbasic_equivalent'
            elif self.output_format == 'pdsx':
                translation_key = 'pdsx_equivalent'
            elif self.output_format == 'pseudo':
                translation_key = 'pseudo_equivalent'
            elif self.output_format == 'commodorebasicv2':
                translation_key = 'commodorebasicv2_equivalent'
            else:
                translation_key = f"{self.output_format}_equivalent"
            
            translation = self.translations[opcode_name].get(translation_key, None)
            
            if translation:
                # Operand değerlerini yerine koy
                if operand_value is not None:
                    # Önce büyük harflerle dene
                    if 'ADDRESS' in translation:
                        translation = translation.replace('ADDRESS', str(operand_value))
                    elif 'ADDR' in translation:
                        translation = translation.replace('ADDR', str(operand_value))
                    elif 'address' in translation:
                        translation = translation.replace('address', str(operand_value))
                    elif 'addr' in translation:
                        translation = translation.replace('addr', str(operand_value))
                    elif 'VALUE' in translation:
                        translation = translation.replace('VALUE', str(operand_value))
                    elif 'value' in translation:
                        translation = translation.replace('value', str(operand_value))
                    elif 'label' in translation:
                        translation = translation.replace('label', f"label_{operand_value:04X}")
                    elif 'LABEL' in translation:
                        translation = translation.replace('LABEL', f"label_{operand_value:04X}")
                
                return translation
        
        # Fallback: Bilinmeyen opcode'lar için basit çeviri
        if self.output_format == 'c':
            if operand_value is not None:
                return f"/* {opcode_name} {operand_value} */"
            else:
                return f"/* {opcode_name} */"
        elif self.output_format in ['qbasic', 'pdsx', 'commodorebasicv2']:
            if operand_value is not None:
                return f"REM {opcode_name} {operand_value}"
            else:
                return f"REM {opcode_name}"
        else:
            if operand_value is not None:
                return f"// {opcode_name} {operand_value}"
            else:
                return f"// {opcode_name}"

    def disassemble_simple(self, prg_data):
        """Basit disassemble metodu - dış kullanım için"""
        if not prg_data or len(prg_data) < 2:
            return "Hata: Geçersiz PRG verisi"
        
        # Eğer format assembly değilse, yeni improved disassembler kullan
        if self.output_format != 'asm':
            improved_disasm = ImprovedDisassembler(self.start_address, self.code, self.output_format)
            return improved_disasm.disassemble_to_format(prg_data)
        
        # Assembly format için eski metod
        # PRG dosyasının başlangıç adresini al
        start_addr = prg_data[0] + (prg_data[1] << 8)
        code_data = prg_data[2:]
        
        # Geçici olarak parametreleri güncelle
        old_start = self.start_address
        old_code = self.code
        
        self.start_address = start_addr
        self.code = code_data
        
        result = self._disassemble_simple()
        
        # Eski parametreleri geri yükle
        self.start_address = old_start
        self.code = old_code
        
        return '\n'.join(result)
        
    def disassemble_py65(self, prg_data):
        """py65 disassemble metodu - dış kullanım için"""
        if not prg_data or len(prg_data) < 2:
            return "Hata: Geçersiz PRG verisi"
            
        # PRG dosyasının başlangıç adresini al
        start_addr = prg_data[0] + (prg_data[1] << 8)
        code_data = prg_data[2:]
        
        # Geçici olarak parametreleri güncelle
        old_start = self.start_address
        old_code = self.code
        
        self.start_address = start_addr
        self.code = code_data
        
        result = self._disassemble_py65()
        
        # Eski parametreleri geri yükle
        self.start_address = old_start
        self.code = old_code
        
        return '\n'.join(result)

    def disassemble(self):
        """Disassembler metodu - seçilen yazım tarzına göre çıktı üretir"""
        if self.output_format == 'tass':
            return self._disassemble_tass()
        elif self.output_format == 'kickassembler':
            return self._disassemble_kickassembler()
        elif self.output_format == 'cc64':
            return self._disassemble_cc64()
        else:
            raise ValueError(f"Desteklenmeyen çıktı formatı: {self.output_format}")

    def _disassemble_tass(self):
        """TASS yazım tarzı için disassembler"""
        lines = []
        pc = self.start_address
        while pc < self.start_address + len(self.code):
            opcode = self.code[pc - self.start_address]
            if opcode in self.opcodes:
                template, length, mnemonic = self.opcodes[opcode]
                if length == 1:
                    lines.append(f"{mnemonic}")
                elif length == 2:
                    operand = self.code[pc - self.start_address + 1]
                    lines.append(f"{mnemonic} ${operand:02X}")
                elif length == 3:
                    operand_lo = self.code[pc - self.start_address + 1]
                    operand_hi = self.code[pc - self.start_address + 2]
                    operand = operand_lo + (operand_hi << 8)
                    lines.append(f"{mnemonic} ${operand:04X}")
                pc += length
            else:
                lines.append(f".BYTE ${opcode:02X}")
                pc += 1
        return lines

    def _disassemble_kickassembler(self):
        """KickAssembler yazım tarzı için disassembler"""
        lines = []
        pc = self.start_address
        while pc < self.start_address + len(self.code):
            opcode = self.code[pc - self.start_address]
            if opcode in self.opcodes:
                template, length, mnemonic = self.opcodes[opcode]
                if length == 1:
                    lines.append(f"{mnemonic}")
                elif length == 2:
                    operand = self.code[pc - self.start_address + 1]
                    lines.append(f"{mnemonic} #{operand:02X}")
                elif length == 3:
                    operand_lo = self.code[pc - self.start_address + 1]
                    operand_hi = self.code[pc - self.start_address + 2]
                    operand = operand_lo + (operand_hi << 8)
                    lines.append(f"{mnemonic} #{operand:04X}")
                pc += length
            else:
                lines.append(f".BYTE #{opcode:02X}")
                pc += 1
        return lines

    def _disassemble_cc64(self):
        """CC64 yazım tarzı için disassembler"""
        lines = []
        pc = self.start_address
        while pc < self.start_address + len(self.code):
            opcode = self.code[pc - self.start_address]
            if opcode in self.opcodes:
                template, length, mnemonic = self.opcodes[opcode]
                if length == 1:
                    lines.append(f"{mnemonic}")
                elif length == 2:
                    operand = self.code[pc - self.start_address + 1]
                    lines.append(f"{mnemonic} {operand:02X}h")
                elif length == 3:
                    operand_lo = self.code[pc - self.start_address + 1]
                    operand_hi = self.code[pc - self.start_address + 2]
                    operand = operand_lo + (operand_hi << 8)
                    lines.append(f"{mnemonic} {operand:04X}h")
                pc += length
            else:
                lines.append(f".BYTE {opcode:02X}h")
                pc += 1
        return lines
    
    def _disassemble_simple(self):
        """Basit opcode table ile disassemble"""
        if not self.code:
            return ["Hata: Kod verisi yok"]
        
        lines = []
        pc = self.start_address
        end_address = self.start_address + len(self.code)
        
        while pc < end_address:
            try:
                if pc - self.start_address >= len(self.code):
                    break
                    
                opcode = self.code[pc - self.start_address]
                
                if opcode in self.opcodes:
                    template, length, opcode_name = self.opcodes[opcode]
                    operand_value = None
                    
                    if length == 1:
                        disasm_text = template
                    elif length == 2:
                        if pc - self.start_address + 1 < len(self.code):
                            operand = self.code[pc - self.start_address + 1]
                            operand_value = operand
                            disasm_text = template % operand
                            
                            # Memory map kontrolü (sadece assembly için)
                            if self.output_format == 'asm':
                                memory_info = self.get_memory_info(operand)
                                if memory_info:
                                    disasm_text += f" ; {memory_info}"
                        else:
                            disasm_text = f".BYTE ${opcode:02X}"
                    elif length == 3:
                        if pc - self.start_address + 2 < len(self.code):
                            operand_lo = self.code[pc - self.start_address + 1]
                            operand_hi = self.code[pc - self.start_address + 2]
                            operand = operand_lo + (operand_hi << 8)
                            operand_value = operand
                            disasm_text = template % operand
                            
                            # Memory map kontrolü (sadece assembly için)
                            if self.output_format == 'asm':
                                memory_info = self.get_memory_info(operand)
                                if memory_info:
                                    disasm_text += f" ; {memory_info}"
                        else:
                            disasm_text = f".BYTE ${opcode:02X}"
                    
                    # Format'a göre çeviri yap
                    if self.output_format != 'asm':
                        translation = self.translate_instruction(opcode_name, operand_value)
                        if translation:
                            # Çeviri ana kod olsun, assembly yorum olsun
                            if self.output_format == 'c':
                                disasm_text = f"{translation}  /* {disasm_text} */"
                            elif self.output_format == 'qbasic':
                                disasm_text = f"{translation}  REM {disasm_text}"
                            elif self.output_format == 'pdsx':
                                disasm_text = f"{translation}  REM {disasm_text}"
                            elif self.output_format == 'commodorebasicv2':
                                disasm_text = f"{translation}  REM {disasm_text}"
                            elif self.output_format == 'pseudo':
                                disasm_text = f"{translation}  // {disasm_text}"
                            else:
                                disasm_text = f"{translation}  /* {disasm_text} */"
                        
                        lines.append(f"{disasm_text}")
                    else:
                        # Assembly format için address ile beraber
                        lines.append(f"${pc:04X}: {disasm_text}")
                    
                    pc += length
                else:
                    # Bilinmeyen opcode - sabit çeviri
                    if self.output_format == 'asm':
                        lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
                    else:
                        # Bilinmeyen opcode'lar için format'a göre sabit çeviri
                        if self.output_format == 'c':
                            lines.append(f"/* Unknown opcode: 0x{opcode:02X} */")
                        elif self.output_format == 'qbasic':
                            lines.append(f"REM Unknown opcode: 0x{opcode:02X}")
                        elif self.output_format == 'pdsx':
                            lines.append(f"REM Unknown opcode: 0x{opcode:02X}")
                        elif self.output_format == 'commodorebasicv2':
                            lines.append(f"REM Unknown opcode: 0x{opcode:02X}")
                        elif self.output_format == 'pseudo':
                            lines.append(f"// Unknown opcode: 0x{opcode:02X}")
                        else:
                            lines.append(f"/* Unknown opcode: 0x{opcode:02X} */")
                    pc += 1
                    
            except Exception as e:
                lines.append(f"${pc:04X}: HATA - {e}")
                pc += 1
        
        return lines
    
    def _disassemble_py65(self):
        """py65 ile disassemble (eski method)"""
        try:
            # Memory'ye kodu yükle
            self.memory[self.start_address:self.start_address + len(self.code)] = self.code
            
            lines = []
            pc = self.start_address
            end_address = self.start_address + len(self.code)
            
            while pc < end_address:
                try:
                    # py65 disassembler kullan
                    length, disasm_text = self.py65_disassembler.instruction_at(pc)
                    lines.append(f"${pc:04X}: {disasm_text}")
                    pc += length
                    
                except Exception as e:
                    # Fallback: Basit disassemble
                    opcode = self.memory[pc]
                    if opcode in self.opcodes:
                        length = self.opcodes[opcode][1]
                        lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
                    else:
                        lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
                        length = 1
                    pc += length
                    
            return lines
            
        except Exception as e:
            return [f"py65 Hatası: {e}"]
    
    def _get_instruction_length(self, opcode):
        """Instruction uzunluğunu hesapla"""
        if opcode in self.opcodes:
            return self.opcodes[opcode][1]
        return 1
    
    def convert_to_language(self, asm_lines, target_language):
        """Assembly'yi başka dillere çevir"""
        if not asm_lines:
            return []
        
        converted = []
        
        for line in asm_lines:
            try:
                # Assembly satırını parse et
                if ':' in line:
                    addr_part, inst_part = line.split(':', 1)
                    addr = addr_part.strip()
                    instruction = inst_part.strip()
                    
                    # Opcode'u çıkar
                    opcode_name = instruction.split()[0] if instruction else ""
                    
                    # Çeviri yap
                    translation = self.opcode_manager.get_translation(opcode_name, target_language)
                    converted.append(f"{addr}: {translation}")
                else:
                    converted.append(f"// {line}")
                    
            except Exception as e:
                converted.append(f"// Çeviri hatası: {line}")
        
        return converted
    
    def to_c(self, asm_lines):
        """C diline çevir"""
        return self.convert_to_language(asm_lines, "c")
    
    def to_qbasic(self, asm_lines):
        """QBasic'e çevir"""
        return self.convert_to_language(asm_lines, "qbasic")
    
    def to_pdsx(self, asm_lines):
        """PDSX'e çevir"""
        return self.convert_to_language(asm_lines, "pdsx")
    
    def to_commodore_basic_v2(self, asm_lines):
        """Commodore BASIC V2'ye çevir"""
        return self.convert_to_language(asm_lines, "commodorebasicv2")
    
    def to_pseudo(self, asm_lines):
        """Pseudo-code'a çevir"""
        return self.convert_to_language(asm_lines, "pseudo")

# Geriye uyumluluk için eski API
class Disassembler:
    def __init__(self, start_address, code):
        self.advanced = AdvancedDisassembler(start_address, code, use_py65=False)
    
    def disassemble(self):
        return self.advanced.disassemble()

# py65 destekli versiyon
class PY65Disassembler:
    def __init__(self, start_address, code):
        self.advanced = AdvancedDisassembler(start_address, code, use_py65=True)
    
    def disassemble(self):
        return self.advanced.disassemble()

if __name__ == "__main__":
    # Test
    test_code = [0xA9, 0x00, 0x85, 0x02, 0x60]  # LDA #$00, STA $02, RTS
    
    print("=== Basit Disassembler ===")
    disasm = Disassembler(0xC000, test_code)
    for line in disasm.disassemble():
        print(line)
    
    print("\n=== Gelişmiş Disassembler ===")
    advanced = AdvancedDisassembler(0xC000, test_code)
    asm_lines = advanced.disassemble()
    for line in asm_lines:
        print(line)
    
    print("\n=== C Çevirisi ===")
    c_lines = advanced.to_c(asm_lines)
    for line in c_lines:
        print(line)
    
    print("\n=== QBasic Çevirisi ===")
    qbasic_lines = advanced.to_qbasic(asm_lines)
    for line in qbasic_lines:
        print(line)
