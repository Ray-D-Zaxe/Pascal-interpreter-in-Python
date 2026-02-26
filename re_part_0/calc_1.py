INTEGER, EOF, PLUS = "INTEGER", "EOF", "PLUS"

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"
    
    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(program, text):
        program.text = text
        program.position = 0
        program.current_token = None
    
    def error():
        raise Exception('Invalid SYNTAX')
    
    def get_next_token(program):
        if (program.position > len(program.text) -1):
            return Token(EOF, None)
        
        current_character = program.text[program.position]

        if (current_character.isdigit()):
            program.position += 1
            return Token(INTEGER, int(current_character))
        
        if (current_character == '+'):
            program.position += 1
            return Token(PLUS, current_character)
        
        program.error()

    def eat(program, token_type):
        if(program.current_token.type == token_type):
            program.current_token = program.get_next_token()
        else:
            program.error()
    
    def expr(program):
        program.current_token = program.get_next_token()

        left = program.current_token
        program.eat(INTEGER)

        operation = program.current_token
        program.eat(PLUS)

        right = program.current_token
        program.eat(INTEGER)

        return left.value + right.value


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