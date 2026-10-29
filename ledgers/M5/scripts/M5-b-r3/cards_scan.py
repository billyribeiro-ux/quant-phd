"""Scan M5 cards for lessons L05-L07: duplicates, lesson membership, and numbers absent from the lesson text."""
import json
import re
import sys
from collections import Counter

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M5/cards.json", encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("total cards", len(cards), "duplicate ids", [k for k, v in ids.items() if v > 1])
fronts = Counter(c["front"] for c in cards)
print("duplicate fronts", [k[:60] for k, v in fronts.items() if v > 1])
text = {}
for L in ("L05", "L06", "L07"):
    text[L] = open(f"{root}/course/modules/M/M5/{L.lower()}.html", encoding="utf-8").read()
    text[L] = re.sub(r"<[^>]+>", " ", text[L])
    text[L] = text[L].replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
mine = [c for c in cards if c["lesson"] in ("L05", "L06", "L07")]
print("cards for L05-L07:", len(mine), "first", mine[0]["id"], "last", mine[-1]["id"])
for c in mine:
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["back"]))
    body = text[c["lesson"]]
    missing = [n for n in nums if n not in body and n not in ("0",)]
    if missing:
        print("NUMBER NOT IN LESSON", c["id"], c["lesson"], missing)
