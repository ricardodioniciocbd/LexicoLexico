# 🐍 Compilador Interactivo de Python - IDE Profesional

## 🎯 Descripción Completa

Este es un compilador educativo completo para un subconjunto de Python que incluye **TODAS** las fases de compilación modernas:

### ✅ Fases Implementadas

1. **📋 Análisis Léxico** - Tokenización del código fuente
2. **🌳 Análisis Sintáctico** - Construcción del AST (Árbol de Sintaxis Abstracta)
3. **🔍 Análisis Semántico** - Verificación de variables y tipos
4. **⚙️ Generación de Código Intermedio** - Código TAC (Three Address Code)
5. **🚀 Optimización de Código** - 6 técnicas de optimización
6. **💻 Generación de Código Máquina** - Código ensamblador RISC
7. **▶️ Ejecución** - Interpretación y ejecución del código

## 🎨 Características Visuales

- ✅ **Fondo azul gradiente** profesional
- ✅ Tema oscuro con colores vibrantes
- ✅ Editor con números de línea
- ✅ 9 pestañas de análisis
- ✅ Interfaz moderna y atractiva

## 🔍 Análisis Semántico Completo

### Verificaciones Implementadas:

1. **Variables no declaradas**: Detecta uso de variables sin declarar
2. **Tipos incompatibles**: No permite sumar int con string
3. **División por cero**: Advierte sobre divisiones por cero
4. **Cambios de tipo**: Advierte cuando una variable cambia de tipo
5. **Operadores inválidos**: Verifica compatibilidad de operadores

### Ejemplo de Errores Detectados:

```python
# Error 1: Variable no declarada
print(variable_inexistente)  # ❌ Error semántico

# Error 2: Tipos incompatibles
x = 5
y = "texto"
z = x + y  # ❌ No se puede sumar int con string

# Error 3: División por cero
a = 10
b = 0
c = a / b  # ⚠️ Advertencia
```

## 📚 Reglas Semánticas Integradas

El IDE incluye una pestaña completa con las **reglas semánticas** organizadas por fases:

- **Léxico**: 7 reglas
- **Sintáctico**: 10 reglas
- **Semántico**: 10 reglas
- **Generación de Código**: 8 reglas

**Total: 35 reglas semánticas documentadas**

## 💻 Generación de Código Máquina

Después de la optimización, el compilador genera código ensamblador RISC de 32 bits:

```assembly
.data
    x: .word 0
    y: .word 0
    
.text
    .globl main
main:
    MOV R0, #5          ; Cargar constante
    STR R0, [SP, #0]    ; Almacenar en x
    MOV R1, #10
    STR R1, [SP, #4]    ; Almacenar en y
    LDR R2, [SP, #0]    ; Cargar x
    LDR R3, [SP, #4]    ; Cargar y
    ADD R4, R2, R3      ; x + y
    ...
```

## 📋 Pestañas del IDE

1. **📋 Análisis Léxico** - Tabla de tokens (Token, Tipo, Línea, Posición)
2. **🌳 Análisis Sintáctico** - Árbol AST visualizado
3. **🔍 Análisis Semántico** - Tabla de símbolos y errores
4. **⚙️ Código TAC** - Código intermedio de tres direcciones
5. **🚀 Optimización** - TAC optimizado + reporte
6. **💻 Código Máquina** - Código ensamblador generado
7. **▶️ Ejecución** - Salida del programa
8. **📚 Reglas Semánticas** - 35 reglas documentadas por fases
9. **📖 Gramática** - Gramática completa del lenguaje

## 🎯 Ejemplos Incluidos

### 1. Fibonacci (Correcto)
Calcula la serie de Fibonacci perfectamente.

### 2. Búsqueda en Arreglo (Correcto)
Búsqueda lineal en una lista.

### 3. Procesamiento de Listas (Correcto)
Suma, promedio y filtrado.

### 4. Con Errores (Demostración)
**Ejemplo especial que demuestra la captura de errores en todas las fases:**

```python
# Error Léxico (comentado para no romper)
# x = 5 @@ 3  # Carácter inválido @@

# Error Sintáctico (comentado)
# if x > 0  # Falta dos puntos :
#     print(x)

# Error Semántico: Variable no declarada
print(variable_no_declarada)

# Error Semántico: Tipos incompatibles
x = 5
y = "texto"
z = x + y  # No se puede sumar int con string

# Advertencia Semántica: División por cero
a = 10
b = 0
c = a / b
```

**Al ejecutar este ejemplo, se mostrarán:**
- ✅ Análisis Léxico: Completado
- ✅ Análisis Sintáctico: Completado
- ❌ Análisis Semántico: 3 errores detectados
- ⚠️ La compilación se detiene con reporte de errores

## 🚀 Optimizaciones Aplicadas

El compilador aplica automáticamente:

1. **Plegado de Constantes**: `2 + 3` → `5`
2. **Propagación de Constantes**: Reemplaza variables con valores conocidos
3. **Eliminación de Código Muerto**: Remueve instrucciones innecesarias
4. **Reducción de Fuerza**: `x * 1` → `x`, `x + 0` → `x`, `x * 0` → `0`
5. **Eliminación de Asignaciones Redundantes**: `x = x` eliminado
6. **Eliminación de Saltos Innecesarios**: Optimiza flujo de control

## 📊 Arquitectura del Compilador

```
Código Fuente Python
         ↓
[Análisis Léxico] → Tokens
         ↓
[Análisis Sintáctico] → AST
         ↓
[Análisis Semántico] → Verificaciones
         ↓                (¿Errores?)
[Generación TAC] → Código Intermedio      ↓ SÍ → DETENER
         ↓                                 ↓ NO
[Optimización] → TAC Optimizado           ↓
         ↓                                 ↓
[Generación Código Máquina] → ASM         ↓
         ↓                                 ↓
[Interpretación] → Salida                 ↓
```

## 💾 Archivos del Proyecto

### Núcleo del Compilador:
- `python_compiler.py` - Lexer, Parser y nodos AST
- `semantic_analyzer.py` - Analizador semántico completo
- `tac_generator.py` - Generador de código intermedio
- `tac_optimizer.py` - Optimizador de código
- `tac_interpreter.py` - Intérprete de TAC
- `machine_code_generator.py` - Generador de código máquina
- `reglas_semanticas.py` - Base de datos de reglas semánticas

### Interfaz:
- `python_ide_complete.py` - **⭐ IDE COMPLETO (EJECUTAR ESTE)**

## 🎮 Cómo Usar

### Ejecutar el IDE:
```bash
python python_ide_complete.py
```

### Pasos:
1. **Cargar un ejemplo** usando los radio buttons
2. **Hacer clic en "▶ ANALIZAR"**
3. **Revisar las 9 pestañas** de resultados
4. **Ver errores** en la pestaña correspondiente si los hay

### Probar Errores:
1. Seleccionar "Con Errores" en los ejemplos
2. Hacer clic en "▶ ANALIZAR"
3. Ver cómo se detectan los errores semánticos
4. La compilación se detiene y muestra el reporte

## 🎓 Características Educativas

### Reglas Semánticas Visibles:
- Cada fase tiene sus reglas documentadas
- Incluye ejemplos de cada regla
- Organizadas en pestañas por fase
- Totalmente accesibles desde el IDE

### Análisis Semántico Completo:
- Tabla de símbolos con todas las variables
- Lista de errores con número de línea
- Advertencias para casos problemáticos
- Detección de múltiples tipos de errores

### Generación de Código Máquina:
- Código ensamblador RISC real
- Asignación de registros
- Gestión de memoria
- Llamadas a funciones del sistema

## 🔧 Requisitos

- Python 3.7 o superior
- Tkinter (incluido con Python)
- No requiere dependencias externas

## ✨ Mejoras Implementadas

Comparado con versiones anteriores:

✅ Fondo azul gradiente profesional
✅ Análisis semántico completo
✅ Reglas semánticas integradas en el IDE
✅ Generación de código máquina
✅ Ejemplo con errores para demostración
✅ Verificación de variables no declaradas
✅ Verificación de tipos compatibles
✅ Tabla de símbolos completa
✅ 9 pestañas de análisis
✅ Interfaz moderna y atractiva

## 📈 Estadísticas del Proyecto

- **Líneas de código**: ~3500+
- **Archivos**: 8 módulos principales
- **Fases de compilación**: 7
- **Reglas semánticas**: 35
- **Optimizaciones**: 6 técnicas
- **Ejemplos**: 4 (3 correctos + 1 con errores)
- **Pestañas del IDE**: 9

## 🎯 Casos de Uso

### Para Estudiantes:
- Aprender cómo funciona un compilador
- Ver todas las fases de compilación
- Entender el análisis semántico
- Estudiar optimizaciones de código

### Para Profesores:
- Herramienta educativa completa
- Demostración de conceptos
- Ejemplos con y sin errores
- Visualización de cada fase

### Para Desarrolladores:
- Base para compiladores más complejos
- Referencia de implementación
- Código bien documentado
- Arquitectura modular

## 🏆 Logros

✅ Compilador completo funcional
✅ Análisis semántico con detección de errores
✅ Generación de código máquina
✅ Optimizaciones reales aplicadas
✅ Interfaz profesional con gradiente
✅ Ejemplos educativos completos
✅ Documentación integrada

## 📞 Notas Finales

Este compilador es una herramienta educativa completa que muestra **todas las fases de un compilador moderno**, desde el análisis léxico hasta la generación de código máquina y la ejecución.

**El análisis semántico** es especialmente completo, detectando:
- Variables no declaradas
- Tipos incompatibles en operaciones
- Advertencias sobre código problemático
- Tabla completa de símbolos

**La interfaz** es profesional y atractiva con:
- Fondo azul gradiente
- Colores vibrantes
- 9 pestañas de información
- Ejemplo con errores incluido

---

**🎉 ¡Disfruta explorando el compilador! 🎉**

**Versión**: 2.0.0 Completa
**Fecha**: Octubre 2024
**Estado**: ✅ 100% FUNCIONAL


