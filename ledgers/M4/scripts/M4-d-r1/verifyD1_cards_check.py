"""Verifier round-1 card checks for course/modules/M/M4/cards.json (all 212 cards).

(1) Every numeric token on a card (front and back, excluding 0-3) occurs in the visible text of that card's own lesson.
(2) Every theorem-style reference on a card (Definition, Proposition, Example, Remark, Lemma, Theorem, Problem X, Assumption)
    occurs in its own lesson's visible text, with 'Problem X' matched as the lesson's 'X ·' heading form.
(3) Full pairwise scan for near-duplicate cards (difflib on fronts and on backs).
(4) Schema: fields, unique ids, lesson coverage, grade counts, a basis on every C card.
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_cards_check.py
"""

from __future__ import annotations

import difflib
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
COURSE = ROOT / "course/modules/M/M4"
CARDS = COURSE / "cards.json"


def visible_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.S)
    text = re.sub(r"<br\s*/?>|</p>|</li>|</h[1-6]>|</tr>|</pre>", "\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"[ \t]+", " ", html.unescape(text))


def main() -> int:
    cards = json.loads(CARDS.read_text(encoding="utf-8"))
    lessons = {f"L{n:02d}": visible_text(COURSE / f"L{n:02d}.html") for n in range(1, 11)}

    # (4) schema
    ids = [c["id"] for c in cards]
    print(f"cards {len(cards)}, unique ids {len(set(ids))}")
    print("lesson counts", dict(sorted(Counter(c["lesson"] for c in cards).items())))
    print("grade counts", dict(Counter(c["grade"] for c in cards)))
    print("C cards without basis", [c["id"] for c in cards if c["grade"] == "C" and not c.get("basis")])
    print("id gaps", sorted(set(f"M4-c{n:03d}" for n in range(1, 219)) - set(ids)))

    # (1) numbers
    misses = []
    for c in cards:
        text = lessons[c["lesson"]]
        for token in re.findall(r"\d[\d,]*\.?\d*(?:e-?\d+)?", c["front"] + " " + c["back"]):
            tok = token.rstrip(".,")
            if tok in {"0", "1", "2", "3"}:
                continue
            if tok not in text:
                misses.append((c["id"], tok))
    print("number tokens not found in own lesson:", misses)

    # (2) references
    pattern = re.compile(r"\b(Definition|Proposition|Example|Remark|Lemma|Theorem|Assumption)\s+(\d+(?:\.\d+)?)")
    problem = re.compile(r"\b(Problem)\s+([A-Z]\d+)\b")
    ref_misses = []
    for c in cards:
        text = lessons[c["lesson"]]
        body = c["front"] + " " + c["back"]
        for m in pattern.finditer(body):
            label = m.group(0)
            if label not in text:
                ref_misses.append((c["id"], label))
        for m in problem.finditer(body):
            tag = m.group(2)
            if f"{tag} ·" not in text:
                ref_misses.append((c["id"], m.group(0)))
    print("theorem-style references not found in own lesson:", ref_misses)

    # (3) duplicates
    def norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

    print("near-duplicate pairs (front ratio > 0.75 and back ratio > 0.8, or back ratio > 0.92):")
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            a, b = cards[i], cards[j]
            rf = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
            rb = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
            if (rf > 0.75 and rb > 0.8) or rb > 0.92:
                print(f"  {a['id']} {b['id']} front {rf:.2f} back {rb:.2f} | {a['front'][:50]} || {b['front'][:50]}")
    fronts = Counter(norm(c["front"]) for c in cards)
    print("exact duplicate fronts:", [k for k, v in fronts.items() if v > 1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
