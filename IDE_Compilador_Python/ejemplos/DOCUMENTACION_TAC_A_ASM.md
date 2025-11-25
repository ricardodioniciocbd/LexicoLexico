# Documentación: Conversión de TAC a Código Ensamblador

## 📋 Resumen General

Este documento describe el proceso de conversión de código TAC (Three Address Code) a código ensamblador x86 de 16 bits compatible con emu8086, implementado en el compilador de Python.

## 🔄 Flujo del Compilador

```
Python → AST → TAC → Optimización → ASM (x86 16 bits)
```

### 1. **Análisis Léxico y Sintáctico**
- El código Python se tokeniza y se construye un AST (Árbol de Sintaxis Abstracta)
- Se identifican funciones, variables, operaciones, estructuras de control, etc.

### 2. **Generación de TAC (Three Address Code)**
- El AST se convierte en código intermedio de tres direcciones
- Cada instrucción TAC tiene la forma: `resultado = operando1 operador operando2`
- Ejemplos de instrucciones TAC:
  - `ASSIGN`: Asignación de valores
  - `ADD`, `SUB`, `MUL`, `DIV`, `MOD`: Operaciones aritméticas
  - `EQ`, `NEQ`, `LT`, `GT`: Comparaciones
  - `CALL`: Llamadas a funciones
  - `RETURN`: Retorno de funciones
  - `LIST_GET`, `LIST_SET`: Operaciones con listas
  - `DICT_GET`, `DICT_SET`: Operaciones con diccionarios

### 3. **Optimización de TAC**
- Se aplican optimizaciones como:
  - Plegado de constantes
  - Propagación de constantes
  - Eliminación de código muerto
  - Reducción de fuerza

### 4. **Generación de Código Ensamblador**
- El TAC optimizado se convierte en código ensamblador x86 de 16 bits
- Se generan dos secciones principales:
  - **`.data`**: Declaración de variables, strings y estructuras de datos
  - **`.code`**: Instrucciones de código ejecutable

## 🎯 Proceso de Conversión TAC → ASM

### Fase 1: Recopilación de Información
```python
collect_variables_and_strings(tac_instructions)
```
- Identifica todas las variables utilizadas
- Detecta strings literales y los mapea a etiquetas
- Identifica funciones y sus parámetros
- Detecta patrones especiales (CRUD, diccionarios)

### Fase 2: Generación de Sección de Datos
- **Variables simples**: Se declaran como `DW` (word) o `DB` (byte)
- **Strings**: Se almacenan como cadenas terminadas en `$`
- **Listas**: Se implementan como arrays en memoria
- **Diccionarios**: Se implementan como estructuras con claves y valores

### Fase 3: Generación de Código
Cada instrucción TAC se traduce a instrucciones ensamblador:

| TAC | ASM |
|-----|-----|
| `ASSIGN` | `MOV destino, origen` |
| `ADD` | `MOV AX, op1`<br>`ADD AX, op2`<br>`MOV resultado, AX` |
| `CALL len()` | Llamada a procedimiento que calcula longitud |
| `CALL print()` | Llamada a procedimiento de impresión |
| `IF_FALSE` | `CMP condición, 0`<br>`JE etiqueta` |
| `LIST_GET` | Cálculo de offset y acceso a memoria |

## 🔧 Modos Especiales de Generación

### Modo CRUD Simple
Se activa automáticamente cuando se detectan funciones: `menu`, `alta`, `baja`, `modificar`, `listar`

**Características:**
- Genera estructuras de datos para gestión de estudiantes
- Implementa menú interactivo con entrada de usuario
- Maneja operaciones CRUD completas
- Usa buffers de entrada para capturar datos

**Ejemplo:** `Sistema_de_gestion_d_estudiantes.py`

### Modo Diccionarios
Se activa cuando se detectan operaciones con diccionarios (`DICT_GET`, `DICT_SET`)

**Características:**
- Mapea strings literales a etiquetas en la sección de datos
- Implementa funciones helper para búsqueda y actualización
- Maneja acceso por claves string

**Ejemplo:** `Sistema_inventario_DICCIONARIO.py`

### Modo Estándar
Para programas simples sin patrones especiales:
- Generación directa de código ASM
- Manejo de funciones básicas
- Operaciones aritméticas y lógicas estándar

**Ejemplos:** `Factorial_con_recursion.py`, `Sistema_de_procesamiento_d_cadenas.py`

## 📝 Ejemplos Soportados

### 1. **Factorial con Recursión**
- Demuestra llamadas recursivas
- Manejo de parámetros y valores de retorno
- Stack de llamadas

### 2. **Sistema de Gestión de Estudiantes**
- Modo CRUD completo
- Menú interactivo
- Operaciones de alta, baja, modificación y listado

### 3. **Sistema de Inventario Simple**
- Manejo de listas paralelas
- Operaciones de búsqueda y actualización
- Cálculos con arrays

### 4. **Sistema de Inventario con Diccionarios**
- Uso de diccionarios
- Acceso por claves string
- Operaciones de actualización

### 5. **Procesamiento de Cadenas**
- Operaciones con strings
- Funciones de manipulación de texto
- Menú interactivo

## 🛠️ Funciones Helper Generadas

El generador crea automáticamente funciones helper en ASM:

- **`print_string`**: Imprime una cadena terminada en `$`
- **`print_number`**: Convierte número a string e imprime
- **`input_string`**: Lee entrada del usuario
- **`str_to_int`**: Convierte string a entero
- **`int_to_str`**: Convierte entero a string
- **`len_string`**: Calcula longitud de string
- **`find_dict_key`**: Busca clave en diccionario (modo diccionarios)

## ⚙️ Mapeo de Variables y Registros

- **Variables temporales** (`t0`, `t1`, ...): Se asignan a registros (AX, BX, CX, DX, SI, DI) cuando es posible
- **Variables globales**: Se almacenan en memoria con nombres únicos
- **Parámetros de función**: Se pasan mediante registros o memoria según el contexto

## 📌 Consideraciones Importantes

1. **Compatibilidad**: El código generado es compatible con emu8086
2. **Límites**: 
   - Registros de 16 bits
   - Memoria limitada
   - Strings terminados en `$`
3. **Optimizaciones**: Se evitan asignaciones redundantes y se optimiza el uso de registros
4. **Funciones**: Se implementan como procedimientos con etiquetas `func_nombre:`

## 🔍 Estructura del Código ASM Generado

```asm
.model small
.stack 100h

.data
    ; Variables y strings aquí

.code
    mov ax, @data
    mov ds, ax
    
    ; Código principal
    call func_main
    
    ; Funciones helper
    print_string proc
        ; ...
    print_string endp
    
    ; Funciones del programa
    func_main proc
        ; ...
    func_main endp
```

## 📚 Referencias

- `machine_code_generator.py`: Implementación principal del generador
- `tac_generator.py`: Generación de código TAC desde AST
- `tac_interpreter.py`: Intérprete de código TAC (para ejecución directa)
- Ejemplos en `IDE_Compilador_Python/ejemplos/`

