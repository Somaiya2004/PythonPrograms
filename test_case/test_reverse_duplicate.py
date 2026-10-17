import unittest

def remove_duplicates_and_reverse(seq):
    if not isinstance(seq, (list, str)):
        raise ValueError("Input must be a list or a string.")
    reversed_seq = seq[::-1]
    unique_items = list(dict.fromkeys(reversed_seq))
    if isinstance(seq, str):
        return "".join(unique_items)
    return unique_items

class TestRemoveDuplicatesAndReverse(unittest.TestCase):
    
    def test_with_list(self):
        # [1, 2, 2, 3, 1, 4] reversed -> [4, 1, 3, 2, 2, 1], unique -> [4, 1, 3, 2]
        self.assertEqual(remove_duplicates_and_reverse([1, 2, 2, 3, 1, 4]), [4, 1, 3, 2])

    def test_with_string(self):
        # "programming" reversed -> "gnimmargorp", unique -> "gnimarop"
        self.assertEqual(remove_duplicates_and_reverse("programming"), "gnimarop")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            remove_duplicates_and_reverse(12345)

if __name__ == "__main__":
    unittest.main()