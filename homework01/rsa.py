def is_prime(n: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
