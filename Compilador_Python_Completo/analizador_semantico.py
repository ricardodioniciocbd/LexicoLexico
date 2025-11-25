"""
Módulo de Análisis Semántico
Realiza análisis semántico incluyendo verificación de tipos y gestión de tabla de símbolos
"""

from nodos_ast import *


class ErrorSemantico(Exception):
    """Excepción lanzada para errores semánticos"""
    pass


class TablaSimbolos:
    """Tabla de símbolos para rastrear variables y sus tipos"""
    
    def __init__(self, padre=None):
        self.simbolos = {}
        self.padre = padre
    
    def definir(self, nombre, tipo_var, valor=None):
        """Definir una nueva variable en el ámbito actual"""
        self.simbolos[nombre] = {
            'tipo': tipo_var,
            'valor': valor,
            'inicializada': valor is not None
        }
    
    def buscar(self, nombre):
        """Buscar una variable en el ámbito actual o ámbitos padre"""
        if nombre in self.simbolos:
            return self.simbolos[nombre]
        elif self.padre:
            return self.padre.buscar(nombre)
        return None
    
    def actualizar(self, nombre, tipo_var=None, valor=None):
        """Actualizar una variable existente"""
        if nombre in self.simbolos:
            if tipo_var:
                self.simbolos[nombre]['tipo'] = tipo_var
            if valor is not None:
                self.simbolos[nombre]['valor'] = valor
                self.simbolos[nombre]['inicializada'] = True
        elif self.padre:
            self.padre.actualizar(nombre, tipo_var, valor)
    
    def existe(self, nombre):
        """Verificar si la variable existe en cualquier ámbito"""
        return self.buscar(nombre) is not None


class AnalizadorSemantico:
    """Realiza análisis semántico sobre el AST"""
    
    def __init__(self):
        self.ambito_global = TablaSimbolos()
        self.ambito_actual = self.ambito_global
        self.errores = []
        self.advertencias = []
    
    def error(self, mensaje, linea=0):
        """Registrar un error semántico"""
        mensaje_error = f"Error Semántico en línea {linea}: {mensaje}"
        self.errores.append(mensaje_error)
    
    def advertencia(self, mensaje, linea=0):
        """Registrar una advertencia semántica"""
        mensaje_advertencia = f"Advertencia en línea {linea}: {mensaje}"
        self.advertencias.append(mensaje_advertencia)
    
    def entrar_ambito(self):
        """Entrar a un nuevo ámbito (por ejemplo, para bloques)"""
        self.ambito_actual = TablaSimbolos(padre=self.ambito_actual)
    
    def salir_ambito(self):
        """Salir del ámbito actual"""
        if self.ambito_actual.padre:
            self.ambito_actual = self.ambito_actual.padre
    
    def analizar(self, ast):
        """Punto de entrada principal para análisis semántico"""
        self.visitar(ast)
        return len(self.errores) == 0
    
    def visitar(self, nodo):
        """Despachar al método visitante apropiado"""
        nombre_metodo = f'visitar_{nodo.__class__.__name__}'
        visitante = getattr(self, nombre_metodo, self.visita_generica)
        return visitante(nodo)
    
    def visita_generica(self, nodo):
        """Visitante por defecto para tipos de nodo desconocidos"""
        raise Exception(f'No hay método de visita para {nodo.__class__.__name__}')
    
    # Métodos visitantes para cada tipo de nodo AST
    
    def visitar_NodoPrograma(self, nodo):
        """Visitar nodo raíz del programa"""
        for sentencia in nodo.sentencias:
            self.visitar(sentencia)
    
    def visitar_NodoAsignacion(self, nodo):
        """
        Acción Semántica: Agregar/actualizar variable en tabla de símbolos, inferir tipo
        """
        # Evaluar tipo de expresión
        tipo_expr = self.visitar(nodo.expresion)
        
        # Verificar si la variable ya existe
        if self.ambito_actual.existe(nodo.identificador):
            # Actualizar variable existente (tipado dinámico permite cambio de tipo)
            self.ambito_actual.actualizar(nodo.identificador, tipo_expr)
        else:
            # Definir nueva variable
            self.ambito_actual.definir(nodo.identificador, tipo_expr)
        
        return tipo_expr
    
    def visitar_NodoPrint(self, nodo):
        """Visitar sentencia print"""
        tipo_expr = self.visitar(nodo.expresion)
        return None
    
    def visitar_NodoIf(self, nodo):
        """
        Acción Semántica: Verificar condición válida, analizar bloques en nuevos ámbitos
        """
        # Verificar condición
        tipo_cond = self.visitar(nodo.condicion)
        
        # Analizar bloque entonces
        self.entrar_ambito()
        for sentencia in nodo.bloque_entonces.sentencias:
            self.visitar(sentencia)
        self.salir_ambito()
        
        # Analizar bloques elif
        for cond_elif, bloque_elif in nodo.partes_elif:
            self.visitar(cond_elif)
            self.entrar_ambito()
            for sentencia in bloque_elif.sentencias:
                self.visitar(sentencia)
            self.salir_ambito()
        
        # Analizar bloque else
        if nodo.bloque_sino:
            self.entrar_ambito()
            for sentencia in nodo.bloque_sino.sentencias:
                self.visitar(sentencia)
            self.salir_ambito()
        
        return None
    
    def visitar_NodoWhile(self, nodo):
        """
        Acción Semántica: Verificar condición, analizar bloque en nuevo ámbito
        """
        # Verificar condición
        tipo_cond = self.visitar(nodo.condicion)
        
        # Analizar bloque
        self.entrar_ambito()
        for sentencia in nodo.bloque.sentencias:
            self.visitar(sentencia)
        self.salir_ambito()
        
        return None
    
    def visitar_NodoFor(self, nodo):
        """
        Acción Semántica: Verificar rango numérico, definir variable de bucle, analizar bloque
        """
        # Verificar que expresión de rango sea numérica
        tipo_rango = self.visitar(nodo.expresion_rango)
        if tipo_rango not in ('int', 'float', 'numero'):
            self.error(f"La expresión de rango debe ser numérica, se obtuvo {tipo_rango}", nodo.linea)
        
        # Entrar a nuevo ámbito y definir variable de bucle
        self.entrar_ambito()
        self.ambito_actual.definir(nodo.identificador, 'int')
        
        # Analizar bloque
        for sentencia in nodo.bloque.sentencias:
            self.visitar(sentencia)
        
        self.salir_ambito()
        return None
    
    def visitar_NodoOperacionBinaria(self, nodo):
        """
        Acción Semántica: Verificar tipos de operandos, determinar tipo de resultado
        """
        tipo_izq = self.visitar(nodo.izquierda)
        tipo_der = self.visitar(nodo.derecha)
        
        # Operadores aritméticos
        if nodo.operador in ('+', '-', '*', '/'):
            # Concatenación de cadenas con +
            if nodo.operador == '+' and tipo_izq == 'cadena' and tipo_der == 'cadena':
                return 'cadena'
            
            # Operaciones numéricas
            if tipo_izq in ('int', 'float', 'numero') and tipo_der in ('int', 'float', 'numero'):
                # El resultado es float si cualquier operando es float
                if tipo_izq == 'float' or tipo_der == 'float':
                    return 'float'
                return 'int'
            
            # Error de tipo
            self.error(
                f"Incompatibilidad de tipos en operación: {tipo_izq} {nodo.operador} {tipo_der}",
                nodo.linea
            )
            return 'error'
        
        # Operadores de comparación
        elif nodo.operador in ('==', '!=', '<', '>', '<=', '>='):
            # Se pueden comparar tipos iguales
            if tipo_izq == tipo_der:
                return 'bool'
            # Se pueden comparar tipos numéricos
            if tipo_izq in ('int', 'float', 'numero') and tipo_der in ('int', 'float', 'numero'):
                return 'bool'
            
            self.advertencia(
                f"Comparando tipos diferentes: {tipo_izq} {nodo.operador} {tipo_der}",
                nodo.linea
            )
            return 'bool'
        
        return 'desconocido'
    
    def visitar_NodoOperacionUnaria(self, nodo):
        """Visitar operación unaria"""
        tipo_operando = self.visitar(nodo.operando)
        
        if nodo.operador == '-':
            if tipo_operando in ('int', 'float', 'numero'):
                return tipo_operando
            else:
                self.error(f"No se puede negar tipo no numérico: {tipo_operando}", nodo.linea)
                return 'error'
        
        return 'desconocido'
    
    def visitar_NodoNumero(self, nodo):
        """
        Acción Semántica: Retornar tipo numérico
        """
        if isinstance(nodo.valor, float):
            return 'float'
        return 'int'
    
    def visitar_NodoCadena(self, nodo):
        """
        Acción Semántica: Retornar tipo cadena
        """
        return 'cadena'
    
    def visitar_NodoIdentificador(self, nodo):
        """
        Acción Semántica: Verificar que variable esté declarada, retornar su tipo
        """
        simbolo = self.ambito_actual.buscar(nodo.nombre)
        
        if simbolo is None:
            self.error(f"Variable no definida: '{nodo.nombre}'", nodo.linea)
            return 'error'
        
        if not simbolo['inicializada']:
            self.advertencia(f"La variable '{nodo.nombre}' puede no estar inicializada", nodo.linea)
        
        return simbolo['tipo']
    
    def visitar_NodoBloque(self, nodo):
        """Visitar bloque de sentencias"""
        for sentencia in nodo.sentencias:
            self.visitar(sentencia)
        return None
    
    def obtener_tabla_simbolos(self):
        """Obtener la tabla de símbolos global para mostrar"""
        return self.ambito_global.simbolos
