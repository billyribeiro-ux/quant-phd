# Round-6: per-card identity and slice-lesson checks for M2 cards.json (old = dde0486b, new = e896b7a4).
import json, sys, collections
old = json.load(open(sys.argv[1], encoding="utf-8"))
new = json.load(open(sys.argv[2], encoding="utf-8"))
print("cards old", len(old), "new", len(new))
oi = {c["id"]: c for c in old}; ni = {c["id"]: c for c in new}
print("dup ids old", [k for k, v in collections.Counter(oi).items() if v > 1] if len(oi) != len(old) else "none")
print("dup ids new", [k for k, v in collections.Counter(c["id"] for c in new).items() if v > 1] or "none")
norm = lambda s: " ".join(s.split()).lower()
fr = collections.Counter(norm(c["front"]) for c in new)
print("dup fronts new", [k for k, v in fr.items() if v > 1] or "none")
print("removed", sorted(set(oi) - set(ni)) or "none")
print("added", sorted(set(ni) - set(oi)) or "none")
changed = sorted(k for k in set(oi) & set(ni) if oi[k] != ni[k])
print("changed", changed)
for k in changed:
    print(" ", k, "lesson", ni[k]["lesson"], "in-slice(L07-L12)" if ni[k]["lesson"] in {"L07","L08","L09","L10","L11","L12"} else "out-of-slice")
slice_ids = [c["id"] for c in new if c["lesson"] in {"L07","L08","L09","L10","L11","L12"}]
print("slice cards new", len(slice_ids), "by lesson", dict(collections.Counter(c["lesson"] for c in new if c["lesson"] in {"L07","L08","L09","L10","L11","L12"})))
print("slice cards identical to dde0486b:", sum(1 for k in slice_ids if k in oi and oi[k] == ni[k]), "of", len(slice_ids))
print("slice cards changed or added:", [k for k in slice_ids if k not in oi or oi[k] != ni[k]])
print("keys new", sorted({tuple(sorted(c.keys())) for c in new}, key=len))
