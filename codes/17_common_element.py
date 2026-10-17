# Function to find common elements between two lists
def find_common_elements(list1, list2):
    if not isinstance(list1, list) or not isinstance(list2, list):
        raise ValueError("Both inputs must be lists.")
    
    # Use a set for efficient lookup and preserve order from the first list
    seen = set()
    common = []
    set2 = set(list2)
    
    for item in list1:
        if item in set2 and item not in seen:
            seen.add(item)
            common.append(item)
            
    return common

# Get input from the user
if __name__ == "__main__":
    try:
        input1 = input("Enter first list elements (space-separated): ").split()
        input2 = input("Enter second list elements (space-separated): ").split()
        
        # Helper to convert string inputs into numbers if possible
        def parse_val(v):
            try:
                return float(v) if '.' in v else int(v)
            except ValueError:
                return v
                
        list1 = [parse_val(x) for x in input1]
        list2 = [parse_val(x) for x in input2]
        
        result = find_common_elements(list1, list2)
        print(f"Common elements: {result}")
    except ValueError as e:
        print(f"Error: {e}")