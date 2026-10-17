# Function to calculate the sum of digits of a number
def sum_of_digits(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    
    # Use absolute value so negative signs don't interfere with digit calculation
    return sum(int(digit) for digit in str(abs(n)))

# Get input from the user
try:
    user_input = int(input("Enter an integer: "))
    result = sum_of_digits(user_input)
    print(f"The sum of the digits is: {result}")
except ValueError as e:
    print(f"Error: {e}")