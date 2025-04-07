def is_even(n):
    return n % 2 == 0

def factorial(n):
    if n < 0:
        raise ValueError("Cannot compute factorial of negative number")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result