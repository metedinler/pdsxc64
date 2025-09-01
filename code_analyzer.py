#!/usr/bin/env python
"""
CODE ANALYZER - ADVANCED PATTERN RECOGNITION SYSTEM
===================================================

Bu modül, 6502 assembly kodunda gelişmiş pattern tanıma ve kod analizi yapar.
Unified Decompiler ile entegre çalışarak code quality'yi artırır.

ÖZELLİKLER:
- Loop pattern detection (FOR/WHILE döngüleri)
- Subroutine call analysis
- Data structure identification
- Algorithm pattern recognition
- Memory usage pattern analysis
- Code complexity measurement
- Optimization suggestions

DESTEKLENEN PATTERN'LER:
- Counting loops (FOR i = 1 TO 10)
- Conditional loops (WHILE condition)
- Array operations (data processing)
- String operations (text manipulation)
- Sorting algorithms (bubble sort, etc.)
- Search algorithms (linear, binary search)
- Math operations (multiplication, division)

KULLANIM:
analyzer = CodeAnalyzer(prg_data, start_address)
patterns = analyzer.analyze_all_patterns()
suggestions = analyzer.get_optimization_suggestions()
"""

import os
import sys
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass
from enum import Enum

# Import our components
from enhanced_c64_memory_manager import EnhancedC64MemoryManager

class PatternType(Enum):
    """Tanınabilir pattern türleri"""
    COUNTING_LOOP = "counting_loop"
    CONDITIONAL_LOOP = "conditional_loop"
    ARRAY_ACCESS = "array_access"
    STRING_OPERATION = "string_operation"
    SORTING_ALGORITHM = "sorting_algorithm"
    SEARCH_ALGORITHM = "search_algorithm"
    MATH_OPERATION = "math_operation"
    SUBROUTINE_CALL = "subroutine_call"
    DATA_INITIALIZATION = "data_initialization"
    MEMORY_COPY = "memory_copy"
    SCREEN_MANIPULATION = "screen_manipulation"
    SOUND_GENERATION = "sound_generation"

@dataclass
class CodePattern:
    """Tespit edilen kod pattern'i"""
    pattern_type: PatternType
    start_address: int
    end_address: int
    confidence: float  # 0.0 - 1.0
    description: str
    high_level_equivalent: str
    optimization_suggestion: str = ""
    variables_used: List[str] = None
    
    def __post_init__(self):
        if self.variables_used is None:
            self.variables_used = []

@dataclass 
class AnalysisResult:
    """Kod analiz sonuçları"""
    patterns: List[CodePattern]
    complexity_score: float
    memory_usage: Dict[str, int]
    subroutine_map: Dict[int, str]
    data_structures: List[Dict]
    optimization_opportunities: List[str]

class CodeAnalyzer:
    """
    Gelişmiş 6502 kod analiz sistemi
    """
    
    def __init__(self, prg_data: bytes, start_address: int = 0x801):
        """
        CodeAnalyzer başlatma
        
        Args:
            prg_data: 6502 machine code bytes
            start_address: Kodun başlangıç adresi
        """
        self.prg_data = prg_data
        self.start_address = start_address
        self.memory_manager = None
        
        # Analysis state
        self.instructions = []  # Parsed instructions
        self.patterns = []
        self.subroutines = {}
        self.labels = {}
        self.data_areas = []
        
        # Pattern detection thresholds
        self.loop_confidence_threshold = 0.7
        self.pattern_confidence_threshold = 0.6
        
        print(f"🔍 CodeAnalyzer başlatıldı - Start: ${start_address:04X}, Size: {len(prg_data)} bytes")
    
    def initialize_memory_manager(self) -> bool:
        """Memory manager'ı başlat"""
        try:
            self.memory_manager = EnhancedC64MemoryManager()
            return True
        except Exception as e:
            print(f"⚠️ Memory Manager başlatılamadı: {e}")
            return False
    
    def parse_instructions(self) -> bool:
        """PRG data'sını instruction'lara ayrıştır"""
        try:
            # py65 kullanarak disassemble et
            from py65.disassembler import Disassembler
            
            disasm = Disassembler()
            pc = self.start_address
            
            for i in range(len(self.prg_data)):
                if pc + i >= self.start_address + len(self.prg_data):
                    break
                
                try:
                    # Instruction parse et
                    length, disasm_str = disasm.instruction_at(pc + i, self.prg_data[i:i+3])
                    if length > 0:
                        instruction = {
                            'address': pc + i,
                            'bytes': self.prg_data[i:i+length],
                            'length': length,
                            'disassembly': disasm_str,
                            'mnemonic': disasm_str.split()[0] if disasm_str else '',
                            'operand': self._extract_operand(disasm_str)
                        }
                        self.instructions.append(instruction)
                        i += length - 1
                except:
                    # Parse edilemeyen byte'lar - data olabilir
                    self.data_areas.append(pc + i)
            
            print(f"✅ {len(self.instructions)} instruction parse edildi")
            return True
            
        except Exception as e:
            print(f"❌ Instruction parsing hatası: {e}")
            # Fallback - basit parsing
            return self._fallback_parsing()
    
    def _fallback_parsing(self) -> bool:
        """Basit fallback parsing"""
        # Temel instruction recognition
        pc = self.start_address
        i = 0
        
        while i < len(self.prg_data):
            opcode = self.prg_data[i]
            
            # Common opcodes ve length'leri
            length = 1
            mnemonic = "UNK"
            
            if opcode == 0xA9:  # LDA immediate
                length = 2
                mnemonic = "LDA"
            elif opcode == 0x20:  # JSR
                length = 3
                mnemonic = "JSR"
            elif opcode == 0x60:  # RTS
                length = 1
                mnemonic = "RTS"
            elif opcode == 0x4C:  # JMP absolute
                length = 3
                mnemonic = "JMP"
            elif opcode == 0x10:  # BPL
                length = 2
                mnemonic = "BPL"
            # Daha fazla opcode eklenebilir
            
            instruction = {
                'address': pc + i,
                'bytes': self.prg_data[i:i+length],
                'length': length,
                'mnemonic': mnemonic,
                'operand': None
            }
            
            if length > 1:
                if length == 2:
                    instruction['operand'] = self.prg_data[i+1]
                elif length == 3:
                    instruction['operand'] = self.prg_data[i+1] + (self.prg_data[i+2] << 8)
            
            self.instructions.append(instruction)
            i += length
        
        print(f"✅ Fallback: {len(self.instructions)} instruction parse edildi")
        return True
    
    def _extract_operand(self, disasm_str: str) -> Optional[int]:
        """Disassembly string'den operand'ı çıkar"""
        if not disasm_str or ' ' not in disasm_str:
            return None
        
        operand_part = disasm_str.split(' ', 1)[1]
        
        # $XXXX format
        if operand_part.startswith('$'):
            try:
                return int(operand_part[1:], 16)
            except:
                pass
        
        # #$XX format  
        if operand_part.startswith('#$'):
            try:
                return int(operand_part[2:], 16)
            except:
                pass
        
        return None
    
    def detect_loop_patterns(self) -> List[CodePattern]:
        """Döngü pattern'lerini tespit et"""
        loop_patterns = []
        
        for i, instruction in enumerate(self.instructions):
            # Counting loop pattern detection
            if instruction['mnemonic'] in ['LDX', 'LDY', 'LDA'] and i + 3 < len(self.instructions):
                # Pattern: LDX #count, loop:, ..., DEX, BNE loop
                
                if (instruction['mnemonic'] == 'LDX' and 
                    self._find_dex_bne_pattern(i)):
                    
                    pattern = CodePattern(
                        pattern_type=PatternType.COUNTING_LOOP,
                        start_address=instruction['address'],
                        end_address=self._find_loop_end(i),
                        confidence=0.8,
                        description="X register counting loop",
                        high_level_equivalent=f"for (int x = {instruction.get('operand', 0)}; x > 0; x--)",
                        optimization_suggestion="Consider using higher-level loop constructs"
                    )
                    loop_patterns.append(pattern)
        
        return loop_patterns
    
    def _find_dex_bne_pattern(self, start_idx: int) -> bool:
        """DEX + BNE pattern'i bul"""
        for i in range(start_idx + 1, min(start_idx + 20, len(self.instructions))):
            if (i + 1 < len(self.instructions) and
                self.instructions[i]['mnemonic'] == 'DEX' and
                self.instructions[i + 1]['mnemonic'] == 'BNE'):
                return True
        return False
    
    def _find_loop_end(self, start_idx: int) -> int:
        """Döngünün bitiş adresini bul"""
        for i in range(start_idx + 1, min(start_idx + 30, len(self.instructions))):
            if self.instructions[i]['mnemonic'] == 'BNE':
                return self.instructions[i]['address']
        return self.instructions[start_idx]['address']
    
    def detect_subroutine_patterns(self) -> List[CodePattern]:
        """Subroutine call pattern'lerini tespit et"""
        subroutine_patterns = []
        
        for instruction in self.instructions:
            if instruction['mnemonic'] == 'JSR':
                target_addr = instruction.get('operand')
                if target_addr:
                    # Memory manager ile routine ismi al
                    routine_name = "unknown_routine"
                    if self.memory_manager:
                        routine_name = self.memory_manager.get_smart_variable_name(target_addr)
                    
                    pattern = CodePattern(
                        pattern_type=PatternType.SUBROUTINE_CALL,
                        start_address=instruction['address'],
                        end_address=instruction['address'],
                        confidence=1.0,
                        description=f"Subroutine call to {routine_name}",
                        high_level_equivalent=f"{routine_name}();",
                        variables_used=[routine_name]
                    )
                    subroutine_patterns.append(pattern)
        
        return subroutine_patterns
    
    def detect_array_patterns(self) -> List[CodePattern]:
        """Array access pattern'lerini tespit et"""
        array_patterns = []
        
        for i, instruction in enumerate(self.instructions):
            # Array indexing pattern: LDA data,X veya STA data,X
            if (instruction['mnemonic'] in ['LDA', 'STA'] and 
                i > 0 and 
                self.instructions[i-1]['mnemonic'] in ['LDX', 'INX']):
                
                pattern = CodePattern(
                    pattern_type=PatternType.ARRAY_ACCESS,
                    start_address=self.instructions[i-1]['address'],
                    end_address=instruction['address'],
                    confidence=0.7,
                    description="Array access with X indexing",
                    high_level_equivalent="array[x]",
                    optimization_suggestion="Consider using pointer arithmetic"
                )
                array_patterns.append(pattern)
        
        return array_patterns
    
    def detect_math_patterns(self) -> List[CodePattern]:
        """Matematik pattern'lerini tespit et"""
        math_patterns = []
        
        for i, instruction in enumerate(self.instructions):
            # Multiplication pattern detection
            if (instruction['mnemonic'] == 'CLC' and 
                i + 2 < len(self.instructions) and
                self.instructions[i + 1]['mnemonic'] == 'ADC' and
                self.instructions[i + 2]['mnemonic'] == 'BCC'):
                
                pattern = CodePattern(
                    pattern_type=PatternType.MATH_OPERATION,
                    start_address=instruction['address'],
                    end_address=self.instructions[i + 2]['address'],
                    confidence=0.6,
                    description="Addition with carry handling",
                    high_level_equivalent="result = a + b;",
                    optimization_suggestion="Use high-level arithmetic operators"
                )
                math_patterns.append(pattern)
        
        return math_patterns
    
    def detect_screen_patterns(self) -> List[CodePattern]:
        """Screen manipulation pattern'lerini tespit et"""
        screen_patterns = []
        
        for instruction in self.instructions:
            operand = instruction.get('operand')
            if operand:
                # Screen memory ($0400-$07FF) veya color memory ($D800-$DBFF)
                if (0x0400 <= operand <= 0x07FF) or (0xD800 <= operand <= 0xDBFF):
                    pattern = CodePattern(
                        pattern_type=PatternType.SCREEN_MANIPULATION,
                        start_address=instruction['address'],
                        end_address=instruction['address'],
                        confidence=0.9,
                        description="Screen or color memory access",
                        high_level_equivalent="screen_write()",
                        optimization_suggestion="Use screen handling functions"
                    )
                    screen_patterns.append(pattern)
        
        return screen_patterns
    
    def analyze_all_patterns(self) -> AnalysisResult:
        """Tüm pattern'leri analiz et"""
        print("🔍 Pattern analysis başlıyor...")
        
        # Memory manager'ı başlat
        self.initialize_memory_manager()
        
        # Instructions'ları parse et
        if not self.parse_instructions():
            print("❌ Instruction parsing başarısız")
            return AnalysisResult([], 0.0, {}, {}, [], [])
        
        # Farklı pattern türlerini tespit et
        all_patterns = []
        
        print("   🔄 Loop patterns...")
        all_patterns.extend(self.detect_loop_patterns())
        
        print("   🔄 Subroutine patterns...")
        all_patterns.extend(self.detect_subroutine_patterns())
        
        print("   🔄 Array patterns...")
        all_patterns.extend(self.detect_array_patterns())
        
        print("   🔄 Math patterns...")
        all_patterns.extend(self.detect_math_patterns())
        
        print("   🔄 Screen patterns...")
        all_patterns.extend(self.detect_screen_patterns())
        
        # Complexity score hesapla
        complexity = self._calculate_complexity()
        
        # Memory usage analizi
        memory_usage = self._analyze_memory_usage()
        
        # Subroutine map oluştur
        subroutine_map = self._build_subroutine_map()
        
        # Optimization opportunities
        optimizations = self._generate_optimization_suggestions(all_patterns)
        
        print(f"✅ Pattern analysis tamamlandı: {len(all_patterns)} pattern tespit edildi")
        
        return AnalysisResult(
            patterns=all_patterns,
            complexity_score=complexity,
            memory_usage=memory_usage,
            subroutine_map=subroutine_map,
            data_structures=[],
            optimization_opportunities=optimizations
        )
    
    def _calculate_complexity(self) -> float:
        """Kod karmaşıklığını hesapla"""
        if not self.instructions:
            return 0.0
        
        complexity = 0.0
        
        # Instruction çeşitliliği
        unique_mnemonics = len(set(inst['mnemonic'] for inst in self.instructions))
        complexity += unique_mnemonics * 0.1
        
        # Branch instruction'ları (karmaşıklık artırır)
        branch_count = sum(1 for inst in self.instructions 
                          if inst['mnemonic'] in ['BEQ', 'BNE', 'BCC', 'BCS', 'BMI', 'BPL'])
        complexity += branch_count * 0.3
        
        # Subroutine call'ları
        jsr_count = sum(1 for inst in self.instructions if inst['mnemonic'] == 'JSR')
        complexity += jsr_count * 0.2
        
        # Normalize (0-10 scale)
        max_complexity = len(self.instructions) * 0.5
        normalized = min(complexity / max_complexity * 10, 10.0) if max_complexity > 0 else 0.0
        
        return normalized
    
    def _analyze_memory_usage(self) -> Dict[str, int]:
        """Memory kullanım pattern'lerini analiz et"""
        memory_usage = {
            'zero_page': 0,
            'stack': 0,
            'screen_memory': 0,
            'color_memory': 0,
            'basic_rom': 0,
            'kernal_rom': 0,
            'user_ram': 0
        }
        
        for instruction in self.instructions:
            operand = instruction.get('operand')
            if operand:
                if 0x00 <= operand <= 0xFF:
                    memory_usage['zero_page'] += 1
                elif 0x0100 <= operand <= 0x01FF:
                    memory_usage['stack'] += 1
                elif 0x0400 <= operand <= 0x07FF:
                    memory_usage['screen_memory'] += 1
                elif 0xD800 <= operand <= 0xDBFF:
                    memory_usage['color_memory'] += 1
                elif 0xA000 <= operand <= 0xBFFF:
                    memory_usage['basic_rom'] += 1
                elif 0xE000 <= operand <= 0xFFFF:
                    memory_usage['kernal_rom'] += 1
                else:
                    memory_usage['user_ram'] += 1
        
        return memory_usage
    
    def _build_subroutine_map(self) -> Dict[int, str]:
        """Subroutine map'i oluştur"""
        subroutine_map = {}
        
        for instruction in self.instructions:
            if instruction['mnemonic'] == 'JSR':
                addr = instruction.get('operand')
                if addr:
                    name = f"SUB_{addr:04X}"
                    if self.memory_manager:
                        name = self.memory_manager.get_smart_variable_name(addr)
                    subroutine_map[addr] = name
        
        return subroutine_map
    
    def _generate_optimization_suggestions(self, patterns: List[CodePattern]) -> List[str]:
        """Optimization önerilerini üret"""
        suggestions = []
        
        # Pattern-based suggestions
        loop_count = sum(1 for p in patterns if p.pattern_type == PatternType.COUNTING_LOOP)
        if loop_count > 3:
            suggestions.append("Consider using loop unrolling for performance")
        
        jsr_count = sum(1 for p in patterns if p.pattern_type == PatternType.SUBROUTINE_CALL)
        if jsr_count > 10:
            suggestions.append("High subroutine usage - consider inlining frequent calls")
        
        screen_count = sum(1 for p in patterns if p.pattern_type == PatternType.SCREEN_MANIPULATION)
        if screen_count > 5:
            suggestions.append("Multiple screen accesses - consider buffering")
        
        # General suggestions
        if len(self.instructions) > 100:
            suggestions.append("Large code size - consider modularization")
        
        return suggestions
    
    def generate_report(self, analysis_result: AnalysisResult) -> str:
        """Analiz raporu üret"""
        report = []
        report.append("=== CODE ANALYSIS REPORT ===")
        report.append(f"Total Instructions: {len(self.instructions)}")
        report.append(f"Complexity Score: {analysis_result.complexity_score:.1f}/10")
        report.append(f"Patterns Detected: {len(analysis_result.patterns)}")
        
        report.append("\n=== DETECTED PATTERNS ===")
        for pattern in analysis_result.patterns:
            report.append(f"• {pattern.pattern_type.value}: {pattern.description}")
            report.append(f"  Address: ${pattern.start_address:04X}")
            report.append(f"  High-level: {pattern.high_level_equivalent}")
            if pattern.optimization_suggestion:
                report.append(f"  Suggestion: {pattern.optimization_suggestion}")
        
        report.append("\n=== MEMORY USAGE ===")
        for area, count in analysis_result.memory_usage.items():
            if count > 0:
                report.append(f"• {area}: {count} accesses")
        
        report.append("\n=== OPTIMIZATION OPPORTUNITIES ===")
        for suggestion in analysis_result.optimization_opportunities:
            report.append(f"• {suggestion}")
        
        return "\n".join(report)


# Convenience functions
def analyze_prg_file(prg_data: bytes, start_address: int = 0x801) -> AnalysisResult:
    """
    PRG dosyasını analiz et
    
    Args:
        prg_data: PRG bytes
        start_address: Start address
    
    Returns:
        Analysis results
    """
    analyzer = CodeAnalyzer(prg_data, start_address)
    return analyzer.analyze_all_patterns()

def quick_pattern_check(prg_data: bytes) -> List[str]:
    """
    Hızlı pattern check
    
    Returns:
        Pattern descriptions list
    """
    analyzer = CodeAnalyzer(prg_data)
    result = analyzer.analyze_all_patterns()
    return [p.description for p in result.patterns]


if __name__ == "__main__":
    # Test için basit örnek
    print("=== CODE ANALYZER TEST ===")
    
    # Test PRG: LDA #65, JSR $FFD2, RTS (Hello World)
    test_prg = bytes.fromhex('a94120d2ff60')
    
    print(f"Test PRG: {test_prg.hex()}")
    
    analyzer = CodeAnalyzer(test_prg, 0x801)
    result = analyzer.analyze_all_patterns()
    
    print(f"\n=== ANALYSIS RESULTS ===")
    print(f"Patterns found: {len(result.patterns)}")
    print(f"Complexity score: {result.complexity_score:.1f}")
    
    for pattern in result.patterns:
        print(f"• {pattern.description}")
        print(f"  High-level: {pattern.high_level_equivalent}")
    
    # Generate report
    report = analyzer.generate_report(result)
    print(f"\n{report}")
