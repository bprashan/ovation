import pytest
from src.calculator import add, subtract, multiply, divide

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(2, 1) == 1
    assert subtract(2, 2) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 5) == -5

def test_divide():
    assert divide(6, 2) == 3
    assert divide(5, 2) == 2.5
    with pytest.raises(ValueError):
        divide(1, 0)