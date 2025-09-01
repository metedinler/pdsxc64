#!/usr/bin/env python3

with open('pdsxv12xNEW.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_class = False
last_method_line = 0
class_end_line = 0

for i, line in enumerate(lines):
    stripped = line.strip()
    
    if 'class pdsXInterpreter:' in line:
        in_class = True
        print(f"Found pdsXInterpreter class at line {i+1}")
        
    elif in_class and stripped.startswith('def ') and not stripped.startswith('def main'):
        last_method_line = i+1
        print(f"Found method: {stripped[:50]} at line {i+1}")
        
    elif in_class and (stripped.startswith('class ') or stripped.startswith('def main') or stripped.startswith('# Main')):
        class_end_line = i+1
        print(f"Class ends at line {i+1}: {stripped[:50]}")
        break

print(f"\nSummary:")
print(f"Class starts: around line 3559")
print(f"Last method: line {last_method_line}")
print(f"Class ends: line {class_end_line}")

# Check if C64 method is inside class
c64_method_line = 7795
print(f"C64 method at line {c64_method_line}")
if c64_method_line < class_end_line:
    print("C64 method is INSIDE the class")
else:
    print("C64 method is OUTSIDE the class - THIS IS THE PROBLEM!")
