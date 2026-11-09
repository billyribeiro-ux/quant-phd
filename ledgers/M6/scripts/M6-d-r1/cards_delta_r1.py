import json, sys
base = json.load(open(sys.argv[1]))
head = json.load(open(sys.argv[2]))
bi = {c["id"]: c for c in base}
hi = {c["id"]: c for c in head}
print("base cards", len(base), "head cards", len(head))
print("base dup ids", len(base) - len(bi), "head dup ids", len(head) - len(hi))
print("removed", sorted(set(bi) - set(hi)))
print("added", sorted(set(hi) - set(bi)))
changed = sorted(k for k in set(bi) & set(hi) if bi[k] != hi[k])
print("changed", len(changed), changed)
same = sorted(k for k in set(bi) & set(hi) if bi[k] == hi[k])
print("identical", len(same))
print("head order ids", [c["id"] for c in head][:3], "...", [c["id"] for c in head][-3:])
fronts = {}
for c in head:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
print("duplicate fronts", [v for v in fronts.values() if len(v) > 1])
