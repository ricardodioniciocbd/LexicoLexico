"""
IDE Completo del Compilador de Python
Con fondo azul gradiente y todas las fases de compilación
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font as tkfont
from python_compiler import *
from semantic_analyzer import SemanticAnalyzer
from tac_generator import TACGenerator
from tac_optimizer import TACOptimizer
from tac_interpreter import TACInterpreter
from machine_code_generator import MachineCodeGenerator
from reglas_semanticas import REGLAS_SEMANTICAS, obtener_reglas_por_fase, obtener_nombre_fase


# Colores Dark Mode
COLORS = {
    'bg_gradient_start': '#1e1e1e',  # Negro suave
    'bg_gradient_end': '#2d2d30',    # Gris muy oscuro
    'bg_dark': '#1e1e1e',            # Negro suave
    'bg_medium': '#252526',          # Gris oscuro
    'bg_light': '#2d2d30',           # Gris medio-oscuro
    'bg_editor': '#1e1e1e',          # Negro para editor
    'fg_primary': '#d4d4d4',         # Gris claro
    'fg_secondary': '#858585',       # Gris medio
    'accent_cyan': '#4ec9b0',        # Verde-cyan suave
    'accent_green': '#4ec9b0',       # Verde-cyan
    'accent_yellow': '#dcdcaa',      # Amarillo suave
    'accent_red': '#f48771',         # Rojo suave
    'accent_purple': '#c586c0',      # Púrpura suave
    'border': '#3e3e42',             # Gris oscuro
    'selection': '#264f78',          # Azul oscuro selección
    'line_number': '#858585',        # Gris para números
    'button_hover': '#3e3e42',       # Gris para hover
}


class GradientFrame(tk.Canvas):
    """Frame con gradiente azul"""
    def __init__(self, parent, color1, color2, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)
    
    def _draw_gradient(self, event=None):
        """Dibuja el gradiente"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height
        
        # Convertir colores hex a RGB
        r1, g1, b1 = int(self.color1[1:3], 16), int(self.color1[3:5], 16), int(self.color1[5:7], 16)
        r2, g2, b2 = int(self.color2[1:3], 16), int(self.color2[3:5], 16), int(self.color2[5:7], 16)
        
        for i in range(limit):
            r = int(r1 + (r2 - r1) * i / limit)
            g = int(g1 + (g2 - g1) * i / limit)
            b = int(b1 + (b2 - b1) * i / limit)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)


class PythonCompilerIDE:
    """IDE Completo del Compilador"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Interactivo de Python - IDE Profesional")
        self.root.geometry("1700x950")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Datos de compilación
        self.tokens = []
        self.ast = None
        self.semantic_analyzer = None
        self.tac_instructions = []
        self.optimized_tac = []
        self.machine_code = []
        self.execution_output = ""
        
        self.setup_ui()
        self.load_fibonacci_example()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal con gradiente
        self.main_gradient = GradientFrame(
            self.root,
            COLORS['bg_gradient_start'],
            COLORS['bg_gradient_end'],
            highlightthickness=0
        )
        self.main_gradient.pack(fill=tk.BOTH, expand=True)
        
        # Contenedor principal
        main_container = tk.Frame(self.main_gradient, bg=COLORS['bg_dark'])
        self.main_gradient.create_window(0, 0, anchor='nw', window=main_container)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Barra de título personalizada
        self.create_custom_title(main_container)
        
        # Barra de herramientas
        self.create_toolbar(main_container)
        
        # Contenedor principal con editor y salidas
        content_paned = tk.PanedWindow(
            main_container,
            orient=tk.HORIZONTAL,
            bg=COLORS['bg_dark'],
            sashwidth=6,
            sashrelief=tk.RAISED,
            bd=0
        )
        content_paned.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Panel izquierdo - Editor
        left_panel = self.create_editor_panel(content_paned)
        content_paned.add(left_panel, width=750)
        
        # Panel derecho - Pestañas de salida
        right_panel = self.create_output_panel(content_paned)
        content_paned.add(right_panel, width=900)
        
        # Barra de estado
        self.create_status_bar(main_container)
    
    def create_custom_title(self, parent):
        """Crea barra de título personalizada"""
        title_frame = tk.Frame(parent, bg=COLORS['bg_medium'], height=70)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título principal
        title_font = tkfont.Font(family='Segoe UI', size=20, weight='bold')
        title_label = tk.Label(
            title_frame,
            text="🐍 Compilador Interactivo de Python",
            bg=COLORS['bg_medium'],
            fg=COLORS['fg_primary'],
            font=title_font,
            pady=10
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Subtítulo
        subtitle_font = tkfont.Font(family='Segoe UI', size=10)
        subtitle_label = tk.Label(
            title_frame,
            text="Análisis Completo: Léxico • Sintáctico • Semántico • TAC • Optimización • Código Máquina",
            bg=COLORS['bg_medium'],
            fg=COLORS['fg_secondary'],
            font=subtitle_font
        )
        subtitle_label.pack(side=tk.LEFT, padx=10)
    
    def create_toolbar(self, parent):
        """Crea la barra de herramientas"""
        toolbar = tk.Frame(parent, bg=COLORS['bg_light'], height=70)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        button_font = tkfont.Font(family='Segoe UI', size=11, weight='bold')
        
        # Botón Analizar (principal)
        btn_analyze = tk.Button(
            toolbar,
            text="▶ ANALIZAR",
            command=self.analyze_code,
            bg=COLORS['accent_cyan'],
            fg='#000000',
            font=button_font,
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground=COLORS['accent_green'],
            borderwidth=0
        )
        btn_analyze.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Separador
        sep = tk.Frame(toolbar, bg=COLORS['border'], width=2)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Label de ejemplos
        examples_label = tk.Label(
            toolbar,
            text="Ejemplos:",
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Segoe UI', size=10, weight='bold')
        )
        examples_label.pack(side=tk.LEFT, padx=10)
        
        # Radio buttons para ejemplos
        self.example_var = tk.StringVar(value="fibonacci")
        examples = [
            ("Fibonacci", "fibonacci"),
            ("Búsqueda", "busqueda"),
            ("Listas", "listas"),
            ("Con Errores", "errores")
        ]
        
        for label, value in examples:
            tk.Radiobutton(
                toolbar,
                text=label,
                variable=self.example_var,
                value=value,
                bg=COLORS['bg_light'],
                fg=COLORS['fg_primary'],
                selectcolor=COLORS['bg_dark'],
                font=tkfont.Font(family='Segoe UI', size=9),
                command=self.load_selected_example,
                activebackground=COLORS['button_hover'],
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=5)
        
        # Botón Limpiar
        btn_clear = tk.Button(
            toolbar,
            text="🗑 Limpiar",
            command=self.clear_output,
            bg=COLORS['bg_medium'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Segoe UI', size=10),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        btn_clear.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def create_editor_panel(self, parent):
        """Crea el panel del editor de código"""
        editor_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        
        # Etiqueta del editor
        label_frame = tk.Frame(editor_frame, bg=COLORS['bg_light'])
        label_frame.pack(fill=tk.X, padx=0, pady=0)
        
        label = tk.Label(
            label_frame,
            text=" 📝 Editor de Código Python",
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Segoe UI', size=12, weight='bold'),
            anchor='w',
            pady=8
        )
        label.pack(fill=tk.X, padx=15)
        
        # Frame para números de línea y editor
        editor_container = tk.Frame(editor_frame, bg=COLORS['bg_dark'])
        editor_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Números de línea
        self.line_numbers = tk.Text(
            editor_container,
            width=5,
            bg=COLORS['bg_light'],
            fg=COLORS['line_number'],
            font=tkfont.Font(family='Consolas', size=11),
            state='disabled',
            relief=tk.FLAT,
            padx=8
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor de código
        self.code_editor = scrolledtext.ScrolledText(
            editor_container,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            insertbackground='white',
            font=tkfont.Font(family='Consolas', size=11),
            relief=tk.FLAT,
            padx=15,
            pady=15,
            wrap=tk.NONE,
            undo=True,
            selectbackground=COLORS['selection']
        )
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)
        
        return editor_frame
    
    def create_output_panel(self, parent):
        """Crea el panel de salidas con pestañas"""
        output_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        
        # Configurar estilo del notebook
        self.style.configure(
            'Custom.TNotebook',
            background=COLORS['bg_medium'],
            borderwidth=0
        )
        self.style.configure(
            'Custom.TNotebook.Tab',
            background=COLORS['bg_light'],
            foreground=COLORS['fg_primary'],
            padding=[18, 10],
            font=('Segoe UI', 10, 'bold')
        )
        self.style.map(
            'Custom.TNotebook.Tab',
            background=[('selected', COLORS['accent_green'])],
            foreground=[('selected', '#000000')]
        )
        
        self.notebook = ttk.Notebook(output_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.create_lexical_tab()
        self.create_syntax_tab()
        self.create_semantic_tab()  # Nueva pestaña
        self.create_intermediate_code_tab()
        self.create_optimization_tab()
        self.create_machine_code_tab()  # Nueva pestaña
        self.create_execution_tab()
        self.create_semantic_rules_tab()  # Nueva pestaña
        self.create_grammar_tab()
        
        return output_frame
    
    def create_lexical_tab(self):
        """Crea la pestaña de Análisis Léxico"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="📋 Análisis Léxico")
        
        self.lexical_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.lexical_text.pack(fill=tk.BOTH, expand=True)
    
    def create_syntax_tab(self):
        """Crea la pestaña de Análisis Sintáctico"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="🌳 Análisis Sintáctico")
        
        self.syntax_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.syntax_text.pack(fill=tk.BOTH, expand=True)
    
    def create_semantic_tab(self):
        """Crea la pestaña de Análisis Semántico"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="🔍 Análisis Semántico")
        
        self.semantic_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.semantic_text.pack(fill=tk.BOTH, expand=True)
    
    def create_intermediate_code_tab(self):
        """Crea la pestaña de Código Intermedio"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="⚙️ Código TAC")
        
        self.intermediate_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.intermediate_text.pack(fill=tk.BOTH, expand=True)
    
    def create_optimization_tab(self):
        """Crea la pestaña de Optimización"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="🚀 Optimización")
        
        self.optimization_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.optimization_text.pack(fill=tk.BOTH, expand=True)
    
    def create_machine_code_tab(self):
        """Crea la pestaña de Código Máquina"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="💻 Código Máquina")
        
        self.machine_code_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.machine_code_text.pack(fill=tk.BOTH, expand=True)
    
    def create_execution_tab(self):
        """Crea la pestaña de Ejecución"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="▶️ Ejecución")
        
        self.execution_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['accent_green'],
            font=tkfont.Font(family='Consolas', size=12, weight='bold'),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.execution_text.pack(fill=tk.BOTH, expand=True)
    
    def create_semantic_rules_tab(self):
        """Crea la pestaña de Reglas Semánticas"""
        tab = tk.Frame(self.notebook, bg='#0a1929')
        self.notebook.add(tab, text="📚 Reglas Semánticas")
        
        # Crear notebook interno para las fases
        rules_notebook = ttk.Notebook(tab, style='Custom.TNotebook')
        rules_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear pestaña para cada fase
        for fase_id in ['lexico', 'sintactico', 'semantico', 'codigo']:
            fase_tab = tk.Frame(rules_notebook, bg=COLORS['bg_editor'])
            rules_notebook.add(fase_tab, text=obtener_nombre_fase(fase_id))
            
            rules_text = scrolledtext.ScrolledText(
                fase_tab,
                bg=COLORS['bg_editor'],
                fg=COLORS['fg_primary'],
                font=tkfont.Font(family='Consolas', size=9),
                relief=tk.FLAT,
                padx=15,
                pady=15,
                wrap=tk.WORD
            )
            rules_text.pack(fill=tk.BOTH, expand=True)
            
            # Llenar con reglas de la fase
            reglas = obtener_reglas_por_fase(fase_id)
            content = f"REGLAS SEMÁNTICAS - {obtener_nombre_fase(fase_id).upper()}\n"
            content += "=" * 100 + "\n\n"
            
            for i, regla in enumerate(reglas, 1):
                content += f"{i}. ID: {regla.id_regla}\n"
                content += f"   Regla Gramatical: {regla.regla_gramatical}\n"
                content += f"   Producción: {regla.produccion}\n"
                content += f"   Acción Semántica: {regla.accion_semantica}\n"
                content += f"   Ejemplo:\n   {regla.ejemplo}\n"
                content += "-" * 100 + "\n\n"
            
            rules_text.insert('1.0', content)
            rules_text.config(state='disabled')
    
    def create_grammar_tab(self):
        """Crea la pestaña de Gramática"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="📖 Gramática")
        
        grammar_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15,
            wrap=tk.WORD
        )
        grammar_text.pack(fill=tk.BOTH, expand=True)
        grammar_text.insert('1.0', self.get_grammar_content())
        grammar_text.config(state='disabled')
    
    def create_status_bar(self, parent):
        """Crea la barra de estado"""
        self.status_bar = tk.Label(
            parent,
            text="Listo para analizar código",
            bg=COLORS['accent_green'],
            fg='#000000',
            font=tkfont.Font(family='Segoe UI', size=10, weight='bold'),
            anchor='w',
            padx=15,
            pady=8
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
    
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
        
        self.status_bar.config(text="Analizando código...", bg=COLORS['accent_yellow'], fg='#000000')
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
            
            # Fase 3: Análisis Semántico
            self.semantic_analyzer = SemanticAnalyzer()
            self.semantic_analyzer.analyze(self.ast)
            self.display_semantic_analysis()
            
            # Verificar si hay errores semánticos
            if self.semantic_analyzer.errors:
                self.status_bar.config(
                    text=f"⚠️ Compilación completada con {len(self.semantic_analyzer.errors)} errores semánticos",
                    bg=COLORS['accent_red']
                )
                return
            
            # Fase 4: Generación de Código Intermedio
            self.tac_generator = TACGenerator()
            self.tac_instructions = self.tac_generator.generate(self.ast)
            self.display_intermediate_code()
            
            # Fase 5: Optimización
            optimizer = TACOptimizer()
            self.optimized_tac = optimizer.optimize(self.tac_instructions)
            self.display_optimization(optimizer)
            
            # Fase 6: Generación de Código Máquina
            machine_gen = MachineCodeGenerator()
            self.machine_code = machine_gen.generate(self.optimized_tac, self.tac_generator.function_params)
            self.display_machine_code()
            
            # Fase 7: Ejecución
            # Crear callback para entrada interactiva
            def get_user_input(prompt=""):
                """Callback para obtener entrada del usuario mediante diálogo"""
                from tkinter import simpledialog
                if prompt:
                    return simpledialog.askstring("Entrada", prompt, parent=self.root)
                else:
                    return simpledialog.askstring("Entrada", "Ingrese un valor:", parent=self.root) or "5"
            
            interpreter = TACInterpreter(input_callback=get_user_input)
            self.execution_output = interpreter.interpret(self.optimized_tac, self.tac_generator.function_params)
            self.display_execution()
            
            self.status_bar.config(
                text="✅ Análisis completado exitosamente",
                bg=COLORS['accent_green'],
                fg='#000000'
            )
            
        except LexerError as e:
            messagebox.showerror("Error Léxico", str(e))
            self.status_bar.config(text=f"❌ Error léxico", bg=COLORS['accent_red'])
        except ParserError as e:
            messagebox.showerror("Error Sintáctico", str(e))
            self.status_bar.config(text=f"❌ Error sintáctico", bg=COLORS['accent_red'])
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            self.status_bar.config(text=f"❌ Error", bg=COLORS['accent_red'])
    
    # Los métodos de display se continuarán en la siguiente parte...
    
    def display_lexical_analysis(self):
        """Muestra el análisis léxico"""
        self.lexical_text.delete('1.0', 'end')
        
        output = "ANÁLISIS LÉXICO\n"
        output += "=" * 120 + "\n\n"
        output += f"{'Token':<25} {'Tipo':<30} {'Línea':<15} {'Posición':<15}\n"
        output += "-" * 120 + "\n"
        
        for token in self.tokens:
            if token.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT'):
                value = str(token.value) if token.value is not None else ''
                output += f"{value:<25} {token.type.name:<30} {token.line:<15} {token.column:<15}\n"
        
        output += "\n" + "=" * 120 + "\n"
        output += f"Total de tokens: {len([t for t in self.tokens if t.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT')])}\n"
        
        self.lexical_text.insert('1.0', output)
    
    def display_syntax_analysis(self):
        """Muestra el análisis sintáctico"""
        self.syntax_text.delete('1.0', 'end')
        
        output = "ÁRBOL DE SINTAXIS ABSTRACTA (AST)\n"
        output += "=" * 120 + "\n\n"
        output += self.format_ast(self.ast, 0)
        
        self.syntax_text.insert('1.0', output)
    
    def format_ast(self, node, indent):
        """Formatea el AST"""
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
            result += f"{indent_str}│  └─ Expresiones ({len(node.expressions)}):\n"
            for i, expr in enumerate(node.expressions):
                result += f"{indent_str}│     [{i}]:\n"
                result += self.format_ast(expr, indent + 3)
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
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                result += self.format_ast(stmt, indent + 1)
        elif isinstance(node, FunctionNode):
            result += f"{indent_str}│  ├─ Nombre: {node.name}\n"
            result += f"{indent_str}│  ├─ Parámetros: {', '.join(node.parameters)}\n"
            result += f"{indent_str}│  └─ Cuerpo:\n"
            result += self.format_ast(node.body, indent + 2)
        elif isinstance(node, ReturnNode):
            if node.expression:
                result += f"{indent_str}│  └─ Expresión:\n"
                result += self.format_ast(node.expression, indent + 2)
            else:
                result += f"{indent_str}│  └─ (sin valor)\n"
        elif isinstance(node, DictNode):
            result += f"{indent_str}│  └─ Elementos: {len(node.items)}\n"
            for i, (key, value) in enumerate(node.items):
                result += f"{indent_str}│     ├─ [{i}] Clave:\n"
                result += self.format_ast(key, indent + 3)
                result += f"{indent_str}│     └─ Valor:\n"
                result += self.format_ast(value, indent + 3)
        elif isinstance(node, InputNode):
            if node.prompt:
                result += f"{indent_str}│  └─ Prompt:\n"
                result += self.format_ast(node.prompt, indent + 2)
            else:
                result += f"{indent_str}│  └─ (sin prompt)\n"
        
        return result
    
    def display_semantic_analysis(self):
        """Muestra el análisis semántico"""
        self.semantic_text.delete('1.0', 'end')
        output = self.semantic_analyzer.get_report()
        self.semantic_text.insert('1.0', output)
    
    def display_intermediate_code(self):
        """Muestra el código intermedio"""
        self.intermediate_text.delete('1.0', 'end')
        
        output = "CÓDIGO INTERMEDIO DE TRES DIRECCIONES (TAC)\n"
        output += "=" * 120 + "\n\n"
        
        for i, instr in enumerate(self.tac_instructions):
            output += f"{i:4d}: {str(instr)}\n"
        
        output += "\n" + "=" * 120 + "\n"
        output += f"Total de instrucciones: {len(self.tac_instructions)}\n"
        
        self.intermediate_text.insert('1.0', output)
    
    def display_optimization(self, optimizer):
        """Muestra el código optimizado"""
        self.optimization_text.delete('1.0', 'end')
        
        output = "CÓDIGO TAC OPTIMIZADO\n"
        output += "=" * 120 + "\n\n"
        
        for i, instr in enumerate(self.optimized_tac):
            output += f"{i:4d}: {str(instr)}\n"
        
        output += "\n" + "=" * 120 + "\n"
        output += f"Instrucciones originales: {len(self.tac_instructions)}\n"
        output += f"Instrucciones optimizadas: {len(self.optimized_tac)}\n"
        output += f"Reducción: {len(self.tac_instructions) - len(self.optimized_tac)} instrucciones\n\n"
        
        output += optimizer.get_optimizations_report()
        
        self.optimization_text.insert('1.0', output)
    
    def display_machine_code(self):
        """Muestra el código máquina"""
        self.machine_code_text.delete('1.0', 'end')
        
        output = "CÓDIGO ENSAMBLADOR GENERADO\n"
        output += "=" * 120 + "\n\n"
        output += '\n'.join(self.machine_code)
        
        self.machine_code_text.insert('1.0', output)
    
    def display_execution(self):
        """Muestra la salida de ejecución"""
        self.execution_text.delete('1.0', 'end')
        
        output = "SALIDA DE LA EJECUCIÓN\n"
        output += "=" * 120 + "\n\n"
        output += self.execution_output
        output += "\n\n" + "=" * 120 + "\n"
        
        self.execution_text.insert('1.0', output)
    
    def clear_output(self):
        """Limpia todas las salidas"""
        self.lexical_text.delete('1.0', 'end')
        self.syntax_text.delete('1.0', 'end')
        self.semantic_text.delete('1.0', 'end')
        self.intermediate_text.delete('1.0', 'end')
        self.optimization_text.delete('1.0', 'end')
        self.machine_code_text.delete('1.0', 'end')
        self.execution_text.delete('1.0', 'end')
        self.status_bar.config(text="Salidas limpiadas", bg=COLORS['accent_green'], fg='#000000')
    
    def load_selected_example(self):
        """Carga el ejemplo seleccionado"""
        example = self.example_var.get()
        if example == "fibonacci":
            self.load_fibonacci_example()
        elif example == "busqueda":
            self.load_search_example()
        elif example == "listas":
            self.load_list_processing_example()
        elif example == "errores":
            self.load_error_example()
    
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
        self.status_bar.config(text="Ejemplo de Fibonacci cargado", bg=COLORS['accent_green'], fg='#000000')
    
    def load_search_example(self):
        """Carga el ejemplo de búsqueda"""
        code = '''# Búsqueda en Arreglo
numeros = [10, 25, 30, 45, 50, 60, 75]
buscando = 45
encontrado = 0
posicion = 0

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
        self.status_bar.config(text="Ejemplo de búsqueda cargado", bg=COLORS['accent_green'], fg='#000000')
    
    def load_list_processing_example(self):
        """Carga el ejemplo de procesamiento de listas"""
        code = '''# Procesamiento de Listas
numeros = [10, 20, 30, 40, 50]
suma = 0
contador = 0

print("Números:")
for num in numeros:
    print(num)
    suma = suma + num
    contador = contador + 1

promedio = suma / contador

print("Suma total:")
print(suma)

print("Promedio:")
print(promedio)
'''
        self.code_editor.delete('1.0', 'end')
        self.code_editor.insert('1.0', code)
        self.update_line_numbers()
        self.status_bar.config(text="Ejemplo de procesamiento cargado", bg=COLORS['accent_green'], fg='#000000')
    
    def load_error_example(self):
        """Carga el ejemplo con errores"""
        code = '''# Ejemplo con ERRORES para demostración

# Error léxico: carácter inválido
# resultado = 5 @@ 3

# Error sintáctico: falta dos puntos
# if x > 0
#     print(x)

# Error semántico: variable no declarada
print(variable_no_declarada)

# Error semántico: tipos incompatibles
x = 5
y = "texto"
z = x + y  # No se puede sumar int con string

# Error semántico: división por cero
a = 10
b = 0
c = a / b

print("Este código tiene errores")
'''
        self.code_editor.delete('1.0', 'end')
        self.code_editor.insert('1.0', code)
        self.update_line_numbers()
        self.status_bar.config(text="Ejemplo con ERRORES cargado", bg=COLORS['accent_red'], fg='#ffffff')
    
    def get_grammar_content(self):
        """Retorna el contenido de la gramática"""
        return r"""GRAMÁTICA DEL COMPILADOR PYTHON (Subconjunto)
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


def main():
    """Punto de entrada principal"""
    root = tk.Tk()
    app = PythonCompilerIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()


"""
IDE Completo del Compilador de Python
Con fondo azul gradiente y todas las fases de compilación
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font as tkfont
from python_compiler import *
from semantic_analyzer import SemanticAnalyzer
from tac_generator import TACGenerator
from tac_optimizer import TACOptimizer
from tac_interpreter import TACInterpreter
from machine_code_generator import MachineCodeGenerator
from reglas_semanticas import REGLAS_SEMANTICAS, obtener_reglas_por_fase, obtener_nombre_fase


# Colores Dark Mode
COLORS = {
    'bg_gradient_start': '#1e1e1e',  # Negro suave
    'bg_gradient_end': '#2d2d30',    # Gris muy oscuro
    'bg_dark': '#1e1e1e',            # Negro suave
    'bg_medium': '#252526',          # Gris oscuro
    'bg_light': '#2d2d30',           # Gris medio-oscuro
    'bg_editor': '#1e1e1e',          # Negro para editor
    'fg_primary': '#d4d4d4',         # Gris claro
    'fg_secondary': '#858585',       # Gris medio
    'accent_cyan': '#4ec9b0',        # Verde-cyan suave
    'accent_green': '#4ec9b0',       # Verde-cyan
    'accent_yellow': '#dcdcaa',      # Amarillo suave
    'accent_red': '#f48771',         # Rojo suave
    'accent_purple': '#c586c0',      # Púrpura suave
    'border': '#3e3e42',             # Gris oscuro
    'selection': '#264f78',          # Azul oscuro selección
    'line_number': '#858585',        # Gris para números
    'button_hover': '#3e3e42',       # Gris para hover
}


class GradientFrame(tk.Canvas):
    """Frame con gradiente azul"""
    def __init__(self, parent, color1, color2, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)
    
    def _draw_gradient(self, event=None):
        """Dibuja el gradiente"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height
        
        # Convertir colores hex a RGB
        r1, g1, b1 = int(self.color1[1:3], 16), int(self.color1[3:5], 16), int(self.color1[5:7], 16)
        r2, g2, b2 = int(self.color2[1:3], 16), int(self.color2[3:5], 16), int(self.color2[5:7], 16)
        
        for i in range(limit):
            r = int(r1 + (r2 - r1) * i / limit)
            g = int(g1 + (g2 - g1) * i / limit)
            b = int(b1 + (b2 - b1) * i / limit)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)


class PythonCompilerIDE:
    """IDE Completo del Compilador"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador Interactivo de Python - IDE Profesional")
        self.root.geometry("1700x950")
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Datos de compilación
        self.tokens = []
        self.ast = None
        self.semantic_analyzer = None
        self.tac_instructions = []
        self.optimized_tac = []
        self.machine_code = []
        self.execution_output = ""
        
        self.setup_ui()
        self.load_fibonacci_example()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal con gradiente
        self.main_gradient = GradientFrame(
            self.root,
            COLORS['bg_gradient_start'],
            COLORS['bg_gradient_end'],
            highlightthickness=0
        )
        self.main_gradient.pack(fill=tk.BOTH, expand=True)
        
        # Contenedor principal
        main_container = tk.Frame(self.main_gradient, bg=COLORS['bg_dark'])
        self.main_gradient.create_window(0, 0, anchor='nw', window=main_container)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Barra de título personalizada
        self.create_custom_title(main_container)
        
        # Barra de herramientas
        self.create_toolbar(main_container)
        
        # Contenedor principal con editor y salidas
        content_paned = tk.PanedWindow(
            main_container,
            orient=tk.HORIZONTAL,
            bg=COLORS['bg_dark'],
            sashwidth=6,
            sashrelief=tk.RAISED,
            bd=0
        )
        content_paned.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Panel izquierdo - Editor
        left_panel = self.create_editor_panel(content_paned)
        content_paned.add(left_panel, width=750)
        
        # Panel derecho - Pestañas de salida
        right_panel = self.create_output_panel(content_paned)
        content_paned.add(right_panel, width=900)
        
        # Barra de estado
        self.create_status_bar(main_container)
    
    def create_custom_title(self, parent):
        """Crea barra de título personalizada"""
        title_frame = tk.Frame(parent, bg=COLORS['bg_medium'], height=70)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título principal
        title_font = tkfont.Font(family='Segoe UI', size=20, weight='bold')
        title_label = tk.Label(
            title_frame,
            text="🐍 Compilador Interactivo de Python",
            bg=COLORS['bg_medium'],
            fg=COLORS['fg_primary'],
            font=title_font,
            pady=10
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Subtítulo
        subtitle_font = tkfont.Font(family='Segoe UI', size=10)
        subtitle_label = tk.Label(
            title_frame,
            text="Análisis Completo: Léxico • Sintáctico • Semántico • TAC • Optimización • Código Máquina",
            bg=COLORS['bg_medium'],
            fg=COLORS['fg_secondary'],
            font=subtitle_font
        )
        subtitle_label.pack(side=tk.LEFT, padx=10)
    
    def create_toolbar(self, parent):
        """Crea la barra de herramientas"""
        toolbar = tk.Frame(parent, bg=COLORS['bg_light'], height=70)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        button_font = tkfont.Font(family='Segoe UI', size=11, weight='bold')
        
        # Botón Analizar (principal)
        btn_analyze = tk.Button(
            toolbar,
            text="▶ ANALIZAR",
            command=self.analyze_code,
            bg=COLORS['accent_cyan'],
            fg='#000000',
            font=button_font,
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground=COLORS['accent_green'],
            borderwidth=0
        )
        btn_analyze.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Separador
        sep = tk.Frame(toolbar, bg=COLORS['border'], width=2)
        sep.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Label de ejemplos
        examples_label = tk.Label(
            toolbar,
            text="Ejemplos:",
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Segoe UI', size=10, weight='bold')
        )
        examples_label.pack(side=tk.LEFT, padx=10)
        
        # Radio buttons para ejemplos
        self.example_var = tk.StringVar(value="fibonacci")
        examples = [
            ("Fibonacci", "fibonacci"),
            ("Búsqueda", "busqueda"),
            ("Listas", "listas"),
            ("Con Errores", "errores")
        ]
        
        for label, value in examples:
            tk.Radiobutton(
                toolbar,
                text=label,
                variable=self.example_var,
                value=value,
                bg=COLORS['bg_light'],
                fg=COLORS['fg_primary'],
                selectcolor=COLORS['bg_dark'],
                font=tkfont.Font(family='Segoe UI', size=9),
                command=self.load_selected_example,
                activebackground=COLORS['button_hover'],
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=5)
        
        # Botón Limpiar
        btn_clear = tk.Button(
            toolbar,
            text="🗑 Limpiar",
            command=self.clear_output,
            bg=COLORS['bg_medium'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Segoe UI', size=10),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        btn_clear.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def create_editor_panel(self, parent):
        """Crea el panel del editor de código"""
        editor_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        
        # Etiqueta del editor
        label_frame = tk.Frame(editor_frame, bg=COLORS['bg_light'])
        label_frame.pack(fill=tk.X, padx=0, pady=0)
        
        label = tk.Label(
            label_frame,
            text=" 📝 Editor de Código Python",
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Segoe UI', size=12, weight='bold'),
            anchor='w',
            pady=8
        )
        label.pack(fill=tk.X, padx=15)
        
        # Frame para números de línea y editor
        editor_container = tk.Frame(editor_frame, bg=COLORS['bg_dark'])
        editor_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Números de línea
        self.line_numbers = tk.Text(
            editor_container,
            width=5,
            bg=COLORS['bg_light'],
            fg=COLORS['line_number'],
            font=tkfont.Font(family='Consolas', size=11),
            state='disabled',
            relief=tk.FLAT,
            padx=8
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Editor de código
        self.code_editor = scrolledtext.ScrolledText(
            editor_container,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            insertbackground='white',
            font=tkfont.Font(family='Consolas', size=11),
            relief=tk.FLAT,
            padx=15,
            pady=15,
            wrap=tk.NONE,
            undo=True,
            selectbackground=COLORS['selection']
        )
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)
        
        return editor_frame
    
    def create_output_panel(self, parent):
        """Crea el panel de salidas con pestañas"""
        output_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        
        # Configurar estilo del notebook
        self.style.configure(
            'Custom.TNotebook',
            background=COLORS['bg_medium'],
            borderwidth=0
        )
        self.style.configure(
            'Custom.TNotebook.Tab',
            background=COLORS['bg_light'],
            foreground=COLORS['fg_primary'],
            padding=[18, 10],
            font=('Segoe UI', 10, 'bold')
        )
        self.style.map(
            'Custom.TNotebook.Tab',
            background=[('selected', COLORS['accent_green'])],
            foreground=[('selected', '#000000')]
        )
        
        self.notebook = ttk.Notebook(output_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.create_lexical_tab()
        self.create_syntax_tab()
        self.create_semantic_tab()  # Nueva pestaña
        self.create_intermediate_code_tab()
        self.create_optimization_tab()
        self.create_machine_code_tab()  # Nueva pestaña
        self.create_execution_tab()
        self.create_semantic_rules_tab()  # Nueva pestaña
        self.create_grammar_tab()
        
        return output_frame
    
    def create_lexical_tab(self):
        """Crea la pestaña de Análisis Léxico"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="📋 Análisis Léxico")
        
        self.lexical_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.lexical_text.pack(fill=tk.BOTH, expand=True)
    
    def create_syntax_tab(self):
        """Crea la pestaña de Análisis Sintáctico"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="🌳 Análisis Sintáctico")
        
        self.syntax_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.syntax_text.pack(fill=tk.BOTH, expand=True)
    
    def create_semantic_tab(self):
        """Crea la pestaña de Análisis Semántico"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="🔍 Análisis Semántico")
        
        self.semantic_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.semantic_text.pack(fill=tk.BOTH, expand=True)
    
    def create_intermediate_code_tab(self):
        """Crea la pestaña de Código Intermedio"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="⚙️ Código TAC")
        
        self.intermediate_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.intermediate_text.pack(fill=tk.BOTH, expand=True)
    
    def create_optimization_tab(self):
        """Crea la pestaña de Optimización"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="🚀 Optimización")
        
        self.optimization_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.optimization_text.pack(fill=tk.BOTH, expand=True)
    
    def create_machine_code_tab(self):
        """Crea la pestaña de Código Máquina"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="💻 Código Máquina")
        
        self.machine_code_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.machine_code_text.pack(fill=tk.BOTH, expand=True)
    
    def create_execution_tab(self):
        """Crea la pestaña de Ejecución"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="▶️ Ejecución")
        
        self.execution_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['accent_green'],
            font=tkfont.Font(family='Consolas', size=12, weight='bold'),
            relief=tk.FLAT,
            padx=15,
            pady=15
        )
        self.execution_text.pack(fill=tk.BOTH, expand=True)
    
    def create_semantic_rules_tab(self):
        """Crea la pestaña de Reglas Semánticas"""
        tab = tk.Frame(self.notebook, bg='#0a1929')
        self.notebook.add(tab, text="📚 Reglas Semánticas")
        
        # Crear notebook interno para las fases
        rules_notebook = ttk.Notebook(tab, style='Custom.TNotebook')
        rules_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear pestaña para cada fase
        for fase_id in ['lexico', 'sintactico', 'semantico', 'codigo']:
            fase_tab = tk.Frame(rules_notebook, bg=COLORS['bg_editor'])
            rules_notebook.add(fase_tab, text=obtener_nombre_fase(fase_id))
            
            rules_text = scrolledtext.ScrolledText(
                fase_tab,
                bg=COLORS['bg_editor'],
                fg=COLORS['fg_primary'],
                font=tkfont.Font(family='Consolas', size=9),
                relief=tk.FLAT,
                padx=15,
                pady=15,
                wrap=tk.WORD
            )
            rules_text.pack(fill=tk.BOTH, expand=True)
            
            # Llenar con reglas de la fase
            reglas = obtener_reglas_por_fase(fase_id)
            content = f"REGLAS SEMÁNTICAS - {obtener_nombre_fase(fase_id).upper()}\n"
            content += "=" * 100 + "\n\n"
            
            for i, regla in enumerate(reglas, 1):
                content += f"{i}. ID: {regla.id_regla}\n"
                content += f"   Regla Gramatical: {regla.regla_gramatical}\n"
                content += f"   Producción: {regla.produccion}\n"
                content += f"   Acción Semántica: {regla.accion_semantica}\n"
                content += f"   Ejemplo:\n   {regla.ejemplo}\n"
                content += "-" * 100 + "\n\n"
            
            rules_text.insert('1.0', content)
            rules_text.config(state='disabled')
    
    def create_grammar_tab(self):
        """Crea la pestaña de Gramática"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_editor'])
        self.notebook.add(tab, text="📖 Gramática")
        
        grammar_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_editor'],
            fg=COLORS['fg_primary'],
            font=tkfont.Font(family='Consolas', size=10),
            relief=tk.FLAT,
            padx=15,
            pady=15,
            wrap=tk.WORD
        )
        grammar_text.pack(fill=tk.BOTH, expand=True)
        grammar_text.insert('1.0', self.get_grammar_content())
        grammar_text.config(state='disabled')
    
    def create_status_bar(self, parent):
        """Crea la barra de estado"""
        self.status_bar = tk.Label(
            parent,
            text="Listo para analizar código",
            bg=COLORS['accent_green'],
            fg='#000000',
            font=tkfont.Font(family='Segoe UI', size=10, weight='bold'),
            anchor='w',
            padx=15,
            pady=8
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
    
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
        
        self.status_bar.config(text="Analizando código...", bg=COLORS['accent_yellow'], fg='#000000')
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
            
            # Fase 3: Análisis Semántico
            self.semantic_analyzer = SemanticAnalyzer()
            self.semantic_analyzer.analyze(self.ast)
            self.display_semantic_analysis()
            
            # Verificar si hay errores semánticos
            if self.semantic_analyzer.errors:
                self.status_bar.config(
                    text=f"⚠️ Compilación completada con {len(self.semantic_analyzer.errors)} errores semánticos",
                    bg=COLORS['accent_red']
                )
                return
            
            # Fase 4: Generación de Código Intermedio
            self.tac_generator = TACGenerator()
            self.tac_instructions = self.tac_generator.generate(self.ast)
            self.display_intermediate_code()
            
            # Fase 5: Optimización
            optimizer = TACOptimizer()
            self.optimized_tac = optimizer.optimize(self.tac_instructions)
            self.display_optimization(optimizer)
            
            # Fase 6: Generación de Código Máquina
            machine_gen = MachineCodeGenerator()
            self.machine_code = machine_gen.generate(self.optimized_tac, self.tac_generator.function_params)
            self.display_machine_code()
            
            # Fase 7: Ejecución
            # Crear callback para entrada interactiva
            def get_user_input(prompt=""):
                """Callback para obtener entrada del usuario mediante diálogo"""
                from tkinter import simpledialog
                if prompt:
                    return simpledialog.askstring("Entrada", prompt, parent=self.root)
                else:
                    return simpledialog.askstring("Entrada", "Ingrese un valor:", parent=self.root) or "5"
            
            interpreter = TACInterpreter(input_callback=get_user_input)
            self.execution_output = interpreter.interpret(self.optimized_tac, self.tac_generator.function_params)
            self.display_execution()
            
            self.status_bar.config(
                text="✅ Análisis completado exitosamente",
                bg=COLORS['accent_green'],
                fg='#000000'
            )
            
        except LexerError as e:
            messagebox.showerror("Error Léxico", str(e))
            self.status_bar.config(text=f"❌ Error léxico", bg=COLORS['accent_red'])
        except ParserError as e:
            messagebox.showerror("Error Sintáctico", str(e))
            self.status_bar.config(text=f"❌ Error sintáctico", bg=COLORS['accent_red'])
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            self.status_bar.config(text=f"❌ Error", bg=COLORS['accent_red'])
    
    # Los métodos de display se continuarán en la siguiente parte...
    
    def display_lexical_analysis(self):
        """Muestra el análisis léxico"""
        self.lexical_text.delete('1.0', 'end')
        
        output = "ANÁLISIS LÉXICO\n"
        output += "=" * 120 + "\n\n"
        output += f"{'Token':<25} {'Tipo':<30} {'Línea':<15} {'Posición':<15}\n"
        output += "-" * 120 + "\n"
        
        for token in self.tokens:
            if token.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT'):
                value = str(token.value) if token.value is not None else ''
                output += f"{value:<25} {token.type.name:<30} {token.line:<15} {token.column:<15}\n"
        
        output += "\n" + "=" * 120 + "\n"
        output += f"Total de tokens: {len([t for t in self.tokens if t.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT')])}\n"
        
        self.lexical_text.insert('1.0', output)
    
    def display_syntax_analysis(self):
        """Muestra el análisis sintáctico"""
        self.syntax_text.delete('1.0', 'end')
        
        output = "ÁRBOL DE SINTAXIS ABSTRACTA (AST)\n"
        output += "=" * 120 + "\n\n"
        output += self.format_ast(self.ast, 0)
        
        self.syntax_text.insert('1.0', output)
    
    def format_ast(self, node, indent):
        """Formatea el AST"""
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
            result += f"{indent_str}│  └─ Expresiones ({len(node.expressions)}):\n"
            for i, expr in enumerate(node.expressions):
                result += f"{indent_str}│     [{i}]:\n"
                result += self.format_ast(expr, indent + 3)
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
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                result += self.format_ast(stmt, indent + 1)
        
        return result
    
    def display_semantic_analysis(self):
        """Muestra el análisis semántico"""
        self.semantic_text.delete('1.0', 'end')
        output = self.semantic_analyzer.get_report()
        self.semantic_text.insert('1.0', output)
    
    def display_intermediate_code(self):
        """Muestra el código intermedio"""
        self.intermediate_text.delete('1.0', 'end')
        
        output = "CÓDIGO INTERMEDIO DE TRES DIRECCIONES (TAC)\n"
        output += "=" * 120 + "\n\n"
        
        for i, instr in enumerate(self.tac_instructions):
            output += f"{i:4d}: {str(instr)}\n"
        
        output += "\n" + "=" * 120 + "\n"
        output += f"Total de instrucciones: {len(self.tac_instructions)}\n"
        
        self.intermediate_text.insert('1.0', output)
    
    def display_optimization(self, optimizer):
        """Muestra el código optimizado"""
        self.optimization_text.delete('1.0', 'end')
        
        output = "CÓDIGO TAC OPTIMIZADO\n"
        output += "=" * 120 + "\n\n"
        
        for i, instr in enumerate(self.optimized_tac):
            output += f"{i:4d}: {str(instr)}\n"
        
        output += "\n" + "=" * 120 + "\n"
        output += f"Instrucciones originales: {len(self.tac_instructions)}\n"
        output += f"Instrucciones optimizadas: {len(self.optimized_tac)}\n"
        output += f"Reducción: {len(self.tac_instructions) - len(self.optimized_tac)} instrucciones\n\n"
        
        output += optimizer.get_optimizations_report()
        
        self.optimization_text.insert('1.0', output)
    
    def display_machine_code(self):
        """Muestra el código máquina"""
        self.machine_code_text.delete('1.0', 'end')
        
        output = "CÓDIGO ENSAMBLADOR GENERADO\n"
        output += "=" * 120 + "\n\n"
        output += '\n'.join(self.machine_code)
        
        self.machine_code_text.insert('1.0', output)
    
    def display_execution(self):
        """Muestra la salida de ejecución"""
        self.execution_text.delete('1.0', 'end')
        
        output = "SALIDA DE LA EJECUCIÓN\n"
        output += "=" * 120 + "\n\n"
        output += self.execution_output
        output += "\n\n" + "=" * 120 + "\n"
        
        self.execution_text.insert('1.0', output)
    
    def clear_output(self):
        """Limpia todas las salidas"""
        self.lexical_text.delete('1.0', 'end')
        self.syntax_text.delete('1.0', 'end')
        self.semantic_text.delete('1.0', 'end')
        self.intermediate_text.delete('1.0', 'end')
        self.optimization_text.delete('1.0', 'end')
        self.machine_code_text.delete('1.0', 'end')
        self.execution_text.delete('1.0', 'end')
        self.status_bar.config(text="Salidas limpiadas", bg=COLORS['accent_green'], fg='#000000')
    
    def load_selected_example(self):
        """Carga el ejemplo seleccionado"""
        example = self.example_var.get()
        if example == "fibonacci":
            self.load_fibonacci_example()
        elif example == "busqueda":
            self.load_search_example()
        elif example == "listas":
            self.load_list_processing_example()
        elif example == "errores":
            self.load_error_example()
    
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
        self.status_bar.config(text="Ejemplo de Fibonacci cargado", bg=COLORS['accent_green'], fg='#000000')
    
    def load_search_example(self):
        """Carga el ejemplo de búsqueda"""
        code = '''# Búsqueda en Arreglo
numeros = [10, 25, 30, 45, 50, 60, 75]
buscando = 45
encontrado = 0
posicion = 0

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
        self.status_bar.config(text="Ejemplo de búsqueda cargado", bg=COLORS['accent_green'], fg='#000000')
    
    def load_list_processing_example(self):
        """Carga el ejemplo de procesamiento de listas"""
        code = '''# Procesamiento de Listas
numeros = [10, 20, 30, 40, 50]
suma = 0
contador = 0

print("Números:")
for num in numeros:
    print(num)
    suma = suma + num
    contador = contador + 1

promedio = suma / contador

print("Suma total:")
print(suma)

print("Promedio:")
print(promedio)
'''
        self.code_editor.delete('1.0', 'end')
        self.code_editor.insert('1.0', code)
        self.update_line_numbers()
        self.status_bar.config(text="Ejemplo de procesamiento cargado", bg=COLORS['accent_green'], fg='#000000')
    
    def load_error_example(self):
        """Carga el ejemplo con errores"""
        code = '''# Ejemplo con ERRORES para demostración

# Error léxico: carácter inválido
# resultado = 5 @@ 3

# Error sintáctico: falta dos puntos
# if x > 0
#     print(x)

# Error semántico: variable no declarada
print(variable_no_declarada)

# Error semántico: tipos incompatibles
x = 5
y = "texto"
z = x + y  # No se puede sumar int con string

# Error semántico: división por cero
a = 10
b = 0
c = a / b

print("Este código tiene errores")
'''
        self.code_editor.delete('1.0', 'end')
        self.code_editor.insert('1.0', code)
        self.update_line_numbers()
        self.status_bar.config(text="Ejemplo con ERRORES cargado", bg=COLORS['accent_red'], fg='#ffffff')
    
    def get_grammar_content(self):
        """Retorna el contenido de la gramática"""
        return r"""GRAMÁTICA DEL COMPILADOR PYTHON (Subconjunto)
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


def main():
    """Punto de entrada principal"""
    root = tk.Tk()
    app = PythonCompilerIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()

