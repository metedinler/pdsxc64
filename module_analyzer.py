#!/usr/bin/env python3
"""
Module Usage Analyzer for D64 Converter Project
Analyzes which modules are used/unused in the codebase
"""

import os
import ast
import sys

def extract_imports(file_path):
    """Extract all import statements from a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=file_path)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        
        return imports
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return []

def main():
    # Ana dosyalar
    core_files = [
        'main.py', 'main_ultimate.py', 'main_legacy.py', 'main_complete_restore.py',
        'gui_demo.py', 'gui_manager.py', 'clean_gui_selector.py', 'eski_gui_3.py',
        'enhanced_c64_memory_manager.py', 'unified_decompiler.py', 'code_analyzer.py',
        'assembly_formatters.py', 'disassembler.py', 'advanced_disassembler.py',
        'improved_disassembler.py', 'py65_professional_disassembler.py',
        'd64_reader.py', 'c64_basic_parser.py', 'parser.py', 'sid_converter.py', 'sprite_converter.py'
    ]

    print('🔍 MODUL IMPORT ANALİZİ')
    print('='*80)

    all_imports = set()
    used_modules = set()
    import_details = {}

    # Standard library modules to filter out
    stdlib_modules = [
        'tkinter', 'os', 'sys', 'json', 'pathlib', 'typing', 're', 'threading', 
        'logging', 'datetime', 'argparse', 'subprocess', 'platform', 'venv', 
        'time', 'collections', 'math', 'ast', 'warnings', 'io', 'copy', 'struct', 
        'base64', 'hashlib', 'urllib', 'tempfile', 'shutil', 'glob', 'unittest', 
        'pickle', 'csv', 'PIL', 'pillow', 'numpy', 'py65', 'tkinterdnd2', 'colorama'
    ]

    for file_name in core_files:
        if os.path.exists(file_name):
            imports = extract_imports(file_name)
            local_imports = [imp for imp in imports if not any(imp.startswith(lib) for lib in stdlib_modules)]
            
            if local_imports:
                print(f'📁 {file_name}:')
                import_details[file_name] = local_imports
                for imp in local_imports:
                    print(f'   ├─ {imp}')
                    all_imports.add(imp)
                    
                    # Check if this import corresponds to an existing file
                    possible_files = [f'{imp}.py', f'{imp.replace(".", "/")}.py']
                    for pf in possible_files:
                        if os.path.exists(pf):
                            used_modules.add(pf)
                print()
        else:
            print(f'❌ {file_name}: BULUNAMADI')

    print('\n📊 ÖZET:')
    print('='*50)
    print(f'📄 Toplam core dosyalar: {len(core_files)}')
    print(f'✅ Mevcut dosyalar: {len([f for f in core_files if os.path.exists(f)])}')
    print(f'📦 Import edilen lokal modüller: {len(all_imports)}')
    print(f'🔗 Kullanılan modüller: {len(used_modules)}')

    print('\n🔍 DETAYLAR:')
    print('='*50)
    
    existing_files = [f for f in core_files if os.path.exists(f)]
    unused_files = []
    
    for file in existing_files:
        is_imported = False
        file_without_ext = file.replace('.py', '')
        
        for other_file, imports in import_details.items():
            if file_without_ext in imports or file in imports:
                is_imported = True
                break
        
        if not is_imported and file not in ['main.py', 'main_ultimate.py', 'main_legacy.py']:
            unused_files.append(file)

    print(f'\n✅ KULLANILAN MODULLER ({len(existing_files) - len(unused_files)} adet):')
    for file in existing_files:
        if file not in unused_files:
            print(f'   ✓ {file}')

    print(f'\n⚠️  KULLANILMAYAN MODULLER ({len(unused_files)} adet):')
    for file in unused_files:
        print(f'   ⚪ {file}')

    print(f'\n🎯 ÖNERİLER:')
    print('='*50)
    if unused_files:
        print(f'• {len(unused_files)} adet kullanılmayan modül temizlenebilir')
        print('• Backup alınarak bu dosyalar silinebilir veya archive klasörüne taşınabilir')
    else:
        print('• Tüm modüller aktif olarak kullanılıyor!')

if __name__ == "__main__":
    main()
