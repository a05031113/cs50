# Questions

## What's `stdint.h`?

It is a header file which defines ints with exact width.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

So that the program can be more portable instead of depending on the implementation of the compiler, because widths of the int
is going to be fixed.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE:  1
DWORD: 4
LONG:  4
WORD:  2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

0x424d

## What's the difference between `bfSize` and `biSize`?

bfSize is the size of the file whereas biSize is size of the Bitmap info header.

## What does it mean if `biHeight` is negative?

If biHeight is negative that means the image is defined upside down, that is information about the bottom most pixels is defined
first.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If for some reason, fopen is not able to open/create the file on the disk then it will return NULL pointer.

## Why is the third argument to `fread` always `1` in our code?

Third argument is 1, that means we are reading precisely 1 times the size of RGBTRIPLE bytes from the file.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

It changes the current position in the file which we are reading from.

## What is `SEEK_CUR`?

It is the current position in the file we are reading.

## Whodunit?

It was Professor Plum with the candlestick in the library.
