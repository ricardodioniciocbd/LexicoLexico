"""
Propiedades de Cerradura y Decidibilidad de Lenguajes Formales
Implementa verificaciones de propiedades formales según la teoría de autómatas
"""

from typing import Set, List, Tuple, Optional
from dataclasses import dataclass
from automata_optimizer import FiniteAutomaton, State
from parser_stack import Production
import re


@dataclass
class Language:
    """
    Representación de un lenguaje formal
    Puede ser representado por:
    - Un autómata finito (para lenguajes regulares)
    - Una gramática libre de contexto
    - Una expresión regular
    """
    name: str
    automaton: Optional[FiniteAutomaton] = None
    grammar_productions: Optional[List[Production]] = None
    regex: Optional[str] = None
    language_type: str = "regular"  # regular, context-free, context-sensitive, recursively-enumerable


class ClosureProperties:
    """
    Verificación de Propiedades de Cerradura
    
    Los lenguajes regulares son cerrados bajo:
    - Unión
    - Concatenación
    - Estrella de Kleene
    - Complemento
    - Intersección
    - Diferencia
    """
    
    def __init__(self):
        self.operations_log = []
    
    def union(self, dfa1: FiniteAutomaton, dfa2: FiniteAutomaton) -> FiniteAutomaton:
        """
        Unión de dos lenguajes: L1 ∪ L2
        
        Teorema: Si L1 y L2 son regulares, entonces L1 ∪ L2 es regular
        
        Construcción: Producto cartesiano de estados con regla:
        (q1, q2) es final si q1 es final EN L1 O q2 es final EN L2
        """
        self.operations_log.append(f"UNIÓN: L({dfa1.initial_state}) ∪ L({dfa2.initial_state})")
        
        result = FiniteAutomaton()
        
        # Crear producto cartesiano de estados
        state_map = {}
        state_counter = 0
        
        for s1 in dfa1.states:
            for s2 in dfa2.states:
                # Estado es final si CUALQUIERA de los dos es final
                is_final = s1.is_final or s2.is_final
                new_state = State(state_counter, is_final)
                state_map[(s1, s2)] = new_state
                result.add_state(new_state)
                
                # Estado inicial es el par de estados iniciales
                if s1 == dfa1.initial_state and s2 == dfa2.initial_state:
                    result.initial_state = new_state
                
                state_counter += 1
        
        # Crear transiciones
        alphabet = dfa1.alphabet | dfa2.alphabet
        for symbol in alphabet:
            for s1 in dfa1.states:
                for s2 in dfa2.states:
                    # Obtener transiciones en ambos autómatas
                    next1 = dfa1.transitions.get((s1, symbol))
                    next2 = dfa2.transitions.get((s2, symbol))
                    
                    if next1 and next2:
                        from_state = state_map[(s1, s2)]
                        to_state = state_map[(next1, next2)]
                        result.add_transition(from_state, symbol, to_state)
        
        self.operations_log.append(f"  → Estados resultantes: {len(result.states)}")
        return result
    
    def concatenation(self, dfa1: FiniteAutomaton, dfa2: FiniteAutomaton) -> str:
        """
        Concatenación de dos lenguajes: L1 · L2 = {xy | x ∈ L1, y ∈ L2}
        
        Teorema: Si L1 y L2 son regulares, entonces L1 · L2 es regular
        
        Nota: Devuelve descripción (construcción completa requiere NFA)
        """
        self.operations_log.append(f"CONCATENACIÓN: L1 · L2")
        
        description = (
            "Construcción de NFA para concatenación:\n"
            "1. Agregar ε-transiciones desde estados finales de L1 al estado inicial de L2\n"
            "2. Estados finales de L2 son los únicos estados finales del resultado\n"
            f"3. Estados: {len(dfa1.states)} + {len(dfa2.states)} = {len(dfa1.states) + len(dfa2.states)}"
        )
        
        self.operations_log.append(f"  → {description}")
        return description
    
    def kleene_star(self, dfa: FiniteAutomaton) -> str:
        """
        Estrella de Kleene: L* = {ε} ∪ L ∪ L² ∪ L³ ∪ ...
        
        Teorema: Si L es regular, entonces L* es regular
        
        Construcción:
        1. Crear nuevo estado inicial que también es final (para aceptar ε)
        2. Agregar ε-transiciones del nuevo inicial al antiguo inicial
        3. Agregar ε-transiciones de estados finales al nuevo inicial
        """
        self.operations_log.append(f"ESTRELLA DE KLEENE: L*")
        
        description = (
            "Construcción de NFA para estrella de Kleene:\n"
            "1. Nuevo estado inicial (también final) para aceptar ε\n"
            "2. ε-transición: nuevo_inicial → antiguo_inicial\n"
            "3. ε-transiciones: estados_finales → nuevo_inicial\n"
            f"4. Estados resultantes: {len(dfa.states) + 1}"
        )
        
        self.operations_log.append(f"  → {description}")
        return description
    
    def complement(self, dfa: FiniteAutomaton) -> FiniteAutomaton:
        """
        Complemento de un lenguaje: L' = Σ* - L
        
        Teorema: Si L es regular, entonces L' es regular
        
        Construcción: Invertir estados finales y no finales
        """
        self.operations_log.append(f"COMPLEMENTO: L'")
        
        result = FiniteAutomaton()
        result.alphabet = dfa.alphabet.copy()
        
        # Mapeo de estados
        state_map = {}
        
        for old_state in dfa.states:
            # Invertir finalidad
            new_state = State(old_state.id, not old_state.is_final)
            state_map[old_state] = new_state
            result.add_state(new_state)
            
            if old_state == dfa.initial_state:
                result.initial_state = new_state
        
        # Copiar transiciones
        for (from_state, symbol), to_state in dfa.transitions.items():
            result.add_transition(
                state_map[from_state],
                symbol,
                state_map[to_state]
            )
        
        self.operations_log.append(f"  → Estados finales: {len(dfa.final_states)} → {len(result.final_states)}")
        return result
    
    def intersection(self, dfa1: FiniteAutomaton, dfa2: FiniteAutomaton) -> FiniteAutomaton:
        """
        Intersección de dos lenguajes: L1 ∩ L2
        
        Teorema: Si L1 y L2 son regulares, entonces L1 ∩ L2 es regular
        
        Construcción: Producto cartesiano con regla:
        (q1, q2) es final si q1 es final EN L1 Y q2 es final EN L2
        """
        self.operations_log.append(f"INTERSECCIÓN: L1 ∩ L2")
        
        result = FiniteAutomaton()
        state_map = {}
        state_counter = 0
        
        for s1 in dfa1.states:
            for s2 in dfa2.states:
                # Estado es final si AMBOS son finales
                is_final = s1.is_final and s2.is_final
                new_state = State(state_counter, is_final)
                state_map[(s1, s2)] = new_state
                result.add_state(new_state)
                
                if s1 == dfa1.initial_state and s2 == dfa2.initial_state:
                    result.initial_state = new_state
                
                state_counter += 1
        
        # Crear transiciones
        alphabet = dfa1.alphabet & dfa2.alphabet  # Intersección de alfabetos
        for symbol in alphabet:
            for s1 in dfa1.states:
                for s2 in dfa2.states:
                    next1 = dfa1.transitions.get((s1, symbol))
                    next2 = dfa2.transitions.get((s2, symbol))
                    
                    if next1 and next2:
                        from_state = state_map[(s1, s2)]
                        to_state = state_map[(next1, next2)]
                        result.add_transition(from_state, symbol, to_state)
        
        self.operations_log.append(f"  → Estados resultantes: {len(result.states)}")
        return result
    
    def get_operations_report(self) -> str:
        """Genera reporte de operaciones realizadas"""
        report = []
        report.append("OPERACIONES DE CERRADURA EJECUTADAS")
        report.append("=" * 80)
        report.append("")
        for log in self.operations_log:
            report.append(log)
        report.append("")
        
        return '\n'.join(report)


class DecidabilityAnalyzer:
    """
    Análisis de Propiedades Decidibles
    
    Para lenguajes regulares, los siguientes problemas son DECIDIBLES:
    1. Problema del vacío: ¿L = ∅?
    2. Problema de finitud: ¿|L| < ∞?
    3. Problema de pertenencia: ¿w ∈ L?
    4. Problema de equivalencia: ¿L1 = L2?
    5. Problema de inclusión: ¿L1 ⊆ L2?
    """
    
    def __init__(self):
        self.analysis_results = {}
    
    def is_empty(self, dfa: FiniteAutomaton) -> Tuple[bool, str]:
        """
        Problema del Vacío: ¿L(A) = ∅?
        
        Algoritmo:
        1. Realizar búsqueda desde el estado inicial
        2. Si se alcanza algún estado final, L ≠ ∅
        3. Si no se alcanza ningún estado final, L = ∅
        
        Complejidad: O(n + m) donde n = estados, m = transiciones
        """
        if not dfa.initial_state:
            return True, "No hay estado inicial definido"
        
        # BFS desde estado inicial
        visited = set()
        queue = [dfa.initial_state]
        
        while queue:
            current = queue.pop(0)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Si encontramos un estado final, el lenguaje NO es vacío
            if current.is_final:
                explanation = (
                    f"El lenguaje NO es vacío.\n"
                    f"Se encontró camino al estado final {current} desde el estado inicial.\n"
                    f"Estados visitados: {len(visited)}"
                )
                self.analysis_results['emptiness'] = {
                    'is_empty': False,
                    'witness_state': str(current),
                    'states_explored': len(visited)
                }
                return False, explanation
            
            # Explorar transiciones
            for symbol in dfa.alphabet:
                key = (current, symbol)
                if key in dfa.transitions:
                    next_state = dfa.transitions[key]
                    if next_state not in visited:
                        queue.append(next_state)
        
        explanation = (
            f"El lenguaje ES vacío.\n"
            f"No existe camino desde el estado inicial a ningún estado final.\n"
            f"Estados explorados: {len(visited)}/{len(dfa.states)}"
        )
        
        self.analysis_results['emptiness'] = {
            'is_empty': True,
            'states_explored': len(visited),
            'total_states': len(dfa.states)
        }
        
        return True, explanation
    
    def is_finite(self, dfa: FiniteAutomaton) -> Tuple[bool, str]:
        """
        Problema de Finitud: ¿|L(A)| < ∞?
        
        Algoritmo:
        1. Encontrar todos los estados alcanzables desde el inicial
        2. Encontrar todos los estados desde los que se puede alcanzar un estado final
        3. Si existe un ciclo en la intersección de ambos conjuntos, L es infinito
        
        Complejidad: O(n²)
        """
        if not dfa.initial_state:
            return True, "No hay estado inicial (lenguaje vacío = finito)"
        
        # Encontrar estados alcanzables desde el inicial
        reachable_from_initial = self._find_reachable(dfa, dfa.initial_state, forward=True)
        
        # Encontrar estados desde los que se puede alcanzar un final
        can_reach_final = set()
        for state in dfa.states:
            if self._can_reach_final(dfa, state):
                can_reach_final.add(state)
        
        # Intersección: estados en caminos válidos (inicial → ... → final)
        valid_path_states = reachable_from_initial & can_reach_final
        
        # Buscar ciclos en estados válidos
        has_cycle, cycle_info = self._has_cycle_in_states(dfa, valid_path_states)
        
        if has_cycle:
            explanation = (
                f"El lenguaje es INFINITO.\n"
                f"Existe un ciclo en estados que están en caminos válidos: {cycle_info}\n"
                f"Estados en caminos válidos: {len(valid_path_states)}\n"
                f"Cualquier string puede ser 'bombeada' infinitamente."
            )
            
            self.analysis_results['finiteness'] = {
                'is_finite': False,
                'has_cycle': True,
                'cycle_info': cycle_info,
                'valid_path_states': len(valid_path_states)
            }
            
            return False, explanation
        else:
            explanation = (
                f"El lenguaje es FINITO.\n"
                f"No existen ciclos en caminos válidos.\n"
                f"Estados en caminos válidos: {len(valid_path_states)}\n"
                f"El lenguaje contiene un número finito de strings."
            )
            
            self.analysis_results['finiteness'] = {
                'is_finite': True,
                'has_cycle': False,
                'valid_path_states': len(valid_path_states)
            }
            
            return True, explanation
    
    def membership(self, dfa: FiniteAutomaton, word: str) -> Tuple[bool, str]:
        """
        Problema de Pertenencia: ¿w ∈ L(A)?
        
        Algoritmo: Simular el DFA con la palabra de entrada
        
        Complejidad: O(|w|) donde |w| = longitud de la palabra
        """
        if not dfa.initial_state:
            return False, "No hay estado inicial definido"
        
        current_state = dfa.initial_state
        path = [str(current_state)]
        
        for i, symbol in enumerate(word):
            key = (current_state, symbol)
            
            if key not in dfa.transitions:
                explanation = (
                    f"La palabra '{word}' NO pertenece al lenguaje.\n"
                    f"No hay transición desde {current_state} con símbolo '{symbol}' (posición {i}).\n"
                    f"Camino: {' → '.join(path)}"
                )
                
                self.analysis_results['membership'] = {
                    'word': word,
                    'accepted': False,
                    'failure_position': i,
                    'failure_symbol': symbol,
                    'path': path
                }
                
                return False, explanation
            
            current_state = dfa.transitions[key]
            path.append(f"{symbol}→{current_state}")
        
        if current_state.is_final:
            explanation = (
                f"La palabra '{word}' SÍ pertenece al lenguaje.\n"
                f"El autómata terminó en el estado final {current_state}.\n"
                f"Camino: {' '.join(path)}"
            )
            
            self.analysis_results['membership'] = {
                'word': word,
                'accepted': True,
                'final_state': str(current_state),
                'path': path
            }
            
            return True, explanation
        else:
            explanation = (
                f"La palabra '{word}' NO pertenece al lenguaje.\n"
                f"El autómata terminó en estado no final {current_state}.\n"
                f"Camino: {' '.join(path)}"
            )
            
            self.analysis_results['membership'] = {
                'word': word,
                'accepted': False,
                'final_state': str(current_state),
                'is_final': False,
                'path': path
            }
            
            return False, explanation
    
    def equivalence(self, dfa1: FiniteAutomaton, dfa2: FiniteAutomaton) -> Tuple[bool, str]:
        """
        Problema de Equivalencia: ¿L(A1) = L(A2)?
        
        Algoritmo: L1 = L2 si y solo si (L1 - L2) ∪ (L2 - L1) = ∅
        
        Complejidad: O(n1 × n2)
        """
        # Este algoritmo requiere operaciones de complemento e intersección
        # Simplificado para demostración
        
        explanation = (
            "Verificación de equivalencia:\n"
            f"1. Estados en A1: {len(dfa1.states)}\n"
            f"2. Estados en A2: {len(dfa2.states)}\n"
            f"3. Alfabeto A1: {sorted(dfa1.alphabet)}\n"
            f"4. Alfabeto A2: {sorted(dfa2.alphabet)}\n"
            "\nAlgoritmo completo requiere:\n"
            "   - Calcular (L1 - L2): L1 ∩ L2'\n"
            "   - Calcular (L2 - L1): L2 ∩ L1'\n"
            "   - Verificar si ambas diferencias son vacías\n"
        )
        
        self.analysis_results['equivalence'] = {
            'dfa1_states': len(dfa1.states),
            'dfa2_states': len(dfa2.states),
            'same_alphabet': dfa1.alphabet == dfa2.alphabet
        }
        
        return None, explanation
    
    def _find_reachable(self, dfa: FiniteAutomaton, start: State, forward: bool = True) -> Set[State]:
        """Encuentra todos los estados alcanzables desde un estado dado"""
        reachable = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            if current in reachable:
                continue
            
            reachable.add(current)
            
            for symbol in dfa.alphabet:
                key = (current, symbol)
                if key in dfa.transitions:
                    next_state = dfa.transitions[key]
                    if next_state not in reachable:
                        queue.append(next_state)
        
        return reachable
    
    def _can_reach_final(self, dfa: FiniteAutomaton, start: State) -> bool:
        """Verifica si desde un estado se puede alcanzar algún estado final"""
        visited = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            
            visited.add(current)
            
            if current.is_final:
                return True
            
            for symbol in dfa.alphabet:
                key = (current, symbol)
                if key in dfa.transitions:
                    next_state = dfa.transitions[key]
                    if next_state not in visited:
                        queue.append(next_state)
        
        return False
    
    def _has_cycle_in_states(self, dfa: FiniteAutomaton, states: Set[State]) -> Tuple[bool, str]:
        """Detecta si existe un ciclo en un conjunto de estados"""
        # DFS con detección de ciclos
        visited = set()
        rec_stack = set()
        
        def dfs(state):
            visited.add(state)
            rec_stack.add(state)
            
            for symbol in dfa.alphabet:
                key = (state, symbol)
                if key in dfa.transitions:
                    next_state = dfa.transitions[key]
                    
                    if next_state not in states:
                        continue
                    
                    if next_state in rec_stack:
                        return True, f"Ciclo encontrado: {state} --{symbol}--> {next_state}"
                    
                    if next_state not in visited:
                        has_cycle, info = dfs(next_state)
                        if has_cycle:
                            return True, info
            
            rec_stack.remove(state)
            return False, ""
        
        for state in states:
            if state not in visited:
                has_cycle, info = dfs(state)
                if has_cycle:
                    return True, info
        
        return False, "No hay ciclos"
    
    def get_analysis_report(self) -> str:
        """Genera reporte del análisis de decidibilidad"""
        report = []
        report.append("ANÁLISIS DE PROPIEDADES DECIDIBLES")
        report.append("=" * 80)
        report.append("")
        
        for property_name, results in self.analysis_results.items():
            report.append(f"{property_name.upper()}:")
            report.append("-" * 80)
            for key, value in results.items():
                report.append(f"  {key}: {value}")
            report.append("")
        
        return '\n'.join(report)


# Funciones de prueba
def test_closure_properties():
    """Prueba las propiedades de cerradura"""
    print("PRUEBA DE PROPIEDADES DE CERRADURA")
    print("=" * 80)
    
    # Crear dos DFAs simples
    dfa1 = FiniteAutomaton()
    q0 = State(0, False)
    q1 = State(1, True)
    dfa1.add_state(q0)
    dfa1.add_state(q1)
    dfa1.initial_state = q0
    dfa1.add_transition(q0, 'a', q1)
    dfa1.add_transition(q1, 'a', q1)
    
    dfa2 = FiniteAutomaton()
    p0 = State(0, True)
    p1 = State(1, False)
    dfa2.add_state(p0)
    dfa2.add_state(p1)
    dfa2.initial_state = p0
    dfa2.add_transition(p0, 'a', p1)
    dfa2.add_transition(p1, 'a', p0)
    
    closure = ClosureProperties()
    
    # Probar operaciones
    print("\n1. UNIÓN:")
    union_dfa = closure.union(dfa1, dfa2)
    print(f"   Estados resultantes: {len(union_dfa.states)}")
    
    print("\n2. COMPLEMENTO:")
    complement_dfa = closure.complement(dfa1)
    print(f"   Estados finales: {len(dfa1.final_states)} → {len(complement_dfa.final_states)}")
    
    print("\n3. INTERSECCIÓN:")
    intersection_dfa = closure.intersection(dfa1, dfa2)
    print(f"   Estados resultantes: {len(intersection_dfa.states)}")
    
    print("\n" + closure.get_operations_report())


def test_decidability():
    """Prueba el análisis de decidibilidad"""
    print("\n\nPRUEBA DE PROPIEDADES DECIDIBLES")
    print("=" * 80)
    
    # Crear DFA para pruebas
    dfa = FiniteAutomaton()
    q0 = State(0, False)
    q1 = State(1, False)
    q2 = State(2, True)
    
    dfa.add_state(q0)
    dfa.add_state(q1)
    dfa.add_state(q2)
    dfa.initial_state = q0
    
    dfa.add_transition(q0, 'a', q1)
    dfa.add_transition(q1, 'b', q2)
    dfa.add_transition(q2, 'a', q0)  # Ciclo
    
    analyzer = DecidabilityAnalyzer()
    
    # Problema del vacío
    print("\n1. PROBLEMA DEL VACÍO:")
    is_empty, explanation = analyzer.is_empty(dfa)
    print(explanation)
    
    # Problema de finitud
    print("\n2. PROBLEMA DE FINITUD:")
    is_finite, explanation = analyzer.is_finite(dfa)
    print(explanation)
    
    # Problema de pertenencia
    print("\n3. PROBLEMA DE PERTENENCIA:")
    words = ['ab', 'aba', 'abc', 'aa']
    for word in words:
        accepted, explanation = analyzer.membership(dfa, word)
        print(f"\n   Palabra: '{word}'")
        print(f"   Aceptada: {accepted}")
    
    print("\n" + analyzer.get_analysis_report())


if __name__ == "__main__":
    test_closure_properties()
    test_decidability()

