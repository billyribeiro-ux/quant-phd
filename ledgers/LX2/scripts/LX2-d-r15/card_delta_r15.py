"""Per-object comparison of cards.json between the round-13 pin (e919577b) and the current pin.

Usage: python3 -I card_delta_r15.py <old_cards.json> <new_cards.json>
Prints ids added, removed and changed (byte-identical JSON objects are not listed as changed).
"""
import json
import sys

old = {c["id"]: c for c in json.load(open(sys.argv[1], encoding="utf-8"))}
new = {c["id"]: c for c in json.load(open(sys.argv[2], encoding="utf-8"))}
print("old", len(old), "new", len(new))
print("added:", sorted(set(new) - set(old)))
print("removed:", sorted(set(old) - set(new)))
changed = sorted(i for i in set(old) & set(new) if json.dumps(old[i], ensure_ascii=False, sort_keys=True) != json.dumps(new[i], ensure_ascii=False, sort_keys=True))
print("changed:", changed)
print("unchanged:", len(set(old) & set(new)) - len(changed))
