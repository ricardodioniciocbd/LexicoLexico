# IDE Compilador Interactivo de Python

## Descripción
IDE completo con interfaz gráfica (GUI) para compilar y analizar código Python, con soporte para todas las fases de compilación: análisis léxico, sintáctico, semántico, generación de código intermedio (TAC), optimización y ejecución.

## Requisitos del Sistema
- Python 3.10 o superior
- Tkinter (incluido con Python)

## Instalación

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar el IDE
```bash
python python_ide_complete.py
```

## Archivos del Proyecto

### Archivos Principales
- **python_ide_complete.py** - Interfaz gráfica principal del IDE
- **python_compiler.py** - Compilador con todas las fases

### Módulos de Análisis
- **lexer.py** - Análisis léxico
- **parser.py** - Análisis sintáctico
- **semantic_analyzer.py** - Análisis semántico
- **ast_nodes.py** - Definiciones de nodos del AST

### Módulos de Código Intermedio y Optimización
- **tac_generator.py** - Generación de código de tres direcciones (TAC)
- **tac_optimizer.py** - Optimización del código TAC
- **tac_interpreter.py** - Interpretación y ejecución del TAC

### Módulos Adicionales
- **machine_code_generator.py** - Generación de código ensamblador
- **token_types.py** - Definiciones de tipos de tokens
- **reglas_semanticas.py** - Reglas semánticas y validaciones

## Características

✅ **Análisis Léxico** - Tokenización y validación de símbolos
✅ **Análisis Sintáctico** - Validación de estructura gramatical
✅ **Análisis Semántico** - Validación de tipos y variables
✅ **Código Intermedio (TAC)** - Generación de instrucciones de tres direcciones
✅ **Optimización** - Optimización del código intermedio
✅ **Código Máquina** - Generación de código ensamblador
✅ **Ejecución** - Interpretación y ejecución del código
✅ **Interfaz Gráfica** - IDE moderno con tema oscuro

## Uso del IDE

1. **Escribir código**: Usa el editor en el lado izquierdo para escribir código Python
2. **Analizar**: Haz clic en el botón "▶ ANALIZAR" para compilar el código
3. **Ver resultados**: Consulta las diferentes pestañas para ver:
   - Análisis Léxico
   - Análisis Sintáctico (AST)
   - Análisis Semántico
   - Código TAC
   - Optimización
   - Código Máquina
   - Ejecución

## Ejemplos Predefinidos

El IDE incluye ejemplos predefinidos:
- **Fibonacci** - Serie de Fibonacci
- **Búsqueda** - Búsqueda en arreglo
- **Listas** - Procesamiento de listas
- **Con Errores** - Ejemplos con errores para demostración

## Código Soportado

El compilador soporta un subconjunto de Python incluyendo:
- Variables y asignaciones
- Operaciones aritméticas y lógicas
- Condicionales (if/elif/else)
- Bucles (while/for)
- Listas y arrays
- Funciones print
- Comparaciones

## Solución de Problemas

### Error "ModuleNotFoundError"
Asegúrate de que todos los archivos `.py` están en la misma carpeta.

### Error "SyntaxWarning invalid escape sequence"
Se corrigió usando cadenas raw (r"") en las expresiones regulares.

### La GUI no aparece
Verifica que Tkinter esté instalado en tu sistema.

## Estructura del Compilador

```
Código Fuente
     ↓
[Análisis Léxico] → Tokens
     ↓
[Análisis Sintáctico] → AST
     ↓
[Análisis Semántico] → Validación de tipos
     ↓
[Generación TAC] → Código Intermedio
     ↓
[Optimización] → TAC Optimizado
     ↓
[Generación de Código Máquina] → Ensamblador
     ↓
[Interpretación/Ejecución] → Salida
```

## Licencia
Proyecto educativo

## Autor
Ricardo (2025)
