"""Round-4 cards check for L03 and L04 (LX1-b). Reads cards.json and the two lesson pages; does not import twins.
Usage: python -I cards_l03_l04_r4.py <checkout>"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/LX/LX1/cards.json").read_text(encoding="utf-8"))
pages = {}
for lesson, name in (("L03", "L03.html"), ("L04", "L04.html")):
    raw = (root / "course/modules/LX/LX1" / name).read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    pages[lesson] = text
sel = [c for c in cards if c["lesson"] in pages]
print("cards in L03/L04:", len(sel), "of", len(cards), "total")
fronts = Counter(c["front"] for c in cards)
print("duplicate fronts across all cards:", [f for f, n in fronts.items() if n > 1])
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [i for i, n in ids.items() if n > 1])
bad = 0
for c in sel:
    page = pages[c["lesson"]]
    for field in ("front", "back"):
        for num in re.findall(r"\d[\d,.]*\d|\d{3,}", c[field]):
            n = num.rstrip(".,")
            if len(n.replace(",", "").replace(".", "")) < 3:
                continue
            if n not in page and n.replace(",", "") not in page.replace(",", ""):
                bad += 1
                print("NUMBER NOT IN LESSON:", c["id"], field, n)
    if c.get("basis") and "misconception" in c["basis"]:
        m = re.search(r"misconception (\d)", c["basis"])
        print(c["id"], "cites", m.group(0), "- section 6 has misconceptions:", "Misconceptions" in page)
print("unmatched numbers:", bad)
