"""Slice e check: structural scan of cards.json (ids, duplicates, lesson coverage, grades, cite keys, basis).

Usage: python -I card_scan.py <cards.json> <references.json>
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


def normal(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def main() -> None:
    cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    registry = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    keys = {entry["key"] for entry in registry["entries"]}
    print(f"cards={len(cards)}")
    print("ids sequential E4-c001..:", all(c["id"] == f"E4-c{i:03d}" for i, c in enumerate(cards, 1)))
    for field in ("id", "front", "back"):
        dup = [v for v, n in Counter(c[field] for c in cards).items() if n > 1]
        print(f"duplicate {field}: {len(dup)}")
    print("duplicate normalised front:", sum(1 for n in Counter(normal(c["front"]) for c in cards).values() if n > 1))
    print("cards per lesson:", dict(sorted(Counter(c["lesson"] for c in cards).items())))
    print("grade counts:", dict(Counter(c.get("grade", "-") for c in cards)))
    bad_keys = [(c["id"], k) for c in cards for k in c.get("cite", []) if k not in keys]
    print("cite keys:", [c["id"] + ":" + k for c in cards for k in c.get("cite", [])], "unknown:", bad_keys)
    no_basis = [c["id"] for c in cards if c.get("grade") in ("T", "C") and not c.get("basis")]
    print("graded cards without basis:", no_basis)
    keysets = Counter(tuple(sorted(c)) for c in cards)
    print("field sets:", {", ".join(k): v for k, v in keysets.items()})


if __name__ == "__main__":
    main()
