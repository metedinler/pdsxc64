#!/usr/bin/env python
"""
TEST AMACI: Enhanced Unified Decompiler (Code Analyzer entegrasyonlu) test eder
AÇIKLAMA:
- UnifiedDecompiler + CodeAnalyzer entegrasyonu
- Code pattern analysis ile enhanced decompile
- Pattern detection + optimization suggestions
- Enhanced statistics ve reporting
- Full system integration testi

KULLANIM:
python test_files/test_enhanced_unified_decompiler.py

BEKLENEN SONUÇ:
✅ Enhanced UnifiedDecompiler başlatma başarılı
✅ Code pattern analysis entegrasyonu çalışıyor
✅ Pattern detection active (loop, subroutine, etc.)
✅ Enhanced statistics işlevsel
✅ Optimization suggestions üretiliyor
✅ Analysis reporting çalışıyor

BAŞARI KRİTERLERİ:
- Decompile + code analysis birlikte çalışmalı
- Pattern detection aktif olmalı
- Enhanced statistics mevcut olmalı
- Analysis report üretilmeli
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unified_decompiler import UnifiedDecompiler, quick_decompile

def test_enhanced_unified_decompiler():
    print("=== ENHANCED UNIFIED DECOMPILER TEST ===")
    
    success_count = 0
    total_tests = 0
    
    # Test data: More complex program
    test_cases = [
        {
            'name': 'Hello World with Analysis',
            'data': '0108a94120d2ff60',  # LDA #65, JSR $FFD2, RTS
            'expected_features': ['subroutine_call', 'enhanced_stats']
        },
        {
            'name': 'Complex Pattern Test',
            'data': '0108a203bd00048d0004ca10f720d2ff60',  # LDX #3, loop, JSR CHROUT, RTS
            'expected_features': ['patterns', 'complexity']
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== TEST CASE {i+1}: {test_case['name']} ===")
        
        # Test 1: Enhanced decompile with analysis
        total_tests += 1
        try:
            decompiler = UnifiedDecompiler('c')
            result = decompiler.decompile(test_case['data'], enable_code_analysis=True)
            
            if "❌ HATA" not in result and len(result) > 50:
                print("✅ Enhanced decompile başarılı")
                success_count += 1
            else:
                print(f"❌ Enhanced decompile failed: {result[:100]}")
        except Exception as e:
            print(f"❌ Enhanced decompile exception: {e}")
        
        # Test 2: Code analysis integration
        total_tests += 1
        try:
            analysis = decompiler.get_code_analysis()
            if analysis and hasattr(analysis, 'patterns'):
                print(f"✅ Code analysis integration: {len(analysis.patterns)} patterns")
                success_count += 1
            else:
                print("❌ Code analysis integration failed")
        except Exception as e:
            print(f"❌ Code analysis exception: {e}")
        
        # Test 3: Enhanced statistics
        total_tests += 1
        try:
            stats = decompiler.get_stats()
            enhanced_keys = ['patterns_detected', 'complexity_score', 'memory_usage_areas']
            has_enhanced = any(key in stats for key in enhanced_keys)
            
            if has_enhanced:
                print("✅ Enhanced statistics available")
                for key in enhanced_keys:
                    if key in stats:
                        print(f"   {key}: {stats[key]}")
                success_count += 1
            else:
                print("❌ Enhanced statistics missing")
        except Exception as e:
            print(f"❌ Enhanced statistics exception: {e}")
        
        # Test 4: Pattern summary
        total_tests += 1
        try:
            pattern_summary = decompiler.get_pattern_summary()
            print(f"✅ Pattern summary: {len(pattern_summary)} patterns")
            for pattern in pattern_summary[:3]:  # Show first 3
                print(f"   • {pattern}")
            success_count += 1
        except Exception as e:
            print(f"❌ Pattern summary exception: {e}")
        
        # Test 5: Optimization suggestions
        total_tests += 1
        try:
            suggestions = decompiler.get_optimization_suggestions()
            print(f"✅ Optimization suggestions: {len(suggestions)}")
            for suggestion in suggestions[:2]:  # Show first 2
                print(f"   • {suggestion}")
            success_count += 1
        except Exception as e:
            print(f"❌ Optimization suggestions exception: {e}")
        
        # Test 6: Analysis report
        total_tests += 1
        try:
            report = decompiler.get_analysis_report()
            if len(report) > 100 and "CODE ANALYSIS REPORT" in report:
                print("✅ Analysis report generation başarılı")
                success_count += 1
            else:
                print("❌ Analysis report insufficient")
        except Exception as e:
            print(f"❌ Analysis report exception: {e}")
    
    # Test 7: Batch analysis
    print(f"\n=== BATCH ANALYSIS TEST ===")
    total_tests += 1
    try:
        from unified_decompiler import batch_decompile
        
        test_data = '0108a94120d2ff60'
        batch_results = batch_decompile(test_data, ['asm', 'c'])
        
        successful_batch = 0
        for fmt, result in batch_results.items():
            if "❌ HATA" not in result and len(result) > 50:
                successful_batch += 1
        
        if successful_batch >= 1:
            print(f"✅ Batch analysis: {successful_batch} formats başarılı")
            success_count += 1
        else:
            print("❌ Batch analysis insufficient")
    except Exception as e:
        print(f"❌ Batch analysis exception: {e}")
    
    # Test 8: Analysis levels
    print(f"\n=== ANALYSIS LEVELS TEST ===")
    total_tests += 1
    try:
        test_data = '0108a94120d2ff60'
        
        # Basic level (no analysis)
        decompiler_basic = UnifiedDecompiler('c')
        result_basic = decompiler_basic.decompile(test_data, analysis_level='basic', enable_code_analysis=False)
        
        # Advanced level (with analysis)
        decompiler_advanced = UnifiedDecompiler('c')
        result_advanced = decompiler_advanced.decompile(test_data, analysis_level='advanced', enable_code_analysis=True)
        
        basic_analysis = decompiler_basic.get_code_analysis()
        advanced_analysis = decompiler_advanced.get_code_analysis()
        
        if (basic_analysis is None and 
            advanced_analysis is not None and 
            len(result_basic) > 0 and 
            len(result_advanced) > 0):
            print("✅ Analysis levels differentiation başarılı")
            print(f"   Basic: No analysis, {len(result_basic)} chars")
            print(f"   Advanced: {len(advanced_analysis.patterns)} patterns, {len(result_advanced)} chars")
            success_count += 1
        else:
            print("❌ Analysis levels differentiation failed")
    except Exception as e:
        print(f"❌ Analysis levels exception: {e}")
    
    # Final results
    print(f"\n=== TEST SUMMARY ===")
    print(f"Successful tests: {success_count}/{total_tests}")
    success_rate = (success_count / total_tests) * 100
    print(f"Success rate: {success_rate:.1f}%")
    
    if success_rate >= 75:
        print("🎉 ENHANCED UNIFIED DECOMPILER TEST: ✅ PASSED")
        print("Enhanced Unified Decompiler sistemi başarıyla çalışıyor!")
        
        # Show sample enhanced output
        print(f"\n=== SAMPLE ENHANCED OUTPUT ===")
        sample_decompiler = UnifiedDecompiler('c')
        sample_result = sample_decompiler.decompile('0108a94120d2ff60', enable_code_analysis=True)
        sample_stats = sample_decompiler.get_stats()
        sample_report = sample_decompiler.get_analysis_report()
        
        print("DECOMPILED CODE:")
        print(sample_result[:200] + "..." if len(sample_result) > 200 else sample_result)
        
        print(f"\nENHANCED STATS:")
        for key, value in sample_stats.items():
            if key.startswith(('patterns_', 'complexity_', 'memory_', 'optimization_')):
                print(f"  {key}: {value}")
        
        print(f"\nANALYSIS REPORT (excerpt):")
        print(sample_report[:300] + "..." if len(sample_report) > 300 else sample_report)
        
    elif success_rate >= 50:
        print("⚠️ PARTIAL SUCCESS: Enhanced system kısmen çalışıyor")
    else:
        print("❌ MAJOR ISSUES: Enhanced system ciddi problemler içeriyor")
    
    return success_rate >= 75

if __name__ == "__main__":
    test_enhanced_unified_decompiler()
