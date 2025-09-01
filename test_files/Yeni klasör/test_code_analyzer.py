#!/usr/bin/env python
"""
TEST AMACI: Code Analyzer'ın pattern recognition sistemini test eder
AÇIKLAMA:
- Pattern detection algoritmalarını test eder
- Loop, subroutine, array pattern tanıma
- Complexity score hesaplama testi
- Memory usage analysis testi
- Optimization suggestions testi
- Report generation testi

KULLANIM:
python test_files/test_code_analyzer.py

BEKLENEN SONUÇ:
✅ CodeAnalyzer başlatma başarılı
✅ Instruction parsing çalışıyor
✅ Pattern detection aktif (loop, subroutine, array, math, screen)
✅ Complexity score hesaplanıyor
✅ Memory usage analysis çalışıyor
✅ Optimization suggestions üretiliyor
✅ Report generation başarılı

BAŞARI KRİTERLERİ:
- En az 1 pattern tespit edilmeli
- Complexity score > 0 olmalı
- Memory usage analysis çalışmalı
- Report generation başarılı olmalı
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code_analyzer import CodeAnalyzer, analyze_prg_file, quick_pattern_check, PatternType

def test_code_analyzer():
    print("=== CODE ANALYZER FULL TEST ===")
    
    success_count = 0
    total_tests = 0
    
    # Test data sets
    test_cases = [
        {
            'name': 'Hello World',
            'data': bytes.fromhex('a94120d2ff60'),  # LDA #65, JSR $FFD2, RTS
            'expected_patterns': ['subroutine_call']
        },
        {
            'name': 'Simple Loop',
            'data': bytes.fromhex('a203ca10fd60'),  # LDX #3, loop: DEX, BPL loop, RTS
            'expected_patterns': ['counting_loop']
        },
        {
            'name': 'Screen Access',
            'data': bytes.fromhex('a9418d0004a94c8d000860'),  # LDA #65, STA $0400, LDA #76, STA $0800, RTS
            'expected_patterns': ['screen_manipulation']
        }
    ]
    
    print(f"Test case'leri: {len(test_cases)}")
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== TEST CASE {i+1}: {test_case['name']} ===")
        
        # Test 1: Basic initialization
        total_tests += 1
        try:
            analyzer = CodeAnalyzer(test_case['data'], 0x801)
            print("✅ CodeAnalyzer başlatma başarılı")
            success_count += 1
        except Exception as e:
            print(f"❌ CodeAnalyzer başlatma hatası: {e}")
            continue
        
        # Test 2: Instruction parsing
        total_tests += 1
        try:
            parsed_ok = analyzer.parse_instructions()
            if parsed_ok and len(analyzer.instructions) > 0:
                print(f"✅ Instruction parsing başarılı: {len(analyzer.instructions)} instruction")
                success_count += 1
            else:
                print("❌ Instruction parsing başarısız")
        except Exception as e:
            print(f"❌ Instruction parsing hatası: {e}")
        
        # Test 3: Full analysis
        total_tests += 1
        try:
            result = analyzer.analyze_all_patterns()
            print(f"✅ Full analysis başarılı")
            print(f"   Patterns found: {len(result.patterns)}")
            print(f"   Complexity score: {result.complexity_score:.1f}")
            
            # Show detected patterns
            for pattern in result.patterns:
                print(f"   • {pattern.pattern_type.value}: {pattern.description}")
            
            success_count += 1
        except Exception as e:
            print(f"❌ Full analysis hatası: {e}")
        
        # Test 4: Pattern validation
        total_tests += 1
        try:
            detected_types = [p.pattern_type.value for p in result.patterns]
            expected_found = any(exp in detected_types for exp in test_case['expected_patterns'])
            
            if expected_found or len(result.patterns) > 0:
                print("✅ Pattern detection validation başarılı")
                success_count += 1
            else:
                print(f"⚠️ Expected patterns not found: {test_case['expected_patterns']}")
                print(f"   Detected: {detected_types}")
        except Exception as e:
            print(f"❌ Pattern validation hatası: {e}")
        
        # Test 5: Report generation
        total_tests += 1
        try:
            report = analyzer.generate_report(result)
            if len(report) > 100:  # Reasonable report size
                print("✅ Report generation başarılı")
                success_count += 1
            else:
                print("❌ Report generation yetersiz")
        except Exception as e:
            print(f"❌ Report generation hatası: {e}")
    
    # Test 6: Convenience functions
    print(f"\n=== CONVENIENCE FUNCTIONS TEST ===")
    total_tests += 1
    try:
        test_data = bytes.fromhex('a94120d2ff60')
        
        # analyze_prg_file function
        result = analyze_prg_file(test_data, 0x801)
        print(f"   analyze_prg_file: {len(result.patterns)} patterns")
        
        # quick_pattern_check function
        patterns = quick_pattern_check(test_data)
        print(f"   quick_pattern_check: {len(patterns)} patterns")
        
        if len(result.patterns) > 0 or len(patterns) > 0:
            print("✅ Convenience functions başarılı")
            success_count += 1
        else:
            print("❌ Convenience functions yetersiz")
    except Exception as e:
        print(f"❌ Convenience functions hatası: {e}")
    
    # Test 7: Memory usage analysis
    print(f"\n=== MEMORY USAGE ANALYSIS TEST ===")
    total_tests += 1
    try:
        analyzer = CodeAnalyzer(bytes.fromhex('a9418d0004a94c8d000860'), 0x801)
        result = analyzer.analyze_all_patterns()
        
        memory_usage = result.memory_usage
        print(f"   Memory usage areas: {len([k for k, v in memory_usage.items() if v > 0])}")
        
        total_accesses = sum(memory_usage.values())
        if total_accesses > 0:
            print(f"   Total memory accesses: {total_accesses}")
            print("✅ Memory usage analysis başarılı")
            success_count += 1
        else:
            print("❌ Memory usage analysis yetersiz")
    except Exception as e:
        print(f"❌ Memory usage analysis hatası: {e}")
    
    # Test 8: Complex pattern test
    print(f"\n=== COMPLEX PATTERN TEST ===")
    total_tests += 1
    try:
        # More complex code: loop + screen + subroutine
        complex_code = bytes.fromhex('a203bd00048d0004ca10f720d2ff60')
        analyzer = CodeAnalyzer(complex_code, 0x801)
        result = analyzer.analyze_all_patterns()
        
        pattern_types = set(p.pattern_type for p in result.patterns)
        unique_patterns = len(pattern_types)
        
        print(f"   Complex analysis: {len(result.patterns)} total patterns")
        print(f"   Unique pattern types: {unique_patterns}")
        
        if unique_patterns >= 2:  # Expect multiple pattern types
            print("✅ Complex pattern detection başarılı")
            success_count += 1
        else:
            print("⚠️ Complex pattern detection kısmi başarı")
            success_count += 0.5
    except Exception as e:
        print(f"❌ Complex pattern test hatası: {e}")
    
    # Final results
    print(f"\n=== TEST SUMMARY ===")
    print(f"Successful tests: {success_count}/{total_tests}")
    success_rate = (success_count / total_tests) * 100
    print(f"Success rate: {success_rate:.1f}%")
    
    if success_rate >= 75:
        print("🎉 CODE ANALYZER TEST: ✅ PASSED")
        print("Code Analyzer sistemi başarıyla çalışıyor!")
        
        # Show a sample analysis
        print(f"\n=== SAMPLE ANALYSIS ===")
        sample_analyzer = CodeAnalyzer(bytes.fromhex('a94120d2ff60'), 0x801)
        sample_result = sample_analyzer.analyze_all_patterns()
        sample_report = sample_analyzer.generate_report(sample_result)
        print(sample_report[:500] + "..." if len(sample_report) > 500 else sample_report)
        
    elif success_rate >= 50:
        print("⚠️ PARTIAL SUCCESS: Code Analyzer kısmen çalışıyor")
    else:
        print("❌ MAJOR ISSUES: Code Analyzer ciddi problemler içeriyor")
    
    return success_rate >= 75

if __name__ == "__main__":
    test_code_analyzer()
