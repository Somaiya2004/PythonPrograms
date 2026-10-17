# Function to reverse the digits of a number
def reverse_number(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    
    if n < 0:
        # Handle negative numbers by converting to string, dropping '-', reversing, and restoring sign
        return -int(str(-n)[::-1])
    else:
        return int(str(n)[::-1])

# Get input from the user
try:
    user_input = int(input("Enter an integer to reverse: "))
    result = reverse_number(user_input)
    print(f"The reversed number is: {result}")
except ValueError as e:
    print(f"Error: {e}")