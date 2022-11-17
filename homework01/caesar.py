def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for letters in plaintext:
        if letters.isalpha():
            stay_in_alphabet = ord(letters) + shift
            if (
                stay_in_alphabet > ord("z")
                and letters.lower() == letters
                or stay_in_alphabet > ord("Z")
                and letters.upper() == letters
            ):
                stay_in_alphabet -= 26
            final_letter = chr(stay_in_alphabet)
            ciphertext += final_letter
        else:
            ciphertext += letters

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for letters in ciphertext:
        if letters.isalpha():
            stay_in_alphabet = ord(letters) - shift
            if (
                stay_in_alphabet < ord("a")
                and letters.lower() == letters
                or stay_in_alphabet < ord("A")
                and letters.upper() == letters
            ):
                stay_in_alphabet += 26
            final_letter = chr(stay_in_alphabet)
            plaintext += final_letter
        else:
            plaintext += letters

    return plaintext
