
# Function to check if a single number is prime
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

# Function to find all primes in a range [start, end]
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

# Get input from the user
try:
    start_val = int(input("Enter the start of the range: "))
    end_val = int(input("Enter the end of the range: "))
    result = find_primes_in_range(start_val, end_val)
    print(f"Prime numbers between {start_val} and {end_val}: {result}")
except ValueError as e:
    print(f"Error: {e}")