import pytest
from src.password_strength_checker import check_password_strength

def test_strong_password():
    assert check_password_strength("Abc123@#") == "Strong"

def test_weak_no_upper():
    assert check_password_strength("abc123@#") == "Weak"

def test_weak_no_digit():
    assert check_password_strength("Abcdef@#") == "Weak"

def test_weak_no_special():
    assert check_password_strength("Abc12345") == "Weak"

def test_too_short():
    assert check_password_strength("A1@a") == "Weak"