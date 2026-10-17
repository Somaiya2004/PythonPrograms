# Function to find the largest of three numbers
def find_largest(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c

# Get input from the user
try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    num3 = float(input("Enter third number: "))
    
    print(f"The largest number is: {find_largest(num1, num2, num3)}")
except ValueError:
    print("Please enter valid numbers.")