'''
Token types::
- EOF (End-Of-File)
- INTEGER (Integers)
- PLUS ('+' binary operator)
'''

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

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

    def error(self):
        raise Exception('Error parsing input.')

    def getNextToken(self):
        text = self.text

        if self.pos > (len(text) - 1):
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char == '+':
            self.pos += 1
            return Token(PLUS, '+')
        elif current_char.isdigit():
            self.pos += 1
            return Token(INTEGER, int(current_char))

        self.error()

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
        self.eatToken(PLUS)

        right = self.current_token
        self.eatToken(INTEGER)

        result = left.value + right.value
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
