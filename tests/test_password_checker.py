import pytest
import logging

from src.password_checker import check_password

logging.basicConfig(level=logging.INFO)

def test_strong_password():
    assert check_password("Abc123@#") == "Strong"

def test_weak_no_upper():
    assert check_password("abc123@#") == "Weak"

def test_weak_no_digit():
    assert check_password("Abcdef@#") == "Weak"

def test_weak_no_special():
    assert check_password("Abc12345") == "Weak"

def test_too_short():
    assert check_password("A1@a") == "Weak"

