/*
 * Resize Less Comfortable
 * CS50 Problem Set 4
 *
 * Generates the resized version of input image
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "bmp.h"

bool check_bmp(BITMAPFILEHEADER *bf, BITMAPINFOHEADER *bi);
void update_headers(BITMAPFILEHEADER *orig_bf, BITMAPFILEHEADER *new_bf,
                    BITMAPINFOHEADER *orig_bi, BITMAPINFOHEADER *new_bi,
                    int factor, int padding);
void write_headers(BITMAPFILEHEADER *bf, BITMAPINFOHEADER *bi, FILE *file);
void read_scanline(RGBTRIPLE *scanline, int width, int factor, FILE *file);
void write_scanline(RGBTRIPLE *scanline, int width, int padding, int factor,
                    FILE *file);

int main(int argc, char *argv[])
{
    // Invalid number of arguments
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    // Parse arguments
    int factor = atoi(argv[1]);
    if (factor <= 0 || factor > 100)
    {
        fprintf(stderr, "Invalid n.\n");
        return 1;
    }

    FILE *infile = fopen(argv[2], "r");
    if (infile == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[2]);
        return 2;
    }

    FILE *outfile = fopen(argv[3], "w");
    if (outfile == NULL)
    {
        fclose(infile);
        fprintf(stderr, "Could not create %s.\n", argv[3]);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, new_bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, infile);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, new_bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, infile);

    // Validate infile
    if (!check_bmp(&bf, &bi))
    {
        fclose(outfile);
        fclose(infile);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Compute original and new padding
    int padding, new_padding;
    padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    new_padding = (4 - (factor * bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Update headers
    update_headers(&bf, &new_bf, &bi, &new_bi, factor, new_padding);

    // Write new headers
    write_headers(&new_bf, &new_bi, outfile);

    // Iterate over scanlines and write them "factor" times
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // Storage for scanline
        RGBTRIPLE scanline[new_bi.biWidth];

        // Read scanline
        read_scanline(scanline, new_bi.biWidth, factor, infile);

        // Write scanline
        write_scanline(scanline, new_bi.biWidth, new_padding, factor, outfile);

        // skip over padding, if any
        fseek(infile, padding, SEEK_CUR);
    }

    // Close files
    fclose(infile);
    fclose(outfile);

    // success
    return 0;
}

bool check_bmp(BITMAPFILEHEADER *bf, BITMAPINFOHEADER *bi)
{
    // Check for properties of BMP in header
    if (bf->bfType != 0x4d42 || bf->bfOffBits != 54 || bi->biSize != 40 ||
        bi->biBitCount != 24 || bi->biCompression != 0)
    {
        return false;
    }

    return true;
}

void update_headers(BITMAPFILEHEADER *orig_bf, BITMAPFILEHEADER *new_bf,
                    BITMAPINFOHEADER *orig_bi, BITMAPINFOHEADER *new_bi,
                    int factor, int padding)
{
    // Copy original headers
    *new_bf = *orig_bf;
    *new_bi = *orig_bi;

    // Increase width and height by "Factor"
    new_bi->biWidth *= factor;
    new_bi->biHeight *= factor;

    // Updates image and file size
    new_bi->biSizeImage = ((sizeof(RGBTRIPLE) * new_bi->biWidth) + padding)
                          * abs(new_bi->biHeight);
    new_bf->bfSize = new_bi->biSizeImage + sizeof(BITMAPFILEHEADER)
                     + sizeof(BITMAPINFOHEADER);
    return;
}

void write_headers(BITMAPFILEHEADER *bf, BITMAPINFOHEADER *bi, FILE *file)
{
    // Write file header
    fwrite(bf, sizeof(BITMAPFILEHEADER), 1, file);

    // Write info header
    fwrite(bi, sizeof(BITMAPINFOHEADER), 1, file);

    return;
}

void read_scanline(RGBTRIPLE *scanline, int width, int factor, FILE *file)
{
    // Iterate over each pixel on the current scanline
    for (int i = 0; i < (width / factor); i++)
    {
        // Variable to store pixels from scanline
        RGBTRIPLE pixel;

        // Read pixel
        fread(&pixel, sizeof(RGBTRIPLE), 1, file);

        // Write pixel "factor" times
        for (int j = 0; j < factor; j++)
        {
            *scanline++ = pixel;
        }
    }

    return;
}

void write_scanline(RGBTRIPLE *scanline, int width, int padding, int factor,
                    FILE *file)
{
    // Iterate "factor" times
    for (int i = 0; i < factor; i++)
    {
        // Write scanline
        fwrite(scanline, sizeof(RGBTRIPLE), width, file);

        // add padding at the end of each scanline
        for (int j = 0; j < padding; j++)
        {
            fputc(0x00, file);
        }
    }

    return;
}
