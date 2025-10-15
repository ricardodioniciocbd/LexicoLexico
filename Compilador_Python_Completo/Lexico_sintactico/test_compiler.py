"""
Script de Prueba para el Compilador
Verifica que todas las fases funcionan correctamente
"""

from python_compiler import Lexer, Parser
from tac_generator import TACGenerator
from tac_optimizer import TACOptimizer
from tac_interpreter import TACInterpreter


def test_compiler():
    """Prueba completa del compilador"""
    
    print("=" * 80)
    print("PRUEBA DEL COMPILADOR INTERACTIVO DE PYTHON")
    print("=" * 80)
    print()
    
    # Código de prueba
    source_code = '''# Prueba simple
x = 5
y = 10
suma = x + y
print("La suma es:")
print(suma)

if suma > 12:
    print("Mayor que 12")
else:
    print("Menor o igual a 12")
'''
    
    print("CÓDIGO FUENTE:")
    print("-" * 80)
    print(source_code)
    print()
    
    try:
        # Fase 1: Análisis Léxico
        print("FASE 1: ANÁLISIS LÉXICO")
        print("-" * 80)
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        visible_tokens = [t for t in tokens if t.type.name not in ('NEWLINE', 'EOF', 'INDENT', 'DEDENT')]
        print(f"[OK] Tokens generados: {len(visible_tokens)}")
        print()
        
        # Fase 2: Análisis Sintáctico
        print("FASE 2: ANALISIS SINTACTICO")
        print("-" * 80)
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"[OK] AST construido con {len(ast.statements)} sentencias")
        print()
        
        # Fase 3: Generación de Código Intermedio
        print("FASE 3: GENERACION DE CODIGO INTERMEDIO (TAC)")
        print("-" * 80)
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        print(f"[OK] TAC generado: {len(tac_instructions)} instrucciones")
        print("\nPrimeras 10 instrucciones TAC:")
        for i, instr in enumerate(tac_instructions[:10]):
            print(f"  {i}: {str(instr)}")
        print()
        
        # Fase 4: Optimización
        print("FASE 4: OPTIMIZACION DE CODIGO")
        print("-" * 80)
        optimizer = TACOptimizer()
        optimized_tac = optimizer.optimize(tac_instructions)
        reduction = len(tac_instructions) - len(optimized_tac)
        print(f"[OK] Codigo optimizado")
        print(f"  Instrucciones originales: {len(tac_instructions)}")
        print(f"  Instrucciones optimizadas: {len(optimized_tac)}")
        print(f"  Reduccion: {reduction} instrucciones")
        print(f"  Optimizaciones aplicadas: {len(optimizer.optimizations_applied)}")
        print()
        
        # Fase 5: Ejecución
        print("FASE 5: EJECUCION")
        print("-" * 80)
        interpreter = TACInterpreter()
        output = interpreter.interpret(optimized_tac)
        print("[OK] Codigo ejecutado correctamente")
        print("\nSALIDA DEL PROGRAMA:")
        print(output)
        print()
        
        print("=" * 80)
        print("[EXITO] TODAS LAS FASES COMPLETADAS EXITOSAMENTE")
        print("=" * 80)
        print()
        print("El compilador está funcionando correctamente.")
        print("Ejecuta 'python python_ide.py' para usar la interfaz gráfica.")
        
        return True
        
    except Exception as e:
        print("=" * 80)
        print("[ERROR] ERROR EN LA PRUEBA")
        print("=" * 80)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_compiler()

