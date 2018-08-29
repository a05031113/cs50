"""
Caesar
CS50 Problem Set 6

Encrypts text using Caesar cipher
"""
import sys
import string


UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase


def main():
    # Error if invalid number of args
    if not len(sys.argv) is 2:
        print("Usage: caesar KEY")
        exit(1)

    # Check if key is int
    try:
        key = int(sys.argv[1])
    except ValueError:
        print("Key must be integer")
        exit(1)

    # Prompts user for input
    plaintext = input("plaintext: ")

    # Encrypts
    print("ciphertext:", encrypt(plaintext, key))


def encrypt(plain, key):
    # String to store cipher text
    cipher = ""

    # Iterate over string
    for i in plain:
        # Uppercase
        if i.isupper():
            shift = (UPPERCASE.index(i) + key) % len(UPPERCASE)
            cipher += UPPERCASE[shift]
        # Lowercase
        elif i.islower():
            shift = (LOWERCASE.index(i) + key) % len(LOWERCASE)
            cipher += LOWERCASE[shift]
        # Non alphabetic characters
        else:
            cipher += i

    return cipher


if __name__ == "__main__":
    main()
