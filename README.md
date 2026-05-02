# Genome Pattern Matching using Wu-Manber Algorithm

# Overview

This project focuses on analyzing DNA sequences using efficient pattern matching techniques. As genomic data is growing rapidly, traditional string matching methods become slow and impractical. To address this, we implemented and compared the Wu–Manber (WM) and its optimized version WM-q for fast multi-pattern searching in DNA sequences.

# Features

* Supports multi-pattern exact matching on DNA sequences
* Implementation of Wu–Manber (WM) and WM-q algorithms
* Handles DNA data in FASTA format with proper preprocessing
* Generates patterns dynamically with configurable size and count
* Includes mutation simulation to mimic real biological variations
* Evaluates performance using runtime and comparison metrics
* Provides a simple Flask-based web interface to run experiments

#  Problem Statement

Searching multiple patterns in large DNA datasets is computationally expensive using basic approaches. This project aims to build a system that can efficiently perform pattern matching on genomic data and compare algorithm performance under different conditions.

# Methodology

* Load DNA sequence from a FASTA file
* Clean and preprocess the sequence
* Generate patterns from the genome
* Optionally introduce mutations in patterns
* Execute WM and WM-q algorithms
* Measure and compare performance metrics

#  Performance Metrics

* Execution time (runtime)
* Number of hash comparisons
* Number of character comparisons
* Total matches found
* Match success rate

# Results

From the experiments, it was observed that:

* WM-q performs faster than WM in most cases
* WM-q significantly reduces unnecessary character comparisons
* WM suffers from more hash collisions due to the small DNA alphabet
* Using q-grams in WM-q improves filtering efficiency

# Tech Stack

* Python
* Flask
* NumPy
* HTML
* CSS
* Java Script
