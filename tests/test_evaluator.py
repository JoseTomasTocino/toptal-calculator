import math
import unittest

from calculator import evaluator


class TestEvaluator(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(5, evaluator.evaluate('5'))

    def test_constants(self):
        self.assertAlmostEqual(math.pi, evaluator.evaluate('pi'))
        self.assertAlmostEqual(math.e, evaluator.evaluate('e'))

    def test_addition(self):
        self.assertEqual(3, evaluator.evaluate('2 + 1'))
        self.assertEqual(5, evaluator.evaluate('x + x = 10'))

    def test_subtraction(self):
        self.assertEqual(3, evaluator.evaluate('5 - 2'))
        self.assertEqual(5, evaluator.evaluate('3x - x = 10'))

    def test_product(self):
        self.assertEqual(6, evaluator.evaluate('3 * 2'))
        self.assertEqual(20, evaluator.evaluate('x * 2 = 40'))

    def test_division(self):
        self.assertEqual(6, evaluator.evaluate('60 / 10'))
        self.assertEqual(20, evaluator.evaluate('4x / 2 = 40'))
        self.assertEqual(2, evaluator.evaluate('20 / (2x) = 5'))

    def test_simple_equation(self):
        self.assertEqual(5, evaluator.evaluate('x = 5'))
        self.assertEqual(5, evaluator.evaluate('2x = 10'))

    def test_bad_expression(self):
        with self.assertRaises(RuntimeError):
            evaluator.evaluate('5x + 2')

        with self.assertRaises(RuntimeError):
            evaluator.evaluate('5x * x = 5')
