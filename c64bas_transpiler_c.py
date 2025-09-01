#!/usr/bin/env python3
"""
C64 BASIC v2 to C Language Transpiler
Enhanced D64 Converter v5.0 Component

This module provides transpilation from Commodore 64 BASIC v2
to C language with GCC compatibility.

Author: Enhanced D64 Converter v5.0
Version: 1.0.0
"""

import re
import sys
import os
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    """Token types for C64 BASIC lexical analysis"""
    LINE_NUMBER = "LINE_NUMBER"
    KEYWORD = "KEYWORD"
    FUNCTION = "FUNCTION"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    COMMENT = "COMMENT"
    EOF = "EOF"

@dataclass
class Token:
    """Represents a token in the C64 BASIC source"""
    type: TokenType
    value: str
    line: int
    column: int

@dataclass
class Variable:
    """Represents a variable in the program"""
    name: str
    var_type: str  # "int", "float", "char*"
    is_array: bool = False
    array_size: int = 0
    first_use_line: int = 0

class C64BasicLexer:
    """Tokenize C64 BASIC v2 source code"""
    
    def __init__(self):
        self.keywords = {
            'PRINT', 'INPUT', 'IF', 'THEN', 'ELSE', 'FOR', 'TO', 'STEP', 'NEXT',
            'GOTO', 'GOSUB', 'RETURN', 'END', 'REM', 'DIM', 'LET', 'DATA', 'READ',
            'AND', 'OR', 'NOT', 'PEEK', 'POKE', 'SYS', 'USR', 'OPEN', 'CLOSE',
            'GET', 'ON', 'STOP', 'CONT', 'RUN', 'LIST', 'NEW', 'CLR', 'CMD',
            'VERIFY', 'SAVE', 'LOAD'
        }
        
        self.functions = {
            'SIN', 'COS', 'TAN', 'ATN', 'EXP', 'LOG', 'ABS', 'SGN', 'SQR',
            'INT', 'RND', 'LEN', 'LEFT$', 'RIGHT$', 'MID$', 'CHR$', 'ASC',
            'STR$', 'VAL', 'FRE', 'POS', 'TAB', 'SPC'
        }
    
    def tokenize(self, source_code: str) -> List[Token]:
        """Convert source code to token stream"""
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
                
            tokens.extend(self._tokenize_line(line, line_num))
        
        tokens.append(Token(TokenType.EOF, "", len(lines), 0))
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """Tokenize a single line"""
        tokens = []
        i = 0
        col = 1
        
        while i < len(line):
            # Skip whitespace
            if line[i].isspace():
                i += 1
                col += 1
                continue
            
            # Line numbers at start of line
            if col == 1 and line[i].isdigit():
                num_match = re.match(r'\d+', line[i:])
                if num_match:
                    tokens.append(Token(TokenType.LINE_NUMBER, num_match.group(), line_num, col))
                    i += len(num_match.group())
                    col += len(num_match.group())
                    continue
            
            # REM comments
            if line[i:i+3].upper() == 'REM':
                comment_text = line[i+3:].strip()
                tokens.append(Token(TokenType.COMMENT, comment_text, line_num, col))
                break
            
            # String literals
            if line[i] == '"':
                string_val, consumed = self._parse_string(line[i:])
                tokens.append(Token(TokenType.STRING, string_val, line_num, col))
                i += consumed
                col += consumed
                continue
            
            # Numbers
            if line[i].isdigit() or line[i] == '.':
                num_match = re.match(r'\d*\.?\d+([eE][+-]?\d+)?', line[i:])
                if num_match:
                    tokens.append(Token(TokenType.NUMBER, num_match.group(), line_num, col))
                    i += len(num_match.group())
                    col += len(num_match.group())
                    continue
            
            # Two-character operators
            if i + 1 < len(line) and line[i:i+2] in ['<=', '>=', '<>']:
                op = line[i:i+2]
                if op == '<>':
                    op = '!='  # Convert to C operator
                tokens.append(Token(TokenType.OPERATOR, op, line_num, col))
                i += 2
                col += 2
                continue
            
            # Single character operators
            if line[i] in '+-*/^=<>':
                op = line[i]
                if op == '^':
                    op = '**'  # Will be handled later as pow()
                tokens.append(Token(TokenType.OPERATOR, op, line_num, col))
                i += 1
                col += 1
                continue
            
            # Delimiters
            if line[i] in '(),;:$%':
                tokens.append(Token(TokenType.DELIMITER, line[i], line_num, col))
                i += 1
                col += 1
                continue
            
            # Identifiers, keywords, and functions
            if line[i].isalpha():
                id_match = re.match(r'[A-Za-z][A-Za-z0-9]*[\$%]?', line[i:])
                if id_match:
                    identifier = id_match.group().upper()
                    
                    if identifier in self.keywords:
                        token_type = TokenType.KEYWORD
                    elif identifier in self.functions:
                        token_type = TokenType.FUNCTION
                    else:
                        token_type = TokenType.IDENTIFIER
                    
                    tokens.append(Token(token_type, identifier, line_num, col))
                    i += len(id_match.group())
                    col += len(id_match.group())
                    continue
            
            # Unknown character - skip it
            i += 1
            col += 1
        
        return tokens
    
    def _parse_string(self, text: str) -> Tuple[str, int]:
        """Parse a string literal"""
        if not text.startswith('"'):
            return "", 0
        
        i = 1
        result = ""
        
        while i < len(text):
            if text[i] == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    result += '"'
                    i += 2
                else:
                    return result, i + 1
            else:
                result += text[i]
                i += 1
        
        return result, i

class CCodeGenerator:
    """Generate C code from C64 BASIC AST"""
    
    def __init__(self):
        self.output_lines = []
        self.indent_level = 0
        self.variables = {}
        self.labels = set()
        self.needs_math = False
        self.needs_string = False
        self.needs_stdio = False
        
    def generate_program(self, tokens: List[Token]) -> str:
        """Generate complete C program"""
        self.output_lines = []
        
        # First pass: analyze tokens to understand program structure
        self._analyze_tokens(tokens)
        
        # Generate includes
        self._generate_includes()
        
        # Generate C64 compatibility functions
        self._generate_c64_functions()
        
        # Generate variable declarations
        self._generate_variable_declarations()
        
        # Generate main function
        self._generate_main_function(tokens)
        
        return '\n'.join(self.output_lines)
    
    def _analyze_tokens(self, tokens: List[Token]):
        """Analyze tokens to determine what we need"""
        for i, token in enumerate(tokens):
            if token.type == TokenType.KEYWORD:
                if token.value in ['PRINT', 'INPUT']:
                    self.needs_stdio = True
                elif token.value == 'POKE':
                    self.needs_stdio = True  # For simulation
            elif token.type == TokenType.FUNCTION:
                if token.value in ['SIN', 'COS', 'TAN', 'LOG', 'EXP', 'SQR']:
                    self.needs_math = True
                elif token.value.endswith('$'):
                    self.needs_string = True
            elif token.type == TokenType.IDENTIFIER:
                self._register_variable(token.value)
            elif token.type == TokenType.LINE_NUMBER:
                self.labels.add(f"label_{token.value}")
    
    def _register_variable(self, name: str):
        """Register a variable with type inference"""
        if name not in self.variables:
            if name.endswith('$'):
                var_type = "char*"
                c_name = name[:-1].lower() + "_str"
            elif name.endswith('%'):
                var_type = "int"
                c_name = name[:-1].lower()
            else:
                var_type = "float"
                c_name = name.lower()
            
            self.variables[name] = Variable(
                name=c_name,
                var_type=var_type,
                first_use_line=0
            )
    
    def _generate_includes(self):
        """Generate necessary #include statements"""
        if self.needs_stdio:
            self._add_line("#include <stdio.h>")
        if self.needs_math:
            self._add_line("#include <math.h>")
        if self.needs_string:
            self._add_line("#include <string.h>")
            self._add_line("#include <stdlib.h>")
        
        self._add_line("")
    
    def _generate_c64_functions(self):
        """Generate C64 compatibility functions"""
        # C64 Memory simulation
        self._add_line("// C64 Memory simulation")
        self._add_line("static unsigned char c64_memory[65536];")
        self._add_line("")
        
        # PEEK function
        self._add_line("int peek(int address) {")
        self.indent_level += 1
        self._add_line("if (address >= 0 && address < 65536) {")
        self.indent_level += 1
        self._add_line("return c64_memory[address];")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("return 0;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # POKE function
        self._add_line("void poke(int address, int value) {")
        self.indent_level += 1
        self._add_line("if (address >= 0 && address < 65536) {")
        self.indent_level += 1
        self._add_line("c64_memory[address] = value & 0xFF;")
        self._add_line("// Simulate hardware effects")
        self._add_line("if (address == 53280) {")
        self.indent_level += 1
        self._add_line('printf("Border color changed to %d\\n", value);')
        self.indent_level -= 1
        self._add_line("} else if (address == 53281) {")
        self.indent_level += 1
        self._add_line('printf("Background color changed to %d\\n", value);')
        self.indent_level -= 1
        self._add_line("}")
        self.indent_level -= 1
        self._add_line("}")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # RND function
        self._add_line("float rnd(void) {")
        self.indent_level += 1
        self._add_line("return (float)rand() / RAND_MAX;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
    
    def _generate_variable_declarations(self):
        """Generate variable declarations"""
        if not self.variables:
            return
            
        self._add_line("// Variable declarations")
        for var_name, var_info in sorted(self.variables.items()):
            if var_info.var_type == "char*":
                self._add_line(f"char {var_info.name}[256] = \"\";")
            else:
                self._add_line(f"{var_info.var_type} {var_info.name} = 0;")
        self._add_line("")
    
    def _generate_main_function(self, tokens: List[Token]):
        """Generate main function"""
        self._add_line("int main(void) {")
        self.indent_level += 1
        
        # Process tokens
        i = 0
        while i < len(tokens):
            if tokens[i].type == TokenType.EOF:
                break
            
            # Generate labels for line numbers
            if tokens[i].type == TokenType.LINE_NUMBER:
                label = f"label_{tokens[i].value}"
                self._add_line(f"{label}:")
                i += 1
                continue
            
            # Process statements
            i = self._process_statement(tokens, i)
        
        self._add_line("return 0;")
        self.indent_level -= 1
        self._add_line("}")
    
    def _process_statement(self, tokens: List[Token], start: int) -> int:
        """Process a single statement and return next position"""
        if start >= len(tokens):
            return start
        
        token = tokens[start]
        
        if token.type == TokenType.KEYWORD:
            if token.value == 'PRINT':
                return self._process_print(tokens, start)
            elif token.value == 'INPUT':
                return self._process_input(tokens, start)
            elif token.value == 'IF':
                return self._process_if(tokens, start)
            elif token.value == 'FOR':
                return self._process_for(tokens, start)
            elif token.value == 'NEXT':
                return self._process_next(tokens, start)
            elif token.value == 'GOTO':
                return self._process_goto(tokens, start)
            elif token.value == 'POKE':
                return self._process_poke(tokens, start)
            elif token.value == 'REM':
                return self._process_rem(tokens, start)
            elif token.value == 'END':
                self._add_line("return 0;")
                return start + 1
        elif token.type == TokenType.COMMENT:
            self._add_line(f"// {token.value}")
            return start + 1
        elif token.type == TokenType.IDENTIFIER:
            # Check if it's an assignment
            if start + 1 < len(tokens) and tokens[start + 1].value == '=':
                return self._process_assignment(tokens, start)
        
        return start + 1
    
    def _process_print(self, tokens: List[Token], start: int) -> int:
        """Process PRINT statement"""
        i = start + 1  # Skip PRINT
        print_parts = []
        
        while i < len(tokens) and not self._is_statement_end(tokens, i):
            if tokens[i].type == TokenType.STRING:
                print_parts.append(f'"{tokens[i].value}"')
            elif tokens[i].type == TokenType.IDENTIFIER:
                var_name = self._get_c_variable_name(tokens[i].value)
                if tokens[i].value.endswith('$'):
                    print_parts.append(f'"%s", {var_name}')
                else:
                    var_type = self.variables.get(tokens[i].value, Variable("", "float")).var_type
                    if var_type == "int":
                        print_parts.append(f'"%d", {var_name}')
                    else:
                        print_parts.append(f'"%g", {var_name}')
            elif tokens[i].type == TokenType.NUMBER:
                print_parts.append(f'"%s"', tokens[i].value)
            elif tokens[i].value == ';':
                # Semicolon suppresses newline
                pass
            elif tokens[i].value == ',':
                # Comma adds tab space
                print_parts.append('"\\t"')
            
            i += 1
        
        if print_parts:
            format_str = " ".join(print_parts)
            # Simplify format string
            if '", "' in format_str:
                format_str = format_str.replace('", "', '')
            self._add_line(f'printf({format_str});')
        else:
            self._add_line('printf("\\n");')
        
        return i
    
    def _process_input(self, tokens: List[Token], start: int) -> int:
        """Process INPUT statement"""
        i = start + 1  # Skip INPUT
        
        # Check for prompt string
        if i < len(tokens) and tokens[i].type == TokenType.STRING:
            self._add_line(f'printf("{tokens[i].value}");')
            i += 1
            if i < len(tokens) and tokens[i].value == ';':
                i += 1
        
        # Get variable to input into
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = self._get_c_variable_name(tokens[i].value)
            if tokens[i].value.endswith('$'):
                self._add_line(f'scanf("%255s", {var_name});')
            else:
                var_type = self.variables.get(tokens[i].value, Variable("", "float")).var_type
                if var_type == "int":
                    self._add_line(f'scanf("%d", &{var_name});')
                else:
                    self._add_line(f'scanf("%f", &{var_name});')
            i += 1
        
        return i
    
    def _process_if(self, tokens: List[Token], start: int) -> int:
        """Process IF statement"""
        i = start + 1  # Skip IF
        condition_parts = []
        
        # Parse condition until THEN
        while i < len(tokens) and tokens[i].value != 'THEN':
            if tokens[i].type == TokenType.IDENTIFIER:
                condition_parts.append(self._get_c_variable_name(tokens[i].value))
            elif tokens[i].type == TokenType.OPERATOR:
                if tokens[i].value == '=':
                    condition_parts.append('==')
                else:
                    condition_parts.append(tokens[i].value)
            else:
                condition_parts.append(tokens[i].value)
            i += 1
        
        if i < len(tokens) and tokens[i].value == 'THEN':
            i += 1  # Skip THEN
            
            condition = ' '.join(condition_parts)
            self._add_line(f'if ({condition}) {{')
            self.indent_level += 1
            
            # Check if THEN is followed by line number (GOTO)
            if i < len(tokens) and tokens[i].type == TokenType.LINE_NUMBER:
                self._add_line(f'goto label_{tokens[i].value};')
                i += 1
            else:
                # Process statements until end of line
                while i < len(tokens) and not self._is_statement_end(tokens, i):
                    i = self._process_statement(tokens, i)
            
            self.indent_level -= 1
            self._add_line('}')
        
        return i
    
    def _process_for(self, tokens: List[Token], start: int) -> int:
        """Process FOR statement"""
        i = start + 1  # Skip FOR
        
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = self._get_c_variable_name(tokens[i].value)
            i += 1
            
            if i < len(tokens) and tokens[i].value == '=':
                i += 1  # Skip =
                
                # Get start value
                start_val = tokens[i].value if i < len(tokens) else "0"
                i += 1
                
                if i < len(tokens) and tokens[i].value == 'TO':
                    i += 1  # Skip TO
                    
                    # Get end value
                    end_val = tokens[i].value if i < len(tokens) else "0"
                    i += 1
                    
                    # Check for STEP
                    step_val = "1"
                    if i < len(tokens) and tokens[i].value == 'STEP':
                        i += 1
                        step_val = tokens[i].value if i < len(tokens) else "1"
                        i += 1
                    
                    self._add_line(f'for ({var_name} = {start_val}; {var_name} <= {end_val}; {var_name} += {step_val}) {{')
                    self.indent_level += 1
        
        return i
    
    def _process_next(self, tokens: List[Token], start: int) -> int:
        """Process NEXT statement"""
        self.indent_level -= 1
        self._add_line('}')
        return start + 1
    
    def _process_goto(self, tokens: List[Token], start: int) -> int:
        """Process GOTO statement"""
        i = start + 1  # Skip GOTO
        
        if i < len(tokens) and tokens[i].type == TokenType.LINE_NUMBER:
            self._add_line(f'goto label_{tokens[i].value};')
            i += 1
        
        return i
    
    def _process_poke(self, tokens: List[Token], start: int) -> int:
        """Process POKE statement"""
        i = start + 1  # Skip POKE
        
        if i < len(tokens):
            address = tokens[i].value
            i += 1
            
            if i < len(tokens) and tokens[i].value == ',':
                i += 1  # Skip comma
                
                if i < len(tokens):
                    value = tokens[i].value
                    self._add_line(f'poke({address}, {value});')
                    i += 1
        
        return i
    
    def _process_rem(self, tokens: List[Token], start: int) -> int:
        """Process REM statement"""
        i = start + 1  # Skip REM
        comment_parts = []
        
        while i < len(tokens) and not self._is_statement_end(tokens, i):
            comment_parts.append(tokens[i].value)
            i += 1
        
        if comment_parts:
            self._add_line(f'// {" ".join(comment_parts)}')
        else:
            self._add_line('//')
        
        return i
    
    def _process_assignment(self, tokens: List[Token], start: int) -> int:
        """Process assignment statement"""
        var_name = self._get_c_variable_name(tokens[start].value)
        i = start + 2  # Skip variable and =
        
        value_parts = []
        while i < len(tokens) and not self._is_statement_end(tokens, i):
            if tokens[i].type == TokenType.IDENTIFIER:
                value_parts.append(self._get_c_variable_name(tokens[i].value))
            elif tokens[i].type == TokenType.FUNCTION:
                if tokens[i].value == 'RND':
                    value_parts.append('rnd()')
                elif tokens[i].value == 'PEEK':
                    # Skip to opening parenthesis and get address
                    i += 1
                    if i < len(tokens) and tokens[i].value == '(':
                        i += 1
                        if i < len(tokens):
                            addr = tokens[i].value
                            value_parts.append(f'peek({addr})')
                            i += 1
                            if i < len(tokens) and tokens[i].value == ')':
                                i += 1
                else:
                    # Handle other math functions
                    func_name = tokens[i].value.lower()
                    if func_name in ['sin', 'cos', 'tan', 'log', 'exp']:
                        value_parts.append(func_name)
                    elif func_name == 'sqr':
                        value_parts.append('sqrt')
                    elif func_name == 'int':
                        value_parts.append('(int)')
                    else:
                        value_parts.append(tokens[i].value)
            else:
                value_parts.append(tokens[i].value)
            i += 1
        
        if value_parts:
            value_expr = ' '.join(value_parts)
            # Handle string assignment
            if tokens[start].value.endswith('$'):
                self._add_line(f'strcpy({var_name}, {value_expr});')
            else:
                self._add_line(f'{var_name} = {value_expr};')
        
        return i
    
    def _get_c_variable_name(self, basic_name: str) -> str:
        """Convert BASIC variable name to C variable name"""
        if basic_name in self.variables:
            return self.variables[basic_name].name
        return basic_name.lower()
    
    def _is_statement_end(self, tokens: List[Token], pos: int) -> bool:
        """Check if we're at the end of a statement"""
        if pos >= len(tokens):
            return True
        
        token = tokens[pos]
        return (token.value == ':' or 
                token.type == TokenType.LINE_NUMBER or 
                token.type == TokenType.EOF)
    
    def _add_line(self, line: str):
        """Add line with proper indentation"""
        indent = "    " * self.indent_level
        self.output_lines.append(indent + line)

class C64BasicToCTranspiler:
    """Main transpiler class"""
    
    def __init__(self):
        self.lexer = C64BasicLexer()
        self.generator = CCodeGenerator()
    
    def transpile_file(self, input_file: str, output_file: str) -> bool:
        """Transpile C64 BASIC file to C"""
        try:
            # Read input file
            with open(input_file, 'r', encoding='utf-8') as f:
                c64_source = f.read()
            
            # Transpile
            c_code = self.transpile_source(c64_source)
            
            # Write output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(c_code)
            
            print(f"Successfully transpiled {input_file} to {output_file}")
            print(f"Compile with: gcc -o program {output_file} -lm")
            return True
            
        except Exception as e:
            print(f"Error transpiling {input_file}: {e}")
            return False
    
    def transpile_source(self, c64_source: str) -> str:
        """Transpile C64 BASIC source code to C"""
        # Tokenize
        tokens = self.lexer.tokenize(c64_source)
        
        # Generate C code
        c_code = self.generator.generate_program(tokens)
        
        return c_code

def main():
    """Main entry point for command-line usage"""
    if len(sys.argv) != 3:
        print("Usage: python c64bas_transpiler_c.py <input_file> <output_file>")
        print("Example: python c64bas_transpiler_c.py program.bas program.c")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    transpiler = C64BasicToCTranspiler()
    success = transpiler.transpile_file(input_file, output_file)
    
    if success:
        print("Transpilation completed successfully!")
        print("Note: Generated C code simulates C64 hardware features.")
    else:
        print("Transpilation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
