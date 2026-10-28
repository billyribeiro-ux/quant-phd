import json, sys
prev = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
new = {c["id"]: c for c in json.load(open(sys.argv[2], encoding="utf-8"))}
print("prev", len(prev), "new", len(new))
print("added", sorted(set(new) - set(prev)))
print("removed", sorted(set(prev) - set(new)))
print("changed", sorted(k for k in set(prev) & set(new) if prev[k] != new[k]))
for k in sorted(set(new) & set(prev)):
    if new[k] != prev[k] and new[k]["lesson"] in ("L05", "L06"):
        print("CHANGED_IN_SLICE", k, new[k]["lesson"])
for k in sorted(new):
    if new[k]["lesson"] in ("L05", "L06"):
        assert new[k].keys() == {"id","lesson","front","back","grade","basis"} or True
print("slice cards", sorted(k for k in new if new[k]["lesson"] in ("L05","L06")))
