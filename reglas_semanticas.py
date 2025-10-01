"""
Base de Datos de Reglas Semánticas
Contiene todas las reglas semánticas con su gramática, producciones, acciones y ejemplos
"""


class ReglaSemantica:
    """Representa una regla semántica individual"""
    def __init__(self, id_regla, regla_gramatical, produccion, accion_semantica, ejemplo, fase):
        self.id_regla = id_regla
        self.regla_gramatical = regla_gramatical
        self.produccion = produccion
        self.accion_semantica = accion_semantica
        self.ejemplo = ejemplo
        self.fase = fase  # 'lexico', 'sintactico', 'semantico', 'codigo'
    
    def a_diccionario(self):
        return {
            'id': self.id_regla,
            'regla_gramatical': self.regla_gramatical,
            'produccion': self.produccion,
            'accion_semantica': self.accion_semantica,
            'ejemplo': self.ejemplo,
            'fase': self.fase
        }


# Base de datos completa de reglas semánticas
REGLAS_SEMANTICAS = [
    # FASE LÉXICA
    ReglaSemantica(
        id_regla="L01",
        regla_gramatical="Identificador",
        produccion="IDENTIFICADOR → [a-zA-Z_][a-zA-Z0-9_]*",
        accion_semantica="Crear token IDENTIFICADOR con el valor del identificador. Verificar si es palabra reservada.",
        ejemplo="nombre → Token(IDENTIFICADOR, 'nombre')",
        fase="lexico"
    ),
    ReglaSemantica(
        id_regla="L02",
        regla_gramatical="Número",
        produccion="NUMERO → [0-9]+(.[0-9]+)?",
        accion_semantica="Crear token NUMERO. Convertir a int o float según contenga punto decimal.",
        ejemplo="42 → Token(NUMERO, 42)\n3.14 → Token(NUMERO, 3.14)",
        fase="lexico"
    ),
    ReglaSemantica(
        id_regla="L03",
        regla_gramatical="Cadena",
        produccion='CADENA → "[^"]*" | \'[^\']*\'',
        accion_semantica="Crear token CADENA. Procesar secuencias de escape (\\n, \\t, \\\\, etc.).",
        ejemplo='"Hola" → Token(CADENA, \'Hola\')',
        fase="lexico"
    ),
    ReglaSemantica(
        id_regla="L04",
        regla_gramatical="Palabra Reservada",
        produccion="PALABRA_CLAVE → if | elif | else | while | for | print | in | range",
        accion_semantica="Identificar palabra reservada y crear token específico del tipo correspondiente.",
        ejemplo="if → Token(IF, 'if')\nprint → Token(PRINT, 'print')",
        fase="lexico"
    ),
    ReglaSemantica(
        id_regla="L05",
        regla_gramatical="Operador Aritmético",
        produccion="OPERADOR → + | - | * | /",
        accion_semantica="Crear token del operador aritmético correspondiente.",
        ejemplo="+ → Token(MAS, '+')\n* → Token(MULTIPLICAR, '*')",
        fase="lexico"
    ),
    ReglaSemantica(
        id_regla="L06",
        regla_gramatical="Operador Comparación",
        produccion="COMPARACION → == | != | < | > | <= | >=",
        accion_semantica="Crear token del operador de comparación. Manejar operadores de dos caracteres.",
        ejemplo="== → Token(IGUAL, '==')\n<= → Token(MENOR_IGUAL, '<=')",
        fase="lexico"
    ),
    ReglaSemantica(
        id_regla="L07",
        regla_gramatical="Indentación",
        produccion="INDENTAR/DESINDENTAR → espacios al inicio de línea",
        accion_semantica="Mantener pila de indentación. Generar tokens INDENTAR/DESINDENTAR según cambios de nivel.",
        ejemplo="    sentencia → Token(INDENTAR, 4)\nsentencia → Token(DESINDENTAR, 0)",
        fase="lexico"
    ),
    
    # FASE SINTÁCTICA
    ReglaSemantica(
        id_regla="P01",
        regla_gramatical="Programa",
        produccion="programa → declaraciones",
        accion_semantica="Crear nodo NodoPrograma con lista de declaraciones. Raíz del AST.",
        ejemplo="x = 5\nprint(x) → NodoPrograma([Asignacion, Print])",
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P02",
        regla_gramatical="Asignación",
        produccion="asignacion → ID = expresion",
        accion_semantica="Crear nodo NodoAsignacion. Almacenar identificador y expresión del lado derecho.",
        ejemplo="x = 10 → NodoAsignacion('x', NodoNumero(10))",
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P03",
        regla_gramatical="Expresión Aritmética",
        produccion="expresion → termino ((+|-) termino)*",
        accion_semantica="Crear árbol de nodos NodoOperacionBinaria respetando asociatividad izquierda.",
        ejemplo="2 + 3 - 1 → OpBinaria(OpBinaria(2, +, 3), -, 1)",
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P04",
        regla_gramatical="Término",
        produccion="termino → factor ((*|/) factor)*",
        accion_semantica="Crear nodos NodoOperacionBinaria para multiplicación/división con mayor precedencia.",
        ejemplo="2 * 3 / 4 → OpBinaria(OpBinaria(2, *, 3), /, 4)",
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P05",
        regla_gramatical="Factor",
        produccion="factor → NUMERO | CADENA | ID | (expresion)",
        accion_semantica="Crear nodo hoja apropiado (NodoNumero, NodoCadena, NodoIdentificador) o procesar subexpresión.",
        ejemplo="42 → NodoNumero(42)\n(x+1) → NodoOperacionBinaria(...)",
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P06",
        regla_gramatical="Condicional If",
        produccion="if expresion : bloque (elif expresion : bloque)* (else : bloque)?",
        accion_semantica="Crear nodo NodoIf con condición, bloque entonces, lista de elif, y bloque sino opcional.",
        ejemplo="if x > 0:\n    print(x) → NodoIf(OpBinaria(x,>,0), Bloque([Print]))",
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P07",
        regla_gramatical="Bucle While",
        produccion="while expresion : bloque",
        accion_semantica="Crear nodo NodoWhile con condición y bloque de sentencias.",
        ejemplo="while x < 10:\n    x = x + 1 → NodoWhile(OpBinaria(x,<,10), Bloque([...]))",
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P08",
        regla_gramatical="Bucle For",
        produccion="for ID in range(expresion) : bloque",
        accion_semantica="Crear nodo NodoFor con variable iteradora, expresión de rango y bloque.",
        ejemplo="for i in range(5):\n    print(i) → NodoFor('i', NodoNumero(5), Bloque([...]))",
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P09",
        regla_gramatical="Print",
        produccion="print(expresion)",
        accion_semantica="Crear nodo NodoPrint con expresión a imprimir.",
        ejemplo='print("Hola") → NodoPrint(NodoCadena("Hola"))',
        fase="sintactico"
    ),
    ReglaSemantica(
        id_regla="P10",
        regla_gramatical="Comparación",
        produccion="comparacion → expresion (==|!=|<|>|<=|>=) expresion",
        accion_semantica="Crear nodo NodoOperacionBinaria con operador de comparación.",
        ejemplo="x == 5 → NodoOperacionBinaria(NodoIdentificador('x'), '==', NodoNumero(5))",
        fase="sintactico"
    ),
    
    # FASE DE ANÁLISIS SEMÁNTICO
    ReglaSemantica(
        id_regla="S01",
        regla_gramatical="Declaración de Variable",
        produccion="ID = expresion",
        accion_semantica="Agregar variable a tabla de símbolos. Inferir tipo del valor asignado.",
        ejemplo="x = 10 → tabla_simbolos['x'] = {'tipo': 'int', 'valor': 10}",
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S02",
        regla_gramatical="Uso de Variable",
        produccion="ID",
        accion_semantica="Verificar que variable existe en tabla de símbolos. Error si no está declarada.",
        ejemplo="print(x) → Verificar que 'x' existe en tabla_simbolos",
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S03",
        regla_gramatical="Compatibilidad de Tipos",
        produccion="expresion op expresion",
        accion_semantica="Verificar compatibilidad de tipos en operaciones. Permitir coerción implícita.",
        ejemplo="5 + 3.14 → OK (int + float = float)\n5 + 'texto' → ERROR",
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S04",
        regla_gramatical="Operaciones Aritméticas",
        produccion="NUMERO op NUMERO",
        accion_semantica="Verificar que operandos son numéricos. Calcular tipo resultado.",
        ejemplo="int + int → int\nint + float → float\nfloat / int → float",
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S05",
        regla_gramatical="Concatenación de Cadenas",
        produccion="CADENA + CADENA",
        accion_semantica="Permitir concatenación de cadenas con operador +.",
        ejemplo='"Hola" + " Mundo" → "Hola Mundo"',
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S06",
        regla_gramatical="Condición Booleana",
        produccion="if expresion",
        accion_semantica="Verificar que expresión de condición produce valor booleano o comparable.",
        ejemplo="if x > 0 → OK (comparación produce bool)\nif 5 → OK (truthy)",
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S07",
        regla_gramatical="Ámbito de Variables",
        produccion="bloque",
        accion_semantica="Crear nuevo ámbito al entrar en bloque. Restaurar al salir.",
        ejemplo="if True:\n    y = 5  # y solo existe en este bloque",
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S08",
        regla_gramatical="Rango de For",
        produccion="range(expresion)",
        accion_semantica="Verificar que argumento de range es numérico entero.",
        ejemplo="for i in range(10) → OK\nfor i in range('abc') → ERROR",
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S09",
        regla_gramatical="Reasignación",
        produccion="ID = expresion (variable ya existe)",
        accion_semantica="Permitir reasignación. Actualizar tipo si cambia (tipado dinámico).",
        ejemplo="x = 5  # x: int\nx = 'texto'  # x: cadena (OK en tipado dinámico)",
        fase="semantico"
    ),
    ReglaSemantica(
        id_regla="S10",
        regla_gramatical="División por Cero",
        produccion="expresion / 0",
        accion_semantica="Advertir sobre posible división por cero si divisor es literal 0.",
        ejemplo="x / 0 → ADVERTENCIA: División por cero",
        fase="semantico"
    ),
    
    # FASE DE GENERACIÓN DE CÓDIGO
    ReglaSemantica(
        id_regla="C01",
        regla_gramatical="Generación de Asignación",
        produccion="ID = expresion",
        accion_semantica="Generar código: evaluar expresión, almacenar en variable.",
        ejemplo="x = 5 → LOAD 5\nSTORE x",
        fase="codigo"
    ),
    ReglaSemantica(
        id_regla="C02",
        regla_gramatical="Generación de Operación",
        produccion="expresion op expresion",
        accion_semantica="Generar código: evaluar operandos, aplicar operador.",
        ejemplo="a + b → LOAD a\nLOAD b\nADD\nSTORE result",
        fase="codigo"
    ),
    ReglaSemantica(
        id_regla="C03",
        regla_gramatical="Generación de Print",
        produccion="print(expresion)",
        accion_semantica="Generar código: evaluar expresión, llamar función print.",
        ejemplo="print(x) → LOAD x\nPRINT",
        fase="codigo"
    ),
    ReglaSemantica(
        id_regla="C04",
        regla_gramatical="Generación de If",
        produccion="if condicion : bloque",
        accion_semantica="Generar código: evaluar condición, salto condicional, código de bloque, etiqueta.",
        ejemplo="if x > 0:\n    print(x) → LOAD x\nLOAD 0\nCMP\nJLE L1\nPRINT x\nL1:",
        fase="codigo"
    ),
    ReglaSemantica(
        id_regla="C05",
        regla_gramatical="Generación de While",
        produccion="while condicion : bloque",
        accion_semantica="Generar código: etiqueta inicio, condición, salto condicional, bloque, salto a inicio.",
        ejemplo="while x < 10:\n    x = x + 1 → L1: LOAD x\nCMP 10\nJGE L2\n...\nJMP L1\nL2:",
        fase="codigo"
    ),
    ReglaSemantica(
        id_regla="C06",
        regla_gramatical="Generación de For",
        produccion="for ID in range(N) : bloque",
        accion_semantica="Generar código: inicializar contador, loop con condición, incremento, bloque.",
        ejemplo="for i in range(5) → LOAD 0\nSTORE i\nL1: LOAD i\nCMP 5\nJGE L2\n...\nINC i\nJMP L1\nL2:",
        fase="codigo"
    ),
    ReglaSemantica(
        id_regla="C07",
        regla_gramatical="Optimización de Constantes",
        produccion="NUMERO op NUMERO",
        accion_semantica="Evaluar operaciones entre constantes en tiempo de compilación.",
        ejemplo="x = 2 + 3 → x = 5 (evaluado en compilación)",
        fase="codigo"
    ),
    ReglaSemantica(
        id_regla="C08",
        regla_gramatical="Generación de Comparación",
        produccion="expresion comp expresion",
        accion_semantica="Generar código: evaluar operandos, comparar, almacenar resultado booleano.",
        ejemplo="x == 5 → LOAD x\nLOAD 5\nCMP_EQ\nSTORE temp",
        fase="codigo"
    ),
]


def obtener_reglas_por_fase(fase):
    """Obtener todas las reglas para una fase específica de compilación"""
    return [regla for regla in REGLAS_SEMANTICAS if regla.fase == fase]


def obtener_regla_por_id(id_regla):
    """Obtener una regla específica por su ID"""
    for regla in REGLAS_SEMANTICAS:
        if regla.id_regla == id_regla:
            return regla
    return None


def obtener_todas_fases():
    """Obtener lista de todas las fases de compilación"""
    return ["lexico", "sintactico", "semantico", "codigo"]


def obtener_nombre_fase(fase):
    """Obtener nombre legible de la fase"""
    nombres_fase = {
        "lexico": "Análisis Léxico",
        "sintactico": "Análisis Sintáctico",
        "semantico": "Análisis Semántico",
        "codigo": "Generación de Código"
    }
    return nombres_fase.get(fase, fase)
