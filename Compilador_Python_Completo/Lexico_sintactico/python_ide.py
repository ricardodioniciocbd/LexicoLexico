"""
IDE Interactivo para Compilador de Python
Interfaz gráfica completa con todas las fases de compilación
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from python_compiler import *
from tac_generator import TACGenerator
from tac_optimizer import TACOptimizer
from tac_interpreter import TACInterpreter


# Colores del tema oscuro
COLORS = {
    'bg_dark': '#1e1e1e',
    'bg_medium': '#252526',
    'bg_light': '#2d2d30',
    'fg_primary': '#d4d4d4',
    'fg_secondary': '#858585',
    'accent_blue': '#007acc',
    'accent_green': '#4ec9b0',
    'accent_yellow': '#dcdcaa',
    'accent_red': '#f48771',
    'accent_purple': '#c586c0',
    'border': '#3e3e42',
    'selection': '#264f78',
    'line_number': '#858585',
}


class PythonCompilerIDE:
    """IDE para el compilador de Python"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Interactivo de Python - IDE Completo")
        self.root.geometry("1600x900")
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Datos de compilación
        self.tokens = []
        self.ast = None
        self.tac_instructions = []
        self.optimized_tac = []
        self.execution_output = ""
        
        self.setup_ui()
        self.load_fibonacci_example()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        main_container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra de herramientas
        self.create_toolbar(main_container)
        
        # Contenedor principal con editor y salidas
        content_paned = tk.PanedWindow(
            main_container,
            orient=tk.HORIZONTAL,
            bg=COLORS['bg_dark'],
            sashwidth=5,
            sashrelief=tk.RAISED
        )
        content_paned.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Panel izquierdo - Editor
        left_panel = self.create_editor_panel(content_paned)
        content_paned.add(left_panel, width=700)
        
        # Panel derecho - Pestañas de salida
        right_panel = self.create_output_panel(content_paned)
        content_paned.add(right_panel, width=850)
        
        # Barra de estado
        self.create_status_bar(main_container)
    
    def create_toolbar(self, parent):
        """Crea la barra de herramientas"""
        toolbar = tk.Frame(parent, bg=COLORS['bg_medium'], height=60)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        button_style = {
            'bg': COLORS['accent_blue'],
            'fg': 'white',
            'font': ('Segoe UI', 10, 'bold'),
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2'
        }
        
        # Botón Analizar
        btn_analyze = tk.Button(
            toolbar,
            text="▶ Analizar",
            command=self.analyze_code,
            **button_style
        )
        btn_analyze.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Selector de ejemplos
        tk.Label(
            toolbar,
            text="Ejemplos:",
            bg=COLORS['bg_medium'],
            fg=COLORS['fg_primary'],
            font=('Segoe UI', 10)
        ).pack(side=tk.LEFT, padx=(20, 5), pady=10)
        
        self.example_var = tk.StringVar(value="fibonacci")
        examples = [
            ("Fibonacci", "fibonacci"),
            ("Búsqueda en Arreglo", "busqueda"),
            ("Procesamiento de Listas", "listas")
        ]
        
        for label, value in examples:
            tk.Radiobutton(
                toolbar,
                text=label,
                variable=self.example_var,
                value=value,
                bg=COLORS['bg_medium'],
                fg=COLORS['fg_primary'],
                selectcolor=COLORS['bg_dark'],
                font=('Segoe UI', 9),
                command=self.load_selected_example
            ).pack(side=tk.LEFT, padx=5)
        
        # Botón Limpiar
        btn_clear = tk.Button(
            toolbar,
            text="🗑 Limpiar",
            command=self.clear_output,
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor='hand2'
        )
        btn_clear.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Título
        title_label = tk.Label(
            toolbar,
            text="Compilador Python - IDE Completo",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_green'],
            font=('Segoe UI', 13, 'bold')
        )
        title_label.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def create_editor_panel(self, parent):
        """Crea el panel del editor de código"""
        editor_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        
        # Etiqueta del editor
        label = tk.Label(
            editor_frame,
            text="Editor de Código Python",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_yellow'],
            font=('Segoe UI', 12, 'bold'),
            anchor='w'
        )
        label.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Frame para números de línea y editor
        editor_container = tk.Frame(editor_frame, bg=COLORS['bg_dark'])
        editor_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Números de línea
        self.line_numbers = tk.Text(
            editor_container,
            width=4,
            bg=COLORS['bg_light'],
            fg=COLORS['line_number'],
            font=('Consolas', 11),
            state='disabled',
            relief=tk.FLAT,
            padx=5
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor de código
        self.code_editor = scrolledtext.ScrolledText(
            editor_container,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            insertbackground='white',
            font=('Consolas', 11),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.NONE,
            undo=True
        )
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)
        
        return editor_frame
    
    def create_output_panel(self, parent):
        """Crea el panel de salidas con pestañas"""
        output_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        
        # Configurar estilo del notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'Custom.TNotebook',
            background=COLORS['bg_medium'],
            borderwidth=0
        )
        style.configure(
            'Custom.TNotebook.Tab',
            background=COLORS['bg_light'],
            foreground=COLORS['fg_primary'],
            padding=[20, 10],
            font=('Segoe UI', 10)
        )
        style.map(
            'Custom.TNotebook.Tab',
            background=[('selected', COLORS['accent_blue'])],
            foreground=[('selected', 'white')]
        )
        
        self.notebook = ttk.Notebook(output_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.create_lexical_tab()
        self.create_syntax_tab()
        self.create_intermediate_code_tab()
        self.create_optimization_tab()
        self.create_execution_tab()
        self.create_rules_tab()
        
        return output_frame
    
    def create_lexical_tab(self):
        """Crea la pestaña de Análisis Léxico"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Análisis Léxico")
        
        self.lexical_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.lexical_text.pack(fill=tk.BOTH, expand=True)
    
    def create_syntax_tab(self):
        """Crea la pestaña de Análisis Sintáctico"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Análisis Sintáctico")
        
        self.syntax_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.syntax_text.pack(fill=tk.BOTH, expand=True)
    
    def create_intermediate_code_tab(self):
        """Crea la pestaña de Código Intermedio"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Código Intermedio (TAC)")
        
        self.intermediate_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.intermediate_text.pack(fill=tk.BOTH, expand=True)
    
    def create_optimization_tab(self):
        """Crea la pestaña de Optimización"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Optimización de Código")
        
        self.optimization_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.optimization_text.pack(fill=tk.BOTH, expand=True)
    
    def create_execution_tab(self):
        """Crea la pestaña de Ejecución"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Salida de Ejecución")
        
        self.execution_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 11),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.execution_text.pack(fill=tk.BOTH, expand=True)
    
    def create_rules_tab(self):
        """Crea la pestaña de Reglas"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Reglas y Gramática")
        
        # Crear notebook interno para reglas
        rules_notebook = ttk.Notebook(tab, style='Custom.TNotebook')
        rules_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña de Gramática
        grammar_tab = tk.Frame(rules_notebook, bg=COLORS['bg_dark'])
        rules_notebook.add(grammar_tab, text="Gramática")
        
        grammar_text = scrolledtext.ScrolledText(
            grammar_tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        grammar_text.pack(fill=tk.BOTH, expand=True)
        grammar_text.insert('1.0', self.get_grammar_rules())
        grammar_text.config(state='disabled')
        
        # Pestaña de Optimizaciones
        opt_rules_tab = tk.Frame(rules_notebook, bg=COLORS['bg_dark'])
        rules_notebook.add(opt_rules_tab, text="Reglas de Optimización")
        
        opt_rules_text = scrolledtext.ScrolledText(
            opt_rules_tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        opt_rules_text.pack(fill=tk.BOTH, expand=True)
        opt_rules_text.insert('1.0', self.get_optimization_rules())
        opt_rules_text.config(state='disabled')
    
    def create_status_bar(self, parent):
        """Crea la barra de estado"""
        self.status_bar = tk.Label(
            parent,
            text="Listo",
            bg=COLORS['accent_blue'],
            fg='white',
            font=('Segoe UI', 9),
            anchor='w',
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def update_line_numbers(self, event=None):
        """Actualiza los números de línea"""
        lines = self.code_editor.get('1.0', 'end-1c').split('\n')
        line_numbers_string = '\n'.join(str(i) for i in range(1, len(lines) + 1))
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')
    
    def analyze_code(self):
        """Analiza el código fuente"""
        source_code = self.code_editor.get('1.0', 'end-1c')
        
        if not source_code.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return
        
        self.status_bar.config(text="Analizando...", bg=COLORS['accent_yellow'], fg='black')
        self.root.update()
        
        try:
            # Fase 1: Análisis Léxico
            lexer = Lexer(source_code)
            self.tokens = lexer.tokenize()
            self.display_lexical_analysis()
            
            # Fase 2: Análisis Sintáctico
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            self.display_syntax_analysis()
            
            # Fase 3: Generación de Código Intermedio
            tac_gen = TACGenerator()
            self.tac_instructions = tac_gen.generate(self.ast)
            self.display_intermediate_code()
            
            # Fase 4: Optimización
            optimizer = TACOptimizer()
            self.optimized_tac = optimizer.optimize(self.tac_instructions)
            self.display_optimization(optimizer)
            
            # Fase 5: Ejecución
            interpreter = TACInterpreter()
            self.execution_output = interpreter.interpret(self.optimized_tac)
            self.display_execution()
            
            self.status_bar.config(
                text="✓ Análisis completado exitosamente",
                bg=COLORS['accent_green'],
                fg='white'
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis:\n{str(e)}")
            self.status_bar.config(text="Error en el análisis", bg=COLORS['accent_red'])
    
    def display_lexical_analysis(self):
        """Muestra el análisis léxico"""
        self.lexical_text.delete('1.0', 'end')
        
        output = "ANÁLISIS LÉXICO\n"
        output += "=" * 100 + "\n\n"
        output += f"{'Token':<20} {'Tipo':<25} {'Línea':<10} {'Posición':<10}\n"
        output += "-" * 100 + "\n"
        
        for token in self.tokens:
            if token.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT'):
                value = str(token.value) if token.value is not None else ''
                output += f"{value:<20} {token.type.name:<25} {token.line:<10} {token.column:<10}\n"
        
        output += "\n" + "=" * 100 + "\n"
        output += f"Total de tokens: {len([t for t in self.tokens if t.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT')])}\n"
        
        self.lexical_text.insert('1.0', output)
    
    def display_syntax_analysis(self):
        """Muestra el análisis sintáctico (AST)"""
        self.syntax_text.delete('1.0', 'end')
        
        output = "ÁRBOL DE SINTAXIS ABSTRACTA (AST)\n"
        output += "=" * 100 + "\n\n"
        output += self.format_ast(self.ast, 0)
        
        self.syntax_text.insert('1.0', output)
    
    def format_ast(self, node, indent):
        """Formatea el AST para visualización"""
        indent_str = "  " * indent
        result = f"{indent_str}├─ {node.__class__.__name__}\n"
        
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                result += self.format_ast(stmt, indent + 1)
        elif isinstance(node, AssignmentNode):
            result += f"{indent_str}│  ├─ Variable: {node.identifier}\n"
            result += f"{indent_str}│  └─ Expresión:\n"
            result += self.format_ast(node.expression, indent + 2)
        elif isinstance(node, PrintNode):
            result += f"{indent_str}│  └─ Expresión:\n"
            result += self.format_ast(node.expression, indent + 2)
        elif isinstance(node, IfNode):
            result += f"{indent_str}│  ├─ Condición:\n"
            result += self.format_ast(node.condition, indent + 2)
            result += f"{indent_str}│  ├─ Bloque Then:\n"
            result += self.format_ast(node.then_block, indent + 2)
            if node.else_block:
                result += f"{indent_str}│  └─ Bloque Else:\n"
                result += self.format_ast(node.else_block, indent + 2)
        elif isinstance(node, WhileNode):
            result += f"{indent_str}│  ├─ Condición:\n"
            result += self.format_ast(node.condition, indent + 2)
            result += f"{indent_str}│  └─ Bloque:\n"
            result += self.format_ast(node.block, indent + 2)
        elif isinstance(node, ForNode):
            result += f"{indent_str}│  ├─ Variable: {node.identifier}\n"
            result += f"{indent_str}│  ├─ Iterable:\n"
            result += self.format_ast(node.iterable, indent + 2)
            result += f"{indent_str}│  └─ Bloque:\n"
            result += self.format_ast(node.block, indent + 2)
        elif isinstance(node, BinaryOpNode):
            result += f"{indent_str}│  ├─ Operador: {node.operator}\n"
            result += f"{indent_str}│  ├─ Izquierda:\n"
            result += self.format_ast(node.left, indent + 2)
            result += f"{indent_str}│  └─ Derecha:\n"
            result += self.format_ast(node.right, indent + 2)
        elif isinstance(node, NumberNode):
            result += f"{indent_str}│  └─ Valor: {node.value}\n"
        elif isinstance(node, StringNode):
            result += f"{indent_str}│  └─ Valor: \"{node.value}\"\n"
        elif isinstance(node, IdentifierNode):
            result += f"{indent_str}│  └─ Nombre: {node.name}\n"
        elif isinstance(node, ListNode):
            result += f"{indent_str}│  └─ Elementos: {len(node.elements)}\n"
            for elem in node.elements:
                result += self.format_ast(elem, indent + 2)
        elif isinstance(node, CallNode):
            result += f"{indent_str}│  ├─ Función: {node.function}\n"
            result += f"{indent_str}│  └─ Argumentos: {len(node.args)}\n"
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                result += self.format_ast(stmt, indent + 1)
        
        return result
    
    def display_intermediate_code(self):
        """Muestra el código intermedio (TAC)"""
        self.intermediate_text.delete('1.0', 'end')
        
        output = "CÓDIGO INTERMEDIO DE TRES DIRECCIONES (TAC)\n"
        output += "=" * 100 + "\n\n"
        
        for i, instr in enumerate(self.tac_instructions):
            output += f"{i:3d}: {str(instr)}\n"
        
        output += "\n" + "=" * 100 + "\n"
        output += f"Total de instrucciones: {len(self.tac_instructions)}\n"
        
        self.intermediate_text.insert('1.0', output)
    
    def display_optimization(self, optimizer):
        """Muestra el código optimizado"""
        self.optimization_text.delete('1.0', 'end')
        
        output = "CÓDIGO TAC OPTIMIZADO\n"
        output += "=" * 100 + "\n\n"
        
        for i, instr in enumerate(self.optimized_tac):
            output += f"{i:3d}: {str(instr)}\n"
        
        output += "\n" + "=" * 100 + "\n"
        output += f"Instrucciones originales: {len(self.tac_instructions)}\n"
        output += f"Instrucciones optimizadas: {len(self.optimized_tac)}\n"
        output += f"Reducción: {len(self.tac_instructions) - len(self.optimized_tac)} instrucciones\n\n"
        
        output += optimizer.get_optimizations_report()
        
        self.optimization_text.insert('1.0', output)
    
    def display_execution(self):
        """Muestra la salida de ejecución"""
        self.execution_text.delete('1.0', 'end')
        
        output = "SALIDA DE LA EJECUCIÓN\n"
        output += "=" * 100 + "\n\n"
        output += self.execution_output
        output += "\n\n" + "=" * 100 + "\n"
        
        self.execution_text.insert('1.0', output)
    
    def clear_output(self):
        """Limpia todas las salidas"""
        self.lexical_text.delete('1.0', 'end')
        self.syntax_text.delete('1.0', 'end')
        self.intermediate_text.delete('1.0', 'end')
        self.optimization_text.delete('1.0', 'end')
        self.execution_text.delete('1.0', 'end')
        self.status_bar.config(text="Salidas limpiadas", bg=COLORS['accent_blue'], fg='white')
    
    def load_selected_example(self):
        """Carga el ejemplo seleccionado"""
        example = self.example_var.get()
        if example == "fibonacci":
            self.load_fibonacci_example()
        elif example == "busqueda":
            self.load_search_example()
        elif example == "listas":
            self.load_list_processing_example()
    
    def load_fibonacci_example(self):
        """Carga el ejemplo de Fibonacci"""
        code = '''# Serie de Fibonacci
n = 10
a = 0
b = 1

print("Serie de Fibonacci:")
print(a)
print(b)

i = 2
while i < n:
    c = a + b
    print(c)
    a = b
    b = c
    i = i + 1
'''
        self.code_editor.delete('1.0', 'end')
        self.code_editor.insert('1.0', code)
        self.update_line_numbers()
        self.status_bar.config(text="Ejemplo de Fibonacci cargado", bg=COLORS['accent_blue'], fg='white')
    
    def load_search_example(self):
        """Carga el ejemplo de búsqueda en arreglo"""
        code = '''# Búsqueda en Arreglo
numeros = [10, 25, 30, 45, 50, 60, 75]
buscando = 45
encontrado = 0
posicion = 0

print("Arreglo:")
for num in numeros:
    print(num)

print("Buscando:")
print(buscando)

i = 0
while i < len(numeros):
    if numeros[i] == buscando:
        encontrado = 1
        posicion = i
    i = i + 1

if encontrado == 1:
    print("Encontrado en posición:")
    print(posicion)
else:
    print("No encontrado")
'''
        self.code_editor.delete('1.0', 'end')
        self.code_editor.insert('1.0', code)
        self.update_line_numbers()
        self.status_bar.config(text="Ejemplo de búsqueda cargado", bg=COLORS['accent_blue'], fg='white')
    
    def load_list_processing_example(self):
        """Carga el ejemplo de procesamiento de listas"""
        code = '''# Procesamiento de Listas
# Calcular suma y promedio de números

numeros = [10, 20, 30, 40, 50]
suma = 0
contador = 0

print("Números originales:")
for num in numeros:
    print(num)
    suma = suma + num
    contador = contador + 1

promedio = suma / contador

print("Suma total:")
print(suma)

print("Promedio:")
print(promedio)

# Crear lista de números pares
pares = []
for num in numeros:
    resto = num % 2
    if resto == 0:
        pares.append(num)

print("Números pares:")
for par in pares:
    print(par)
'''
        self.code_editor.delete('1.0', 'end')
        self.code_editor.insert('1.0', code)
        self.update_line_numbers()
        self.status_bar.config(text="Ejemplo de procesamiento de listas cargado", bg=COLORS['accent_blue'], fg='white')
    
    def get_grammar_rules(self):
        """Retorna las reglas gramaticales"""
        return """GRAMÁTICA DEL COMPILADOR PYTHON (Subconjunto)
================================================================================

PROGRAMA
--------
programa → sentencias

SENTENCIAS
----------
sentencias → sentencia sentencias | ε

sentencia → asignacion
          | impresion
          | condicional
          | bucle_while
          | bucle_for

ASIGNACIÓN
----------
asignacion → IDENTIFICADOR = expresion

IMPRESIÓN
---------
impresion → print ( expresion )

CONDICIONAL
-----------
condicional → if expresion : bloque
             (elif expresion : bloque)*
             (else : bloque)?

BUCLES
------
bucle_while → while expresion : bloque

bucle_for → for IDENTIFICADOR in iterable : bloque

iterable → range ( expresion )
         | IDENTIFICADOR
         | lista

BLOQUE
------
bloque → INDENT sentencias DEDENT

EXPRESIONES
-----------
expresion → comparacion

comparacion → aritmetica ((== | != | < | > | <= | >=) aritmetica)?

aritmetica → termino ((+ | -) termino)*

termino → factor ((* | / | %) factor)*

factor → NUMERO
       | STRING
       | IDENTIFICADOR
       | IDENTIFICADOR [ expresion ]
       | ( expresion )
       | - factor
       | llamada_funcion
       | lista

lista → [ elementos ]

elementos → expresion (, expresion)* | ε

llamada_funcion → IDENTIFICADOR ( argumentos )
                | IDENTIFICADOR . IDENTIFICADOR ( argumentos )

argumentos → expresion (, expresion)* | ε

TOKENS
======
Palabras Reservadas: def, return, if, elif, else, while, for, in, range, 
                     print, len, append, True, False, None

Identificadores: [a-zA-Z_][a-zA-Z0-9_]*

Números: [0-9]+(\.[0-9]+)?

Strings: "[^"]*" | '[^']*'

Operadores: + - * / % ** == != < > <= >=

Delimitadores: ( ) [ ] : , .

Asignación: =

Especiales: NEWLINE, INDENT, DEDENT, EOF
"""
    
    def get_optimization_rules(self):
        """Retorna las reglas de optimización"""
        return """REGLAS DE OPTIMIZACIÓN DEL COMPILADOR
================================================================================

1. PLEGADO DE CONSTANTES (Constant Folding)
--------------------------------------------
Descripción: Evalúa operaciones con constantes en tiempo de compilación.

Ejemplos:
  - 2 + 3 → 5
  - 10 * 5 → 50
  - 100 / 4 → 25

Beneficio: Reduce el tiempo de ejecución al precalcular valores constantes.


2. PROPAGACIÓN DE CONSTANTES (Constant Propagation)
----------------------------------------------------
Descripción: Reemplaza variables con sus valores constantes conocidos.

Ejemplos:
  - x = 5; y = x + 3 → x = 5; y = 8
  - a = 10; b = a * 2 → a = 10; b = 20

Beneficio: Permite aplicar más optimizaciones y reduce accesos a memoria.


3. ELIMINACIÓN DE CÓDIGO MUERTO (Dead Code Elimination)
--------------------------------------------------------
Descripción: Remueve instrucciones que no afectan el resultado del programa.

Ejemplos:
  - Variables temporales nunca usadas
  - Asignaciones a variables que no se leen después

Beneficio: Reduce el tamaño del código y mejora el rendimiento.


4. REDUCCIÓN DE FUERZA (Strength Reduction)
--------------------------------------------
Descripción: Reemplaza operaciones costosas por otras más eficientes.

Ejemplos:
  - x * 2 → x << 1 (desplazamiento de bits)
  - x / 4 → x >> 2 (desplazamiento de bits)
  - x * 0 → 0
  - x * 1 → x
  - x + 0 → x

Beneficio: Operaciones más rápidas en el procesador.


5. ELIMINACIÓN DE ASIGNACIONES REDUNDANTES
-------------------------------------------
Descripción: Remueve asignaciones de una variable a sí misma.

Ejemplos:
  - x = x (eliminado)

Beneficio: Reduce instrucciones innecesarias.


6. ELIMINACIÓN DE SALTOS INNECESARIOS
--------------------------------------
Descripción: Remueve saltos a la siguiente instrucción.

Ejemplos:
  - goto L1; L1: → L1: (sin el goto)

Beneficio: Mejora el flujo de control y reduce instrucciones.


ESTADÍSTICAS DE OPTIMIZACIÓN
=============================
El compilador muestra:
- Número de instrucciones antes y después
- Reducción en número de instrucciones
- Lista detallada de optimizaciones aplicadas

IMPACTO EN RENDIMIENTO
======================
Las optimizaciones pueden:
- Reducir el tamaño del código en 20-40%
- Mejorar el tiempo de ejecución en 15-30%
- Disminuir el uso de memoria temporal
"""


def main():
    """Punto de entrada principal"""
    root = tk.Tk()
    app = PythonCompilerIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()

