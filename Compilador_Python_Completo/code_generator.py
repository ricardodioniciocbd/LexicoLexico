"""
Code Generator Module
Generates intermediate code or target code from AST
"""

from ast_nodes import *


class CodeGenerator:
    """Generates three-address code from AST"""
    
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        """Generate a new temporary variable"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        """Generate a new label"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, instruction):
        """Emit a code instruction"""
        self.code.append(instruction)
    
    def generate(self, ast):
        """Main entry point for code generation"""
        self.visit(ast)
        return self.code
    
    def visit(self, node):
        """Dispatch to appropriate visitor method"""
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Default visitor"""
        raise Exception(f'No visit method for {node.__class__.__name__}')
    
    # Visitor methods
    
    def visit_ProgramNode(self, node):
        """Generate code for entire program"""
        self.emit("# MiniLang Compiled Code")
        self.emit("# Three-Address Code Representation")
        self.emit("")
        
        for statement in node.statements:
            self.visit(statement)
        
        self.emit("")
        self.emit("# End of program")
    
    def visit_AssignmentNode(self, node):
        """
        Semantic Action: Generate code to evaluate expression and store in variable
        """
        # Generate code for expression
        expr_result = self.visit(node.expression)
        
        # Store result in variable
        self.emit(f"{node.identifier} = {expr_result}")
        
        return node.identifier
    
    def visit_PrintNode(self, node):
        """
        Semantic Action: Generate code to evaluate expression and print
        """
        expr_result = self.visit(node.expression)
        self.emit(f"PRINT {expr_result}")
        return None
    
    def visit_IfNode(self, node):
        """
        Semantic Action: Generate conditional jump code
        """
        # Evaluate condition
        cond_result = self.visit(node.condition)
        
        # Labels
        else_label = self.new_label()
        end_label = self.new_label()
        
        # If condition is false, jump to else/end
        if node.elif_parts or node.else_block:
            self.emit(f"IF_FALSE {cond_result} GOTO {else_label}")
        else:
            self.emit(f"IF_FALSE {cond_result} GOTO {end_label}")
        
        # Then block
        for stmt in node.then_block.statements:
            self.visit(stmt)
        
        # Jump to end after then block
        if node.elif_parts or node.else_block:
            self.emit(f"GOTO {end_label}")
        
        # Elif parts
        for i, (elif_cond, elif_block) in enumerate(node.elif_parts):
            self.emit(f"{else_label}:")
            cond_result = self.visit(elif_cond)
            
            next_label = self.new_label()
            self.emit(f"IF_FALSE {cond_result} GOTO {next_label}")
            
            for stmt in elif_block.statements:
                self.visit(stmt)
            
            self.emit(f"GOTO {end_label}")
            else_label = next_label
        
        # Else block
        if node.else_block:
            self.emit(f"{else_label}:")
            for stmt in node.else_block.statements:
                self.visit(stmt)
        
        # End label
        self.emit(f"{end_label}:")
        return None
    
    def visit_WhileNode(self, node):
        """
        Semantic Action: Generate loop with condition check and back jump
        """
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Start of loop
        self.emit(f"{start_label}:")
        
        # Evaluate condition
        cond_result = self.visit(node.condition)
        self.emit(f"IF_FALSE {cond_result} GOTO {end_label}")
        
        # Loop body
        for stmt in node.block.statements:
            self.visit(stmt)
        
        # Jump back to start
        self.emit(f"GOTO {start_label}")
        
        # End of loop
        self.emit(f"{end_label}:")
        return None
    
    def visit_ForNode(self, node):
        """
        Semantic Action: Generate loop initialization, condition, increment
        """
        # Initialize loop variable
        range_result = self.visit(node.range_expr)
        self.emit(f"{node.identifier} = 0")
        
        # Labels
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Start of loop
        self.emit(f"{start_label}:")
        
        # Check condition
        temp = self.new_temp()
        self.emit(f"{temp} = {node.identifier} < {range_result}")
        self.emit(f"IF_FALSE {temp} GOTO {end_label}")
        
        # Loop body
        for stmt in node.block.statements:
            self.visit(stmt)
        
        # Increment
        temp2 = self.new_temp()
        self.emit(f"{temp2} = {node.identifier} + 1")
        self.emit(f"{node.identifier} = {temp2}")
        
        # Jump back
        self.emit(f"GOTO {start_label}")
        
        # End of loop
        self.emit(f"{end_label}:")
        return None
    
    def visit_BinaryOpNode(self, node):
        """
        Semantic Action: Generate code for binary operation
        """
        left_result = self.visit(node.left)
        right_result = self.visit(node.right)
        
        temp = self.new_temp()
        self.emit(f"{temp} = {left_result} {node.operator} {right_result}")
        
        return temp
    
    def visit_UnaryOpNode(self, node):
        """Generate code for unary operation"""
        operand_result = self.visit(node.operand)
        
        temp = self.new_temp()
        self.emit(f"{temp} = {node.operator}{operand_result}")
        
        return temp
    
    def visit_NumberNode(self, node):
        """Return number literal"""
        return str(node.value)
    
    def visit_StringNode(self, node):
        """Return string literal"""
        return f'"{node.value}"'
    
    def visit_IdentifierNode(self, node):
        """Return variable name"""
        return node.name
    
    def visit_BlockNode(self, node):
        """Visit block statements"""
        for stmt in node.statements:
            self.visit(stmt)
        return None
    
    def get_code_as_string(self):
        """Get generated code as formatted string"""
        return '\n'.join(self.code)
