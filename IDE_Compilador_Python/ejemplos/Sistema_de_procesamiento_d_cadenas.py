# ============================================
# Procesamiento de Cadenas
# ============================================

# ---------------------------------------
# Contar vocales en una cadena
# ---------------------------------------
def contar_vocales(texto):
    contador = 0
    i = 0
    while i < len(texto):
        ch = texto[i]
        if ch == 'a' or ch == 'e' or ch == 'i' or ch == 'o' or ch == 'u' \
        or ch == 'A' or ch == 'E' or ch == 'I' or ch == 'O' or ch == 'U':
            contador = contador + 1
        i = i + 1
    return contador

# ---------------------------------------
# Invertir una cadena manualmente
# ---------------------------------------
def invertir(texto):
    invertida = ""
    i = len(texto) - 1
    while i >= 0:
        invertida = invertida + texto[i]
        i = i - 1
    return invertida

# ---------------------------------------
# Verificar si es palíndromo
# ---------------------------------------
def es_palindromo(texto):
    texto_invertido = invertir(texto)
    if texto_invertido == texto:
        return True
    else:
        return False

# ---------------------------------------
# Contar cuántas veces aparece un carácter
# ---------------------------------------
def contar_caracter(texto, caracter):
    contador = 0
    i = 0
    while i < len(texto):
        if texto[i] == caracter:
            contador = contador + 1
        i = i + 1
    return contador

# ---------------------------------------
# Convertir a mayúsculas (simplificado)
# ---------------------------------------
def a_mayusculas(texto):
    resultado = ""
    i = 0
    while i < len(texto):
        ch = texto[i]
        if ch >= 'a' and ch <= 'z':
            mayus = chr(ord(ch) - 32)
            resultado = resultado + mayus
        else:
            resultado = resultado + ch
        i = i + 1
    return resultado

# ---------------------------------------
# Menú principal
# ---------------------------------------
def menu():
    opcion = ""
    while opcion != "6":
        print("\n===== PROCESAMIENTO DE CADENAS =====")
        print("1. Contar vocales")
        print("2. Invertir cadena")
        print("3. Verificar palíndromo")
        print("4. Contar un carácter específico")
        print("5. Convertir a mayúsculas")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            texto = input("Ingrese texto: ")
            print("Cantidad de vocales:", contar_vocales(texto))

        elif opcion == "2":
            texto = input("Ingrese texto: ")
            print("Invertida:", invertir(texto))

        elif opcion == "3":
            texto = input("Ingrese texto: ")
            if es_palindromo(texto):
                print(" Es palíndromo.")
            else:
                print(" No es palíndromo.")

        elif opcion == "4":
            texto = input("Ingrese texto: ")
            caracter = input("Ingrese carácter a buscar: ")
            print("El carácter aparece", contar_caracter(texto, caracter), "veces.")

        elif opcion == "5":
            texto = input("Ingrese texto: ")
            print("En mayúsculas:", a_mayusculas(texto))

        elif opcion == "6":
            print("👋 Saliendo...")
        else:
            print("⚠️ Opción inválida.")

# ---------------------------------------
# Programa principal
# ---------------------------------------
menu()
