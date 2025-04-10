import re
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

def check_password(password):
    logging.info(f"Checking password: {password}")
    
    length = len(password)
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        logging.debug(f"Analyzing character: {char}")
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif re.match(r"[@#$%^&+=]", char):
            has_special = True

    logging.debug(f"Flags — Length: {length}, Upper: {has_upper}, Lower: {has_lower}, Digit: {has_digit}, Special: {has_special}")

    if length >= 8 and has_upper and has_lower and has_digit and has_special:
        logging.info("Password is strong.")
        return "Strong"
    else:
        logging.warning("Password is weak.")
        return "Weak"

