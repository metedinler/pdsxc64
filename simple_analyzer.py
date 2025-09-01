"""
Simple illegal opcode analyzer for 6502 PRG files
"""

class SimpleIllegalAnalyzer:
    def __init__(self):
        # Legal 6502 opcodes
        self.legal_opcodes = {
            0x00, 0x01, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0D, 0x0E, 0x10, 0x11, 0x15, 0x16, 0x18, 0x19, 0x1D, 0x1E,
            0x20, 0x21, 0x24, 0x25, 0x26, 0x28, 0x29, 0x2A, 0x2C, 0x2D, 0x2E, 0x30, 0x31, 0x35, 0x36, 0x38, 0x39, 0x3D, 0x3E,
            0x40, 0x41, 0x45, 0x46, 0x48, 0x49, 0x4A, 0x4C, 0x4D, 0x4E, 0x50, 0x51, 0x55, 0x56, 0x58, 0x59, 0x5D, 0x5E,
            0x60, 0x61, 0x65, 0x66, 0x68, 0x69, 0x6A, 0x6C, 0x6D, 0x6E, 0x70, 0x71, 0x75, 0x76, 0x78, 0x79, 0x7D, 0x7E,
            0x81, 0x84, 0x85, 0x86, 0x88, 0x8A, 0x8C, 0x8D, 0x8E, 0x90, 0x91, 0x94, 0x95, 0x96, 0x98, 0x99, 0x9A, 0x9D,
            0xA0, 0xA1, 0xA2, 0xA4, 0xA5, 0xA6, 0xA8, 0xA9, 0xAA, 0xAC, 0xAD, 0xAE, 0xB0, 0xB1, 0xB4, 0xB5, 0xB6, 0xB8, 0xB9, 0xBA, 0xBC, 0xBD, 0xBE,
            0xC0, 0xC1, 0xC4, 0xC5, 0xC6, 0xC8, 0xC9, 0xCA, 0xCC, 0xCD, 0xCE, 0xD0, 0xD1, 0xD5, 0xD6, 0xD8, 0xD9, 0xDD, 0xDE,
            0xE0, 0xE1, 0xE4, 0xE5, 0xE6, 0xE8, 0xE9, 0xEA, 0xEC, 0xED, 0xEE, 0xF0, 0xF1, 0xF5, 0xF6, 0xF8, 0xF9, 0xFD, 0xFE
        }
        
        # Instruction lengths (legal opcodes)
        self.instruction_lengths = {
            # 1 byte (implied)
            0x00: 1, 0x08: 1, 0x0A: 1, 0x18: 1, 0x28: 1, 0x38: 1, 0x40: 1, 0x48: 1, 0x4A: 1, 0x58: 1,
            0x60: 1, 0x68: 1, 0x6A: 1, 0x78: 1, 0x88: 1, 0x8A: 1, 0x98: 1, 0x9A: 1, 0xA8: 1, 0xAA: 1,
            0xB8: 1, 0xBA: 1, 0xC8: 1, 0xCA: 1, 0xD8: 1, 0xE8: 1, 0xEA: 1, 0xF8: 1,
            
            # 2 bytes (immediate, zero page, relative)
            0x01: 2, 0x05: 2, 0x06: 2, 0x09: 2, 0x10: 2, 0x11: 2, 0x15: 2, 0x16: 2, 0x21: 2, 0x24: 2,
            0x25: 2, 0x26: 2, 0x29: 2, 0x30: 2, 0x31: 2, 0x35: 2, 0x36: 2, 0x41: 2, 0x45: 2, 0x46: 2,
            0x49: 2, 0x50: 2, 0x51: 2, 0x55: 2, 0x56: 2, 0x61: 2, 0x65: 2, 0x66: 2, 0x69: 2, 0x70: 2,
            0x71: 2, 0x75: 2, 0x76: 2, 0x81: 2, 0x84: 2, 0x85: 2, 0x86: 2, 0x90: 2, 0x91: 2, 0x94: 2,
            0x95: 2, 0x96: 2, 0xA0: 2, 0xA1: 2, 0xA2: 2, 0xA4: 2, 0xA5: 2, 0xA6: 2, 0xA9: 2, 0xB0: 2,
            0xB1: 2, 0xB4: 2, 0xB5: 2, 0xB6: 2, 0xC0: 2, 0xC1: 2, 0xC4: 2, 0xC5: 2, 0xC6: 2, 0xC9: 2,
            0xD0: 2, 0xD1: 2, 0xD5: 2, 0xD6: 2, 0xE0: 2, 0xE1: 2, 0xE4: 2, 0xE5: 2, 0xE6: 2, 0xF0: 2,
            0xF1: 2, 0xF5: 2, 0xF6: 2,
            
            # 3 bytes (absolute, indexed absolute)
            0x0D: 3, 0x0E: 3, 0x19: 3, 0x1D: 3, 0x1E: 3, 0x20: 3, 0x2C: 3, 0x2D: 3, 0x2E: 3, 0x39: 3,
            0x3D: 3, 0x3E: 3, 0x4C: 3, 0x4D: 3, 0x4E: 3, 0x59: 3, 0x5D: 3, 0x5E: 3, 0x6C: 3, 0x6D: 3,
            0x6E: 3, 0x79: 3, 0x7D: 3, 0x7E: 3, 0x8C: 3, 0x8D: 3, 0x8E: 3, 0x99: 3, 0x9D: 3, 0xAC: 3,
            0xAD: 3, 0xAE: 3, 0xB9: 3, 0xBC: 3, 0xBD: 3, 0xBE: 3, 0xCC: 3, 0xCD: 3, 0xCE: 3, 0xD9: 3,
            0xDD: 3, 0xDE: 3, 0xE9: 2, 0xEC: 3, 0xED: 3, 0xEE: 3, 0xF9: 3, 0xFD: 3, 0xFE: 3
        }
        
        # Common illegal opcodes
        self.illegal_opcodes = {
            0x02: "KIL/JAM (Dangerous - freezes CPU)",
            0x03: "SLO (Stable undocumented)",
            0x04: "NOP (Illegal NOP)",
            0x07: "SLO (Stable undocumented)",
            0x0B: "ANC (Undocumented)",
            0x0C: "NOP (Illegal NOP)",
            0x0F: "SLO (Stable undocumented)",
            0x12: "KIL/JAM (Dangerous - freezes CPU)",
            0x13: "SLO (Stable undocumented)",
            0x14: "NOP (Illegal NOP)",
            0x17: "SLO (Stable undocumented)",
            0x1A: "NOP (Illegal NOP)",
            0x1B: "SLO (Stable undocumented)",
            0x1C: "NOP (Illegal NOP)",
            0x1F: "SLO (Stable undocumented)",
            0x22: "KIL/JAM (Dangerous - freezes CPU)",
            0x23: "RLA (Stable undocumented)",
            0x27: "RLA (Stable undocumented)",
            0x2B: "ANC (Undocumented)",
            0x2F: "RLA (Stable undocumented)",
            0x32: "KIL/JAM (Dangerous - freezes CPU)",
            0x33: "RLA (Stable undocumented)",
            0x34: "NOP (Illegal NOP)",
            0x37: "RLA (Stable undocumented)",
            0x3A: "NOP (Illegal NOP)",
            0x3B: "RLA (Stable undocumented)",
            0x3C: "NOP (Illegal NOP)",
            0x3F: "RLA (Stable undocumented)",
            0x42: "KIL/JAM (Dangerous - freezes CPU)",
            0x43: "SRE (Stable undocumented)",
            0x44: "NOP (Illegal NOP)",
            0x47: "SRE (Stable undocumented)",
            0x4B: "ALR (Undocumented)",
            0x4F: "SRE (Stable undocumented)",
            0x52: "KIL/JAM (Dangerous - freezes CPU)",
            0x53: "SRE (Stable undocumented)",
            0x54: "NOP (Illegal NOP)",
            0x57: "SRE (Stable undocumented)",
            0x5A: "NOP (Illegal NOP)",
            0x5B: "SRE (Stable undocumented)",
            0x5C: "NOP (Illegal NOP)",
            0x5F: "SRE (Stable undocumented)",
            0x62: "KIL/JAM (Dangerous - freezes CPU)",
            0x63: "RRA (Stable undocumented)",
            0x64: "NOP (Illegal NOP)",
            0x67: "RRA (Stable undocumented)",
            0x6B: "ARR (Undocumented)",
            0x6F: "RRA (Stable undocumented)",
            0x72: "KIL/JAM (Dangerous - freezes CPU)",
            0x73: "RRA (Stable undocumented)",
            0x74: "NOP (Illegal NOP)",
            0x77: "RRA (Stable undocumented)",
            0x7A: "NOP (Illegal NOP)",
            0x7B: "RRA (Stable undocumented)",
            0x7C: "NOP (Illegal NOP)",
            0x7F: "RRA (Stable undocumented)",
            0x80: "NOP (Illegal NOP)",
            0x82: "NOP (Illegal NOP)",
            0x83: "SAX (Stable undocumented)",
            0x87: "SAX (Stable undocumented)",
            0x89: "NOP (Illegal NOP)",
            0x8B: "XAA (Highly unstable!)",
            0x8F: "SAX (Stable undocumented)",
            0x92: "KIL/JAM (Dangerous - freezes CPU)",
            0x93: "AHX (Unstable)",
            0x97: "SAX (Stable undocumented)",
            0x9B: "TAS (Unstable)",
            0x9C: "SHY (Unstable)",
            0x9E: "SHX (Unstable)",
            0x9F: "AHX (Unstable)",
            0xA3: "LAX (Stable undocumented)",
            0xA7: "LAX (Stable undocumented)",
            0xAB: "LAX (Stable undocumented)",
            0xAF: "LAX (Stable undocumented)",
            0xB2: "KIL/JAM (Dangerous - freezes CPU)",
            0xB3: "LAX (Stable undocumented)",
            0xB7: "LAX (Stable undocumented)",
            0xBB: "LAS (Unstable)",
            0xBF: "LAX (Stable undocumented)",
            0xC2: "NOP (Illegal NOP)",
            0xC3: "DCP (Stable undocumented)",
            0xC7: "DCP (Stable undocumented)",
            0xCB: "AXS/SBX (Stable undocumented)",
            0xCF: "DCP (Stable undocumented)",
            0xD2: "KIL/JAM (Dangerous - freezes CPU)",
            0xD3: "DCP (Stable undocumented)",
            0xD4: "NOP (Illegal NOP)",
            0xD7: "DCP (Stable undocumented)",
            0xDA: "NOP (Illegal NOP)",
            0xDB: "DCP (Stable undocumented)",
            0xDC: "NOP (Illegal NOP)",
            0xDF: "DCP (Stable undocumented)",
            0xE2: "NOP (Illegal NOP)",
            0xE3: "ISC (Stable undocumented)",
            0xE7: "ISC (Stable undocumented)",
            0xEB: "SBC (Undocumented)",
            0xEF: "ISC (Stable undocumented)",
            0xF2: "KIL/JAM (Dangerous - freezes CPU)",
            0xF3: "ISC (Stable undocumented)",
            0xF4: "NOP (Illegal NOP)",
            0xF7: "ISC (Stable undocumented)",
            0xFA: "NOP (Illegal NOP)",
            0xFB: "ISC (Stable undocumented)",
            0xFC: "NOP (Illegal NOP)",
            0xFF: "ISC (Stable undocumented)"
        }
        
        # Illegal instruction lengths (assumed based on addressing mode)
        self.illegal_lengths = {
            0x02: 1, 0x03: 2, 0x04: 2, 0x07: 2, 0x0B: 2, 0x0C: 3, 0x0F: 3,
            0x12: 1, 0x13: 2, 0x14: 2, 0x17: 2, 0x1A: 1, 0x1B: 3, 0x1C: 3, 0x1F: 3,
            0x22: 1, 0x23: 2, 0x27: 2, 0x2B: 2, 0x2F: 3, 0x32: 1, 0x33: 2, 0x34: 2,
            0x37: 2, 0x3A: 1, 0x3B: 3, 0x3C: 3, 0x3F: 3, 0x42: 1, 0x43: 2, 0x44: 2,
            0x47: 2, 0x4B: 2, 0x4F: 3, 0x52: 1, 0x53: 2, 0x54: 2, 0x57: 2, 0x5A: 1,
            0x5B: 3, 0x5C: 3, 0x5F: 3, 0x62: 1, 0x63: 2, 0x64: 2, 0x67: 2, 0x6B: 2,
            0x6F: 3, 0x72: 1, 0x73: 2, 0x74: 2, 0x77: 2, 0x7A: 1, 0x7B: 3, 0x7C: 3,
            0x7F: 3, 0x80: 2, 0x82: 2, 0x83: 2, 0x87: 2, 0x89: 2, 0x8B: 2, 0x8F: 3,
            0x92: 1, 0x93: 2, 0x97: 2, 0x9B: 3, 0x9C: 3, 0x9E: 3, 0x9F: 3, 0xA3: 2,
            0xA7: 2, 0xAB: 2, 0xAF: 3, 0xB2: 1, 0xB3: 2, 0xB7: 2, 0xBB: 3, 0xBF: 3,
            0xC2: 2, 0xC3: 2, 0xC7: 2, 0xCB: 2, 0xCF: 3, 0xD2: 1, 0xD3: 2, 0xD4: 2,
            0xD7: 2, 0xDA: 1, 0xDB: 3, 0xDC: 3, 0xDF: 3, 0xE2: 2, 0xE3: 2, 0xE7: 2,
            0xEB: 2, 0xEF: 3, 0xF2: 1, 0xF3: 2, 0xF4: 2, 0xF7: 2, 0xFA: 1, 0xFB: 3,
            0xFC: 3, 0xFF: 3
        }
        
        # Merge lengths
        self.all_lengths = {**self.instruction_lengths, **self.illegal_lengths}
    
    def analyze_prg_file(self, file_path):
        """Analyze a PRG file for illegal opcodes"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            if len(data) < 2:
                return {
                    'error': 'File too small',
                    'total_instructions': 0,
                    'illegal_opcodes': []
                }
            
            # Skip PRG header (first 2 bytes = load address)
            load_address = data[0] | (data[1] << 8)
            code_data = data[2:]
            
            print(f"Analyzing PRG file: {file_path}")
            print(f"Load address: ${load_address:04X}")
            print(f"Code size: {len(code_data)} bytes")
            
            return self.analyze_code(code_data, load_address)
            
        except Exception as e:
            return {
                'error': f'File read error: {str(e)}',
                'total_instructions': 0,
                'illegal_opcodes': []
            }
    
    def analyze_code(self, code_data, start_address=0x1000):
        """Analyze code data for illegal opcodes"""
        illegal_opcodes = []
        total_instructions = 0
        i = 0
        
        while i < len(code_data):
            opcode = code_data[i]
            address = start_address + i
            
            # Get instruction length
            length = self.all_lengths.get(opcode, 1)
            
            # Get operand bytes
            operand_bytes = []
            for j in range(1, length):
                if i + j < len(code_data):
                    operand_bytes.append(code_data[i + j])
            
            # Check if illegal
            if opcode in self.illegal_opcodes:
                # Get context
                context_start = max(0, i - 3)
                context_end = min(len(code_data), i + 4)
                context = code_data[context_start:context_end]
                
                illegal_opcodes.append({
                    'address': address,
                    'opcode': opcode,
                    'description': self.illegal_opcodes[opcode],
                    'operand_bytes': operand_bytes,
                    'context': context,
                    'context_position': i - context_start,
                    'is_dangerous': 'KIL/JAM' in self.illegal_opcodes[opcode]
                })
            
            total_instructions += 1
            i += length
        
        return {
            'total_instructions': total_instructions,
            'illegal_count': len(illegal_opcodes),
            'illegal_opcodes': illegal_opcodes
        }
    
    def print_results(self, results):
        """Print analysis results"""
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return
        
        print(f"\n📊 Analysis Results:")
        print(f"   Total instructions: {results['total_instructions']}")
        print(f"   Illegal opcodes found: {results['illegal_count']}")
        
        if results['illegal_count'] == 0:
            print("   ✅ No illegal opcodes found! Code is clean.")
            return
        
        print(f"\n🔍 Illegal Opcodes Found:")
        print("=" * 60)
        
        dangerous_count = 0
        for i, illegal in enumerate(results['illegal_opcodes'], 1):
            if illegal['is_dangerous']:
                dangerous_count += 1
                danger_mark = "🚨 DANGEROUS"
            else:
                danger_mark = "⚠️ "
            
            print(f"\n#{i} {danger_mark}")
            print(f"   Address: ${illegal['address']:04X}")
            print(f"   Opcode: ${illegal['opcode']:02X}")
            print(f"   Description: {illegal['description']}")
            
            if illegal['operand_bytes']:
                operand_str = ' '.join(f"${b:02X}" for b in illegal['operand_bytes'])
                print(f"   Operands: {operand_str}")
            
            # Print context
            context_str = ' '.join(f"${b:02X}" for b in illegal['context'])
            marker_pos = illegal['context_position'] * 4  # 4 chars per byte ($XX )
            context_with_marker = context_str[:marker_pos] + '^^' + context_str[marker_pos+2:]
            print(f"   Context: {context_str}")
            print(f"            {' ' * marker_pos}^^")
        
        if dangerous_count > 0:
            print(f"\n🚨 WARNING: {dangerous_count} dangerous KIL/JAM instructions found!")
            print("   These instructions will freeze the CPU!")


# Test function
def test_analyzer():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_analyzer.py <prg_file>")
        return
    
    analyzer = SimpleIllegalAnalyzer()
    results = analyzer.analyze_prg_file(sys.argv[1])
    analyzer.print_results(results)


if __name__ == "__main__":
    test_analyzer()
