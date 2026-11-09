import json, sys
old = json.load(open(sys.argv[1], encoding="utf-8"))
new = json.load(open(sys.argv[2], encoding="utf-8"))
print("count old", len(old), "new", len(new))
def key(c):
    return c.get("id")
o = {key(c): c for c in old}
n = {key(c): c for c in new}
print("ids only old", sorted(set(o) - set(n)), "ids only new", sorted(set(n) - set(o)))
print("order same:", [key(c) for c in old] == [key(c) for c in new])
changed = []
for k in n:
    if k in o and o[k] != n[k]:
        fields = [f for f in set(o[k]) | set(n[k]) if o[k].get(f) != n[k].get(f)]
        changed.append((k, sorted(fields)))
print("changed cards:", len(changed))
for k, f in changed:
    print(k, f, n[k].get("lesson", n[k].get("module", "")), n[k].get("type", ""))
