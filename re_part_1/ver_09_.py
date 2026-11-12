"""
Objectives::
1. [x] Lexer
    1.1 [x] New tokens
    1.2 [x] New and updated reserved keywords
    1.3 [x] New skip_comment method to handle Pascal comments
    1.4 [x] Rename the integer method and make some changes to the method itself
    1.5 [x] Update the get_next_token method to return new tokens
2. [x] Parser
    2.1 [x] New AST nodes: Program, Block, VarDecl, Type
    2.2 [x] New methods corresponding to new grammar rules: block, declarations,
        variable_declaration, and type_spec.
    2.3 [x] Updates to the existing parser methods: program, term, and factor
3. [-] Interpreter (Adding new methods)
    - [-] visit_Program, visit_Block, visit_VarDecl, visit_Type
"""

INTEGER = "INTEGER"
REAL = "REAL"
INTEGER_CONST = "INTEGER_CONST"
REAL_CONST = "REAL_CONST"
PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
INTEGER_DIV = "INTEGER_DIV"
FLOAT_DIV = "FLOAT_DIV"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
ID = "ID"
ASSIGN = "ASSIGN"
BEGIN = "BEGIN"
END = "END"
SEMI = "SEMI"
DOT = "DOT"
PROGRAM = "PROGRAM"
VAR = "VAR"
COLON = "COLON"
COMMA = "COMMA"
EOF = "EOF"


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    "PROGRAM": Token("PROGRAM", "PROGRAM"),
    "VAR": Token("VAR", "VAR"),
    "DIV": Token("INTEGER_DIV", "DIV"),
    "INTEGER": Token("INTEGER", "INTEGER"),
    "REAL": Token("REAL", "REAL"),
    "BEGIN": Token("BEGIN", "BEGIN"),
    "END": Token("END", "END"),
}


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Lexer says:: Invalid Character!!!")

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > (len(self.text) - 1):
            return None
        else:
            return self.text[peek_pos]

    def advance(self):
        self.pos += 1
        if self.pos > (len(self.text) - 1):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skipWhitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != "}":
            self.advance()

        # Skipping the '}' character as well
        self.advance()

    def number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == ".":
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            token = Token(REAL_CONST, float(result))
        else:
            token = Token(INTEGER_CONST, int(result))

        return token

    def _id(self):
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def getNextToken(self):
        while self.current_char is not None:
            # Skipping all whitespace characters
            if self.current_char.isspace():
                self.skipWhitespace()
                continue

            # Skipping comments
            if self.current_char == "{":
                self.advance()
                self.skip_comment()
                continue

            # For reserved keywords and ids
            if self.current_char.isalpha():
                return self._id()

            # For integer values
            if self.current_char.isdigit():
                return self.number()

            # For the assignment operator
            if self.current_char == ":" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(ASSIGN, ":=")

            # For termination operator
            if self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")

            # For colon operator
            if self.current_char == ":":
                self.advance()
                return Token(COLON, ":")

            # For comma operator
            if self.current_char == ",":
                self.advance()
                return Token(COMMA, ",")

            # For Plus (+) operator
            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            # For Minus (-) operator
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            # For Multiplication (*) operator
            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            # For Division (/) operator
            if self.current_char == "/":
                self.advance()
                return Token(FLOAT_DIV, "/")

            # For Left-Paranthesis '('
            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            # For Right-Paranthesis ')'
            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            # For dot operator
            if self.current_char == ".":
                self.advance()
                return Token(DOT, DOT)

            # If the current_char value is nither specified above nor is None
            self.error()

        # If the current_char value is None, i.e, it's the end of file.
        return Token(EOF, None)


class AST(object):
    pass


class UnaryOp(AST):
    def __init__(self, op, expr):
        super().__init__()
        self.token = self.op = op
        self.expr = expr


class BinOp(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.value = token.value


class Compound(AST):
    # For a 'BEGIN ... END' block
    def __init__(self):
        super().__init__()
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Program(AST):
    def __init__(self, name, block):
        super().__init__()
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        super().__init__()
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDecl(AST):
    def __init__(self, var_node, type_node):
        super().__init__()
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.getNextToken()

    def error(self):
        raise Exception("Parser says:: Invalid Syntax!!!")

    def eatToken(self, expectedType):
        if self.current_token.type == expectedType:
            self.current_token = self.lexer.getNextToken()
        else:
            self.error()

    def program(self):
        self.eatToken(PROGRAM)
        
        var_node = self.variable()
        prog_name = var_node.value
        self.eatToken(SEMI)
        
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eatToken(DOT)
        return program_node
    
    def block(self):
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node
    
    def declarations(self):
        declarations = []
        if self.current_token.type == VAR:
            self.eatToken(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eatToken(SEMI)
        
        return declarations
    
    def variable_declaration(self):
        var_nodes = [Var(self.current_token)]
        self.eatToken(ID)
        while self.current_token.type == COMMA:
            self.eatToken(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eatToken(ID)
        
        self.eatToken(COLON)
        
        type_node = self.type_spec()
        variable_declaration = [VarDecl(var_node, type_node) for var_node in var_nodes]
        return variable_declaration
    
    def type_spec(self):
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eatToken(INTEGER)
        else:
            self.eatToken(REAL)
        
        node = Type(token)
        return node

    def compound_statement(self):
        self.eatToken(BEGIN)
        nodes = self.statement_list()
        self.eatToken(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type == SEMI:
            self.eatToken(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()

        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token

        self.eatToken(ASSIGN)

        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        node = Var(self.current_token)
        self.eatToken(ID)
        return node

    def empty(self):
        return NoOp()

    def expr(self):
        # expr:: term | term (PLUS | MINUS) term
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eatToken(PLUS)
            elif token.type == MINUS:
                self.eatToken(MINUS)

            node = BinOp(node, token, self.term())

        return node

    def term(self):
        # term:: factor | factor (MUL | INTEGER_DIV | FLOAT_DIV) factor
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.eatToken(MUL)
            elif token.type == INTEGER_DIV:
                self.eatToken(INTEGER_DIV)
            elif token.type == FLOAT_DIV:
                self.eatToken(FLOAT_DIV)

            node = BinOp(node, token, self.factor())

        return node

    def factor(self):
        """
        factor:: PLUS factor
                | MINUS factor
                | INTEGER_CONST
                | REAL_CONST
                | LPAREN expr RPAREN
                | variable
        """
        token = self.current_token

        if token.type == PLUS:
            self.eatToken(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eatToken(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER_CONST:
            self.eatToken(INTEGER_CONST)
            return Num(token)
        elif token.type == REAL_CONST:
            self.eatToken(REAL_CONST)
            return Num(token)
        elif token.type == LPAREN:
            self.eatToken(LPAREN)
            node = self.expr()
            self.eatToken(RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node


class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        super().__init__()
        self.parser = parser
        self.GLOBAL_SCOPE = {}
    
    def visit_Program(self, node):
        self.visit(node.block)
    
    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        
        self.visit(node.compound_statement)
    
    def visit_VarDecl(self, node):
        pass
    
    def visit_Type(self, node):
        pass

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            text = input("spi> ")
        except EOFError:
            break
        if not text:
            continue

        # Responsible for individual tokens.
        lexer = Lexer(text)

        # Responsible for creating an AST from said tokens.
        parser = Parser(lexer)

        # Responsible for traversing the AST while operating on it's values.
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == "__main__":
    main()
