# ============================================
# Diccionarios Básicos
# Compatible con el Compilador Python
# ============================================

print("===== EJEMPLO DE DICCIONARIOS =====")
print("")

# Crear un producto como diccionario
print("Creando producto con diccionario...")

producto1 = {"desc": "Laptop", "precio": 1200, "stock": 5}

print("Producto creado:")
print(producto1)
print("")

# Crear otro producto
producto2 = {"desc": "Mouse", "precio": 25, "stock": 20}

print("Segundo producto:")
print(producto2)
print("")

# Calcular valor de inventario de un producto
print("Calculando valor del producto 1...")

valor1 = producto1["precio"] * producto1["stock"]
print("Valor total del Producto 1:")
print(valor1)

print("")

valor2 = producto2["precio"] * producto2["stock"]
print("Valor total del Producto 2:")
print(valor2)

print("")

# Sumar valores totales
total = valor1 + valor2
print("Valor total de inventario:")
print(total)

print("")

# Actualizar stock
print("Actualizando stock del producto 1...")
print("Stock anterior:")
print(producto1["stock"])

producto1["stock"] = producto1["stock"] + 3

print("Stock nuevo:")
print(producto1["stock"])

print("")
print("===== FIN =====")

