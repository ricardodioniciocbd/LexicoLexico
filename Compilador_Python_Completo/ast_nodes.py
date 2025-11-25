"""
Abstract Syntax Tree (AST) Node Definitions
Defines all AST node types for MiniLang
"""


class ASTNode:
    """Base class for all AST nodes"""
    pass


# Program Structure
class ProgramNode(ASTNode):
    """Root node representing the entire program"""
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Program({len(self.statements)} statements)"


# Statements
class AssignmentNode(ASTNode):
    """Variable assignment: identifier = expression"""
    def __init__(self, identifier, expression, line=0):
        self.identifier = identifier
        self.expression = expression
        self.line = line
    
    def __repr__(self):
        return f"Assignment({self.identifier} = {self.expression})"


class PrintNode(ASTNode):
    """Print statement: print(expression)"""
    def __init__(self, expression, line=0):
        self.expression = expression
        self.line = line
    
    def __repr__(self):
        return f"Print({self.expression})"


class IfNode(ASTNode):
    """Conditional statement: if/elif/else"""
    def __init__(self, condition, then_block, elif_parts=None, else_block=None, line=0):
        self.condition = condition
        self.then_block = then_block
        self.elif_parts = elif_parts or []  # List of (condition, block) tuples
        self.else_block = else_block
        self.line = line
    
    def __repr__(self):
        return f"If(condition={self.condition}, elifs={len(self.elif_parts)}, has_else={self.else_block is not None})"


class WhileNode(ASTNode):
    """While loop: while condition: block"""
    def __init__(self, condition, block, line=0):
        self.condition = condition
        self.block = block
        self.line = line
    
    def __repr__(self):
        return f"While({self.condition})"


class ForNode(ASTNode):
    """For loop: for identifier in range(expression): block"""
    def __init__(self, identifier, range_expr, block, line=0):
        self.identifier = identifier
        self.range_expr = range_expr
        self.block = block
        self.line = line
    
    def __repr__(self):
        return f"For({self.identifier} in range({self.range_expr}))"


# Expressions
class BinaryOpNode(ASTNode):
    """Binary operation: left operator right"""
    def __init__(self, left, operator, right, line=0):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.operator} {self.right})"


class UnaryOpNode(ASTNode):
    """Unary operation: operator operand"""
    def __init__(self, operator, operand, line=0):
        self.operator = operator
        self.operand = operand
        self.line = line
    
    def __repr__(self):
        return f"UnaryOp({self.operator}{self.operand})"


class NumberNode(ASTNode):
    """Numeric literal"""
    def __init__(self, value, line=0):
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Number({self.value})"


class StringNode(ASTNode):
    """String literal"""
    def __init__(self, value, line=0):
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"String({repr(self.value)})"


class IdentifierNode(ASTNode):
    """Variable identifier"""
    def __init__(self, name, line=0):
        self.name = name
        self.line = line
    
    def __repr__(self):
        return f"Identifier({self.name})"


class BlockNode(ASTNode):
    """Block of statements (used in control structures)"""
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Block({len(self.statements)} statements)"
