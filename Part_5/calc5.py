INTEGER, PLUS, MINUS, MUL, DIV, EOF = "INTEGER", "PLUS", "MINUS", "MUL", "DIV", "EOF"



class Token:
    def __init__(tkn, type, value):
        tkn.type = type
        tkn.value = value
    
    def __str__(tkn):
        return f"Token({tkn.type}, {tkn.value})"
    
    def __repr__(tkn):
        return tkn.__str__()



class Lexer:
    def __init__(lxr, text):
        lxr.text = text
        lxr.pos = 0
        lxr.current_char = lxr.text[lxr.pos]
        lxr.current_token = None
    
    def error(lxr):
        raise Exception("Invalid Syntax!!!")
    
    def advance(lxr):
        lxr.pos += 1
        if lxr.pos > len(lxr.text) - 1:
            lxr.current_char = None
        else:
            lxr.current_char = lxr.text[lxr.pos]
    
    def skip_whitespace(lxr):
        while lxr.current_char is not None and lxr.current_char.isspace():
            lxr.advance()
    
    def integer(lxr):
        result = ""
        while lxr.current_char is not None and lxr.current_char.isdigit():
            result += lxr.current_char
            lxr.advance()
        return int(result)
    
    def get_next_token(lxr):
        while lxr.current_char is not None:
            if lxr.current_char.isspace():
                lxr.skip_whitespace()
                continue
            if lxr.current_char.isdigit():
                return Token(INTEGER, lxr.integer())
            if lxr.current_char == "+":
                lxr.advance()
                return Token(PLUS, "+")
            if lxr.current_char == "-":
                lxr.advance()
                return Token(MINUS, "-")
            if lxr.current_char == "*":
                lxr.advance()
                return Token(MUL, "*")
            if lxr.current_char == "/":
                lxr.advance()
                return Token(DIV, "/")
            lxr.error()
        return Token(EOF, None)



class Interpreter:
    def __init__(intr, text):
        intr.lexer = Lexer(text)
        intr.current_token = intr.lexer.get_next_token()
    
    def eat(intr, token_type):
        if intr.current_token.type == token_type:
            intr.current_token = intr.lexer.get_next_token()
        else:
            intr.lexer.error()
    
    def factor(intr):
        token = intr.current_token
        intr.eat(INTEGER)
        return token.value

    def term(intr):
        value = intr.factor()
        while intr.current_token.type in (MUL, DIV):
            if intr.current_token.type == MUL:
                intr.eat(MUL)
                value *= intr.factor()
            if intr.current_token.type == DIV:
                intr.eat(DIV)
                value /= intr.factor()
        return value
    
    def expr(intr):
        result = intr.term()
        
        while intr.current_token.type in (PLUS, MINUS):
            if intr.current_token.type == PLUS:
                intr.eat(PLUS)
                result += intr.term()
            if intr.current_token.type == MINUS:
                intr.eat(MINUS)
                result -= intr.term()
        
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