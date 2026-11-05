"""Extract the L07-L09 cards and check duplicates (round 9). Run from the checkout root with .venv/bin/python -I."""

import json
from pathlib import Path

cards = json.loads(Path("course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
print("total cards", len(cards))
ids = [c["id"] for c in cards]
fronts = [c["front"] for c in cards]
print("dup ids", len(ids) - len(set(ids)), "dup fronts", len(fronts) - len(set(fronts)))
sel = [c for c in cards if c["lesson"] in ("L07", "L08", "L09")]
print("slice cards", len(sel))
for c in sel:
    extra = {k: v for k, v in c.items() if k not in ("id", "lesson", "front", "back", "grade", "basis")}
    print(c["id"], c["lesson"], c.get("grade"), "|", c["front"], "|| BACK:", c["back"], "|| BASIS:", c.get("basis"), "|| KEYS:", extra)
    print()
