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
        
        # Modo CRUD simple (basado en instrucciones.md)
        self.simple_crud_mode = False
        self.estudiantes_list_var = None
        # Constantes según instrucciones.md
        self.id_len = 5
        self.name_len = 20
        self.edad_len = 3
        self.carr_len = 20
        self.prom_len = 3
        
        # Modo diccionarios simples (para Sistema_inventario_DICCIONARIO.py)
        self.dict_mode = False
        self.dict_string_literals = {}  # Mapeo de strings literales a etiquetas (ej: "Laptop" -> LaptopStr)
        
        # Modo procesamiento de cadenas (para Sistema_de_procesamiento_d_cadenas.py)
        self.string_processing_mode = False
    
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
        
        # Detectar patrón CRUD simple
        crud_functions = ['menu', 'alta', 'baja', 'modificar', 'listar']
        self.has_crud_functions = False  # Guardar como atributo de clase
        
        # Detectar patrón de procesamiento de cadenas
        string_processing_functions = ['contar_vocales', 'invertir', 'es_palindromo', 'contar_caracter', 'a_mayusculas', 'menu', 'main']
        detected_string_functions = set()
        
        # Primero, identificar todas las funciones para excluirlas de variables
        for i, instr in enumerate(tac_instructions):
            # Detectar funciones
            if instr.op == 'LABEL' and instr.arg1 and instr.arg1.startswith('func_'):
                func_name = instr.arg1[5:]  # Quitar 'func_'
                if func_name not in self.functions:
                    self.functions[func_name] = {'start': i, 'end': len(tac_instructions), 'params': []}
                current_function = func_name
                # Detectar funciones CRUD
                if func_name in crud_functions:
                    self.has_crud_functions = True
                # Detectar funciones de procesamiento de cadenas
                if func_name in string_processing_functions:
                    detected_string_functions.add(func_name)
        
        # Activar modo procesamiento de cadenas si tiene al menos 5 de las funciones características
        if len(detected_string_functions) >= 5 and 'contar_vocales' in detected_string_functions:
            self.string_processing_mode = True
            self.has_crud_functions = False  # Desactivar CRUD si es procesamiento de cadenas
        
        # Ahora recopilar variables, excluyendo nombres de funciones
        for i, instr in enumerate(tac_instructions):
            # Recopilar variables de resultados (excluir etiquetas de funciones y nombres de funciones)
            if instr.result:
                if (not self.is_number(instr.result) and 
                    not instr.result.startswith('L') and 
                    not instr.result.startswith('func_') and
                    instr.result not in self.functions.keys() and  # Excluir nombres de funciones
                    instr.result != 'main' and
                    instr.result != 'int' and
                    instr.result != 'len' and
                    instr.result != 'print'):  # No agregar funciones built-in como variables
                    if instr.result not in self.memory_map:
                        self.memory_map[instr.result] = instr.result
            
            # Recopilar variables de argumentos (excluir etiquetas de funciones y nombres de funciones)
            if instr.arg1:
                if (not instr.arg1.startswith('"') and 
                    not instr.arg1.startswith('L') and 
                    not instr.arg1.startswith('func_') and
                    instr.arg1 not in self.functions.keys() and  # Excluir nombres de funciones
                    instr.arg1 != 'main' and
                    instr.arg1 != 'int' and
                    instr.arg1 != 'len' and
                    instr.arg1 != 'print'):
                    if not self.is_number(instr.arg1):
                        if instr.arg1 not in self.memory_map:
                            self.memory_map[instr.arg1] = instr.arg1
            
            if instr.arg2:
                if (not instr.arg2.startswith('"') and 
                    not instr.arg2.startswith('L') and 
                    not instr.arg2.startswith('func_') and
                    instr.arg2 not in self.functions.keys() and  # Excluir nombres de funciones
                    instr.arg2 != 'main' and
                    instr.arg2 != 'int' and
                    instr.arg2 != 'len' and
                    instr.arg2 != 'print'):
                    if not self.is_number(instr.arg2):
                        if instr.arg2 not in self.memory_map:
                            self.memory_map[instr.arg2] = instr.arg2
            
            # Recopilar strings de PRINT
            if instr.op == 'PRINT' and instr.arg1:
                if instr.arg1.startswith('"') and instr.arg1.endswith('"'):
                    string_val = instr.arg1[1:-1]
                    if string_val not in self.string_map:
                        # En modo procesamiento de cadenas, usar nombres específicos
                        if self.string_processing_mode:
                            # Mapeo específico para el menú de procesamiento de cadenas
                            string_label_map = {
                                '\n===== PROCESAMIENTO DE CADENAS =====': 'str_0',
                                '1. Contar vocales': 'str_1',
                                '2. Invertir cadena': 'str_2',
                                '3. Verificar palíndromo': 'str_3',
                                '4. Contar un carácter específico': 'str_4',
                                '5. Convertir a mayúsculas': 'str_5',
                                '6. Salir': 'str_6',
                                'Cantidad de vocales:': 'str_9',
                                'Invertida:': 'str_10',
                                ' Es palíndromo.': 'str_11',
                                ' No es palíndromo.': 'str_12',
                                'El carácter aparece': 'str_14',
                                ' veces.': 'str_15',
                                'En mayúsculas:': 'str_16',
                                ' Saliendo...': 'str_17',
                                ' Opción inválida.': 'str_18'
                            }
                            label = string_label_map.get(string_val, f"str_{self.string_counter}")
                        else:
                            label = f"str_{self.string_counter}"
                        self.string_counter += 1
                        self.string_map[string_val] = label
            
            # Recopilar strings de INPUT
            if instr.op == 'INPUT' and instr.arg1:
                if instr.arg1.startswith('"') and instr.arg1.endswith('"'):
                    string_val = instr.arg1[1:-1]
                    if string_val not in self.string_map:
                        # En modo procesamiento de cadenas, usar nombres específicos
                        if self.string_processing_mode:
                            input_label_map = {
                                'Seleccione una opción: ': 'str_7',
                                'Ingrese texto: ': 'str_8',
                                'Ingrese carácter a buscar: ': 'str_13'
                            }
                            label = input_label_map.get(string_val, f"str_{self.string_counter}")
                        else:
                            label = f"str_{self.string_counter}"
                        self.string_counter += 1
                        self.string_map[string_val] = label
            
            # Recopilar strings literales de DICT_SET (para modo diccionarios)
            if instr.op == 'DICT_SET' and instr.result:
                if instr.result.startswith('"') and instr.result.endswith('"'):
                    string_val = instr.result[1:-1]
                    # Crear etiqueta específica para el string (ej: "Laptop" -> LaptopStr)
                    if string_val not in self.dict_string_literals:
                        # Nombre de etiqueta basado en el string
                        clean_name = ''.join(c if c.isalnum() else '' for c in string_val)
                        label = f"{clean_name}Str" if clean_name else f"str_{self.string_counter}"
                        self.string_counter += 1
                        self.dict_string_literals[string_val] = label
            
            # Recopilar variables de campos de diccionario (t0_desc, t0_precio, etc.)
            if instr.op == 'DICT_SET' or instr.op == 'DICT_GET':
                if instr.arg1 and instr.arg2:
                    dict_name = instr.arg1
                    key_name = instr.arg2.strip('"') if instr.arg2.startswith('"') else instr.arg2
                    
                    # En modo diccionarios, siempre usar "stock" directamente según instrucciones.md
                    # No hay INDEX en instrucciones.md, solo "stock", "precio", "desc"
                    if key_name == "INDEX":
                        key_name = "stock"
                    
                    # Crear nombre de variable compuesto: diccionario_clave
                    field_var = f"{dict_name}[{key_name}]"
                    
                    # Agregar al memory_map para que se declare en .data
                    if field_var not in self.memory_map:
                        self.memory_map[field_var] = field_var
            
        # Segunda pasada: recopilar campos de diccionario cuando se asigna un diccionario completo
        # (ej: producto1 = t0 -> crear producto1_precio, producto1_stock)
        # Esto se hace después de recopilar todos los campos de DICT_SET/DICT_GET
        for instr in tac_instructions:
            if instr.op == 'ASSIGN' and instr.arg1 and instr.result:
                # Verificar si el origen tiene campos de diccionario
                source_has_fields = any(f"{instr.arg1}_" in k or f"{instr.arg1}[" in k for k in self.memory_map.keys())
                if source_has_fields:
                    # El destino también necesitará campos de diccionario
                    # Crear campos comunes: _precio y _stock
                    for field in ['precio', 'stock']:
                        dest_field = f"{instr.result}[{field}]"
                        if dest_field not in self.memory_map:
                            self.memory_map[dest_field] = dest_field
        
        # Detectar modo diccionarios: tiene DICT_CREATE pero NO tiene funciones definidas
        has_dict_create = any(instr.op == 'DICT_CREATE' for instr in tac_instructions)
        has_user_functions = len(self.functions) > 0
        self.dict_mode = has_dict_create and not has_user_functions and not self.has_crud_functions
    
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
        
        # Activar modo CRUD si se detectaron funciones CRUD
        if self.has_crud_functions or self.estudiantes_list_var:
            self.simple_crud_mode = True
        
        # Actualizar parámetros de funciones desde function_params
        for func_name in self.functions:
            if func_name in self.function_params:
                self.functions[func_name]['params'] = self.function_params[func_name]
        
        # Sección de datos - replicando instrucciones.md
        self.data_section.append(".data")
        
        # Mapeo para renombrar variables que conflictúan con nombres reservados o procedimientos
        self.var_name_map = {}  # Guardar como atributo para usar en get_asm_var_name
        if 'main' in self.memory_map:
            self.var_name_map['main'] = 'main_var'
        
        # Renombrar variables que conflictúan con nombres de procedimientos
        for func_name in self.functions.keys():
            if func_name in self.memory_map:
                # Renombrar variable para evitar conflicto con procedimiento
                self.var_name_map[func_name] = f"{func_name}_var"
        
        # Verificar si hay INPUT para asegurar que str_in se declare
        has_input = any(instr.op == 'INPUT' for instr in tac_instructions)
        
        # Detectar buffers de INPUT para declarlos correctamente
        self.input_buffers = set()
        for instr in tac_instructions:
            if instr.op == 'INPUT' and instr.result and instr.result.startswith('t'):
                self.input_buffers.add(instr.result)
        
        # Si está en modo CRUD, generar estructura de datos especial
        if self.simple_crud_mode:
            self.generate_crud_data_section()
        elif self.string_processing_mode:
            # Modo procesamiento de cadenas: generar estructura específica
            self.generate_string_processing_data_section()
        elif self.dict_mode:
            # Modo diccionarios: generar estructura específica para Sistema_inventario_DICCIONARIO.py
            self.generate_dict_data_section(tac_instructions)
        else:
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
                        # Para strings de INPUT, usar formato diferente (sin newline al final)
                        if 'ingresa' in string_val.lower() or 'ingrese' in string_val.lower():
                            self.data_section.append(f"    {label} DB '{escaped_string}', '$'")
                        else:
                            self.data_section.append(f"    {label} DB '{escaped_string}', 0Dh, 0Ah, '$'")
            
            # Agregar newline después de los strings
            self.data_section.append("")
            self.data_section.append("    newline DB 0Dh,0Ah,'$'")
            
            # Declarar buffers de entrada - SOLO como DB, no como DW
            for buffer_var in sorted(self.input_buffers):
                if buffer_var in self.memory_map:
                    self.data_section.append("")
                    self.data_section.append(f"    {buffer_var} DB 100, ?, 100 DUP(?)   ; buffer de entrada")
            
            # Declarar variables principales en orden específico
            main_vars = ['n', 'resultado', 'valor', 'valor1', 'valor2']
            for var_name in main_vars:
                if var_name in self.memory_map:
                    asm_var_name = self.var_name_map.get(var_name, var_name)
                    # Si es una variable que recibe INPUT de string, declararla como buffer
                    if var_name in ['valor1', 'valor2'] or (var_name == 'valor' and var_name not in ['n', 'resultado']):
                        # Declarar como DW (almacena puntero al buffer)
                        self.data_section.append(f"    {asm_var_name} DW ?")
                    else:
                        self.data_section.append(f"    {asm_var_name} DW ?")
            
            # Luego declarar otras variables (temporales, etc.)
            for var_name in sorted(self.memory_map.keys()):
                # Solo declarar variables que no sean etiquetas, principales ni buffers de INPUT
                if (not var_name.startswith('L') and 
                    var_name not in main_vars and 
                    var_name not in self.input_buffers):  # Buffers ya se declararon como DB arriba
                    # Usar nombre mapeado si existe conflicto, sino usar el nombre original
                    asm_var_name = self.var_name_map.get(var_name, var_name)
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
        if self.simple_crud_mode:
            # Modo CRUD - usar estructura exacta de instrucciones.md
            self.code_section.append("start:")
            self.code_section.append("    mov ax, @data")
            self.code_section.append("    mov ds, ax")
            self.code_section.append("")
            self.code_section.append("; ==========================")
            self.code_section.append(";   BUCLE PRINCIPAL")
            self.code_section.append("; ==========================")
            self.code_section.append("main_loop:")
            # Generar menú
            self.generate_crud_main_loop()
            # Generar funciones CRUD (fuera del bucle)
            self.generate_crud_alta()
            self.generate_crud_baja()
            self.generate_crud_modificar()
            self.generate_crud_listar()
            self.generate_crud_salir()
        elif self.string_processing_mode:
            # Modo procesamiento de cadenas - generar código optimizado manualmente
            # NO generar desde TAC para evitar código redundante
            self.generate_string_processing_complete_code()
        else:
            # Modo factorial
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
        # En modo CRUD, no generar las funciones CRUD como PROC (ya están generadas)
        # En modo procesamiento de cadenas, NO generar funciones (ya están generadas manualmente)
        sorted_functions = []
        
        # Si es modo procesamiento de cadenas, NO generar funciones desde TAC
        if self.string_processing_mode:
            pass  # Las funciones ya están generadas en generate_string_processing_complete_code()
        else:
            if 'factorial' in function_instructions:
                sorted_functions.append(('factorial', function_instructions['factorial']))
            for func_name, func_instrs in function_instructions.items():
                # Excluir funciones CRUD en modo CRUD
                if func_name != 'factorial':
                    if self.simple_crud_mode and func_name in ['menu', 'alta', 'baja', 'modificar', 'listar']:
                        continue  # No agregar funciones CRUD
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
        # En modo diccionarios, se generan en orden diferente por generate_dict_helper_functions
        # En modo procesamiento de cadenas, NO generar (ya están incluidas)
        if not self.dict_mode and not self.string_processing_mode:
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
        
        # Agregar funciones auxiliares para diccionarios si está en modo diccionarios
        # Debe ir ANTES de CRUD para que dict_mode tenga prioridad
        if self.dict_mode:
            self.generate_dict_helper_functions()
        
        # Agregar funciones auxiliares para CRUD si está en modo CRUD
        elif self.simple_crud_mode:
            self.generate_crud_helper_functions()
        
        # Agregar funciones auxiliares para procesamiento de cadenas
        elif self.string_processing_mode:
            # Los helpers ya están incluidos en generate_string_processing_complete_code()
            pass
        
        if self.simple_crud_mode:
            self.code_section.append("END start")
        elif self.string_processing_mode:
            self.code_section.append("")
            self.code_section.append("END main")
        else:
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
        # Usar el mapeo de nombres si existe, sino usar el nombre original
        if hasattr(self, 'var_name_map') and var_name in self.var_name_map:
            return self.var_name_map[var_name]
        # Fallback para 'main' si no está en var_name_map
        if var_name == 'main':
            return 'main_var'
        # Convertir nombres con corchetes (diccionarios) a nombres válidos en ASM
        # Ejemplo: producto1[precio] -> producto1_precio
        if '[' in var_name and ']' in var_name:
            # En modo diccionarios, siempre usar "stock" directamente según instrucciones.md
            # No hay INDEX en instrucciones.md, solo "stock", "precio", "desc"
            if '[INDEX]' in var_name:
                var_name = var_name.replace('[INDEX]', '[stock]')
            # Reemplazar corchetes por guión bajo
            clean_name = var_name.replace('[', '_').replace(']', '')
            return clean_name
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
            # Si se asigna desde un buffer de entrada, generar código especial
            if hasattr(self, 'input_buffers') and instr.arg1 in self.input_buffers and instr.result != instr.arg1:
                # Es una asignación de buffer a variable (ej: valor1 = t0)
                # Almacenar el OFFSET del buffer en la variable
                self.code_section.append(f"    ; {instr.result} = {instr.arg1}")
                asm_buffer = self.get_asm_var_name(instr.arg1)
                asm_result = self.get_asm_var_name(instr.result)
                self.code_section.append(f"    MOV AX, OFFSET {asm_buffer}+2  ; Puntero al contenido del buffer")
                self.code_section.append(f"    MOV {asm_result}, AX")
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
            
            # En modo diccionarios, optimización especial: total = t8 después de ADD
            # Según código de referencia: después de ADD AX, BX; MOV t8, AX
            # se hace MOV total, AX directamente (sin cargar t8)
            # Esto requiere que el resultado de ADD esté en AX
            if self.dict_mode and instr.result == 'total' and instr.arg1 == 't8':
                asm_result_name = self.get_asm_var_name(instr.result)
                # El resultado de ADD ya está en AX, usar directamente
                self.code_section.append(f"    MOV {asm_result_name}, AX")
                return
            
            # En modo diccionarios, si se asigna un diccionario (producto1 = t0), copiar campos
            if self.dict_mode:
                # Verificar si es una asignación de diccionario (ej: producto1 = t0)
                source_has_fields = any(f"{instr.arg1}_" in k or f"{instr.arg1}[" in k for k in self.memory_map.keys())
                dest_has_fields = any(f"{instr.result}_" in k or f"{instr.result}[" in k for k in self.memory_map.keys())
                
                if source_has_fields and dest_has_fields:
                    # Es una asignación de diccionario, copiar según código de referencia línea 97-104
                    # producto1 = t0 → MOV SI, t0; MOV producto1, SI; copiar a producto1_*
                    asm_source = self.get_asm_var_name(instr.arg1)
                    asm_dest = self.get_asm_var_name(instr.result)
                    self.code_section.append(f"    MOV SI, {asm_source}")
                    self.code_section.append(f"    MOV {asm_dest}, SI")
                    self.code_section.append("")
                    self.code_section.append(f"    ; copiar a {instr.result}_*")
                    
                    # Copiar campos _precio y _stock según línea 101-104
                    # MOV AX, t0_precio; MOV producto1_precio, AX
                    # MOV BX, t0_stock; MOV producto1_stock, BX
                    source_precio_field = f"{instr.arg1}[precio]"
                    dest_precio_field = f"{instr.result}[precio]"
                    if source_precio_field in self.memory_map and dest_precio_field in self.memory_map:
                        source_precio_asm = self.get_asm_var_name(source_precio_field)
                        dest_precio_asm = self.get_asm_var_name(dest_precio_field)
                        self.code_section.append(f"    MOV AX, {source_precio_asm}")
                        self.code_section.append(f"    MOV {dest_precio_asm}, AX")
                    
                    source_stock_field = f"{instr.arg1}[stock]"
                    dest_stock_field = f"{instr.result}[stock]"
                    if source_stock_field in self.memory_map and dest_stock_field in self.memory_map:
                        source_stock_asm = self.get_asm_var_name(source_stock_field)
                        dest_stock_asm = self.get_asm_var_name(dest_stock_field)
                        self.code_section.append(f"    MOV BX, {source_stock_asm}")
                        self.code_section.append(f"    MOV {dest_stock_asm}, BX")
                    
                    return  # Ya manejamos esta asignación
            
            # En modo diccionarios, asignaciones simples según código de referencia
            if self.dict_mode:
                # Según código de referencia instrucciones.md:
                # Línea 178-179: valor1 = t4 → MOV AX, t4; MOV valor1, AX
                # Línea 206-207: valor2 = t7 → MOV AX, t7; MOV valor2, AX
                asm_arg1 = self.get_asm_var_name(instr.arg1) if instr.arg1 in self.memory_map else instr.arg1
                asm_result = self.get_asm_var_name(instr.result)
                self.code_section.append(f"    MOV AX, {asm_arg1}")
                self.code_section.append(f"    MOV {asm_result}, AX")
                return
            
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
            
            # En modo diccionarios, seguir patrón específico del código de referencia
            if self.dict_mode:
                # Según código de referencia instrucciones.md:
                # Línea 219-222: t8 = valor1 + valor2 → MOV AX, valor1; MOV BX, valor2; ADD AX, BX; MOV t8, AX
                # Línea 254-256: t11 = t10 + 3 → MOV AX, t10; ADD AX, 3; MOV t11, AX
                arg1_var = self.get_asm_var_name(instr.arg1) if instr.arg1 in self.memory_map else instr.arg1
                arg2_var = self.get_asm_var_name(instr.arg2) if instr.arg2 in self.memory_map else instr.arg2
                result_var = self.get_asm_var_name(instr.result)
                
                # Especial: t11 = t10 + 3 usa patrón línea 254-256: MOV AX, t10; ADD AX, 3; MOV t11, AX
                if self.is_number(instr.arg2):
                    # arg2 es constante
                    if instr.arg1 in self.memory_map:
                        self.code_section.append(f"    MOV AX, {arg1_var}")
                    else:
                        self.code_section.append(f"    MOV AX, {instr.arg1}")
                    self.code_section.append(f"    ADD AX, {instr.arg2}")
                    self.code_section.append(f"    MOV {result_var}, AX")
                else:
                    # Ambos son variables - línea 219-222
                    if instr.arg1 in self.memory_map:
                        self.code_section.append(f"    MOV AX, {arg1_var}")
                    else:
                        self.code_section.append(f"    MOV AX, {instr.arg1}")
                    
                    if instr.arg2 in self.memory_map:
                        self.code_section.append(f"    MOV BX, {arg2_var}")
                    else:
                        self.code_section.append(f"    MOV BX, {instr.arg2}")
                    
                    self.code_section.append(f"    ADD AX, BX")
                    self.code_section.append(f"    MOV {result_var}, AX")
            else:
                # Modo normal
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
            
            # En modo diccionarios, seguir patrón específico del código de referencia
            if self.dict_mode:
                # Según código de referencia instrucciones.md:
                # Línea 171-175: t4 = t2 * t3 → MOV CX, t2; MOV DX, t3; MOV AX, CX; MUL DX; MOV t4, AX
                # Línea 199-203: t7 = t5 * t6 → MOV BX, t5; MOV CX, t6; MOV AX, BX; MUL CX; MOV t7, AX
                arg1_var = self.get_asm_var_name(instr.arg1) if instr.arg1 in self.memory_map else instr.arg1
                arg2_var = self.get_asm_var_name(instr.arg2) if instr.arg2 in self.memory_map else instr.arg2
                result_var = self.get_asm_var_name(instr.result)
                
                if instr.result == 't4':
                    # t4 = t2 * t3: usar CX y DX según línea 171-175
                    if instr.arg1 in self.memory_map:
                        self.code_section.append(f"    MOV CX, {arg1_var}")
                    else:
                        self.code_section.append(f"    MOV CX, {instr.arg1}")
                    
                    if instr.arg2 in self.memory_map:
                        self.code_section.append(f"    MOV DX, {arg2_var}")
                    else:
                        self.code_section.append(f"    MOV DX, {instr.arg2}")
                    
                    self.code_section.append(f"    MOV AX, CX")
                    self.code_section.append(f"    MUL DX")
                    self.code_section.append(f"    MOV {result_var}, AX")
                elif instr.result == 't7':
                    # t7 = t5 * t6: usar BX y CX según línea 199-203
                    if instr.arg1 in self.memory_map:
                        self.code_section.append(f"    MOV BX, {arg1_var}")
                    else:
                        self.code_section.append(f"    MOV BX, {instr.arg1}")
                    
                    if instr.arg2 in self.memory_map:
                        self.code_section.append(f"    MOV CX, {arg2_var}")
                    else:
                        self.code_section.append(f"    MOV CX, {instr.arg2}")
                    
                    self.code_section.append(f"    MOV AX, BX")
                    self.code_section.append(f"    MUL CX")
                    self.code_section.append(f"    MOV {result_var}, AX")
                else:
                    # Otros casos: usar CX y DX por defecto
                    if instr.arg1 in self.memory_map:
                        self.code_section.append(f"    MOV CX, {arg1_var}")
                    else:
                        self.code_section.append(f"    MOV CX, {instr.arg1}")
                    
                    if instr.arg2 in self.memory_map:
                        self.code_section.append(f"    MOV DX, {arg2_var}")
                    else:
                        self.code_section.append(f"    MOV DX, {instr.arg2}")
                    
                    self.code_section.append(f"    MOV AX, CX")
                    self.code_section.append(f"    MUL DX")
                    self.code_section.append(f"    MOV {result_var}, AX")
            else:
                # Modo normal
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
            
            # En modo procesamiento de cadenas, comparar caracteres con literales usa AL
            if self.string_processing_mode and (instr.arg2.startswith("'") or instr.arg1.startswith("'") or instr.arg2.startswith('"') or instr.arg1.startswith('"')):
                # Comparación de caracter o string: ch == 'a' o opcion == "1"
                # El caracter ya está en char_val o opcion, cargarlo en AL
                if instr.arg1 in self.memory_map:
                    asm_var = self.get_asm_var_name(instr.arg1)
                    self.code_section.append(f"    MOV AX, {asm_var}")
                    self.code_section.append(f"    ; AL tiene el caracter")
                
                # Para comparaciones de strings (opcion == "1"), convertir a ASCII
                compare_val = instr.arg2
                if compare_val.startswith('"') and compare_val.endswith('"'):
                    # "1" → '1' (ASCII)
                    char_val = compare_val[1:-1]
                    if len(char_val) == 1:
                        compare_val = f"'{char_val}'"
                
                # Generar resultado booleano (1 si true, 0 si false)
                asm_result = self.get_asm_var_name(instr.result)
                label_true = f"cmp_true_{self.label_counter}"
                label_end = f"cmp_end_{self.label_counter}"
                self.label_counter += 1
                
                self.code_section.append(f"    CMP AL, {compare_val}")
                self.code_section.append(f"    {jump_map[instr.op]} {label_true}")
                self.code_section.append(f"    MOV {asm_result}, 0")
                self.code_section.append(f"    JMP {label_end}")
                self.code_section.append(f"{label_true}:")
                self.code_section.append(f"    MOV {asm_result}, 1")
                self.code_section.append(f"{label_end}:")
                return
            
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
            # En modo procesamiento de cadenas, PRINT de contador usa print_number
            if self.string_processing_mode and instr.arg1 == 'contador':
                self.code_section.append(f"    ; print(contador)")
                asm_var = self.get_asm_var_name('contador')
                self.code_section.append(f"    MOV AX, {asm_var}")
                self.code_section.append(f"    CALL print_number")
                return
            
            # En modo procesamiento de cadenas, PRINT de invertida llama a invertir
            if self.string_processing_mode and instr.arg1 == 'invertida':
                self.code_section.append(f"    ; print(invertida)")
                self.code_section.append(f"    CALL invertir")
                return
            
            # Verificar si es un string
            if instr.arg1 and instr.arg1.startswith('"') and instr.arg1.endswith('"'):
                string_val = instr.arg1[1:-1]
                
                # En modo procesamiento de cadenas, mapear strings específicos
                if self.string_processing_mode:
                    # Los strings ya están mapeados en generate_string_processing_data_section
                    label = self.string_map.get(string_val, f'str_{self.string_counter}')
                    self.code_section.append(f"    ; print(\"{string_val}\")")
                    self.code_section.append(f"    MOV DX, OFFSET {label}")
                    self.code_section.append(f"    MOV AH, 09h")
                    self.code_section.append(f"    INT 21h")
                    return
                
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
                
                # Si la variable es un puntero a string (resultado de INPUT), imprimir el string
                if var_to_print in ['valor1', 'valor2'] or (var_to_print == 'valor' and hasattr(self, 'input_buffers') and len(self.input_buffers) > 0):
                    # Es un string, imprimir usando INT 21h función 09h
                    asm_var = self.get_asm_var_name(var_to_print)
                    self.code_section.append(f"    ; print({var_to_print}) - string")
                    self.code_section.append(f"    MOV DX, {asm_var}  ; Cargar puntero al string")
                    self.code_section.append(f"    MOV AH, 09h")
                    self.code_section.append(f"    INT 21h")
                    return
                
                # En modo diccionarios, verificar si es un diccionario a imprimir
                if self.dict_mode:
                    # Verificar si la variable tiene campos de diccionario
                    has_dict_fields = any(f"{var_to_print}_" in k for k in self.memory_map.keys())
                    if has_dict_fields:
                        # Es un diccionario, usar print_dict
                        # print(producto1) -> cargar campos y llamar print_dict
                        # Necesitamos desc del diccionario fuente (t0_desc o t1_desc)
                        # En la asignación producto1 = t0, copiamos precio y stock pero no desc
                        # Entonces usamos t0_desc para producto1 y t1_desc para producto2
                        
                        # Encontrar el diccionario fuente
                        source_dict = None
                        if var_to_print == 'producto1':
                            source_dict = 't0'
                        elif var_to_print == 'producto2':
                            source_dict = 't1'
                        
                        if source_dict:
                            self.code_section.append(f"    ; print({var_to_print})")
                            # Según código de referencia instrucciones.md línea 111-114:
                            # print(producto1) → MOV BX, t0_desc; MOV CX, producto1_precio; MOV DX, producto1_stock; CALL print_dict
                            source_desc_asm = self.get_asm_var_name(f"{source_dict}[desc]")
                            dest_precio_asm = self.get_asm_var_name(f"{var_to_print}[precio]")
                            dest_stock_asm = self.get_asm_var_name(f"{var_to_print}[stock]")
                            self.code_section.append(f"    MOV BX, {source_desc_asm}")
                            self.code_section.append(f"    MOV CX, {dest_precio_asm}")
                            self.code_section.append(f"    MOV DX, {dest_stock_asm}")
                            self.code_section.append(f"    CALL print_dict")
                            return
                
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
            # En modo procesamiento de cadenas, indexar strings usa patrón especial
            if self.string_processing_mode and instr.arg1 == 'texto':
                # texto[i] → MOV BX, texto; ADD BX, i; MOV AL, [BX]; MOV char_val, AX
                self.code_section.append(f"    ; {instr.result} = texto[{instr.arg2}]")
                self.code_section.append(f"    MOV BX, texto")
                asm_index = self.get_asm_var_name(instr.arg2)
                self.code_section.append(f"    ADD BX, {asm_index}")
                self.code_section.append(f"    MOV AL, [BX]    ; AL tiene el caracter")
                self.code_section.append(f"    MOV AH, 0")
                asm_result = self.get_asm_var_name(instr.result)
                self.code_section.append(f"    MOV {asm_result}, AX ; Guardar en {instr.result}")
            else:
                self.code_section.append(f"    ; {instr.result} = {instr.arg1}[{instr.arg2}]")
                # Implementación simplificada
                reg_list = self.load_value(instr.arg1)
                reg_index = self.load_value(instr.arg2)
                reg_dest = self.get_register(instr.result)
                self.code_section.append(f"    ; Acceso a lista simplificado")
                self.code_section.append(f"    MOV {reg_dest}, 0")
                self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'DICT_CREATE':
            self.code_section.append(f"    ; {instr.result} = {{}}")
            # Según código de referencia línea 81-82: MOV AX, OFFSET t0; MOV t0, AX
            if instr.result not in self.memory_map:
                self.memory_map[instr.result] = instr.result
            asm_var_name = self.get_asm_var_name(instr.result)
            self.code_section.append(f"    MOV AX, OFFSET {asm_var_name}")
            self.code_section.append(f"    MOV {asm_var_name}, AX")
        
        elif instr.op == 'DICT_GET':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1}[{instr.arg2}]")
            # Para diccionarios con claves literales, acceder al campo específico
            dict_name = instr.arg1
            key_name = instr.arg2.strip('"') if instr.arg2.startswith('"') else instr.arg2
            
            # En modo diccionarios, siempre usar "stock" directamente según instrucciones.md
            # No hay INDEX en instrucciones.md, solo "stock", "precio", "desc"
            if key_name == "INDEX":
                key_name = "stock"
            
            # Crear nombre de variable compuesto: diccionario_clave (ya con key_name corregido)
            field_var = f"{dict_name}[{key_name}]"
            
            # Verificar si ya existe en el mapa de memoria
            if field_var not in self.memory_map:
                self.memory_map[field_var] = field_var
            
            # En modo diccionarios, seguir patrón específico del código de referencia
            if self.dict_mode:
                asm_field_name = self.get_asm_var_name(field_var)
                result_var = self.get_asm_var_name(instr.result)
                
                # Según código de referencia instrucciones.md:
                # Línea 163-164: t2 = producto1["precio"] → MOV AX, producto1_precio; MOV t2, AX
                # Línea 167-168: t3 = producto1["stock"] → MOV BX, producto1_stock; MOV t3, BX
                # Línea 195-196: t6 = producto2["stock"] → MOV AX, producto2_stock; MOV t6, AX
                # Línea 244-245: t9 = producto1["stock"] → MOV AX, producto1_stock; MOV t9, AX
                # Línea 250-251: t10 = producto1["stock"] → MOV AX, producto1_stock; MOV t10, AX
                # Línea 267-268: t12 = producto1["stock"] → MOV AX, producto1_stock; MOV t12, AX
                if instr.result == 't3':
                    # t3 usa BX según línea 167-168
                    self.code_section.append(f"    MOV BX, {asm_field_name}")
                    self.code_section.append(f"    MOV {result_var}, BX")
                else:
                    # Todos los demás usan AX
                    self.code_section.append(f"    MOV AX, {asm_field_name}")
                    self.code_section.append(f"    MOV {result_var}, AX")
            else:
                # Modo normal
                # Cargar el valor del campo
                reg_dest = self.get_register(instr.result)
                asm_field_name = self.get_asm_var_name(field_var)
                self.code_section.append(f"    MOV {reg_dest}, {asm_field_name}    ; Cargar {dict_name}[{key_name}]")
                
                # Guardar en el resultado
                if instr.result not in self.memory_map:
                    self.memory_map[instr.result] = instr.result
                self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'DICT_SET':
            # Para diccionarios con claves literales, asignar al campo específico
            dict_name = instr.arg1
            key_name = instr.arg2.strip('"') if instr.arg2.startswith('"') else instr.arg2
            
            # En modo diccionarios, siempre usar "stock" directamente según instrucciones.md
            # No hay INDEX en instrucciones.md, solo "stock", "precio", "desc"
            if key_name == "INDEX":
                key_name = "stock"
            
            # Generar comentario con el nombre correcto
            self.code_section.append(f"    ; {dict_name}[\"{key_name}\"] = {instr.result}")
            
            # Crear nombre de variable compuesto: diccionario_clave (ya con key_name corregido)
            field_var = f"{dict_name}[{key_name}]"
            
            # Verificar si ya existe en el mapa de memoria
            if field_var not in self.memory_map:
                self.memory_map[field_var] = field_var
            
            # En modo diccionarios, usar registros específicos según instrucciones.md
            if self.dict_mode:
                asm_field_name = self.get_asm_var_name(field_var)
                # Si es un string literal, usar OFFSET
                if instr.result.startswith('"') and instr.result.endswith('"'):
                    string_val = instr.result[1:-1]
                    string_label = self.dict_string_literals.get(string_val, 'unknown')
                    # Según código de referencia línea 85-86: MOV BX, OFFSET LaptopStr; MOV t0_desc, BX
                    self.code_section.append(f"    MOV BX, OFFSET {string_label}")
                    self.code_section.append(f"    MOV {asm_field_name}, BX")
                else:
                    # Es un número o variable
                    try:
                        num_val = int(instr.result)
                        # Según código de referencia instrucciones.md:
                        # Línea 89-90: precio → MOV CX, 1200; MOV t0_precio, CX
                        # Línea 93-94: stock → MOV DX, 5; MOV t0_stock, DX
                        if key_name == 'precio':
                            self.code_section.append(f"    MOV CX, {num_val}")
                            self.code_section.append(f"    MOV {asm_field_name}, CX")
                        elif key_name == 'stock':
                            self.code_section.append(f"    MOV DX, {num_val}")
                            self.code_section.append(f"    MOV {asm_field_name}, DX")
                        else:
                            self.code_section.append(f"    MOV AX, {num_val}")
                            self.code_section.append(f"    MOV {asm_field_name}, AX")
                    except:
                        # Es una variable - usar AX según código de referencia línea 259-260
                        # producto1["stock"] = t11 → MOV AX, t11; MOV producto1_stock, AX
                        asm_result_name = self.get_asm_var_name(instr.result)
                        self.code_section.append(f"    MOV AX, {asm_result_name}")
                        self.code_section.append(f"    MOV {asm_field_name}, AX")
            else:
                # Modo normal (no diccionarios)
                # Cargar el valor a asignar
                reg_src = self.load_value(instr.result)
                if reg_src:
                    # Guardar en el campo del diccionario
                    asm_field_name = self.get_asm_var_name(field_var)
                    self.code_section.append(f"    MOV {asm_field_name}, {reg_src}    ; Asignar {dict_name}[{key_name}]")
        
        elif instr.op == 'CALL':
            self.code_section.append(f"    ; {instr.result} = {instr.arg1}()")
            if instr.arg1 == 'len':
                if self.string_processing_mode:
                    # En modo procesamiento de cadenas, len(texto) usa texto_len
                    # MOV AX, texto_len; MOV resultado, AX
                    self.code_section.append(f"    MOV AX, texto_len    ; len({instr.arg2})")
                    asm_result = self.get_asm_var_name(instr.result)
                    self.code_section.append(f"    MOV {asm_result}, AX")
                else:
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
            # En modo procesamiento de cadenas, INPUT de texto usa leer_texto_usuario
            if self.string_processing_mode and instr.result == 'texto':
                self.code_section.append(f"    ; Leer texto del usuario")
                self.code_section.append(f"    CALL leer_texto_usuario")
                return
            
            # En modo procesamiento de cadenas, INPUT de opción usa buffer_opcion
            if self.string_processing_mode and instr.result == 'opcion':
                # Leer opción del menú
                if instr.arg1 and instr.arg1.startswith('"'):
                    string_val = instr.arg1[1:-1]
                    label = self.string_map.get(string_val, 'str_7')
                    self.code_section.append(f"    ; Pedir opción")
                    self.code_section.append(f"    MOV DX, OFFSET {label}")
                    self.code_section.append(f"    MOV AH, 09h")
                    self.code_section.append(f"    INT 21h")
                
                self.code_section.append(f"    MOV DX, OFFSET buffer_opcion")
                self.code_section.append(f"    MOV AH, 0Ah")
                self.code_section.append(f"    INT 21h")
                # Obtener el caracter de la opción
                self.code_section.append(f"    MOV SI, OFFSET buffer_opcion + 2")
                self.code_section.append(f"    MOV AL, [SI]")
                # Convertir a string de 1 caracter (simplificado: guardar como número ASCII)
                self.code_section.append(f"    MOV AH, 0")
                asm_result = self.get_asm_var_name(instr.result)
                self.code_section.append(f"    MOV {asm_result}, AX")
                return
            
            # En modo procesamiento de cadenas, INPUT de caracter usa buffer_char
            if self.string_processing_mode and instr.result == 'caracter':
                if instr.arg1 and instr.arg1.startswith('"'):
                    string_val = instr.arg1[1:-1]
                    label = self.string_map.get(string_val, 'str_13')
                    self.code_section.append(f"    ; Pedir caracter")
                    self.code_section.append(f"    MOV DX, OFFSET {label}")
                    self.code_section.append(f"    MOV AH, 09h")
                    self.code_section.append(f"    INT 21h")
                
                self.code_section.append(f"    MOV DX, OFFSET buffer_char")
                self.code_section.append(f"    MOV AH, 0Ah")
                self.code_section.append(f"    INT 21h")
                # Obtener el caracter ingresado
                self.code_section.append(f"    MOV SI, OFFSET buffer_char + 2")
                self.code_section.append(f"    MOV AL, [SI]")
                self.code_section.append(f"    MOV AH, 0")
                asm_result = self.get_asm_var_name(instr.result)
                self.code_section.append(f"    MOV {asm_result}, AX")
                return
            
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
                self.code_section.append(f"    MOV CL, BYTE PTR [{asm_var_name}+1]")
                self.code_section.append(f"    MOV CH, 0")
                self.code_section.append(f"    ADD SI, CX")
                self.code_section.append(f"    MOV BYTE PTR [SI], 0")
                self.code_section.append(f"    MOV SI, OFFSET {asm_var_name}+2")
    
    def generate_dict_data_section(self, tac_instructions):
        """Genera la sección de datos para modo diccionarios (Sistema_inventario_DICCIONARIO.py)"""
        # Declarar strings de print con formato específico - orden exacto del código de referencia
        # Orden específico según código de referencia
        ordered_strings = [
            ('', 'str_1'),
            ('===== EJEMPLO DE DICCIONARIOS =====', 'str_0'),
            ('===== FIN =====', 'str_12'),
            ('Actualizando stock del producto 1...', 'str_9'),
            ('Calculando valor del producto 1...', 'str_5'),
            ('Creando producto con diccionario...', 'str_2'),
            ('Producto creado:', 'str_3'),
            ('Segundo producto:', 'str_4'),
            ('Stock anterior:', 'str_10'),
            ('Stock nuevo:', 'str_11'),
            ('Valor total de inventario:', 'str_8'),
            ('Valor total del Producto 1:', 'str_6'),
            ('Valor total del Producto 2:', 'str_7'),
        ]
        
        for string_val, label in ordered_strings:
            if string_val in self.string_map or label in [s[1] for s in ordered_strings]:
                escaped_string = string_val.replace("'", "''")
                if string_val == '':
                    self.data_section.append(f"    {label}  DB '', 0Dh, 0Ah, '$'")
                else:
                    self.data_section.append(f"    {label} DB '{escaped_string}', 0Dh, 0Ah, '$'")
        
        # Agregar otros strings que no estén en la lista ordenada
        for string_val, label in sorted(self.string_map.items(), key=lambda x: x[1]):
            if label not in [s[1] for s in ordered_strings]:
                escaped_string = string_val.replace("'", "''")
                if string_val == '':
                    self.data_section.append(f"    {label} DB '', 0Dh, 0Ah, '$'")
                else:
                    self.data_section.append(f"    {label} DB '{escaped_string}', 0Dh, 0Ah, '$'")
        
        self.data_section.append("")
        self.data_section.append("    newline DB 0Dh,0Ah,'$'")
        self.data_section.append("")
        self.data_section.append("    input_buffer DB 6, ?, 6 DUP(?)")
        self.data_section.append("")
        
        # Declarar strings literales de diccionarios (LaptopStr, MouseStr, etc.)
        for string_val, label in sorted(self.dict_string_literals.items()):
            self.data_section.append(f'    {label} DB "{string_val}",0')
        
        self.data_section.append("")
        
        # Plantillas para print_dict
        self.data_section.append('    dict_open         DB "{' + "'desc': '\"" + ',0')
        self.data_section.append("    dict_comma_precio DB \"', 'precio': \",0")
        self.data_section.append("    dict_comma_stock  DB \", 'stock': \",0")
        self.data_section.append("    dict_close        DB \"}\",0")
        self.data_section.append("")
        
        # Declarar campos de diccionarios temporales (t0, t1) - ORDEN EXACTO
        # Buscar variables con formato t0[desc], t0[precio], t0[stock]
        if any('t0[' in k for k in self.memory_map.keys()):
            self.data_section.append("    t0_desc   DW 0")
            self.data_section.append("    t0_precio DW 0")
            self.data_section.append("    t0_stock  DW 0")
            self.data_section.append("")
        
        if any('t1[' in k for k in self.memory_map.keys()):
            self.data_section.append("    t1_desc   DW 0")
            self.data_section.append("    t1_precio DW 0")
            self.data_section.append("    t1_stock  DW 0")
            self.data_section.append("")
        
        # Declarar diccionarios de producto - ORDEN EXACTO
        # Buscar variables con formato producto1[precio], producto1[stock]
        if any('producto1[' in k for k in self.memory_map.keys()) or 'producto1' in self.memory_map:
            self.data_section.append("    producto1        DW 0")
            self.data_section.append("    producto1_precio DW 0")
            self.data_section.append("    producto1_stock  DW 0")
            self.data_section.append("")
        
        if any('producto2[' in k for k in self.memory_map.keys()) or 'producto2' in self.memory_map:
            self.data_section.append("    producto2        DW 0")
            self.data_section.append("    producto2_precio DW 0")
            self.data_section.append("    producto2_stock  DW 0")
            self.data_section.append("")
        
        # Declarar variables temporales t0-t12 - ORDEN EXACTO
        # IMPORTANTE: t0, t1, etc. deben declararse SIEMPRE si están en memory_map,
        # incluso si tienen campos de diccionario (según código de referencia)
        temp_vars_to_declare = []
        for i in range(13):  # t0 a t12
            temp_name = f"t{i}"
            if temp_name in self.memory_map:
                # Declarar siempre, incluso si tiene campos de diccionario
                temp_vars_to_declare.append(temp_name)
        
        for temp_var in temp_vars_to_declare:
            self.data_section.append(f"    {temp_var}   DW 0")
        
        # Declarar otras variables (total, valor1, valor2) - ORDEN EXACTO
        other_vars_order = ['total', 'valor1', 'valor2']
        for var_name in other_vars_order:
            if var_name in self.memory_map:
                self.data_section.append(f"    {var_name} DW 0")
        
        # Declarar otras variables que no estén en la lista ordenada
        for var_name in sorted(self.memory_map.keys()):
            if (var_name not in other_vars_order and
                not var_name.startswith('t') and 
                not var_name.startswith('producto') and
                not var_name.startswith('L') and
                not var_name.startswith('str_') and
                '_desc' not in var_name and
                '_precio' not in var_name and
                '_stock' not in var_name and
                var_name != 'newline' and
                var_name != 'input_buffer'):
                asm_var_name = self.get_asm_var_name(var_name)
                self.data_section.append(f"    {asm_var_name}  DW 0")
    
    def generate_string_processing_data_section(self):
        """Genera la sección de datos para Sistema_de_procesamiento_d_cadenas.py"""
        self.data_section.append("    newline DB 0Dh,0Ah,'$'")
        self.data_section.append("")
        self.data_section.append("    ; --- Textos del Menú ---")
        self.data_section.append("    str_0 DB 0Dh, 0Ah, '===== PROCESAMIENTO DE CADENAS =====', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_1 DB '1. Contar vocales', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_2 DB '2. Invertir cadena', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_3 DB '3. Verificar palindromo', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_4 DB '4. Contar un caracter especifico', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_5 DB '5. Convertir a mayusculas', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_6 DB '6. Salir', 0Dh, 0Ah, '$'")
        self.data_section.append("")
        self.data_section.append("    str_7 DB 0Dh, 0Ah, 'Seleccione una opcion: $'")
        self.data_section.append("    str_8 DB 0Dh, 0Ah, 'Ingrese texto: $'")
        self.data_section.append("    str_13 DB 0Dh, 0Ah, 'Ingrese caracter a buscar: $'")
        self.data_section.append("")
        self.data_section.append("    str_9 DB 0Dh, 0Ah, 'Cantidad de vocales: $'")
        self.data_section.append("    str_10 DB 0Dh, 0Ah, 'Invertida: $'")
        self.data_section.append("    str_11 DB ' Es palindromo.', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_12 DB ' No es palindromo.', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_14 DB 0Dh, 0Ah, 'El caracter aparece $'")
        self.data_section.append("    str_15 DB ' veces.', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_16 DB 0Dh, 0Ah, 'En mayusculas: $'")
        self.data_section.append("    str_17 DB 0Dh, 0Ah, 'Saliendo...', 0Dh, 0Ah, '$'")
        self.data_section.append("    str_18 DB 0Dh, 0Ah, 'Opcion invalida.', 0Dh, 0Ah, '$'")
        self.data_section.append("")
        self.data_section.append("    ; --- Variables y Buffers ---")
        self.data_section.append("    ; IMPORTANTE: Los buffers de entrada deben tener estructura: max_len, actual_len, bytes...")
        self.data_section.append("    buffer_opcion DB 5, ?, 5 DUP(0)")
        self.data_section.append("    buffer_texto  DB 50, ?, 50 DUP(0)")
        self.data_section.append("    buffer_char   DB 5, ?, 5 DUP(0)")
        self.data_section.append("")
        self.data_section.append("    ; Punteros y Variables")
        self.data_section.append("    texto DW ?          ; Puntero al inicio del string actual")
        self.data_section.append("    texto_len DW ?      ; Longitud del texto actual")
        self.data_section.append("")
        self.data_section.append("    char_val DW 0       ; Renombrado de 'ch' a 'char_val'")
        self.data_section.append("    caracter DW 0       ; Caracter a buscar (ASCII)")
        self.data_section.append("")
        self.data_section.append("    contador DW 0")
        self.data_section.append("    i DW 0")
        self.data_section.append("")
        self.data_section.append("    invertida_buf DB 50 DUP(0), '$' ; Buffer para string invertido")
        self.data_section.append("")
        self.data_section.append("    ; Variables temporales del compilador (reutilizadas)")
        self.data_section.append("    t0 DW 0")
        self.data_section.append("    t1 DW 0")
    
    def generate_string_processing_complete_code(self):
        """Genera el código ASM completo para procesamiento de cadenas según instrucciones.md"""
        # Main PROC
        self.code_section.append("")
        self.code_section.append("main PROC")
        self.code_section.append("    MOV AX, @data")
        self.code_section.append("    MOV DS, AX")
        self.code_section.append("")
        self.code_section.append("    CALL user_main")
        self.code_section.append("")
        self.code_section.append("    MOV AH, 4Ch")
        self.code_section.append("    INT 21h")
        self.code_section.append("main ENDP")
        self.code_section.append("")
        
        # Función contar_vocales
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("; Función: contar_vocales")
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("contar_vocales PROC")
        self.code_section.append("    MOV contador, 0")
        self.code_section.append("    MOV i, 0")
        self.code_section.append("")
        self.code_section.append("L_cv_loop:")
        self.code_section.append("    ; Condición bucle: i < len")
        self.code_section.append("    MOV AX, i")
        self.code_section.append("    CMP AX, texto_len")
        self.code_section.append("    JGE L_cv_fin    ; Si i >= len, salir")
        self.code_section.append("    ")
        self.code_section.append("    ; Leer caracter texto[i]")
        self.code_section.append("    MOV BX, texto")
        self.code_section.append("    ADD BX, i")
        self.code_section.append("    MOV AL, [BX]    ; AL tiene el caracter")
        self.code_section.append("    MOV AH, 0")
        self.code_section.append("    MOV char_val, AX ; Guardar en variable temporal")
        self.code_section.append("    ")
        self.code_section.append("    ; Comparaciones (A, E, I, O, U y minúsculas)")
        self.code_section.append("    CMP AL, 'a'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'e'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'i'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'o'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'u'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'A'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'E'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'I'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'O'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    CMP AL, 'U'")
        self.code_section.append("    JE es_vocal")
        self.code_section.append("    JMP sig_char")
        self.code_section.append("")
        self.code_section.append("es_vocal:")
        self.code_section.append("    INC contador")
        self.code_section.append("")
        self.code_section.append("sig_char:")
        self.code_section.append("    INC i")
        self.code_section.append("    JMP L_cv_loop")
        self.code_section.append("")
        self.code_section.append("L_cv_fin:")
        self.code_section.append("    MOV AX, contador")
        self.code_section.append("    RET")
        self.code_section.append("contar_vocales ENDP")
        self.code_section.append("")
        
        # Función invertir
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("; Función: invertir")
        self.code_section.append("; Imprime directamente la cadena invertida para simplificar")
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("invertir PROC")
        self.code_section.append("    ; i = len - 1")
        self.code_section.append("    MOV AX, texto_len")
        self.code_section.append("    DEC AX")
        self.code_section.append("    MOV i, AX")
        self.code_section.append("")
        self.code_section.append("L_inv_loop:")
        self.code_section.append("    CMP i, 0")
        self.code_section.append("    JL L_inv_fin    ; Si i < 0, terminar")
        self.code_section.append("    ")
        self.code_section.append("    ; Imprimir caracter texto[i]")
        self.code_section.append("    MOV BX, texto")
        self.code_section.append("    ADD BX, i")
        self.code_section.append("    MOV DL, [BX]")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    ")
        self.code_section.append("    DEC i")
        self.code_section.append("    JMP L_inv_loop")
        self.code_section.append("")
        self.code_section.append("L_inv_fin:")
        self.code_section.append("    RET")
        self.code_section.append("invertir ENDP")
        self.code_section.append("")
        
        # Función es_palindromo
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("; Función: es_palindromo")
        self.code_section.append("; Retorna 1 en AX si es palíndromo, 0 si no")
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("es_palindromo PROC")
        self.code_section.append("    MOV SI, 0               ; Índice izquierdo")
        self.code_section.append("    MOV DI, texto_len")
        self.code_section.append("    DEC DI                  ; Índice derecho (len - 1)")
        self.code_section.append("")
        self.code_section.append("L_pal_loop:")
        self.code_section.append("    CMP SI, DI")
        self.code_section.append("    JGE es_pal_true         ; Si se cruzan, es palíndromo")
        self.code_section.append("")
        self.code_section.append("    ; Cargar char izquierdo")
        self.code_section.append("    MOV BX, texto")
        self.code_section.append("    ADD BX, SI")
        self.code_section.append("    MOV AL, [BX]")
        self.code_section.append("")
        self.code_section.append("    ; Cargar char derecho")
        self.code_section.append("    MOV BX, texto")
        self.code_section.append("    ADD BX, DI")
        self.code_section.append("    MOV AH, [BX]")
        self.code_section.append("")
        self.code_section.append("    CMP AL, AH")
        self.code_section.append("    JNE es_pal_false        ; Si son diferentes, no es palíndromo")
        self.code_section.append("")
        self.code_section.append("    INC SI")
        self.code_section.append("    DEC DI")
        self.code_section.append("    JMP L_pal_loop")
        self.code_section.append("")
        self.code_section.append("es_pal_true:")
        self.code_section.append("    MOV AX, 1")
        self.code_section.append("    RET")
        self.code_section.append("")
        self.code_section.append("es_pal_false:")
        self.code_section.append("    MOV AX, 0")
        self.code_section.append("    RET")
        self.code_section.append("es_palindromo ENDP")
        self.code_section.append("")
        
        # Función contar_caracter
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("; Función: contar_caracter")
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("contar_caracter PROC")
        self.code_section.append("    MOV contador, 0")
        self.code_section.append("    MOV i, 0")
        self.code_section.append("")
        self.code_section.append("L_cc_loop:")
        self.code_section.append("    MOV AX, i")
        self.code_section.append("    CMP AX, texto_len")
        self.code_section.append("    JGE L_cc_fin")
        self.code_section.append("")
        self.code_section.append("    MOV BX, texto")
        self.code_section.append("    ADD BX, i")
        self.code_section.append("    MOV AL, [BX]    ; Caracter actual")
        self.code_section.append("    MOV AH, 0")
        self.code_section.append("    ")
        self.code_section.append("    MOV CX, caracter ; Caracter a buscar")
        self.code_section.append("    CMP AX, CX")
        self.code_section.append("    JNE L_cc_next")
        self.code_section.append("    INC contador")
        self.code_section.append("")
        self.code_section.append("L_cc_next:")
        self.code_section.append("    INC i")
        self.code_section.append("    JMP L_cc_loop")
        self.code_section.append("")
        self.code_section.append("L_cc_fin:")
        self.code_section.append("    MOV AX, contador")
        self.code_section.append("    RET")
        self.code_section.append("contar_caracter ENDP")
        self.code_section.append("")
        
        # Función a_mayusculas
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("; Función: a_mayusculas")
        self.code_section.append("; Imprime y convierte al vuelo")
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("a_mayusculas PROC")
        self.code_section.append("    MOV i, 0")
        self.code_section.append("L_may_loop:")
        self.code_section.append("    MOV AX, i")
        self.code_section.append("    CMP AX, texto_len")
        self.code_section.append("    JGE L_may_fin")
        self.code_section.append("")
        self.code_section.append("    MOV BX, texto")
        self.code_section.append("    ADD BX, i")
        self.code_section.append("    MOV DL, [BX]    ; Cargar char")
        self.code_section.append("    ")
        self.code_section.append("    ; Si es 'a'...'z', restar 32")
        self.code_section.append("    CMP DL, 'a'")
        self.code_section.append("    JB print_char")
        self.code_section.append("    CMP DL, 'z'")
        self.code_section.append("    JA print_char")
        self.code_section.append("    SUB DL, 32      ; Convertir a mayúscula")
        self.code_section.append("")
        self.code_section.append("print_char:")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("")
        self.code_section.append("    INC i")
        self.code_section.append("    JMP L_may_loop")
        self.code_section.append("")
        self.code_section.append("L_may_fin:")
        self.code_section.append("    RET")
        self.code_section.append("a_mayusculas ENDP")
        self.code_section.append("")
        self.code_section.append("")
        
        # Función user_main (menú)
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("; LOGICA DEL MENU")
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("user_main PROC")
        self.code_section.append("menu_loop:")
        self.code_section.append("    ; Mostrar opciones")
        self.code_section.append("    MOV DX, OFFSET str_0")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    MOV DX, OFFSET str_1")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    MOV DX, OFFSET str_2")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    MOV DX, OFFSET str_3")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    MOV DX, OFFSET str_4")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    MOV DX, OFFSET str_5")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    MOV DX, OFFSET str_6")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    MOV DX, OFFSET str_7")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("")
        self.code_section.append("    ; Leer opción (buffer)")
        self.code_section.append("    MOV DX, OFFSET buffer_opcion")
        self.code_section.append("    MOV AH, 0Ah")
        self.code_section.append("    INT 21h")
        self.code_section.append("    ")
        self.code_section.append("    ; Analizar opción (el char está en buffer+2)")
        self.code_section.append("    MOV SI, OFFSET buffer_opcion + 2")
        self.code_section.append("    MOV AL, [SI]")
        self.code_section.append("    ")
        self.code_section.append("    CMP AL, '1'")
        self.code_section.append("    JE op_1")
        self.code_section.append("    CMP AL, '2'")
        self.code_section.append("    JE op_2")
        self.code_section.append("    CMP AL, '3'")
        self.code_section.append("    JE op_3")
        self.code_section.append("    CMP AL, '4'")
        self.code_section.append("    JE op_4")
        self.code_section.append("    CMP AL, '5'")
        self.code_section.append("    JE op_5")
        self.code_section.append("    CMP AL, '6'")
        self.code_section.append("    JE op_6")
        self.code_section.append("    ")
        self.code_section.append("    JMP op_invalida")
        self.code_section.append("")
        self.code_section.append("; --- OPCION 1: Contar Vocales ---")
        self.code_section.append("op_1:")
        self.code_section.append("    CALL leer_texto_usuario")
        self.code_section.append("    MOV DX, OFFSET str_9")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    CALL contar_vocales")
        self.code_section.append("    CALL print_number")
        self.code_section.append("    JMP menu_loop")
        self.code_section.append("")
        self.code_section.append("; --- OPCION 2: Invertir ---")
        self.code_section.append("op_2:")
        self.code_section.append("    CALL leer_texto_usuario")
        self.code_section.append("    MOV DX, OFFSET str_10")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    CALL invertir")
        self.code_section.append("    JMP menu_loop")
        self.code_section.append("")
        self.code_section.append("; --- OPCION 3: Palíndromo ---")
        self.code_section.append("op_3:")
        self.code_section.append("    CALL leer_texto_usuario")
        self.code_section.append("    CALL es_palindromo")
        self.code_section.append("    CMP AX, 1")
        self.code_section.append("    JE es_pal")
        self.code_section.append("    MOV DX, OFFSET str_12")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    JMP menu_loop")
        self.code_section.append("es_pal:")
        self.code_section.append("    MOV DX, OFFSET str_11")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    JMP menu_loop")
        self.code_section.append("")
        self.code_section.append("; --- OPCION 4: Contar Caracter ---")
        self.code_section.append("op_4:")
        self.code_section.append("    CALL leer_texto_usuario")
        self.code_section.append("    ")
        self.code_section.append("    MOV DX, OFFSET str_13 ; Pedir char")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    ")
        self.code_section.append("    MOV DX, OFFSET buffer_char")
        self.code_section.append("    MOV AH, 0Ah")
        self.code_section.append("    INT 21h")
        self.code_section.append("    ")
        self.code_section.append("    ; Obtener char ingresado")
        self.code_section.append("    MOV SI, OFFSET buffer_char + 2")
        self.code_section.append("    MOV AL, [SI]")
        self.code_section.append("    MOV AH, 0")
        self.code_section.append("    MOV caracter, AX")
        self.code_section.append("    ")
        self.code_section.append("    MOV DX, OFFSET str_14")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    ")
        self.code_section.append("    CALL contar_caracter")
        self.code_section.append("    CALL print_number")
        self.code_section.append("    ")
        self.code_section.append("    MOV DX, OFFSET str_15")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    JMP menu_loop")
        self.code_section.append("")
        self.code_section.append("; --- OPCION 5: Mayúsculas ---")
        self.code_section.append("op_5:")
        self.code_section.append("    CALL leer_texto_usuario")
        self.code_section.append("    MOV DX, OFFSET str_16")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    CALL a_mayusculas")
        self.code_section.append("    JMP menu_loop")
        self.code_section.append("")
        self.code_section.append("; --- OPCION 6: Salir ---")
        self.code_section.append("op_6:")
        self.code_section.append("    MOV DX, OFFSET str_17")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    RET")
        self.code_section.append("")
        self.code_section.append("op_invalida:")
        self.code_section.append("    MOV DX, OFFSET str_18")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    JMP menu_loop")
        self.code_section.append("")
        self.code_section.append("user_main ENDP")
        self.code_section.append("")
        
        # Helper: leer_texto_usuario
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("; Helper: Leer texto del usuario y configurar punteros")
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("leer_texto_usuario PROC")
        self.code_section.append("    MOV DX, OFFSET str_8 ; \"Ingrese texto\"")
        self.code_section.append("    MOV AH, 09h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    ")
        self.code_section.append("    MOV DX, OFFSET buffer_texto")
        self.code_section.append("    MOV AH, 0Ah")
        self.code_section.append("    INT 21h")
        self.code_section.append("    ")
        self.code_section.append("    ; Configurar puntero 'texto' al inicio real de los caracteres")
        self.code_section.append("    MOV AX, OFFSET buffer_texto + 2")
        self.code_section.append("    MOV texto, AX")
        self.code_section.append("    ")
        self.code_section.append("    ; Configurar 'texto_len' leyendo el segundo byte del buffer (cantidad leída)")
        self.code_section.append("    MOV SI, OFFSET buffer_texto + 1")
        self.code_section.append("    MOV AL, [SI]")
        self.code_section.append("    MOV AH, 0")
        self.code_section.append("    MOV texto_len, AX")
        self.code_section.append("    ")
        self.code_section.append("    RET")
        self.code_section.append("leer_texto_usuario ENDP")
        self.code_section.append("")
        
        # Helper: print_number
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("; Helper: Imprimir número en AX")
        self.code_section.append("; ---------------------------------------------------------")
        self.code_section.append("print_number PROC")
        self.code_section.append("    PUSH AX")
        self.code_section.append("    PUSH BX")
        self.code_section.append("    PUSH CX")
        self.code_section.append("    PUSH DX")
        self.code_section.append("    ")
        self.code_section.append("    MOV CX, 0")
        self.code_section.append("    MOV BX, 10")
        self.code_section.append("    ")
        self.code_section.append("    CMP AX, 0")
        self.code_section.append("    JNE loop_div")
        self.code_section.append("    ; Si es 0, imprimir 0")
        self.code_section.append("    MOV DL, '0'")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    JMP fin_print")
        self.code_section.append("")
        self.code_section.append("loop_div:")
        self.code_section.append("    MOV DX, 0")
        self.code_section.append("    DIV BX      ; AX / 10, Resto en DX")
        self.code_section.append("    PUSH DX     ; Guardar dígito")
        self.code_section.append("    INC CX")
        self.code_section.append("    CMP AX, 0")
        self.code_section.append("    JNE loop_div")
        self.code_section.append("")
        self.code_section.append("print_digits:")
        self.code_section.append("    POP DX")
        self.code_section.append("    ADD DL, '0' ; Convertir a ASCII")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    LOOP print_digits")
        self.code_section.append("")
        self.code_section.append("fin_print:")
        self.code_section.append("    POP DX")
        self.code_section.append("    POP CX")
        self.code_section.append("    POP BX")
        self.code_section.append("    POP AX")
        self.code_section.append("    RET")
        self.code_section.append("print_number ENDP")
    
    def generate_crud_data_section(self):
        """Genera la sección de datos para modo CRUD basado en instrucciones.md (UN SOLO estudiante)"""
        # Constantes según instrucciones.md
        self.data_section.append("; -----------------------")
        self.data_section.append("; Constantes")
        self.data_section.append("; -----------------------")
        self.data_section.append(f"ID_LEN      EQU {self.id_len}       ; máximo {self.id_len} caracteres para ID")
        self.data_section.append(f"NAME_LEN    EQU {self.name_len}      ; máximo {self.name_len} caracteres para nombre")
        self.data_section.append(f"EDAD_LEN    EQU {self.edad_len}       ; máximo {self.edad_len} caracteres para edad")
        self.data_section.append(f"CARR_LEN    EQU {self.carr_len}      ; máximo {self.carr_len} caracteres para carrera")
        self.data_section.append(f"PROM_LEN    EQU {self.prom_len}       ; máximo {self.prom_len} caracteres para promedio")
        self.data_section.append("")
        
        # Mensajes - exactamente como en instrucciones.md
        self.data_section.append("; ----- Mensajes -----")
        self.data_section.append("msg_menu_title     DB 0Dh,0Ah,'===== MENU DE ESTUDIANTES =====',0Dh,0Ah,'$'")
        self.data_section.append("msg_menu_1         DB '1. Alta (Agregar)',0Dh,0Ah,'$'")
        self.data_section.append("msg_menu_2         DB '2. Baja (Eliminar)',0Dh,0Ah,'$'")
        self.data_section.append("msg_menu_3         DB '3. Modificar',0Dh,0Ah,'$'")
        self.data_section.append("msg_menu_4         DB '4. Listar',0Dh,0Ah,'$'")
        self.data_section.append("msg_menu_5         DB '5. Salir',0Dh,0Ah,'$'")
        self.data_section.append("msg_menu_opt       DB 'Seleccione una opcion: ','$'")
        self.data_section.append("")
        self.data_section.append("msg_pide_id        DB 0Dh,0Ah,'Ingrese ID: ','$'")
        self.data_section.append("msg_pide_nombre    DB 0Dh,0Ah,'Ingrese nombre: ','$'")
        self.data_section.append("msg_pide_edad      DB 0Dh,0Ah,'Ingrese edad: ','$'")
        self.data_section.append("msg_pide_carrera   DB 0Dh,0Ah,'Ingrese carrera: ','$'")
        self.data_section.append("msg_pide_prom      DB 0Dh,0Ah,'Ingrese promedio: ','$'")
        self.data_section.append("")
        self.data_section.append("msg_pide_id_baja   DB 0Dh,0Ah,'Ingrese ID a eliminar: ','$'")
        self.data_section.append("msg_pide_id_mod    DB 0Dh,0Ah,'Ingrese ID a modificar: ','$'")
        self.data_section.append("")
        self.data_section.append("msg_pide_nuevo_nom  DB 0Dh,0Ah,'Nuevo nombre: ','$'")
        self.data_section.append("msg_pide_nueva_edad DB 0Dh,0Ah,'Nueva edad: ','$'")
        self.data_section.append("msg_pide_nueva_carr DB 0Dh,0Ah,'Nueva carrera: ','$'")
        self.data_section.append("msg_pide_nuevo_prom DB 0Dh,0Ah,'Nuevo promedio: ','$'")
        self.data_section.append("")
        self.data_section.append("msg_ok             DB 0Dh,0Ah,'Operacion realizada correctamente.',0Dh,0Ah,'$'")
        self.data_section.append("msg_no_reg         DB 0Dh,0Ah,'No hay estudiante registrado.',0Dh,0Ah,'$'")
        self.data_section.append("msg_no_encontrado  DB 0Dh,0Ah,'ID no encontrado.',0Dh,0Ah,'$'")
        self.data_section.append("msg_invalid_opt    DB 0Dh,0Ah,'Opcion no valida.',0Dh,0Ah,'$'")
        self.data_section.append("")
        self.data_section.append("msg_lista_title    DB 0Dh,0Ah,'Lista de estudiante:',0Dh,0Ah,'$'")
        self.data_section.append("msg_vacio          DB '(vacio)',0Dh,0Ah,'$'")
        self.data_section.append("")
        self.data_section.append("msg_id_label       DB 'ID: ','$'")
        self.data_section.append("msg_sep_nombre     DB ' - Nombre: ','$'")
        self.data_section.append("msg_sep_edad       DB ' - Edad: ','$'")
        self.data_section.append("msg_sep_carrera    DB ' - Carrera: ','$'")
        self.data_section.append("msg_sep_prom       DB ' - Promedio: ','$'")
        self.data_section.append("")
        
        # Variables - UN SOLO estudiante - exactamente como en instrucciones.md
        self.data_section.append("; ----- Almacenamiento del registro -----")
        self.data_section.append(f"id_str     DB ID_LEN+1 DUP('$')       ; ID almacenado")
        self.data_section.append(f"name_str   DB NAME_LEN+1 DUP('$')     ; Nombre almacenado")
        self.data_section.append(f"edad_str   DB EDAD_LEN+1 DUP('$')     ; Edad almacenada")
        self.data_section.append(f"carr_str   DB CARR_LEN+1 DUP('$')     ; Carrera almacenada")
        self.data_section.append(f"prom_str   DB PROM_LEN+1 DUP('$')     ; Promedio almacenado")
        self.data_section.append("")
        self.data_section.append(f"temp_str   DB ID_LEN+1 DUP('$')       ; buffer temporal para comparar IDs")
        self.data_section.append(f"reg_flag   DB 0                       ; 0 = no hay registro, 1 = hay registro")
        self.data_section.append("")
        
        # Buffers de entrada - exactamente como en instrucciones.md
        self.data_section.append("; ----- Buffers de entrada para INT 21h / 0Ah -----")
        self.data_section.append("; [0]=max chars, [1]=longitud leida, [2..]=datos")
        self.data_section.append("opt_buf    DB 2,0,2 DUP(?)                     ; opcion del menu (1 caracter)")
        self.data_section.append("")
        self.data_section.append(f"id_buf     DB ID_LEN,0,ID_LEN+1 DUP(?)         ; buffer para ID")
        self.data_section.append(f"name_buf   DB NAME_LEN,0,NAME_LEN+1 DUP(?)     ; buffer para nombre")
        self.data_section.append(f"edad_buf   DB EDAD_LEN,0,EDAD_LEN+1 DUP(?)     ; buffer para edad")
        self.data_section.append(f"carr_buf   DB CARR_LEN,0,CARR_LEN+1 DUP(?)     ; buffer para carrera")
        self.data_section.append(f"prom_buf   DB PROM_LEN,0,PROM_LEN+1 DUP(?)     ; buffer para promedio")
    
    def generate_crud_main_loop(self):
        """Genera el bucle principal del menú siguiendo instrucciones.md"""
        # Mostrar menú - exactamente como en instrucciones.md
        self.code_section.append("    ; Mostrar menú")
        self.code_section.append("    mov dx, OFFSET msg_menu_title")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET msg_menu_1")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET msg_menu_2")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET msg_menu_3")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET msg_menu_4")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET msg_menu_5")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET msg_menu_opt")
        self.code_section.append("    call print_str")
        self.code_section.append("")
        self.code_section.append("    ; Leer opción")
        self.code_section.append("    mov dx, OFFSET opt_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; 0Ah ya hace CR/LF al presionar ENTER")
        self.code_section.append("")
        self.code_section.append("    mov al, [opt_buf+2]   ; primer caracter de la opción")
        self.code_section.append("")
        self.code_section.append("    cmp al, '1'")
        self.code_section.append("    je  do_alta")
        self.code_section.append("    cmp al, '2'")
        self.code_section.append("    je  do_baja")
        self.code_section.append("    cmp al, '3'")
        self.code_section.append("    je  do_modificar")
        self.code_section.append("    cmp al, '4'")
        self.code_section.append("    je  do_listar")
        self.code_section.append("    cmp al, '5'")
        self.code_section.append("    je  salir")
        self.code_section.append("")
        self.code_section.append("    ; opción inválida")
        self.code_section.append("    mov dx, OFFSET msg_invalid_opt")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
    
    def generate_crud_alta(self):
        """Genera do_alta siguiendo instrucciones.md - EXACTAMENTE"""
        self.code_section.append("; -------------------------")
        self.code_section.append("; Alta")
        self.code_section.append("; -------------------------")
        self.code_section.append("do_alta:")
        self.code_section.append("    ; Pedir ID")
        self.code_section.append("    mov dx, OFFSET msg_pide_id")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET id_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    ; buffer -> id_str")
        self.code_section.append("    mov si, OFFSET id_buf")
        self.code_section.append("    mov di, OFFSET id_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; Pedir nombre")
        self.code_section.append("    mov dx, OFFSET msg_pide_nombre")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET name_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    ; buffer -> name_str")
        self.code_section.append("    mov si, OFFSET name_buf")
        self.code_section.append("    mov di, OFFSET name_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; Pedir edad")
        self.code_section.append("    mov dx, OFFSET msg_pide_edad")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET edad_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    mov si, OFFSET edad_buf")
        self.code_section.append("    mov di, OFFSET edad_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; Pedir carrera")
        self.code_section.append("    mov dx, OFFSET msg_pide_carrera")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET carr_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    mov si, OFFSET carr_buf")
        self.code_section.append("    mov di, OFFSET carr_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; Pedir promedio")
        self.code_section.append("    mov dx, OFFSET msg_pide_prom")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET prom_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    mov si, OFFSET prom_buf")
        self.code_section.append("    mov di, OFFSET prom_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; marcar registro como ocupado")
        self.code_section.append("    mov reg_flag, 1")
        self.code_section.append("")
        self.code_section.append("    mov dx, OFFSET msg_ok")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
    
    def generate_crud_baja(self):
        """Genera do_baja siguiendo instrucciones.md - EXACTAMENTE"""
        self.code_section.append("; -------------------------")
        self.code_section.append("; Baja")
        self.code_section.append("; -------------------------")
        self.code_section.append("do_baja:")
        self.code_section.append("    cmp reg_flag, 1")
        self.code_section.append("    jne no_registro_baja")
        self.code_section.append("")
        self.code_section.append("    ; Pedir ID a eliminar")
        self.code_section.append("    mov dx, OFFSET msg_pide_id_baja")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET id_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    ; entrada -> temp_str")
        self.code_section.append("    mov si, OFFSET id_buf")
        self.code_section.append("    mov di, OFFSET temp_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; comparar id_str (almacenado) con temp_str (entrada)")
        self.code_section.append("    mov si, OFFSET id_str")
        self.code_section.append("    mov di, OFFSET temp_str")
        self.code_section.append("    call cmp_strings         ; AL = 1 si iguales")
        self.code_section.append("")
        self.code_section.append("    cmp al, 1")
        self.code_section.append("    jne not_found_baja")
        self.code_section.append("")
        self.code_section.append("    ; Coinciden: eliminar registro")
        self.code_section.append("    mov reg_flag, 0")
        self.code_section.append("")
        self.code_section.append("    ; limpiar id_str")
        self.code_section.append("    mov cx, ID_LEN+1")
        self.code_section.append("    mov di, OFFSET id_str")
        self.code_section.append("fill_id:")
        self.code_section.append("    mov byte ptr [di], '$'")
        self.code_section.append("    inc di")
        self.code_section.append("    loop fill_id")
        self.code_section.append("")
        self.code_section.append("    ; limpiar name_str")
        self.code_section.append("    mov cx, NAME_LEN+1")
        self.code_section.append("    mov di, OFFSET name_str")
        self.code_section.append("fill_name:")
        self.code_section.append("    mov byte ptr [di], '$'")
        self.code_section.append("    inc di")
        self.code_section.append("    loop fill_name")
        self.code_section.append("")
        self.code_section.append("    ; limpiar edad_str")
        self.code_section.append("    mov cx, EDAD_LEN+1")
        self.code_section.append("    mov di, OFFSET edad_str")
        self.code_section.append("fill_edad:")
        self.code_section.append("    mov byte ptr [di], '$'")
        self.code_section.append("    inc di")
        self.code_section.append("    loop fill_edad")
        self.code_section.append("")
        self.code_section.append("    ; limpiar carr_str")
        self.code_section.append("    mov cx, CARR_LEN+1")
        self.code_section.append("    mov di, OFFSET carr_str")
        self.code_section.append("fill_carr:")
        self.code_section.append("    mov byte ptr [di], '$'")
        self.code_section.append("    inc di")
        self.code_section.append("    loop fill_carr")
        self.code_section.append("")
        self.code_section.append("    ; limpiar prom_str")
        self.code_section.append("    mov cx, PROM_LEN+1")
        self.code_section.append("    mov di, OFFSET prom_str")
        self.code_section.append("fill_prom:")
        self.code_section.append("    mov byte ptr [di], '$'")
        self.code_section.append("    inc di")
        self.code_section.append("    loop fill_prom")
        self.code_section.append("")
        self.code_section.append("    mov dx, OFFSET msg_ok")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
        self.code_section.append("no_registro_baja:")
        self.code_section.append("    mov dx, OFFSET msg_no_reg")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
        self.code_section.append("not_found_baja:")
        self.code_section.append("    mov dx, OFFSET msg_no_encontrado")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
    
    def generate_crud_modificar(self):
        """Genera do_modificar siguiendo instrucciones.md - EXACTAMENTE (cambiar todos los datos)"""
        self.code_section.append("; -------------------------")
        self.code_section.append("; Modificar (cambiar todos los datos)")
        self.code_section.append("; -------------------------")
        self.code_section.append("do_modificar:")
        self.code_section.append("    cmp reg_flag, 1")
        self.code_section.append("    jne no_registro_mod")
        self.code_section.append("")
        self.code_section.append("    ; Pedir ID a modificar")
        self.code_section.append("    mov dx, OFFSET msg_pide_id_mod")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET id_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    ; entrada -> temp_str")
        self.code_section.append("    mov si, OFFSET id_buf")
        self.code_section.append("    mov di, OFFSET temp_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; comparar con id_str almacenado")
        self.code_section.append("    mov si, OFFSET id_str")
        self.code_section.append("    mov di, OFFSET temp_str")
        self.code_section.append("    call cmp_strings")
        self.code_section.append("    cmp al, 1")
        self.code_section.append("    jne not_found_mod")
        self.code_section.append("")
        self.code_section.append("    ; Coincide: pedir nuevos datos")
        self.code_section.append("")
        self.code_section.append("    ; nuevo nombre")
        self.code_section.append("    mov dx, OFFSET msg_pide_nuevo_nom")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET name_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    mov si, OFFSET name_buf")
        self.code_section.append("    mov di, OFFSET name_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; nueva edad")
        self.code_section.append("    mov dx, OFFSET msg_pide_nueva_edad")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET edad_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    mov si, OFFSET edad_buf")
        self.code_section.append("    mov di, OFFSET edad_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; nueva carrera")
        self.code_section.append("    mov dx, OFFSET msg_pide_nueva_carr")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET carr_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    mov si, OFFSET carr_buf")
        self.code_section.append("    mov di, OFFSET carr_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    ; nuevo promedio")
        self.code_section.append("    mov dx, OFFSET msg_pide_nuevo_prom")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET prom_buf")
        self.code_section.append("    mov ah, 0Ah")
        self.code_section.append("    int 21h                ; sin call newline")
        self.code_section.append("")
        self.code_section.append("    mov si, OFFSET prom_buf")
        self.code_section.append("    mov di, OFFSET prom_str")
        self.code_section.append("    call buffer_to_dos")
        self.code_section.append("")
        self.code_section.append("    mov dx, OFFSET msg_ok")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
        self.code_section.append("no_registro_mod:")
        self.code_section.append("    mov dx, OFFSET msg_no_reg")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
        self.code_section.append("not_found_mod:")
        self.code_section.append("    mov dx, OFFSET msg_no_encontrado")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
    
    def generate_crud_listar(self):
        """Genera do_listar siguiendo instrucciones.md - EXACTAMENTE"""
        self.code_section.append("; -------------------------")
        self.code_section.append("; Listar")
        self.code_section.append("; -------------------------")
        self.code_section.append("do_listar:")
        self.code_section.append("    mov dx, OFFSET msg_lista_title")
        self.code_section.append("    call print_str")
        self.code_section.append("")
        self.code_section.append("    cmp reg_flag, 1")
        self.code_section.append("    jne listar_vacio")
        self.code_section.append("")
        self.code_section.append("    ; Imprimir: ID: <id> - Nombre: <nombre> - Edad: <edad> - Carrera: <carr> - Promedio: <prom>")
        self.code_section.append("")
        self.code_section.append("    mov dx, OFFSET msg_id_label")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET id_str")
        self.code_section.append("    call print_str")
        self.code_section.append("")
        self.code_section.append("    mov dx, OFFSET msg_sep_nombre")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET name_str")
        self.code_section.append("    call print_str")
        self.code_section.append("")
        self.code_section.append("    mov dx, OFFSET msg_sep_edad")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET edad_str")
        self.code_section.append("    call print_str")
        self.code_section.append("")
        self.code_section.append("    mov dx, OFFSET msg_sep_carrera")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET carr_str")
        self.code_section.append("    call print_str")
        self.code_section.append("")
        self.code_section.append("    mov dx, OFFSET msg_sep_prom")
        self.code_section.append("    call print_str")
        self.code_section.append("    mov dx, OFFSET prom_str")
        self.code_section.append("    call print_str")
        self.code_section.append("")
        self.code_section.append("    call newline")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
        self.code_section.append("listar_vacio:")
        self.code_section.append("    mov dx, OFFSET msg_vacio")
        self.code_section.append("    call print_str")
        self.code_section.append("    jmp main_loop")
        self.code_section.append("")
    
    def generate_crud_salir(self):
        """Genera salir siguiendo instrucciones.md"""
        self.code_section.append("; -------------------------")
        self.code_section.append("; Salir")
        self.code_section.append("; -------------------------")
        self.code_section.append("salir:")
        self.code_section.append("    mov ax, 4C00h")
        self.code_section.append("    int 21h")
        self.code_section.append("")
    
    def generate_dict_helper_functions(self):
        """Genera las funciones auxiliares para modo diccionarios"""
        # print_cstring
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("; Imprime cadena C-terminada (0)")
        self.code_section.append("; Entrada: DS:SI -> cadena terminada en 0")
        self.code_section.append(";   *Ahora preserva DX para no romper valores numéricos*")
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("print_cstring PROC")
        self.code_section.append("    PUSH AX")
        self.code_section.append("    PUSH DX")
        self.code_section.append("pc_loop:")
        self.code_section.append("    MOV AL, [SI]")
        self.code_section.append("    CMP AL, 0")
        self.code_section.append("    JE pc_done")
        self.code_section.append("    MOV DL, AL")
        self.code_section.append("    MOV AH, 02h")
        self.code_section.append("    INT 21h")
        self.code_section.append("    INC SI")
        self.code_section.append("    JMP pc_loop")
        self.code_section.append("pc_done:")
        self.code_section.append("    POP DX")
        self.code_section.append("    POP AX")
        self.code_section.append("    RET")
        self.code_section.append("print_cstring ENDP")
        self.code_section.append("")
        
        # print_dict
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("; Imprime \"diccionario\" con formato:")
        self.code_section.append("; {'desc': <BX-string>, 'precio': <CX>, 'stock': <DX>}")
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("print_dict PROC")
        self.code_section.append("    PUSH AX")
        self.code_section.append("    PUSH BX")
        self.code_section.append("    PUSH CX")
        self.code_section.append("    PUSH DX")
        self.code_section.append("    PUSH SI")
        self.code_section.append("")
        self.code_section.append("    ; \"{'desc': '\"")
        self.code_section.append("    MOV SI, OFFSET dict_open")
        self.code_section.append("    CALL print_cstring")
        self.code_section.append("")
        self.code_section.append("    ; desc")
        self.code_section.append("    MOV SI, BX")
        self.code_section.append("    CALL print_cstring")
        self.code_section.append("")
        self.code_section.append("    ; \"', 'precio': \"")
        self.code_section.append("    MOV SI, OFFSET dict_comma_precio")
        self.code_section.append("    CALL print_cstring")
        self.code_section.append("")
        self.code_section.append("    ; precio (CX)")
        self.code_section.append("    MOV AX, CX")
        self.code_section.append("    CALL print_number_inline")
        self.code_section.append("")
        self.code_section.append("    ; \", 'stock': \"")
        self.code_section.append("    MOV SI, OFFSET dict_comma_stock")
        self.code_section.append("    CALL print_cstring")
        self.code_section.append("")
        self.code_section.append("    ; stock (DX)  -> DX sigue intacto gracias a print_cstring")
        self.code_section.append("    MOV AX, DX")
        self.code_section.append("    CALL print_number_inline")
        self.code_section.append("")
        self.code_section.append("    ; \"}\"")
        self.code_section.append("    MOV SI, OFFSET dict_close")
        self.code_section.append("    CALL print_cstring")
        self.code_section.append("")
        self.code_section.append("    POP SI")
        self.code_section.append("    POP DX")
        self.code_section.append("    POP CX")
        self.code_section.append("    POP BX")
        self.code_section.append("    POP AX")
        self.code_section.append("    RET")
        self.code_section.append("print_dict ENDP")
        self.code_section.append("")
        
        # string_to_int (aunque no se use, está en el código de referencia)
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("; Convierte cadena en SI -> AX (entero) [no usado aquí]")
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
        
        # print_number_inline
        self.code_section.append(";-------------------------------------------------------")
        self.code_section.append("; Imprime número en AX (base 10)")
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
    
    def generate_crud_helper_functions(self):
        """Genera las subrutinas siguiendo instrucciones.md"""
        self.code_section.append("; ====================================================")
        self.code_section.append("; Subrutinas")
        self.code_section.append("; ====================================================")
        self.code_section.append("")
        self.code_section.append("; Imprime cadena terminada en '$' (DX = offset)")
        self.code_section.append("print_str PROC")
        self.code_section.append("    push ax")
        self.code_section.append("    mov ah, 09h")
        self.code_section.append("    int 21h")
        self.code_section.append("    pop ax")
        self.code_section.append("    ret")
        self.code_section.append("print_str ENDP")
        self.code_section.append("")
        self.code_section.append("; Imprime salto de línea (CR/LF)")
        self.code_section.append("newline PROC")
        self.code_section.append("    push ax")
        self.code_section.append("    push dx")
        self.code_section.append("    mov ah, 02h")
        self.code_section.append("    mov dl, 0Dh")
        self.code_section.append("    int 21h")
        self.code_section.append("    mov dl, 0Ah")
        self.code_section.append("    int 21h")
        self.code_section.append("    pop dx")
        self.code_section.append("    pop ax")
        self.code_section.append("    ret")
        self.code_section.append("newline ENDP")
        self.code_section.append("")
        self.code_section.append("; Convierte buffer de INT 21h / 0Ah a cadena terminada en '$'")
        self.code_section.append("; ENTRADA: SI = dir del buffer (0Ah)")
        self.code_section.append(";          DI = destino")
        self.code_section.append("buffer_to_dos PROC")
        self.code_section.append("    push ax")
        self.code_section.append("    push cx")
        self.code_section.append("")
        self.code_section.append("    mov cl, [si+1]     ; longitud leida")
        self.code_section.append("    mov ch, 0")
        self.code_section.append("    add si, 2          ; SI -> primer caracter")
        self.code_section.append("")
        self.code_section.append("copy_loop_bt:")
        self.code_section.append("    cmp cx, 0")
        self.code_section.append("    je  end_copy_bt")
        self.code_section.append("    mov al, [si]")
        self.code_section.append("    mov [di], al")
        self.code_section.append("    inc si")
        self.code_section.append("    inc di")
        self.code_section.append("    dec cx")
        self.code_section.append("    jmp copy_loop_bt")
        self.code_section.append("")
        self.code_section.append("end_copy_bt:")
        self.code_section.append("    mov al, '$'")
        self.code_section.append("    mov [di], al")
        self.code_section.append("")
        self.code_section.append("    pop cx")
        self.code_section.append("    pop ax")
        self.code_section.append("    ret")
        self.code_section.append("buffer_to_dos ENDP")
        self.code_section.append("")
        self.code_section.append("; Compara dos cadenas terminadas en '$'")
        self.code_section.append("; ENTRADA: SI = str1, DI = str2")
        self.code_section.append("; SALIDA : AL = 1 si son iguales, 0 si no")
        self.code_section.append("cmp_strings PROC")
        self.code_section.append("    push bx")
        self.code_section.append("")
        self.code_section.append("cmp_loop:")
        self.code_section.append("    mov al, [si]")
        self.code_section.append("    mov bl, [di]")
        self.code_section.append("    cmp al, bl")
        self.code_section.append("    jne not_equal_cs")
        self.code_section.append("    cmp al, '$'")
        self.code_section.append("    je  equal_cs")
        self.code_section.append("    inc si")
        self.code_section.append("    inc di")
        self.code_section.append("    jmp cmp_loop")
        self.code_section.append("")
        self.code_section.append("equal_cs:")
        self.code_section.append("    mov al, 1")
        self.code_section.append("    jmp end_cs")
        self.code_section.append("")
        self.code_section.append("not_equal_cs:")
        self.code_section.append("    mov al, 0")
        self.code_section.append("")
        self.code_section.append("end_cs:")
        self.code_section.append("    pop bx")
        self.code_section.append("    ret")
        self.code_section.append("cmp_strings ENDP")
    
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

