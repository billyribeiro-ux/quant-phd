"""Record-level diff of cards.json for lessons L07-L12 between two git revisions (argv: rev_old rev_new).

Run from the checkout root. Prints the card ids whose JSON record changed, and the per-lesson card counts."""
import json
import subprocess
import sys

def load(rev: str) -> dict:
    raw = subprocess.run(["git", "show", f"{rev}:course/modules/M/M2/cards.json"], capture_output=True,
                         text=True, check=True).stdout
    return {c["id"]: c for c in json.loads(raw)}

old, new = load(sys.argv[1]), load(sys.argv[2])
print("old", len(old), "new", len(new), "removed", sorted(set(old) - set(new)), "added", sorted(set(new) - set(old)))
changed = sorted(k for k in old if k in new and old[k] != new[k])
print("changed records:", changed)
for L in ["L07", "L08", "L09", "L10", "L11", "L12"]:
    print(L, "cards", sum(1 for c in new.values() if c["lesson"] == L), "changed", [k for k in changed if new[k]["lesson"] == L])
