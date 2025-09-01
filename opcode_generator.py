"""
JSON dosyalarından tam 6502 opcode tablosu oluşturucu
"""

import json
import os

def load_opcode_data():
    """JSON dosyalarından opcode verilerini yükle"""
    opcodes_data = {}
    
    # opcode.json dosyasını yükle
    json_path = os.path.join(os.path.dirname(__file__), "help", "opcode.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            opcode_list = json.load(f)
            
        for opcode_info in opcode_list:
            opcode_name = opcode_info["opcode"]
            opcodes_data[opcode_name] = opcode_info
    
    return opcodes_data

def create_full_opcode_table():
    """Tam 256 opcode tablosu oluştur"""
    # Tam 6502 opcode tablosu - her hex değer için
    full_table = {}
    
    # Temel opcodes
    opcodes = {
        # ADC - Add with Carry
        0x69: ("ADC #$%02X", 2), 0x65: ("ADC $%02X", 2), 0x75: ("ADC $%02X,X", 2),
        0x6D: ("ADC $%04X", 3), 0x7D: ("ADC $%04X,X", 3), 0x79: ("ADC $%04X,Y", 3),
        0x61: ("ADC ($%02X,X)", 2), 0x71: ("ADC ($%02X),Y", 2),
        
        # AND - Logical AND
        0x29: ("AND #$%02X", 2), 0x25: ("AND $%02X", 2), 0x35: ("AND $%02X,X", 2),
        0x2D: ("AND $%04X", 3), 0x3D: ("AND $%04X,X", 3), 0x39: ("AND $%04X,Y", 3),
        0x21: ("AND ($%02X,X)", 2), 0x31: ("AND ($%02X),Y", 2),
        
        # ASL - Arithmetic Shift Left
        0x0A: ("ASL A", 1), 0x06: ("ASL $%02X", 2), 0x16: ("ASL $%02X,X", 2),
        0x0E: ("ASL $%04X", 3), 0x1E: ("ASL $%04X,X", 3),
        
        # BCC - Branch if Carry Clear
        0x90: ("BCC $%02X", 2),
        
        # BCS - Branch if Carry Set
        0xB0: ("BCS $%02X", 2),
        
        # BEQ - Branch if Equal
        0xF0: ("BEQ $%02X", 2),
        
        # BIT - Bit Test
        0x24: ("BIT $%02X", 2), 0x2C: ("BIT $%04X", 3),
        
        # BMI - Branch if Minus
        0x30: ("BMI $%02X", 2),
        
        # BNE - Branch if Not Equal
        0xD0: ("BNE $%02X", 2),
        
        # BPL - Branch if Plus
        0x10: ("BPL $%02X", 2),
        
        # BRK - Force Interrupt
        0x00: ("BRK", 1),
        
        # BVC - Branch if Overflow Clear
        0x50: ("BVC $%02X", 2),
        
        # BVS - Branch if Overflow Set
        0x70: ("BVS $%02X", 2),
        
        # CLC - Clear Carry Flag
        0x18: ("CLC", 1),
        
        # CLD - Clear Decimal Flag
        0xD8: ("CLD", 1),
        
        # CLI - Clear Interrupt Flag
        0x58: ("CLI", 1),
        
        # CLV - Clear Overflow Flag
        0xB8: ("CLV", 1),
        
        # CMP - Compare
        0xC9: ("CMP #$%02X", 2), 0xC5: ("CMP $%02X", 2), 0xD5: ("CMP $%02X,X", 2),
        0xCD: ("CMP $%04X", 3), 0xDD: ("CMP $%04X,X", 3), 0xD9: ("CMP $%04X,Y", 3),
        0xC1: ("CMP ($%02X,X)", 2), 0xD1: ("CMP ($%02X),Y", 2),
        
        # CPX - Compare X Register
        0xE0: ("CPX #$%02X", 2), 0xE4: ("CPX $%02X", 2), 0xEC: ("CPX $%04X", 3),
        
        # CPY - Compare Y Register
        0xC0: ("CPY #$%02X", 2), 0xC4: ("CPY $%02X", 2), 0xCC: ("CPY $%04X", 3),
        
        # DEC - Decrement Memory
        0xC6: ("DEC $%02X", 2), 0xD6: ("DEC $%02X,X", 2), 0xCE: ("DEC $%04X", 3), 0xDE: ("DEC $%04X,X", 3),
        
        # DEX - Decrement X Register
        0xCA: ("DEX", 1),
        
        # DEY - Decrement Y Register
        0x88: ("DEY", 1),
        
        # EOR - Exclusive OR
        0x49: ("EOR #$%02X", 2), 0x45: ("EOR $%02X", 2), 0x55: ("EOR $%02X,X", 2),
        0x4D: ("EOR $%04X", 3), 0x5D: ("EOR $%04X,X", 3), 0x59: ("EOR $%04X,Y", 3),
        0x41: ("EOR ($%02X,X)", 2), 0x51: ("EOR ($%02X),Y", 2),
        
        # INC - Increment Memory
        0xE6: ("INC $%02X", 2), 0xF6: ("INC $%02X,X", 2), 0xEE: ("INC $%04X", 3), 0xFE: ("INC $%04X,X", 3),
        
        # INX - Increment X Register
        0xE8: ("INX", 1),
        
        # INY - Increment Y Register
        0xC8: ("INY", 1),
        
        # JMP - Jump
        0x4C: ("JMP $%04X", 3), 0x6C: ("JMP ($%04X)", 3),
        
        # JSR - Jump to Subroutine
        0x20: ("JSR $%04X", 3),
        
        # LDA - Load Accumulator
        0xA9: ("LDA #$%02X", 2), 0xA5: ("LDA $%02X", 2), 0xB5: ("LDA $%02X,X", 2),
        0xAD: ("LDA $%04X", 3), 0xBD: ("LDA $%04X,X", 3), 0xB9: ("LDA $%04X,Y", 3),
        0xA1: ("LDA ($%02X,X)", 2), 0xB1: ("LDA ($%02X),Y", 2),
        
        # LDX - Load X Register
        0xA2: ("LDX #$%02X", 2), 0xA6: ("LDX $%02X", 2), 0xB6: ("LDX $%02X,Y", 2),
        0xAE: ("LDX $%04X", 3), 0xBE: ("LDX $%04X,Y", 3),
        
        # LDY - Load Y Register
        0xA0: ("LDY #$%02X", 2), 0xA4: ("LDY $%02X", 2), 0xB4: ("LDY $%02X,X", 2),
        0xAC: ("LDY $%04X", 3), 0xBC: ("LDY $%04X,X", 3),
        
        # LSR - Logical Shift Right
        0x4A: ("LSR A", 1), 0x46: ("LSR $%02X", 2), 0x56: ("LSR $%02X,X", 2),
        0x4E: ("LSR $%04X", 3), 0x5E: ("LSR $%04X,X", 3),
        
        # NOP - No Operation
        0xEA: ("NOP", 1),
        
        # ORA - Logical OR
        0x09: ("ORA #$%02X", 2), 0x05: ("ORA $%02X", 2), 0x15: ("ORA $%02X,X", 2),
        0x0D: ("ORA $%04X", 3), 0x1D: ("ORA $%04X,X", 3), 0x19: ("ORA $%04X,Y", 3),
        0x01: ("ORA ($%02X,X)", 2), 0x11: ("ORA ($%02X),Y", 2),
        
        # PHA - Push Accumulator
        0x48: ("PHA", 1),
        
        # PHP - Push Processor Status
        0x08: ("PHP", 1),
        
        # PLA - Pull Accumulator
        0x68: ("PLA", 1),
        
        # PLP - Pull Processor Status
        0x28: ("PLP", 1),
        
        # ROL - Rotate Left
        0x2A: ("ROL A", 1), 0x26: ("ROL $%02X", 2), 0x36: ("ROL $%02X,X", 2),
        0x2E: ("ROL $%04X", 3), 0x3E: ("ROL $%04X,X", 3),
        
        # ROR - Rotate Right
        0x6A: ("ROR A", 1), 0x66: ("ROR $%02X", 2), 0x76: ("ROR $%02X,X", 2),
        0x6E: ("ROR $%04X", 3), 0x7E: ("ROR $%04X,X", 3),
        
        # RTI - Return from Interrupt
        0x40: ("RTI", 1),
        
        # RTS - Return from Subroutine
        0x60: ("RTS", 1),
        
        # SBC - Subtract with Carry
        0xE9: ("SBC #$%02X", 2), 0xE5: ("SBC $%02X", 2), 0xF5: ("SBC $%02X,X", 2),
        0xED: ("SBC $%04X", 3), 0xFD: ("SBC $%04X,X", 3), 0xF9: ("SBC $%04X,Y", 3),
        0xE1: ("SBC ($%02X,X)", 2), 0xF1: ("SBC ($%02X),Y", 2),
        
        # SEC - Set Carry Flag
        0x38: ("SEC", 1),
        
        # SED - Set Decimal Flag
        0xF8: ("SED", 1),
        
        # SEI - Set Interrupt Flag
        0x78: ("SEI", 1),
        
        # STA - Store Accumulator
        0x85: ("STA $%02X", 2), 0x95: ("STA $%02X,X", 2), 0x8D: ("STA $%04X", 3),
        0x9D: ("STA $%04X,X", 3), 0x99: ("STA $%04X,Y", 3), 0x81: ("STA ($%02X,X)", 2), 0x91: ("STA ($%02X),Y", 2),
        
        # STX - Store X Register
        0x86: ("STX $%02X", 2), 0x96: ("STX $%02X,Y", 2), 0x8E: ("STX $%04X", 3),
        
        # STY - Store Y Register
        0x84: ("STY $%02X", 2), 0x94: ("STY $%02X,X", 2), 0x8C: ("STY $%04X", 3),
        
        # TAX - Transfer Accumulator to X
        0xAA: ("TAX", 1),
        
        # TAY - Transfer Accumulator to Y
        0xA8: ("TAY", 1),
        
        # TSX - Transfer Stack Pointer to X
        0xBA: ("TSX", 1),
        
        # TXA - Transfer X to Accumulator
        0x8A: ("TXA", 1),
        
        # TXS - Transfer X to Stack Pointer
        0x9A: ("TXS", 1),
        
        # TYA - Transfer Y to Accumulator
        0x98: ("TYA", 1),
        
        # ILLEGAL OPCODES (bazı yaygın olanlar) # yaygin olanlarin haricindekileri, undocumented olarak kabul edilenleri de eklemek gerekli.
        0x0C: ("NOP $%04X", 3),  # TOP
        0x1C: ("NOP $%04X,X", 3),  # TOP
        0x3C: ("NOP $%04X,X", 3),  # TOP
        0x5C: ("NOP $%04X,X", 3),  # TOP
        0x7C: ("NOP $%04X,X", 3),  # TOP
        0xDC: ("NOP $%04X,X", 3),  # TOP
        0xFC: ("NOP $%04X,X", 3),  # TOP
        0x04: ("NOP $%02X", 2),  # DOP
        0x14: ("NOP $%02X,X", 2),  # DOP
        0x34: ("NOP $%02X,X", 2),  # DOP
        0x44: ("NOP $%02X", 2),  # DOP
        0x54: ("NOP $%02X,X", 2),  # DOP
        0x64: ("NOP $%02X", 2),  # DOP
        0x74: ("NOP $%02X,X", 2),  # DOP
        0x80: ("NOP #$%02X", 2),  # DOP
        0x82: ("NOP #$%02X", 2),  # DOP
        0x89: ("NOP #$%02X", 2),  # DOP
        0xC2: ("NOP #$%02X", 2),  # DOP
        0xD4: ("NOP $%02X,X", 2),  # DOP
        0xE2: ("NOP #$%02X", 2),  # DOP
        0xF4: ("NOP $%02X,X", 2),  # DOP
        0x1A: ("NOP", 1),  # NOP
        0x3A: ("NOP", 1),  # NOP
        0x5A: ("NOP", 1),  # NOP
        0x7A: ("NOP", 1),  # NOP
        0xDA: ("NOP", 1),  # NOP
        0xFA: ("NOP", 1),  # NOP
    }
    
    return opcodes

def get_opcode_translations():
    """JSON dosyalarından çeviri tablolarını al"""
    translations = {}
    
    opcode_data = load_opcode_data()
    
    for opcode_name, info in opcode_data.items():
        translations[opcode_name] = {
            'function': info.get('function', ''),
            'c_equivalent': info.get('c_equivalent', ''),
            'qbasic_equivalent': info.get('qbasic_equivalent', ''),
            'pdsx_equivalent': info.get('pdsx_equivalent', ''),
            'commodorebasicv2_equivalent': info.get('commodorebasicv2_equivalent', ''),
            'pseudo_equivalent': info.get('pseudo_equivalent', '')
        }
    
    return translations

if __name__ == "__main__":
    # Test
    opcodes = create_full_opcode_table()
    translations = get_opcode_translations()
    
    print(f"Toplam opcode sayısı: {len(opcodes)}")
    print(f"Çeviri tablosu: {len(translations)} opcode")
    
    # Örnek
    if 0xA9 in opcodes:
        print(f"0xA9: {opcodes[0xA9]}")
    if 'LDA' in translations:
        print(f"LDA çevirisi: {translations['LDA']}")
