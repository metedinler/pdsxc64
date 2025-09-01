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
import sys
import os

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
    var_type: str  # "int", "float", "char*", "array"
    is_array: bool = False
    array_size: int = 0
    array_declaration: str = ""  # For custom array declarations
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
            'STR$', 'VAL', 'FRE', 'POS', 'TAB', 'SPC', 'TI', 'TI$', 'USR', 'PEEK'
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

class ExpressionParser:
    """Parse complex expressions with operator precedence"""
    
    def __init__(self, generator):
        self.generator = generator
        # Operator precedence (higher number = higher precedence)
        self.precedence = {
            'OR': 1,
            'AND': 2,
            '=': 3, '<>': 3, '<': 3, '>': 3, '<=': 3, '>=': 3,
            '+': 4, '-': 4,
            '*': 5, '/': 5, 'MOD': 5,
            '^': 6, '**': 6,  # Exponentiation
            'NOT': 7,  # Unary operators
            'UMINUS': 8  # Unary minus
        }
    
    def parse_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse expression starting from start position"""
        if start >= len(tokens):
            return "0", start
        return self._parse_or_expression(tokens, start, stop_on_assignment)
    
    def _is_statement_end(self, tokens: List[Token], pos: int, stop_on_assignment=False) -> bool:
        """Check if we're at the end of a statement"""
        if pos >= len(tokens):
            return True
        
        token = tokens[pos]
        
        # If in assignment mode, stop on assignment operator (but not for equality comparison)
        # This should only stop if we've already processed the assignment target
        if stop_on_assignment and token.value == '=' and pos > 0:
            # Make sure we're not inside an expression that started with '='
            return False  # Don't stop on '=' in assignment context, let expression parser handle it
            
        return (token.value == ':' or 
                token.type == TokenType.LINE_NUMBER or 
                token.type == TokenType.EOF)
    
    def _parse_or_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse OR expressions (lowest precedence)"""
        left, pos = self._parse_and_expression(tokens, start, stop_on_assignment)
        
        while pos < len(tokens) and not self._is_statement_end(tokens, pos, stop_on_assignment) and tokens[pos].value == 'OR':
            pos += 1  # Skip OR
            right, pos = self._parse_and_expression(tokens, pos, stop_on_assignment)
            left = f'({left} || {right})'
        
        return left, pos
    
    def _parse_and_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse AND expressions"""
        left, pos = self._parse_equality_expression(tokens, start, stop_on_assignment)
        
        while pos < len(tokens) and not self._is_statement_end(tokens, pos, stop_on_assignment) and tokens[pos].value == 'AND':
            pos += 1  # Skip AND
            right, pos = self._parse_equality_expression(tokens, pos, stop_on_assignment)
            left = f'({left} && {right})'
        
        return left, pos
    
    def _parse_equality_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse equality/comparison expressions"""
        left, pos = self._parse_additive_expression(tokens, start, stop_on_assignment)
        
        # Skip assignment operator in assignment mode
        comparison_ops = ['<>', '<', '>', '<=', '>=']
        if not stop_on_assignment:
            comparison_ops.append('=')
        
        while pos < len(tokens) and not self._is_statement_end(tokens, pos, stop_on_assignment) and tokens[pos].value in comparison_ops:
            op = tokens[pos].value
            pos += 1
            right, pos = self._parse_additive_expression(tokens, pos, stop_on_assignment)
            
            # Convert BASIC operators to C
            c_op = {'=': '==', '<>': '!=', '<=': '<=', '>=': '>='}.get(op, op)
            left = f'({left} {c_op} {right})'
        
        return left, pos
    
    def _parse_additive_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse addition/subtraction expressions"""
        left, pos = self._parse_multiplicative_expression(tokens, start, stop_on_assignment)
        
        while pos < len(tokens) and not self._is_statement_end(tokens, pos, stop_on_assignment) and tokens[pos].value in ['+', '-']:
            op = tokens[pos].value
            pos += 1
            right, pos = self._parse_multiplicative_expression(tokens, pos, stop_on_assignment)
            left = f'({left} {op} {right})'
        
        return left, pos
    
    def _parse_multiplicative_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse multiplication/division expressions"""
        left, pos = self._parse_power_expression(tokens, start, stop_on_assignment)
        
        while pos < len(tokens) and not self._is_statement_end(tokens, pos, stop_on_assignment) and tokens[pos].value in ['*', '/', 'MOD']:
            op = tokens[pos].value
            pos += 1
            right, pos = self._parse_power_expression(tokens, pos, stop_on_assignment)
            
            if op == 'MOD':
                left = f'fmod({left}, {right})'
            else:
                left = f'({left} {op} {right})'
        
        return left, pos
    
    def _parse_power_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse power expressions (right associative)"""
        left, pos = self._parse_unary_expression(tokens, start, stop_on_assignment)
        
        if pos < len(tokens) and not self._is_statement_end(tokens, pos, stop_on_assignment) and tokens[pos].value in ['^', '**']:
            pos += 1  # Skip power operator
            right, pos = self._parse_power_expression(tokens, pos, stop_on_assignment)  # Right associative
            left = f'pow({left}, {right})'
            self.generator.needs_math = True
        
        return left, pos
    
    def _parse_unary_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse unary expressions (NOT, -, +)"""
        if start >= len(tokens):
            return "0", start
        
        if tokens[start].value == 'NOT':
            expr, pos = self._parse_unary_expression(tokens, start + 1, stop_on_assignment)
            return f'(!{expr})', pos
        elif tokens[start].value == '-':
            expr, pos = self._parse_unary_expression(tokens, start + 1, stop_on_assignment)
            return f'(-{expr})', pos
        elif tokens[start].value == '+':
            return self._parse_unary_expression(tokens, start + 1, stop_on_assignment)
        
        return self._parse_primary_expression(tokens, start, stop_on_assignment)
    
    def _parse_primary_expression(self, tokens: List[Token], start: int, stop_on_assignment=False) -> Tuple[str, int]:
        """Parse primary expressions (numbers, variables, functions, parentheses)"""
        if start >= len(tokens):
            return "0", start
        
        token = tokens[start]
        
        # Parentheses
        if token.value == '(':
            expr, pos = self._parse_or_expression(tokens, start + 1, stop_on_assignment)
            if pos < len(tokens) and tokens[pos].value == ')':
                pos += 1  # Skip closing parenthesis
            return expr, pos
        
        # Numbers
        elif token.type == TokenType.NUMBER:
            return token.value, start + 1
        
        # Strings
        elif token.type == TokenType.STRING:
            return f'"{token.value}"', start + 1
        
        # Functions
        elif token.type == TokenType.FUNCTION:
            return self.generator._process_math_function(tokens, start) or (token.value, start + 1)
        
        # Variables (including special cases like TI, TI$)
        elif token.type == TokenType.IDENTIFIER:
            if token.value in ['TI', 'TI$']:
                if token.value == 'TI':
                    return 'c64_ti()', start + 1
                else:  # TI$
                    return 'c64_ti_str()', start + 1
            else:
                var_name = self.generator._get_c_variable_name(token.value)
                pos = start + 1
                
                # Check for array indexing
                if pos < len(tokens) and tokens[pos].value == '(':
                    pos += 1  # Skip (
                    indices = []
                    current_index = []
                    paren_count = 1
                    
                    while pos < len(tokens) and paren_count > 0:
                        if tokens[pos].value == '(':
                            paren_count += 1
                            current_index.append(tokens[pos])
                        elif tokens[pos].value == ')':
                            paren_count -= 1
                            if paren_count == 0:
                                if current_index:
                                    idx_expr, _ = self.parse_expression(current_index, 0, stop_on_assignment)
                                    indices.append(idx_expr)
                                break
                            else:
                                current_index.append(tokens[pos])
                        elif tokens[pos].value == ',' and paren_count == 1:
                            if current_index:
                                idx_expr, _ = self.parse_expression(current_index, 0, stop_on_assignment)
                                indices.append(idx_expr)
                                current_index = []
                        else:
                            current_index.append(tokens[pos])
                        pos += 1
                    
                    # Generate array access
                    if indices:
                        array_access = var_name
                        for idx in indices:
                            array_access += f'[{idx}]'
                        return array_access, pos
                
                return var_name, pos
        
        # Default case
        return token.value, start + 1

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
        self.needs_time = False
        self.expression_parser = ExpressionParser(self)
        self.arrays = {}  # Track array dimensions
        self.used_labels = set()  # Track which labels are actually used
        self.all_labels = set()   # Track all labels defined
        self.debug_mode = False
        self.verbose_mode = False
    
    def debug_print(self, message: str):
        """Print debug message if debug mode is enabled"""
        if self.debug_mode:
            print(f"DEBUG: {message}")
            import sys; sys.stdout.flush()
    
    def verbose_print(self, message: str):
        """Print verbose message if verbose mode is enabled"""
        if self.verbose_mode:
            print(f"INFO: {message}")
        
    def generate_program(self, tokens: List[Token]) -> str:
        """Generate complete C program"""
        self.output_lines = []
        self._tokens = tokens  # Store for later use
        
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
        # Set basic requirements - we always need these for our generated functions
        self.needs_stdio = True  # For printf
        self.needs_math = True   # For math functions used in C64 functions
        self.needs_string = True # For string functions
        self.needs_time = True   # For time functions
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == TokenType.KEYWORD:
                if token.value in ['PRINT', 'INPUT']:
                    self.needs_stdio = True
                elif token.value == 'POKE':
                    self.needs_stdio = True  # For simulation
                elif token.value == 'DIM':
                    # Process DIM statement during analysis
                    i = self._process_dim(tokens, i) - 1  # -1 because loop will increment
            elif token.type == TokenType.FUNCTION:
                if token.value in ['SIN', 'COS', 'TAN', 'ATN', 'LOG', 'EXP', 'SQR', 'ABS', 'SGN', 'INT']:
                    self.needs_math = True
                elif token.value in ['LEFT$', 'RIGHT$', 'MID$', 'CHR$', 'STR$', 'ASC', 'VAL', 'LEN']:
                    self.needs_string = True
                elif token.value in ['TI', 'TI$', 'POS', 'USR']:
                    self.needs_time = True  # For TI functions
                elif token.value.endswith('$'):
                    self.needs_string = True
                elif token.value in ['RND', 'FRE']:
                    self.needs_stdio = True  # For random seed initialization
            elif token.type == TokenType.IDENTIFIER:
                self._register_variable(token.value)
            elif token.type == TokenType.LINE_NUMBER:
                self.labels.add(f"label_{token.value}")
            i += 1
    
    def _register_variable(self, name: str, custom_declaration: str = None):
        """Register a variable with type inference or custom declaration"""
        if name not in self.variables:
            if custom_declaration:
                # For arrays with custom declarations
                c_name = self._get_c_variable_name(name)  # Use standard C name conversion
                self.variables[name] = Variable(
                    name=c_name,
                    var_type="array",
                    first_use_line=0,
                    is_array=True,
                    array_declaration=custom_declaration
                )
            else:
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
        # Always include these for our C64 compatibility functions
        self._add_line("#include <stdio.h>")
        self._add_line("#include <math.h>")
        self._add_line("#include <string.h>")
        self._add_line("#include <stdlib.h>")
        self._add_line("#include <time.h>")
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
        
        # C64 Math functions
        self._add_line("// C64 Math functions")
        
        # SGN function (sign)
        self._add_line("float sgn(float x) {")
        self.indent_level += 1
        self._add_line("if (x > 0) return 1.0;")
        self._add_line("if (x < 0) return -1.0;")
        self._add_line("return 0.0;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # ATN function (arctangent)
        self._add_line("float atn(float x) {")
        self.indent_level += 1
        self._add_line("return atan(x);")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # SQR function (square root)
        self._add_line("float sqr(float x) {")
        self.indent_level += 1
        self._add_line("return sqrt(x);")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # INT function (integer part)
        self._add_line("float c64_int(float x) {")
        self.indent_level += 1
        self._add_line("return floor(x);")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # FRE function (free memory simulation)
        self._add_line("float fre(float dummy) {")
        self.indent_level += 1
        self._add_line("// Simulate C64 free memory (38911 bytes max)")
        self._add_line("return 38911.0;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # C64 String functions
        self._add_line("// C64 String functions")
        
        # LEFT$ function
        self._add_line("void c64_left(char* result, const char* str, int length) {")
        self.indent_level += 1
        self._add_line("int len = strlen(str);")
        self._add_line("if (length > len) length = len;")
        self._add_line("if (length < 0) length = 0;")
        self._add_line("strncpy(result, str, length);")
        self._add_line("result[length] = '\\0';")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # RIGHT$ function
        self._add_line("void c64_right(char* result, const char* str, int length) {")
        self.indent_level += 1
        self._add_line("int len = strlen(str);")
        self._add_line("if (length > len) length = len;")
        self._add_line("if (length < 0) length = 0;")
        self._add_line("int start = len - length;")
        self._add_line("strcpy(result, str + start);")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # MID$ function
        self._add_line("void c64_mid(char* result, const char* str, int start, int length) {")
        self.indent_level += 1
        self._add_line("int len = strlen(str);")
        self._add_line("start--; // C64 uses 1-based indexing")
        self._add_line("if (start < 0) start = 0;")
        self._add_line("if (start >= len) {")
        self.indent_level += 1
        self._add_line("result[0] = '\\0';")
        self._add_line("return;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("if (length < 0) length = 0;")
        self._add_line("if (start + length > len) length = len - start;")
        self._add_line("strncpy(result, str + start, length);")
        self._add_line("result[length] = '\\0';")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # CHR$ function
        self._add_line("void c64_chr(char* result, int ascii_code) {")
        self.indent_level += 1
        self._add_line("if (ascii_code >= 0 && ascii_code <= 255) {")
        self.indent_level += 1
        self._add_line("result[0] = (char)ascii_code;")
        self._add_line("result[1] = '\\0';")
        self.indent_level -= 1
        self._add_line("} else {")
        self.indent_level += 1
        self._add_line("result[0] = '\\0';")
        self.indent_level -= 1
        self._add_line("}")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # ASC function
        self._add_line("int c64_asc(const char* str) {")
        self.indent_level += 1
        self._add_line("if (str && str[0] != '\\0') {")
        self.indent_level += 1
        self._add_line("return (unsigned char)str[0];")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("return 0;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # STR$ function
        self._add_line("void c64_str(char* result, float number) {")
        self.indent_level += 1
        self._add_line("if (number == (int)number) {")
        self.indent_level += 1
        self._add_line("sprintf(result, \"%.0f\", number);")
        self.indent_level -= 1
        self._add_line("} else {")
        self.indent_level += 1
        self._add_line("sprintf(result, \"%g\", number);")
        self.indent_level -= 1
        self._add_line("}")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # VAL function
        self._add_line("float c64_val(const char* str) {")
        self.indent_level += 1
        self._add_line("if (!str) return 0.0;")
        self._add_line("// Skip leading whitespace")
        self._add_line("while (*str == ' ') str++;")
        self._add_line("return atof(str);")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # LEN function
        self._add_line("int c64_len(const char* str) {")
        self.indent_level += 1
        self._add_line("return str ? strlen(str) : 0;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # String helper functions that return strings
        self._add_line("// String helper functions")
        
        # Helper for LEFT$ that returns a new string
        self._add_line("char* left_str(const char* str, int length) {")
        self.indent_level += 1
        self._add_line("static char result[256];")
        self._add_line("c64_left(result, str, length);")
        self._add_line("return result;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # Helper for RIGHT$ that returns a new string
        self._add_line("char* right_str(const char* str, int length) {")
        self.indent_level += 1
        self._add_line("static char result[256];")
        self._add_line("c64_right(result, str, length);")
        self._add_line("return result;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # Helper for MID$ that returns a new string
        self._add_line("char* mid_str(const char* str, int start, int length) {")
        self.indent_level += 1
        self._add_line("static char result[256];")
        self._add_line("c64_mid(result, str, start, length);")
        self._add_line("return result;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # Helper for CHR$ that returns a new string
        self._add_line("char* chr_str(int ascii_code) {")
        self.indent_level += 1
        self._add_line("static char result[2];")
        self._add_line("c64_chr(result, ascii_code);")
        self._add_line("return result;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # Helper for STR$ that returns a new string
        self._add_line("char* str_str(float number) {")
        self.indent_level += 1
        self._add_line("static char result[32];")
        self._add_line("c64_str(result, number);")
        self._add_line("return result;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # C64 System and I/O functions
        self._add_line("// C64 System and I/O functions")
        
        # TI (Timer - jiffy clock, 60Hz)
        self._add_line("float c64_ti(void) {")
        self.indent_level += 1
        self._add_line("// Simulate C64 timer (60Hz, since power on)")
        self._add_line("static clock_t start_time = 0;")
        self._add_line("if (start_time == 0) start_time = clock();")
        self._add_line("clock_t current = clock();")
        self._add_line("return (float)((current - start_time) * 60 / CLOCKS_PER_SEC);")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # TI$ (Timer string format HHMMSS)
        self._add_line("char* c64_ti_str(void) {")
        self.indent_level += 1
        self._add_line("static char result[7];")
        self._add_line("float jiffies = c64_ti();")
        self._add_line("int total_seconds = (int)(jiffies / 60);")
        self._add_line("int hours = total_seconds / 3600;")
        self._add_line("int minutes = (total_seconds % 3600) / 60;")
        self._add_line("int seconds = total_seconds % 60;")
        self._add_line("sprintf(result, \"%02d%02d%02d\", hours % 24, minutes, seconds);")
        self._add_line("return result;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # POS(x) - cursor position (simulate)
        self._add_line("int c64_pos(int dummy) {")
        self.indent_level += 1
        self._add_line("// Simulate cursor position (0-39 for C64)")
        self._add_line("static int cursor_pos = 0;")
        self._add_line("return cursor_pos;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
        
        # USR(x) - user defined function (placeholder)
        self._add_line("float c64_usr(float x) {")
        self.indent_level += 1
        self._add_line("// Placeholder for user-defined machine language routine")
        self._add_line("printf(\"USR(%g) called - not implemented\\n\", x);")
        self._add_line("return 0.0;")
        self.indent_level -= 1
        self._add_line("}")
        self._add_line("")
    
    def _generate_variable_declarations(self):
        """Generate variable declarations"""
        if not self.variables:
            return
            
        self._add_line("// Variable declarations")
        for var_name, var_info in sorted(self.variables.items()):
            if var_info.var_type == "array":
                # Use custom array declaration
                self._add_line(f"{var_info.array_declaration};")
            elif var_info.var_type == "char*":
                self._add_line(f"char {var_info.name}[256] = \"\";")
            else:
                self._add_line(f"{var_info.var_type} {var_info.name} = 0;")
        self._add_line("")
    
    def _generate_main_function(self, tokens: List[Token]):
        """Generate main function"""
        self._add_line("int main(void) {")
        self.indent_level += 1
        
        # Initialize random seed if RND is used
        if any(token.type == TokenType.FUNCTION and token.value == 'RND' for token in tokens):
            self._add_line("srand(time(NULL));  // Initialize random seed")
            self._add_line("")
        
        # First pass: collect all labels and track usage
        i = 0
        while i < len(tokens):
            if tokens[i].type == TokenType.EOF:
                break
            
            # Collect all line number labels
            if tokens[i].type == TokenType.LINE_NUMBER:
                label = f"label_{tokens[i].value}"
                self.all_labels.add(label)
                i += 1
                continue
            
            # Track GOTO/GOSUB usage
            if tokens[i].type == TokenType.KEYWORD and tokens[i].value in ['GOTO', 'GOSUB']:
                i += 1
                if i < len(tokens) and tokens[i].type == TokenType.LINE_NUMBER:
                    target_label = f"label_{tokens[i].value}"
                    self.used_labels.add(target_label)
                    i += 1
                continue
                    
            i += 1
        
        # Second pass: generate code
        i = 0
        while i < len(tokens):
            if tokens[i].type == TokenType.EOF:
                break
            
            # Generate labels only if they are used
            if tokens[i].type == TokenType.LINE_NUMBER:
                label = f"label_{tokens[i].value}"
                if label in self.used_labels:
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
            elif token.value == 'GET':
                return self._process_get(tokens, start)
            elif token.value == 'READ':
                return self._process_read(tokens, start)
            elif token.value == 'DATA':
                return self._process_data(tokens, start)
            elif token.value == 'IF':
                return self._process_if(tokens, start)
            elif token.value == 'FOR':
                return self._process_for(tokens, start)
            elif token.value == 'NEXT':
                return self._process_next(tokens, start)
            elif token.value == 'GOTO':
                return self._process_goto(tokens, start)
            elif token.value == 'GOSUB':
                return self._process_gosub(tokens, start)
            elif token.value == 'POKE':
                return self._process_poke(tokens, start)
            elif token.value == 'DIM':
                return self._process_dim(tokens, start)
            elif token.value == 'REM':
                return self._process_rem(tokens, start)
            elif token.value == 'END':
                self._add_line("return 0;")
                return start + 1
        elif token.type == TokenType.COMMENT:
            self._add_line(f"// {token.value}")
            return start + 1
        elif token.type == TokenType.IDENTIFIER:
            # Check if it's an assignment (including array assignments)
            if start + 1 < len(tokens) and tokens[start + 1].value == '=':
                return self._process_assignment(tokens, start)
            elif start + 1 < len(tokens) and tokens[start + 1].value == '(':
                # Could be array assignment like A(I) = 5
                paren_pos = start + 1
                paren_count = 1
                pos = paren_pos + 1
                
                while pos < len(tokens) and paren_count > 0:
                    if tokens[pos].value == '(':
                        paren_count += 1
                    elif tokens[pos].value == ')':
                        paren_count -= 1
                    pos += 1
                
                if pos < len(tokens) and tokens[pos].value == '=':
                    return self._process_array_assignment(tokens, start)
        
        return start + 1
    
    def _process_print(self, tokens: List[Token], start: int) -> int:
        """Process PRINT statement"""
        i = start + 1  # Skip PRINT
        print_items = []
        
        while i < len(tokens) and not self._is_statement_end(tokens, i):
            if tokens[i].type == TokenType.STRING:
                print_items.append(f'printf("{tokens[i].value}");')
            elif tokens[i].type == TokenType.IDENTIFIER:
                # Check for array access A(1) or simple variable
                if i + 1 < len(tokens) and tokens[i + 1].value == '(':
                    # Array access - parse it properly
                    array_name = self._get_c_variable_name(tokens[i].value)
                    i += 2  # Skip identifier and (
                    
                    # Parse array index
                    index_tokens = []
                    paren_count = 1
                    while i < len(tokens) and paren_count > 0:
                        if tokens[i].value == '(':
                            paren_count += 1
                        elif tokens[i].value == ')':
                            paren_count -= 1
                            if paren_count == 0:
                                break
                        else:
                            index_tokens.append(tokens[i])
                        i += 1
                    
                    if index_tokens:
                        index_expr, _ = self.expression_parser.parse_expression(index_tokens, 0)
                        if tokens[i-2].value.endswith('$'):  # Check original variable name
                            print_items.append(f'printf("%s", {array_name}[{index_expr}]);')
                        else:
                            print_items.append(f'printf("%g", {array_name}[{index_expr}]);')
                else:
                    # Simple variable or system variable
                    if tokens[i].value in ['TI', 'TI$']:
                        if tokens[i].value == 'TI':
                            print_items.append('printf("%g", c64_ti());')
                        else:
                            print_items.append('printf("%s", c64_ti_str());')
                    else:
                        var_name = self._get_c_variable_name(tokens[i].value)
                        if tokens[i].value.endswith('$'):
                            print_items.append(f'printf("%s", {var_name});')
                        else:
                            print_items.append(f'printf("%g", {var_name});')
            elif tokens[i].type == TokenType.NUMBER:
                print_items.append(f'printf("%g", {tokens[i].value});')
            elif tokens[i].value == ';':
                # Semicolon continues on same line - no action needed
                pass
            elif tokens[i].value == ',':
                # Comma adds space
                print_items.append('printf(" ");')
            
            i += 1
        
        # Generate print statements
        for print_item in print_items:
            self._add_line(print_item)
        
        # Add newline if not suppressed by semicolon
        if not (i > start + 1 and tokens[i-1].value == ';'):
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
    
    def _process_get(self, tokens: List[Token], start: int) -> int:
        """Process GET statement (single character input)"""
        i = start + 1  # Skip GET
        
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = self._get_c_variable_name(tokens[i].value)
            
            if tokens[i].value.endswith('$'):
                # String variable - get single character
                self._add_line(f"int ch = getchar();")
                self._add_line(f"if (ch != EOF) {{")
                self.indent_level += 1
                self._add_line(f"{var_name}[0] = (char)ch;")
                self._add_line(f"{var_name}[1] = '\\0';")
                self.indent_level -= 1
                self._add_line("} else {")
                self.indent_level += 1
                self._add_line(f"{var_name}[0] = '\\0';")
                self.indent_level -= 1
                self._add_line("}")
            else:
                # Numeric variable - get ASCII value
                self._add_line(f"int ch = getchar();")
                self._add_line(f"{var_name} = (ch != EOF) ? (float)ch : 0.0;")
            
            i += 1
        
        return i
    
    def _process_read(self, tokens: List[Token], start: int) -> int:
        """Process READ statement"""
        i = start + 1  # Skip READ
        
        # For now, simulate READ with predefined values
        while i < len(tokens) and not self._is_statement_end(tokens, i):
            if tokens[i].type == TokenType.IDENTIFIER:
                var_name = self._get_c_variable_name(tokens[i].value)
                
                if tokens[i].value.endswith('$'):
                    self._add_line(f'// READ {var_name} (simulated)')
                    self._add_line(f'strcpy({var_name}, "DATA_VALUE");')
                else:
                    self._add_line(f'// READ {var_name} (simulated)')
                    self._add_line(f'{var_name} = 0.0;  // Would read from DATA')
                
                i += 1
                
                # Skip comma if present
                if i < len(tokens) and tokens[i].value == ',':
                    i += 1
            else:
                i += 1
        
        return i
    
    def _process_data(self, tokens: List[Token], start: int) -> int:
        """Process DATA statement"""
        i = start + 1  # Skip DATA
        
        # For now, just add a comment
        data_items = []
        while i < len(tokens) and not self._is_statement_end(tokens, i):
            if tokens[i].value != ',':
                data_items.append(tokens[i].value)
            i += 1
        
        self._add_line(f'// DATA: {", ".join(data_items)}')
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
        """Process FOR statement with complex expressions"""
        i = start + 1  # Skip FOR
        
        if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
            var_name = self._get_c_variable_name(tokens[i].value)
            i += 1
            
            if i < len(tokens) and tokens[i].value == '=':
                i += 1  # Skip =
                
                # Parse start expression
                start_expr, i = self.expression_parser.parse_expression(tokens, i)
                
                if i < len(tokens) and tokens[i].value == 'TO':
                    i += 1  # Skip TO
                    
                    # Parse end expression
                    end_expr, i = self.expression_parser.parse_expression(tokens, i)
                    
                    # Parse optional STEP
                    step_expr = "1"
                    if i < len(tokens) and tokens[i].value == 'STEP':
                        i += 1  # Skip STEP
                        step_expr, i = self.expression_parser.parse_expression(tokens, i)
                    
                    self._add_line(f'for ({var_name} = {start_expr}; {var_name} <= {end_expr}; {var_name} += {step_expr}) {{')
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
            target_label = f'label_{tokens[i].value}'
            self.used_labels.add(target_label)  # Track label usage
            self._add_line(f'goto {target_label};')
            i += 1
        
        return i
    
    def _process_gosub(self, tokens: List[Token], start: int) -> int:
        """Process GOSUB statement"""
        i = start + 1  # Skip GOSUB
        
        if i < len(tokens) and tokens[i].type == TokenType.LINE_NUMBER:
            target_label = f'label_{tokens[i].value}'
            self.used_labels.add(target_label)  # Track label usage
            self._add_line(f'// GOSUB {tokens[i].value} - TODO: implement subroutine stack')
            self._add_line(f'goto {target_label};')
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
    
    def _process_dim(self, tokens: List[Token], start: int) -> int:
        """Process DIM statement for array declarations"""
        i = start + 1  # Skip DIM
        
        while i < len(tokens) and not self._is_statement_end(tokens, i):
            if tokens[i].type == TokenType.IDENTIFIER:
                array_name = tokens[i].value
                c_name = self._get_c_variable_name(array_name)
                i += 1
                
                if i < len(tokens) and tokens[i].value == '(':
                    i += 1  # Skip (
                    
                    # Parse dimensions
                    dimensions = []
                    current_dim = []
                    paren_count = 1
                    
                    while i < len(tokens) and paren_count > 0:
                        if tokens[i].value == '(':
                            paren_count += 1
                        elif tokens[i].value == ')':
                            paren_count -= 1
                            if paren_count == 0:
                                if current_dim:
                                    dim_expr, _ = self.expression_parser.parse_expression(current_dim, 0)
                                    dimensions.append(dim_expr)
                                break
                        elif tokens[i].value == ',' and paren_count == 1:
                            if current_dim:
                                dim_expr, _ = self.expression_parser.parse_expression(current_dim, 0)
                                dimensions.append(dim_expr)
                                current_dim = []
                        else:
                            current_dim.append(tokens[i])
                        i += 1
                    
                    # Register array and generate declaration
                    self.arrays[array_name] = dimensions
                    
                    # Generate C array declaration properly
                    if array_name.endswith('$'):
                        # String array
                        if len(dimensions) == 1:
                            decl = f'char {c_name}[{dimensions[0]}+1][256] = {{}}'
                            self._register_variable(array_name, decl)
                        else:
                            # Multi-dimensional string arrays not fully supported yet
                            decl = f'char {c_name}[{dimensions[0]}+1][256] = {{}}'
                            self._register_variable(array_name, decl)
                    else:
                        # Numeric array
                        if len(dimensions) == 1:
                            decl = f'float {c_name}[{dimensions[0]}+1] = {{}}'
                            self._register_variable(array_name, decl)
                        elif len(dimensions) == 2:
                            decl = f'float {c_name}[{dimensions[0]}+1][{dimensions[1]}+1] = {{}}'
                            self._register_variable(array_name, decl)
                        else:
                            # Higher dimensions - flatten to 1D for simplicity
                            total_size = '+1)*('.join(dimensions) + '+1)'
                            decl = f'float {c_name}[({total_size})] = {{}}'
                            self._register_variable(array_name, decl)
                
                # Skip comma if present
                if i < len(tokens) and tokens[i].value == ',':
                    i += 1
            else:
                i += 1
        
        return i
    
    def _process_assignment(self, tokens: List[Token], start: int) -> int:
        """Process assignment statement with complex expressions"""
        var_name = self._get_c_variable_name(tokens[start].value)
        i = start + 2  # Skip variable and =
        
        # Use expression parser to handle complex expressions - Don't use stop_on_assignment since we're already past the assignment operator
        expr, next_pos = self.expression_parser.parse_expression(tokens, i)
        
        # Handle string assignment
        if tokens[start].value.endswith('$'):
            self._add_line(f'strcpy({var_name}, {expr});')
        else:
            self._add_line(f'{var_name} = {expr};')
        
        return next_pos
    
    def _process_array_assignment(self, tokens: List[Token], start: int) -> int:
        """Process array assignment like A(I) = 5"""
        var_name = self._get_c_variable_name(tokens[start].value)
        i = start + 1  # Skip to (
        
        self.debug_print(f"Processing array assignment for {tokens[start].value}")
        self.debug_print(f"Tokens from position {i}: {[t.value for t in tokens[i:i+10]]}")
        
        # Parse array indices
        indices = []
        current_index = []
        paren_count = 1
        i += 1  # Skip opening (
        
        while i < len(tokens) and paren_count > 0:
            self.debug_print(f"Processing token at {i}: '{tokens[i].value}', paren_count={paren_count}")
            if tokens[i].value == '(':
                paren_count += 1
                current_index.append(tokens[i])
            elif tokens[i].value == ')':
                paren_count -= 1
                if paren_count == 0:
                    if current_index:
                        self.debug_print(f"Parsing index tokens: {[t.value for t in current_index]}")
                        idx_expr, _ = self.expression_parser.parse_expression(current_index, 0)
                        self.debug_print(f"Parsed index expression: {idx_expr}")
                        indices.append(idx_expr)
                    self.debug_print(f"End of array indices, position after ): {i+1}")
                    i += 1  # Move past the closing )
                    break
                else:
                    current_index.append(tokens[i])
            elif tokens[i].value == ',' and paren_count == 1:
                if current_index:
                    idx_expr, _ = self.expression_parser.parse_expression(current_index, 0)
                    indices.append(idx_expr)
                    current_index = []
            else:
                current_index.append(tokens[i])
            i += 1
        
        # Skip = sign
        if i < len(tokens) and tokens[i].value == '=':
            self.debug_print(f"Found = at position {i}")
            i += 1
            self.debug_print(f"After =, position i={i}, token={tokens[i].value if i < len(tokens) else 'EOF'}")
            self.debug_print(f"After =, tokens from position {i}: {[t.value for t in tokens[i:i+5]]}")
        else:
            self.debug_print(f"No = found at position {i}, token={tokens[i].value if i < len(tokens) else 'EOF'}")
        
        # Parse value expression - Don't use stop_on_assignment since we're already past the assignment operator
        self.debug_print(f"About to parse expression starting at position {i}")
        expr, next_pos = self.expression_parser.parse_expression(tokens, i)
        self.debug_print(f"Parsed value expression: {expr}")
        self.debug_print(f"Next position: {next_pos}")
        
        # Generate array assignment
        array_ref = var_name
        for idx in indices:
            array_ref += f'[{idx}]'
        
        if tokens[start].value.endswith('$'):
            self._add_line(f'strcpy({array_ref}, {expr});')
        else:
            self._add_line(f'{array_ref} = {expr};')
        
        return next_pos
        
        # Generate array assignment
        array_ref = var_name
        for idx in indices:
            array_ref += f'[{idx}]'
        
        if tokens[start].value.endswith('$'):
            self._add_line(f'strcpy({array_ref}, {expr});')
        else:
            self._add_line(f'{array_ref} = {expr};')
        
        return next_pos
    
    def _process_math_function(self, tokens: List[Token], start: int) -> Optional[Tuple[str, int]]:
        """Process C64 math function and return (C_code, next_position)"""
        func_name = tokens[start].value
        i = start + 1
        
        # Skip to opening parenthesis
        if i < len(tokens) and tokens[i].value == '(':
            i += 1  # Skip '('
            
            # Get argument(s)
            args = []
            arg_parts = []
            paren_count = 1
            
            while i < len(tokens) and paren_count > 0:
                if tokens[i].value == '(':
                    paren_count += 1
                    arg_parts.append(tokens[i].value)
                elif tokens[i].value == ')':
                    paren_count -= 1
                    if paren_count > 0:
                        arg_parts.append(tokens[i].value)
                elif tokens[i].value == ',' and paren_count == 1:
                    # New argument
                    if arg_parts:
                        args.append(' '.join(arg_parts))
                        arg_parts = []
                else:
                    if tokens[i].type == TokenType.IDENTIFIER:
                        arg_parts.append(self._get_c_variable_name(tokens[i].value))
                    else:
                        arg_parts.append(tokens[i].value)
                i += 1
            
            # Add last argument
            if arg_parts:
                args.append(' '.join(arg_parts))
            
            # Convert C64 function to C equivalent
            if func_name == 'SIN':
                return f'sin({args[0] if args else "0"})', i
            elif func_name == 'COS':
                return f'cos({args[0] if args else "0"})', i
            elif func_name == 'TAN':
                return f'tan({args[0] if args else "0"})', i
            elif func_name == 'ATN':
                return f'atn({args[0] if args else "0"})', i
            elif func_name == 'EXP':
                return f'exp({args[0] if args else "0"})', i
            elif func_name == 'LOG':
                return f'log({args[0] if args else "1"})', i
            elif func_name == 'SQR':
                return f'sqr({args[0] if args else "0"})', i
            elif func_name == 'ABS':
                return f'fabs({args[0] if args else "0"})', i
            elif func_name == 'SGN':
                return f'sgn({args[0] if args else "0"})', i
            elif func_name == 'INT':
                return f'c64_int({args[0] if args else "0"})', i
            elif func_name == 'RND':
                return 'rnd()', i
            elif func_name == 'FRE':
                return f'fre({args[0] if args else "0"})', i
            elif func_name == 'PEEK':
                return f'peek({args[0] if args else "0"})', i
            
            # String functions
            elif func_name == 'LEFT$':
                if len(args) >= 2:
                    return f'left_str({args[0]}, {args[1]})', i
                return 'left_str("", 0)', i
            elif func_name == 'RIGHT$':
                if len(args) >= 2:
                    return f'right_str({args[0]}, {args[1]})', i
                return 'right_str("", 0)', i
            elif func_name == 'MID$':
                if len(args) >= 3:
                    return f'mid_str({args[0]}, {args[1]}, {args[2]})', i
                elif len(args) >= 2:
                    return f'mid_str({args[0]}, {args[1]}, strlen({args[0]}))', i
                return 'mid_str("", 0, 0)', i
            elif func_name == 'CHR$':
                return f'chr_str({args[0] if args else "0"})', i
            elif func_name == 'STR$':
                return f'str_str({args[0] if args else "0"})', i
            elif func_name == 'ASC':
                return f'c64_asc({args[0] if args else "\"\""})', i
            elif func_name == 'VAL':
                return f'c64_val({args[0] if args else "\"\""})', i
            elif func_name == 'LEN':
                return f'c64_len({args[0] if args else "\"\""})', i
            
            # System and I/O functions
            elif func_name == 'TI':
                return 'c64_ti()', i
            elif func_name == 'TI$':
                return 'c64_ti_str()', i
            elif func_name == 'POS':
                return f'c64_pos({args[0] if args else "0"})', i
            elif func_name == 'USR':
                return f'c64_usr({args[0] if args else "0"})', i
        
        return None
    
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
        self.debug_mode = False
        self.verbose_mode = False
    
    def set_debug_mode(self, debug: bool = False, verbose: bool = False):
        """Set debug and verbose modes"""
        self.debug_mode = debug
        self.verbose_mode = verbose
        self.generator.debug_mode = debug
        self.generator.verbose_mode = verbose
    
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
        
        # Debug: print all tokens if debug mode is enabled
        if self.debug_mode:
            print("DEBUG: All tokens:")
            for i, token in enumerate(tokens):
                print(f"  {i}: {token.type.name} = '{token.value}'")
            print()
        
        # Generate C code
        c_code = self.generator.generate_program(tokens)
        
        return c_code

def main():
    """Main entry point for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='C64 BASIC to C Transpiler')
    parser.add_argument('input_file', help='Input C64 BASIC file (.bas)')
    parser.add_argument('output_file', help='Output C file (.c)')
    parser.add_argument('--debug', '-d', action='store_true', 
                       help='Enable debug output for parsing and code generation')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    input_file = args.input_file
    output_file = args.output_file
    debug_mode = args.debug
    verbose_mode = args.verbose
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    transpiler = C64BasicToCTranspiler()
    transpiler.set_debug_mode(debug_mode, verbose_mode)
    success = transpiler.transpile_file(input_file, output_file)
    
    if success:
        print("Transpilation completed successfully!")
        print("Note: Generated C code simulates C64 hardware features.")
    else:
        print("Transpilation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
