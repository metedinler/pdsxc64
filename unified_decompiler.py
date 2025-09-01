#!/usr/bin/env python
"""
UNIFIED DECOMPILER INTERFACE
============================

Bu modül, tüm decompiler sistemlerini birleştiren ana interface'i sağlar.
Enhanced C64 Memory Manager ve improved_disassembler.py'yi koordine eder.

ÖZELLİKLER:
- Tek bir interface ile tüm formatları destekler
- Memory mapping otomatik entegrasyonu
- Format-specific optimizasyonlar
- Advanced code analysis hazırlığı
- Comprehensive error handling

DESTEKLENEN FORMATLAR:
- ASM: Assembly output with enhanced annotations
- C: C language with smart pointer usage
- QBasic: QBasic with PEEK/POKE optimizations  
- PDSx: Custom programming language developed by project author (EXPERIMENTAL - limited functionality)
- Pseudocode: High-level abstraction (gelecek)

KULLANIM:
unified = UnifiedDecompiler('c')  # Target format
result = unified.decompile(prg_data, options={'enhanced_memory': True})
"""

import os
import sys
from typing import Dict, List, Optional, Union, Any

# Import our enhanced components
from enhanced_c64_memory_manager import EnhancedC64MemoryManager
from improved_disassembler import ImprovedDisassembler
from code_analyzer import CodeAnalyzer, AnalysisResult

class UnifiedDecompiler:
    """
    Birleşik decompiler interface - tüm formatları destekler
    """
    
    # Desteklenen target formatları
    SUPPORTED_FORMATS = ['asm', 'c', 'qbasic', 'pdsx', 'pseudocode']
    
    # Format-specific ayarları
    FORMAT_DEFAULTS = {
        'asm': {
            'show_hex': True,
            'show_labels': True,
            'enhanced_annotations': True
        },
        'c': {
            'use_pointers': True,
            'optimize_structs': True,
            'include_headers': True,
            'function_prototypes': True
        },
        'qbasic': {
            'line_numbers': False,
            'optimize_goto': True,
            'use_peek_poke': True,
            'modern_syntax': False
        },
        'pdsx': {
            'line_numbers': True,
            'line_increment': 10,
            'start_line': 100,
            'experimental_mode': True,  # PDSX is experimental/custom format
            'author_format': True       # Custom format by project author
        },
        'pseudocode': {
            'high_level': True,
            'abstract_loops': True,
            'hide_registers': True
        }
    }
    
    def __init__(self, target_format: str = 'c', **options):
        """
        UnifiedDecompiler başlatma
        
        Args:
            target_format: Hedef format ('asm', 'c', 'qbasic', 'pdsx', 'pseudocode')
            **options: Format-specific seçenekler
        """
        if target_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Desteklenmeyen format: {target_format}. Desteklenen: {self.SUPPORTED_FORMATS}")
        
        self.target_format = target_format
        self.options = self._merge_options(target_format, options)
        
        # Enhanced components
        self.memory_manager = None
        self.disassembler = None
        self.code_analyzer = None
        
        # Analysis results
        self.analysis_results = {}
        self.last_decompile_stats = {}
        self.last_code_analysis = None
        
        print(f"🎯 UnifiedDecompiler başlatıldı - Target: {target_format.upper()}")
    
    def _merge_options(self, target_format: str, user_options: Dict) -> Dict:
        """Format defaults ile user options'ı birleştir"""
        defaults = self.FORMAT_DEFAULTS.get(target_format, {}).copy()
        defaults.update(user_options)
        return defaults
    
    def initialize_components(self) -> bool:
        """Enhanced components'leri başlat"""
        try:
            # Enhanced Memory Manager
            print("🔧 Enhanced C64 Memory Manager başlatılıyor...")
            self.memory_manager = EnhancedC64MemoryManager()
            
            # Component'leri test et
            test_addr = 0xFFD2
            test_name = self.memory_manager.get_smart_variable_name(test_addr)
            print(f"   ✅ Memory Manager test: ${test_addr:04X} → {test_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Component başlatma hatası: {e}")
            return False
    
    def decompile(self, 
                 prg_data: Union[bytes, str], 
                 start_address: Optional[int] = None,
                 analysis_level: str = 'standard',
                 enable_code_analysis: bool = True) -> str:
        """
        Ana decompile fonksiyonu
        
        Args:
            prg_data: PRG dosya data'sı (bytes) veya hex string
            start_address: Başlangıç adresi (None ise PRG header'dan al)
            analysis_level: Analiz seviyesi ('basic', 'standard', 'advanced')
            enable_code_analysis: Code pattern analysis aktif et
            
        Returns:
            Decompile edilmiş kod string'i
        """
        
        # Input validation ve preprocessing
        processed_data = self._preprocess_input(prg_data, start_address)
        if not processed_data:
            return "❌ HATA: Geçersiz input data"
        
        prg_bytes, start_addr = processed_data
        
        # Components başlatma
        if not self.memory_manager:
            if not self.initialize_components():
                return "❌ HATA: Component başlatma başarısız"
        
        try:
            # Enhanced Disassembler oluştur
            print(f"🔧 Disassembler başlatılıyor - Start: ${start_addr:04X}")
            self.disassembler = ImprovedDisassembler(start_addr, prg_bytes)
            self.disassembler.output_format = self.target_format
            
            # Enhanced memory integration
            if hasattr(self.disassembler, 'enhanced_memory'):
                self.disassembler.enhanced_memory = True
                print("   ✅ Enhanced Memory integration aktif")
            
            # Code analysis (if enabled)
            if enable_code_analysis and analysis_level in ['standard', 'advanced']:
                print("🔍 Code pattern analysis başlıyor...")
                try:
                    self.code_analyzer = CodeAnalyzer(prg_bytes, start_addr)
                    self.last_code_analysis = self.code_analyzer.analyze_all_patterns()
                    print(f"   ✅ {len(self.last_code_analysis.patterns)} pattern tespit edildi")
                except Exception as e:
                    print(f"   ⚠️ Code analysis kısmi başarı: {e}")
            
            # Decompile işlemi
            print(f"🚀 Decompile başlıyor - Format: {self.target_format.upper()}")
            result = self.disassembler.disassemble_to_format(prg_bytes)
            
            # Post-processing (with code analysis enhancement)
            final_result = self._post_process_output(result)
            
            # İstatistikleri güncelle
            self._update_stats(prg_bytes, result)
            
            print(f"✅ Decompile tamamlandı - {len(final_result)} karakter")
            return final_result
            
        except Exception as e:
            error_msg = f"❌ DECOMPILE HATASI: {str(e)}"
            print(error_msg)
            import traceback
            print(f"TRACEBACK:\n{traceback.format_exc()}")
            return error_msg
    
    def _preprocess_input(self, prg_data: Union[bytes, str], start_address: Optional[int]):
        """Input data'yı preprocess et"""
        
        # String to bytes conversion
        if isinstance(prg_data, str):
            try:
                prg_bytes = bytes.fromhex(prg_data.replace(' ', ''))
            except ValueError:
                print("❌ Geçersiz hex string")
                return None
        else:
            prg_bytes = prg_data
        
        # Start address determination
        if start_address is not None:
            start_addr = start_address
        elif len(prg_bytes) >= 2:
            # PRG format - first 2 bytes are load address
            start_addr = prg_bytes[0] + (prg_bytes[1] << 8)
            prg_bytes = prg_bytes[2:]  # Skip header
        else:
            print("❌ Start address belirlenemedi")
            return None
        
        if len(prg_bytes) == 0:
            print("❌ Boş code data")
            return None
            
        return prg_bytes, start_addr
    
    def _post_process_output(self, raw_output: str) -> str:
        """Output'u format-specific post-processing'den geçir"""
        
        if self.target_format == 'c':
            return self._post_process_c(raw_output)
        elif self.target_format == 'qbasic':
            return self._post_process_qbasic(raw_output)
        elif self.target_format == 'pdsx':
            return self._post_process_pdsx(raw_output)
        elif self.target_format == 'asm':
            return self._post_process_asm(raw_output)
        else:
            return raw_output
    
    def _post_process_c(self, output: str) -> str:
        """C format post-processing"""
        lines = output.split('\n')
        
        # Enhanced C optimizations
        if self.options.get('optimize_structs', True):
            # Struct optimization logic
            pass
        
        if self.options.get('function_prototypes', True):
            # Function prototype generation
            pass
            
        return '\n'.join(lines)
    
    def _post_process_qbasic(self, output: str) -> str:
        """QBasic format post-processing"""
        lines = output.split('\n')
        
        # QBasic optimizations
        if self.options.get('optimize_goto', True):
            # GOTO optimization logic
            pass
            
        return '\n'.join(lines)
    
    def _post_process_pdsx(self, output: str) -> str:
        """PDSx format post-processing - EXPERIMENTAL custom format"""
        lines = output.split('\n')
        
        # PDSX custom format optimizations - EXPERIMENTAL
        # Note: PDSX is a custom format developed by project author
        # Current implementation may have limited functionality
        if self.options.get('experimental_mode', True):
            # Custom PDSX format processing - needs integration with pdsXv12.py
            lines.insert(0, "; PDSX format - EXPERIMENTAL/CUSTOM")
            lines.insert(1, "; Requires pdsXv12.py interpreter")
            
        return '\n'.join(lines)
    
    def _post_process_asm(self, output: str) -> str:
        """Assembly format post-processing"""
        lines = output.split('\n')
        
        # Assembly enhancements
        if self.options.get('enhanced_annotations', True):
            # Enhanced annotation logic
            pass
            
        return '\n'.join(lines)
    
    def _update_stats(self, prg_bytes: bytes, output: str):
        """Decompile istatistiklerini güncelle"""
        self.last_decompile_stats = {
            'input_size': len(prg_bytes),
            'output_size': len(output),
            'output_lines': len(output.split('\n')),
            'target_format': self.target_format,
            'memory_manager_active': self.memory_manager is not None,
            'enhanced_features': getattr(self.disassembler, 'enhanced_memory', False)
        }
    
    def get_code_analysis(self) -> Optional[AnalysisResult]:
        """Son code analysis sonuçlarını döndür"""
        return self.last_code_analysis
    
    def get_analysis_report(self) -> str:
        """Code analysis raporu üret"""
        if not self.last_code_analysis or not self.code_analyzer:
            return "Code analysis yapılmadı"
        
        return self.code_analyzer.generate_report(self.last_code_analysis)
    
    def get_pattern_summary(self) -> List[str]:
        """Tespit edilen pattern'lerin özetini döndür"""
        if not self.last_code_analysis:
            return []
        
        return [f"{p.pattern_type.value}: {p.description}" 
                for p in self.last_code_analysis.patterns]
    
    def get_stats(self) -> Dict:
        """Son decompile istatistiklerini döndür"""
        stats = self.last_decompile_stats.copy()
        
        # Code analysis stats ekle
        if self.last_code_analysis:
            stats.update({
                'patterns_detected': len(self.last_code_analysis.patterns),
                'complexity_score': self.last_code_analysis.complexity_score,
                'memory_usage_areas': len([k for k, v in self.last_code_analysis.memory_usage.items() if v > 0]),
                'optimization_suggestions': len(self.last_code_analysis.optimization_opportunities)
            })
        
        return stats
    
    def get_supported_formats(self) -> List[str]:
        """Desteklenen formatları döndür"""
        return self.SUPPORTED_FORMATS.copy()
    
    def set_format(self, new_format: str) -> bool:
        """Target format'ı değiştir"""
        if new_format not in self.SUPPORTED_FORMATS:
            print(f"❌ Desteklenmeyen format: {new_format}")
            return False
        
        self.target_format = new_format
        self.options = self._merge_options(new_format, {})
        
        if self.disassembler:
            self.disassembler.output_format = new_format
        
        print(f"✅ Format değiştirildi: {new_format.upper()}")
        return True
    
    def configure_options(self, **new_options) -> Dict:
        """Format-specific options'ı güncelle"""
        self.options.update(new_options)
        print(f"✅ Options güncellendi: {new_options}")
        return self.options.copy()


# Convenience functions
def quick_decompile(prg_data: Union[bytes, str], 
                   target_format: str = 'c', 
                   start_address: Optional[int] = None) -> str:
    """
    Hızlı decompile işlemi
    
    Args:
        prg_data: PRG data
        target_format: Hedef format
        start_address: Start address (optional)
    
    Returns:
        Decompiled code
    """
    decompiler = UnifiedDecompiler(target_format)
    return decompiler.decompile(prg_data, start_address)


def batch_decompile(prg_data: Union[bytes, str], 
                   formats: List[str] = None, 
                   start_address: Optional[int] = None) -> Dict[str, str]:
    """
    Birden fazla formatta decompile
    
    Args:
        prg_data: PRG data
        formats: Format listesi (None ise tümü)
        start_address: Start address (optional)
    
    Returns:
        Format → result dictionary
    """
    if formats is None:
        formats = UnifiedDecompiler.SUPPORTED_FORMATS
    
    results = {}
    for fmt in formats:
        if fmt == 'pseudocode':  # Skip unimplemented
            continue
        try:
            decompiler = UnifiedDecompiler(fmt)
            results[fmt] = decompiler.decompile(prg_data, start_address)
        except Exception as e:
            results[fmt] = f"❌ HATA: {str(e)}"
    
    return results


if __name__ == "__main__":
    # Test için basit örnek
    print("=== UNIFIED DECOMPILER TEST ===")
    
    # Test PRG: LDA #65, JSR $FFD2, RTS
    test_prg = "0108a94120d2ff60"
    
    print(f"Test PRG: {test_prg}")
    
    # Single format test
    print("\n--- Single Format Test ---")
    result = quick_decompile(test_prg, 'c')
    print("C FORMAT:")
    print(result[:200] + "..." if len(result) > 200 else result)
    
    # Batch test
    print("\n--- Batch Test ---") 
    batch_results = batch_decompile(test_prg, ['asm', 'c', 'qbasic'])
    for fmt, res in batch_results.items():
        print(f"\n{fmt.upper()}:")
        print(res[:100] + "..." if len(res) > 100 else res)
