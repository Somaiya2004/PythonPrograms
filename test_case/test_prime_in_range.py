import unittest

# The functions to be tested
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_primes_in_range(start, end):
    if not isinstance(start, int) or not isinstance(end, int):
        raise ValueError("Range limits must be integers.")
    if start > end:
        raise ValueError("Start range cannot be greater than end range.")
    
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

# Test class
class TestPrimeRange(unittest.TestCase):
    
    def test_primes_in_standard_range(self):
        self.assertEqual(find_primes_in_range(1, 10), [2, 3, 5, 7])
        self.assertEqual(find_primes_in_range(10, 20), [11, 13, 17, 19])

    def test_primes_no_primes_in_range(self):
        self.assertEqual(find_primes_in_range(24, 28), [])

    def test_invalid_range_order(self):
        with self.assertRaises(ValueError):
            find_primes_in_range(20, 10)

if __name__ == "__main__":
    unittest.main()