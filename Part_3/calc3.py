INTEGER, PLUS, MINUS, EOF = "INTEGER", "PLUS", "MINUS", "EOF"



class Token(object):
    def __init__(tkn, type, value):
        tkn.type = type
        tkn.value = value
    
    
    def __str__(tkn):
        return f"Token({tkn.type}, {tkn.value})"
    
    
    def __repr__(tkn):
        return tkn.__str__()



class Interpreter(object):
    def __init__(intr, text):
        intr.text = text
        intr.pos = 0
        intr.current_char = intr.text[intr.pos]
        intr.current_token = None
    
    
    def error(intr):
        raise Exception("Invalid Syntax!!!")
    
    
    def advance(intr):
        intr.pos += 1
        if intr.pos > len(intr.text) - 1:
            intr.current_char = None
        else:
            intr.current_char = intr.text[intr.pos]
    
    
    def skip_whitespace(intr):
        while intr.current_char is not None and intr.current_char.isspace():
            intr.advance()
    
    
    def integer(intr):
        result = ""
        
        while intr.current_char is not None and intr.current_char.isdigit():
            result += intr.current_char
            intr.advance()
        
        return int(result)
    
    
    def get_next_token(intr):
        while intr.current_char is not None:
            if intr.current_char.isspace():
                intr.skip_whitespace()
                continue
            
            if intr.current_char.isdigit():
                return Token(INTEGER, intr.integer())
            
            if intr.current_char == "+":
                intr.advance()
                return Token(PLUS, "+")
            
            if intr.current_char == "-":
                intr.advance()
                return Token(MINUS, "-")
            
            intr.error()
        
        return Token(EOF, None)
    
    
    def eat(intr, token_type):
        
        if intr.current_token.type == token_type:
            intr.current_token = intr.get_next_token()
        else:
            intr.error()
    
    
    def term(intr):
        value = intr.current_token.value
        intr.eat(INTEGER)
        return value


    def expr(intr):
        intr.current_token = intr.get_next_token()
        
        result = intr.term()
        
        while intr.current_token.type in (PLUS, MINUS):
            if intr.current_token.type == PLUS:
                intr.eat(PLUS)
                result += intr.term()
            else:
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
