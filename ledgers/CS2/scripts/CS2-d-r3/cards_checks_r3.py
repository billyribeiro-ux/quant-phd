"""Verifier round 3 (CS2-d): card-level checks run against the checkout.

Usage: python -I cards_checks_r3.py <checkout>
Prints: ungraded cards that cite a lab, cards with no grade field, the number of cards, numbers in each back
that are absent from the cited lesson page (regex artifacts excluded by hand), and the card-level arithmetic of
CS2-c151 for L = floor(log2 n), epsilon = 1/20.
"""

import html
import json
import math
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
print("ungraded with lab citation:", [c["id"] for c in cards if "grade" not in c and "Lab" in c["back"]])
print("cards with no grade field:", len([c for c in cards if "grade" not in c]))
for c in cards:
    page = (root / f"course/modules/CS/CS2/{c['lesson']}.html").read_text(encoding="utf-8")
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page)))
    for num in set(re.findall(r"\d+\.\d+e-\d+|\d+\.\d{3,}|\b\d{3,}\b", c["back"])):
        if num not in text:
            print("number not in lesson:", c["id"], num)
L = 12
print("CS2-c151 closed form at n=5000, eps=1/20:", (L + 1) * (L + 2) * (L + 3) / (3 / 20) + (L + 1))
L = 29
print("CS2-c151 closed form at n=10^9, eps=1/20:", (L + 1) * (L + 2) * (L + 3) / (3 / 20) + (L + 1))
print("ratios:", round(7.286e-15 / 9.258e-16, 3), round(1.418e-2 / 8.852e-11, 0), round(1.000 / 7.449e-8, 0))
