INTEGER, PLUS, MINUS, MUL, DIV, LPARN, RPARN, EOF = "INTEGER", "PLUS", "MINUS", "MUL", "DIV", "LPRAN", "RPRAN", "EOF"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"
    
    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def error(self):
        raise Exception("Invalid Syntax")
    
    def advance(self):
        self.pos += 1
        if (self.pos > (len(self.text) - 1)):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        while (self.current_char is not None and self.current_char.isspace()):
            self.advance()
    
    def integer(self):
        result = ""
        while (self.current_char is not None and self.current_char.isdigit()):
            result += self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        while (self.current_char is not None):
            if self.current_char.isspace():
                self.skip_whitespace()
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if "+" == self.current_char:
                self.advance()
                return Token(PLUS, "+")
            if "-" == self.current_char:
                self.advance()
                return Token(MINUS, "-")
            if "*" == self.current_char:
                self.advance()
                return Token(MUL, "*")
            if "/" == self.current_char:
                self.advance()
                return Token(DIV, "/")
            if "(" == self.current_char:
                self.advance()
                return Token(LPARN, "(")
            if ")" == self.current_char:
                self.advance()
                return Token(RPARN, ")")
            self.error()
        return Token(EOF, None)


class Interpreter:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        if (token_type == self.current_token.type):
            self.current_token = self.lexer.get_next_token()
        else:
            self.lexer.error()
    
    def factor(self):
        token = self.current_token
        if (INTEGER == token.type):
            self.eat(INTEGER)
            return token.value
        if (LPARN == token.type):
            self.eat(LPARN)
            result = self.expr()
            self.eat(RPARN)
            return result
    
    def term(self):
        value = self.factor()
        while (self.current_token.type in (MUL, DIV)):
            if (MUL == self.current_token.type):
                self.eat(MUL)
                value *= self.factor()
            else:
                self.eat(DIV)
                value /= self.factor()
        return value
    
    def expr(self):
        result = self.term()
        while (self.current_token.type in (PLUS, MINUS)):
            if (PLUS == self.current_token.type):
                self.eat(PLUS)
                result += self.term()
            else:
                self.eat(MINUS)
                result -= self.term()
        return result


def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)



if __name__ == "__main__":
    main()