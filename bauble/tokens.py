from collections import namedtuple
from enum import Enum
from typing import Optional


class TokenKind(Enum):
    # Single character tokens
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"
    OPEN_BRACKET = "["
    CLOSE_BRACKET = "]"
    OPEN_BRACE = "{"
    CLOSE_BRACE = "}"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";"

    # Operator tokens
    EQUAL = "="
    EQUAL_EQUAL = "=="
    BANG = "!"
    BANG_EQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"

    # Literals
    INTEGER = "INTEGER"
    STRING = "STRING"
    FLOAT = "FLOT"

    # Identifiers
    IDENT = "IDENTIFIER"

    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FOR = "for"
    FN = "fn"
    IF = "if"
    IMPORT = "import"
    LET = "let"
    NONE = "none"
    OR = "or"
    RETURN = "return"
    TRUE = "true"
    WHILE = "while"

    # Misc
    ERROR = "error"
    EOF = "End of File"


Position = namedtuple("Position", "line column")


class Token:
    def __init__(
        self, kind: TokenKind, position: Position, value: Optional[str] = None
    ):
        self.kind = kind
        self.value = (
            value or kind.value
        )  # If no value is given, use the string description for the token on the TokenKind enum
        self.position = position

    @property
    def line(self) -> int:
        return self.position.line

    @property
    def column(self) -> int:
        return self.position.column

    def __repr__(self):
        return f"[{self.kind} {self.value}]"

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)
