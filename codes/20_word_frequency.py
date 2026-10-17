import string

# Function to calculate word frequency in a string
def get_word_frequency(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    if not text.strip():
        return {}
    
    # Remove punctuation and convert to lowercase for accurate word counting
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator).lower()
    
    words = cleaned_text.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

# Get input from the user
if __name__ == "__main__":
    try:
        user_input = input("Enter a sentence or paragraph: ")
        result = get_word_frequency(user_input)
        print("\nWord frequencies:")
        for word, count in result.items():
            print(f"'{word}': {count}")
    except ValueError as e:
        print(f"Error: {e}")