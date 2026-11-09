"""Round-5 card audit for FC1-a: parse prev (edbb7aa8) and current (dde0486b) cards.json; compare per id."""
import json
import re
import sys
from collections import Counter

prev = json.load(open(sys.argv[1], encoding="utf-8"))
cur = json.load(open(sys.argv[2], encoding="utf-8"))
print("prev total", len(prev), "cur total", len(cur))
pi = {c["id"]: c for c in prev}
ci = {c["id"]: c for c in cur}
print("ids dup in cur:", [k for k, v in Counter(c["id"] for c in cur).items() if v > 1])
print("ids dup in prev:", [k for k, v in Counter(c["id"] for c in prev).items() if v > 1])
slice_lessons = {"L01", "L02", "L03"}
cur_slice = [c for c in cur if c["lesson"] in slice_lessons]
prev_slice = [c for c in prev if c["lesson"] in slice_lessons]
print("slice (L01-L03) cards prev", len(prev_slice), "cur", len(cur_slice))
print("lesson counts cur:", dict(Counter(c["lesson"] for c in cur)))
added = sorted(set(ci) - set(pi))
removed = sorted(set(pi) - set(ci))
changed = sorted(k for k in set(ci) & set(pi) if ci[k] != pi[k])
print("added:", added)
print("removed:", removed)
print("changed:", changed)
for k in changed:
    print("CHANGED", k, ci[k]["lesson"], "slice" if ci[k]["lesson"] in slice_lessons else "other")
# grade convention: which cards have grade, and grade values
print("grade values cur:", Counter(c.get("grade", "<none>") for c in cur_slice))
print("slice cards without grade:", [c["id"] for c in cur_slice if "grade" not in c])
print("keys:", Counter(tuple(sorted(c.keys())) for c in cur))
# near duplicates by normalised front (Jaccard on word sets)
def words(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))
pairs = []
for i, a in enumerate(cur_slice):
    for b in cur_slice[i + 1:]:
        wa, wb = words(a["front"]), words(b["front"])
        j = len(wa & wb) / max(1, len(wa | wb))
        if j >= 0.5:
            pairs.append((round(j, 2), a["id"], b["id"], a["front"][:80], b["front"][:80]))
for p in sorted(pairs, reverse=True):
    print("NEARDUP", p)
