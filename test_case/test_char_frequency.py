import unittest

# The function to be tested
def get_character_frequency(s):
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq

# Test class
class TestCharFrequency(unittest.TestCase):
    
    def test_frequency_standard(self):
        self.assertEqual(get_character_frequency("apple"), {'a': 1, 'p': 2, 'l': 1, 'e': 1})

    def test_frequency_case_sensitivity(self):
        self.assertEqual(get_character_frequency("Banana"), {'B': 1, 'a': 3, 'n': 2})

    def test_frequency_with_spaces(self):
        self.assertEqual(get_character_frequency("a b a"), {'a': 2, ' ': 2, 'b': 1})

    def test_frequency_empty_string(self):
        self.assertEqual(get_character_frequency(""), {})

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            get_character_frequency(12345)

if __name__ == "__main__":
    unittest.main()
    