"""
IDE de MiniLang - Aplicación GUI Principal
IDE profesional con tema oscuro para el compilador MiniLang
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys

from analizador_lexico import AnalizadorLexico, ErrorLexico
from analizador_sintactico import AnalizadorSintactico, ErrorSintactico
from analizador_semantico import AnalizadorSemantico, ErrorSemantico
from generador_codigo import GeneradorCodigo
from reglas_semanticas import REGLAS_SEMANTICAS, obtener_reglas_por_fase, obtener_nombre_fase
from nodos_ast import (NodoPrograma, NodoAsignacion, NodoPrint, NodoIf, NodoWhile, NodoFor,
                       NodoOperacionBinaria, NodoOperacionUnaria, NodoNumero, NodoCadena,
                       NodoIdentificador, NodoBloque)


# Colores del tema oscuro
COLORES = {
    'fondo_oscuro': '#1e1e1e',
    'fondo_medio': '#252526',
    'fondo_claro': '#2d2d30',
    'texto_primario': '#d4d4d4',
    'texto_secundario': '#858585',
    'acento_azul': '#007acc',
    'acento_verde': '#4ec9b0',
    'acento_amarillo': '#dcdcaa',
    'acento_rojo': '#f48771',
    'acento_purpura': '#c586c0',
    'borde': '#3e3e42',
    'seleccion': '#264f78',
    'numero_linea': '#858585',
}


class IDEMiniLang:
    """Aplicación principal del IDE"""
    
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("IDE MiniLang - Compilador con Acciones Semánticas")
        self.raiz.geometry("1400x900")
        self.raiz.configure(bg=COLORES['fondo_oscuro'])
        
        # Resultados de compilación
        self.tokens = []
        self.ast = None
        self.analizador_semantico = None
        self.codigo_generado = []
        
        # Regla seleccionada para detalles
        self.regla_seleccionada = None
        
        self.configurar_interfaz()
        self.cargar_codigo_ejemplo()
    
    def configurar_interfaz(self):
        """Configurar la interfaz de usuario"""
        # Contenedor principal con padding
        contenedor_principal = tk.Frame(self.raiz, bg=COLORES['fondo_oscuro'])
        contenedor_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de herramientas superior
        self.crear_barra_herramientas(contenedor_principal)
        
        # Área de contenido principal (división horizontal)
        panel_contenido = tk.PanedWindow(
            contenedor_principal,
            orient=tk.HORIZONTAL,
            bg=COLORES['fondo_oscuro'],
            sashwidth=5,
            sashrelief=tk.RAISED
        )
        panel_contenido.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Panel izquierdo - Editor de código
        panel_izquierdo = self.crear_panel_editor(panel_contenido)
        panel_contenido.add(panel_izquierdo, width=600)
        
        # Panel derecho - Pestañas de salida
        panel_derecho = self.crear_panel_salida(panel_contenido)
        panel_contenido.add(panel_derecho, width=750)
        
        # Barra de estado
        self.crear_barra_estado(contenedor_principal)
    
    def crear_barra_herramientas(self, padre):
        """Crear barra de herramientas con botones de acción"""
        barra_herramientas = tk.Frame(padre, bg=COLORES['fondo_medio'], height=50)
        barra_herramientas.pack(fill=tk.X, pady=(0, 5))
        
        estilo_boton = {
            'bg': COLORES['acento_azul'],
            'fg': 'white',
            'font': ('Segoe UI', 10, 'bold'),
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        # Botón compilar
        btn_compilar = tk.Button(
            barra_herramientas,
            text="▶ Compilar",
            command=self.compilar_codigo,
            **estilo_boton
        )
        btn_compilar.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón limpiar
        btn_limpiar = tk.Button(
            barra_herramientas,
            text="🗑 Limpiar",
            command=self.limpiar_salida,
            bg=COLORES['fondo_claro'],
            fg=COLORES['texto_primario'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_limpiar.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón cargar ejemplo
        btn_ejemplo = tk.Button(
            barra_herramientas,
            text="📄 Ejemplo",
            command=self.cargar_codigo_ejemplo,
            bg=COLORES['fondo_claro'],
            fg=COLORES['texto_primario'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_ejemplo.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón guardar
        btn_guardar = tk.Button(
            barra_herramientas,
            text="💾 Guardar",
            command=self.guardar_codigo,
            bg=COLORES['fondo_claro'],
            fg=COLORES['texto_primario'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_guardar.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón abrir
        btn_abrir = tk.Button(
            barra_herramientas,
            text="📂 Abrir",
            command=self.abrir_archivo,
            bg=COLORES['fondo_claro'],
            fg=COLORES['texto_primario'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_abrir.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Etiqueta de título
        etiqueta_titulo = tk.Label(
            barra_herramientas,
            text="Compilador MiniLang IDE",
            bg=COLORES['fondo_medio'],
            fg=COLORES['acento_verde'],
            font=('Segoe UI', 12, 'bold')
        )
        etiqueta_titulo.pack(side=tk.RIGHT, padx=10)
    
    def crear_panel_editor(self, padre):
        """Crear panel del editor de código"""
        marco_editor = tk.Frame(padre, bg=COLORES['fondo_medio'])
        
        # Etiqueta del editor
        etiqueta = tk.Label(
            marco_editor,
            text="Editor de Código",
            bg=COLORES['fondo_medio'],
            fg=COLORES['acento_amarillo'],
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        )
        etiqueta.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Marco para números de línea
        marco_numeros = tk.Frame(marco_editor, bg=COLORES['fondo_claro'])
        marco_numeros.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=(0, 10))
        
        self.numeros_linea = tk.Text(
            marco_numeros,
            width=4,
            bg=COLORES['fondo_claro'],
            fg=COLORES['numero_linea'],
            font=('Consolas', 11),
            state='disabled',
            relief=tk.FLAT,
            padx=5
        )
        self.numeros_linea.pack(fill=tk.Y)
        
        # Editor de código
        self.editor_codigo = scrolledtext.ScrolledText(
            marco_editor,
            bg=COLORES['fondo_oscuro'],
            fg=COLORES['texto_primario'],
            insertbackground='white',
            font=('Consolas', 11),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.NONE,
            undo=True
        )
        self.editor_codigo.pack(fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 10))
        self.editor_codigo.bind('<KeyRelease>', self.actualizar_numeros_linea)
        self.editor_codigo.bind('<MouseWheel>', self.sincronizar_scroll)
        
        return marco_editor
    
    def crear_panel_salida(self, padre):
        """Crear panel de salida con pestañas"""
        marco_salida = tk.Frame(padre, bg=COLORES['fondo_medio'])
        
        # Crear notebook para pestañas
        estilo = ttk.Style()
        estilo.theme_use('default')
        estilo.configure(
            'Personalizado.TNotebook',
            background=COLORES['fondo_medio'],
            borderwidth=0
        )
        estilo.configure(
            'Personalizado.TNotebook.Tab',
            background=COLORES['fondo_claro'],
            foreground=COLORES['texto_primario'],
            padding=[20, 10],
            font=('Segoe UI', 10)
        )
        estilo.map(
            'Personalizado.TNotebook.Tab',
            background=[('selected', COLORES['acento_azul'])],
            foreground=[('selected', 'white')]
        )
        
        self.notebook = ttk.Notebook(marco_salida, style='Personalizado.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.crear_pestana_ejecucion()
        self.crear_pestana_tokens()
        self.crear_pestana_ast()
        self.crear_pestana_semantico()
        self.crear_pestana_codigo()
        self.crear_pestana_reglas()
        self.crear_pestana_gramatica()
        
        return marco_salida
    
    def crear_pestana_tokens(self):
        """Crear pestaña de salida de tokens"""
        pestana = tk.Frame(self.notebook, bg=COLORES['fondo_oscuro'])
        self.notebook.add(pestana, text="Tokens")
        
        self.texto_tokens = scrolledtext.ScrolledText(
            pestana,
            bg=COLORES['fondo_oscuro'],
            fg=COLORES['texto_primario'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.texto_tokens.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestana_ast(self):
        """Crear pestaña de salida del AST"""
        pestana = tk.Frame(self.notebook, bg=COLORES['fondo_oscuro'])
        self.notebook.add(pestana, text="AST")
        
        self.texto_ast = scrolledtext.ScrolledText(
            pestana,
            bg=COLORES['fondo_oscuro'],
            fg=COLORES['texto_primario'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.texto_ast.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestana_semantico(self):
        """Crear pestaña de análisis semántico"""
        pestana = tk.Frame(self.notebook, bg=COLORES['fondo_oscuro'])
        self.notebook.add(pestana, text="Análisis Semántico")
        
        self.texto_semantico = scrolledtext.ScrolledText(
            pestana,
            bg=COLORES['fondo_oscuro'],
            fg=COLORES['texto_primario'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.texto_semantico.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestana_codigo(self):
        """Crear pestaña de generación de código"""
        pestana = tk.Frame(self.notebook, bg=COLORES['fondo_oscuro'])
        self.notebook.add(pestana, text="Código Generado")
        
        self.texto_codigo = scrolledtext.ScrolledText(
            pestana,
            bg=COLORES['fondo_oscuro'],
            fg=COLORES['texto_primario'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.texto_codigo.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestana_ejecucion(self):
        """Crear pestaña de salida de ejecución"""
        pestana = tk.Frame(self.notebook, bg=COLORES['fondo_oscuro'])
        self.notebook.add(pestana, text="Salida de Ejecución")
        
        self.texto_ejecucion = scrolledtext.ScrolledText(
            pestana,
            bg=COLORES['fondo_oscuro'],
            fg=COLORES['texto_primario'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.texto_ejecucion.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestana_reglas(self):
        """Crear pestaña de reglas semánticas con tabla y detalles"""
        pestana = tk.Frame(self.notebook, bg=COLORES['fondo_oscuro'])
        self.notebook.add(pestana, text="Reglas Semánticas")
        
        # Selector de fase
        marco_fase = tk.Frame(pestana, bg=COLORES['fondo_medio'])
        marco_fase.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            marco_fase,
            text="Fase:",
            bg=COLORES['fondo_medio'],
            fg=COLORES['texto_primario'],
            font=('Segoe UI', 10, 'bold')
        ).pack(side=tk.LEFT, padx=5)
        
        self.variable_fase = tk.StringVar(value="lexico")
        fases = [
            ("Análisis Léxico", "lexico"),
            ("Análisis Sintáctico", "sintactico"),
            ("Análisis Semántico", "semantico"),
            ("Generación de Código", "codigo")
        ]
        
        for nombre_fase, valor_fase in fases:
            tk.Radiobutton(
                marco_fase,
                text=nombre_fase,
                variable=self.variable_fase,
                value=valor_fase,
                bg=COLORES['fondo_medio'],
                fg=COLORES['texto_primario'],
                selectcolor=COLORES['fondo_oscuro'],
                font=('Segoe UI', 9),
                command=self.actualizar_tabla_reglas
            ).pack(side=tk.LEFT, padx=5)
        
        # Panel dividido para tabla y detalles
        panel = tk.PanedWindow(pestana, orient=tk.VERTICAL, bg=COLORES['fondo_oscuro'], sashwidth=5)
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Marco de tabla de reglas
        marco_tabla = tk.Frame(panel, bg=COLORES['fondo_oscuro'])
        panel.add(marco_tabla, height=400)
        
        # Crear treeview para tabla de reglas
        self.crear_tabla_reglas(marco_tabla)
        
        # Marco de detalles
        marco_detalles = tk.Frame(panel, bg=COLORES['fondo_medio'])
        panel.add(marco_detalles, height=200)
        
        tk.Label(
            marco_detalles,
            text="Detalles de la Regla Seleccionada",
            bg=COLORES['fondo_medio'],
            fg=COLORES['acento_amarillo'],
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor='w', padx=10, pady=10)
        
        self.texto_detalles_regla = scrolledtext.ScrolledText(
            marco_detalles,
            bg=COLORES['fondo_oscuro'],
            fg=COLORES['texto_primario'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.texto_detalles_regla.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def crear_tabla_reglas(self, padre):
        """Crear tabla treeview para reglas semánticas"""
        # Barras de desplazamiento
        barra_v = tk.Scrollbar(padre, orient="vertical")
        barra_h = tk.Scrollbar(padre, orient="horizontal")
        
        # Treeview
        columnas = ('ID', 'Regla Gramatical', 'Producción', 'Acción Semántica')
        self.arbol_reglas = ttk.Treeview(
            padre,
            columns=columnas,
            show='headings',
            yscrollcommand=barra_v.set,
            xscrollcommand=barra_h.set,
            height=15
        )
        
        barra_v.config(command=self.arbol_reglas.yview)
        barra_h.config(command=self.arbol_reglas.xview)
        
        # Configurar columnas
        self.arbol_reglas.heading('ID', text='ID')
        self.arbol_reglas.heading('Regla Gramatical', text='Regla Gramatical')
        self.arbol_reglas.heading('Producción', text='Producción')
        self.arbol_reglas.heading('Acción Semántica', text='Acción Semántica')
        
        self.arbol_reglas.column('ID', width=50, anchor='center')
        self.arbol_reglas.column('Regla Gramatical', width=150)
        self.arbol_reglas.column('Producción', width=200)
        self.arbol_reglas.column('Acción Semántica', width=300)
        
        # Estilo
        estilo = ttk.Style()
        estilo.configure(
            'Treeview',
            background=COLORES['fondo_oscuro'],
            foreground=COLORES['texto_primario'],
            fieldbackground=COLORES['fondo_oscuro'],
            font=('Segoe UI', 9)
        )
        estilo.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        estilo.map('Treeview', background=[('selected', COLORES['seleccion'])])
        
        # Vincular evento de selección
        self.arbol_reglas.bind('<<TreeviewSelect>>', self.al_seleccionar_regla)
        
        # Empaquetar
        self.arbol_reglas.grid(row=0, column=0, sticky='nsew')
        barra_v.grid(row=0, column=1, sticky='ns')
        barra_h.grid(row=1, column=0, sticky='ew')
        
        padre.grid_rowconfigure(0, weight=1)
        padre.grid_columnconfigure(0, weight=1)
        
        # Cargar reglas iniciales
        self.actualizar_tabla_reglas()
    
    def crear_pestana_gramatica(self):
        """Crear pestaña de documentación de gramática"""
        pestana = tk.Frame(self.notebook, bg=COLORES['fondo_oscuro'])
        self.notebook.add(pestana, text="Gramática")
        
        texto_gramatica = scrolledtext.ScrolledText(
            pestana,
            bg=COLORES['fondo_oscuro'],
            fg=COLORES['texto_primario'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        texto_gramatica.pack(fill=tk.BOTH, expand=True)
        
        contenido_gramatica = """
GRAMÁTICA DE MINILANG
=====================

programa → declaraciones

declaraciones → declaracion declaraciones | ε

declaracion → asignacion 
            | condicional 
            | bucle 
            | sentencia_print

asignacion → ID '=' expresion

condicional → 'if' expresion ':' bloque
              ('elif' expresion ':' bloque)*
              ('else' ':' bloque)?

bucle_while → 'while' expresion ':' bloque

bucle_for → 'for' ID 'in' 'range' '(' expresion ')' ':' bloque

sentencia_print → 'print' '(' expresion ')'

expresion → termino (('+'|'-') termino)*

termino → factor (('*'|'/') factor)*

factor → NUMERO 
       | CADENA 
       | ID 
       | '(' expresion ')'
       | '-' factor

comparacion → expresion ('=='|'!='|'<'|'>'|'<='|'>=') expresion


TOKENS
======

Palabras Reservadas: print, if, elif, else, while, for, in, range, var

Identificadores: [a-zA-Z_][a-zA-Z0-9_]*

Números: [0-9]+(\.[0-9]+)?

Cadenas: "[^"]*" | '[^']*'

Operadores Aritméticos: + - * /

Operadores de Comparación: == != < > <= >=

Delimitadores: ( ) : , ;

Asignación: =

Especiales: NUEVA_LINEA, INDENTAR, DESINDENTAR, FIN_ARCHIVO
        """
        
        texto_gramatica.insert('1.0', contenido_gramatica)
        texto_gramatica.config(state='disabled')
    
    def crear_barra_estado(self, padre):
        """Crear barra de estado"""
        self.barra_estado = tk.Label(
            padre,
            text="Listo",
            bg=COLORES['acento_azul'],
            fg='white',
            font=('Segoe UI', 9),
            anchor='w',
            padx=10,
            pady=5
        )
        self.barra_estado.pack(fill=tk.X, side=tk.BOTTOM)
    
    def actualizar_numeros_linea(self, evento=None):
        """Actualizar números de línea en el editor"""
        lineas = self.editor_codigo.get('1.0', 'end-1c').split('\n')
        cadena_numeros_linea = '\n'.join(str(i) for i in range(1, len(lineas) + 1))
        
        self.numeros_linea.config(state='normal')
        self.numeros_linea.delete('1.0', 'end')
        self.numeros_linea.insert('1.0', cadena_numeros_linea)
        self.numeros_linea.config(state='disabled')
    
    def sincronizar_scroll(self, evento=None):
        """Sincronizar scroll de números de línea con editor"""
        self.numeros_linea.yview_moveto(self.editor_codigo.yview()[0])
    
    def actualizar_tabla_reglas(self):
        """Actualizar tabla de reglas según la fase seleccionada"""
        # Limpiar elementos existentes
        for item in self.arbol_reglas.get_children():
            self.arbol_reglas.delete(item)
        
        # Obtener reglas para la fase seleccionada
        fase = self.variable_fase.get()
        reglas = obtener_reglas_por_fase(fase)
        
        # Poblar tabla
        for regla in reglas:
            self.arbol_reglas.insert('', 'end', values=(
                regla.id_regla,
                regla.regla_gramatical,
                regla.produccion,
                regla.accion_semantica
            ))
    
    def al_seleccionar_regla(self, evento):
        """Manejar selección de regla en la tabla"""
        seleccion = self.arbol_reglas.selection()
        if not seleccion:
            return
        
        item = self.arbol_reglas.item(seleccion[0])
        id_regla = item['values'][0]
        
        # Encontrar regla
        for regla in REGLAS_SEMANTICAS:
            if regla.id_regla == id_regla:
                self.mostrar_detalles_regla(regla)
                break
    
    def mostrar_detalles_regla(self, regla):
        """Mostrar información detallada sobre la regla seleccionada"""
        detalles = f"""
ID: {regla.id_regla}
Fase: {obtener_nombre_fase(regla.fase)}

REGLA GRAMATICAL:
{regla.regla_gramatical}

PRODUCCIÓN:
{regla.produccion}

ACCIÓN SEMÁNTICA:
{regla.accion_semantica}

EJEMPLO:
{regla.ejemplo}
        """
        
        self.texto_detalles_regla.delete('1.0', 'end')
        self.texto_detalles_regla.insert('1.0', detalles.strip())
    
    def compilar_codigo(self):
        """Compilar el código en el editor"""
        codigo_fuente = self.editor_codigo.get('1.0', 'end-1c')
        
        if not codigo_fuente.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return
        
        self.barra_estado.config(text="Compilando...", bg=COLORES['acento_amarillo'], fg='black')
        self.raiz.update()
        
        try:
            # Análisis Léxico
            lexico = AnalizadorLexico(codigo_fuente)
            self.tokens = lexico.tokenizar()
            self.mostrar_tokens()
            
            # Análisis Sintáctico
            sintactico = AnalizadorSintactico(self.tokens)
            self.ast = sintactico.analizar()
            self.mostrar_ast()
            
            # Análisis Semántico
            self.analizador_semantico = AnalizadorSemantico()
            exito = self.analizador_semantico.analizar(self.ast)
            self.mostrar_analisis_semantico()
            
            if not exito:
                self.barra_estado.config(
                    text=f"Compilación completada con {len(self.analizador_semantico.errores)} errores semánticos",
                    bg=COLORES['acento_rojo']
                )
                return
            
            # Generación de Código
            generador = GeneradorCodigo()
            self.codigo_generado = generador.generar(self.ast)
            self.mostrar_codigo_generado()
            
            self.barra_estado.config(
                text="✓ Compilación exitosa",
                bg=COLORES['acento_verde'],
                fg='white'
            )
            
        except ErrorLexico as e:
            messagebox.showerror("Error Léxico", str(e))
            self.barra_estado.config(text="Error léxico", bg=COLORES['acento_rojo'])
        
        except ErrorSintactico as e:
            messagebox.showerror("Error Sintáctico", str(e))
            self.barra_estado.config(text="Error sintáctico", bg=COLORES['acento_rojo'])
        
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            self.barra_estado.config(text="Error", bg=COLORES['acento_rojo'])
    
    def mostrar_tokens(self):
        """Mostrar tokens en la pestaña de tokens"""
        self.texto_tokens.delete('1.0', 'end')
        
        salida = "ANÁLISIS LÉXICO - TOKENS\n"
        salida += "=" * 80 + "\n\n"
        salida += f"{'Tipo':<20} {'Valor':<20} {'Línea':<10} {'Columna':<10}\n"
        salida += "-" * 80 + "\n"
        
        for token in self.tokens:
            if token.tipo.name not in ('NUEVA_LINEA', 'FIN_ARCHIVO', 'INDENTAR', 'DESINDENTAR'):
                salida += f"{token.tipo.name:<20} {str(token.valor):<20} {token.linea:<10} {token.columna:<10}\n"
        
        salida += "\n" + "=" * 80 + "\n"
        salida += f"Total de tokens: {len([t for t in self.tokens if t.tipo.name not in ('NUEVA_LINEA', 'FIN_ARCHIVO', 'INDENTAR', 'DESINDENTAR')])}\n"
        
        self.texto_tokens.insert('1.0', salida)
    
    def mostrar_ast(self):
        """Mostrar AST en la pestaña de AST"""
        self.texto_ast.delete('1.0', 'end')
        
        salida = "ÁRBOL DE SINTAXIS ABSTRACTA (AST)\n"
        salida += "=" * 80 + "\n\n"
        salida += self.formatear_ast(self.ast, 0)
        
        self.texto_ast.insert('1.0', salida)
    
    def formatear_ast(self, nodo, indentacion):
        """Formatear nodo AST para mostrar"""
        cadena_indent = "  " * indentacion
        resultado = f"{cadena_indent}{nodo.__class__.__name__}\n"
        
        if isinstance(nodo, NodoPrograma):
            for sentencia in nodo.sentencias:
                resultado += self.formatear_ast(sentencia, indentacion + 1)
        
        elif isinstance(nodo, NodoAsignacion):
            resultado += f"{cadena_indent}  identificador: {nodo.identificador}\n"
            resultado += f"{cadena_indent}  expresion:\n"
            resultado += self.formatear_ast(nodo.expresion, indentacion + 2)
        
        elif isinstance(nodo, NodoPrint):
            resultado += f"{cadena_indent}  expresion:\n"
            resultado += self.formatear_ast(nodo.expresion, indentacion + 2)
        
        elif isinstance(nodo, NodoIf):
            resultado += f"{cadena_indent}  condicion:\n"
            resultado += self.formatear_ast(nodo.condicion, indentacion + 2)
            resultado += f"{cadena_indent}  entonces:\n"
            resultado += self.formatear_ast(nodo.bloque_entonces, indentacion + 2)
            if nodo.partes_elif:
                for i, (cond, bloque) in enumerate(nodo.partes_elif):
                    resultado += f"{cadena_indent}  elif {i+1}:\n"
                    resultado += self.formatear_ast(cond, indentacion + 2)
                    resultado += self.formatear_ast(bloque, indentacion + 2)
            if nodo.bloque_sino:
                resultado += f"{cadena_indent}  sino:\n"
                resultado += self.formatear_ast(nodo.bloque_sino, indentacion + 2)
        
        elif isinstance(nodo, NodoWhile):
            resultado += f"{cadena_indent}  condicion:\n"
            resultado += self.formatear_ast(nodo.condicion, indentacion + 2)
            resultado += f"{cadena_indent}  bloque:\n"
            resultado += self.formatear_ast(nodo.bloque, indentacion + 2)
        
        elif isinstance(nodo, NodoFor):
            resultado += f"{cadena_indent}  variable: {nodo.identificador}\n"
            resultado += f"{cadena_indent}  rango:\n"
            resultado += self.formatear_ast(nodo.expresion_rango, indentacion + 2)
            resultado += f"{cadena_indent}  bloque:\n"
            resultado += self.formatear_ast(nodo.bloque, indentacion + 2)
        
        elif isinstance(nodo, NodoOperacionBinaria):
            resultado += f"{cadena_indent}  operador: {nodo.operador}\n"
            resultado += f"{cadena_indent}  izquierda:\n"
            resultado += self.formatear_ast(nodo.izquierda, indentacion + 2)
            resultado += f"{cadena_indent}  derecha:\n"
            resultado += self.formatear_ast(nodo.derecha, indentacion + 2)
        
        elif isinstance(nodo, NodoOperacionUnaria):
            resultado += f"{cadena_indent}  operador: {nodo.operador}\n"
            resultado += f"{cadena_indent}  operando:\n"
            resultado += self.formatear_ast(nodo.operando, indentacion + 2)
        
        elif isinstance(nodo, NodoNumero):
            resultado += f"{cadena_indent}  valor: {nodo.valor}\n"
        
        elif isinstance(nodo, NodoCadena):
            resultado += f"{cadena_indent}  valor: \"{nodo.valor}\"\n"
        
        elif isinstance(nodo, NodoIdentificador):
            resultado += f"{cadena_indent}  nombre: {nodo.nombre}\n"
        
        elif isinstance(nodo, NodoBloque):
            for sentencia in nodo.sentencias:
                resultado += self.formatear_ast(sentencia, indentacion + 1)
        
        return resultado
    
    def mostrar_analisis_semantico(self):
        """Mostrar resultados del análisis semántico"""
        self.texto_semantico.delete('1.0', 'end')
        
        salida = "ANÁLISIS SEMÁNTICO\n"
        salida += "=" * 80 + "\n\n"
        
        # Tabla de símbolos
        salida += "TABLA DE SÍMBOLOS\n"
        salida += "-" * 80 + "\n"
        salida += f"{'Variable':<20} {'Tipo':<15} {'Inicializada':<15}\n"
        salida += "-" * 80 + "\n"
        
        simbolos = self.analizador_semantico.obtener_tabla_simbolos()
        for nombre, info in simbolos.items():
            salida += f"{nombre:<20} {info['tipo']:<15} {'Sí' if info['inicializada'] else 'No':<15}\n"
        
        salida += "\n"
        
        # Errores
        if self.analizador_semantico.errores:
            salida += "ERRORES SEMÁNTICOS\n"
            salida += "-" * 80 + "\n"
            for error in self.analizador_semantico.errores:
                salida += f"❌ {error}\n"
            salida += "\n"
        else:
            salida += "✓ No se encontraron errores semánticos\n"
        
        self.texto_semantico.insert('1.0', salida)
    
    def mostrar_codigo_generado(self):
        """Mostrar código generado"""
        self.texto_codigo.delete('1.0', 'end')
        
        salida = '\n'.join(self.codigo_generado)
        self.texto_codigo.insert('1.0', salida)
        
        # Ejecutar el código y mostrar salida
        self.ejecutar_codigo()
    
    def ejecutar_codigo(self):
        """Ejecutar el código generado y mostrar la salida"""
        self.texto_ejecucion.delete('1.0', 'end')
        
        salida = "SALIDA DEL CÓDIGO EJECUTADO\n"
        salida += "=" * 80 + "\n\n"
        
        # Variables para la ejecución
        variables = {}
        salida_prints = []
        salida_operaciones = []
        salida_condicionales = []
        
        try:
            # Ejecutar cada instrucción del código generado
            i = 0
            while i < len(self.codigo_generado):
                linea = self.codigo_generado[i].strip()
                
                # Saltar comentarios y líneas vacías
                if not linea or linea.startswith('#'):
                    i += 1
                    continue
                
                # Procesar PRINT
                if linea.startswith('PRINT '):
                    valor_a_imprimir = linea[6:].strip()
                    
                    # Evaluar la expresión o variable
                    if valor_a_imprimir in variables:
                        salida_prints.append(str(variables[valor_a_imprimir]))
                    elif valor_a_imprimir.startswith('"') and valor_a_imprimir.endswith('"'):
                        salida_prints.append(valor_a_imprimir[1:-1])
                    else:
                        try:
                            salida_prints.append(str(eval(valor_a_imprimir, {}, variables)))
                        except:
                            salida_prints.append(valor_a_imprimir)
                
                # Procesar asignaciones
                elif '=' in linea and not any(op in linea for op in ['==', '!=', '<=', '>=']):
                    partes = linea.split('=', 1)
                    var_nombre = partes[0].strip()
                    expresion = partes[1].strip()
                    
                    # Evaluar la expresión
                    try:
                        # Reemplazar variables temporales y normales por sus valores
                        expr_evaluada = expresion
                        for var in variables:
                            expr_evaluada = expr_evaluada.replace(var, str(variables[var]))
                        
                        # Eliminar comillas de cadenas
                        if expr_evaluada.startswith('"') and expr_evaluada.endswith('"'):
                            valor = expr_evaluada[1:-1]
                        else:
                            try:
                                valor = eval(expr_evaluada)
                            except:
                                valor = expr_evaluada
                        
                        variables[var_nombre] = valor
                        
                        # Registrar operaciones aritméticas (no temporales)
                        if not var_nombre.startswith('t') and any(op in expresion for op in ['+', '-', '*', '/']):
                            salida_operaciones.append(f"{var_nombre} = {valor}")
                    
                    except Exception as e:
                        pass
                
                # Procesar condicionales
                elif 'IF_FALSE' in linea:
                    # Extraer la condición
                    partes = linea.split('IF_FALSE')[1].split('GOTO')
                    condicion = partes[0].strip()
                    
                    try:
                        # Evaluar condición
                        cond_evaluada = condicion
                        for var in variables:
                            cond_evaluada = cond_evaluada.replace(var, str(variables[var]))
                        
                        resultado = eval(cond_evaluada)
                        salida_condicionales.append(f"Condición evaluada: {resultado}")
                    except:
                        pass
                
                i += 1
            
            # Mostrar VARIABLES
            if variables:
                salida += "VARIABLES:\n"
                salida += "-" * 80 + "\n"
                for var, valor in variables.items():
                    if not var.startswith('t'):  # No mostrar variables temporales
                        salida += f"{var} = {valor}\n"
                salida += "\n"
            
            # Mostrar OPERACIONES ARITMÉTICAS
            if salida_operaciones:
                salida += "OPERACIONES ARITMÉTICAS:\n"
                salida += "-" * 80 + "\n"
                for op in salida_operaciones:
                    salida += f"{op}\n"
                salida += "\n"
            
            # Mostrar SALIDA DE PRINT
            if salida_prints:
                salida += "SALIDA DE PRINT:\n"
                salida += "-" * 80 + "\n"
                for print_val in salida_prints:
                    salida += f"{print_val}\n"
                salida += "\n"
            
            # Mostrar RESULTADOS DE CONDICIONALES
            if salida_condicionales:
                salida += "RESULTADOS DE LAS CONDICIONALES:\n"
                salida += "-" * 80 + "\n"
                for cond in salida_condicionales:
                    salida += f"{cond}\n"
                salida += "\n"
            
            if not variables and not salida_prints and not salida_operaciones and not salida_condicionales:
                salida += "No hay salida que mostrar\n"
        
        except Exception as e:
            salida += f"Error durante la ejecución: {str(e)}\n"
        
        self.texto_ejecucion.insert('1.0', salida)
    
    def limpiar_salida(self):
        """Limpiar todas las pestañas de salida"""
        self.texto_tokens.delete('1.0', 'end')
        self.texto_ast.delete('1.0', 'end')
        self.texto_semantico.delete('1.0', 'end')
        self.texto_codigo.delete('1.0', 'end')
        self.texto_ejecucion.delete('1.0', 'end')
        self.barra_estado.config(text="Salida limpiada", bg=COLORES['acento_azul'], fg='white')
    
    def cargar_codigo_ejemplo(self):
        """Cargar código de ejemplo en el editor"""
        ejemplo = '''# Programa de ejemplo en MiniLang
nombre = "MiniLang"
x = 10
y = 5

# Operaciones aritméticas
suma = x + y
resta = x - y
multiplicacion = x * y
division = x / y

# Imprimir resultados
print("Bienvenido a MiniLang")
print("Operaciones con numeros")
print(suma)
print(resta)
print(multiplicacion)
print(division)

# Condicional
if x > y:
    print("x es mayor que y")
elif x < y:
    print("y es mayor que x")
else:
    print("x e y son iguales")

# Bucle for
for i in range(5):
    print(i)

# Bucle while
contador = 0
while contador < 3:
    print(contador)
    contador = contador + 1
'''
        self.editor_codigo.delete('1.0', 'end')
        self.editor_codigo.insert('1.0', ejemplo)
        self.actualizar_numeros_linea()
        self.barra_estado.config(text="Código de ejemplo cargado", bg=COLORES['acento_azul'], fg='white')
    
    def guardar_codigo(self):
        """Guardar código en archivo"""
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension=".ml",
            filetypes=[("Archivos MiniLang", "*.ml"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if ruta_archivo:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(self.editor_codigo.get('1.0', 'end-1c'))
            self.barra_estado.config(text=f"Guardado: {ruta_archivo}", bg=COLORES['acento_verde'], fg='white')
    
    def abrir_archivo(self):
        """Abrir código desde archivo"""
        ruta_archivo = filedialog.askopenfilename(
            filetypes=[("Archivos MiniLang", "*.ml"), ("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if ruta_archivo:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            self.editor_codigo.delete('1.0', 'end')
            self.editor_codigo.insert('1.0', contenido)
            self.actualizar_numeros_linea()
            self.barra_estado.config(text=f"Abierto: {ruta_archivo}", bg=COLORES['acento_azul'], fg='white')


def main():
    """Punto de entrada principal"""
    raiz = tk.Tk()
    aplicacion = IDEMiniLang(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
