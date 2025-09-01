"""
Test advanced disassembler ile tam opcode table
"""
import json
from advanced_disassembler import AdvancedDisassembler

def test_with_complete_opcodes():
    # Tam opcode haritasını yükle
    with open('complete_6502_opcode_map.json', 'r') as f:
        complete_opcodes = json.load(f)
    
    # Test verisi - JMP $CCE1 + DEC $CECE (bizim working case)
    test_data = bytes([0x4C, 0xE1, 0xCC, 0xCE, 0xCE, 0xCC])
    start_address = 0xCC00
    
    print("Test: Complete opcode map ile disassemble")
    
    # Basic disassembler - direkt method çağır
    disasm = AdvancedDisassembler(start_address, test_data, use_py65=False, output_format='tass')
    result = disasm._disassemble_basic()
    print("Basic disassembler:")
    for line in result[:10]:
        print(f"  {line}")
    
    # Şimdi py65 ile
    print("\npy65 ile:")
    disasm_py65 = AdvancedDisassembler(start_address, test_data, use_py65=True, output_format='tass')
    result_py65 = disasm_py65._disassemble_py65()
    for line in result_py65[:10]:
        print(f"  {line}")
    
    # Complete opcodes ile kendi disassembler
    print("\nComplete opcodes ile:")
    result_complete = disassemble_with_complete_opcodes(test_data, start_address, complete_opcodes)
    for line in result_complete[:10]:
        print(f"  {line}")

def disassemble_with_complete_opcodes(code, start_address, opcode_map):
    """Complete opcode map ile disassemble"""
    lines = []
    pc = start_address
    end_address = start_address + len(code)
    
    while pc < end_address:
        if pc - start_address >= len(code):
            break
            
        opcode = code[pc - start_address]
        opcode_key = f"0x{opcode:02X}"
        
        if opcode_key in opcode_map:
            opcode_info = opcode_map[opcode_key]
            mnemonic = opcode_info["mnemonic"]
            length = opcode_info["length"]
            
            if mnemonic == "???":
                # Illegal opcode
                lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
                pc += 1
            elif length == 1:
                lines.append(f"${pc:04X}: {mnemonic}")
                pc += length
            elif length == 2:
                if pc - start_address + 1 < len(code):
                    operand = code[pc - start_address + 1]
                    # Instruction'ı format et
                    if "JMP" in mnemonic or "JSR" in mnemonic:
                        formatted = f"{mnemonic.split()[0]} ${operand:02X}"
                    elif "#$" in opcode_info["description"]:
                        formatted = f"{mnemonic} #${operand:02X}"
                    elif "$nn,X" in opcode_info["description"]:
                        formatted = f"{mnemonic} ${operand:02X},X"
                    elif "$nn,Y" in opcode_info["description"]:
                        formatted = f"{mnemonic} ${operand:02X},Y"
                    else:
                        formatted = f"{mnemonic} ${operand:02X}"
                    lines.append(f"${pc:04X}: {formatted}")
                else:
                    lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
                pc += length
            elif length == 3:
                if pc - start_address + 2 < len(code):
                    operand_lo = code[pc - start_address + 1]
                    operand_hi = code[pc - start_address + 2]
                    operand = operand_lo + (operand_hi << 8)
                    # Instruction'ı format et
                    if "JMP" in mnemonic:
                        formatted = f"{mnemonic.split()[0]} ${operand:04X}"
                    elif ",X" in opcode_info["description"]:
                        formatted = f"{mnemonic} ${operand:04X},X"
                    elif ",Y" in opcode_info["description"]:
                        formatted = f"{mnemonic} ${operand:04X},Y"
                    else:
                        formatted = f"{mnemonic} ${operand:04X}"
                    lines.append(f"${pc:04X}: {formatted}")
                else:
                    lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
                pc += length
        else:
            # Bilinmeyen opcode
            lines.append(f"${pc:04X}: .BYTE ${opcode:02X}")
            pc += 1
    
    return lines

if __name__ == "__main__":
    test_with_complete_opcodes()
