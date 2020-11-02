import unittest
from factor import factorize


class TestFactorize(unittest.TestCase):

    def test_wrong_types_raise_exception(self):
        cases = ['sting', 1.5]
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_negative(self):
        cases = [-1, -10, -100]
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        cases = [0, 1]
        true_case = [(0,), (1,)]
        for i, x in enumerate(cases):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), true_case[i])

    def test_simple_numbers(self):
        cases = [3, 13, 29]
        true_case = [(3,), (13,), (29,)]
        for i, x in enumerate(cases):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), true_case[i])

    def test_two_simple_multipliers(self):
        cases = [6, 26, 121]
        true_case = [(2, 3), (2, 13), (11, 11)]
        for i, x in enumerate(cases):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), true_case[i])

    def test_many_multipliers(self):
        cases = [1001, 9699690]
        true_case = [(7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19)]
        for i, x in enumerate(cases):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), true_case[i])
