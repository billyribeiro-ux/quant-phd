"""Full scan of cards.json for duplicate ids, duplicate fronts and backs (normalised), and field shape.

Usage: python -I cards_scan.py <module dir>
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

cards = json.loads((Path(sys.argv[1]) / "cards.json").read_text(encoding="utf-8"))


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(norm(c["front"]) for c in cards)
backs = collections.Counter(norm(c["back"]) for c in cards)
print("cards", len(cards), "unique ids", len(ids), "duplicate ids", [i for i, n in ids.items() if n > 1])
print("duplicate fronts", [f for f, n in fronts.items() if n > 1])
print("duplicate backs", [b[:60] for b, n in backs.items() if n > 1])
print("field shapes", dict(collections.Counter(tuple(sorted(c)) for c in cards)))
print("grades", dict(collections.Counter(c.get("grade", "-") for c in cards)))
print("lessons", dict(collections.Counter(c["lesson"] for c in cards)))
