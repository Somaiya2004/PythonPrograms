# Function to check if a character is a vowel or consonant
def check_vowel_consonant(char):
    if not isinstance(char, str) or len(char) != 1 or not char.isalpha():
        raise ValueError("Input must be a single alphabetic character.")
    
    vowels = "aeiou"
    if char.lower() in vowels:
        return f"'{char}' is a Vowel"
    else:
        return f"'{char}' is a Consonant"

# Get input from the user
try:
    user_input = input("Enter a single character: ")
    result = check_vowel_consonant(user_input)
    print(result)
except ValueError as e:
    print(f"Error: {e}")