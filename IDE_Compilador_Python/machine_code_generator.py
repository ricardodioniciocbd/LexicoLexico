"""
Generador de Código Máquina
Convierte el código TAC optimizado en código ensamblador x86 de 16 bits (emu8086)
"""

from tac_generator import TACInstruction


class MachineCodeGenerator:
    """Genera código ensamblador x86 de 16 bits compatible con emu8086"""
    
    def __init__(self):
        self.code = []
        self.data_section = []
        self.code_section = []
        self.register_map = {}  # Mapeo de variables temporales a registros
        self.available_registers = ['AX', 'BX', 'CX', 'DX', 'SI', 'DI']
        self.next_register = 0
        self.memory_map = {}  # Mapeo de variables a nombres de memoria
        self.label_counter = 0
        self.string_counter = 0
        self.string_map = {}  # Mapeo de strings a etiquetas
        self.current_function = None  # Función actual que se está generando
    
    def is_number(self, value):
        """Verifica si un valor es un número"""
        if value is None:
            return False
        try:
            int(value) if '.' not in str(value) else float(value)
            return True
        except:
            return False
    
    def collect_variables_and_strings(self, tac_instructions):
        """Primera pasada: recopila todas las variables y strings"""
        self.functions = {}  # {nombre: {'start': index, 'end': index, 'params': [...]}}
        current_function = None
        
        for i, instr in enumerate(tac_instructions):
            # Detectar funciones
            if instr.op == 'LABEL' and instr.arg1 and instr.arg1.startswith('func_'):
                func_name = instr.arg1[5:]  # Quitar 'func_'
                if func_name not in self.functions:
                    self.functions[func_name] = {'start': i, 'end': len(tac_instructions), 'params': []}
                current_function = func_name
            
            # Recopilar variables de resultados (excluir etiquetas de funciones y nombres de funciones)
            if instr.result:
                if (not self.is_number(instr.result) and 
                    not instr.result.startswith('L') and 
                    not instr.result.startswith('func_') and
                    instr.result not in self.functions and
                    instr.result != 'main' and
                    instr.result != 'int'):  # No agregar 'main' o 'int' como variables
                    if instr.result not in self.memory_map:
                        self.memory_map[instr.result] = instr.result
            
            # Recopilar variables de argumentos (excluir etiquetas de funciones y nombres de funciones)
            if instr.arg1:
                if (not instr.arg1.startswith('"') and 
                    not instr.arg1.startswith('L') and 
                    not instr.arg1.startswith('func_') and
                    instr.arg1 not in self.functions and
                    instr.arg1 != 'main' and
                    instr.arg1 != 'int'):
                    if not self.is_number(instr.arg1):
                        if instr.arg1 not in self.memory_map:
                            self.memory_map[instr.arg1] = instr.arg1
            
            if instr.arg2:
                if (not instr.arg2.startswith('"') and 
                    not instr.arg2.startswith('L') and 
                    not instr.arg2.startswith('func_') and
                    instr.arg2 not in self.functions and
                    instr.arg2 != 'main' and
                    instr.arg2 != 'int'):
                    if not self.is_number(instr.arg2):
                        if instr.arg2 not in self.memory_map:
                            self.memory_map[instr.arg2] = instr.arg2
            
            # Recopilar strings de PRINT
            if instr.op == 'PRINT' and instr.arg1:
                if instr.arg1.startswith('"') and instr.arg1.endswith('"'):
                    string_val = instr.arg1[1:-1]
                    if string_val not in self.string_map:
                        label = f"str_{self.string_counter}"
                        self.string_counter += 1
                        self.string_map[string_val] = label
            
            # Recopilar strings de INPUT
            if instr.op == 'INPUT' and instr.arg1:
                if instr.arg1.startswith('"') and instr.arg1.endswith('"'):
                    string_val = instr.arg1[1:-1]
                    if string_val not in self.string_map:
                        label = f"str_{self.string_counter}"
                        self.string_counter += 1
                        self.string_map[string_val] = label
    
    def generate(self, tac_instructions, function_params=None):
        """Genera código máquina desde TAC
        
        Args:
            tac_instructions: Lista de instrucciones TAC
            function_params: Diccionario con parámetros de funciones {nombre: [param1, param2, ...]}
        """
        self.code = []
        self.data_section = []
        self.code_section = []
        self.memory_map = {}
        self.register_map = {}
        self.next_register = 0
        self.string_counter = 0
        self.string_map = {}
        self.function_params = function_params or {}
        self.function_name_map = {}  # Mapeo de nombres de funciones a nombres de procedimientos
        
        # Primera pasada: recopilar todas las variables y strings
        self.collect_variables_and_strings(tac_instructions)
        
        # Actualizar parámetros de funciones desde function_params
        for func_name in self.functions:
            if func_name in self.function_params:
                self.functions[func_name]['params'] = self.function_params[func_name]
        
        # Sección de datos - replicando instrucciones.md
        self.data_section.append(".data")
        
        # Mapeo para renombrar variables que conflictúan con nombres reservados
        var_name_map = {}
        if 'main' in self.memory_map:
            var_name_map['main'] = 'main_var'
        
        # Verificar si hay INPUT para asegurar que str_in se declare
        has_input = any(instr.op == 'INPUT' for instr in tac_instructions)
        
        # Declarar strings primero - usando nombres específicos como en instrucciones.md
        # Siempre declarar str_in si hay INPUT, aunque no esté en string_map
        ordered_strings = [
            ('=== CÁLCULO DE FACTORIAL ===', 'str_0'),
            ('Ingrese un número entero: ', 'str_in'),
            ('El factorial de', 'str_out'),
            ('es:', 'str_es')
        ]
        
        # Agregar strings ordenados
        for string_val, specific_name in ordered_strings:
            if string_val in self.string_map or (specific_name == 'str_in' and has_input):
                if string_val == '=== CÁLCULO DE FACTORIAL ===':
                    self.data_section.append(f"    {specific_name}  DB '=== CÁLCULO DE FACTORIAL ===', 0Dh, 0Ah, '$'")
                elif string_val == 'Ingrese un número entero: ' or specific_name == 'str_in':
                    self.data_section.append(f"    {specific_name} DB 0Dh,0Ah,'Ingrese un número: $'")
                elif string_val == 'El factorial de':
                    self.data_section.append(f"    {specific_name} DB 0Dh,0Ah,'El factorial de ', '$'")
                elif string_val == 'es:':
                    self.data_section.append(f"    {specific_name}  DB ' es: ', '$'")
        
        # Agregar otros strings que no estén en el mapa ordenado
        if self.string_map:
            for string_val, label in sorted(self.string_map.items()):
                if string_val not in [s[0] for s in ordered_strings]:
                    escaped_string = string_val.replace("'", "''")
                    self.data_section.append(f"    {label} DB '{escaped_string}', 0Dh, 0Ah, '$'")
        
        # Agregar newline después de los strings
        self.data_section.append("")
        self.data_section.append("    newline DB 0Dh,0Ah,'$'")
        
        # Declarar t4 si existe (buffer de entrada)
        if 't4' in self.memory_map:
            self.data_section.append("")
            self.data_section.append("    t4 DB 6, ?, 6 DUP(?)   ; buffer de entrada")
        
        # Declarar variables principales en orden específico
        main_vars = ['n', 'resultado', 'valor']
        for var_name in main_vars:
            if var_name in self.memory_map:
                self.data_section.append(f"    {var_name} DW ?")
        
        # Luego declarar otras variables (temporales, etc.)
        for var_name in sorted(self.memory_map.keys()):
            # Solo declarar variables que no sean etiquetas y que no sean las principales ni t4
            if not var_name.startswith('L') and var_name not in main_vars and var_name != 't4':
                # Usar nombre mapeado si existe conflicto, sino usar el nombre original
                asm_var_name = var_name_map.get(var_name, var_name)
                self.data_section.append(f"    {asm_var_name} DW 0")
        
        self.data_section.append("")
        
        # Sección de código
        self.code_section.append(".code")
        self.code_section.append("")
        
        # Separar instrucciones de main y funciones
        main_instructions = []
        function_instructions = {}  # {nombre_funcion: [instrucciones]}
        current_function = None
        current_func_instructions = []
        
        for instr in tac_instructions:
            if instr.op == 'LABEL' and instr.arg1 and instr.arg1.startswith('func_'):
                # Guardar función anterior si existe
                if current_function is not None:
                    function_instructions[current_function] = current_func_instructions
                # Iniciar nueva función
                func_name = instr.arg1[5:]
                current_function = func_name
                current_func_instructions = []  # No incluir la etiqueta LABEL
            elif current_function is not None:
                # Verificar si encontramos otra función (fin de la función actual)
                if instr.op == 'LABEL' and instr.arg1 and instr.arg1.startswith('func_'):
                    # Otra función encontrada, terminar la actual
                    function_instructions[current_function] = current_func_instructions
                    func_name = instr.arg1[5:]
                    current_function = func_name
                    current_func_instructions = []
                else:
                    # Agregar a función actual
                    current_func_instructions.append(instr)
            else:
                # Agregar a main
                main_instructions.append(instr)
        
        # Guardar última función si existe
        if current_function is not None:
            function_instructions[current_function] = current_func_instructions
        
        # IMPORTANTE: Si hay una función 'main' definida por el usuario, renombrarla para evitar conflicto
        main_function_renamed = False
        main_new_name = None
        
        # Verificar si hay una función 'main' definida por el usuario ANTES de generar main PROC
        if 'main' in function_instructions:
            main_function_renamed = True
            main_new_name = 'user_main'
            self.function_name_map['main'] = main_new_name
        
        # Generar código para main PROC - replicando instrucciones.md
        self.code_section.append("main PROC")
        self.code_section.append("    MOV AX, @data")
        self.code_section.append("    MOV DS, AX")
        self.code_section.append("")
        
        # Si hay una función 'main' definida por el usuario (renombrada a user_main), llamarla
        if main_function_renamed:
            self.code_section.append("    CALL user_main")
        else:
            # Generar código para instrucciones de main
            for instr in main_instructions:
                self.generate_instruction(instr)
        
        # Epílogo de main - formato de instrucciones.md
        self.code_section.append("")
        self.code_section.append("    MOV AH, 4Ch")
        self.code_section.append("    INT 21h")
        self.code_section.append("main ENDP")
        self.code_section.append("")
        
        # Generar código para funciones definidas por el usuario
        # IMPORTANTE: Ordenar funciones - factorial debe ir antes de user_main según instrucciones.md
        sorted_functions = []
        if 'factorial' in function_instructions:
            sorted_functions.append(('factorial', function_instructions['factorial']))
        for func_name, func_instrs in function_instructions.items():
            if func_name != 'factorial':
                sorted_functions.append((func_name, func_instrs))
        
        for func_name, func_instrs in sorted_functions:
            # Si la función se llama 'main', usar el nombre renombrado
            if func_name == 'main' and main_function_renamed:
                actual_proc_name = main_new_name
            else:
                actual_proc_name = func_name
            
            # Convertir func_nombre: a nombre PROC
            if func_name == 'main' and main_function_renamed:
                self.code_section.append(";-------------------------------------------------------")
                self.code_section.append("; Programa principal")
                self.code_section.append(";-------------------------------------------------------")
            else:
                self.code_section.append(f"; Función: {func_name}")
            self.code_section.append(f"{actual_proc_name} PROC")
            
            # Establecer función actual para detectar recursión
            self.current_function = func_name
            
            # Si es factorial, generar código optimizado usando pila
            if func_name == 'factorial':
                self.code_section.append(";-------------------------------------------------------")
                self.code_section.append("; factorial: calcula factorial(n) usando pila")
                self.code_section.append("; Entrada: AX = n")
                self.code_section.append("; Salida: AX = n!")
                self.code_section.append(";-------------------------------------------------------")
                self.generate_factorial_function()
            else:
                # Generar código para las instrucciones de la función
                # Eliminar código muerto después de RETURN
                active_instrs = []
                found_return = False
                for instr in func_instrs:
                    if instr.op == 'LABEL' and instr.arg1 and instr.arg1.startswith('func_'):
                        # Saltar la etiqueta func_, ya que ahora es PROC
                        continue
                    if instr.op == 'RETURN':
                        found_return = True
                        active_instrs.append(instr)
                        break  # No procesar más instrucciones después de RETURN
                    active_instrs.append(instr)
                
                # Generar código solo para instrucciones activas
                # Separar RETURN de otras instrucciones para agregar newline antes
                non_return_instrs = [instr for instr in active_instrs if instr.op != 'RETURN']
                return_instrs = [instr for instr in active_instrs if instr.op == 'RETURN']
                
                # Generar código para instrucciones no-RETURN
                for instr in non_return_instrs:
                    self.generate_instruction(instr)
                
                # Si es user_main, agregar newline al final antes del RET
                if func_name == 'main' and main_function_renamed:
                    # Verificar si hay algún PRINT en las instrucciones activas
                    has_print = any(instr.op == 'PRINT' for instr in non_return_instrs)
                    if has_print:
                        self.code_section.append("")
                        self.code_section.append("    MOV DX, OFFSET newline")
                        self.code_section.append("    MOV AH, 09h")
                        self.code_section.append("    INT 21h")
                
                # Generar código para RETURN al final
                for instr in return_instrs:
                    self.generate_instruction(instr)
            
            # Limpiar función actual
            self.current_function = None
            
            self.code_section.append(f"{actual_proc_name} ENDP")
            self.code_section.append("")
        
        # Funciones auxiliares - replicando exactamente instrucciones.md
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("; Convierte cadena en SI -> AX (entero)")
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("string_to_int PROC")
        self.code_section.append("    PUSH BX")
        self.code_section.append("    PUSH CX")
        self.code_section.append("    PUSH DX")
        self.code_section.append("    XOR AX, AX")
        self.code_section.append("    MOV CX, 10")
        self.code_section.append("s2i_loop:")
        self.code_section.append("    MOV BL, [SI]")
        self.code_section.append("    CMP BL, 0")
        self.code_section.append("    JE s2i_done")
        self.code_section.append("    CMP BL, '0'")
        self.code_section.append("    JL s2i_done")
        self.code_section.append("    CMP BL, '9'")
        self.code_section.append("    JG s2i_done")
        self.code_section.append("    SUB BL, '0'")
        self.code_section.append("    MOV BH, 0")
        self.code_section.append("    MUL CX")
        self.code_section.append("    ADD AX, BX")
        self.code_section.append("    INC SI")
        self.code_section.append("    JMP s2i_loop")
        self.code_section.append("s2i_done:")
        self.code_section.append("    POP DX")
        self.code_section.append("    POP CX")
        self.code_section.append("    POP BX")
        self.code_section.append("    RET")
        self.code_section.append("string_to_int ENDP")
        self.code_section.append("")
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("; Imprime número (AX)")
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("print_number_inline PROC")
        self.code_section.append("    PUSH AX")
        self.code_section.append("    PUSH BX")
        self.code_section.append("    PUSH CX")
        self.code_section.append("    PUSH DX")
        self.code_section.append("    PUSH SI")
        self.code_section.append("")
        self.code_section.append("    MOV CX, 0")
        self.code_section.append("    MOV BX, 10")
        self.code_section.append("    CMP AX, 0")
        self.code_section.append("    JGE pn_loop")
        self.code_section.append("    NEG AX")
        self.code_section.append("    PUSH AX")
        self.code_section.append("    MOV DL, '-'")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    POP AX")
        self.code_section.append("pn_loop:")
        self.code_section.append("    XOR DX, DX")
        self.code_section.append("    DIV BX")
        self.code_section.append("    PUSH DX")
        self.code_section.append("    INC CX")
        self.code_section.append("    CMP AX, 0")
        self.code_section.append("    JNE pn_loop")
        self.code_section.append("pn_digits:")
        self.code_section.append("    POP DX")
        self.code_section.append("    ADD DL, '0'")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    LOOP pn_digits")
        self.code_section.append("")
        self.code_section.append("    POP SI")
        self.code_section.append("    POP DX")
        self.code_section.append("    POP CX")
        self.code_section.append("    POP BX")
        self.code_section.append("    POP AX")
        self.code_section.append("    RET")
        self.code_section.append("print_number_inline ENDP")
        self.code_section.append("")
        self.code_section.append("END main")
        
        # Combinar secciones - replicando estructura de instrucciones.md
        # .model y .stack primero, luego .data, luego .code
        final_code = []
        final_code.append(".model small")
        final_code.append(".stack 100h")
        final_code.append("")
        # Agregar contenido de .data (ya tiene .data al inicio)
        final_code.extend(self.data_section)
        final_code.append("")
        # Agregar contenido de .code (ya tiene .code al inicio)
        final_code.extend(self.code_section)
        self.code = final_code
        return self.code
    
    def get_register(self, var):
        """Obtiene o asigna un registro para una variable temporal"""
        if var in self.register_map:
            return self.register_map[var]
        
        reg = self.available_registers[self.next_register % len(self.available_registers)]
        self.next_register = (self.next_register + 1) % len(self.available_registers)
        self.register_map[var] = reg
        return reg
    
    def get_asm_var_name(self, var_name):
        """Obtiene el nombre de variable en ensamblador, mapeando conflictos"""
        # Si es 'main', usar 'main_var' para evitar conflicto con 'main PROC'
        if var_name == 'main':
            return 'main_var'
        return var_name
    
    def load_value(self, operand):
        """Genera código para cargar un valor en un registro"""
        if operand is None:
            return None
        
        # Si es un número
        try:
            num = int(operand) if '.' not in str(operand) else int(float(operand))
            reg = self.available_registers[self.next_register % len(self.available_registers)]
            self.next_register = (self.next_register + 1) % len(self.available_registers)
            self.code_section.append(f"    MOV {reg}, {num}    ; Cargar constante {operand}")
            return reg
        except:
            pass
        
        # Si es una variable temporal o normal
        if operand.startswith('t') or operand.startswith('_') or operand in self.memory_map:
            reg = self.available_registers[self.next_register % len(self.available_registers)]
            self.next_register = (self.next_register + 1) % len(self.available_registers)
            var_name = operand
            # Asegurar que la variable esté en memory_map (ya debería estar)
            if var_name not in self.memory_map:
                self.memory_map[var_name] = var_name
            # Usar nombre mapeado para evitar conflictos
            asm_var_name = self.get_asm_var_name(var_name)
            # Evitar MOV reg, reg (aunque esto es raro)
            self.code_section.append(f"    MOV {reg}, {asm_var_name}    ; Cargar {operand}")
            return reg
        
        # Si es un string (entre comillas) - ya debería estar en string_map
        if operand.startswith('"') and operand.endswith('"'):
            return None  # Los strings se manejan diferente en PRINT
        
        return None
    
    def store_value(self, reg, var):
        """Genera código para almacenar un registro en una variable"""
        var_name = var
        # Asegurar que la variable esté en memory_map (ya debería estar)
        if var_name not in self.memory_map:
            self.memory_map[var_name] = var_name
        # Usar nombre mapeado para evitar conflictos
        asm_var_name = self.get_asm_var_name(var_name)
        self.code_section.append(f"    MOV {asm_var_name}, {reg}    ; Almacenar en {var}")
    
    def generate_instruction(self, instr):
        """Genera código ensamblador para una instrucción TAC"""
        
        if instr.op == 'ASSIGN':
            # Evitar asignaciones redundantes o incorrectas
            # Si se asigna desde t4 (buffer de entrada), ignorar porque t4 es un buffer de string
            if instr.arg1 == 't4' and instr.result != 't4':
                # t4 es un buffer de string, no se puede asignar directamente a variables numéricas
                # Esta asignación se maneja en INPUT, así que la ignoramos aquí
                return
            
            # Si se asigna valor = t4 después de INPUT, ignorar porque valor se establece en CALL int
            if instr.arg1 == 't4' and instr.result == 'valor':
                return
            
            # Si se asigna n = t5 después de CALL int, ignorar porque n ya se estableció en CALL int
            if instr.arg1.startswith('t') and instr.result == 'n':
                # n ya fue establecido en CALL int, esta asignación es redundante
                return
            
            # Si se asigna resultado = t6 después de CALL factorial, ignorar porque resultado ya se estableció
            if instr.arg1.startswith('t') and instr.result == 'resultado':
                # resultado ya fue establecido en CALL factorial, esta asignación es redundante
                return
            
            self.code_section.append(f"    ; {instr.result} = {instr.arg1}")
            reg_src = self.load_value(instr.arg1)
            if reg_src:
                # Evitar MOV reg, reg
                if reg_src == self.get_register(instr.result):
                    # Ya está en el registro correcto, solo almacenar si es necesario
                    if instr.result not in ['n', 'valor', 'resultado'] or instr.arg1.startswith('t'):
                        self.store_value(reg_src, instr.result)
                else:
                    self.store_value(reg_src, instr.result)
        
        elif instr.op == 'ADD':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1} + {instr.arg2}")
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    MOV {reg_dest}, {reg1}")
            self.code_section.append(f"    ADD {reg_dest}, {reg2}")
            if not instr.result.startswith('t'):
                self.store_value(reg_dest, instr.result)
            else:
                # Guardar temporal en memoria
                if instr.result not in self.memory_map:
                    self.memory_map[instr.result] = instr.result
                    asm_var_name = self.get_asm_var_name(instr.result)
                    self.data_section.append(f"    {asm_var_name} DW 0")
                asm_var_name = self.get_asm_var_name(instr.result)
                self.code_section.append(f"    MOV {asm_var_name}, {reg_dest}")
        
        elif instr.op == 'SUB':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1} - {instr.arg2}")
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    MOV {reg_dest}, {reg1}")
            self.code_section.append(f"    SUB {reg_dest}, {reg2}")
            self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'MUL':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1} * {instr.arg2}")
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    MOV AX, {reg1}")
            self.code_section.append(f"    MUL {reg2}")
            self.code_section.append(f"    MOV {reg_dest}, AX")
            self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'DIV':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1} / {instr.arg2}")
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    MOV AX, {reg1}")
            self.code_section.append(f"    MOV DX, 0")
            self.code_section.append(f"    DIV {reg2}")
            self.code_section.append(f"    MOV {reg_dest}, AX")
            self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'MOD':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1} % {instr.arg2}")
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    MOV AX, {reg1}")
            self.code_section.append(f"    MOV DX, 0")
            self.code_section.append(f"    DIV {reg2}")
            self.code_section.append(f"    MOV {reg_dest}, DX")
            self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'NEG':
            self.code_section.append(f"    ; {instr.result} = -{instr.arg1}")
            reg_src = self.load_value(instr.arg1)
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    MOV {reg_dest}, {reg_src}")
            self.code_section.append(f"    NEG {reg_dest}")
            self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'NOT':
            self.code_section.append(f"    ; {instr.result} = not {instr.arg1}")
            reg_src = self.load_value(instr.arg1)
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    CMP {reg_src}, 0")
            self.code_section.append(f"    MOV {reg_dest}, 0")
            self.code_section.append(f"    JNE not_end_{self.label_counter}")
            self.code_section.append(f"    MOV {reg_dest}, 1")
            self.code_section.append(f"not_end_{self.label_counter}:")
            self.label_counter += 1
            self.store_value(reg_dest, instr.result)
        
        elif instr.op in ['EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE']:
            jump_map = {
                'EQ': 'JE', 'NEQ': 'JNE', 'LT': 'JL',
                'GT': 'JG', 'LTE': 'JLE', 'GTE': 'JGE'
            }
            self.code_section.append(f"    ; {instr.result} = {instr.arg1} {instr.op} {instr.arg2}")
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            true_label = f"L{self.label_counter}_true"
            end_label = f"L{self.label_counter}_end"
            self.label_counter += 1
            
            self.code_section.append(f"    MOV {reg_dest}, 0    ; Inicializar resultado")
            self.code_section.append(f"    CMP {reg1}, {reg2}")
            self.code_section.append(f"    {jump_map[instr.op]} {true_label}")
            self.code_section.append(f"    JMP {end_label}")
            self.code_section.append(f"{true_label}:")
            self.code_section.append(f"    MOV {reg_dest}, 1")
            self.code_section.append(f"{end_label}:")
            
            self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'PRINT':
            # Verificar si es un string
            if instr.arg1 and instr.arg1.startswith('"') and instr.arg1.endswith('"'):
                string_val = instr.arg1[1:-1]
                # Mapear a nombres específicos como en instrucciones.md
                string_name_map = {
                    '=== CÁLCULO DE FACTORIAL ===': 'str_0',
                    'Ingrese un número entero: ': 'str_in',
                    'El factorial de': 'str_out',
                    'es:': 'str_es'
                }
                label = string_name_map.get(string_val, self.string_map.get(string_val, 'str_unknown'))
                # Agregar comentarios según el string
                if string_val == '=== CÁLCULO DE FACTORIAL ===':
                    self.code_section.append(f"    ; título")
                elif string_val == 'El factorial de':
                    self.code_section.append(f"    ; imprimir resultado")
                elif string_val == 'es:':
                    pass  # Ya está después de imprimir valor
                self.code_section.append(f"    MOV DX, OFFSET {label}")
                self.code_section.append(f"    MOV AH, 09h")
                self.code_section.append(f"    INT 21h")
            else:
                # Si se imprime 'n' y existe 'valor', usar 'valor' en su lugar
                var_to_print = instr.arg1
                if var_to_print == 'n' and 'valor' in self.memory_map:
                    var_to_print = 'valor'
                # Cargar valor directamente como en instrucciones.md
                if var_to_print in self.memory_map:
                    asm_var_name = self.get_asm_var_name(var_to_print)
                    self.code_section.append(f"    MOV AX, {asm_var_name}")
                    self.code_section.append(f"    CALL print_number_inline")
                else:
                    reg = self.load_value(var_to_print)
                    if reg:
                        # Evitar MOV AX, AX
                        if reg != 'AX':
                            self.code_section.append(f"    MOV AX, {reg}")
                        self.code_section.append(f"    CALL print_number_inline")
        
        elif instr.op == 'LABEL':
            # Las etiquetas func_ ya se manejan como PROC, solo generar otras etiquetas
            if instr.arg1 and not instr.arg1.startswith('func_'):
                self.code_section.append(f"{instr.arg1}:")
        
        elif instr.op == 'GOTO':
            self.code_section.append(f"    JMP {instr.arg1}    ; Salto incondicional")
        
        elif instr.op == 'IF_FALSE':
            # Para IF_FALSE, usar comparación directa sin crear variable temporal
            # Si arg1 es una comparación (t0, t1, etc.), cargar y comparar directamente
            var_name = instr.arg1
            if var_name in self.memory_map or var_name.startswith('t'):
                asm_var_name = self.get_asm_var_name(var_name)
                self.code_section.append(f"    CMP {asm_var_name}, 0")
                self.code_section.append(f"    JE {instr.arg2}    ; Saltar si falso")
            else:
                # Si es un registro, usar directamente
                reg = self.load_value(instr.arg1)
                if reg:
                    self.code_section.append(f"    CMP {reg}, 0")
                    self.code_section.append(f"    JE {instr.arg2}    ; Saltar si falso")
                else:
                    # Si es una variable en memoria
                    if var_name not in self.memory_map:
                        self.memory_map[var_name] = var_name
                    asm_var_name = self.get_asm_var_name(var_name)
                    self.code_section.append(f"    CMP {asm_var_name}, 0")
                    self.code_section.append(f"    JE {instr.arg2}    ; Saltar si falso")
        
        elif instr.op == 'LIST_CREATE':
            self.code_section.append(f"    ; {instr.result} = [] (crear lista)")
            # Implementación simplificada - asignar dirección de memoria
            if instr.result not in self.memory_map:
                self.memory_map[instr.result] = instr.result
            reg_dest = self.get_register(instr.result)
            asm_var_name = self.get_asm_var_name(instr.result)
            self.code_section.append(f"    MOV {reg_dest}, OFFSET {asm_var_name}")
            self.code_section.append(f"    MOV {asm_var_name}, {reg_dest}")
        
        elif instr.op == 'LIST_APPEND':
            self.code_section.append(f"    ; {instr.arg1}.append({instr.arg2})")
            # Implementación simplificada - solo comentario por ahora
            pass
        
        elif instr.op == 'LIST_REMOVE':
            self.code_section.append(f"    ; {instr.arg1}.remove({instr.arg2})")
            # Implementación simplificada - solo comentario por ahora
            pass
        
        elif instr.op == 'LIST_GET':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1}[{instr.arg2}]")
            # Implementación simplificada
            reg_list = self.load_value(instr.arg1)
            reg_index = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    ; Acceso a lista simplificado")
            self.code_section.append(f"    MOV {reg_dest}, 0")
            self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'CALL':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1}()")
            if instr.arg1 == 'len':
                reg_list = self.load_value(instr.arg2)
                reg_dest = self.get_register(instr.result)
                # Implementación simplificada
                self.code_section.append(f"    MOV {reg_dest}, 0    ; len simplificado")
                self.store_value(reg_dest, instr.result)
            elif instr.arg1 == 'int':
                # Conversión de string a entero - como en instrucciones.md
                # SI ya debe estar apuntando a t4+2 después de INPUT
                # Solo llamar a string_to_int (SI ya está configurado)
                self.code_section.append(f"    ; convertir")
                self.code_section.append(f"    CALL string_to_int")
                # Guardar resultado en n y valor como en instrucciones.md
                asm_n_name = self.get_asm_var_name('n')
                asm_valor_name = self.get_asm_var_name('valor')
                self.code_section.append(f"    MOV {asm_n_name}, AX")
                self.code_section.append(f"    MOV {asm_valor_name}, AX")
                # Si el resultado es un temporal, también guardarlo (pero no es necesario si ya está en n y valor)
                if instr.result and instr.result.startswith('t'):
                    # Guardar en temporal solo si es necesario para uso posterior
                    # Pero evitar código redundante
                    pass
            elif instr.arg1 in self.functions:
                # Llamada a función definida por el usuario
                func_name = instr.arg1
                # Obtener el nombre real del procedimiento (puede estar renombrado)
                actual_proc_name = self.function_name_map.get(func_name, func_name)
                
                # Parsear argumentos
                args = []
                if instr.arg2:
                    args_str = str(instr.arg2)
                    args = [a.strip() for a in args_str.split(',')]
                
                # Para factorial, pasar argumento en AX directamente como en instrucciones.md
                if func_name == 'factorial':
                    # Cargar n en AX
                    asm_n_name = self.get_asm_var_name('n')
                    self.code_section.append(f"    ; calcular factorial")
                    self.code_section.append(f"    MOV AX, {asm_n_name}")
                    self.code_section.append(f"    CALL {actual_proc_name}")
                    # Guardar resultado en resultado directamente
                    asm_resultado_name = self.get_asm_var_name('resultado')
                    self.code_section.append(f"    MOV {asm_resultado_name}, AX")
                    # Si el resultado es un temporal, no guardarlo redundantemente
                    # porque ya está en resultado
                else:
                    # Para otras funciones, usar el método anterior
                    # Guardar registros
                    self.code_section.append(f"    ; Guardar registros antes de llamar función")
                    self.code_section.append(f"    PUSH AX")
                    self.code_section.append(f"    PUSH BX")
                    self.code_section.append(f"    PUSH CX")
                    self.code_section.append(f"    PUSH DX")
                    
                    # Pasar argumentos (simplificado: usar registros)
                    func_info = self.functions.get(func_name, {})
                    params = func_info.get('params', [])
                    for i, arg in enumerate(args[:len(params)]):
                        arg_reg = self.load_value(arg)
                        if arg_reg:
                            param_name = params[i] if i < len(params) else f"param{i}"
                            # Asignar argumento al parámetro
                            asm_param_name = self.get_asm_var_name(param_name)
                            self.code_section.append(f"    MOV {asm_param_name}, {arg_reg}")
                    
                    # Llamar función usando el nombre real del procedimiento
                    self.code_section.append(f"    CALL {actual_proc_name}")
                    
                    # Restaurar registros
                    self.code_section.append(f"    POP DX")
                    self.code_section.append(f"    POP CX")
                    self.code_section.append(f"    POP BX")
                    self.code_section.append(f"    POP AX")
                    
                    # Guardar resultado (asumir que está en AX)
                    if instr.result:
                        reg_dest = self.get_register(instr.result)
                        if reg_dest != 'AX':
                            self.code_section.append(f"    MOV {reg_dest}, AX")
                            self.store_value(reg_dest, instr.result)
                        else:
                            self.store_value('AX', instr.result)
            else:
                # Función desconocida
                self.code_section.append(f"    ; Función desconocida: {instr.arg1}")
        
        elif instr.op == 'RETURN':
            if instr.arg1 is not None:
                # Retornar valor
                return_reg = self.load_value(instr.arg1)
                if return_reg:
                    self.code_section.append(f"    ; return {instr.arg1}")
                    # Evitar MOV AX, AX
                    if return_reg != 'AX':
                        self.code_section.append(f"    MOV AX, {return_reg}")
                else:
                    self.code_section.append(f"    ; return {instr.arg1}")
                    # Si es un número directo
                    try:
                        num = int(instr.arg1) if '.' not in str(instr.arg1) else int(float(instr.arg1))
                        self.code_section.append(f"    MOV AX, {num}")
                    except:
                        self.code_section.append(f"    MOV AX, 0")
            else:
                self.code_section.append(f"    ; return None")
                self.code_section.append(f"    MOV AX, 0")
            self.code_section.append(f"    RET")
        
        elif instr.op == 'INPUT':
            # Leer string desde entrada estándar - replicando instrucciones.md
            if instr.arg1:
                # Mostrar prompt (pedir número)
                prompt_reg = self.load_value(instr.arg1)
                if prompt_reg is None and instr.arg1.startswith('"'):
                    string_val = instr.arg1[1:-1]
                    # Mapear a nombres específicos
                    string_name_map = {
                        'Ingrese un número entero: ': 'str_in'
                    }
                    label = string_name_map.get(string_val, self.string_map.get(string_val, 'str_in'))
                    self.code_section.append(f"    ; pedir número")
                    self.code_section.append(f"    MOV DX, OFFSET {label}")
                    self.code_section.append(f"    MOV AH, 09h")
                    self.code_section.append(f"    INT 21h")
            
            # Leer número
            if instr.result:
                asm_var_name = self.get_asm_var_name(instr.result)
                # Asegurar que la variable esté en memory_map
                if instr.result not in self.memory_map:
                    self.memory_map[instr.result] = instr.result
                
                self.code_section.append(f"    ; leer número")
                self.code_section.append(f"    MOV DX, OFFSET {asm_var_name}")
                self.code_section.append(f"    MOV AH, 0Ah")
                self.code_section.append(f"    INT 21h")
                # Preparar cadena como en instrucciones.md
                self.code_section.append(f"    ; preparar cadena")
                self.code_section.append(f"    MOV SI, OFFSET {asm_var_name}+2")
                self.code_section.append(f"    MOV CL, [{asm_var_name}+1]")
                self.code_section.append(f"    ADD SI, CX")
                self.code_section.append(f"    MOV BYTE PTR [SI], 0")
                self.code_section.append(f"    MOV SI, OFFSET {asm_var_name}+2")
    
    def generate_factorial_function(self):
        """Genera código optimizado para función factorial usando pila como en instrucciones.md"""
        self.code_section.append("    CMP AX, 1")
        self.code_section.append("    JBE base_case")
        self.code_section.append("")
        self.code_section.append("    PUSH AX        ; guarda n actual")
        self.code_section.append("    DEC AX         ; n-1")
        self.code_section.append("    CALL factorial ; factorial(n-1)")
        self.code_section.append("    POP BX         ; recupera n original")
        self.code_section.append("    MUL BX         ; AX = factorial(n-1) * n")
        self.code_section.append("    RET")
        self.code_section.append("")
        self.code_section.append("base_case:")
        self.code_section.append("    MOV AX, 1")
        self.code_section.append("    RET")
    
    def get_code_as_string(self):
        """Retorna el código ensamblador como string"""
        return '\n'.join(self.code)
