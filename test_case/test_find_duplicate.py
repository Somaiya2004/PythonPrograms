import unittest

# The function to be tested
def find_duplicates(nums):
    if not isinstance(nums, list):
        raise ValueError("Input must be a list.")
    
    seen = set()
    duplicates = []
    for item in nums:
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
    return duplicates

# Test class
class TestFindDuplicates(unittest.TestCase):
    
    def test_duplicates_standard(self):
        self.assertEqual(find_duplicates([1, 2, 3, 2, 4, 1, 5]), [2, 1])

    def test_no_duplicates(self):
        self.assertEqual(find_duplicates([1, 2, 3, 4, 5]), [])

    def test_all_duplicates(self):
        self.assertEqual(find_duplicates([7, 7, 7, 7]), [7])

    def test_with_strings(self):
        self.assertEqual(find_duplicates(["apple", "banana", "apple", "orange", "banana"]), ["apple", "banana"])

    def test_empty_list(self):
        self.assertEqual(find_duplicates([]), [])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            find_duplicates("1 2 3 2")  # Passing a string instead of a list

if __name__ == "__main__":
    unittest.main()