"""Scan SC1 cards: id order, duplicates, near-duplicate pairs, process words, horizon symbol T, unlisted lesson numbers.

Usage: python -I card_scan_r9.py <repo_root>
"""
import difflib
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("count", len(cards), "distinct", len(set(ids)))
nums = [int(i.split("-c")[1]) for i in ids]
print("sorted in file order:", nums == sorted(nums), "min", min(nums), "max", max(nums))
missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
print("missing numbers in 1..max:", missing)
fronts = {}
for c in cards:
    fronts.setdefault(c["front"], []).append(c["id"])
print("identical fronts:", [v for v in fronts.values() if len(v) > 1])
backs = {}
for c in cards:
    backs.setdefault(c["back"], []).append(c["id"])
print("identical backs:", [v for v in backs.values() if len(v) > 1])
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = cards[i]["front"] + " " + cards[i]["back"]
        b = cards[j]["front"] + " " + cards[j]["back"]
        r = difflib.SequenceMatcher(None, a, b).ratio()
        if r >= 0.6:
            pairs.append((round(r, 3), cards[i]["id"], cards[j]["id"]))
print("pairs ratio>=0.6:", sorted(pairs, reverse=True))
banned = re.compile(r"\b(builder|verifier|verification|round|fixer|ledger|reviewer|agent|session|sub-?agent|r\d+)\b", re.I)
hits = [(c["id"], m.group(0)) for c in cards for m in banned.finditer(c["front"] + " " + c["back"] + " " + str(c.get("basis", "")))]
print("process-word hits:", hits)
tsym = [c["id"] for c in cards if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", c["front"] + c["back"])]
print("bare T symbol in card text:", tsym)
