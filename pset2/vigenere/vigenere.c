/*
 * Vigenere
 * CS50 Problem Set 2
 *
 * Encrypts text using Vigenere cipher
 */
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

void encrypt(string plain, string key);

int main(int argc, string argv[])
{
    // Error if invalid number of args
    if (argc != 2)
    {
        printf("Usage: vigenere KEY\n");
        return 1;
    }

    // Initialize key, check and capitalize
    string key = argv[1];
    for (int i = 0, len = strlen(key); i < len; i++)
    {
        if (isalpha(key[i]))
        {
            key[i] = toupper(key[i]);
        }
        else
        {
            printf("Invalid Key!\n");
            return 1;
        }
    }

    // Prompts user for input
    string plaintext = get_string("plaintext: ");

    // Encrypts
    printf("ciphertext: ");
    encrypt(plaintext, key);

    return 0;
}

void encrypt(string plain, string key)
{
    int length = strlen(plain), keylen = strlen(key);

    // Iterate over the string
    for (int i = 0, j = 0; i < length; i++)
    {
        // Uppercase
        if (isupper(plain[i]))
        {
            printf("%c", (plain[i] - 'A' + key[j % keylen] - 'A') % 26 + 'A');
            j++;
        }
        // Lowercase
        else if (islower(plain[i]))
        {
            printf("%c", (plain[i] - 'a' + key[j % keylen] - 'A') % 26 + 'a');
            j++;
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
