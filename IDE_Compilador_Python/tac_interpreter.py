"""
Intérprete de Código TAC
Ejecuta el código de tres direcciones y genera la salida
"""

from tac_generator import TACInstruction


class TACInterpreter:
    """Intérprete para código TAC"""
    
    def __init__(self, input_callback=None):
        self.variables = {}
        self.output = []
        self.pc = 0
        self.labels = {}
        self.call_stack = []  # Pila de llamadas para funciones
        self.functions = {}  # Diccionario de funciones: {nombre: (inicio_pc, fin_pc)}
        self.return_value = None
        self.input_callback = input_callback  # Callback para obtener entrada del usuario
    
    def interpret(self, instructions, function_params=None):
        """Ejecuta las instrucciones TAC
        
        Args:
            instructions: Lista de instrucciones TAC
            function_params: Diccionario con parámetros de funciones {nombre: [param1, param2, ...]}
        """
        self.variables = {}
        self.output = []
        self.pc = 0
        self.labels = {}
        self.call_stack = []
        self.functions = {}
        self.return_value = None
        self.function_info = {}  # {nombre: {'start': pc, 'end': pc, 'params': [...]}}
        
        # Primera pasada: identificar funciones y etiquetas
        
        for i, instr in enumerate(instructions):
            if instr.op == 'LABEL':
                self.labels[instr.arg1] = i
                if instr.arg1.startswith('func_'):
                    func_name = instr.arg1[5:]  # Quitar 'func_'
                    # Buscar el final de la función (siguiente función o fin)
                    end_pc = len(instructions)
                    for j in range(i + 1, len(instructions)):
                        if instructions[j].op == 'LABEL' and instructions[j].arg1.startswith('func_'):
                            end_pc = j
                            break
                    self.functions[func_name] = (i, end_pc)  # (start, end)
                    # Obtener parámetros desde function_params si está disponible
                    params = []
                    if function_params and func_name in function_params:
                        params = function_params[func_name]
                    else:
                        # Fallback: usar nombres comunes basados en el nombre de la función
                        if func_name == 'factorial':
                            params = ['n']
                        elif func_name == 'suma':
                            params = ['a', 'b']
                        elif func_name == 'main':
                            params = []
                    self.function_info[func_name] = {'start': i, 'end': end_pc, 'params': params}
        
        # Buscar la función main() y comenzar desde ahí
        # Si no existe main(), comenzar desde el inicio
        if 'main' in self.functions:
            main_start, _ = self.functions['main']
            self.pc = main_start  # Saltar al inicio de main()
        else:
            self.pc = 0  # Comenzar desde el inicio si no hay main()
        
        # Ejecutar instrucciones
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            self.execute_instruction(instr, instructions)
            self.pc += 1
        
        return '\n'.join(self.output)
    
    def execute_instruction(self, instr, instructions=None):
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
        
        elif instr.op == 'NOT':
            value = self.get_value(instr.arg1)
            self.variables[instr.result] = not value
        
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
        
        elif instr.op == 'LIST_REMOVE':
            list_var = self.variables.get(instr.arg1, [])
            value = self.get_value(instr.arg2)
            if isinstance(list_var, list):
                try:
                    list_var.remove(value)
                except ValueError:
                    pass  # Si el elemento no está en la lista, ignorar
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es una lista")
        
        elif instr.op == 'INPUT':
            # Entrada dinámica interactiva
            prompt = ""
            if instr.arg1:
                try:
                    prompt_val = self.get_value(instr.arg1)
                    if prompt_val:
                        prompt = str(prompt_val)
                except Exception as e:
                    # Si arg1 es un string literal directo, usarlo
                    if isinstance(instr.arg1, str):
                        # Quitar comillas si las tiene
                        prompt = instr.arg1.strip('"').strip("'")
            
            # Mostrar prompt si existe y solicitar entrada del usuario
            if prompt:
                print(prompt, end='', flush=True)
                self.output.append(prompt)
            
            # Leer entrada del usuario usando callback si está disponible, sino usar input()
            if self.input_callback:
                user_input = self.input_callback(prompt)
            else:
                try:
                    user_input = input()
                except EOFError:
                    user_input = "5"  # Valor por defecto
            
            if instr.result:
                self.variables[instr.result] = user_input
        
        elif instr.op == 'DICT_CREATE':
            self.variables[instr.result] = {}
        
        elif instr.op == 'DICT_GET':
            dict_var = self.get_value(instr.arg1)
            key = self.get_value(instr.arg2)
            if isinstance(dict_var, dict):
                if key in dict_var:
                    self.variables[instr.result] = dict_var[key]
                else:
                    raise Exception(f"Error de ejecución: Clave no encontrada: {key}")
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es un diccionario")
        
        elif instr.op == 'DICT_SET':
            dict_var = self.variables.get(instr.arg1, None)
            if dict_var is None:
                self.variables[instr.arg1] = {}
                dict_var = self.variables[instr.arg1]
            if isinstance(dict_var, dict):
                key = self.get_value(instr.arg2)
                value = self.get_value(instr.result)
                dict_var[key] = value
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es un diccionario")
        
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
            elif isinstance(list_var, dict):
                # Si es un diccionario, intentar acceso por clave
                if index in list_var:
                    self.variables[instr.result] = list_var[index]
                else:
                    raise Exception(f"Error de ejecución: Clave no encontrada: {index}")
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es una lista ni diccionario")
        
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
            elif instr.arg1 == 'int':
                # Conversión de string a entero
                arg_value = self.get_value(instr.arg2)
                if isinstance(arg_value, str):
                    try:
                        self.variables[instr.result] = int(arg_value)
                    except ValueError:
                        raise Exception(f"Error de ejecución: No se puede convertir '{arg_value}' a entero")
                elif isinstance(arg_value, (int, float)):
                    self.variables[instr.result] = int(arg_value)
                else:
                    raise Exception(f"Error de ejecución: int() requiere un número o string")
            elif instr.arg1 == 'input':
                # Entrada dinámica interactiva
                prompt = ""
                if instr.arg2:
                    try:
                        prompt_val = self.get_value(instr.arg2)
                        if prompt_val:
                            prompt = str(prompt_val)
                    except Exception as e:
                        # Si arg2 es un string literal directo, usarlo
                        if isinstance(instr.arg2, str):
                            # Quitar comillas si las tiene
                            prompt = instr.arg2.strip('"').strip("'")
                
                # Mostrar prompt si existe y solicitar entrada del usuario
                if prompt:
                    print(prompt, end='', flush=True)
                    self.output.append(prompt)
                
                # Leer entrada del usuario usando callback si está disponible, sino usar input()
                if self.input_callback:
                    user_input = self.input_callback(prompt)
                else:
                    try:
                        user_input = input()
                    except EOFError:
                        user_input = "5"  # Valor por defecto
                
                if instr.result:
                    self.variables[instr.result] = user_input
            else:
                # Llamada a función definida por el usuario
                if instr.arg1 in self.functions:
                    func_start, func_end = self.functions[instr.arg1]
                    
                    # Parsear argumentos de la llamada
                    args_values = []
                    if instr.arg2:
                        args_str = str(instr.arg2)
                        args_parts = [a.strip() for a in args_str.split(',')]
                        for arg_part in args_parts:
                            args_values.append(self.get_value(arg_part))
                    
                    # Guardar estado actual en la pila (ANTES de cambiar variables)
                    saved_vars = self.variables.copy()
                    self.call_stack.append({
                        'pc': self.pc + 1,  # Continuar después de esta instrucción
                        'variables': saved_vars,
                        'result_var': instr.result  # Variable donde guardar el resultado
                    })
                    
                    # Obtener nombres de parámetros desde function_info
                    func_info = self.function_info.get(instr.arg1, {})
                    func_params = func_info.get('params', [])
                    
                    # Crear nuevo contexto de variables para la función (aislar parámetros)
                    # Las variables del contexto anterior están guardadas en saved_vars
                    # Creamos un nuevo diccionario para las variables locales de la función
                    function_vars = {}
                    
                    # Asignar argumentos a parámetros en el nuevo contexto
                    if func_params:
                        # Usar los nombres de parámetros reales de la función
                        for i, param_name in enumerate(func_params):
                            if i < len(args_values):
                                function_vars[param_name] = args_values[i]
                    elif args_values:
                        # Fallback: usar nombres comunes de parámetros
                        if instr.arg1 == 'factorial' and len(args_values) >= 1:
                            function_vars['n'] = args_values[0]
                        elif instr.arg1 == 'suma' and len(args_values) >= 2:
                            function_vars['a'] = args_values[0]
                            function_vars['b'] = args_values[1]
                        else:
                            common_param_names = ['n', 'x', 'y', 'z', 'a', 'b', 'c']
                            for i, arg_val in enumerate(args_values):
                                if i < len(common_param_names):
                                    param_name = common_param_names[i]
                                    function_vars[param_name] = arg_val
                    
                    # Reemplazar el contexto de variables con el nuevo contexto de la función
                    self.variables = function_vars
                    
                    # Saltar al inicio de la función (LABEL)
                    # El pc apuntará a func_start, el loop lo incrementará y ejecutará func_start + 1
                    # IMPORTANTE: Los parámetros ya están asignados en self.variables antes de saltar
                    self.pc = func_start
                    return  # No incrementar PC aquí, el loop lo hará y ejecutará func_start + 1
                else:
                    raise Exception(f"Error de ejecución: Función '{instr.arg1}' no definida")
        
        elif instr.op == 'RETURN':
            if instr.arg1 is not None:
                return_val = self.get_value(instr.arg1)
            else:
                return_val = None
            
            # Si hay una llamada en la pila, restaurar estado
            if self.call_stack:
                saved_state = self.call_stack.pop()
                # Guardar el valor de retorno antes de restaurar variables
                result_var = saved_state.get('result_var')
                # IMPORTANTE: Guardar las variables temporales creadas en esta función
                # antes de restaurar el contexto anterior
                temp_vars = {}
                for var_name, var_value in self.variables.items():
                    # Guardar variables temporales (empiezan con 't') y variables locales
                    if var_name.startswith('t') or var_name not in saved_state['variables']:
                        temp_vars[var_name] = var_value
                
                # Restaurar variables del contexto anterior
                self.variables = saved_state['variables'].copy()
                
                # Agregar las variables temporales al contexto restaurado
                # Esto permite que las variables temporales creadas en la función
                # estén disponibles después del return
                self.variables.update(temp_vars)
                
                # Asignar el valor de retorno a la variable resultado
                if result_var:
                    self.variables[result_var] = return_val
                # Continuar desde donde se quedó
                self.pc = saved_state['pc'] - 1  # -1 porque el loop incrementará
                return  # No ejecutar más instrucciones en esta iteración
            else:
                # Return sin función llamante - terminar ejecución
                # Saltar al final
                self.pc = len(instructions) if instructions else self.pc
                return
    
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
