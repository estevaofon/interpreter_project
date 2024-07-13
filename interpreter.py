import re
import argparse

# Token specification
token_specification = [
    ('IF', r'if'),  # if keyword
    ('ELSE', r'else'),  # else keyword
    ('FOR', r'for'),  # for keyword
    ('puts', r'puts'),  # puts keyword
    ('EQ', r'=='),  # Equality operator (must come before ASSIGN)
    ('NEQ', r'!='),  # Not equal operator
    ('LTE', r'<='),  # Less than or equal operator
    ('GTE', r'>='),  # Greater than or equal operator
    ('ASSIGN', r'='),  # Assignment operator
    ('LT', r'<'),  # Less than operator
    ('GT', r'>'),  # Greater than operator
    ('PLUS', r'\+'),  # Addition operator
    ('MINUS', r'-'),  # Subtraction operator
    ('TIMES', r'\*'),  # Multiplication operator
    ('DIVIDE', r'\/'),  # Division operator
    ('NUMBER', r'\d+'),  # Integer
    ('CHAR', r"'(.)'"),  # Character literal
    ('ID', r'[A-Za-z]+'),  # Identifiers
    ('WHITESPACE', r'\s+'),  # Whitespace
    ('SEMICOLON', r';'),  # Statement terminator
    ('LPAREN', r'\('),  # Left parenthesis
    ('RPAREN', r'\)'),  # Right parenthesis
    ('LBRACE', r'\{'),  # Left brace
    ('RBRACE', r'\}'),  # Right brace
    ('STRING', r'\".*?\"'),  # String literals
    ('COMMA', r','),  # Comma
    ('LBRACKET', r'\['),  # Left bracket for array
    ('RBRACKET', r'\]'),  # Right bracket for array
]

# Tokenize function
def tokenize(code):
    tokens = []
    while code:
        match = None
        for tok_type, pattern in token_specification:
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                if tok_type != 'WHITESPACE':  # Ignore whitespace tokens
                    if tok_type == 'CHAR':
                        tokens.append((tok_type, match.group(1)))
                    else:
                        tokens.append((tok_type, match.group(0)))
                code = code[match.end():]
                break
        if not match:
            raise SyntaxError(f'Unexpected character: {code[0]}')
    return tokens

# Node class
class Node:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

# Parse function
def parse(tokens):
    def parse_expression(tokens):
        def parse_term(tokens):
            token = tokens.pop(0)
            if token[0] == 'ID':
                node = Node('identifier', token[1])
                if tokens and tokens[0][0] == 'LBRACKET':
                    tokens.pop(0)  # Discard '['
                    index = parse_expression(tokens)
                    if tokens.pop(0)[0] != 'RBRACKET':
                        raise SyntaxError('Expected "]"')
                    node = Node('array_access', node.value)
                    node.children.append(index)
                return node
            elif token[0] == 'NUMBER':
                return Node('number', token[1])
            elif token[0] == 'CHAR':
                return Node('char', token[1])
            elif token[0] == 'LPAREN':
                expr = parse_expression(tokens)
                if tokens.pop(0)[0] != 'RPAREN':
                    raise SyntaxError('Expected ")"')
                return expr
            elif token[0] == 'STRING':
                return Node('identifier', token[1].strip('"'))
            else:
                raise SyntaxError('Unexpected token in term')

        def parse_factor(tokens):
            node = parse_term(tokens)
            while tokens and tokens[0][0] in ('TIMES', 'DIVIDE'):
                op = tokens.pop(0)
                right = parse_term(tokens)
                new_node = Node(op[0])
                new_node.children = [node, right]
                node = new_node
            return node

        node = parse_factor(tokens)
        while tokens and tokens[0][0] in ('PLUS', 'MINUS'):
            op = tokens.pop(0)
            right = parse_factor(tokens)
            new_node = Node(op[0])
            new_node.children = [node, right]
            node = new_node
        return node

    def parse_condition(tokens):
        left = parse_expression(tokens)
        operator = tokens.pop(0)
        if operator[0] not in ('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE'):
            raise SyntaxError('Expected comparison operator')
        right = parse_expression(tokens)
        node = Node('condition')
        node.children = [left, operator, right]
        return node

    def parse_statement(tokens):
        if tokens[0][0] == 'ID' and tokens[1][0] == 'LBRACKET':
            return parse_array_assignment(tokens)
        elif tokens[0][0] == 'ID' and tokens[1][0] != 'LBRACKET':
            return parse_assignment(tokens)
        elif tokens[0][0] == 'IF':
            return parse_if_statement(tokens)
        elif tokens[0][0] == 'puts':
            return parse_puts_statement(tokens)
        elif tokens[0][0] == 'FOR':
            return parse_for_statement(tokens)
        elif tokens[0][0] in ('ID', 'char') and tokens[1][0] == 'ID' and tokens[2][0] == 'LBRACKET':
            return parse_array_declaration(tokens)
        else:
            raise SyntaxError('Unexpected token in statement')

    def parse_assignment(tokens):
        left = parse_expression(tokens)
        if not tokens or tokens[0][0] != 'ASSIGN':
            raise SyntaxError('Expected "="')
        tokens.pop(0)  # Discard the '=' token
        right = parse_expression(tokens)
        if tokens and tokens[0][0] == 'SEMICOLON':
            tokens.pop(0)  # Discard the ';' token
        node = Node('assignment')
        node.children = [left, right]
        return node

    def parse_if_statement(tokens):
        tokens.pop(0)  # Discard 'if' token
        if tokens.pop(0)[0] != 'LPAREN':
            raise SyntaxError('Expected "("')
        condition = parse_condition(tokens)
        if tokens.pop(0)[0] != 'RPAREN':
            raise SyntaxError('Expected ")"')
        if tokens.pop(0)[0] != 'LBRACE':
            raise SyntaxError('Expected "{"')
        true_branch = []
        while tokens[0][0] != 'RBRACE':
            true_branch.append(parse_statement(tokens))
        tokens.pop(0)  # Discard '}' token
        false_branch = None
        if tokens and tokens[0][0] == 'ELSE':
            tokens.pop(0)  # Discard 'else' token
            if tokens.pop(0)[0] != 'LBRACE':
                raise SyntaxError('Expected "{"')
            false_branch = []
            while tokens[0][0] != 'RBRACE':
                false_branch.append(parse_statement(tokens))
            tokens.pop(0)  # Discard '}' token
        node = Node('if')
        node.children = [condition, true_branch, false_branch]
        return node

    def parse_puts_statement(tokens):
        tokens.pop(0)  # Discard 'puts' token
        if tokens.pop(0)[0] != 'LPAREN':
            raise SyntaxError('Expected "("')
        format_string = tokens.pop(0)
        if format_string[0] != 'STRING':
            raise SyntaxError('Expected string literal')
        args = []
        while tokens[0][0] != 'RPAREN':
            if tokens[0][0] == 'COMMA':
                tokens.pop(0)  # Discard ','
            args.append(parse_expression(tokens))
        tokens.pop(0)  # Discard ')'
        if tokens.pop(0)[0] != 'SEMICOLON':
            raise SyntaxError('Expected ";"')
        node = Node('puts', format_string[1])
        node.children = args
        return node

    def parse_for_statement(tokens):
        tokens.pop(0)  # Discard 'for' token
        if tokens.pop(0)[0] != 'LPAREN':
            raise SyntaxError('Expected "("')
        var_name = tokens.pop(0)
        if tokens.pop(0)[0] != 'ASSIGN':
            raise SyntaxError('Expected "="')
        start_value = parse_expression(tokens)
        if tokens.pop(0)[0] != 'COMMA':
            raise SyntaxError('Expected ","')
        end_value = parse_expression(tokens)
        if tokens.pop(0)[0] != 'COMMA':
            raise SyntaxError('Expected ","')
        step_value = parse_expression(tokens)
        if tokens.pop(0)[0] != 'RPAREN':
            raise SyntaxError('Expected ")"')
        if tokens.pop(0)[0] != 'LBRACE':
            raise SyntaxError('Expected "{"')
        body = []
        while tokens[0][0] != 'RBRACE':
            body.append(parse_statement(tokens))
        tokens.pop(0)  # Discard '}' token
        node = Node('for')
        node.children = [var_name, start_value, end_value, step_value, body]
        return node

    def parse_array_declaration(tokens):
        tokens.pop(0)  # Discard 'int' or 'char' token
        identifier = tokens.pop(0)
        if tokens.pop(0)[0] != 'LBRACKET':
            raise SyntaxError('Expected "["')
        size = parse_expression(tokens)
        if tokens.pop(0)[0] != 'RBRACKET':
            raise SyntaxError('Expected "]"')
        if tokens.pop(0)[0] != 'SEMICOLON':
            raise SyntaxError('Expected ";"')
        node = Node('array_declaration', identifier[1])
        node.children = [size]
        return node

    def parse_array_assignment(tokens):
        identifier = tokens.pop(0)
        if tokens.pop(0)[0] != 'LBRACKET':
            raise SyntaxError('Expected "["')
        index = parse_expression(tokens)
        if tokens.pop(0)[0] != 'RBRACKET':
            raise SyntaxError('Expected "]"')
        if tokens.pop(0)[0] != 'ASSIGN':
            raise SyntaxError('Expected "="')
        value = parse_expression(tokens)
        if tokens.pop(0)[0] != 'SEMICOLON':
            raise SyntaxError('Expected ";"')
        node = Node('array_assignment', identifier[1])
        node.children = [index, value]
        return node

    statements = []
    while tokens:
        if tokens[0][0] == 'ID' and tokens[1][0] == 'ID' and tokens[2][0] == 'LBRACKET':
            statements.append(parse_array_declaration(tokens))
        else:
            statements.append(parse_statement(tokens))
    return statements

# Evaluate condition function
def evaluate_condition(node, env):
    left = execute(node.children[0], env)
    operator = node.children[1][0]
    right = execute(node.children[2], env)
    if operator == 'EQ':
        return left == right
    elif operator == 'NEQ':
        return left != right
    elif operator == 'LT':
        return left < right
    elif operator == 'GT':
        return left > right
    elif operator == 'LTE':
        return left <= right
    elif operator == 'GTE':
        return left >= right
    else:
        raise RuntimeError('Unknown operator')

# Execute function
def execute(node, env):
    if node.type == 'assignment':
        identifier = node.children[0].value
        value = execute(node.children[1], env)
        env[identifier] = value
    elif node.type == 'array_declaration':
        identifier = node.value
        size = execute(node.children[0], env)
        env[identifier] = [0] * size if identifier[0].isdigit() else ['\0'] * size
    elif node.type == 'array_assignment':
        identifier = node.value
        index = execute(node.children[0], env)
        value = execute(node.children[1], env)
        if identifier not in env:
            env[identifier] = []
        while len(env[identifier]) <= index:
            env[identifier].append('\0' if identifier[0].isdigit() else 0)
        env[identifier][index] = value
    elif node.type == 'number':
        return int(node.value)
    elif node.type == 'char':
        return node.value
    elif node.type == 'identifier':
        return env[node.value]
    elif node.type == 'array_access':
        identifier = node.value
        index = execute(node.children[0], env)
        return env[identifier][index]
    elif node.type in ('PLUS', 'MINUS', 'TIMES', 'DIVIDE'):
        left = execute(node.children[0], env)
        right = execute(node.children[1], env)
        if node.type == 'PLUS':
            return left + right
        elif node.type == 'MINUS':
            return left - right
        elif node.type == 'TIMES':
            return left * right
        elif node.type == 'DIVIDE':
            return left / right
    elif node.type == 'puts':
        format_string = node.value
        args = [execute(child, env) for child in node.children]
        formatted_args = []
        arg_index = 0
        i = 0
        while i < len(format_string):
            if format_string[i] == '%' and i + 1 < len(format_string):
                if format_string[i + 1] == 's':
                    # Handle character array
                    array_name = args[arg_index]
                    if isinstance(array_name, str) and array_name in env:
                        char_array = env[array_name]
                        string_value = ''.join(char_array).split('\0', 1)[0]
                        formatted_args.append(string_value)
                    else:
                        formatted_args.append(args[arg_index])
                    arg_index += 1
                    i += 2
                elif format_string[i + 1] == 'd':
                    formatted_args.append(args[arg_index])
                    arg_index += 1
                    i += 2
            else:
                formatted_args.append(format_string[i])
                i += 1
        formatted_string = ''.join(str(arg) for arg in formatted_args)
        print(formatted_string.strip('"'))  # Strip double quotes from the formatted string
    elif node.type == 'if':
        condition = node.children[0]
        true_branch = node.children[1]
        false_branch = node.children[2]
        if evaluate_condition(condition, env):
            for stmt in true_branch:
                execute(stmt, env)
        elif false_branch:
            for stmt in false_branch:
                execute(stmt, env)
    elif node.type == 'for':
        var_name = node.children[0][1]
        start_value = execute(node.children[1], env)
        end_value = execute(node.children[2], env)
        step_value = execute(node.children[3], env)
        env[var_name] = start_value
        while (step_value > 0 and env[var_name] < end_value) or (step_value < 0 and env[var_name] > end_value):
            for stmt in node.children[4]:
                execute(stmt, env)
            env[var_name] += step_value
    else:
        raise RuntimeError('Unknown node type')

# Main function to read from a file and execute
def main():
    parser = argparse.ArgumentParser(description="Interpreter for a custom language")
    parser.add_argument('filename', type=str, help='The file containing the code to interpret')
    args = parser.parse_args()

    with open(args.filename, 'r') as file:
        code = file.read()

    tokens = tokenize(code)
    ast = parse(tokens)
    env = {}
    for stmt in ast:
        execute(stmt, env)
    # print("Environment:", env)  # Output should reflect the correct execution of arithmetic operations and array handling

if __name__ == "__main__":
    main()
