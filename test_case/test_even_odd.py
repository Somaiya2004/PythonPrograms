import unittest

# The function to be tested
def check_even_odd(number):
    if number % 2 == 0:
        return f"{number} is Even"
    else:
        return f"{number} is Odd"

# Test class
class TestCheckEvenOdd(unittest.TestCase):
    
    def test_even_positive_numbers(self):
        self.assertEqual(check_even_odd(4), "4 is Even")
        self.assertEqual(check_even_odd(0), "0 is Even")

    def test_odd_positive_numbers(self):
        self.assertEqual(check_even_odd(5), "5 is Odd")
        self.assertEqual(check_even_odd(1), "1 is Odd")

    def test_even_negative_numbers(self):
        self.assertEqual(check_even_odd(-2), "-2 is Even")

    def test_odd_negative_numbers(self):
        self.assertEqual(check_even_odd(-3), "-3 is Odd")

if __name__ == "__main__":
    unittest.main()