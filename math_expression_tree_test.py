import unittest
from math_expression_tree import *


class MathExpressionTest(unittest.TestCase):
    def test_sin_cos_tan(self):
        i = MathExpression('cos(0)+tan(0.3)*sin(0)')
        i.to_Postfix()
        i.visualize(1)
        self.assertEqual(i.calculate(), cos(0)+tan(0.3)*sin(0))

    def test_add(self):
        i = MathExpression('22.2+33.3+44.4')
        i.to_Postfix()
        i.visualize(2)
        self.assertEqual(i.calculate(), 99.9)

    def test_minus(self):
        i = MathExpression('10-(7-2)')
        i.to_Postfix()
        i.visualize(3)
        self.assertEqual(i.calculate(), 5.0)
        i = MathExpression('19-8-4-2')
        i.to_Postfix()
        i.visualize(4)
        self.assertEqual(i.calculate(), 5.0)

    def test_mul(self):
        i = MathExpression('19-14.21*20.91')
        i.to_Postfix()
        i.visualize(5)
        self.assertEqual(i.calculate(), -278.1311)
        i = MathExpression('(8-12)*func(10)')
        i.to_Postfix()
        i.visualize(6)
        self.assertEqual(i.calculate(func=lambda x: x * x), -400.0)

    def test_dev(self):
        i = MathExpression('77/6')
        i.to_Postfix()
        i.visualize(7)
        self.assertEqual(round(i.calculate(), 2), 12.83)

    def test_pow_log(self):
        i = MathExpression('pow(2,2)*log(9,3)')
        i.to_Postfix()
        i.visualize(8)
        self.assertEqual(i.calculate(), 8.0)

    def test_specialFunc(self):
        i = MathExpression('cos(0)+func(a)')
        i.to_Postfix()
        i.visualize(9)
        self.assertEqual(i.calculate(a=2, func=lambda x: x * 2), 5.0)

    # hard test
    def test_1(self):
        i = MathExpression('a + 2 - sin(0.3)*(b - c)')
        i.to_Postfix()
        i.visualize(10)
        self.assertEqual(round(i.calculate(a=1.1, b=77, c=66), 2), -0.15)

    def test_2(self):
        i = MathExpression('cos((3-a)*b)+func(c,d)/3')
        i.to_Postfix()
        i.visualize(11)
        self.assertEqual(i.calculate(a=3, b=2, c=20, d=10, func=lambda x, y: x + y), 11.0)


if __name__ == '__main__':
    unittest.main()
