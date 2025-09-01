"""
Rust Transpiler Plugin
======================

Author: Enhanced AI System
Plugin Type: Transpiler  
Description: Assembly → Rust transpiler with 6502 support
Version: 1.0.0
"""

from typing import Dict, Any
import re
import sys
import os

# Plugin Manager import path düzeltmesi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from plugin_manager import ITranspilerPlugin, PluginMetadata, PluginType
except ImportError:
    # Fallback için base classes
    from abc import ABC, abstractmethod
    from enum import Enum
    from dataclasses import dataclass
    
    class PluginType(Enum):
        TRANSPILER = "transpiler"
    
    @dataclass  
    class PluginMetadata:
        name: str
        version: str
        author: str
        description: str
        plugin_type: PluginType
        dependencies: list
        entry_point: str
    
    class ITranspilerPlugin(ABC):
        @abstractmethod
        def get_metadata(self): pass
        @abstractmethod
        def initialize(self, context): pass
        @abstractmethod
        def cleanup(self): pass
        @abstractmethod
        def get_target_language(self): pass
        @abstractmethod
        def get_file_extension(self): pass
        @abstractmethod
        def transpile(self, assembly_code, options=None): pass
        @abstractmethod
        def execute(self, *args, **kwargs): pass

class RustTranspilerPlugin(ITranspilerPlugin):
    """Assembly → Rust Transpiler Plugin"""
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="rust_transpiler",
            version="1.0.0", 
            author="Enhanced AI System",
            description="Assembly to Rust transpiler with 6502 emulation",
            plugin_type=PluginType.TRANSPILER,
            dependencies=[],
            entry_point="RustTranspilerPlugin"
        )
    
    def initialize(self, context: Dict[str, Any]) -> bool:
        self.context = context
        
        # 6502 instruction mapping to Rust
        self.instruction_map = {
            'LDA': 'load_accumulator',
            'LDX': 'load_x_register', 
            'LDY': 'load_y_register',
            'STA': 'store_accumulator',
            'STX': 'store_x_register',
            'STY': 'store_y_register',
            'TAX': 'transfer_a_to_x',
            'TAY': 'transfer_a_to_y', 
            'TXA': 'transfer_x_to_a',
            'TYA': 'transfer_y_to_a',
            'INX': 'increment_x',
            'INY': 'increment_y',
            'DEX': 'decrement_x',
            'DEY': 'decrement_y',
            'ADC': 'add_with_carry',
            'SBC': 'subtract_with_carry',
            'CMP': 'compare_accumulator',
            'CPX': 'compare_x_register',
            'CPY': 'compare_y_register',
            'JMP': 'jump',
            'JSR': 'jump_subroutine',
            'RTS': 'return_from_subroutine',
            'BEQ': 'branch_if_equal',
            'BNE': 'branch_if_not_equal',
            'BCC': 'branch_if_carry_clear',
            'BCS': 'branch_if_carry_set',
            'BMI': 'branch_if_minus',
            'BPL': 'branch_if_plus',
            'BVC': 'branch_if_overflow_clear', 
            'BVS': 'branch_if_overflow_set',
            'CLC': 'clear_carry_flag',
            'SEC': 'set_carry_flag',
            'CLD': 'clear_decimal_flag',
            'SED': 'set_decimal_flag',
            'CLI': 'clear_interrupt_flag',
            'SEI': 'set_interrupt_flag',
            'CLV': 'clear_overflow_flag',
            'NOP': 'no_operation'
        }
        
        # Register mappings
        self.registers = {
            'A': 'cpu.accumulator',
            'X': 'cpu.x_register', 
            'Y': 'cpu.y_register',
            'SP': 'cpu.stack_pointer'
        }
        
        return True
    
    def cleanup(self) -> None:
        pass
    
    def get_target_language(self) -> str:
        return "Rust"
    
    def get_file_extension(self) -> str:
        return ".rs"
    
    def transpile(self, assembly_code: str, options: Dict[str, Any] = None) -> str:
        """Assembly'yi Rust'a çevir"""
        if not assembly_code:
            return ""
        
        lines = assembly_code.split('\n')
        rust_code = []
        
        # Rust header
        rust_code.extend([
            "// Generated Rust code from 6502 Assembly",
            "// Transpiled by Rust Transpiler Plugin",
            "",
            "use std::collections::HashMap;",
            "",
            "#[derive(Debug, Clone)]",
            "pub struct Cpu6502 {",
            "    pub accumulator: u8,",
            "    pub x_register: u8,", 
            "    pub y_register: u8,",
            "    pub stack_pointer: u8,",
            "    pub program_counter: u16,",
            "    pub status_flags: u8,",
            "    pub memory: [u8; 65536],",
            "}",
            "",
            "impl Cpu6502 {",
            "    pub fn new() -> Self {",
            "        Self {",
            "            accumulator: 0,",
            "            x_register: 0,",
            "            y_register: 0,", 
            "            stack_pointer: 0xFF,",
            "            program_counter: 0,",
            "            status_flags: 0,",
            "            memory: [0; 65536],",
            "        }",
            "    }",
            "",
            "    pub fn execute_program(&mut self) -> Result<(), String> {",
            "        // Generated assembly execution"
        ])
        
        # Process assembly lines
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';') or line.startswith('//'):
                if line.startswith(';'):
                    rust_code.append(f"        // {line[1:].strip()}")
                elif line.startswith('//'):
                    rust_code.append(f"        {line}")
                continue
            
            # Handle labels
            if line.endswith(':'):
                label = line[:-1].strip()
                rust_code.append(f"        // Label: {label}")
                continue
            
            # Handle directives
            if line.upper().startswith(('ORG', 'EQU', 'DC.', 'DS.')):
                rust_code.append(f"        // Directive: {line}")
                continue
            
            # Transpile instruction
            rust_instruction = self._transpile_instruction(line)
            if rust_instruction:
                rust_code.append(f"        {rust_instruction}")
        
        # Rust footer
        rust_code.extend([
            "",
            "        Ok(())",
            "    }",
            "",
            "    // Helper methods for 6502 operations"
        ])
        
        # Add helper methods
        rust_code.extend(self._generate_helper_methods())
        
        rust_code.extend([
            "}",
            "",
            "fn main() {", 
            "    let mut cpu = Cpu6502::new();",
            "    match cpu.execute_program() {",
            "        Ok(()) => println!(\"Program executed successfully\"),",
            "        Err(e) => eprintln!(\"Error: {}\", e),",
            "    }",
            "}"
        ])
        
        return '\n'.join(rust_code)
    
    def _transpile_instruction(self, instruction: str) -> str:
        """Tek assembly instruction'ını Rust'a çevir"""
        parts = instruction.split()
        if not parts:
            return ""
        
        opcode = parts[0].upper()
        operand = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        if opcode not in self.instruction_map:
            return f"// Unknown instruction: {instruction}"
        
        rust_method = self.instruction_map[opcode]
        
        # Handle different addressing modes
        if not operand:
            # Implied addressing
            return f"self.{rust_method}();"
        
        # Immediate addressing
        if operand.startswith('#'):
            value = operand[1:]
            if value.startswith('$'):
                value = f"0x{value[1:]}"
            return f"self.{rust_method}_immediate({value});"
        
        # Register operations
        if operand in self.registers:
            return f"self.{rust_method}();"
        
        # Memory addressing
        if operand.startswith('$'):
            addr = f"0x{operand[1:]}"
            return f"self.{rust_method}_absolute({addr});"
        
        # Indexed addressing
        if ',X' in operand:
            addr = operand.replace(',X', '')
            if addr.startswith('$'):
                addr = f"0x{addr[1:]}"
            return f"self.{rust_method}_indexed_x({addr});"
        
        if ',Y' in operand:
            addr = operand.replace(',Y', '') 
            if addr.startswith('$'):
                addr = f"0x{addr[1:]}"
            return f"self.{rust_method}_indexed_y({addr});"
        
        # Default case
        if operand.startswith('$'):
            addr = f"0x{operand[1:]}"
            return f"self.{rust_method}_absolute({addr});"
        
        return f"self.{rust_method}(); // {operand}"
    
    def _generate_helper_methods(self) -> list:
        """6502 emülasyon için helper methodlar"""
        return [
            "",
            "    // Load operations",
            "    fn load_accumulator_immediate(&mut self, value: u8) {",
            "        self.accumulator = value;",
            "        self.update_zero_negative_flags(self.accumulator);",
            "    }",
            "",
            "    fn load_accumulator_absolute(&mut self, address: u16) {",
            "        self.accumulator = self.memory[address as usize];",
            "        self.update_zero_negative_flags(self.accumulator);", 
            "    }",
            "",
            "    fn load_x_register_immediate(&mut self, value: u8) {",
            "        self.x_register = value;",
            "        self.update_zero_negative_flags(self.x_register);",
            "    }",
            "",
            "    fn load_y_register_immediate(&mut self, value: u8) {",
            "        self.y_register = value;",
            "        self.update_zero_negative_flags(self.y_register);",
            "    }",
            "",
            "    // Store operations", 
            "    fn store_accumulator_absolute(&mut self, address: u16) {",
            "        self.memory[address as usize] = self.accumulator;",
            "    }",
            "",
            "    // Transfer operations",
            "    fn transfer_a_to_x(&mut self) {",
            "        self.x_register = self.accumulator;",
            "        self.update_zero_negative_flags(self.x_register);",
            "    }",
            "",
            "    fn transfer_a_to_y(&mut self) {",
            "        self.y_register = self.accumulator;",
            "        self.update_zero_negative_flags(self.y_register);",
            "    }",
            "",
            "    // Arithmetic operations",
            "    fn add_with_carry_immediate(&mut self, value: u8) {",
            "        let carry = if self.status_flags & 0x01 != 0 { 1 } else { 0 };",
            "        let result = self.accumulator as u16 + value as u16 + carry;",
            "        ",
            "        self.status_flags &= !0x01; // Clear carry",
            "        if result > 255 {",
            "            self.status_flags |= 0x01; // Set carry",
            "        }",
            "        ",
            "        self.accumulator = (result & 0xFF) as u8;",
            "        self.update_zero_negative_flags(self.accumulator);",
            "    }",
            "",
            "    // Utility methods",
            "    fn update_zero_negative_flags(&mut self, value: u8) {",
            "        self.status_flags &= !0x82; // Clear zero and negative flags",
            "        if value == 0 {",
            "            self.status_flags |= 0x02; // Set zero flag",
            "        }",
            "        if value & 0x80 != 0 {", 
            "            self.status_flags |= 0x80; // Set negative flag",
            "        }",
            "    }",
            "",
            "    fn no_operation(&mut self) {",
            "        // NOP - do nothing",
            "    }"
        ]
    
    def execute(self, *args, **kwargs) -> Any:
        """Plugin'in ana işlevi"""
        if args:
            return self.transpile(*args, **kwargs)
        return {"status": "ready", "target_language": "Rust"}

# Plugin class'ını export et
__all__ = ['RustTranspilerPlugin']
