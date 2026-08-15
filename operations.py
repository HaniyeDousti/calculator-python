import math

def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        return 'Error: division by zero'
    
    return round(num1 / num2, 3)

def square(num1):
    return num1 ** 2

def mod(num1, num2):
    if num2 != 0:
        return num1 % num2
    else:
        return 'Error! modulo by zero'
    
def power(num1, num2):
    return num1 ** num2

def square_root(num1):
    if num1 >= 0:
        return round(math.sqrt(num1), 5)
    else:
        return 'Error! negative value'