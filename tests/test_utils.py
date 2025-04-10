import pytest
from src.utils import is_even, factorial

def test_is_even():
    assert is_even(2) == True
    assert is_even(3) == False  # This test will fail

def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1
    assert factorial(-1) == 1  # This test will fail