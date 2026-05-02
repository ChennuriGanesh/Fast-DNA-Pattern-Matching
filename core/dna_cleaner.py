
def clean_dna(seq):
    return "".join(c for c in seq if c in {"A", "C", "G", "T"})
