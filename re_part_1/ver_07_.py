'''
Objectives::
1. [x] Add a new UnaryOp AST node class
2. [x] Extend the parser to generate an AST with UnaryOp nodes
3. [ ] Extend the interpreter and add a new visit_UnaryOp method
    to interpret unary operators
'''

'''
Token types::
- EOF (End-Of-File)
- INTEGER (Integers)

- MUL ('*' arithmatic operator)
- DIV ('/' arithmatic operator)
- PLUS ('+' binary arithmatic operator)
- MINUS ('-' binary arithmatic operator)
- LPARAN ('(' Left-Paranthesis)
- RPARAN (')' Right-Paranthesis)
'''

INTEGER, EOF = 'INTEGER', 'EOF'
MUL, DIV, PLUS, MINUS = 'MUL', 'DIV', 'PLUS', 'MINUS'
LPARAN, RPARAN = '(', ')'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid Character!!!')

    def advance(self):
        self.pos += 1
        if self.pos > (len(self.text) - 1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skipWhitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def getNextToken(self):
        while self.current_char is not None:
            # Skipping all whitespace characters
            if self.current_char.isspace():
                self.skipWhitespace()

            # For integer values
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            # For Left-Paranthesis '('
            if self.current_char == '(':
                self.advance()
                return Token(LPARAN, '(')
            
            # For Right-Paranthesis ')'
            if self.current_char == ')':
                self.advance()
                return Token(RPARAN, ')')
            
            # For Multiplication (*) operator
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            # For Division (/) operator
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            # For Plus (+) operator
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            # For Minus (-) operator
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            # If the current_char value is nither specified above nor is None
            self.error()

        # If the current_char value is None, i.e, it's the end of file.
        return Token(EOF, None)

class AST(object):
    pass

class UnaryOp(AST):
    def __init__(self, op, expr):
        super().__init__()
        self.token = self.op = op
        self.expr = expr

class BinOp(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.value = token.value

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.getNextToken()
        
    def error(self):
        raise Exception('Invalid Syntax!!!')
    
    def eatToken(self, expectedType):
        if self.current_token.type == expectedType:
            self.current_token = self.lexer.getNextToken()
        else:
            self.error()
    
    def factor(self):
        # factor:: (PLUS | MINUS) factor | INTEGER | LPARAN expr RPARAN
        token = self.current_token
        
        if token.type == PLUS:
            self.eatToken(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eatToken(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eatToken(INTEGER)
            return Num(token)
        elif token.type == LPARAN:
            self.eatToken(LPARAN)
            node = self.expr()
            self.eatToken(RPARAN)
            return node
    
    def term(self):
        # term:: factor | factor (MUL | DIV) factor
        node = self.factor()
        
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eatToken(MUL)
            elif token.type == DIV:
                self.eatToken(DIV)
            
            node = BinOp(node, token, self.factor())
        
        return node

    def expr(self):
        # expr:: term | term (PLUS | MINUS) term
        node = self.term()
        
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eatToken(PLUS)
            elif token.type == MINUS:
                self.eatToken(MINUS)

            node = BinOp(node, token, self.term())
            
        return node
    
    def parse(self):
        return self.expr()

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser
    
    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)
        
    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
    
    def visit_Num(self, node):
        return node.value
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    while True:
        try:
            text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue
        
        # Responsible for individual tokens.
        lexer = Lexer(text)
        
        # Responsible for creating an AST from said tokens.
        parser = Parser(lexer)
        
        # Responsible for traversing the AST while operating on it's values.
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()
