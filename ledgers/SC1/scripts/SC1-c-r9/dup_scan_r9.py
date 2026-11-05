"""Duplicate scan over course/modules/SC/SC1/cards.json (round 9, SC1 slice c).

Reports: duplicate ids; exact duplicate fronts or backs; pairs of cards in the same lesson whose
fronts share a token-set Jaccard similarity of at least 0.6 (near-duplicates); and every card whose
lesson is L07 or L08, with the count of each.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[A-Za-zΑ-Ωα-ω0-9]+", text.lower()))


def main() -> None:
    root = Path(__file__).resolve().parents[4]
    cards = json.loads((root / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
    ids = Counter(c["id"] for c in cards)
    print(f"cards: {len(cards)}; duplicate ids: {[i for i, n in ids.items() if n > 1]}")
    fronts = Counter(c["front"] for c in cards)
    backs = Counter(c["back"] for c in cards)
    print(f"exact duplicate fronts: {[f[:60] for f, n in fronts.items() if n > 1]}")
    print(f"exact duplicate backs: {[b[:60] for b, n in backs.items() if n > 1]}")
    near = []
    for i, a in enumerate(cards):
        for b in cards[i + 1 :]:
            if a.get("lesson") != b.get("lesson"):
                continue
            ta, tb = tokens(a["front"]), tokens(b["front"])
            if not ta or not tb:
                continue
            jac = len(ta & tb) / len(ta | tb)
            if jac >= 0.6:
                near.append((round(jac, 2), a["id"], b["id"]))
    print(f"same-lesson front pairs with Jaccard >= 0.6: {sorted(near)}")
    sel = Counter(c.get("lesson") for c in cards if c.get("lesson") in ("L07", "L08"))
    print(f"L07/L08 cards: {dict(sel)}")
    for c in cards:
        if c.get("lesson") in ("L07", "L08"):
            print(c["id"], c["lesson"], "grade" in c, "basis" in c, c.get("grade", "-"))


if __name__ == "__main__":
    main()
