"""Structural scan of cards.json against the six lesson dumps (verifier slice d, round 12). Standard library only."""
import collections
import html
import json
import re
import sys

ROOT = sys.argv[1]
cards = json.load(open(f"{ROOT}/course/modules/PC/PC3/cards.json", encoding="utf-8"))
texts = {}
for L in ("L01", "L02", "L03", "L04", "L05", "L06"):
    raw = open(f"{ROOT}/course/modules/PC/PC3/{L}.html", encoding="utf-8").read()
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    texts[L] = re.sub(r"\s+", " ", t)
allt = " ".join(texts.values())
allt_nospace = re.sub(r"(?<=\d) (?=\d{3}\b)", "", allt)  # 12 000 -> 12000

ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)) == len(ids))
nums = [int(re.search(r"(\d+)$", i).group(1)) for i in ids]
print("ids strictly increasing:", nums == sorted(nums) and len(set(nums)) == len(nums))
print("id gaps:", [n for n in range(1, max(nums) + 1) if n not in nums])
print("per lesson:", dict(collections.Counter(c["lesson"] for c in cards)))
fr = collections.Counter(c["front"] for c in cards)
bk = collections.Counter(c["back"] for c in cards)
print("duplicate fronts:", [k for k, v in fr.items() if v > 1])
print("duplicate backs:", [k for k, v in bk.items() if v > 1])
print("keys:", collections.Counter(tuple(sorted(c.keys())) for c in cards))
print("grade counts:", collections.Counter(c.get("grade") for c in cards))
print("cite non-empty:", sum(1 for c in cards if c["cite"]))
print("lesson field matches id prefix card count:", all(c["lesson"] in texts for c in cards))

# numeric tokens in front/back must appear in some lesson text (any lesson)
miss = []
for c in cards:
    for field in ("front", "back"):
        for tok in re.findall(r"\d+(?:\.\d+)?", c[field]):
            if len(tok) < 2 and tok not in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                continue
            if tok in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                continue
            if tok not in allt_nospace:
                miss.append((c["id"], field, tok))
print("numeric tokens (>=2 digits) absent from all lesson text:", len(miss))
for m in miss:
    print("  ", m)
