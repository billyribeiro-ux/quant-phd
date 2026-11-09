"""Checks the Exemplar B data claims against Lab 3's answers: prize range, prizes per lottery, mixed count, pairs 0 and 3."""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
block = re.search(r"ANSWERS: list\[Answer\] = \[(.*?)\n\]", src, flags=re.S).group(1)
rows = re.findall(r"\((\d+), \"([AB])\", (\[[^\]]*\]), (\[[^\]]*\]), (\[[^\]]*\]), (\[[^\]]*\])\)", block)
prizes = []
counts = []
mixed = 0
for pid, ch, pa, qa, pb, qb in rows:
    pa, pb = eval(pa), eval(pb)
    qa, qb = eval(qa), eval(qb)
    prizes += pa + pb
    counts += [len(pa), len(pb)]
    def mix(pz, qs):
        from fractions import Fraction as F
        return any(x > 0 and F(p) > 0 for x, p in zip(pz, qs)) and any(x < 0 and F(p) > 0 for x, p in zip(pz, qs))
    mixed += mix(pa, qa) or mix(pb, qb)
print("pairs", len(rows), "min prize", min(prizes), "max prize", max(prizes), "prizes per lottery", sorted(set(counts)), "mixed pairs", mixed)
print("pair 0:", [r for r in rows if r[0] == "0"])
print("pair 3:", [r for r in rows if r[0] == "3"])
