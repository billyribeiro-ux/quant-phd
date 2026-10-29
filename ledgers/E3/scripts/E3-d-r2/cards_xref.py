"""Cross-reference scan of cards.json against the lesson text (round 2, E3 slice d).

For each card, every 'Proposition/Remark/Theorem/Definition/Corollary/Example/Lemma/Problem/Assumption N' reference must
occur in the card's own lesson, and every 'section N, <ordinal> misconception' must match a list item of section N.
Also prints the number tokens of each card that do not occur in its lesson, and near-duplicate fronts.
Usage (from the checkout): .venv/bin/python ledgers/E3/scripts/E3-d-r2/cards_xref.py
"""

from __future__ import annotations

import difflib
import html
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "course" / "modules" / "E" / "E3"
ORD = {"first": 1, "second": 2, "third": 3}


def main() -> None:
    cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))
    texts = {}
    for lesson in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
        raw = (BASE / f"{lesson}.html").read_text(encoding="utf-8")
        texts[lesson] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    pattern = re.compile(r"\b(Proposition|Remark|Theorem|Definition|Corollary|Example|Lemma|Problem|Assumption)s?\s+([A-Z]?\d+(?:\.\d+)?)")
    unresolved, refs = [], 0
    for c in cards:
        for kind, num in pattern.findall(c["back"] + " " + c["front"]):
            refs += 1
            if re.search(kind + r"\s+" + re.escape(num) + r"\b", texts[c["lesson"]]) is None:
                unresolved.append((c["id"], kind, num))
        m = re.search(r"section (\d), (first|second|third) misconception", c["back"])
        if m:
            section, ordinal = int(m.group(1)), ORD[m.group(2)]
            raw = (BASE / f"{c['lesson']}.html").read_text(encoding="utf-8")
            block = re.search(rf'<h2 id="s{section}"><span class="section-number">{section}</span>[^<]*</h2>\s*<ol>(.*?)</ol>', raw, flags=re.S)
            items = re.findall(r'<li class="misconception">', block.group(1)) if block else []
            if len(items) < ordinal:
                unresolved.append((c["id"], "misconception", f"section {section} item {ordinal}"))
    print("references checked:", refs, "unresolved:", unresolved)
    fronts = [c["front"] for c in cards]
    dups = [
        (cards[i]["id"], cards[j]["id"], round(difflib.SequenceMatcher(None, fronts[i], fronts[j]).ratio(), 2))
        for i in range(len(cards)) for j in range(i + 1, len(cards))
        if difflib.SequenceMatcher(None, fronts[i], fronts[j]).ratio() > 0.85
    ]
    print("near-duplicate fronts:", dups)


if __name__ == "__main__":
    main()
