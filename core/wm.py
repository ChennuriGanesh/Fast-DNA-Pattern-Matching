from collections import defaultdict
from core.dna_hash import dna_hash

def wm_search(T, patterns):
    m = len(patterns[0])
    n = len(T)
    B = 2

    shift = defaultdict(lambda: m - B + 1)
    prefix = defaultdict(list)

    # Preprocessing
    for p in patterns:
        block = p[m-B:m]
        h = dna_hash(block)
        shift[h] = 0
        prefix[h].append(p)

    i = 0
    matches = 0
    char_comp = 0
    hash_comp = 0

    # Searching
    while i <= n - m:
        block = T[i+m-B:i+m]
        h = dna_hash(block)
        hash_comp += 1

        if shift[h] == 0:
            for p in prefix[h]:
                char_comp += 1
                if T[i:i+m] == p:
                    matches += 1
            i += 1
        else:
            i += shift[h]

    return {
        "algorithm": "WM",
        "matches_found": matches,
        "hash_comparisons": hash_comp,
        "char_comparisons": char_comp
    }
