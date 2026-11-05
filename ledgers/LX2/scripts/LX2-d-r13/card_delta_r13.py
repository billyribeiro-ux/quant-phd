"""Round 13: per-card byte comparison of cards.json between the round-12 pin (5db69a9) and the current pin.
Usage: python3 -I card_delta_r13.py <old_cards.json> <new_cards.json>"""
import json, sys
old = json.load(open(sys.argv[1], encoding="utf-8"))
new = json.load(open(sys.argv[2], encoding="utf-8"))
o = {c["id"]: json.dumps(c, sort_keys=True, ensure_ascii=False) for c in old}
n = {c["id"]: json.dumps(c, sort_keys=True, ensure_ascii=False) for c in new}
print("ids old:", len(o), "ids new:", len(n), "same id set:", set(o) == set(n))
print("order same:", [c["id"] for c in old] == [c["id"] for c in new])
changed = sorted(i for i in o if i in n and o[i] != n[i])
print("changed entries:", changed)
