"""Card scan for E4 L04-L06 (pin 06994db). Checks: unique ids, unique fronts, lesson membership, and that every
numbered reference a card makes (Lemma/Proposition/Theorem/Definition/Remark/Example/Corollary/Assumption n.m,
'Problem X n', 'Lab 1, Part X', 'Lesson Ln') appears in the card's own lesson page.
Run: .venv/bin/python ledgers/E4/scripts/E4-b-r7/cards_scan.py  (from the checkout root)."""

import collections
import html
import json
import re

cards = json.load(open("course/modules/E/E4/cards.json", encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("cards", len(cards), "dup ids", [i for i, n in ids.items() if n > 1], "dup fronts", [f[:60] for f, n in fronts.items() if n > 1])
pages = {}
for L in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"):
    raw = open(f"course/modules/E/E4/{L}.html", encoding="utf-8").read()
    pages[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    pages[L] = re.sub(r"\s+", " ", pages[L])
pat = re.compile(r"(Lemma|Proposition|Theorem|Definition|Remark|Example|Corollary|Assumption|Problem|Derivation|Lab \d, Part|Lesson|Step) ([A-Z]?\d(?:\.\d+)?|Part [A-Z]|[A-Z][a-z]* \d)")
bad = []
for c in cards:
    if c["lesson"] not in pages:
        bad.append((c["id"], "lesson missing")); continue
    text = c["front"] + " " + c["back"]
    for m in pat.finditer(text):
        ref = m.group(0)
        if c["lesson"] in ("L04", "L05", "L06") or True:
            # numbered refs are checked against the card's own lesson; Lab/Part refs against the lesson's lab text
            if ref not in pages[c["lesson"]] and not re.search(re.escape(ref.split(" (")[0]), pages[c["lesson"]]):
                bad.append((c["id"], c["lesson"], ref))
for b in bad:
    print("UNMATCHED", b)
print("unmatched refs", len(bad))
print("per-lesson counts", dict(collections.Counter(c["lesson"] for c in cards)))
