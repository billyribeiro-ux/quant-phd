"""Card-level diff of course/modules/E/E4/cards.json between pins 4bd8cb9 and 06994db (parsed JSON, by id).
Run from the checkout root: .venv/bin/python ledgers/E4/scripts/E4-b-r7/card_diff.py"""

import json
import subprocess


def load(rev):
    raw = subprocess.run(["git", "show", f"{rev}:course/modules/E/E4/cards.json"], capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


old = {c["id"]: c for c in load("4bd8cb94")}
new = {c["id"]: c for c in load("06994db1")}
print("old", len(old), "new", len(new))
print("added", sorted(set(new) - set(old)))
print("removed", sorted(set(old) - set(new)))
changed = sorted(i for i in old if i in new and old[i] != new[i])
print("changed", len(changed), changed)
print("unchanged", len([i for i in old if i in new and old[i] == new[i]]))
for i in changed:
    print(i, "lesson", new[i]["lesson"], "fields", sorted(k for k in set(old[i]) | set(new[i]) if old[i].get(k) != new[i].get(k)))
