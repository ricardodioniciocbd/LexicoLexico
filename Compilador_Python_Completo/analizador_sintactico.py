"""
Módulo de Análisis Sintáctico (Parser)
Realiza el análisis sintáctico y construye el Árbol de Sintaxis Abstracta (AST)
"""

from tipos_token import TipoToken
from nodos_ast import *


class ErrorSintactico(Exception):
    """Excepción lanzada para errores de sintaxis"""
    pass


class AnalizadorSintactico:
    """Analizador sintáctico de descenso recursivo para MiniLang"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0
        self.token_actual = self.tokens[0] if tokens else None
    
    def error(self, mensaje):
        """Lanzar un error sintáctico con información del token actual"""
        if self.token_actual:
            raise ErrorSintactico(
                f"Error Sintáctico en línea {self.token_actual.linea}, "
                f"columna {self.token_actual.columna}: {mensaje}\n"
                f"Token actual: {self.token_actual}"
            )
        else:
            raise ErrorSintactico(f"Error Sintáctico: {mensaje}")
    
    def mirar(self, desplazamiento=0):
        """Mirar adelante un token sin consumirlo"""
        pos = self.posicion + desplazamiento
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def avanzar(self):
        """Moverse al siguiente token"""
        if self.posicion < len(self.tokens) - 1:
            self.posicion += 1
            self.token_actual = self.tokens[self.posicion]
        return self.token_actual
    
    def esperar(self, tipo_token):
        """Consumir token del tipo esperado o lanzar error"""
        if self.token_actual.tipo != tipo_token:
            self.error(f"Se esperaba {tipo_token.name}, se obtuvo {self.token_actual.tipo.name}")
        token = self.token_actual
        self.avanzar()
        return token
    
    def saltar_nuevas_lineas(self):
        """Saltar cualquier token de nueva línea"""
        while self.token_actual and self.token_actual.tipo == TipoToken.NUEVA_LINEA:
            self.avanzar()
    
    def analizar(self):
        """Punto de entrada principal - analizar programa completo"""
        return self.analizar_programa()
    
    def analizar_programa(self):
        """
        programa → declaraciones
        Acción Semántica: Crear NodoPrograma con lista de sentencias
        """
        sentencias = []
        self.saltar_nuevas_lineas()
        
        while self.token_actual.tipo != TipoToken.FIN_ARCHIVO:
            sentencia = self.analizar_sentencia()
            if sentencia:
                sentencias.append(sentencia)
            self.saltar_nuevas_lineas()
        
        return NodoPrograma(sentencias)
    
    def analizar_sentencia(self):
        """
        Analizar una sentencia individual
        Redirige al analizador de sentencia apropiado según el token actual
        """
        self.saltar_nuevas_lineas()
        
        tipo_token = self.token_actual.tipo
        
        # Asignación o sentencia de expresión
        if tipo_token == TipoToken.IDENTIFICADOR:
            # Mirar adelante para determinar si es una asignación
            if self.mirar(1) and self.mirar(1).tipo == TipoToken.ASIGNAR:
                return self.analizar_asignacion()
            else:
                # Solo una expresión (no debería ocurrir en programas bien formados)
                expr = self.analizar_expresion()
                self.saltar_nuevas_lineas()
                return expr
        
        # Sentencia print
        elif tipo_token == TipoToken.PRINT:
            return self.analizar_print()
        
        # Sentencia if
        elif tipo_token == TipoToken.IF:
            return self.analizar_if()
        
        # Bucle while
        elif tipo_token == TipoToken.WHILE:
            return self.analizar_while()
        
        # Bucle for
        elif tipo_token == TipoToken.FOR:
            return self.analizar_for()
        
        # Declaración de variable (palabra clave 'var' opcional)
        elif tipo_token == TipoToken.VAR:
            self.avanzar()
            return self.analizar_asignacion()
        
        else:
            self.error(f"Token inesperado: {self.token_actual}")
    
    def analizar_asignacion(self):
        """
        asignacion → ID = expresion
        Acción Semántica: Crear NodoAsignacion con identificador y expresión
        """
        linea = self.token_actual.linea
        identificador = self.esperar(TipoToken.IDENTIFICADOR).valor
        self.esperar(TipoToken.ASIGNAR)
        expresion = self.analizar_expresion()
        
        return NodoAsignacion(identificador, expresion, linea)
    
    def analizar_print(self):
        """
        sentencia_print → print(expresion)
        Acción Semántica: Crear NodoPrint con expresión a imprimir
        """
        linea = self.token_actual.linea
        self.esperar(TipoToken.PRINT)
        self.esperar(TipoToken.PAREN_IZQ)
        expresion = self.analizar_expresion()
        self.esperar(TipoToken.PAREN_DER)
        
        return NodoPrint(expresion, linea)
    
    def analizar_if(self):
        """
        condicional → if expresion : bloque (elif expresion : bloque)* (else : bloque)?
        Acción Semántica: Crear NodoIf con condición, bloque entonces, partes elif y bloque sino
        """
        linea = self.token_actual.linea
        self.esperar(TipoToken.IF)
        condicion = self.analizar_expresion()
        self.esperar(TipoToken.DOS_PUNTOS)
        self.saltar_nuevas_lineas()
        
        # Analizar bloque entonces
        bloque_entonces = self.analizar_bloque()
        
        # Analizar partes elif
        partes_elif = []
        while self.token_actual.tipo == TipoToken.ELIF:
            self.avanzar()
            condicion_elif = self.analizar_expresion()
            self.esperar(TipoToken.DOS_PUNTOS)
            self.saltar_nuevas_lineas()
            bloque_elif = self.analizar_bloque()
            partes_elif.append((condicion_elif, bloque_elif))
        
        # Analizar bloque else
        bloque_sino = None
        if self.token_actual.tipo == TipoToken.ELSE:
            self.avanzar()
            self.esperar(TipoToken.DOS_PUNTOS)
            self.saltar_nuevas_lineas()
            bloque_sino = self.analizar_bloque()
        
        return NodoIf(condicion, bloque_entonces, partes_elif, bloque_sino, linea)
    
    def analizar_while(self):
        """
        bucle_while → while expresion : bloque
        Acción Semántica: Crear NodoWhile con condición y bloque
        """
        linea = self.token_actual.linea
        self.esperar(TipoToken.WHILE)
        condicion = self.analizar_expresion()
        self.esperar(TipoToken.DOS_PUNTOS)
        self.saltar_nuevas_lineas()
        bloque = self.analizar_bloque()
        
        return NodoWhile(condicion, bloque, linea)
    
    def analizar_for(self):
        """
        bucle_for → for ID in range(expresion) : bloque
        Acción Semántica: Crear NodoFor con variable iteradora, expresión de rango y bloque
        """
        linea = self.token_actual.linea
        self.esperar(TipoToken.FOR)
        identificador = self.esperar(TipoToken.IDENTIFICADOR).valor
        self.esperar(TipoToken.IN)
        self.esperar(TipoToken.RANGE)
        self.esperar(TipoToken.PAREN_IZQ)
        expresion_rango = self.analizar_expresion()
        self.esperar(TipoToken.PAREN_DER)
        self.esperar(TipoToken.DOS_PUNTOS)
        self.saltar_nuevas_lineas()
        bloque = self.analizar_bloque()
        
        return NodoFor(identificador, expresion_rango, bloque, linea)
    
    def analizar_bloque(self):
        """
        Analizar un bloque indentado de sentencias
        Acción Semántica: Crear NodoBloque con lista de sentencias
        """
        sentencias = []
        
        # Esperar INDENTAR
        if self.token_actual.tipo != TipoToken.INDENTAR:
            self.error("Se esperaba bloque indentado")
        self.avanzar()
        self.saltar_nuevas_lineas()
        
        # Analizar sentencias hasta DESINDENTAR
        while self.token_actual.tipo not in (TipoToken.DESINDENTAR, TipoToken.FIN_ARCHIVO):
            sentencia = self.analizar_sentencia()
            if sentencia:
                sentencias.append(sentencia)
            self.saltar_nuevas_lineas()
        
        # Consumir DESINDENTAR
        if self.token_actual.tipo == TipoToken.DESINDENTAR:
            self.avanzar()
        
        return NodoBloque(sentencias)
    
    def analizar_expresion(self):
        """
        expresion → comparacion
        Punto de entrada para análisis de expresiones
        """
        return self.analizar_comparacion()
    
    def analizar_comparacion(self):
        """
        comparacion → aritmetica ((==|!=|<|>|<=|>=) aritmetica)?
        Acción Semántica: Crear NodoOperacionBinaria para operaciones de comparación
        """
        izquierda = self.analizar_aritmetica()
        
        operadores_comparacion = {
            TipoToken.IGUAL, TipoToken.NO_IGUAL,
            TipoToken.MENOR, TipoToken.MAYOR,
            TipoToken.MENOR_IGUAL, TipoToken.MAYOR_IGUAL
        }
        
        if self.token_actual.tipo in operadores_comparacion:
            operador = self.token_actual.valor
            linea = self.token_actual.linea
            self.avanzar()
            derecha = self.analizar_aritmetica()
            return NodoOperacionBinaria(izquierda, operador, derecha, linea)
        
        return izquierda
    
    def analizar_aritmetica(self):
        """
        expresion → termino ((+|-) termino)*
        Acción Semántica: Crear árbol de NodoOperacionBinaria con asociatividad izquierda
        """
        izquierda = self.analizar_termino()
        
        while self.token_actual.tipo in (TipoToken.MAS, TipoToken.MENOS):
            operador = self.token_actual.valor
            linea = self.token_actual.linea
            self.avanzar()
            derecha = self.analizar_termino()
            izquierda = NodoOperacionBinaria(izquierda, operador, derecha, linea)
        
        return izquierda
    
    def analizar_termino(self):
        """
        termino → factor ((*|/) factor)*
        Acción Semántica: Crear NodoOperacionBinaria para multiplicación/división con mayor precedencia
        """
        izquierda = self.analizar_factor()
        
        while self.token_actual.tipo in (TipoToken.MULTIPLICAR, TipoToken.DIVIDIR):
            operador = self.token_actual.valor
            linea = self.token_actual.linea
            self.avanzar()
            derecha = self.analizar_factor()
            izquierda = NodoOperacionBinaria(izquierda, operador, derecha, linea)
        
        return izquierda
    
    def analizar_factor(self):
        """
        factor → NUMERO | CADENA | ID | (expresion) | -factor
        Acción Semántica: Crear nodo hoja apropiado o manejar expresión entre paréntesis
        """
        token = self.token_actual
        
        # Literal numérico
        if token.tipo == TipoToken.NUMERO:
            self.avanzar()
            return NodoNumero(token.valor, token.linea)
        
        # Literal de cadena
        elif token.tipo == TipoToken.CADENA:
            self.avanzar()
            return NodoCadena(token.valor, token.linea)
        
        # Identificador
        elif token.tipo == TipoToken.IDENTIFICADOR:
            self.avanzar()
            return NodoIdentificador(token.valor, token.linea)
        
        # Expresión entre paréntesis
        elif token.tipo == TipoToken.PAREN_IZQ:
            self.avanzar()
            expr = self.analizar_expresion()
            self.esperar(TipoToken.PAREN_DER)
            return expr
        
        # Menos unario
        elif token.tipo == TipoToken.MENOS:
            self.avanzar()
            operando = self.analizar_factor()
            return NodoOperacionUnaria('-', operando, token.linea)
        
        else:
            self.error(f"Token inesperado en expresión: {token}")
