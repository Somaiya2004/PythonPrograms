# Function to check if a string is a palindrome
def is_palindrome_string(s):
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Clean the string: convert to lowercase and keep only alphanumeric characters
    cleaned = "".join(char.lower() for char in s if char.isalnum())
    
    # Check if the cleaned string equals its reverse
    return cleaned == cleaned[::-1]

# Get input from the user
try:
    user_input = input("Enter a string or phrase: ")
    if is_palindrome_string(user_input):
        print(f"'{user_input}' is a Palindrome!")
    else:
        print(f"'{user_input}' is NOT a Palindrome.")
except ValueError as e:
    print(f"Error: {e}")