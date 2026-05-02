def load_fasta(path):
    seq = []
    with open(path, "r") as f:
        for line in f:
            if line.startswith(">"):
                continue
            seq.append(line.strip().upper())
    return "".join(seq)
