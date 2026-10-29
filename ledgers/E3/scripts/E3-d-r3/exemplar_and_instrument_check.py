"""Recompute the numbers the project page quotes from Lab 3's data (exemplar B, rubric prose)."""
import importlib.util
import math
import sys
from fractions import Fraction
from pathlib import Path

LAB = Path(sys.argv[1])  # path to tests/labs/E3/lab-E3-project-3.py is NOT used; the answers are copied from the page
spec_src = LAB.read_text(encoding="utf-8")
ns: dict = {}
# Execute only the data block (everything before the first 'def value(') to read ANSWERS.
head = spec_src.split("def value(")[0]
exec(compile(head, str(LAB), "exec"), {"__name__": "lab_data", "math": math, "Fraction": Fraction}, ns)
answers = ns["ANSWERS"]
prizes = [p for a in answers for p in a[2] + a[4]]
print("answers:", len(answers))
print("prize range (cents):", min(prizes), max(prizes))
bad = []
for pid, choice, pa, qa, pb, qb in answers:
    for name, pr, pq in (("A", pa, qa), ("B", pb, qb)):
        s = sum(Fraction(q) for q in pq)
        if s != 1 or any(Fraction(q) < 0 for q in pq) or len(pr) != len(pq) or not (2 <= len(pr) <= 3):
            bad.append((pid, name))
print("lotteries that fail sum-to-1 / nonnegative / 2-3 prizes:", bad)
def mixed(pr, pq):
    return any(x > 0 and Fraction(q) > 0 for x, q in zip(pr, pq)) and any(x < 0 and Fraction(q) > 0 for x, q in zip(pr, pq))
print("mixed-sign pairs:", sum(1 for a in answers if mixed(a[2], a[3]) or mixed(a[4], a[5])))
print("pair ids:", [a[0] for a in answers])
