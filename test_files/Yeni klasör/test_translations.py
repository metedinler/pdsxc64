"""
Çeviri sistemi test betiği
"""

from opcode_manager import OpcodeManager
from advanced_disassembler import AdvancedDisassembler

def test_translations():
    print("=== ÇEVIRI SISTEMI TEST ===")
    
    # OpcodeManager'ı başlat
    manager = OpcodeManager()
    
    print(f"Yüklenen opcode sayısı: {len(manager.opcodes)}")
    print(f"Çeviri tablosu: {len(manager.translations)} opcode")
    
    # Test opcodes
    test_opcodes = ['ADC', 'LDA', 'STA', 'JMP', 'BEQ', 'NOP']
    
    for opcode in test_opcodes:
        if opcode in manager.translations:
            print(f"\n{opcode} çevirileri:")
            translations = manager.translations[opcode]
            for key, value in translations.items():
                print(f"  {key}: {value}")
        else:
            print(f"\n{opcode}: Çeviri bulunamadı")
    
    # Disassembler test
    print("\n=== DISASSEMBLER TEST ===")
    
    # Basit bir PRG verisi (LDA #$01, STA $D020, RTS)
    test_data = bytes([0x00, 0x08,  # Load address: $0800
                      0xA9, 0x01,  # LDA #$01
                      0x8D, 0x20, 0xD0,  # STA $D020
                      0x60])  # RTS
    
    formats = ['asm', 'c', 'qbasic', 'pdsx', 'commodorebasicv2', 'pseudo']
    
    for fmt in formats:
        print(f"\n--- {fmt.upper()} FORMAT ---")
        try:
            disasm = AdvancedDisassembler(0x0800, test_data[2:], output_format=fmt)
            result = disasm.disassemble()
            print(result[:200] + "..." if len(result) > 200 else result)
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    test_translations()
