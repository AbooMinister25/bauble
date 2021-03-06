import pytest
from bauble.bauble_parser import Parser


@pytest.mark.parametrize(
    "data",
    [
        ("10", "Literal[10]"),
        ("1.5", "Literal[1.5]"),
        ('"Hello"', "Literal[Hello]"),
        ("false", "Literal[false]"),
        ("true", "Literal[true]"),
        ("foo", "Identifier[foo]"),
        ("_", "Identifier[_]"),
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


@pytest.mark.parametrize(
    "data",
    [
        ("-5", "(- 5)"),
        ("!foo", "(! foo)"),
        ("-5 + 3 * -2", "((- 5) + (3 * (- 2)))"),
        ("!foo + 10 - (3 / -2)", "(((! foo) + 10) - (3 / (- 2)))"),
    ],
)
def test_unary(data):
    parser = Parser(data[0], "main.bl")
    node = parser.parse_expression()
    assert str(node) == data[1]


@pytest.mark.parametrize(
    "data",
    [
        ("foo()", "foo()"),
        ("foo(1, 2, 3)", "foo(1, 2, 3)"),
        ("foo(a, b, c)", "foo(a, b, c)"),
        ("foo(5 + 5, 5 * 5, 5 - 5)", "foo((5 + 5), (5 * 5), (5 - 5))"),
    ],
)
def test_function_call(data):
    parser = Parser(data[0], "main.bl")
    node = parser.parse_expression()
    assert str(node) == data[1]
