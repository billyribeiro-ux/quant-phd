import json, sys
old = json.load(open(sys.argv[1], encoding="utf-8"))
new = json.load(open(sys.argv[2], encoding="utf-8"))
def idx(cards):
    d = {}
    for c in cards:
        if c["id"] in d:
            print("DUP ID", c["id"])
        d[c["id"]] = c
    return d
o, n = idx(old), idx(new)
print("counts old", len(o), "new", len(n))
print("added", sorted(set(n) - set(o)))
print("removed", sorted(set(o) - set(n)))
changed = sorted(k for k in set(o) & set(n) if o[k] != n[k])
print("changed", changed)
for k in changed:
    fields = [f for f in set(o[k]) | set(n[k]) if o[k].get(f) != n[k].get(f)]
    print(k, o[k]["lesson"], "->", n[k]["lesson"], "fields:", sorted(fields))
fronts = [c["front"] for c in new]
print("dup fronts", len(fronts) - len(set(fronts)))
print("lesson counts in-slice (L05-L08) at new:", sum(1 for c in new if c["lesson"] in ("L05","L06","L07","L08")))
print("lesson counts in-slice (L05-L08) at old:", sum(1 for c in old if c["lesson"] in ("L05","L06","L07","L08")))
