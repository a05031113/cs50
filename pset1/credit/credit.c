/*
 * Credit
 * CS50 Problem Set 1
 *
 * Checks if credit card number is valid using
 * Luhn's Algorithm and which company
 * the credit card belongs to
 */
#include <stdio.h>
#include <cs50.h>
#include <stdbool.h>

bool valid_card(long long card);
int  number_length(long long n);
void card_company(long long card, int length);

int main(void)
{
    // Prompts user for card number
    long long card = get_long_long("Number: ");

    // If card is valid, then check the card company
    if (valid_card(card))
    {
        card_company(card, number_length(card));
    }
    // Card not valid
    else
    {
        printf("INVALID\n");
    }
}

int  number_length(long long n)
{
    // Go through each digit to calculate length of number
    int length = 0;
    while (n > 0)
    {
        n /= 10;
        length++;
    }
    return length;
}

bool valid_card(long long card)
{
    int sum, digit;
    sum = 0;

    // Calculates sum according to Luhn's Algorithm
    while (card > 0)
    {
        digit = card % 10;
        card /= 10;
        sum += digit;

        digit = card % 10;
        digit *= 2;
        sum += digit % 10;
        digit /= 10;
        sum += digit % 10;
        card /= 10;
    }

    // Checks if sum is divisible by 10
    if (sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

void card_company(long long card, int length)
{
    int first, second, num;

    // Removes all the digits from card number except first 2
    while (card >= 100)
    {
        card /= 10;
    }

    // Gets first two digits of card number
    second = card % 10;
    card /= 10;
    first = card % 10;
    num = first * 10 + second;

    // Check for conditions of all companies
    switch (num)
    {
        // American Express
        case (34):
        case (37):
            if (length == 15)
            {
                printf("AMEX\n");
                break;
            }
        // Mastercard
        case (51):
        case (52):
        case (53):
        case (54):
        case (55):
            if (length == 16)
            {
                printf("MASTERCARD\n");
                break;
            }
        // Visa
        case (40):
        case (41):
        case (42):
        case (43):
        case (44):
        case (45):
        case (46):
        case (47):
        case (48):
        case (49):
            if (length == 13 || length == 16)
            {
                printf("VISA\n");
                break;
            }
        // Invalid if none of the above
        default:
            printf("INVALID\n");
    }
}
