/*
 * Crack
 * CS50 Problem Set 2
 *
 * Password cracker for DES hashed passwords using
 * bruteforce
 */
#include <crypt.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define MAXLENGTH   5  // Maximux length of password
#define LEN_CHARSET 53 // Length of Character Set

// Character set for password
char charset[] =
{
    '\0',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z'
};

void decrypt(string hash);

int main(int argc, string argv[])
{
    // Error if invalid number of args
    if (argc != 2)
    {
        printf("Usage: crack HASH\n");
        return 1;
    }

    // Initialize hash
    string hash = argv[1];

    decrypt(hash);
    return 0;
}

void decrypt(string hash)
{
    char salt[] =
    {
        hash[0],
        hash[1],
        '\0'
    };
    char testcase[MAXLENGTH + 1];

    // Iterate over all the possibilities
    for (int i = 1; i < LEN_CHARSET; i++)
    {
        // First Letter
        testcase[0] = charset[i];
        for (int j = 0; j < LEN_CHARSET; j++)
        {
            // Second Letter
            testcase[1] = charset[j];

            // One lettered words
            if (j == 0)
            {
                if (strcmp(hash, crypt(testcase, salt)) == 0)
                {
                    printf("%s\n", testcase);
                    break;
                }
                continue;
            }
            for (int k = 0; k < LEN_CHARSET; k++)
            {
                // Third Letter
                testcase[2] = charset[k];

                // Two lettered words
                if (k == 0)
                {
                    if (strcmp(hash, crypt(testcase, salt)) == 0)
                    {
                        printf("%s\n", testcase);
                        break;
                    }
                    continue;
                }
                for (int l = 0; l < LEN_CHARSET; l++)
                {
                    // Forth Letter
                    testcase[3] = charset[l];

                    // Three lettered words
                    if (k == 0)
                    {
                        if (strcmp(hash, crypt(testcase, salt)) == 0)
                        {
                            printf("%s\n", testcase);
                            return;
                        }
                        continue;
                    }
                    for (int m = 0; m < LEN_CHARSET; m++)
                    {
                        // Fifth Letter
                        testcase[4] = charset[m];

                        // Sets null byte
                        testcase[5] = '\0';
                        if (strcmp(hash, crypt(testcase, salt)) == 0)
                        {
                            printf("%s\n", testcase);
                            return;
                        }
                        continue;
                    }
                }
            }
        }
    }
    return;
}
