#!/usr/bin/env python3
"""
6502 Assembly Syntax Highlighter
Hem Viper IDE hem de GUI Manager için syntax highlighting

Bu modül şunları sağlar:
- 6502 Assembly syntax highlighting
- C64 BASIC syntax highlighting
- Memory location highlighting
- Opcode tanıma ve renklendirme
- Tkinter text widget entegrasyonu
"""

import tkinter as tk
import re
from typing import Dict, List, Tuple, Optional

class SyntaxHighlighter:
    """Base syntax highlighter sınıfı"""
    
    def __init__(self, text_widget: tk.Text):
        self.text_widget = text_widget
        self.setup_tags()
        
    def setup_tags(self):
        """Syntax highlighting tag'lerini yapılandır"""
        pass
    
    def highlight(self, start="1.0", end="end"):
        """Text'i highlight et"""
        pass
    
    def clear_tags(self, start="1.0", end="end"):
        """Tüm tag'leri temizle"""
        for tag in self.text_widget.tag_names():
            if not tag.startswith('sel'):  # Selection tag'lerini korumak
                self.text_widget.tag_remove(tag, start, end)

class Assembly6502Highlighter(SyntaxHighlighter):
    """6502 Assembly syntax highlighter"""
    
    def __init__(self, text_widget: tk.Text):
        # 6502 Assembly keywords
        self.opcodes = {
            'ADC', 'AND', 'ASL', 'BCC', 'BCS', 'BEQ', 'BIT', 'BMI', 'BNE', 'BPL',
            'BRK', 'BVC', 'BVS', 'CLC', 'CLD', 'CLI', 'CLV', 'CMP', 'CPX', 'CPY',
            'DEC', 'DEX', 'DEY', 'EOR', 'INC', 'INX', 'INY', 'JMP', 'JSR', 'LDA',
            'LDX', 'LDY', 'LSR', 'NOP', 'ORA', 'PHA', 'PHP', 'PLA', 'PLP', 'ROL',
            'ROR', 'RTI', 'RTS', 'SBC', 'SEC', 'SED', 'SEI', 'STA', 'STX', 'STY',
            'TAX', 'TAY', 'TSX', 'TXA', 'TXS', 'TYA'
        }
        
        # Assembly directives
        self.directives = {
            'ORG', 'BYTE', 'WORD', 'TEXT', 'INCLUDE', 'DEFINE', 'EQU',
            '.pc', '.byte', '.word', '.text', '.include', '.define', '.macro', '.endm',
            '*=', 'DB', 'DW', 'DS', 'ALIGN', '!byte', '!word', '!text', '!fill'
        }
        
        # C64 memory locations
        self.c64_memory = {
            '$0000', '$0001', '$0002', '$00BA', '$00C1', '$00C2',  # Zero page
            '$0200', '$0300', '$0400', '$0800', '$0801',          # BASIC areas
            '$A000', '$A002', '$A004', '$A006', '$A008',          # BASIC ROM
            '$D000', '$D010', '$D020', '$D021', '$D400', '$D800', # I/O
            '$DC00', '$DD00', '$FFFE', '$FFFA', '$FFFC',          # Hardware
            '$4000', '$6000', '$8000', '$C000', '$E000'           # Memory banks
        }
        
        # 64tass specific
        self.tass_directives = {
            '*=', '.proc', '.pend', '.block', '.bend', '.page', '.align',
            '.fill', '.text', '.shift', '.shiftl', '.enc', '.cpu'
        }
        
        # KickAssembler specific  
        self.kickass_directives = {
            '.pc', '.pseudopc', '.namespace', '.filenamespace', '.import',
            '.importonce', '.label', '.const', '.var', '.eval', '.print',
            '.error', '.warning', '.macro', '.function', '.return'
        }
        
        super().__init__(text_widget)
    
    def setup_tags(self):
        """6502 Assembly syntax highlighting tag'lerini yapılandır"""
        # Opcode - Mavi, kalın
        self.text_widget.tag_configure('opcode', 
                                     foreground='#0066CC', 
                                     font=('Courier', 10, 'bold'))
        
        # Directive - Mor, kalın
        self.text_widget.tag_configure('directive', 
                                     foreground='#800080', 
                                     font=('Courier', 10, 'bold'))
        
        # Hex değer - Turuncu
        self.text_widget.tag_configure('hex', 
                                     foreground='#FF8000')
        
        # Immediate değer - Yeşil
        self.text_widget.tag_configure('immediate', 
                                     foreground='#008000')
        
        # Comment - Gri, italik
        self.text_widget.tag_configure('comment', 
                                     foreground='#808080', 
                                     font=('Courier', 10, 'italic'))
        
        # Label - Kırmızımsı, kalın
        self.text_widget.tag_configure('label', 
                                     foreground='#CC0000', 
                                     font=('Courier', 10, 'bold'))
        
        # Memory location - Lacivert
        self.text_widget.tag_configure('memory', 
                                     foreground='#000080',
                                     font=('Courier', 10, 'bold'))
        
        # String - Koyu yeşil
        self.text_widget.tag_configure('string', 
                                     foreground='#006600')
        
        # Number - Turuncu
        self.text_widget.tag_configure('number', 
                                     foreground='#FF6600')
        
        # Register - Mavi
        self.text_widget.tag_configure('register', 
                                     foreground='#0066FF',
                                     font=('Courier', 10, 'bold'))
        
        # Default - Siyah
        self.text_widget.tag_configure('default', 
                                     foreground='#000000')
    
    def highlight(self, start="1.0", end="end"):
        """6502 Assembly syntax highlighting uygula"""
        # Önce mevcut tag'leri temizle
        self.clear_tags(start, end)
        
        # Text içeriğini al
        content = self.text_widget.get(start, end)
        lines = content.split('\n')
        
        current_line = 1
        for line in lines:
            self.highlight_line(line, current_line)
            current_line += 1
    
    def highlight_line(self, line: str, line_num: int):
        """Tek bir satırı highlight et"""
        # Boş satırları atla
        if not line.strip():
            return
        
        # Comment satırları
        comment_match = re.search(r';.*$', line)
        if comment_match:
            start_pos = f"{line_num}.{comment_match.start()}"
            end_pos = f"{line_num}.{comment_match.end()}"
            self.text_widget.tag_add('comment', start_pos, end_pos)
        
        # String literals
        string_pattern = r'"[^"]*"'
        for match in re.finditer(string_pattern, line):
            start_pos = f"{line_num}.{match.start()}"
            end_pos = f"{line_num}.{match.end()}"
            self.text_widget.tag_add('string', start_pos, end_pos)
        
        # Words'leri analiz et
        words = re.findall(r'\S+', line)
        current_pos = 0
        
        for word in words:
            # Word'ün pozisyonunu bul
            word_start = line.find(word, current_pos)
            if word_start == -1:
                continue
            
            word_end = word_start + len(word)
            current_pos = word_end
            
            start_pos = f"{line_num}.{word_start}"
            end_pos = f"{line_num}.{word_end}"
            
            # Word analizi
            word_upper = word.upper()
            
            # Label check (word ends with :)
            if word.endswith(':'):
                self.text_widget.tag_add('label', start_pos, end_pos)
            
            # Opcode check
            elif word_upper in self.opcodes:
                self.text_widget.tag_add('opcode', start_pos, end_pos)
            
            # Directive check
            elif (word_upper in self.directives or 
                  word_upper in self.tass_directives or 
                  word_upper in self.kickass_directives):
                self.text_widget.tag_add('directive', start_pos, end_pos)
            
            # Memory location check
            elif word.upper() in self.c64_memory:
                self.text_widget.tag_add('memory', start_pos, end_pos)
            
            # Hex number check
            elif self.is_hex_number(word):
                self.text_widget.tag_add('hex', start_pos, end_pos)
            
            # Immediate value check
            elif word.startswith('#'):
                self.text_widget.tag_add('immediate', start_pos, end_pos)
            
            # Register check
            elif word_upper in ['A', 'X', 'Y']:
                self.text_widget.tag_add('register', start_pos, end_pos)
            
            # Decimal number check
            elif self.is_decimal_number(word):
                self.text_widget.tag_add('number', start_pos, end_pos)
    
    def is_hex_number(self, word: str) -> bool:
        """Hex sayı kontrolü"""
        if word.startswith('$'):
            try:
                int(word[1:], 16)
                return True
            except ValueError:
                return False
        elif word.startswith('0x') or word.startswith('0X'):
            try:
                int(word[2:], 16)
                return True
            except ValueError:
                return False
        elif word.startswith('#$'):
            try:
                int(word[2:], 16)
                return True
            except ValueError:
                return False
        return False
    
    def is_decimal_number(self, word: str) -> bool:
        """Decimal sayı kontrolü"""
        try:
            int(word)
            return True
        except ValueError:
            return False

class C64BasicHighlighter(SyntaxHighlighter):
    """C64 BASIC syntax highlighter"""
    
    def __init__(self, text_widget: tk.Text):
        # C64 BASIC keywords
        self.basic_keywords = {
            'PRINT', 'INPUT', 'IF', 'THEN', 'ELSE', 'FOR', 'TO', 'NEXT', 'STEP',
            'GOSUB', 'RETURN', 'GOTO', 'ON', 'RUN', 'LIST', 'NEW', 'LOAD', 'SAVE',
            'GET', 'POKE', 'PEEK', 'SYS', 'LET', 'DIM', 'DATA', 'READ', 'RESTORE',
            'REM', 'STOP', 'END', 'CONT', 'CLR', 'DEF', 'FN', 'AND', 'OR', 'NOT',
            'ABS', 'ATN', 'COS', 'EXP', 'INT', 'LOG', 'RND', 'SGN', 'SIN', 'SQR',
            'TAN', 'ASC', 'CHR$', 'LEFT$', 'LEN', 'MID$', 'RIGHT$', 'STR$', 'VAL'
        }
        
        # C64 BASIC functions
        self.basic_functions = {
            'SIN', 'COS', 'TAN', 'ATN', 'EXP', 'LOG', 'ABS', 'SGN', 'SQR', 'INT',
            'RND', 'ASC', 'LEN', 'VAL', 'POS', 'FRE', 'USR', 'PEEK', 'CHR$',
            'LEFT$', 'RIGHT$', 'MID$', 'STR$', 'TIME$'
        }
        
        super().__init__(text_widget)
    
    def setup_tags(self):
        """C64 BASIC syntax highlighting tag'lerini yapılandır"""
        # BASIC keyword - Mavi, kalın
        self.text_widget.tag_configure('basic_keyword', 
                                     foreground='#0000FF', 
                                     font=('Courier', 10, 'bold'))
        
        # BASIC function - Mor
        self.text_widget.tag_configure('basic_function', 
                                     foreground='#800080')
        
        # Line number - Kırmızı
        self.text_widget.tag_configure('line_number', 
                                     foreground='#CC0000',
                                     font=('Courier', 10, 'bold'))
        
        # String - Yeşil
        self.text_widget.tag_configure('basic_string', 
                                     foreground='#008000')
        
        # Comment (REM) - Gri
        self.text_widget.tag_configure('basic_comment', 
                                     foreground='#808080',
                                     font=('Courier', 10, 'italic'))
        
        # Number - Turuncu
        self.text_widget.tag_configure('basic_number', 
                                     foreground='#FF6600')
    
    def highlight(self, start="1.0", end="end"):
        """C64 BASIC syntax highlighting uygula"""
        # Önce mevcut tag'leri temizle
        self.clear_tags(start, end)
        
        # Text içeriğini al
        content = self.text_widget.get(start, end)
        lines = content.split('\n')
        
        current_line = 1
        for line in lines:
            self.highlight_basic_line(line, current_line)
            current_line += 1
    
    def highlight_basic_line(self, line: str, line_num: int):
        """Tek bir BASIC satırını highlight et"""
        if not line.strip():
            return
        
        # Line number check (başta sayı varsa)
        line_number_match = re.match(r'^\s*(\d+)', line)
        if line_number_match:
            start_pos = f"{line_num}.{line_number_match.start(1)}"
            end_pos = f"{line_num}.{line_number_match.end(1)}"
            self.text_widget.tag_add('line_number', start_pos, end_pos)
        
        # REM comment
        rem_match = re.search(r'\bREM\b.*$', line, re.IGNORECASE)
        if rem_match:
            start_pos = f"{line_num}.{rem_match.start()}"
            end_pos = f"{line_num}.{rem_match.end()}"
            self.text_widget.tag_add('basic_comment', start_pos, end_pos)
            return  # REM sonrası hiçbir şey highlight etme
        
        # String literals
        string_pattern = r'"[^"]*"'
        for match in re.finditer(string_pattern, line):
            start_pos = f"{line_num}.{match.start()}"
            end_pos = f"{line_num}.{match.end()}"
            self.text_widget.tag_add('basic_string', start_pos, end_pos)
        
        # Keywords ve functions
        word_pattern = r'\b[A-Z][A-Z0-9$]*\b'
        for match in re.finditer(word_pattern, line, re.IGNORECASE):
            word = match.group().upper()
            start_pos = f"{line_num}.{match.start()}"
            end_pos = f"{line_num}.{match.end()}"
            
            if word in self.basic_keywords:
                self.text_widget.tag_add('basic_keyword', start_pos, end_pos)
            elif word in self.basic_functions:
                self.text_widget.tag_add('basic_function', start_pos, end_pos)
        
        # Numbers
        number_pattern = r'\b\d+(\.\d+)?\b'
        for match in re.finditer(number_pattern, line):
            start_pos = f"{line_num}.{match.start()}"
            end_pos = f"{line_num}.{match.end()}"
            self.text_widget.tag_add('basic_number', start_pos, end_pos)

class HybridHighlighter(SyntaxHighlighter):
    """Hybrid highlighter - hem Assembly hem BASIC destekler"""
    
    def __init__(self, text_widget: tk.Text):
        self.asm_highlighter = Assembly6502Highlighter(text_widget)
        self.basic_highlighter = C64BasicHighlighter(text_widget)
        super().__init__(text_widget)
    
    def setup_tags(self):
        """Her iki highlighter'ın tag'lerini setup et"""
        self.asm_highlighter.setup_tags()
        self.basic_highlighter.setup_tags()
    
    def highlight(self, start="1.0", end="end"):
        """İçeriğe göre uygun highlighter'ı seç"""
        content = self.text_widget.get(start, end)
        
        # BASIC mi Assembly mi kontrol et
        if self.detect_basic(content):
            self.basic_highlighter.highlight(start, end)
        else:
            self.asm_highlighter.highlight(start, end)
    
    def detect_basic(self, content: str) -> bool:
        """İçeriğin BASIC mi Assembly mi olduğunu tespit et"""
        lines = content.split('\n')
        basic_indicators = 0
        asm_indicators = 0
        
        for line in lines[:10]:  # İlk 10 satırı kontrol et
            line = line.strip().upper()
            
            # BASIC indicators
            if re.match(r'^\d+\s+', line):  # Line number ile başlıyor
                basic_indicators += 2
            if any(keyword in line for keyword in ['PRINT', 'INPUT', 'REM', 'GOTO', 'GOSUB']):
                basic_indicators += 1
            
            # Assembly indicators
            if any(opcode in line for opcode in ['LDA', 'STA', 'JMP', 'JSR', 'RTS']):
                asm_indicators += 1
            if line.endswith(':'):  # Label
                asm_indicators += 1
            if line.startswith('*=') or line.startswith('ORG'):
                asm_indicators += 2
        
        return basic_indicators > asm_indicators

# Test fonksiyonu
def test_syntax_highlighter():
    """Syntax highlighter test"""
    print("🎨 Syntax Highlighter Test")
    
    root = tk.Tk()
    root.title("Syntax Highlighter Test")
    root.geometry("800x600")
    
    # Text widget
    text_widget = tk.Text(root, font=('Courier', 10))
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    # Highlighter
    highlighter = Assembly6502Highlighter(text_widget)
    
    # Test assembly kodu
    test_code = """
ORG $0800
START:
    LDA #$05        ; Load 5 into accumulator
    STA $D020       ; Set border color
    LDX #$00        ; Initialize X register
LOOP:
    INX             ; Increment X
    CPX #$FF        ; Compare with 255
    BNE LOOP        ; Branch if not equal
    RTS             ; Return from subroutine
"""
    
    text_widget.insert('1.0', test_code)
    
    # Highlight
    highlighter.highlight()
    
    # Update fonksiyonu
    def update_highlight(event=None):
        root.after(100, highlighter.highlight)
    
    text_widget.bind('<KeyRelease>', update_highlight)
    
    root.mainloop()

if __name__ == "__main__":
    test_syntax_highlighter()
