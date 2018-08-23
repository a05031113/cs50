/*
 * Recover
 * CS50 Problem Set 4
 *
 * Recovers deleted JPEGs from raw image
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define FILENAME_LEN 8      // length of filename array
#define BUFFER_LEN   512    // length of buffer

// Create BYTE datatype
typedef uint8_t BYTE;

bool jpeg_bits(BYTE *buffer);

int main(int argc, char *argv[])
{
    // Invalid number of arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover card.raw\n");
        return 1;
    }

    // Open raw image
    FILE *raw = fopen(argv[1], "r");
    if (!raw)
    {
        fprintf(stderr, "Could not open %s\n", argv[1]);
        return 2;
    }

    // Declare buffer to store chunks
    BYTE buffer[BUFFER_LEN];

    // Declase image pointer
    FILE *image = NULL;

    // image name counter
    int img_count = 0;

    // Iterates over raw image
    for (; !feof(raw); fread(buffer, sizeof(BYTE), BUFFER_LEN, raw))
    {
        // Checks if initial bytes match jpeg
        if (jpeg_bits(buffer))
        {
            // If image file is open, close it
            if (image != NULL)
            {
                fclose(image);
            }

            // Open next image file
            char *filename[FILENAME_LEN];
            sprintf((char *) &filename, "%03i.jpg", img_count++);
            image = fopen((char *) &filename, "w");
        }

        // If image file is open, write buffer
        if (image != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BUFFER_LEN, image);
        }
    }

    // Close raw image
    fclose(raw);
    return 0;
}

bool jpeg_bits(BYTE *buffer)
{
    // Checks if first 4 bytes match jpeg
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff
        && (buffer[3] & 0xf0) == 0xe0)
    {
        return true;
    }
    return false;
}
