"""
Performance Analyzer Plugin
===========================

Author: Enhanced AI System
Plugin Type: Analyzer
Description: 6502 Assembly performance analizi
Version: 1.0.0
"""

from typing import Dict, Any, List
import re
import sys
import os

# Plugin Manager import path düzeltmesi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from plugin_manager import IAnalyzerPlugin, PluginMetadata, PluginType
except ImportError:
    # Fallback için base classes
    from abc import ABC, abstractmethod
    from enum import Enum
    from dataclasses import dataclass
    
    class PluginType(Enum):
        ANALYZER = "analyzer"
    
    @dataclass
    class PluginMetadata:
        name: str
        version: str
        author: str
        description: str
        plugin_type: PluginType
        dependencies: list
        entry_point: str
    
    class IAnalyzerPlugin(ABC):
        @abstractmethod
        def get_metadata(self): pass
        @abstractmethod
        def initialize(self, context): pass
        @abstractmethod
        def cleanup(self): pass
        @abstractmethod
        def get_analysis_type(self): pass
        @abstractmethod
        def analyze(self, code, context=None): pass
        @abstractmethod
        def execute(self, *args, **kwargs): pass

class PerformanceAnalyzerPlugin(IAnalyzerPlugin):
    """6502 Assembly Performance Analyzer Plugin"""
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="performance_analyzer",
            version="1.0.0",
            author="Enhanced AI System", 
            description="6502 Assembly performance and cycle count analyzer",
            plugin_type=PluginType.ANALYZER,
            dependencies=[],
            entry_point="PerformanceAnalyzerPlugin"
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        self.context = context
        
        # 6502 instruction cycle counts
        self.cycle_counts = {
            # Load/Store
            'LDA': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_x': 4, 'indexed_y': 4, 'indirect_x': 6, 'indirect_y': 5},
            'LDX': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_y': 4},
            'LDY': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_x': 4},
            'STA': {'zeropage': 3, 'absolute': 4, 'indexed_x': 5, 'indexed_y': 5, 'indirect_x': 6, 'indirect_y': 6},
            'STX': {'zeropage': 3, 'absolute': 4, 'indexed_y': 4},
            'STY': {'zeropage': 3, 'absolute': 4, 'indexed_x': 4},
            
            # Transfer
            'TAX': {'implied': 2}, 'TAY': {'implied': 2}, 'TXA': {'implied': 2}, 'TYA': {'implied': 2},
            'TSX': {'implied': 2}, 'TXS': {'implied': 2},
            
            # Stack
            'PHA': {'implied': 3}, 'PHP': {'implied': 3}, 'PLA': {'implied': 4}, 'PLP': {'implied': 4},
            
            # Arithmetic
            'ADC': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_x': 4, 'indexed_y': 4, 'indirect_x': 6, 'indirect_y': 5},
            'SBC': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_x': 4, 'indexed_y': 4, 'indirect_x': 6, 'indirect_y': 5},
            
            # Increment/Decrement
            'INX': {'implied': 2}, 'INY': {'implied': 2}, 'DEX': {'implied': 2}, 'DEY': {'implied': 2},
            'INC': {'zeropage': 5, 'absolute': 6, 'indexed_x': 7},
            'DEC': {'zeropage': 5, 'absolute': 6, 'indexed_x': 7},
            
            # Shift/Rotate
            'ASL': {'accumulator': 2, 'zeropage': 5, 'absolute': 6, 'indexed_x': 7},
            'LSR': {'accumulator': 2, 'zeropage': 5, 'absolute': 6, 'indexed_x': 7},
            'ROL': {'accumulator': 2, 'zeropage': 5, 'absolute': 6, 'indexed_x': 7},
            'ROR': {'accumulator': 2, 'zeropage': 5, 'absolute': 6, 'indexed_x': 7},
            
            # Logic
            'AND': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_x': 4, 'indexed_y': 4, 'indirect_x': 6, 'indirect_y': 5},
            'ORA': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_x': 4, 'indexed_y': 4, 'indirect_x': 6, 'indirect_y': 5},
            'EOR': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_x': 4, 'indexed_y': 4, 'indirect_x': 6, 'indirect_y': 5},
            
            # Compare
            'CMP': {'immediate': 2, 'zeropage': 3, 'absolute': 4, 'indexed_x': 4, 'indexed_y': 4, 'indirect_x': 6, 'indirect_y': 5},
            'CPX': {'immediate': 2, 'zeropage': 3, 'absolute': 4},
            'CPY': {'immediate': 2, 'zeropage': 3, 'absolute': 4},
            
            # Branch (2 cycles if not taken, 3 if taken, +1 if page boundary crossed)
            'BCC': {'relative': 2}, 'BCS': {'relative': 2}, 'BEQ': {'relative': 2}, 'BNE': {'relative': 2},
            'BMI': {'relative': 2}, 'BPL': {'relative': 2}, 'BVC': {'relative': 2}, 'BVS': {'relative': 2},
            
            # Jump
            'JMP': {'absolute': 3, 'indirect': 5},
            'JSR': {'absolute': 6},
            'RTS': {'implied': 6},
            'RTI': {'implied': 6},
            
            # Flag operations
            'CLC': {'implied': 2}, 'SEC': {'implied': 2}, 'CLI': {'implied': 2}, 'SEI': {'implied': 2},
            'CLV': {'implied': 2}, 'CLD': {'implied': 2}, 'SED': {'implied': 2},
            
            # Misc
            'BIT': {'zeropage': 3, 'absolute': 4},
            'NOP': {'implied': 2},
            'BRK': {'implied': 7}
        }
        
        # Performance patterns to detect
        self.performance_patterns = {
            'redundant_loads': r'(LDA\s+[^;]+)\s*\n\s*\1',  # Consecutive identical loads
            'redundant_stores': r'(STA\s+[^;]+)\s*\n\s*\1',  # Consecutive identical stores
            'unnecessary_transfers': r'TAX\s*\n\s*TXA',  # Transfer A to X then back
            'dead_code': r'JMP\s+\w+\s*\n\s*[^:\n]+',  # Code after unconditional jump
        }
        
        return True
    
    def cleanup(self) -> None:
        pass
    
    def get_analysis_type(self) -> str:
        return "Performance"
    
    def analyze(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """6502 Assembly performance analizi"""
        lines = code.split('\n')
        analysis_result = {
            "analysis_type": "Performance",
            "total_cycles": 0,
            "instruction_count": 0,
            "performance_issues": [],
            "optimizations": [],
            "cycle_breakdown": {},
            "hotspots": [],
            "summary": "",
            "success": True
        }
        
        try:
            # Instruction analysis
            for line_no, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith(';') or line.endswith(':'):
                    continue
                
                # Parse instruction
                instruction_info = self._parse_instruction(line)
                if instruction_info:
                    analysis_result["instruction_count"] += 1
                    
                    # Calculate cycles
                    cycles = self._calculate_cycles(instruction_info)
                    analysis_result["total_cycles"] += cycles
                    
                    # Update cycle breakdown
                    opcode = instruction_info["opcode"]
                    if opcode not in analysis_result["cycle_breakdown"]:
                        analysis_result["cycle_breakdown"][opcode] = {"count": 0, "cycles": 0}
                    analysis_result["cycle_breakdown"][opcode]["count"] += 1
                    analysis_result["cycle_breakdown"][opcode]["cycles"] += cycles
                    
                    # Check for performance issues
                    issues = self._check_performance_issues(line, line_no)
                    analysis_result["performance_issues"].extend(issues)
            
            # Pattern analysis
            pattern_issues = self._analyze_patterns(code)
            analysis_result["performance_issues"].extend(pattern_issues)
            
            # Generate optimizations
            analysis_result["optimizations"] = self._generate_optimizations(analysis_result)
            
            # Find hotspots
            analysis_result["hotspots"] = self._find_hotspots(analysis_result["cycle_breakdown"])
            
            # Generate summary
            analysis_result["summary"] = self._generate_summary(analysis_result)
            
        except Exception as e:
            analysis_result["success"] = False
            analysis_result["error"] = str(e)
        
        return analysis_result
    
    def _parse_instruction(self, line: str) -> Dict[str, Any]:
        """Assembly instruction'ını parse et"""
        parts = line.split()
        if not parts:
            return None
        
        opcode = parts[0].upper()
        operand = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        # Determine addressing mode
        addressing_mode = self._determine_addressing_mode(operand)
        
        return {
            "opcode": opcode,
            "operand": operand,
            "addressing_mode": addressing_mode,
            "full_instruction": line
        }
    
    def _determine_addressing_mode(self, operand: str) -> str:
        """Addressing mode'unu belirle"""
        if not operand:
            return "implied"
        elif operand.startswith('#'):
            return "immediate"
        elif operand.startswith('(') and operand.endswith(',X)'):
            return "indirect_x"
        elif operand.startswith('(') and operand.endswith('),Y'):
            return "indirect_y"
        elif operand.startswith('(') and operand.endswith(')'):
            return "indirect"
        elif operand.endswith(',X'):
            addr = operand[:-2].strip()
            if addr.startswith('$') and len(addr) <= 3:  # $00-$FF
                return "zeropage_x"
            else:
                return "indexed_x"
        elif operand.endswith(',Y'):
            addr = operand[:-2].strip()
            if addr.startswith('$') and len(addr) <= 3:  # $00-$FF
                return "zeropage_y"
            else:
                return "indexed_y"
        elif operand.startswith('$') and len(operand) <= 3:  # $00-$FF
            return "zeropage"
        else:
            return "absolute"
    
    def _calculate_cycles(self, instruction_info: Dict[str, Any]) -> int:
        """Instruction için cycle sayısını hesapla"""
        opcode = instruction_info["opcode"]
        addressing_mode = instruction_info["addressing_mode"]
        
        if opcode not in self.cycle_counts:
            return 2  # Default cycle count
        
        cycles_for_opcode = self.cycle_counts[opcode]
        
        # Direct match
        if addressing_mode in cycles_for_opcode:
            return cycles_for_opcode[addressing_mode]
        
        # Fallback mappings
        fallback_map = {
            "zeropage_x": "indexed_x",
            "zeropage_y": "indexed_y"
        }
        
        if addressing_mode in fallback_map:
            fallback_mode = fallback_map[addressing_mode]
            if fallback_mode in cycles_for_opcode:
                return cycles_for_opcode[fallback_mode]
        
        # Default to first available cycle count
        return list(cycles_for_opcode.values())[0]
    
    def _check_performance_issues(self, line: str, line_no: int) -> List[Dict[str, Any]]:
        """Performance sorunlarını kontrol et"""
        issues = []
        
        # Inefficient operations
        if "BRK" in line.upper():
            issues.append({
                "type": "inefficient_operation",
                "line": line_no,
                "severity": "high",
                "description": "BRK instruction is very slow (7 cycles)",
                "suggestion": "Avoid BRK unless necessary for debugging"
            })
        
        # Expensive indirect addressing
        if ")" in line and "," in line:
            issues.append({
                "type": "expensive_addressing",
                "line": line_no,
                "severity": "medium", 
                "description": "Indirect indexed addressing is expensive",
                "suggestion": "Consider using direct addressing when possible"
            })
        
        return issues
    
    def _analyze_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Code pattern'lerini analiz et"""
        issues = []
        
        for pattern_name, pattern in self.performance_patterns.items():
            matches = re.finditer(pattern, code, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                line_no = code[:match.start()].count('\n') + 1
                issues.append({
                    "type": "pattern_issue",
                    "pattern": pattern_name,
                    "line": line_no,
                    "severity": "medium",
                    "description": f"Detected {pattern_name.replace('_', ' ')}",
                    "suggestion": self._get_pattern_suggestion(pattern_name)
                })
        
        return issues
    
    def _get_pattern_suggestion(self, pattern_name: str) -> str:
        """Pattern için optimizasyon önerisi"""
        suggestions = {
            "redundant_loads": "Remove redundant load operations",
            "redundant_stores": "Remove redundant store operations", 
            "unnecessary_transfers": "Eliminate unnecessary register transfers",
            "dead_code": "Remove code after unconditional jump"
        }
        return suggestions.get(pattern_name, "Optimize this pattern")
    
    def _generate_optimizations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Optimizasyon önerileri üret"""
        optimizations = []
        
        # High cycle count instructions
        for opcode, info in analysis["cycle_breakdown"].items():
            if info["cycles"] / info["count"] > 5:  # Average > 5 cycles
                optimizations.append({
                    "type": "high_cycle_instruction",
                    "instruction": opcode,
                    "description": f"{opcode} instruction has high cycle count",
                    "suggestion": f"Consider alternatives to {opcode} for better performance"
                })
        
        # Total cycle optimization
        total_cycles = analysis["total_cycles"]
        if total_cycles > 1000:
            optimizations.append({
                "type": "overall_optimization",
                "description": f"Total cycle count is high ({total_cycles} cycles)",
                "suggestion": "Consider loop unrolling or algorithm optimization"
            })
        
        return optimizations
    
    def _find_hotspots(self, cycle_breakdown: Dict[str, Dict[str, int]]) -> List[Dict[str, Any]]:
        """Performance hotspot'larını bul"""
        hotspots = []
        
        # Sort by total cycles
        sorted_instructions = sorted(
            cycle_breakdown.items(),
            key=lambda x: x[1]["cycles"],
            reverse=True
        )
        
        # Top 3 most expensive instructions
        for i, (opcode, info) in enumerate(sorted_instructions[:3]):
            hotspots.append({
                "rank": i + 1,
                "instruction": opcode,
                "total_cycles": info["cycles"],
                "count": info["count"],
                "avg_cycles": info["cycles"] / info["count"]
            })
        
        return hotspots
    
    def _generate_summary(self, analysis: Dict[str, Any]) -> str:
        """Analiz özeti oluştur"""
        total_cycles = analysis["total_cycles"]
        instruction_count = analysis["instruction_count"]
        issue_count = len(analysis["performance_issues"])
        
        summary = f"Performance Analysis Summary:\n"
        summary += f"- Total Instructions: {instruction_count}\n"
        summary += f"- Total Cycles: {total_cycles}\n"
        summary += f"- Average Cycles per Instruction: {total_cycles/instruction_count:.2f}\n"
        summary += f"- Performance Issues Found: {issue_count}\n"
        
        if analysis["hotspots"]:
            top_hotspot = analysis["hotspots"][0]
            summary += f"- Top Hotspot: {top_hotspot['instruction']} ({top_hotspot['total_cycles']} cycles)\n"
        
        # Performance rating
        avg_cycles = total_cycles / instruction_count if instruction_count > 0 else 0
        if avg_cycles < 3:
            rating = "Excellent"
        elif avg_cycles < 4:
            rating = "Good"
        elif avg_cycles < 5:
            rating = "Average"
        else:
            rating = "Needs Optimization"
        
        summary += f"- Performance Rating: {rating}"
        
        return summary
    
    def execute(self, *args, **kwargs) -> Any:
        """Plugin'in ana işlevi"""
        if args:
            return self.analyze(*args, **kwargs)
        return {"status": "ready", "analysis_type": "Performance"}

# Plugin class'ını export et
__all__ = ['PerformanceAnalyzerPlugin']
