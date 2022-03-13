import pytest

from bauble.bauble_lexer import Lexer
from bauble.tokens import TokenKind


@pytest.mark.parametrize(
    "data",
    [
        ("10", [TokenKind.INTEGER], "10"),
        ("1.5", [TokenKind.FLOAT], "1.5"),
        ('"Hello, World"', [TokenKind.STRING], "Hello, World"),
        ("foo", [TokenKind.IDENT], "foo"),
        ("false", [TokenKind.FALSE], "false"),
        ("true", [TokenKind.TRUE], "true"),
    ],
)
def test_literals(data):
    lexer = Lexer(data[0])
    tokens = []

    while lexer.next.kind != TokenKind.EOF:
        tokens.append(lexer.next_token())

    assert [token.kind for token in tokens] == data[1] and "".join(
        [token.value for token in tokens]
    ) == data[2]


@pytest.mark.parametrize(
    "data",
    [
        ("(", [TokenKind.OPEN_PAREN]),
        (")", [TokenKind.CLOSE_PAREN]),
        ("[", [TokenKind.OPEN_BRACKET]),
        ("]", [TokenKind.CLOSE_BRACKET]),
        ("{", [TokenKind.OPEN_BRACE]),
        ("}", [TokenKind.CLOSE_BRACE]),
        (",", [TokenKind.COMMA]),
        (".", [TokenKind.DOT]),
        (";", [TokenKind.SEMICOLON]),
    ],
)
def test_punctuation(data):
    lexer = Lexer(data[0])
    tokens = []

    while lexer.next.kind != TokenKind.EOF:
        tokens.append(lexer.next_token().kind)

    assert tokens == data[1]


@pytest.mark.parametrize(
    "data",
    [
        ("=", [TokenKind.EQUAL]),
        ("==", [TokenKind.EQUAL_EQUAL]),
        ("!", [TokenKind.BANG]),
        ("!=", [TokenKind.BANG_EQUAL]),
        (">", [TokenKind.GREATER]),
        (">=", [TokenKind.GREATER_EQUAL]),
        ("<", [TokenKind.LESS]),
        ("<=", [TokenKind.LESS_EQUAL]),
        ("+", [TokenKind.PLUS]),
        ("-", [TokenKind.MINUS]),
        ("*", [TokenKind.STAR]),
        ("/", [TokenKind.SLASH]),
    ],
)
def test_operators(data):
    lexer = Lexer(data[0])
    tokens = []

    while lexer.next.kind != TokenKind.EOF:
        tokens.append(lexer.next_token().kind)

    assert tokens == data[1]


@pytest.mark.parametrize(
    "data",
    [
        ("and", [TokenKind.AND]),
        ("class", [TokenKind.CLASS]),
        ("else", [TokenKind.ELSE]),
        ("for", [TokenKind.FOR]),
        ("fn", [TokenKind.FN]),
        ("if", [TokenKind.IF]),
        ("import", [TokenKind.IMPORT]),
        ("let", [TokenKind.LET]),
        ("none", [TokenKind.NONE]),
        ("or", [TokenKind.OR]),
        ("return", [TokenKind.RETURN]),
        ("while", [TokenKind.WHILE]),
    ],
)
def test_keywords(data):
    lexer = Lexer(data[0])
    tokens = []

    while lexer.next.kind != TokenKind.EOF:
        tokens.append(lexer.next_token())

    assert [token.kind for token in tokens] == data[1] and "".join(
        [token.value for token in tokens]
    ) == data[0]


def test_misc():
    error_str = '"Unclosed String D:'
    lexer = Lexer(error_str)

    error = lexer.next_token()
    assert error.kind == TokenKind.ERROR and error.value == (
        "Unterminated string literal, expected to find closing quote, instead found EOF (End of File)"
    )

    assert lexer.next_token().kind == TokenKind.EOF
