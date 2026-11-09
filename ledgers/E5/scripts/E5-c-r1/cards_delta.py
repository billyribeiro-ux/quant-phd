import json, sys
def load(p):
    d = json.load(open(p, encoding="utf-8"))
    cards = d if isinstance(d, list) else d.get("cards", d)
    out = {}
    for c in cards:
        out[c["id"]] = c
    return out, cards
base, bl = load(sys.argv[1])
head, hl = load(sys.argv[2])
print("base count", len(base), "head count", len(head), "list lens", len(bl), len(hl))
changed = sorted(k for k in set(base) | set(head) if base.get(k) != head.get(k))
print("changed or added or removed ids:", changed)
slice_ids = [f"E5-c{n}" for n in range(105, 131)]
print("slice ids changed:", [i for i in slice_ids if base.get(i) != head.get(i)])
print("slice ids present base/head:", sum(i in base for i in slice_ids), sum(i in head for i in slice_ids))
fronts = {}
for c in hl:
    fronts.setdefault(c.get("front"), []).append(c["id"])
dups = {k: v for k, v in fronts.items() if len(v) > 1}
print("duplicate fronts at head:", dups)
