#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Transpiler Engine Demo - Faz 3.2 Test
"""
from transpiler_engine import EnhancedTranspilerEngine, TranspilationContext, LanguageTarget, TranspilationQuality
from c64_enhanced_knowledge_manager import KnowledgeLevel

def main():
    print("🚀 FAZ 3.2 ENHANCED TRANSPILER ENGINE DEMO")
    print("=" * 50)
    
    # Test assembly kodu - VIC-II border color manipulation
    test_assembly = """
LDA #$05        ; Load color 5 into accumulator
STA $D020       ; Set VIC-II border color
LDX #$00        ; Load 0 into X register  
STA $0400,X     ; Set screen character at position X
RTS             ; Return from subroutine
"""
    
    # Create transpiler engine
    engine = EnhancedTranspilerEngine()
    
    # Test context - Enhanced quality with hardware info
    context = TranspilationContext(
        target_language=LanguageTarget.PYTHON,
        quality_level=TranspilationQuality.ENHANCED, 
        include_comments=True,
        include_hardware_info=True,
        knowledge_level=KnowledgeLevel.ANNOTATED
    )
    
    print(f"\n🔄 Test: Assembly → {context.target_language.value.upper()}")
    print("Assembly Code:")
    print(test_assembly.strip())
    
    # Test transpilation
    result = engine.transpile_assembly(test_assembly, context)
    
    if result.success:
        print("\n✅ TRANSPILATION SUCCESS!")
        print(f"📄 Generated {context.target_language.value.upper()} code:")
        print("-" * 40)
        print(result.output)
        print("-" * 40)
        print(f"📊 Stats: {len(result.output)} characters generated")
        print(f"🧠 Enhanced Knowledge Manager: {result.conversion_notes}")
    else:
        print(f"\n❌ TRANSPILATION FAILED: {result.error_message}")
        
    # Test C transpilation too
    print("\n" + "=" * 50)
    context.target_language = LanguageTarget.C
    print(f"🔄 Test: Assembly → {context.target_language.value.upper()}")
    
    result_c = engine.transpile_assembly(test_assembly, context)
    if result_c.success:
        print("✅ C TRANSPILATION SUCCESS!")
        print("📄 Generated C code preview:")
        print("-" * 40)
        print(result_c.output[:500] + "...")
        print("-" * 40)
    else:
        print(f"❌ C TRANSPILATION FAILED: {result_c.error_message}")

if __name__ == "__main__":
    main()
