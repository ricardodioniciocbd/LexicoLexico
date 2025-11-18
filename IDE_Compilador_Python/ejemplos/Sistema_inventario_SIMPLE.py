# ============================================
# Sistema de Inventario SIMPLIFICADO
# Compatible con el Compilador Python
# ============================================

# Simulación de inventario con listas paralelas
# (El compilador no soporta diccionarios complejos)

# Listas paralelas para almacenar datos
codigos = []
descripciones = []
precios = []
stocks = []

print("===== SISTEMA DE INVENTARIO =====")
print("")

# ---------------------------------------
# Agregar 3 productos de ejemplo
# ---------------------------------------
print("Agregando productos iniciales...")

# Producto 1
codigos = codigos + ["P001"]
descripciones = descripciones + ["Laptop"]
precios = precios + [1200]
stocks = stocks + [5]

# Producto 2
codigos = codigos + ["P002"]
descripciones = descripciones + ["Mouse"]
precios = precios + [25]
stocks = stocks + [20]

# Producto 3
codigos = codigos + ["P003"]
descripciones = descripciones + ["Teclado"]
precios = precios + [45]
stocks = stocks + [15]

print("Productos agregados correctamente")
print("")

# ---------------------------------------
# Listar productos
# ---------------------------------------
print("===== INVENTARIO ACTUAL =====")

i = 0
while i < len(codigos):
    print("Codigo:")
    print(codigos[i])
    print("Descripcion:")
    print(descripciones[i])
    print("Precio:")
    print(precios[i])
    print("Stock:")
    print(stocks[i])
    print("---")
    i = i + 1

print("")

# ---------------------------------------
# Calcular valor total del inventario
# ---------------------------------------
print("Calculando valor total...")

total = 0
i = 0
while i < len(codigos):
    valor_producto = precios[i] * stocks[i]
    total = total + valor_producto
    i = i + 1

print("Valor total del inventario:")
print(total)
print("")

# ---------------------------------------
# Buscar un producto específico
# ---------------------------------------
print("Buscando producto P002...")

codigo_buscar = "P002"
encontrado = 0
posicion = 0

i = 0
while i < len(codigos):
    if codigos[i] == codigo_buscar:
        encontrado = 1
        posicion = i
    i = i + 1

if encontrado == 1:
    print("Producto encontrado:")
    print("Descripcion:")
    print(descripciones[posicion])
    print("Precio:")
    print(precios[posicion])
    print("Stock:")
    print(stocks[posicion])
else:
    print("Producto no encontrado")

print("")

# ---------------------------------------
# Actualizar stock de un producto
# ---------------------------------------
print("Actualizando stock de P001...")

codigo_actualizar = "P001"
cantidad_agregar = 3

i = 0
while i < len(codigos):
    if codigos[i] == codigo_actualizar:
        stock_anterior = stocks[i]
        stocks[i] = stocks[i] + cantidad_agregar
        print("Stock actualizado")
        print("Anterior:")
        print(stock_anterior)
        print("Nuevo:")
        print(stocks[i])
    i = i + 1

print("")
print("===== FIN DEL PROGRAMA =====")

