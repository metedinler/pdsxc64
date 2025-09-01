#!/usr/bin/env python3
"""Petcat test script"""

from petcat_detokenizer import PetcatDetokenizer
import os

def test_petcat():
    print("🔍 Testing Petcat Detokenizer...")
    
    petcat = PetcatDetokenizer()
    print(f"✅ Petcat available: {petcat.available}")
    print(f"✅ Petcat path: {petcat.petcat_path}")
    
    if petcat.petcat_path and os.path.exists(petcat.petcat_path):
        print("✅ petcat.exe found and accessible")
        
        # Test with simple BASIC program
        test_data = bytes([
            0x01, 0x08,  # Start address $0801
            0x0B, 0x08,  # Next line pointer
            0x0A, 0x00,  # Line 10
            0x97,        # PRINT token
            0x22,        # "
            0x48, 0x45, 0x4C, 0x4C, 0x4F,  # HELLO
            0x22,        # "
            0x00,        # End of line
            0x00, 0x00   # End of program
        ])
        
        print(f"🧪 Testing with sample BASIC program ({len(test_data)} bytes)")
        result = petcat.detokenize_prg(test_data)
        
        print(f"📋 Petcat result:")
        for i, line in enumerate(result):
            print(f"   {i+1}: {line}")
            
    else:
        print("❌ petcat.exe not found or not accessible")
        print("🔧 Make sure VICE emulator is installed or petcat.exe is in the current directory")

if __name__ == "__main__":
    test_petcat()
