import unittest

# The function to be tested
def find_max(a, b):
    if a > b:
        return a
    elif b > a:
        return b
    else:
        return "Both numbers are equal"

# Test class
class TestTwoNumbers(unittest.TestCase):
    
    def test_first_is_larger(self):
        self.assertEqual(find_max(10, 5), 10)

    def test_second_is_larger(self):
        self.assertEqual(find_max(3, 8), 8)

    def test_both_equal(self):
        self.assertEqual(find_max(7, 7), "Both numbers are equal")

    def test_negative_numbers(self):
        self.assertEqual(find_max(-2, -5), -2)

if __name__ == "__main__":
    unittest.main()