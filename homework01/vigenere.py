def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        letters = plaintext[i]
        if letters.isalpha():
            stay_in_alphabet = ord(letters) + ord(keyword[i % len(keyword)].lower()) - ord("a")
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


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i in range(len(ciphertext)):
        letters = ciphertext[i]
        if letters.isalpha():
            stay_in_alphabet = ord(letters) - (ord(keyword[i % len(keyword)].lower()) - ord("a"))
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
