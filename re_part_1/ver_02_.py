'''
Objectives::
1. [x] Handle whitespace characters anywhere in the input string
2. [x] Consume multi-digit integers from the input
3. [x] Subtract two integers (currently it can only add integers)

Side note::
- Trailing spaces like in 'calc> 4 + 7 ' are not accepted.
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
        raise Exception('Error parsing input.')

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

    def expr(self):
        self.current_token = self.getNextToken()

        left = self.current_token
        self.eatToken(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eatToken(PLUS)
        else:
            self.eatToken(MINUS)

        right = self.current_token
        self.eatToken(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
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
