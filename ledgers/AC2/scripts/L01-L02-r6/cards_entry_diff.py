"""Entry-level comparison of cards.json at 11b3477 and at HEAD (run after git show 11b3477:... > cards_r5.json)."""
import json
import sys

old = json.load(open(sys.argv[1], encoding="utf-8"))
new = json.load(open(sys.argv[2], encoding="utf-8"))
old = old if isinstance(old, list) else old.get("cards", old)
new = new if isinstance(new, list) else new.get("cards", new)
od = {c["id"]: c for c in old}
nd = {c["id"]: c for c in new}
print("counts:", len(old), len(new))
print("changed:", sorted(i for i in od if od[i] != nd.get(i)))
l12 = [c["id"] for c in new if c["lesson"] in ("L01", "L02")]
print("L01/L02 ids:", len(l12), "changed:", [i for i in l12 if od.get(i) != nd.get(i)])
