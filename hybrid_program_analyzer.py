"""
� D64 Converter - Hybrid Program Analyzer v2.0
===========================================
BASIC+Assembly hibrit programların gelişmiş analizi

ÖZELLIKLER:
1. BASIC program boyut hesaplama ve analiz
2. SYS çağrıları tespiti ve adres analizi  
3. POKE/PEEK memory mapping analizi
4. Hibrit program tip belirleme
5. Assembly başlangıç adres hesaplama
6. Disk directory analizi ve dosya tipi tespiti
7. Memory map tabanlı değişken isimlendirme
8. C64 Memory Map entegrasyonu
9. BASIC V2 Token parsing
10. Variable renaming suggestions

Author: D64 Converter Team
Version: 2.0 - Enhanced Hybrid Analysis
"""

import struct
import re
from typing import Dict, List, Optional, Tuple, Any
import logging

class HybridProgramAnalyzer:
    """Gelişmiş hibrit program analiz sistemi"""
    
    def __init__(self, memory_manager=None):
        """
        HybridProgramAnalyzer başlatma
        
        Args:
            memory_manager: C64MemoryMapManager instance
        """
        self.memory_manager = memory_manager
        self.logger = logging.getLogger(__name__)
        
        # BASIC V2 Token tablosu (tüm tokenlar)
        self.basic_tokens = {
            0x80: "END", 0x81: "FOR", 0x82: "NEXT", 0x83: "DATA", 0x84: "INPUT",
            0x85: "DIM", 0x86: "READ", 0x87: "LET", 0x88: "GOTO", 0x89: "RUN",
            0x8A: "IF", 0x8B: "RESTORE", 0x8C: "GOSUB", 0x8D: "RETURN", 0x8E: "REM",
            0x8F: "STOP", 0x90: "ON", 0x91: "WAIT", 0x92: "LOAD", 0x93: "SAVE",
            0x94: "VERIFY", 0x95: "DEF", 0x96: "POKE", 0x97: "PRINT", 0x98: "CONT",
            0x99: "LIST", 0x9A: "CLR", 0x9B: "CMD", 0x9C: "SYS", 0x9D: "OPEN",
            0x9E: "CLOSE", 0x9F: "GET", 0xA0: "NEW", 0xA1: "TAB(", 0xA2: "TO",
            0xA3: "FN", 0xA4: "SPC(", 0xA5: "THEN", 0xA6: "NOT", 0xA7: "STEP",
            0xA8: "+", 0xA9: "-", 0xAA: "*", 0xAB: "/", 0xAC: "^", 0xAD: "AND",
            0xAE: "OR", 0xAF: ">", 0xB0: "=", 0xB1: "<", 0xB2: "SGN", 0xB3: "INT",
            0xB4: "ABS", 0xB5: "USR", 0xB6: "FRE", 0xB7: "POS", 0xB8: "SQR",
            0xB9: "RND", 0xBA: "LOG", 0xBB: "EXP", 0xBC: "COS", 0xBD: "SIN",
            0xBE: "TAN", 0xBF: "ATN", 0xC0: "PEEK", 0xC1: "LEN", 0xC2: "STR$",
            0xC3: "VAL", 0xC4: "ASC", 0xC5: "CHR$", 0xC6: "LEFT$", 0xC7: "RIGHT$",
            0xC8: "MID$", 0xC9: "GO"
        }
        
        # C64 Memory Map (critical addresses)
        self.memory_map = {
            # Zero Page - Program pointers
            0x002B: "TXTTAB",    # BASIC program start
            0x002D: "VARTAB",    # BASIC variables start  
            0x002F: "ARYTAB",    # BASIC arrays start
            0x0031: "STREND",    # End of BASIC arrays
            0x0033: "FRETOP",    # Start of string variables
            0x0037: "FRESPC",    # Temporary string pointer
            
            # Screen and Color Memory
            0x0400: "SCREEN",    # Screen memory start
            0x07E8: "SCREEN_END", # Screen memory end
            0xD800: "COLOR_RAM", # Color memory start
            
            # VIC-II Registers
            0xD000: "VIC_SPR0_X", # Sprite 0 X position
            0xD001: "VIC_SPR0_Y", # Sprite 0 Y position
            0xD010: "VIC_SPR_HI_X", # Sprites X MSB
            0xD015: "VIC_SPR_ENA", # Sprite enable
            0xD016: "VIC_CR2",   # Control register 2
            0xD018: "VIC_MEMPTR", # Memory pointers
            0xD020: "VIC_BORDER", # Border color
            0xD021: "VIC_BG0",   # Background color 0
            
            # SID Registers
            0xD400: "SID_FREQ1_LO", # Voice 1 frequency low
            0xD401: "SID_FREQ1_HI", # Voice 1 frequency high
            0xD404: "SID_CTRL1",    # Voice 1 control
            0xD418: "SID_VOLUME",   # Volume and filter
            
            # CIA Registers
            0xDC00: "CIA1_PRA",  # Port A data register
            0xDC01: "CIA1_PRB",  # Port B data register
            0xDC02: "CIA1_DDRA", # Port A direction
            0xDC03: "CIA1_DDRB", # Port B direction
            
            # BASIC ROM addresses
            0xA000: "BASIC_ROM", # BASIC ROM start
            0xE000: "KERNAL_ROM", # KERNAL ROM start
            
            # Common program locations
            0x0801: "BASIC_START", # Standard BASIC start
            0x1000: "COMMON_ML",   # Common machine language start
            0x8000: "CARTRIDGE",   # Cartridge area
            0xC000: "RAM_AREA"     # High RAM area
        }
        
        # Dosya tipleri (D64 directory)
        self.file_types = {
            0x00: "DEL",  # Deleted
            0x01: "SEQ",  # Sequential  
            0x02: "PRG",  # Program
            0x03: "USR",  # User
            0x04: "REL",  # Relative
            0x05: "CBM"   # CBM
        }
        
        # SYS çağrı pattern'leri
        self.sys_patterns = [
            r'SYS\s*(\d+)',           # SYS 2064
            r'SYS\s*\(\s*(\d+)\s*\)', # SYS(2064)
            r'SYS\s*([A-Z]+)',        # SYS VARIABLE
            r'SYS\s*(\d+\s*[\+\-]\s*\d+)', # SYS 2064+5
        ]
    
    def analyze_prg_data(self, prg_data: bytes) -> Dict[str, Any]:
        """PRG verilerini gelişmiş hibrit analiz"""
        
        if len(prg_data) < 4:
            return {"error": "Invalid PRG data", "is_hybrid": False}
        
        # Başlangıç adresi
        start_address = prg_data[0] + (prg_data[1] << 8)
        actual_data = prg_data[2:]
        
        result = {
            "start_address": start_address,
            "start_address_hex": f"${start_address:04X}",
            "total_file_size": len(prg_data),
            "data_size": len(actual_data),
            "estimated_end_address": start_address + len(actual_data),
            "is_basic_program": start_address == 0x0801,
            "is_hybrid": False,
            "program_type": "UNKNOWN",
            "basic_info": {},
            "assembly_info": {},
            "sys_calls": [],
            "poke_operations": [],
            "peek_operations": [],
            "memory_usage": [],
            "hybrid_analysis": {},
            "disassembly_plan": {},
            "variable_suggestions": []
        }
        
        if start_address == 0x0801:
            # BASIC program analizi
            basic_analysis = self.analyze_basic_code(actual_data)
            result["basic_info"] = basic_analysis
            
            # Hibrit kontrol - Enhanced detection
            if basic_analysis.get("basic_calculated_size", 0) > 0:
                basic_end = start_address + basic_analysis["basic_calculated_size"]
                file_end = start_address + len(actual_data)
                remaining_bytes = file_end - basic_end
                
                # Debug info
                if self.logger:
                    self.logger.debug(f"Hybrid check: BASIC_end=${basic_end:04X}, File_end=${file_end:04X}, Remaining={remaining_bytes} bytes")
                
                # Daha hassas hibrit tespit
                if remaining_bytes > 5:  # En az 5 byte kalan kod olmalı
                    result["is_hybrid"] = True
                    result["program_type"] = "HYBRID"
                    result["assembly_info"] = {
                        "assembly_start": basic_end,
                        "assembly_start_hex": f"${basic_end:04X}",
                        "assembly_size": remaining_bytes,
                        "assembly_end": file_end,
                        "assembly_end_hex": f"${file_end:04X}"
                    }
                    result["hybrid_analysis"] = self.analyze_hybrid_structure(basic_analysis, result["assembly_info"])
                else:
                    result["program_type"] = "BASIC"
            else:
                result["program_type"] = "BASIC"
                
            # SYS çağrıları, POKE/PEEK analizi
            result["sys_calls"] = basic_analysis.get("sys_calls", [])
            result["poke_operations"] = basic_analysis.get("poke_operations", [])
            result["peek_operations"] = basic_analysis.get("peek_operations", [])
            
        elif start_address >= 0x1000:
            # Pure assembly/machine language
            result["program_type"] = "ASSEMBLY"
            result["assembly_info"] = {
                "assembly_start": start_address,
                "assembly_start_hex": f"${start_address:04X}",
                "assembly_size": len(actual_data),
                "assembly_end": start_address + len(actual_data),
                "assembly_end_hex": f"${start_address + len(actual_data):04X}"
            }
        else:
            # Diğer lokasyonlar
            result["program_type"] = "OTHER"
        
        # Memory usage analizi
        result["memory_usage"] = self.analyze_memory_usage(result)
        
        # Variable naming suggestions
        result["variable_suggestions"] = self.generate_variable_suggestions(result)
        
        # Disassembly planı oluştur
        result["disassembly_plan"] = self.generate_disassembly_plan(result)
        
        return result
    
    def analyze_basic_code(self, data: bytes) -> Dict[str, Any]:
        """Gelişmiş BASIC kodu analizi"""
        
        analysis = {
            "basic_lines": [],
            "sys_calls": [],
            "poke_operations": [],
            "peek_operations": [],
            "goto_targets": [],
            "basic_calculated_size": 0,
            "line_count": 0,
            "has_sys_calls": False,
            "memory_operations": [],
            "variables": [],
            "screen_codes": [],
            "color_operations": []
        }
        
        try:
            pos = 0
            current_address = 0x0801
            
            while pos < len(data) - 1:
                # Next line pointer (2 bytes, little-endian)
                if pos + 1 >= len(data):
                    break
                    
                next_line_ptr = data[pos] + (data[pos + 1] << 8)
                pos += 2
                
                # BASIC programının sonu
                if next_line_ptr == 0:
                    analysis["basic_calculated_size"] = pos
                    break
                
                # Line number (2 bytes, little-endian)
                if pos + 1 >= len(data):
                    break
                    
                line_number = data[pos] + (data[pos + 1] << 8)
                pos += 2
                
                # Line content parsing
                line_start_pos = pos
                line_tokens = []
                line_text = ""
                
                while pos < len(data) and data[pos] != 0:
                    byte_val = data[pos]
                    
                    if byte_val >= 0x80:  # BASIC token
                        token_name = self.basic_tokens.get(byte_val, f"TOKEN_{byte_val:02X}")
                        line_tokens.append(token_name)
                        line_text += token_name
                        
                        # Özel token işlemleri
                        if byte_val == 0x9C:  # SYS token
                            sys_info = self.extract_sys_call_info(data, pos + 1)
                            if sys_info:
                                analysis["sys_calls"].append({
                                    "line_number": line_number,
                                    "address": sys_info["address"],
                                    "address_hex": f"${sys_info['address']:04X}",
                                    "raw_text": sys_info["raw_text"],
                                    "calculation": sys_info.get("calculation", "")
                                })
                                analysis["has_sys_calls"] = True
                        
                        elif byte_val == 0x96:  # POKE token
                            poke_info = self.extract_poke_info(data, pos + 1)
                            if poke_info:
                                analysis["poke_operations"].append({
                                    "line_number": line_number,
                                    "address": poke_info["address"],
                                    "value": poke_info["value"],
                                    "address_hex": f"${poke_info['address']:04X}",
                                    "memory_name": self.get_memory_name(poke_info["address"]),
                                    "raw_text": poke_info["raw_text"]
                                })
                        
                        elif byte_val == 0xC0:  # PEEK token
                            peek_info = self.extract_peek_info(data, pos + 1)
                            if peek_info:
                                analysis["peek_operations"].append({
                                    "line_number": line_number,
                                    "address": peek_info["address"],
                                    "address_hex": f"${peek_info['address']:04X}",
                                    "memory_name": self.get_memory_name(peek_info["address"]),
                                    "raw_text": peek_info["raw_text"]
                                })
                    
                    else:
                        # Regular character
                        if 32 <= byte_val <= 126:  # Printable ASCII
                            line_text += chr(byte_val)
                        else:
                            line_text += f"[{byte_val:02X}]"
                    
                    pos += 1
                
                # Line terminator (0x00)
                if pos < len(data):
                    pos += 1
                
                # Line bilgilerini kaydet
                analysis["basic_lines"].append({
                    "line_number": line_number,
                    "content": line_text,
                    "tokens": line_tokens,
                    "address": current_address,
                    "size": pos - line_start_pos + 4  # +4 for next_line_ptr and line_number
                })
                
                analysis["line_count"] += 1
                current_address = next_line_ptr
            
            # BASIC boyutu hesaplanmadıysa
            if analysis["basic_calculated_size"] == 0:
                analysis["basic_calculated_size"] = pos
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"BASIC parsing error: {e}")
        
        return analysis
    
    def extract_sys_call_info(self, data: bytes, start_pos: int) -> Optional[Dict]:
        """SYS çağrısından detaylı bilgi çıkar"""
        try:
            pos = start_pos
            # Space ve parantezleri atla
            while pos < len(data) and data[pos] in [0x20, 0x28]:  # space, (
                pos += 1
            
            # Number string oku
            number_text = ""
            calculation_text = ""
            raw_start = pos
            
            while pos < len(data) and data[pos] != 0x00 and data[pos] not in [0x3A, 0x0D]:  # : or CR
                if 0x30 <= data[pos] <= 0x39:  # 0-9
                    number_text += chr(data[pos])
                elif data[pos] in [0x2B, 0x2D]:  # + or -
                    calculation_text += chr(data[pos])
                elif data[pos] == 0x20:  # space
                    if number_text and calculation_text:
                        calculation_text += chr(data[pos])
                elif 0x30 <= data[pos] <= 0x39 and calculation_text:  # number after operation
                    calculation_text += chr(data[pos])
                
                pos += 1
            
            if number_text:
                base_addr = int(number_text)
                final_addr = base_addr
                
                # Hesaplama varsa
                if calculation_text:
                    try:
                        # Basit +/- hesaplama
                        if '+' in calculation_text:
                            parts = calculation_text.split('+')
                            if len(parts) == 2 and parts[1].strip().isdigit():
                                final_addr = base_addr + int(parts[1].strip())
                        elif '-' in calculation_text:
                            parts = calculation_text.split('-')
                            if len(parts) == 2 and parts[1].strip().isdigit():
                                final_addr = base_addr - int(parts[1].strip())
                    except:
                        pass
                
                return {
                    "address": final_addr,
                    "base_address": base_addr,
                    "calculation": calculation_text,
                    "raw_text": number_text + calculation_text
                }
        except:
            pass
        return None
    
    def extract_poke_info(self, data: bytes, start_pos: int) -> Optional[Dict]:
        """POKE komutundan adres ve değer çıkar"""
        try:
            pos = start_pos
            # POKE address,value formatı
            
            # Address kısmı
            while pos < len(data) and data[pos] == 0x20:  # space
                pos += 1
            
            addr_text = ""
            while pos < len(data) and 0x30 <= data[pos] <= 0x39:  # 0-9
                addr_text += chr(data[pos])
                pos += 1
            
            # Comma
            while pos < len(data) and data[pos] in [0x20, 0x2C]:  # space, comma
                pos += 1
            
            # Value kısmı
            value_text = ""
            while pos < len(data) and 0x30 <= data[pos] <= 0x39:  # 0-9
                value_text += chr(data[pos])
                pos += 1
            
            if addr_text and value_text:
                return {
                    "address": int(addr_text),
                    "value": int(value_text),
                    "raw_text": f"{addr_text},{value_text}"
                }
        except:
            pass
        return None
    
    def extract_peek_info(self, data: bytes, start_pos: int) -> Optional[Dict]:
        """PEEK komutundan adres çıkar"""
        try:
            pos = start_pos
            # PEEK(address) formatı
            
            # Parantez ve space
            while pos < len(data) and data[pos] in [0x20, 0x28]:  # space, (
                pos += 1
            
            addr_text = ""
            while pos < len(data) and 0x30 <= data[pos] <= 0x39:  # 0-9
                addr_text += chr(data[pos])
                pos += 1
            
            if addr_text:
                return {
                    "address": int(addr_text),
                    "raw_text": addr_text
                }
        except:
            pass
        return None
    
    def get_memory_name(self, address: int) -> str:
        """Memory adresinin ismini döndür"""
        # Exact match kontrolü
        if address in self.memory_map:
            return self.memory_map[address]
        
        # Range kontrolü
        if 0x0400 <= address <= 0x07E7:
            return f"SCREEN+{address-0x0400}"
        elif 0xD800 <= address <= 0xDBE7:
            return f"COLOR_RAM+{address-0xD800}"
        elif 0xD000 <= address <= 0xD3FF:
            return f"VIC_II+{address-0xD000:02X}"
        elif 0xD400 <= address <= 0xD7FF:
            return f"SID+{address-0xD400:02X}"
        elif 0xDC00 <= address <= 0xDCFF:
            return f"CIA1+{address-0xDC00:02X}"
        elif 0xDD00 <= address <= 0xDDFF:
            return f"CIA2+{address-0xDD00:02X}"
        elif 0xA000 <= address <= 0xBFFF:
            return f"BASIC_ROM+{address-0xA000:04X}"
        elif 0xE000 <= address <= 0xFFFF:
            return f"KERNAL_ROM+{address-0xE000:04X}"
        else:
            return f"MEMORY_{address:04X}"
    
    def analyze_hybrid_structure(self, basic_info: Dict, assembly_info: Dict) -> Dict[str, Any]:
        """Hibrit program yapısını analiz et"""
        
        hybrid_analysis = {
            "structure_type": "BASIC_THEN_ASSEMBLY",
            "basic_portion": {
                "size": basic_info.get("basic_calculated_size", 0),
                "line_count": basic_info.get("line_count", 0),
                "has_sys_calls": basic_info.get("has_sys_calls", False),
                "sys_call_count": len(basic_info.get("sys_calls", []))
            },
            "assembly_portion": {
                "start_address": assembly_info.get("assembly_start"),
                "size": assembly_info.get("assembly_size", 0),
                "start_address_hex": assembly_info.get("assembly_start_hex")
            },
            "connection_analysis": {},
            "recommendations": []
        }
        
        # SYS çağrıları analizi
        sys_calls = basic_info.get("sys_calls", [])
        assembly_start = assembly_info.get("assembly_start")
        
        for sys_call in sys_calls:
            sys_addr = sys_call["address"]
            if assembly_start and abs(sys_addr - assembly_start) <= 100:
                hybrid_analysis["connection_analysis"]["sys_calls_to_assembly"] = True
                hybrid_analysis["recommendations"].append(
                    f"SYS {sys_addr} likely calls assembly code at ${assembly_start:04X}"
                )
        
        # POKE 44,45 analizi
        poke_ops = basic_info.get("poke_operations", [])
        for poke in poke_ops:
            if poke["address"] in [44, 45]:
                hybrid_analysis["connection_analysis"]["modifies_basic_pointers"] = True
                hybrid_analysis["recommendations"].append(
                    f"POKE {poke['address']},{poke['value']} modifies BASIC memory pointers"
                )
        
        return hybrid_analysis
    
    def analyze_memory_usage(self, program_analysis: Dict) -> List[Dict[str, Any]]:
        """Memory kullanım analizi"""
        memory_usage = []
        
        # POKE operations
        for poke in program_analysis.get("poke_operations", []):
            memory_usage.append({
                "type": "POKE",
                "address": poke["address"],
                "address_hex": poke["address_hex"],
                "memory_name": poke["memory_name"],
                "value": poke["value"],
                "line_number": poke["line_number"],
                "description": f"Writes {poke['value']} to {poke['memory_name']}"
            })
        
        # PEEK operations
        for peek in program_analysis.get("peek_operations", []):
            memory_usage.append({
                "type": "PEEK",
                "address": peek["address"],
                "address_hex": peek["address_hex"],
                "memory_name": peek["memory_name"],
                "line_number": peek["line_number"],
                "description": f"Reads from {peek['memory_name']}"
            })
        
        return memory_usage
    
    def generate_variable_suggestions(self, program_analysis: Dict) -> List[Dict[str, str]]:
        """Variable isimlendirme önerileri"""
        suggestions = []
        
        # POKE/PEEK adreslerine göre değişken önerileri
        for poke in program_analysis.get("poke_operations", []):
            addr = poke["address"]
            memory_name = poke["memory_name"]
            
            # Screen memory
            if 0x0400 <= addr <= 0x07E7:
                screen_pos = addr - 0x0400
                row = screen_pos // 40
                col = screen_pos % 40
                suggestions.append({
                    "address": f"${addr:04X}",
                    "original_name": memory_name,
                    "suggested_variable": f"screen_char_r{row}_c{col}",
                    "description": f"Screen character at row {row}, column {col}"
                })
            
            # Color memory
            elif 0xD800 <= addr <= 0xDBE7:
                color_pos = addr - 0xD800
                row = color_pos // 40
                col = color_pos % 40
                suggestions.append({
                    "address": f"${addr:04X}",
                    "original_name": memory_name,
                    "suggested_variable": f"color_r{row}_c{col}",
                    "description": f"Color memory at row {row}, column {col}"
                })
            
            # VIC-II registers
            elif 0xD000 <= addr <= 0xD3FF:
                suggestions.append({
                    "address": f"${addr:04X}",
                    "original_name": memory_name,
                    "suggested_variable": f"vic_{memory_name.lower()}",
                    "description": f"VIC-II register: {memory_name}"
                })
            
            # SID registers
            elif 0xD400 <= addr <= 0xD7FF:
                suggestions.append({
                    "address": f"${addr:04X}",
                    "original_name": memory_name,
                    "suggested_variable": f"sid_{memory_name.lower()}",
                    "description": f"SID register: {memory_name}"
                })
        
        return suggestions
    
    def generate_disassembly_plan(self, program_analysis: Dict) -> Dict[str, Any]:
        """Disassembly planı oluştur"""
        
        plan = {
            "program_type": program_analysis.get("program_type", "UNKNOWN"),
            "tasks": [],
            "recommendations": [],
            "priority_order": []
        }
        
        prog_type = program_analysis.get("program_type")
        
        if prog_type == "BASIC":
            plan["tasks"].append({
                "type": "BASIC_DECOMPILE",
                "description": "Convert BASIC V2 to modern languages",
                "input": {
                    "start_address": program_analysis.get("start_address"),
                    "size": program_analysis.get("data_size")
                },
                "outputs": ["QBasic 7.1", "C", "C++", "PDSX Basic", "Modern BASIC"],
                "priority": "HIGH"
            })
            
            plan["recommendations"].append("Focus on POKE/PEEK optimization in target language")
            plan["recommendations"].append("Convert SYS calls to function calls where possible")
            
        elif prog_type == "ASSEMBLY":
            asm_info = program_analysis.get("assembly_info", {})
            plan["tasks"].append({
                "type": "ASSEMBLY_DISASSEMBLY",
                "description": "Disassemble 6502 machine code",
                "input": {
                    "start_address": asm_info.get("assembly_start"),
                    "size": asm_info.get("assembly_size")
                },
                "outputs": ["Assembly (ACME)", "Assembly (KickAss)", "Assembly (DASM)", "C", "Pseudo-code"],
                "priority": "HIGH"
            })
            
        elif prog_type == "HYBRID":
            # BASIC kısmı
            plan["tasks"].append({
                "type": "BASIC_DECOMPILE",
                "description": "Convert BASIC portion of hybrid program",
                "input": {
                    "start_address": program_analysis.get("start_address"),
                    "size": program_analysis["basic_info"].get("basic_calculated_size")
                },
                "outputs": ["QBasic 7.1", "C", "PDSX Basic"],
                "priority": "HIGH"
            })
            
            # Assembly kısmı
            asm_info = program_analysis.get("assembly_info", {})
            if asm_info:
                plan["tasks"].append({
                    "type": "ASSEMBLY_DISASSEMBLY",
                    "description": "Disassemble assembly portion of hybrid program",
                    "input": {
                        "start_address": asm_info.get("assembly_start"),
                        "size": asm_info.get("assembly_size")
                    },
                    "outputs": ["Assembly (Multiple formats)", "C", "Pseudo-code"],
                    "priority": "HIGH"
                })
            
            plan["recommendations"].append("Hybrid program: Process BASIC and Assembly separately")
            plan["recommendations"].append("Link SYS calls to assembly entry points")
            plan["recommendations"].append("Preserve memory layout in target language")
        
        # Priority order
        if prog_type == "HYBRID":
            plan["priority_order"] = ["BASIC_DECOMPILE", "ASSEMBLY_DISASSEMBLY"]
        elif prog_type == "BASIC":
            plan["priority_order"] = ["BASIC_DECOMPILE"]
        elif prog_type == "ASSEMBLY":
            plan["priority_order"] = ["ASSEMBLY_DISASSEMBLY"]
        
        return plan
    
    def format_analysis_report(self, analysis: Dict[str, Any]) -> str:
        """Detaylı analiz raporu formatla"""
        
        report = []
        report.append("🔬 HYBRID PROGRAM ANALYSIS REPORT v2.0")
        report.append("=" * 60)
        report.append("")
        
        # Program Bilgileri
        report.append("📋 PROGRAM INFORMATION:")
        report.append(f"   🎯 Start Address: {analysis.get('start_address_hex', 'Unknown')}")
        report.append(f"   📊 Total Size: {analysis.get('total_file_size', 0)} bytes")
        report.append(f"   🏁 End Address: ${analysis.get('estimated_end_address', 0):04X}")
        report.append(f"   🏷️  Program Type: {analysis.get('program_type', 'Unknown')}")
        
        if analysis.get("is_hybrid"):
            report.append("   🎭 HYBRID PROGRAM DETECTED!")
        
        report.append("")
        
        # BASIC Analizi
        basic_info = analysis.get("basic_info", {})
        if basic_info:
            report.append("📝 BASIC ANALYSIS:")
            report.append(f"   📏 BASIC Size: {basic_info.get('basic_calculated_size', 0)} bytes")
            report.append(f"   📄 Line Count: {basic_info.get('line_count', 0)}")
            report.append(f"   🚀 SYS Calls: {len(basic_info.get('sys_calls', []))}")
            report.append(f"   📝 POKE Operations: {len(basic_info.get('poke_operations', []))}")
            report.append(f"   👁️  PEEK Operations: {len(basic_info.get('peek_operations', []))}")
            report.append("")
        
        # Assembly Analizi
        asm_info = analysis.get("assembly_info", {})
        if asm_info:
            report.append("⚙️ ASSEMBLY ANALYSIS:")
            report.append(f"   🎯 Start: {asm_info.get('assembly_start_hex', 'Unknown')}")
            report.append(f"   📏 Size: {asm_info.get('assembly_size', 0)} bytes")
            report.append(f"   🏁 End: {asm_info.get('assembly_end_hex', 'Unknown')}")
            report.append("")
        
        # SYS Çağrıları
        sys_calls = analysis.get("sys_calls", [])
        if sys_calls:
            report.append("🚀 SYS CALLS DETECTED:")
            for sys_call in sys_calls[:5]:  # İlk 5 tanesi
                report.append(f"   Line {sys_call['line_number']}: SYS {sys_call['address']} ({sys_call['address_hex']})")
                if sys_call.get('calculation'):
                    report.append(f"      Calculation: {sys_call['calculation']}")
            if len(sys_calls) > 5:
                report.append(f"   ... and {len(sys_calls) - 5} more SYS calls")
            report.append("")
        
        # Memory Operations
        memory_usage = analysis.get("memory_usage", [])
        if memory_usage:
            report.append("🧠 MEMORY OPERATIONS:")
            for mem_op in memory_usage[:8]:  # İlk 8 tanesi
                report.append(f"   {mem_op['type']} {mem_op['address_hex']}: {mem_op['description']}")
            if len(memory_usage) > 8:
                report.append(f"   ... and {len(memory_usage) - 8} more operations")
            report.append("")
        
        # Variable Suggestions
        var_suggestions = analysis.get("variable_suggestions", [])
        if var_suggestions:
            report.append("💡 VARIABLE NAMING SUGGESTIONS:")
            for suggestion in var_suggestions[:5]:  # İlk 5 tanesi
                report.append(f"   {suggestion['address']}: {suggestion['suggested_variable']}")
                report.append(f"      ({suggestion['description']})")
            if len(var_suggestions) > 5:
                report.append(f"   ... and {len(var_suggestions) - 5} more suggestions")
            report.append("")
        
        # Disassembly Plan
        plan = analysis.get("disassembly_plan", {})
        if plan.get("tasks"):
            report.append("📋 DISASSEMBLY PLAN:")
            for task in plan["tasks"]:
                report.append(f"   {task['type']}: {task['description']}")
                report.append(f"      Priority: {task['priority']}")
                report.append(f"      Outputs: {', '.join(task['outputs'])}")
            report.append("")
        
        # Recommendations
        if plan.get("recommendations"):
            report.append("💡 RECOMMENDATIONS:")
            for rec in plan["recommendations"]:
                report.append(f"   • {rec}")
            report.append("")
        
        return "\n".join(report)
    
    def generate_hybrid_report(self, analysis: Dict[str, Any]) -> str:
        """Hibrit analiz raporu oluştur (GUI uyumlu)"""
        
        report = []
        report.append("🔍 HYBRID PROGRAM ANALYSIS REPORT")
        report.append("=" * 50)
        
        # Genel bilgi
        report.append(f"📁 File Size: {analysis.get('total_file_size', 0)} bytes")
        report.append(f"🎯 Start Address: {analysis.get('start_address_hex', 'Unknown')}")
        report.append(f"🔤 Is BASIC Program: {'✅' if analysis.get('is_basic_program') else '❌'}")
        report.append(f"🔄 Is Hybrid: {'✅' if analysis.get('is_hybrid') else '❌'}")
        
        # BASIC analizi
        if analysis.get("basic_info"):
            basic = analysis["basic_info"]
            report.append("\n📝 BASIC CODE ANALYSIS:")
            report.append(f"   Lines: {basic.get('line_count', 0)}")
            report.append(f"   Calculated Size: {basic.get('basic_calculated_size', 0)} bytes")
            report.append(f"   SYS Calls: {len(basic.get('sys_calls', []))}")
            
            # SYS çağrıları
            if basic.get("sys_calls"):
                report.append("\n   🎯 SYS CALLS FOUND:")
                for sys_call in basic["sys_calls"]:
                    report.append(f"      • Line {sys_call['line_number']}: SYS {sys_call['address']} ({sys_call['address_hex']})")
        
        # Hibrit analizi
        if analysis.get("hybrid_analysis"):
            hybrid = analysis["hybrid_analysis"]
            report.append(f"\n🔄 HYBRID ANALYSIS:")
            report.append(f"   Basic Size: {hybrid.get('basic_portion', {}).get('size', 0)} bytes")
            report.append(f"   Assembly Size: {hybrid.get('assembly_portion', {}).get('size', 0)} bytes")
            
            if hybrid.get("recommendations"):
                report.append("   📊 Recommendations:")
                for rec in hybrid["recommendations"]:
                    report.append(f"      • {rec}")
        
        # Assembly info
        if analysis.get("assembly_info"):
            asm = analysis["assembly_info"]
            report.append(f"\n⚙️ ASSEMBLY CODE:")
            report.append(f"   Start Address: {asm.get('assembly_start_hex', 'Unknown')}")
            report.append(f"   Size: {asm.get('assembly_size', 0)} bytes")
        
        return "\n".join(report)

# Test fonksiyonu
if __name__ == "__main__":
    print("🔬 Hybrid Program Analyzer Test v2.0")
    print("=" * 50)
    
    analyzer = HybridProgramAnalyzer()
    
    # Test Case 1: BASIC+Assembly hibrit program
    print("\n📋 Test Case 1: BASIC+Assembly Hybrid Program")
    test_data = bytearray()
    test_data.extend([0x01, 0x08])  # Start address $0801
    
    # BASIC program: 10 SYS 2064
    test_data.extend([0x0C, 0x08])  # Next line pointer
    test_data.extend([0x0A, 0x00])  # Line 10
    test_data.extend([0x9C])        # SYS token
    test_data.extend([0x20])        # Space
    test_data.extend(b"2064")       # Address
    test_data.extend([0x00])        # Line end
    test_data.extend([0x00, 0x00])  # Program end
    
    # Assembly kodu ekle (2064 = $0810)
    test_data.extend([0x78, 0xA9, 0x00, 0x8D, 0x20, 0xD0, 0x60])  # SEI, LDA #0, STA $D020, RTS
    
    # Analiz et
    result = analyzer.analyze_prg_data(bytes(test_data))
    
    # Sonuçları göster
    print(f"✅ Program Type: {result.get('program_type', 'Unknown')}")
    print(f"✅ Is Hybrid: {result.get('is_hybrid', False)}")
    print(f"✅ Start Address: {result.get('start_address_hex', 'Unknown')}")
    print(f"✅ File Size: {result.get('total_file_size', 0)} bytes")
    
    if result.get('basic_info'):
        basic = result['basic_info']
        print(f"✅ BASIC Size: {basic.get('basic_calculated_size', 0)} bytes")
        print(f"✅ BASIC Lines: {basic.get('line_count', 0)}")
        print(f"✅ SYS Calls: {len(basic.get('sys_calls', []))}")
    
    if result.get('assembly_info'):
        asm = result['assembly_info']
        print(f"✅ Assembly Start: {asm.get('assembly_start_hex', 'Unknown')}")
        print(f"✅ Assembly Size: {asm.get('assembly_size', 0)} bytes")
    
    # Detaylı rapor
    print("\n📋 DETAILED ANALYSIS REPORT:")
    detailed_report = analyzer.format_analysis_report(result)
    print(detailed_report)
    
    # Test Case 2: Pure BASIC program
    print("\n" + "="*50)
    print("📋 Test Case 2: Pure BASIC Program")
    basic_only = bytearray()
    basic_only.extend([0x01, 0x08])  # Start address $0801
    basic_only.extend([0x15, 0x08])  # Next line pointer
    basic_only.extend([0x0A, 0x00])  # Line 10
    basic_only.extend([0x97])        # PRINT token
    basic_only.extend(b'"HELLO WORLD"')
    basic_only.extend([0x00])        # Line end
    basic_only.extend([0x00, 0x00])  # Program end
    
    result2 = analyzer.analyze_prg_data(bytes(basic_only))
    print(f"✅ Program Type: {result2.get('program_type', 'Unknown')}")
    print(f"✅ Is Hybrid: {result2.get('is_hybrid', False)}")
    
    # Test Case 3: Pure Assembly program
    print("\n📋 Test Case 3: Pure Assembly Program")
    asm_only = bytearray()
    asm_only.extend([0x00, 0x10])  # Start address $1000
    asm_only.extend([0x78, 0xA9, 0x01, 0x8D, 0x20, 0xD0, 0x60])  # Assembly code
    
    result3 = analyzer.analyze_prg_data(bytes(asm_only))
    print(f"✅ Program Type: {result3.get('program_type', 'Unknown')}")
    print(f"✅ Assembly Start: {result3.get('assembly_info', {}).get('assembly_start_hex', 'Unknown')}")
    
    print("\n✅ All tests completed successfully!")
    print("🔬 HybridProgramAnalyzer v2.0 working properly")
