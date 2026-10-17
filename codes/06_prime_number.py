# Function to check if a number is prime
def is_prime(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Get input from the user
if __name__ == "__main__":
    try:
        num = int(input("Enter a number: "))
        if is_prime(num):
            print(f"{num} is a Prime number.")
        else:
            print(f"{num} is NOT a Prime number.")
    except ValueError as e:
        print(f"Error: {e}")