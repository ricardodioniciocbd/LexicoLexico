"""
Compilador Interactivo para Subconjunto de Python
Incluye: Análisis Léxico, Sintáctico, Semántico, Generación de Código Intermedio, 
Optimización y Generación de Código Máquina
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Any, Dict


# ============= ANÁLISIS LÉXICO =============

class TokenType(Enum):
    """Tipos de tokens para subconjunto de Python"""
    # Palabras clave
    DEF = auto()
    RETURN = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RANGE = auto()
    PRINT = auto()
    LEN = auto()
    APPEND = auto()
    INT = auto()
    FLOAT = auto()
    STR = auto()
    
    # Literales
    NUMBER = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()
    NONE = auto()
    
    # Identificadores
    IDENTIFIER = auto()
    
    # Operadores
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    NOT = auto()  # Operador not para negación booleana
    
    # Comparación
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    
    # Asignación
    ASSIGN = auto()
    
    # Delimitadores
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()      # {
    RBRACE = auto()      # }
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    
    # Funciones built-in
    INPUT = auto()
    OPEN = auto()
    READ = auto()
    WRITE = auto()
    CLOSE = auto()
    REMOVE = auto()  # Método remove para listas
    BREAK = auto()   # Palabra clave break
    
    # Especiales
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()


@dataclass
class Token:
    """Representa un token con su tipo, valor y posición"""
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value}, {self.line}:{self.column})"


KEYWORDS = {
    'def': TokenType.DEF,
    'return': TokenType.RETURN,
    'if': TokenType.IF,
    'elif': TokenType.ELIF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'range': TokenType.RANGE,
    'print': TokenType.PRINT,
    'len': TokenType.LEN,
    # 'append': TokenType.APPEND,  # No debe ser palabra reservada, es un método
    'input': TokenType.INPUT,
    'open': TokenType.OPEN,
    'read': TokenType.READ,
    'write': TokenType.WRITE,
    'close': TokenType.CLOSE,
    'True': TokenType.TRUE,
    'False': TokenType.FALSE,
    'None': TokenType.NONE,
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'str': TokenType.STR,
    'not': TokenType.NOT,
    'break': TokenType.BREAK,  # Agregar también break para bucles
}


class LexerError(Exception):
    """Error en el análisis léxico"""
    pass


class Lexer:
    """Analizador Léxico para Python"""
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.indent_stack = [0]
    
    def error(self, message):
        raise LexerError(f"Error Léxico en línea {self.line}, columna {self.column}: {message}")
    
    def peek(self, offset=0):
        pos = self.position + offset
        return self.source[pos] if pos < len(self.source) else None
    
    def advance(self):
        if self.position < len(self.source):
            char = self.source[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        while self.peek() in ' \t':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '#':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_number(self):
        start_line, start_column = self.line, self.column
        num_str = ''
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.advance()
        try:
            value = float(num_str) if '.' in num_str else int(num_str)
            return Token(TokenType.NUMBER, value, start_line, start_column)
        except:
            self.error(f"Número inválido: {num_str}")
    
    def read_string(self):
        start_line, start_column = self.line, self.column
        quote = self.advance()
        string_value = ''
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                string_value += escape_map.get(next_char, next_char)
            else:
                string_value += self.advance()
        if self.peek() != quote:
            self.error("String sin cerrar")
        self.advance()
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def read_identifier(self):
        start_line, start_column = self.line, self.column
        identifier = ''
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            identifier += self.advance()
        token_type = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        return Token(token_type, identifier, start_line, start_column)
    
    def handle_indentation(self, indent_level):
        tokens = []
        current = self.indent_stack[-1]
        if indent_level > current:
            self.indent_stack.append(indent_level)
            tokens.append(Token(TokenType.INDENT, indent_level, self.line, 1))
        elif indent_level < current:
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, indent_level, self.line, 1))
            if not self.indent_stack or self.indent_stack[-1] != indent_level:
                self.error("Indentación inconsistente")
        return tokens
    
    def tokenize(self):
        self.tokens = []
        at_line_start = True
        
        while self.position < len(self.source):
            if at_line_start:
                indent_level = 0
                while self.peek() in ' \t':
                    indent_level += 4 if self.peek() == '\t' else 1
                    self.advance()
                
                if self.peek() in '\n#':
                    if self.peek() == '\n':
                        self.advance()
                    else:
                        self.skip_comment()
                    continue
                
                self.tokens.extend(self.handle_indentation(indent_level))
                at_line_start = False
            
            self.skip_whitespace()
            if not self.peek():
                break
            
            char = self.peek()
            start_line, start_column = self.line, self.column
            
            if char == '#':
                self.skip_comment()
            elif char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', start_line, start_column))
                at_line_start = True
            elif char.isdigit():
                self.tokens.append(self.read_number())
            elif char in '"\'':
                self.tokens.append(self.read_string())
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            elif char == '*' and self.peek(1) == '*':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.POWER, '**', start_line, start_column))
            elif char == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '==', start_line, start_column))
            elif char == '!' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', start_line, start_column))
            elif char == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_column))
            elif char == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_column))
            elif char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_column))
            elif char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_column))
            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_column))
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_column))
            elif char == '%':
                self.advance()
                self.tokens.append(Token(TokenType.MODULO, '%', start_line, start_column))
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_column))
            elif char == '<':
                self.advance()
                self.tokens.append(Token(TokenType.LESS, '<', start_line, start_column))
            elif char == '>':
                self.advance()
                self.tokens.append(Token(TokenType.GREATER, '>', start_line, start_column))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_column))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_column))
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_column))
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_column))
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_column))
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_column))
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_column))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_column))
            elif char == '.':
                self.advance()
                self.tokens.append(Token(TokenType.DOT, '.', start_line, start_column))
            else:
                self.error(f"Carácter inesperado: '{char}'")
        
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, 0, self.line, self.column))
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens


# ============= NODOS AST =============

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class AssignmentNode(ASTNode):
    def __init__(self, identifier, expression, line=0):
        self.identifier = identifier
        self.expression = expression
        self.line = line

class PrintNode(ASTNode):
    def __init__(self, expressions, line=0):
        self.expressions = expressions  # Lista de expresiones para imprimir
        self.line = line

class IfNode(ASTNode):
    def __init__(self, condition, then_block, elif_parts=None, else_block=None, line=0):
        self.condition = condition
        self.then_block = then_block
        self.elif_parts = elif_parts or []
        self.else_block = else_block
        self.line = line

class WhileNode(ASTNode):
    def __init__(self, condition, block, line=0):
        self.condition = condition
        self.block = block
        self.line = line

class ForNode(ASTNode):
    def __init__(self, identifier, iterable, block, line=0):
        self.identifier = identifier
        self.iterable = iterable
        self.block = block
        self.line = line

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right, line=0):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line

class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand, line=0):
        self.operator = operator
        self.operand = operand
        self.line = line

class NumberNode(ASTNode):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line

class StringNode(ASTNode):
    def __init__(self, value, line=0):
        self.value = value
        self.line = line

class IdentifierNode(ASTNode):
    def __init__(self, name, line=0):
        self.name = name
        self.line = line

class ListNode(ASTNode):
    def __init__(self, elements, line=0):
        self.elements = elements
        self.line = line

class IndexNode(ASTNode):
    def __init__(self, list_expr, index_expr, line=0):
        self.list_expr = list_expr
        self.index_expr = index_expr
        self.line = line

class CallNode(ASTNode):
    def __init__(self, function, args, line=0):
        self.function = function
        self.args = args
        self.line = line

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class FunctionNode(ASTNode):
    def __init__(self, name, parameters, body, line=0):
        self.name = name
        self.parameters = parameters  # Lista de nombres de parámetros
        self.body = body  # BlockNode
        self.line = line

class ReturnNode(ASTNode):
    def __init__(self, expression, line=0):
        self.expression = expression  # Puede ser None para return sin valor
        self.line = line

class DictNode(ASTNode):
    def __init__(self, items, line=0):
        self.items = items  # Lista de tuplas (clave, valor)
        self.line = line

class InputNode(ASTNode):
    def __init__(self, prompt=None, line=0):
        self.prompt = prompt  # Expresión opcional para el prompt
        self.line = line


# ============= ANÁLISIS SINTÁCTICO =============

class ParserError(Exception):
    """Error en el análisis sintáctico"""
    pass


class Parser:
    """Analizador Sintáctico"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self, message):
        if self.current_token:
            raise ParserError(f"Error Sintáctico en línea {self.current_token.line}: {message}")
        raise ParserError(f"Error Sintáctico: {message}")
    
    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        return self.current_token
    
    def expect(self, token_type):
        if self.current_token.type != token_type:
            self.error(f"Se esperaba {token_type.name}, se encontró {self.current_token.type.name}")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self):
        return self.parse_program()
    
    def parse_program(self):
        statements = []
        self.skip_newlines()
        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        return ProgramNode(statements)
    
    def parse_statement(self):
        self.skip_newlines()
        token_type = self.current_token.type
        
        if token_type == TokenType.DEF:
            return self.parse_function()
        elif token_type == TokenType.RETURN:
            return self.parse_return()
        elif token_type == TokenType.IDENTIFIER:
            next_token = self.tokens[self.position + 1] if self.position + 1 < len(self.tokens) else None
            if next_token and next_token.type == TokenType.ASSIGN:
                return self.parse_assignment()
            elif next_token and next_token.type == TokenType.LBRACKET:
                return self.parse_list_assignment()
            else:
                expr = self.parse_expression()
                self.skip_newlines()
                return expr
        elif token_type == TokenType.PRINT:
            return self.parse_print()
        elif token_type == TokenType.IF:
            return self.parse_if()
        elif token_type == TokenType.WHILE:
            return self.parse_while()
        elif token_type == TokenType.FOR:
            return self.parse_for()
        elif token_type == TokenType.BREAK:
            # break statement - simplemente avanzar el token
            self.advance()
            self.skip_newlines()
            return None  # break no necesita nodo AST especial por ahora
        else:
            self.error(f"Token inesperado: {self.current_token}")
    
    def parse_assignment(self):
        line = self.current_token.line
        identifier = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        expression = self.parse_expression()
        return AssignmentNode(identifier, expression, line)
    
    def parse_list_assignment(self):
        line = self.current_token.line
        identifier = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LBRACKET)
        index_expr = self.parse_expression()
        self.expect(TokenType.RBRACKET)
        self.expect(TokenType.ASSIGN)
        value_expr = self.parse_expression()
        return AssignmentNode(f"{identifier}[INDEX]", value_expr, line)
    
    def parse_print(self):
        """Parse print statement: print(expr1, expr2, ...)"""
        line = self.current_token.line
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        
        expressions = []
        if self.current_token.type != TokenType.RPAREN:
            expressions.append(self.parse_expression())
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                expressions.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        return PrintNode(expressions, line)
    
    def parse_if(self):
        line = self.current_token.line
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        then_block = self.parse_block()
        
        elif_parts = []
        while self.current_token.type == TokenType.ELIF:
            self.advance()
            elif_condition = self.parse_expression()
            self.expect(TokenType.COLON)
            self.skip_newlines()
            elif_block = self.parse_block()
            elif_parts.append((elif_condition, elif_block))
        
        else_block = None
        if self.current_token.type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.COLON)
            self.skip_newlines()
            else_block = self.parse_block()
        
        return IfNode(condition, then_block, elif_parts, else_block, line)
    
    def parse_while(self):
        line = self.current_token.line
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        block = self.parse_block()
        return WhileNode(condition, block, line)
    
    def parse_for(self):
        line = self.current_token.line
        self.expect(TokenType.FOR)
        identifier = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        block = self.parse_block()
        return ForNode(identifier, iterable, block, line)
    
    def parse_block(self):
        statements = []
        if self.current_token.type != TokenType.INDENT:
            self.error("Se esperaba bloque indentado")
        self.advance()
        self.skip_newlines()
        
        while self.current_token.type not in (TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        if self.current_token.type == TokenType.DEDENT:
            self.advance()
        
        return BlockNode(statements)
    
    def parse_function(self):
        """Parse function definition: def nombre(param1, param2): bloque"""
        line = self.current_token.line
        self.expect(TokenType.DEF)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        
        parameters = []
        if self.current_token.type != TokenType.RPAREN:
            parameters.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                parameters.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.COLON)
        self.skip_newlines()
        body = self.parse_block()
        
        return FunctionNode(name, parameters, body, line)
    
    def parse_return(self):
        """Parse return statement: return expresion"""
        line = self.current_token.line
        self.expect(TokenType.RETURN)
        if self.current_token.type != TokenType.NEWLINE and self.current_token.type != TokenType.DEDENT:
            expression = self.parse_expression()
            return ReturnNode(expression, line)
        return ReturnNode(None, line)
    
    def parse_dict(self):
        """Parse dictionary: {clave1: valor1, clave2: valor2}"""
        line = self.current_token.line
        self.expect(TokenType.LBRACE)
        items = []
        
        if self.current_token.type != TokenType.RBRACE:
            key = self.parse_expression()
            self.expect(TokenType.COLON)
            value = self.parse_expression()
            items.append((key, value))
            
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                key = self.parse_expression()
                self.expect(TokenType.COLON)
                value = self.parse_expression()
                items.append((key, value))
        
        self.expect(TokenType.RBRACE)
        return DictNode(items, line)
    
    def parse_input(self):
        """Parse input() call: input() or input(prompt)"""
        line = self.current_token.line
        self.expect(TokenType.INPUT)
        self.expect(TokenType.LPAREN)
        
        prompt = None
        if self.current_token.type != TokenType.RPAREN:
            prompt = self.parse_expression()
        
        self.expect(TokenType.RPAREN)
        return InputNode(prompt, line)
    
    def parse_expression(self):
        return self.parse_comparison()
    
    def parse_comparison(self):
        left = self.parse_arithmetic()
        comparison_ops = {TokenType.EQUAL, TokenType.NOT_EQUAL, TokenType.LESS, 
                         TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL}
        
        if self.current_token.type in comparison_ops:
            operator = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_arithmetic()
            return BinaryOpNode(left, operator, right, line)
        return left
    
    def parse_arithmetic(self):
        left = self.parse_term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_term()
            left = BinaryOpNode(left, operator, right, line)
        return left
    
    def parse_term(self):
        left = self.parse_factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_factor()
            left = BinaryOpNode(left, operator, right, line)
        return left
    
    def parse_factor(self):
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value, token.line)
        elif token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value, token.line)
        elif token.type == TokenType.TRUE:
            self.advance()
            return NumberNode(1, token.line)  # True = 1
        elif token.type == TokenType.FALSE:
            self.advance()
            return NumberNode(0, token.line)  # False = 0
        elif token.type == TokenType.NONE:
            self.advance()
            return NumberNode(0, token.line)  # None = 0 (para compatibilidad)
        elif token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            if self.current_token.type == TokenType.LPAREN:
                # Llamada a función
                self.advance()
                args = []
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current_token.type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                return CallNode(name, args, token.line)
            elif self.current_token.type == TokenType.LBRACKET:
                self.advance()
                index_expr = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                return IndexNode(IdentifierNode(name, token.line), index_expr, token.line)
            elif self.current_token.type == TokenType.DOT:
                self.advance()
                method = self.expect(TokenType.IDENTIFIER).value
                self.expect(TokenType.LPAREN)
                args = []
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.current_token.type == TokenType.COMMA:
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                return CallNode(f"{name}.{method}", args, token.line)
            return IdentifierNode(name, token.line)
        elif token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            if self.current_token.type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                while self.current_token.type == TokenType.COMMA:
                    self.advance()
                    elements.append(self.parse_expression())
            self.expect(TokenType.RBRACKET)
            return ListNode(elements, token.line)
        elif token.type == TokenType.LBRACE:
            return self.parse_dict()
        elif token.type == TokenType.INPUT:
            return self.parse_input()
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        elif token.type in (TokenType.RANGE, TokenType.LEN, TokenType.INT):
            func_name = token.value
            self.advance()
            self.expect(TokenType.LPAREN)
            args = []
            if self.current_token.type != TokenType.RPAREN:
                args.append(self.parse_expression())
                while self.current_token.type == TokenType.COMMA:
                    self.advance()
                    args.append(self.parse_expression())
            self.expect(TokenType.RPAREN)
            return CallNode(func_name, args, token.line)
        elif token.type == TokenType.MINUS:
            self.advance()
            operand = self.parse_factor()
            return UnaryOpNode('-', operand, token.line)
        elif token.type == TokenType.NOT:
            self.advance()
            operand = self.parse_factor()
            return UnaryOpNode('not', operand, token.line)
        else:
            self.error(f"Token inesperado en expresión: {token}")
