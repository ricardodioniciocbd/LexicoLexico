# GUÍA DE COMENTARIOS EN ESPAÑOL - CÓDIGO FUENTE

Este documento lista todos los comentarios importantes en español agregados al código para facilitar su identificación y comprensión.

---

## 📄 `lexer.py` - Análisis Léxico (PUNTO 2)

### Comentarios Principales

```python
"""
Módulo de Análisis Léxico
Realiza la tokenización del código fuente (convierte texto en tokens)
PUNTO 2: Implementa Autómatas Finitos Deterministas (AFD)
"""

class Lexer:
    """
    Analizador Léxico (Lexer) - PUNTO 2
    Implementa AFD (Autómata Finito Determinista) para reconocer tokens
    """
```

### Funciones Clave

| Función | Descripción en Español |
|---------|------------------------|
| `peek()` | **Lookahead**: Mira el siguiente carácter sin consumirlo. Esencial para AFD con lookahead |
| `advance()` | Consume y retorna el carácter actual (avanza en el código) |
| `read_number()` | **AFD para números**: Estados q0 → q1 (dígitos) → q2 (punto) → q3 (más dígitos) |
| `read_string()` | **AFD para strings**: Lee cadenas encerradas en comillas, maneja secuencias de escape |
| `read_identifier()` | **AFD para identificadores**: q0 --[letra\|_]--> q1 --[letra\|dígito\|_]--> q1 |
| `handle_indentation()` | Genera tokens INDENT/DEDENT basado en cambios de indentación |
| `tokenize()` | **Método principal**: Convierte código fuente en tokens |

### Comentarios Inline Importantes

```python
# Línea 24: Posición actual en el código
self.position = 0

# Línea 25: Línea actual
self.line = 1

# Línea 26: Columna actual
self.column = 1

# Línea 27: Lista de tokens generados
self.tokens = []

# Línea 28: Pila para rastrear niveles de indentación
self.indent_stack = [0]

# Línea 80: Convertir a tipo numérico apropiado
# Línea 104: Manejar secuencias de escape
# Línea 128: Verificar si es una palabra clave (keyword)
# Línea 162: Manejar indentación al inicio de líneas
# Línea 172-177: Comentarios
# Línea 183-189: Números
# Línea 191-193: Strings
# Línea 195-199: Identificadores y palabras clave
# Línea 201-221: Operadores de dos caracteres
# Línea 223-270: Operadores de un carácter y delimitadores
# Línea 275: Agregar tokens DEDENT restantes
# Línea 280: Agregar token EOF
```

---

## 📄 `parser.py` - Análisis Sintáctico (PUNTO 3)

### Comentarios Principales

```python
"""
Módulo de Análisis Sintáctico (Parser)
Realiza el análisis sintáctico y construye el Árbol de Sintaxis Abstracta (AST)
PUNTO 3: Implementa Gramática Libre de Contexto (CFG) tipo LL(1)
"""

class Parser:
    """
    Parser de Descenso Recursivo - PUNTO 3
    Implementa análisis sintáctico LL(1) sin recursión izquierda
    Construye el AST (Árbol de Sintaxis Abstracta)
    """
```

### Producciones Gramaticales con Acciones Semánticas

| Función | Producción | Acción Semántica |
|---------|-----------|------------------|
| `parse_program()` | programa → declaraciones | Crea ProgramNode con lista de sentencias |
| `parse_statement()` | sentencia → asignacion \| impresion \| condicional \| bucle | Enruta al parser apropiado según token |
| `parse_assignment()` | asignacion → ID = expresion | Crea AssignmentNode con identificador y expresión |
| `parse_print()` | print_statement → print(expresion) | Crea PrintNode con expresión a imprimir |
| `parse_if()` | condicional → if expr : bloque (elif)* (else)? | Crea IfNode con condición, bloques then/else |
| `parse_while()` | bucle_while → while expresion : bloque | Crea WhileNode con condición y bloque |
| `parse_for()` | bucle_for → for ID in range(expr) : bloque | Crea ForNode con variable, rango y bloque |
| `parse_block()` | bloque → INDENT sentencias DEDENT | Crea BlockNode con lista de sentencias |
| `parse_expression()` | expresion → comparacion | Punto de entrada para expresiones |
| `parse_comparison()` | comparacion → aritmetica ((==\|!=\|<\|>)...)? | Crea BinaryOpNode para comparaciones |
| `parse_arithmetic()` | expresion → termino ((+\|-) termino)* | Crea árbol de BinaryOpNode con asociatividad izquierda |
| `parse_term()` | termino → factor ((*\|/) factor)* | BinaryOpNode para multiplicación/división con mayor precedencia |
| `parse_factor()` | factor → NUMBER \| STRING \| ID \| (expr) \| -factor | Crea nodo hoja apropiado o maneja expresión parentizada |

### Jerarquía de Precedencia (de mayor a menor)

```python
# NIVEL 1: Paréntesis ( )
# NIVEL 2: Unario -
# NIVEL 3: Multiplicación/División * / %  ← parse_term()
# NIVEL 4: Suma/Resta + -                ← parse_arithmetic()
# NIVEL 5: Comparación < > <= >=         ← parse_comparison()
# NIVEL 6: Igualdad == !=                ← parse_comparison()
```

### Comentarios Importantes

```python
# Línea 24: Lanza error de parser con información del token actual
# Línea 34: Lookahead: Mira token siguiente sin consumirlo
# Línea 41: Avanza al siguiente token
# Línea 48: Consume token del tipo esperado o lanza error
# Línea 56: Salta tokens de nueva línea (NEWLINE)
# Línea 86: Analiza una sentencia individual
# Línea 90-99: Asignación o expresión
# Línea 91-93: Lookahead para determinar si es asignación
# Línea 161-172: Analiza bloques elif
# Línea 174-180: Analiza bloque else
# Línea 224-226: Espera token INDENT
# Línea 230-235: Analiza sentencias hasta DEDENT
# Línea 237-239: Consume DEDENT
# Línea 257-261: Operadores de comparación
# Línea 272-286: Jerarquía de precedencia - Recursión eliminada
# Línea 311-340: Literales numéricos, strings, identificadores, paréntesis, unario
```

---

## 📄 `semantic_analyzer.py` - Análisis Semántico (PUNTOS 4 y 7)

### Comentarios Principales

```python
"""
Analizador Semántico
Verifica que las variables estén declaradas antes de usarse y que los tipos sean compatibles
PUNTO 4: Tabla de Símbolos y Gestión de Contexto
PUNTO 7: Análisis Semántico Basado en Gramáticas Atribuidas
"""

class SemanticAnalyzer:
    """
    Analizador Semántico - PUNTOS 4 y 7
    - Tabla de símbolos con inferencia de tipos
    - Verificación de declaración antes de uso
    - Compatibilidad de tipos en operaciones
    - Visitor Pattern para recorrer el AST
    """
```

### Estructura de la Tabla de Símbolos

```python
# Línea 18: Tabla de símbolos
self.symbol_table = {
    'nombre_variable': {
        'type': tipo,           # str, int, float, list, bool
        'initialized': bool,    # ¿Está inicializada?
        'line': linea          # Línea de declaración
    }
}
```

### Métodos Importantes

| Método | Descripción | Punto |
|--------|-------------|-------|
| `infer_type()` | Infiere el tipo de una expresión (atributos sintetizados) | 7 |
| `check_type_compatibility()` | Verifica compatibilidad de tipos en operaciones | 7 |
| `analyze()` | Analiza el AST completo | 4, 7 |
| `visit()` | Visitor Pattern - visita un nodo del AST | 6, 7 |
| `visit_AssignmentNode()` | Registra variable en tabla de símbolos | 4 |
| `visit_IdentifierNode()` | Verifica que variable esté declarada antes de uso | 4 |
| `visit_BinaryOpNode()` | Verifica compatibilidad de tipos | 7 |
| `get_report()` | Genera reporte del análisis semántico | 5 |

### Comentarios Clave

```python
# Línea 34: Infiere el tipo de una expresión
# Línea 36: Números: 'int' o 'float'
# Línea 38: Strings: 'str'
# Línea 40-42: Identificadores: busca en tabla de símbolos
# Línea 48-49: Comparaciones siempre devuelven 'bool'
# Línea 53-59: Operaciones aritméticas
# Línea 54-55: Si alguno es float, el resultado es float
# Línea 57-59: Si ambos son int, resultado es int (excepto división)
# Línea 60-62: Concatenación de strings con +
# Línea 75: Verifica compatibilidad de tipos en una operación
# Línea 78: Operadores aritméticos
# Línea 79-88: Suma de strings (concatenación)
# Línea 90-105: Operaciones numéricas
# Línea 108-109: Advertencia por posible división por cero
# Línea 114: Operadores de comparación
# Línea 116-117: Cualquier tipo se puede comparar con ==, !=
# Línea 119-122: <, >, <=, >= requieren tipos compatibles
# Línea 132: Analiza el AST completo
# Línea 137: Visitor Pattern
# Línea 139: Busca método visit_{NombreNodo}
# Línea 152-174: Visita asignación - actualiza tabla de símbolos
# Línea 158: Infiere el tipo de la expresión
# Línea 160-167: Verifica cambio de tipo (advertencia)
# Línea 169-174: Registra/actualiza variable en tabla
# Línea 234-246: Visita operación binaria - verifica tipos
# Línea 260-271: Visita identificador - verifica declaración
```

---

## 📄 `ast_nodes.py` - Nodos del AST (PUNTO 6)

### Comentarios Principales

```python
"""
Definiciones de Nodos del Árbol de Sintaxis Abstracta (AST)
PUNTO 6: Estructura Jerárquica que representa el programa
"""

class ASTNode:
    """Nodo base del AST - todos los nodos heredan de esta clase"""
    pass

class ProgramNode(ASTNode):
    """Nodo raíz del programa - contiene lista de sentencias"""
    def __init__(self, statements):
        self.statements = statements  # Lista de sentencias del programa

class AssignmentNode(ASTNode):
    """Nodo de asignación: x = expresion"""
    def __init__(self, identifier, expression, line=0):
        self.identifier = identifier  # Nombre de la variable
        self.expression = expression  # Expresión a asignar
        self.line = line  # Línea en el código fuente

class BinaryOpNode(ASTNode):
    """Nodo de operación binaria: left operador right"""
    def __init__(self, left, operator, right, line=0):
        self.left = left        # Expresión izquierda
        self.operator = operator  # Operador (+, -, *, /, ==, etc.)
        self.right = right       # Expresión derecha
        self.line = line
```

### Todos los Nodos del AST

| Clase | Descripción |
|-------|-------------|
| `ASTNode` | Nodo base (clase padre) |
| `ProgramNode` | Raíz del programa |
| `AssignmentNode` | Asignación (x = expr) |
| `PrintNode` | Sentencia print |
| `IfNode` | Condicional if/elif/else |
| `WhileNode` | Bucle while |
| `ForNode` | Bucle for |
| `BlockNode` | Bloque de sentencias |
| `BinaryOpNode` | Operación binaria |
| `UnaryOpNode` | Operación unaria |
| `NumberNode` | Literal numérico |
| `StringNode` | Literal de cadena |
| `IdentifierNode` | Identificador/variable |
| `ListNode` | Lista/arreglo |
| `IndexNode` | Acceso por índice |
| `CallNode` | Llamada a función |

---

## 📄 `token_types.py` - Tipos de Tokens (PUNTO 1)

### Comentarios Principales

```python
"""
Definición de Tipos de Tokens y Alfabeto del Lenguaje
PUNTO 1: Define formalmente Σ (alfabeto de entrada)
"""

class TokenType(Enum):
    """
    Tipos de tokens del lenguaje - PUNTO 1
    Define el alfabeto Σ para la gramática formal
    """
    # Literales
    NUMBER = auto()      # Números: [0-9]+(\.[0-9]+)?
    STRING = auto()      # Strings: "[^"]*" | '[^']*'
    IDENTIFIER = auto()  # Identificadores: [a-zA-Z_][a-zA-Z0-9_]*
    
    # Palabras clave
    IF = auto()          # if
    ELIF = auto()        # elif
    ELSE = auto()        # else
    WHILE = auto()       # while
    FOR = auto()         # for
    # ... etc

KEYWORDS = {
    'if': TokenType.IF,
    'elif': TokenType.ELIF,
    # ... más palabras clave
}
```

---

## 📄 `parser_stack.py` - Autómata de Pila (PUNTO 8) 🆕

### Comentarios Principales

```python
"""
Autómata de Pila Formal para Análisis Sintáctico
Implementa un parser LR(1) con tabla de parsing explícita
PUNTO 8: Autómatas de Pila con Tablas ACTION y GOTO
"""

class PushdownAutomaton:
    """
    Autómata de Pila (PDA) para Análisis Sintáctico
    
    Formalmente: PDA = (Q, Σ, Γ, δ, q0, Z0, F)
    Donde:
    - Q: Conjunto de estados
    - Σ: Alfabeto de entrada (tokens)
    - Γ: Alfabeto de la pila
    - δ: Función de transición
    - q0: Estado inicial
    - Z0: Símbolo inicial de la pila
    - F: Estados finales
    """
```

### Tablas LR

```python
# Tabla ACTION: (estado, terminal) → acción
self.action_table[(estado, terminal)] = LRAction(Action.SHIFT, nuevo_estado)
self.action_table[(estado, terminal)] = LRAction(Action.REDUCE, regla)
self.action_table[(estado, terminal)] = LRAction(Action.ACCEPT)

# Tabla GOTO: (estado, no_terminal) → estado
self.goto_table[(estado, no_terminal)] = nuevo_estado
```

---

## 📄 `automata_optimizer.py` - Minimización (PUNTO 9) 🆕

### Comentarios Principales

```python
"""
Optimizaciones Basadas en Teoría de Autómatas
Implementa minimización de autómatas y análisis de complejidad
PUNTO 9: Minimización de DFA con algoritmo de Hopcroft
"""

class AutomataMinimizer:
    """
    Minimizador de Autómatas Finitos Deterministas
    Implementa el algoritmo de Hopcroft para minimización en O(n log n)
    
    Pasos:
    1. Eliminar estados inalcanzables
    2. Particionar estados en equivalentes/no equivalentes
    3. Refinar particiones hasta convergencia
    4. Construir DFA mínimo
    """
```

### Análisis de Complejidad

```python
# Complejidad temporal: O(n log n) - algoritmo de Hopcroft
# Complejidad espacial: O(n²) - particiones
# Reducción de estados: original → minimizado
```

---

## 📄 `formal_properties.py` - Propiedades Formales (PUNTO 10) 🆕

### Comentarios Principales

```python
"""
Propiedades de Cerradura y Decidibilidad de Lenguajes Formales
Implementa verificaciones de propiedades formales según teoría de autómatas
PUNTO 10: Operaciones de Cerradura y Problemas Decidibles
"""

class ClosureProperties:
    """
    Verificación de Propiedades de Cerradura
    
    Los lenguajes regulares son cerrados bajo:
    - Unión: L1 ∪ L2
    - Concatenación: L1 · L2
    - Estrella de Kleene: L*
    - Complemento: L'
    - Intersección: L1 ∩ L2
    - Diferencia: L1 - L2
    """

class DecidabilityAnalyzer:
    """
    Análisis de Propiedades Decidibles
    
    Para lenguajes regulares, estos problemas son DECIDIBLES:
    1. Problema del vacío: ¿L = ∅?  → O(n + m)
    2. Problema de finitud: ¿|L| < ∞?  → O(n²)
    3. Problema de pertenencia: ¿w ∈ L?  → O(|w|)
    4. Problema de equivalencia: ¿L1 = L2?  → O(n1 × n2)
    """
```

---

## 📊 RESUMEN DE COMENTARIOS POR PUNTO

| Punto | Archivo Principal | Comentarios Clave |
|-------|-------------------|-------------------|
| 1 | `token_types.py` | Define Σ (alfabeto), G = (N, Σ, P, S) |
| 2 | `lexer.py` | AFD para tokens, lookahead, tabla de transiciones |
| 3 | `parser.py` | CFG, LL(1), eliminación recursión izquierda, precedencia |
| 4 | `semantic_analyzer.py` | Tabla de símbolos, ámbitos, verificación tipos |
| 5 | Todos | Manejo errores, panic mode, localización, recuperación |
| 6 | `ast_nodes.py` | Jerarquía de nodos, Visitor Pattern |
| 7 | `semantic_analyzer.py` | Gramáticas atribuidas, inferencia tipos |
| 8 | `parser_stack.py` | PDA, tablas LR, ACTION/GOTO |
| 9 | `automata_optimizer.py` | Minimización O(n log n), compresión tablas |
| 10 | `formal_properties.py` | Cerradura, decidibilidad, complejidad |

---

## 🔍 CÓMO BUSCAR COMENTARIOS ESPECÍFICOS

### Por Punto Teórico
```bash
# Buscar comentarios del PUNTO 2 (AFD)
grep -r "PUNTO 2" *.py

# Buscar comentarios del PUNTO 8 (PDA)
grep -r "PUNTO 8" *.py
```

### Por Concepto
```bash
# Buscar AFD (Autómata Finito Determinista)
grep -r "AFD" *.py

# Buscar Tabla de Símbolos
grep -r "Tabla de símbolos" *.py

# Buscar Visitor Pattern
grep -r "Visitor" *.py
```

### Por Complejidad
```bash
# Buscar análisis de complejidad
grep -r "O(n" *.py

# Buscar Complejidad temporal
grep -r "Complejidad temporal" *.py
```

---

## 📝 NOTAS IMPORTANTES

### Convenciones de Comentarios

1. **Docstrings de Módulo**: Explican el propósito general y qué punto implementan
2. **Docstrings de Clase**: Describen la estructura formal (AFD, PDA, etc.)
3. **Docstrings de Función**: Incluyen producción gramatical y acción semántica
4. **Comentarios Inline**: Explican líneas específicas importantes

### Identificadores Clave

- **"PUNTO X"**: Indica qué punto de los 10 implementa
- **"AFD"**: Autómata Finito Determinista
- **"PDA"**: Autómata de Pila (Pushdown Automaton)
- **"CFG"**: Gramática Libre de Contexto
- **"AST"**: Árbol de Sintaxis Abstracta
- **"Visitor"**: Patrón Visitor
- **"O(n)"**: Notación Big-O de complejidad

---

**Última actualización**: Octubre 2025  
**Idioma**: Español  
**Propósito**: Facilitar identificación y comprensión del código


