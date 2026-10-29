import json, sys, pathlib, collections
root = pathlib.Path(sys.argv[1]); S = pathlib.Path(sys.argv[2])
new = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
old = json.loads((S / "cards_r6_pin.json").read_text(encoding="utf-8"))
ob = {c["id"]: c for c in old}; nb = {c["id"]: c for c in new}
print("old count", len(old), "new count", len(new))
print("ids only in old:", sorted(set(ob) - set(nb)))
print("ids only in new:", sorted(set(nb) - set(ob)))
changed = sorted(i for i in set(ob) & set(nb) if ob[i] != nb[i])
print("changed:", changed)
for i in changed:
    print(" ", i, nb[i]["lesson"])
# duplicates
fr = collections.Counter(c["front"].strip().lower() for c in new)
bk = collections.Counter(c["back"].strip().lower() for c in new)
print("dup fronts:", [k for k, v in fr.items() if v > 1])
print("dup backs:", [k[:60] for k, v in bk.items() if v > 1])
ids = collections.Counter(c["id"] for c in new)
print("dup ids:", [k for k, v in ids.items() if v > 1])
by = collections.defaultdict(list)
for c in new: by[c["lesson"]].append(c["id"])
for l in ["L13","L14","L15","L16","L17","L18"]:
    print(l, len(by[l]), by[l][0], by[l][-1])
