import json, sys
base = json.load(open(sys.argv[1]))
head = json.load(open(sys.argv[2]))
print("counts base", len(base), "head", len(head))
bi = {c["id"]: c for c in base}
hi = {c["id"]: c for c in head}
print("dup ids base", len(base) - len(bi), "head", len(head) - len(hi))
removed = sorted(set(bi) - set(hi))
added = sorted(set(hi) - set(bi))
changed = sorted(k for k in set(bi) & set(hi) if bi[k] != hi[k])
print("REMOVED", removed)
print("ADDED", added)
print("CHANGED", changed)
for k in changed:
    b, h = bi[k], hi[k]
    keys = set(b) | set(h)
    diffs = [f for f in sorted(keys) if b.get(f) != h.get(f)]
    print(k, b.get("lesson"), h.get("lesson"), "fields:", diffs, "grade", b.get("grade"), "->", h.get("grade"))
for k in added:
    print("ADD", json.dumps(hi[k], ensure_ascii=False))
for k in removed:
    print("REM", json.dumps(bi[k], ensure_ascii=False))
