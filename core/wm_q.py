from collections import defaultdict
from core.dna_hash import dna_hash

def wm_q_search(T, patterns, q):
    m = len(patterns[0])
    n = len(T)

    shift = defaultdict(lambda: m - q + 1)
    prefix = defaultdict(list)

    # Preprocessing
    for p in patterns:
        suffix = p[m-q:m]
        prefix_block = p[:q]

        s_hash = dna_hash(suffix)
        p_hash = dna_hash(prefix_block)

        shift[s_hash] = 0
        prefix[s_hash].append((p_hash, p))

    i = 0
    matches = 0
    char_comp = 0
    hash_comp = 0

    # Searching
    while i <= n - m:
        suffix = T[i+m-q:i+m]
        s_hash = dna_hash(suffix)
        hash_comp += 1

        if shift[s_hash] == 0:
            prefix_block = T[i:i+q]
            p_hash = dna_hash(prefix_block)
            hash_comp += 1

            for ph, p in prefix[s_hash]:
                if ph == p_hash:
                    char_comp += 1
                    if T[i:i+m] == p:
                        matches += 1
            i += 1
        else:
            i += shift[s_hash]

    return {
        "algorithm": "WM-q",
        "q": q,
        "matches_found": matches,
        "hash_comparisons": hash_comp,
        "char_comparisons": char_comp
    }
