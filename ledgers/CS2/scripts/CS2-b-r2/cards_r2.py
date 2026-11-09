"""CS2 slice b, round 2: cards L05-L08 checked against the current lesson text.

1. every number token in a card (front or back) must occur in its lesson's visible text or lab output
   (tags stripped, entities unescaped, the lab code block excluded so a card cannot cite code alone);
2. the card's lesson field must be L05..L08 for the slice, and every card of the slice must carry a grade;
3. near-duplicate fronts (difflib ratio >= 0.75) among all cards of the unit, and exact duplicate backs;
4. C-graded cards must carry a basis; T-graded cards must not name a lab as their basis.
Usage: python -I -W error cards_r2.py <checkout-root>
"""

from __future__ import annotations

import difflib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
UNIT_DIR = ROOT / "course/modules/CS/CS2"
SLICE = {"L05", "L06", "L07", "L08"}
NUM_RE = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")
CODE_RE = re.compile(r"<pre><code.*?</code></pre>", re.S)
TAG_RE = re.compile(r"<[^>]+>")


def visible(page: str) -> str:
    body = CODE_RE.sub(" ", page)
    body = TAG_RE.sub(" ", body)
    body = html.unescape(body)
    body = body.replace("\\(", " ").replace("\\)", " ")
    return re.sub(r"\s+", " ", body)


def lesson_text(page: str) -> str:
    return visible(page) + " " + " ".join(re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S))


def main() -> int:
    cards = json.loads((UNIT_DIR / "cards.json").read_text(encoding="utf-8"))
    texts = {p: lesson_text((UNIT_DIR / f"{p}.html").read_text(encoding="utf-8")) for p in SLICE | {"L01", "L02", "L03", "L04", "L09", "L10", "L11"}}
    bad = 0
    slice_cards = [c for c in cards if c["lesson"] in SLICE]
    print(f"slice cards: {len(slice_cards)} (per lesson: { {p: sum(1 for c in slice_cards if c['lesson'] == p) for p in sorted(SLICE)} })")
    for c in slice_cards:
        text = texts[c["lesson"]]
        for field in ("front", "back"):
            for tok in NUM_RE.findall(c[field]):
                if tok not in text:
                    # allow a number that appears only in the lab output of another part of the same page
                    print(f"MISSING {c['id']} {c['lesson']} {field} number {tok!r}: {c['front'][:80]}")
                    bad += 1
        if c["grade"] == "C" and not c.get("basis"):
            print(f"C-WITHOUT-BASIS {c['id']}")
            bad += 1
        if c["grade"] == "T" and c.get("basis", "").startswith("Lab"):
            print(f"T-WITH-LAB-BASIS {c['id']}")
            bad += 1
        if c["grade"] not in {"T", "C"}:
            print(f"OTHER-GRADE {c['id']} {c['grade']}")
    # duplicates across the whole unit deck
    pairs = []
    for i, a in enumerate(cards):
        for b in cards[i + 1 :]:
            r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
            if r >= 0.75:
                pairs.append((r, a["id"], b["id"], a["front"][:70], b["front"][:70]))
    for r, x, y, fx, fy in sorted(pairs, reverse=True):
        print(f"NEAR-DUP-FRONT {r:.2f} {x} {y} | {fx} | {fy}")
    backs: dict[str, list[str]] = {}
    for c in cards:
        backs.setdefault(c["back"], []).append(c["id"])
    print("exact duplicate backs:", [v for v in backs.values() if len(v) > 1])
    print(f"near-dup front pairs (>=0.75) in unit: {len(pairs)}")
    print("SLICE_CARD_PROBLEMS", bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
