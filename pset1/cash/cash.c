/*
 * Cash
 * CS50 Problem Set 1
 *
 * Calculates minimum coins required
 * to pay the change owed
 */
#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float money;
    int   pennies, coins;

    // Prompts for change owed
    do
    {
        money = get_float("Change owed: ");
    }
    while (money < 0);

    // Converts money into pennies
    pennies = round(money * 100);

    // Calculate coins
    coins   = 0;
    while (pennies > 0)
    {
        if (pennies >= 25)
        {
            pennies -= 25;
        }
        else if (pennies >= 10)
        {
            pennies -= 10;
        }
        else if (pennies >= 5)
        {
            pennies -= 5;
        }
        else if (pennies >= 1)
        {
            pennies -= 1;
        }

        // Increment coins
        coins++;
    }

    printf("%d\n", coins);
}
