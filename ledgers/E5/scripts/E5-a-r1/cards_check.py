"""Mechanical checks for E5 L01-L03 cards: every cited label exists in its lesson and every card number occurs in its lesson."""

import html
import json
import pathlib
import re

ROOT = pathlib.Path(".")
E5 = ROOT / "course/modules/E/E5"
cards = json.loads((E5 / "cards.json").read_text(encoding="utf-8"))
lessons = {}
for lid in ("L01", "L02", "L03"):
    raw = (E5 / f"{lid}.html").read_text(encoding="utf-8")
    lessons[lid] = raw
    lessons[lid + "_text"] = html.unescape(re.sub(r"<[^>]+>", " ", raw))

label_re = re.compile(r"(Definition|Proposition|Theorem|Remark|Assumption|Example|Derivation|Problem|Lemma|Corollary|Misconception)\s+([A-Z]?\d+(?:\.\d+)?)")
num_re = re.compile(r"(?<![A-Za-z_(\d.])(\d+\.\d+|\d+/\d+|\d{2,})(?![\d])")

for card in cards:
    lid = card["lesson"]
    if lid not in ("L01", "L02", "L03"):
        continue
    text = lessons[lid + "_text"]
    raw = lessons[lid]
    for field in ("basis",):
        for kind, num in label_re.findall(card.get(field) or ""):
            key = f"{kind} {num}"
            present = key in text
            line = None
            for i, l in enumerate(raw.splitlines(), 1):
                if key in html.unescape(re.sub(r"<[^>]+>", " ", l)):
                    line = i
                    break
            print(f"{card['id']} basis {key!r}: present={present} first_line={line}")
    missing = []
    for n in set(num_re.findall(card["back"])):
        if n not in text and n not in raw:
            missing.append(n)
    if missing:
        print(f"{card['id']} numbers NOT in lesson: {sorted(missing)}")
