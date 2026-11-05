"""Round 11 M4 slice a: every numeric token on a card back or front (L01-L04) must appear on its lesson page.

Fractions a/b must appear as a/b in the page text or as \\tfrac{a}{b} / \\frac{a}{b} in the page HTML.
Run from the checkout root: python3 -I ledgers/M4/scripts/M4-a-r11/card_numbers.py
"""

import html
import json
import pathlib
import re

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD11-M4-a/course/modules/M/M4")
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
pages = {}
missing = []
checked = 0
for c in cards:
    if c["lesson"] not in ("L01", "L02", "L03", "L04"):
        continue
    if c["lesson"] not in pages:
        raw = (ROOT / f"{c['lesson']}.html").read_text(encoding="utf-8")
        pages[c["lesson"]] = (raw, html.unescape(re.sub(r"<[^>]+>", " ", raw)))
    raw, text = pages[c["lesson"]]
    for field in ("front", "back"):
        for tok in re.findall(r"\d+(?:\.\d+)?(?:/\d+)?", c[field]):
            if len(tok.replace("/", "").replace(".", "")) < 2:
                continue
            checked += 1
            if "/" in tok:
                a, b = tok.split("/")
                ok = (f"{a}/{b}" in text) or (f"{{{a}}}{{{b}}}" in raw) or (f"{a}}}{{{b}" in raw) or (f"{a}/{b}" in raw)
            else:
                ok = tok in text or tok in raw
            if not ok:
                missing.append((c["id"], field, tok))
print("tokens checked:", checked)
print("missing:", missing)
