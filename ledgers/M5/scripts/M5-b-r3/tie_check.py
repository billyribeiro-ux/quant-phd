"""Bisection step counts for L06 Lab 1 Part A (verifier's own code): counts of indices in the left and right
halves at each step, with TIE marked where they are equal."""
from fractions import Fraction as F
vals = [F(n * n % 1000, 1000) for n in range(1, 4097)]
l, r = F(0), F(1)
last = 0
for step in range(1, 9):
    mid = (l + r) / 2
    pool = [n for n in range(last + 1, 4097) if l <= vals[n - 1] <= r]
    lo = [n for n in pool if vals[n - 1] < mid]
    hi = [n for n in pool if vals[n - 1] >= mid]
    print(step, len(lo), len(hi), "TIE" if len(lo) == len(hi) else "")
    if len(lo) >= len(hi):
        r, half = mid, lo
    else:
        l, half = mid, hi
    last = half[0]
