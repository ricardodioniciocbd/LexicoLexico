"""
Módulo de Generación de Código
Genera código intermedio o código destino desde el AST
"""

from nodos_ast import *


class GeneradorCodigo:
    """Genera código de tres direcciones desde el AST"""
    
    def __init__(self):
        self.codigo = []
        self.contador_temporal = 0
        self.contador_etiqueta = 0
    
    def nueva_temporal(self):
        """Generar una nueva variable temporal"""
        temp = f"t{self.contador_temporal}"
        self.contador_temporal += 1
        return temp
    
    def nueva_etiqueta(self):
        """Generar una nueva etiqueta"""
        etiqueta = f"L{self.contador_etiqueta}"
        self.contador_etiqueta += 1
        return etiqueta
    
    def emitir(self, instruccion):
        """Emitir una instrucción de código"""
        self.codigo.append(instruccion)
    
    def generar(self, ast):
        """Punto de entrada principal para generación de código"""
        self.visitar(ast)
        return self.codigo
    
    def visitar(self, nodo):
        """Despachar al método visitante apropiado"""
        nombre_metodo = f'visitar_{nodo.__class__.__name__}'
        visitante = getattr(self, nombre_metodo, self.visita_generica)
        return visitante(nodo)
    
    def visita_generica(self, nodo):
        """Visitante por defecto"""
        raise Exception(f'No hay método de visita para {nodo.__class__.__name__}')
    
    # Métodos visitantes
    
    def visitar_NodoPrograma(self, nodo):
        """Generar código para programa completo"""
        self.emitir("# Código Compilado de MiniLang")
        self.emitir("# Representación de Código de Tres Direcciones")
        self.emitir("")
        
        for sentencia in nodo.sentencias:
            self.visitar(sentencia)
        
        self.emitir("")
        self.emitir("# Fin del programa")
    
    def visitar_NodoAsignacion(self, nodo):
        """
        Acción Semántica: Generar código para evaluar expresión y almacenar en variable
        """
        # Generar código para expresión
        resultado_expr = self.visitar(nodo.expresion)
        
        # Almacenar resultado en variable
        self.emitir(f"{nodo.identificador} = {resultado_expr}")
        
        return nodo.identificador
    
    def visitar_NodoPrint(self, nodo):
        """
        Acción Semántica: Generar código para evaluar expresión e imprimir
        """
        resultado_expr = self.visitar(nodo.expresion)
        self.emitir(f"PRINT {resultado_expr}")
        return None
    
    def visitar_NodoIf(self, nodo):
        """
        Acción Semántica: Generar código de salto condicional
        """
        # Evaluar condición
        resultado_cond = self.visitar(nodo.condicion)
        
        # Etiquetas
        etiqueta_sino = self.nueva_etiqueta()
        etiqueta_fin = self.nueva_etiqueta()
        
        # Si la condición es falsa, saltar a else/fin
        if nodo.partes_elif or nodo.bloque_sino:
            self.emitir(f"IF_FALSE {resultado_cond} GOTO {etiqueta_sino}")
        else:
            self.emitir(f"IF_FALSE {resultado_cond} GOTO {etiqueta_fin}")
        
        # Bloque entonces
        for sentencia in nodo.bloque_entonces.sentencias:
            self.visitar(sentencia)
        
        # Saltar al fin después del bloque entonces
        if nodo.partes_elif or nodo.bloque_sino:
            self.emitir(f"GOTO {etiqueta_fin}")
        
        # Partes elif
        for i, (cond_elif, bloque_elif) in enumerate(nodo.partes_elif):
            self.emitir(f"{etiqueta_sino}:")
            resultado_cond = self.visitar(cond_elif)
            
            siguiente_etiqueta = self.nueva_etiqueta()
            self.emitir(f"IF_FALSE {resultado_cond} GOTO {siguiente_etiqueta}")
            
            for sentencia in bloque_elif.sentencias:
                self.visitar(sentencia)
            
            self.emitir(f"GOTO {etiqueta_fin}")
            etiqueta_sino = siguiente_etiqueta
        
        # Bloque else
        if nodo.bloque_sino:
            self.emitir(f"{etiqueta_sino}:")
            for sentencia in nodo.bloque_sino.sentencias:
                self.visitar(sentencia)
        
        # Etiqueta de fin
        self.emitir(f"{etiqueta_fin}:")
        return None
    
    def visitar_NodoWhile(self, nodo):
        """
        Acción Semántica: Generar bucle con verificación de condición y salto hacia atrás
        """
        etiqueta_inicio = self.nueva_etiqueta()
        etiqueta_fin = self.nueva_etiqueta()
        
        # Inicio del bucle
        self.emitir(f"{etiqueta_inicio}:")
        
        # Evaluar condición
        resultado_cond = self.visitar(nodo.condicion)
        self.emitir(f"IF_FALSE {resultado_cond} GOTO {etiqueta_fin}")
        
        # Cuerpo del bucle
        for sentencia in nodo.bloque.sentencias:
            self.visitar(sentencia)
        
        # Saltar de vuelta al inicio
        self.emitir(f"GOTO {etiqueta_inicio}")
        
        # Fin del bucle
        self.emitir(f"{etiqueta_fin}:")
        return None
    
    def visitar_NodoFor(self, nodo):
        """
        Acción Semántica: Generar inicialización de bucle, condición, incremento
        """
        # Inicializar variable de bucle
        resultado_rango = self.visitar(nodo.expresion_rango)
        self.emitir(f"{nodo.identificador} = 0")
        
        # Etiquetas
        etiqueta_inicio = self.nueva_etiqueta()
        etiqueta_fin = self.nueva_etiqueta()
        
        # Inicio del bucle
        self.emitir(f"{etiqueta_inicio}:")
        
        # Verificar condición
        temp = self.nueva_temporal()
        self.emitir(f"{temp} = {nodo.identificador} < {resultado_rango}")
        self.emitir(f"IF_FALSE {temp} GOTO {etiqueta_fin}")
        
        # Cuerpo del bucle
        for sentencia in nodo.bloque.sentencias:
            self.visitar(sentencia)
        
        # Incremento
        temp2 = self.nueva_temporal()
        self.emitir(f"{temp2} = {nodo.identificador} + 1")
        self.emitir(f"{nodo.identificador} = {temp2}")
        
        # Saltar de vuelta
        self.emitir(f"GOTO {etiqueta_inicio}")
        
        # Fin del bucle
        self.emitir(f"{etiqueta_fin}:")
        return None
    
    def visitar_NodoOperacionBinaria(self, nodo):
        """
        Acción Semántica: Generar código para operación binaria
        """
        resultado_izq = self.visitar(nodo.izquierda)
        resultado_der = self.visitar(nodo.derecha)
        
        temp = self.nueva_temporal()
        self.emitir(f"{temp} = {resultado_izq} {nodo.operador} {resultado_der}")
        
        return temp
    
    def visitar_NodoOperacionUnaria(self, nodo):
        """Generar código para operación unaria"""
        resultado_operando = self.visitar(nodo.operando)
        
        temp = self.nueva_temporal()
        self.emitir(f"{temp} = {nodo.operador}{resultado_operando}")
        
        return temp
    
    def visitar_NodoNumero(self, nodo):
        """Retornar literal numérico"""
        return str(nodo.valor)
    
    def visitar_NodoCadena(self, nodo):
        """Retornar literal de cadena"""
        return f'"{nodo.valor}"'
    
    def visitar_NodoIdentificador(self, nodo):
        """Retornar nombre de variable"""
        return nodo.nombre
    
    def visitar_NodoBloque(self, nodo):
        """Visitar sentencias del bloque"""
        for sentencia in nodo.sentencias:
            self.visitar(sentencia)
        return None
    
    def obtener_codigo_como_cadena(self):
        """Obtener código generado como cadena formateada"""
        return '\n'.join(self.codigo)
