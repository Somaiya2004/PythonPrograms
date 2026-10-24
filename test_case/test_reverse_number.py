import unittest

# The function to be tested
def reverse_number(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    
    if n < 0:
        return -int(str(-n)[::-1])
    else:
        return int(str(n)[::-1])

# Test class
class TestReverseNumber(unittest.TestCase):
    
    def test_reverse_positive(self):
        self.assertEqual(reverse_number(12345), 54321)
        self.assertEqual(reverse_number(1200), 21)  # Leading zeros drop in integer conversion

    def test_reverse_negative(self):
        self.assertEqual(reverse_number(-123), -321)

    def test_reverse_zero(self):
        self.assertEqual(reverse_number(0), 0)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            reverse_number("123")

if __name__ == "__main__":
    unittest.main()
    