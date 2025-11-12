# ============================================
# Sistema de Gestión de Estudiantes (CRUD)
# ============================================

# Lista global de estudiantes (cada estudiante es un diccionario)
estudiantes = []

# ------------------------------
# Menú principal
# ------------------------------
def menu():
    opcion = ""
    while opcion != "5":
        print("\n===== MENÚ DE ESTUDIANTES =====")
        print("1. Alta (Agregar)")
        print("2. Baja (Eliminar)")
        print("3. Modificar")
        print("4. Listar")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            alta()
        elif opcion == "2":
            baja()
        elif opcion == "3":
            modificar()
        elif opcion == "4":
            listar()
        elif opcion == "5":
            print(" Saliendo del sistema...")
        else:
            print(" Opción no válida.")
# ------------------------------
# Función: agregar un estudiante
# ------------------------------
def alta():
    id = input("Ingrese ID: ")
    nombre = input("Ingrese nombre: ")
    edad = input("Ingrese edad: ")
    carrera = input("Ingrese carrera: ")
    promedio = input("Ingrese promedio: ")

    nuevo = {"id": id, "nombre": nombre, "edad": edad, "carrera": carrera, "promedio": promedio}
    estudiantes.append(nuevo)

    print(" Estudiante agregado correctamente.")

# ------------------------------
# Función: listar estudiantes
# ------------------------------
def listar():
    print(" Lista de estudiantes:")
    for e in estudiantes:
        print("ID:", e["id"], "- Nombre:", e["nombre"], "- Edad:", e["edad"], "- Carrera:", e["carrera"], "- Promedio:", e["promedio"])

# ------------------------------
# Función: eliminar estudiante
# ------------------------------
def baja():
    id = input("Ingrese ID a eliminar: ")

    encontrado = False
    for e in estudiantes:
        if e["id"] == id:
            estudiantes.remove(e)
            print(" Estudiante eliminado.")
            encontrado = True
            break

    if not encontrado:
        print(" No se encontró el ID especificado.")

# ------------------------------
# Función: modificar estudiante
# ------------------------------
def modificar():
    id = input("Ingrese ID a modificar: ")
    encontrado = False

    for e in estudiantes:
        if e["id"] == id:
            nuevo_nombre = input("Nuevo nombre: ")
            nueva_edad = input("Nueva edad: ")
            nueva_carrera = input("Nueva carrera: ")
            nuevo_promedio = input("Nuevo promedio: ")                              
            e["nombre"] = nuevo_nombre
            e["edad"] = nueva_edad
            e["carrera"] = nueva_carrera
            e["promedio"] = nuevo_promedio
            print(" Datos modificados correctamente.")
            encontrado = True
            break

    if not encontrado:
        print(" Estudiante no encontrado.")






# ------------------------------
# Programa principal
# ------------------------------
menu()
