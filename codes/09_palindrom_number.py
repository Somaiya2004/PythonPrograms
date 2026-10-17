# Function to check if a number is a palindrome
def is_palindrome(n):
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    
    # Negative numbers are typically not palindromes due to the minus sign
    if n < 0:
        return False
    
    s = str(n)
    return s == s[::-1]

# Get input from the user
try:
    user_input = int(input("Enter an integer: "))
    if is_palindrome(user_input):
        print(f"{user_input} is a Palindrome!")
    else:
        print(f"{user_input} is NOT a Palindrome.")
except ValueError as e:
    print(f"Error: {e}")