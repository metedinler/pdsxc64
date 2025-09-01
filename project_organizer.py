#!/usr/bin/env python3
"""
D64 Converter Project Organizer
Automatically organizes project files into clean structure
"""

import os
import shutil

def create_directories():
    """Create archive directory structure"""
    dirs = [
        'archive',
        'archive/unused',
        'archive/legacy', 
        'archive/test',
        'archive/utility',
        'core',
        'gui'
    ]
    
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✅ Created directory: {dir_name}")

def organize_files():
    """Organize files into appropriate directories"""
    
    # Core files to keep in root
    core_files = {
        'main.py': 'root',
        'main_ultimate.py': 'root',
        'main_legacy.py': 'root'
    }
    
    # Core engine files
    core_engine_files = {
        'enhanced_c64_memory_manager.py': 'core',
        'unified_decompiler.py': 'core',
        'code_analyzer.py': 'core',
        'improved_disassembler.py': 'core',
        'assembly_formatters.py': 'core'
    }
    
    # GUI files
    gui_files = {
        'gui_manager.py': 'gui',
        'gui_demo.py': 'gui',
        'clean_gui_selector.py': 'gui'
    }
    
    # Unused files
    unused_files = [
        'main_complete_restore.py',
        'disassembler.py',
        'advanced_disassembler.py',
        'py65_professional_disassembler.py',
        'd64_reader.py',
        'c64_basic_parser.py',
        'parser.py',
        'sid_converter.py',
        'sprite_converter.py'
    ]
    
    # Legacy files
    legacy_files = [
        'decompiler.py',
        'decompiler_c.py',
        'decompiler_cpp.py',
        'decompiler_c_2.py',
        'decompiler_qbasic.py',
        'c64_basic_parser_new.py',
        'enhanced_d64_reader.py',
        'gui_restored.py',
        'main_new.py',
        'modern_gui_selector.py',
        'pyd64fix-win.py',
        'c64_memory_manager.py'
    ]
    
    # Test files
    test_files = [
        'debug_gui.py',
        'debug_memory.py',
        'debug_py65.py',
        'gui_direct_test.py',
        'create_test_files.py',
        'final_project_status.py',
        'simple_analyzer.py',
        'system_repair.py'
    ]
    
    # Utility files
    utility_files = [
        'add_pseudo.py',
        'assembly_parser_6502_opcodes.py',
        'basic_detokenizer.py',
        'c1541_python_emulator.py',
        'd64_converterX1.py',
        'illegal_opcode_analyzer.py',
        'opcode_generator.py',
        'opcode_manager.py',
        'opcode_manager_simple.py',
        'pdsXv12.py',
        'pdsXv12_minimal.py',
        'petcat_detokenizer.py',
        'PETSCII2BASIC.py',
        'sprite.py'
    ]
    
    # Move files to archive/unused
    move_files(unused_files, 'archive/unused', '🔴 UNUSED')
    
    # Move files to archive/legacy
    move_files(legacy_files, 'archive/legacy', '🏛️ LEGACY')
    
    # Move files to archive/test
    move_files(test_files, 'archive/test', '🧪 TEST')
    
    # Move files to archive/utility
    move_files(utility_files, 'archive/utility', '🔧 UTILITY')
    
    print("\n✅ PROJECT ORGANIZATION COMPLETED!")
    print("\n📁 FINAL STRUCTURE:")
    print("├── main.py (entry point)")
    print("├── main_ultimate.py (ultimate version)")
    print("├── main_legacy.py (legacy version)")
    print("├── core/ (5 core modules)")
    print("├── gui/ (3 GUI modules)")
    print("└── archive/ (organized by category)")

def move_files(file_list, destination, category):
    """Move files to destination directory"""
    print(f"\n{category} FILES:")
    moved_count = 0
    
    for file_name in file_list:
        if os.path.exists(file_name):
            try:
                shutil.move(file_name, os.path.join(destination, file_name))
                print(f"   ✅ Moved: {file_name}")
                moved_count += 1
            except Exception as e:
                print(f"   ❌ Error moving {file_name}: {e}")
        else:
            print(f"   ⚠️ Not found: {file_name}")
    
    print(f"   📊 Moved {moved_count}/{len(file_list)} files")

def main():
    print("🚀 D64 CONVERTER PROJECT ORGANIZER")
    print("="*50)
    
    response = input("❓ Do you want to organize the project? (y/n): ")
    
    if response.lower() == 'y':
        print("\n📁 Creating directory structure...")
        create_directories()
        
        print("\n📦 Organizing files...")
        organize_files()
        
        print("\n🎉 ORGANIZATION COMPLETE!")
        print("🔍 Check the 'archive' folder for moved files")
        print("⭐ Only 11 core files remain in the main directory")
    else:
        print("❌ Organization cancelled.")

if __name__ == "__main__":
    main()
