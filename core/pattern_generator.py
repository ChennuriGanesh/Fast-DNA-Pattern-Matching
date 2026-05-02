import random

def generate_patterns(T, m, d):
    n = len(T)
    patterns = set()

    if n < m:
        raise ValueError("Genome shorter than pattern length")

    while len(patterns) < d:
        i = random.randint(0, n - m)
        patterns.add(T[i:i+m])

    return list(patterns)
