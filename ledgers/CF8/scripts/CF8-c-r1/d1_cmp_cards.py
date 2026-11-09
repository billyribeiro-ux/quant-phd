import json, sys
base = json.load(open(sys.argv[1], encoding="utf-8"))
head = json.load(open(sys.argv[2], encoding="utf-8"))
def norm(d):
    if isinstance(d, dict) and "cards" in d:
        d = d["cards"]
    return d
b = norm(base); h = norm(head)
print("type", type(base).__name__, type(head).__name__, "n", len(b), len(h))
bi = {c["id"]: c for c in b}; hi = {c["id"]: c for c in h}
print("ids base", len(bi), "head", len(hi), "unique head", len(set(c["id"] for c in h)))
print("removed", sorted(set(bi)-set(hi)))
print("added", sorted(set(hi)-set(bi)))
changed = sorted(k for k in bi if k in hi and bi[k] != hi[k])
print("changed", len(changed), changed)
for k in changed:
    diffs = [f for f in set(bi[k])|set(hi[k]) if bi[k].get(f)!=hi[k].get(f)]
    print(k, sorted(diffs))
