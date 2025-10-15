"""
Analizador Semántico
Verifica que las variables estén declaradas antes de usarse y que los tipos sean compatibles
"""

from python_compiler import *


class SemanticError(Exception):
    """Error en el análisis semántico"""
    pass


class SemanticAnalyzer:
    """Analizador Semántico que verifica variables y tipos"""
    
    def __init__(self):
        self.symbol_table = {}  # {nombre_variable: {'type': tipo, 'initialized': bool, 'line': linea}}
        self.errors = []
        self.warnings = []
        self.current_scope = 'global'
    
    def error(self, message, line=0):
        """Registra un error semántico"""
        error_msg = f"Línea {line}: {message}" if line else message
        self.errors.append(error_msg)
    
    def warning(self, message, line=0):
        """Registra una advertencia"""
        warn_msg = f"Línea {line}: {message}" if line else message
        self.warnings.append(warn_msg)
    
    def infer_type(self, node):
        """Infiere el tipo de una expresión"""
        if isinstance(node, NumberNode):
            return 'float' if isinstance(node.value, float) else 'int'
        elif isinstance(node, StringNode):
            return 'str'
        elif isinstance(node, IdentifierNode):
            if node.name in self.symbol_table:
                return self.symbol_table[node.name]['type']
            else:
                return 'unknown'
        elif isinstance(node, BinaryOpNode):
            left_type = self.infer_type(node.left)
            right_type = self.infer_type(node.right)
            
            # Operaciones de comparación siempre devuelven bool
            if node.operator in ['==', '!=', '<', '>', '<=', '>=']:
                return 'bool'
            
            # Operaciones aritméticas
            if node.operator in ['+', '-', '*', '/', '%']:
                # Si alguno es float, el resultado es float
                if left_type == 'float' or right_type == 'float':
                    return 'float'
                # Si ambos son int, el resultado es int (excepto división)
                if left_type == 'int' and right_type == 'int':
                    return 'float' if node.operator == '/' else 'int'
                # Si uno es string y el operador es +, es concatenación
                if (left_type == 'str' or right_type == 'str') and node.operator == '+':
                    return 'str'
                return 'unknown'
        elif isinstance(node, ListNode):
            return 'list'
        elif isinstance(node, CallNode):
            if node.function == 'len':
                return 'int'
            elif node.function == 'range':
                return 'range'
            return 'unknown'
        
        return 'unknown'
    
    def check_type_compatibility(self, left_type, operator, right_type, line=0):
        """Verifica compatibilidad de tipos en una operación"""
        # Operadores aritméticos
        if operator in ['+', '-', '*', '/', '%']:
            # Suma de strings está permitida (concatenación)
            if operator == '+' and (left_type == 'str' or right_type == 'str'):
                if left_type != 'str' or right_type != 'str':
                    self.error(
                        f"No se puede concatenar {left_type} con {right_type}. "
                        f"Ambos deben ser strings.",
                        line
                    )
                    return False
                return True
            
            # Operaciones numéricas
            numeric_types = ['int', 'float']
            if left_type not in numeric_types:
                self.error(
                    f"Operando izquierdo de '{operator}' debe ser numérico, "
                    f"se encontró '{left_type}'",
                    line
                )
                return False
            if right_type not in numeric_types:
                self.error(
                    f"Operando derecho de '{operator}' debe ser numérico, "
                    f"se encontró '{right_type}'",
                    line
                )
                return False
            
            # Advertencia por división por cero si es literal
            if operator == '/' and right_type == 'int':
                self.warning("Posible división por cero", line)
            
            return True
        
        # Operadores de comparación
        if operator in ['==', '!=', '<', '>', '<=', '>=']:
            # Cualquier tipo se puede comparar con ==, !=
            if operator in ['==', '!=']:
                return True
            # <, >, <=, >= requieren tipos compatibles (números o strings)
            numeric_types = ['int', 'float']
            if (left_type in numeric_types and right_type in numeric_types) or \
               (left_type == 'str' and right_type == 'str'):
                return True
            else:
                self.error(
                    f"No se puede comparar '{left_type}' con '{right_type}' usando '{operator}'",
                    line
                )
                return False
        
        return True
    
    def analyze(self, ast):
        """Analiza el AST completo"""
        self.visit(ast)
        return len(self.errors) == 0
    
    def visit(self, node):
        """Visita un nodo del AST"""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Visita genérica"""
        pass
    
    def visit_ProgramNode(self, node):
        """Visita el programa"""
        for statement in node.statements:
            self.visit(statement)
    
    def visit_AssignmentNode(self, node):
        """Visita una asignación"""
        # Analizar la expresión del lado derecho
        self.visit(node.expression)
        
        # Inferir el tipo de la expresión
        expr_type = self.infer_type(node.expression)
        
        # Si la variable ya existe, verificar compatibilidad (advertencia)
        if node.identifier in self.symbol_table:
            old_type = self.symbol_table[node.identifier]['type']
            if old_type != expr_type and expr_type != 'unknown':
                self.warning(
                    f"Variable '{node.identifier}' cambia de tipo de '{old_type}' a '{expr_type}'",
                    node.line
                )
        
        # Registrar o actualizar variable en la tabla de símbolos
        self.symbol_table[node.identifier] = {
            'type': expr_type,
            'initialized': True,
            'line': node.line
        }
    
    def visit_PrintNode(self, node):
        """Visita un print"""
        self.visit(node.expression)
    
    def visit_IfNode(self, node):
        """Visita un condicional"""
        # Verificar condición
        self.visit(node.condition)
        cond_type = self.infer_type(node.condition)
        
        if cond_type not in ['bool', 'int', 'float', 'unknown']:
            self.warning(
                f"La condición del if es de tipo '{cond_type}', se esperaba un valor booleano",
                node.line
            )
        
        # Visitar bloques
        self.visit(node.then_block)
        for elif_cond, elif_block in node.elif_parts:
            self.visit(elif_cond)
            self.visit(elif_block)
        if node.else_block:
            self.visit(node.else_block)
    
    def visit_WhileNode(self, node):
        """Visita un bucle while"""
        self.visit(node.condition)
        cond_type = self.infer_type(node.condition)
        
        if cond_type not in ['bool', 'int', 'float', 'unknown']:
            self.warning(
                f"La condición del while es de tipo '{cond_type}', se esperaba un valor booleano",
                node.line
            )
        
        self.visit(node.block)
    
    def visit_ForNode(self, node):
        """Visita un bucle for"""
        # Verificar el iterable
        self.visit(node.iterable)
        iter_type = self.infer_type(node.iterable)
        
        if iter_type not in ['range', 'list', 'unknown']:
            self.error(
                f"El for requiere un iterable (range o lista), se encontró '{iter_type}'",
                node.line
            )
        
        # Registrar variable del iterador
        self.symbol_table[node.identifier] = {
            'type': 'int',
            'initialized': True,
            'line': node.line
        }
        
        self.visit(node.block)
    
    def visit_BinaryOpNode(self, node):
        """Visita una operación binaria"""
        # Visitar operandos
        self.visit(node.left)
        self.visit(node.right)
        
        # Obtener tipos
        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)
        
        # Verificar compatibilidad
        if left_type != 'unknown' and right_type != 'unknown':
            self.check_type_compatibility(left_type, node.operator, right_type, node.line)
    
    def visit_UnaryOpNode(self, node):
        """Visita una operación unaria"""
        self.visit(node.operand)
        operand_type = self.infer_type(node.operand)
        
        if node.operator == '-':
            if operand_type not in ['int', 'float', 'unknown']:
                self.error(
                    f"El operador '-' requiere un operando numérico, se encontró '{operand_type}'",
                    node.line
                )
    
    def visit_IdentifierNode(self, node):
        """Visita un identificador (uso de variable)"""
        if node.name not in self.symbol_table:
            self.error(
                f"Variable '{node.name}' no está declarada antes de usarse",
                node.line
            )
        elif not self.symbol_table[node.name]['initialized']:
            self.warning(
                f"Variable '{node.name}' podría no estar inicializada",
                node.line
            )
    
    def visit_NumberNode(self, node):
        """Visita un número"""
        pass
    
    def visit_StringNode(self, node):
        """Visita un string"""
        pass
    
    def visit_ListNode(self, node):
        """Visita una lista"""
        for element in node.elements:
            self.visit(element)
    
    def visit_IndexNode(self, node):
        """Visita un acceso por índice"""
        self.visit(node.list_expr)
        self.visit(node.index_expr)
        
        list_type = self.infer_type(node.list_expr)
        index_type = self.infer_type(node.index_expr)
        
        if list_type not in ['list', 'unknown']:
            self.error(
                f"El acceso por índice requiere una lista, se encontró '{list_type}'",
                node.line
            )
        
        if index_type not in ['int', 'unknown']:
            self.error(
                f"El índice debe ser un entero, se encontró '{index_type}'",
                node.line
            )
    
    def visit_CallNode(self, node):
        """Visita una llamada a función"""
        # Visitar argumentos
        for arg in node.args:
            self.visit(arg)
        
        # Verificar funciones específicas
        if node.function == 'range':
            if len(node.args) == 0:
                self.error("range() requiere al menos un argumento", 0)
            elif len(node.args) > 0:
                arg_type = self.infer_type(node.args[0])
                if arg_type not in ['int', 'unknown']:
                    self.error(
                        f"range() requiere un argumento entero, se encontró '{arg_type}'",
                        node.line
                    )
        elif node.function == 'len':
            if len(node.args) != 1:
                self.error("len() requiere exactamente un argumento", 0)
            else:
                arg_type = self.infer_type(node.args[0])
                if arg_type not in ['list', 'str', 'unknown']:
                    self.error(
                        f"len() requiere una lista o string, se encontró '{arg_type}'",
                        node.line
                    )
    
    def visit_BlockNode(self, node):
        """Visita un bloque de código"""
        for statement in node.statements:
            self.visit(statement)
    
    def get_report(self):
        """Genera un reporte del análisis semántico"""
        report = "ANÁLISIS SEMÁNTICO\n"
        report += "=" * 100 + "\n\n"
        
        # Tabla de símbolos
        report += "TABLA DE SÍMBOLOS\n"
        report += "-" * 100 + "\n"
        report += f"{'Variable':<20} {'Tipo':<15} {'Inicializada':<15} {'Línea':<10}\n"
        report += "-" * 100 + "\n"
        
        for name, info in self.symbol_table.items():
            report += f"{name:<20} {info['type']:<15} {'Sí' if info['initialized'] else 'No':<15} {info['line']:<10}\n"
        
        report += "\n"
        
        # Errores
        if self.errors:
            report += f"ERRORES SEMÁNTICOS ({len(self.errors)})\n"
            report += "-" * 100 + "\n"
            for i, error in enumerate(self.errors, 1):
                report += f"{i}. {error}\n"
            report += "\n"
        
        # Advertencias
        if self.warnings:
            report += f"ADVERTENCIAS ({len(self.warnings)})\n"
            report += "-" * 100 + "\n"
            for i, warning in enumerate(self.warnings, 1):
                report += f"{i}. {warning}\n"
            report += "\n"
        
        if not self.errors and not self.warnings:
            report += "[OK] No se encontraron errores ni advertencias semánticas\n"
        
        return report
