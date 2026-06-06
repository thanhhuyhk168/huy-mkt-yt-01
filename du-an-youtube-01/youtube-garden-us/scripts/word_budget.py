#!/usr/bin/env python3
"""Word budget check — count words by Format HARD MIN/MAX.
Usage: python word_budget.py script.txt --format E2
Exit 0 = PASS, exit 1 = UNDER-HARD-MIN (auto-fail)."""
import re, sys, argparse

RANGES = {
    "E1": (1600, 1760),  # Tutorial
    "E2": (1920, 2080),  # List
    "E3": (2080, 2240),  # Deep Dive
    "E4": (1760, 1920),  # Story / Jenga / 30-Day
}

DESCRIPTIONS = {
    "E1": "Tutorial",
    "E2": "List / Listicle",
    "E3": "Deep Dive",
    "E4": "Story / Jenga / 30-Day Challenge",
}


def count_words(text):
    return len(re.findall(r"\b[\w'-]+\b", text))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="Path to script .txt file")
    ap.add_argument("--format", required=True, choices=RANGES.keys(),
                    help="Script format: E1=Tutorial, E2=List, E3=DeepDive, E4=Story")
    a = ap.parse_args()

    text = open(a.file, encoding="utf-8").read()
    n = count_words(text)
    lo, hi = RANGES[a.format]
    mins = round(n / 160, 1)

    if n < lo:
        status = "❌ UNDER-HARD-MIN (AUTO-FAIL)"
    elif n > hi:
        status = "⚠️  OVER MAX (trim weakest example)"
    else:
        status = "✅ PASS"

    print(f"\n{'='*50}")
    print(f"Format {a.format} — {DESCRIPTIONS[a.format]}")
    print(f"Word count : {n:,} words (~{mins} min at 160 wpm)")
    print(f"Target     : {lo:,} – {hi:,} words")
    print(f"Status     : {status}")
    print(f"{'='*50}\n")

    sys.exit(1 if n < lo else 0)
