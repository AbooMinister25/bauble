from typing import Literal, Union

# Alias for available types for a Literal
LiteralKind = Union[int, float, str, Literal["true", "false", "none"]]

# Alias for different operators
Operator = Literal[
    "+", "-", "*", "/", "==", "!", "!=", ">", ">=", "<", "<=", "and", "or"
]

# Alias for different infix operators
IOperator = Literal["+", "-", "!"]
