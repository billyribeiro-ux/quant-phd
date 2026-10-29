"""Verifier round 3 (E2-d): cards.json duplicate scan, and every number on a card must occur in its lesson page.

Usage (repository root): .venv/bin/python -I ledgers/E2/scripts/E2-d-r3/card_checks_r3.py
"""

from __future__ import annotations

import difflib
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOD = ROOT / "course/modules/E/E2"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards), "ids unique:", len({c["id"] for c in cards}) == len(cards))
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()  # noqa: E731
fronts = Counter(norm(c["front"]) for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
backs = Counter(norm(c["back"]) for c in cards)
print("duplicate backs:", [b[:60] for b, n in backs.items() if n > 1])
near = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        r = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        if r > 0.85:
            near.append((a["id"], b["id"], round(r, 2)))
print("near-duplicate fronts (ratio>0.85):", near)
lessons = {}
for c in cards:
    if c["lesson"] not in lessons:
        text = (MOD / f"{c['lesson']}.html").read_text(encoding="utf-8")
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
        lessons[c["lesson"]] = re.sub(r"\s+", " ", text)
missing = []
for c in cards:
    for field in ("front", "back"):
        for num in re.findall(r"\d[\d,\.]*\d|\d", c[field]):
            token = num.rstrip(".,")
            if token not in lessons[c["lesson"]]:
                missing.append((c["id"], field, token))
print("card numbers not found verbatim in their lesson:", missing)
for c in cards[::10]:
    print(c["id"], c["lesson"], "|", c["front"][:110])
