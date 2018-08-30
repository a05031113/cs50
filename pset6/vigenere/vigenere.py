"""
Vigenere
CS50 Problem Set 6

Encrypts text using Vigenere cipher
"""
import sys
import string


UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase


def main():
    # Error if invalid number of args
    if len(sys.argv) != 2:
        print("Usage: vigenere KEY")
        exit(1)

    # Set key, capitalize and check
    key = sys.argv[1].upper()
    if not key.isalpha():
        print("Invalid Key!")
        exit(1)

    # Prompts user for input
    plaintext = input("plaintext: ")

    # Encrypts
    print("ciphertext:", encrypt(plaintext, key))


def encrypt(plain, key):
    # String to store cipher text
    cipher = ""

    key_len, key_index = len(key), 0

    # Iterate over string
    for i in plain:
        # Uppercase
        if i.isupper():
            shift = UPPERCASE.index(i) + UPPERCASE.index(key[key_index])
            cipher += UPPERCASE[shift % len(UPPERCASE)]
            key_index = (key_index + 1) % key_len

        # Lowercase
        elif i.islower():
            shift = LOWERCASE.index(i) + UPPERCASE.index(key[key_index])
            cipher += LOWERCASE[shift % len(LOWERCASE)]
            key_index = (key_index + 1) % key_len

        # Non alphabetic characters
        else:
            cipher += i

    return cipher


if __name__ == "__main__":
    main()
