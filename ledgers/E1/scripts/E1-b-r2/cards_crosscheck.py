"""For every slice card (L04-L06): (a) each cited label (Definition/Proposition/Lemma/Theorem/Corollary/Remark/
Example/Assumption/Problem/Lab/Section) and (b) each number token must appear in the card's lesson page (visible text,
code and expected blocks included). Prints every miss for manual reading. Also reports exact duplicate fronts over all cards."""
import json
import re
import sys

ROOT = sys.argv[1]
cards = json.load(open(f"{ROOT}/course/modules/E/E1/cards.json", encoding="utf-8"))
pages = {}
for L in ("L04", "L05", "L06"):
    raw = open(f"{ROOT}/course/modules/E/E1/{L}.html", encoding="utf-8").read()
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = re.sub(r"&[a-z]+;", " ", txt)
    pages[L] = " ".join(txt.split())
LABEL = re.compile(r"(Definition|Proposition|Lemma|Theorem|Corollary|Remark|Example|Assumption|Problem|Lab|Section|§)\s?([0-9]+(?:\.[0-9]+)?|[A-Z][0-9]?|M)?")
NUM = re.compile(r"(?<![A-Za-z_])-?\d+(?:\.\d+)?")
misses = []
for card in cards:
    if card["lesson"] not in pages:
        continue
    page = pages[card["lesson"]]
    body = card["front"] + " " + card["back"] + " " + card.get("basis", "")
    for m in LABEL.finditer(body):
        lab = m.group(0).strip()
        if m.group(2) is None and m.group(1) in ("Assumption", "Lab"):
            key = m.group(1)
        else:
            key = lab
        if key not in page and key.rstrip() not in page:
            misses.append((card["id"], "label", key))
    for m in NUM.finditer(body):
        tok = m.group(0)
        if tok.lstrip("-") in ("0", "1", "2", "3"):
            continue
        if tok not in page and tok.lstrip("-") not in page:
            misses.append((card["id"], "number", tok))
for x in misses:
    print(*x)
print("misses", len(misses))
fronts = {}
for card in cards:
    k = re.sub(r"\W+", " ", card["front"].lower()).strip()
    fronts.setdefault(k, []).append(card["id"])
print("duplicate fronts", [v for v in fronts.values() if len(v) > 1])
