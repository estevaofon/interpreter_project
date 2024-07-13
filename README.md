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
int array[5];
array[0] = 1;
array[1] = 2;
array[2] = 3;
array[3] = 4;
array[4] = 5;

if (array[0] == 1) {
    puts("First element is %d\n", array[0]);
} else {
    puts("First element is not 1\n");
}

for (i = 0, 5, 1) {
    puts("Array element %d: %d\n", i, array[i]);
}
```
### Usage
```python interpreter.py <filename>```

### Code Overview
####Tokenizer

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