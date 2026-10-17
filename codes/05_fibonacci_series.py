# Function to generate the first n terms of the Fibonacci series
def generate_fibonacci(n):
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Number of terms must be a positive integer.")
    if n == 1:
        return [0]
    
    fib_series = [0, 1]
    for _ in range(2, n):
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series

# Get input from the user
try:
    user_input = int(input("Enter the number of terms: "))
    print(f"Fibonacci series: {generate_fibonacci(user_input)}")
except ValueError as e:
    print(f"Error: {e}")