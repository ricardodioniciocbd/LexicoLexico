# 🚀 Guía Rápida - MiniLang IDE

## Inicio Rápido

### 1. Ejecutar el IDE

```bash
python minilang_ide.py
```

### 2. Usar el IDE

#### Compilar Código
1. Escribe o carga código en el editor
2. Haz clic en el botón **"▶ Compilar"**
3. Revisa los resultados en las pestañas

#### Pestañas Disponibles

- **Tokens**: Ver todos los tokens generados por el análisis léxico
- **AST**: Visualizar el árbol de sintaxis abstracta
- **Análisis Semántico**: Ver tabla de símbolos y errores
- **Código Generado**: Ver código de tres direcciones
- **Reglas Semánticas**: Tabla interactiva con 38 reglas
- **Gramática**: Documentación de la sintaxis

#### Botones de la Barra de Herramientas

- **▶ Compilar**: Compila el código actual
- **🗑 Limpiar**: Limpia todas las salidas
- **📄 Ejemplo**: Carga código de ejemplo
- **💾 Guardar**: Guarda el código en archivo .ml
- **📂 Abrir**: Abre un archivo existente

## 📝 Ejemplos Rápidos

### Hola Mundo
```python
nombre = "Mundo"
print("Hola " + nombre)
```

### Variables y Operaciones
```python
x = 10
y = 5
suma = x + y
print("Resultado: " + str(suma))
```

### Condicional
```python
edad = 18
if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor de edad")
```

### Bucle For
```python
for i in range(5):
    print("Número: " + str(i))
```

### Bucle While
```python
contador = 0
while contador < 3:
    print(contador)
    contador = contador + 1
```

## 🎯 Explorar Reglas Semánticas

1. Ve a la pestaña **"Reglas Semánticas"**
2. Selecciona una fase (Léxico, Sintáctico, Semántico, Código)
3. Haz clic en cualquier regla de la tabla
4. Lee los detalles en la sección inferior

### Fases Disponibles

- **Análisis Léxico** (7 reglas): Tokenización
- **Análisis Sintáctico** (10 reglas): Construcción del AST
- **Análisis Semántico** (10 reglas): Verificación de tipos
- **Generación de Código** (8 reglas): Código intermedio

## 📂 Archivos de Ejemplo

Ubicación: `examples/`

- **basic.ml**: Operaciones básicas
- **conditionals.ml**: Estructuras if/elif/else
- **loops.ml**: Bucles for y while
- **complete.ml**: Programa completo con todas las características

## 🐛 Tipos de Errores

### Error Léxico
```python
x = @invalid  # Carácter no reconocido
```

### Error Sintáctico
```python
if x > 5  # Falta ':'
    print(x)
```

### Error Semántico
```python
print(variable_no_declarada)  # Variable no existe
```

## 💡 Consejos

1. **Indentación**: Usa espacios consistentes (4 espacios recomendado)
2. **Comentarios**: Usa `#` para comentarios de una línea
3. **Strings**: Usa comillas dobles `"` o simples `'`
4. **Concatenación**: Usa `+` para unir strings
5. **Conversión**: Usa `str()` para convertir números a string

## 🎨 Características del IDE

- ✅ Tema oscuro profesional
- ✅ Números de línea
- ✅ Múltiples pestañas de salida
- ✅ Tabla interactiva de reglas
- ✅ Detalles de reglas al seleccionar
- ✅ Guardar/Abrir archivos
- ✅ Ejemplos precargados
- ✅ Barra de estado con feedback

## 📊 Flujo de Compilación

```
Código Fuente
    ↓
[Análisis Léxico] → Tokens
    ↓
[Análisis Sintáctico] → AST
    ↓
[Análisis Semántico] → Tabla de Símbolos
    ↓
[Generación de Código] → Código Intermedio
```

## 🔍 Verificar Compilación

Una compilación exitosa muestra:
- ✅ Barra de estado verde: "✓ Compilación exitosa"
- ✅ Tokens en la pestaña Tokens
- ✅ AST en la pestaña AST
- ✅ Tabla de símbolos sin errores
- ✅ Código generado en la pestaña correspondiente

## ❓ Solución de Problemas

### El IDE no inicia
```bash
# Verifica que tienes Python 3.7+
python --version

# Verifica que tkinter está instalado
python -c "import tkinter"
```

### Error de importación
```bash
# Asegúrate de estar en el directorio correcto
cd c:\Cursos\AccionesSemanticas_py
python minilang_ide.py
```

## 📚 Más Información

Consulta el archivo **README.md** para documentación completa.

---

**¡Comienza a compilar con MiniLang IDE!** 🎉
