# Function to find the missing number in a sequence from 1 to n
def find_missing_number(nums):
    if not isinstance(nums, list) or not nums:
        raise ValueError("Input must be a non-empty list of integers.")
    
    for num in nums:
        if not isinstance(num, int):
            raise ValueError("All elements in the list must be integers.")
            
    # N is the expected total count of numbers including the missing one
    n = len(nums) + 1
    
    # Mathematical formula for the sum of first n natural numbers: n * (n + 1) / 2
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    
    return expected_sum - actual_sum

# Get input from the user
if __name__ == "__main__":
    try:
        user_input = input("Enter numbers separated by spaces (e.g., 1 2 4 5): ")
        nums = [int(x) for x in user_input.split()]
        result = find_missing_number(nums)
        print(f"The missing number is: {result}")
    except ValueError as e:
        print(f"Error: {e}")