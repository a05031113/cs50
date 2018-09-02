from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    lines_a = a.splitlines()
    lines_b = b.splitlines()

    return union(lines_a, lines_b)


def sentences(a, b):
    """Return sentences in both a and b"""

    sentences_a = sent_tokenize(a)
    sentences_b = sent_tokenize(b)

    return union(sentences_a, sentences_b)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # Removes \n
    a = a.replace('\n', '')
    b = b.replace('\n', '')

    # Extract substrings
    subs_a = extract_substrings(a, n)
    subs_b = extract_substrings(b, n)

    return union(subs_a, subs_b)


def union(a, b):
    """Returns a list of common elements in both a and b"""
    result = set()
    for i in a:
        if i in b:
            result.add(i)

    return list(result)


def extract_substrings(a, n):
    """Given a string it returns all possible substrings of length n"""
    subs = set()

    for i in range(len(a)):
        if i + n > len(a):
            break
        subs.add(a[i:i + n])

    return list(subs)
