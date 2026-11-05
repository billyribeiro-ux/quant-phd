"""Scans all of cards.json for duplicate ids, fronts and backs, checks that each L01-L03 card's numbers appear in its
lesson text (tags stripped, entities decoded), and lists card keys and grade/basis consistency. Usage: python -I cards_scan_r12.py <checkout>"""
import html
import json
import re
import sys
from collections import Counter

root = sys.argv[1]
cards = json.load(open(root + "/course/modules/SC/SC1/cards.json", encoding="utf-8"))
print("cards:", len(cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
fronts = Counter(c["front"].strip() for c in cards)
backs = Counter(c["back"].strip() for c in cards)
print("duplicate fronts:", [k[:60] for k, v in fronts.items() if v > 1])
print("duplicate backs:", [k[:60] for k, v in backs.items() if v > 1])
print("ids by lesson:", sorted(Counter(c["lesson"] for c in cards).items()))
print("bad id prefix:", [c["id"] for c in cards if not re.match(r"SC1-c\d{3}$", c["id"])])
lessons = {}
for n in ("L01", "L02", "L03"):
    t = open(root + f"/course/modules/SC/SC1/{n}.html", encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<pre class=\"expected\".*?</pre>", "", t, flags=re.S)  # numbers in printed output checked separately
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\s+", " ", t)
    lessons[n] = t
missing = []
for c in cards:
    if c["lesson"] not in lessons:
        continue
    text = c["front"] + " " + c["back"]
    nums = set(re.findall(r"\d+(?:\.\d+)?", text))
    for x in sorted(nums):
        if x not in lessons[c["lesson"]] and x not in ("0", "1", "2"):
            missing.append((c["id"], x))
print("card numbers (>2) not found verbatim in their lesson:", missing)
print("grade values:", Counter(c.get("grade") for c in cards))
print("T cards without basis:", [c["id"] for c in cards if c.get("grade") == "T" and not c.get("basis")])
print("C cards whose basis is not a lab:", [c["id"] for c in cards if c.get("grade") == "C" and "Lab" not in (c.get("basis") or "")])
