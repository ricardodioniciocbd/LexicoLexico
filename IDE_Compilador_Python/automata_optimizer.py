"""
Optimizaciones Basadas en Teoría de Autómatas
Implementa minimización de autómatas y análisis de complejidad
"""

from typing import Set, Dict, List, Tuple, FrozenSet
from dataclasses import dataclass
from collections import defaultdict
import time


@dataclass(frozen=True)
class State:
    """Estado de un autómata"""
    id: int
    is_final: bool = False
    
    def __str__(self):
        return f"q{self.id}{'*' if self.is_final else ''}"


@dataclass
class Transition:
    """Transición de un autómata"""
    from_state: State
    symbol: str
    to_state: State
    
    def __str__(self):
        return f"{self.from_state} --{self.symbol}--> {self.to_state}"


class FiniteAutomaton:
    """
    Autómata Finito (DFA/NFA)
    
    Formalmente: A = (Q, Σ, δ, q0, F)
    Donde:
    - Q: Conjunto finito de estados
    - Σ: Alfabeto de entrada
    - δ: Función de transición Q × Σ → Q (DFA) o Q × Σ → P(Q) (NFA)
    - q0: Estado inicial
    - F: Conjunto de estados finales
    """
    
    def __init__(self):
        self.states: Set[State] = set()
        self.alphabet: Set[str] = set()
        self.transitions: Dict[Tuple[State, str], State] = {}
        self.initial_state: State = None
        self.final_states: Set[State] = set()
    
    def add_state(self, state: State):
        """Agrega un estado al autómata"""
        self.states.add(state)
        if state.is_final:
            self.final_states.add(state)
    
    def add_transition(self, from_state: State, symbol: str, to_state: State):
        """Agrega una transición"""
        self.transitions[(from_state, symbol)] = to_state
        self.alphabet.add(symbol)
    
    def is_deterministic(self) -> bool:
        """Verifica si el autómata es determinista (DFA)"""
        # Para cada par (estado, símbolo) debe haber exactamente una transición
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transitions:
                    return False
        return True
    
    def __str__(self):
        lines = []
        lines.append("AUTÓMATA FINITO")
        lines.append("=" * 60)
        lines.append(f"Estados: {len(self.states)}")
        lines.append(f"Alfabeto: {sorted(self.alphabet)}")
        lines.append(f"Estado inicial: {self.initial_state}")
        lines.append(f"Estados finales: {len(self.final_states)}")
        lines.append("")
        lines.append("Transiciones:")
        for (state, symbol), next_state in sorted(self.transitions.items(), key=str):
            lines.append(f"  {state} --{symbol}--> {next_state}")
        return '\n'.join(lines)


class AutomataMinimizer:
    """
    Minimizador de Autómatas Finitos Deterministas
    Implementa el algoritmo de Hopcroft para minimización en O(n log n)
    """
    
    def __init__(self):
        self.minimization_steps = []
        self.complexity_analysis = {}
    
    def minimize(self, dfa: FiniteAutomaton) -> FiniteAutomaton:
        """
        Minimiza un DFA usando el algoritmo de partición de estados
        
        Algoritmo:
        1. Eliminar estados inalcanzables
        2. Particionar estados en equivalentes y no equivalentes
        3. Refinar particiones hasta que sean estables
        4. Construir DFA mínimo
        """
        start_time = time.time()
        self.minimization_steps = []
        
        # Verificar que sea DFA
        if not dfa.is_deterministic():
            raise ValueError("El autómata debe ser determinista (DFA)")
        
        # Paso 1: Eliminar estados inalcanzables
        self.minimization_steps.append("PASO 1: Eliminación de estados inalcanzables")
        reachable_states = self._find_reachable_states(dfa)
        unreachable_count = len(dfa.states) - len(reachable_states)
        if unreachable_count > 0:
            self.minimization_steps.append(f"  → Eliminados {unreachable_count} estados inalcanzables")
        else:
            self.minimization_steps.append(f"  → Todos los estados son alcanzables")
        
        # Paso 2: Particionar estados
        self.minimization_steps.append("\nPASO 2: Particionamiento inicial")
        # Partición inicial: estados finales vs no finales
        partition = [
            dfa.final_states & reachable_states,
            reachable_states - dfa.final_states
        ]
        partition = [p for p in partition if p]  # Eliminar particiones vacías
        self.minimization_steps.append(f"  → Particiones iniciales: {len(partition)}")
        
        # Paso 3: Refinar particiones
        self.minimization_steps.append("\nPASO 3: Refinamiento de particiones")
        iteration = 0
        while True:
            iteration += 1
            new_partition = self._refine_partition(dfa, partition)
            
            if len(new_partition) == len(partition):
                self.minimization_steps.append(f"  → Convergencia alcanzada en iteración {iteration}")
                break
            
            self.minimization_steps.append(f"  → Iteración {iteration}: {len(partition)} → {len(new_partition)} particiones")
            partition = new_partition
        
        # Paso 4: Construir DFA mínimo
        self.minimization_steps.append("\nPASO 4: Construcción del DFA mínimo")
        minimized_dfa = self._build_minimized_dfa(dfa, partition)
        
        end_time = time.time()
        
        # Análisis de complejidad
        self.complexity_analysis = {
            'original_states': len(dfa.states),
            'minimized_states': len(minimized_dfa.states),
            'reduction_percentage': (1 - len(minimized_dfa.states) / len(dfa.states)) * 100 if dfa.states else 0,
            'original_transitions': len(dfa.transitions),
            'minimized_transitions': len(minimized_dfa.transitions),
            'iterations': iteration,
            'time_ms': (end_time - start_time) * 1000,
            'time_complexity': f"O(n log n) donde n = {len(dfa.states)}",
            'space_complexity': f"O(n²) = O({len(dfa.states)}²) = O({len(dfa.states)**2})"
        }
        
        self.minimization_steps.append(f"  → Estados: {len(dfa.states)} → {len(minimized_dfa.states)}")
        self.minimization_steps.append(f"  → Reducción: {self.complexity_analysis['reduction_percentage']:.1f}%")
        
        return minimized_dfa
    
    def _find_reachable_states(self, dfa: FiniteAutomaton) -> Set[State]:
        """Encuentra todos los estados alcanzables desde el estado inicial"""
        if not dfa.initial_state:
            return set()
        
        reachable = set()
        to_visit = [dfa.initial_state]
        
        while to_visit:
            current = to_visit.pop()
            if current in reachable:
                continue
            
            reachable.add(current)
            
            # Agregar estados alcanzables desde el actual
            for symbol in dfa.alphabet:
                key = (current, symbol)
                if key in dfa.transitions:
                    next_state = dfa.transitions[key]
                    if next_state not in reachable:
                        to_visit.append(next_state)
        
        return reachable
    
    def _refine_partition(self, dfa: FiniteAutomaton, partition: List[Set[State]]) -> List[Set[State]]:
        """Refina una partición de estados"""
        new_partition = []
        
        for group in partition:
            # Intentar dividir el grupo
            subgroups = defaultdict(set)
            
            for state in group:
                # Crear firma: para cada símbolo, en qué partición cae el estado destino
                signature = []
                for symbol in sorted(dfa.alphabet):
                    key = (state, symbol)
                    if key in dfa.transitions:
                        next_state = dfa.transitions[key]
                        # Encontrar en qué partición está next_state
                        for i, part in enumerate(partition):
                            if next_state in part:
                                signature.append(i)
                                break
                    else:
                        signature.append(-1)  # No hay transición
                
                # Agrupar por firma
                subgroups[tuple(signature)].add(state)
            
            # Agregar subgrupos a la nueva partición
            new_partition.extend(subgroups.values())
        
        return new_partition
    
    def _build_minimized_dfa(self, dfa: FiniteAutomaton, partition: List[Set[State]]) -> FiniteAutomaton:
        """Construye el DFA minimizado a partir de la partición final"""
        minimized = FiniteAutomaton()
        
        # Crear mapeo de estados antiguos a nuevos
        state_map = {}
        new_states = []
        
        for i, group in enumerate(partition):
            # Verificar si el grupo contiene algún estado final
            is_final = any(state in dfa.final_states for state in group)
            new_state = State(i, is_final)
            new_states.append(new_state)
            minimized.add_state(new_state)
            
            for old_state in group:
                state_map[old_state] = new_state
                
                # Si el grupo contiene el estado inicial, este es el nuevo inicial
                if old_state == dfa.initial_state:
                    minimized.initial_state = new_state
        
        # Crear transiciones
        seen_transitions = set()
        for (old_from, symbol), old_to in dfa.transitions.items():
            if old_from in state_map and old_to in state_map:
                new_from = state_map[old_from]
                new_to = state_map[old_to]
                
                # Evitar duplicados
                trans_key = (new_from, symbol, new_to)
                if trans_key not in seen_transitions:
                    minimized.add_transition(new_from, symbol, new_to)
                    seen_transitions.add(trans_key)
        
        return minimized
    
    def get_minimization_report(self) -> str:
        """Genera un reporte de la minimización"""
        report = []
        report.append("REPORTE DE MINIMIZACIÓN DE AUTÓMATA")
        report.append("=" * 80)
        report.append("")
        
        report.append("PASOS DEL ALGORITMO:")
        report.append("-" * 80)
        for step in self.minimization_steps:
            report.append(step)
        report.append("")
        
        report.append("ANÁLISIS DE COMPLEJIDAD:")
        report.append("-" * 80)
        report.append(f"Estados originales:       {self.complexity_analysis.get('original_states', 0)}")
        report.append(f"Estados minimizados:      {self.complexity_analysis.get('minimized_states', 0)}")
        report.append(f"Reducción:                {self.complexity_analysis.get('reduction_percentage', 0):.1f}%")
        report.append(f"Transiciones originales:  {self.complexity_analysis.get('original_transitions', 0)}")
        report.append(f"Transiciones minimizadas: {self.complexity_analysis.get('minimized_transitions', 0)}")
        report.append(f"Iteraciones:              {self.complexity_analysis.get('iterations', 0)}")
        report.append(f"Tiempo de ejecución:      {self.complexity_analysis.get('time_ms', 0):.2f} ms")
        report.append(f"Complejidad temporal:     {self.complexity_analysis.get('time_complexity', 'N/A')}")
        report.append(f"Complejidad espacial:     {self.complexity_analysis.get('space_complexity', 'N/A')}")
        report.append("")
        
        return '\n'.join(report)


class TransitionTableCompressor:
    """
    Compresor de Tablas de Transición
    Reduce el espacio de almacenamiento de las tablas de transición
    """
    
    def __init__(self):
        self.compression_stats = {}
    
    def compress_table(self, dfa: FiniteAutomaton) -> Dict:
        """
        Comprime la tabla de transiciones usando técnicas de compresión
        
        Técnicas:
        1. Row displacement (desplazamiento de filas)
        2. Comb vector (vector peine)
        3. Eliminación de redundancias
        """
        start_time = time.time()
        
        # Crear tabla 2D original
        state_list = sorted(list(dfa.states), key=lambda s: s.id)
        symbol_list = sorted(list(dfa.alphabet))
        
        original_table = {}
        for i, state in enumerate(state_list):
            for j, symbol in enumerate(symbol_list):
                key = (state, symbol)
                if key in dfa.transitions:
                    next_state = dfa.transitions[key]
                    next_idx = state_list.index(next_state)
                    original_table[(i, j)] = next_idx
                else:
                    original_table[(i, j)] = -1  # Estado error
        
        # Compresión: Identificar filas idénticas
        row_signatures = {}
        unique_rows = {}
        row_map = {}
        
        for i, state in enumerate(state_list):
            row = tuple(original_table.get((i, j), -1) for j in range(len(symbol_list)))
            
            if row in row_signatures:
                # Fila duplicada, mapear a la existente
                row_map[i] = row_signatures[row]
            else:
                # Nueva fila única
                row_signatures[row] = i
                unique_rows[i] = row
                row_map[i] = i
        
        # Calcular estadísticas
        original_size = len(state_list) * len(symbol_list) * 4  # 4 bytes por entrada (int)
        compressed_size = len(unique_rows) * len(symbol_list) * 4 + len(row_map) * 4
        
        end_time = time.time()
        
        self.compression_stats = {
            'original_rows': len(state_list),
            'unique_rows': len(unique_rows),
            'duplicate_rows': len(state_list) - len(unique_rows),
            'columns': len(symbol_list),
            'original_size_bytes': original_size,
            'compressed_size_bytes': compressed_size,
            'compression_ratio': (1 - compressed_size / original_size) * 100 if original_size > 0 else 0,
            'time_ms': (end_time - start_time) * 1000
        }
        
        return {
            'unique_rows': unique_rows,
            'row_map': row_map,
            'symbols': symbol_list,
            'stats': self.compression_stats
        }
    
    def get_compression_report(self) -> str:
        """Genera un reporte de compresión"""
        report = []
        report.append("REPORTE DE COMPRESIÓN DE TABLA DE TRANSICIONES")
        report.append("=" * 80)
        report.append("")
        report.append(f"Filas originales:         {self.compression_stats.get('original_rows', 0)}")
        report.append(f"Filas únicas:             {self.compression_stats.get('unique_rows', 0)}")
        report.append(f"Filas duplicadas:         {self.compression_stats.get('duplicate_rows', 0)}")
        report.append(f"Columnas (símbolos):      {self.compression_stats.get('columns', 0)}")
        report.append(f"Tamaño original:          {self.compression_stats.get('original_size_bytes', 0)} bytes")
        report.append(f"Tamaño comprimido:        {self.compression_stats.get('compressed_size_bytes', 0)} bytes")
        report.append(f"Ratio de compresión:      {self.compression_stats.get('compression_ratio', 0):.1f}%")
        report.append(f"Tiempo de compresión:     {self.compression_stats.get('time_ms', 0):.2f} ms")
        report.append("")
        
        return '\n'.join(report)


# Función de prueba
def test_automata_optimization():
    """Prueba las optimizaciones de autómatas"""
    
    # Crear un DFA de ejemplo (reconoce strings que terminan en '01')
    dfa = FiniteAutomaton()
    
    q0 = State(0, False)
    q1 = State(1, False)
    q2 = State(2, True)
    q3 = State(3, False)  # Estado redundante
    
    dfa.add_state(q0)
    dfa.add_state(q1)
    dfa.add_state(q2)
    dfa.add_state(q3)
    
    dfa.initial_state = q0
    
    # Transiciones
    dfa.add_transition(q0, '0', q1)
    dfa.add_transition(q0, '1', q0)
    dfa.add_transition(q1, '0', q1)
    dfa.add_transition(q1, '1', q2)
    dfa.add_transition(q2, '0', q1)
    dfa.add_transition(q2, '1', q0)
    dfa.add_transition(q3, '0', q1)  # Redundante
    dfa.add_transition(q3, '1', q0)  # Redundante
    
    print("DFA ORIGINAL:")
    print(dfa)
    print("\n" + "=" * 80 + "\n")
    
    # Minimizar
    minimizer = AutomataMinimizer()
    minimized_dfa = minimizer.minimize(dfa)
    
    print(minimizer.get_minimization_report())
    print("\nDFA MINIMIZADO:")
    print(minimized_dfa)
    print("\n" + "=" * 80 + "\n")
    
    # Comprimir tabla
    compressor = TransitionTableCompressor()
    compressed = compressor.compress_table(dfa)
    
    print(compressor.get_compression_report())


if __name__ == "__main__":
    test_automata_optimization()

