/*
 * Caesar
 * CS50 Problem Set 2
 *
 * Encrypts text using Caesar cipher
 */
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void encrypt(string plain, int key);

int main(int argc, string argv[])
{
    // Error if invalid number of args
    if (argc != 2)
    {
        printf("Usage: caesar KEY\n");
        return 1;
    }

    // Initialize key
    int key = atoi(argv[1]);

    // Prompts user for input
    string plaintext = get_string("plaintext: ");

    // Encrypts
    printf("ciphertext: ");
    encrypt(plaintext, key);

    return 0;
}

void encrypt(string plain, int key)
{
    // Iterate over the string
    for (int i = 0, length = strlen(plain); i < length; i++)
    {
        // Uppercase
        if (isupper(plain[i]))
        {
            printf("%c", (plain[i] - 'A' + key) % 26 + 'A');
        }
        // Lowercase
        else if (islower(plain[i]))
        {
            printf("%c", (plain[i] - 'a' + key) % 26 + 'a');
        }
        // Non alphabetic characters
        else
        {
            printf("%c", plain[i]);
        }
    }
    printf("\n");
    return;
}
