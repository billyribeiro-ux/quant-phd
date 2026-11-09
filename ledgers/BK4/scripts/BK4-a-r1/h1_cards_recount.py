import json
import sys
from collections import Counter, defaultdict

path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
ids = [c["id"] for c in cards]
print("total cards:", len(cards))
print("duplicate ids:", [i for i, n in Counter(ids).items() if n > 1])
print("duplicate fronts:", [f for f, n in Counter(c["front"] for c in cards).items() if n > 1])
print("duplicate backs:", [b[:40] for b, n in Counter(c["back"] for c in cards).items() if n > 1])
by = defaultdict(list)
for c in cards:
    by[c["lesson"]].append(c["id"])
for lesson in sorted(by):
    print(lesson, len(by[lesson]), " ".join(sorted(by[lesson])))
l13 = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("L01-L03 total:", len(l13))
print("L01-L03 id numbers min/max:", min(int(c["id"].split("c")[-1]) for c in l13), max(int(c["id"].split("c")[-1]) for c in l13))
print("keys:", sorted({k for c in cards for k in c}))
print("cards without grade key:", [c["id"] for c in cards if "grade" not in c])
print("cards whose id prefix differs from BK4-c:", [c["id"] for c in cards if not c["id"].startswith("BK4-c")])
