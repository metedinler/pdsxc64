#!/usr/bin/env python3
"""
Geliştirilmiş BASIC Detokenizer - ML Hatası Çözümü
BASIC ve Machine Language (ML) programlarını ayırt eder
"""
import logging
from basic_detokenizer import BasicDetokenizer

class EnhancedBasicDetokenizer(BasicDetokenizer):
    """ML hatası düzeltilmiş gelişmiş BASIC detokenizer"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
    
    def analyze_prg_type(self, prg_data):
        """PRG dosyasının tipini analiz et (BASIC vs ML)"""
        if len(prg_data) < 2:
            return "unknown", "Dosya çok küçük"
        
        start_address = prg_data[0] + (prg_data[1] << 8)
        
        # C64 BASIC programları genellikle $0801'de başlar
        if start_address == 0x0801:
            return "basic", f"BASIC program (${start_address:04X})"
        
        # Machine Language program adresleri
        common_ml_addresses = {
            0x0800: "ML program (alternative BASIC start)",
            0x1000: "ML program (4KB start)", 
            0x2000: "ML program (8KB start)",
            0x4000: "ML program (16KB start)",
            0x8000: "ML program (32KB start)",
            0xA000: "ML program (40KB start)",
            0xC000: "ML program (49KB start)",
        }
        
        if start_address in common_ml_addresses:
            return "machine_language", common_ml_addresses[start_address]
        
        # Diğer adresler
        if start_address < 0x0801:
            return "machine_language", f"ML program (${start_address:04X}) - Low memory"
        elif start_address > 0x0801 and start_address < 0x2000:
            return "machine_language", f"ML program (${start_address:04X}) - BASIC area"
        else:
            return "machine_language", f"ML program (${start_address:04X}) - High memory"
    
    def detokenize_prg(self, prg_data):
        """Geliştirilmiş PRG analizi - BASIC ve ML'yi ayırt eder"""
        try:
            # Önce dosya tipini analiz et
            file_type, description = self.analyze_prg_type(prg_data)
            
            if file_type == "basic":
                # BASIC program - normal detokenize işlemi
                return super().detokenize_prg(prg_data)
            
            elif file_type == "machine_language":
                # Machine Language program - disassembly öner
                start_address = prg_data[0] + (prg_data[1] << 8)
                size = len(prg_data) - 2
                
                return [
                    f"MACHINE LANGUAGE PROGRAM DETECTED",
                    f"Start Address: ${start_address:04X}",
                    f"Program Size: {size} bytes",
                    f"Description: {description}",
                    "",
                    "This is not a BASIC program - it contains machine language code.",
                    "To analyze this file, use:",
                    "  • Disassembler (disassembler.py)",
                    "  • Improved Disassembler (improved_disassembler.py)", 
                    "  • Professional Disassembler (py65_professional_disassembler.py)",
                    "",
                    f"Hex dump preview (first 32 bytes):",
                    self._create_hex_dump(prg_data[:34], start_address-2)  # Include load address
                ]
            
            else:
                return [f"UNKNOWN FILE TYPE: {description}"]
                
        except Exception as e:
            self.logger.error(f"Enhanced detokenize error: {e}")
            return [f"ERROR: Enhanced detokenization failed: {e}"]
    
    def _create_hex_dump(self, data, start_addr):
        """Hex dump oluştur"""
        lines = []
        for i in range(0, len(data), 16):
            addr = start_addr + i
            chunk = data[i:i+16]
            
            # Hex representation
            hex_str = " ".join(f"{b:02X}" for b in chunk)
            hex_str = hex_str.ljust(48)  # 16 bytes * 3 chars = 48
            
            # ASCII representation
            ascii_str = ""
            for b in chunk:
                if 32 <= b <= 126:
                    ascii_str += chr(b)
                else:
                    ascii_str += "."
            
            lines.append(f"{addr:04X}: {hex_str} |{ascii_str}|")
        
        return "\n".join(lines)
    
    def suggest_analysis_tools(self, prg_data):
        """Dosya tipine göre analiz araçları öner"""
        file_type, description = self.analyze_prg_type(prg_data)
        
        suggestions = {
            "basic": [
                "basic_detokenizer.py - BASIC kod çözme",
                "c64_basic_parser.py - BASIC analizi", 
                "c64bas_transpiler_c.py - C çevirisi",
                "c64bas_transpiler_qbasic.py - QBasic çevirisi"
            ],
            "machine_language": [
                "disassembler.py - Temel disassembly",
                "improved_disassembler.py - Gelişmiş disassembly",
                "py65_professional_disassembler.py - Profesyonel analiz",
                "hybrid_program_analyzer.py - Hibrit analiz"
            ],
            "unknown": [
                "hex_viewer.py - Ham veri görüntüleme",
                "file_analyzer.py - Dosya tipi analizi"
            ]
        }
        
        return {
            "file_type": file_type,
            "description": description,
            "suggested_tools": suggestions.get(file_type, suggestions["unknown"])
        }

def test_enhanced_detokenizer():
    """Geliştirilmiş detokenizer test"""
    print("🔍 Testing Enhanced BASIC Detokenizer")
    print("=" * 50)
    
    detokenizer = EnhancedBasicDetokenizer()
    
    # Test 1: BASIC program
    print("\n📝 Test 1: BASIC Program")
    basic_data = bytes([
        0x01, 0x08,  # Load address $0801
        0x0B, 0x08,  # Next line address
        0x0A, 0x00,  # Line number 10
        0x99, 0x22,  # PRINT "
        0x48, 0x45, 0x4C, 0x4C, 0x4F,  # HELLO
        0x22, 0x00,  # " and line end
        0x00, 0x00   # Program end
    ])
    
    lines = detokenizer.detokenize_prg(basic_data)
    for line in lines:
        print(f"  {line}")
    
    # Test 2: Machine Language program
    print("\n⚙️ Test 2: Machine Language Program")
    ml_data = bytes([
        0x00, 0x08,  # Load address $0800 (ML program)
        0xA9, 0x05,  # LDA #$05
        0x8D, 0x20, 0xD0,  # STA $D020
        0x60,        # RTS
        0x00, 0x00   # Padding
    ])
    
    lines = detokenizer.detokenize_prg(ml_data)
    for line in lines:
        print(f"  {line}")
    
    # Test 3: Analysis suggestions
    print("\n🔧 Test 3: Analysis Tool Suggestions")
    suggestions = detokenizer.suggest_analysis_tools(ml_data)
    print(f"File Type: {suggestions['file_type']}")
    print(f"Description: {suggestions['description']}")
    print("Suggested Tools:")
    for tool in suggestions['suggested_tools']:
        print(f"  • {tool}")

if __name__ == "__main__":
    test_enhanced_detokenizer()
