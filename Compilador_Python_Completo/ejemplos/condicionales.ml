# Programa de Condicionales en MiniLang
# Demuestra if, elif, else

edad = 18
nombre = "Juan"

print("Verificación de edad")

if edad < 13:
    print("Eres un niño")
elif edad < 18:
    print("Eres un adolescente")
elif edad < 65:
    print("Eres un adulto")
else:
    print("Eres un adulto mayor")

# Comparaciones
x = 10
y = 10

if x == y:
    print("x es igual a y")

if x >= y:
    print("x es mayor o igual a y")

if x != 5:
    print("x no es igual a 5")

# Condicionales anidados
temperatura = 25

if temperatura > 30:
    print("Hace mucho calor")
else:
    if temperatura > 20:
        print("Temperatura agradable")
    else:
        print("Hace frío")
