# Function to reverse a sequence and remove duplicates (keeping the first occurrence from the right)
def remove_duplicates_and_reverse(seq):
    if not isinstance(seq, (list, str)):
        raise ValueError("Input must be a list or a string.")
    
    # Reverse the sequence first
    reversed_seq = seq[::-1]
    
    # Remove duplicates while preserving the new reversed order
    unique_items = list(dict.fromkeys(reversed_seq))
    
    # Return as a string if input was a string, otherwise as a list
    if isinstance(seq, str):
        return "".join(unique_items)
    return unique_items

# Get input from the user
if __name__ == "__main__":
    try:
        user_input = input("Enter elements (space-separated items or a string): ")
        
        if " " in user_input:
            seq = [float(x) if '.' in x else int(x) if x.lstrip('-').isdigit() else x for x in user_input.split()]
        else:
            seq = user_input
            
        result = remove_duplicates_and_reverse(seq)
        print(f"Result (reversed & duplicates removed): {result}")
    except ValueError as e:
        print(f"Error: {e}")