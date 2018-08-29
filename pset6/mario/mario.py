"""
Mario More Comfortable
CS50 Problem Set 6

Recreates pyramid from Mario using Hashs ("#")
"""
from cs50 import get_int


def main():
    # Prompts user for appropriate height
    while True:
        height = get_int("Height: ")
        if height >= 0 and height < 24:
            break

    pyramid(height)


def pyramid(n):
    # Prints line by line
    for i in range(n):
        print(" " * (n - i - 1) + "#" * (i + 1) + "  " + "#" * (i + 1))


if __name__ == "__main__":
    main()
