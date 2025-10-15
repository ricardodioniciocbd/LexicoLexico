"""
Intérprete de Código TAC
Ejecuta el código de tres direcciones y genera la salida
"""

from tac_generator import TACInstruction


class TACInterpreter:
    """Intérprete para código TAC"""
    
    def __init__(self):
        self.variables = {}
        self.output = []
        self.pc = 0
        self.labels = {}
    
    def interpret(self, instructions):
        """Ejecuta las instrucciones TAC"""
        self.variables = {}
        self.output = []
        self.pc = 0
        self.labels = {}
        
        for i, instr in enumerate(instructions):
            if instr.op == 'LABEL':
                self.labels[instr.arg1] = i
        
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            self.execute_instruction(instr)
            self.pc += 1
        
        return '\n'.join(self.output)
    
    def execute_instruction(self, instr):
        """Ejecuta una instrucción individual"""
        
        if instr.op == 'ASSIGN':
            value = self.get_value(instr.arg1)
            self.variables[instr.result] = value
        
        elif instr.op == 'ADD':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left + right
        
        elif instr.op == 'SUB':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left - right
        
        elif instr.op == 'MUL':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left * right
        
        elif instr.op == 'DIV':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            if right == 0:
                raise Exception("Error de ejecución: División por cero")
            self.variables[instr.result] = left / right
        
        elif instr.op == 'MOD':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            if right == 0:
                raise Exception("Error de ejecución: Módulo por cero")
            self.variables[instr.result] = left % right
        
        elif instr.op == 'NEG':
            value = self.get_value(instr.arg1)
            self.variables[instr.result] = -value
        
        elif instr.op == 'EQ':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left == right
        
        elif instr.op == 'NEQ':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left != right
        
        elif instr.op == 'LT':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left < right
        
        elif instr.op == 'GT':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left > right
        
        elif instr.op == 'LTE':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left <= right
        
        elif instr.op == 'GTE':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left >= right
        
        elif instr.op == 'PRINT':
            value = self.get_value(instr.arg1)
            self.output.append(str(value))
        
        elif instr.op == 'LABEL':
            pass
        
        elif instr.op == 'GOTO':
            if instr.arg1 in self.labels:
                self.pc = self.labels[instr.arg1] - 1
            else:
                raise Exception(f"Error de ejecución: Etiqueta no encontrada: {instr.arg1}")
        
        elif instr.op == 'IF_FALSE':
            condition = self.get_value(instr.arg1)
            if not condition:
                if instr.arg2 in self.labels:
                    self.pc = self.labels[instr.arg2] - 1
                else:
                    raise Exception(f"Error de ejecución: Etiqueta no encontrada: {instr.arg2}")
        
        elif instr.op == 'LIST_CREATE':
            self.variables[instr.result] = []
        
        elif instr.op == 'LIST_APPEND':
            list_var = self.variables.get(instr.arg1, [])
            value = self.get_value(instr.arg2)
            if isinstance(list_var, list):
                list_var.append(value)
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es una lista")
        
        elif instr.op == 'LIST_GET':
            list_var = self.get_value(instr.arg1)
            index = self.get_value(instr.arg2)
            if isinstance(list_var, list):
                if isinstance(index, (int, float)):
                    index = int(index)
                    if 0 <= index < len(list_var):
                        self.variables[instr.result] = list_var[index]
                    else:
                        raise Exception(f"Error de ejecución: Índice fuera de rango: {index}")
                else:
                    raise Exception(f"Error de ejecución: Índice debe ser número: {index}")
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es una lista")
        
        elif instr.op == 'LIST_SET':
            list_var = self.variables.get(instr.arg1, None)
            if isinstance(list_var, list):
                index = self.get_value(instr.arg2)
                if isinstance(index, (int, float)):
                    index = int(index)
                    value = self.get_value(instr.result)
                    if 0 <= index < len(list_var):
                        list_var[index] = value
                    else:
                        raise Exception(f"Error de ejecución: Índice fuera de rango: {index}")
                else:
                    raise Exception(f"Error de ejecución: Índice debe ser número")
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es una lista")
        
        elif instr.op == 'CALL':
            if instr.arg1 == 'len':
                list_var = self.get_value(instr.arg2)
                if isinstance(list_var, list):
                    self.variables[instr.result] = len(list_var)
                else:
                    raise Exception(f"Error de ejecución: len() requiere una lista")
    
    def get_value(self, operand):
        """Obtiene el valor de un operando (constante o variable)"""
        if operand is None:
            return None
        
        if isinstance(operand, str) and operand.startswith('"') and operand.endswith('"'):
            return operand[1:-1]
        
        try:
            if '.' in str(operand):
                return float(operand)
            else:
                return int(operand)
        except:
            pass
        
        if operand == 'True':
            return True
        if operand == 'False':
            return False
        
        if operand in self.variables:
            return self.variables[operand]
        
        raise Exception(f"Error de ejecución: Variable no definida: {operand}")
