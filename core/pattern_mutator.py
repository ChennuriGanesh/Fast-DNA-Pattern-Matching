import random

DNA_ALPHABET = ["A", "C", "G", "T"]

def mutate_pattern(pattern, num_mutations):
    """
    Introduce exactly `num_mutations` point mutations into a DNA pattern.
    """
    pattern = list(pattern)
    length = len(pattern)

    positions = random.sample(range(length), num_mutations)

    for pos in positions:
        original = pattern[pos]
        choices = [b for b in DNA_ALPHABET if b != original]
        pattern[pos] = random.choice(choices)

    return "".join(pattern)
