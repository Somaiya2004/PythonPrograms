import unittest

# The function to be tested
def is_palindrome(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]

# Test class
class TestPalindrome(unittest.TestCase):
    
    def test_palindrome_numbers(self):
        self.assertTrue(is_palindrome(121))
        self.assertTrue(is_palindrome(12321))
        self.assertTrue(is_palindrome(0))
        self.assertTrue(is_palindrome(7))

    def test_non_palindrome_numbers(self):
        self.assertFalse(is_palindrome(123))
        self.assertFalse(is_palindrome(10))

    def test_negative_numbers(self):
        self.assertFalse(is_palindrome(-121))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            is_palindrome("121")

if __name__ == "__main__":
    unittest.main()