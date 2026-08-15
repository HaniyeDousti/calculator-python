from operations import add, subtract, multiply, divide, power, mod, square, square_root

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(4, 2) == 2

def test_multiply():
    assert multiply(4, 5) == 20

def test_divide():
    assert divide(25, 5) == 5

def test_divide_by_zero():
    assert divide(25, 0) == "Error: division by zero"

def test_power():
    assert power(3, 3) == 27

def test_mod():
    assert mod(10, 3) == 1

def test_square():
    assert square(2) == 4

def test_square_root():
    assert square_root(4) == 2