"""Extract the M3 retrieval cards for lessons L07-L09 and check duplicate ids and fronts.

Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-c-r10/cards_extract.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

cards = json.loads(Path("course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
fronts = Counter(c["front"] for c in cards)
print(f"total cards {len(cards)}; duplicate ids {sum(1 for v in ids.values() if v > 1)}; duplicate fronts {sum(1 for v in fronts.values() if v > 1)}")
slice_cards = [c for c in cards if c["lesson"] in ("L07", "L08", "L09")]
print(f"slice cards {len(slice_cards)}")
for c in slice_cards:
    print(f"{c['id']} | {c['lesson']} | grade {c.get('grade')} | basis {c.get('basis', '-')}")
    print(f"  F: {c['front']}")
    print(f"  B: {c['back']}")
