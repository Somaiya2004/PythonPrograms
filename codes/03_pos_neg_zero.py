# Function to check if a number is positive, negative, or zero
def check_number_sign(number):
    if number > 0:
        return f"{number} is Positive"
    elif number < 0:
        return f"{number} is Negative"
    else:
        return f"{number} is Zero"

# Get input from the user
try:
    user_input = float(input("Enter a number: "))
    print(check_number_sign(user_input))
except ValueError:
    print("Please enter a valid number.")