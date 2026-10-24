import unittest

# The function to be tested
def check_number_sign(number):
    if number > 0:
        return f"{number} is Positive"
    elif number < 0:
        return f"{number} is Negative"
    else:
        return f"{number} is Zero"

# Test class
class TestCheckNumberSign(unittest.TestCase):
    
    def test_positive_numbers(self):
        self.assertEqual(check_number_sign(5), "5 is Positive")
        self.assertEqual(check_number_sign(0.5), "0.5 is Positive")

    def test_negative_numbers(self):
        self.assertEqual(check_number_sign(-3), "-3 is Negative")
        self.assertEqual(check_number_sign(-10.5), "-10.5 is Negative")

    def test_zero(self):
        self.assertEqual(check_number_sign(0), "0 is Zero")

if __name__ == "__main__":
    unittest.main()