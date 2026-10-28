import json, sys
a = {c["id"]: c for c in json.load(open(sys.argv[1]))}
b = {c["id"]: c for c in json.load(open(sys.argv[2]))}
ch = [k for k in a if k in b and a[k] != b[k]]
print("removed", sorted(set(a) - set(b)), "added", sorted(set(b) - set(a)))
print("changed", [(k, b[k]["lesson"]) for k in ch if b[k]["lesson"] in ("L07", "L08")])
