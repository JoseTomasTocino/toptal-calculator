from unittest import TestCase

from calculator import tokens
from calculator.parser import tokenize


class TestTokenizer(TestCase):
    def test_tokenize_1(self):
        expression = "(3 + (4 - 1)) * 5"
        token_list = [
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(3),
            tokens.PlusOperatorToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(4),
            tokens.MinusOperatorToken(),
            tokens.OperandToken(1),
            tokens.CloseParenthesisToken(),
            tokens.CloseParenthesisToken(),
            tokens.ProductOperatorToken(),
            tokens.OperandToken(5)
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)

    def test_tokenize_2(self):
        expression = "2 * var + 0.5 = 1"
        token_list = [
            tokens.OperandToken(2),
            tokens.ProductOperatorToken(),
            tokens.VariableToken('var'),
            tokens.PlusOperatorToken(),
            tokens.OperandToken(0.5),
            tokens.EqualSignToken(),
            tokens.OperandToken(1)
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)

    def test_tokenize_3(self):
        expression = "2x + 1 = 2(1-x)"
        token_list = [
            tokens.OperandToken(2),
            tokens.ProductOperatorToken(),
            tokens.VariableToken('x'),
            tokens.PlusOperatorToken(),
            tokens.OperandToken(1),
            tokens.EqualSignToken(),
            tokens.OperandToken(2),
            tokens.ProductOperatorToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(1),
            tokens.MinusOperatorToken(),
            tokens.VariableToken('x'),
            tokens.CloseParenthesisToken()
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)

    def test_tokenize_4(self):
        expression = "Log(10)"
        token_list = [
            tokens.LogFunctionToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(10),
            tokens.CloseParenthesisToken()
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)

    def test_tokenize_5(self):
        expression = "Log10"
        token_list = [
            tokens.LogFunctionToken(),
            tokens.OperandToken(10),
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)

    def test_tokenize_6(self):
        expression = "sinpi"
        token_list = [
            tokens.SinFunctionToken(),
            tokens.PiConstantToken()
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)

    def test_tokenize_7(self):
        expression = "sin(1.5*pi)"
        token_list = [
            tokens.SinFunctionToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(1.5),
            tokens.ProductOperatorToken(),
            tokens.PiConstantToken(),
            tokens.CloseParenthesisToken()
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)

    def test_tokenize_constants(self):
        expression = "pi * e"
        token_list = [
            tokens.PiConstantToken(),
            tokens.ProductOperatorToken(),
            tokens.EulerConstantToken()
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)

    def test_tokenize_division(self):
        expr = "5 / 2"
        token_list = [
            tokens.OperandToken(5),
            tokens.DivisionOperatorToken(),
            tokens.OperandToken(2)
        ]

        self.assertListEqual(token_list, tokenize(expr))

    def test_tokenize_implicit_product_operand_and_constant(self):
        expr = "5 pi"
        token_list = [
            tokens.OperandToken(5),
            tokens.ProductOperatorToken(),
            tokens.PiConstantToken()
        ]

        self.assertListEqual(token_list, tokenize(expr))

    def test_tokenize_implicit_product_variable_and_parentheses(self):
        expr = "x(2-1)"
        token_list = [
            tokens.VariableToken('x'),
            tokens.ProductOperatorToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(2),
            tokens.MinusOperatorToken(),
            tokens.OperandToken(1),
            tokens.CloseParenthesisToken()
        ]

        self.assertListEqual(token_list, tokenize(expr))

    def test_tokenize_logarithm_with_custom_base(self):
        expr = "Log100(10)"
        token_list = [
            tokens.LogFunctionToken(has_custom_base=True),
            tokens.OperandToken(100),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(10),
            tokens.CloseParenthesisToken()
        ]

        self.assertListEqual(token_list, tokenize(expr))

    def test_tokenize_trigonometrics(self):
        expression = "sin(5) + cos(5) + tan(5) + ctan(5)"
        token_list = [
            tokens.SinFunctionToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(5),
            tokens.CloseParenthesisToken(),
            tokens.PlusOperatorToken(),
            tokens.CosFunctionToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(5),
            tokens.CloseParenthesisToken(),
            tokens.PlusOperatorToken(),
            tokens.TanFunctionToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(5),
            tokens.CloseParenthesisToken(),
            tokens.PlusOperatorToken(),
            tokens.CtanFunctionToken(),
            tokens.OpenParenthesisToken(),
            tokens.OperandToken(5),
            tokens.CloseParenthesisToken()
        ]

        computed_token_list = tokenize(expression)

        self.assertListEqual(computed_token_list, token_list)
