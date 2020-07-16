from unittest import TestCase

from calculator.parser import tokens
from calculator.parser.tokenizer import tokenize


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
        expression = "2 * x + 0.5 = 1"
        token_list = [
            tokens.OperandToken(2),
            tokens.ProductOperatorToken(),
            tokens.VariableToken('x'),
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
    #
    #
    # def test_tokenize_8(self):
    #     expression = "2x + 1"
    #     token_list = [
    #         tokens.SinFunctionToken(),
    #         tokens.OpenParenthesisToken(),
    #         tokens.OperandToken(1.5),
    #         tokens.ProductOperatorToken(),
    #         tokens.PiConstantToken(),
    #         tokens.CloseParenthesisToken()
    #     ]
    #
    #     computed_token_list = tokenize(expression)
    #
    #     self.assertListEqual(computed_token_list, token_list)
