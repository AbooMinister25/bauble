import sys
from dataclasses import dataclass
from typing import Callable, Optional

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
from bauble.bauble_lexer import Lexer
from bauble.tokens import Position, Token, TokenKind


@dataclass
class Precedence:
    """Represents the precedence of a token"""

    prefix: Optional[int]
    infix: Optional[int]


@dataclass
class Rule:
    """Represents a parse rule with a prefix and infix handler"""

    prefix: Optional[Optional[Callable[[], Expr]]]
    infix: Optional[Optional[Callable[[Expr], Expr]]]


PRECEDENCE_MAP = {
    TokenKind.EQUAL: Precedence(None, 1),
    TokenKind.OR: Precedence(None, 2),
    TokenKind.AND: Precedence(None, 3),
    TokenKind.EQUAL_EQUAL: Precedence(None, 4),
    TokenKind.BANG_EQUAL: Precedence(None, 4),
    TokenKind.GREATER: Precedence(None, 5),
    TokenKind.GREATER_EQUAL: Precedence(None, 5),
    TokenKind.LESS: Precedence(None, 5),
    TokenKind.LESS_EQUAL: Precedence(None, 5),
    TokenKind.PLUS: Precedence(None, 6),
    TokenKind.MINUS: Precedence(8, 6),
    TokenKind.STAR: Precedence(None, 7),
    TokenKind.SLASH: Precedence(None, 7),
    TokenKind.BANG: Precedence(8, None),
    TokenKind.OPEN_PAREN: Precedence(None, 9),
    TokenKind.DOT: Precedence(None, 9),
}


def get_precedence(kind: TokenKind) -> Precedence:
    """Returns the precedence level for the given token kind

    Args:
        kind: The token kind to get the precedence for.

    Returns:
        A dataclass which represents the prefix and infix
        precedence levels for the given token kind.
    """

    return PRECEDENCE_MAP.get(kind, Precedence(None, 0))


class Parser:
    """Parses a source string into an AST (Abstract Syntax Tree)

    The parser invokes the lexer, and parses the token stream into
    a tree-like representation of Bauble's syntax.

    Args:
        source: The source string to parse.
        filename: The name of the file being parsed.

    Attributes:
        lexer: The lexer which is generating the token stream.
        filename: The name of the file being parsed.
        ast: The AST that the parser is generating.
    """

    def __init__(self, source: str, filename: str):
        self.source = source
        self.lexer = Lexer(source)  # Initialize the lexer
        self.filename = filename

        self.ast: list[Statement] = []  # The list which will store the AST

        # A dictionary of rules that map different token kinds to a
        # corresponding function for them to be parsed with.
        self.rules_map = {
            TokenKind.INTEGER: Rule(self.parse_literal, None),
            TokenKind.FLOAT: Rule(self.parse_literal, None),
            TokenKind.STRING: Rule(self.parse_literal, None),
            TokenKind.FALSE: Rule(self.parse_literal, None),
            TokenKind.TRUE: Rule(self.parse_literal, None),
            TokenKind.NONE: Rule(self.parse_literal, None),
            TokenKind.IDENT: Rule(self.parse_ident, None),
            TokenKind.OPEN_PAREN: Rule(self.parse_grouping, None),
            TokenKind.PLUS: Rule(None, self.parse_binary),
            TokenKind.MINUS: Rule(self.parse_unary, self.parse_binary),
            TokenKind.STAR: Rule(None, self.parse_binary),
            TokenKind.SLASH: Rule(None, self.parse_binary),
            TokenKind.BANG: Rule(self.parse_unary, self.parse_binary),
        }

    def advance(self) -> Token:
        """Advances and returns the next token in the token stream.

        Returns:
            A `Token` object which represents the next token in the token stream.
        """

        return self.lexer.next_token()

    def peek(self) -> Optional[Token]:
        """Returns the `next` attribute of the Lexer

        Returns:
            A `Token` object which represents a token in the token stream, or
            if it hasn't been given a value yet, it returns `None`.
        """

        return self.lexer.next

    def consume(self, expected: TokenKind, message: str):
        """Advances if the peeked token is of the same kind as the expected one.

        Args:
            expected: The expected token kind.
            message: The error message to use if the peeked token
            isn't of the same kind as the expected one.
        """

        if self.peek().kind != expected:
            self.emit_error(message, self.peek())
            return

        self.advance()  # Advance, since the next token is the expected one

    def emit_error(self, message: str, token: Token):
        """Emits an error with the information given

        Args:
            message: The error message to use.
            token: The token that the error is on.
        """

        print("Syntax Error ", file=sys.stderr)
        print(f"= [{self.filename}:{token.line}:{token.column}]", file=sys.stderr)
        print(f"| {token if token.kind != TokenKind.ERROR else ''}", file=sys.stderr)
        print(
            "{:>{spaces}}".format(
                f"^^-{message}",
                spaces=" " * (token.column - len(token))
                if token.column - len(token) < 1
                else " ",
            ),
            file=sys.stderr,
        )

    def parse_expression(self, precedence: int = 0) -> Expr:
        """Parses an expression

        Args:
            precedence: The operator precedence level to use.

        Returns:
            A parsed Expr AST node.
        """

        # Get the rule for the next token from the rule map dictionary

        rule = self.rules_map[self.peek().kind]

        # If no prefix rule, return an error
        if rule.prefix is None:
            self.emit_error(
                f"Invalid Syntax: Expected expression, found {self.peek()}", self.peek()
            )

        lhs = rule.prefix()

        while precedence < get_precedence(self.peek().kind).infix:
            rule = self.rules_map[self.peek().kind]
            lhs = rule.infix(lhs)

        return lhs

    def parse_literal(self) -> Expr:
        """Parses a literal value"""

        token = self.advance()

        if token.kind == TokenKind.INTEGER:
            return Literal(int(token.value), token.position)
        elif token.kind == TokenKind.FLOAT:
            return Literal(float(token.value), token.position)
        else:
            return Literal(token.value, token.position)

    def parse_ident(self) -> Expr:
        """Parses an identifier"""

        token = self.advance()

        # If the next token is an equal sign, parse as an assignment
        if self.peek().kind == TokenKind.EQUAL:
            self.advance()
            value = self.parse_expression(1)

            return Assignment(token.value, value, token.position)
        # If next token is an opening parenthesis, parse as a function call
        elif self.peek().kind == TokenKind.OPEN_PAREN:
            args = self.parse_function_args()
            return FunctionCall(token.value, args, token.position)

        return Identifier(token.value, token.position)

    def parse_function_args(self) -> list[Expr]:
        """Parse a function's arguments"""

        args = []
        self.consume(TokenKind.OPEN_PAREN, "Expected to find opening parenthesis `(`")

        # While the next token isn't a closing parenthesis, parse the next argument
        while self.peek().kind != TokenKind.CLOSE_PAREN:
            arg = self.parse_expression(1)
            args.append(arg)

            if self.peek().kind == TokenKind.COMMA:
                self.advance()

        self.consume(TokenKind.CLOSE_PAREN, "Expected to find closing parenthesis `)`")
        return args

    def parse_grouping(self) -> Expr:
        """Parse a grouping (expression in between parenthesis)"""

        self.advance()
        expr = self.parse_expression(1)
        self.consume(TokenKind.CLOSE_PAREN, "Expected to find closing parenthesis `)`")

        return expr

    def parse_unary(self) -> Expr:
        """Parse a unary operation"""

        op = self.advance()
        precedence = get_precedence(op.kind).prefix
        expr = self.parse_expression(precedence)

        return UnaryOp(op.value, expr, op.position)

    def parse_binary(self, lhs: Expr) -> Expr:
        """Parse a binary operation"""

        op = self.advance()
        precedence = get_precedence(op.kind).infix

        rhs = self.parse_expression(precedence)

        return BinOp(op.value, lhs, rhs, lhs.position)
