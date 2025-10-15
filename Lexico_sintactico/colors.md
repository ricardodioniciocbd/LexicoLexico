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