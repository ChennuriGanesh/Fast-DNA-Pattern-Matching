import csv
import time
import os

from core.fasta_loader import load_fasta
from core.dna_cleaner import clean_dna
from core.pattern_generator import generate_patterns
from core.wm import wm_search
from core.wm_q import wm_q_search


# =======================
# EXPERIMENT PARAMETERS
# =======================
FASTA_PATH = "data/ecoli.fasta"

M_VALUES = [32, 64, 128]
D_VALUES = [100, 500, 1000]
Q_VALUES = [4, 8]

OUTPUT_CSV = "results.csv"


def run_experiments():
    print("Loading genome...")
    T = clean_dna(load_fasta(FASTA_PATH))
    genome_length = len(T)
    print(f"Genome length: {genome_length}")

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "algorithm",
            "genome_length",
            "pattern_length_m",
            "num_patterns_d",
            "q",
            "runtime_seconds",
            "hash_comparisons",
            "char_comparisons",
            "matches_found"
        ])

        for m in M_VALUES:
            for d in D_VALUES:
                print(f"\nGenerating patterns (m={m}, d={d})")
                patterns = generate_patterns(T, m, d)
                assert len(patterns) == d, f"Expected {d}, got {len(patterns)}"

                # -----------------------
                # WM (baseline)
                # -----------------------
                print("Running WM...")
                start = time.perf_counter()
                stats = wm_search(T, patterns)
                runtime = time.perf_counter() - start

                writer.writerow([
                    "WM",
                    genome_length,
                    m,
                    d,
                    "",
                    round(runtime, 6),
                    stats["hash_comparisons"],
                    stats["char_comparisons"],
                    stats["matches_found"]
                ])

                # -----------------------
                # WM-q
                # -----------------------
                for q in Q_VALUES:
                    print(f"Running WM-q (q={q})...")
                    start = time.perf_counter()
                    stats = wm_q_search(T, patterns, q)
                    runtime = time.perf_counter() - start

                    writer.writerow([
                        "WM-q",
                        genome_length,
                        m,
                        d,
                        q,
                        round(runtime, 6),
                        stats["hash_comparisons"],
                        stats["char_comparisons"],
                        stats["matches_found"]
                    ])

    print(f"\nAll experiments completed.")
    print(f"Results saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    run_experiments()
