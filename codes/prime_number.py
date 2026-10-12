def is_prime(num):
    if num < 2:
        return False  
    i = 2
    while i * i <= num:
        if num % i == 0:
            return False 
        i += 1 

    return True

if __name__ == "__main__":
    num = int(input("enter the number : "))
    if is_prime(num=num):
        print(num," is prime ")
    else:
        print(num, " is not prime")

#  python .\codes\prime_number.py