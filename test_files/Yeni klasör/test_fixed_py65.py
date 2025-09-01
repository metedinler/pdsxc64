"""
Düzeltilmiş py65 test
"""
from advanced_disassembler import AdvancedDisassembler

def test_fixed_py65():
    # Test verisi - JMP $CCE1 + DEC $CECE (bizim working case)
    test_data = bytes([0x4C, 0xE1, 0xCC, 0xCE, 0xCE, 0xCC])
    start_address = 0xCC00
    
    print("Düzeltilmiş py65 test:")
    
    # py65 ile
    print("\npy65 ile (düzeltilmiş):")
    disasm_py65 = AdvancedDisassembler(start_address, test_data, use_py65=True, output_format='tass')
    if disasm_py65.py65_available:
        result_py65 = disasm_py65._disassemble_py65()
        print("py65 çalışıyor:")
        for line in result_py65[:10]:
            print(f"  {line}")
    else:
        print("py65 yüklenemedi")

if __name__ == "__main__":
    test_fixed_py65()
