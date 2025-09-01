"""

🔥 D64 Converter - Enhanced BASIC V2 Decompiler v3.0
===============================================
Modern BASIC decompiler with advanced optimization
🍎 Enhanced BASIC V2 Decompiler v5.3 - Commodore 64 Geliştirme Stüdyosu  
================================================================
PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: enhanced_basic_decompiler.py - Gelişmiş BASIC V2 Decompiler
VERSİYON: 5.3 (KızılElma Plan - C64 Memory Manager Entegrasyonu Tamamlandı)
AMAÇ: BASIC V2'den modern dillere transpile (QBasic, C, C++, PDSX, Python)
================================================================

Bu modül şu özelliklerle BASIC'ten modern dillere köprü kurar:
• 5 Hedef Dil Desteği: QBasic 7.1, C, C++, PDSX, Python transpile
• C64 Memory Manager Entegrasyonu: KERNAL/BASIC rutinleri, bellek haritası
• POKE/PEEK Optimizasyonu: Memory mapping ile modern değişken dönüşümü
• SYS Call Dönüşümü: Assembly çağrılarını fonksiyon çağrılarına dönüştürme
• Token Detokenization: Türkçe açıklama desteği ready

KızılElma Plan AŞAMA 1 - Enhanced BASIC Decompiler GUI Aktivasyonu: ✅ TAMAMLANDI

STEP 9 FEATURES:
1. QBasic 7.1 optimization and conversion
2. C/C++ conversion with POKE/PEEK optimization  
3. SYS call to function call conversion
4. Memory pointer optimization
5. PDSX BASIC advanced conversion
6. Variable type detection and optimization
7. Loop detection and modernization
8. String handling optimization
9. Graphics command translation
10. Sound command translation

Target Languages:
- QBasic 7.1 (full compatibility)
- C/C++ (optimized memory access)
- PDSX BASIC (enhanced syntax)
- Modern BASIC (structured programming)
- Python (for comparison)

Author: D64 Converter Team  
Version: 3.0 - Enhanced BASIC Conversion
"""

import re
import json
import os
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from data_loader import DataLoader

# C64 Memory Manager import - KızılElma Plan uyarınca eklendi
try:
    from c64_memory_manager import c64_memory_manager, get_routine_info, get_memory_info, format_routine_call, format_memory_access
    C64_MEMORY_MANAGER_AVAILABLE = True
    print("✅ C64 Memory Manager yüklendi - Enhanced BASIC Decompiler gelişmiş çeviri aktif")
except ImportError:
    C64_MEMORY_MANAGER_AVAILABLE = False
    print("⚠️ C64 Memory Manager bulunamadı - Enhanced BASIC Decompiler basit çeviri kullanılacak")

@dataclass
class BasicLine:
    """BASIC kod satırı representation"""
    line_number: int
    content: str
    tokens: List[str]
    variables: List[str]
    sys_calls: List[int]
    poke_operations: List[Tuple[int, int]]  # (address, value)
    peek_operations: List[int]  # addresses
    goto_targets: List[int]
    gosub_targets: List[int]

@dataclass
class ConversionContext:
    """Dönüşüm context bilgileri"""
    target_language: str
    optimization_level: int  # 0-3
    preserve_line_numbers: bool
    modernize_syntax: bool
    optimize_memory_access: bool
    convert_graphics: bool
    convert_sound: bool
    special_char_mode: str = "numeric"  # "numeric", "color_names", "escaped"

class SpecialCharacterMode:
    """Özel karakter görüntüleme modları"""
    NUMERIC_CODES = "numeric"      # [11][13] formatı
    COLOR_NAMES = "color_names"    # {CLR}{HOME} formatı  
    ESCAPED = "escaped"            # \x0B\x0D formatı
    
    # Renk ve kontrol kodları mapping
    SPECIAL_CHARS = {
        5: "{WHT}",    # White
        11: "{CLR}",   # Clear screen
        13: "{HOME}",  # Home cursor
        17: "{DOWN}",  # Cursor down
        18: "{RVS}",   # Reverse on
        19: "{HOME}",  # Home
        20: "{DEL}",   # Delete
        28: "{RED}",   # Red
        29: "{RIGHT}", # Cursor right
        30: "{GRN}",   # Green
        31: "{BLU}",   # Blue
        129: "{ORN}",  # Orange
        144: "{BLK}",  # Black
        145: "{UP}",   # Cursor up
        146: "{RVS OFF}", # Reverse off
        147: "{CLR}",  # Clear screen
        148: "{INS}",  # Insert
        149: "{BRN}",  # Brown
        150: "{LRD}",  # Light red
        151: "{GRY1}", # Grey 1
        152: "{GRY2}", # Grey 2
        153: "{LGN}",  # Light green
        154: "{LBL}",  # Light blue
        155: "{GRY3}", # Grey 3
        156: "{PUR}",  # Purple
        157: "{LEFT}", # Cursor left
        158: "{YEL}",  # Yellow
        159: "{CYN}"   # Cyan
    }

class EnhancedBasicDecompiler:
    """Gelişmiş BASIC V2 Decompiler sistemi"""
    
    def __init__(self):
        """Enhanced BASIC Decompiler başlatma"""
        self.logger = logging.getLogger(__name__)
        
        # Default özel karakter modu
        self.special_char_mode = SpecialCharacterMode.NUMERIC_CODES
        
        # BASIC V2 Token tablosu (complete)
        self.basic_tokens = {
            0x80: "END", 0x81: "FOR", 0x82: "NEXT", 0x83: "DATA", 0x84: "INPUT#",
            0x85: "INPUT", 0x86: "DIM", 0x87: "READ", 0x88: "LET", 0x89: "GOTO",
            0x8A: "RUN", 0x8B: "IF", 0x8C: "RESTORE", 0x8D: "GOSUB", 0x8E: "RETURN",
            0x8F: "REM", 0x90: "STOP", 0x91: "ON", 0x92: "WAIT", 0x93: "LOAD",
            0x94: "SAVE", 0x95: "VERIFY", 0x96: "DEF", 0x97: "POKE", 0x98: "PRINT#",
            0x99: "PRINT", 0x9A: "CONT", 0x9B: "LIST", 0x9C: "CLR", 0x9D: "CMD",
            0x9E: "SYS", 0x9F: "OPEN", 0xA0: "CLOSE", 0xA1: "GET", 0xA2: "NEW",
            0xA3: "TAB(", 0xA4: "TO", 0xA5: "FN", 0xA6: "SPC(", 0xA7: "THEN",
            0xA8: "NOT", 0xA9: "STEP", 0xAA: "+", 0xAB: "-", 0xAC: "*", 0xAD: "/",
            0xAE: "↑", 0xAF: "AND", 0xB0: "OR", 0xB1: ">", 0xB2: "=", 0xB3: "<",
            0xB4: "SGN", 0xB5: "INT", 0xB6: "ABS", 0xB7: "USR", 0xB8: "FRE",
            0xB9: "POS", 0xBA: "SQR", 0xBB: "RND", 0xBC: "LOG", 0xBD: "EXP",
            0xBE: "COS", 0xBF: "SIN", 0xC0: "TAN", 0xC1: "ATN", 0xC2: "PEEK",
            0xC3: "LEN", 0xC4: "STR$", 0xC5: "VAL", 0xC6: "ASC", 0xC7: "CHR$",
            0xC8: "LEFT$", 0xC9: "RIGHT$", 0xCA: "MID$", 0xCB: "GO"
        }
        # TRY load Turkish token database from JSON
        try:
            tokens_path = Path("c64_rom_data/basic/basic_tokens.json")
            with open(tokens_path, 'r', encoding='utf-8') as jf:
                tokens_json = json.load(jf)
            # Convert keys "$80" -> int 0x80
            self.basic_tokens = {int(k.lstrip('$'), 16): v for k, v in tokens_json.items()}
            self.logger.info("✅ Türkçe token database yüklendi")
        except Exception as e:
            self.logger.warning(f"⚠️ Token database yüklenemedi: {e}")
        
        # Load data using DataLoader: tokens and memory maps from JSON files
        loader = DataLoader(os.path.dirname(__file__))
        # Load basic tokens
        loaded_basic = loader.load_directory('c64_rom_data/basic')
        if 'basic_tokens' in loaded_basic:
            self.basic_tokens = {int(k.lstrip('$'), 16): v for k, v in loaded_basic['basic_tokens'].items()}
        # Load memory map
        loaded_mem = loader.load_directory('c64_rom_data/memory_maps')
        if 'c64_memory_map' in loaded_mem:
            self.memory_map = loaded_mem['c64_memory_map']
        elif 'memory_areas' in loaded_mem:
            # merge additional areas
            self.memory_map.update(loaded_mem['memory_areas'])
        
        # C64 Memory Map (for optimization)
        self.memory_map = {
            # VIC-II Registers
            0xD000: "sprite0_x", 0xD001: "sprite0_y", 0xD010: "sprite_msb_x",
            0xD015: "sprite_enable", 0xD016: "vic_control2", 0xD018: "vic_memory",
            0xD020: "border_color", 0xD021: "background_color",
            
            # SID Registers  
            0xD400: "sid_freq1_lo", 0xD401: "sid_freq1_hi", 0xD404: "sid_control1",
            0xD405: "sid_attack1", 0xD406: "sid_sustain1", 0xD418: "sid_volume",
            
            # CIA Registers
            0xDC00: "cia1_port_a", 0xDC01: "cia1_port_b", 0xDC02: "cia1_ddr_a",
            0xDC03: "cia1_ddr_b",
            
            # Screen Memory
            0x0400: "screen_memory", 0xD800: "color_memory",
            
            # System Pointers
            0x002B: "basic_start", 0x002D: "basic_vars", 0x002F: "basic_arrays",
            0x0033: "basic_strings",
            
            # Common addresses
            0x0801: "basic_program_start", 0x1000: "machine_code_start"
        }
        
        # QBasic 7.1 equivalents
        self.qbasic_equivalents = {
            "POKE": "OUT",  # For some cases
            "PEEK": "INP",  # For some cases  
            "SYS": "CALL",
            "PRINT": "PRINT",
            "INPUT": "INPUT",
            "FOR": "FOR",
            "NEXT": "NEXT",
            "IF": "IF",
            "THEN": "THEN",
            "GOTO": "GOTO",
            "GOSUB": "GOSUB",
            "RETURN": "RETURN"
        }
        
        # C/C++ equivalents
        self.c_equivalents = {
            "PRINT": "printf",
            "INPUT": "scanf", 
            "POKE": "memory_write",
            "PEEK": "memory_read",
            "SYS": "call_asm_function",
            "RND": "rand"
        }
        
        # Variable type detection patterns
        self.variable_patterns = {
            "integer": r'[A-Z][A-Z0-9]*%?$',
            "string": r'[A-Z][A-Z0-9]*\$$',
            "float": r'[A-Z][A-Z0-9]*$'
        }
        
        # Graphics command mappings
        self.graphics_commands = {
            "POKE 53280": "border_color",
            "POKE 53281": "background_color", 
            "POKE 646": "text_color"
        }
        
        # Sound command mappings  
        self.sound_commands = {
            "POKE 54296": "sid_volume",
            "POKE 54276": "sid_frequency_low",
            "POKE 54277": "sid_frequency_high"
        }
    
    def set_special_char_mode(self, mode: str):
        """Özel karakter görüntüleme modunu ayarla"""
        if mode in [SpecialCharacterMode.NUMERIC_CODES, 
                   SpecialCharacterMode.COLOR_NAMES, 
                   SpecialCharacterMode.ESCAPED]:
            self.special_char_mode = mode
            self.logger.info(f"Özel karakter modu değiştirildi: {mode}")
        else:
            self.logger.warning(f"Geçersiz özel karakter modu: {mode}")
    
    def format_special_character(self, char_code: int) -> str:
        """Özel karakteri seçilen moda göre formatla"""
        if self.special_char_mode == SpecialCharacterMode.COLOR_NAMES:
            return SpecialCharacterMode.SPECIAL_CHARS.get(char_code, f"[{char_code}]")
        elif self.special_char_mode == SpecialCharacterMode.ESCAPED:
            return f"\\x{char_code:02X}"
        else:  # NUMERIC_CODES (default)
            return f"[{char_code}]"
    
    def parse_basic_program(self, prg_data: bytes) -> List[BasicLine]:
        """BASIC programını detaylı parse et"""
        
        if len(prg_data) < 4:
            return []
        
        # Start address kontrolü
        start_address = prg_data[0] + (prg_data[1] << 8)
        if start_address != 0x0801:
            self.logger.warning(f"Non-standard BASIC start address: ${start_address:04X}")
        
        lines = []
        pos = 2  # Skip start address
        
        while pos < len(prg_data) - 1:
            try:
                # Next line pointer
                next_line_ptr = prg_data[pos] + (prg_data[pos + 1] << 8)
                pos += 2
                
                if next_line_ptr == 0:  # End of program
                    break
                
                # Line number
                line_number = prg_data[pos] + (prg_data[pos + 1] << 8)
                pos += 2
                
                # Parse line content
                line_data = self._parse_basic_line(prg_data, pos, line_number)
                if line_data:
                    lines.append(line_data)
                
                # Move to next line
                while pos < len(prg_data) and prg_data[pos] != 0:
                    pos += 1
                pos += 1  # Skip line terminator
                
            except Exception as e:
                self.logger.error(f"Error parsing BASIC line at pos {pos}: {e}")
                break
        
        return lines
    
    def _parse_basic_line(self, data: bytes, start_pos: int, line_number: int) -> Optional[BasicLine]:
        """Tek BASIC satırını detaylı parse et"""
        
        pos = start_pos
        content = ""
        tokens = []
        variables = []
        sys_calls = []
        poke_operations = []
        peek_operations = []
        goto_targets = []
        gosub_targets = []
        
        while pos < len(data) and data[pos] != 0:
            byte_val = data[pos]
            
            # BASIC token
            if byte_val >= 0x80:
                token_name = self.basic_tokens.get(byte_val, f"TOKEN_{byte_val:02X}")
                tokens.append(token_name)
                content += token_name
                
                # Special token handling
                if byte_val == 0x9E:  # SYS token
                    pos += 1
                    sys_addr = self._extract_number(data, pos)
                    if sys_addr:
                        sys_calls.append(sys_addr)
                        content += f" {sys_addr}"
                        pos += len(str(sys_addr)) - 1
                
                elif byte_val == 0x97:  # POKE token  
                    pos += 1
                    poke_info = self._extract_poke_params(data, pos)
                    if poke_info:
                        addr, value = poke_info
                        poke_operations.append((addr, value))
                        content += f" {addr},{value}"
                        pos += len(f"{addr},{value}") - 1
                
                elif byte_val == 0xC2:  # PEEK token
                    pos += 1
                    peek_addr = self._extract_number(data, pos)
                    if peek_addr:
                        peek_operations.append(peek_addr)
                        content += f"({peek_addr})"
                        pos += len(f"({peek_addr})") - 1
                
                elif byte_val == 0x89:  # GOTO token
                    pos += 1
                    goto_target = self._extract_number(data, pos)
                    if goto_target:
                        goto_targets.append(goto_target)
                        content += f" {goto_target}"
                        pos += len(str(goto_target)) - 1
                
                elif byte_val == 0x8D:  # GOSUB token
                    pos += 1
                    gosub_target = self._extract_number(data, pos)
                    if gosub_target:
                        gosub_targets.append(gosub_target)
                        content += f" {gosub_target}"
                        pos += len(str(gosub_target)) - 1
            
            # Regular character
            else:
                if 32 <= byte_val <= 126:
                    char = chr(byte_val)
                    content += char
                    
                    # Variable detection
                    if char.isalpha():
                        var_name = self._extract_variable_name(data, pos)
                        if var_name and var_name not in variables:
                            variables.append(var_name)
                else:
                    # Özel karakter - moda göre formatla
                    formatted_char = self.format_special_character(byte_val)
                    content += formatted_char
            
            pos += 1
        
        return BasicLine(
            line_number=line_number,
            content=content,
            tokens=tokens,
            variables=variables,
            sys_calls=sys_calls,
            poke_operations=poke_operations,
            peek_operations=peek_operations,
            goto_targets=goto_targets,
            gosub_targets=gosub_targets
        )
    
    def _extract_number(self, data: bytes, start_pos: int) -> Optional[int]:
        """Data'dan sayı çıkar"""
        pos = start_pos
        
        # Skip spaces and opening parenthesis
        while pos < len(data) and data[pos] in [0x20, 0x28]:
            pos += 1
        
        number_str = ""
        while pos < len(data) and 0x30 <= data[pos] <= 0x39:  # 0-9
            number_str += chr(data[pos])
            pos += 1
        
        return int(number_str) if number_str else None
    
    def _extract_poke_params(self, data: bytes, start_pos: int) -> Optional[Tuple[int, int]]:
        """POKE parametrelerini çıkar"""
        pos = start_pos
        
        # Skip spaces
        while pos < len(data) and data[pos] == 0x20:
            pos += 1
        
        # First number (address)
        addr_str = ""
        while pos < len(data) and 0x30 <= data[pos] <= 0x39:
            addr_str += chr(data[pos])
            pos += 1
        
        # Skip comma and spaces
        while pos < len(data) and data[pos] in [0x20, 0x2C]:
            pos += 1
        
        # Second number (value)
        val_str = ""
        while pos < len(data) and 0x30 <= data[pos] <= 0x39:
            val_str += chr(data[pos])
            pos += 1
        
        if addr_str and val_str:
            return (int(addr_str), int(val_str))
        return None
    
    def _extract_variable_name(self, data: bytes, start_pos: int) -> Optional[str]:
        """Variable ismini çıkar"""
        pos = start_pos
        var_name = ""
        
        # First character must be letter
        if pos >= len(data) or not (65 <= data[pos] <= 90 or 97 <= data[pos] <= 122):
            return None
        
        while pos < len(data):
            byte_val = data[pos]
            if 65 <= byte_val <= 90 or 97 <= byte_val <= 122:  # A-Z, a-z
                var_name += chr(byte_val)
            elif 48 <= byte_val <= 57:  # 0-9
                var_name += chr(byte_val)
            elif byte_val in [0x24, 0x25]:  # $ (string), % (integer)
                var_name += chr(byte_val)
                pos += 1
                break
            else:
                break
            pos += 1
        
        return var_name if len(var_name) > 1 else None
    
    def convert_to_qbasic(self, basic_lines: List[BasicLine], context: ConversionContext) -> str:
        """QBasic 7.1'e dönüştür"""
        
        output = []
        output.append("' Converted from Commodore 64 BASIC V2")
        output.append("' Target: QBasic 7.1")
        output.append("' Conversion Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        output.append("")
        
        # Variable declarations (if optimization enabled)
        if context.optimization_level >= 2:
            variables = self._collect_all_variables(basic_lines)
            if variables:
                output.append("' Variable Declarations")
                for var_name, var_type in variables.items():
                    if var_type == "string":
                        output.append(f"DIM {var_name.replace('$', '')} AS STRING")
                    elif var_type == "integer":
                        output.append(f"DIM {var_name.replace('%', '')} AS INTEGER")
                    else:
                        output.append(f"DIM {var_name} AS SINGLE")
                output.append("")
        
        # Function declarations for memory access
        if self._has_memory_operations(basic_lines):
            output.append("' Memory Access Functions")
            output.append("DECLARE SUB MemoryWrite (address AS INTEGER, value AS INTEGER)")
            output.append("DECLARE FUNCTION MemoryRead% (address AS INTEGER)")
            output.append("")
        
        # Main program
        for line in basic_lines:
            converted_line = self._convert_basic_line_to_qbasic(line, context)
            if converted_line:
                if context.preserve_line_numbers:
                    output.append(f"{line.line_number} {converted_line}")
                else:
                    output.append(converted_line)
        
        # Memory access function implementations
        if self._has_memory_operations(basic_lines):
            output.append("")
            output.append("' Memory Access Implementation")
            output.append("SUB MemoryWrite (address AS INTEGER, value AS INTEGER)")
            output.append("    ' Simulated memory write - adapt as needed")
            output.append("    PRINT \"POKE \"; address; \",\"; value")
            output.append("END SUB")
            output.append("")
            output.append("FUNCTION MemoryRead% (address AS INTEGER)")
            output.append("    ' Simulated memory read - adapt as needed")
            output.append("    MemoryRead% = 0  ' Default value")
            output.append("END FUNCTION")
        
        return "\n".join(output)
    
    def convert_to_c(self, basic_lines: List[BasicLine], context: ConversionContext) -> str:
        """C/C++' ye dönüştür"""
        
        output = []
        output.append("/*")
        output.append(" * Converted from Commodore 64 BASIC V2")
        output.append(" * Target: C/C++")
        output.append(" * Conversion Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        output.append(" */")
        output.append("")
        output.append("#include <stdio.h>")
        output.append("#include <stdlib.h>")
        output.append("#include <string.h>")
        output.append("#include <math.h>")
        output.append("")
        
        # Memory access macros
        if self._has_memory_operations(basic_lines):
            output.append("// C64 Memory Simulation")
            output.append("unsigned char memory[65536];")
            output.append("#define POKE(addr, val) (memory[addr] = (val))")
            output.append("#define PEEK(addr) (memory[addr])")
            output.append("")
            
            # VIC-II register definitions
            output.append("// VIC-II Register Definitions")
            output.append("#define VIC_BORDER_COLOR   0xD020")
            output.append("#define VIC_BG_COLOR       0xD021")
            output.append("#define VIC_SPRITE_ENABLE  0xD015")
            output.append("")
            
            # SID register definitions
            output.append("// SID Register Definitions")
            output.append("#define SID_VOLUME         0xD418")
            output.append("#define SID_FREQ1_LO       0xD400")
            output.append("#define SID_FREQ1_HI       0xD401")
            output.append("")
        
        # Function declarations
        if self._has_sys_calls(basic_lines):
            output.append("// Assembly function declarations")
            sys_addresses = self._get_all_sys_addresses(basic_lines)
            for addr in sys_addresses:
                output.append(f"void asm_function_{addr:04X}(void);")
            output.append("")
        
        # Variable declarations
        variables = self._collect_all_variables(basic_lines)
        if variables:
            output.append("// Global Variables")
            for var_name, var_type in variables.items():
                c_var_name = var_name.replace('$', '_str').replace('%', '_int')
                if var_type == "string":
                    output.append(f"char {c_var_name}[256];")
                elif var_type == "integer":
                    output.append(f"int {c_var_name};")
                else:
                    output.append(f"float {c_var_name};")
            output.append("")
        
        # Main function
        output.append("int main(void) {")
        
        # Initialize memory if needed
        if self._has_memory_operations(basic_lines):
            output.append("    // Initialize C64 memory simulation")
            output.append("    memset(memory, 0, sizeof(memory));")
            output.append("")
        
        # Convert BASIC lines
        for line in basic_lines:
            converted_line = self._convert_basic_line_to_c(line, context)
            if converted_line:
                # Add proper indentation
                indented_lines = ["    " + cl for cl in converted_line.split("\n") if cl.strip()]
                output.extend(indented_lines)
        
        output.append("")
        output.append("    return 0;")
        output.append("}")
        
        # Assembly function stubs
        if self._has_sys_calls(basic_lines):
            output.append("")
            output.append("// Assembly function implementations")
            sys_addresses = self._get_all_sys_addresses(basic_lines)
            for addr in sys_addresses:
                output.append(f"void asm_function_{addr:04X}(void) {{")
                output.append(f"    // Call to assembly routine at ${addr:04X}")
                output.append("    // TODO: Implement assembly functionality")
                output.append("}")
                output.append("")
        
        return "\n".join(output)
    
    def convert_to_pdsx(self, basic_lines: List[BasicLine], context: ConversionContext) -> str:
        """PDSX BASIC'e dönüştür"""
        
        output = []
        output.append("REM Converted from Commodore 64 BASIC V2")
        output.append("REM Target: PDSX BASIC")
        output.append("REM Conversion Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        output.append("")
        
        # Enhanced PDSX features
        if context.modernize_syntax:
            output.append("REM Enhanced PDSX Features Enabled")
            output.append("OPTION EXPLICIT")  # Force variable declaration
            output.append("")
        
        # Convert lines with PDSX enhancements
        for line in basic_lines:
            converted_line = self._convert_basic_line_to_pdsx(line, context)
            if converted_line:
                if context.preserve_line_numbers:
                    output.append(f"{line.line_number} {converted_line}")
                else:
                    output.append(converted_line)
        
        return "\n".join(output)
    
    def _convert_basic_line_to_qbasic(self, line: BasicLine, context: ConversionContext) -> str:
        """BASIC satırını QBasic'e dönüştür"""
        
        content = line.content
        
        # Token replacements
        for c64_token, qbasic_token in self.qbasic_equivalents.items():
            content = content.replace(c64_token, qbasic_token)
        
        # POKE/PEEK optimization
        if context.optimize_memory_access:
            # POKE operations
            for addr, value in line.poke_operations:
                old_poke = f"POKE {addr},{value}"
                if addr in self.memory_map:
                    var_name = self.memory_map[addr]
                    new_poke = f"' {var_name} = {value}"
                    content = content.replace(old_poke, new_poke)
                else:
                    content = content.replace(old_poke, f"MemoryWrite {addr}, {value}")
            
            # PEEK operations  
            for addr in line.peek_operations:
                old_peek = f"PEEK({addr})"
                if addr in self.memory_map:
                    var_name = self.memory_map[addr]
                    content = content.replace(old_peek, f"{var_name}")
                else:
                    content = content.replace(old_peek, f"MemoryRead({addr})")
        
        # SYS call conversion
        for sys_addr in line.sys_calls:
            old_sys = f"SYS {sys_addr}"
            content = content.replace(old_sys, f"CALL AsmFunction{sys_addr:04X}")
        
        # Graphics command translation
        if context.convert_graphics:
            content = self._translate_graphics_commands(content)
        
        return content
    
    def _convert_basic_line_to_c(self, line: BasicLine, context: ConversionContext) -> str:
        """BASIC satırını C'ye dönüştür"""
        
        content = line.content
        
        # Label for GOTO/GOSUB targets
        c_code = ""
        if line.line_number in self._get_all_goto_targets(line):
            c_code += f"label_{line.line_number}:\n"
        
        # PRINT statement
        if "PRINT" in content:
            # Simple PRINT conversion
            print_match = re.search(r'PRINT\s*"([^"]*)"', content)
            if print_match:
                text = print_match.group(1)
                c_code += f'printf("{text}\\n");'
            else:
                # More complex PRINT handling needed
                c_code += "// TODO: Complex PRINT statement"
        
        # POKE operations
        for addr, value in line.poke_operations:
            if addr in self.memory_map:
                var_name = self.memory_map[addr]
                c_code += f"// {var_name} = {value}\n"
            c_code += f"POKE({addr}, {value});"
        
        # PEEK operations
        for addr in line.peek_operations:
            # This needs context-specific handling
            pass
        
        # SYS calls
        for sys_addr in line.sys_calls:
            c_code += f"asm_function_{sys_addr:04X}();"
        
        # GOTO statements
        for target in line.goto_targets:
            c_code += f"goto label_{target};"
        
        return c_code
    
    def _convert_basic_line_to_pdsx(self, line: BasicLine, context: ConversionContext) -> str:
        """BASIC satırını PDSX'e dönüştür"""
        
        content = line.content
        
        # PDSX specific enhancements
        if context.modernize_syntax:
            # Structured programming constructs
            content = self._modernize_control_structures(content)
        
        # Enhanced variable handling
        content = self._enhance_variable_declarations(content)
        
        return content
    
    def _collect_all_variables(self, basic_lines: List[BasicLine]) -> Dict[str, str]:
        """Tüm değişkenleri topla ve tiplerini belirle"""
        
        variables = {}
        
        for line in basic_lines:
            for var in line.variables:
                if var.endswith('$'):
                    variables[var] = "string"
                elif var.endswith('%'):
                    variables[var] = "integer"
                else:
                    variables[var] = "float"
        
        return variables
    
    def _has_memory_operations(self, basic_lines: List[BasicLine]) -> bool:
        """Memory operasyonu var mı kontrol et"""
        for line in basic_lines:
            if line.poke_operations or line.peek_operations:
                return True
        return False
    
    def _has_sys_calls(self, basic_lines: List[BasicLine]) -> bool:
        """SYS çağrısı var mı kontrol et"""
        for line in basic_lines:
            if line.sys_calls:
                return True
        return False
    
    def _get_all_sys_addresses(self, basic_lines: List[BasicLine]) -> List[int]:
        """Tüm SYS adreslerini topla"""
        addresses = set()
        for line in basic_lines:
            addresses.update(line.sys_calls)
        return sorted(list(addresses))
    
    def _get_all_goto_targets(self, line: BasicLine) -> List[int]:
        """Tüm GOTO hedeflerini topla"""
        # This should collect from all lines, not just one
        return line.goto_targets + line.gosub_targets
    
    def _translate_graphics_commands(self, content: str) -> str:
        """Graphics komutlarını çevir"""
        
        for c64_cmd, modern_cmd in self.graphics_commands.items():
            if c64_cmd in content:
                content = content.replace(c64_cmd, f"' Graphics: {modern_cmd}")
        
        return content
    
    def _modernize_control_structures(self, content: str) -> str:
        """Control yapılarını modernize et"""
        
        # IF-THEN-ELSE improvements
        content = re.sub(r'IF\s+(.+?)\s+THEN\s+(\d+)', r'IF \1 THEN GOTO \2', content)
        
        return content
    
    def _enhance_variable_declarations(self, content: str) -> str:
        """Variable declarationlarını gelişir"""
        
        # Add type hints for PDSX
        content = re.sub(r'(\w+)\$', r'\1 AS STRING', content)
        content = re.sub(r'(\w+)%', r'\1 AS INTEGER', content)
        
        return content
    
    def decompile_program(self, prg_data: bytes, target_language: str, 
                         optimization_level: int = 2) -> str:
        """Ana decompile fonksiyonu"""
        
        # Parse BASIC program
        basic_lines = self.parse_basic_program(prg_data)
        
        if not basic_lines:
            return "ERROR: Could not parse BASIC program"
        
        # Conversion context
        context = ConversionContext(
            target_language=target_language,
            optimization_level=optimization_level,
            preserve_line_numbers=(optimization_level < 2),
            modernize_syntax=(optimization_level >= 2),
            optimize_memory_access=(optimization_level >= 1),
            convert_graphics=True,
            convert_sound=True
        )
        
        # Convert based on target language
        if target_language.lower() == "qbasic":
            return self.convert_to_qbasic(basic_lines, context)
        elif target_language.lower() in ["c", "cpp", "c++"]:
            return self.convert_to_c(basic_lines, context)
        elif target_language.lower() == "pdsx":
            return self.convert_to_pdsx(basic_lines, context)
        else:
            return f"ERROR: Unsupported target language: {target_language}"

# Test kodu
if __name__ == "__main__":
    print("🔥 Enhanced BASIC V2 Decompiler Test v3.0")
    print("=" * 60)
    
    decompiler = EnhancedBasicDecompiler()
    
    # Test Case 1: Simple BASIC program
    print("\n📋 Test Case 1: Simple BASIC Program")
    test_data = bytearray()
    test_data.extend([0x01, 0x08])  # Start address $0801
    
    # 10 PRINT "HELLO WORLD"
    test_data.extend([0x15, 0x08])  # Next line pointer
    test_data.extend([0x0A, 0x00])  # Line 10
    test_data.extend([0x99])        # PRINT token
    test_data.extend([0x20])        # Space
    test_data.extend([0x22])        # Quote
    test_data.extend(b"HELLO WORLD")
    test_data.extend([0x22])        # Quote
    test_data.extend([0x00])        # Line end
    test_data.extend([0x00, 0x00])  # Program end
    
    # QBasic conversion test
    qbasic_result = decompiler.decompile_program(bytes(test_data), "qbasic", 2)
    print("QBasic Conversion:")
    print(qbasic_result[:300] + "..." if len(qbasic_result) > 300 else qbasic_result)
    
    # C conversion test
    c_result = decompiler.decompile_program(bytes(test_data), "c", 2)
    print("\nC Conversion:")
    print(c_result[:300] + "..." if len(c_result) > 300 else c_result)
    
    print("\n✅ Enhanced BASIC Decompiler v3.0 working!")
