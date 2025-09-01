"""
illegal_opcode_analyzer.py
6502 Illegal Opcode Analyzer
Gelişmiş illegal opcode detection ve analiz sistemi
"""

import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum

# Logger setup
logger = logging.getLogger(__name__)

class IllegalOpcodeType(Enum):
    """Illegal opcode türleri"""
    UNDOCUMENTED = "undocumented"  # Dokümantasyon dışı ama çalışan
    UNSTABLE = "unstable"  # Kararsız davranış
    ILLEGAL = "illegal"  # Tamamen illegal
    UNKNOWN = "unknown"  # Bilinmeyen

@dataclass
class IllegalOpcodeInfo:
    """Illegal opcode bilgisi"""
    opcode: int
    mnemonic: str
    description: str
    opcode_type: IllegalOpcodeType
    stability: str
    addressing_mode: str
    cycles: int
    side_effects: str
    alternate_names: List[str]
    
    def __post_init__(self):
        if not self.alternate_names:
            self.alternate_names = []

class IllegalOpcodeAnalyzer:
    """
    6502 Illegal Opcode Analyzer
    Gelişmiş illegal opcode detection ve analiz
    """
    
    def __init__(self):
        """Illegal opcode analyzer başlatma"""
        self.illegal_opcodes = self._initialize_illegal_opcodes()
        self.analysis_results = []
        self.statistics = {
            'total_opcodes': 0,
            'illegal_count': 0,
            'undocumented_count': 0,
            'unstable_count': 0,
            'unknown_count': 0
        }
        
        logger.info("IllegalOpcodeAnalyzer initialized")
    
    def _initialize_illegal_opcodes(self) -> Dict[int, IllegalOpcodeInfo]:
        """Illegal opcode veritabanını başlat"""
        illegal_db = {}
        
        # Undocumented/Illegal opcodes database
        illegal_data = [
            # SLO (ASL + ORA) - Shift Left and OR
            (0x03, "SLO", "Shift Left and OR with accumulator (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 8, "Memory modified, A modified", ["ASO"]),
            (0x07, "SLO", "Shift Left and OR with accumulator (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 5, "Memory modified, A modified", ["ASO"]),
            (0x0F, "SLO", "Shift Left and OR with accumulator (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 6, "Memory modified, A modified", ["ASO"]),
            (0x13, "SLO", "Shift Left and OR with accumulator (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 8, "Memory modified, A modified", ["ASO"]),
            (0x17, "SLO", "Shift Left and OR with accumulator (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 6, "Memory modified, A modified", ["ASO"]),
            (0x1B, "SLO", "Shift Left and OR with accumulator (absolute,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "aby", 7, "Memory modified, A modified", ["ASO"]),
            (0x1F, "SLO", "Shift Left and OR with accumulator (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 7, "Memory modified, A modified", ["ASO"]),
            
            # RLA (ROL + AND) - Rotate Left and AND
            (0x23, "RLA", "Rotate Left and AND with accumulator (indirect,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "inx", 8, "Memory modified, A modified", []),
            (0x27, "RLA", "Rotate Left and AND with accumulator (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 5, "Memory modified, A modified", []),
            (0x2F, "RLA", "Rotate Left and AND with accumulator (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 6, "Memory modified, A modified", []),
            (0x33, "RLA", "Rotate Left and AND with accumulator (indirect,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "iny", 8, "Memory modified, A modified", []),
            (0x37, "RLA", "Rotate Left and AND with accumulator (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 6, "Memory modified, A modified", []),
            (0x3B, "RLA", "Rotate Left and AND with accumulator (absolute,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "aby", 7, "Memory modified, A modified", []),
            (0x3F, "RLA", "Rotate Left and AND with accumulator (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 7, "Memory modified, A modified", []),
            
            # SRE (LSR + EOR) - Shift Right and EOR
            (0x43, "SRE", "Shift Right and EOR with accumulator (indirect,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "inx", 8, "Memory modified, A modified", ["LSE"]),
            (0x47, "SRE", "Shift Right and EOR with accumulator (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 5, "Memory modified, A modified", ["LSE"]),
            (0x4F, "SRE", "Shift Right and EOR with accumulator (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 6, "Memory modified, A modified", ["LSE"]),
            (0x53, "SRE", "Shift Right and EOR with accumulator (indirect,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "iny", 8, "Memory modified, A modified", ["LSE"]),
            (0x57, "SRE", "Shift Right and EOR with accumulator (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 6, "Memory modified, A modified", ["LSE"]),
            (0x5B, "SRE", "Shift Right and EOR with accumulator (absolute,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "aby", 7, "Memory modified, A modified", ["LSE"]),
            (0x5F, "SRE", "Shift Right and EOR with accumulator (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 7, "Memory modified, A modified", ["LSE"]),
            
            # RRA (ROR + ADC) - Rotate Right and ADC
            (0x63, "RRA", "Rotate Right and ADC with accumulator (indirect,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "inx", 8, "Memory modified, A modified", []),
            (0x67, "RRA", "Rotate Right and ADC with accumulator (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 5, "Memory modified, A modified", []),
            (0x6F, "RRA", "Rotate Right and ADC with accumulator (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 6, "Memory modified, A modified", []),
            (0x73, "RRA", "Rotate Right and ADC with accumulator (indirect,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "iny", 8, "Memory modified, A modified", []),
            (0x77, "RRA", "Rotate Right and ADC with accumulator (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 6, "Memory modified, A modified", []),
            (0x7B, "RRA", "Rotate Right and ADC with accumulator (absolute,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "aby", 7, "Memory modified, A modified", []),
            (0x7F, "RRA", "Rotate Right and ADC with accumulator (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 7, "Memory modified, A modified", []),
            
            # SAX (STA + STX) - Store A AND X
            (0x83, "SAX", "Store A AND X (indirect,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "inx", 6, "Memory modified", ["AXS"]),
            (0x87, "SAX", "Store A AND X (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 3, "Memory modified", ["AXS"]),
            (0x8F, "SAX", "Store A AND X (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 4, "Memory modified", ["AXS"]),
            (0x97, "SAX", "Store A AND X (zero page,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpy", 4, "Memory modified", ["AXS"]),
            
            # LAX (LDA + LDX) - Load A and X
            (0xA3, "LAX", "Load A and X (indirect,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "inx", 6, "A and X modified", []),
            (0xA7, "LAX", "Load A and X (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 3, "A and X modified", []),
            (0xAF, "LAX", "Load A and X (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 4, "A and X modified", []),
            (0xB3, "LAX", "Load A and X (indirect,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "iny", 5, "A and X modified", []),
            (0xB7, "LAX", "Load A and X (zero page,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpy", 4, "A and X modified", []),
            (0xBF, "LAX", "Load A and X (absolute,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "aby", 4, "A and X modified", []),
            
            # DCP (DEC + CMP) - Decrement and Compare
            (0xC3, "DCP", "Decrement and Compare with accumulator (indirect,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "inx", 8, "Memory modified, flags affected", ["DCM"]),
            (0xC7, "DCP", "Decrement and Compare with accumulator (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 5, "Memory modified, flags affected", ["DCM"]),
            (0xCF, "DCP", "Decrement and Compare with accumulator (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 6, "Memory modified, flags affected", ["DCM"]),
            (0xD3, "DCP", "Decrement and Compare with accumulator (indirect,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "iny", 8, "Memory modified, flags affected", ["DCM"]),
            (0xD7, "DCP", "Decrement and Compare with accumulator (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 6, "Memory modified, flags affected", ["DCM"]),
            (0xDB, "DCP", "Decrement and Compare with accumulator (absolute,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "aby", 7, "Memory modified, flags affected", ["DCM"]),
            (0xDF, "DCP", "Decrement and Compare with accumulator (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 7, "Memory modified, flags affected", ["DCM"]),
            
            # ISC (INC + SBC) - Increment and Subtract with Carry
            (0xE3, "ISC", "Increment and Subtract with Carry (indirect,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "inx", 8, "Memory modified, A modified", ["ISB", "INS"]),
            (0xE7, "ISC", "Increment and Subtract with Carry (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 5, "Memory modified, A modified", ["ISB", "INS"]),
            (0xEF, "ISC", "Increment and Subtract with Carry (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 6, "Memory modified, A modified", ["ISB", "INS"]),
            (0xF3, "ISC", "Increment and Subtract with Carry (indirect,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "iny", 8, "Memory modified, A modified", ["ISB", "INS"]),
            (0xF7, "ISC", "Increment and Subtract with Carry (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 6, "Memory modified, A modified", ["ISB", "INS"]),
            (0xFB, "ISC", "Increment and Subtract with Carry (absolute,Y)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "aby", 7, "Memory modified, A modified", ["ISB", "INS"]),
            (0xFF, "ISC", "Increment and Subtract with Carry (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 7, "Memory modified, A modified", ["ISB", "INS"]),
            
            # NOP variants - No Operation
            (0x04, "NOP", "No Operation (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 3, "None", ["DOP", "SKB"]),
            (0x0C, "NOP", "No Operation (absolute)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abs", 4, "None", ["TOP", "SKW"]),
            (0x14, "NOP", "No Operation (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 4, "None", ["DOP", "SKB"]),
            (0x1A, "NOP", "No Operation (implied)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imp", 2, "None", []),
            (0x1C, "NOP", "No Operation (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 4, "None", ["TOP", "SKW"]),
            (0x34, "NOP", "No Operation (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 4, "None", ["DOP", "SKB"]),
            (0x3A, "NOP", "No Operation (implied)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imp", 2, "None", []),
            (0x3C, "NOP", "No Operation (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 4, "None", ["TOP", "SKW"]),
            (0x44, "NOP", "No Operation (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 3, "None", ["DOP", "SKB"]),
            (0x54, "NOP", "No Operation (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 4, "None", ["DOP", "SKB"]),
            (0x5A, "NOP", "No Operation (implied)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imp", 2, "None", []),
            (0x5C, "NOP", "No Operation (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 4, "None", ["TOP", "SKW"]),
            (0x64, "NOP", "No Operation (zero page)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpg", 3, "None", ["DOP", "SKB"]),
            (0x74, "NOP", "No Operation (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 4, "None", ["DOP", "SKB"]),
            (0x7A, "NOP", "No Operation (implied)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imp", 2, "None", []),
            (0x7C, "NOP", "No Operation (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 4, "None", ["TOP", "SKW"]),
            (0x80, "NOP", "No Operation (immediate)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imm", 2, "None", ["DOP", "SKB"]),
            (0x82, "NOP", "No Operation (immediate)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imm", 2, "None", ["DOP", "SKB"]),
            (0x89, "NOP", "No Operation (immediate)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imm", 2, "None", ["DOP", "SKB"]),
            (0xC2, "NOP", "No Operation (immediate)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imm", 2, "None", ["DOP", "SKB"]),
            (0xD4, "NOP", "No Operation (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 4, "None", ["DOP", "SKB"]),
            (0xDA, "NOP", "No Operation (implied)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imp", 2, "None", []),
            (0xDC, "NOP", "No Operation (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 4, "None", ["TOP", "SKW"]),
            (0xE2, "NOP", "No Operation (immediate)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imm", 2, "None", ["DOP", "SKB"]),
            (0xF4, "NOP", "No Operation (zero page,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "zpx", 4, "None", ["DOP", "SKB"]),
            (0xFA, "NOP", "No Operation (implied)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imp", 2, "None", []),
            (0xFC, "NOP", "No Operation (absolute,X)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "abx", 4, "None", ["TOP", "SKW"]),
            
            # Highly unstable/illegal opcodes
            (0x02, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0x12, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0x22, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0x32, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0x42, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0x52, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0x62, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0x72, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0x92, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0xB2, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0xD2, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            (0xF2, "KIL", "Kill/Halt processor", IllegalOpcodeType.ILLEGAL, "Unstable", "imp", 0, "Processor halts", ["JAM", "HLT"]),
            
            # More unstable opcodes
            (0x8B, "XAA", "X AND A to A (immediate)", IllegalOpcodeType.UNSTABLE, "Highly unstable", "imm", 2, "A modified, unstable", ["ANE"]),
            (0x9B, "TAS", "Transfer A AND X to S and A AND X AND H+1 to memory", IllegalOpcodeType.UNSTABLE, "Highly unstable", "aby", 5, "S and memory modified", ["SHS", "XAS"]),
            (0x9C, "SHY", "Store Y AND H+1 (absolute,X)", IllegalOpcodeType.UNSTABLE, "Highly unstable", "abx", 5, "Memory modified", ["SAY", "A11"]),
            (0x9E, "SHX", "Store X AND H+1 (absolute,Y)", IllegalOpcodeType.UNSTABLE, "Highly unstable", "aby", 5, "Memory modified", ["SXA", "XAS"]),
            (0x9F, "AHX", "Store A AND X AND H+1 (absolute,Y)", IllegalOpcodeType.UNSTABLE, "Highly unstable", "aby", 5, "Memory modified", ["SHA", "AXA"]),
            (0xAB, "LAX", "Load A and X (immediate)", IllegalOpcodeType.UNSTABLE, "Highly unstable", "imm", 2, "A and X modified", ["LXA", "OAL"]),
            (0xBB, "LAS", "Load A, X and S (absolute,Y)", IllegalOpcodeType.UNSTABLE, "Highly unstable", "aby", 4, "A, X and S modified", ["LAR"]),
            (0xCB, "AXS", "A AND X minus immediate to X", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imm", 2, "X modified", ["SBX", "SAX"]),
            (0xEB, "SBC", "Subtract with Carry (immediate)", IllegalOpcodeType.UNDOCUMENTED, "Stable", "imm", 2, "A modified", ["USBC"]),
        ]
        
        for opcode, mnemonic, desc, opcode_type, stability, addressing, cycles, effects, alts in illegal_data:
            illegal_db[opcode] = IllegalOpcodeInfo(
                opcode=opcode,
                mnemonic=mnemonic,
                description=desc,
                opcode_type=opcode_type,
                stability=stability,
                addressing_mode=addressing,
                cycles=cycles,
                side_effects=effects,
                alternate_names=alts
            )
        
        logger.info(f"Loaded {len(illegal_db)} illegal/undocumented opcodes")
        return illegal_db
    
    def is_illegal_opcode(self, opcode: int) -> bool:
        """Opcode illegal mi kontrol et"""
        return opcode in self.illegal_opcodes
    
    def get_illegal_opcode_info(self, opcode: int) -> Optional[IllegalOpcodeInfo]:
        """Illegal opcode bilgisini al"""
        return self.illegal_opcodes.get(opcode)
    
    def analyze_code_data(self, code_data: bytes, start_address: int = 0x1000) -> Dict:
        """Kod verisini analiz et ve illegal opcodes bul"""
        self.analysis_results = []
        self.statistics = {
            'total_opcodes': 0,
            'illegal_count': 0,
            'undocumented_count': 0,
            'unstable_count': 0,
            'unknown_count': 0
        }
        
        address = start_address
        i = 0
        
        logger.info(f"Analyzing {len(code_data)} bytes starting at ${start_address:04X}")
        
        while i < len(code_data):
            opcode = code_data[i]
            self.statistics['total_opcodes'] += 1
            
            if self.is_illegal_opcode(opcode):
                illegal_info = self.get_illegal_opcode_info(opcode)
                
                # Operand bytes hesapla
                operand_bytes = []
                instruction_length = self._get_instruction_length(opcode, illegal_info.addressing_mode)
                
                for j in range(1, instruction_length):
                    if i + j < len(code_data):
                        operand_bytes.append(code_data[i + j])
                
                # Analiz sonucu kaydet
                result = {
                    'address': address,
                    'opcode': opcode,
                    'opcode_info': illegal_info,
                    'operand_bytes': operand_bytes,
                    'instruction_length': instruction_length,
                    'context': self._get_context(code_data, i, 5)
                }
                
                self.analysis_results.append(result)
                
                # İstatistikleri güncelle
                self.statistics['illegal_count'] += 1
                if illegal_info.opcode_type == IllegalOpcodeType.UNDOCUMENTED:
                    self.statistics['undocumented_count'] += 1
                elif illegal_info.opcode_type == IllegalOpcodeType.UNSTABLE:
                    self.statistics['unstable_count'] += 1
                elif illegal_info.opcode_type == IllegalOpcodeType.UNKNOWN:
                    self.statistics['unknown_count'] += 1
                
                logger.debug(f"Illegal opcode found: ${opcode:02X} at ${address:04X} - {illegal_info.mnemonic}")
                
                address += instruction_length
                i += instruction_length
            else:
                # Normal opcode, single byte skip
                address += 1
                i += 1
        
        logger.info(f"Analysis complete: {self.statistics}")
        return self.get_analysis_summary()
    
    def _get_instruction_length(self, opcode: int, addressing_mode: str) -> int:
        """Instruction uzunluğunu hesapla"""
        length_map = {
            'imp': 1,  # Implied
            'imm': 2,  # Immediate
            'zpg': 2,  # Zero page
            'zpx': 2,  # Zero page,X
            'zpy': 2,  # Zero page,Y
            'abs': 3,  # Absolute
            'abx': 3,  # Absolute,X
            'aby': 3,  # Absolute,Y
            'ind': 3,  # Indirect
            'inx': 2,  # Indirect,X
            'iny': 2,  # Indirect,Y
            'rel': 2,  # Relative
        }
        return length_map.get(addressing_mode, 1)
    
    def _get_context(self, code_data: bytes, position: int, context_size: int) -> Dict:
        """Opcode'un çevresindeki context'i al"""
        start = max(0, position - context_size)
        end = min(len(code_data), position + context_size + 1)
        
        context_bytes = code_data[start:end]
        context_position = position - start
        
        return {
            'bytes': list(context_bytes),
            'position': context_position,
            'start_offset': start,
            'end_offset': end
        }
    
    def get_analysis_summary(self) -> Dict:
        """Analiz özetini al"""
        return {
            'statistics': self.statistics,
            'illegal_opcodes_found': self.analysis_results,
            'severity_breakdown': self._calculate_severity_breakdown(),
            'recommendations': self._generate_recommendations()
        }
    
    def _calculate_severity_breakdown(self) -> Dict:
        """Severity breakdown hesapla"""
        severity_counts = {
            'low': 0,    # Undocumented but stable
            'medium': 0, # Unstable behavior
            'high': 0,   # Illegal/dangerous
            'unknown': 0 # Unknown behavior
        }
        
        for result in self.analysis_results:
            illegal_info = result['opcode_info']
            if illegal_info.opcode_type == IllegalOpcodeType.UNDOCUMENTED:
                if 'Stable' in illegal_info.stability:
                    severity_counts['low'] += 1
                else:
                    severity_counts['medium'] += 1
            elif illegal_info.opcode_type == IllegalOpcodeType.UNSTABLE:
                severity_counts['high'] += 1
            elif illegal_info.opcode_type == IllegalOpcodeType.ILLEGAL:
                severity_counts['high'] += 1
            else:
                severity_counts['unknown'] += 1
        
        return severity_counts
    
    def _generate_recommendations(self) -> List[str]:
        """Öneriler oluştur"""
        recommendations = []
        
        if self.statistics['illegal_count'] == 0:
            recommendations.append("✅ Illegal opcode bulunamadı - kod güvenli görünüyor")
        else:
            recommendations.append(f"⚠️ {self.statistics['illegal_count']} illegal opcode bulundu")
            
            if self.statistics['unstable_count'] > 0:
                recommendations.append(f"🔥 {self.statistics['unstable_count']} unstable opcode - dikkatli olun!")
            
            if self.statistics['undocumented_count'] > 0:
                recommendations.append(f"📋 {self.statistics['undocumented_count']} undocumented opcode - genellikle güvenli")
            
            # Specific recommendations based on found opcodes
            found_opcodes = [result['opcode'] for result in self.analysis_results]
            
            if any(opcode in [0x02, 0x12, 0x22, 0x32, 0x42, 0x52, 0x62, 0x72, 0x92, 0xB2, 0xD2, 0xF2] for opcode in found_opcodes):
                recommendations.append("🚨 TEHLIKE: KIL/JAM instruction bulundu - işlemci donabilir!")
            
            if any(opcode in [0x8B, 0x9B, 0x9C, 0x9E, 0x9F, 0xAB, 0xBB] for opcode in found_opcodes):
                recommendations.append("⚠️ Highly unstable opcodes bulundu - davranış öngörülemez")
            
            if any(opcode in [0x03, 0x07, 0x0F, 0x13, 0x17, 0x1B, 0x1F] for opcode in found_opcodes):
                recommendations.append("ℹ️ SLO opcodes bulundu - genellikle güvenli")
        
        return recommendations
    
    def generate_detailed_report(self) -> str:
        """Detaylı rapor oluştur"""
        report = []
        report.append("=" * 60)
        report.append("6502 ILLEGAL OPCODE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # İstatistikler
        report.append("STATISTICS:")
        report.append(f"  Total opcodes analyzed: {self.statistics['total_opcodes']}")
        report.append(f"  Illegal opcodes found: {self.statistics['illegal_count']}")
        report.append(f"  Undocumented opcodes: {self.statistics['undocumented_count']}")
        report.append(f"  Unstable opcodes: {self.statistics['unstable_count']}")
        report.append(f"  Unknown opcodes: {self.statistics['unknown_count']}")
        report.append("")
        
        # Severity breakdown
        severity = self._calculate_severity_breakdown()
        report.append("SEVERITY BREAKDOWN:")
        report.append(f"  Low (Stable undocumented): {severity['low']}")
        report.append(f"  Medium (Unstable): {severity['medium']}")
        report.append(f"  High (Illegal/Dangerous): {severity['high']}")
        report.append(f"  Unknown: {severity['unknown']}")
        report.append("")
        
        # Öneriler
        report.append("RECOMMENDATIONS:")
        for rec in self._generate_recommendations():
            report.append(f"  {rec}")
        report.append("")
        
        # Detaylı bulgular
        if self.analysis_results:
            report.append("DETAILED FINDINGS:")
            report.append("-" * 40)
            
            for i, result in enumerate(self.analysis_results):
                opcode_info = result['opcode_info']
                report.append(f"#{i+1} Address: ${result['address']:04X}")
                report.append(f"    Opcode: ${result['opcode']:02X}")
                report.append(f"    Mnemonic: {opcode_info.mnemonic}")
                report.append(f"    Type: {opcode_info.opcode_type.value}")
                report.append(f"    Stability: {opcode_info.stability}")
                report.append(f"    Description: {opcode_info.description}")
                report.append(f"    Side effects: {opcode_info.side_effects}")
                report.append(f"    Cycles: {opcode_info.cycles}")
                if opcode_info.alternate_names:
                    report.append(f"    Alternate names: {', '.join(opcode_info.alternate_names)}")
                
                # Operand bytes
                if result['operand_bytes']:
                    operand_str = ' '.join(f"${b:02X}" for b in result['operand_bytes'])
                    report.append(f"    Operand bytes: {operand_str}")
                
                # Context
                context = result['context']
                context_str = ' '.join(f"${b:02X}" for b in context['bytes'])
                report.append(f"    Context: {context_str}")
                report.append(f"             {' ' * (context['position'] * 4)}^^")
                report.append("")
        
        return "\n".join(report)
    
    def export_results(self, filename: str, format: str = 'text'):
        """Sonuçları dosyaya export et"""
        if format == 'text':
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.generate_detailed_report())
        elif format == 'json':
            import json
            summary = self.get_analysis_summary()
            # IllegalOpcodeInfo objelerini serialize et
            serializable_results = []
            for result in summary['illegal_opcodes_found']:
                serializable_result = dict(result)
                serializable_result['opcode_info'] = {
                    'opcode': result['opcode_info'].opcode,
                    'mnemonic': result['opcode_info'].mnemonic,
                    'description': result['opcode_info'].description,
                    'opcode_type': result['opcode_info'].opcode_type.value,
                    'stability': result['opcode_info'].stability,
                    'addressing_mode': result['opcode_info'].addressing_mode,
                    'cycles': result['opcode_info'].cycles,
                    'side_effects': result['opcode_info'].side_effects,
                    'alternate_names': result['opcode_info'].alternate_names
                }
                serializable_results.append(serializable_result)
            
            summary['illegal_opcodes_found'] = serializable_results
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results exported to {filename}")

# Test function
    def analyze_prg_file(self, file_path: str) -> Dict:
        """PRG dosyasını analiz et"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            if len(data) < 2:
                return {
                    'error': 'Dosya çok küçük',
                    'statistics': {'total_opcodes': 0, 'illegal_count': 0},
                    'illegal_opcodes_found': []
                }
            
            # PRG header'ını skip et (ilk 2 byte load address)
            load_address = data[0] | (data[1] << 8)
            code_data = data[2:]
            
            print(f"PRG dosyası analiz ediliyor: {file_path}")
            print(f"Load address: ${load_address:04X}")
            print(f"Code size: {len(code_data)} bytes")
            
            return self.analyze_code_data(code_data, start_address=load_address)
        
        except Exception as e:
            return {
                'error': f'Dosya okuma hatası: {str(e)}',
                'statistics': {'total_opcodes': 0, 'illegal_count': 0},
                'illegal_opcodes_found': []
            }

def test_illegal_analyzer():
    """Test illegal opcode analyzer"""
    analyzer = IllegalOpcodeAnalyzer()
    
    # Test data with some illegal opcodes
    test_data = bytes([
        0xA9, 0x01,  # LDA #$01 (legal)
        0x03, 0x20,  # SLO $20 (illegal)
        0x8D, 0x00, 0x02,  # STA $0200 (legal)
        0x02,  # KIL (illegal - dangerous)
        0x4C, 0x00, 0x10,  # JMP $1000 (legal)
        0xCB, 0x05,  # AXS #$05 (illegal)
        0x60  # RTS (legal)
    ])
    
    # Analyze
    summary = analyzer.analyze_code_data(test_data, 0x1000)
    
    # Print results
    print("Illegal Opcode Analysis Test:")
    print("=" * 40)
    print(f"Total opcodes: {summary['statistics']['total_opcodes']}")
    print(f"Illegal found: {summary['statistics']['illegal_count']}")
    print("\nDetailed report:")
    print(analyzer.generate_detailed_report())
    
    return len(summary['illegal_opcodes_found']) > 0

def test_prg_file_analyzer():
    """Test PRG file analyzer"""
    import sys
    if len(sys.argv) < 2:
        print("Usage: python illegal_opcode_analyzer.py <prg_file>")
        return
    
    file_path = sys.argv[1]
    analyzer = IllegalOpcodeAnalyzer()
    
    result = analyzer.analyze_prg_file(file_path)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    print("\nAnalysis Results:")
    print("=" * 50)
    print(f"Total opcodes: {result['statistics']['total_opcodes']}")
    print(f"Illegal found: {result['statistics']['illegal_count']}")
    
    if result['statistics']['illegal_count'] > 0:
        print("\nDetailed report:")
        print(analyzer.generate_detailed_report())
    else:
        print("\n✅ No illegal opcodes found! Code is clean.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_prg_file_analyzer()
    else:
        test_illegal_analyzer()
