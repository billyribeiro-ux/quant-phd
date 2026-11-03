"""FC1 cards scan (verifier r4): parse cards.json, check ids and fronts for duplicates, grades, and that every
number and every numbered reference (Proposition/Assumption/Remark/Definition/Lab/misconception) on a card appears in its lesson."""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c/course/modules/FC/FC1")
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
print("grades:", Counter(c.get("grade") for c in cards))
print("lessons:", Counter(c["lesson"] for c in cards))
print("keys:", Counter(tuple(sorted(c.keys())) for c in cards))


def lesson_text(name: str) -> str:
    raw = (ROOT / name).read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


texts = {}
problems = []
for c in cards:
    lt = texts.setdefault(c["lesson"], lesson_text(f"{c['lesson']}.html"))
    blob = " ".join(str(c.get(k, "")) for k in ("front", "back", "basis"))
    for num in re.findall(r"\d+(?:\.\d+)?", blob):
        if num not in lt:
            problems.append((c["id"], "number", num))
    for ref in re.findall(r"(Proposition|Assumption|Remark|Definition|Lemma|Theorem|Lab|misconception|Example|Corollary) ?([0-9A-Za-z.]+)?", blob):
        token = " ".join(x for x in ref if x)
        if token and token not in lt:
            problems.append((c["id"], "ref", token))
print("card-to-lesson problems:", len(problems))
for p in problems:
    print("  ", p)
