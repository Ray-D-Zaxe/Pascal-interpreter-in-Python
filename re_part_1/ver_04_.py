'''
Objectives::
1. [x] Extend the calculator to handle multiplication of two integers
2. [x] Extend the calculator to handle division of two integers
'''

'''
Token types::
- EOF (End-Of-File)
- INTEGER (Integers)

- MUL ('*' arithmatic operator)
- DIV ('/' arithmatic operator)
- PLUS ('+' binary arithmatic operator)
- MINUS ('-' binary arithmatic operator)
'''

INTEGER, EOF = 'INTEGER', 'EOF'
MUL, DIV, PLUS, MINUS = 'MUL', 'DIV', 'PLUS', 'MINUS'

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

class Interpreter(object):
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
        token = self.current_token
        self.eatToken(INTEGER)
        return token.value
    
    def term(self):
        result = self.factor()
        
        while self.current_token.type in (MUL, DIV):
            if self.current_token.type == MUL:
                self.eatToken(MUL)
                result *= self.factor()
            elif self.current_token.type == DIV:
                self.eatToken(DIV)
                result /= self.factor()
        
        return result

    def expr(self):
        result = self.term()
        
        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == PLUS:
                self.eatToken(PLUS)
                result += self.term()
            elif self.current_token.type == MINUS:
                self.eatToken(MINUS)
                result -= self.term()
        
        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
