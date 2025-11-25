"""
Módulo de Análisis Sintáctico (Parser)
Realiza el análisis sintáctico y construye el Árbol de Sintaxis Abstracta (AST)
PUNTO 3: Implementa Gramática Libre de Contexto (CFG) tipo LL(1)
"""

from token_types import TokenType
from ast_nodes import *


class ParserError(Exception):
    """Excepción lanzada cuando hay errores sintácticos"""
    pass


class Parser:
    """
    Parser de Descenso Recursivo - PUNTO 3
    Implementa análisis sintáctico LL(1) sin recursión izquierda
    Construye el AST (Árbol de Sintaxis Abstracta)
    """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, message):
        """Lanza un error sintáctico con información del token actual"""
        if self.current_token:
            raise ParserError(
                f"Error Sintáctico en línea {self.current_token.line}, "
                f"columna {self.current_token.column}: {message}\n"
                f"Token actual: {self.current_token}"
            )
        else:
            raise ParserError(f"Error Sintáctico: {message}")
    
    def peek(self, offset=0):
        """Lookahead: Mira el siguiente token sin consumirlo"""
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self):
        """Avanza al siguiente token"""
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        return self.current_token
    
    def expect(self, token_type):
        """Consume token del tipo esperado o lanza error"""
        if self.current_token.type != token_type:
            self.error(f"Se esperaba {token_type.name}, se encontró {self.current_token.type.name}")
        token = self.current_token
        self.advance()
        return token
    
    def skip_newlines(self):
        """Salta tokens de nueva línea (NEWLINE)"""
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def parse(self):
        """Punto de entrada principal - analiza todo el programa"""
        return self.parse_program()
    
    def parse_program(self):
        """
        Producción: programa → declaraciones
        Acción Semántica: Crea ProgramNode con lista de sentencias
        """
        statements = []
        self.skip_newlines()
        
        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return ProgramNode(statements)
    
    def parse_statement(self):
        """
        Parse a single statement
        Routes to appropriate statement parser based on current token
        """
        self.skip_newlines()
        
        token_type = self.current_token.type
        
        # Assignment or expression statement
        if token_type == TokenType.IDENTIFIER:
            # Look ahead to determine if it's an assignment
            if self.peek(1) and self.peek(1).type == TokenType.ASSIGN:
                return self.parse_assignment()
            else:
                # Just an expression (shouldn't happen in well-formed programs)
                expr = self.parse_expression()
                self.skip_newlines()
                return expr
        
        # Print statement
        elif token_type == TokenType.PRINT:
            return self.parse_print()
        
        # If statement
        elif token_type == TokenType.IF:
            return self.parse_if()
        
        # While loop
        elif token_type == TokenType.WHILE:
            return self.parse_while()
        
        # For loop
        elif token_type == TokenType.FOR:
            return self.parse_for()
        
        # Variable declaration (optional 'var' keyword)
        elif token_type == TokenType.VAR:
            self.advance()
            return self.parse_assignment()
        
        else:
            self.error(f"Unexpected token: {self.current_token}")
    
    def parse_assignment(self):
        """
        asignacion → ID = expresion
        Semantic Action: Create AssignmentNode with identifier and expression
        """
        line = self.current_token.line
        identifier = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        expression = self.parse_expression()
        
        return AssignmentNode(identifier, expression, line)
    
    def parse_print(self):
        """
        print_statement → print(expresion)
        Semantic Action: Create PrintNode with expression to print
        """
        line = self.current_token.line
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        expression = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        return PrintNode(expression, line)
    
    def parse_if(self):
        """
        condicional → if expresion : bloque (elif expresion : bloque)* (else : bloque)?
        Semantic Action: Create IfNode with condition, then block, elif parts, and else block
        """
        line = self.current_token.line
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        
        # Parse then block
        then_block = self.parse_block()
        
        # Parse elif parts
        elif_parts = []
        while self.current_token.type == TokenType.ELIF:
            self.advance()
            elif_condition = self.parse_expression()
            self.expect(TokenType.COLON)
            self.skip_newlines()
            elif_block = self.parse_block()
            elif_parts.append((elif_condition, elif_block))
        
        # Parse else block
        else_block = None
        if self.current_token.type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.COLON)
            self.skip_newlines()
            else_block = self.parse_block()
        
        return IfNode(condition, then_block, elif_parts, else_block, line)
    
    def parse_while(self):
        """
        bucle_while → while expresion : bloque
        Semantic Action: Create WhileNode with condition and block
        """
        line = self.current_token.line
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.COLON)
        self.skip_newlines()
        block = self.parse_block()
        
        return WhileNode(condition, block, line)
    
    def parse_for(self):
        """
        bucle_for → for ID in range(expresion) : bloque
        Semantic Action: Create ForNode with iterator variable, range expression, and block
        """
        line = self.current_token.line
        self.expect(TokenType.FOR)
        identifier = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IN)
        self.expect(TokenType.RANGE)
        self.expect(TokenType.LPAREN)
        range_expr = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.COLON)
        self.skip_newlines()
        block = self.parse_block()
        
        return ForNode(identifier, range_expr, block, line)
    
    def parse_block(self):
        """
        Parse an indented block of statements
        Semantic Action: Create BlockNode with list of statements
        """
        statements = []
        
        # Expect INDENT
        if self.current_token.type != TokenType.INDENT:
            self.error("Expected indented block")
        self.advance()
        self.skip_newlines()
        
        # Parse statements until DEDENT
        while self.current_token.type not in (TokenType.DEDENT, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        # Consume DEDENT
        if self.current_token.type == TokenType.DEDENT:
            self.advance()
        
        return BlockNode(statements)
    
    def parse_expression(self):
        """
        expresion → comparacion
        Entry point for expression parsing
        """
        return self.parse_comparison()
    
    def parse_comparison(self):
        """
        comparacion → aritmetica ((==|!=|<|>|<=|>=) aritmetica)?
        Semantic Action: Create BinaryOpNode for comparison operations
        """
        left = self.parse_arithmetic()
        
        comparison_ops = {
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.LESS, TokenType.GREATER,
            TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL
        }
        
        if self.current_token.type in comparison_ops:
            operator = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_arithmetic()
            return BinaryOpNode(left, operator, right, line)
        
        return left
    
    def parse_arithmetic(self):
        """
        expresion → termino ((+|-) termino)*
        Semantic Action: Create BinaryOpNode tree with left associativity
        """
        left = self.parse_term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_term()
            left = BinaryOpNode(left, operator, right, line)
        
        return left
    
    def parse_term(self):
        """
        termino → factor ((*|/) factor)*
        Semantic Action: Create BinaryOpNode for multiplication/division with higher precedence
        """
        left = self.parse_factor()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_factor()
            left = BinaryOpNode(left, operator, right, line)
        
        return left
    
    def parse_factor(self):
        """
        factor → NUMBER | STRING | ID | (expresion) | -factor
        Semantic Action: Create appropriate leaf node or handle parenthesized expression
        """
        token = self.current_token
        
        # Number literal
        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value, token.line)
        
        # String literal
        elif token.type == TokenType.STRING:
            self.advance()
            return StringNode(token.value, token.line)
        
        # Identifier
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return IdentifierNode(token.value, token.line)
        
        # Parenthesized expression
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # Unary minus
        elif token.type == TokenType.MINUS:
            self.advance()
            operand = self.parse_factor()
            return UnaryOpNode('-', operand, token.line)
        
        else:
            self.error(f"Unexpected token in expression: {token}")
