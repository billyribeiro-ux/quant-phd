"""Show that the six round-2 card ids are absent from cards.json at the round-3 pin and at the round-4 pin (verifier round 4, slice e).

Run from the checkout root: python3 -I ledgers/M7/scripts/M7-e-r4/stale_ids_check.py
"""
import json
import subprocess

STALE = ["M7-c010", "M7-c048", "M7-c134", "M7-c146", "M7-c180", "M7-c188"]
PINS = {"a007712f (round-3 pin)": "a007712f", "4eb6788 (round-4 pin)": "4eb6788"}
for label, rev in PINS.items():
    raw = subprocess.run(
        ["git", "show", f"{rev}:course/modules/M/M7/cards.json"], capture_output=True, text=True, check=True
    ).stdout
    ids = {c["id"] for c in json.loads(raw)}
    print(label, "cards:", len(ids), {s: (s in ids) for s in STALE})
