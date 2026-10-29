"""Round-3 scan of course/modules/E/E3/cards.json: schema, id uniqueness, duplicates, number tokens against the
card's own lesson text, and cross-references (Definition/Proposition/... N) against the card's lesson.

Usage (from the checkout): .venv/bin/python ledgers/E3/scripts/E3-d-r3/cards_scan.py
"""

from __future__ import annotations

import difflib
import json
import re
from html.parser import HTMLParser
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "course" / "modules" / "E" / "E3"
LESSONS = ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]


class _Text(HTMLParser):
    """Visible text with a real HTML parser. A regex that strips <...> would swallow text after a bare '<' such as 'x < 0'."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def lesson_text(name: str) -> str:
    raw = (BASE / f"{name}.html").read_text(encoding="utf-8")
    parser = _Text()
    parser.feed(raw)
    parser.close()
    return re.sub(r"\s+", " ", " ".join(parser.parts))


def main() -> None:
    cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))
    texts = {k: lesson_text(k) for k in LESSONS}
    print("cards:", len(cards))
    keys = Counter(tuple(sorted(c.keys())) for c in cards)
    print("key sets:", dict(keys))
    ids = Counter(c["id"] for c in cards)
    print("duplicate ids:", [i for i, n in ids.items() if n > 1])
    print("lesson counts:", dict(Counter(c["lesson"] for c in cards)))
    print("bad lesson field:", [c["id"] for c in cards if c["lesson"] not in LESSONS])
    fronts = Counter(c["front"].strip().lower() for c in cards)
    print("exact duplicate fronts:", [f for f, n in fronts.items() if n > 1])
    backs = Counter(c["back"].strip().lower() for c in cards)
    print("exact duplicate backs:", [f[:60] for f, n in backs.items() if n > 1])
    near = []
    for i, a in enumerate(cards):
        for b in cards[i + 1 :]:
            r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
            if r >= 0.85:
                near.append((a["id"], b["id"], round(r, 2), a["front"], b["front"]))
    print("near-duplicate fronts (ratio >= 0.85):", near)
    miss = []
    for c in cards:
        nums = set(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", c["back"] + " " + c["front"]))
        for n in sorted(nums):
            if n in ("0", "1", "2", "3", "4", "5"):
                continue
            if n not in texts[c["lesson"]].replace(",", ""):
                miss.append((c["id"], n))
    print("numbers (>5) not literal in own lesson:", miss)
    pat = re.compile(r"\b(Proposition|Remark|Theorem|Definition|Corollary|Example|Lemma|Problem|Assumption)s?\s+([A-Z]?\d+(?:\.\d+)?)")
    unresolved = []
    for c in cards:
        for kind, num in pat.findall(c["back"] + " " + c["front"]):
            if f"{kind} {num}" not in texts[c["lesson"]]:
                unresolved.append((c["id"], f"{kind} {num}"))
    print("cross-references not found in own lesson:", unresolved)


if __name__ == "__main__":
    main()
