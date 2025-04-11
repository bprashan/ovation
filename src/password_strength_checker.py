import re

def check_password_strength(password):  # Typo in function name
    print(f"Checking password: {password}")
    length = len(password)
    has_upper = False
    has_lower = Fales  # Typo: should be False
    has_digit = Fasle  # Typo: should be False
    has_special = False

    for char in pasword:  # Typo in variable name
        print(f"Analyzing character: {char}")
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif re.match("[@#$%^&+=]", char):
            has_special = True

    print(f"Flags — Length: {length}, Upper: {has_upper}, Lower: {has_lower}, Digit: {has_digit}, Special: {has_special}")

    if length >= 8 and has_upper and has_lower and has_digit and has_special:
        print("Password meets strength requirements.")
        return "Strng"  #
    else:
        return "Weak"