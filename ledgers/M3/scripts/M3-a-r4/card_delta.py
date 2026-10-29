"""Compare M3 cards for lessons L01-L03 between two git pins, by card id. Usage: card_delta.py <checkout> <old-pin> <new-pin>"""
import json
import subprocess
import sys

checkout, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
path = "course/modules/M/M3/cards.json"


def load(rev):
    raw = subprocess.run(["git", "-C", checkout, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


a, b = load(old), load(new)
ids_a = {c["id"]: c for c in a} if isinstance(a, list) else {c["id"]: c for c in a["cards"]}
cards_b = b if isinstance(b, list) else b["cards"]
ids_b = {c["id"]: c for c in cards_b}
print("cards old:", len(ids_a), "new:", len(ids_b))
print("added:", sorted(set(ids_b) - set(ids_a)), "removed:", sorted(set(ids_a) - set(ids_b)))
changed = sorted(k for k in ids_a if k in ids_b and ids_a[k] != ids_b[k])
print("changed:", changed)
for k in changed:
    print(k, ids_b[k].get("lesson"))
print("L01-L03 cards in new pin:", sorted(k for k, c in ids_b.items() if c.get("lesson") in ("L01", "L02", "L03")).__len__())
print("L01-L03 changed:", [k for k in changed if ids_b[k].get("lesson") in ("L01", "L02", "L03")])
print("L01-L03 added:", [k for k in set(ids_b) - set(ids_a) if ids_b[k].get("lesson") in ("L01", "L02", "L03")])
