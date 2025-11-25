# 📘 Guía de Uso Completa - MiniLang IDE

## 🎯 Introducción

MiniLang IDE es un compilador educativo completo que demuestra todas las fases de compilación con énfasis en **acciones semánticas**. Esta guía te ayudará a aprovechar al máximo todas sus características.

## 🚀 Iniciar el IDE

### Método 1: Línea de comandos
```bash
cd c:\Cursos\AccionesSemanticas_py
python minilang_ide.py
```

### Método 2: Doble clic
Haz doble clic en `minilang_ide.py` (si tienes Python asociado con archivos .py)

## 🖥️ Interfaz del IDE

### Barra de Herramientas Superior

| Botón | Función | Descripción |
|-------|---------|-------------|
| **▶ Compilar** | Compilar código | Ejecuta todas las fases de compilación |
| **🗑 Limpiar** | Limpiar salida | Borra todas las pestañas de salida |
| **📄 Ejemplo** | Cargar ejemplo | Carga código de ejemplo en el editor |
| **💾 Guardar** | Guardar archivo | Guarda el código en un archivo .ml |
| **📂 Abrir** | Abrir archivo | Abre un archivo existente |

### Panel Izquierdo: Editor de Código

- **Números de línea**: Se actualizan automáticamente
- **Sintaxis**: Tipo Python con indentación significativa
- **Scroll sincronizado**: Los números de línea se mueven con el código
- **Fuente**: Consolas (monoespaciada) tamaño 11

### Panel Derecho: Pestañas de Salida

#### 1️⃣ Pestaña "Tokens"
**Muestra**: Todos los tokens generados por el análisis léxico

**Formato**:
```
Tipo                 Valor                Línea      Columna    
--------------------------------------------------------------------------------
IDENTIFIER           x                    1          1         
ASSIGN               =                    1          3         
NUMBER               10                   1          5         
```

**Información**:
- Tipo de token (IDENTIFIER, NUMBER, STRING, etc.)
- Valor del token
- Posición en el código (línea y columna)
- Total de tokens al final

#### 2️⃣ Pestaña "AST"
**Muestra**: Árbol de Sintaxis Abstracta (Abstract Syntax Tree)

**Formato jerárquico**:
```
ProgramNode
  AssignmentNode
    identifier: x
    expression:
      NumberNode
        value: 10
```

**Información**:
- Estructura del programa
- Jerarquía de nodos
- Valores y relaciones

#### 3️⃣ Pestaña "Análisis Semántico"
**Muestra**: Tabla de símbolos, errores y advertencias

**Secciones**:

1. **Tabla de Símbolos**:
```
Variable             Tipo            Inicializada   
--------------------------------------------------------------------------------
x                    int             Sí             
nombre               string          Sí             
```

2. **Errores Semánticos** (si existen):
```
❌ Semantic Error at line 5: Undefined variable: 'z'
❌ Semantic Error at line 7: Type mismatch in operation: int + string
```

3. **Advertencias** (si existen):
```
⚠ Warning at line 10: Comparing different types: int == string
```

#### 4️⃣ Pestaña "Código Generado"
**Muestra**: Código de tres direcciones (intermedio)

**Formato**:
```
# MiniLang Compiled Code
# Three-Address Code Representation

x = 10
y = 5
t0 = x + y
suma = t0
PRINT suma
```

**Elementos**:
- Asignaciones directas
- Variables temporales (t0, t1, t2...)
- Etiquetas para saltos (L0, L1, L2...)
- Instrucciones de control (IF_FALSE, GOTO, PRINT)

#### 5️⃣ Pestaña "Reglas Semánticas"
**Muestra**: Tabla interactiva de 38 reglas semánticas

**Selector de Fase**:
- ⚪ Análisis Léxico (7 reglas)
- ⚪ Análisis Sintáctico (10 reglas)
- ⚪ Análisis Semántico (10 reglas)
- ⚪ Generación de Código (8 reglas)

**Tabla de Reglas**:
| ID | Regla Gramatical | Producción | Acción Semántica |
|----|------------------|------------|------------------|
| L01 | Identificador | IDENTIFIER → ... | Crear token... |

**Panel de Detalles** (parte inferior):
Al hacer clic en una regla, se muestra:
- ID de la regla
- Fase de compilación
- Regla gramatical completa
- Producción formal
- Acción semántica detallada
- Ejemplo concreto de uso

#### 6️⃣ Pestaña "Gramática"
**Muestra**: Documentación completa de la gramática de MiniLang

**Contenido**:
- Reglas de producción completas
- Lista de tokens
- Palabras reservadas
- Operadores
- Delimitadores

### Barra de Estado Inferior

**Colores y significados**:
- 🔵 **Azul**: Estado normal / Información
- 🟢 **Verde**: Compilación exitosa
- 🟡 **Amarillo**: Compilando / Procesando
- 🔴 **Rojo**: Error de compilación

## 📝 Escribir Código en MiniLang

### Reglas de Sintaxis

#### 1. Variables
```python
# Declaración implícita (primera asignación)
x = 10
nombre = "Juan"
precio = 19.99

# Declaración explícita (opcional)
var contador = 0
```

#### 2. Tipos de Datos

**Números**:
```python
entero = 42
flotante = 3.14
negativo = -10
```

**Strings**:
```python
comillas_dobles = "Hola Mundo"
comillas_simples = 'Hola Mundo'
concatenacion = "Hola" + " " + "Mundo"
```

#### 3. Operaciones Aritméticas

```python
suma = 10 + 5        # 15
resta = 10 - 5       # 5
multiplicacion = 10 * 5  # 50
division = 10 / 5    # 2.0

# Con paréntesis para precedencia
resultado = (10 + 5) * 2  # 30
```

#### 4. Operaciones de Comparación

```python
igual = x == y       # Igualdad
diferente = x != y   # Desigualdad
menor = x < y        # Menor que
mayor = x > y        # Mayor que
menor_igual = x <= y # Menor o igual
mayor_igual = x >= y # Mayor o igual
```

#### 5. Condicionales

**If simple**:
```python
if x > 0:
    print("Positivo")
```

**If-else**:
```python
if x > 0:
    print("Positivo")
else:
    print("No positivo")
```

**If-elif-else**:
```python
if x > 0:
    print("Positivo")
elif x < 0:
    print("Negativo")
else:
    print("Cero")
```

**Importante**: 
- Siempre terminar la línea con `:`
- Indentar el bloque (4 espacios recomendado)

#### 6. Bucle For

```python
# Sintaxis básica
for i in range(10):
    print(i)

# Con variable
limite = 5
for contador in range(limite):
    print("Iteración: " + str(contador))
```

**Nota**: `range(n)` genera números de 0 a n-1

#### 7. Bucle While

```python
contador = 0
while contador < 5:
    print(contador)
    contador = contador + 1
```

**Importante**: Asegurarse de que la condición eventualmente sea falsa

#### 8. Print

```python
# Imprimir string
print("Hola Mundo")

# Imprimir variable
print(x)

# Concatenar (convertir números a string)
print("El valor es: " + str(x))
```

#### 9. Comentarios

```python
# Esto es un comentario de una línea
x = 10  # Comentario al final de la línea

// También se pueden usar barras dobles
y = 5  // Otro comentario
```

### Indentación

**Correcto** ✅:
```python
if x > 0:
    print("Positivo")
    y = x + 1
```

**Incorrecto** ❌:
```python
if x > 0:
print("Positivo")  # Error: falta indentación
    y = x + 1
```

## 🎯 Flujo de Trabajo Recomendado

### 1. Escribir Código
- Escribe tu programa en el editor
- Usa comentarios para documentar
- Verifica la indentación

### 2. Compilar
- Haz clic en "▶ Compilar"
- Observa la barra de estado

### 3. Revisar Tokens
- Ve a la pestaña "Tokens"
- Verifica que todos los tokens sean correctos
- Busca tokens inesperados

### 4. Revisar AST
- Ve a la pestaña "AST"
- Verifica la estructura del programa
- Asegúrate de que refleje tu intención

### 5. Revisar Análisis Semántico
- Ve a la pestaña "Análisis Semántico"
- Revisa la tabla de símbolos
- Corrige errores si los hay
- Atiende advertencias

### 6. Revisar Código Generado
- Ve a la pestaña "Código Generado"
- Observa el código intermedio
- Comprende cómo se traduce tu código

### 7. Estudiar Reglas
- Ve a la pestaña "Reglas Semánticas"
- Selecciona la fase relevante
- Haz clic en reglas para ver detalles
- Relaciona las reglas con tu código

## 🐛 Depuración de Errores

### Error Léxico

**Síntoma**: Mensaje "Error Léxico"

**Causas comunes**:
- Carácter no reconocido: `x = @invalid`
- String sin cerrar: `nombre = "Juan`
- Número mal formado: `x = 3.14.15`

**Solución**: Revisa el mensaje de error para ver línea y columna

### Error Sintáctico

**Síntoma**: Mensaje "Error Sintáctico"

**Causas comunes**:
- Falta `:` después de if/while/for
- Paréntesis no balanceados
- Indentación incorrecta
- Token inesperado

**Solución**: Lee el mensaje que indica qué se esperaba

### Error Semántico

**Síntoma**: Compilación completa pero con errores en "Análisis Semántico"

**Causas comunes**:
- Variable no declarada: `print(z)` sin definir z
- Incompatibilidad de tipos: `x = 5 + "texto"`
- Rango no numérico: `for i in range("abc")`

**Solución**: Revisa la tabla de símbolos y los mensajes de error

## 💡 Consejos y Mejores Prácticas

### 1. Nombres de Variables
```python
# Buenos nombres ✅
edad_usuario = 25
precio_total = 99.99
contador_iteraciones = 0

# Malos nombres ❌
x = 25
p = 99.99
c = 0
```

### 2. Comentarios
```python
# Explica el propósito, no lo obvio
# Calcular el promedio de calificaciones
suma = nota1 + nota2 + nota3
promedio = suma / 3
```

### 3. Indentación Consistente
- Usa siempre 4 espacios
- No mezcles espacios y tabs
- Configura tu editor para convertir tabs a espacios

### 4. Conversión de Tipos
```python
# Siempre convierte números a string para concatenar
edad = 25
print("Edad: " + str(edad))  # ✅ Correcto

# Esto causará error
print("Edad: " + edad)  # ❌ Error de tipos
```

### 5. Condiciones Claras
```python
# Usa comparaciones explícitas
if contador > 0:  # ✅ Claro
    print("Hay elementos")

# Aunque esto funcione, es menos claro
if contador:  # ⚠️ Menos explícito
    print("Hay elementos")
```

## 📚 Ejemplos Paso a Paso

### Ejemplo 1: Calculadora Simple

**Código**:
```python
# Calculadora simple
x = 10
y = 5

suma = x + y
resta = x - y
multiplicacion = x * y
division = x / y

print("Resultados:")
print("Suma: " + str(suma))
print("Resta: " + str(resta))
print("Multiplicación: " + str(multiplicacion))
print("División: " + str(division))
```

**Resultado esperado**:
- ✅ 7 variables en tabla de símbolos
- ✅ 4 operaciones aritméticas en AST
- ✅ 4 sentencias print
- ✅ Código generado con variables temporales

### Ejemplo 2: Clasificador de Edad

**Código**:
```python
# Clasificador de edad
edad = 18

if edad < 13:
    print("Niño")
elif edad < 18:
    print("Adolescente")
elif edad < 65:
    print("Adulto")
else:
    print("Adulto mayor")
```

**Resultado esperado**:
- ✅ 1 variable en tabla de símbolos
- ✅ IfNode con 2 elif y 1 else
- ✅ Código con etiquetas de salto

### Ejemplo 3: Tabla de Multiplicar

**Código**:
```python
# Tabla de multiplicar
numero = 7

for i in range(10):
    resultado = numero * i
    print(str(numero) + " x " + str(i) + " = " + str(resultado))
```

**Resultado esperado**:
- ✅ 2 variables en tabla de símbolos (numero, i)
- ✅ ForNode con rango 10
- ✅ Código con bucle y etiquetas

## 🎓 Aprender sobre Reglas Semánticas

### Cómo Usar la Tabla de Reglas

1. **Selecciona una fase**:
   - Léxico: Para entender tokenización
   - Sintáctico: Para entender construcción de AST
   - Semántico: Para entender verificación de tipos
   - Código: Para entender generación

2. **Explora las reglas**:
   - Lee la producción gramatical
   - Comprende la acción semántica
   - Estudia el ejemplo

3. **Relaciona con tu código**:
   - Compila tu programa
   - Identifica qué reglas se aplicaron
   - Observa el resultado en cada fase

### Ejemplo de Análisis

**Código**: `x = 10`

**Reglas aplicadas**:

1. **L01** (Léxico): Reconocer `x` como IDENTIFIER
2. **L02** (Léxico): Reconocer `10` como NUMBER
3. **P02** (Sintáctico): Crear AssignmentNode
4. **P05** (Sintáctico): Crear NumberNode(10)
5. **S01** (Semántico): Agregar `x` a tabla de símbolos
6. **C01** (Código): Generar `x = 10`

## 📊 Interpretar Resultados

### Compilación Exitosa ✅

**Indicadores**:
- Barra de estado verde: "✓ Compilación exitosa"
- Tokens generados correctamente
- AST bien formado
- Sin errores semánticos
- Código generado presente

### Compilación con Errores ❌

**Indicadores**:
- Barra de estado roja
- Mensaje de error específico
- Compilación detenida en fase con error

### Compilación con Advertencias ⚠️

**Indicadores**:
- Barra de estado verde pero con advertencias
- Compilación completa
- Advertencias en pestaña "Análisis Semántico"
- Código generado presente

## 🔧 Solución de Problemas

### El IDE no inicia

**Problema**: Al ejecutar `python minilang_ide.py` no pasa nada

**Soluciones**:
1. Verifica versión de Python: `python --version` (debe ser 3.7+)
2. Verifica tkinter: `python -c "import tkinter"`
3. Verifica que estás en el directorio correcto

### Error de importación

**Problema**: `ModuleNotFoundError: No module named 'lexer'`

**Solución**: Asegúrate de estar en el directorio del proyecto:
```bash
cd c:\Cursos\AccionesSemanticas_py
python minilang_ide.py
```

### El código no compila

**Problema**: Errores constantes al compilar

**Soluciones**:
1. Verifica la sintaxis (`:` después de if/while/for)
2. Verifica la indentación (4 espacios)
3. Verifica que las variables estén declaradas
4. Lee el mensaje de error completo

## 📞 Referencia Rápida

### Palabras Reservadas
```
print, if, elif, else, while, for, in, range, var
```

### Operadores
```
Aritméticos: + - * /
Comparación: == != < > <= >=
Asignación: =
```

### Estructura Básica
```python
# Variables
variable = valor

# Condicional
if condicion:
    codigo

# Bucle for
for i in range(n):
    codigo

# Bucle while
while condicion:
    codigo

# Print
print(expresion)
```

---

**¡Disfruta programando en MiniLang!** 🎉

Para más información, consulta:
- `README.md` - Documentación completa
- `QUICK_START.md` - Inicio rápido
- `PROJECT_SUMMARY.md` - Resumen del proyecto
