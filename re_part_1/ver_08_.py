'''
Objectives::
1. [x] Lexer::
    1.1 [x] New tokens (BEGIN, END, DOT, ID, ASSIGN, SEMI).
    1.2 [x] New peek method.
    1.3 [x] New _id method.
    1.4 [x] Update getNextToken method.
2. [x] Parser::
    2.1 [x] New AST nodes (Compound, Assign, Var, NoOp)
    2.2 [x] New methods => (
            program, compound_statement, statement_list,
            statement, assigned_statement, variables, empty
        )
    2.3 [x] Update parse method.
    2.4 [x] Update factor method.
3. [x] Interpreter::
    3.1 [x] New methods => (
        visit_Compound, visit_Assign, visit_Var, visit_NoOp
    )
    3.2 [x] Create basic symbol table, GLOBAL_SCOPE.
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
- BEGIN (syntax)
- END (syntax)
- DOT (syntax)
- ID (syntax)
- ASSIGN (syntax)
- SEMI (syntax)
'''

INTEGER, EOF = 'INTEGER', 'EOF'
MUL, DIV, PLUS, MINUS = 'MUL', 'DIV', 'PLUS', 'MINUS'
LPARAN, RPARAN = '(', ')'

BEGIN, END = 'BEGIN', 'END'
DOT, ASSIGN, SEMI = '.', ':=', ';'
ID = 'ID'

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
    
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > (len(self.text) - 1):
            return None
        else:
            return self.text[peek_pos]

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
    
    RESERVED_KEYWORDS = {
        BEGIN: Token(BEGIN, BEGIN),
        END: Token(END, END),
    }
    
    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        
        token = self.RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def getNextToken(self):
        while self.current_char is not None:
            # Skipping all whitespace characters
            if self.current_char.isspace():
                self.skipWhitespace()
                continue
            
            # For reserved keywords and ids
            if self.current_char.isalpha():
                return self._id()
                            
            # For the assignment operator
            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ASSIGN)
                            
            # For termination operator
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')
                            
            # For dot operator
            if self.current_char == '.':
                self.advance()
                return Token(DOT, DOT)
                
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

class Compound(AST):
    # For a 'BEGIN ... END' block
    def __init__(self):
        super().__init__()
        self.children = []
    
class Assign(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right
    
class Var(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.value = token.value
    
class NoOp(AST):
    pass

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
        '''
        factor:: (PLUS | MINUS) factor
                | INTEGER
                | LPARAN expr RPARAN
                | variable
        '''
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
        else:
            node = self.variable()
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
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        
        return node
    
    def program(self):
        node = self.compound_statement()
        self.eatToken(DOT)
        return node
    
    def compound_statement(self):
        self.eatToken(BEGIN)
        nodes = self.statement_list()
        self.eatToken(END)
        
        root = Compound()
        for node in nodes:
            root.children.append(node)
        
        return root
    
    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type == SEMI:
            self.eatToken(SEMI)
            results.append(self.statement())
        
        if self.current_token.type == ID:
            self.error()
        
        return results
    
    def statement(self):
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        
        return node
    
    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        
        self.eatToken(ASSIGN)
        
        right = self.expr()
        node = Assign(left, token, right)
        return node
    
    def variable(self):
        node = Var(self.current_token)
        self.eatToken(ID)
        return node
    
    def empty(self):
        return NoOp()

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
        self.GLOBAL_SCOPE = {}
    
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
    
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_NoOp(self, node):
        pass
    
    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
    
    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val
    
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
