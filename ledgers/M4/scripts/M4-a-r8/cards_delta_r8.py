"""Verifier r8: per-card delta of cards.json between pin 9373ef3 and 2d75559, plus duplicate scan (exact and near fronts)."""
import difflib
import itertools
import json
import subprocess
import sys

repo = sys.argv[1]
def load(rev):
    raw = subprocess.run(["git", "-C", repo, "show", f"{rev}:course/modules/M/M4/cards.json"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)
old = {c["id"]: c for c in load("9373ef39")}
new = {c["id"]: c for c in load("2d755599")}
print("old", len(old), "new", len(new))
for cid in sorted(set(old) | set(new)):
    if cid not in old:
        print("ADDED", cid, new[cid]["lesson"])
    elif cid not in new:
        print("REMOVED", cid, old[cid]["lesson"])
    elif old[cid] != new[cid]:
        print("CHANGED", cid, new[cid]["lesson"], sorted(k for k in set(old[cid]) | set(new[cid]) if old[cid].get(k) != new[cid].get(k)))
cards = list(new.values())
fronts = [c["front"].strip().lower() for c in cards]
backs = [c["back"].strip().lower() for c in cards]
print("dup fronts", [f for f in set(fronts) if fronts.count(f) > 1])
print("dup backs", [b for b in set(backs) if backs.count(b) > 1])
near = []
for a, b in itertools.combinations(cards, 2):
    r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
    if r >= 0.7:
        near.append((round(r, 2), a["id"], b["id"], a["front"], b["front"]))
for n in sorted(near, reverse=True):
    print("NEAR-FRONT", n)
