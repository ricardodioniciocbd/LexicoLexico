"""
Semantic Analyzer Module
Performs semantic analysis including type checking and symbol table management
"""

from ast_nodes import *


class SemanticError(Exception):
    """Exception raised for semantic errors"""
    pass


class SymbolTable:
    """Symbol table for tracking variables and their types"""
    
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
    
    def define(self, name, var_type, value=None):
        """Define a new variable in current scope"""
        self.symbols[name] = {
            'type': var_type,
            'value': value,
            'initialized': value is not None
        }
    
    def lookup(self, name):
        """Look up a variable in current or parent scopes"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        return None
    
    def update(self, name, var_type=None, value=None):
        """Update an existing variable"""
        if name in self.symbols:
            if var_type:
                self.symbols[name]['type'] = var_type
            if value is not None:
                self.symbols[name]['value'] = value
                self.symbols[name]['initialized'] = True
        elif self.parent:
            self.parent.update(name, var_type, value)
    
    def exists(self, name):
        """Check if variable exists in any scope"""
        return self.lookup(name) is not None


class SemanticAnalyzer:
    """Performs semantic analysis on AST"""
    
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.errors = []
        self.warnings = []
    
    def error(self, message, line=0):
        """Record a semantic error"""
        error_msg = f"Semantic Error at line {line}: {message}"
        self.errors.append(error_msg)
    
    def warning(self, message, line=0):
        """Record a semantic warning"""
        warning_msg = f"Warning at line {line}: {message}"
        self.warnings.append(warning_msg)
    
    def enter_scope(self):
        """Enter a new scope (e.g., for blocks)"""
        self.current_scope = SymbolTable(parent=self.current_scope)
    
    def exit_scope(self):
        """Exit current scope"""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def analyze(self, ast):
        """Main entry point for semantic analysis"""
        self.visit(ast)
        return len(self.errors) == 0
    
    def visit(self, node):
        """Dispatch to appropriate visitor method"""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Default visitor for unknown node types"""
        raise Exception(f'No visit method for {node.__class__.__name__}')
    
    # Visitor methods for each AST node type
    
    def visit_ProgramNode(self, node):
        """Visit program root node"""
        for statement in node.statements:
            self.visit(statement)
    
    def visit_AssignmentNode(self, node):
        """
        Semantic Action: Add/update variable in symbol table, infer type
        """
        # Evaluate expression type
        expr_type = self.visit(node.expression)
        
        # Check if variable already exists
        if self.current_scope.exists(node.identifier):
            # Update existing variable (dynamic typing allows type change)
            self.current_scope.update(node.identifier, expr_type)
        else:
            # Define new variable
            self.current_scope.define(node.identifier, expr_type)
        
        return expr_type
    
    def visit_PrintNode(self, node):
        """Visit print statement"""
        expr_type = self.visit(node.expression)
        return None
    
    def visit_IfNode(self, node):
        """
        Semantic Action: Verify condition is valid, analyze blocks in new scopes
        """
        # Check condition
        cond_type = self.visit(node.condition)
        
        # Analyze then block
        self.enter_scope()
        for stmt in node.then_block.statements:
            self.visit(stmt)
        self.exit_scope()
        
        # Analyze elif blocks
        for elif_cond, elif_block in node.elif_parts:
            self.visit(elif_cond)
            self.enter_scope()
            for stmt in elif_block.statements:
                self.visit(stmt)
            self.exit_scope()
        
        # Analyze else block
        if node.else_block:
            self.enter_scope()
            for stmt in node.else_block.statements:
                self.visit(stmt)
            self.exit_scope()
        
        return None
    
    def visit_WhileNode(self, node):
        """
        Semantic Action: Verify condition, analyze block in new scope
        """
        # Check condition
        cond_type = self.visit(node.condition)
        
        # Analyze block
        self.enter_scope()
        for stmt in node.block.statements:
            self.visit(stmt)
        self.exit_scope()
        
        return None
    
    def visit_ForNode(self, node):
        """
        Semantic Action: Verify range is numeric, define loop variable, analyze block
        """
        # Check range expression is numeric
        range_type = self.visit(node.range_expr)
        if range_type not in ('int', 'float', 'number'):
            self.error(f"Range expression must be numeric, got {range_type}", node.line)
        
        # Enter new scope and define loop variable
        self.enter_scope()
        self.current_scope.define(node.identifier, 'int')
        
        # Analyze block
        for stmt in node.block.statements:
            self.visit(stmt)
        
        self.exit_scope()
        return None
    
    def visit_BinaryOpNode(self, node):
        """
        Semantic Action: Type check operands, determine result type
        """
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Arithmetic operators
        if node.operator in ('+', '-', '*', '/'):
            # String concatenation with +
            if node.operator == '+' and left_type == 'string' and right_type == 'string':
                return 'string'
            
            # Numeric operations
            if left_type in ('int', 'float', 'number') and right_type in ('int', 'float', 'number'):
                # Result is float if either operand is float
                if left_type == 'float' or right_type == 'float':
                    return 'float'
                return 'int'
            
            # Type error
            self.error(
                f"Type mismatch in operation: {left_type} {node.operator} {right_type}",
                node.line
            )
            return 'error'
        
        # Comparison operators
        elif node.operator in ('==', '!=', '<', '>', '<=', '>='):
            # Can compare same types
            if left_type == right_type:
                return 'bool'
            # Can compare numeric types
            if left_type in ('int', 'float', 'number') and right_type in ('int', 'float', 'number'):
                return 'bool'
            
            self.warning(
                f"Comparing different types: {left_type} {node.operator} {right_type}",
                node.line
            )
            return 'bool'
        
        return 'unknown'
    
    def visit_UnaryOpNode(self, node):
        """Visit unary operation"""
        operand_type = self.visit(node.operand)
        
        if node.operator == '-':
            if operand_type in ('int', 'float', 'number'):
                return operand_type
            else:
                self.error(f"Cannot negate non-numeric type: {operand_type}", node.line)
                return 'error'
        
        return 'unknown'
    
    def visit_NumberNode(self, node):
        """
        Semantic Action: Return numeric type
        """
        if isinstance(node.value, float):
            return 'float'
        return 'int'
    
    def visit_StringNode(self, node):
        """
        Semantic Action: Return string type
        """
        return 'string'
    
    def visit_IdentifierNode(self, node):
        """
        Semantic Action: Verify variable is declared, return its type
        """
        symbol = self.current_scope.lookup(node.name)
        
        if symbol is None:
            self.error(f"Undefined variable: '{node.name}'", node.line)
            return 'error'
        
        if not symbol['initialized']:
            self.warning(f"Variable '{node.name}' may not be initialized", node.line)
        
        return symbol['type']
    
    def visit_BlockNode(self, node):
        """Visit block of statements"""
        for stmt in node.statements:
            self.visit(stmt)
        return None
    
    def get_symbol_table(self):
        """Get the global symbol table for display"""
        return self.global_scope.symbols
