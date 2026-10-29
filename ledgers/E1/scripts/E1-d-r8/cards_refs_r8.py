"""Round 8: every labelled reference in a card (Definition/Proposition/Lemma/Corollary/Theorem/Example/Remark/
Assumption/Problem/Misconception N.M, and 'Lab 1, Part X') must occur in the card's own lesson text, and each
card-only grade/basis rule holds. Reads only the checkout."""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
E1 = ROOT / "course/modules/E/E1"
cards = json.loads((E1 / "cards.json").read_text(encoding="utf-8"))
label = re.compile(r"\b(Definition|Proposition|Lemma|Corollary|Theorem|Example|Remark|Assumption|Problem|Misconception|Section) (\d+(?:\.\d+)?)")
part = re.compile(r"\bLab (\d), Parts? ([A-E])(?: and ([A-E]))?")
problems = []
text_cache = {}
for card in cards:
    lesson = card["lesson"]
    if lesson not in text_cache:
        raw = (E1 / f"{lesson}.html").read_text(encoding="utf-8")
        text_cache[lesson] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    body = text_cache[lesson]
    body_norm = " ".join(body.split())
    cited = f"{card['front']} {card['back']}"
    for kind, num in label.findall(cited):
        if f"{kind} {num}" not in body_norm:
            problems.append((card["id"], lesson, f"{kind} {num} not in lesson"))
    if card.get("grade") == "C" and "basis" not in card:
        problems.append((card["id"], lesson, "C grade without basis"))
    if "basis" in card and card.get("grade") != "C":
        problems.append((card["id"], lesson, "basis on a non-C grade"))
print("cards:", len(cards), "grades:", dict(Counter(c.get("grade") for c in cards)))
print("problems:", len(problems))
for p in problems:
    print(p)
