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
        if ch == 'a':
            contador = contador + 1
        elif ch == 'e':
            contador = contador + 1
        elif ch == 'i':
            contador = contador + 1
        elif ch == 'o':
            contador = contador + 1
        elif ch == 'u':
            contador = contador + 1
        elif ch == 'A':
            contador = contador + 1
        elif ch == 'E':
            contador = contador + 1
        elif ch == 'I':
            contador = contador + 1
        elif ch == 'O':
            contador = contador + 1
        elif ch == 'U':
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
def convertir_a_mayuscula(caracter):
    if caracter == 'a':
        return 'A'
    elif caracter == 'b':
        return 'B'
    elif caracter == 'c':
        return 'C'
    elif caracter == 'd':
        return 'D'
    elif caracter == 'e':
        return 'E'
    elif caracter == 'f':
        return 'F'
    elif caracter == 'g':
        return 'G'
    elif caracter == 'h':
        return 'H'
    elif caracter == 'i':
        return 'I'
    elif caracter == 'j':
        return 'J'
    elif caracter == 'k':
        return 'K'
    elif caracter == 'l':
        return 'L'
    elif caracter == 'm':
        return 'M'
    elif caracter == 'n':
        return 'N'
    elif caracter == 'o':
        return 'O'
    elif caracter == 'p':
        return 'P'
    elif caracter == 'q':
        return 'Q'
    elif caracter == 'r':
        return 'R'
    elif caracter == 's':
        return 'S'
    elif caracter == 't':
        return 'T'
    elif caracter == 'u':
        return 'U'
    elif caracter == 'v':
        return 'V'
    elif caracter == 'w':
        return 'W'
    elif caracter == 'x':
        return 'X'
    elif caracter == 'y':
        return 'Y'
    elif caracter == 'z':
        return 'Z'
    else:
        return caracter

def a_mayusculas(texto):
    resultado = ""
    i = 0
    while i < len(texto):
        ch = texto[i]
        mayus = convertir_a_mayuscula(ch)
        resultado = resultado + mayus
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
            print(" Saliendo...")
        else:
            print(" Opción inválida.")

# ---------------------------------------
# Programa principal
# ---------------------------------------
def main():
    menu()

main()
