import unittest

from calculator import tokens, evaluator
from calculator.parser import tokenize, infix_to_postfix


class MyTestPostfixCase(unittest.TestCase):
    def test_simple_operator(self):
        expression = "2 + 1"
        computed_token_list = tokenize(expression)
        postfix_token_list = infix_to_postfix(computed_token_list)

        token_list = [
            tokens.OperandToken(2),
            tokens.OperandToken(1),
            tokens.PlusOperatorToken(),
        ]

        self.assertListEqual(postfix_token_list, token_list)

    def test_multiple_operators(self):
        expression = "2 + 1 * 5"
        computed_token_list = tokenize(expression)
        postfix_token_list = infix_to_postfix(computed_token_list)

        token_list = [
            tokens.OperandToken(2),
            tokens.OperandToken(1),
            tokens.OperandToken(5),
            tokens.ProductOperatorToken(),
            tokens.PlusOperatorToken(),
        ]

        self.assertListEqual(postfix_token_list, token_list)

    def test_multiple_operators_reversed(self):
        expression = "2 * 1 + 5"
        computed_token_list = tokenize(expression)
        postfix_token_list = infix_to_postfix(computed_token_list)

        token_list = [
            tokens.OperandToken(2),
            tokens.OperandToken(1),
            tokens.ProductOperatorToken(),
            tokens.OperandToken(5),
            tokens.PlusOperatorToken(),
        ]

        self.assertListEqual(postfix_token_list, token_list)

    def test_parenthesis(self):
        expression = "2 * (1 + 5)"
        computed_token_list = tokenize(expression)
        postfix_token_list = infix_to_postfix(computed_token_list)

        token_list = [
            tokens.OperandToken(2),
            tokens.OperandToken(1),
            tokens.OperandToken(5),
            tokens.PlusOperatorToken(),
            tokens.ProductOperatorToken()
        ]

        self.assertListEqual(postfix_token_list, token_list)

    def test_missing_left_parenthesis(self):
        expression = "2 * 2) + 1 + 5"
        computed_token_list = tokenize(expression)

        with self.assertRaises(RuntimeError):
            postfix_token_list = infix_to_postfix(computed_token_list)

    def test_missing_right_parenthesis(self):
        expression = "2 * (1 + 5"
        computed_token_list = tokenize(expression)

        with self.assertRaises(RuntimeError):
            postfix_token_list = infix_to_postfix(computed_token_list)

    def test_simple_function(self):
        expression = "sin 5"
        computed_token_list = tokenize(expression)
        postfix_token_list = infix_to_postfix(computed_token_list)

        token_list = [
            tokens.OperandToken(5),
            tokens.SinFunctionToken(),
        ]

        self.assertListEqual(postfix_token_list, token_list)

    def test_equation_in_postfix_not_allowed(self):
        with self.assertRaises(RuntimeError):
            evaluator.evaluate('(5 + 2)', True)

        with self.assertRaises(RuntimeError):
            evaluator.evaluate('x + 1', True)

        with self.assertRaises(RuntimeError):
            evaluator.evaluate('x = 5', True)
