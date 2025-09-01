#!/usr/bin/env python3
# Çalışan basit disassembler test

from advanced_disassembler_working import AdvancedDisassembler

# Test PRG data - JMP $CCE1, DEC $CECE, etc.
test_prg = bytes([
    0x00, 0xCC,  # Start address $CC00
    0x4C, 0xE1, 0xCC,  # JMP $CCE1
    0xCE, 0xCE, 0xCE,  # DEC $CECE
    0xCE, 0xCE, 0xCE,  # DEC $CECE
    0xCD, 0xCD, 0xCD,  # CMP $CDCD
    0xCE, 0xCE, 0x21,  # DEC $21CE
    0x25, 0x21,        # AND $21
    0x25, 0x21,        # AND $21
    0x78,              # SEI
    0x47,              # ???
    0x47,              # ???
    0x47,              # ???
    0x6E, 0x6B, 0x25,  # ROR $256B
    0x2F,              # ???
    0xAD, 0x5E, 0xAE,  # LDA $AE5E
    0x5F,              # ???
    0x2E, 0xB1, 0x40,  # ROL $40B1
    0x23,              # ???
    0x45, 0x00,        # EOR $00
    0xAA,              # TAX
])

print("Çalışan BASIT Disassembler (advanced disassembler working):")
start_addr = test_prg[0] + (test_prg[1] << 8)
code_data = test_prg[2:]

disasm = AdvancedDisassembler(
    start_address=start_addr,
    code=code_data,
    use_py65=False,  # py65 kullanma - basit disassembler
    use_illegal_opcodes=True,
    output_format='asm'
)

result = disasm.disassemble_simple(test_prg)
print(result)
