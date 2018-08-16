// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>

#include "helpers.h"

#define A4FREQ 440

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int numerator, denominator;

    // Set X as numerator
    numerator = fraction[0] - '0';

    // Set Y as denominator
    denominator = fraction[2] - '0';

    // Returns duration as multiple of 1/8
    return ((int) 8 / denominator) * numerator;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    int accidental, octave, distance;

    // Check if accidental is present
    if (strlen(note) == 3)
    {
        // Set octave to be last character
        octave = note[2] - '0';

        // Set accidental value
        accidental = (note[1] == '#') ? 1 : -1;
    }
    else if (strlen(note) == 2)
    {
        // Set octave to be last character
        octave = (int) note[1] - '0';

        // No accidental
        accidental = 0;
    }
    else
    {
        // Error -1 if string is not 2/3 characters long
        return -1;
    }

    // Calculate distance from A note in the particular octave
    switch (note[0])
    {
        case ('A'):
            distance = 0;
            break;
        case ('B'):
            distance = 2;
            break;
        case ('C'):
            distance = -9;
            break;
        case ('D'):
            distance = -7;
            break;
        case ('E'):
            distance = -5;
            break;
        case ('F'):
            distance = -4;
            break;
        case ('G'):
            distance = -2;
            break;
        default:
            return -2;
            break;
    }

    // Add accidental value to the distance
    distance += accidental;

    // Return the frequency
    return round(A4FREQ * pow(2, octave - 4) * pow(2, (float) distance / 12));
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    // Check for empty string
    if (s[0] == '\0')
    {
        return true;
    }
    else
    {
        return false;
    }
}
