"""Exact-duplicate, number-presence and id checks for E3 cards.json (verifier E3-f round 6)."""
import json, re, sys
from collections import Counter
cards = json.load(open(sys.argv[1], encoding="utf-8"))
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s.lower())).strip()
print("cards", len(cards))
print("duplicate ids", [k for k, v in Counter(c["id"] for c in cards).items() if v > 1])
print("duplicate normalised fronts", [k for k, v in Counter(norm(c["front"]) for c in cards).items() if v > 1])
print("duplicate normalised backs", [k for k, v in Counter(norm(c["back"]) for c in cards).items() if v > 1])
texts = {L: open(f"ledgers/E3/scripts/E3-f-r6/text/{L}.txt", encoding="utf-8").read() + open(f"course/modules/E/E3/{L}.html", encoding="utf-8").read()
         for L in ("L01", "L02", "L03", "L04")}
miss = []
for c in cards:
    if c["lesson"] not in texts:
        continue
    s = re.sub(r"E3-c\d+", "", c["front"] + " " + c["back"])
    s = re.sub(r"\b(Definition|Proposition|Lemma|Theorem|Remark|Problem|Example|Lab|Part|Section|Assumption|A|F|R|M|E|P)\s?\d+(\.\d+)?", "", s)
    for n in re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?", s):
        if n not in ("0", "1", "2", "3", "4", "5", "6", "10") and n not in texts[c["lesson"]]:
            miss.append((c["id"], n))
print("numeric tokens absent from own lesson:", miss)
