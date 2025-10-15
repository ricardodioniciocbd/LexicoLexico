# Compilador Interactivo de Python

## Descripción

Este es un compilador interactivo completo para un subconjunto de Python que incluye:

- **Análisis Léxico**: Tokenización del código fuente
- **Análisis Sintáctico**: Construcción del Árbol de Sintaxis Abstracta (AST)
- **Generación de Código Intermedio**: Producción de código de tres direcciones (TAC)
- **Optimización de Código**: Aplicación de múltiples técnicas de optimización
- **Ejecución**: Interpretación y ejecución del código optimizado

## Características Principales

### 🔍 Análisis Léxico
- Reconocimiento de tokens de Python
- Manejo de indentación (INDENT/DEDENT)
- Soporte para números, strings, identificadores y operadores
- Detección de palabras reservadas

### 🌳 Análisis Sintáctico
- Parser recursivo descendente
- Construcción de AST completo
- Soporte para:
  - Asignaciones
  - Condicionales (if/elif/else)
  - Bucles (while, for)
  - Listas y acceso por índice
  - Expresiones aritméticas y de comparación

### ⚙️ Generación de Código Intermedio (TAC)
- Código de tres direcciones
- Variables temporales
- Etiquetas para control de flujo
- Instrucciones optimizadas para interpretación

### 🚀 Optimización de Código
1. **Plegado de Constantes**: Evalúa operaciones constantes en compilación
2. **Propagación de Constantes**: Reemplaza variables con valores conocidos
3. **Eliminación de Código Muerto**: Remueve instrucciones sin efecto
4. **Reducción de Fuerza**: Simplifica operaciones costosas
5. **Eliminación de Asignaciones Redundantes**: Remueve x = x
6. **Eliminación de Saltos Innecesarios**: Optimiza el flujo de control

### ▶️ Ejecución
- Intérprete completo de TAC
- Soporte para variables, listas y operaciones
- Salida de resultados con print()

## Instalación

### Requisitos
- Python 3.7 o superior
- Tkinter (incluido con Python en Windows)

### Instrucciones
```bash
# Clonar o descargar el repositorio
cd Lexico_sintactico

# Ejecutar el IDE
python python_ide.py
```

## Uso

### Interfaz Gráfica

El IDE incluye:

1. **Editor de Código**: Editor con números de línea para escribir código Python
2. **Botón Analizar**: Ejecuta todas las fases del compilador
3. **Selector de Ejemplos**: Carga ejemplos precargados
4. **Pestañas de Salida**:
   - **Análisis Léxico**: Tabla de tokens
   - **Análisis Sintáctico**: Árbol AST
   - **Código Intermedio**: TAC generado
   - **Optimización**: TAC optimizado con reporte
   - **Salida de Ejecución**: Resultado del programa
   - **Reglas y Gramática**: Documentación

### Ejemplos Incluidos

#### 1. Serie de Fibonacci
Calcula y muestra los primeros N números de la serie de Fibonacci.

#### 2. Búsqueda en Arreglo
Busca un elemento en una lista y muestra su posición.

#### 3. Procesamiento de Listas
Calcula suma, promedio y filtra números pares de una lista.

## Sintaxis Soportada

### Variables y Asignación
```python
x = 10
nombre = "Python"
lista = [1, 2, 3, 4, 5]
```

### Condicionales
```python
if x > 5:
    print("Mayor que 5")
elif x == 5:
    print("Igual a 5")
else:
    print("Menor que 5")
```

### Bucles
```python
# While
while contador < 10:
    print(contador)
    contador = contador + 1

# For con range
for i in range(5):
    print(i)

# For con lista
for num in numeros:
    print(num)
```

### Listas
```python
lista = [10, 20, 30]
elemento = lista[0]
lista.append(40)
tamanio = len(lista)
```

### Operadores
```python
# Aritméticos: +, -, *, /, %
resultado = (a + b) * c

# Comparación: ==, !=, <, >, <=, >=
if x == y:
    print("Iguales")
```

### Impresión
```python
print("Hola Mundo")
print(variable)
print(expresion + 10)
```

## Arquitectura del Compilador

```
Código Fuente
     ↓
[Análisis Léxico] → Tokens
     ↓
[Análisis Sintáctico] → AST
     ↓
[Generación TAC] → Código Intermedio
     ↓
[Optimización] → TAC Optimizado
     ↓
[Interpretación] → Salida
```

## Archivos del Proyecto

- `python_ide.py`: Interfaz gráfica principal
- `python_compiler.py`: Lexer, Parser y nodos AST
- `tac_generator.py`: Generador de código intermedio
- `tac_optimizer.py`: Optimizador de código TAC
- `tac_interpreter.py`: Intérprete de código TAC

## Ejemplos de Optimización

### Antes de Optimización
```
0: t0 = 2 + 3
1: x = t0
2: t1 = x * 1
3: y = t1
4: t2 = y + 0
5: z = t2
```

### Después de Optimización
```
0: x = 5          # Plegado de constantes: 2 + 3 = 5
1: y = x          # Reducción de fuerza: x * 1 = x
2: z = y          # Reducción de fuerza: y + 0 = y
```

## Limitaciones

Este es un compilador educativo con un subconjunto limitado de Python:
- No soporta funciones definidas por el usuario
- No soporta clases y objetos
- No soporta importaciones
- No soporta manejo de excepciones
- No soporta comprehensions
- Operaciones con strings limitadas

## Próximas Mejoras

- [ ] Soporte para funciones
- [ ] Tipos de datos adicionales (tuplas, diccionarios)
- [ ] Más operadores (and, or, not)
- [ ] Generación de código assembly
- [ ] Análisis de complejidad
- [ ] Depurador interactivo

## Contribuir

Este es un proyecto educativo. Sugerencias y mejoras son bienvenidas.

## Licencia

Proyecto educativo de código abierto.

## Autor

Compilador desarrollado como herramienta educativa para el curso de Compiladores.

---

**Fecha**: Octubre 2024
**Versión**: 1.0.0

