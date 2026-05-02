DNA_MAP = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3
}

def dna_hash(s):
    """Perfect hash for DNA string"""
    h = 0
    for c in s:
        h = (h << 2) | DNA_MAP[c]
    return h
