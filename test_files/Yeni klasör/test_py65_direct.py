"""
Direkt py65 problemi test
"""
try:
    from py65.devices.mpu6502 import MPU
    from py65.memory import ObservableMemory
    from py65.disassembler import Disassembler as PY65Disassembler

    # Test verisi - JMP $CCE1 (0x4C 0xE1 0xCC)
    test_data = bytes([0x4C, 0xE1, 0xCC])
    start_address = 0xCC00

    # py65 setup
    memory = ObservableMemory()
    mpu = MPU(memory)
    py65_disassembler = PY65Disassembler(mpu, memory)

    # Memory'ye kodu yükle
    memory[start_address:start_address + len(test_data)] = test_data

    print("py65 instruction_at test:")
    try:
        length, disasm_text = py65_disassembler.instruction_at(start_address)
        print(f"$CC00: {disasm_text} (length: {length})")
        
        # Opcode'u kontrol et
        opcode = memory[start_address]
        print(f"Opcode: 0x{opcode:02X}")
        
        # Memory'deki veriler
        print(f"Memory[$CC00]: 0x{memory[start_address]:02X}")
        print(f"Memory[$CC01]: 0x{memory[start_address+1]:02X}")  
        print(f"Memory[$CC02]: 0x{memory[start_address+2]:02X}")
        
    except Exception as e:
        print(f"py65 hatası: {e}")

    # Manuel 0x4C testi
    print(f"\n0x4C opcode manual test:")
    print(f"0x4C = {0x4C} = 76 decimal")
    print(f"Expected: JMP instruction")
    
except ImportError as e:
    print(f"py65 import hatası: {e}")
except Exception as e:
    print(f"Genel hata: {e}")
