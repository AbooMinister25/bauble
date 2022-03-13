from typing import Optional

from bauble.tokens import Position, Token, TokenKind

# Global dictionary of Bauble's keywords
KEYWORDS = {
    "and": TokenKind.AND,
    "class": TokenKind.CLASS,
    "else": TokenKind.ELSE,
    "false": TokenKind.FALSE,
    "for": TokenKind.FOR,
    "fn": TokenKind.FN,
    "if": TokenKind.IF,
    "import": TokenKind.IMPORT,
    "let": TokenKind.LET,
    "none": TokenKind.NONE,
    "or": TokenKind.OR,
    "return": TokenKind.RETURN,
    "true": TokenKind.TRUE,
    "while": TokenKind.WHILE,
}


def is_whitespace(char: str) -> bool:
    """Returns whether the given character is whitespace or a newline"""
    return char in (" ", "\t", "\n", "\r")


class Lexer:
    """Converts a source string into a stream of `Token`s

    The lexer is the first step of Bauble's execution, it converts a
    string of some source code to a stream of tokens, which the parser
    uses to generate an AST.

    Args:
        source: The source string to tokenize.

    Attributes:
        source: The source string being tokenized.
        position: The lexer's position in the source string.
        line: The current line the lexer is on.
        column: The column number the lexer is on.
        next: The next token in the token stream.
    """

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

        # Stores the next token in the token stream ahead of time. The
        # lexer stays one token ahead of the parser.
        self.next = self.lex_token()

    def advance(self) -> Optional[str]:
        """Advances a single position forward in the lexer and returns the next char

        Returns:
            A string or None indicating that the lexer has reached the end of
            the source string.
        """

        # If the position is out of the range of the source string, return None
        if self.position >= len(self.source):
            return None

        next_char = self.source[self.position]

        # If the next character is a newline, advance the line and reset the column
        if next_char == "\n":
            self.line += 1
            self.column = 1

        self.position += 1

        return next_char

    def peek(self) -> Optional[str]:
        """Returns the next character in the source without advancing the lexer position

        Returns:
            A string, or None indicating that the current character is the
            last one in the source string.
        """

        # If the position with 1 added to it is out of the range of the source string, return None
        if self.position >= len(self.source):
            return None

        return self.source[self.position]

    def consume(self, expected: str) -> bool:
        """Advances the lexer if the peeked character is equal to the expected one

        Returns:
            True if the expected character was found, otherwise returns False.
        """

        if self.peek() == expected:
            self.advance()
            return True  # Can't shorten to a ternary, since the lexer needs to advance

        return False

    def at_end(self) -> bool:
        """Returns whether the lexer is at the end of the source string or not"""

        return self.peek() is None

    def create_token(self, kind: TokenKind, value: Optional[str] = None) -> Token:
        """Helper function that creates a Token using the data given"""
        position = Position(self.line, self.column)
        return Token(kind, position, value)

    def lex_string(self) -> Token:
        """Lexes a string and returns the created Token"""

        value = ""

        # Add to the final string value until a closing quote is found
        while self.peek() != '"' and not self.at_end():
            char = self.advance()
            value += char

        # If at the end of the source string and a closing quote wasn't found, return an error token
        if self.at_end():
            return self.create_token(
                TokenKind.ERROR,
                "Unterminated string literal, expected to find closing quote, instead found EOF (End of File)",
            )

        # Consume the closing quote
        self.advance()
        return self.create_token(TokenKind.STRING, value)

    def lex_number(self, first_char: str) -> Token:
        """Lexes a number (int or float) an returns the created Token"""

        # True if the number is an integer, set to False if numb er is found to be a float
        is_integer = True
        value = first_char

        # Add to the final value as long as the peeked character is a number
        while not self.at_end() and self.peek().isnumeric():
            value += self.advance()

        if self.peek() == ".":
            # Set is_integer to False, since the dot indicates that the value is a float
            is_integer = False
            value += self.advance()

            # Add to the final value as long as the peeked character is a number
            while not self.at_end() and self.peek().isnumeric():
                value += self.advance()

        return self.create_token(
            TokenKind.INTEGER if is_integer else TokenKind.FLOAT, value
        )

    def lex_identifier(self, first_char: str) -> Token:
        """Lexes an identifier or keyword and returns the created Token"""
        value = first_char

        # Add to the final value as long as the next character is a valid identifier
        while not self.at_end() and self.peek().isidentifier():
            value += self.advance()

        # If the final value is a keyword, return the corresponding token, otherwise create an Ident token
        return self.create_token(KEYWORDS.get(value, TokenKind.IDENT), value)

    def lex_token(self) -> Token:
        """Returns the next `Token` in the token stream"""

        next_char = self.advance()

        # if next is None, indicating that the lexer has reached the end of the input
        # string, return an EOF (End of File) Token.
        if next_char is None:
            return self.create_token(TokenKind.EOF)

        while is_whitespace(next_char):
            next_char = self.advance()

        # Handle comments
        if next_char == "/" and self.peek() == "/":
            while self.peek() != "\n" and not self.at_end():
                self.advance()

        # Single character tokens
        if next_char == "(":
            return self.create_token(TokenKind.OPEN_PAREN)
        elif next_char == ")":
            return self.create_token(TokenKind.CLOSE_PAREN)
        elif next_char == "[":
            return self.create_token(TokenKind.OPEN_BRACKET)
        elif next_char == "]":
            return self.create_token(TokenKind.CLOSE_BRACKET)
        elif next_char == "{":
            return self.create_token(TokenKind.OPEN_BRACE)
        elif next_char == "}":
            return self.create_token(TokenKind.CLOSE_BRACE)
        elif next_char == ",":
            return self.create_token(TokenKind.COMMA)
        elif next_char == ".":
            return self.create_token(TokenKind.DOT)
        elif next_char == ";":
            return self.create_token(TokenKind.SEMICOLON)

        # Two character operators
        elif next_char == "=":
            return (
                self.create_token(TokenKind.EQUAL_EQUAL)
                if self.consume("=")
                else self.create_token(TokenKind.EQUAL)
            )
        elif next_char == "!":
            return (
                self.create_token(TokenKind.BANG_EQUAL)
                if self.consume("=")
                else self.create_token(TokenKind.BANG)
            )
        elif next_char == ">":
            return (
                self.create_token(TokenKind.GREATER_EQUAL)
                if self.consume("=")
                else self.create_token(TokenKind.GREATER)
            )
        elif next_char == "<":
            return (
                self.create_token(TokenKind.LESS_EQUAL)
                if self.consume("=")
                else self.create_token(TokenKind.LESS)
            )

        # One character operators
        elif next_char == "+":
            return self.create_token(TokenKind.PLUS)
        elif next_char == "-":
            return self.create_token(TokenKind.MINUS)
        elif next_char == "*":
            return self.create_token(TokenKind.STAR)
        elif next_char == "/":
            return self.create_token(TokenKind.SLASH)

        # String literals
        elif next_char == '"':
            return self.lex_string()

        # Integer and float literals
        elif next_char.isnumeric():
            return self.lex_number(next_char)

        # Identifiers and keywords
        elif next_char.isidentifier():
            return self.lex_identifier(next_char)

        else:
            return self.create_token(
                TokenKind.ERROR, f"Unknown character {next_char} found"
            )

    def next_token(self) -> Token:
        """wrapper around lex_token that returns the current token and stores the next one"""

        # print(self.next.kind)
        current = self.next
        self.next = self.lex_token()

        return current
