"""
Optimizador de Código TAC
Aplica optimizaciones al código de tres direcciones
"""

from tac_generator import TACInstruction


class TACOptimizer:
    """Optimiza el código TAC aplicando diversas reglas"""
    
    def __init__(self):
        self.optimizations_applied = []
    
    def optimize(self, instructions):
        """Aplica todas las optimizaciones al código TAC"""
        self.optimizations_applied = []
        optimized = list(instructions)
        
        changed = True
        iteration = 0
        while changed and iteration < 10:
            changed = False
            old_len = len(optimized)
            
            optimized = self.constant_folding(optimized)
            optimized = self.constant_propagation(optimized)
            optimized = self.dead_code_elimination(optimized)
            optimized = self.strength_reduction(optimized)
            optimized = self.remove_redundant_assignments(optimized)
            optimized = self.eliminate_dead_jumps(optimized)
            
            if len(optimized) != old_len or iteration == 0:
                changed = True
            
            iteration += 1
        
        return optimized
    
    def constant_folding(self, instructions):
        """Plegado de constantes"""
        optimized = []
        
        for instr in instructions:
            if instr.op in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']:
                try:
                    left = self._parse_number(instr.arg1)
                    right = self._parse_number(instr.arg2)
                    
                    if left is not None and right is not None:
                        result = None
                        if instr.op == 'ADD':
                            result = left + right
                        elif instr.op == 'SUB':
                            result = left - right
                        elif instr.op == 'MUL':
                            result = left * right
                        elif instr.op == 'DIV' and right != 0:
                            result = left / right
                        elif instr.op == 'MOD' and right != 0:
                            result = left % right
                        
                        if result is not None:
                            optimized.append(TACInstruction('ASSIGN', str(result), None, instr.result))
                            self.optimizations_applied.append(
                                f"Plegado de constantes: {left} {instr.op} {right} = {result}"
                            )
                            continue
                except:
                    pass
            
            optimized.append(instr)
        
        return optimized
    
    def constant_propagation(self, instructions):
        """Propagación de constantes"""
        constants = {}
        optimized = []
        
        for instr in instructions:
            if instr.op == 'ASSIGN':
                const_val = self._parse_number(instr.arg1)
                if const_val is not None:
                    constants[instr.result] = instr.arg1
            
            new_instr = self._replace_with_constants(instr, constants)
            optimized.append(new_instr)
            
            if instr.op in ['ASSIGN', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'NEG']:
                if instr.result in constants:
                    del constants[instr.result]
        
        return optimized
    
    def dead_code_elimination(self, instructions):
        """Eliminación de código muerto"""
        changed = True
        used_vars = set()
        
        while changed:
            changed = False
            
            for instr in instructions:
                if instr.result and instr.result in used_vars:
                    if instr.arg1 and instr.arg1 not in used_vars:
                        used_vars.add(instr.arg1)
                        changed = True
                    if instr.arg2 and instr.arg2 not in used_vars:
                        used_vars.add(instr.arg2)
                        changed = True
                
                # IMPORTANTE: Las variables usadas en RETURN son necesarias
                if instr.op == 'RETURN':
                    if instr.arg1 and instr.arg1 not in used_vars:
                        used_vars.add(instr.arg1)
                        changed = True
                
                if instr.op in ['PRINT', 'IF_FALSE']:
                    if instr.arg1 and instr.arg1 not in used_vars:
                        used_vars.add(instr.arg1)
                        changed = True
                
                if instr.op == 'ASSIGN' and instr.result in used_vars:
                    if instr.arg1 and instr.arg1 not in used_vars:
                        used_vars.add(instr.arg1)
                        changed = True
                
                if instr.op in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE']:
                    if instr.result in used_vars:
                        if instr.arg1 and instr.arg1 not in used_vars:
                            used_vars.add(instr.arg1)
                            changed = True
                        if instr.arg2 and instr.arg2 not in used_vars:
                            used_vars.add(instr.arg2)
                            changed = True
                
                if instr.op in ['LIST_APPEND', 'LIST_GET', 'LIST_SET']:
                    if instr.arg1:
                        used_vars.add(instr.arg1)
                    if instr.arg2:
                        used_vars.add(instr.arg2)
                
                if instr.result and not instr.result.startswith('t') and not instr.result.startswith('_'):
                    used_vars.add(instr.result)
        
        optimized = []
        for instr in instructions:
            keep = True
            
            # IMPORTANTE: RETURN debe mantenerse siempre
            if instr.op in ['PRINT', 'LABEL', 'GOTO', 'IF_FALSE', 'LIST_CREATE', 
                           'LIST_APPEND', 'LIST_GET', 'LIST_SET', 'CALL', 'RETURN', 'INPUT']:
                keep = True
            elif instr.result:
                keep = instr.result in used_vars
            
            if keep:
                optimized.append(instr)
            else:
                self.optimizations_applied.append(
                    f"Código muerto eliminado: {str(instr)}"
                )
        
        return optimized
    
    def strength_reduction(self, instructions):
        """Reducción de fuerza"""
        optimized = []
        
        for instr in instructions:
            if instr.op == 'MUL':
                if instr.arg1 == '0' or instr.arg2 == '0':
                    optimized.append(TACInstruction('ASSIGN', '0', None, instr.result))
                    self.optimizations_applied.append(
                        f"Reducción de fuerza: multiplicación por 0 = 0"
                    )
                    continue
                elif instr.arg2 == '1':
                    optimized.append(TACInstruction('ASSIGN', instr.arg1, None, instr.result))
                    self.optimizations_applied.append(
                        f"Reducción de fuerza: {instr.arg1} * 1 = {instr.arg1}"
                    )
                    continue
                elif instr.arg1 == '1':
                    optimized.append(TACInstruction('ASSIGN', instr.arg2, None, instr.result))
                    self.optimizations_applied.append(
                        f"Reducción de fuerza: 1 * {instr.arg2} = {instr.arg2}"
                    )
                    continue
            
            if instr.op == 'ADD':
                if instr.arg2 == '0':
                    optimized.append(TACInstruction('ASSIGN', instr.arg1, None, instr.result))
                    self.optimizations_applied.append(
                        f"Reducción de fuerza: {instr.arg1} + 0 = {instr.arg1}"
                    )
                    continue
                elif instr.arg1 == '0':
                    optimized.append(TACInstruction('ASSIGN', instr.arg2, None, instr.result))
                    self.optimizations_applied.append(
                        f"Reducción de fuerza: 0 + {instr.arg2} = {instr.arg2}"
                    )
                    continue
            
            optimized.append(instr)
        
        return optimized
    
    def remove_redundant_assignments(self, instructions):
        """Elimina asignaciones redundantes"""
        optimized = []
        
        for instr in instructions:
            if instr.op == 'ASSIGN' and instr.arg1 == instr.result:
                self.optimizations_applied.append(
                    f"Asignación redundante eliminada: {instr.result} = {instr.arg1}"
                )
                continue
            optimized.append(instr)
        
        return optimized
    
    def eliminate_dead_jumps(self, instructions):
        """Elimina saltos innecesarios"""
        optimized = []
        
        for i, instr in enumerate(instructions):
            if instr.op == 'GOTO':
                if i + 1 < len(instructions):
                    next_instr = instructions[i + 1]
                    if next_instr.op == 'LABEL' and next_instr.arg1 == instr.arg1:
                        self.optimizations_applied.append(
                            f"Salto innecesario eliminado: goto {instr.arg1}"
                        )
                        continue
            
            optimized.append(instr)
        
        return optimized
    
    def _parse_number(self, value):
        """Intenta parsear un valor como número"""
        if value is None:
            return None
        try:
            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                return None
            return float(value) if '.' in str(value) else int(value)
        except:
            return None
    
    def _replace_with_constants(self, instr, constants):
        """Reemplaza variables con sus valores constantes conocidos"""
        new_arg1 = constants.get(instr.arg1, instr.arg1) if instr.arg1 else instr.arg1
        new_arg2 = constants.get(instr.arg2, instr.arg2) if instr.arg2 else instr.arg2
        
        if new_arg1 != instr.arg1 or new_arg2 != instr.arg2:
            return TACInstruction(instr.op, new_arg1, new_arg2, instr.result)
        
        return instr
    
    def get_optimizations_report(self):
        """Retorna un reporte de las optimizaciones aplicadas"""
        if not self.optimizations_applied:
            return "No se aplicaron optimizaciones."
        
        report = "OPTIMIZACIONES APLICADAS:\n"
        report += "=" * 100 + "\n\n"
        
        optimizations_by_type = {}
        for opt in self.optimizations_applied:
            opt_type = opt.split(':')[0]
            if opt_type not in optimizations_by_type:
                optimizations_by_type[opt_type] = []
            optimizations_by_type[opt_type].append(opt)
        
        for opt_type, opts in optimizations_by_type.items():
            report += f"{opt_type}:\n"
            for opt in opts:
                report += f"  - {opt}\n"
            report += "\n"
        
        report += f"Total de optimizaciones: {len(self.optimizations_applied)}\n"
        return report
