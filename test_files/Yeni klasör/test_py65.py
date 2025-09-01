#!/usr/bin/env python3
# py65 test script

try:
    from py65.devices.mpu6502 import MPU
    from py65.memory import ObservableMemory
    from py65.disassembler import Disassembler as PY65Disassembler
    
    print("py65 import başarılı")
    
    mpu = MPU()
    memory = ObservableMemory()
    disasm = PY65Disassembler(mpu, memory)
    
    print("py65 nesneleri oluşturuldu")
    
    # Test kodu: JMP $CCE1 (4C E1 CC)
    test_code = [0x4C, 0xE1, 0xCC, 0xCE, 0xCE, 0xCE]
    start_addr = 0xCC00
    
    print(f"Test kodu: {[hex(x) for x in test_code]}")
    
    # Memory'ye yükle - doğru yöntem
    for i, byte in enumerate(test_code):
        memory[start_addr + i] = byte
    
    print(f"Memory'ye kod yüklendi: ${start_addr:04X}")
    
    # Test et
    length, disasm_text = disasm.instruction_at(start_addr)
    print(f"Test: ${start_addr:04X}: {disasm_text} (length: {length})")
    
    # Sonraki instruction
    length2, disasm_text2 = disasm.instruction_at(start_addr + length)
    print(f"Next: ${start_addr + length:04X}: {disasm_text2} (length: {length2})")
    
    # BRK testi - sıfırlar
    memory[0xDD00] = 0x00
    memory[0xDD01] = 0x00  
    memory[0xDD02] = 0x00
    
    length3, disasm_text3 = disasm.instruction_at(0xDD00)
    print(f"BRK test: $DD00: {disasm_text3} (length: {length3})")
    
    print("py65 test başarılı!")
    
except Exception as e:
    print(f"py65 test hatası: {e}")
    import traceback
    traceback.print_exc()
