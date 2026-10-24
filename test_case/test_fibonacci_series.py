import unittest

# The function to be tested
def generate_fibonacci(n):
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Number of terms must be a positive integer.")
    if n == 1:
        return [0]
    
    fib_series = [0, 1]
    for _ in range(2, n):
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series

# Test class
class TestFibonacci(unittest.TestCase):
    
    def test_fibonacci_one_term(self):
        self.assertEqual(generate_fibonacci(1), [0])

    def test_fibonacci_two_terms(self):
        self.assertEqual(generate_fibonacci(2), [0, 1])

    def test_fibonacci_multiple_terms(self):
        self.assertEqual(generate_fibonacci(5), [0, 1, 1, 2, 3])
        self.assertEqual(generate_fibonacci(8), [0, 1, 1, 2, 3, 5, 8, 13])

    def test_fibonacci_invalid_input(self):
        with self.assertRaises(ValueError):
            generate_fibonacci(0)
        with self.assertRaises(ValueError):
            generate_fibonacci(-3)

if __name__ == "__main__":
    unittest.main()