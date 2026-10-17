# Function to calculate character frequency in a string
def get_character_frequency(s):
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq

# Get input from the user
try:
    user_input = input("Enter a string: ")
    result = get_character_frequency(user_input)
    print("\nCharacter frequencies:")
    for char, count in result.items():
        print(f"'{char}': {count}")
except ValueError as e:
    print(f"Error: {e}")