import sys

from bauble.bauble_lexer import Lexer

HELP_MESSAGE = """Usage: bauble [options]
"""


def run():
    source = 'print("hi")'
    lexer = Lexer(source)

    while not lexer.at_end():
        print(lexer.next_token())
        # print(lexer.next)
        # print("--")


for cmd in sys.argv:
    if cmd.startswith("--") or cmd.startswith("-"):
        if cmd == "--help":
            print(HELP_MESSAGE)
    else:
        run()
