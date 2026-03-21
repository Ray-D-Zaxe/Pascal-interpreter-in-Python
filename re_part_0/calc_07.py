INTEGER, PLUS, MINUS, MUL, DIV, LPRN, RPRN, EOF = "INTEGER", "PLUS", "MINUS", "MUL", "DIV", "LPRN", "RPRN", "EOF"



class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"
    
    def __repr__(self):
        return self.__str__()



RESERVED_KEYWORD = {
    "BEGIN": Token("BEGIN", "BEGIN"),
    "END": Token("END", "END"),
}



class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def error(self):
        raise Exception("Invalid Characters!!!")
    
    def advance(self):
        self.pos += 1
        if (self.pos > (len(self.text) - 1)):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self):
        peek_pos = self.pos + 1
        if (peek_pos > (len(self.text) - 1)):
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while (self.current_char is not None and self.current_char.isspace()):
            self.advance()
    
    def integer(self):
        result = ""
        while (self.current_char is not None and self.current_char.isdigit()):
            result += self.current_char
            self.advance()
        return int(result)
    

    
    def _id(self):
        result = ""
        while (self.current_char is not None and self.current_char.isalnum()):
            result += self.current_char
            self.advance()
        
        token = RESERVED_KEYWORD.get(result, Token(ID, result))
        return token
    
    def get_next_token(self):
        while (self.current_char is not None):
            # For removal of space
            if (self.current_char.isspace()):
                self.skip_whitespace()
            # Let's play a game, keyword or variable...its an identifier
            if (self.current_char.isalnum()):
                return self._id()
            # Lets work on assignment
            if ((":" == self.current_char) and ("=" == self.peek())):
                self.advance()
                self.advance()
                return Token(ASSIGN, ":=")
            # What about semi colons???
            if (";" == self.current_char):
                self.advance()
                return Token(SEMI, ";")
            # And the DOT
            if ("." == self.current_char):
                self.advance()
                return Token(DOT, ".")
            # This is an integer
            if (self.current_char.isdigit()):
                return Token(INTEGER, self.integer())
            # This is for addition
            if ("+" == self.current_char):
                self.advance()
                return Token(PLUS, "+")
            # This is for subtraction
            if ("-" == self.current_char):
                self.advance()
                return Token(MINUS, "-")
            # This is for multiplication
            if ("*" == self.current_char):
                self.advance()
                return Token(MUL, "*")
            # This is for division
            if ("/" == self.current_char):
                self.advance()
                return Token(DIV, "/")
            # The left round bracket/paranthesis
            if ("(" == self.current_char):
                self.advance()
                return Token(LPRN, "(")
            # The right rounf bracket/paranthesis
            if (")" == self.current_char):
                self.advance()
                return Token(RPRN, ")")
            self.error()
        return Token(EOF, None)



class AST:
    pass



class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr



class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right



class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value



class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception("Invalid Syntex!!!")
    
    def eat(self, token_type):
        if (token_type == self.current_token.type):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        token = self.current_token
        if (INTEGER == token.type):
            self.eat(INTEGER)
            return Num(token)
        elif (PLUS == token.type):
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif (MINUS == token.type):
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif (LPRN == token.type):
            self.eat(LPRN)
            node = self.expr()
            self.eat(RPRN)
            return node
    
    def term(self):
        node = self.factor()
        while (self.current_token.type in (MUL, DIV)):
            token = self.current_token
            if (MUL == token.type):
                self.eat(MUL)
            else:
                self.eat(DIV)
            node = BinOp(left= node, op= token, right= self.factor())
        
        return node
    
    def expr(self):
        node = self.term()
        while (self.current_token.type in (PLUS, MINUS)):
            token = self.current_token
            if (PLUS == token.type):
                self.eat(PLUS)
            else:
                self.eat(MINUS)
            node = BinOp(left= node, op= token, right= self.term())
        return node
    
    def parse(self):
        return self.expr()



class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')



class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_UnaryOp(self, node):
        if (PLUS == node.op.type):
            return +self.visit(node.expr)
        elif (MINUS == node.op.type):
            return -self.visit(node.expr)
    
    def visit_BinOp(self, node):
        if (PLUS == node.op.type):
            return self.visit(node.left) + self.visit(node.right)
        elif (MINUS == node.op.type):
            return self.visit(node.left) - self.visit(node.right)
        elif (MUL == node.op.type):
            return self.visit(node.left) * self.visit(node.right)
        elif (DIV == node.op.type):
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
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
if __name__ == '__main__':
    main()
