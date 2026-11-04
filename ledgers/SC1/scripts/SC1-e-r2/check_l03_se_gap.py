"""Re-derive the population SE H*sqrt(2/N)/20 and the printed-SE gaps of SC1 Lesson 3 Lab 1 (card SC1-c187, c052).
Reads the printed SEs from the lesson-3 stdout saved in ledgers/SC1/scripts/SC1-e-r2/out/lab-SC1-L03-1.stdout.
Usage: check_l03_se_gap.py <stdout file>
"""
import math
import re
import sys

rows = []
horizon = None
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"H = ([0-9.]+): mean", line)
    if m:
        horizon = float(m.group(1))
        continue
    m = re.match(r"\s+N =\s*(\d+) steps: mean ([-0-9.]+), se ([0-9.]+), z = ([-0-9.]+)", line)
    if m and horizon is not None:
        n, mean, se = int(m.group(1)), float(m.group(2)), float(m.group(3))
        pop = horizon * math.sqrt(2 / n) / 20
        gap = (se - pop) / pop * 100
        rows.append((horizon, n, se, pop, gap))
for h, n, se, pop, gap in rows:
    print(f"H={h:g} N={n:3d} printed se={se:.4f} population={pop:.5f} gap={gap:+.2f}%")
print("max |gap| % =", max(abs(r[4]) for r in rows), "at", max(rows, key=lambda r: abs(r[4]))[:2])
print("count rows =", len(rows))
