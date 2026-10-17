import unittest

# The function to be tested
def find_second_largest(nums):
    if not isinstance(nums, list) or not nums:
        raise ValueError("Input must be a non-empty list of numbers.")
    for num in nums:
        if not isinstance(num, (int, float)):
            raise ValueError("All elements in the list must be numbers.")
    
    unique_nums = sorted(list(set(nums)), reverse=True)
    if len(unique_nums) < 2:
        raise ValueError("List must contain at least two unique numbers.")
    return unique_nums[1]

# Test class
class TestSecondLargest(unittest.TestCase):
    
    def test_second_largest_standard(self):
        self.assertEqual(find_second_largest([10, 20, 4, 45, 99]), 45)
        self.assertEqual(find_second_largest([1, 2, 3, 4, 5]), 4)

    def test_second_largest_with_duplicates(self):
        self.assertEqual(find_second_largest([10, 20, 20, 4, 45, 99, 99]), 45)

    def test_second_largest_negative_numbers(self):
        self.assertEqual(find_second_largest([-10, -20, -5, -2]), -5)

    def test_not_enough_unique_elements(self):
        with self.assertRaises(ValueError):
            find_second_largest([10])
        with self.assertRaises(ValueError):
            find_second_largest([10, 10, 10])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            find_second_largest("10 20 30")  # Passing a string instead of a list
        with self.assertRaises(ValueError):
            find_second_largest([10, "twenty", 30])  # Non-numeric element

if __name__ == "__main__":
    unittest.main()