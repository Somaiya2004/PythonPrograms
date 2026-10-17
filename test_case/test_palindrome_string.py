import unittest

# The function to be tested
def is_palindrome_string(s):
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    cleaned = "".join(char.lower() for char in s if char.isalnum())
    return cleaned == cleaned[::-1]

# Test class
class TestPalindromeString(unittest.TestCase):
    
    def test_simple_palindromes(self):
        self.assertTrue(is_palindrome_string("racecar"))
        self.assertTrue(is_palindrome_string("Madam"))

    def test_phrase_palindromes(self):
        self.assertTrue(is_palindrome_string("A man, a plan, a canal: Panama"))
        self.assertTrue(is_palindrome_string("No 'x' in Nixon"))

    def test_non_palindromes(self):
        self.assertFalse(is_palindrome_string("hello"))
        self.assertFalse(is_palindrome_string("python"))

    def test_empty_and_single_char(self):
        self.assertTrue(is_palindrome_string(""))
        self.assertTrue(is_palindrome_string("a"))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            is_palindrome_string(12345)  # Passing an integer instead of string

if __name__ == "__main__":
    unittest.main()