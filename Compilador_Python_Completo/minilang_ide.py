"""
MiniLang IDE - Main GUI Application
Professional IDE with dark theme for MiniLang compiler
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sys

from lexer import Lexer, LexerError
from parser import Parser, ParserError
from semantic_analyzer import SemanticAnalyzer, SemanticError
from code_generator import CodeGenerator
from semantic_rules import SEMANTIC_RULES, get_rules_by_phase, get_phase_name


# Dark theme colors
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


class MiniLangIDE:
    """Main IDE application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MiniLang IDE - Compilador con Acciones Semánticas")
        self.root.geometry("1400x900")
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Compilation results
        self.tokens = []
        self.ast = None
        self.semantic_analyzer = None
        self.generated_code = []
        
        # Selected rule for details
        self.selected_rule = None
        
        self.setup_ui()
        self.load_example_code()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=COLORS['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top toolbar
        self.create_toolbar(main_container)
        
        # Main content area (horizontal split)
        content_paned = tk.PanedWindow(
            main_container,
            orient=tk.HORIZONTAL,
            bg=COLORS['bg_dark'],
            sashwidth=5,
            sashrelief=tk.RAISED
        )
        content_paned.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Left panel - Code editor
        left_panel = self.create_editor_panel(content_paned)
        content_paned.add(left_panel, width=600)
        
        # Right panel - Tabs for output
        right_panel = self.create_output_panel(content_paned)
        content_paned.add(right_panel, width=750)
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_toolbar(self, parent):
        """Create toolbar with action buttons"""
        toolbar = tk.Frame(parent, bg=COLORS['bg_medium'], height=50)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        button_style = {
            'bg': COLORS['accent_blue'],
            'fg': 'white',
            'font': ('Segoe UI', 10, 'bold'),
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 8,
            'cursor': 'hand2'
        }
        
        # Compile button
        btn_compile = tk.Button(
            toolbar,
            text="▶ Compilar",
            command=self.compile_code,
            **button_style
        )
        btn_compile.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Clear button
        btn_clear = tk.Button(
            toolbar,
            text="🗑 Limpiar",
            command=self.clear_output,
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Load example button
        btn_example = tk.Button(
            toolbar,
            text="📄 Ejemplo",
            command=self.load_example_code,
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_example.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Save button
        btn_save = tk.Button(
            toolbar,
            text="💾 Guardar",
            command=self.save_code,
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Open button
        btn_open = tk.Button(
            toolbar,
            text="📂 Abrir",
            command=self.open_file,
            bg=COLORS['bg_light'],
            fg=COLORS['fg_primary'],
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_open.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Title label
        title_label = tk.Label(
            toolbar,
            text="MiniLang Compiler IDE",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_green'],
            font=('Segoe UI', 12, 'bold')
        )
        title_label.pack(side=tk.RIGHT, padx=10)
    
    def create_editor_panel(self, parent):
        """Create code editor panel"""
        editor_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        
        # Editor label
        label = tk.Label(
            editor_frame,
            text="Editor de Código",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_yellow'],
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        )
        label.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Line numbers frame
        numbers_frame = tk.Frame(editor_frame, bg=COLORS['bg_light'])
        numbers_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=(0, 10))
        
        self.line_numbers = tk.Text(
            numbers_frame,
            width=4,
            bg=COLORS['bg_light'],
            fg=COLORS['line_number'],
            font=('Consolas', 11),
            state='disabled',
            relief=tk.FLAT,
            padx=5
        )
        self.line_numbers.pack(fill=tk.Y)
        
        # Code editor
        self.code_editor = scrolledtext.ScrolledText(
            editor_frame,
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
        self.code_editor.pack(fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 10))
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)
        self.code_editor.bind('<MouseWheel>', self.sync_scroll)
        
        return editor_frame
    
    def create_output_panel(self, parent):
        """Create output panel with tabs"""
        output_frame = tk.Frame(parent, bg=COLORS['bg_medium'])
        
        # Create notebook for tabs
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
        
        # Create tabs
        self.create_tokens_tab()
        self.create_ast_tab()
        self.create_semantic_tab()
        self.create_codegen_tab()
        self.create_rules_tab()
        self.create_grammar_tab()
        
        return output_frame
    
    def create_tokens_tab(self):
        """Create tokens output tab"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Tokens")
        
        self.tokens_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.tokens_text.pack(fill=tk.BOTH, expand=True)
    
    def create_ast_tab(self):
        """Create AST output tab"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="AST")
        
        self.ast_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.ast_text.pack(fill=tk.BOTH, expand=True)
    
    def create_semantic_tab(self):
        """Create semantic analysis tab"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Análisis Semántico")
        
        self.semantic_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.semantic_text.pack(fill=tk.BOTH, expand=True)
    
    def create_codegen_tab(self):
        """Create code generation tab"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Código Generado")
        
        self.codegen_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.codegen_text.pack(fill=tk.BOTH, expand=True)
    
    def create_rules_tab(self):
        """Create semantic rules tab with table and details"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Reglas Semánticas")
        
        # Phase selector
        phase_frame = tk.Frame(tab, bg=COLORS['bg_medium'])
        phase_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            phase_frame,
            text="Fase:",
            bg=COLORS['bg_medium'],
            fg=COLORS['fg_primary'],
            font=('Segoe UI', 10, 'bold')
        ).pack(side=tk.LEFT, padx=5)
        
        self.phase_var = tk.StringVar(value="lexer")
        phases = [
            ("Análisis Léxico", "lexer"),
            ("Análisis Sintáctico", "parser"),
            ("Análisis Semántico", "semantic"),
            ("Generación de Código", "codegen")
        ]
        
        for phase_name, phase_value in phases:
            tk.Radiobutton(
                phase_frame,
                text=phase_name,
                variable=self.phase_var,
                value=phase_value,
                bg=COLORS['bg_medium'],
                fg=COLORS['fg_primary'],
                selectcolor=COLORS['bg_dark'],
                font=('Segoe UI', 9),
                command=self.update_rules_table
            ).pack(side=tk.LEFT, padx=5)
        
        # Paned window for table and details
        paned = tk.PanedWindow(tab, orient=tk.VERTICAL, bg=COLORS['bg_dark'], sashwidth=5)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Rules table frame
        table_frame = tk.Frame(paned, bg=COLORS['bg_dark'])
        paned.add(table_frame, height=400)
        
        # Create treeview for rules table
        self.create_rules_table(table_frame)
        
        # Details frame
        details_frame = tk.Frame(paned, bg=COLORS['bg_medium'])
        paned.add(details_frame, height=200)
        
        tk.Label(
            details_frame,
            text="Detalles de la Regla Seleccionada",
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_yellow'],
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor='w', padx=10, pady=10)
        
        self.rule_details_text = scrolledtext.ScrolledText(
            details_frame,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.rule_details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def create_rules_table(self, parent):
        """Create treeview table for semantic rules"""
        # Scrollbars
        vsb = tk.Scrollbar(parent, orient="vertical")
        hsb = tk.Scrollbar(parent, orient="horizontal")
        
        # Treeview
        columns = ('ID', 'Regla Gramatical', 'Producción', 'Acción Semántica')
        self.rules_tree = ttk.Treeview(
            parent,
            columns=columns,
            show='headings',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            height=15
        )
        
        vsb.config(command=self.rules_tree.yview)
        hsb.config(command=self.rules_tree.xview)
        
        # Configure columns
        self.rules_tree.heading('ID', text='ID')
        self.rules_tree.heading('Regla Gramatical', text='Regla Gramatical')
        self.rules_tree.heading('Producción', text='Producción')
        self.rules_tree.heading('Acción Semántica', text='Acción Semántica')
        
        self.rules_tree.column('ID', width=50, anchor='center')
        self.rules_tree.column('Regla Gramatical', width=150)
        self.rules_tree.column('Producción', width=200)
        self.rules_tree.column('Acción Semántica', width=300)
        
        # Style
        style = ttk.Style()
        style.configure(
            'Treeview',
            background=COLORS['bg_dark'],
            foreground=COLORS['fg_primary'],
            fieldbackground=COLORS['bg_dark'],
            font=('Segoe UI', 9)
        )
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        style.map('Treeview', background=[('selected', COLORS['selection'])])
        
        # Bind selection event
        self.rules_tree.bind('<<TreeviewSelect>>', self.on_rule_selected)
        
        # Pack
        self.rules_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Load initial rules
        self.update_rules_table()
    
    def create_grammar_tab(self):
        """Create grammar documentation tab"""
        tab = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(tab, text="Gramática")
        
        grammar_text = scrolledtext.ScrolledText(
            tab,
            bg=COLORS['bg_dark'],
            fg=COLORS['fg_primary'],
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        grammar_text.pack(fill=tk.BOTH, expand=True)
        
        grammar_content = """
GRAMÁTICA DE MINILANG
=====================

programa → declaraciones

declaraciones → declaracion declaraciones | ε

declaracion → asignacion 
            | condicional 
            | bucle 
            | print_statement

asignacion → ID '=' expresion

condicional → 'if' expresion ':' bloque
              ('elif' expresion ':' bloque)*
              ('else' ':' bloque)?

bucle_while → 'while' expresion ':' bloque

bucle_for → 'for' ID 'in' 'range' '(' expresion ')' ':' bloque

print_statement → 'print' '(' expresion ')'

expresion → termino (('+'|'-') termino)*

termino → factor (('*'|'/') factor)*

factor → NUMERO 
       | STRING 
       | ID 
       | '(' expresion ')'
       | '-' factor

comparacion → expresion ('=='|'!='|'<'|'>'|'<='|'>=') expresion


TOKENS
======

Palabras Reservadas: print, if, elif, else, while, for, in, range, var

Identificadores: [a-zA-Z_][a-zA-Z0-9_]*

Números: [0-9]+(\.[0-9]+)?

Strings: "[^"]*" | '[^']*'

Operadores Aritméticos: + - * /

Operadores de Comparación: == != < > <= >=

Delimitadores: ( ) : , ;

Asignación: =

Especiales: NEWLINE, INDENT, DEDENT, EOF
        """
        
        grammar_text.insert('1.0', grammar_content)
        grammar_text.config(state='disabled')
    
    def create_status_bar(self, parent):
        """Create status bar"""
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
        """Update line numbers in editor"""
        lines = self.code_editor.get('1.0', 'end-1c').split('\n')
        line_numbers_string = '\n'.join(str(i) for i in range(1, len(lines) + 1))
        
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', line_numbers_string)
        self.line_numbers.config(state='disabled')
    
    def sync_scroll(self, event=None):
        """Sync line numbers scroll with editor"""
        self.line_numbers.yview_moveto(self.code_editor.yview()[0])
    
    def update_rules_table(self):
        """Update rules table based on selected phase"""
        # Clear existing items
        for item in self.rules_tree.get_children():
            self.rules_tree.delete(item)
        
        # Get rules for selected phase
        phase = self.phase_var.get()
        rules = get_rules_by_phase(phase)
        
        # Populate table
        for rule in rules:
            self.rules_tree.insert('', 'end', values=(
                rule.rule_id,
                rule.grammar_rule,
                rule.production,
                rule.semantic_action
            ))
    
    def on_rule_selected(self, event):
        """Handle rule selection in table"""
        selection = self.rules_tree.selection()
        if not selection:
            return
        
        item = self.rules_tree.item(selection[0])
        rule_id = item['values'][0]
        
        # Find rule
        for rule in SEMANTIC_RULES:
            if rule.rule_id == rule_id:
                self.show_rule_details(rule)
                break
    
    def show_rule_details(self, rule):
        """Show detailed information about selected rule"""
        details = f"""
ID: {rule.rule_id}
Fase: {get_phase_name(rule.phase)}

REGLA GRAMATICAL:
{rule.grammar_rule}

PRODUCCIÓN:
{rule.production}

ACCIÓN SEMÁNTICA:
{rule.semantic_action}

EJEMPLO:
{rule.example}
        """
        
        self.rule_details_text.delete('1.0', 'end')
        self.rule_details_text.insert('1.0', details.strip())
    
    def compile_code(self):
        """Compile the code in editor"""
        source_code = self.code_editor.get('1.0', 'end-1c')
        
        if not source_code.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío")
            return
        
        self.status_bar.config(text="Compilando...", bg=COLORS['accent_yellow'], fg='black')
        self.root.update()
        
        try:
            # Lexical Analysis
            lexer = Lexer(source_code)
            self.tokens = lexer.tokenize()
            self.display_tokens()
            
            # Syntax Analysis
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            self.display_ast()
            
            # Semantic Analysis
            self.semantic_analyzer = SemanticAnalyzer()
            success = self.semantic_analyzer.analyze(self.ast)
            self.display_semantic_analysis()
            
            if not success:
                self.status_bar.config(
                    text=f"Compilación completada con {len(self.semantic_analyzer.errors)} errores semánticos",
                    bg=COLORS['accent_red']
                )
                return
            
            # Code Generation
            code_gen = CodeGenerator()
            self.generated_code = code_gen.generate(self.ast)
            self.display_generated_code()
            
            self.status_bar.config(
                text="✓ Compilación exitosa",
                bg=COLORS['accent_green'],
                fg='white'
            )
            
        except LexerError as e:
            messagebox.showerror("Error Léxico", str(e))
            self.status_bar.config(text="Error léxico", bg=COLORS['accent_red'])
        
        except ParserError as e:
            messagebox.showerror("Error Sintáctico", str(e))
            self.status_bar.config(text="Error sintáctico", bg=COLORS['accent_red'])
        
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            self.status_bar.config(text="Error", bg=COLORS['accent_red'])
    
    def display_tokens(self):
        """Display tokens in tokens tab"""
        self.tokens_text.delete('1.0', 'end')
        
        output = "ANÁLISIS LÉXICO - TOKENS\n"
        output += "=" * 80 + "\n\n"
        output += f"{'Tipo':<20} {'Valor':<20} {'Línea':<10} {'Columna':<10}\n"
        output += "-" * 80 + "\n"
        
        for token in self.tokens:
            if token.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT'):
                output += f"{token.type.name:<20} {str(token.value):<20} {token.line:<10} {token.column:<10}\n"
        
        output += "\n" + "=" * 80 + "\n"
        output += f"Total de tokens: {len([t for t in self.tokens if t.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT')])}\n"
        
        self.tokens_text.insert('1.0', output)
    
    def display_ast(self):
        """Display AST in AST tab"""
        self.ast_text.delete('1.0', 'end')
        
        output = "ÁRBOL DE SINTAXIS ABSTRACTA (AST)\n"
        output += "=" * 80 + "\n\n"
        output += self.format_ast(self.ast, 0)
        
        self.ast_text.insert('1.0', output)
    
    def format_ast(self, node, indent):
        """Format AST node for display"""
        indent_str = "  " * indent
        result = f"{indent_str}{node.__class__.__name__}\n"
        
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                result += self.format_ast(stmt, indent + 1)
        
        elif isinstance(node, AssignmentNode):
            result += f"{indent_str}  identifier: {node.identifier}\n"
            result += f"{indent_str}  expression:\n"
            result += self.format_ast(node.expression, indent + 2)
        
        elif isinstance(node, PrintNode):
            result += f"{indent_str}  expression:\n"
            result += self.format_ast(node.expression, indent + 2)
        
        elif isinstance(node, IfNode):
            result += f"{indent_str}  condition:\n"
            result += self.format_ast(node.condition, indent + 2)
            result += f"{indent_str}  then:\n"
            result += self.format_ast(node.then_block, indent + 2)
            if node.elif_parts:
                for i, (cond, block) in enumerate(node.elif_parts):
                    result += f"{indent_str}  elif {i+1}:\n"
                    result += self.format_ast(cond, indent + 2)
                    result += self.format_ast(block, indent + 2)
            if node.else_block:
                result += f"{indent_str}  else:\n"
                result += self.format_ast(node.else_block, indent + 2)
        
        elif isinstance(node, WhileNode):
            result += f"{indent_str}  condition:\n"
            result += self.format_ast(node.condition, indent + 2)
            result += f"{indent_str}  block:\n"
            result += self.format_ast(node.block, indent + 2)
        
        elif isinstance(node, ForNode):
            result += f"{indent_str}  variable: {node.identifier}\n"
            result += f"{indent_str}  range:\n"
            result += self.format_ast(node.range_expr, indent + 2)
            result += f"{indent_str}  block:\n"
            result += self.format_ast(node.block, indent + 2)
        
        elif isinstance(node, BinaryOpNode):
            result += f"{indent_str}  operator: {node.operator}\n"
            result += f"{indent_str}  left:\n"
            result += self.format_ast(node.left, indent + 2)
            result += f"{indent_str}  right:\n"
            result += self.format_ast(node.right, indent + 2)
        
        elif isinstance(node, UnaryOpNode):
            result += f"{indent_str}  operator: {node.operator}\n"
            result += f"{indent_str}  operand:\n"
            result += self.format_ast(node.operand, indent + 2)
        
        elif isinstance(node, NumberNode):
            result += f"{indent_str}  value: {node.value}\n"
        
        elif isinstance(node, StringNode):
            result += f"{indent_str}  value: \"{node.value}\"\n"
        
        elif isinstance(node, IdentifierNode):
            result += f"{indent_str}  name: {node.name}\n"
        
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                result += self.format_ast(stmt, indent + 1)
        
        return result
    
    def display_semantic_analysis(self):
        """Display semantic analysis results"""
        self.semantic_text.delete('1.0', 'end')
        
        output = "ANÁLISIS SEMÁNTICO\n"
        output += "=" * 80 + "\n\n"
        
        # Symbol table
        output += "TABLA DE SÍMBOLOS\n"
        output += "-" * 80 + "\n"
        output += f"{'Variable':<20} {'Tipo':<15} {'Inicializada':<15}\n"
        output += "-" * 80 + "\n"
        
        symbols = self.semantic_analyzer.get_symbol_table()
        for name, info in symbols.items():
            output += f"{name:<20} {info['type']:<15} {'Sí' if info['initialized'] else 'No':<15}\n"
        
        output += "\n"
        
        # Errors
        if self.semantic_analyzer.errors:
            output += "ERRORES SEMÁNTICOS\n"
            output += "-" * 80 + "\n"
            for error in self.semantic_analyzer.errors:
                output += f"❌ {error}\n"
            output += "\n"
        
        # Warnings
        if self.semantic_analyzer.warnings:
            output += "ADVERTENCIAS\n"
            output += "-" * 80 + "\n"
            for warning in self.semantic_analyzer.warnings:
                output += f"⚠ {warning}\n"
            output += "\n"
        
        if not self.semantic_analyzer.errors and not self.semantic_analyzer.warnings:
            output += "✓ No se encontraron errores ni advertencias\n"
        
        self.semantic_text.insert('1.0', output)
    
    def display_generated_code(self):
        """Display generated code"""
        self.codegen_text.delete('1.0', 'end')
        
        output = '\n'.join(self.generated_code)
        self.codegen_text.insert('1.0', output)
    
    def clear_output(self):
        """Clear all output tabs"""
        self.tokens_text.delete('1.0', 'end')
        self.ast_text.delete('1.0', 'end')
        self.semantic_text.delete('1.0', 'end')
        self.codegen_text.delete('1.0', 'end')
        self.status_bar.config(text="Salida limpiada", bg=COLORS['accent_blue'], fg='white')
    
    def load_example_code(self):
        """Load example code into editor"""
        example = '''# Programa de ejemplo en MiniLang
nombre = "MiniLang"
version = 1.0
x = 10
y = 5

# Operaciones aritméticas
suma = x + y
resta = x - y
multiplicacion = x * y
division = x / y

# Imprimir resultados
print("Bienvenido a MiniLang")
print("x = " + str(x))
print("y = " + str(y))
print("x + y = " + str(suma))
print("x - y = " + str(resta))

# Condicional
if x > y:
    print("x es mayor que y")
elif x < y:
    print("y es mayor que x")
else:
    print("x e y son iguales")

# Bucle for
for i in range(5):
    print("Iteración: " + str(i))

# Bucle while
contador = 0
while contador < 3:
    print("Contador: " + str(contador))
    contador = contador + 1
'''
        self.code_editor.delete('1.0', 'end')
        self.code_editor.insert('1.0', example)
        self.update_line_numbers()
        self.status_bar.config(text="Código de ejemplo cargado", bg=COLORS['accent_blue'], fg='white')
    
    def save_code(self):
        """Save code to file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ml",
            filetypes=[("MiniLang Files", "*.ml"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.code_editor.get('1.0', 'end-1c'))
            self.status_bar.config(text=f"Guardado: {file_path}", bg=COLORS['accent_green'], fg='white')
    
    def open_file(self):
        """Open code from file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("MiniLang Files", "*.ml"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.code_editor.delete('1.0', 'end')
            self.code_editor.insert('1.0', content)
            self.update_line_numbers()
            self.status_bar.config(text=f"Abierto: {file_path}", bg=COLORS['accent_blue'], fg='white')


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MiniLangIDE(root)
    root.mainloop()


if __name__ == "__main__":
    main()
