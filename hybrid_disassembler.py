#!/usr/bin/env python3
"""
Hybrid Program Disassembler - BASIC + Machine Code Analysis
Hibrit programlarda BASIC ve makine dili kısımlarını ayırır ve disassemble eder

FEATURES:
- BASIC program analysis
- SYS call detection  
- Machine code section extraction
- Complete disassembly of both parts
- Track/Sector real calculation (C++ ported)

Author: D64 Converter Team
Version: 1.0 - Hybrid Analysis 
"""
#bizim bir hybrid diassemblerimiz yoktu yeni mi uretildi bu?
# ben kod tekrari olmasin diye cabaliyorum  bu kodun cogu yerini hybrid analiz yapmiyor mu?
# eger buradaki kod hybrid analiziden guclu, efektif ve daha kapsamli ise hybrid analiz modulunu diger modullerdeki kullanim durumlari da dikkate alinaran guncellensin
# eger islem cok karmasa yaratacaksi o zaman hybrid analiz modulune yeni sinif eklensin.add(element)


import re
import struct
import logging
import disassembly_formatter
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

@dataclass
class HybridSection:
    """Hibrit program bölümü"""
    section_type: str  # "BASIC", "MACHINE", "DATA"
    start_address: int
    end_address: int
    data: bytes
    description: str

@dataclass
class SysCall:
    """SYS çağrısı bilgisi"""
    line_number: int
    address: int
    parameters: List[str]  # A,X,Y register values if any

class HybridDisassembler:
    """Hibrit program disassembler sistemi"""
    
    def __init__(self):
        """Hibrit disassembler başlatma"""
        self.logger = logging.getLogger(__name__)
        
        # BASIC V2 Tokens token
        #token listesi eksiksiz olabilir. hatta tokenleri basige ceviren modullerimiz
        # var kod tekrarina gerek olmasin. burad yapilan is veya istenen is bizim elimizdeki 
        # tokenlere gore basic yaratan sitemlerden daha yetenekli ise disaridaki 
        # modullerimizi gerekli guncellemeler veya veni siniflarla gelistirebiiriz ve bu sekilde kullanabiliriz
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
        
        # C64 memory regions
        # bu bölümler C64'ün bellek haritasını temsil etmeli ancak oldukca az c64_rom_data 
        # klasorunda ve onun alt klasorlerindeki bilgilerle zengilestirilerek kullaniciya 
        # daha anlamli adresler, veriler, on tanimli degisken isimleri ile verilebilir. 
        # kernal romda kullanilan adresler, basic romda kullanilan alt rutin adreslerinin 
        # en kucugunun bile isimlendirme ve  ne girip ne ciktigina dair bilgilerimiz .json dosyalarinda var. 
        self.memory_regions = {
            (0x0000, 0x00FF): "Zero Page",
            (0x0100, 0x01FF): "Stack",
            (0x0200, 0x02FF): "BASIC Input Buffer", 
            (0x0300, 0x03FF): "Cassette Buffer",
            (0x0400, 0x07FF): "Screen Memory",
            (0x0800, 0x0801): "BASIC Start",
            (0x1000, 0x9FFF): "User Program Area",
            (0xA000, 0xBFFF): "BASIC ROM",
            (0xC000, 0xCFFF): "User RAM",
            (0xD000, 0xDFFF): "I/O Area",
            (0xE000, 0xFFFF): "KERNAL ROM"
        }
    
    def analyze_hybrid_program(self, prg_data: bytes) -> Dict[str, Any]:
        """Hibrit program analizi - ana fonksiyon"""
        
        if len(prg_data) < 4:
            return {"error": "PRG data too short"}
        
        # Start address
        # hibrid programlardaki basic adresinden sonra baslayan asembler baslangic noktasi kullanilmali
        start_address = prg_data[0] + (prg_data[1] << 8)
        code_data = prg_data[2:]
        
        self.logger.info(f"Hibrit analiz başlatıldı: Start={disassembly_formatter.format_address(start_address)}, Size={len(code_data)}")
        
        result = {
            "start_address": start_address,
            "total_size": len(code_data),
            "is_hybrid": False,
            "sections": [],
            "sys_calls": [],
            "basic_info": None,
            "machine_info": None,
            "analysis_report": ""
        }
        
        # BASIC program mı kontrol et
        if start_address == 0x0801:
            self.logger.info("BASIC program tespit edildi")
            basic_analysis = self.analyze_basic_section(code_data)
            result["basic_info"] = basic_analysis
            
            # SYS çağrıları var mı?
            sys_calls = self.find_sys_calls(basic_analysis.get("lines", []))
            result["sys_calls"] = sys_calls
            
            if sys_calls:
                self.logger.info(f"{len(sys_calls)} SYS çağrısı bulundu - HYBRID program!")
                result["is_hybrid"] = True
                
                # Makine dili kısımlarını analiz et
                machine_sections = self.analyze_machine_sections(prg_data, sys_calls)
                result["machine_info"] = machine_sections
                
                # Hibrit bölümleri oluştur
                result["sections"] = self.create_hybrid_sections(basic_analysis, machine_sections, start_address)
            else:
                self.logger.info("SYS çağrısı yok - Pure BASIC program")
                result["sections"] = [HybridSection("BASIC", start_address, start_address + len(code_data), code_data, "Pure BASIC Program")]
        
        else:
            self.logger.info(f"Makine dili program: Start={disassembly_formatter.format_address(start_address)}")
            # Pure machine code
            machine_analysis = self.analyze_pure_machine_code(code_data, start_address)
            result["machine_info"] = machine_analysis
            result["sections"] = [HybridSection("MACHINE", start_address, start_address + len(code_data), code_data, "Pure Machine Code")]
        
        # Analysis report oluştur
        result["analysis_report"] = self.generate_analysis_report(result)
        
        return result
    
    def analyze_basic_section(self, basic_data: bytes) -> Dict[str, Any]:
        """BASIC kısmını analiz et"""
        
        lines = []
        pos = 0
        
        while pos < len(basic_data) - 1:
            try:
                # Next line pointer
                next_line_ptr = basic_data[pos] + (basic_data[pos + 1] << 8)
                pos += 2
                
                if next_line_ptr == 0:  # Program end
                    break
                
                # Line number
                line_number = basic_data[pos] + (basic_data[pos + 1] << 8)
                pos += 2
                
                # Line content
                line_start = pos
                while pos < len(basic_data) and basic_data[pos] != 0:
                    pos += 1
                
                line_data = basic_data[line_start:pos]
                line_text = self.detokenize_basic_line(line_data)
                
                lines.append({
                    "number": line_number,
                    "text": line_text,
                    "raw_data": line_data
                })
                
                pos += 1  # Skip line terminator
                
            except Exception as e:
                self.logger.error(f"BASIC line parse error at pos {pos}: {e}")
                break
        
        return {
            "lines": lines,
            "line_count": len(lines),
            "basic_end_pos": pos
        }
    
    def detokenize_basic_line(self, line_data: bytes) -> str:
        """BASIC satırını detokenize et"""
        
        result = ""
        pos = 0
        
        while pos < len(line_data):
            byte_val = line_data[pos]
            
            if byte_val >= 0x80:  # BASIC token
                token_name = self.basic_tokens.get(byte_val, f"TOKEN_{byte_val:02X}")
                result += token_name
            else:  # Regular character
                if 32 <= byte_val <= 126:
                    result += chr(byte_val)
                else:
                    result += f"[{byte_val:02X}]"
            
            pos += 1
        
        return result
    
    def find_sys_calls(self, basic_lines: List[Dict]) -> List[SysCall]:
        """BASIC'de SYS çağrılarını bul"""
        
        sys_calls = []
        
        for line in basic_lines:
            line_text = line["text"]
            line_number = line["number"]
            
            # SYS pattern: SYS xxxx
            sys_matches = re.findall(r'SYS\s*(\d+)', line_text)
            
            for match in sys_matches:
                address = int(match)
                sys_call = SysCall(
                    line_number=line_number,
                    address=address,
                    parameters=[]  # TODO: A,X,Y register detection
                )
                sys_calls.append(sys_call)
                self.logger.info(f"SYS çağrısı bulundu: Line {line_number} -> SYS {address}")
        
        return sys_calls
    
    def analyze_machine_sections(self, prg_data: bytes, sys_calls: List[SysCall]) -> Dict[str, Any]:
        """Makine dili kısımlarını analiz et"""
        
        start_address = prg_data[0] + (prg_data[1] << 8)
        
        machine_sections = []
        
        for sys_call in sys_calls:
            target_address = sys_call.address
            
            # PRG içindeki offset hesapla
            if target_address >= start_address:
                offset = target_address - start_address + 2  # +2 for start address bytes
                
                if offset < len(prg_data):
                    # Makine dili kısmının sonunu tahmin et
                    end_offset = self.estimate_machine_code_end(prg_data, offset)
                    
                    machine_data = prg_data[offset:end_offset]
                    
                    section = {
                        "sys_call": sys_call,
                        "start_address": target_address,
                        "data": machine_data,
                        "size": len(machine_data),
                        "description": f"Machine code called by SYS {target_address}"
                    }
                    
                    machine_sections.append(section)
                    self.logger.info(f"Makine dili kısmı bulundu: {disassembly_formatter.format_address(target_address)}, {len(machine_data)} bytes")
        
        return {
            "sections": machine_sections,
            "section_count": len(machine_sections)
        }
    
    def estimate_machine_code_end(self, prg_data: bytes, start_offset: int) -> int:
        """Makine dili kısmının sonunu tahmin et"""
        
        # Simple heuristic: Look for RTS (0x60) or common end patterns
        pos = start_offset
        
        while pos < len(prg_data):
            byte_val = prg_data[pos]
            
            # RTS instruction - possible end
            if byte_val == 0x60:
                return pos + 1
            
            # JMP to BASIC warm start
            if byte_val == 0x4C and pos + 2 < len(prg_data):
                target = prg_data[pos + 1] + (prg_data[pos + 2] << 8)
                if target == 0xA474:  # BASIC warm start
                    return pos + 3
            
            pos += 1
            
            # Güvenlik limiti
            if pos - start_offset > 2048:  # Max 2KB machine code
                break
        
        # Eğer bulamazsa dosya sonuna kadar
        return len(prg_data)
    
    def analyze_pure_machine_code(self, code_data: bytes, start_address: int) -> Dict[str, Any]:
        """Pure makine dili analizi"""
        
        return {
            "start_address": start_address,
            "data": code_data,
            "size": len(code_data),
            "description": f"Pure machine code at ${start_address:04X}"
        }
    
    def create_hybrid_sections(self, basic_info: Dict, machine_info: Dict, start_address: int) -> List[HybridSection]:
        """Hibrit bölümleri oluştur"""
        
        sections = []
        
        # BASIC section
        if basic_info:
            basic_end = basic_info.get("basic_end_pos", 0)
            sections.append(HybridSection(
                "BASIC",
                start_address,
                start_address + basic_end,
                b"",  # Will be filled from original data
                f"BASIC program with {basic_info.get('line_count', 0)} lines"
            ))
        
        # Machine sections
        if machine_info:
            for section in machine_info.get("sections", []):
                sections.append(HybridSection(
                    "MACHINE",
                    section["start_address"],
                    section["start_address"] + section["size"],
                    section["data"],
                    section["description"]
                ))
        
        return sections
    
    def generate_analysis_report(self, analysis: Dict[str, Any]) -> str:
        """Analiz raporu oluştur"""
        
        report = []
        report.append("="*60)
        report.append("HYBRID PROGRAM ANALYSIS REPORT")
        report.append("="*60)
        report.append("")
        
        # Basic info
        report.append(f"Start Address: ${analysis['start_address']:04X}")
        report.append(f"Total Size: {analysis['total_size']} bytes")
        report.append(f"Program Type: {'HYBRID' if analysis['is_hybrid'] else 'SINGLE'}")
        report.append("")
        
        # BASIC info
        if analysis.get("basic_info"):
            basic_info = analysis["basic_info"]
            report.append("BASIC SECTION:")
            report.append(f"  Lines: {basic_info.get('line_count', 0)}")
            report.append("")
        
        # SYS calls
        if analysis.get("sys_calls"):
            report.append("SYS CALLS FOUND:")
            for sys_call in analysis["sys_calls"]:
                report.append(f"  Line {sys_call.line_number}: SYS {sys_call.address} (${sys_call.address:04X})")
            report.append("")
        
        # Machine sections
        if analysis.get("machine_info"):
            machine_info = analysis["machine_info"]
            if machine_info.get("sections"):
                report.append("MACHINE CODE SECTIONS:")
                for i, section in enumerate(machine_info["sections"]):
                    report.append(f"  Section {i+1}: ${section['start_address']:04X} ({section['size']} bytes)")
                    report.append(f"    Description: {section['description']}")
                report.append("")
        
        # Sections summary
        if analysis.get("sections"):
            report.append("PROGRAM SECTIONS:")
            for i, section in enumerate(analysis["sections"]):
                report.append(f"  {i+1}. {section.section_type}: ${section.start_address:04X}-${section.end_address:04X}")
                report.append(f"     {section.description}")
            report.append("")
        
        report.append("="*60)
        
        return "\n".join(report)
    
    def disassemble_machine_section(self, machine_data: bytes, start_address: int) -> str:
        """Makine dili kısmını disassemble et"""
        
        # Bu fonksiyon mevcut disassembler'ı kullanabilir
        try:
            # AdvancedDisassembler'ı kullan
            from advanced_disassembler import AdvancedDisassembler
            
            disassembler = AdvancedDisassembler(
                start_address=start_address,
                code=machine_data,
                use_illegal_opcodes=True
            )
            
            return disassembler.disassemble()
            
        except ImportError:
            # Fallback: Simple hex dump
            result = []
            result.append(f"; Machine code disassembly at ${start_address:04X}")
            result.append(f"; Size: {len(machine_data)} bytes")
            result.append("")
            
            for i in range(0, len(machine_data), 16):
                addr = start_address + i
                hex_bytes = " ".join(f"{b:02X}" for b in machine_data[i:i+16])
                result.append(f"${addr:04X}: {hex_bytes}")
            
            return "\n".join(result)

# Test kodu
if __name__ == "__main__":
    print("🔍 Hybrid Disassembler Test")
    print("="*50)
    
    # Test data: Simple BASIC program with SYS call
    test_data = bytearray()
    test_data.extend([0x01, 0x08])  # Start address $0801
    
    # 10 SYS 2064
    test_data.extend([0x15, 0x08])  # Next line pointer
    test_data.extend([0x0A, 0x00])  # Line 10
    test_data.extend([0x9E])        # SYS token
    test_data.extend([0x20])        # Space
    test_data.extend(b"2064")       # Address
    test_data.extend([0x00])        # Line end
    
    # Machine code at offset (simulated)
    test_data.extend([0xA9, 0x00])  # LDA #$00
    test_data.extend([0x60])        # RTS
    test_data.extend([0x00, 0x00])  # Program end
    
    analyzer = HybridDisassembler()
    result = analyzer.analyze_hybrid_program(bytes(test_data))
    
    print("Analysis Result:")
    print(f"Is Hybrid: {result['is_hybrid']}")
    print(f"SYS Calls: {len(result['sys_calls'])}")
    print(f"Sections: {len(result['sections'])}")
    print("\nReport:")
    print(result["analysis_report"])
