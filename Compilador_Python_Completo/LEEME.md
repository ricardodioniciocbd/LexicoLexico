# 🚀 Compilador MiniLang con Acciones Semánticas

## ✅ Proyecto Completado - Todo en Español

Este proyecto es un **compilador educativo completo** con interfaz gráfica profesional que demuestra todas las fases de compilación con énfasis en **acciones semánticas**.

## 📁 Estructura del Proyecto (Nombres en Español)

```
AccionesSemanticas_py/
│
├── 📄 ide_minilang.py              # Aplicación principal del IDE
├── 📄 tipos_token.py                # Definiciones de tipos de tokens
├── 📄 analizador_lexico.py          # Analizador léxico (tokenización)
├── 📄 nodos_ast.py                  # Nodos del Árbol de Sintaxis Abstracta
├── 📄 analizador_sintactico.py      # Analizador sintáctico (parser)
├── 📄 analizador_semantico.py       # Analizador semántico
├── 📄 generador_codigo.py           # Generador de código intermedio
├── 📄 reglas_semanticas.py          # Base de datos de 38 reglas semánticas
│
├── 📂 ejemplos/                     # Programas de ejemplo
│   ├── basico.ml                    # Operaciones básicas
│   ├── condicionales.ml             # Estructuras if/elif/else
│   ├── bucles.ml                    # Bucles for y while
│   └── completo.ml                  # Programa completo
│
└── 📖 Documentación (en español)
    ├── LEEME.md                     # Este archivo
    ├── README.md                    # Documentación completa
    ├── QUICK_START.md               # Inicio rápido
    ├── GUIA_USO.md                  # Guía de uso detallada
    ├── PROJECT_SUMMARY.md           # Resumen del proyecto
    └── FEATURES.md                  # Características destacadas
```

## 🎯 Características Principales

✅ **Todos los nombres de archivos en español**
✅ **Todos los comentarios en español**
✅ **Todos los nombres de variables y funciones en español**
✅ **38 reglas semánticas documentadas**
✅ **Interfaz gráfica profesional con tema oscuro**
✅ **Tabla interactiva de reglas semánticas**
✅ **6 pestañas informativas**
✅ **Ejemplos funcionales incluidos**

## 🚀 Inicio Rápido

### 1. Ejecutar el IDE

```bash
cd c:\Cursos\AccionesSemanticas_py
python ide_minilang.py
```

### 2. Usar el IDE

1. **Cargar ejemplo**: Haz clic en el botón "📄 Ejemplo"
2. **Compilar**: Haz clic en el botón "▶ Compilar"
3. **Ver resultados**: Navega por las pestañas:
   - **Tokens**: Análisis léxico
   - **AST**: Árbol de sintaxis abstracta
   - **Análisis Semántico**: Tabla de símbolos y errores
   - **Código Generado**: Código de tres direcciones
   - **Reglas Semánticas**: Tabla interactiva con 38 reglas
   - **Gramática**: Documentación de la sintaxis

## 📝 Sintaxis de MiniLang

### Ejemplo Básico

```python
# Variables
x = 10
y = 5

# Operaciones
suma = x + y
print(suma)

# Condicional
if x > y:
    print("x es mayor")
else:
    print("y es mayor")

# Bucle for
for i in range(5):
    print(i)

# Bucle while
contador = 0
while contador < 3:
    print(contador)
    contador = contador + 1
```

## 🔧 Módulos del Sistema

### 1. tipos_token.py
- Define la enumeración `TipoToken` con todos los tipos de tokens
- Define la clase `Token` para representar tokens individuales
- Mapeo de palabras reservadas en español

### 2. analizador_lexico.py
- Clase `AnalizadorLexico` para tokenización
- Método `tokenizar()` que convierte código fuente en tokens
- Manejo de indentación (INDENTAR/DESINDENTAR)
- Soporte para comentarios con `#` y `//`

### 3. nodos_ast.py
- Clases de nodos AST con nombres en español:
  - `NodoPrograma`, `NodoAsignacion`, `NodoPrint`
  - `NodoIf`, `NodoWhile`, `NodoFor`
  - `NodoOperacionBinaria`, `NodoOperacionUnaria`
  - `NodoNumero`, `NodoCadena`, `NodoIdentificador`

### 4. analizador_sintactico.py
- Clase `AnalizadorSintactico` (parser recursivo descendente)
- Métodos `analizar_*()` para cada construcción del lenguaje
- Construcción del AST con acciones semánticas

### 5. analizador_semantico.py
- Clase `AnalizadorSemantico` para verificación semántica
- Clase `TablaSimbolos` para gestión de variables
- Verificación de tipos y detección de errores

### 6. generador_codigo.py
- Clase `GeneradorCodigo` para código de tres direcciones
- Generación de variables temporales y etiquetas
- Código intermedio optimizado

### 7. reglas_semanticas.py
- Base de datos con 38 reglas semánticas
- Organizadas por fase: léxico, sintáctico, semántico, código
- Cada regla incluye: ID, gramática, producción, acción, ejemplo

### 8. ide_minilang.py
- Aplicación principal con interfaz gráfica
- Tema oscuro profesional estilo VS Code
- 6 pestañas de salida
- Tabla interactiva de reglas semánticas
- Editor con números de línea

## 🎨 Interfaz del IDE

### Colores del Tema Oscuro
- Fondo oscuro: `#1e1e1e`
- Fondo medio: `#252526`
- Texto primario: `#d4d4d4`
- Acento azul: `#007acc`
- Acento verde: `#4ec9b0`
- Acento amarillo: `#dcdcaa`

### Botones de la Barra de Herramientas
- **▶ Compilar**: Ejecuta todas las fases de compilación
- **🗑 Limpiar**: Limpia todas las pestañas de salida
- **📄 Ejemplo**: Carga código de ejemplo
- **💾 Guardar**: Guarda el código en archivo .ml
- **📂 Abrir**: Abre un archivo existente

## 📊 Tabla de Reglas Semánticas

El IDE incluye una tabla interactiva con **38 reglas semánticas**:

| Fase | Cantidad | IDs |
|------|----------|-----|
| Análisis Léxico | 7 reglas | L01-L07 |
| Análisis Sintáctico | 10 reglas | P01-P10 |
| Análisis Semántico | 10 reglas | S01-S10 |
| Generación de Código | 8 reglas | C01-C08 |

### Características de la Tabla
- ✅ Filtrado por fase de compilación
- ✅ Selección de reglas para ver detalles
- ✅ Panel de detalles con información completa
- ✅ Ejemplos concretos para cada regla

## 🔍 Fases de Compilación

### 1. Análisis Léxico
- **Entrada**: Código fuente (string)
- **Proceso**: Tokenización
- **Salida**: Lista de tokens
- **Reglas**: L01-L07

### 2. Análisis Sintáctico
- **Entrada**: Lista de tokens
- **Proceso**: Parser recursivo descendente
- **Salida**: Árbol de Sintaxis Abstracta (AST)
- **Reglas**: P01-P10

### 3. Análisis Semántico
- **Entrada**: AST
- **Proceso**: Verificación de tipos, tabla de símbolos
- **Salida**: Errores/advertencias, tabla de símbolos
- **Reglas**: S01-S10

### 4. Generación de Código
- **Entrada**: AST
- **Proceso**: Generación de código de tres direcciones
- **Salida**: Código intermedio
- **Reglas**: C01-C08

## 📚 Ejemplos Incluidos

### 1. basico.ml
Demuestra variables y operaciones aritméticas básicas.

### 2. condicionales.ml
Demuestra estructuras if, elif, else y comparaciones.

### 3. bucles.ml
Demuestra bucles for y while con diferentes casos de uso.

### 4. completo.ml
Programa completo que utiliza todas las características del lenguaje.

## 🎓 Valor Educativo

Este proyecto es ideal para:

1. **Aprender sobre compiladores**: Demuestra todas las fases
2. **Entender acciones semánticas**: Cada regla está documentada
3. **Experimentar con código**: IDE funcional e interactivo
4. **Enseñar compiladores**: Herramienta visual para profesores

## 🔧 Requisitos

- Python 3.7 o superior
- tkinter (incluido con Python en Windows)
- No requiere dependencias externas

## 💡 Características Únicas

1. **Todo en español**: Nombres, comentarios, documentación
2. **Tabla de reglas interactiva**: Primera implementación de este tipo
3. **Detalles de reglas**: Panel expandido al seleccionar
4. **Tema oscuro profesional**: Reduce fatiga visual
5. **6 pestañas informativas**: Visualización completa del proceso

## ✅ Checklist de Requisitos Cumplidos

- ✅ Compilador completo funcional
- ✅ Reglas semánticas en tabla
- ✅ Columnas: Regla, Producción, Acción, Ejemplo
- ✅ Interfaz tipo IDE moderno
- ✅ Colores oscuros profesionales
- ✅ Documentación integrada
- ✅ Sintaxis tipo Python
- ✅ Salida visual clara
- ✅ Detalles de regla seleccionada
- ✅ Múltiples pestañas informativas
- ✅ Código modularizado
- ✅ Nombres entendibles en español

## 🎉 Conclusión

El proyecto **Compilador MiniLang** está **100% completo** con:

- ✨ Todos los archivos con nombres en español
- ✨ Todos los comentarios en español
- ✨ Todas las variables y funciones en español
- ✨ IDE profesional completamente funcional
- ✨ 38 reglas semánticas documentadas
- ✨ Ejemplos funcionales incluidos
- ✨ Documentación completa en español

**¡Listo para usar y demostrar!** 🚀

---

**Autor**: Proyecto Educativo de Compiladores
**Fecha**: 2025-09-30
**Versión**: 1.0
**Idioma**: Español
