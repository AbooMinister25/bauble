from __future__ import annotations

from typing import Optional

from bauble.bauble_types import IOperator, LiteralKind, Operator
from bauble.tokens import Position


class Expr:
    """Base class for all expression AST nodes"""

    def __init__(self, position: Position):
        self.position = position


class Statement:
    """Base class for all statement AST nodes"""

    def __init__(self, position: Position):
        self.position = position


class Literal(Expr):
    """Represents a literal, one of - string, floating point number,
    integer, boolean (True/False) or None"""

    def __init__(self, value: LiteralKind, position: Position):
        super().__init__(position)

        self.value = value

    def __repr__(self):
        return f"Literal[{self.value}]"

    def __str__(self):
        return str(self.value)


class BinOp(Expr):
    """Represents a binary operation, with an infix operator and two operands"""

    def __init__(self, op: Operator, lhs: Expr, rhs: Expr, position: Position):
        super().__init__(position)

        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f"BinOp[op: {self.op} lhs: {self.lhs} rhs: {self.rhs}]"

    def __str__(self):
        return f"({self.lhs} {self.op} {self.rhs})"


class UnaryOp(Expr):
    """Represents an unary operation, with a prefix operator and one operand"""

    def __init__(self, op: IOperator, rhs: Expr, position: Position):
        super().__init__(position)

        self.op = op
        self.rhs = rhs

    def __repr__(self):
        return f"UnaryOp[op: {self.op} rhs: {self.rhs}]"

    def __str__(self):
        return f"({self.op} {self.rhs})"


class Identifier(Expr):
    """Represents an identifier"""

    def __init__(self, name: str, position: Position):
        super().__init__(position)

        self.name = name

    def __repr__(self):
        return f"Identifier[{self.name}]"

    def __str__(self):
        return self.name


class Grouping(Expr):
    """Represents a grouping in between parenthesis"""

    def __init__(self, expr: Expr, position: Position):
        super().__init__(position)

        self.expr = expr

    def __repr__(self):
        return f"Grouping[{self.expr}}}"

    def __str__(self):
        return f"({self.expr})"


class FunctionCall(Expr):
    """Represents a function call"""

    def __init__(self, name: str, args: list[Expr], position: Position):
        super().__init__(position)

        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall[name: {self.name} args: {self.args}]"

    def __str__(self):
        return f"{self.name}({', '.join([str(arg) for arg in self.args])})"


class Assignment(Expr):
    """Represents an assignment of a variable"""

    def __init__(self, name: str, value: Expr, position: Position):
        super().__init__(position)

        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment[name: {self.name} value: {self.value}]"

    def __str__(self):
        return f"{self.name} = {self.value}"


class If(Statement):
    """Represents an if statement"""

    def __init__(
        self,
        condition: Expr,
        code: Statement,
        else_: Optional[Statement],
        position: Position,
    ):
        super().__init__(position)

        self.condition = condition
        self.code = code
        self.else_ = else_

    def __repr__(self):
        return f"If[condition: {self.condition} code: {self.code} else: {self.else_}]"

    def __str__(self):
        return f"if {self.condition} {self.code} {self.else_}"


class Block(Statement):
    """Represents a block of code"""

    def __init__(self, code: list[Statement], position: Position):
        super().__init__(position)

        self.code = code

    def __repr__(self):
        return f"Block[code: {self.code}]"

    def __str__(self):
        return f"{{{self.code}}}"


class For(Statement):
    """Represents a for loop"""

    def __init__(self, expr: Expr, code: list[Statement], position: Position):
        super().__init__(position)

        self.expr = expr
        self.code = code

    def __repr__(self):
        return f"For[expr: {self.expr} code: {self.code}]"

    def __str__(self):
        return f"for {self.expr} {self.code}"


class While(Statement):
    """Represents a while while"""

    def __init__(self, expr: Expr, code: list[Statement], position: Position):
        super().__init__(position)

        self.expr = expr
        self.code = code

    def __repr__(self):
        return f"While[expr: {self.expr} code: {self.code}]"

    def __str__(self):
        return f"while {self.expr} {self.code}"


class Return(Statement):
    """Represents a return statement"""

    def __init__(self, value: Expr, position: Position):
        super().__init__(position)

        self.value = value

    def __repr__(self):
        return f"Return[value: {self.value}]"

    def __str__(self):
        return f"return {self.value}"


class Let(Statement):
    """Represents a variable declaration"""

    def __init__(self, name: str, value: Expr, position: Position):
        super().__init__(position)

        self.name = name
        self.value = value

    def __repr__(self):
        return f"Let[name: {self.value} value: {self.value}]"

    def __str__(self):
        return f"let {self.name} = {self.value}"


class FunctionDef(Statement):
    """Represents a function definition"""

    def __init__(
        self, name: str, params: tuple[str], body: Statement, position: Position
    ):
        super().__init__(position)

        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef[name: {self.name} params: {self.params} body: {self.body}]"

    def __str__(self):
        return f"fn {self.name}({', '.join(self.params)}) {self.body}"


class ExpressionStmt(Statement):
    """Represents an expression statement, or an expression
    in a place where a statement is expected"""

    def __init__(self, expr: Expr, position: Position):
        super().__init__(position)

        self.expr = expr

    def __str__(self):
        return str(self.expr)
