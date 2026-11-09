"""Round-14 check: cards.json changes against the round-13 pin e919577 (SC1 slice b cards are L04-L06)."""

from __future__ import annotations

import json
import subprocess
import sys

ROOT = sys.argv[1]
old_text = subprocess.run(
    ["git", "-C", ROOT, "show", "e919577:course/modules/SC/SC1/cards.json"], check=True, capture_output=True, text=True
).stdout
old = {c["id"]: c for c in json.loads(old_text)}
with open(f"{ROOT}/course/modules/SC/SC1/cards.json", encoding="utf-8") as fh:
    new = {c["id"]: c for c in json.load(fh)}
print("added:", sorted(set(new) - set(old)))
print("removed:", sorted(set(old) - set(new)))
changed = sorted(i for i in new if i in old and new[i] != old[i])
print("changed:", changed)
print("changed in slice b (L04-L06):", [i for i in changed if new[i]["lesson"] in ("L04", "L05", "L06")])
print("added in slice b (L04-L06):", [i for i in set(new) - set(old) if new[i]["lesson"] in ("L04", "L05", "L06")])
