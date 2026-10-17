import unittest

# The function to be tested
def is_prime(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Test class
class TestPrimeNumber(unittest.TestCase):
    
    def test_prime_numbers(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(13))
        self.assertTrue(is_prime(97))

    def test_non_prime_numbers(self):
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(-5))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(100))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            is_prime("11")  # String instead of integer
        with self.assertRaises(ValueError):
            is_prime(7.5)   # Float instead of integer

if __name__ == "__main__":
    unittest.main()