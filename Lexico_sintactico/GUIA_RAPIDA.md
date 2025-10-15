# 🚀 Guía Rápida - Compilador Interactivo de Python

## ⚡ Inicio Rápido

### Ejecutar el IDE
```bash
python python_ide.py
```

### Pasos para Compilar
1. **Escribir o cargar código** en el editor
2. **Hacer clic en "▶ Analizar"**
3. **Ver resultados** en las pestañas

## 📋 Pestañas de Resultados

### 1. Análisis Léxico
Muestra una tabla con:
- Token (valor)
- Tipo (IDENTIFIER, NUMBER, STRING, etc.)
- Línea
- Posición

### 2. Análisis Sintáctico
Visualiza el **Árbol de Sintaxis Abstracta (AST)** con estructura jerárquica del código.

### 3. Código Intermedio (TAC)
Muestra el **código de tres direcciones** generado:
- Asignaciones
- Operaciones aritméticas
- Saltos condicionales
- Etiquetas

### 4. Optimización de Código
Presenta:
- TAC optimizado
- Comparación antes/después
- **Reporte de optimizaciones aplicadas**

### 5. Salida de Ejecución
Muestra el **resultado final** del programa ejecutado.

### 6. Reglas y Gramática
Documentación de:
- Gramática del lenguaje
- Reglas de optimización

## 🎯 Ejemplos Precargados

### Fibonacci
Calcula la serie de Fibonacci hasta N términos.
```python
n = 10
a = 0
b = 1
while i < n:
    c = a + b
    ...
```

### Búsqueda en Arreglo
Busca un elemento en una lista.
```python
numeros = [10, 25, 30, 45, 50]
buscando = 45
# Búsqueda lineal
```

### Procesamiento de Listas
Calcula suma, promedio y filtra elementos.
```python
numeros = [10, 20, 30, 40, 50]
suma = 0
# Procesa la lista
```

## 📝 Sintaxis Soportada

### Variables
```python
x = 10
nombre = "Python"
lista = [1, 2, 3]
```

### Condicionales
```python
if condicion:
    # bloque
elif otra_condicion:
    # bloque
else:
    # bloque
```

### Bucles
```python
# While
while condicion:
    # bloque

# For con range
for i in range(10):
    # bloque

# For con lista
for item in lista:
    # bloque
```

### Listas
```python
lista = [1, 2, 3]
elemento = lista[0]
lista.append(4)
tamanio = len(lista)
```

### Operadores
```python
# Aritméticos
resultado = a + b - c * d / e % f

# Comparación
if x == y:
    ...
if x != y:
    ...
if x < y:
    ...
```

### Impresión
```python
print("Texto")
print(variable)
print(expresion)
```

## 🔧 Optimizaciones Automáticas

El compilador aplica automáticamente:

1. **Plegado de Constantes**
   - `2 + 3` → `5`

2. **Propagación de Constantes**
   - `x = 5; y = x + 3` → `x = 5; y = 8`

3. **Eliminación de Código Muerto**
   - Remueve variables temporales no usadas

4. **Reducción de Fuerza**
   - `x * 1` → `x`
   - `x + 0` → `x`
   - `x * 0` → `0`

5. **Eliminación de Asignaciones Redundantes**
   - `x = x` → (eliminado)

6. **Eliminación de Saltos Innecesarios**
   - Optimiza el flujo de control

## 📊 Interpretando Resultados

### Tabla de Tokens (Análisis Léxico)
```
Token                Tipo                     Línea      Posición
--------------------------------------------------------------------------------
x                    IDENTIFIER               1          1
=                    ASSIGN                   1          3
10                   NUMBER                   1          5
```

### AST (Análisis Sintáctico)
```
├─ ProgramNode
│  ├─ AssignmentNode
│  │  ├─ Variable: x
│  │  └─ Expresión:
│  │     └─ NumberNode
│  │        └─ Valor: 10
```

### TAC (Código Intermedio)
```
  0: x = 10
  1: y = 5
  2: t0 = x + y
  3: print(t0)
```

### TAC Optimizado
```
  0: x = 10
  1: y = 5
  2: t0 = 15          # Optimización: plegado de constantes
  3: print(t0)
```

### Salida
```
15
```

## ❓ Solución de Problemas

### Error: "Error Léxico"
- Verifica caracteres inválidos
- Revisa strings sin cerrar
- Comprueba la sintaxis

### Error: "Error Sintáctico"
- Verifica la indentación
- Revisa los dos puntos (:) después de if, while, for
- Comprueba paréntesis balanceados

### Error: "Error de Ejecución"
- División por cero
- Índice fuera de rango
- Variable no definida

## 💡 Tips y Trucos

1. **Usa indentación de 4 espacios** (estándar Python)
2. **Carga ejemplos** para ver la sintaxis correcta
3. **Revisa las pestañas en orden** para entender el proceso
4. **Compara TAC original vs optimizado** para ver mejoras
5. **Lee el reporte de optimizaciones** para aprender

## 🎓 Propósito Educativo

Este compilador es una herramienta educativa que muestra:
- Cómo funciona un compilador por dentro
- Las fases de compilación
- Técnicas de optimización
- Representación intermedia (TAC)
- Ejecución de código

## 📚 Recursos Adicionales

- `README_COMPILADOR.md` - Documentación completa
- Pestaña "Reglas y Gramática" - Referencia del lenguaje
- Ejemplos incluidos - Código de muestra

---

**¡Disfruta compilando! 🎉**

