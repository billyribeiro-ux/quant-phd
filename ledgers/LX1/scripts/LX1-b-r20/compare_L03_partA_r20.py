"""Round 20: the L03 twin's printed Part A rows (out/twin_L03.out) against the independent derivation (rederive_L03_r20.py).

Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r20/compare_L03_partA_r20.py
"""
import re
S = "ledgers/LX1/scripts/LX1-b-r20/out/"
mine = [l for l in open(S + "rederive_L03_r20.out", encoding="utf-8") if l.startswith("m=")]
tw = open(S + "twin_L03.out", encoding="utf-8").read().splitlines()
rows = [l for l in tw if re.match(r"  t =\s*\d+: index", l)]
bad = 0
for a, b in zip(mine, rows):
    m = re.match(r"m=(\d+) t=\s*(\d+) index (\S+) realdebt (\d+) lev (\S+) prem (\S+) fall (\S+)", a)
    t = re.match(r"  t =\s*(\d+): index (\S+); real debt (\d+) cents; leverage (\S+); premium (\S+); output fall (\S+) percent", b)
    if tuple(m.group(i) for i in range(2, 8)) != tuple(t.group(i) for i in range(1, 7)):
        bad += 1
print("rows compared", len(rows), "mine", len(mine), "mismatches", bad)
