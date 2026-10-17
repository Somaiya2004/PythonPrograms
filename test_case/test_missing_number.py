import unittest

# The function to be tested
def find_missing_number(nums):
    if not isinstance(nums, list) or not nums:
        raise ValueError("Input must be a non-empty list of integers.")
    for num in nums:
        if not isinstance(num, int):
            raise ValueError("All elements in the list must be integers.")
    n = len(nums) + 1
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum

# Test class
class TestMissingNumber(unittest.TestCase):
    
    def test_missing_in_middle(self):
        self.assertEqual(find_missing_number([1, 2, 4, 5]), 3)

    def test_missing_at_end(self):
        self.assertEqual(find_missing_number([1, 2, 3, 4]), 5)

    def test_missing_at_start(self):
        self.assertEqual(find_missing_number([2, 3, 4, 5]), 1)

    def test_single_element_list(self):
        self.assertEqual(find_missing_number([2]), 1)
        self.assertEqual(find_missing_number([1]), 2)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            find_missing_number("1 2 4 5")  # Passing a string instead of a list
        with self.assertRaises(ValueError):
            find_missing_number([])       # Empty list
        with self.assertRaises(ValueError):
            find_missing_number([1, 2, 3.5, 5])  # Non-integer element

if __name__ == "__main__":
    unittest.main()