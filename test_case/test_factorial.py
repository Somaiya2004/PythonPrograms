import unittest

# The function to be tested
def factorial(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial is only defined for non-negative integers.")
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Test class
class TestFactorial(unittest.TestCase):
    
    def test_factorial_zero_and_one(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)

    def test_factorial_positive_numbers(self):
        self.assertEqual(factorial(5), 120)  # 5! = 5 * 4 * 3 * 2 * 1 = 120
        self.assertEqual(factorial(6), 720)  # 6! = 720

    def test_factorial_negative_number(self):
        with self.assertRaises(ValueError):
            factorial(-3)

if __name__ == "__main__":
    unittest.main()