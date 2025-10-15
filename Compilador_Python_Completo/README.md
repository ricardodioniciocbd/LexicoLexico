# MiniLang IDE - Compilador con Acciones Semánticas

Un compilador educativo completo con interfaz gráfica profesional que demuestra todas las fases de compilación con énfasis en **acciones semánticas**.

## 🎯 Características Principales

- **Análisis Léxico**: Tokenización completa con soporte para Python-like syntax
- **Análisis Sintáctico**: Parser recursivo descendente que genera AST
- **Análisis Semántico**: Verificación de tipos, tabla de símbolos, detección de errores
- **Generación de Código**: Código de tres direcciones
- **Tabla de Reglas Semánticas**: 38 reglas documentadas con ejemplos
- **IDE Profesional**: Interfaz oscura moderna estilo VS Code
- **Documentación Integrada**: Gramática completa y ejemplos

## 📋 Requisitos

- Python 3.7 o superior
- tkinter (incluido con Python en Windows)

## 🚀 Instalación y Uso

### Instalación

```bash
# Clonar o descargar el proyecto
cd AccionesSemanticas_py

# No requiere instalación de dependencias adicionales
# tkinter viene incluido con Python
```

### Ejecutar el IDE

```bash
python minilang_ide.py
```

## 📁 Estructura del Proyecto

```
AccionesSemanticas_py/
│
├── token_types.py          # Definiciones de tokens
├── lexer.py                # Analizador léxico
├── ast_nodes.py            # Nodos del AST
├── parser.py               # Analizador sintáctico
├── semantic_analyzer.py    # Analizador semántico
├── code_generator.py       # Generador de código
├── semantic_rules.py       # Base de datos de reglas semánticas
├── minilang_ide.py         # Aplicación principal del IDE
├── README.md               # Este archivo
└── examples/               # Programas de ejemplo
    ├── basic.ml
    ├── conditionals.ml
    ├── loops.ml
    └── complete.ml
```

## 💻 Sintaxis de MiniLang

### Características

- Sintaxis tipo Python (sin punto y coma)
- Tipado dinámico
- Indentación significativa
- Comentarios con `#`
- Soporte para números, strings e identificadores

### Palabras Reservadas

```
print, if, elif, else, while, for, in, range, var
```

### Operadores

**Aritméticos**: `+`, `-`, `*`, `/`

**Comparación**: `==`, `!=`, `<`, `>`, `<=`, `>=`

**Asignación**: `=`

### Ejemplos de Código

#### Variables y Operaciones

```python
x = 10
y = 5
suma = x + y
print("Resultado: " + str(suma))
```

#### Condicionales

```python
if x > y:
    print("x es mayor")
elif x < y:
    print("y es mayor")
else:
    print("Son iguales")
```

#### Bucles

```python
# For loop
for i in range(10):
    print("Iteración: " + str(i))

# While loop
contador = 0
while contador < 5:
    print(contador)
    contador = contador + 1
```

## 🔍 Fases de Compilación

### 1. Análisis Léxico

Convierte el código fuente en tokens:

```
x = 10  →  [IDENTIFIER(x), ASSIGN(=), NUMBER(10)]
```

**Reglas semánticas aplicadas**:
- L01: Reconocimiento de identificadores
- L02: Reconocimiento de números
- L05: Reconocimiento de operadores

### 2. Análisis Sintáctico

Construye el Árbol de Sintaxis Abstracta (AST):

```
x = 10  →  AssignmentNode('x', NumberNode(10))
```

**Reglas semánticas aplicadas**:
- P02: Creación de nodo de asignación
- P05: Creación de nodo numérico

### 3. Análisis Semántico

Verifica tipos y construye tabla de símbolos:

```
x = 10  →  symbol_table['x'] = {'type': 'int', 'value': 10}
```

**Reglas semánticas aplicadas**:
- S01: Declaración de variable
- S03: Verificación de compatibilidad de tipos
- S04: Verificación de operaciones aritméticas

### 4. Generación de Código

Genera código de tres direcciones:

```
x = 10  →  x = 10
```

**Reglas semánticas aplicadas**:
- C01: Generación de asignación
- C02: Generación de operaciones

## 📊 Tabla de Reglas Semánticas

El IDE incluye una tabla completa con **38 reglas semánticas** organizadas por fase:

| Fase | Cantidad de Reglas |
|------|-------------------|
| Análisis Léxico | 7 reglas |
| Análisis Sintáctico | 10 reglas |
| Análisis Semántico | 10 reglas |
| Generación de Código | 8 reglas |

Cada regla incluye:
- **ID**: Identificador único
- **Regla Gramatical**: Nombre descriptivo
- **Producción**: Regla de la gramática
- **Acción Semántica**: Descripción de la acción
- **Ejemplo**: Caso de uso concreto

## 🎨 Interfaz del IDE

### Pestañas Principales

1. **Tokens**: Muestra todos los tokens generados por el lexer
2. **AST**: Visualización del árbol de sintaxis abstracta
3. **Análisis Semántico**: Tabla de símbolos, errores y advertencias
4. **Código Generado**: Código de tres direcciones generado
5. **Reglas Semánticas**: Tabla interactiva con todas las reglas
6. **Gramática**: Documentación completa de la gramática

### Características de la Interfaz

- ✨ Tema oscuro profesional
- 📝 Editor con números de línea
- 🎯 Resaltado de sintaxis visual
- 📊 Tabla interactiva de reglas
- 🔍 Detalles de reglas al seleccionar
- 💾 Guardar y abrir archivos
- 📄 Ejemplos precargados

## 🧪 Ejemplos de Uso

### Ejemplo 1: Programa Básico

```python
# basic.ml
x = 10
y = 20
suma = x + y
print("La suma es: " + str(suma))
```

### Ejemplo 2: Condicionales

```python
# conditionals.ml
edad = 18

if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")
```

### Ejemplo 3: Bucles

```python
# loops.ml
# Tabla de multiplicar
numero = 5
for i in range(10):
    resultado = numero * i
    print(str(numero) + " x " + str(i) + " = " + str(resultado))
```

## 🐛 Detección de Errores

El compilador detecta múltiples tipos de errores:

### Errores Léxicos

```python
x = @invalid  # Error: Carácter inesperado '@'
```

### Errores Sintácticos

```python
if x > 5  # Error: Se esperaba ':'
    print(x)
```

### Errores Semánticos

```python
print(z)  # Error: Variable 'z' no declarada
x = 5 + "texto"  # Error: Incompatibilidad de tipos
```

## 📚 Gramática Completa

```
programa → declaraciones

declaraciones → declaracion declaraciones | ε

declaracion → asignacion 
            | condicional 
            | bucle 
            | print_statement

asignacion → ID = expresion

condicional → if expresion : bloque
              (elif expresion : bloque)*
              (else : bloque)?

bucle_while → while expresion : bloque

bucle_for → for ID in range(expresion) : bloque

print_statement → print(expresion)

expresion → termino ((+|-) termino)*

termino → factor ((*|/) factor)*

factor → NUMERO | STRING | ID | (expresion) | -factor

comparacion → expresion (==|!=|<|>|<=|>=) expresion
```

## 🎓 Propósito Educativo

Este proyecto está diseñado para:

1. **Enseñar conceptos de compiladores**: Demuestra todas las fases de compilación
2. **Ilustrar acciones semánticas**: Cada regla gramatical tiene su acción semántica asociada
3. **Proporcionar herramienta práctica**: IDE funcional para experimentar
4. **Documentar el proceso**: Tabla completa de reglas con ejemplos

## 🔧 Extensiones Posibles

- Agregar más tipos de datos (arrays, objetos)
- Implementar funciones y procedimientos
- Optimización de código
- Generación de código ejecutable
- Depurador integrado
- Más estructuras de control (switch, do-while)

## 📝 Notas Técnicas

### Técnicas de Compilación Utilizadas

- **Parser Recursivo Descendente**: Análisis sintáctico top-down
- **Tabla de Símbolos con Ámbitos**: Soporte para scoping
- **Tipado Dinámico**: Las variables pueden cambiar de tipo
- **Código de Tres Direcciones**: Representación intermedia estándar
- **Análisis Semántico en un Paso**: Visitor pattern sobre el AST

### Limitaciones Conocidas

- No soporta funciones definidas por el usuario
- No hay tipos de datos complejos (arrays, objetos)
- El código generado es simbólico (no ejecutable directamente)
- Indentación debe ser consistente (espacios o tabs)

## 👨‍💻 Autor

Proyecto educativo para demostrar compiladores con acciones semánticas.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

**¡Disfruta explorando el mundo de los compiladores con MiniLang IDE!** 🚀
