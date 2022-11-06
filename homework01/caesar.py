def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for letters in plaintext:
        if letters.isalpha():
            stay_in_alphabet = ord(letters) + shift
            if stay_in_alphabet > ord('z') and letters.lower() == letters or stay_in_alphabet > ord(
                    'Z') and letters.upper() == letters:
                stay_in_alphabet -= 26
            final_letter = chr(stay_in_alphabet)
            ciphertext += final_letter
        else:
            ciphertext += letters

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for letters in ciphertext:
        if letters.isalpha():
            stay_in_alphabet = ord(letters) - shift
            if stay_in_alphabet < ord('a') and letters.lower() == letters or stay_in_alphabet < ord(
                    'A') and letters.upper() == letters:
                stay_in_alphabet += 26
            final_letter = chr(stay_in_alphabet)
            plaintext += final_letter
        else:
            plaintext += letters

    return plaintext
