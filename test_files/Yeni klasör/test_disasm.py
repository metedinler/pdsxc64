"""
Test disassembler API
"""
from py65.devices.mpu6502 import MPU
from py65.memory import ObservableMemory

# Test data: LDA #$41; STA $0400; RTS
test_code = [0xA9, 0x41, 0x8D, 0x00, 0x04, 0x60]

# MPU ve Memory oluştur
mpu = MPU()
memory = ObservableMemory()

# Code'u memory'ye yükle
start_addr = 0xC000
for i, byte in enumerate(test_code):
    memory[start_addr + i] = byte

# MPU memory'yi set et
mpu.memory = memory

print("Test disassembly:")
pc = start_addr
for i in range(6):  # 6 instruction test
    try:
        # MPU disassemble method kullan
        instruction = mpu.disassemble(pc)
        print(f"${pc:04X}: {instruction}")
        
        # Next instruction için PC'yi güncelle
        opcode = memory[pc]
        if opcode == 0xA9:  # LDA immediate
            pc += 2
        elif opcode == 0x8D:  # STA absolute
            pc += 3
        elif opcode == 0x60:  # RTS
            pc += 1
        else:
            pc += 1
            
    except Exception as e:
        print(f"${pc:04X}: ERROR - {e}")
        pc += 1
