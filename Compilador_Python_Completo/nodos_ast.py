"""
Definiciones de Nodos del Árbol de Sintaxis Abstracta (AST)
Define todos los tipos de nodos AST para MiniLang
"""


class NodoAST:
    """Clase base para todos los nodos AST"""
    pass


# Estructura del programa
class NodoPrograma(NodoAST):
    """Nodo raíz que representa el programa completo"""
    def __init__(self, sentencias):
        self.sentencias = sentencias
    
    def __repr__(self):
        return f"Programa({len(self.sentencias)} sentencias)"


# Sentencias
class NodoAsignacion(NodoAST):
    """Asignación de variable: identificador = expresion"""
    def __init__(self, identificador, expresion, linea=0):
        self.identificador = identificador
        self.expresion = expresion
        self.linea = linea
    
    def __repr__(self):
        return f"Asignacion({self.identificador} = {self.expresion})"


class NodoPrint(NodoAST):
    """Sentencia print: print(expresion)"""
    def __init__(self, expresion, linea=0):
        self.expresion = expresion
        self.linea = linea
    
    def __repr__(self):
        return f"Print({self.expresion})"


class NodoIf(NodoAST):
    """Sentencia condicional: if/elif/else"""
    def __init__(self, condicion, bloque_entonces, partes_elif=None, bloque_sino=None, linea=0):
        self.condicion = condicion
        self.bloque_entonces = bloque_entonces
        self.partes_elif = partes_elif or []  # Lista de tuplas (condicion, bloque)
        self.bloque_sino = bloque_sino
        self.linea = linea
    
    def __repr__(self):
        return f"If(condicion={self.condicion}, elifs={len(self.partes_elif)}, tiene_else={self.bloque_sino is not None})"


class NodoWhile(NodoAST):
    """Bucle while: while condicion: bloque"""
    def __init__(self, condicion, bloque, linea=0):
        self.condicion = condicion
        self.bloque = bloque
        self.linea = linea
    
    def __repr__(self):
        return f"While({self.condicion})"


class NodoFor(NodoAST):
    """Bucle for: for identificador in range(expresion): bloque"""
    def __init__(self, identificador, expresion_rango, bloque, linea=0):
        self.identificador = identificador
        self.expresion_rango = expresion_rango
        self.bloque = bloque
        self.linea = linea
    
    def __repr__(self):
        return f"For({self.identificador} in range({self.expresion_rango}))"


# Expresiones
class NodoOperacionBinaria(NodoAST):
    """Operación binaria: izquierda operador derecha"""
    def __init__(self, izquierda, operador, derecha, linea=0):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha
        self.linea = linea
    
    def __repr__(self):
        return f"OpBinaria({self.izquierda} {self.operador} {self.derecha})"


class NodoOperacionUnaria(NodoAST):
    """Operación unaria: operador operando"""
    def __init__(self, operador, operando, linea=0):
        self.operador = operador
        self.operando = operando
        self.linea = linea
    
    def __repr__(self):
        return f"OpUnaria({self.operador}{self.operando})"


class NodoNumero(NodoAST):
    """Literal numérico"""
    def __init__(self, valor, linea=0):
        self.valor = valor
        self.linea = linea
    
    def __repr__(self):
        return f"Numero({self.valor})"


class NodoCadena(NodoAST):
    """Literal de cadena"""
    def __init__(self, valor, linea=0):
        self.valor = valor
        self.linea = linea
    
    def __repr__(self):
        return f"Cadena({repr(self.valor)})"


class NodoIdentificador(NodoAST):
    """Identificador de variable"""
    def __init__(self, nombre, linea=0):
        self.nombre = nombre
        self.linea = linea
    
    def __repr__(self):
        return f"Identificador({self.nombre})"


class NodoBloque(NodoAST):
    """Bloque de sentencias (usado en estructuras de control)"""
    def __init__(self, sentencias):
        self.sentencias = sentencias
    
    def __repr__(self):
        return f"Bloque({len(self.sentencias)} sentencias)"
