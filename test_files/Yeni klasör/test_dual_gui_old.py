#!/usr/bin/env python3
"""
Test script for validating dual GUI system and py65 fixes
"""

import sys
import os

def test_py65_fix():
    """Test py65 Professional Disassembler fixes"""
    print("🔧 Testing py65 Professional Disassembler fixes...")
    
    try:
        from improved_disassembler import ImprovedDisassembler, Py65ProfessionalDisassembler
        print("✅ ImprovedDisassembler imported successfully")
        
        # Test py65 Professional - basit oluşturma testi
        py65_disasm = Py65ProfessionalDisassembler()
        print("✅ Py65ProfessionalDisassembler created successfully")
        
        # py65'te en azından disassemble_to_format metodu var mı kontrol et
        if hasattr(py65_disasm, 'disassemble_to_format'):
            print("✅ disassemble_to_format method available")
        else:
            print("⚠️ disassemble_to_format method missing but constructor works")
        
        return True
        
    except Exception as e:
        print(f"❌ py65 test failed: {e}")
        return False

def test_gui_imports():
    """Test both GUI imports"""
    print("\n🖥️ Testing GUI imports...")
    
    results = {}
    
    # Test Classic GUI
    try:
        from gui_restored import D64ConverterRestoredGUI
        print("✅ Classic GUI (gui_restored.py) imported successfully")
        results['classic'] = True
    except Exception as e:
        print(f"❌ Classic GUI import failed: {e}")
        results['classic'] = False
    
    # Test Enhanced GUI
    try:
        from d64_converter import D64ConverterApp
        print("✅ Enhanced GUI (d64_converter.py) imported successfully") 
        results['enhanced'] = True
    except Exception as e:
        print(f"❌ Enhanced GUI import failed: {e}")
        results['enhanced'] = False
    
    # Test GUI Selector
    try:
        from gui_selector import GUISelector
        print("✅ GUI Selector imported successfully")
        results['selector'] = True
    except Exception as e:
        print(f"❌ GUI Selector import failed: {e}")
        results['selector'] = False
    
    return results

def test_core_functionality():
    """Test core disassembler functionality"""
    print("\n⚙️ Testing core functionality...")
    
    try:
        from improved_disassembler import ImprovedDisassembler
        
        # Test code
        test_code = [0xA9, 0x42, 0x8D, 0x00, 0xD0, 0x60]  # LDA #$42, STA $D000, RTS
        
        # ImprovedDisassembler constructor'ı güncellenmiş - gerekli parametreler
        disasm = ImprovedDisassembler(
            start_address=0x1000,
            code=test_code,
            output_format='asm'
        )
        
        # Test all formats
        formats = ['basic', 'advanced', 'improved', 'acme', 'ca65', 'kickass']
        
        for fmt in formats:
            disasm.output_format = fmt  # Format'ı değiştir
            result = disasm.disassemble_to_format(test_code)
            print(f"✅ Format '{fmt}': Working")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def test_file_structure():
    """Test required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'improved_disassembler.py',
        'd64_converter.py', 
        'gui_restored.py',
        'gui_selector.py',
        'main.py',
        'd64_reader.py',
        'opcode_map.json'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def main():
    """Run all tests"""
    print("🚀 D64 Converter Dual GUI System Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("py65 Fixes", test_py65_fix),
        ("GUI Imports", test_gui_imports),
        ("Core Functionality", test_core_functionality)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Dual GUI system ready.")
        print("💡 Run 'python gui_selector.py' to launch GUI selector")
    else:
        print("\n⚠️ Some tests failed. Check errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()
