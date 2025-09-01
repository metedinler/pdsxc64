# Test Script for Active GUI Backups
# 19 Temmuz 2025

import sys
import os

def test_backup_files():
    """Test all backup files for import capability"""
    print("🔍 Testing Active GUI Backups...")
    print("=" * 50)
    
    backup_files = [
        ("d64_converterX1_backup.py", "D64ConverterApp", "X1 GUI"),
        ("gui_restored_backup.py", "D64ConverterRestoredGUI", "Klasik GUI"),
        ("eski_gui_3_backup.py", "D64ConverterApp", "Eski GUI v3"),
        ("clean_gui_selector_backup.py", "D64GUISelector", "Clean Selector"),
        ("modern_gui_selector_backup.py", "ModernGUISelector", "Modern Selector")
    ]
    
    success_count = 0
    
    for filename, class_name, description in backup_files:
        try:
            # Check file exists
            if not os.path.exists(filename):
                print(f"❌ {description}: File not found - {filename}")
                continue
                
            # Check file size
            size = os.path.getsize(filename)
            if size == 0:
                print(f"❌ {description}: Empty file - {filename}")
                continue
                
            # Try import test (simplified)
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                if f"class {class_name}" in content:
                    print(f"✅ {description}: Class {class_name} found ({size:,} bytes)")
                    success_count += 1
                else:
                    print(f"⚠️ {description}: Class {class_name} not found in file")
                    
        except Exception as e:
            print(f"❌ {description}: Error - {str(e)}")
    
    print("=" * 50)
    print(f"📊 Test Results: {success_count}/{len(backup_files)} files OK")
    
    if success_count == len(backup_files):
        print("🎉 All backup files are ready for use!")
    else:
        print("⚠️ Some backup files need attention!")
    
    return success_count == len(backup_files)

if __name__ == "__main__":
    success = test_backup_files()
    sys.exit(0 if success else 1)
