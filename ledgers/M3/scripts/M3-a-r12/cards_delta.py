"""Compare M3 cards.json at round-11 pin and round-12 pin; list changed/new/removed cards and duplicate fronts or backs."""
import json
import sys
from collections import Counter

old = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
new_list = json.load(open(sys.argv[2], encoding="utf-8"))
new = {c["id"]: c for c in new_list}
print("cards old", len(old), "new", len(new_list), "unique new ids", len(new))
for cid in sorted(set(old) | set(new)):
    if cid not in old:
        print("NEW", cid, new[cid]["lesson"])
    elif cid not in new:
        print("REMOVED", cid)
    elif old[cid] != new[cid]:
        print("CHANGED", cid, new[cid]["lesson"])
norm = lambda s: " ".join(s.lower().split())
for key in ("front", "back"):
    cnt = Counter(norm(c[key]) for c in new_list)
    for text, n in cnt.items():
        if n > 1:
            print("DUP", key, n, [c["id"] for c in new_list if norm(c[key]) == text])
lessons = Counter(c["lesson"] for c in new_list if c["id"].startswith("M3-"))
print("M3 cards per lesson in new:", dict(sorted(lessons.items())))
