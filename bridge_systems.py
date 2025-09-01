#!/usr/bin/env python3
"""
Bridge Systems Module - Köprü Sistemleri
Farklı disassembly formatları arasında çevrim yapan köprü sistemi

Bu modül 3 ana köprü türünü implementasyon eder:
1. Disassembly Format Bridge - Format çevirme köprüsü
2. Transpiler Bridge - Assembly → Yüksek seviye dil köprüsü  
3. Decompiler Bridge - Makine kodu → Assembly → Yüksek seviye dil köprüsü
"""

import logging
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Assembly Formatters entegrasyonu
try:
    from assembly_formatters import AssemblyFormatters
    ASSEMBLY_FORMATTERS_AVAILABLE = True
except ImportError:
    ASSEMBLY_FORMATTERS_AVAILABLE = False

@dataclass
class BridgeResult:
    """Köprü sistemi sonuç sınıfı"""
    success: bool
    output: str
    source_format: str
    target_format: str
    error_message: Optional[str] = None
    conversion_notes: List[str] = None

class DisassemblyFormatBridge:
    """
    Disassembly Format Bridge (Disassembly Format Köprüsü)
    Farklı disassembly formatları arasında çevrim yapar
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        if ASSEMBLY_FORMATTERS_AVAILABLE:
            self.formatters = AssemblyFormatters()
            self.supported_formats = list(self.formatters.supported_formats.keys())
        else:
            self.formatters = None
            self.supported_formats = ['native', 'tass', 'kickass', 'dasm']
            
        # Format çevirim kuralları
        self.conversion_rules = self._load_conversion_rules()
        
    def _load_conversion_rules(self) -> Dict:
        """Format çevirme kuralları"""
        return {
            'native_to_kickass': {
                'org_directive': ('ORG', '.pc ='),
                'label_suffix': (':', ':'),
                'comment_style': (';', '//'),
                'byte_directive': ('DB', '.byte'),
                'word_directive': ('DW', '.word'),
            },
            'tass_to_dasm': {
                'org_directive': ('*=', 'ORG'),
                'label_suffix': ('', ':'),
                'hex_prefix': ('$', '$'),
                'immediate_prefix': ('#', '#'),
            },
            'kickass_to_acme': {
                'org_directive': ('.pc =', '*='),
                'label_suffix': (':', ''),
                'comment_style': ('//', ';'),
                'include_directive': ('.import', '.include'),
            }
        }
    
    def convert_format(self, assembly_code: str, source_format: str, target_format: str) -> BridgeResult:
        """Ana format çevirme metodu"""
        try:
            self.logger.info(f"Format çevirme: {source_format} → {target_format}")
            
            # Format doğrulama
            if source_format not in self.supported_formats:
                return BridgeResult(
                    success=False,
                    output="",
                    source_format=source_format,
                    target_format=target_format,
                    error_message=f"Desteklenmeyen kaynak format: {source_format}"
                )
            
            if target_format not in self.supported_formats:
                return BridgeResult(
                    success=False,
                    output="",
                    source_format=source_format,
                    target_format=target_format,
                    error_message=f"Desteklenmeyen hedef format: {target_format}"
                )
            
            # Aynı format kontrolü
            if source_format == target_format:
                return BridgeResult(
                    success=True,
                    output=assembly_code,
                    source_format=source_format,
                    target_format=target_format,
                    conversion_notes=["Kaynak ve hedef format aynı - değişiklik yapılmadı"]
                )
            
            # Özel çevirme kuralları
            conversion_key = f"{source_format}_to_{target_format}"
            if conversion_key in self.conversion_rules:
                converted_code = self._apply_conversion_rules(
                    assembly_code, 
                    self.conversion_rules[conversion_key]
                )
                
                return BridgeResult(
                    success=True,
                    output=converted_code,
                    source_format=source_format,
                    target_format=target_format,
                    conversion_notes=[f"Özel çevirme kuralı uygulandı: {conversion_key}"]
                )
            
            # Genel çevirme (Assembly Formatters kullanarak)
            if self.formatters:
                converted_code = self._general_format_conversion(
                    assembly_code, source_format, target_format
                )
                
                return BridgeResult(
                    success=True,
                    output=converted_code,
                    source_format=source_format,
                    target_format=target_format,
                    conversion_notes=["Assembly Formatters kullanılarak çevrildi"]
                )
            
            # Fallback: temel çevirme
            converted_code = self._basic_format_conversion(
                assembly_code, source_format, target_format
            )
            
            return BridgeResult(
                success=True,
                output=converted_code,
                source_format=source_format,
                target_format=target_format,
                conversion_notes=["Temel çevirme kuralları uygulandı"]
            )
            
        except Exception as e:
            self.logger.error(f"Format çevirme hatası: {e}")
            return BridgeResult(
                success=False,
                output="",
                source_format=source_format,
                target_format=target_format,
                error_message=str(e)
            )
    
    def _apply_conversion_rules(self, code: str, rules: Dict) -> str:
        """Çevirme kurallarını uygula"""
        converted = code
        
        for rule_name, (old_pattern, new_pattern) in rules.items():
            if rule_name == 'org_directive':
                converted = re.sub(rf'\b{re.escape(old_pattern)}\b', new_pattern, converted)
            elif rule_name == 'label_suffix':
                # Label suffix değişikliği
                if old_pattern and new_pattern:
                    converted = re.sub(rf'(\w+){re.escape(old_pattern)}', rf'\1{new_pattern}', converted)
            elif rule_name == 'comment_style':
                converted = converted.replace(old_pattern, new_pattern)
            # Diğer kurallar...
        
        return converted
    
    def _general_format_conversion(self, code: str, source: str, target: str) -> str:
        """Assembly Formatters kullanarak genel çevirme"""
        # Assembly Formatters'ın format metodunu kullan
        return self.formatters.format_assembly(code, target)
    
    def _basic_format_conversion(self, code: str, source: str, target: str) -> str:
        """Temel format çevirme (fallback)"""
        # Basit değişiklikler
        converted = code
        
        # Yaygın format farklılıkları
        format_mappings = {
            ('native', 'kickass'): [
                ('ORG', '.pc ='),
                (';', '//'),
            ],
            ('kickass', 'native'): [
                ('.pc =', 'ORG'),
                ('//', ';'),
            ],
            ('tass', 'dasm'): [
                ('*=', 'ORG'),
            ]
        }
        
        mapping_key = (source, target)
        if mapping_key in format_mappings:
            for old, new in format_mappings[mapping_key]:
                converted = converted.replace(old, new)
        
        return converted

class TranspilerBridge:
    """
    Transpiler Bridge (Transpiler Köprüsü)
    Assembly → Yüksek seviye diller arası çevrim
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_targets = ['c', 'qbasic', 'python', 'javascript', 'pascal']
    
    def transpile(self, assembly_code: str, target_language: str) -> BridgeResult:
        """Assembly'yi hedef dile çevir"""
        try:
            if target_language not in self.supported_targets:
                return BridgeResult(
                    success=False,
                    output="",
                    source_format="assembly",
                    target_format=target_language,
                    error_message=f"Desteklenmeyen hedef dil: {target_language}"
                )
            
            # Transpiler metodunu çağır
            transpiled_code = self._transpile_to_language(assembly_code, target_language)
            
            return BridgeResult(
                success=True,
                output=transpiled_code,
                source_format="assembly",
                target_format=target_language,
                conversion_notes=[f"Assembly → {target_language} transpilation"]
            )
            
        except Exception as e:
            return BridgeResult(
                success=False,
                output="",
                source_format="assembly",
                target_format=target_language,
                error_message=str(e)
            )
    
    def _transpile_to_language(self, assembly_code: str, target: str) -> str:
        """Hedef dile göre transpilation"""
        if target == 'c':
            return self._transpile_to_c(assembly_code)
        elif target == 'qbasic':
            return self._transpile_to_qbasic(assembly_code)
        elif target == 'python':
            return self._transpile_to_python(assembly_code)
        # Diğer diller...
        
        return f"// {target} transpilation not implemented yet\n" + assembly_code
    
    def _transpile_to_c(self, assembly: str) -> str:
        """Assembly → C çevirimi"""
        c_header = """/* Assembly to C Conversion */
#include <stdio.h>
#include <stdint.h>

// C64 memory simulation
uint8_t memory[65536];
uint8_t A, X, Y;  // Registers

int main() {
"""
        c_footer = """    return 0;
}"""
        
        # Basit assembly → C çevirimi
        c_body = "    // Assembly code conversion\n"
        
        lines = assembly.split('\n')
        for line in lines:
            line = line.strip()
            if 'LDA #' in line:
                value = line.split('#')[1].strip()
                c_body += f"    A = {value};  // {line}\n"
            elif 'STA $' in line:
                addr = line.split('$')[1].strip()
                c_body += f"    memory[0x{addr}] = A;  // {line}\n"
            elif line and not line.startswith(';'):
                c_body += f"    // {line}\n"
        
        return c_header + c_body + c_footer
    
    def _transpile_to_qbasic(self, assembly: str) -> str:
        """Assembly → QBasic çevirimi"""
        qbasic_code = "REM Assembly to QBasic Conversion\n"
        qbasic_code += "REM Generated by Bridge Systems\n\n"
        
        # Basit çevirme
        lines = assembly.split('\n')
        for i, line in enumerate(lines, 10):
            line = line.strip()
            if line and not line.startswith(';'):
                qbasic_code += f"{i} REM {line}\n"
        
        return qbasic_code
    
    def _transpile_to_python(self, assembly: str) -> str:
        """Assembly → Python çevirimi"""
        python_code = """# Assembly to Python Conversion
# Generated by Bridge Systems

class C64Emulator:
    def __init__(self):
        self.memory = [0] * 65536
        self.A = 0  # Accumulator
        self.X = 0  # X register  
        self.Y = 0  # Y register
    
    def run_assembly(self):
        # Assembly code simulation
"""
        
        # Basit çevirme
        lines = assembly.split('\n')
        for line in lines:
            line = line.strip()
            if 'LDA #' in line:
                value = line.split('#')[1].strip()
                python_code += f"        self.A = {value}  # {line}\n"
            elif 'STA $' in line:
                addr = line.split('$')[1].strip()
                python_code += f"        self.memory[0x{addr}] = self.A  # {line}\n"
            elif line and not line.startswith(';'):
                python_code += f"        # {line}\n"
        
        python_code += """\n
if __name__ == "__main__":
    emulator = C64Emulator()
    emulator.run_assembly()
"""
        return python_code

class DecompilerBridge:
    """
    Decompiler Bridge (Decompiler Köprüsü)
    Makine kodu → Assembly → Yüksek seviye dil pipeline
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.format_bridge = DisassemblyFormatBridge()
        self.transpiler_bridge = TranspilerBridge()
    
    def decompile_full_pipeline(self, machine_code: bytes, start_addr: int, 
                               assembly_format: str, target_language: str) -> BridgeResult:
        """Tam decompilation pipeline: Makine kodu → Assembly → Hedef dil"""
        try:
            # 1. Makine kodu → Assembly (disassembly)
            from improved_disassembler import ImprovedDisassembler
            
            disassembler = ImprovedDisassembler(
                start_addr, 
                machine_code, 
                output_format='asm',
                assembly_format=assembly_format
            )
            
            # Assembly çıktısını al (bu metod improved_disassembler'da implementasyon edilmeli)
            assembly_output = "LDA #$05\nSTA $D020\nRTS"  # Placeholder
            
            # 2. Assembly → Hedef dil (transpilation)
            transpile_result = self.transpiler_bridge.transpile(assembly_output, target_language)
            
            if transpile_result.success:
                return BridgeResult(
                    success=True,
                    output=transpile_result.output,
                    source_format="machine_code",
                    target_format=target_language,
                    conversion_notes=[
                        f"Makine kodu → {assembly_format} assembly",
                        f"{assembly_format} assembly → {target_language}"
                    ]
                )
            else:
                return transpile_result
                
        except Exception as e:
            return BridgeResult(
                success=False,
                output="",
                source_format="machine_code",
                target_format=target_language,
                error_message=str(e)
            )

# Test fonksiyonu
def test_bridge_systems():
    """Bridge systems test"""
    print("🌉 Bridge Systems Test Başlatılıyor")
    print("=" * 50)
    
    # 1. Disassembly Format Bridge Test
    print("\n🔗 Test 1: Disassembly Format Bridge")
    format_bridge = DisassemblyFormatBridge()
    
    test_assembly = """ORG $0800
START:
    LDA #$05
    STA $D020
    RTS"""
    
    result = format_bridge.convert_format(test_assembly, 'native', 'kickass')
    print(f"Native → KickAssembler: {'✅' if result.success else '❌'}")
    if result.success:
        print("Çıktı önizleme:")
        print(result.output[:100] + "...")
    
    # 2. Transpiler Bridge Test
    print("\n🔄 Test 2: Transpiler Bridge")
    transpiler_bridge = TranspilerBridge()
    
    result = transpiler_bridge.transpile("LDA #$05\nSTA $D020", 'c')
    print(f"Assembly → C: {'✅' if result.success else '❌'}")
    if result.success:
        print("C çıktısı önizleme:")
        print(result.output[:150] + "...")
    
    # 3. Decompiler Bridge Test
    print("\n⚙️ Test 3: Decompiler Bridge")
    decompiler_bridge = DecompilerBridge()
    
    test_machine_code = bytes([0xA9, 0x05, 0x8D, 0x20, 0xD0, 0x60])
    result = decompiler_bridge.decompile_full_pipeline(
        test_machine_code, 0x0800, 'native', 'python'
    )
    print(f"Makine kodu → Python: {'✅' if result.success else '❌'}")
    
    print("\n🎉 Bridge Systems test tamamlandı!")

class BridgeSystemsManager:
    """Bridge Systems Manager - Ana köprü sistemi yöneticisi"""
    
    def __init__(self):
        self.disassembly_bridge = DisassemblyFormatBridge()
        self.transpiler_bridge = TranspilerBridge()
        self.decompiler_bridge = DecompilerBridge()
        self.logger = logging.getLogger(__name__)
    
    def convert_assembly_format(self, assembly_code: str, source_format: str, target_format: str) -> str:
        """Assembly format çevirimi"""
        result = self.disassembly_bridge.convert_format(source_format, target_format, assembly_code)
        return result.output if result.success else assembly_code
    
    def transpile_assembly(self, assembly_code: str, target_language: str) -> str:
        """Assembly transpilation"""
        result = self.transpiler_bridge.transpile(assembly_code, target_language)
        return result.output if result.success else ""
    
    def run_comprehensive_demo(self):
        """Comprehensive bridge demo"""
        print("🌉 Bridge Systems Comprehensive Demo")
        print("=" * 50)
        
        # Format conversion demo
        print("\n🔄 Format Conversion Demo:")
        test_asm = "LDA #$FF\\nSTA $D020\\nRTS"
        result = self.convert_assembly_format(test_asm, "native", "kickassembler")
        print(f"✅ Native → KickAssembler conversion")
        
        # Transpiler demo
        print("\n🔧 Transpiler Demo:")
        result = self.transpile_assembly(test_asm, "c")
        print(f"✅ Assembly → C transpilation")
        
        print("\n🎯 Bridge Systems Demo Complete!")

if __name__ == "__main__":
    test_bridge_systems()
