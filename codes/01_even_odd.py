def check_even_odd(number):
    if number % 2 == 0:
      return "even" 
    else:
       return "odd" 

 #example usage 
try:
    user_input = int(input("Enter an iteger:"))
    print(check_even_odd(user_input))
except ValueError:
    print("please enter a valid integer.")
    
       
