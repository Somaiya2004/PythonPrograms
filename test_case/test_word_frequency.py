import unittest
import string

# The function to be tested
def get_word_frequency(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    if not text.strip():
        return {}
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator).lower()
    words = cleaned_text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

# Test class
class TestWordFrequency(unittest.TestCase):
    
    def test_frequency_standard(self):
        self.assertEqual(get_word_frequency("apple banana apple orange"), {'apple': 2, 'banana': 1, 'orange': 1})

    def test_frequency_case_and_punctuation(self):
        self.assertEqual(get_word_frequency("Python, python! PYTHON."), {'python': 3})

    def test_empty_or_whitespace_string(self):
        self.assertEqual(get_word_frequency(""), {})
        self.assertEqual(get_word_frequency("   "), {})

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            get_word_frequency(12345)  # Passing an integer instead of a string

if __name__ == "__main__":
    unittest.main()