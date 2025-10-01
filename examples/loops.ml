# Programa de Bucles en MiniLang
# Demuestra for y while

print("Bucle FOR - Conteo del 0 al 9")
for i in range(10):
    print("i = " + str(i))

print("Bucle FOR - Tabla de multiplicar del 5")
numero = 5
for i in range(11):
    resultado = numero * i
    print(str(numero) + " x " + str(i) + " = " + str(resultado))

print("Bucle WHILE - Cuenta regresiva")
contador = 10
while contador > 0:
    print("Contador: " + str(contador))
    contador = contador - 1

print("Despegue!")

print("Bucle WHILE - Suma acumulativa")
suma = 0
n = 1
while n <= 5:
    suma = suma + n
    print("Suma hasta " + str(n) + " = " + str(suma))
    n = n + 1

print("Bucle FOR - Números pares")
for i in range(20):
    if i == i:
        print(str(i))
