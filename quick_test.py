#!/usr/bin/env python3
"""Quick bounds check test for AdvancedDisassembler"""

try:
    from advanced_disassembler import AdvancedDisassembler
    print("✅ AdvancedDisassembler import successful")
    
    # Test 1: Normal case
    print("\n=== Test 1: Normal case ===")
    test_code = bytes([0xA9, 0x00, 0x60])  # LDA #$00, RTS
    disasm = AdvancedDisassembler(0x1000, test_code, output_format='asm')
    result = disasm.disassemble()
    print(f"✅ Normal test successful: {type(result)}")
    if isinstance(result, list):
        print("✅ Returns list format")
        for i, line in enumerate(result):
            if i < 3: print(f"   {line}")
    
    # Test 2: Truncated 2-byte instruction
    print("\n=== Test 2: Truncated 2-byte instruction ===")
    test_code = bytes([0xA9])  # LDA #(missing operand)
    disasm = AdvancedDisassembler(0x1000, test_code, output_format='asm')
    result = disasm.disassemble()
    print(f"✅ Truncated 2-byte test successful")
    if isinstance(result, list):
        for i, line in enumerate(result):
            if i < 5: print(f"   {line}")
    
    # Test 3: Truncated 3-byte instruction
    print("\n=== Test 3: Partially truncated 3-byte instruction ===")
    test_code = bytes([0x8D, 0x20])  # STA $D020 (missing high byte)
    disasm = AdvancedDisassembler(0x1000, test_code, output_format='asm')
    result = disasm.disassemble()
    print(f"✅ Truncated 3-byte test successful")
    if isinstance(result, list):
        for i, line in enumerate(result):
            if i < 5: print(f"   {line}")
    
    # Test 4: Completely truncated 3-byte instruction
    print("\n=== Test 4: Completely truncated 3-byte instruction ===")
    test_code = bytes([0x8D])  # STA (missing both operand bytes)
    disasm = AdvancedDisassembler(0x1000, test_code, output_format='asm')
    result = disasm.disassemble()
    print(f"✅ Completely truncated 3-byte test successful")
    if isinstance(result, list):
        for i, line in enumerate(result):
            if i < 5: print(f"   {line}")
    
    # Test 5: Empty code
    print("\n=== Test 5: Empty code ===")
    test_code = bytes([])
    disasm = AdvancedDisassembler(0x1000, test_code, output_format='asm')
    result = disasm.disassemble()
    print(f"✅ Empty code test successful")
    if isinstance(result, list):
        for i, line in enumerate(result):
            if i < 5: print(f"   {line}")
    
    print("\n🎉 All bounds check tests passed!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
