# Function to find the second largest number in a list
def find_second_largest(nums):
    if not isinstance(nums, list) or not nums:
        raise ValueError("Input must be a non-empty list of numbers.")
    
    # Ensure all elements are numbers
    for num in nums:
        if not isinstance(num, (int, float)):
            raise ValueError("All elements in the list must be numbers.")
    
    # Remove duplicates and sort in descending order
    unique_nums = sorted(list(set(nums)), reverse=True)
    
    if len(unique_nums) < 2:
        raise ValueError("List must contain at least two unique numbers.")
    
    return unique_nums[1]

# Get input from the user
if __name__ == "__main__":
    try:
        user_input = input("Enter numbers separated by spaces: ")
        # Convert space-separated string inputs into a list of integers or floats
        nums = [float(x) if '.' in x else int(x) for x in user_input.split()]
        result = find_second_largest(nums)
        print(f"The second largest number is: {result}")
    except ValueError as e:
        print(f"Error: {e}")