#!/usr/bin/env python3
import re

with open('gui_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Font tanımını bul ve düzelt
pattern = r'(font=\("Consolas", 10\),)\n(            \n            # Syntax highlighting)'
replacement = r'\1\n                                                  insertbackground=ModernStyle.FG_ACCENT)\n            text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)\n            \n            # Syntax highlighting'

fixed_content = re.sub(pattern, replacement, content)

with open('gui_manager.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print('ScrolledText syntax düzeltildi')
