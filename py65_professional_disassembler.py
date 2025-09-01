"""

py65_professional_disassembler.py
Profesyonel 6502 Disassembler Modülü
py65 kütüphanesi kullanarak gelişmiş disassembly özellikleri

🍎 Py65 Professional Disassembler v5.3 - Commodore 64 Geliştirme Stüdyosu
================================================================
PROJE: KızılElma Ana Plan - Enhanced Universal Disk Reader v2.0 → C64 Development Studio
MODÜL: py65_professional_disassembler.py - Professional py65 Disassembler Motoru
VERSİYON: 5.3 (4 Disassembler Motor - "py65_professional" seçeneği)
AMAÇ: py65 kütüphanesi ile profesyonel seviye 6502 disassembly
================================================================

Bu modül 4 Disassembler Motor sisteminin "py65_professional" motorudur:
• py65 Library Integration: Güçlü py65 kütüphane desteği
• Professional Features: 6502 instruction-level analiz
• Advanced Disassembly: Opcode-level detaylı çözümleme
• Memory Mapping: Gelişmiş bellek haritalama
• GUI Integration: 4 Disassembler dropdown'ında "py65_professional" seçeneği

4 Disassembler Motor Sistemi:
1. basic - Temel disassembler
2. advanced - Gelişmiş özellikli disassembler
3. improved - C64 Enhanced disassembler  
4. py65_professional - Bu modül (Professional py65 library)

Profesyonel 6502 Disassembler Modülü - py65 kütüphanesi ile gelişmiş özellikler
================================================================
"""

import os
import sys
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
from data_loader import DataLoader
import disassembly_formatter

# py65 kütüphanesini güvenli import
try:
    from py65.devices.mpu6502 import MPU
    from py65.memory import ObservableMemory
    from py65.disassembler import Disassembler
    from py65.utils.addressing import AddressParser
    PY65_AVAILABLE = True
    print("✓ py65 kütüphanesi başarıyla yüklendi")
except ImportError as e:
    PY65_AVAILABLE = False
    print(f"✗ py65 kütüphanesi yüklenemedi: {e}")
    print("  Çözüm: venv_asmto ortamında çalıştırın veya py65'i sistem Python'una yükleyin")

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddressingMode(Enum):
    """6502 Addressing Mode enumeration"""
    ACCUMULATOR = "acc"
    ABSOLUTE = "abs"
    ABSOLUTE_X = "abx"
    ABSOLUTE_Y = "aby"
    IMMEDIATE = "imm"
    IMPLIED = "imp"
    INDIRECT = "ind"
    INDIRECT_Y = "iny"
    INDIRECT_X = "inx"
    INDIRECT_ABSOLUTE_X = "iax"
    RELATIVE = "rel"
    ZERO_PAGE_INDIRECT = "zpi"
    ZERO_PAGE = "zpg"
    ZERO_PAGE_X = "zpx"
    ZERO_PAGE_Y = "zpy"

class InstructionType(Enum):
    """Instruction type classification"""
    SEQUENTIAL = "sequential"
    BRANCH = "branch"
    JUMP = "jump"
    CALL = "call"
    RETURN = "return"
    INTERRUPT = "interrupt"
    ILLEGAL = "illegal"

class SymbolType(Enum):
    """Symbol type classification"""
    LABEL = "label"
    SUBROUTINE = "subroutine"
    VARIABLE = "variable"
    CONSTANT = "constant"
    ENTRY_POINT = "entry_point"
    KERNAL_CALL = "kernal_call"
    VECTOR = "vector"

@dataclass
class Symbol:
    """Symbol information"""
    name: str
    address: int
    symbol_type: SymbolType
    references: List[int]
    comment: str = ""
    
    def __post_init__(self):
        if not self.references:
            self.references = []

@dataclass
class CodeFlowInfo:
    """Code flow analysis information"""
    instruction_type: InstructionType
    targets: List[int]
    is_branch: bool = False
    is_jump: bool = False
    is_call: bool = False
    is_return: bool = False
    condition: str = ""
    
    def __post_init__(self):
        if not self.targets:
            self.targets = []

@dataclass
class DisassemblyResult:
    """Disassembly result for a single instruction"""
    address: int
    bytes: List[int]
    instruction: str
    mnemonic: str
    operand: str
    addressing_mode: AddressingMode
    length: int
    symbol: Optional[Symbol] = None
    comment: str = ""
    flow_info: Optional[CodeFlowInfo] = None
    cycle_count: int = 0

class Py65ProfessionalDisassembler:
    """
    Profesyonel 6502 Disassembler
    py65 kütüphanesi kullanarak gelişmiş disassembly özellikleri
    """
    
    def __init__(self, memory_size: int = 0x10000):
        """
        Disassembler başlatma
        
        Args:
            memory_size: Bellek boyutu (default: 64KB)
        """
        if not PY65_AVAILABLE:
            raise ImportError("py65 kütüphanesi gerekli ancak yüklü değil")
        
        self.memory_size = memory_size
        self.memory = ObservableMemory()
        self.mpu = MPU(memory=self.memory)
        self.disassembler = Disassembler(self.mpu)
        self.address_parser = AddressParser()
        
        # Symbol management
        self.symbol_table: Dict[int, Symbol] = {}
        self.reverse_symbol_table: Dict[str, int] = {}
        
        # Code analysis
        self.code_blocks: List[Tuple[int, int]] = []
        self.data_blocks: List[Tuple[int, int]] = []
        self.visited_addresses: set = set()
        
        # C64 ROM Data integration using DataLoader
        try:
            self.data_loader = DataLoader(os.path.dirname(__file__))
            self.c64_rom_data = {
                'memory_maps': self.data_loader.load_directory('c64_rom_data/memory_maps'),
                'zeropage': self.data_loader.load_directory('c64_rom_data/zeropage'),
                'kernal': self.data_loader.load_directory('c64_rom_data/kernal'),
                'basic': self.data_loader.load_directory('c64_rom_data/basic')
            }
            print("✅ py65_professional: C64 ROM Data entegrasyonu tamamlandı")
        except Exception as e:
            self.data_loader = None
            self.c64_rom_data = {}
            print(f"⚠️ py65_professional: C64 ROM Data yüklenemedi: {e}")
        
        # C64 specific addresses
        self._init_c64_symbols()
        
        # Statistics
        self.stats = {
            'total_instructions': 0,
            'branch_instructions': 0,
            'jump_instructions': 0,
            'call_instructions': 0,
            'illegal_opcodes': 0
        }
        
        logger.info("Py65ProfessionalDisassembler initialized successfully")
    
    def _init_c64_symbols(self):
        """Initialize C64 specific symbols"""
        c64_symbols = {
            # Zero page
            0x0000: Symbol("ZERO_PAGE", 0x0000, SymbolType.LABEL, [], "Zero page start"),
            0x00FB: Symbol("CHRGET", 0x00FB, SymbolType.KERNAL_CALL, [], "Get next character"),
            0x00A0: Symbol("BASIC_TXTPTR", 0x00A0, SymbolType.VARIABLE, [], "BASIC text pointer"),
            
            # BASIC ROM
            0xA000: Symbol("BASIC_START", 0xA000, SymbolType.ENTRY_POINT, [], "BASIC ROM start"),
            0xA483: Symbol("BASIC_LIST", 0xA483, SymbolType.SUBROUTINE, [], "BASIC LIST command"),
            0xA560: Symbol("BASIC_RUN", 0xA560, SymbolType.SUBROUTINE, [], "BASIC RUN command"),
            
            # KERNAL ROM
            0xE000: Symbol("KERNAL_START", 0xE000, SymbolType.ENTRY_POINT, [], "KERNAL ROM start"),
            0xFFD2: Symbol("CHROUT", 0xFFD2, SymbolType.KERNAL_CALL, [], "Output character"),
            0xFFCF: Symbol("CHRIN", 0xFFCF, SymbolType.KERNAL_CALL, [], "Input character"),
            0xFFE4: Symbol("GETIN", 0xFFE4, SymbolType.KERNAL_CALL, [], "Get character"),
            0xFFC6: Symbol("CHKOUT", 0xFFC6, SymbolType.KERNAL_CALL, [], "Open output channel"),
            0xFFC9: Symbol("CHKIN", 0xFFC9, SymbolType.KERNAL_CALL, [], "Open input channel"),
            0xFFCC: Symbol("CLRCHN", 0xFFCC, SymbolType.KERNAL_CALL, [], "Clear channels"),
            
            # Vectors
            0xFFFA: Symbol("NMI_VECTOR", 0xFFFA, SymbolType.VECTOR, [], "NMI vector"),
            0xFFFC: Symbol("RESET_VECTOR", 0xFFFC, SymbolType.VECTOR, [], "RESET vector"),
            0xFFFE: Symbol("IRQ_VECTOR", 0xFFFE, SymbolType.VECTOR, [], "IRQ vector"),
            
            # VIC-II
            0xD000: Symbol("VIC_BASE", 0xD000, SymbolType.LABEL, [], "VIC-II base address"),
            0xD020: Symbol("BORDER_COLOR", 0xD020, SymbolType.VARIABLE, [], "Border color"),
            0xD021: Symbol("BACKGROUND_COLOR", 0xD021, SymbolType.VARIABLE, [], "Background color"),
            
            # SID
            0xD400: Symbol("SID_BASE", 0xD400, SymbolType.LABEL, [], "SID base address"),
            
            # CIA
            0xDC00: Symbol("CIA1_BASE", 0xDC00, SymbolType.LABEL, [], "CIA1 base address"),
            0xDD00: Symbol("CIA2_BASE", 0xDD00, SymbolType.LABEL, [], "CIA2 base address"),
        }
        
        for addr, symbol in c64_symbols.items():
            self.add_symbol(addr, symbol)
    
    def add_symbol(self, address: int, symbol: Symbol):
        """Add symbol to symbol table"""
        self.symbol_table[address] = symbol
        self.reverse_symbol_table[symbol.name] = address
        logger.debug(f"Added symbol: {symbol.name} at ${address:04X}")
    
    def get_symbol(self, address: int) -> Optional[Symbol]:
        """Get symbol by address - enhanced with C64 ROM Data"""
        # Önce mevcut symbol table'da ara
        if address in self.symbol_table:
            return self.symbol_table[address]
        
        # C64 ROM Data'dan ara
        rom_label = self.get_c64_rom_address_label(address)
        if rom_label:
            # Dinamik symbol oluştur
            symbol = Symbol(
                name=rom_label,
                address=address,
                symbol_type=SymbolType.LABEL,
                references=[],
                comment=f"C64 ROM address: {rom_label}"
            )
            self.add_symbol(address, symbol)
            return symbol
        
        return None
    
    def get_c64_rom_address_label(self, address: int) -> Optional[str]:
        """C64 ROM Data'dan address için anlamlı isim al"""
        if not self.c64_rom_data:
            return None
            
        try:
            # Zero page değişkenlerini kontrol et
            zeropage_vars = self.c64_rom_data.get('zeropage', {}).get('zeropage_vars', {})
            for key, data in zeropage_vars.items():
                try:
                    addr = int(key.replace('$', ''), 16)
                    if addr == address:
                        name = data.get('name', '')
                        return name.upper() if name else None
                except:
                    continue
            
            # Memory map'i kontrol et
            memory_maps = self.c64_rom_data.get('memory_maps', {}).get('c64_memory_map', {})
            for key, data in memory_maps.items():
                try:
                    start_addr = int(key.replace('$', ''), 16)
                    end_addr_str = data.get('end_addr', key)
                    end_addr = int(end_addr_str.replace('$', ''), 16)
                    
                    if start_addr <= address <= end_addr:
                        name = data.get('name', '')
                        return name.replace(' ', '_').upper() if name else None
                except:
                    continue
            
            # KERNAL routines
            kernal_routines = self.c64_rom_data.get('kernal', {}).get('kernal_routines', {})
            addr_hex = f"${address:04X}"
            if addr_hex in kernal_routines:
                name = kernal_routines[addr_hex].get('name', '')
                return name.upper() if name else None
            
            # BASIC routines
            basic_routines = self.c64_rom_data.get('basic', {}).get('basic_routines', {})
            if addr_hex in basic_routines:
                name = basic_routines[addr_hex].get('name', '')
                return name.upper() if name else None
            
            return None
            
        except Exception as e:
            logger.error(f"py65_professional address label lookup error: {e}")
            return None
        if address in self.symbol_table:
            return self.symbol_table[address]
        
        # C64 ROM Data'dan ara
        symbol_name = self.get_c64_rom_address_label(address)
        if symbol_name:
            # Dinamik symbol oluştur
            symbol = Symbol(
                name=symbol_name,
                address=address,
                symbol_type=SymbolType.LABEL,
                references=[],
                comment=f"C64 ROM address: {symbol_name}"
            )
            self.add_symbol(address, symbol)
            return symbol
        
        return None
    
    def get_c64_rom_address_label(self, address: int) -> Optional[str]:
        """C64 ROM Data'dan address için anlamlı isim al"""
        if not self.c64_rom_data:
            return None
            
        try:
            # Zero page değişkenlerini kontrol et
            zeropage_vars = self.c64_rom_data.get('zeropage', {}).get('zeropage_vars', {})
            for key, data in zeropage_vars.items():
                try:
                    addr = int(key.replace('$', ''), 16)
                    if addr == address:
                        name = data.get('name', '')
                        return name.upper() if name else None
                except:
                    continue
            
            # Memory map'i kontrol et
            memory_maps = self.c64_rom_data.get('memory_maps', {}).get('c64_memory_map', {})
            for key, data in memory_maps.items():
                try:
                    start_addr = int(key.replace('$', ''), 16)
                    end_addr_str = data.get('end_addr', key)
                    end_addr = int(end_addr_str.replace('$', ''), 16)
                    
                    if start_addr <= address <= end_addr:
                        name = data.get('name', '')
                        return name.replace(' ', '_').upper() if name else None
                except:
                    continue
            
            # KERNAL routines
            kernal_routines = self.c64_rom_data.get('kernal', {}).get('kernal_routines', {})
            addr_hex = f"${address:04X}"
            if addr_hex in kernal_routines:
                name = kernal_routines[addr_hex].get('name', '')
                return name.upper() if name else None
            
            # BASIC routines
            basic_routines = self.c64_rom_data.get('basic', {}).get('basic_routines', {})
            if addr_hex in basic_routines:
                name = basic_routines[addr_hex].get('name', '')
                return name.upper() if name else None
            
            return None
            
        except Exception as e:
            logger.debug(f"Address label lookup error: {e}")
            return None
    
    def get_symbol_by_name(self, name: str) -> Optional[Symbol]:
        """Get symbol by name"""
        address = self.reverse_symbol_table.get(name)
        if address is not None:
            return self.symbol_table.get(address)
        return None
    
    def load_memory(self, data: bytes, start_address: int = 0):
        """Load data into memory"""
        if len(data) > 0:
            self.memory[start_address:start_address + len(data)] = data
        logger.info(f"Loaded {len(data)} bytes at ${start_address:04X}")
    
    def load_c64_prg(self, prg_data: bytes) -> int:
        """
        Load C64 PRG file into memory
        
        Args:
            prg_data: PRG file data
            
        Returns:
            Load address
        """
        if len(prg_data) < 2:
            raise ValueError("PRG file too short")
        
        # PRG header (2 bytes little-endian load address)
        load_addr = prg_data[0] | (prg_data[1] << 8)
        
        # Load program data
        self.load_memory(prg_data[2:], load_addr)
        
        # Add entry point symbol
        self.add_symbol(load_addr, Symbol(
            f"PRG_START_{load_addr:04X}", 
            load_addr, 
            SymbolType.ENTRY_POINT, 
            [],
            "PRG file entry point"
        ))
        
        logger.info(f"Loaded C64 PRG file, load address: ${load_addr:04X}")
        return load_addr
    
    def analyze_code_flow(self, address: int, instruction: str, mnemonic: str, operand: str) -> CodeFlowInfo:
        """Analyze code flow for instruction"""
        flow_info = CodeFlowInfo(InstructionType.SEQUENTIAL, [])
        
        # Branch instructions
        if mnemonic in ['BCC', 'BCS', 'BEQ', 'BMI', 'BNE', 'BPL', 'BVC', 'BVS']:
            flow_info.instruction_type = InstructionType.BRANCH
            flow_info.is_branch = True
            flow_info.condition = self._get_branch_condition(mnemonic)
            # Extract branch target
            if operand.startswith('$'):
                try:
                    target = int(operand[1:], 16)
                    flow_info.targets.append(target)
                except ValueError:
                    pass
        
        # Jump instructions
        elif mnemonic == 'JMP':
            flow_info.instruction_type = InstructionType.JUMP
            flow_info.is_jump = True
            if operand.startswith('$'):
                try:
                    target = int(operand[1:], 16)
                    flow_info.targets.append(target)
                except ValueError:
                    pass
        
        # Subroutine calls
        elif mnemonic == 'JSR':
            flow_info.instruction_type = InstructionType.CALL
            flow_info.is_call = True
            if operand.startswith('$'):
                try:
                    target = int(operand[1:], 16)
                    flow_info.targets.append(target)
                    # Auto-create subroutine symbol
                    if target not in self.symbol_table:
                        self.add_symbol(target, Symbol(
                            f"sub_{target:04X}",
                            target,
                            SymbolType.SUBROUTINE,
                            [address],
                            "Auto-generated subroutine"
                        ))
                except ValueError:
                    pass
        
        # Return instructions
        elif mnemonic in ['RTS', 'RTI']:
            flow_info.instruction_type = InstructionType.RETURN
            flow_info.is_return = True
        
        # Interrupt instructions
        elif mnemonic in ['BRK', 'IRQ', 'NMI']:
            flow_info.instruction_type = InstructionType.INTERRUPT
        
        return flow_info
    
    def _get_branch_condition(self, mnemonic: str) -> str:
        """Get branch condition description"""
        conditions = {
            'BCC': 'Carry Clear',
            'BCS': 'Carry Set',
            'BEQ': 'Equal/Zero',
            'BMI': 'Minus/Negative',
            'BNE': 'Not Equal/Not Zero',
            'BPL': 'Plus/Positive',
            'BVC': 'Overflow Clear',
            'BVS': 'Overflow Set'
        }
        return conditions.get(mnemonic, '')
    
    def _parse_instruction(self, instruction: str) -> Tuple[str, str]:
        """Parse instruction to mnemonic and operand"""
        parts = instruction.split(' ', 1)
        mnemonic = parts[0]
        operand = parts[1] if len(parts) > 1 else ''
        return mnemonic, operand
    
    def _get_addressing_mode(self, operand: str) -> AddressingMode:
        """Determine addressing mode from operand"""
        if not operand:
            return AddressingMode.IMPLIED
        elif operand == 'A':
            return AddressingMode.ACCUMULATOR
        elif operand.startswith('#'):
            return AddressingMode.IMMEDIATE
        elif operand.startswith('(') and operand.endswith(')'):
            return AddressingMode.INDIRECT
        elif operand.startswith('(') and operand.endswith(',X)'):
            return AddressingMode.INDIRECT_X
        elif operand.startswith('(') and operand.endswith('),Y'):
            return AddressingMode.INDIRECT_Y
        elif operand.endswith(',X'):
            if operand.startswith('$') and len(operand) <= 4:  # $XX,X
                return AddressingMode.ZERO_PAGE_X
            else:
                return AddressingMode.ABSOLUTE_X
        elif operand.endswith(',Y'):
            if operand.startswith('$') and len(operand) <= 4:  # $XX,Y
                return AddressingMode.ZERO_PAGE_Y
            else:
                return AddressingMode.ABSOLUTE_Y
        elif operand.startswith('$'):
            if len(operand) == 3:  # $XX
                return AddressingMode.ZERO_PAGE
            else:
                return AddressingMode.ABSOLUTE
        else:
            return AddressingMode.ABSOLUTE
    
    def _generate_comment(self, address: int, instruction: str, mnemonic: str, operand: str) -> str:
        """Generate comment for instruction"""
        comments = []
        
        # Add symbol comment if available
        symbol = self.get_symbol(address)
        if symbol and symbol.comment:
            comments.append(symbol.comment)
        
        # Add addressing mode comment
        if operand:
            if operand.startswith('#$'):
                try:
                    value = int(operand[2:], 16)
                    comments.append(f"Immediate: ${value:02X} ({value})")
                except ValueError:
                    pass
            elif operand.startswith('$'):
                try:
                    addr = int(operand[1:].split(',')[0], 16)
                    target_symbol = self.get_symbol(addr)
                    if target_symbol:
                        comments.append(f"-> {target_symbol.name}")
                except ValueError:
                    pass
        
        # Add instruction-specific comments
        if mnemonic == 'LDA':
            comments.append("Load Accumulator")
        elif mnemonic == 'STA':
            comments.append("Store Accumulator")
        elif mnemonic == 'JSR':
            comments.append("Jump to Subroutine")
        elif mnemonic == 'RTS':
            comments.append("Return from Subroutine")
        elif mnemonic == 'BRK':
            comments.append("Break/Interrupt")
        
        return '; '.join(comments)
    
    def disassemble_instruction(self, address: int) -> DisassemblyResult:
        """Disassemble single instruction at address"""
        try:
            # Get raw instruction data
            length, instruction = self.disassembler.instruction_at(address)
            
            # Parse instruction
            mnemonic, operand = self._parse_instruction(instruction)
            
            # Get bytes
            bytes_data = []
            for i in range(length):
                bytes_data.append(self.mpu.ByteAt(address + i))
            
            # Analyze code flow
            flow_info = self.analyze_code_flow(address, instruction, mnemonic, operand)
            
            # Get addressing mode
            addressing_mode = self._get_addressing_mode(operand)
            
            # Get symbol
            symbol = self.get_symbol(address)
            
            # Generate comment
            comment = self._generate_comment(address, instruction, mnemonic, operand)
            
            # Get cycle count (basic estimation)
            cycle_count = self._estimate_cycle_count(mnemonic, addressing_mode)
            
            result = DisassemblyResult(
                address=address,
                bytes=bytes_data,
                instruction=instruction,
                mnemonic=mnemonic,
                operand=operand,
                addressing_mode=addressing_mode,
                length=length,
                symbol=symbol,
                comment=comment,
                flow_info=flow_info,
                cycle_count=cycle_count
            )
            
            # Update statistics
            self.stats['total_instructions'] += 1
            if flow_info.is_branch:
                self.stats['branch_instructions'] += 1
            if flow_info.is_jump:
                self.stats['jump_instructions'] += 1
            if flow_info.is_call:
                self.stats['call_instructions'] += 1
            
            return result
            
        except Exception as e:
            logger.error(f"Error disassembling instruction at ${address:04X}: {e}")
            # Return illegal instruction
            self.stats['illegal_opcodes'] += 1
            return DisassemblyResult(
                address=address,
                bytes=[self.mpu.ByteAt(address)],
                instruction=f"???",
                mnemonic="???",
                operand="",
                addressing_mode=AddressingMode.IMPLIED,
                length=1,
                comment="Illegal or unknown opcode"
            )
    
    def _estimate_cycle_count(self, mnemonic: str, addressing_mode: AddressingMode) -> int:
        """Estimate cycle count for instruction"""
        # Basic cycle count estimation
        base_cycles = {
            'LDA': 2, 'STA': 2, 'LDX': 2, 'STX': 2, 'LDY': 2, 'STY': 2,
            'ADC': 2, 'SBC': 2, 'AND': 2, 'ORA': 2, 'EOR': 2,
            'CMP': 2, 'CPX': 2, 'CPY': 2,
            'INC': 2, 'DEC': 2, 'INX': 2, 'DEX': 2, 'INY': 2, 'DEY': 2,
            'ASL': 2, 'LSR': 2, 'ROL': 2, 'ROR': 2,
            'BIT': 2, 'BRK': 7, 'RTI': 6, 'RTS': 6, 'JSR': 6,
            'JMP': 3, 'NOP': 2,
            'PHA': 3, 'PLA': 4, 'PHP': 3, 'PLP': 4,
            'TAX': 2, 'TXA': 2, 'TAY': 2, 'TYA': 2, 'TXS': 2, 'TSX': 2,
            'CLC': 2, 'SEC': 2, 'CLI': 2, 'SEI': 2, 'CLV': 2, 'CLD': 2, 'SED': 2
        }
        
        cycles = base_cycles.get(mnemonic, 2)
        
        # Add addressing mode penalties
        if addressing_mode in [AddressingMode.ABSOLUTE, AddressingMode.ABSOLUTE_X, AddressingMode.ABSOLUTE_Y]:
            cycles += 1
        elif addressing_mode in [AddressingMode.INDIRECT, AddressingMode.INDIRECT_X, AddressingMode.INDIRECT_Y]:
            cycles += 2
        
        return cycles
    
    def disassemble_range(self, start_address: int, end_address: int) -> List[DisassemblyResult]:
        """Disassemble a range of addresses"""
        results = []
        address = start_address
        
        logger.info(f"Disassembling range ${start_address:04X}-${end_address:04X}")
        
        while address <= end_address:
            result = self.disassemble_instruction(address)
            results.append(result)
            address += result.length
            self.visited_addresses.add(result.address)
        
        return results
    
    def auto_analyze(self, start_address: int, max_length: int = 0x1000) -> List[DisassemblyResult]:
        """
        Automatic code analysis with flow following
        
        Args:
            start_address: Starting address
            max_length: Maximum analysis length
            
        Returns:
            List of disassembly results
        """
        results = []
        to_visit = [start_address]
        visited = set()
        
        logger.info(f"Starting auto-analysis from ${start_address:04X}")
        
        while to_visit and len(results) < max_length:
            address = to_visit.pop(0)
            
            if address in visited or address < 0 or address >= self.memory_size:
                continue
            
            visited.add(address)
            result = self.disassemble_instruction(address)
            results.append(result)
            
            # Add flow targets to visit queue
            if result.flow_info:
                for target in result.flow_info.targets:
                    if target not in visited:
                        to_visit.append(target)
            
            # Continue with next sequential instruction if not a jump
            if result.flow_info and not result.flow_info.is_jump:
                next_addr = address + result.length
                if next_addr not in visited:
                    to_visit.append(next_addr)
        
        logger.info(f"Auto-analysis complete. Analyzed {len(results)} instructions")
        return results
    
    def generate_assembly_listing(self, results: List[DisassemblyResult], 
                                 show_bytes: bool = True,
                                 show_addresses: bool = True,
                                 show_symbols: bool = True,
                                 show_comments: bool = True) -> str:
        """Generate formatted assembly listing"""
        lines = []
        
        # Header
        lines.append("; 6502 Assembly Listing")
        lines.append("; Generated by Py65ProfessionalDisassembler")
        lines.append("; " + "=" * 50)
        lines.append("")
        
        # Statistics
        lines.append(f"; Statistics:")
        lines.append(f"; Total instructions: {self.stats['total_instructions']}")
        lines.append(f"; Branch instructions: {self.stats['branch_instructions']}")
        lines.append(f"; Jump instructions: {self.stats['jump_instructions']}")
        lines.append(f"; Call instructions: {self.stats['call_instructions']}")
        lines.append(f"; Illegal opcodes: {self.stats['illegal_opcodes']}")
        lines.append("")
        
        # Symbols table
        if show_symbols and self.symbol_table:
            lines.append("; Symbol Table:")
            for addr, symbol in sorted(self.symbol_table.items()):
                lines.append(f"; ${addr:04X} {symbol.name:<20} {symbol.symbol_type.value}")
            lines.append("")
        
        # Assembly listing
        lines.append("; Assembly Listing:")
        lines.append("; " + "=" * 50)
        
        for result in results:
            line_parts = []
            
            # Address
            if show_addresses:
                line_parts.append(f"${result.address:04X}")
            
            # Bytes
            if show_bytes:
                bytes_str = ' '.join(f"{b:02X}" for b in result.bytes)
                line_parts.append(f"{bytes_str:<8}")
            
            # Symbol label
            if result.symbol and show_symbols:
                lines.append(f"{result.symbol.name}:")
            
            # Instruction
            instruction_part = f"  {result.instruction:<12}"
            
            # Comment
            comment_part = ""
            if show_comments and result.comment:
                comment_part = f" ; {result.comment}"
            
            # Combine parts
            if line_parts:
                line = "  ".join(line_parts) + "  " + instruction_part + comment_part
            else:
                line = instruction_part + comment_part
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def export_symbols(self, filename: str):
        """Export symbols to file"""
        with open(filename, 'w') as f:
            f.write("# Symbol Table Export\n")
            f.write("# Address  Name                 Type         Comment\n")
            f.write("# " + "=" * 60 + "\n")
            
            for addr, symbol in sorted(self.symbol_table.items()):
                f.write(f"${addr:04X}     {symbol.name:<20} {symbol.symbol_type.value:<12} {symbol.comment}\n")
        
        logger.info(f"Symbols exported to {filename}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get disassembly statistics"""
        return {
            **self.stats,
            'symbols_count': len(self.symbol_table),
            'visited_addresses': len(self.visited_addresses),
            'memory_usage': sum(1 for i in range(self.memory_size) if self.mpu.ByteAt(i) != 0)
        }

# Helper functions
def create_professional_disassembler() -> Optional[Py65ProfessionalDisassembler]:
    """Create professional disassembler instance"""
    try:
        return Py65ProfessionalDisassembler()
    except ImportError:
        return None

def disassemble_prg_file(filename: str, output_file: str = None) -> bool:
    """
    Disassemble a C64 PRG file
    
    Args:
        filename: PRG file path
        output_file: Output assembly file path
        
    Returns:
        Success status
    """
    try:
        disasm = create_professional_disassembler()
        if not disasm:
            print("py65 kütüphanesi gerekli")
            return False
        
        # Load PRG file
        with open(filename, 'rb') as f:
            prg_data = f.read()
        
        load_addr = disasm.load_c64_prg(prg_data)
        
        # Disassemble
        end_addr = load_addr + len(prg_data) - 3
        results = disasm.disassemble_range(load_addr, end_addr)
        
        # Generate listing
        listing = disasm.generate_assembly_listing(results)
        
        # Save to file
        if output_file:
            with open(output_file, 'w') as f:
                f.write(listing)
            print(f"Assembly listing saved to {output_file}")
        else:
            print(listing)
        
        # Print statistics
        stats = disasm.get_statistics()
        print(f"\nStatistics: {stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error disassembling PRG file: {e}")
        return False

# Test function
def test_disassembler():
    """Test disassembler functionality"""
    if not PY65_AVAILABLE:
        print("py65 kütüphanesi test edilemez - yüklü değil")
        return False
    
    try:
        # Create disassembler
        disasm = Py65ProfessionalDisassembler()
        
        # Test data (simple 6502 program)
        test_program = bytes([
            0xA9, 0x01,  # LDA #$01
            0x8D, 0x00, 0x02,  # STA $0200
            0xA2, 0x00,  # LDX #$00
            0xBD, 0x00, 0x03,  # LDA $0300,X
            0x4C, 0x00, 0x10,  # JMP $1000
            0x60  # RTS
        ])
        
        # Load test program
        disasm.load_memory(test_program, 0x1000)
        
        # Disassemble
        end_addr = 0x1000 + len(test_program) - 1
        results = disasm.disassemble_range(0x1000, end_addr)
        
        # Generate listing
        listing = disasm.generate_assembly_listing(results)
        print("Test Disassembly:")
        print(listing)
        
        # Print statistics
        stats = disasm.get_statistics()
        print(f"\nTest Statistics: {stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    print("Py65 Professional Disassembler")
    print("=" * 40)
    
    if PY65_AVAILABLE:
        print("✓ py65 kütüphanesi kullanılabilir")
        test_disassembler()
    else:
        print("✗ py65 kütüphanesi yüklü değil")
        print("  venv_asmto ortamında çalıştırın:")
        print("  venv_asmto\\Scripts\\python py65_professional_disassembler.py")
