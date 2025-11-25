"""
Módulo de Análisis Léxico
Realiza la tokenización del código fuente (convierte texto en tokens)
PUNTO 2: Implementa Autómatas Finitos Deterministas (AFD)
"""

import re
from token_types import Token, TokenType, KEYWORDS


class LexerError(Exception):
    """Excepción lanzada cuando hay errores léxicos"""
    pass


class Lexer:
    """
    Analizador Léxico (Lexer) - PUNTO 2
    Implementa AFD (Autómata Finito Determinista) para reconocer tokens
    """
    
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0  # Posición actual en el código
        self.line = 1  # Línea actual
        self.column = 1  # Columna actual
        self.tokens = []  # Lista de tokens generados
        self.indent_stack = [0]  # Pila para rastrear niveles de indentación
        
    def error(self, message):
        """Lanza un error léxico con información de posición"""
        raise LexerError(f"Error Léxico en línea {self.line}, columna {self.column}: {message}")
    
    def peek(self, offset=0):
        """
        Lookahead: Mira el siguiente carácter sin consumirlo
        Esencial para AFD con lookahead
        """
        pos = self.position + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self):
        """Consume y retorna el carácter actual (avanza en el código)"""
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
        """Salta espacios y tabs (pero no saltos de línea)"""
        while self.peek() in ' \t':
            self.advance()
    
    def skip_comment(self):
        """Salta comentarios de una línea que empiezan con # o //"""
        if self.peek() == '#' or (self.peek() == '/' and self.peek(1) == '/'):
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_number(self):
        """
        AFD para leer números (enteros o flotantes)
        Estados: q0 → q1 (dígitos) → q2 (punto) → q3 (más dígitos)
        """
        start_line = self.line
        start_column = self.column
        num_str = ''
        
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.advance()
        
        # Convertir a tipo numérico apropiado
        try:
            if '.' in num_str:
                value = float(num_str)
            else:
                value = int(num_str)
            return Token(TokenType.NUMBER, value, start_line, start_column)
        except ValueError:
            self.error(f"Formato de número inválido: {num_str}")
    
    def read_string(self):
        """
        AFD para leer cadenas de texto (strings) encerradas en comillas
        Maneja secuencias de escape como \n, \t, etc.
        """
        start_line = self.line
        start_column = self.column
        quote_char = self.advance()  # Consume opening quote
        string_value = ''
        
        while self.peek() and self.peek() != quote_char:
            if self.peek() == '\\':
                self.advance()
                next_char = self.advance()
                # Manejar secuencias de escape
                escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                string_value += escape_map.get(next_char, next_char)
            else:
                string_value += self.advance()
        
        if self.peek() != quote_char:
            self.error("Cadena de texto sin cerrar (falta comilla final)")
        
        self.advance()  # Consumir comilla de cierre
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def read_identifier(self):
        """
        AFD para leer identificadores o palabras clave
        Estados: q0 --[letra|_]--> q1 --[letra|dígito|_]--> q1 (ACEPTA)
        """
        start_line = self.line
        start_column = self.column
        identifier = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            identifier += self.advance()
        
        # Verificar si es una palabra clave (keyword)
        token_type = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        return Token(token_type, identifier, start_line, start_column)
    
    def handle_indentation(self, indent_level):
        """
        Genera tokens INDENT/DEDENT basado en cambios de indentación
        Importante para lenguajes como Python que usan indentación significativa
        """
        tokens = []
        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            self.indent_stack.append(indent_level)
            tokens.append(Token(TokenType.INDENT, indent_level, self.line, 1))
        elif indent_level < current_indent:
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                tokens.append(Token(TokenType.DEDENT, indent_level, self.line, 1))
            
            if not self.indent_stack or self.indent_stack[-1] != indent_level:
                self.error("Indentación inconsistente")
        
        return tokens
    
    def tokenize(self):
        """
        Método principal de tokenización - convierte código fuente en tokens
        Este es el punto de entrada del análisis léxico
        """
        self.tokens = []
        at_line_start = True
        
        while self.position < len(self.source):
            # Handle indentation at the start of lines
            if at_line_start:
                indent_level = 0
                while self.peek() in ' \t':
                    if self.peek() == ' ':
                        indent_level += 1
                    elif self.peek() == '\t':
                        indent_level += 4  # Tab = 4 spaces
                    self.advance()
                
                # Skip empty lines and comments
                if self.peek() in '\n#' or (self.peek() == '/' and self.peek(1) == '/'):
                    if self.peek() == '\n':
                        self.advance()
                    else:
                        self.skip_comment()
                    continue
                
                # Generate indent/dedent tokens
                indent_tokens = self.handle_indentation(indent_level)
                self.tokens.extend(indent_tokens)
                at_line_start = False
            
            self.skip_whitespace()
            
            if not self.peek():
                break
            
            char = self.peek()
            start_line = self.line
            start_column = self.column
            
            # Comments
            if char == '#' or (char == '/' and self.peek(1) == '/'):
                self.skip_comment()
                continue
            
            # Newline
            elif char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', start_line, start_column))
                at_line_start = True
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings
            elif char in '"\'':
                self.tokens.append(self.read_string())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Two-character operators
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
            
            # Single-character operators and delimiters
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
            
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_column))
            
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_column))
            
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_column))
            
            else:
                self.error(f"Unexpected character: '{char}'")
        
        # Add remaining DEDENT tokens
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(TokenType.DEDENT, 0, self.line, self.column))
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
