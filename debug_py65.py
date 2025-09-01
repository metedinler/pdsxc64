"""
AdvancedDisassembler py65 debug
"""
from advanced_disassembler import AdvancedDisassembler

def debug_py65():
    # Test verisi - JMP $CCE1 
    test_data = bytes([0x4C, 0xE1, 0xCC])
    start_address = 0xCC00
    
    print("py65 debug:")
    
    # py65 ile
    disasm_py65 = AdvancedDisassembler(start_address, test_data, use_py65=True, output_format='tass')
    
    if disasm_py65.py65_available:
        print("py65 available - debug başlıyor")
        
        # Memory'ye kodu yükle
        disasm_py65.memory[start_address:start_address + len(test_data)] = test_data
        
        print(f"Memory[$CC00]: 0x{disasm_py65.memory[start_address]:02X}")
        print(f"Memory[$CC01]: 0x{disasm_py65.memory[start_address+1]:02X}")  
        print(f"Memory[$CC02]: 0x{disasm_py65.memory[start_address+2]:02X}")
        
        # Direkt instruction_at test
        try:
            length, disasm_text = disasm_py65.py65_disassembler.instruction_at(start_address)
            print(f"Direkt py65 result: {disasm_text} (length: {length})")
        except Exception as e:
            print(f"Direkt py65 hatası: {e}")
            import traceback
            traceback.print_exc()
        
        # _disassemble_py65 test
        try:
            result = disasm_py65._disassemble_py65()
            print("_disassemble_py65 result:")
            for line in result[:3]:
                print(f"  {line}")
        except Exception as e:
            print(f"_disassemble_py65 hatası: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("py65 yüklenemedi")

if __name__ == "__main__":
    debug_py65()
