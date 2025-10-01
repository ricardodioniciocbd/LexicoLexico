"""
Módulo de Definición de Tipos de Token
Define todos los tipos de tokens utilizados en el compilador MiniLang
"""

from enum import Enum, auto


class TipoToken(Enum):
    """Enumeración de todos los tipos de tokens en MiniLang"""
    
    # Palabras reservadas
    PRINT = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    RANGE = auto()
    VAR = auto()
    
    # Identificadores y literales
    IDENTIFICADOR = auto()
    NUMERO = auto()
    CADENA = auto()
    
    # Operadores aritméticos
    MAS = auto()
    MENOS = auto()
    MULTIPLICAR = auto()
    DIVIDIR = auto()
    
    # Operadores de comparación
    IGUAL = auto()          # ==
    NO_IGUAL = auto()       # !=
    MENOR = auto()          # <
    MAYOR = auto()          # >
    MENOR_IGUAL = auto()    # <=
    MAYOR_IGUAL = auto()    # >=
    
    # Asignación
    ASIGNAR = auto()        # =
    
    # Delimitadores
    PAREN_IZQ = auto()      # (
    PAREN_DER = auto()      # )
    DOS_PUNTOS = auto()     # :
    COMA = auto()           # ,
    PUNTO_COMA = auto()     # ;
    
    # Especiales
    NUEVA_LINEA = auto()
    INDENTAR = auto()
    DESINDENTAR = auto()
    FIN_ARCHIVO = auto()
    

class Token:
    """Representa un token individual en el código fuente"""
    
    def __init__(self, tipo_token, valor, linea, columna):
        self.tipo = tipo_token
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def __repr__(self):
        return f"Token({self.tipo.name}, {repr(self.valor)}, {self.linea}:{self.columna})"
    
    def __str__(self):
        return f"{self.tipo.name}({self.valor})"


# Mapeo de palabras reservadas
PALABRAS_RESERVADAS = {
    'print': TipoToken.PRINT,
    'if': TipoToken.IF,
    'elif': TipoToken.ELIF,
    'else': TipoToken.ELSE,
    'while': TipoToken.WHILE,
    'for': TipoToken.FOR,
    'in': TipoToken.IN,
    'range': TipoToken.RANGE,
    'var': TipoToken.VAR,
}
