#!/usr/bin/env python3
"""
Simple BASIC Detokenizer for Commodore 64
$0801 programlarını BASIC koduna çevirmek için
"""

# C64 BASIC token tablosu
C64_BASIC_TOKENS = {
    0x80: "END",
    0x81: "FOR",
    0x82: "NEXT",
    0x83: "DATA",
    0x84: "INPUT#",
    0x85: "INPUT",
    0x86: "DIM",
    0x87: "READ",
    0x88: "LET",
    0x89: "GOTO",
    0x8A: "RUN",
    0x8B: "IF",
    0x8C: "RESTORE",
    0x8D: "GOSUB",
    0x8E: "RETURN",
    0x8F: "REM",
    0x90: "STOP",
    0x91: "ON",
    0x92: "WAIT",
    0x93: "LOAD",
    0x94: "SAVE",
    0x95: "VERIFY",
    0x96: "DEF",
    0x97: "POKE",
    0x98: "PRINT#",
    0x99: "PRINT",
    0x9A: "CONT",
    0x9B: "LIST",
    0x9C: "CLR",
    0x9D: "CMD",
    0x9E: "SYS",
    0x9F: "OPEN",
    0xA0: "CLOSE",
    0xA1: "GET",
    0xA2: "NEW",
    0xA3: "TAB(",
    0xA4: "TO",
    0xA5: "FN",
    0xA6: "SPC(",
    0xA7: "THEN",
    0xA8: "NOT",
    0xA9: "STEP",
    0xAA: "+",
    0xAB: "-",
    0xAC: "*",
    0xAD: "/",
    0xAE: "^",
    0xAF: "AND",
    0xB0: "OR",
    0xB1: ">",
    0xB2: "=",
    0xB3: "<",
    0xB4: "SGN",
    0xB5: "INT",
    0xB6: "ABS",
    0xB7: "USR",
    0xB8: "FRE",
    0xB9: "POS",
    0xBA: "SQR",
    0xBB: "RND",
    0xBC: "LOG",
    0xBD: "EXP",
    0xBE: "COS",
    0xBF: "SIN",
    0xC0: "TAN",
    0xC1: "ATN",
    0xC2: "PEEK",
    0xC3: "LEN",
    0xC4: "STR$",
    0xC5: "VAL",
    0xC6: "ASC",
    0xC7: "CHR$",
    0xC8: "LEFT$",
    0xC9: "RIGHT$",
    0xCA: "MID$",
    0xCB: "GO"
}

class BasicDetokenizer:
    def __init__(self):
        self.tokens = C64_BASIC_TOKENS
        
    def detokenize_prg(self, prg_data):
        """PRG dosyasını BASIC koduna çevir"""
        try:
            if len(prg_data) < 4:
                return ["ERROR: File too small"]
            
            # Start address kontrolü
            start_address = prg_data[0] + (prg_data[1] << 8)
            if start_address != 0x0801:
                return [f"ERROR: Not a BASIC program (start: ${start_address:04X}, expected: $0801)"]
            
            # BASIC program data
            data = prg_data[2:]  # Skip load address
            lines = []
            pos = 0
            
            while pos < len(data):
                # Program end check
                if pos + 1 < len(data) and data[pos] == 0x00 and data[pos + 1] == 0x00:
                    break
                
                # Line structure: [next_line_addr_lo] [next_line_addr_hi] [line_no_lo] [line_no_hi] [tokens...] [0x00]
                if pos + 4 >= len(data):
                    break
                
                next_line_addr = data[pos] + (data[pos + 1] << 8)
                line_number = data[pos + 2] + (data[pos + 3] << 8)
                
                # Invalid line
                if next_line_addr == 0:
                    break
                
                pos += 4  # Skip line header
                
                # Extract line tokens
                line_text = f"{line_number} "
                
                while pos < len(data) and data[pos] != 0x00:
                    byte = data[pos]
                    
                    if byte in self.tokens:
                        # Token
                        line_text += self.tokens[byte]
                    elif byte == 0x22:  # Quote
                        line_text += '"'
                    elif byte >= 0x20 and byte <= 0x7E:
                        # Printable ASCII
                        line_text += chr(byte)
                    else:
                        # Non-printable
                        line_text += f"[{byte:02X}]"
                    
                    pos += 1
                
                lines.append(line_text)
                
                # Skip line terminator
                if pos < len(data) and data[pos] == 0x00:
                    pos += 1
            
            return lines if lines else ["ERROR: No BASIC lines found"]
            
        except Exception as e:
            return [f"ERROR: Detokenization failed: {e}"]
    
    def transpile_to_format(self, basic_lines, output_format):
        """BASIC lines'ı farklı formatlara çevir"""
        try:
            if not basic_lines or any(line.startswith("ERROR:") for line in basic_lines):
                return "\n".join(basic_lines)
            
            result = []
            
            if output_format == "commodorebasicv2":
                # Orijinal BASIC format
                return "\n".join(basic_lines)
            
            elif output_format == "qbasic":
                # QBasic format
                result.append("REM Converted from Commodore 64 BASIC")
                result.append("REM")
                
                for line in basic_lines:
                    if " " in line:
                        line_num, code = line.split(" ", 1)
                        result.append(f"'{line_num}: {code}")
                    else:
                        result.append(f"'{line}")
                
                return "\n".join(result)
            
            elif output_format == "c":
                # C format
                result.append("/* Converted from Commodore 64 BASIC */")
                result.append("#include <stdio.h>")
                result.append("#include <stdlib.h>")
                result.append("")
                result.append("int main() {")
                result.append("    printf(\"C64 BASIC Program\\n\");")
                
                for line in basic_lines:
                    if " " in line:
                        line_num, code = line.split(" ", 1)
                        result.append(f"    // Line {line_num}: {code}")
                    else:
                        result.append(f"    // {line}")
                
                result.append("    return 0;")
                result.append("}")
                
                return "\n".join(result)
            
            elif output_format == "pdsx":
                # PDSX format (similar to BASIC)
                result.append("; Converted from Commodore 64 BASIC")
                result.append("; PDSX Format")
                result.append("")
                
                for line in basic_lines:
                    result.append(f"; {line}")
                
                return "\n".join(result)
            
            else:
                # Default: comment format
                result.append(f"; Commodore 64 BASIC Program")
                result.append(f"; Use commodorebasicv2 format for proper BASIC code")
                result.append("")
                
                for line in basic_lines:
                    result.append(f"; {line}")
                
                return "\n".join(result)
                
        except Exception as e:
            return f"ERROR: Transpilation failed: {e}"

# Test function
def test_detokenizer():
    """Test the detokenizer"""
    print("🔍 Testing BASIC Detokenizer")
    
    # Test data: 10 PRINT "HELLO"
    test_data = bytes([
        0x01, 0x08,  # Load address $0801
        0x0B, 0x08,  # Next line address
        0x0A, 0x00,  # Line number 10
        0x99, 0x22,  # PRINT "
        0x48, 0x45, 0x4C, 0x4C, 0x4F,  # HELLO
        0x22, 0x00,  # " and line end
        0x00, 0x00   # Program end
    ])
    
    detokenizer = BasicDetokenizer()
    lines = detokenizer.detokenize_prg(test_data)
    
    print("BASIC Lines:")
    for line in lines:
        print(f"  {line}")
    
    print("\nTranspiled to C:")
    c_code = detokenizer.transpile_to_format(lines, "c")
    print(c_code)

if __name__ == "__main__":
    test_detokenizer()
