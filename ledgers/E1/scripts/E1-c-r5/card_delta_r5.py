"""Verifier round 5: per-card comparison of cards.json at the round-4 pin (edbb7aa8) and the pin (dde0486b)."""
import json
import subprocess
import sys

root = sys.argv[1]
old = json.loads(subprocess.run(["git", "-C", root, "show", "edbb7aa8:course/modules/E/E1/cards.json"], capture_output=True, text=True, check=True).stdout)
new = json.loads(open(f"{root}/course/modules/E/E1/cards.json", encoding="utf-8").read())
o = {c["id"]: c for c in old}
n = {c["id"]: c for c in new}
changed = sorted(i for i in o if i in n and o[i] != n[i])
removed = sorted(i for i in o if i not in n)
added = sorted(i for i in n if i not in o)
print("changed:", changed)
print("removed:", removed)
print("added:", added)
slice_ids = [i for i in n if n[i]["lesson"] in ("L07", "L08", "L09")]
print("slice cards:", len(slice_ids), "slice cards changed:", [i for i in slice_ids if i in changed])
print("slice cards byte-identical JSON (count):", sum(1 for i in slice_ids if o.get(i) == n[i]))
