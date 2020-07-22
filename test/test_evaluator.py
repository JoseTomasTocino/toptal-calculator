import math
import unittest

from calculator import evaluator
from calculator.evaluator import EquationNode


class TestEvaluator(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(5, evaluator.evaluate('5'))

    def test_constants(self):
        self.assertAlmostEqual(math.pi, evaluator.evaluate('pi'))
        self.assertAlmostEqual(math.e, evaluator.evaluate('e'))

    def test_addition(self):
        self.assertEqual(3, evaluator.evaluate('2 + 1'))
        self.assertEqual(5, evaluator.evaluate('x + x = 10'))
        self.assertEqual(0, evaluator.evaluate('-10 + 5 + 5'))

    def test_subtraction(self):
        self.assertEqual(3, evaluator.evaluate('5 - 2'))
        self.assertEqual(5, evaluator.evaluate('3x - x = 10'))
        self.assertEqual(0, evaluator.evaluate('5 + 5 - 10'))

    def test_product(self):
        self.assertEqual(6, evaluator.evaluate('3 * 2'))
        self.assertEqual(20, evaluator.evaluate('x * 2 = 40'))

    def test_division(self):
        self.assertEqual(6, evaluator.evaluate('60 / 10'))
        self.assertEqual(20, evaluator.evaluate('4x / 2 = 40'))

        with self.assertRaises(RuntimeError):
            evaluator.evaluate('20 / (2x) = 5')

    def test_empty_expression(self):
        with self.assertRaises(RuntimeError):
            evaluator.evaluate("")

    def test_simple_equation(self):
        self.assertEqual(5, evaluator.evaluate('x = 5'))
        self.assertEqual(5, evaluator.evaluate('2x = 10'))

    def test_bad_expression(self):
        with self.assertRaises(RuntimeError):
            evaluator.evaluate('5 + ')

    def test_bad_equation(self):
        with self.assertRaises(RuntimeError):
            evaluator.evaluate('5x + 2')

        with self.assertRaises(RuntimeError):
            evaluator.evaluate('5x * x = 5')

        with self.assertRaises(RuntimeError):
            evaluator.evaluate('x + y = 0')

        with self.assertRaises(RuntimeError):
            evaluator.evaluate('5 + 2 = 0')

        with self.assertRaises(RuntimeError):
            evaluator.evaluate('5x + 2 = 0 = 0')

        with self.assertRaises(RuntimeError):
            evaluator.evaluate("x/(2x) = 5")

    def test_functions(self):
        with self.assertRaises(RuntimeError):
            evaluator.evaluate("sin (5x) = 5")

        with self.assertRaises(RuntimeError):
            evaluator.evaluate("sin")

    def test_trigonometric(self):
        self.assertAlmostEqual(evaluator.evaluate("sin(pi)"), math.sin(math.pi))
        self.assertAlmostEqual(evaluator.evaluate("cos(pi)"), math.cos(math.pi))

    def test_log(self):
        self.assertEqual(evaluator.evaluate("log 100"), 2)
        self.assertAlmostEqual(evaluator.evaluate("log 100 (1000)"), 1.5)
        self.assertAlmostEqual(evaluator.evaluate("ln e"), 1)

    def test_equation_node_print(self):
        node = EquationNode(coefficient=5)
        self.assertEqual(str(node), "[EquationNode, coeff = 5, constant = None]")

        node = EquationNode(constant=5)
        self.assertEqual(repr(node), "[EquationNode, coeff = None, constant = 5]")
