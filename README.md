# Custom Language Interpreter

This project implements an interpreter for a custom language. The interpreter can tokenize, parse, and execute code written in this custom language. It supports basic arithmetic operations, conditional statements, loops, array handling, and formatted output.

## Features

- **Arithmetic Operations**: Supports addition, subtraction, multiplication, and division.
- **Conditional Statements**: Supports `if` and `else` statements.
- **Loops**: Supports `for` loops.
- **Arrays**: Supports array declarations, assignments, and access.
- **Formatted Output**: Supports printing formatted strings with the `puts` statement.

## Language Syntax

### Supported Tokens

- **Keywords**: `if`, `else`, `for`, `puts`
- **Operators**: `==`, `!=`, `<=`, `>=`, `=`, `<`, `>`, `+`, `-`, `*`, `/`
- **Other Tokens**: Identifiers, Numbers, Characters, Strings, Whitespace, `;`, `(`, `)`, `{`, `}`, `[`, `]`, `,`

### Example Code

```python
upper = 300;
step = 20;

for (f = 0, upper, step) {
    c = (5 / 9) * (f - 32);
    puts("Fahrenheit: %d Celsius: %d", f, c);
}
```

### Usage
```python interpreter.py <filename>```

### Code Overview
#### Tokenizer

The tokenize function takes source code as input and returns a list of tokens. Each token is a tuple containing a type and the matched value.

#### Parser
The parse function takes a list of tokens and constructs an abstract syntax tree (AST). It uses several helper functions to parse different constructs:

* parse_expression
* parse_condition
* parse_statement
* parse_assignment
* parse_if_statement
* parse_puts_statement
* parse_for_statement
* parse_array_declaration
* parse_array_assignment

#### Executor
The execute function takes an AST node and an environment (a dictionary) and performs the corresponding actions. It handles different node types like assignments, array declarations, array accesses, arithmetic operations, puts statements, if statements, and for loops.

#### Execution Flow
```text
Tokenization:
    The tokenize function reads the source code and converts it into a list of tokens.

Parsing:
    The parse function takes the list of tokens and converts it into an abstract syntax tree (AST). Each node of the AST represents a construct in the language (e.g., expressions, statements).

Execution:
    The execute function recursively traverses the AST and performs the corresponding actions. The environment (env) is a dictionary that stores the values of variables and arrays.
```
