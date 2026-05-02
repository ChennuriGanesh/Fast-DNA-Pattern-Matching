from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import time

from core.fasta_loader import load_fasta
from core.dna_cleaner import clean_dna
from core.pattern_generator import generate_patterns
from core.wm import wm_search
from core.wm_q import wm_q_search
from core.pattern_mutator import mutate_pattern



# --------------------
# App Setup
# --------------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Global state (simple but effective)
CURRENT_GENOME = None
CURRENT_GENOME_LENGTH = 0


# --------------------
# Frontend Route
# --------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------
# RUN SINGLE ALGORITHM
# --------------------
@app.route("/run", methods=["POST"])
def run():
    global CURRENT_GENOME, CURRENT_GENOME_LENGTH

    fasta = request.files.get("fasta_file")
    if not fasta:
        return jsonify({"error": "FASTA file missing"}), 400

    algorithm = request.form.get("algorithm", "wm")
    m = int(request.form.get("m", 64))
    d = int(request.form.get("d", 1000))
    q = int(request.form.get("q", 8))
    mutation = int(request.form.get("mutation", 0))

    # Save once
    fasta_path = os.path.join(UPLOAD_FOLDER, fasta.filename)
    fasta.save(fasta_path)

    # Load + Clean genome
    T = clean_dna(load_fasta(fasta_path))
    CURRENT_GENOME = T
    CURRENT_GENOME_LENGTH = len(T)

    # Generate patterns
    original_patterns = generate_patterns(T, m, d)

    if mutation > 0:
        patterns = mutate_pattern(original_patterns, mutation)
    else:
        patterns = original_patterns

    # Run algorithm
    start = time.perf_counter()

    if algorithm == "wm":
        stats = wm_search(T, patterns)
    elif algorithm == "wm_q":
        stats = wm_q_search(T, patterns, q)
    else:
        return jsonify({"error": "Invalid algorithm"}), 400

    runtime = round(time.perf_counter() - start, 6)

# Attach metadata (clean + consistent)
    stats = {
        "algorithm": algorithm.upper(),
        "genome_length": CURRENT_GENOME_LENGTH,
        "pattern_length": m,
        "num_patterns": d,
        "mutation_rate": mutation,
        "q_value": q if algorithm == "wm_q" else "-",
        "runtime_seconds": round(runtime, 6),
        "hash_comparisons": stats["hash_comparisons"],
        "char_comparisons": stats["char_comparisons"],
        "matches_found": stats["matches_found"]
    }

    return jsonify(stats)


# --------------------
# COMPARE WM vs WM-Q
# --------------------
@app.route("/compare", methods=["POST"])
def compare():
    global CURRENT_GENOME, CURRENT_GENOME_LENGTH

    fasta = request.files.get("fasta_file")
    if not fasta:
        return jsonify({"error": "FASTA file missing"}), 400

    m = int(request.form.get("m", 64))
    d = int(request.form.get("d", 1000))
    q = int(request.form.get("q", 8))

    fasta_path = os.path.join(UPLOAD_FOLDER, fasta.filename)
    fasta.save(fasta_path)

    T = clean_dna(load_fasta(fasta_path))
    CURRENT_GENOME = T
    CURRENT_GENOME_LENGTH = len(T)

    patterns = generate_patterns(T, m, d)

    # WM
    start = time.perf_counter()
    wm_stats = wm_search(T, patterns)
    wm_time = round(time.perf_counter() - start, 6)

    # WM-Q
    start = time.perf_counter()
    wmq_stats = wm_q_search(T, patterns, q)
    wmq_time = round(time.perf_counter() - start, 6)

    return jsonify({
        "genome_length": CURRENT_GENOME_LENGTH,
        "pattern_length": m,
        "num_patterns": d,
        "q": q,
        "WM": {**wm_stats, "runtime_seconds": wm_time},
        "WM_q": {**wmq_stats, "runtime_seconds": wmq_time}
    })




# --------------------
# Run Server
# --------------------
if __name__ == "__main__":
    app.run(debug=True)