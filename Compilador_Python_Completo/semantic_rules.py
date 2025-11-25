"""
Semantic Rules Database
Contains all semantic rules with their grammar, productions, actions, and examples
"""


class SemanticRule:
    """Represents a single semantic rule"""
    def __init__(self, rule_id, grammar_rule, production, semantic_action, example, phase):
        self.rule_id = rule_id
        self.grammar_rule = grammar_rule
        self.production = production
        self.semantic_action = semantic_action
        self.example = example
        self.phase = phase  # 'lexer', 'parser', 'semantic', 'codegen'
    
    def to_dict(self):
        return {
            'id': self.rule_id,
            'grammar_rule': self.grammar_rule,
            'production': self.production,
            'semantic_action': self.semantic_action,
            'example': self.example,
            'phase': self.phase
        }


# Complete semantic rules database
SEMANTIC_RULES = [
    # LEXER PHASE
    SemanticRule(
        rule_id="L01",
        grammar_rule="Identificador",
        production="IDENTIFIER → [a-zA-Z_][a-zA-Z0-9_]*",
        semantic_action="Crear token IDENTIFIER con el valor del identificador. Verificar si es palabra reservada.",
        example="nombre → Token(IDENTIFIER, 'nombre')",
        phase="lexer"
    ),
    SemanticRule(
        rule_id="L02",
        grammar_rule="Número",
        production="NUMBER → [0-9]+(.[0-9]+)?",
        semantic_action="Crear token NUMBER. Convertir a int o float según contenga punto decimal.",
        example="42 → Token(NUMBER, 42)\n3.14 → Token(NUMBER, 3.14)",
        phase="lexer"
    ),
    SemanticRule(
        rule_id="L03",
        grammar_rule="Cadena",
        production='STRING → "[^"]*" | \'[^\']*\'',
        semantic_action="Crear token STRING. Procesar secuencias de escape (\\n, \\t, \\\\, etc.).",
        example='"Hola" → Token(STRING, \'Hola\')',
        phase="lexer"
    ),
    SemanticRule(
        rule_id="L04",
        grammar_rule="Palabra Reservada",
        production="KEYWORD → if | elif | else | while | for | print | in | range",
        semantic_action="Identificar palabra reservada y crear token específico del tipo correspondiente.",
        example="if → Token(IF, 'if')\nprint → Token(PRINT, 'print')",
        phase="lexer"
    ),
    SemanticRule(
        rule_id="L05",
        grammar_rule="Operador Aritmético",
        production="OPERATOR → + | - | * | /",
        semantic_action="Crear token del operador aritmético correspondiente.",
        example="+ → Token(PLUS, '+')\n* → Token(MULTIPLY, '*')",
        phase="lexer"
    ),
    SemanticRule(
        rule_id="L06",
        grammar_rule="Operador Comparación",
        production="COMPARISON → == | != | < | > | <= | >=",
        semantic_action="Crear token del operador de comparación. Manejar operadores de dos caracteres.",
        example="== → Token(EQUAL, '==')\n<= → Token(LESS_EQUAL, '<=')",
        phase="lexer"
    ),
    SemanticRule(
        rule_id="L07",
        grammar_rule="Indentación",
        production="INDENT/DEDENT → espacios al inicio de línea",
        semantic_action="Mantener pila de indentación. Generar tokens INDENT/DEDENT según cambios de nivel.",
        example="    statement → Token(INDENT, 4)\nstatement → Token(DEDENT, 0)",
        phase="lexer"
    ),
    
    # PARSER PHASE
    SemanticRule(
        rule_id="P01",
        grammar_rule="Programa",
        production="programa → declaraciones",
        semantic_action="Crear nodo ProgramNode con lista de declaraciones. Raíz del AST.",
        example="x = 5\nprint(x) → ProgramNode([Assignment, Print])",
        phase="parser"
    ),
    SemanticRule(
        rule_id="P02",
        grammar_rule="Asignación",
        production="asignacion → ID = expresion",
        semantic_action="Crear nodo AssignmentNode. Almacenar identificador y expresión del lado derecho.",
        example="x = 10 → AssignmentNode('x', NumberNode(10))",
        phase="parser"
    ),
    SemanticRule(
        rule_id="P03",
        grammar_rule="Expresión Aritmética",
        production="expresion → termino ((+|-) termino)*",
        semantic_action="Crear árbol de nodos BinaryOpNode respetando asociatividad izquierda.",
        example="2 + 3 - 1 → BinaryOp(BinaryOp(2, +, 3), -, 1)",
        phase="parser"
    ),
    SemanticRule(
        rule_id="P04",
        grammar_rule="Término",
        production="termino → factor ((*|/) factor)*",
        semantic_action="Crear nodos BinaryOpNode para multiplicación/división con mayor precedencia.",
        example="2 * 3 / 4 → BinaryOp(BinaryOp(2, *, 3), /, 4)",
        phase="parser"
    ),
    SemanticRule(
        rule_id="P05",
        grammar_rule="Factor",
        production="factor → NUMBER | STRING | ID | (expresion)",
        semantic_action="Crear nodo hoja apropiado (NumberNode, StringNode, IdentifierNode) o procesar subexpresión.",
        example="42 → NumberNode(42)\n(x+1) → BinaryOpNode(...)",
        phase="parser"
    ),
    SemanticRule(
        rule_id="P06",
        grammar_rule="Condicional If",
        production="if expresion : bloque (elif expresion : bloque)* (else : bloque)?",
        semantic_action="Crear nodo IfNode con condición, bloque then, lista de elif, y bloque else opcional.",
        example="if x > 0:\n    print(x) → IfNode(BinaryOp(x,>,0), Block([Print]))",
        phase="parser"
    ),
    SemanticRule(
        rule_id="P07",
        grammar_rule="Bucle While",
        production="while expresion : bloque",
        semantic_action="Crear nodo WhileNode con condición y bloque de sentencias.",
        example="while x < 10:\n    x = x + 1 → WhileNode(BinaryOp(x,<,10), Block([...]))",
        phase="parser"
    ),
    SemanticRule(
        rule_id="P08",
        grammar_rule="Bucle For",
        production="for ID in range(expresion) : bloque",
        semantic_action="Crear nodo ForNode con variable iteradora, expresión de rango y bloque.",
        example="for i in range(5):\n    print(i) → ForNode('i', NumberNode(5), Block([...]))",
        phase="parser"
    ),
    SemanticRule(
        rule_id="P09",
        grammar_rule="Print",
        production="print(expresion)",
        semantic_action="Crear nodo PrintNode con expresión a imprimir.",
        example='print("Hola") → PrintNode(StringNode("Hola"))',
        phase="parser"
    ),
    SemanticRule(
        rule_id="P10",
        grammar_rule="Comparación",
        production="comparacion → expresion (==|!=|<|>|<=|>=) expresion",
        semantic_action="Crear nodo BinaryOpNode con operador de comparación.",
        example="x == 5 → BinaryOpNode(IdentifierNode('x'), '==', NumberNode(5))",
        phase="parser"
    ),
    
    # SEMANTIC ANALYSIS PHASE
    SemanticRule(
        rule_id="S01",
        grammar_rule="Declaración de Variable",
        production="ID = expresion",
        semantic_action="Agregar variable a tabla de símbolos. Inferir tipo del valor asignado.",
        example="x = 10 → symbol_table['x'] = {'type': 'int', 'value': 10}",
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S02",
        grammar_rule="Uso de Variable",
        production="ID",
        semantic_action="Verificar que variable existe en tabla de símbolos. Error si no está declarada.",
        example="print(x) → Verificar que 'x' existe en symbol_table",
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S03",
        grammar_rule="Compatibilidad de Tipos",
        production="expresion op expresion",
        semantic_action="Verificar compatibilidad de tipos en operaciones. Permitir coerción implícita.",
        example="5 + 3.14 → OK (int + float = float)\n5 + 'texto' → ERROR",
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S04",
        grammar_rule="Operaciones Aritméticas",
        production="NUMBER op NUMBER",
        semantic_action="Verificar que operandos son numéricos. Calcular tipo resultado.",
        example="int + int → int\nint + float → float\nfloat / int → float",
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S05",
        grammar_rule="Concatenación de Strings",
        production="STRING + STRING",
        semantic_action="Permitir concatenación de strings con operador +.",
        example='"Hola" + " Mundo" → "Hola Mundo"',
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S06",
        grammar_rule="Condición Booleana",
        production="if expresion",
        semantic_action="Verificar que expresión de condición produce valor booleano o comparable.",
        example="if x > 0 → OK (comparación produce bool)\nif 5 → OK (truthy)",
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S07",
        grammar_rule="Ámbito de Variables",
        production="bloque",
        semantic_action="Crear nuevo ámbito al entrar en bloque. Restaurar al salir.",
        example="if True:\n    y = 5  # y solo existe en este bloque",
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S08",
        grammar_rule="Rango de For",
        production="range(expresion)",
        semantic_action="Verificar que argumento de range es numérico entero.",
        example="for i in range(10) → OK\nfor i in range('abc') → ERROR",
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S09",
        grammar_rule="Reasignación",
        production="ID = expresion (variable ya existe)",
        semantic_action="Permitir reasignación. Actualizar tipo si cambia (tipado dinámico).",
        example="x = 5  # x: int\nx = 'texto'  # x: string (OK en tipado dinámico)",
        phase="semantic"
    ),
    SemanticRule(
        rule_id="S10",
        grammar_rule="División por Cero",
        production="expresion / 0",
        semantic_action="Advertir sobre posible división por cero si divisor es literal 0.",
        example="x / 0 → WARNING: División por cero",
        phase="semantic"
    ),
    
    # CODE GENERATION PHASE
    SemanticRule(
        rule_id="C01",
        grammar_rule="Generación de Asignación",
        production="ID = expresion",
        semantic_action="Generar código: evaluar expresión, almacenar en variable.",
        example="x = 5 → LOAD 5\nSTORE x",
        phase="codegen"
    ),
    SemanticRule(
        rule_id="C02",
        grammar_rule="Generación de Operación",
        production="expresion op expresion",
        semantic_action="Generar código: evaluar operandos, aplicar operador.",
        example="a + b → LOAD a\nLOAD b\nADD\nSTORE result",
        phase="codegen"
    ),
    SemanticRule(
        rule_id="C03",
        grammar_rule="Generación de Print",
        production="print(expresion)",
        semantic_action="Generar código: evaluar expresión, llamar función print.",
        example="print(x) → LOAD x\nPRINT",
        phase="codegen"
    ),
    SemanticRule(
        rule_id="C04",
        grammar_rule="Generación de If",
        production="if condicion : bloque",
        semantic_action="Generar código: evaluar condición, salto condicional, código de bloque, etiqueta.",
        example="if x > 0:\n    print(x) → LOAD x\nLOAD 0\nCMP\nJLE L1\nPRINT x\nL1:",
        phase="codegen"
    ),
    SemanticRule(
        rule_id="C05",
        grammar_rule="Generación de While",
        production="while condicion : bloque",
        semantic_action="Generar código: etiqueta inicio, condición, salto condicional, bloque, salto a inicio.",
        example="while x < 10:\n    x = x + 1 → L1: LOAD x\nCMP 10\nJGE L2\n...\nJMP L1\nL2:",
        phase="codegen"
    ),
    SemanticRule(
        rule_id="C06",
        grammar_rule="Generación de For",
        production="for ID in range(N) : bloque",
        semantic_action="Generar código: inicializar contador, loop con condición, incremento, bloque.",
        example="for i in range(5) → LOAD 0\nSTORE i\nL1: LOAD i\nCMP 5\nJGE L2\n...\nINC i\nJMP L1\nL2:",
        phase="codegen"
    ),
    SemanticRule(
        rule_id="C07",
        grammar_rule="Optimización de Constantes",
        production="NUMERO op NUMERO",
        semantic_action="Evaluar operaciones entre constantes en tiempo de compilación.",
        example="x = 2 + 3 → x = 5 (evaluado en compilación)",
        phase="codegen"
    ),
    SemanticRule(
        rule_id="C08",
        grammar_rule="Generación de Comparación",
        production="expresion comp expresion",
        semantic_action="Generar código: evaluar operandos, comparar, almacenar resultado booleano.",
        example="x == 5 → LOAD x\nLOAD 5\nCMP_EQ\nSTORE temp",
        phase="codegen"
    ),
]


def get_rules_by_phase(phase):
    """Get all rules for a specific compilation phase"""
    return [rule for rule in SEMANTIC_RULES if rule.phase == phase]


def get_rule_by_id(rule_id):
    """Get a specific rule by its ID"""
    for rule in SEMANTIC_RULES:
        if rule.rule_id == rule_id:
            return rule
    return None


def get_all_phases():
    """Get list of all compilation phases"""
    return ["lexer", "parser", "semantic", "codegen"]


def get_phase_name(phase):
    """Get human-readable phase name"""
    phase_names = {
        "lexer": "Análisis Léxico",
        "parser": "Análisis Sintáctico",
        "semantic": "Análisis Semántico",
        "codegen": "Generación de Código"
    }
    return phase_names.get(phase, phase)
