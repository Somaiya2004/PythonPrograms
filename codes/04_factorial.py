# Function to calculate the factorial of a number
def factorial(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial is only defined for non-negative integers.")
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Get input from the user
try:
    user_input = int(input("Enter a non-negative integer: "))
    print(f"The factorial of {user_input} is: {factorial(user_input)}")
except ValueError as e:
    print(f"Error: {e}")