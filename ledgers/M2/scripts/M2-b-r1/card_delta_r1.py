# Round-1 closing delta: per-card identity, duplicates, and slice membership for M2 cards.json (old = e896b7a4, new = 95f3f8cb).
import json, sys, collections, difflib
S = "ledgers/M2/scripts/M2-b-r1/"
old = json.load(open(S + "cards_base_e896b7a4.json", encoding="utf-8"))
new = json.load(open(S + "cards_head_95f3f8cb.json", encoding="utf-8"))
SLICE = {"L07", "L08", "L09", "L10", "L11", "L12"}
print("cards old", len(old), "new", len(new))
oi = {c["id"]: c for c in old}; ni = {c["id"]: c for c in new}
print("dup ids new", [k for k, v in collections.Counter(c["id"] for c in new).items() if v > 1] or "none")
norm = lambda s: " ".join(s.split()).lower()
print("removed", sorted(set(oi) - set(ni)))
print("added", sorted(set(ni) - set(oi)))
changed = sorted(k for k in set(oi) & set(ni) if oi[k] != ni[k])
print("changed", len(changed), changed)
print("changed in slice:", [(k, ni[k]["lesson"]) for k in changed if ni[k]["lesson"] in SLICE])
print("changed out of slice:", [(k, ni[k]["lesson"]) for k in changed if ni[k]["lesson"] not in SLICE])
print("removed in slice:", [(k, oi[k]["lesson"]) for k in sorted(set(oi) - set(ni)) if oi[k]["lesson"] in SLICE])
print("added in slice:", [(k, ni[k]["lesson"]) for k in sorted(set(ni) - set(oi)) if ni[k]["lesson"] in SLICE])
print("added out of slice:", [(k, ni[k]["lesson"]) for k in sorted(set(ni) - set(oi)) if ni[k]["lesson"] not in SLICE])
slice_new = [c for c in new if c["lesson"] in SLICE]
print("slice cards new", len(slice_new), dict(collections.Counter(c["lesson"] for c in slice_new)))
print("slice cards in base", len([c for c in old if c["lesson"] in SLICE]))
print("identical slice cards (carry):", sorted(k for k in ni if ni[k]["lesson"] in SLICE and k in oi and oi[k] == ni[k]) and len([k for k in ni if ni[k]["lesson"] in SLICE and k in oi and oi[k] == ni[k]]))
print("keys", sorted({k for c in new for k in c}))
print("grade values", collections.Counter(c.get("grade", "<none>") for c in new))
print("--- duplicate fronts (normalized) ---")
fr = collections.Counter(norm(c["front"]) for c in new)
print([k for k, v in fr.items() if v > 1] or "none")
print("--- near-duplicate fronts (ratio>=0.8) ---")
pairs = []
ids = [c["id"] for c in new]
for i in range(len(new)):
    for j in range(i + 1, len(new)):
        r = difflib.SequenceMatcher(None, norm(new[i]["front"]), norm(new[j]["front"])).ratio()
        if r >= 0.8:
            pairs.append((round(r, 2), new[i]["id"], new[j]["id"], new[i]["front"][:90], new[j]["front"][:90]))
for p in sorted(pairs, reverse=True):
    print(p)
print("--- near-duplicate backs (ratio>=0.8) ---")
bp = []
for i in range(len(new)):
    for j in range(i + 1, len(new)):
        r = difflib.SequenceMatcher(None, norm(new[i]["back"]), norm(new[j]["back"])).ratio()
        if r >= 0.8:
            bp.append((round(r, 2), new[i]["id"], new[j]["id"]))
print(sorted(bp, reverse=True) or "none")
