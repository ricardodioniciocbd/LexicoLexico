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
        for instr in tac_instructions:
            # Recopilar variables de resultados
            if instr.result:
                if not self.is_number(instr.result) and not instr.result.startswith('L'):
                    if instr.result not in self.memory_map:
                        self.memory_map[instr.result] = instr.result
            
            # Recopilar variables de argumentos
            if instr.arg1:
                if not instr.arg1.startswith('"') and not instr.arg1.startswith('L'):
                    if not self.is_number(instr.arg1):
                        if instr.arg1 not in self.memory_map:
                            self.memory_map[instr.arg1] = instr.arg1
            
            if instr.arg2:
                if not instr.arg2.startswith('"') and not instr.arg2.startswith('L'):
                    if not self.is_number(instr.arg2):
                        if instr.arg2 not in self.memory_map:
                            self.memory_map[instr.arg2] = instr.arg2
            
            # Recopilar strings
            if instr.op == 'PRINT' and instr.arg1:
                if instr.arg1.startswith('"') and instr.arg1.endswith('"'):
                    string_val = instr.arg1[1:-1]
                    if string_val not in self.string_map:
                        label = f"str_{self.string_counter}"
                        self.string_counter += 1
                        self.string_map[string_val] = label
    
    def generate(self, tac_instructions):
        """Genera código máquina desde TAC"""
        self.code = []
        self.data_section = []
        self.code_section = []
        self.memory_map = {}
        self.register_map = {}
        self.next_register = 0
        self.string_counter = 0
        self.string_map = {}
        
        # Primera pasada: recopilar todas las variables y strings
        self.collect_variables_and_strings(tac_instructions)
        
        # Encabezado del programa
        self.code_section.append("; Código Ensamblador Generado")
        self.code_section.append("; Arquitectura: x86 de 16 bits (emu8086)")
        self.code_section.append("")
        self.code_section.append(".model small")
        self.code_section.append(".stack 100h")
        self.code_section.append("")
        
        # Sección de datos
        self.data_section.append(".data")
        self.data_section.append("    ; Variables del programa")
        
        # Declarar todas las variables recopiladas
        for var_name in sorted(self.memory_map.keys()):
            # Solo declarar variables que no sean etiquetas
            if not var_name.startswith('L'):
                self.data_section.append(f"    {var_name} DW 0")
        
        # Declarar strings
        if self.string_map:
            self.data_section.append("")
            self.data_section.append("    ; Strings del programa")
            for string_val, label in sorted(self.string_map.items()):
                # Escapar comillas simples en el string
                escaped_string = string_val.replace("'", "''")
                self.data_section.append(f"    {label} DB '{escaped_string}', 0Dh, 0Ah, '$'")
        
        self.data_section.append("")
        self.data_section.append("    ; Buffer para conversión de números")
        self.data_section.append("    num_buffer DB 10 DUP(0)")
        self.data_section.append("    newline DB 0Dh, 0Ah, '$'")
        self.data_section.append("")
        
        # Sección de código
        self.code_section.append(".code")
        self.code_section.append("")
        self.code_section.append("main PROC")
        self.code_section.append("    MOV AX, @data")
        self.code_section.append("    MOV DS, AX")
        self.code_section.append("")
        
        # Generar código para cada instrucción TAC
        for instr in tac_instructions:
            self.generate_instruction(instr)
        
        # Epílogo
        self.code_section.append("")
        self.code_section.append("    ; Finalización del programa")
        self.code_section.append("    MOV AH, 4Ch")
        self.code_section.append("    MOV AL, 0")
        self.code_section.append("    INT 21h")
        self.code_section.append("")
        self.code_section.append("main ENDP")
        self.code_section.append("")
        
        # Funciones auxiliares
        self.code_section.append("; Función para imprimir número")
        self.code_section.append("print_number PROC")
        self.code_section.append("    ; AX contiene el número a imprimir")
        self.code_section.append("    PUSH AX")
        self.code_section.append("    PUSH BX")
        self.code_section.append("    PUSH CX")
        self.code_section.append("    PUSH DX")
        self.code_section.append("    PUSH SI")
        self.code_section.append("")
        self.code_section.append("    MOV CX, 0")
        self.code_section.append("    MOV BX, 10")
        self.code_section.append("    CMP AX, 0")
        self.code_section.append("    JGE print_loop")
        self.code_section.append("    NEG AX")
        self.code_section.append("    PUSH AX")
        self.code_section.append("    MOV DL, '-'")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    POP AX")
        self.code_section.append("")
        self.code_section.append("print_loop:")
        self.code_section.append("    MOV DX, 0")
        self.code_section.append("    DIV BX")
        self.code_section.append("    PUSH DX")
        self.code_section.append("    INC CX")
        self.code_section.append("    CMP AX, 0")
        self.code_section.append("    JNE print_loop")
        self.code_section.append("")
        self.code_section.append("print_digits:")
        self.code_section.append("    POP DX")
        self.code_section.append("    ADD DL, '0'")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    LOOP print_digits")
        self.code_section.append("")
        self.code_section.append("    ; Imprimir nueva línea")
        self.code_section.append("    MOV DX, OFFSET newline")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("")
        self.code_section.append("    POP SI")
        self.code_section.append("    POP DX")
        self.code_section.append("    POP CX")
        self.code_section.append("    POP BX")
        self.code_section.append("    POP AX")
        self.code_section.append("    RET")
        self.code_section.append("print_number ENDP")
        self.code_section.append("")
        self.code_section.append("END main")
        
        # Combinar secciones
        self.code = self.data_section + [""] + self.code_section
        return self.code
    
    def get_register(self, var):
        """Obtiene o asigna un registro para una variable temporal"""
        if var in self.register_map:
            return self.register_map[var]
        
        reg = self.available_registers[self.next_register % len(self.available_registers)]
        self.next_register = (self.next_register + 1) % len(self.available_registers)
        self.register_map[var] = reg
        return reg
    
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
            self.code_section.append(f"    MOV {reg}, {var_name}    ; Cargar {operand}")
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
        self.code_section.append(f"    MOV {var_name}, {reg}    ; Almacenar en {var}")
    
    def generate_instruction(self, instr):
        """Genera código ensamblador para una instrucción TAC"""
        
        if instr.op == 'ASSIGN':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1}")
            reg_src = self.load_value(instr.arg1)
            if reg_src:
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
                    self.data_section.append(f"    {instr.result} DW 0")
                self.code_section.append(f"    MOV {instr.result}, {reg_dest}")
        
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
            self.code_section.append(f"    ; print({instr.arg1})")
            # Verificar si es un string
            if instr.arg1 and instr.arg1.startswith('"') and instr.arg1.endswith('"'):
                string_val = instr.arg1[1:-1]
                # El string ya debería estar en string_map de la primera pasada
                if string_val in self.string_map:
                    label = self.string_map[string_val]
                    self.code_section.append(f"    MOV DX, OFFSET {label}")
                    self.code_section.append(f"    MOV AH, 09h")
                    self.code_section.append(f"    INT 21h")
            else:
                reg = self.load_value(instr.arg1)
                if reg:
                    self.code_section.append(f"    MOV AX, {reg}")
                    self.code_section.append(f"    CALL print_number")
        
        elif instr.op == 'LABEL':
            self.code_section.append(f"{instr.arg1}:")
        
        elif instr.op == 'GOTO':
            self.code_section.append(f"    JMP {instr.arg1}    ; Salto incondicional")
        
        elif instr.op == 'IF_FALSE':
            reg = self.load_value(instr.arg1)
            if reg:
                self.code_section.append(f"    CMP {reg}, 0")
                self.code_section.append(f"    JE {instr.arg2}    ; Saltar si falso")
            else:
                # Si es una variable en memoria
                var_name = instr.arg1
                if var_name not in self.memory_map:
                    self.memory_map[var_name] = var_name
                self.code_section.append(f"    CMP {var_name}, 0")
                self.code_section.append(f"    JE {instr.arg2}    ; Saltar si falso")
        
        elif instr.op == 'LIST_CREATE':
            self.code_section.append(f"    ; {instr.result} = [] (crear lista)")
            # Implementación simplificada - asignar dirección de memoria
            if instr.result not in self.memory_map:
                self.memory_map[instr.result] = instr.result
            reg_dest = self.get_register(instr.result)
            self.code_section.append(f"    MOV {reg_dest}, OFFSET {instr.result}")
            self.code_section.append(f"    MOV {instr.result}, {reg_dest}")
        
        elif instr.op == 'LIST_APPEND':
            self.code_section.append(f"    ; {instr.arg1}.append({instr.arg2})")
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
    
    def get_code_as_string(self):
        """Retorna el código ensamblador como string"""
        return '\n'.join(self.code)
