import math


class Token:
    def __str__(self):
        return "Token: {}".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class OpenParenthesisToken(Token): pass


class CloseParenthesisToken(Token): pass


class OperandToken(Token):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Token: Operand ({})".format(self.value)


class VariableToken(Token):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Token: Variable ({})".format(self.value)


class PlusOperatorToken(Token): pass


class MinusOperatorToken(Token): pass


class ProductOperatorToken(Token): pass


class DivisionOperatorToken(Token): pass


class EqualSignToken(Token): pass


class LogFunctionToken(Token):
    def __init__(self, has_custom_base=False):
        self.has_custom_base = has_custom_base

    def __str__(self):
        return "Token: LogFunctionToken ({})".format("Custom base" if self.has_custom_base else "10-base")

class LnFunctionToken(Token): pass


class SinFunctionToken(Token):
    def __init__(self):
        self.oper = math.sin


class CosFunctionToken(Token):
    def __init__(self):
        self.oper = math.cos


class TanFunctionToken(Token):
    def __init__(self):
        self.oper = math.tan


class CtanFunctionToken(Token):
    def oper(self, x):
        return 1 / math.tan(x)


class PiConstantToken(Token):
    def __init__(self):
        self.value = math.pi


class EulerConstantToken(Token):
    def __init__(self):
        self.value = math.e


is_operand = lambda token: isinstance(token, OperandToken)
is_variable = lambda token: isinstance(token, VariableToken)
is_constant = lambda token: isinstance(token, (PiConstantToken, EulerConstantToken))
is_operator = lambda token: isinstance(token, (
    ProductOperatorToken, DivisionOperatorToken, PlusOperatorToken, MinusOperatorToken))
is_function = lambda token: isinstance(token, (
    LogFunctionToken, LnFunctionToken, SinFunctionToken, CosFunctionToken, TanFunctionToken, CtanFunctionToken))
is_trigonometric = lambda token: isinstance(token,
                                            (SinFunctionToken, CosFunctionToken, TanFunctionToken, CtanFunctionToken))
is_left_paren = lambda token: isinstance(token, OpenParenthesisToken)
is_right_paren = lambda token: isinstance(token, CloseParenthesisToken)
