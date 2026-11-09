import json, sys, collections
prev = json.load(open(sys.argv[1], encoding="utf-8"))
head = json.load(open(sys.argv[2], encoding="utf-8"))
def norm(x): return " ".join(x.strip().lower().split())
print("cards prev", len(prev), "head", len(head))
pid = {c["id"]: c for c in prev}; hid = {c["id"]: c for c in head}
print("ids unique prev", len(pid) == len(prev), "head", len(hid) == len(head))
print("removed ids", sorted(set(pid) - set(hid)))
print("added ids", sorted(set(hid) - set(pid)))
changed = sorted(i for i in set(pid) & set(hid) if pid[i] != hid[i])
print("changed ids", changed)
for lesson in ("L07", "L08"):
    ids_prev = [c["id"] for c in prev if c["lesson"] == lesson]
    ids_head = [c["id"] for c in head if c["lesson"] == lesson]
    same = all(pid[i] == hid[i] for i in ids_head)
    print(lesson, "count prev", len(ids_prev), "head", len(ids_head), "identical objects", same and ids_prev == ids_head)
    for i in ids_head:
        if pid[i] != hid[i]:
            print("  CHANGED", i)
    print(" ", lesson, "ids:", ids_head[0], "...", ids_head[-1])
fronts = collections.Counter(norm(c["front"]) for c in head)
backs = collections.Counter(norm(c["back"]) for c in head)
print("dup fronts", sum(1 for k, v in fronts.items() if v > 1), "dup backs", sum(1 for k, v in backs.items() if v > 1))
print("cards with 0.0266/0.0267/0.000266/0.000267:", [c["id"] for c in head if any(s in json.dumps(c, ensure_ascii=False) for s in ("0.0266", "0.0267", "0.000266", "0.000267"))])
print("cards with lesson L08 mentioning volatility points:", [c["id"] for c in head if "volatility point" in json.dumps(c, ensure_ascii=False)])
print("all card keys:", sorted({k for c in head for k in c}))
print("ids sorted order sample:", [c["id"] for c in head][-5:])
