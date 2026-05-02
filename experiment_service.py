import csv
import time

from core.pattern_generator import generate_patterns
from core.wm import wm_search
from core.wm_q import wm_q_search
from core.pattern_mutator import mutate_pattern


def run_full_experiment(T, output_path):
    M_VALUES = [32, 64, 128]
    D_VALUES = [100, 500, 1000]
    Q_VALUES = [4, 8]
    MUTATION_LEVELS = [0, 1, 2]

    genome_length = len(T)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "algorithm",
            "genome_length",
            "pattern_length_m",
            "num_patterns_d",
            "q",
            "mutation_rate",
            "match_success_rate",
            "runtime_seconds",
            "hash_comparisons",
            "char_comparisons",
            "matches_found"
        ])

        for m in M_VALUES:
            for d in D_VALUES:
                for mutation_rate in MUTATION_LEVELS:

                    # ---------- Pattern generation ----------
                    if mutation_rate == 0:
                        patterns = generate_patterns(T, m, d)
                    else:
                        patterns = generate_mutated_patterns(T, m, d, mutation_rate)

                    actual_d = len(patterns)
                    if actual_d == 0:
                        print(f"Skipping m={m}, d={d}, mut={mutation_rate}")
                        continue

                    print(f"m={m}, d={actual_d}, mutation={mutation_rate}")

                    # ---------- WM ----------
                    start = time.perf_counter()
                    stats = wm_search(T, patterns)
                    runtime = time.perf_counter() - start
                    match_success_rate = stats["matches_found"] / actual_d

                    writer.writerow([
                        "WM",
                        genome_length,
                        m,
                        actual_d,
                        "",
                        mutation_rate,
                        round(match_success_rate, 4),
                        round(runtime, 6),
                        stats["hash_comparisons"],
                        stats["char_comparisons"],
                        stats["matches_found"]
                    ])

                    # ---------- WM-q ----------
                    for q in Q_VALUES:
                        start = time.perf_counter()
                        stats = wm_q_search(T, patterns, q)
                        runtime = time.perf_counter() - start
                        match_success_rate = stats["matches_found"] / actual_d

                        writer.writerow([
                            "WM-q",
                            genome_length,
                            m,
                            actual_d,
                            q,
                            mutation_rate,
                            round(match_success_rate, 4),
                            round(runtime, 6),
                            stats["hash_comparisons"],
                            stats["char_comparisons"],
                            stats["matches_found"]
                        ])


def generate_mutated_patterns(T, m, d, num_mutations):
    base_patterns = generate_patterns(T, m, d)
    return [mutate_pattern(p, num_mutations) for p in base_patterns]
