import unittest

# The function to be tested
def find_common_elements(list1, list2):
    if not isinstance(list1, list) or not isinstance(list2, list):
        raise ValueError("Both inputs must be lists.")
    
    seen = set()
    common = []
    set2 = set(list2)
    
    for item in list1:
        if item in set2 and item not in seen:
            seen.add(item)
            common.append(item)
            
    return common

# Test class
class TestCommonElements(unittest.TestCase):
    
    def test_common_standard(self):
        self.assertEqual(find_common_elements([1, 2, 3, 4], [3, 4, 5, 6]), [3, 4])

    def test_common_with_duplicates(self):
        self.assertEqual(find_common_elements([1, 2, 2, 3], [2, 3, 3, 4]), [2, 3])

    def test_no_common_elements(self):
        self.assertEqual(find_common_elements([1, 2], [3, 4]), [])

    def test_empty_lists(self):
        self.assertEqual(find_common_elements([], [1, 2]), [])
        self.assertEqual(find_common_elements([], []), [])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            find_common_elements("1 2 3", [1, 2, 3])
        with self.assertRaises(ValueError):
            find_common_elements([1, 2, 3], "1 2 3")

if __name__ == "__main__":
    unittest.main()