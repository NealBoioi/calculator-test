import unittest
import calculator


class CalculatorTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(calculator.evaluate_expression('2+3*4'), 14)

    def test_decimal_arithmetic(self):
        self.assertEqual(calculator.evaluate_expression('10.5+2.25'), 12.75)

    def test_division_sequence(self):
        self.assertEqual(calculator.evaluate_expression('12/3*4'), 16)


if __name__ == '__main__':
    unittest.main()
