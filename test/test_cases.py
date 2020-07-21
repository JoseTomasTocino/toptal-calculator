import unittest

from calculator import evaluator


class SampleTestCases(unittest.TestCase):
    def test_case_1(self):
        self.assertAlmostEqual(-4.7509872468, evaluator.evaluate("3+sin(6*3)-7"))

    def test_case_2(self):
        self.assertEqual(0.25, evaluator.evaluate("2x + 1 = 2(1-x)"))

    def test_case_3(self):
        self.assertEqual(0.25, evaluator.evaluate("2x + 1 = 2 - 2x"))

    def test_case_4(self):
        self.assertEqual(30, evaluator.evaluate("(3+(4-1))*5"))

    def test_case_5(self):
        self.assertEqual(0.25, evaluator.evaluate("2 * x + 0.5 = 1"))

    def test_case_6(self):
        self.assertEqual(0.25, evaluator.evaluate("2x + 1 = 2(1-x)"))

    def test_case_7(self):
        self.assertEqual(2, evaluator.evaluate("(x-2)*(2-3)=0"))

    def test_case_8(self):
        self.assertEqual(2, evaluator.evaluate("4x-7(2-x)=3x+2"))

    def test_case_9(self):
        self.assertEqual(9.8, evaluator.evaluate("2(w+3)-10=6(32-3w)"))

    def test_case_10(self):
        self.assertEqual(-3.5, evaluator.evaluate("(4-2z)/3 = 3/4 - (5z)/6"))

    def test_case_12(self):
        self.assertAlmostEqual(-0.1428571429, evaluator.evaluate("(3(7x-1)+10x-4+3x)=90x+1"))

    def test_case_14(self):
        self.assertEqual(0.25, evaluator.evaluate("2 * x + 0.5 = 1"))

    def test_case_16(self):
        self.assertEqual(1, evaluator.evaluate("Log(10)"))

    def test_case_17(self):
        self.assertEqual(1, evaluator.evaluate("Log10"))

    def test_case_18(self):
        self.assertEqual(0.5, evaluator.evaluate("Log100(10)"))

    def test_case_19(self):
        self.assertEqual(0, evaluator.evaluate("sinpi"))

    def test_case_20(self):
        self.assertEqual(0, evaluator.evaluate("sin(pi)"))

    def test_case_21(self):
        self.assertEqual(-1, evaluator.evaluate("sin(1.5pi)"))

    def test_case_22(self):
        self.assertEqual(-1, evaluator.evaluate("sin(1.5*pi)"))


if __name__ == '__main__':
    unittest.main()
