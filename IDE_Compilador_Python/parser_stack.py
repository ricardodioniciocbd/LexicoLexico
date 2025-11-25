"""
Autómata de Pila Formal para Análisis Sintáctico
Implementa un parser LR(1) con tabla de parsing explícita
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from enum import Enum, auto


class Action(Enum):
    """Tipos de acción en la tabla LR"""
    SHIFT = auto()
    REDUCE = auto()
    ACCEPT = auto()
    ERROR = auto()


@dataclass
class LRAction:
    """Acción en la tabla LR"""
    action_type: Action
    value: Optional[int] = None  # Estado para SHIFT, regla para REDUCE


@dataclass
class Production:
    """Producción de la gramática"""
    left: str  # Símbolo no terminal
    right: List[str]  # Lista de símbolos
    
    def __str__(self):
        return f"{self.left} → {' '.join(self.right) if self.right else 'ε'}"


class PushdownAutomaton:
    """
    Autómata de Pila (PDA) para Análisis Sintáctico
    
    Formalmente: PDA = (Q, Σ, Γ, δ, q0, Z0, F)
    Donde:
    - Q: Conjunto de estados
    - Σ: Alfabeto de entrada (tokens)
    - Γ: Alfabeto de la pila
    - δ: Función de transición
    - q0: Estado inicial
    - Z0: Símbolo inicial de la pila
    - F: Estados finales
    """
    
    def __init__(self):
        # Q: Estados
        self.states = set()
        
        # Σ: Alfabeto de entrada (terminales)
        self.terminals = {
            'NUMBER', 'STRING', 'IDENTIFIER',
            '+', '-', '*', '/', '(', ')', '=',
            'if', 'while', 'for', 'print',
            '$'  # Marcador de fin
        }
        
        # Γ: Alfabeto de la pila (terminales + no terminales)
        self.stack_alphabet = self.terminals | {
            'Program', 'Statement', 'Expression', 'Term', 'Factor',
            'Assignment', 'Comparison', 'Arithmetic',
            '$0'  # Símbolo inicial de pila
        }
        
        # q0: Estado inicial
        self.initial_state = 0
        
        # Z0: Símbolo inicial de pila
        self.initial_stack_symbol = '$0'
        
        # F: Estados finales
        self.accepting_states = set()
        
        # δ: Función de transición (implementada como tabla LR)
        self.action_table = {}  # (estado, terminal) → LRAction
        self.goto_table = {}    # (estado, no_terminal) → estado
        
        # Producciones de la gramática
        self.productions = []
        
        # Pila de análisis
        self.stack = []
        
        # Inicializar gramática y tablas
        self._init_grammar()
        self._build_parsing_tables()
    
    def _init_grammar(self):
        """Inicializa las producciones de la gramática"""
        # Gramática aumentada para análisis LR
        # 0: S' → Program
        self.productions.append(Production("S'", ["Program"]))
        
        # 1: Program → Statement
        self.productions.append(Production("Program", ["Statement"]))
        
        # 2: Statement → Assignment
        self.productions.append(Production("Statement", ["Assignment"]))
        
        # 3: Statement → print ( Expression )
        self.productions.append(Production("Statement", ["print", "(", "Expression", ")"]))
        
        # 4: Assignment → IDENTIFIER = Expression
        self.productions.append(Production("Assignment", ["IDENTIFIER", "=", "Expression"]))
        
        # 5: Expression → Comparison
        self.productions.append(Production("Expression", ["Comparison"]))
        
        # 6: Comparison → Arithmetic
        self.productions.append(Production("Comparison", ["Arithmetic"]))
        
        # 7: Arithmetic → Arithmetic + Term
        self.productions.append(Production("Arithmetic", ["Arithmetic", "+", "Term"]))
        
        # 8: Arithmetic → Arithmetic - Term
        self.productions.append(Production("Arithmetic", ["Arithmetic", "-", "Term"]))
        
        # 9: Arithmetic → Term
        self.productions.append(Production("Arithmetic", ["Term"]))
        
        # 10: Term → Term * Factor
        self.productions.append(Production("Term", ["Term", "*", "Factor"]))
        
        # 11: Term → Term / Factor
        self.productions.append(Production("Term", ["Term", "/", "Factor"]))
        
        # 12: Term → Factor
        self.productions.append(Production("Term", ["Factor"]))
        
        # 13: Factor → NUMBER
        self.productions.append(Production("Factor", ["NUMBER"]))
        
        # 14: Factor → STRING
        self.productions.append(Production("Factor", ["STRING"]))
        
        # 15: Factor → IDENTIFIER
        self.productions.append(Production("Factor", ["IDENTIFIER"]))
        
        # 16: Factor → ( Expression )
        self.productions.append(Production("Factor", ["(", "Expression", ")"]))
    
    def _build_parsing_tables(self):
        """
        Construye las tablas ACTION y GOTO para el parser LR
        
        Esta es una versión simplificada. En un compilador real,
        estas tablas se generarían automáticamente usando:
        - Conjuntos de items LR(1)
        - Clausura y función GOTO
        - Resolución de conflictos shift/reduce
        """
        
        # Tabla ACTION: (estado, terminal) → acción
        # Estado 0 (inicial)
        self.action_table[(0, 'IDENTIFIER')] = LRAction(Action.SHIFT, 2)
        self.action_table[(0, 'print')] = LRAction(Action.SHIFT, 3)
        self.action_table[(0, 'NUMBER')] = LRAction(Action.SHIFT, 4)
        self.action_table[(0, 'STRING')] = LRAction(Action.SHIFT, 5)
        self.action_table[(0, '(')] = LRAction(Action.SHIFT, 6)
        
        # Estado 1 (después de Program)
        self.action_table[(1, '$')] = LRAction(Action.ACCEPT)
        
        # Estado 2 (después de IDENTIFIER)
        self.action_table[(2, '=')] = LRAction(Action.SHIFT, 7)
        self.action_table[(2, '+')] = LRAction(Action.REDUCE, 15)  # Factor → IDENTIFIER
        self.action_table[(2, '-')] = LRAction(Action.REDUCE, 15)
        self.action_table[(2, '*')] = LRAction(Action.REDUCE, 15)
        self.action_table[(2, '/')] = LRAction(Action.REDUCE, 15)
        self.action_table[(2, ')')] = LRAction(Action.REDUCE, 15)
        self.action_table[(2, '$')] = LRAction(Action.REDUCE, 15)
        
        # Estado 3 (después de print)
        self.action_table[(3, '(')] = LRAction(Action.SHIFT, 8)
        
        # Estado 4 (después de NUMBER)
        self.action_table[(4, '+')] = LRAction(Action.REDUCE, 13)  # Factor → NUMBER
        self.action_table[(4, '-')] = LRAction(Action.REDUCE, 13)
        self.action_table[(4, '*')] = LRAction(Action.REDUCE, 13)
        self.action_table[(4, '/')] = LRAction(Action.REDUCE, 13)
        self.action_table[(4, ')')] = LRAction(Action.REDUCE, 13)
        self.action_table[(4, '$')] = LRAction(Action.REDUCE, 13)
        
        # Estado 5 (después de STRING)
        self.action_table[(5, '+')] = LRAction(Action.REDUCE, 14)  # Factor → STRING
        self.action_table[(5, '-')] = LRAction(Action.REDUCE, 14)
        self.action_table[(5, '*')] = LRAction(Action.REDUCE, 14)
        self.action_table[(5, '/')] = LRAction(Action.REDUCE, 14)
        self.action_table[(5, ')')] = LRAction(Action.REDUCE, 14)
        self.action_table[(5, '$')] = LRAction(Action.REDUCE, 14)
        
        # Estado 6 (después de '(')
        self.action_table[(6, 'NUMBER')] = LRAction(Action.SHIFT, 4)
        self.action_table[(6, 'STRING')] = LRAction(Action.SHIFT, 5)
        self.action_table[(6, 'IDENTIFIER')] = LRAction(Action.SHIFT, 2)
        self.action_table[(6, '(')] = LRAction(Action.SHIFT, 6)
        
        # Tabla GOTO: (estado, no_terminal) → estado
        self.goto_table[(0, 'Program')] = 1
        self.goto_table[(0, 'Statement')] = 9
        self.goto_table[(0, 'Assignment')] = 10
        self.goto_table[(0, 'Expression')] = 11
        self.goto_table[(0, 'Comparison')] = 12
        self.goto_table[(0, 'Arithmetic')] = 13
        self.goto_table[(0, 'Term')] = 14
        self.goto_table[(0, 'Factor')] = 15
        
        # Estados adicionales (simplificados)
        self.states = set(range(20))  # 20 estados en total
        self.accepting_states = {1}
    
    def parse(self, tokens: List[str]) -> Tuple[bool, List[str]]:
        """
        Realiza el análisis sintáctico usando el autómata de pila
        
        Args:
            tokens: Lista de tokens de entrada
            
        Returns:
            (éxito, traza): Tupla con resultado y traza de análisis
        """
        # Inicializar pila con estado inicial y símbolo inicial
        self.stack = [0, self.initial_stack_symbol]
        
        # Agregar marcador de fin
        input_buffer = list(tokens) + ['$']
        input_index = 0
        
        # Traza de análisis
        trace = []
        trace.append("INICIO DEL ANÁLISIS SINTÁCTICO")
        trace.append("=" * 80)
        trace.append(f"{'Paso':<6} {'Pila':<30} {'Entrada':<30} {'Acción':<20}")
        trace.append("-" * 80)
        
        step = 0
        
        while True:
            step += 1
            
            # Estado actual (tope de la pila de estados)
            current_state = self.stack[-2] if len(self.stack) >= 2 else 0
            
            # Token actual
            current_token = input_buffer[input_index] if input_index < len(input_buffer) else '$'
            
            # Registrar estado actual
            stack_str = ' '.join(str(s) for s in self.stack[-10:])  # Últimos 10 elementos
            input_str = ' '.join(input_buffer[input_index:input_index+5])  # Próximos 5 tokens
            
            # Buscar acción en la tabla
            action_key = (current_state, current_token)
            if action_key not in self.action_table:
                trace.append(f"{step:<6} {stack_str:<30} {input_str:<30} ERROR")
                trace.append(f"\nError: No hay acción definida para estado {current_state} con token '{current_token}'")
                return False, trace
            
            action = self.action_table[action_key]
            
            # Ejecutar acción
            if action.action_type == Action.SHIFT:
                # SHIFT: Apilar estado y avanzar entrada
                trace.append(f"{step:<6} {stack_str:<30} {input_str:<30} SHIFT {action.value}")
                self.stack.append(current_token)
                self.stack.append(action.value)
                input_index += 1
                
            elif action.action_type == Action.REDUCE:
                # REDUCE: Aplicar producción
                production = self.productions[action.value]
                trace.append(f"{step:<6} {stack_str:<30} {input_str:<30} REDUCE {action.value}: {production}")
                
                # Desapilar 2 * len(right) elementos (símbolo y estado por cada símbolo)
                for _ in range(len(production.right) * 2):
                    if self.stack:
                        self.stack.pop()
                
                # Obtener nuevo estado usando GOTO
                if self.stack:
                    prev_state = self.stack[-1]
                else:
                    prev_state = 0
                    
                goto_key = (prev_state, production.left)
                if goto_key in self.goto_table:
                    new_state = self.goto_table[goto_key]
                    self.stack.append(production.left)
                    self.stack.append(new_state)
                else:
                    trace.append(f"\nError: No hay transición GOTO para estado {prev_state} con no terminal '{production.left}'")
                    return False, trace
                    
            elif action.action_type == Action.ACCEPT:
                # ACCEPT: Análisis exitoso
                trace.append(f"{step:<6} {stack_str:<30} {input_str:<30} ACCEPT")
                trace.append("=" * 80)
                trace.append("ANÁLISIS COMPLETADO EXITOSAMENTE")
                return True, trace
                
            else:
                trace.append(f"{step:<6} {stack_str:<30} {input_str:<30} ERROR")
                return False, trace
            
            # Límite de seguridad
            if step > 1000:
                trace.append("\nError: Límite de pasos excedido (posible bucle infinito)")
                return False, trace
    
    def get_grammar_info(self) -> str:
        """Retorna información sobre la gramática y el autómata"""
        info = []
        info.append("AUTÓMATA DE PILA (PDA) - INFORMACIÓN FORMAL")
        info.append("=" * 80)
        info.append("")
        
        info.append("1. DEFINICIÓN FORMAL:")
        info.append(f"   PDA = (Q, Σ, Γ, δ, q0, Z0, F)")
        info.append(f"   - Q (Estados): {len(self.states)} estados")
        info.append(f"   - Σ (Alfabeto entrada): {len(self.terminals)} símbolos terminales")
        info.append(f"   - Γ (Alfabeto pila): {len(self.stack_alphabet)} símbolos")
        info.append(f"   - q0 (Estado inicial): {self.initial_state}")
        info.append(f"   - Z0 (Símbolo inicial pila): {self.initial_stack_symbol}")
        info.append(f"   - F (Estados finales): {self.accepting_states}")
        info.append("")
        
        info.append("2. PRODUCCIONES DE LA GRAMÁTICA:")
        info.append("-" * 80)
        for i, prod in enumerate(self.productions):
            info.append(f"   {i}: {prod}")
        info.append("")
        
        info.append("3. TABLA ACTION (muestra parcial):")
        info.append("-" * 80)
        action_count = 0
        for (state, terminal), action in sorted(self.action_table.items())[:20]:
            if action.action_type == Action.SHIFT:
                info.append(f"   ACTION[{state}, '{terminal}'] = SHIFT {action.value}")
            elif action.action_type == Action.REDUCE:
                info.append(f"   ACTION[{state}, '{terminal}'] = REDUCE {action.value}")
            elif action.action_type == Action.ACCEPT:
                info.append(f"   ACTION[{state}, '{terminal}'] = ACCEPT")
            action_count += 1
        info.append(f"   ... (Total: {len(self.action_table)} entradas)")
        info.append("")
        
        info.append("4. TABLA GOTO (muestra parcial):")
        info.append("-" * 80)
        for (state, nonterminal), next_state in sorted(self.goto_table.items())[:15]:
            info.append(f"   GOTO[{state}, '{nonterminal}'] = {next_state}")
        info.append(f"   ... (Total: {len(self.goto_table)} entradas)")
        info.append("")
        
        return '\n'.join(info)


# Función de prueba
def test_pda():
    """Prueba el autómata de pila"""
    pda = PushdownAutomaton()
    
    print(pda.get_grammar_info())
    print("\n" + "=" * 80)
    print("PRUEBA DE ANÁLISIS")
    print("=" * 80)
    
    # Ejemplo: x = 5
    tokens = ['IDENTIFIER', '=', 'NUMBER']
    success, trace = pda.parse(tokens)
    
    for line in trace:
        print(line)
    
    print(f"\nResultado: {'ÉXITO' if success else 'FALLO'}")


if __name__ == "__main__":
    test_pda()

