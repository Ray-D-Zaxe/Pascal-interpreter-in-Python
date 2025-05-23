# variables representing the token types (kinda like data types???)
INTEGER, PLUS, MINUS, EOF = "INTEGER", "PLUS", "MINUS", "EOF"



# This is the token class
class Token(object):
    # Initilizes the token type and value
    def __init__(tkn, type, value):
        tkn.type = type
        tkn.value = value
    

    # String representation of the token
    def __str__(tkn):
        return f"Token({tkn.type}, {tkn.value})"
    

    # Returns __str__()
    def __repr__(tkn):
        return tkn.__str__()



# The intepreter/lexer class
class Interpreter(object):
    # Initilizes the text, pos, current_token, current_char
    def __init__(intr, text):
        intr.text = text
        intr.pos = 0
        intr.currunt_token = None
        intr.current_char = intr.text[intr.pos]
    

    # Helps raise error
    def error(intr):
        raise Exception("Invalid Syntax")
    
    
    # This function moves the position to the next character of the input string 
    def advance(intr):
        intr.pos += 1
        
        # Checks if we are at the end of the input string
        if intr.pos > len(intr.text) - 1:
            intr.current_char = None
        else:
            intr.current_char = intr.text[intr.pos]
    

    # This function helps skip all the whitespaces
    def skip_whitespace(intr):
        while intr.current_char is not None and intr.current_char.isspace():
            intr.advance()
    
    
    # This function helps tokenize multi-digit integers in the input string
    def integer(intr):
        result = ''
        
        # we keep concatinating integer-strings as long as the next character is also an integer
        while intr.current_char is not None and intr.current_char.isdigit():
            result += intr.current_char
            intr.advance()
        
        # we then return the integer
        return int(result)
    

    # This function helps get the next token
    def get_next_token(intr): 
        while intr.current_char is not None:
            # Checks to skip whitespaces
            if intr.current_char.isspace():
                intr.skip_whitespace()
                continue
            
            # Returns the integer token
            if intr.current_char.isdigit():
                return Token(INTEGER, intr.integer())
            
            # Returns the plus token and advances the current_char
            if intr.current_char == '+':
                intr.advance()
                return Token(PLUS, "+")
            
            # Returns the minus token and advances the current_char
            if intr.current_char == '-':
                intr.advance()
                return Token(MINUS, "-")
            
            # Returns error if none of the conditions are met !!!
            intr.error()
        
        # Only executes this when the input string is exhausted or if there was no input string to begin with
        return Token(EOF, None)
    
    
    # This function checks and consumes the current token if it matches the given token type
    def eat(intr, token_type):
        if intr.current_token.type == token_type:
            intr.current_token = intr.get_next_token()
        else:
            intr.error()
    

    # This function is responsible for the actual execution
    def expr(intr):
        # Initilizes the current token
        intr.current_token = intr.get_next_token()

        # Takes the first integer operand token
        left = intr.current_token
        intr.eat(INTEGER)

        # Takes the operation token
        op = intr.current_token
        if op.type == PLUS:
            intr.eat(PLUS)
        else:
            intr.eat(MINUS)
        
        # Takes the second integer operand token
        right = intr.current_token
        intr.eat(INTEGER)

        # Returns the appropriate result
        if op.type == PLUS:
            return left.value + right.value
        else:
            return left.value - right.value



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
