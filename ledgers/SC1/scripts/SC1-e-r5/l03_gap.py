"""c187: relative gap between printed L03 Lab 1 standard errors and H*sqrt(2/N)/20. Usage: l03_gap.py <lab-SC1-L03-1.stdout>"""
import math
import re
import sys

H = None
rows = []
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"H = ([\d.]+): mean", line)
    if m:
        H = float(m.group(1))
    m = re.match(r"\s+N =\s*(\d+) steps: mean ([\d.]+), se ([\d.]+), z", line)
    if m:
        N, se = int(m.group(1)), float(m.group(3))
        formula = H * math.sqrt(2 / N) / 20
        rows.append((H, N, se, formula, se / formula - 1))
for H_, N, se, f, g in rows:
    print(f"H={H_:g} N={N:4d} printed se={se:.4f} formula={f:.6f} gap={100*g:+.2f}%")
print("max |gap| %:", max(abs(r[4]) for r in rows) * 100)
print("largest signed gap %:", max(rows, key=lambda r: r[4])[:2], max(r[4] for r in rows) * 100)
print("count of rows", len(rows))
