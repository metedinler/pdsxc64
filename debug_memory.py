"""
py65 memory instance debug
"""
from advanced_disassembler import AdvancedDisassembler
from py65.devices.mpu6502 import MPU
from py65.memory import ObservableMemory
from py65.disassembler import Disassembler as PY65Disassembler

def debug_memory_instances():
    # Test verisi - JMP $CCE1 
    test_data = bytes([0x4C, 0xE1, 0xCC])
    start_address = 0xCC00
    
    print("Memory instance debug:")
    
    # AdvancedDisassembler instance
    disasm = AdvancedDisassembler(start_address, test_data, use_py65=True, output_format='tass')
    
    if disasm.py65_available:
        print("AdvancedDisassembler memory test:")
        print(f"Memory type: {type(disasm.memory)}")
        print(f"MPU type: {type(disasm.mpu)}")
        print(f"Disassembler type: {type(disasm.py65_disassembler)}")
        
        # Memory'ye yükle
        disasm.memory[start_address:start_address + len(test_data)] = test_data
        
        print(f"Memory[$CC00]: 0x{disasm.memory[start_address]:02X}")
        
        # MPU memory ile aynı mı test et
        print(f"MPU memory == disasm memory: {disasm.mpu.memory is disasm.memory}")
        print(f"MPU memory[$CC00]: 0x{disasm.mpu.memory[start_address]:02X}")
        
        # py65 disassembler test
        try:
            length, disasm_text = disasm.py65_disassembler.instruction_at(start_address)
            print(f"Result: {disasm_text} (length: {length})")
        except Exception as e:
            print(f"Hata: {e}")
            
    print("\nDirekt py65 test (karşılaştırma):")
    memory2 = ObservableMemory()
    mpu2 = MPU(memory2)
    py65_disasm2 = PY65Disassembler(mpu2)
    
    # Memory'ye yükle
    memory2[start_address:start_address + len(test_data)] = test_data
    print(f"Direct memory[$CC00]: 0x{memory2[start_address]:02X}")
    
    try:
        length, disasm_text = py65_disasm2.instruction_at(start_address)
        print(f"Direct result: {disasm_text} (length: {length})")
    except Exception as e:
        print(f"Direct hata: {e}")

if __name__ == "__main__":
    debug_memory_instances()
