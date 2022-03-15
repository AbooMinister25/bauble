import sys

from bauble.bauble_lexer import Lexer
from bauble.bauble_parser import Parser
from bauble.tokens import TokenKind

HELP_MESSAGE = """Usage: bauble [options]
"""


def run():
    source = "1 + 2 * 3 * 4 + 5"
    # lexer = Lexer(source)
    #
    # while lexer.next.kind != TokenKind.EOF:
    #     t = lexer.next_token()
    #     print(t)

    parser = Parser(source, "foo")
    lhs = parser.parse_expression()
    print(lhs)


for cmd in sys.argv:
    if cmd.startswith("--") or cmd.startswith("-"):
        if cmd == "--help":
            print(HELP_MESSAGE)
    else:
        run()
