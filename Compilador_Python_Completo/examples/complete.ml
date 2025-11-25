# Programa Completo en MiniLang
# Demuestra todas las características del lenguaje

# Variables y tipos
nombre = "MiniLang"
version = 1.0
anio = 2025

print("=================================")
print("Bienvenido a " + nombre)
print("Version: " + str(version))
print("Año: " + str(anio))
print("=================================")

# Operaciones aritméticas
a = 15
b = 4

print("Operaciones con a=" + str(a) + " y b=" + str(b))
print("Suma: " + str(a + b))
print("Resta: " + str(a - b))
print("Multiplicación: " + str(a * b))
print("División: " + str(a / b))

# Condicionales
print("Análisis de números")

if a > b:
    print("a es mayor que b")
    diferencia = a - b
    print("Diferencia: " + str(diferencia))
elif a < b:
    print("b es mayor que a")
else:
    print("a y b son iguales")

# Clasificación de número
numero = 42

if numero < 0:
    print("El número es negativo")
elif numero == 0:
    print("El número es cero")
else:
    print("El número es positivo")

# Bucle for - Tabla de multiplicar
print("Tabla de multiplicar del 7")
multiplicador = 7

for i in range(10):
    resultado = multiplicador * i
    print(str(multiplicador) + " x " + str(i) + " = " + str(resultado))

# Bucle while - Factorial
print("Cálculo de factorial")
n = 5
factorial = 1
contador = 1

while contador <= n:
    factorial = factorial * contador
    contador = contador + 1

print("Factorial de " + str(n) + " = " + str(factorial))

# Bucle for - Suma de números
print("Suma de números del 1 al 10")
suma = 0

for i in range(11):
    suma = suma + i

print("Suma total: " + str(suma))

# Condicionales con bucles
print("Números del 1 al 20 con clasificación")

for num in range(21):
    if num < 10:
        print(str(num) + " es menor que 10")
    elif num == 10:
        print(str(num) + " es igual a 10")
    else:
        print(str(num) + " es mayor que 10")

# Concatenación de strings
saludo = "Hola"
mundo = "Mundo"
mensaje = saludo + " " + mundo

print(mensaje)

# Operaciones complejas
x = 10
y = 5
z = 2

resultado1 = x + y * z
resultado2 = (x + y) * z

print("Sin paréntesis: " + str(resultado1))
print("Con paréntesis: " + str(resultado2))

# Bucle while con condicional
print("Números pares del 0 al 10")
i = 0

while i <= 10:
    if i == i:
        print(str(i))
    i = i + 1

print("Programa completado exitosamente!")
