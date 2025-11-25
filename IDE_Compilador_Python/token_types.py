

from enum import Enum, auto


class TokenType(Enum):
   
    
    # Keywords
    PRINT = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RANGE = auto()
    VAR = auto()
    
    # Identifiers and Literals
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    # Arithmetic Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    
    # Comparison Operators
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    LESS = auto()           # <
    GREATER = auto()        # >
    LESS_EQUAL = auto()     # <=
    GREATER_EQUAL = auto()  # >=
    
    # Assignment
    ASSIGN = auto()         # =
    
    # Delimiters
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    COLON = auto()          # :
    COMMA = auto()          # ,
    SEMICOLON = auto()      # ;
    
    # Special
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()
    EOF = auto()
    

class Token:
    """Represents a single token in the source code"""
    
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"
    
    def __str__(self):
        return f"{self.type.name}({self.value})"


# Keywords mapping
KEYWORDS = {
    'print': TokenType.PRINT,
    'if': TokenType.IF,
    'elif': TokenType.ELIF,
    'else': TokenType.ELSE,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'range': TokenType.RANGE,
    'var': TokenType.VAR,
}
