"""Verifier round 5: compare slice cards (L05-L08) between the round-4 pin and this pin, object by object.
Usage: python3 -I cards_delta_r5.py <checkout> <old_cards.json> <new_cards.json>"""
import json
import sys

root, old_p, new_p = sys.argv[1], sys.argv[2], sys.argv[3]
old = json.load(open(old_p, encoding="utf-8"))
new = json.load(open(new_p, encoding="utf-8"))
sl = lambda cs: [c for c in cs if c["lesson"] in ("L05", "L06", "L07", "L08")]
o, n = sl(old), sl(new)
oi = {c["id"]: c for c in o}
ni = {c["id"]: c for c in n}
print("old slice", len(o), "new slice", len(n))
print("removed:", sorted(set(oi) - set(ni)))
print("added:", sorted(set(ni) - set(oi)))
changed = sorted(k for k in set(oi) & set(ni) if oi[k] != ni[k])
print("changed:", changed)
print("unchanged:", len([k for k in set(oi) & set(ni) if oi[k] == ni[k]]))
print("order preserved for unchanged:", [c["id"] for c in n if c["id"] in oi and oi[c["id"]] == c] == [c["id"] for c in o if c["id"] in ni and oi[c["id"]] == ni[c["id"]]])
