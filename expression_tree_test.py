import unittest
from math import sin
# from hypothesis import given

# import hypothesis.strategies as st

from expression_tree import ExpressTree


class TestExpressTree(unittest.TestCase):

    def test_ExpressTree(self):
        s0 = 'a/b+c/d'
        tree0 = ExpressTree(s0)
        with self.assertRaises(ZeroDivisionError):
            tree0(a=12, b=0, c=45, d=21)

        s1 = 'a + 2 - sin(-0.3)*(b - c)'
        tree1 = ExpressTree(s1, sin=lambda a: sin(a))
        tree1.visualization()
        res1 = 4 + 2 - sin(-0.3) * (2 - 66)
        self.assertEqual(res1, tree1(a=4, b=2, c=66))

        s2 = 'a + b - c * d / e'
        tree2 = ExpressTree(s2)
        res2 = 123456 + 654321 - 34 * 2 / 6
        self.assertEqual(res2, tree2(a=123456, b=654321, c=34, d=2, e=6))

        s3 = 'oor(aand(a, b), no(c))'
        tree3 = ExpressTree(s3, oor=lambda x, y: x or y,
                            aand=lambda x, y: x and y, no=lambda x: not x)
        self.assertEqual(0, tree3(a=1, b=0, c=1))

        def integration(a, b):
            # left-hand point
            def f(x):
                return x ** 3 - 4 * x ** 2 + 4 * x + 2
            N = 100
            result = 0
            dx = abs(b - a) / N
            while a < b:
                result += f(a) * dx
                a += dx
            return result
        s4 = 'integration(a, b)'
        tree4 = ExpressTree(s4, integration=integration)
        res4 = integration(0.5, 2.5)
        self.assertEqual(res4, tree4(a=0.5, b=2.5))
