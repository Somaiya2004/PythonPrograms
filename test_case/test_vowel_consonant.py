import unittest

# The function to be tested
def check_vowel_consonant(char):
    if not isinstance(char, str) or len(char) != 1 or not char.isalpha():
        raise ValueError("Input must be a single alphabetic character.")
    
    vowels = "aeiou"
    if char.lower() in vowels:
        return f"'{char}' is a Vowel"
    else:
        return f"'{char}' is a Consonant"

# Test class
class TestVowelConsonant(unittest.TestCase):
    
    def test_lowercase_vowels(self):
        self.assertEqual(check_vowel_consonant('a'), "'a' is a Vowel")
        self.assertEqual(check_vowel_consonant('e'), "'e' is a Vowel")

    def test_uppercase_vowels(self):
        self.assertEqual(check_vowel_consonant('I'), "'I' is a Vowel")
        self.assertEqual(check_vowel_consonant('O'), "'O' is a Vowel")

    def test_consonants(self):
        self.assertEqual(check_vowel_consonant('b'), "'b' is a Consonant")
        self.assertEqual(check_vowel_consonant('Z'), "'Z' is a Consonant")

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            check_vowel_consonant('5')     # Numbers are not alphabetic
        with self.assertRaises(ValueError):
            check_vowel_consonant('ab')    # Multiple characters
        with self.assertRaises(ValueError):
            check_vowel_consonant('$')     # Special characters

if __name__ == "__main__":
    unittest.main()