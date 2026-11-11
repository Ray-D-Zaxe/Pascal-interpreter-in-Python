'''
Objectives::
- [] Modify the code to interpret expressions containing an arbitrary number of additions and subtractions,
    for example “9 - 5 + 3 + 11”
'''

'''
Token types::
- EOF (End-Of-File)
- INTEGER (Integers)
- PLUS ('+' binary arithmatic operator)
- MINUS ('-' binary arithmatic operator)
'''

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid Syntax!!!')

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

    def eatToken(self, expectedType):
        if self.current_token.type == expectedType:
            self.current_token = self.getNextToken()
        else:
            self.error()
    
    def term(self):
        token = self.current_token
        self.eatToken(INTEGER)
        return token.value

    def expr(self):
        self.current_token = self.getNextToken()
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
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
