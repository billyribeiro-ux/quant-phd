"""Round-4 structural scan of course/modules/E/E4/cards.json (slice e).

Usage: python -I card_scan_r4.py <cards.json>
Checks: count, unique ids, id format, grade values, lesson values, duplicate fronts/backs (normalised),
near-duplicate fronts (difflib ratio >= 0.85 within the same lesson), and per-lesson counts.
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9α-ωσ]+", " ", s.lower())).strip()


def main() -> None:
    cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print("cards", len(cards))
    ids = [c["id"] for c in cards]
    print("unique ids", len(set(ids)) == len(ids), "format ok", all(re.fullmatch(r"E4-c\d{3}", i) for i in ids))
    print("grades", Counter(c.get("grade") for c in cards))
    print("lessons", sorted(Counter(c["lesson"] for c in cards).items()))
    fronts = Counter(norm(c["front"]) for c in cards)
    backs = Counter(norm(c["back"]) for c in cards)
    print("duplicate normalised fronts", [k for k, v in fronts.items() if v > 1])
    print("duplicate normalised backs", [k for k, v in backs.items() if v > 1])
    near = []
    for i, a in enumerate(cards):
        for b in cards[i + 1 :]:
            if a["lesson"] != b["lesson"]:
                continue
            r = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
            if r >= 0.85:
                near.append((a["id"], b["id"], round(r, 3)))
    print("near-duplicate fronts (same lesson, ratio>=0.85)", near)
    empty = [c["id"] for c in cards if not c["front"].strip() or not c["back"].strip()]
    print("empty front/back", empty)
    ungraded_but_claim = [
        c["id"] for c in cards if c.get("grade") in ("T", "C") and not (c.get("basis") or c.get("cite"))
    ]
    print("T/C cards without basis or cite", ungraded_but_claim)


if __name__ == "__main__":
    main()
