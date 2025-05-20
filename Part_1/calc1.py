# variables representing the token types (kinda like data types???)
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'



# This is the token class
class Token(object):
    #this will initialize the token
    def __init__(tkn, type, value):
        tkn.type = type
        tkn.value = value
    # This will return the string representation of the token
    def __str__(tkn):
        return f"Token({tkn.type}, {tkn.value})"
    # This will return __str__ when the token is printed
    def __repr__(tkn):
        return tkn.__str__()



# This is the lexer/intepreter class
class Interpreter(object):
    

    # This will initilize the interpreter
    def __init__(intr, text):
        intr.text = text                # the input string
        intr.pos = 0                    # the current position in the input string
        intr.currunt_token = None       # the current token
    

    # This helps raise error exception
    def error(intr):
        raise Exception('Invalid syntax')
    

    # This will return the current character as token
    def get_next_token(intr):
        # Checks if we have reached the end of the input string
        if(intr.pos > len(intr.text) - 1):
            return Token(EOF, None)
        
        # Gets the current character
        current_char = intr.text[intr.pos]

        # If the current character is a digit, return an INTEGER token
        if current_char.isdigit():
            intr.pos += 1
            return Token(INTEGER, int(current_char))
        
        # If the current character is a '+', return a PLUS token
        if current_char == '+':
            intr.pos += 1
            return Token(PLUS, current_char)
        
        # If its none of the above then its prolly an error
        intr.error()
    

    # This will help us parse the input string
    def eat(intr, token_type):
        if intr.current_token.type == token_type:
            intr.current_token = intr.get_next_token()
        else:
            intr.error()
    

    #
    def expr(intr):
        # Lets start parsing the input string by getting the first token
        intr.current_token = intr.get_next_token()

        # We are expecting the first token to be an integer
        left = intr.current_token
        intr.eat(INTEGER)

        # We are expecting the second token to be a plus sign ('+')
        intr.eat(PLUS)

        # We are expecting the third token to be an integer
        right = intr.current_token
        intr.eat(INTEGER)

        # We have a left operand, an operator and a right operand
        # We can now perform the operation
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