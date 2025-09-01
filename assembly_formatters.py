#!/usr/bin/env python3
"""
Assembly Formatters Module - Enhanced with C64 Knowledge Manager Integration
Disassembler Output Format System for Different Assemblers
Separate from decompiler languages (C, QBasic, PDSx)

This module handles ASSEMBLY output formatting for different assemblers:
- TASS (Turbo Assembler)  
- KickAssembler
- DASM
- CSS64
- SuperMon
- Native (Generic 6502)
- ACME
- CA65

Enhanced Features:
- Aşamalı bilgi verme sistemi (Natural/Basic/Annotated/Debug)
- Opcode açıklamaları ve cycle timing bilgileri
- Zero page değişken isimleri ve açıklamaları
- KERNAL/BASIC ROM fonksiyon tanımları
- VIC-II, SID, CIA donanım kayıt açıklamaları
- Bellek haritası tabanlı adres açıklamaları

Note: This is DIFFERENT from decompiler languages:
- C, QBasic, PDSx, C++, Commodore BASIC V2 are target LANGUAGES
- This module handles assembly FORMAT styles for different assemblers
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Knowledge Manager entegrasyonu - Enhanced Version
try:
    from c64_enhanced_knowledge_manager import EnhancedC64KnowledgeManager, KnowledgeLevel
    KNOWLEDGE_MANAGER_AVAILABLE = True
    print("✅ Enhanced C64 Knowledge Manager entegre edildi")
except ImportError:
    try:
        # Fallback: eski versiyon
        from c64_knowledge_manager import C64KnowledgeManager, KnowledgeLevel
        # Alias oluştur
        EnhancedC64KnowledgeManager = C64KnowledgeManager
        KNOWLEDGE_MANAGER_AVAILABLE = True
        print("✅ Legacy C64 Knowledge Manager entegre edildi")
    except ImportError:
        KNOWLEDGE_MANAGER_AVAILABLE = False
        print("⚠️ C64 Knowledge Manager bulunamadı, temel formatlar kullanılacak")

class AssemblyFormatters:
    """
    Assembly output formatters for different assembler syntaxes
    Enhanced with C64 Knowledge Manager for intelligent commenting
    """
    
    def __init__(self, knowledge_level: str = "basic"):
        self.logger = logging.getLogger(__name__)
        
        # Knowledge level mapping
        self.knowledge_levels = {
            'natural': KnowledgeLevel.NATURAL if KNOWLEDGE_MANAGER_AVAILABLE else None,
            'basic': KnowledgeLevel.BASIC if KNOWLEDGE_MANAGER_AVAILABLE else None,
            'annotated': KnowledgeLevel.ANNOTATED if KNOWLEDGE_MANAGER_AVAILABLE else None,
            'debug': KnowledgeLevel.DEBUG if KNOWLEDGE_MANAGER_AVAILABLE else None
        }
        
        # Set knowledge level
        self.current_knowledge_level = self.knowledge_levels.get(knowledge_level.lower())
        
        # Initialize knowledge manager if available
        self.knowledge_manager = None
        if KNOWLEDGE_MANAGER_AVAILABLE:
            try:
                self.knowledge_manager = EnhancedC64KnowledgeManager()
                print(f"✅ Assembly Formatters - Enhanced C64 Knowledge Manager entegre edildi: {knowledge_level.upper()} seviyesi")
            except Exception as e:
                print(f"⚠️ Enhanced Knowledge Manager başlatılamadı: {e}")
                self.knowledge_manager = None
        
        self.supported_formats = {
            'tass': 'TASS - Turbo Assembler',
            'kickass': 'KickAssembler', 
            'dasm': 'DASM',
            'css64': 'CSS64',
            'supermon': 'SuperMon',
            'native': 'Native 6502',
            'acme': 'ACME Assembler',
            'ca65': 'CA65 (cc65 Suite)',
            # Yeni hibrit formatlar
            'annotated': 'Annotated Assembly (Knowledge-Enhanced)',
            'structured': 'Structured Assembly (Control Flow)',
            'memory_mapped': 'Memory-Mapped Assembly (Hardware Aware)',
            'debug_trace': 'Debug/Trace Assembly (Full Analysis)'
        }
        
        # Format-specific syntax rules
        self.format_rules = self._load_format_rules()
        
    def _load_format_rules(self) -> Dict:
        """Load syntax rules for each assembler format"""
        return {
            'tass': {
                'comment_char': ';',
                'label_suffix': ':',
                'immediate_prefix': '#',
                'hex_prefix': '$',
                'bin_prefix': '%',
                'org_directive': '.org',
                'byte_directive': '.byte',
                'word_directive': '.word',
                'text_directive': '.text',
                'include_directive': '.include',
                'label_case': 'lower',
                'supports_expressions': True,
                'supports_macros': True
            },
            'kickass': {
                'comment_char': '//',
                'alt_comment': ';',
                'label_suffix': ':',
                'immediate_prefix': '#',
                'hex_prefix': '$',
                'bin_prefix': '%',
                'org_directive': '.pc',
                'byte_directive': '.byte',
                'word_directive': '.word',
                'text_directive': '.text',
                'include_directive': '.import',
                'label_case': 'mixed',
                'supports_expressions': True,
                'supports_macros': True,
                'special_features': ['namespaces', 'advanced_expressions']
            },
            'dasm': {
                'comment_char': ';',
                'label_suffix': '',
                'immediate_prefix': '#',
                'hex_prefix': '$',
                'bin_prefix': '%',
                'org_directive': 'ORG',
                'byte_directive': 'DC.B',
                'word_directive': 'DC.W',
                'text_directive': 'DC.B',
                'include_directive': 'INCLUDE',
                'label_case': 'upper',
                'supports_expressions': True,
                'supports_macros': True
            },
            'css64': {
                'comment_char': ';',
                'label_suffix': ':',
                'immediate_prefix': '#',
                'hex_prefix': '$',
                'bin_prefix': '%',
                'org_directive': '*=',
                'byte_directive': '.byte',
                'word_directive': '.word',
                'text_directive': '.text',
                'include_directive': '.include',
                'label_case': 'mixed',
                'supports_expressions': True,
                'supports_macros': False
            },
            'supermon': {
                'comment_char': ';',
                'label_suffix': '',
                'immediate_prefix': '#',
                'hex_prefix': '$',
                'bin_prefix': '%',
                'org_directive': '*=',
                'byte_directive': '.BYT',
                'word_directive': '.WOR',
                'text_directive': '.ASC',
                'include_directive': None,
                'label_case': 'upper',
                'supports_expressions': False,
                'supports_macros': False,
                'monitor_style': True
            },
            'native': {
                'comment_char': ';',
                'label_suffix': ':',
                'immediate_prefix': '#',
                'hex_prefix': '$',
                'bin_prefix': '%',
                'org_directive': 'ORG',
                'byte_directive': 'DB',
                'word_directive': 'DW',
                'text_directive': 'DB',
                'include_directive': 'INCLUDE',
                'label_case': 'mixed',
                'supports_expressions': True,
                'supports_macros': False
            },
            'acme': {
                'comment_char': ';',
                'label_suffix': '',
                'immediate_prefix': '#',
                'hex_prefix': '$',
                'bin_prefix': '%',
                'org_directive': '*=',
                'byte_directive': '!byte',
                'word_directive': '!word',
                'text_directive': '!text',
                'include_directive': '!source',
                'label_case': 'mixed',
                'supports_expressions': True,
                'supports_macros': True
            },
            'ca65': {
                'comment_char': ';',
                'label_suffix': ':',
                'immediate_prefix': '#',
                'hex_prefix': '$',
                'bin_prefix': '%',
                'org_directive': '.org',
                'byte_directive': '.byte',
                'word_directive': '.word',
                'text_directive': '.asciiz',
                'include_directive': '.include',
                'label_case': 'mixed',
                'supports_expressions': True,
                'supports_macros': True,
                'special_features': ['segments', 'scopes']
            }
        }
    
    def format_instruction(self, mnemonic: str, operand: str, address: int, 
                          format_type: str = 'native', comment: str = '') -> str:
        """
        Format a single instruction according to assembler syntax
        """
        if format_type not in self.supported_formats:
            self.logger.warning(f"Unsupported format: {format_type}, using native")
            format_type = 'native'
        
        rules = self.format_rules[format_type]
        
        # Handle mnemonic case
        if rules['label_case'] == 'upper':
            mnemonic = mnemonic.upper()
        elif rules['label_case'] == 'lower':
            mnemonic = mnemonic.lower()
        
        # Format operand if present
        formatted_operand = self._format_operand(operand, rules) if operand else ''
        
        # Build instruction line
        if formatted_operand:
            instruction = f"{mnemonic:<4} {formatted_operand}"
        else:
            instruction = mnemonic
        
        # Add comment if present
        if comment:
            comment_char = rules['comment_char']
            instruction = f"{instruction:<20} {comment_char} {comment}"
        
        return instruction
    
    def _format_operand(self, operand: str, rules: Dict) -> str:
        """Format operand according to assembler syntax rules"""
        if not operand:
            return ''
        
        # Handle immediate values
        if operand.startswith('#'):
            return operand  # Already formatted
        
        # Handle hex values
        if '$' in operand:
            return operand  # Already formatted
        
        # Handle other addressing modes
        return operand
    
    def format_label(self, label: str, format_type: str = 'native') -> str:
        """Format a label according to assembler syntax"""
        if format_type not in self.supported_formats:
            format_type = 'native'
        
        rules = self.format_rules[format_type]
        
        # Apply case rules
        if rules['label_case'] == 'upper':
            label = label.upper()
        elif rules['label_case'] == 'lower':
            label = label.lower()
        
        # Add suffix if required
        suffix = rules.get('label_suffix', '')
        return f"{label}{suffix}"
    
    def format_directive(self, directive_type: str, value: str, 
                        format_type: str = 'native') -> str:
        """Format assembler directives (ORG, BYTE, WORD, etc.)"""
        if format_type not in self.supported_formats:
            format_type = 'native'
        
        rules = self.format_rules[format_type]
        
        directive_map = {
            'org': rules['org_directive'],
            'byte': rules['byte_directive'], 
            'word': rules['word_directive'],
            'text': rules['text_directive']
        }
        
        if directive_type in directive_map:
            directive = directive_map[directive_type]
            return f"{directive} {value}"
        
        return f"{directive_type} {value}"
    
    def format_file_header(self, format_type: str = 'native', 
                          filename: str = '', start_address: int = 0) -> List[str]:
        """Generate file header for specific assembler format"""
        if format_type not in self.supported_formats:
            format_type = 'native'
        
        rules = self.format_rules[format_type]
        comment_char = rules['comment_char']
        header = []
        
        # Universal header
        header.append(f"{comment_char} Generated by D64 Converter v5.0")
        header.append(f"{comment_char} Assembler format: {self.supported_formats[format_type]}")
        if filename:
            header.append(f"{comment_char} Source file: {filename}")
        header.append(f"{comment_char} " + "="*50)
        header.append("")
        
        # Format-specific headers
        if format_type == 'kickass':
            header.append("// KickAssembler source file")
            header.append(".pc = $0801 \"Basic Upstart\"")
            header.append(".var music = LoadSid(\"music.sid\")")
            header.append("")
        elif format_type == 'tass':
            header.append(".cpu \"6502\"")
            header.append(f".org ${start_address:04x}")
            header.append("")
        elif format_type == 'dasm':
            header.append("        PROCESSOR 6502")
            header.append(f"        ORG ${start_address:04x}")
            header.append("")
        elif format_type == 'ca65':
            header.append(".setcpu \"6502\"")
            header.append(".segment \"CODE\"")
            header.append("")
        
        return header
    
    def get_format_info(self, format_type: str) -> Dict:
        """Get detailed information about a format"""
        if format_type not in self.supported_formats:
            return {}
        
        info = {
            'name': self.supported_formats[format_type],
            'rules': self.format_rules[format_type].copy(),
            'description': self._get_format_description(format_type)
        }
        return info
    
    def _get_format_description(self, format_type: str) -> str:
        """Get description for each format"""
        descriptions = {
            'tass': 'TASS Turbo Assembler - Popular C64 cross-assembler',
            'kickass': 'KickAssembler - Modern Java-based assembler with advanced features',
            'dasm': 'DASM - Multi-platform macro assembler',
            'css64': 'CSS64 - Cross-system assembler for C64',
            'supermon': 'SuperMon - C64 monitor/assembler syntax',
            'native': 'Generic 6502 assembly syntax',
            'acme': 'ACME - Cross-assembler for multiple processors',
            'ca65': 'CA65 - Part of cc65 C compiler suite',
            # Yeni hibrit formatlar
            'annotated': 'Knowledge-enhanced assembly with comprehensive comments',
            'structured': 'Assembly with control flow structure recognition',
            'memory_mapped': 'Hardware-aware assembly with register explanations',
            'debug_trace': 'Full debug assembly with timing and register analysis'
        }
        return descriptions.get(format_type, 'Unknown format')
    
    def list_supported_formats(self) -> Dict[str, str]:
        """Return dictionary of supported formats"""
        return self.supported_formats.copy()
    
    def convert_assembly_format(self, assembly_code: str, 
                               from_format: str, to_format: str) -> str:
        """Convert assembly from one format to another"""
        # This would be a complex conversion process
        # For now, return the original code with a header change
        if to_format not in self.supported_formats:
            self.logger.error(f"Unsupported target format: {to_format}")
            return assembly_code
        
        lines = assembly_code.split('\n')
        header = self.format_file_header(to_format)
        
        # Simple conversion - just add new header
        # More sophisticated conversion would parse and reformat each line
        converted_lines = [header] + lines
        return '\n'.join(converted_lines)

    # === YENİ HİBRİT FORMAT METODLARı ===
    
    def format_annotated_assembly(self, assembly_line: str, address: str = "", opcode_bytes: str = "") -> str:
        """
        Annotated Assembly Format - Knowledge Manager entegreli
        Maksimum bilgi ile zenginleştirilmiş assembly
        """
        if not self.knowledge_manager:
            return assembly_line
            
        # Temel satır formatı
        enhanced_line = assembly_line.strip()
        
        # Address bilgisi varsa ekle
        if address:
            addr_info = self.knowledge_manager.get_address_info(address, KnowledgeLevel.ANNOTATED)
            if addr_info:
                enhanced_line = f"{enhanced_line:<40} ; {address}: {addr_info}"
        
        # Opcode bytes varsa cycle timing ekle
        if opcode_bytes and self.current_knowledge_level == KnowledgeLevel.DEBUG:
            opcode_info = self.knowledge_manager.get_opcode_info(opcode_bytes[:2], KnowledgeLevel.DEBUG)
            if opcode_info:
                if ';' in enhanced_line:
                    enhanced_line += f" | {opcode_info}"
                else:
                    enhanced_line = f"{enhanced_line:<40} ; {opcode_info}"
        
        return enhanced_line
    
    def format_structured_assembly(self, assembly_line: str, 
                                 structure_info: Dict = None) -> str:
        """
        Structured Assembly Format - Kontrol akışı vurgulu
        FOR/IF/WHILE yapılarını tanıyan format
        """
        enhanced_line = assembly_line.strip()
        
        if structure_info:
            structure_type = structure_info.get('type', '')
            if structure_type in ['loop_start', 'loop_end', 'conditional', 'subroutine']:
                indent = "    " * structure_info.get('indent_level', 0)
                enhanced_line = f"{indent}{enhanced_line}"
                
                # Yapı açıklaması ekle
                if structure_type == 'loop_start':
                    enhanced_line += " ; [LOOP START]"
                elif structure_type == 'loop_end':
                    enhanced_line += " ; [LOOP END]"
                elif structure_type == 'conditional':
                    enhanced_line += " ; [CONDITIONAL]"
                elif structure_type == 'subroutine':
                    enhanced_line += " ; [SUBROUTINE]"
        
        return enhanced_line
    
    def format_memory_mapped_assembly(self, assembly_line: str, 
                                    hardware_context: Dict = None) -> str:
        """
        Memory-Mapped Assembly Format - Donanım bilinçli
        VIC-II, SID, CIA register açıklamaları
        """
        if not self.knowledge_manager:
            return assembly_line
            
        enhanced_line = self.knowledge_manager.enhance_assembly_line(
            assembly_line, 
            KnowledgeLevel.ANNOTATED
        )
        
        # Donanım konteksti varsa ekle
        if hardware_context:
            hw_type = hardware_context.get('type', '')
            if hw_type in ['vic', 'sid', 'cia']:
                hw_desc = hardware_context.get('description', '')
                if hw_desc:
                    enhanced_line += f" | {hw_type.upper()}: {hw_desc}"
        
        return enhanced_line
    
    def format_debug_trace_assembly(self, assembly_line: str,
                                  debug_info: Dict = None) -> str:
        """
        Debug/Trace Assembly Format - Tam analiz modu
        Cycle timing, register durumları, bellek etkiler
        """
        if not self.knowledge_manager:
            return assembly_line
            
        enhanced_line = self.knowledge_manager.enhance_assembly_line(
            assembly_line,
            KnowledgeLevel.DEBUG
        )
        
        # Debug bilgileri ekle
        if debug_info:
            debug_parts = []
            
            if 'cycles' in debug_info:
                debug_parts.append(f"Cycles: {debug_info['cycles']}")
            
            if 'registers_affected' in debug_info:
                debug_parts.append(f"Affects: {debug_info['registers_affected']}")
            
            if 'memory_access' in debug_info:
                debug_parts.append(f"Memory: {debug_info['memory_access']}")
                
            if 'flags_affected' in debug_info:
                debug_parts.append(f"Flags: {debug_info['flags_affected']}")
            
            if debug_parts:
                debug_comment = " | ".join(debug_parts)
                if ';' in enhanced_line:
                    enhanced_line += f" | {debug_comment}"
                else:
                    enhanced_line = f"{enhanced_line:<40} ; {debug_comment}"
        
        return enhanced_line
    
    def set_knowledge_level(self, level: str):
        """Bilgi seviyesini değiştir"""
        if level.lower() in self.knowledge_levels:
            self.current_knowledge_level = self.knowledge_levels[level.lower()]
            print(f"📊 Assembly Formatters bilgi seviyesi: {level.upper()}")
        else:
            print(f"⚠️ Geçersiz bilgi seviyesi: {level}")
            print(f"   Geçerli seviyeler: {list(self.knowledge_levels.keys())}")
    
    def generate_comprehensive_format(self, assembly_lines: List[str], 
                                    format_type: str = "annotated",
                                    include_statistics: bool = True) -> str:
        """
        Kapsamlı format oluşturucu
        Tüm assembly satırlarını seçilen formatta zenginleştirir
        """
        if not assembly_lines:
            return ""
        
        formatted_lines = []
        
        # Format header
        header = self.format_file_header(format_type)
        formatted_lines.append(header)
        formatted_lines.append("")
        
        # Statistik bilgileri
        if include_statistics and self.knowledge_manager:
            stats = self._generate_code_statistics(assembly_lines)
            formatted_lines.extend(stats)
            formatted_lines.append("")
        
        # Assembly satırlarını formatla
        for i, line in enumerate(assembly_lines):
            if not line.strip():
                formatted_lines.append("")
                continue
                
            # Format tipine göre işle
            if format_type == "annotated":
                formatted_line = self.format_annotated_assembly(line)
            elif format_type == "structured":
                formatted_line = self.format_structured_assembly(line)
            elif format_type == "memory_mapped":
                formatted_line = self.format_memory_mapped_assembly(line)
            elif format_type == "debug_trace":
                formatted_line = self.format_debug_trace_assembly(line)
            else:
                # Standart format
                formatted_line = self.format_assembly_line(line, format_type)
            
            formatted_lines.append(formatted_line)
        
        return '\n'.join(formatted_lines)
    
    def _generate_code_statistics(self, assembly_lines: List[str]) -> List[str]:
        """Kod istatistikleri oluştur"""
        stats = []
        stats.append("; === KOD İSTATİSTİKLERİ ===")
        stats.append(f"; Toplam satır sayısı: {len(assembly_lines)}")
        
        # Opcode analizi
        opcodes = {}
        addresses = set()
        
        for line in assembly_lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
                
            # Opcode sayımı
            parts = line.split()
            if parts:
                opcode = parts[0].upper()
                if opcode in ['LDA', 'STA', 'LDX', 'STX', 'LDY', 'STY', 
                             'JSR', 'JMP', 'BNE', 'BEQ', 'BCC', 'BCS',
                             'INC', 'DEC', 'CMP', 'CPX', 'CPY']:
                    opcodes[opcode] = opcodes.get(opcode, 0) + 1
        
        if opcodes:
            stats.append(f"; En çok kullanılan opcode'lar:")
            sorted_opcodes = sorted(opcodes.items(), key=lambda x: x[1], reverse=True)
            for opcode, count in sorted_opcodes[:5]:
                stats.append(f";   {opcode}: {count} kez")
        
        stats.append("; === KOD İSTATİSTİKLERİ SONU ===")
        return stats
        converted_lines = header + [line for line in lines if not line.startswith(';')]
        
        return '\n'.join(converted_lines)

# Example usage and testing
if __name__ == "__main__":
    formatter = AssemblyFormatters()
    
    # Test format listing
    print("🔧 Supported Assembly Formats:")
    for key, name in formatter.list_supported_formats().items():
        print(f"  {key}: {name}")
    
    print("\n" + "="*60)
    
    # Test instruction formatting
    test_instructions = [
        ("LDA", "#$41", 0x0800, "Load accumulator with 'A'"),
        ("STA", "$D020", 0x0803, "Store to border color"),
        ("JSR", "$FFD2", 0x0806, "Call CHROUT"),
        ("RTS", "", 0x0809, "Return from subroutine")
    ]
    
    formats_to_test = ['tass', 'kickass', 'dasm', 'native']
    
    for format_type in formats_to_test:
        print(f"\n📝 {formatter.supported_formats[format_type]} Format:")
        print("-" * 50)
        
        # Generate header
        header = formatter.format_file_header(format_type, "test.prg", 0x0800)
        for line in header:
            print(line)
        
        # Format instructions
        for mnemonic, operand, address, comment in test_instructions:
            formatted = formatter.format_instruction(
                mnemonic, operand, address, format_type, comment
            )
            print(f"${address:04x}: {formatted}")
    
    print(f"\n✅ Assembly Formatters Module Ready!")
    print(f"📊 Supports {len(formatter.supported_formats)} different assembler formats")
