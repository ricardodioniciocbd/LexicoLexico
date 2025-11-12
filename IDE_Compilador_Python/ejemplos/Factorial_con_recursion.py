# ============================================
# Cálculo de Factorial (usando recursión)
# ============================================

# ---------------------------------------
# Función recursiva para calcular factorial
# ---------------------------------------
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

# ---------------------------------------
# Programa principal
# ---------------------------------------
def main():
    print("=== CÁLCULO DE FACTORIAL ===")
    valor = input("Ingrese un número entero: ")
    n = int(valor)
    resultado = factorial(n)
    print("El factorial de", n, "es:", resultado)

# ---------------------------------------
# Ejecución
# ---------------------------------------
main()
