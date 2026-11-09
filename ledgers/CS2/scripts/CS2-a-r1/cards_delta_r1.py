import json, sys
base = json.load(open(sys.argv[1], encoding="utf-8"))
head = json.load(open(sys.argv[2], encoding="utf-8"))
print("records base", len(base), "head", len(head))
bmap = {c["id"]: c for c in base}
hmap = {c["id"]: c for c in head}
print("base ids unique", len(bmap) == len(base), "head ids unique", len(hmap) == len(head))
removed = sorted(set(bmap) - set(hmap))
added = sorted(set(hmap) - set(bmap))
changed = sorted(i for i in set(bmap) & set(hmap) if bmap[i] != hmap[i])
print("removed", removed)
print("added", added)
print("changed", changed)
print("changed lessons", sorted({hmap[i]["lesson"] for i in changed}))
l14 = [i for i in hmap if hmap[i]["lesson"] in ("L01", "L02", "L03", "L04")]
print("L01-L04 records in head", len(l14), "by lesson", {l: sum(1 for i in l14 if hmap[i]["lesson"] == l) for l in ("L01","L02","L03","L04")})
print("L01-L04 changed", [i for i in l14 if i in changed])
print("L01-L04 ids base==head set", sorted(i for i in bmap if bmap[i]["lesson"] in ("L01","L02","L03","L04")) == sorted(l14))
# full scan of head
fronts = {}
violations = []
ALLOWED_GRADES = {"T", "A", "B", "C", "D", "X"}
for c in head:
    keys = set(c.keys())
    extra = keys - {"id", "lesson", "front", "back", "grade", "basis", "cite"}
    if extra:
        violations.append((c["id"], "extra keys", sorted(extra)))
    if c.get("grade") not in ALLOWED_GRADES:
        violations.append((c["id"], "grade", c.get("grade")))
    if c.get("lesson") not in {f"L{n:02d}" for n in range(1, 12)}:
        violations.append((c["id"], "lesson", c.get("lesson")))
    if c["grade"] == "T" and "basis" in c:
        violations.append((c["id"], "T with basis"))
    if c["grade"] != "T" and not c.get("basis"):
        violations.append((c["id"], "non-T without basis"))
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
    if not c["id"].startswith("CS2-c"):
        violations.append((c["id"], "id prefix"))
dupfronts = {f: ids for f, ids in fronts.items() if len(ids) > 1}
print("head violations", violations)
print("duplicate fronts", dupfronts)
ids = [c["id"] for c in head]
print("ids sorted/contiguous c001..c%03d" % len(ids), sorted(ids) == ["CS2-c%03d" % i for i in range(1, len(ids) + 1)])
from collections import Counter
print("grade counts", dict(Counter(c["grade"] for c in head)))
print("lesson counts", dict(sorted(Counter(c["lesson"] for c in head).items())))
