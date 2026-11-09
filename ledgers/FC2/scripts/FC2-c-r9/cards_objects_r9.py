import json, sys
prev = json.load(open(sys.argv[1], encoding="utf-8"))
cur = json.load(open(sys.argv[2], encoding="utf-8"))
pm = {c["id"]: c for c in prev}
cm = {c["id"]: c for c in cur}
for L in ("L07", "L08"):
    pids = [c["id"] for c in prev if c["lesson"] == L]
    cids = [c["id"] for c in cur if c["lesson"] == L]
    same = all(pm[i] == cm[i] for i in pids)
    print(f"{L}: prev {len(pids)} cards, now {len(cids)} cards, all previous objects identical: {same}")
    print(f"  now: {' '.join(cids)}")
    print(f"  added: {[i for i in cids if i not in pids]}  removed: {[i for i in pids if i not in cids]}")
changed = [i for i in pm if i in cm and pm[i] != cm[i]]
print("changed previous objects (all lessons):", changed)
print("added objects (all lessons):", [i for i in cm if i not in pm])
