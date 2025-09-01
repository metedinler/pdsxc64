# disassembler.py
from py65.disassembler import Disassembler
from py65.memory import ObservableMemory
from py65.devices.mpu6502 import MPU
import logging
import sys
import os
from d64.d64_image import D64Image

# Logging yapılandırması
logging.basicConfig(filename='logs/d64_converter.log', level=logging.ERROR)

class PRGDisassembler:
    def __init__(self, prg_bytes=None, use_illegal_opcodes=False):
        self.use_illegal_opcodes = use_illegal_opcodes
        if prg_bytes is not None:
            self.prg_bytes = prg_bytes
            self.start_address = prg_bytes[0] | (prg_bytes[1] << 8)
            self.code = prg_bytes[2:]
            self.memory = bytearray(65536)
            self.mpu = MPU()
            self._prepare_memory()
        else:
            # Default initialization for GUI
            self.prg_bytes = None
            self.start_address = 0
            self.code = b''
            self.memory = bytearray(65536)
            self.mpu = MPU()

    def _prepare_memory(self):
        if self.code:
            end_address = self.start_address + len(self.code)
            self.memory[self.start_address:end_address] = self.code

    def disassemble(self):
        """PRG dosyasını disassamble et - Basit opcode lookup ile"""
        if not self.code:
            return ["Hata: Kod verisi yok"]
        
        # Basit 6502 opcode table
        opcodes = {
            0x00: ("BRK", 1), 0x01: ("ORA ($%02X,X)", 2), 0x05: ("ORA $%02X", 2), 0x06: ("ASL $%02X", 2),
            0x08: ("PHP", 1), 0x09: ("ORA #$%02X", 2), 0x0A: ("ASL A", 1), 0x0D: ("ORA $%04X", 3),
            0x0E: ("ASL $%04X", 3), 0x10: ("BPL $%02X", 2), 0x11: ("ORA ($%02X),Y", 2), 0x15: ("ORA $%02X,X", 2),
            0x16: ("ASL $%02X,X", 2), 0x18: ("CLC", 1), 0x19: ("ORA $%04X,Y", 3), 0x1D: ("ORA $%04X,X", 3),
            0x1E: ("ASL $%04X,X", 3), 0x20: ("JSR $%04X", 3), 0x21: ("AND ($%02X,X)", 2), 0x24: ("BIT $%02X", 2),
            0x25: ("AND $%02X", 2), 0x26: ("ROL $%02X", 2), 0x28: ("PLP", 1), 0x29: ("AND #$%02X", 2),
            0x2A: ("ROL A", 1), 0x2C: ("BIT $%04X", 3), 0x2D: ("AND $%04X", 3), 0x2E: ("ROL $%04X", 3),
            0x30: ("BMI $%02X", 2), 0x31: ("AND ($%02X),Y", 2), 0x35: ("AND $%02X,X", 2), 0x36: ("ROL $%02X,X", 2),
            0x38: ("SEC", 1), 0x39: ("AND $%04X,Y", 3), 0x3D: ("AND $%04X,X", 3), 0x3E: ("ROL $%04X,X", 3),
            0x40: ("RTI", 1), 0x41: ("EOR ($%02X,X)", 2), 0x45: ("EOR $%02X", 2), 0x46: ("LSR $%02X", 2),
            0x48: ("PHA", 1), 0x49: ("EOR #$%02X", 2), 0x4A: ("LSR A", 1), 0x4C: ("JMP $%04X", 3),
            0x4D: ("EOR $%04X", 3), 0x4E: ("LSR $%04X", 3), 0x50: ("BVC $%02X", 2), 0x51: ("EOR ($%02X),Y", 2),
            0x55: ("EOR $%02X,X", 2), 0x56: ("LSR $%02X,X", 2), 0x58: ("CLI", 1), 0x59: ("EOR $%04X,Y", 3),
            0x5D: ("EOR $%04X,X", 3), 0x5E: ("LSR $%04X,X", 3), 0x60: ("RTS", 1), 0x61: ("ADC ($%02X,X)", 2),
            0x65: ("ADC $%02X", 2), 0x66: ("ROR $%02X", 2), 0x68: ("PLA", 1), 0x69: ("ADC #$%02X", 2),
            0x6A: ("ROR A", 1), 0x6C: ("JMP ($%04X)", 3), 0x6D: ("ADC $%04X", 3), 0x6E: ("ROR $%04X", 3),
            0x70: ("BVS $%02X", 2), 0x71: ("ADC ($%02X),Y", 2), 0x75: ("ADC $%02X,X", 2), 0x76: ("ROR $%02X,X", 2),
            0x78: ("SEI", 1), 0x79: ("ADC $%04X,Y", 3), 0x7D: ("ADC $%04X,X", 3), 0x7E: ("ROR $%04X,X", 3),
            0x81: ("STA ($%02X,X)", 2), 0x84: ("STY $%02X", 2), 0x85: ("STA $%02X", 2), 0x86: ("STX $%02X", 2),
            0x88: ("DEY", 1), 0x8A: ("TXA", 1), 0x8C: ("STY $%04X", 3), 0x8D: ("STA $%04X", 3),
            0x8E: ("STX $%04X", 3), 0x90: ("BCC $%02X", 2), 0x91: ("STA ($%02X),Y", 2), 0x94: ("STY $%02X,X", 2),
            0x95: ("STA $%02X,X", 2), 0x96: ("STX $%02X,Y", 2), 0x98: ("TYA", 1), 0x99: ("STA $%04X,Y", 3),
            0x9A: ("TXS", 1), 0x9D: ("STA $%04X,X", 3), 0xA0: ("LDY #$%02X", 2), 0xA1: ("LDA ($%02X,X)", 2),
            0xA2: ("LDX #$%02X", 2), 0xA4: ("LDY $%02X", 2), 0xA5: ("LDA $%02X", 2), 0xA6: ("LDX $%02X", 2),
            0xA8: ("TAY", 1), 0xA9: ("LDA #$%02X", 2), 0xAA: ("TAX", 1), 0xAC: ("LDY $%04X", 3),
            0xAD: ("LDA $%04X", 3), 0xAE: ("LDX $%04X", 3), 0xB0: ("BCS $%02X", 2), 0xB1: ("LDA ($%02X),Y", 2),
            0xB4: ("LDY $%02X,X", 2), 0xB5: ("LDA $%02X,X", 2), 0xB6: ("LDX $%02X,Y", 2), 0xB8: ("CLV", 1),
            0xB9: ("LDA $%04X,Y", 3), 0xBA: ("TSX", 1), 0xBC: ("LDY $%04X,X", 3), 0xBD: ("LDA $%04X,X", 3),
            0xBE: ("LDX $%04X,Y", 3), 0xC0: ("CPY #$%02X", 2), 0xC1: ("CMP ($%02X,X)", 2), 0xC4: ("CPY $%02X", 2),
            0xC5: ("CMP $%02X", 2), 0xC6: ("DEC $%02X", 2), 0xC8: ("INY", 1), 0xC9: ("CMP #$%02X", 2),
            0xCA: ("DEX", 1), 0xCC: ("CPY $%04X", 3), 0xCD: ("CMP $%04X", 3), 0xCE: ("DEC $%04X", 3),
            0xD0: ("BNE $%02X", 2), 0xD1: ("CMP ($%02X),Y", 2), 0xD5: ("CMP $%02X,X", 2), 0xD6: ("DEC $%02X,X", 2),
            0xD8: ("CLD", 1), 0xD9: ("CMP $%04X,Y", 3), 0xDD: ("CMP $%04X,X", 3), 0xDE: ("DEC $%04X,X", 3),
            0xE0: ("CPX #$%02X", 2), 0xE1: ("SBC ($%02X,X)", 2), 0xE4: ("CPX $%02X", 2), 0xE5: ("SBC $%02X", 2),
            0xE6: ("INC $%02X", 2), 0xE8: ("INX", 1), 0xE9: ("SBC #$%02X", 2), 0xEA: ("NOP", 1),
            0xEC: ("CPX $%04X", 3), 0xED: ("SBC $%04X", 3), 0xEE: ("INC $%04X", 3), 0xF0: ("BEQ $%02X", 2),
            0xF1: ("SBC ($%02X),Y", 2), 0xF5: ("SBC $%02X,X", 2), 0xF6: ("INC $%02X,X", 2), 0xF8: ("SED", 1),
            0xF9: ("SBC $%04X,Y", 3), 0xFD: ("SBC $%04X,X", 3), 0xFE: ("INC $%04X,X", 3)
        }
        
        lines = []
        pc = self.start_address
        end_address = self.start_address + len(self.code)
        
        while pc < end_address:
            try:
                if pc - self.start_address >= len(self.code):
                    break
                    
                opcode = self.code[pc - self.start_address]
                
                if opcode in opcodes:
                    template, length = opcodes[opcode]
                    
                    if length == 1:
                        disasm_text = template
                    elif length == 2:
                        if pc - self.start_address + 1 < len(self.code):
                            operand = self.code[pc - self.start_address + 1]
                            disasm_text = template % operand
                        else:
                            disasm_text = f".BYTE ${opcode:02X}"
                    elif length == 3:
                        if pc - self.start_address + 2 < len(self.code):
                            operand_lo = self.code[pc - self.start_address + 1]
                            operand_hi = self.code[pc - self.start_address + 2]
                            operand = operand_lo + (operand_hi << 8)
                            disasm_text = template % operand
                        else:
                            disasm_text = f".BYTE ${opcode:02X}"
                    
                    lines.append(f"${pc:04X}: {disasm_text}")
                    pc += length
                else:
                    # Bilinmeyen opcode
                    lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
                    pc += 1
                    
            except Exception as e:
                lines.append(f"${pc:04X}: HATA - {e}")
                pc += 1
        
        return lines

    def disassemble_prg(self, prg_bytes):
        """PRG bytes'ını alıp disassemble et - Uyumluluk için"""
        if prg_bytes is None or len(prg_bytes) < 2:
            return ["Hata: Geçersiz PRG verisi"]
            
        self.prg_bytes = prg_bytes
        self.start_address = prg_bytes[0] | (prg_bytes[1] << 8)
        self.code = prg_bytes[2:]
        self.memory = bytearray(65536)
        self._prepare_memory()
        
        return self.disassemble()

def main():
    # Örnek kullanım
    prg_data = bytes.fromhex("00 00 20 00 4C 00 00")
    disassembler = PRGDisassembler(prg_data)
    assembly = disassembler.disassemble()
    for line in assembly:
        print(line)

if __name__ == "__main__":
    main()