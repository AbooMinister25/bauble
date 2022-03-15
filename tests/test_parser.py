import pytest

from bauble.bauble_parser import Parser
from bauble.bauble_ast import (
    Assignment,
    BinOp,
    Block,
    Expr,
    ExpressionStmt,
    For,
    FunctionCall,
    FunctionDef,
    Grouping,
    Identifier,
    If,
    Let,
    Literal,
    Return,
    Statement,
    UnaryOp,
    While,
)


@pytest.mark.parametrize(
    "data",
    [
        ("10", "Literal[10]"),
        ("1.5", "Literal[1.5]"),
        ('"Hello"', "Literal[Hello]"),
        ("false", "Literal[false]"),
        ("true", "Literal[true]"),
        ("foo", "Identifier[foo]"),
        ("(10)", "Literal[10]"),
    ],
)
def test_literals(data):
    parser = Parser(data[0], "main.bl")
    node = parser.parse_expression()
    assert repr(node) == data[1]


@pytest.mark.parametrize(
    "data",
    [
        ("5 + 5", "(5 + 5)"),
        ("5 - 5", "(5 - 5)"),
        ("5 * 5", "(5 * 5)"),
        ("5 / 5", "(5 / 5)"),
        ("1 + 2 * 3", "(1 + (2 * 3))"),
        ("1 + 2 * 3", "(1 + (2 * 3))"),
        ("1 + 2 * 3 * 4 + 5", "((1 + ((2 * 3) * 4)) + 5)"),
        ("(1 + 2) * 3", "((1 + 2) * 3)"),
    ],
)
def test_binary(data):
    parser = Parser(data[0], "main.bl")
    node = parser.parse_expression()
    assert str(node) == data[1]
