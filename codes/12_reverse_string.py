# Function to reverse a string
def reverse_string(s):
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    # Using python string slicing to reverse the string
    return s[::-1]

# Get input from the user
try:
    user_input = input("Enter a string to reverse: ")
    result = reverse_string(user_input)
    print(f"The reversed string is: {result}")
except ValueError as e:
    print(f"Error: {e}")