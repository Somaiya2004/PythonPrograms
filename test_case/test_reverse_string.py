import unittest

# The function to be tested
def reverse_string(s):
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    return s[::-1]

# Test class
class TestReverseString(unittest.TestCase):
    
    def test_reverse_standard(self):
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("Python"), "nohtyP")

    def test_reverse_empty_and_single(self):
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_string("a"), "a")

    def test_reverse_spaces_and_symbols(self):
        self.assertEqual(reverse_string("hello world"), "dlrow olleh")
        self.assertEqual(reverse_string("123!"), "!321")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            reverse_string(12345)  # Passing an integer instead of a string

if __name__ == "__main__":
    unittest.main()
    