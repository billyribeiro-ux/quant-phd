"""Verifier round 4: every <dfn id> in the CS2 slice is unique across the unit; every concept link resolves.

Usage: python3 -I dfn_links_r4.py <checkout>
"""
import re
import sys
from collections import Counter

root = sys.argv[1]
unit = f"{root}/course/modules/CS/CS2"
dfn_ids = Counter()
where = {}
for n in range(1, 12):
    src = open(f"{unit}/L{n:02d}.html", encoding="utf-8").read()
    for m in re.finditer(r'<dfn id="([^"]+)" data-concept="([^"]+)"', src):
        dfn_ids[m.group(1)] += 1
        where.setdefault(m.group(1), []).append(f"L{n:02d}")
print("unit dfn ids:", len(dfn_ids), "duplicated:", [k for k, v in dfn_ids.items() if v > 1])
for n in (5, 6, 7, 8):
    src = open(f"{unit}/L{n:02d}.html", encoding="utf-8").read()
    dfns = re.findall(r'<dfn id="([^"]+)"', src)
    print(f"L{n:02d} dfn:", dfns)
    links = re.findall(r'<a class="concept" data-concept="([^"]+)"[^>]*href="([^"]+)"', src)
    links2 = re.findall(r'href="([^"]*#def-[^"]+)"', src)
    print(f"L{n:02d} concept links:", sorted(set(h for _, h in links) | set(links2)))
