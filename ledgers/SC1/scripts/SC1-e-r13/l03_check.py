"""Recompute the L03 lab-derived claims from the twin stdout (standard library only).

Usage: python -I l03_check.py <twin_L03.stdout>
"""
import math
import re
import sys

rows = []
horizon = None
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"H = ([\d.]+): mean", line)
    if m:
        horizon = float(m.group(1))
    m = re.match(r"\s+N =\s*(\d+) steps: mean ([\d.]+), se ([\d.]+), z = (-?[\d.]+)", line)
    if m:
        n, mean, se, z = int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        rows.append((horizon, n, mean, se, z))
print("rows", len(rows))
zs = [abs(r[4]) for r in rows]
print("max |z| =", max(zs), "second largest |z| =", sorted(zs)[-2], "count |z|>2:", sum(z > 2 for z in zs))
gaps = []
for h, n, mean, se, z in rows:
    theo = h * math.sqrt(2 / n) / 20
    # recompute z from printed mean and horizon
    zc = (mean - h) / se
    gaps.append((abs(se / theo - 1) * 100, h, n, se, theo, se / theo - 1))
    if abs(zc - z) > 0.006:
        print("z mismatch", h, n, zc, z)
for g in sorted(gaps, reverse=True)[:4]:
    print(f"gap {g[5] * 100:+.2f}% at H={g[1]:g} N={g[2]}: printed se {g[3]:.4f}, theoretical {g[4]:.6f}")
print("H=2,N=1 by the page formula:", 0.1601 / (2 * math.sqrt(2) / 20) - 1)
print("H=1,N=1 theoretical:", math.sqrt(2) / 20)
print("H=2,N=128 theoretical:", 2 * math.sqrt(2 / 128) / 20)
