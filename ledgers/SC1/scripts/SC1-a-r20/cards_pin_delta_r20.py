"""SC1-a round 20: compare every L01-L03 card between the previous pin (cd4dd7df) and the current pin (d1083bf1).
Usage (checkout root): python3 -I ledgers/SC1/scripts/SC1-a-r20/cards_pin_delta_r20.py"""
import json
import subprocess

def load(rev):
    raw = subprocess.run(["git", "show", f"{rev}:course/modules/SC/SC1/cards.json"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)

old = {c["id"]: c for c in load("cd4dd7df")}
new = {c["id"]: c for c in load("d1083bf1")}
print("old cards", len(old), "new cards", len(new))
print("ids only in old:", sorted(set(old) - set(new)))
print("ids only in new:", sorted(set(new) - set(old)))
changed = sorted(i for i in new if i in old and old[i] != new[i])
print("changed card ids (all lessons):", changed)
for i in changed:
    print(i, new[i]["lesson"], "fields changed:", sorted(k for k in set(old[i]) | set(new[i]) if old[i].get(k) != new[i].get(k)))
l123_changed = [i for i in changed if new[i]["lesson"] in ("L01", "L02", "L03")]
print("L01-L03 changed:", l123_changed)
