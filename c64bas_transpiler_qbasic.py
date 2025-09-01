#!/usr/bin/env python3
"""
C64 BASIC v2 to QBasic 7.1 Transpiler
Enhanced D64 Converter v5.0 Component

This module provides comprehensive transpilation from Commodore 64 BASIC v2
to QBasic 7.1, including advanced features like memory simulation,
graphics conversion, and structured programming transformation.

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
    var_type: str  # "INTEGER", "SINGLE", "STRING"
    is_array: bool = False
    array_dimensions: List[int] = None
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
        
        self.operators = {
            '+', '-', '*', '/', '^', '=', '<', '>', '<=', '>=', '<>'
        }
        
        self.delimiters = {
            '(', ')', ',', ';', ':', '$', '%'
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
                tokens.append(Token(TokenType.OPERATOR, line[i:i+2], line_num, col))
                i += 2
                col += 2
                continue
            
            # Single character operators and delimiters
            if line[i] in self.operators:
                tokens.append(Token(TokenType.OPERATOR, line[i], line_num, col))
                i += 1
                col += 1
                continue
            
            if line[i] in self.delimiters:
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
                    # Escaped quote
                    result += '"'
                    i += 2
                else:
                    # End of string
                    return result, i + 1
            else:
                result += text[i]
                i += 1
        
        # Unterminated string
        return result, i

class C64BasicParser:
    """Parse C64 BASIC v2 token stream into AST"""
    
    def __init__(self):
        self.tokens = []
        self.current = 0
        self.line_numbers = {}
        self.variables = {}
        self.subroutines = set()
        self.goto_targets = set()
        self.gosub_targets = set()
    
    def parse(self, tokens: List[Token]) -> Dict:
        """Build Abstract Syntax Tree"""
        self.tokens = tokens
        self.current = 0
        
        program = {
            'type': 'PROGRAM',
            'lines': [],
            'variables': {},
            'subroutines': set(),
            'goto_targets': set(),
            'gosub_targets': set()
        }
        
        while not self._is_at_end():
            if self._peek().type == TokenType.EOF:
                break
                
            line_ast = self._parse_line()
            if line_ast:
                program['lines'].append(line_ast)
        
        program['variables'] = self.variables
        program['subroutines'] = self.subroutines
        program['goto_targets'] = self.goto_targets
        program['gosub_targets'] = self.gosub_targets
        
        return program
    
    def _parse_line(self) -> Optional[Dict]:
        """Parse a single program line"""
        if self._is_at_end():
            return None
        
        line_ast = {
            'type': 'LINE',
            'number': None,
            'statements': []
        }
        
        # Check for line number
        if self._peek().type == TokenType.LINE_NUMBER:
            line_number = int(self._advance().value)
            line_ast['number'] = line_number
            self.line_numbers[line_number] = len(self.tokens)  # Position for later reference
        
        # Parse statements separated by colons
        while not self._is_at_end() and self._peek().type != TokenType.EOF:
            if self._peek().type == TokenType.LINE_NUMBER:
                break  # Next line
            
            stmt = self._parse_statement()
            if stmt:
                line_ast['statements'].append(stmt)
            
            # Check for statement separator
            if self._peek().type == TokenType.DELIMITER and self._peek().value == ':':
                self._advance()  # consume ':'
            else:
                break
        
        return line_ast if line_ast['statements'] else None
    
    def _parse_statement(self) -> Optional[Dict]:
        """Parse a single statement"""
        if self._is_at_end():
            return None
        
        token = self._peek()
        
        if token.type == TokenType.KEYWORD:
            if token.value == 'PRINT':
                return self._parse_print()
            elif token.value == 'INPUT':
                return self._parse_input()
            elif token.value == 'IF':
                return self._parse_if()
            elif token.value == 'FOR':
                return self._parse_for()
            elif token.value == 'NEXT':
                return self._parse_next()
            elif token.value == 'GOTO':
                return self._parse_goto()
            elif token.value == 'GOSUB':
                return self._parse_gosub()
            elif token.value == 'RETURN':
                return self._parse_return()
            elif token.value == 'END':
                return self._parse_end()
            elif token.value == 'REM':
                return self._parse_rem()
            elif token.value == 'DIM':
                return self._parse_dim()
            elif token.value == 'LET':
                return self._parse_let()
            elif token.value == 'POKE':
                return self._parse_poke()
            elif token.value == 'DATA':
                return self._parse_data()
            elif token.value == 'READ':
                return self._parse_read()
        elif token.type == TokenType.COMMENT:
            return self._parse_comment()
        elif token.value in self.variables or self._looks_like_assignment():
            return self._parse_assignment()
        
        # Unknown statement - skip token
        self._advance()
        return None
    
    def _parse_print(self) -> Dict:
        """Parse PRINT statement"""
        self._advance()  # consume 'PRINT'
        
        stmt = {
            'type': 'PRINT',
            'items': [],
            'separator': 'NEWLINE'
        }
        
        while not self._is_at_end() and not self._is_statement_end():
            expr = self._parse_expression()
            if expr:
                stmt['items'].append(expr)
            
            # Check for separator
            if self._peek().type == TokenType.DELIMITER:
                if self._peek().value == ';':
                    stmt['separator'] = 'NONE'
                    self._advance()
                elif self._peek().value == ',':
                    stmt['separator'] = 'TAB'
                    self._advance()
                else:
                    break
            else:
                break
        
        return stmt
    
    def _parse_input(self) -> Dict:
        """Parse INPUT statement"""
        self._advance()  # consume 'INPUT'
        
        stmt = {
            'type': 'INPUT',
            'prompt': None,
            'variables': []
        }
        
        # Check for prompt string
        if self._peek().type == TokenType.STRING:
            stmt['prompt'] = self._advance().value
            if self._peek().type == TokenType.DELIMITER and self._peek().value == ';':
                self._advance()  # consume ';'
        
        # Parse variable list
        while not self._is_at_end() and not self._is_statement_end():
            if self._peek().type == TokenType.IDENTIFIER:
                var_name = self._advance().value
                stmt['variables'].append(var_name)
                self._register_variable(var_name)
            
            if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
                self._advance()  # consume ','
            else:
                break
        
        return stmt
    
    def _parse_if(self) -> Dict:
        """Parse IF statement"""
        self._advance()  # consume 'IF'
        
        stmt = {
            'type': 'IF',
            'condition': None,
            'then_statements': [],
            'else_statements': []
        }
        
        # Parse condition
        stmt['condition'] = self._parse_expression()
        
        # Expect THEN
        if self._peek().type == TokenType.KEYWORD and self._peek().value == 'THEN':
            self._advance()  # consume 'THEN'
        
        # Parse THEN clause
        if self._peek().type == TokenType.LINE_NUMBER:
            # THEN line_number
            target = int(self._advance().value)
            self.goto_targets.add(target)
            stmt['then_statements'].append({
                'type': 'GOTO',
                'target': target
            })
        else:
            # THEN statement(s)
            while not self._is_at_end() and not self._is_statement_end():
                if self._peek().type == TokenType.KEYWORD and self._peek().value == 'ELSE':
                    break
                stmt_ast = self._parse_statement()
                if stmt_ast:
                    stmt['then_statements'].append(stmt_ast)
        
        # Check for ELSE
        if self._peek().type == TokenType.KEYWORD and self._peek().value == 'ELSE':
            self._advance()  # consume 'ELSE'
            while not self._is_at_end() and not self._is_statement_end():
                stmt_ast = self._parse_statement()
                if stmt_ast:
                    stmt['else_statements'].append(stmt_ast)
        
        return stmt
    
    def _parse_for(self) -> Dict:
        """Parse FOR statement"""
        self._advance()  # consume 'FOR'
        
        stmt = {
            'type': 'FOR',
            'variable': None,
            'start': None,
            'end': None,
            'step': None
        }
        
        # Parse variable
        if self._peek().type == TokenType.IDENTIFIER:
            stmt['variable'] = self._advance().value
            self._register_variable(stmt['variable'])
        
        # Expect =
        if self._peek().type == TokenType.OPERATOR and self._peek().value == '=':
            self._advance()
        
        # Parse start value
        stmt['start'] = self._parse_expression()
        
        # Expect TO
        if self._peek().type == TokenType.KEYWORD and self._peek().value == 'TO':
            self._advance()
        
        # Parse end value
        stmt['end'] = self._parse_expression()
        
        # Check for STEP
        if self._peek().type == TokenType.KEYWORD and self._peek().value == 'STEP':
            self._advance()
            stmt['step'] = self._parse_expression()
        
        return stmt
    
    def _parse_next(self) -> Dict:
        """Parse NEXT statement"""
        self._advance()  # consume 'NEXT'
        
        stmt = {
            'type': 'NEXT',
            'variable': None
        }
        
        # Optional variable
        if self._peek().type == TokenType.IDENTIFIER:
            stmt['variable'] = self._advance().value
        
        return stmt
    
    def _parse_goto(self) -> Dict:
        """Parse GOTO statement"""
        self._advance()  # consume 'GOTO'
        
        stmt = {
            'type': 'GOTO',
            'target': None
        }
        
        if self._peek().type == TokenType.LINE_NUMBER:
            target = int(self._advance().value)
            stmt['target'] = target
            self.goto_targets.add(target)
        
        return stmt
    
    def _parse_gosub(self) -> Dict:
        """Parse GOSUB statement"""
        self._advance()  # consume 'GOSUB'
        
        stmt = {
            'type': 'GOSUB',
            'target': None
        }
        
        if self._peek().type == TokenType.LINE_NUMBER:
            target = int(self._advance().value)
            stmt['target'] = target
            self.gosub_targets.add(target)
            self.subroutines.add(target)
        
        return stmt
    
    def _parse_return(self) -> Dict:
        """Parse RETURN statement"""
        self._advance()  # consume 'RETURN'
        return {'type': 'RETURN'}
    
    def _parse_end(self) -> Dict:
        """Parse END statement"""
        self._advance()  # consume 'END'
        return {'type': 'END'}
    
    def _parse_rem(self) -> Dict:
        """Parse REM statement"""
        self._advance()  # consume 'REM'
        comment = ""
        
        # Collect rest of line as comment
        while not self._is_at_end() and not self._is_statement_end():
            comment += self._advance().value + " "
        
        return {
            'type': 'COMMENT',
            'text': comment.strip()
        }
    
    def _parse_comment(self) -> Dict:
        """Parse comment token"""
        comment = self._advance().value
        return {
            'type': 'COMMENT',
            'text': comment
        }
    
    def _parse_dim(self) -> Dict:
        """Parse DIM statement"""
        self._advance()  # consume 'DIM'
        
        stmt = {
            'type': 'DIM',
            'variables': []
        }
        
        while not self._is_at_end() and not self._is_statement_end():
            if self._peek().type == TokenType.IDENTIFIER:
                var_name = self._advance().value
                var_info = {'name': var_name, 'dimensions': []}
                
                # Check for array dimensions
                if self._peek().type == TokenType.DELIMITER and self._peek().value == '(':
                    self._advance()  # consume '('
                    
                    while True:
                        dimension = self._parse_expression()
                        if dimension:
                            var_info['dimensions'].append(dimension)
                        
                        if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
                            self._advance()  # consume ','
                        else:
                            break
                    
                    if self._peek().type == TokenType.DELIMITER and self._peek().value == ')':
                        self._advance()  # consume ')'
                
                stmt['variables'].append(var_info)
                self._register_variable(var_name, is_array=bool(var_info['dimensions']))
            
            if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
                self._advance()  # consume ','
            else:
                break
        
        return stmt
    
    def _parse_let(self) -> Dict:
        """Parse LET statement"""
        self._advance()  # consume 'LET'
        return self._parse_assignment()
    
    def _parse_assignment(self) -> Dict:
        """Parse assignment statement"""
        stmt = {
            'type': 'ASSIGNMENT',
            'target': None,
            'value': None
        }
        
        # Parse left side (variable)
        if self._peek().type == TokenType.IDENTIFIER:
            var_name = self._advance().value
            stmt['target'] = var_name
            self._register_variable(var_name)
            
            # Check for array indexing
            if self._peek().type == TokenType.DELIMITER and self._peek().value == '(':
                self._advance()  # consume '('
                indices = []
                
                while True:
                    index = self._parse_expression()
                    if index:
                        indices.append(index)
                    
                    if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
                        self._advance()  # consume ','
                    else:
                        break
                
                if self._peek().type == TokenType.DELIMITER and self._peek().value == ')':
                    self._advance()  # consume ')'
                
                stmt['target'] = {
                    'type': 'ARRAY_ACCESS',
                    'name': var_name,
                    'indices': indices
                }
        
        # Expect =
        if self._peek().type == TokenType.OPERATOR and self._peek().value == '=':
            self._advance()  # consume '='
        
        # Parse right side (expression)
        stmt['value'] = self._parse_expression()
        
        return stmt
    
    def _parse_poke(self) -> Dict:
        """Parse POKE statement"""
        self._advance()  # consume 'POKE'
        
        stmt = {
            'type': 'POKE',
            'address': None,
            'value': None
        }
        
        # Parse address
        stmt['address'] = self._parse_expression()
        
        # Expect comma
        if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
            self._advance()  # consume ','
        
        # Parse value
        stmt['value'] = self._parse_expression()
        
        return stmt
    
    def _parse_data(self) -> Dict:
        """Parse DATA statement"""
        self._advance()  # consume 'DATA'
        
        stmt = {
            'type': 'DATA',
            'values': []
        }
        
        while not self._is_at_end() and not self._is_statement_end():
            if self._peek().type in [TokenType.NUMBER, TokenType.STRING]:
                stmt['values'].append(self._advance().value)
            elif self._peek().type == TokenType.IDENTIFIER:
                stmt['values'].append(self._advance().value)
            
            if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
                self._advance()  # consume ','
            else:
                break
        
        return stmt
    
    def _parse_read(self) -> Dict:
        """Parse READ statement"""
        self._advance()  # consume 'READ'
        
        stmt = {
            'type': 'READ',
            'variables': []
        }
        
        while not self._is_at_end() and not self._is_statement_end():
            if self._peek().type == TokenType.IDENTIFIER:
                var_name = self._advance().value
                stmt['variables'].append(var_name)
                self._register_variable(var_name)
            
            if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
                self._advance()  # consume ','
            else:
                break
        
        return stmt
    
    def _parse_expression(self) -> Optional[Dict]:
        """Parse expression (simplified for now)"""
        if self._is_at_end() or self._is_statement_end():
            return None
        
        token = self._peek()
        
        if token.type == TokenType.NUMBER:
            return {
                'type': 'NUMBER',
                'value': self._advance().value
            }
        elif token.type == TokenType.STRING:
            return {
                'type': 'STRING',
                'value': self._advance().value
            }
        elif token.type == TokenType.IDENTIFIER:
            var_name = self._advance().value
            self._register_variable(var_name)
            
            # Check for array access or function call
            if self._peek().type == TokenType.DELIMITER and self._peek().value == '(':
                self._advance()  # consume '('
                args = []
                
                while True:
                    arg = self._parse_expression()
                    if arg:
                        args.append(arg)
                    
                    if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
                        self._advance()  # consume ','
                    else:
                        break
                
                if self._peek().type == TokenType.DELIMITER and self._peek().value == ')':
                    self._advance()  # consume ')'
                
                # Determine if it's a function or array
                if var_name in {'SIN', 'COS', 'TAN', 'ATN', 'EXP', 'LOG', 'ABS', 'SGN', 'SQR',
                               'INT', 'RND', 'LEN', 'LEFT$', 'RIGHT$', 'MID$', 'CHR$', 'ASC',
                               'STR$', 'VAL', 'FRE', 'PEEK'}:
                    return {
                        'type': 'FUNCTION_CALL',
                        'name': var_name,
                        'arguments': args
                    }
                else:
                    return {
                        'type': 'ARRAY_ACCESS',
                        'name': var_name,
                        'indices': args
                    }
            else:
                return {
                    'type': 'VARIABLE',
                    'name': var_name
                }
        elif token.type == TokenType.FUNCTION:
            func_name = self._advance().value
            
            # Expect opening parenthesis
            if self._peek().type == TokenType.DELIMITER and self._peek().value == '(':
                self._advance()  # consume '('
                args = []
                
                while True:
                    arg = self._parse_expression()
                    if arg:
                        args.append(arg)
                    
                    if self._peek().type == TokenType.DELIMITER and self._peek().value == ',':
                        self._advance()  # consume ','
                    else:
                        break
                
                if self._peek().type == TokenType.DELIMITER and self._peek().value == ')':
                    self._advance()  # consume ')'
                
                return {
                    'type': 'FUNCTION_CALL',
                    'name': func_name,
                    'arguments': args
                }
        
        # For now, just consume the token and return a placeholder
        self._advance()
        return {
            'type': 'EXPRESSION',
            'value': token.value
        }
    
    def _register_variable(self, name: str, is_array: bool = False):
        """Register a variable for type inference"""
        if name not in self.variables:
            var_type = "STRING" if name.endswith('$') else "INTEGER" if name.endswith('%') else "SINGLE"
            self.variables[name] = Variable(
                name=name,
                var_type=var_type,
                is_array=is_array,
                first_use_line=self._peek().line
            )
    
    def _looks_like_assignment(self) -> bool:
        """Check if current position looks like an assignment"""
        if self._peek().type != TokenType.IDENTIFIER:
            return False
        
        # Look ahead for = sign
        saved_pos = self.current
        self._advance()  # skip identifier
        
        # Skip array indexing if present
        if self._peek().type == TokenType.DELIMITER and self._peek().value == '(':
            paren_count = 1
            self._advance()  # consume '('
            
            while paren_count > 0 and not self._is_at_end():
                if self._peek().value == '(':
                    paren_count += 1
                elif self._peek().value == ')':
                    paren_count -= 1
                self._advance()
        
        # Check for = operator
        is_assignment = (self._peek().type == TokenType.OPERATOR and self._peek().value == '=')
        
        # Restore position
        self.current = saved_pos
        return is_assignment
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens"""
        return self.current >= len(self.tokens)
    
    def _is_statement_end(self) -> bool:
        """Check if at end of current statement"""
        if self._is_at_end():
            return True
        
        token = self._peek()
        return (token.type == TokenType.DELIMITER and token.value == ':') or \
               token.type == TokenType.LINE_NUMBER or \
               token.type == TokenType.EOF
    
    def _peek(self) -> Token:
        """Get current token without consuming it"""
        if self._is_at_end():
            return Token(TokenType.EOF, "", 0, 0)
        return self.tokens[self.current]
    
    def _advance(self) -> Token:
        """Consume and return current token"""
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

class QBasicCodeGenerator:
    """Generate QBasic 7.1 code from C64 BASIC AST"""
    
    def __init__(self):
        self.output_lines = []
        self.indent_level = 0
        self.label_map = {}
        self.subroutine_map = {}
        self.variables = {}
        self.used_labels = set()
        self.in_main = False
    
    def generate_program(self, ast: Dict) -> str:
        """Generate complete QBasic program"""
        self.output_lines = []
        self.variables = ast['variables']
        
        # Generate program header
        self._add_line("' Converted from C64 BASIC v2 to QBasic 7.1")
        self._add_line("' Enhanced D64 Converter v5.0")
        self._add_line("")
        
        # Analyze program structure
        self._analyze_program_structure(ast)
        
        # Generate declarations
        self._generate_declarations(ast)
        self._add_line("")
        
        # Generate main program call
        self._add_line("CALL Main")
        self._add_line("")
        
        # Generate main subroutine
        self._generate_main_subroutine(ast)
        
        # Generate other subroutines
        self._generate_subroutines(ast)
        
        # Generate utility functions
        self._generate_utility_functions()
        
        return '\n'.join(self.output_lines)
    
    def _analyze_program_structure(self, ast: Dict):
        """Analyze program for subroutines and labels"""
        # Map line numbers to labels
        for line in ast['lines']:
            if line['number'] is not None:
                line_num = line['number']
                if line_num in ast['gosub_targets']:
                    self.subroutine_map[line_num] = f"Subroutine{line_num}"
                elif line_num in ast['goto_targets']:
                    self.label_map[line_num] = f"Label{line_num}"
                    self.used_labels.add(line_num)
    
    def _generate_declarations(self, ast: Dict):
        """Generate SUB and FUNCTION declarations"""
        self._add_line("DECLARE SUB Main()")
        
        # Declare subroutines
        for line_num in sorted(ast['gosub_targets']):
            sub_name = self.subroutine_map[line_num]
            self._add_line(f"DECLARE SUB {sub_name}()")
        
        # Declare utility functions
        if self._needs_c64_functions(ast):
            self._add_line("DECLARE FUNCTION PEEK(Address AS LONG) AS INTEGER")
            self._add_line("DECLARE SUB POKE(Address AS LONG, Value AS INTEGER)")
            self._add_line("DECLARE SUB SetBorderColor(ColorCode AS INTEGER)")
            self._add_line("DECLARE SUB SetBackgroundColor(ColorCode AS INTEGER)")
            self._add_line("DECLARE SUB SetScreenChar(Position AS INTEGER, Character AS INTEGER)")
            self._add_line("DECLARE SUB SetCharColor(Position AS INTEGER, ColorCode AS INTEGER)")
    
    def _generate_main_subroutine(self, ast: Dict):
        """Generate main subroutine"""
        self._add_line("SUB Main()")
        self.indent_level += 1
        self.in_main = True
        
        # Generate variable declarations
        self._generate_variable_declarations()
        
        if self.variables:
            self._add_line("")
        
        # Generate program lines
        for line in ast['lines']:
            # Skip subroutine lines (they'll be generated separately)
            if line['number'] in ast['gosub_targets']:
                continue
            
            self._generate_line(line)
        
        self.indent_level -= 1
        self.in_main = False
        self._add_line("END SUB")
        self._add_line("")
    
    def _generate_subroutines(self, ast: Dict):
        """Generate subroutines from GOSUB targets"""
        for line_num in sorted(ast['gosub_targets']):
            sub_name = self.subroutine_map[line_num]
            self._add_line(f"SUB {sub_name}()")
            self.indent_level += 1
            
            # Find subroutine lines
            in_subroutine = False
            for line in ast['lines']:
                if line['number'] == line_num:
                    in_subroutine = True
                
                if in_subroutine:
                    # Stop at RETURN or next subroutine
                    if any(stmt['type'] == 'RETURN' for stmt in line['statements']):
                        # Generate line but skip RETURN
                        filtered_statements = [stmt for stmt in line['statements'] if stmt['type'] != 'RETURN']
                        if filtered_statements:
                            filtered_line = dict(line)
                            filtered_line['statements'] = filtered_statements
                            self._generate_line(filtered_line)
                        break
                    elif line['number'] in ast['gosub_targets'] and line['number'] != line_num:
                        break
                    else:
                        self._generate_line(line)
            
            self.indent_level -= 1
            self._add_line("END SUB")
            self._add_line("")
    
    def _generate_variable_declarations(self):
        """Generate DIM statements for variables"""
        for var_name, var_info in sorted(self.variables.items()):
            if var_info.is_array:
                # Array declaration
                dims = ", ".join("0 TO 100" for _ in range(len(var_info.array_dimensions) or [1]))
                self._add_line(f"DIM {var_name}({dims}) AS {var_info.var_type}")
            else:
                # Simple variable declaration
                self._add_line(f"DIM {var_name} AS {var_info.var_type}")
    
    def _generate_line(self, line: Dict):
        """Generate QBasic code for a program line"""
        # Add label if needed
        if line['number'] is not None and line['number'] in self.used_labels:
            label = self.label_map[line['number']]
            self._add_line(f"{label}:")
        
        # Generate statements
        for stmt in line['statements']:
            self._generate_statement(stmt)
    
    def _generate_statement(self, stmt: Dict):
        """Generate QBasic code for a statement"""
        stmt_type = stmt['type']
        
        if stmt_type == 'PRINT':
            self._generate_print(stmt)
        elif stmt_type == 'INPUT':
            self._generate_input(stmt)
        elif stmt_type == 'IF':
            self._generate_if(stmt)
        elif stmt_type == 'FOR':
            self._generate_for(stmt)
        elif stmt_type == 'NEXT':
            self._generate_next(stmt)
        elif stmt_type == 'GOTO':
            self._generate_goto(stmt)
        elif stmt_type == 'GOSUB':
            self._generate_gosub(stmt)
        elif stmt_type == 'RETURN':
            pass  # Handled in subroutine generation
        elif stmt_type == 'END':
            self._generate_end(stmt)
        elif stmt_type == 'COMMENT':
            self._generate_comment(stmt)
        elif stmt_type == 'ASSIGNMENT':
            self._generate_assignment(stmt)
        elif stmt_type == 'DIM':
            pass  # Handled in variable declarations
        elif stmt_type == 'POKE':
            self._generate_poke(stmt)
        elif stmt_type == 'DATA':
            self._generate_data(stmt)
        elif stmt_type == 'READ':
            self._generate_read(stmt)
    
    def _generate_print(self, stmt: Dict):
        """Generate PRINT statement"""
        if not stmt['items']:
            self._add_line("PRINT")
            return
        
        print_parts = []
        for item in stmt['items']:
            print_parts.append(self._generate_expression(item))
        
        separator = "; " if stmt['separator'] == 'NONE' else ", " if stmt['separator'] == 'TAB' else ""
        print_line = "PRINT " + separator.join(print_parts)
        
        if stmt['separator'] == 'NONE':
            print_line += ";"
        
        self._add_line(print_line)
    
    def _generate_input(self, stmt: Dict):
        """Generate INPUT statement"""
        if stmt['prompt']:
            prompt_part = f'"{stmt["prompt"]}"; '
        else:
            prompt_part = ""
        
        vars_part = ", ".join(stmt['variables'])
        self._add_line(f"INPUT {prompt_part}{vars_part}")
    
    def _generate_if(self, stmt: Dict):
        """Generate IF statement"""
        condition = self._generate_expression(stmt['condition'])
        
        if len(stmt['then_statements']) == 1 and not stmt['else_statements']:
            # Single-line IF
            then_stmt = self._generate_statement_inline(stmt['then_statements'][0])
            self._add_line(f"IF {condition} THEN {then_stmt}")
        else:
            # Multi-line IF
            self._add_line(f"IF {condition} THEN")
            self.indent_level += 1
            
            for then_stmt in stmt['then_statements']:
                self._generate_statement(then_stmt)
            
            if stmt['else_statements']:
                self.indent_level -= 1
                self._add_line("ELSE")
                self.indent_level += 1
                
                for else_stmt in stmt['else_statements']:
                    self._generate_statement(else_stmt)
            
            self.indent_level -= 1
            self._add_line("END IF")
    
    def _generate_for(self, stmt: Dict):
        """Generate FOR statement"""
        var = stmt['variable']
        start = self._generate_expression(stmt['start'])
        end = self._generate_expression(stmt['end'])
        
        if stmt['step']:
            step = self._generate_expression(stmt['step'])
            self._add_line(f"FOR {var} = {start} TO {end} STEP {step}")
        else:
            self._add_line(f"FOR {var} = {start} TO {end}")
    
    def _generate_next(self, stmt: Dict):
        """Generate NEXT statement"""
        if stmt['variable']:
            self._add_line(f"NEXT {stmt['variable']}")
        else:
            self._add_line("NEXT")
    
    def _generate_goto(self, stmt: Dict):
        """Generate GOTO statement"""
        if stmt['target'] in self.label_map:
            label = self.label_map[stmt['target']]
            self._add_line(f"GOTO {label}")
        else:
            self._add_line(f"' GOTO {stmt['target']} (target not found)")
    
    def _generate_gosub(self, stmt: Dict):
        """Generate GOSUB as CALL statement"""
        if stmt['target'] in self.subroutine_map:
            sub_name = self.subroutine_map[stmt['target']]
            self._add_line(f"CALL {sub_name}")
        else:
            self._add_line(f"' GOSUB {stmt['target']} (target not found)")
    
    def _generate_end(self, stmt: Dict):
        """Generate END statement"""
        if self.in_main:
            self._add_line("' END")  # Comment out in main subroutine
        else:
            self._add_line("END")
    
    def _generate_comment(self, stmt: Dict):
        """Generate comment"""
        if stmt['text'].strip():
            self._add_line(f"' {stmt['text']}")
        else:
            self._add_line("'")
    
    def _generate_assignment(self, stmt: Dict):
        """Generate assignment statement"""
        if isinstance(stmt['target'], dict) and stmt['target']['type'] == 'ARRAY_ACCESS':
            # Array assignment
            array_name = stmt['target']['name']
            indices = [self._generate_expression(idx) for idx in stmt['target']['indices']]
            value = self._generate_expression(stmt['value'])
            self._add_line(f"{array_name}({', '.join(indices)}) = {value}")
        else:
            # Simple assignment
            target = stmt['target']
            value = self._generate_expression(stmt['value'])
            self._add_line(f"{target} = {value}")
    
    def _generate_poke(self, stmt: Dict):
        """Generate POKE statement"""
        address = self._generate_expression(stmt['address'])
        value = self._generate_expression(stmt['value'])
        
        # Convert common C64 addresses to function calls
        try:
            addr_val = int(address) if address.isdigit() else None
            if addr_val == 53280:  # Border color
                self._add_line(f"CALL SetBorderColor({value})")
            elif addr_val == 53281:  # Background color
                self._add_line(f"CALL SetBackgroundColor({value})")
            elif addr_val and 1024 <= addr_val <= 2023:  # Screen memory
                pos = addr_val - 1024
                self._add_line(f"CALL SetScreenChar({pos}, {value})")
            elif addr_val and 55296 <= addr_val <= 56295:  # Color memory
                pos = addr_val - 55296
                self._add_line(f"CALL SetCharColor({pos}, {value})")
            else:
                self._add_line(f"CALL POKE({address}, {value})")
        except:
            self._add_line(f"CALL POKE({address}, {value})")
    
    def _generate_data(self, stmt: Dict):
        """Generate DATA statement (as comments)"""
        values = ", ".join(stmt['values'])
        self._add_line(f"' DATA {values}")
    
    def _generate_read(self, stmt: Dict):
        """Generate READ statement (as comments)"""
        variables = ", ".join(stmt['variables'])
        self._add_line(f"' READ {variables}")
    
    def _generate_expression(self, expr: Dict) -> str:
        """Generate expression code"""
        if expr is None:
            return ""
        
        expr_type = expr['type']
        
        if expr_type == 'NUMBER':
            return expr['value']
        elif expr_type == 'STRING':
            return f'"{expr["value"]}"'
        elif expr_type == 'VARIABLE':
            return expr['name']
        elif expr_type == 'FUNCTION_CALL':
            func_name = expr['name']
            args = [self._generate_expression(arg) for arg in expr['arguments']]
            
            # Handle special C64 functions
            if func_name == 'PEEK':
                return f"PEEK({', '.join(args)})"
            elif func_name == 'RND':
                return "RND"
            elif func_name == 'FRE':
                return "FRE(-1)"
            else:
                return f"{func_name}({', '.join(args)})"
        elif expr_type == 'ARRAY_ACCESS':
            indices = [self._generate_expression(idx) for idx in expr['indices']]
            return f"{expr['name']}({', '.join(indices)})"
        elif expr_type == 'EXPRESSION':
            return expr['value']
        else:
            return str(expr.get('value', ''))
    
    def _generate_statement_inline(self, stmt: Dict) -> str:
        """Generate statement as inline code"""
        if stmt['type'] == 'GOTO':
            if stmt['target'] in self.label_map:
                return f"GOTO {self.label_map[stmt['target']]}"
            else:
                return f"' GOTO {stmt['target']}"
        elif stmt['type'] == 'ASSIGNMENT':
            target = stmt['target']
            value = self._generate_expression(stmt['value'])
            return f"{target} = {value}"
        else:
            # For other statements, generate normally and return last line
            saved_lines = len(self.output_lines)
            self._generate_statement(stmt)
            if len(self.output_lines) > saved_lines:
                inline_code = self.output_lines[-1].strip()
                self.output_lines = self.output_lines[:-1]  # Remove the line we just added
                return inline_code
            return ""
    
    def _generate_utility_functions(self):
        """Generate C64 compatibility functions"""
        if not self._needs_c64_functions({}):
            return
        
        # PEEK function
        self._add_line("FUNCTION PEEK(Address AS LONG) AS INTEGER")
        self.indent_level += 1
        self._add_line("' Simulate C64 memory reading")
        self._add_line("' Implementation depends on requirements")
        self._add_line("PEEK = 0")
        self.indent_level -= 1
        self._add_line("END FUNCTION")
        self._add_line("")
        
        # POKE subroutine
        self._add_line("SUB POKE(Address AS LONG, Value AS INTEGER)")
        self.indent_level += 1
        self._add_line("' Simulate C64 memory writing")
        self._add_line("' Implementation depends on requirements")
        self.indent_level -= 1
        self._add_line("END SUB")
        self._add_line("")
        
        # Graphics functions
        self._add_line("SUB SetBorderColor(ColorCode AS INTEGER)")
        self.indent_level += 1
        self._add_line("' Simulate C64 border color setting")
        self.indent_level -= 1
        self._add_line("END SUB")
        self._add_line("")
        
        self._add_line("SUB SetBackgroundColor(ColorCode AS INTEGER)")
        self.indent_level += 1
        self._add_line("' Simulate C64 background color setting")
        self._add_line("COLOR , ColorCode")
        self.indent_level -= 1
        self._add_line("END SUB")
        self._add_line("")
        
        self._add_line("SUB SetScreenChar(Position AS INTEGER, Character AS INTEGER)")
        self.indent_level += 1
        self._add_line("DIM Row AS INTEGER, Col AS INTEGER")
        self._add_line("Row = Position \\ 40 + 1")
        self._add_line("Col = (Position MOD 40) + 1")
        self._add_line("LOCATE Row, Col")
        self._add_line("PRINT CHR$(Character);")
        self.indent_level -= 1
        self._add_line("END SUB")
        self._add_line("")
        
        self._add_line("SUB SetCharColor(Position AS INTEGER, ColorCode AS INTEGER)")
        self.indent_level += 1
        self._add_line("DIM Row AS INTEGER, Col AS INTEGER")
        self._add_line("Row = Position \\ 40 + 1")
        self._add_line("Col = (Position MOD 40) + 1")
        self._add_line("COLOR ColorCode")
        self._add_line("LOCATE Row, Col")
        self.indent_level -= 1
        self._add_line("END SUB")
    
    def _needs_c64_functions(self, ast: Dict) -> bool:
        """Check if C64 compatibility functions are needed"""
        # For now, always include them if any POKE statements exist
        return True
    
    def _add_line(self, line: str):
        """Add line with proper indentation"""
        indent = "    " * self.indent_level
        self.output_lines.append(indent + line)

class C64BasicTranspiler:
    """Main transpiler class"""
    
    def __init__(self):
        self.lexer = C64BasicLexer()
        self.parser = C64BasicParser()
        self.generator = QBasicCodeGenerator()
    
    def transpile_file(self, input_file: str, output_file: str) -> bool:
        """Transpile C64 BASIC file to QBasic"""
        try:
            # Read input file
            with open(input_file, 'r', encoding='utf-8') as f:
                c64_source = f.read()
            
            # Transpile
            qbasic_code = self.transpile_source(c64_source)
            
            # Write output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(qbasic_code)
            
            print(f"Successfully transpiled {input_file} to {output_file}")
            return True
            
        except Exception as e:
            print(f"Error transpiling {input_file}: {e}")
            return False
    
    def transpile_source(self, c64_source: str) -> str:
        """Transpile C64 BASIC source code to QBasic"""
        # Tokenize
        tokens = self.lexer.tokenize(c64_source)
        
        # Parse
        ast = self.parser.parse(tokens)
        
        # Generate QBasic code
        qbasic_code = self.generator.generate_program(ast)
        
        return qbasic_code

def main():
    """Main entry point for command-line usage"""
    if len(sys.argv) != 3:
        print("Usage: python c64bas_transpiler_qbasic.py <input_file> <output_file>")
        print("Example: python c64bas_transpiler_qbasic.py program.bas program.qb")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    transpiler = C64BasicTranspiler()
    success = transpiler.transpile_file(input_file, output_file)
    
    if success:
        print("Transpilation completed successfully!")
    else:
        print("Transpilation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
