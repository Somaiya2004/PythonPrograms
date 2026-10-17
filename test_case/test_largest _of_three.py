import unittest

# The function to be tested
def find_largest(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c

# Test class
class TestFindLargest(unittest.TestCase):
    
    def test_largest_at_first(self):
        self.assertEqual(find_largest(10, 5, 2), 10)

    def test_largest_at_middle(self):
        self.assertEqual(find_largest(3, 15, 7), 15)

    def test_largest_at_end(self):
        self.assertEqual(find_largest(4, 8, 20), 20)

    def test_negative_numbers(self):
        self.assertEqual(find_largest(-5, -2, -10), -2)

    def test_equal_numbers(self):
        self.assertEqual(find_largest(5, 5, 3), 5)

if __name__ == "__main__":
    unittest.main()