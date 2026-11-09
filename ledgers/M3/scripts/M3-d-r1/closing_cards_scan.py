"""Closing-delta card scan for M3 (read-only). Prints structure, counts and duplicates."""
import collections
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    cards = json.load(fh)
print("records:", len(cards))
ids = [c["id"] for c in cards]
print("unique ids:", len(set(ids)))
keysets = collections.Counter(tuple(sorted(c.keys())) for c in cards)
for ks, n in keysets.items():
    print("keys", n, ks)
no_grade = [c["id"] for c in cards if "grade" not in c]
with_grade = [c for c in cards if "grade" in c]
with_basis = [c for c in with_grade if "basis" in c]
print("without grade:", len(no_grade))
print("with grade:", len(with_grade))
print("with grade and basis:", len(with_basis))
grades = collections.Counter(c["grade"] for c in with_grade)
print("grades:", dict(grades))
bad_basis = [c["id"] for c in with_grade if (c["grade"] == "T") == ("basis" in c)]
print("grade/basis mismatch (T with basis or non-T without basis):", bad_basis)
fronts = collections.Counter(c["front"] for c in cards)
backs = collections.Counter(c["back"] for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
print("duplicate backs:", [b for b, n in backs.items() if n > 1])
lessons = collections.Counter(c["lesson"] for c in cards)
print("per lesson:", dict(sorted(lessons.items())))
print("id range:", min(ids), max(ids))
present = {int(i.rsplit("c", 1)[1]) for i in ids}
missing = [n for n in range(1, max(present) + 1) if n not in present]
print("missing numbers:", missing)
for c in cards:
    if c["id"] in ("M3-c138", "M3-c141", "M3-c145", "M3-c174"):
        print(json.dumps(c, ensure_ascii=False, indent=1))
