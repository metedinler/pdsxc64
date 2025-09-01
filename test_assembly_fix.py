#!/usr/bin/env python3
"""
Test script for AdvancedDisassembler - Assembly extraction fix test
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_advanced_disassembler():
    """Test AdvancedDisassembler with 'asm' output format"""
    print("🔧 Testing AdvancedDisassembler with ASM format...")
    
    try:
        from advanced_disassembler import AdvancedDisassembler
        
        # Test code: Simple LDA/STA instructions
        test_code = bytes([
            0xA9, 0x00,  # LDA #$00
            0x8D, 0x20, 0xD0,  # STA $D020 (border color)
            0xA9, 0x01,  # LDA #$01
            0x8D, 0x21, 0xD0,  # STA $D021 (background color)
            0x60  # RTS
        ])
        
        start_address = 0x1000
        
        print(f"📄 Test code: {len(test_code)} bytes")
        print(f"🎯 Start address: ${start_address:04X}")
        
        # Test with 'asm' format (NEW)
        print("\n=== Testing 'asm' format ===")
        try:
            disassembler = AdvancedDisassembler(
                start_address=start_address,
                code=test_code,
                output_format='asm'
            )
            asm_result = disassembler.disassemble()
            print("✅ 'asm' format test - SUCCESS")
            print("Assembly output:")
            print(asm_result)
            print()
        except Exception as e:
            print(f"❌ 'asm' format test - FAILED: {e}")
            return False
        
        # Test with 'tass' format (Should work)
        print("=== Testing 'tass' format ===")
        try:
            disassembler = AdvancedDisassembler(
                start_address=start_address,
                code=test_code,
                output_format='tass'
            )
            tass_result = disassembler.disassemble()
            print("✅ 'tass' format test - SUCCESS")
            print("TASS output:")
            for line in tass_result:
                print(line)
            print()
        except Exception as e:
            print(f"❌ 'tass' format test - FAILED: {e}")
        
        # Test default format
        print("=== Testing default format ===")
        try:
            disassembler = AdvancedDisassembler(
                start_address=start_address,
                code=test_code
            )
            default_result = disassembler.disassemble()
            print("✅ Default format test - SUCCESS")
            print(f"Default format result type: {type(default_result)}")
            if isinstance(default_result, str):
                print("Default output:")
                print(default_result[:200] + "..." if len(default_result) > 200 else default_result)
            elif isinstance(default_result, list):
                print("Default output (first 5 lines):")
                for line in default_result[:5]:
                    print(line)
            print()
        except Exception as e:
            print(f"❌ Default format test - FAILED: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Assembly Extraction Fix Test")
    print("=" * 50)
    
    success = test_advanced_disassembler()
    
    if success:
        print("🎉 Test completed!")
    else:
        print("❌ Test failed!")
        sys.exit(1)
