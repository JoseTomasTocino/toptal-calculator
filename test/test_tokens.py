import math
import unittest

from calculator import tokens


class TestTokens(unittest.TestCase):
    def test_print_token(self):
        token = tokens.PlusOperatorToken()
        self.assertEqual(str(token), "Token: PlusOperatorToken")
        self.assertEqual(repr(token), "Token: PlusOperatorToken")

        token = tokens.LogFunctionToken(has_custom_base=False)
        self.assertEqual(str(token), "Token: LogFunctionToken (10-base)")

        token = tokens.LogFunctionToken(has_custom_base=True)
        self.assertEqual(str(token), "Token: LogFunctionToken (Custom base)")

        token = tokens.OperandToken(5)
        self.assertEqual(str(token), "Token: Operand (5)")

        token = tokens.VariableToken('x')
        self.assertEqual(str(token), "Token: Variable (x)")

    def test_token_equality(self):
        t0 = tokens.PlusOperatorToken()
        t1 = tokens.PlusOperatorToken()
        self.assertEqual(t0, t1)

        t1 = tokens.MinusOperatorToken()
        self.assertNotEqual(t0, t1)

    def test_ctan_operation(self):
        token = tokens.CtanFunctionToken()
        self.assertAlmostEqual(token.oper(math.pi / 2), 1 / math.tan(math.pi / 2))
