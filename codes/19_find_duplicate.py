# Function to find duplicate elements in a list
def find_duplicates(nums):
    if not isinstance(nums, list):
        raise ValueError("Input must be a list.")
    
    seen = set()
    duplicates = []
    
    for item in nums:
        # If the item is already seen and not yet in duplicates, add it
        if item in seen and item not in duplicates:
            duplicates.append(item)
        seen.add(item)
        
    return duplicates

# Get input from the user
if __name__ == "__main__":
    try:
        user_input = input("Enter elements separated by spaces: ").split()
        
        # Helper to convert input strings to numbers if possible
        def parse_val(v):
            try:
                return float(v) if '.' in v else int(v)
            except ValueError:
                return v
                
        nums = [parse_val(x) for x in user_input]
        result = find_duplicates(nums)
        print(f"Duplicate elements found: {result}")
    except ValueError as e:
        print(f"Error: {e}")