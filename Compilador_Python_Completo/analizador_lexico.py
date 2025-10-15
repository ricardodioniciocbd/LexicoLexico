"""
Módulo de Análisis Léxico
Realiza la tokenización del código fuente de MiniLang
"""

import re
from tipos_token import Token, TipoToken, PALABRAS_RESERVADAS


class ErrorLexico(Exception):
    """Excepción lanzada para errores de análisis léxico"""
    pass


class AnalizadorLexico:
    """Analizador léxico para MiniLang"""
    
    def __init__(self, codigo_fuente):
        self.fuente = codigo_fuente
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.pila_indentacion = [0]  # Rastrear niveles de indentación
        
    def error(self, mensaje):
        """Lanzar un error léxico con información de posición"""
        raise ErrorLexico(f"Error Léxico en línea {self.linea}, columna {self.columna}: {mensaje}")
    
    def mirar(self, desplazamiento=0):
        """Mirar adelante un carácter sin consumirlo"""
        pos = self.posicion + desplazamiento
        if pos < len(self.fuente):
            return self.fuente[pos]
        return None
    
    def avanzar(self):
        """Consumir y retornar el carácter actual"""
        if self.posicion < len(self.fuente):
            caracter = self.fuente[self.posicion]
            self.posicion += 1
            if caracter == '\n':
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            return caracter
        return None
    
    def saltar_espacios(self):
        """Saltar espacios y tabulaciones (pero no saltos de línea)"""
        while self.mirar() in ' \t':
            self.avanzar()
    
    def saltar_comentario(self):
        """Saltar comentarios de una línea que comienzan con # o //"""
        if self.mirar() == '#' or (self.mirar() == '/' and self.mirar(1) == '/'):
            while self.mirar() and self.mirar() != '\n':
                self.avanzar()
    
    def leer_numero(self):
        """Leer un literal numérico (entero o flotante)"""
        linea_inicio = self.linea
        columna_inicio = self.columna
        cadena_num = ''
        
        while self.mirar() and (self.mirar().isdigit() or self.mirar() == '.'):
            cadena_num += self.avanzar()
        
        # Convertir al tipo numérico apropiado
        try:
            if '.' in cadena_num:
                valor = float(cadena_num)
            else:
                valor = int(cadena_num)
            return Token(TipoToken.NUMERO, valor, linea_inicio, columna_inicio)
        except ValueError:
            self.error(f"Formato de número inválido: {cadena_num}")
    
    def leer_cadena(self):
        """Leer un literal de cadena encerrado entre comillas"""
        linea_inicio = self.linea
        columna_inicio = self.columna
        caracter_comilla = self.avanzar()  # Consumir comilla de apertura
        valor_cadena = ''
        
        while self.mirar() and self.mirar() != caracter_comilla:
            if self.mirar() == '\\':
                self.avanzar()
                siguiente_car = self.avanzar()
                # Manejar secuencias de escape
                mapa_escape = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                valor_cadena += mapa_escape.get(siguiente_car, siguiente_car)
            else:
                valor_cadena += self.avanzar()
        
        if self.mirar() != caracter_comilla:
            self.error("Literal de cadena sin terminar")
        
        self.avanzar()  # Consumir comilla de cierre
        return Token(TipoToken.CADENA, valor_cadena, linea_inicio, columna_inicio)
    
    def leer_identificador(self):
        """Leer un identificador o palabra reservada"""
        linea_inicio = self.linea
        columna_inicio = self.columna
        identificador = ''
        
        while self.mirar() and (self.mirar().isalnum() or self.mirar() == '_'):
            identificador += self.avanzar()
        
        # Verificar si es una palabra reservada
        tipo_token = PALABRAS_RESERVADAS.get(identificador, TipoToken.IDENTIFICADOR)
        return Token(tipo_token, identificador, linea_inicio, columna_inicio)
    
    def manejar_indentacion(self, nivel_indentacion):
        """Generar tokens INDENTAR/DESINDENTAR basados en cambios de indentación"""
        tokens = []
        indentacion_actual = self.pila_indentacion[-1]
        
        if nivel_indentacion > indentacion_actual:
            self.pila_indentacion.append(nivel_indentacion)
            tokens.append(Token(TipoToken.INDENTAR, nivel_indentacion, self.linea, 1))
        elif nivel_indentacion < indentacion_actual:
            while self.pila_indentacion and self.pila_indentacion[-1] > nivel_indentacion:
                self.pila_indentacion.pop()
                tokens.append(Token(TipoToken.DESINDENTAR, nivel_indentacion, self.linea, 1))
            
            if not self.pila_indentacion or self.pila_indentacion[-1] != nivel_indentacion:
                self.error("Indentación inconsistente")
        
        return tokens
    
    def tokenizar(self):
        """Método principal de tokenización - convierte código fuente en tokens"""
        self.tokens = []
        al_inicio_linea = True
        
        while self.posicion < len(self.fuente):
            # Manejar indentación al inicio de las líneas
            if al_inicio_linea:
                nivel_indentacion = 0
                while self.mirar() in ' \t':
                    if self.mirar() == ' ':
                        nivel_indentacion += 1
                    elif self.mirar() == '\t':
                        nivel_indentacion += 4  # Tab = 4 espacios
                    self.avanzar()
                
                # Saltar líneas vacías y comentarios
                if self.mirar() in '\n#' or (self.mirar() == '/' and self.mirar(1) == '/'):
                    if self.mirar() == '\n':
                        self.avanzar()
                    else:
                        self.saltar_comentario()
                    continue
                
                # Generar tokens de indentación/desindentación
                tokens_indentacion = self.manejar_indentacion(nivel_indentacion)
                self.tokens.extend(tokens_indentacion)
                al_inicio_linea = False
            
            self.saltar_espacios()
            
            if not self.mirar():
                break
            
            caracter = self.mirar()
            linea_inicio = self.linea
            columna_inicio = self.columna
            
            # Comentarios
            if caracter == '#' or (caracter == '/' and self.mirar(1) == '/'):
                self.saltar_comentario()
                continue
            
            # Nueva línea
            elif caracter == '\n':
                self.avanzar()
                self.tokens.append(Token(TipoToken.NUEVA_LINEA, '\\n', linea_inicio, columna_inicio))
                al_inicio_linea = True
            
            # Números
            elif caracter.isdigit():
                self.tokens.append(self.leer_numero())
            
            # Cadenas
            elif caracter in '"\'':
                self.tokens.append(self.leer_cadena())
            
            # Identificadores y palabras reservadas
            elif caracter.isalpha() or caracter == '_':
                self.tokens.append(self.leer_identificador())
            
            # Operadores de dos caracteres
            elif caracter == '=' and self.mirar(1) == '=':
                self.avanzar()
                self.avanzar()
                self.tokens.append(Token(TipoToken.IGUAL, '==', linea_inicio, columna_inicio))
            
            elif caracter == '!' and self.mirar(1) == '=':
                self.avanzar()
                self.avanzar()
                self.tokens.append(Token(TipoToken.NO_IGUAL, '!=', linea_inicio, columna_inicio))
            
            elif caracter == '<' and self.mirar(1) == '=':
                self.avanzar()
                self.avanzar()
                self.tokens.append(Token(TipoToken.MENOR_IGUAL, '<=', linea_inicio, columna_inicio))
            
            elif caracter == '>' and self.mirar(1) == '=':
                self.avanzar()
                self.avanzar()
                self.tokens.append(Token(TipoToken.MAYOR_IGUAL, '>=', linea_inicio, columna_inicio))
            
            # Operadores y delimitadores de un solo carácter
            elif caracter == '+':
                self.avanzar()
                self.tokens.append(Token(TipoToken.MAS, '+', linea_inicio, columna_inicio))
            
            elif caracter == '-':
                self.avanzar()
                self.tokens.append(Token(TipoToken.MENOS, '-', linea_inicio, columna_inicio))
            
            elif caracter == '*':
                self.avanzar()
                self.tokens.append(Token(TipoToken.MULTIPLICAR, '*', linea_inicio, columna_inicio))
            
            elif caracter == '/':
                self.avanzar()
                self.tokens.append(Token(TipoToken.DIVIDIR, '/', linea_inicio, columna_inicio))
            
            elif caracter == '=':
                self.avanzar()
                self.tokens.append(Token(TipoToken.ASIGNAR, '=', linea_inicio, columna_inicio))
            
            elif caracter == '<':
                self.avanzar()
                self.tokens.append(Token(TipoToken.MENOR, '<', linea_inicio, columna_inicio))
            
            elif caracter == '>':
                self.avanzar()
                self.tokens.append(Token(TipoToken.MAYOR, '>', linea_inicio, columna_inicio))
            
            elif caracter == '(':
                self.avanzar()
                self.tokens.append(Token(TipoToken.PAREN_IZQ, '(', linea_inicio, columna_inicio))
            
            elif caracter == ')':
                self.avanzar()
                self.tokens.append(Token(TipoToken.PAREN_DER, ')', linea_inicio, columna_inicio))
            
            elif caracter == ':':
                self.avanzar()
                self.tokens.append(Token(TipoToken.DOS_PUNTOS, ':', linea_inicio, columna_inicio))
            
            elif caracter == ',':
                self.avanzar()
                self.tokens.append(Token(TipoToken.COMA, ',', linea_inicio, columna_inicio))
            
            elif caracter == ';':
                self.avanzar()
                self.tokens.append(Token(TipoToken.PUNTO_COMA, ';', linea_inicio, columna_inicio))
            
            else:
                self.error(f"Carácter inesperado: '{caracter}'")
        
        # Agregar tokens DESINDENTAR restantes
        while len(self.pila_indentacion) > 1:
            self.pila_indentacion.pop()
            self.tokens.append(Token(TipoToken.DESINDENTAR, 0, self.linea, self.columna))
        
        # Agregar token de fin de archivo
        self.tokens.append(Token(TipoToken.FIN_ARCHIVO, None, self.linea, self.columna))
        return self.tokens
