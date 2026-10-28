# Compares the L05/L06 cards of the previous pin (cef676e, copied to scratch) with the current cards.json (run -I).
import json, sys
prev = json.load(open(sys.argv[1], encoding="utf-8"))
cur = json.load(open(sys.argv[2], encoding="utf-8"))
prev = prev if isinstance(prev, list) else prev.get("cards", prev)
cur = cur if isinstance(cur, list) else cur.get("cards", cur)
pm = {c["id"]: c for c in prev}
cm = {c["id"]: c for c in cur}
changed = sorted(k for k in set(pm) | set(cm) if pm.get(k) != cm.get(k))
print("changed ids:", changed)
l56 = [k for k, c in cm.items() if c["lesson"] in ("L05", "L06")]
print("L05/L06 cards in current:", len(l56), "changed among them:", [k for k in changed if k in l56])
print("all cards:", len(cm), "unique ids:", len(cur) == len(cm))
