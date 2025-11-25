# ============================================
# Sistema de Inventario con Diccionarios
# ============================================

# Diccionario global del inventario
# clave: código del producto
# valor: otro diccionario con los datos del producto
inventario = {}

# ---------------------------------------
# Función: agregar un producto nuevo
# ---------------------------------------
def agregar():
    codigo = input("Ingrese código del producto: ")
    descripcion = input("Ingrese descripción: ")
    precio = input("Ingrese precio: ")
    stock = input("Ingrese cantidad en stock: ")

    # crear el "struct" del producto
    producto = {"desc": descripcion, "precio": int(precio), "stock": int(stock)}

    inventario[codigo] = producto
    print(" Producto agregado correctamente.")

# ---------------------------------------
# Función: mostrar todos los productos
# ---------------------------------------
def listar():
    print("\n INVENTARIO ACTUAL:")
    for codigo in inventario:
        p = inventario[codigo]
        print("Código:", codigo, "- Desc:", p["desc"], "- Precio:", p["precio"], "- Stock:", p["stock"])

# ---------------------------------------
# Función: actualizar stock
# ---------------------------------------
def actualizar_stock():
    codigo = input("Ingrese código del producto: ")

    if codigo in inventario:
        cambio = input("Ingrese cantidad a sumar/restar: ")
        inventario[codigo]["stock"] = inventario[codigo]["stock"] + int(cambio)
        print(" Stock actualizado correctamente.")
    else:
        print(" Producto no encontrado.")

# ---------------------------------------
# Función: eliminar producto
# ---------------------------------------
def eliminar():
    codigo = input("Ingrese código a eliminar: ")

    if codigo in inventario:
        del inventario[codigo]
        print(" Producto eliminado.")
    else:
        print(" No existe ese código.")

# ---------------------------------------
# Función: calcular valor total del inventario
# ---------------------------------------
def valor_total():
    total = 0
    for codigo in inventario:
        p = inventario[codigo]
        total = total + (p["precio"] * p["stock"])
    print(" Valor total del inventario:", total)
# ---------------------------------------
# Menú principal
# ---------------------------------------
def menu():
    opcion = ""
    while opcion != "6":
        print("\n===== MENÚ DE INVENTARIO =====")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Actualizar stock")
        print("4. Eliminar producto")
        print("5. Calcular valor total")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar()
        elif opcion == "2":
            listar()
        elif opcion == "3":
            actualizar_stock()
        elif opcion == "4":
            eliminar()
        elif opcion == "5":
            valor_total()
        elif opcion == "6":
            print(" Saliendo del sistema...")
        else:
            print(" Opción no válida.")

# ---------------------------------------
# Programa principal
# ---------------------------------------
menu()
