# 📋 LIMITACIONES Y CARACTERÍSTICAS DEL COMPILADOR PYTHON

## ✅ CARACTERÍSTICAS SOPORTADAS

### 🔹 Estructuras de Control
- ✅ `if`, `elif`, `else` - Condicionales
- ✅ `while` - Bucle while
- ✅ `for ... in range()` - Bucle for con range
- ✅ `for ... in lista` - Bucle for iterando listas

### 🔹 Tipos de Datos
- ✅ Números (int y float)
- ✅ Strings (cadenas de texto)
- ✅ Listas `[]`
- ✅ Diccionarios `{}` (literales básicos)
- ✅ `True`, `False`, `None`

### 🔹 Operadores
- ✅ Aritméticos: `+`, `-`, `*`, `/`, `%`, `**`
- ✅ Comparación: `==`, `!=`, `<`, `>`, `<=`, `>=`
- ✅ Lógicos: `not` (negación booleana)
- ✅ Asignación: `=`

### 🔹 Funciones
- ✅ `print()` - Imprimir
- ✅ `input()` - Entrada de usuario
- ✅ `len()` - Longitud de listas/strings
- ✅ `int()`, `float()`, `str()` - Conversiones
- ✅ `range()` - Generar rangos
- ✅ `append()` - Agregar a listas (método)

### 🔹 Definición de Funciones
- ✅ `def nombre(param1, param2):` - Definir funciones
- ✅ `return` - Retornar valores
- ✅ Llamadas a funciones personalizadas

### 🔹 Acceso a Elementos
- ✅ `lista[indice]` - Acceso por índice a listas
- ✅ `diccionario["clave"]` - Acceso a diccionarios con literales de string

---

## ❌ CARACTERÍSTICAS NO SOPORTADAS

### 🔸 Palabras Clave Ausentes
- ❌ `del` - No se puede eliminar elementos/variables
- ❌ `and`, `or` - Operadores lógicos (solo `not` está)
- ❌ `pass` - Sentencia vacía
- ❌ `continue` - Saltar iteración
- ❌ `break` - Token existe pero no implementado en parser
- ❌ `try`, `except`, `finally` - Manejo de excepciones
- ❌ `class` - Programación orientada a objetos
- ❌ `import` - Importar módulos
- ❌ `with` - Gestores de contexto
- ❌ `lambda` - Funciones anónimas
- ❌ `global`, `nonlocal` - Declaración de ámbito

### 🔸 Operaciones Avanzadas
- ❌ `in` para membership test (solo en `for...in`)
- ❌ Slicing de listas `lista[1:3]`
- ❌ Comprensión de listas `[x for x in lista]`
- ❌ Operadores de asignación compuestos `+=`, `-=`, etc.
- ❌ Operador ternario `x if condition else y`
- ❌ Múltiples asignaciones `a, b = 1, 2`
- ❌ Desempaquetado `a, *rest = lista`

### 🔸 Métodos y Funciones Built-in
- ❌ `.remove()` - Token existe pero no implementado
- ❌ `.pop()`, `.insert()`, `.sort()`
- ❌ `.keys()`, `.values()`, `.items()` para diccionarios
- ❌ `format()`, f-strings
- ❌ `open()`, `read()`, `write()` - Archivos (tokens existen pero no implementados)
- ❌ `type()`, `isinstance()`
- ❌ `min()`, `max()`, `sum()`

### 🔸 Estructuras de Datos
- ❌ Sets `{1, 2, 3}`
- ❌ Tuplas `(1, 2, 3)`
- ❌ Diccionarios anidados complejos
- ❌ Diccionarios dinámicos (inventario global)

---

## 🎯 RECOMENDACIONES PARA ESCRIBIR CÓDIGO COMPATIBLE

### ✅ HACER:

```python
# 1. Usar listas paralelas en lugar de diccionarios complejos
codigos = ["P001", "P002"]
precios = [100, 200]

# 2. Usar bucles while para búsqueda
i = 0
while i < len(codigos):
    if codigos[i] == "P001":
        print("Encontrado")
    i = i + 1

# 3. Comparaciones booleanas explícitas
if encontrado == 1:
    print("Si")

# 4. Concatenación de listas para "agregar"
lista = lista + [nuevo_elemento]

# 5. Diccionarios literales simples
producto = {"nombre": "Laptop", "precio": 1000}
precio = producto["precio"]
```

### ❌ EVITAR:

```python
# 1. NO usar 'del'
del inventario[codigo]  # ❌ NO FUNCIONA

# 2. NO usar 'in' para membership
if "P001" in codigos:  # ❌ NO FUNCIONA

# 3. NO usar 'and', 'or'
if x > 0 and y < 10:  # ❌ NO FUNCIONA

# 4. NO usar operadores compuestos
x += 1  # ❌ NO FUNCIONA
# Usar: x = x + 1

# 5. NO usar diccionarios dinámicos como base de datos
inventario = {}
inventario[codigo] = producto  # ❌ LIMITADO

# 6. NO usar métodos complejos de listas
lista.remove(elemento)  # ❌ NO IMPLEMENTADO
lista.pop()             # ❌ NO IMPLEMENTADO
```

---

## 📊 COMPARACIÓN: CÓDIGO ORIGINAL VS COMPATIBLE

### ❌ ORIGINAL (Sistema_de_inventario_structs.py)
```python
inventario = {}

def agregar():
    codigo = input("Código: ")
    producto = {"desc": desc, "precio": int(precio)}
    inventario[codigo] = producto  # Diccionario dinámico

def eliminar():
    if codigo in inventario:  # 'in' para membership
        del inventario[codigo]  # 'del' keyword
```

### ✅ COMPATIBLE (Sistema_inventario_SIMPLE.py)
```python
codigos = []
descripciones = []
precios = []

# Agregar producto
codigos = codigos + ["P001"]
descripciones = descripciones + ["Laptop"]
precios = precios + [1200]

# Eliminar producto (buscar y recrear listas)
i = 0
nuevos_codigos = []
while i < len(codigos):
    if codigos[i] != "P001":
        nuevos_codigos = nuevos_codigos + [codigos[i]]
    i = i + 1
codigos = nuevos_codigos
```

---

## 🔍 ARCHIVOS DE EJEMPLO INCLUIDOS

| Archivo | Descripción | Complejidad |
|---------|-------------|-------------|
| `Sistema_de_inventario_structs.py` | ❌ Original - NO COMPATIBLE | Alta |
| `Sistema_inventario_SIMPLE.py` | ✅ Versión simplificada con listas paralelas | Media |
| `Sistema_inventario_DICCIONARIO.py` | ✅ Demostración básica de diccionarios | Baja |

---

## 💡 CONCLUSIÓN

El compilador soporta un **subconjunto básico de Python** enfocado en:
- Estructuras de control fundamentales
- Operaciones aritméticas y comparaciones
- Listas y diccionarios literales simples
- Funciones definidas por el usuario

Para código complejo, es necesario **simplificar** y **adaptar** usando:
- Listas paralelas en lugar de diccionarios anidados
- Bucles while para búsquedas
- Variables de flag (0/1) en lugar de booleanos
- Operaciones explícitas en lugar de métodos complejos

