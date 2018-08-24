# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

An invented long word said to mean a lung disease caused by inhaling very fine
ash and sand dust.


## According to its man page, what does `getrusage` do?

It is used to get the usage of resources by either the program itself, it's
children processes or threads.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Both `before` and `after` are struct rusage data types which are quite big in
size. So, passing them by value is just waste of resources because then it will
copy the whole struct multiple times.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

The `for` loop starts by initialising `c` by getting the first letter from the
file and checks if it not `EOF`, that is end of the file. It then checks if the
character is a valid alphabet or apostrophe(but not for the first letter of
word).

If so, then it appends the character in the word array and increments `index`.
Then it goes on to check if the `index` is greater then the `LENGTH`, which
effectively means length of the word. If it is, then it starts a while loop till
the end of the word effectively skipping over the word altogether and resets
`index` to 0.

If, however it is not a character or apostrophe, then it goes to a different
fork (else if) and checks if it is a number. If so it again skips over the word
and resets the `index` to 0.

If it's not even a number, then it has to be a whitespace effectively completing
a word. To verify, it checks if the `index` is greater then 0. If so, it will then
terminate the string with null byte and update word counter. It then calls
the `misspelled` function to check if the word exists in the dictionary while
keeping track of the time and if not present, it prints that word and reset
`index` to 0.

At the end of the loop it reads next letter into `c` and keeps iterating until
end of the file is reached when it goes out of the loop.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

fscanf reads the whole string, so it will be cumbersome to separate out words
and check them individually. Instead it uses fgetc to get individual characters
and when it reaches whitespace it stops and checks the spelling. Also, this way
we can skip over the words we want to ignore easily.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

The parameters are declared as constants so that functions cannot modify them
intentionally or unintentionally. This is a safety measure.
