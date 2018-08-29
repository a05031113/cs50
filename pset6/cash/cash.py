"""
Cash
CS50 Problem Set 6

Calculates minimum coins required to pay the change owed
"""
from cs50 import get_float


# Prompts for change owed
while True:
    money = get_float("Change owed: ")
    if money > 0:
        break

# Converts money into pennies
pennies = round(money * 100)

# Calculate coins
coins = 0
while pennies > 0:
    if pennies >= 25:
        pennies -= 25
    elif pennies >= 10:
        pennies -= 10
    elif pennies >= 5:
        pennies -= 5
    elif pennies >= 1:
        pennies -= 1

    # Increment coins
    coins += 1

print(coins)
